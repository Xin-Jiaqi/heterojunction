#!/usr/bin/python
from math import *
from numpy import *
import sys
import os


countPOSCAR_1 = len(open(r"POSCAR-1",'rU').readlines())
fcell1 = open("POSCAR-1","r")
line = fcell1.readline().split()
line = fcell1.readline().split()
line = fcell1.readline().split()
c_11 = float(line[0])
c_12 = float(line[1])
line = fcell1.readline().split()
c_21 = float(line[0])
c_22 = float(line[1])
#print c_11, c_12, c_21, c_22
line = fcell1.readline().split()
line = fcell1.readline().split()
### print str without kouhao & yinhao
#element = ('').join(line)
#print element
line = fcell1.readline().split()
#####do not forget the case of several elements
noa1 = countPOSCAR_1 - 8
line = fcell1.readline().split()
#type_coordinate = ('').join(line)
#get a b and alpha
a1 = math.sqrt(c_11*c_11+c_12*c_12)
b1 = math.sqrt(c_21*c_21+c_22*c_22)
a_dot_b = c_11*c_21+c_12*c_22
cos1 = a_dot_b/a1/b1
sin1 = math.sqrt(1-cos1*cos1)
fcell1.close()
#print a1, b1, cos1, sin1


countPOSCAR_2 = len(open(r"POSCAR-2",'rU').readlines())
fcell2 = open("POSCAR-2","r")
line = fcell2.readline().split()
line = fcell2.readline().split()
line = fcell2.readline().split()
c_11 = float(line[0])
c_12 = float(line[1])
line = fcell2.readline().split()
c_21 = float(line[0])
c_22 = float(line[1])
#print c_11, c_12, c_21, c_22
line = fcell2.readline().split()
line = fcell2.readline().split()
### print str without kouhao & yinhao
#element = ('').join(line)
#print element
line = fcell2.readline().split()
#####do not forget the case of several elements
noa2 = countPOSCAR_2 - 8
line = fcell2.readline().split()
#type_coordinate = ('').join(line)
#get a b and alpha
a2 = math.sqrt(c_11*c_11+c_12*c_12)
b2 = math.sqrt(c_21*c_21+c_22*c_22)
a_dot_b = c_11*c_21+c_12*c_22
cos2 = a_dot_b/a2/b2
sin2 = math.sqrt(1-cos2*cos2)
fcell2.close()
#print a2, b2, cos2, sin2




#input six parameters of two 2D system
#print "vector a of first lattice"
#a1 = input("vector a of first lattice:")
#b1 = input("vector b of first lattice:")
#angl1 = input("angle of first lattice:")
#noa1 = input("total number of atoms in first lattice:")
#a2 = input("vector a of second lattice:")
#b2 = input("vector a of second lattice:")
#angl2 = input("angle of second lattice:")
#noa2 = input("total number of atoms in second lattice:")
maxarea = 500
accuracy = 0.02
#angle1 = angl1*3.1415926/180
#angle2 = angl2*3.1415926/180
os.system("touch info")
#calculate the cos value of the two angles
#cos1 = math.cos(angle1)
#cos2 = math.cos(angle2)
#calculate the area of the two lattice
##calculate the sin value of the two angles
#sin1 = math.sin(angle1)
#sin2 = math.sin(angle2)
##calculate the area 
area1 = a1*b1*sin1
area2 = a2*b2*sin2
#get two int ratios between maxarea and area1 or area2
ratio1 = int(maxarea/area1)
ratio2 = int(maxarea/area2)
#get proper r1 and r2 for lattice expansion
fw = open("info","w")
for i in range(1,ratio1+1):
    for j in range(1,ratio2+1):
        n1 = area2/area1
        n2 = float(i)/float(j)
        if (n1<n2):
           error = (n2-n1)/n1
           per = error*100
           if (error<accuracy):
	       mj1 = area1*i
	       mj2 = area2*j
               print>>fw, i,  j,  per,  mj1,  mj2
        else:
           error = (n1-n2)/n1
           per = error*100
           if (error<accuracy):
	       mj1 = area1*i
               mj2 = area2*j	       
               print>>fw, i,  j,  per,  mj1,  mj2
fw.close()
#####carry out a loop, from first line of info to the last last
countinfo = len(open(r"info",'rU').readlines())
fileinfo = open('info','r')
for s in range(countinfo):
    line = fileinfo.readline().split()
    ss = str(s)
