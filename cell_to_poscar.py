# cell to POSCAR
# 辛嘉琪 2022.3.16

latticce_parameter = []  # 晶格常数
name = []  # 原子名称
direction = []  # 原子坐标
elements_number = []  # 不重复原子个数

file = "./"+"TiS2 (0 0 -1).cell"  # 修改文件名即可

with open(file) as cell:
    cell = cell.readlines()
    for i in range(len(cell)):
        if cell[i] == "%BLOCK LATTICE_CART\n":
            lattice_parameter_min = i + 1
            break
    lattice_parameter_max = lattice_parameter_min + 3
    for i in range(lattice_parameter_min, lattice_parameter_max):
        latticce_parameter.append(cell[i])  # 读取晶格常数

    for i in range(len(cell)):
        if cell[i] == "%BLOCK POSITIONS_FRAC\n":
            name_direction_min = i + 1
        if cell[i] == "%ENDBLOCK POSITIONS_FRAC\n":
            name_direction_max = i
            break
    for i in range(name_direction_min, name_direction_max):
        name_direction = (cell[i].split(" "))
        while "" in name_direction:
            name_direction.remove("")  # 去掉空元素
        direction.append(name_direction[1] + " " + name_direction[2] + " " + name_direction[-1])  # 读取原子坐标
        name.append(name_direction[0])  # 读取原子种类
    elements = list(set(name))
    elements.sort(key=name.index)
    count = 0
    for i in elements:
        for j in name:
            if j == i:
                count += 1
        elements_number.append(str(count))
        count = 0  # 删除不重复元素

with open("./POSCAR", "w") as poscar:
    poscar.write("CellToPoscar\n 1.00000\n" + "".join(latticce_parameter) + " ".join(elements) + "\n" + " ".join(
        elements_number) + "\n")
    poscar.write("Direct\n" + "".join(direction))
