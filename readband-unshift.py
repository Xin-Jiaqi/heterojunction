#!/usr/bin/python
import os
from math  import *
from numpy import *
import sys

def distance(p1,p2):
        return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2+(p1[2]-p2[2])**2)

f = open(r'CONTCAR','r')
f.readline()
f.readline()
#read the lattice constant from the CONTCAR file and calculate the base vectors in the reciprocal space
a1 = f.readline().split()
a2 = f.readline().split()
a3 = f.readline().split()
a1 = [float(i) for i in a1]
a2 = [float(i) for i in a2]
a3 = [float(i) for i in a3]
#the base vectors in the reciprocal space
volume=abs(dot(a1,cross(a2,a3)))
b1=2*pi*cross(a2,a3)/volume
b2=2*pi*cross(a3,a1)/volume
b3=2*pi*cross(a1,a2)/volume

print "volume of unit cell:",volume

#read the specified path in the reciprocal space from the KPOINTS file
kpoint = open(r"KPOINTS",'r')
line = kpoint.readline()
line = kpoint.readline()
intersection = float(line)

#fermi=os.popen("grep E-fermi OUTCAR").readline().split()
#fermi=float(fermi[2])
fermi = 0
spin=os.popen("grep SPIN OUTCAR").readline().split()
spin=int(spin[2])
ElecNum=os.popen("grep NELECT OUTCAR").readline().split()
ElecNum=int(float(ElecNum[2]))

print "Fermi energy = ",fermi,"eV\nISPIN=",spin

f = open(r'EIGENVAL','r')
line = f.readline().split()
line = f.readline().split()
line = f.readline()
coord = f.readline()
system = f.readline()
line = f.readline().split()
ElecNum = int(line[0])
KpNum = int(line[1])
EigenNum = int(line[2])
val_idx = ElecNum/2-1
con_idx = val_idx+1
eigen = []
eigen_up = []
eigen_dn = []
for eigen_index in range(EigenNum):
	eigen.append([])
	eigen_up.append([])
	eigen_dn.append([])
kx = []
ky = []
kz = []
k_weight = []
for kp_index in range(KpNum):
	f.readline()
	line = f.readline().split()
	kx.append(float(line[0]))
	ky.append(float(line[1]))
	kz.append(float(line[2]))
	k_weight.append(float(line[3]))
	for eigen_index in range(EigenNum):
		line = f.readline().split()
		if spin == 1:
			eigen[eigen_index].append(float(line[1]))
		if spin == 2:
			eigen_up[eigen_index].append(float(line[1]))
			eigen_dn[eigen_index].append(float(line[2]))
f.close()

#tranfer the K points coordinates into cartesian format in the reciprocal space
for kp_index in range(KpNum):
        k = [float(kx[kp_index]),float(ky[kp_index]),float(kz[kp_index])]
        kx[kp_index] = k[0]*b1[0]+k[1]*b2[0]+k[2]*b3[0]
        ky[kp_index] = k[0]*b1[1]+k[1]*b2[1]+k[2]*b3[1]
        kz[kp_index] = k[0]*b1[2]+k[1]*b2[2]+k[2]*b3[2]
print "Number of Electrons = ",ElecNum,"\nNumber of K points =",KpNum,"\nNumber of bands = ",EigenNum,"\n"

#calculate the path and the high symmetric points
path=[]
path.append(0)
for kp_index in range(1,KpNum):
	k1 = [kx[kp_index],ky[kp_index],kz[kp_index]]
	k2 = [kx[kp_index-1],ky[kp_index-1],kz[kp_index-1]]
	path.append(path[kp_index-1]+distance(k2,k1))
	if (kp_index+1)%intersection == 0:
		print "high symmetric points in the reciprocal sapce:",path[kp_index]

#write the file for drawing the band structure
fw = open(r'Band.dat','w')        
for eigen_index in range(EigenNum):
	for kp_index in range(KpNum):
		if spin == 1:
			if kp_index%intersection != 0 or kp_index == 0:
				print>>fw,'{0:5f}  {1:8f}'.format(path[kp_index],eigen[eigen_index][kp_index]-fermi)
		elif spin == 2:
			if kp_index%intersection != 0 or kp_index == 0:
                        	print>>fw,'{0:5f}  {1:8f}  {2:8f}'.format(path[kp_index],eigen_up[eigen_index][kp_index]-fermi,eigen_dn[eigen_index][kp_index]-fermi)
    	print>>fw,''
fw.close()

#read eigenvalues of specified band
fw = open(r'spec_band.dat','w')
if spin == 1:
	for kp_index in range(KpNum):
                if kp_index%intersection != 0 or kp_index == 0:
			print >>fw, '\n{0:10.5f}  '.format(path[kp_index]),
			for eigen_index in (val_idx-4,val_idx-3,val_idx-2,val_idx-1,val_idx,con_idx,con_idx+1):
				print >>fw, '{0:5f}  '.format(eigen[eigen_index][kp_index]-fermi),
fw.close()


if spin == 1:
        VBM = max(eigen[val_idx])-fermi
        CBM = min(eigen[con_idx])-fermi
	print "\nVBM is ",VBM,"eV,	CBM is ",CBM, "eV"
	if CBM-VBM >= 0:
		print "band gap is ",CBM-VBM,"eV"
	else:
		print "this material is metallic!"
elif spin == 2:
	VBM_up = max(eigen_up[val_idx])-fermi
	CBM_up = min(eigen_up[con_idx])-fermi
	VBM_dn = max(eigen_dn[val_idx])-fermi
	CBM_dn = min(eigen_dn[con_idx])-fermi
	print "\nspin up channel:"
	if CBM_up - VBM_up >=0:
		print "\nVBM is ",VBM_up,"eV,	CBM is ",CBM_up,"eV\nband gap is ",CBM_up-VBM_up,"eV"
	else:
		print "spin up channel is metallic!"
        print "\nspin dn channel:"
        if CBM_dn - VBM_dn >=0:
                print "\nVBM is ",VBM_dn,"eV,   CBM is ",CBM_dn,"eV\nband gap is ",CBM_dn-VBM_dn,"eV"
        else:
                print "spin dn channel is metallic!"

print "\ndone!\nplease use the Band.dat file to plot band structures!\nnote the high symmetric points in the path.\n"