#get the supercell vector length
    t1 = int(line[0])
    t2 = int(line[1])
    atom = noa1*t1+noa2*t2
    fl = open("supercell-1-case"+ss,"w")
    for x in range(1,t1+1):
        if (t1%x==0):
           z = t1/x
           for y in range(0,z):
               u1 = math.sqrt(x*x*a1*a1+y*y*b1*b1+2*x*y*a1*b1*cos1)
               v1 = z*b1
               u1dotv1 = x*z*a1*b1*cos1+y*z*b1*b1
               cosalpha1 = u1dotv1/u1/v1
#transform to degree
#	       ang1 = math.acos(cosalpha1)/3.1415926*180
               print>>fl, "u1 =",u1,  "v1 =",v1,  "angu1v1 =",cosalpha1, "i =",x,  "j =",y,  "m =",z
    fl.close()
## first supercell
    fm = open("supercell-2-case"+ss,"w")
    for x in range(1,t2+1):
        if (t2%x==0):
           z = t2/x
           for y in range(0,z):
               u2 = math.sqrt(x*x*a2*a2+y*y*b2*b2+2*x*y*a2*b2*cos2)
               v2 = z*b2
               u2dotv2 = x*z*a2*b2*cos2+y*z*b2*b2
               cosalpha2 = u2dotv2/u2/v2
#transform to degree
#	   ang2 = math.acos(cosalpha2)/3.1415926*180
               print>>fm, "u2 =",u2,  "v2 =",v2,  "angu1v2 =",cosalpha2, "i =",x,  "j =",y,  "m =",z
    fm.close()
#lattice reduction
##for the first lattice
    fr = open("result-1-case"+ss,"w")
    count = len(open(r"supercell-1-case"+ss,'rU').readlines())
    file = open('supercell-1-case'+ss,'r')
    for i in range(count):
        line = file.readline().split()
        u= float(line[2])
        v= float(line[5])
        cosalpha= float(line[8])

        is_not_reduced = True
        while is_not_reduced:
              if (cosalpha < 0):
                 cosalpha = -cosalpha
              if (u > v):
                 t = u
                 u = v
                 v = t
              elif (v > math.sqrt(u*u+v*v+2*u*v*cosalpha)):
                 cosbeta=cosalpha
                 cosalpha = (u*u+u*v*cosalpha)/u/math.sqrt(u*u+v*v+2*u*v*cosalpha)
                 v = math.sqrt(u*u+v*v+2*u*v*cosbeta)
              elif (v > math.sqrt(u*u+v*v-2*u*v*cosalpha)):
                 cosdelta=cosalpha
                 cosalpha = (u*v*cosalpha-u*u)/u/math.sqrt(u*u+v*v-2*u*v*cosalpha)
                 v = math.sqrt(u*u+v*v-2*u*v*cosdelta)
              else:
                 is_not_reduced = False
        ang = math.acos(cosalpha)/3.1415926*180
        print>>fr, "u1 =",u, "v1 =",v, "ang1 =",ang
    file.close()
    fr.close()
##for the second lattice
    fr = open("result-2-case"+ss,"w")
    count = len(open(r"supercell-2-case"+ss,'rU').readlines())
    file = open('supercell-2-case'+ss,'r')
    for i in range(count):
        line = file.readline().split()
        u= float(line[2])
        v= float(line[5])
        cosalpha= float(line[8])

        is_not_reduced = True
        while is_not_reduced:
              if (cosalpha < 0):
                 cosalpha = -cosalpha
              if (u > v):
                 t = u
                 u = v
                 v = t
              elif (v > math.sqrt(u*u+v*v+2*u*v*cosalpha)):
                 cosbeta=cosalpha
                 cosalpha = (u*u+u*v*cosalpha)/u/math.sqrt(u*u+v*v+2*u*v*cosalpha)
                 v = math.sqrt(u*u+v*v+2*u*v*cosbeta)
              elif (v > math.sqrt(u*u+v*v-2*u*v*cosalpha)):
                 cosdelta=cosalpha
                 cosalpha = (u*v*cosalpha-u*u)/u/math.sqrt(u*u+v*v-2*u*v*cosalpha)
                 v = math.sqrt(u*u+v*v-2*u*v*cosdelta)
              else:
                 is_not_reduced = False
        ang = math.acos(cosalpha)/3.1415926*180
        print>>fr, "u2 =",u, "v2 =",v, "ang2 =",ang
    file.close()
    fr.close()
