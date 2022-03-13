import string

#   请准备POSCAR-1，POSCAR-2，poscar_1，poscar_2
#   异质结 1 to 2、异质结2 to 1 将被放入 POSCAR-12 和 POSCAR-21
#   辛嘉琪 2022.3.15

element1 = []  # 第一种材料的元素
number1 = []  # 第一种材料的原子个数
parameter1 = []  # poscar_1的晶格常数
direct1 = []  # poscar_1的分数坐标系
total_number1 = 0  # hetero1的原子总数
Number1 = []  # hetero1的原子个数（写入POSCAR）


element2 = []  # 第二种材料的元素
number2 = []  # 第二种材料的原子个数
parameter2 = []  # poscar_2的晶格常数
direct2 = []  # poscar_2的分数坐标系
total_number2 = 0  # hetero2的原子个数
Number2 = []  # hetero2的原子个数（写入POSCAR）

with open("./POSCAR-1") as POSCAR1:
    POSCAR1 = POSCAR1.readlines()
    element1 = POSCAR1[5].split()
    number1_str = POSCAR1[6].split()
    for i in number1_str:
        number1.append(int(i))

with open("./POSCAR-2") as POSCAR2:
    POSCAR2 = POSCAR2.readlines()
    element2 = POSCAR2[5].split()
    number2_str = POSCAR2[6].split()
    for i in number2_str:
        number2.append(int(i))

with open("./poscar_1") as poscar1:
    poscar1 = poscar1.readlines()
    for i in range(1, 5):  # i = 1,2,3,4
        parameter1.append("".join(poscar1[i]))
    for i in range(6, len(poscar1)):  # i = 6 ,..., len - 1
        direct1.append("".join(poscar1[i]))
        total_number1 = total_number1 + 1
    if len(number1) != 1:
        if total_number1 % sum(number1) != 0:
            print("异质结1计算错误！")
        else:
            for i in number1:
                Number1.append(str(int(total_number1/sum(number1)*i)))
    else:
        Number1.append(str(total_number1))

with open("./poscar_2") as poscar2:
    poscar2 = poscar2.readlines()
    for i in range(1, 5):  # i = 1,2,3,4
        parameter2.append("".join(poscar2[i]))
    for i in range(6, len(poscar2)):  # i = 6 ,..., len - 1
        direct2.append("".join(poscar2[i]))
        total_number2 = total_number2 + 1
    if len(number2) != 1:
        if total_number2 % sum(number2) != 0:
            print("异质结2计算错误！")
        else:
            for i in number2:
                Number2.append(str(int(total_number2/sum(number2)*i)))
    else:
        Number2.append(str(total_number2))

with open("./POSCAR-12", "w") as outcome1:
    outcome1.write("heterojunctions" + "".join(element1) + "".join(element2) + "\n")
    for i in parameter1:
        outcome1.write(i)
    outcome1.write(" ".join(element1) +" "+ " ".join(element2) + "\n")
    outcome1.write(" ".join(Number1)+" "+" ".join(Number2)+"\n")
    outcome1.write("Direct\n")
    for i in direct1:
        outcome1.write(i)
    for i in direct2:
        outcome1.write(i)

with open("./POSCAR-21", "w") as outcome2:
    outcome2.write("heterojunctions" + "".join(element2) + "".join(element1) + "\n")
    for i in parameter2:
        outcome2.write(i)
    outcome2.write(" ".join(element2) +" "+ " ".join(element1) + "\n")
    outcome2.write(" ".join(Number2)+" "+" ".join(Number1)+"\n")
    outcome2.write("Direct\n")
    for i in direct2:
        outcome2.write(i)
    for i in direct1:
        outcome2.write(i)
