import xlwings as xw

#   将Band.dat转为具有两列数据的Excel文件，A列为kpath，B列为Energy，文件名为band-unshift.xlsx
#   依据band图像及OUTCAR结果修改good_gap能量与fermi能级数值（箭头标出）
#   将py文件与xlsx文件放在同一文件夹下，运行程序
#   运行文件，给出总能带数、good_gap以下能带数；价带数、导带数以及二者对应的能量极值
#   辛嘉琪 2022.1.11

#########################################################
# 初始化及关闭“广告通知”
app = xw.App(visible = False, add_book = False)
app.display_alerts = False
app.screen_updating = False

# 打开当前文件夹下能带的Excel数据
wb = app.books.open('./band-unshift.xlsx')
sht = wb.sheets['Sheet1']

# 读取表内数据行、列数
info = sht.used_range
nrows = info.last_cell.row
ncols = info.last_cell.column

# 行、列值读入Python内
data_kpath = sht.range('A1:A'+str(nrows)).value
data_energy = sht.range('B1:B'+str(nrows)).value

# 给出能带数以及每条能带取点个数
bands_number = 1
for i in range(nrows):
    if type(data_kpath[i]) == str:
        bands_number = bands_number + 1
m = int((nrows + 1)/bands_number)-1

# 分组并记录数据
x = [[ 0 for col in range(m) ] for row in range(bands_number) ]
y = [[ 0 for col in range(m) ] for row in range(bands_number) ]
v = 0  # 能带数指标
j = 0  # 每个能带内数值指标
for i in range(nrows):
    if type(data_kpath[i]) == float:
        x[v][j] = data_kpath[i]
        y[v][j] = data_energy[i]
        j = j + 1
    else:
        j = 0
        v = v + 1
print("总能带数NBANDS：",bands_number)
#########################################################

for i in range(bands_number):
    if max(y[i]) > -13.11: # <——————————————————————————————依据能带图修改
        break # 注意break语句，输出时的值为刚好不符合条件的值
under_good_gap = i
print("在good gap以下能带数：", under_good_gap)

for i in range(bands_number):
    if max(y[i]) > -1.6480: # <——————————————————————————————依据fermi能级修改
        break
under_fermi = i
print("价带数：", under_fermi)
print("导带数：", bands_number - under_fermi)
print("价带能量最高值:", max(y[under_fermi-1]), "eV")
print("导带能量最低值:", min(y[under_fermi]), "eV")