###compare lattice1 and lattice2 to find the best match
    count1 = len(open(r"result-1-case"+ss,'rU').readlines())
    file1 = open('result-1-case'+ss,'r')
    fs = open("results-tmp","a")
    for i in range(count1):
        line = file1.readline().split()
        x1 = float('%.3f' % float(line[2]))
        y1 = float('%.3f' % float(line[5]))
        ang1 = float('%.3f' % float(line[8]))
        count2 = len(open(r"result-2-case"+ss,'rU').readlines())
        file2 = open('result-2-case'+ss,'r')
        for j in range(count2):
            line = file2.readline().split()
	    x2 = float('%.3f' % float(line[2]))
	    y2 = float('%.3f' % float(line[5]))
	    ang2 = float('%.3f' % float(line[8]))
	    diffx = abs(x1-x2)
	    diffy = abs(y1-y2)
	    diffang = abs(ang1-ang2)
	    errx = float('%.3f' % float(diffx/x1*100))
	    erry = float('%.3f' % float(diffy/y1*100))
	    errang = float('%.3f' % float(diffang/ang1*100))
            if (errx < 2) and (erry < 2) and (errang < 2) and (atom < 400):
                print>>fs, "u1 =", x1, "v1 =", y1, "ang1 =", ang1, "u2 =", x2, "v2 =", y2, "ang2 =", ang2, "atom =", atom, "errx =", errx, "erry =", erry, "errang =", errang
        file2.close()     
    file1.close()
    fs.close()
fileinfo.close()
os.system("rm result-* super*")
lines_seen = set()
outfile = open("results", "w")
for line in open("results-tmp", "r"):
     if line not in lines_seen:
        outfile.write(line)
        lines_seen.add(line)
outfile.close()
os.system("rm results-tmp")


##########get POSCAR of heterojunction
######## FIRST ###  LATTICE
########get lattice parameters of the primitive cell
fcell = open("POSCAR-1","r")
line = fcell.readline().split()
line = fcell.readline().split()
line = fcell.readline().split()
c_11 = float(line[0])
c_12 = float(line[1])
line = fcell.readline().split()
c_21 = float(line[0])
c_22 = float(line[1])
#print c_11, c_12, c_21, c_22
line = fcell.readline().split()
line = fcell.readline().split()
### print str without kouhao & yinhao
element = ('').join(line)
print element
line = fcell.readline().split()
#####do not forget the case of several elements
number_of_atom = int(line[0])
line = fcell.readline().split()
type_coordinate = ('').join(line)
#get a b and alpha
a = math.sqrt(c_11*c_11+c_12*c_12)
b = math.sqrt(c_21*c_21+c_22*c_22)
a_dot_b = c_11*c_21+c_12*c_22
cosalpha = a_dot_b/a/b
sinalpha = math.sqrt(1-cosalpha*cosalpha)
alpha = math.acos(cosalpha)
fcell.close()
########################################################
##obtain u v gamma
fres = open("results","r")
line = fres.readline().split()
u = float(line[2])
v = float(line[5])
gamma = float(line[8])*3.1415926/180
#print u, v, gamma
#u = 7.380
#v = 7.380
#gamma = 60*3.1415926/180
cosalpha = math.cos(alpha)
sinalpha = math.sin(alpha)
cosgamma = math.cos(gamma)
singamma = math.sin(gamma)
s_lattice = u*v*singamma
#print s_lattice
######################################################

#look for n1 m1 n2 m2
fw = open("test","w")
for n1 in range(-30,30):
    for m1 in range(-30,30):
        uu = float('%.3f' % math.sqrt(n1*n1*a*a+m1*m1*b*b+2*n1*m1*a*b*cosalpha))
        diff_u = abs(uu - u)
    #    print diff_u
        if (diff_u < 0.001):
           for n2 in range(-30,30):
              for m2 in range(-30,30):
                   vv = float('%.3f' % math.sqrt(n2*n2*a*a+m2*m2*b*b+2*n2*m2*a*b*cosalpha)) 
                   diff_v = abs(vv - v)      
     #              print diff_v            
                   if (diff_v < 0.001):
                      uudotvv = n1*n2*a*a+m1*m2*b*b+(n1*m2+n2*m1)*a*b*cosalpha
                      udotv = float('%.3f' % uudotvv)
                      hhhhhh = float('%.3f' % float(udotv/u/v))
               #       print uudotvv, uu, vv
                      angle = math.acos(hhhhhh)
                      diff_angle = abs(angle - gamma)
      #                print diff_angle
                      if (diff_angle < 0.001):
                         n3 = n1+n2
                         m3 = m1+m2 
                         print>>fw, n1, m1, n2, m2, n3, m3
