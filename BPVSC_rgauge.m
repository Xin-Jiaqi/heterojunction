% We apply shift current formula to evaluate it
% Here the equation is taken from PRB 97, 245143 (2018) (Eq. 8 - 13)
% Note that we assume the Eq. 12 summation is complete here, as long as
% the wannier functions form a nearly complete set (?).

% We use 1/omega_nm = omega_nm/(omega_nm^2+eta^2)

clear;

%% constants
hbar = 1.0545718e-34;
electron_charge = 1.60217662e-19;
ev2omega = 241.8e12 * 2*pi;

%% Read Files
[R,HR,wtR,wc,nw,nR] = getwanhr('wannier90');

[alatt, blatt] = readlattice("POSCAR");
Vlatt = det(alatt) * 1e-30;

%% Initial
nkx = 70;
nky = 70;
nkz = 1;
ksi = 0.02; % dissipation term, hbar/tau, in eV;
hv = linspace(1.0, 3.0, 100); % BPV frequency;
nocc = 94;%number of occupied band
a = 2;
b = 2;
c = 2; % dion, sigma^a_bc
thickness = 8.7460; % in Angstrom%%%%%%%

%% Main
kx = linspace(-0.5, 0.5, nkx+1);
ky = linspace(-0.5, 0.5, nky+1);
kz = linspace(0,    0,   nkz+1);
[kx, ky, kz] = meshgrid(kx(1:nkx), ky(1:nky), kz(1:nkz));
kx = permute(kx,[2,1,3]);
ky = permute(ky,[2,1,3]);
kz = permute(kz,[2,1,3]);
bkx = zeros(nkx,nky,nkz);
bky = zeros(nkx,nky,nkz);
bkz = zeros(nkx,nky,nkz);
nkpts = nkx*nky*nkz;
kweight = 1/nkpts;

v = zeros(nw, nw, 3, nkx, nky);
f = zeros(1, nw);
f(1:nocc) = 1;

bpv = zeros(1, length(hv));
bpv_per_k = zeros(nkx, nky, nkz, length(hv));

Rnma = zeros(nkx,nky,nkz,nw,nw);
% R_nm^a only good for linearly polarized light (b = c)
% Rnmac = (Inmabb+Inmabb)/rnmb

%parpool(4)
for ikx = 1:nkx
  for iky = 1:nky
    for ikz = 1:nkz
      kpt = [kx(ikx,iky,ikz), ky(ikx,iky,ikz), kz(ikx,iky,ikz)];
      bkpt = kpt*blatt;
      bkx(ikx,iky,ikz) = bkpt(1);
      bky(ikx,iky,ikz) = bkpt(2);
      bkz(ikx,iky,ikz) = bkpt(3);
      % build Hamiltonian
      [Hk,dHdkx,dHdky,dHdkz,d2Hdk2] = buildHk(R,HR,wtR,wc,nw,nR,kpt,alatt);
      
      % diagonalize
      [V, D] = eig(Hk);
      [d,ind] = sort(diag(D));
      energy = real(d);
      wavefunct = V(:,ind);
      % calculate vmn,wmnab,rmn,omega_ab,rmndk,Imnabc
      [vmn,wmnab] = calc_vmn(wavefunct, dHdkx, dHdky, dHdkz, d2Hdk2,nw);
      [rmn, omn, zmn] = calc_rmn(vmn,energy,nw,ksi);
      rmndk = calc_rmndk(vmn,omn,wmnab,nw,ksi);
      Imnabc = calc_I(rmn,rmndk,nw);
      
      % calcuate the contribution to bpv from this k point
      [this_k,rnma_k] ...
          = bpv_bandsum(omn,Imnabc,rmn,f,nw,hv,ksi,a,b,c);
      Rnma(ikx,iky,ikz,:,:) = rnma_k;
      bpv_per_k(ikx, iky, ikz, :) = real(1i*this_k);
      bpv = bpv + real(1i*kweight * this_k);

      v(:, :, :, ikx, iky) = vmn(:, :, :);
    end
  end
