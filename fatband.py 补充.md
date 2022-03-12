# fatband.py 补充

## 需要的文件

1. fatband.py
2. KPOINTS
3. OUTCAR
4. POSCAR
5. PROCAR
6. vasprun.xml

请放在同一文件夹下，并打开fatband.py

## 代码示例

![image-20220303164240777](C:\Users\XINJIAQI\AppData\Roaming\Typora\typora-user-images\image-20220303164240777.png)

## 参数说明

**elimit:** 能带纵坐标能量范围。示例中为-15至15

![image-20220303164338243](C:\Users\XINJIAQI\AppData\Roaming\Typora\typora-user-images\image-20220303164338243.png)

**knames:** 即高对称路径点，按你所取的名称填写（参考KPOINTS，或能带图）

![image-20220303165625157](C:\Users\XINJIAQI\AppData\Roaming\Typora\typora-user-images\image-20220303165625157.png)



**kticks:** 

- KPOINTS第二行若是20
- 高对称路径点假设有4个
- 则kticks = [0, 19, 39, 59, 79]
- 其他数值同理

**atoms:** 依据POSCAR。例如POSCAR内为：
    Ge    S

​	2       2

​	则atoms = [1, 2, 3, 4] 表示观测所有原子，atoms = [1, 2] 表示观测 Ge 原子

**orbitals**: 

![image-20220303165442672](C:\Users\XINJIAQI\AppData\Roaming\Typora\typora-user-images\image-20220303165442672.png)

vmin, vmax: 示例中为 0~0.8，对应图上 colorbar: 

![image-20220303165540367](C:\Users\XINJIAQI\AppData\Roaming\Typora\typora-user-images\image-20220303165540367.png)