fw.close()
#add atoms under one parameter
filetest = open('test','r')
line = filetest.readline().split()
n1 = int(line[0])
m1 = int(line[1])
n2 = int(line[2])
m2 = int(line[3])
n3 = int(line[4])
m3 = int(line[5])
filetest.close()
#print n1, m1, n2, m2, n3, m3
####lattice
fatom = open("poscar-1","w")
x_u = u
y_u = 0
z_u = 0
x_v = v*cosgamma
y_v = v*singamma
z_v = 0
print>>fatom, "heterostructure-1"
print>>fatom, "1.000000"
print>>fatom, x_u, y_u, z_u
print>>fatom, x_v, y_v, z_v
print>>fatom, 0, 0, 40
print>>fatom, "Direct"
####rotation matrix
u_dot = n1*a*a+m1*a*b*cosalpha
cos_u = u_dot/u/a
sin_u = math.sqrt(1-cos_u*cos_u)
#print cos_u, sin_u

#print n1, m1, n2, m2, n3, m3
#print "hello"
#find all of the points inside the lattice
flattice = open("tem_latt","w")
#fgyg = open("guo", "w")
for x in range (-12,12):
    for y in range (-12,12):
        x0 = 0 - x
        y0 = 0 - y
        x1 = n1 - x
        y1 = m1 - y 
        x2 = n2 - x
        y2 = m2 - y
        x3 = n3 - x
        y3 = m3 - y
        tt0 = x0*x0*a*a+y0*y0*b*b+2*x0*y0*a*b*cosalpha
        tt1 = x1*x1*a*a+y1*y1*b*b+2*x1*y1*a*b*cosalpha
        tt2 = x2*x2*a*a+y2*y2*b*b+2*x2*y2*a*b*cosalpha
        tt3 = x3*x3*a*a+y3*y3*b*b+2*x3*y3*a*b*cosalpha
        t0 = math.sqrt(tt0)
        t1 = math.sqrt(tt1)
        t2 = math.sqrt(tt2)
        t3 = math.sqrt(tt3)
        t0_dot_t1 = x0*x1*a*a+y0*y1*b*b+(x0*y1+x1*y0)*a*b*cosalpha
        t0_dot_t2 = x0*x2*a*a+y0*y2*b*b+(x0*y2+x2*y0)*a*b*cosalpha
        t3_dot_t1 = x3*x1*a*a+y3*y1*b*b+(x3*y1+x1*y3)*a*b*cosalpha
        t3_dot_t2 = x3*x2*a*a+y3*y2*b*b+(x3*y2+x2*y3)*a*b*cosalpha
        if (t0 > 0) and (t1 > 0) and (t2 > 0) and (t3 > 0):
          cos_angle0_1 = t0_dot_t1/t0/t1
          cos_angle0_2 = t0_dot_t2/t0/t2
          cos_angle3_1 = t3_dot_t1/t3/t1
          cos_angle3_2 = t3_dot_t2/t3/t2
#          print cos_angle3_2
          ss0_1 = abs(0.25*tt0*tt1*(1-cos_angle0_1*cos_angle0_1))
          ss0_2 = abs(0.25*tt0*tt2*(1-cos_angle0_2*cos_angle0_2))
          ss3_1 = abs(0.25*tt3*tt1*(1-cos_angle3_1*cos_angle3_1))
          ss3_2 = abs(0.25*tt3*tt2*(1-cos_angle3_2*cos_angle3_2))
#          print ss3_2
          s0_1 = math.sqrt(ss0_1)
          s0_2 = math.sqrt(ss0_2)
          s3_1 = math.sqrt(ss3_1)
          s3_2 = math.sqrt(ss3_2)
          s = s0_1+s0_2+s3_1+s3_2
         # print>>fgyg, s, "bijiao", s_lattice
          diff_s = abs(s-s_lattice)
          if (diff_s < 0.015):
             print>>flattice, x, y
          #   print>> "check", x, y
        elif (t0 == 0) or (t1 == 0) or (t2 == 0) or (t3 == 0):
             print>>flattice, x, y