end
%delete(gcp('nocreate'))
%% BPV

bpv = bpv / Vlatt;%%%%%%%
bpv = bpv * pi * electron_charge^3 / hbar^2;
% length from A to m
bpv = bpv * 1e-30;
% omega in eV to Hz
bpv = bpv / ev2omega;

% a length_z factor for 2D
bpv = bpv * alatt(3,3) / thickness;%%%%%%

% from A/V^2 to mu/V^2
bpv = -bpv * 1e6 * 2;

% save data-sc bpv bpv_per_k bkx bky bkz hv Rnma

% load data

f1 = plot(hv,real(bpv),'--','LineWidth',1.5,'Color',[0.85 0 0]);

fid = fopen('shift-current.txt','w');          
fprintf(fid,'%6.2f\n',hv,real(bpv));         
fclose(fid)

%% Functions
function [bpv_on_k,Rnma] = bpv_bandsum(omn,Imnabc,rmn,f,nw,hv,ksi,a,b,c)
bpv_on_k = zeros(1, length(hv));
Rnma = zeros(nw,nw);
for m = 1:nw
for n = 1:nw
    fac = (Imnabc(m,n,a,b,c)+ Imnabc(m,n,a,c,b));
    Rnma(n,m) = fac/abs(rmn(n,m,b))^2;
    fac1 = (f(n)-f(m)) * fac;

    for iomega = 1:length(hv)
        omega = hv(iomega);
        fac2 = df(omn(m,n)-omega,ksi);
        bpv_on_k(iomega) = bpv_on_k(iomega) + fac1 * fac2 / 2;
    end

end
end

end

function deltafunct = df(x,eps0)
deltafunct = eps0/(x^2+eps0^2)/pi;
%deltafunct = 1/eps0/sqrt(pi)*exp(-x^2/eps0^2);
end

function [vmn,wmnab] = calc_vmn(wavefunct, dHdkx, dHdky, dHdkz, d2Hdk2,nw)
vmn = zeros(nw, nw, 3);
wmnab = zeros(nw,nw,3,3);

vmn(:,:,1) = wavefunct(:,:)' * dHdkx * wavefunct(:,:);
vmn(:,:,2) = wavefunct(:,:)' * dHdky * wavefunct(:,:);
vmn(:,:,3) = wavefunct(:,:)' * dHdkz * wavefunct(:,:);
wmnab(:,:,1,1) = wavefunct(:,:)' * d2Hdk2(:,:,1) * wavefunct(:,:);
wmnab(:,:,1,2) = wavefunct(:,:)' * d2Hdk2(:,:,6) * wavefunct(:,:);
wmnab(:,:,1,3) = wavefunct(:,:)' * d2Hdk2(:,:,5) * wavefunct(:,:);
wmnab(:,:,2,2) = wavefunct(:,:)' * d2Hdk2(:,:,2) * wavefunct(:,:);
wmnab(:,:,2,3) = wavefunct(:,:)' * d2Hdk2(:,:,4) * wavefunct(:,:);
wmnab(:,:,3,3) = wavefunct(:,:)' * d2Hdk2(:,:,3) * wavefunct(:,:);
wmnab(:,:,2,1) = wmnab(:,:,1,2);
wmnab(:,:,3,1) = wmnab(:,:,1,3);
wmnab(:,:,3,2) = wmnab(:,:,2,3);
end

function [rmn, omn, zta] = calc_rmn(vmn,energy,nw,eta)
rmn = zeros(nw,nw,3);
omn = zeros(nw,nw);
zta = zeros(nw,nw,3);
zfac = 4.7e-8;
for i = 1:nw
    for j = 1:nw
        omn(i,j) = energy(i)-energy(j);
        if i ~= j
            rmn(i,j,:) = -1i*vmn(i,j,:)*omn(i,j)/(omn(i,j)^2+eta^2);
            zta(i,j,1) = zfac * omn(i,j) * vmn(j,i,1)*vmn(i,j,1);
            zta(i,j,2) = zfac * omn(i,j) * vmn(j,i,2)*vmn(i,j,2);
            zta(i,j,3) = zfac * omn(i,j) * vmn(j,i,3)*vmn(i,j,3);
        end
    end
