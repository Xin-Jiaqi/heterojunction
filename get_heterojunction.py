#!/usr/bin/python
from math import *
from numpy import *
import sys
import os



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
fres = open("target","r")
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
fatom = open("poscar_1","w")
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
fres = open("target","r")
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
fatom = open("poscar_2","w")
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

