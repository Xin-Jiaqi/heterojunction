import pyprocar
import matplotlib.pyplot as plt

# 　将 POSCAR.PROCAR,OUTCAR,KPOINTS,vasprun.xml 连同本脚本放在同一文件目录下
#   依据 “KPOINTS” 与能带图，修改 pyprocar.bandsplot 部分的 “elimit”、“kticks”与“knames”
# 　运行程序 代码将自动依据 “POSCAR” 输入材料原子数、名称、个数
#   批量 fatband 分析图将自动添加至当前目录
# 　辛嘉琪 2022.1.11 修改：2022.3.6

each_number = []
hetero = []
atoms_name = []

with open("./POSCAR") as POSCAR:
    POSCAR = POSCAR.readlines()
    atoms_name = POSCAR[5].split()
    each_number_str = POSCAR[6].split()
    for i in each_number_str:
        each_number.append(int(i))
    atoms_number = len(atoms_name)

total = 1
element = []
for i in range(atoms_number):  # 0,1,2,...,atoms_number-1
    total += each_number[i]
    element.append(total)
    if i == 0:
        hetero.append(list(range(1, element[i])))
    else:
        hetero.append(list(range(element[i - 1], element[i])))

orbital_name = ['s', 'py', 'pz', 'px', 'dxy', 'dyz', 'dz2', 'dxz', 'dx2-y2', 'p', 'd']
count = 0
for i in range(atoms_number):  # 遍历所有种类的原子
    id_name = []
    for k in range(9):
        id_name.append([k])
    id_name.append([1, 2, 3])
    id_name.append([4, 5, 6, 7, 8])

    for j in range(len(id_name)):  # 遍历s、p、d轨道
        count += 1
        pyprocar.bandsplot('PROCAR', outcar='OUTCAR',
                           elimit=[-11.46, 3.85],
                           kticks=[0, 19, 39, 59, 79], knames=['G', 'X', 'S', 'Y', 'G'],
                           cmap='PuRd', mode='parametric',
                           atoms=hetero[i],
                           orbitals=id_name[j],
                           vmin=0, vmax=0.8, show=False)
        plt.savefig(atoms_name[i] + "-" + orbital_name[j] + ".png")

print(count, "张图已在文件夹中！")
