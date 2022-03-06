import pyprocar
import matplotlib.pyplot as plt

# 根据 POSCAR 输入材料原子种类的数目、每种原子的名称及个数
# 回车即可遍历所有种类原子的 s、p、d 轨道

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