# Wannier拟合及fatband分析

## fatband analysis

### 预先准备

我们需要安装 python 第三方库 “pyprocar”：

Windows：使用 pip install pyprocar 即可在 pycharm 或其他 Windows 端 python 编译器上安装这个库

Linux：在 Linux 虚拟机上同样可以使用该命令完成安装（当然，请先在虚拟机中安装 python3）

详细安装教程请见 pyprocar 官网 [PyProcar documentation — PyProcar 5.5.0 documentation (romerogroup.github.io)](https://romerogroup.github.io/pyprocar/)；除了安装，该网站还提供这个第三方库的使用教程。

### 具体操作

Windows：使用 pycharm 打开我发送的示例文件 fatband.py，依据注释进行修改，运行即可；

Linux：将 fatband.py 传入虚拟机，使用 vim 打开（请先在虚拟机中安装vim）或直接用虚拟机自带的文档编辑器打开，依据注释修改，在终端中输入命令 python3 fatband.py

最终结果将以图片的形式显示在当前文件夹，下图为样例——GeS中 Ge、S 四个原子 p 轨道在费米能级附近的能量贡献：

![GeS_p](D:\Linux\SHARED\down\wannierTrials-GeS\unshifted\GeS_p.png)

同样出示四个原子 s、d 轨道在费米能级附近的能量贡献：

![GeS_d](D:\Linux\SHARED\down\wannierTrials-GeS\unshifted\GeS_d.png)

![GeS_s](D:\Linux\SHARED\down\wannierTrials-GeS\unshifted\GeS_s.png)

得到类似的图标志该步骤成功。

## Wannier拟合

### 预先准备

fatband 分析的图有什么用处，以及如何利用fatband分析获得的信息进行高质量 Wannier 拟合，请先仔细阅读网页：[High-quality Wannier functions – WannierTools](https://www.wanniertools.org/tutorials/high-quality-wfs/)（非常重要的网站，请仔细阅读）

作为支撑，同样给出知乎回答：[一文搞定VASP+wannier90构造紧束缚模型 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/355317202)

如果哪一步卡住，请参考我的工作 /work/wq/workspace/xjq/GeS/DFTwithWannier

### 四部操作

Wannier拟合分为四步：

#### 第1步

mkdir 1-step，做一次带Wannier的自洽，为了得到wannier90.win。需要的文件与 scf 自洽计算相同，值得注意的是这里不再使用 submit.sh，而是使用 submit-wannier.sh 提交作业。该文件同样位于 xjq/files内。

#### 第2步

mkdir 2-step，并将1中所有内容拷贝在2中，即执行mv 1-step/* 2-step。

修改wannier90.win，依据一：Fatband analysis。据此选择你要投影的轨道

依据二：NBANDS。执行 nbands 可以得到 GeS 所有能带数。

删除 **use_bloch_phases = T** 这一行。

粘贴：

**search_shells = 60**

**num_bands =  48**

**num_wann = 44**

**write_xyz = true**

**exclude_bands = 1-8, 57-128**

**** 

**begin projections**

**Rh:d**

**P:p**

**Se:p**

**end projections**

注意这只是一个示例，请根据GeS进行具体更改。其中 num_bands 应大于等于 num_wann。

num_wann数值计算：例如POSCAR内显示有2个Ge原子，2个S原子，你要投影这四个原子的 p 轨道。我们知道 p 轨道内有3个电子，因此 num_wann = （2+2）*3=12

num_bands 可以也取 12；

exclude_bands排除了离费米能级太远的轨道，在本例中应取为1-x , (x+13)-36，请根据网站[High-quality Wannier functions – WannierTools](https://www.wanniertools.org/tutorials/high-quality-wfs/)及fatband确定 x ；36为 nbands，及全部能带数。

begin projections 到 end projections 之间填写每种原子投影的轨道。

#### 第3步

把2中所有文件copy过来，再次修改wannier90.win，加上两个窗口的参数，依据：两个rules，Fatband。

**num_iter = 100**

**dis_win_min  = -10**

**dis_win_max  = 2.158**

**dis_froz_min = -10**

**dis_froz_max = 0.898**

注意这只是个示例，数值请在origin中读取。

运行 ./wannier90.x wannier90.win。

#### 第4步

把3中所有文件copy过来，还是修改wannier90.win，加上计算能带的参数

**restart = plot**

**bands_plot = true**

**write_hr = true**

**begin kpoint_path**

**G 0.0 0.0 0.0 X 0.5 0.0 0.0**

**X 0.5 0.0 0.0 M 0.5 0.5 0.0**

**M 0.5 0.5 0.0 Y 0.0 0.5 0.0**

**Y 0.0 0.5 0.0 G 0.0 0.0 0.0**

**G 0.0 0.0 0.0 M 0.5 0.5 0.0**

**end kpoint_path**

**bands_num_points 101**

这一步只需要更改 begin kpoint_path 到 end kpoint_path 之间的内容即可。根据 band 文件夹内 KPOINTS 进行修改。

运行 ./wannier90.x wannier90.win。

若能得到wannier90_hr.dat，请告诉我，拿入Windows绘图，与能带分析时所画的能带图重合在一起比较。

下图为理想中的效果图：

![image-20220217201210592](C:\Users\XINJIAQI\AppData\Roaming\Typora\typora-user-images\image-20220217201210592.png)

其中蓝色为能带图，红色虚线为Wannier拟合的wannier90_hr.dat。