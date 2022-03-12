import numpy as np
import math
import pandas as pd
from pandas import DataFrame

#   准备 good_gap 以及 fermi 数据
#   准备能带文件 Band.dat，放在与代码同一文件夹下
#   运行文件，给出总能带数、good_gap以下能带数；价带数、导带数以及二者对应的能量极值
#   辛嘉琪 2022.3.12

good_gap = -7.15  # 依据能带图修改
fermi = -2.75  # 依据fermi能级修改

data_kpath=[]
data_energy=[]

with open('./Band.dat') as banddata:
    total_data = banddata.read()
    total_data= total_data.split() # 读取数据

    x = 1
    for y in total_data:
        if x%2 == 0:
            data_energy.append(float(y))
        else:
            data_kpath.append(float(y))
        x = x + 1
        # 行、列值读入Python内
nrows = int(x/2)

# 给出能带数以及每条能带取点个数
bands_number = 0  # 能带数
for i in range(nrows):
    if data_kpath[i] == 0.0:
        bands_number = bands_number + 1
m = int(nrows/bands_number)  # 每组的离散数据个数
print("总能带数NBANDS：",bands_number)

# 分组并记录数据
x = [[ 0 for col in range(m) ] for row in range(bands_number) ]
y = [[ 0 for col in range(m) ] for row in range(bands_number) ]
# bands_number个等长数组，每个里有m个元素

k = 0
for i in range(bands_number):
    for j in range(m):
        x[i][j] = data_kpath[k]
        y[i][j] = data_energy[k]
        k = k + 1
#########################################################

for i in range(bands_number):
    if max(y[i]) > good_gap:
        break # 注意break语句，输出时的值为刚好不符合条件的值
under_good_gap = i
print("在good gap以下能带数：", under_good_gap)

for i in range(bands_number):
    if max(y[i]) > fermi:
        break
under_fermi = i
print("价带数：", under_fermi)
print("导带数：", bands_number - under_fermi)
print("价带能量最高值:", max(y[under_fermi-1]), "eV")
print("导带能量最低值:", min(y[under_fermi]), "eV")