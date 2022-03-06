import pyprocar
import matplotlib.pyplot as plt

# 　将 POSCAR.PROCAR,OUTCAR,KPOINTS,vasprun.xml连同本脚本放在同一文件目录下
#   依据“KPOINTS”与能带图，修改pyprocar.bandsplot部分的“elimit”、“kticks”与“knames”
# 　这个版本固定示例为WSe2: 3 Se 12 W 6 P 16
#   批量fatband分析图将自动添加至当前目录
# 　辛嘉琪 2022.1.11

atoms_number = 3
number_a = 12
number_b = 6
number_c = 16
hetero = [list(range(1, number_a+1)), list(range(number_a+1, number_a+number_b+1)), list(range(number_a+number_b+1, number_a + number_b + number_c+1))]
atoms_name = ['Se', 'W', 'P']

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
        plt.savefig(atoms_name[i] + "-" + orbital_name[j] +"-" + str(id_name[j]) + ".png")