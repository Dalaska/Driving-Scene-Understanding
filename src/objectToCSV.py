# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 15:33:51 2019

@author: wangning
"""

import csv

rows = [['people', 'right','peolple','middle','people','left', 'car', 'right','car','middle', 'car', 'left','others'],
        ['people', 'right','peolple','middle','people','left','car', 'right','car','middle', 'car', 'left','others'],
        ['people', 'right','peolple','middle','people','left','car', 'right','car','middle', 'car', 'left','others'],
        ['people', 'right','peolple','middle','people','left','car', 'right','car','middle', 'car', 'left','others']]
   
def objectToCSV(rows=[],frameTime=0.001):  # rows输入目标种类，位置信息，frameTime一帧的时间
    i=1
    with open('ObjectOut2.csv','w') as csvFile:# a在已有csv中添加， w新建cvs
         writer=csv.writer(csvFile)
         for row in rows:
            row=[i,(i-1)*frameTime]+row        # 每行第一个为帧序号，第二项为时间
            writer.writerow(row)
            i=i+1
    csvFile.close()
    
objectToCSV(rows,0.2)

