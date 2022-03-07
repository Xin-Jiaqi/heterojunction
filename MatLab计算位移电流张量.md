# MatLab计算位移电流张量

## 支撑材料

文献《Large Bulk Photovoltaic Effect and Spontaneous Polarization of Single-Layer Monochalcogenides》。该文献给出了GeS的位移电流计算过程。文中 FIG.2. 即我们要在MatLab中复现出的结果。

## 准备文件

1. m文件：BPVSC_rgauge.m
2. POSCAR
3. wannier90_hr.dat（from 4-step）
4. wannier90_centres.xyz（from 4-step）

## 操作

- 请将4个文件放在同一文件夹下，

- 将 wannier90_centres.xyz 改名为 wannier90-wcenter.dat。并删去：

  - 前两行
  - 元素行

  即删去红框内内容：![image-20220305144320911](C:\Users\XINJIAQI\AppData\Roaming\Typora\typora-user-images\image-20220305144320911.png)

- 用 MatLab 打开BPVSC_rgauge.m，打开 **Initial** 部分

  - nkx、nky、nkz 是取点数，一般来说70足够。且对于二维材料，nkz=1.
  - ksi 是精度吧，我忘记了，不用动。
  - hv = linspace(1.0, 3.0, 100)：表示横坐标范围为1.0~3.0，此区间内共取100个点。请根据文献中图片修改横坐标范围。
  - nocc 表示占据态数，能带图中费米能级（0eV）以下有 n 条能带，即填 n。
  - a、b、c：
    - a 为引起材料位移电流的分量，二维材料中取 1 或 2（即没有 z 方向）.
    - b、c 为外界 施加的光场分量，可以取 1，2，3.
    - 综上且基于对称性，共可以出12张图，每张大概需要跑30min左右（仅对于我的电脑）。但不需要出完所有的图，只要晶轴取向和文献《Large Bulk Photovoltaic Effect and Spontaneous Polarization of Single-Layer Monochalcogenides》取的一样，并且能复现文献结果即可。
  - thickness 指二维材料厚度，eg：

  ![image-20220305150452633](C:\Users\XINJIAQI\AppData\Roaming\Typora\typora-user-images\image-20220305150452633.png)

  取这个值即可。

#### 运行，请耐心等待程序出图。