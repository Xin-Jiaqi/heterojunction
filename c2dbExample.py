'''
Created on 14:35, Mar. 25, 2021

@author: yilinZhang 
@address: Jilin University

These files are needed: c2db.db
'''
# C2DB的使用案例
# 加了点注释，辛嘉琪，2020.3.6
import numpy as np # 类似 MatLab
import pandas as pd # 数据分析工具，可以从各种文件格式比如 CSV、JSON、SQL、Microsoft Excel 导入数据
import os # Python 程序与操作系统进行交互的接口


def prehandle_c2db(): # 根据需要（step4）对数据库内容进行预处理到 sorted_by_condition.csv
    import json  # 轻量级的数据交换格式，易于人阅读和编写
    import sqlite3  # 使用 sqlite3 模块驱动 SQLite
    # Step1： connect database and get the features（功能）
    con = sqlite3.connect("c2db.db")  # 创建与数据库的连接
    df = pd.read_sql_query("select * from systems", con)  # 读取sql查询脚本,返回dataframe,可增删改

    # Step2: convert database to csv
    key_value_pairs = []
    for line in df.key_value_pairs: # 开始读搜索描述
        key_value_pairs.append(json.loads(line))
        # json.loads 用于解码 JSON 数据。该函数返回 Python 字段的数据类型
    key_value_pairs = pd.DataFrame(key_value_pairs) # 创建基本数据帧
    # 应该是将搜索描述放入 key_value_pairs

    # Step3: rename formula（fromula 指化学式）
    formula_values = list(key_value_pairs['folder'].str.split('/'))
    # folder 是路径
    # 分隔所有遇到的 “/”
    flag = []
    for line in formula_values:
        flag.append(line[-2])
    key_value_pairs['formula'] = flag
    # 这步是重新命名化学式

    # Step4： 以下几行是设定在数据库中的搜索条件，根据自己需要修改一下几行即可。以下是搜索spgnum（空间群）= 1, 且gap(带隙)大于0的结构
    key_value_pairs['condition'] = key_value_pairs['spgnum'] 
    hasBandGap = key_value_pairs[key_value_pairs['condition'] == 1]  # 条件1
    hasBandGap = hasBandGap[hasBandGap['gap'] > 0]  # 条件2
    hasBandGap.to_csv('sorted_by_condition.csv')  # DataFrame输出为csv文件 sorted_by_condition.csv


def writePOSCAR(atom):  # 该函数给出原子的 cif 和 POSCAR

    with open(path + os.sep + filename + '_POSCAR', 'w') as f:
        # with: 获取一个文件句柄，从文件中读取数据，然后关闭文件句柄;且可以很好的处理上下文环境产生的异常
        f.write(self.parameters['SystemName'] + '\n')
        f.write(str(self.parameters['ScalingFactor']) + '\n')

        LatticeMatrix = self.parameters['LatticeMatrix']
        for i in range(len(LatticeMatrix)):
            f.write(float2line(LatticeMatrix[i]))

        AtomsInfo = self.parameters['AtomsInfo']
        string = ['', '']
        for key in AtomsInfo.keys():
            string[0] += key + '    '
            string[1] += str(AtomsInfo[key]) + '    '
        string[0] += '\n'
        string[1] += '\n'
        f.write(string[0])
        f.write(string[1])

        f.write(self.parameters['CoordinateType'] + '\n')

        ElementsPositionMatrix = self.parameters['ElementsPositionMatrix'].copy()
        for key in ElementsPositionMatrix.keys():
            arr = ElementsPositionMatrix[key]
            for i in range(len(arr)):
                f.write(float2line(arr[i]))  # float2line 在 output_structure 中定义


def output_structure():
    import ase.db  # ASE 是用 Python 编程语言编写的原子模拟环境
    from ase.io import write
    dbpath = os.path.join(os.getcwd(), 'c2db.db')
    # os.getcwd 返回当前工作目录
    # os.path.join 路径拼接
    db = ase.db.connect(dbpath)  # 连接 ase 到数据库

    def float2line(mart):
        '''
        将矩阵转换成可输出的字符串形式
        '''
        string = ''
        for line in mart:
            for s in line:
                string += '%21.10f' % float(s)
            string += '\n'
        return string

    def count_element(mart):  # 该函数在下一部分调用
        string = ['', '']
        elements = sorted(set(mart), key=mart.index)
        # sorted 排序操作
        # set() 函数创建一个无序不重复元素集
        # key 排序的列
        for key in elements:
            string[0] += key + '    '
            string[1] += str(mart.count(key)) + '    '
        string[0] += '\n'
        string[1] += '\n'
        return string

    csv = pd.read_csv('sorted_by_condition.csv')  # 读取预处理得到的csv文件至 csv
    for i in range(len(csv)):
        atom = db.get_atoms(uid=csv.iloc[i]['uid'], add_additional_information=True)
        # get_atoms 是 ase 的命令
        write('{}.cif'.format(csv.iloc[i]['formula']), atom, format='cif')  # 写cif文件
        with open(csv.iloc[i]['formula'] + '.vasp', 'w') as f: # 写 POSCAR 文件
            f.write(csv.iloc[i]['uid'] + '\n')
            f.write('1.0\n')
            f.write(float2line(atom.get_cell()))
            atomInfo = count_element(atom.get_chemical_symbols())
            f.write(atomInfo[0])
            f.write(atomInfo[1])
            f.write('Cartesian\n')  # 注意这里是笛卡尔坐标，不是分数坐标
            f.write(float2line(atom.get_positions()))


if __name__ == "__main__":
    # 在 if __name__ == '__main__': 下的代码只有在第一种情况下（即文件作为脚本直接执行）才会被执行，而 import 到其他脚本中是不会被执行的
    prehandle_c2db()
    output_structure()
    #os.system('rm *.cif')  # 在Linux环境下，删除所有的 cif 文件