flattice.close()
os.system("cp tem_latt compare")
countcompare = len(open(r"compare",'rU').readlines())
filecompare = open('compare','r')
for s in range(countcompare):
    line = filecompare.readline().split()
    s1 = int(line[0])
    s2 = int(line[1])
    c_1_1 = s1 - n1
    c_2_1 = s2 - m1
    c_1_2 = s1 - n2
    c_2_2 = s2 - m2
    c_1_3 = s1 - n3
    c_2_3 = s2 - m3
    ss = str(s)
    ff = open(ss,"w")
#    print "one", s1, s2
    counttem_latt = len(open(r"tem_latt",'rU').readlines())
    filetem_latt = open('tem_latt','r')
    for e in range(counttem_latt):
        line = filetem_latt.readline().split()
        e1 = int(line[0])
        e2 = int(line[1])
        d_1_1 = c_1_1 - e1
        d_2_1 = c_2_1 - e2
        d_1_2 = c_1_2 - e1
        d_2_2 = c_2_2 - e2
        d_1_3 = c_1_3 - e1
        d_2_3 = c_2_3 - e2
        if ((d_1_1 == 0) and (d_2_1 == 0)) or ((d_1_2 == 0) and (d_2_2 == 0)) or ((d_1_3 == 0) and (d_2_3 == 0)):
           print>>ff, "zheng", s1, s2
        else:
           print>>ff, "fu", s1, s2
    ff.close()
fz = open("ref-1","w")
for k in range(countcompare):
    kk = str(k)
    check = 'zheng'
    with open(kk,'r') as foo:
         for line in foo.readlines():
             if check in line:
                panduan = 1
                os.remove(kk)
                break
             else:
                panduan = 2
    if (panduan == 2):
       fw = open(kk,'r')
       line = fw.readline().split()
       j1 = int(line[1])
       j2 = int(line[2])
       os.remove(kk)
       print>>fz, j1, j2
fz.close()
os.remove("test")
os.remove("tem_latt")
os.remove("compare")
###########fatom = open("poscar","w")      

countPOSCAR = len(open(r"POSCAR-1",'rU').readlines())-8
fcrystal = open("POSCAR-1","r")
line = fcrystal.readline().split()
line = fcrystal.readline().split()
line = fcrystal.readline().split()
line = fcrystal.readline().split()
line = fcrystal.readline().split()
line = fcrystal.readline().split()
line = fcrystal.readline().split()
line = fcrystal.readline().split()
for w in range(0, countPOSCAR):
    line = fcrystal.readline().split()
    x = float(line[0])
    y = float(line[1])
    z = float(line[2])
#    print x, y, z
    countref = len(open(r"ref-1",'rU').readlines())
    fref = open('ref-1','r')
    for i in range(countref):
        line = fref.readline().split()
        g1 = int(line[0])
        g2 = int(line[1])
        x_atom1 = x + g1
        y_atom1 = y + g2
        Dir_1_x = (m2*x_atom1-n2*y_atom1)/(n1*m2-m1*n2)
        Dir_1_y = (m1*x_atom1-n1*y_atom1)/(n2*m1-m2*n1)
        print>>fatom, Dir_1_x, Dir_1_y, z
    fref.close()
fcrystal.close()
fatom.close()
os.remove("ref-1")



#### second #### LATTICE
########get lattice parameters of the primitive cell
fcell = open("POSCAR-2","r")
line = fcell.readline().split()
line = fcell.readline().split()
line = fcell.readline().split()
c_11 = float(line[0])
c_12 = float(line[1])
line = fcell.readline().split()
c_21 = float(line[0])
c_22 = float(line[1])
#print c_11, c_12, c_21, c_22
line = fcell.readline().split()
line = fcell.readline().split()
### print str without kouhao & yinhao
element = ('').join(line)
print element
line = fcell.readline().split()
#####do not forget the case of several elements
number_of_atom = int(line[0])
line = fcell.readline().split()
type_coordinate = ('').join(line)
#get a b and alpha
a = math.sqrt(c_11*c_11+c_12*c_12)
b = math.sqrt(c_21*c_21+c_22*c_22)
a_dot_b = c_11*c_21+c_12*c_22
cosalpha = a_dot_b/a/b
sinalpha = math.sqrt(1-cosalpha*cosalpha)
alpha = math.acos(cosalpha)
fcell.close()
########################################################
##obtain u v gamma
fres = open("results","r")
line = fres.readline().split()
u = float(line[11])
v = float(line[14])
gamma = float(line[17])*3.1415926/180
#print u, v, gamma
#u = 7.380
#v = 7.380
#gamma = 60*3.1415926/180
cosalpha = math.cos(alpha)
sinalpha = math.sin(alpha)
cosgamma = math.cos(gamma)
singamma = math.sin(gamma)
s_lattice = u*v*singamma

