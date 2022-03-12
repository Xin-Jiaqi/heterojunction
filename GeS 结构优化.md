# GeS 结构优化

## 进入服务器以及Linux相关指令

- 直接输入快捷命令：xjq ;进入练习区

1. ls ;命令显示当前文件夹内内容
2. cd lyl ;进入你的文件夹
3. cd.. ;退出当前文件夹到上一级
4. mkdir 自定义文件夹名 ;新建文件夹
5. 文件操作：
   - vi 某文件 ;打开某文件
   - 在文件内 执行 i ;开始编辑。执行 Esc ;退出编辑
   - 在文件内 执行 :q ;退出文件。执行 :wq ;保存文件并退出。执行 :q! ;不保存文件强制退出
   - 按「ctrl」+「u」：屏幕往"后"移动半页。按「ctrl」+「d」：屏幕往"前"移动半页。
6. rm 某文件 ;删除某文件
7. mv 文件A 文件B ;将文件A改名为文件B
8. rm -r  某文件夹 ;删除文件夹及其包含内容
9. cp 路径1/文件名 路径2 ;拷贝并粘贴

- 你可以在lyl文件夹下 mkdir opt ;进行结构优化

## 初始结构 POSCAR

GeS的POSCAR文件位于 xjq/GeS/DFTwithouotWannier/0/，可以在xjq 文件夹下执行 cp GeS/DFTwithouotWannier/0/POSCAR lyl/opt

## 其他输入文件的准备

### 1. POTCAR

1. lyl/opt文件夹下执行命令 pot.py
2. 输入Ge S
3. 注意：POSCAR中顺序若是 S Ge，则第2步需输入：Ge S
4. 检查输入是否正确 执行 paw

### 2. INCAR

1. 请直接在 xjq/files 内找到 INCAR-opt 执行操作 cp files/INCAR-opt lyl/opt INCAR ;以变复制、粘贴、改名
2. 在 lyl/opt 文件夹内执行 vi INCAR 可打开 INCAR 文件
3. 其中ISIF参数修改依据参考网站：https://www.vasp.at/wiki/index.php/ISIF；GeS作为二维材料，ISIF = 4

### 3. KPOINTS

1. 在 lyl/opt 文件夹内执行 writekp
2. vi KPOINTS
3. 遇到偶数 请加一 变为基数
4. GeS是二维材料 因此 z 方向即第三个数直接改为1

## 作业提交及查看

1. 将 submit.sh 拷贝至 lyl/opt
2. 观察 lyl/opt 内是否聚齐 “联合国五常” ：POSCAR, POTCAR, KPOINTS, INCAR, submit.sh
3. 执行 qsub submit.sh 提交作业；系统将返回作业序列号
4. 执行 qs 找到作业序列号查看进度
5. 同一个作业运算时间上限 30 min
6. 请勿在还没有算完时多次提交作业
7. 计算完成后执行 qs 将不在显示提交的作业序列号

## 结果检验

计算结果输出于 OUTCAR 文件，参考https://zhuanlan.zhihu.com/p/391279503，以检验计算结果。例如：查看有无收敛，执行 grep required OUTCAR ;没有结果，则不收敛；

输出最终结果在 CONTCAR 文件内。