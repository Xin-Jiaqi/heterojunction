#   准备 fermi,如果没有，请填 -999
#   准备能带文件名称为 Band.dat (或改代码中文件名)，放在与代码同一文件夹下
#   运行文件，程序会给出总能带数、good_gap以下能带数（或不存在good gao）、坐标轴取值范围、价带数导带数以及二者对应的能量极值
#   分析结果将显示在 pycharm 运行结果中，并保存为 information.txt 文件
#   辛嘉琪 2022.3.12
#   修改自动识别费米能级 2022.3.13
#   修改为手动识别费米能级、自动识别 "good gap"：2022.3.16
#########################################################

fermi = -2.5842  # 在服务器中修改-2.933468

#########################################################
data_kpath = []
data_energy = []

with open('./Band.dat') as banddata:
    total_data = banddata.read()
    total_data = total_data.split()  # 读取数据

    x = 1
    for y in total_data:
        if x % 2 == 0:
            data_energy.append(float(y))
        else:
            data_kpath.append(float(y))
        x = x + 1
        # 行、列值读入Python内
nrows = int(x / 2)

info = []

# 给出能带数以及每条能带取点个数
bands_number = 0  # 能带数
for i in range(nrows):
    if data_kpath[i] == 0.0:
        bands_number = bands_number + 1
m = int(nrows / bands_number)  # 每组的离散数据个数
info.append("总能带数NBANDS：" + str(bands_number))

# 分组并记录数据
x = [[0 for col in range(m)] for row in range(bands_number)]
y = [[0 for col in range(m)] for row in range(bands_number)]
# bands_number个等长数组，每个里有m个元素

k = 0
for i in range(bands_number):
    for j in range(m):
        x[i][j] = data_kpath[k]
        y[i][j] = data_energy[k]
        k = k + 1
#########################################################
info.append("纵坐标 (能量) 取值范围：" + str(min(y[0])) + " eV ~ " + str(max(y[bands_number - 1])) + " eV")
info.append("横坐标 (kpath) 取值范围：0 ~ " + str(max(x[0])))
#########################################################
good_gap = -999
for i in range(bands_number - 1):
    if max(y[i + 1]) < fermi and min(y[i + 1]) - max(y[i]) > 0:
        good_gap = min(y[i + 1])
        under_good_gap = i + 1
if good_gap != -999:
    info.append("在good gap (" + str(good_gap) + " eV) 以下能带数：" + str(under_good_gap))
else:
    info.append('不存在\"good gap\"')
#########################################################
for i in range(bands_number):
    if max(y[i]) > fermi:
        break
under_fermi = i
#########################################################
info.append("费米能级为：" + str(fermi) + " eV")
info.append("价带数：" + str(under_fermi))
info.append("导带数：" + str(bands_number - under_fermi))
info.append("价带能量最高值：" + str(max(y[under_fermi - 1])) + " eV")
info.append("导带能量最低值：" + str(min(y[under_fermi])) + " eV")

for i in info:
    print(i)  # 输出结果
#########################################################
with open("information.txt", "w") as information:
    for i in info:
        information.write(i + '\n')