######################################################

#look for n1 m1 n2 m2
fw = open("test","w")
for n1 in range(-30,30):
    for m1 in range(-30,30):
        uu = float('%.3f' % math.sqrt(n1*n1*a*a+m1*m1*b*b+2*n1*m1*a*b*cosalpha))
        diff_u = abs(uu - u)
    #    print diff_u
        if (diff_u < 0.001):
           for n2 in range(-30,30):
              for m2 in range(-30,30):
                   vv = float('%.3f' % math.sqrt(n2*n2*a*a+m2*m2*b*b+2*n2*m2*a*b*cosalpha)) 
                   diff_v = abs(vv - v)      
     #              print diff_v            
                   if (diff_v < 0.001):
                      uudotvv = n1*n2*a*a+m1*m2*b*b+(n1*m2+n2*m1)*a*b*cosalpha
                      udotv = float('%.3f' % uudotvv)
                      hhhhhh = float('%.3f' % float(udotv/u/v))
                      angle = math.acos(hhhhhh)
                      diff_angle = abs(angle - gamma)
      #                print diff_angle
                      if (diff_angle < 0.001):
                         n3 = n1+n2
                         m3 = m1+m2 
                         print>>fw, n1, m1, n2, m2, n3, m3
fw.close()
#add atoms under one parameter
filetest = open('test','r')
line = filetest.readline().split()
n1 = int(line[0])
m1 = int(line[1])
n2 = int(line[2])
m2 = int(line[3])
n3 = int(line[4])
m3 = int(line[5])
filetest.close()
#print n1, m1, n2, m2
####lattice
fatom = open("poscar-2","w")
x_u = u
y_u = 0
z_u = 0
x_v = v*cosgamma
y_v = v*singamma
z_v = 0
print>>fatom, "heterostructure-2"
print>>fatom, "1.000000"
print>>fatom, x_u, y_u, z_u
print>>fatom, x_v, y_v, z_v
print>>fatom, 0, 0, 40
print>>fatom, "Direct"
####rotation matrix
u_dot = n1*a*a+m1*a*b*cosalpha
cos_u = u_dot/u/a
sin_u = math.sqrt(1-cos_u*cos_u)
#print cos_u, sin_u

#print n1, m1, n2, m2, n3, m3
#print "hello"
#find all of the points inside the lattice
flattice = open("tem_latt","w")
for x in range (-30,30):
    for y in range (-30,30):
        x0 = 0 - x
        y0 = 0 - y
        x1 = n1 - x
        y1 = m1 - y 
        x2 = n2 - x
        y2 = m2 - y
        x3 = n3 - x
        y3 = m3 - y
        tt0 = x0*x0*a*a+y0*y0*b*b+2*x0*y0*a*b*cosalpha
        tt1 = x1*x1*a*a+y1*y1*b*b+2*x1*y1*a*b*cosalpha
        tt2 = x2*x2*a*a+y2*y2*b*b+2*x2*y2*a*b*cosalpha
        tt3 = x3*x3*a*a+y3*y3*b*b+2*x3*y3*a*b*cosalpha
        t0 = math.sqrt(tt0)
        t1 = math.sqrt(tt1)
        t2 = math.sqrt(tt2)
        t3 = math.sqrt(tt3)
        t0_dot_t1 = x0*x1*a*a+y0*y1*b*b+(x0*y1+x1*y0)*a*b*cosalpha
        t0_dot_t2 = x0*x2*a*a+y0*y2*b*b+(x0*y2+x2*y0)*a*b*cosalpha
        t3_dot_t1 = x3*x1*a*a+y3*y1*b*b+(x3*y1+x1*y3)*a*b*cosalpha
        t3_dot_t2 = x3*x2*a*a+y3*y2*b*b+(x3*y2+x2*y3)*a*b*cosalpha
        if (t0 > 0) and (t1 > 0) and (t2 > 0) and (t3 > 0):
          cos_angle0_1 = t0_dot_t1/t0/t1
          cos_angle0_2 = t0_dot_t2/t0/t2
          cos_angle3_1 = t3_dot_t1/t3/t1
          cos_angle3_2 = t3_dot_t2/t3/t2
