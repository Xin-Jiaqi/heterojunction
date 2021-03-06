import pyprocar
import matplotlib.pyplot as plt

# 　将 POSCAR.PROCAR,OUTCAR,KPOINTS,vasprun.xml连同本脚本放在同一文件目录下
#   依据“KPOINTS”与能带图，修改pyprocar.bandsplot部分的“elimit”、“kticks”与“knames”
# 　运行程序 依据“POSCAR”输入材料原子数、名称、个数 例如WSe2: 3 Se 12 W 6 P 16 (每步之间回车)
#   批量fatband分析图将自动添加至当前目录
# 　辛嘉琪 2022.1.11 修改：2022.3.6

atoms_number = int(input('原子种类：'))
each_number = []
hetero = []
atoms_name = []
for count in range(atoms_number):
    element1 = sum(each_number)+1
    atoms_name.append(input("原子"+str(count+1)+"名称："))
    each_number.append(int(input("原子"+str(count+1)+"个数:")))
    element2 = sum(each_number)+1
    hetero.append(list(range(element1,element2)))

orbital_name = ['s', 'py', 'pz', 'px', 'dxy', 'dyz', 'dz2', 'dxz', 'dx2-y2', 'p', 'd']

for i in range(atoms_number):  # 遍历所有种类的原子

    id_name = []
    for k in range(9):
        id_name.append([k])
    id_name.append([1, 2, 3])
    id_name.append([4, 5, 6, 7, 8])

    for j in range(len(id_name)):  # 遍历s、p、d轨道
        pyprocar.bandsplot('PROCAR',outcar='OUTCAR',
                           elimit=[-11.46,3.85],
                           kticks=[0,19,39,59,79],knames=['G','X','S','Y','G'],
                           cmap='PuRd', mode='parametric',
                           atoms=hetero[i],
                           orbitals=id_name[j],
                           vmin=0, vmax=0.8, show=False)
        plt.savefig(atoms_name[i] + "-" + orbital_name[j] + ".png")