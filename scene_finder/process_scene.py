# -*- coding: utf-8 -*-
"""
process scene data
Created on Mon Mar 23 07:33:50 2020

@author: DFTC_ZHANGDR
"""
import pandas as pd
from scene import Scene
# add scene to test

    
# show test
def show_test(dic):
    print('')
    print('.test')
    for key1 in list(dic.keys()): # 一级目录
        print('├──',key1)
        for key2 in list(dic[key1].keys()): # 二级目录
            print('│  ',' └──',key2)
          
# show test case
def show_testcase(dic):
    print('.test_data')
    for key1 in list(dic.keys()):
        print('├──',key1)
        for key2 in list(dic[key1].keys()):
            print('│  ',' └──',key2)
            for scene3 in dic[key1][key2]:
                print('│       ',' └──',scene3.video_id,\
                      scene3.time_start,'-',scene3.time_end,scene3.tag,scene3.desc)
                         
# get test list
def get_testlist(dic):
    test_list = [] 
    test_videoid = []
    for key1 in list(dic.keys()):
        for key2 in list(dic[key1].keys()):
            for elem3 in dic[key1][key2]:
                test_list.append(elem3)
                test_videoid.append(elem3.video_id)
    return(test_list,test_videoid)    

# find test case
def add_scene2test(dic,data):
    for row in data.iterrows():
        # get data
        video_id = row[1][ 'video_id']
        time_start = row[1][ 'time_start']
        time_end = row[1][ 'time_end']
        tag = eval(row[1][ 'tag'])# 输出每一行
        desc = row[1][ 'desc']
        scene = Scene(video_id, time_start, time_end,\
                      tag,desc)  

        # add scne to test case  
        for key1 in list(dic.keys()): # 一级目录
            for key2 in list(dic[key1].keys()): # 二级目录
                tag_needed = [key1,key2]
                if set(tag_needed) <= set(scene.tag): # has all requiredd tags
                    dic[key1][key2].append(scene)
    return(dic)

#===========================================================================
# test example
dic = {'ACC':{'目标误识别':[],\
              '弯道':[]},\
        'AEB':{'车辆':[],\
               '行人':[]}}
            
# show structure
show_test(dic)                        
# read csv
data = pd.read_csv("log.csv",encoding = "gb2312") 

# show data
data.head()

# find test case 
dic_dat = add_scene2test(dic,data)

show_testcase(dic_dat)  

test_list,test_videoid = get_testlist(dic_dat) 

# save test list
df_testvideo = pd.DataFrame(test_videoid) 
file_path = 'test_list.csv'
df_testvideo.to_csv(file_path,index=False,header=False)

pass