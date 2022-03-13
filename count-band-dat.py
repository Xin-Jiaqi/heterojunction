import numpy as np
import math
import pandas as pd
from pandas import DataFrame

#   准备 good_gap,如果没有，请填 -999
#   准备能带文件名称为 Band.dat (或改代码中文件名)，放在与代码同一文件夹下
#   运行文件，程序会给出总能带数、good_gap以下能带数（或不存在good gao）、坐标轴取值范围
#   若存在费米能级，程序将给出价带数导带数以及二者对应的能量极值；反之程序将报告“不存在费米能级”。
#   分析结果将显示在 pycharm 运行结果中，并保存为 information.txt 文件
#   辛嘉琪 2022.3.12
#   修改自动识别费米能级 2022.3.13
#########################################################

good_gap = -13.21192  # 依据能带图修改，如果没有good_gap，就填 -999

#########################################################
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

info = []

# 给出能带数以及每条能带取点个数
bands_number = 0  # 能带数
for i in range(nrows):
    if data_kpath[i] == 0.0:
        bands_number = bands_number + 1
m = int(nrows/bands_number)  # 每组的离散数据个数
info.append("总能带数NBANDS："+str(bands_number))

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
info.append("能带最低值："+str(min(y[0]))+" eV")
info.append("能带最高值："+str(max(y[bands_number-1]))+" eV")
info.append("横坐标(kpath)取值范围：0 ~ "+str(max(x[0])))
#########################################################
if good_gap != -999:
    for i in range(bands_number):
        if max(y[i]) > good_gap:
            break # 注意break语句，输出时的值为刚好不符合条件的值
    under_good_gap = i
    info.append("在good gap（"+str(good_gap)+" eV）以下能带数："+str(under_good_gap))
else:
    info.append('不存在\"good gap\"')
#########################################################
fermi = -999
for i in range(bands_number-1):
    if min(y[i]) > good_gap and min(y[i+1]) - max(y[i]) > 0:
        fermi = max(y[i])
        info.append("费米能级为："+str(fermi)+" eV")
        break
if fermi == -999:
    info.append("没有找到费米能级！")
else:
    for i in range(bands_number):
        if max(y[i]) > fermi:
            break
    under_fermi = i
#########################################################
if fermi != -999:
    info.append("价带数："+str(under_fermi))
    info.append("导带数："+str(bands_number - under_fermi))
    info.append("价带能量最高值："+str(max(y[under_fermi-1]))+" eV")
    info.append("导带能量最低值："+str(min(y[under_fermi]))+" eV")

for i in info:
    print(i)  #  输出结果

#########################################################
with open("information.txt", "w") as information:
    for i in info:
        information.write(i+'\n')