end
end

function rmndk = calc_rmndk(vmn,omn,wmnab,nw,eta)
rmndk = zeros(nw,nw,3,3);  % (m,n,a,b) as r_mn^{a;b}
for a = 1:3
for b = 1:3
    if a==1&&b==1
        ind = 1;
    elseif a==1&&b==2
        ind = 6;
    elseif a==1&&b==3
        ind = 5;
    elseif a==2&&b==1
        ind = 6;
    elseif a==2&&b==2
        ind = 2;
    elseif a==2&&b==3
        ind = 4;
    elseif a==3&&b==1
        ind = 5;
    elseif a==3&&b==2
        ind = 4;
    elseif a==3&&b==3
        ind = 3;
    end
for m = 1:nw
for n = 1:nw
    if m ~= n
    s = 0;
    for p = 1:nw
        if p ~= m && p ~= n
            s = s+vmn(n,p,a)*vmn(p,m,b)*omn(p,m)/(omn(p,m)^2+eta^2) ...
                -vmn(n,p,b)*vmn(p,m,a)*omn(n,p)/(omn(n,p)^2+eta^2);
        end
    end
    
    rmndk(n,m,a,b) = 1i*omn(n,m)/(omn(n,m)^2+eta^2) ...
        *((vmn(n,m,a)*(vmn(n,n,b)-vmn(m,m,b)) ...
        +vmn(n,m,b)*(vmn(n,n,a)-vmn(m,m,a)))*omn(n,m)/(omn(n,m)^2+eta^2)...
        -wmnab(n,m,ind)+s);
    end
end
end
end
end
         
end

function Imnabc = calc_I(rmn,rmndk,nw)
Imnabc = zeros(nw,nw,3,3,3); % r_mn^b * r_nm^c;a
for a = 1:3
for b = 1:3
for c = 1:3
    Imnabc(:,:,a,b,c) = rmn(:,:,b).*rmndk(:,:,c,a).';
end
end
end

end

function [alatt, blatt] = readlattice(filename)
file = fopen(filename);
fgetl(file); 
scale = sscanf( fgetl(file), "%f" );
alatt = zeros(3,3);
for i = 1:3
  alatt(i,:) = sscanf( fgetl(file), "%f" );
end
alatt = scale * alatt;
V = det(alatt);

blatt = zeros(3,3);
blatt(1,:) = 2*pi*cross(alatt(2,:),alatt(3,:))/V;
blatt(2,:) = 2*pi*cross(alatt(3,:),alatt(1,:))/V;
blatt(3,:) = 2*pi*cross(alatt(1,:),alatt(2,:))/V;

end


function [R,HR,wtR,wc,nw,nR] = getwanhr(seedname)
file = fopen(join([seedname, '_hr.dat']), 'r');
fgetl(file);
line = fgetl(file);
nw = sscanf(line, "%d");
line = fgetl(file);
nR = sscanf(line, "%d");