#          print cos_angle3_2
          ss0_1 = abs(0.25*tt0*tt1*(1-cos_angle0_1*cos_angle0_1))
          ss0_2 = abs(0.25*tt0*tt2*(1-cos_angle0_2*cos_angle0_2))
          ss3_1 = abs(0.25*tt3*tt1*(1-cos_angle3_1*cos_angle3_1))
          ss3_2 = abs(0.25*tt3*tt2*(1-cos_angle3_2*cos_angle3_2))
#          print ss3_2
          s0_1 = math.sqrt(ss0_1)
          s0_2 = math.sqrt(ss0_2)
          s3_1 = math.sqrt(ss3_1)
          s3_2 = math.sqrt(ss3_2)
          s = s0_1+s0_2+s3_1+s3_2
          diff_s = abs(s-s_lattice)
          if (diff_s < 0.015):
             print>>flattice, x, y
        elif (t0 == 0) or (t1 == 0) or (t2 == 0) or (t3 == 0):
             print>>flattice, x, y
flattice.close()
os.system("cp tem_latt compare")
countcompare = len(open(r"compare",'rU').readlines())
filecompare = open('compare','r')
for s in range(countcompare):
    line = filecompare.readline().split()
    s1 = int(line[0])
    s2 = int(line[1])
    c_1_1 = s1 - n1
    c_2_1 = s2 - m1
    c_1_2 = s1 - n2
    c_2_2 = s2 - m2
    c_1_3 = s1 - n3
    c_2_3 = s2 - m3
    ss = str(s)
    ff = open(ss,"w")
#    print "one", s1, s2
    counttem_latt = len(open(r"tem_latt",'rU').readlines())
    filetem_latt = open('tem_latt','r')
    for e in range(counttem_latt):
        line = filetem_latt.readline().split()
        e1 = int(line[0])
        e2 = int(line[1])
        d_1_1 = c_1_1 - e1
        d_2_1 = c_2_1 - e2
        d_1_2 = c_1_2 - e1
        d_2_2 = c_2_2 - e2
        d_1_3 = c_1_3 - e1
        d_2_3 = c_2_3 - e2
        if ((d_1_1 == 0) and (d_2_1 == 0)) or ((d_1_2 == 0) and (d_2_2 == 0)) or ((d_1_3 == 0) and (d_2_3 == 0)):
           print>>ff, "zheng", s1, s2
        else:
           print>>ff, "fu", s1, s2
    ff.close()
fz = open("ref-2","w")
for k in range(countcompare):
    kk = str(k)
    check = 'zheng'
    with open(kk,'r') as foo:
         for line in foo.readlines():
             if check in line:
                panduan = 1
                os.remove(kk)
                break
             else:
                panduan = 2
    if (panduan == 2):
       fw = open(kk,'r')
       line = fw.readline().split()
       j1 = int(line[1])
       j2 = int(line[2])
       os.remove(kk)
       print>>fz, j1, j2
fz.close()
os.remove("test")
os.remove("tem_latt")
os.remove("compare") 
###########fatom = open("poscar","w")      

countPOSCAR = len(open(r"POSCAR-2",'rU').readlines())-8
fcrystal = open("POSCAR-2","r")
line = fcrystal.readline().split()
line = fcrystal.readline().split()
line = fcrystal.readline().split()
line = fcrystal.readline().split()
line = fcrystal.readline().split()
line = fcrystal.readline().split()
line = fcrystal.readline().split()
line = fcrystal.readline().split()
for w in range(0, countPOSCAR):
    line = fcrystal.readline().split()
    x = float(line[0])
    y = float(line[1])
    z = float(line[2])
#    print x, y, z
    countref = len(open(r"ref-2",'rU').readlines())
    fref = open('ref-2','r')
    for i in range(countref):
        line = fref.readline().split()
        g1 = int(line[0])
        g2 = int(line[1])
        x_atom1 = x + g1
        y_atom1 = y + g2
        Dir_1_x = (m2*x_atom1-n2*y_atom1)/(n1*m2-m1*n2)
        Dir_1_y = (m1*x_atom1-n1*y_atom1)/(n2*m1-m2*n1)
        print>>fatom, Dir_1_x, Dir_1_y, z
    fref.close()
fcrystal.close()
fatom.close()
os.remove("ref-2")

