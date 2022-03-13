#   比较两文件是否完全相同
#   辛嘉琪 2002.3.13

with open("./POSCAR_cal") as a:
    a = a.readlines()

with open("./POSCAR-12") as b:
    b = b.readlines()

judge = 1
zuobiao = []
if len(a) != len(b):
    judge = 0
else:
    for i in range(0,len(a)):
        if a[i] != b[i]:
            zuobiao.append(i)
            judge = 0
if judge:
    print("yes")
else:
    for i in zuobiao:
        print("@@@@@@@@@@")
        print(a[i])
        print("@@@@@@@@@@")
        print(b[i])
        print("@@@@@@@@@@")
        print("\n")
#
# for i in range(2,10):
#     print(i)