Rdeg = [];
Rlines = ceil(nR/15); % per the format of wannier90_hr, 15 entries per line
for iline = 1:Rlines
	line = fgetl(file);
  Rdeg = [Rdeg, sscanf(line, "%d")'];
end
wtR = 1./Rdeg;

C = textscan(file,'%d %d %d %d %d %n %n');
R1 = C{1};
R2 = C{2};
R3 = C{3};
Hr1 = C{6};
Hr2 = C{7};
% nlines = length(R1);
% nw = sqrt(nlines/nR);
fclose(file);
R = zeros(nR,3);
HR = zeros(nR,nw,nw);
for i = 1:nR
    R(i,1) = R1((i-1)*nw^2+1);
    R(i,2) = R2((i-1)*nw^2+1);
    R(i,3) = R3((i-1)*nw^2+1);
    for j = 1:nw
        for k = 1:nw
            HR(i,j,k) = Hr1((i-1)*nw^2+(k-1)*nw+j) ...
                +1i*Hr2((i-1)*nw^2+(k-1)*nw+j);
        end
    end
    
end
% symmetrize HR
for i = 1:nR
  HR(i,:,:) = 0.5*( HR(i,:,:) + conj(permute(HR(nR+1-i,:,:), [1,3,2])) );
end
% wc = zeros(nw,3);

fileID = fopen(join([seedname,'-wcenter.dat']),'r');
C = textscan(fileID,'%*s %f %f %f');
wc1 = C{1};
wc2 = C{2};
wc3 = C{3};
fclose(fileID);
wc = zeros(nw,3);
for i = 1:nw
    wc(i,1) = wc1(i);
    wc(i,2) = wc2(i);
    wc(i,3) = wc3(i);
end

end


function [Hk,dHdkx,dHdky,dHdkz,d2Hdk2] ...
        = buildHk(R,HR,wtR,wc,nw,nR,kpt,alatt)
% Note that here kpoint coordinate is in direct mode (in unit of reciprocal
% space
Hk = zeros(nw,nw);
dHdkx = zeros(nw,nw);
dHdky = zeros(nw,nw);
dHdkz = zeros(nw,nw);
d2Hdk2 = zeros(nw,nw,6); % 1: xx; 2: yy; 3: zz; 4: yz; 5: zx; 6: xy

for iR = 1:nR
    kdotR = 2*pi*R(iR,:)*kpt';
    
    for i = 1:nw
    for j = 1:nw
    wcdiff = wc(j,:)-wc(i,:);
    aR = R(iR,:)*alatt+wcdiff;
    Hk(i,j) = Hk(i,j) + wtR(iR) * HR(iR,i,j) * exp(1i*kdotR);
    dHdkx(i,j) = dHdkx(i,j) + 1i*wtR(iR)*aR(1)*HR(iR,i,j)*exp(1i*kdotR);
    dHdky(i,j) = dHdky(i,j) + 1i*wtR(iR)*aR(2)*HR(iR,i,j)*exp(1i*kdotR);
    dHdkz(i,j) = dHdkz(i,j) + 1i*wtR(iR)*aR(3)*HR(iR,i,j)*exp(1i*kdotR);
    d2Hdk2(i,j,1) = d2Hdk2(i,j,1)-wtR(iR)*aR(1)^2*HR(iR,i,j)*exp(1i*kdotR);
    d2Hdk2(i,j,2) = d2Hdk2(i,j,2)-wtR(iR)*aR(2)^2*HR(iR,i,j)*exp(1i*kdotR);
    d2Hdk2(i,j,3) = d2Hdk2(i,j,3)-wtR(iR)*aR(3)^2*HR(iR,i,j)*exp(1i*kdotR);
    d2Hdk2(i,j,4) = d2Hdk2(i,j,4)-wtR(iR)*aR(2)*aR(3)*HR(iR,i,j)*exp(1i*kdotR);
    d2Hdk2(i,j,5) = d2Hdk2(i,j,5)-wtR(iR)*aR(3)*aR(1)*HR(iR,i,j)*exp(1i*kdotR);
    d2Hdk2(i,j,6) = d2Hdk2(i,j,6)-wtR(iR)*aR(1)*aR(2)*HR(iR,i,j)*exp(1i*kdotR);
    end
    end
end

rdn = -6;
roundn = @(x,n) 10.^n .* round(x/10.^n);
Hk = roundn(Hk,rdn);
dHdkx = roundn(dHdkx,rdn);
dHdky = roundn(dHdky,rdn);
dHdkz = roundn(dHdkz,rdn);
d2Hdk2 = roundn(d2Hdk2,rdn);
end
