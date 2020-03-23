# -*- coding: utf-8 -*-
"""
process scene data
Created on Mon Mar 23 07:33:50 2020

@author: DFTC_ZHANGDR
"""
import pandas as pd


class Scene():
    def __init__(self,video_id,time_start,time_end,tag,description):
        self.video_id = video_id
        self.time_start = time_start
        self.time_end = time_end
        self.id = hash(str(time_start+time_end))
        self.tag = tag
        self.description = description
        
    def save(self,file_path):
        #
        data ={'id':[self.video_id],'time_start':[self.time_start],\
               'time_end':[self.time_end],'tag':[self.tag],\
               'description':description}
        frame = pd.DataFrame(data)
        frame.to_csv(file_path, mode='a',index=False,header=False)#不将索引和列名写入数据 # 追加写入
        
# show structure
def show_struct(dic):
    print('')
    print('.structure')
    for key1 in list(dic.keys()):
        print('├──',key1)
        for key2 in list(dic[key1].keys()):
            print('│  ',' └──',key2)
 
# get test content
def group_testcase(dic,scene):
    for key1 in list(dic.keys()):
        for key2 in list(dic[key1].keys()):
            tag_needed = [key1,key2]
            if set(tag_needed) <= set(scene.tag): # has all requiredd tags
                dic[key1][key2].append(scene)
    return(dic)
          
# show test dictionary
def show_testcase(dic):
    print('.test_data')
    for key1 in list(dic.keys()):
        print('├──',key1)
        for key2 in list(dic[key1].keys()):
            print('│  ',' └──',key2)
            for scene3 in dic[key1][key2]:
                print('│       ',' └──',scene3.video_id,\
                      scene3.time_start,'-',scene3.time_end,scene3.tag)
                         
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
def find_testcase(dic,data):
    for row in data.iterrows():
        video_id = row[1][ 'video_id']
        time_start = row[1][ 'time_start']
        time_end = row[1][ 'time_end']
        tag = eval(row[1][ 'tag'])# 输出每一行
        description = ''
        scene = Scene(video_id, time_start, time_end,\
                      tag,description)    
        dic_dat = group_testcase(dic,scene)
    return(dic_dat)

#===========================================================================
# test example
dic = {'ACC':{'straight':[],\
              '弯道':[]},\
        'AEB':{'弯道':[],\
               'curv':[]}}
            
# show structure
show_struct(dic)                        
# read csv

data = pd.read_csv("log.csv") 

# show data
data.head()

# find test case 
dic_dat = find_testcase(dic,data)

show_testcase(dic_dat)  

test_list,test_videoid = get_testlist(dic_dat) 

# save test list
df_testvideo = pd.DataFrame(test_videoid) 
file_path = 'test_list.csv'
df_testvideo.to_csv(file_path,index=False,header=False)