# -*- coding: utf-8 -*-
"""
process scene data
Created on Mon Mar 23 07:33:50 2020

@author: DFTC_ZHANGDR
"""
dic = {'ACC':{'straight':[],\
              'curv':[]},\
        'AEB':{'straight':[],\
               'curv':[]}}

dic_dat = {'ACC':{'straight':['DR202021','DR202022'],\
              'curv':['DR202021']},\
        'AEB':{'straight':['DR202021'],\
               'curv':['DR202021']}}

a = list(dic.keys())
 
# show content
print('.')
for key1 in list(dic.keys()):
    print('├──',key1)
    for key2 in list(dic[key1].keys()):
        print('│  ',' └──',key2)
    
# get test content
tags = ['AEB','curv','ni_guang','cam_jump']  
scene_id = 'dz2020'

for key1 in list(dic.keys()):
    for key2 in list(dic[key1].keys()):
        tag_needed = [key1,key2]
        if set(tag_needed) <= set(tags): # has all requiredd tags
          is_select = True
          dic[key1][key2].append(scene_id)
          
# show test dictionary
print('.')
for key1 in list(dic.keys()):
    print('├──',key1)
    for key2 in list(dic[key1].keys()):
        print('│  ',' └──',key2)
        for elem3 in dic[key1][key2]:
            print('│       ',' └──',elem3,tags)
            
# get test list
test_list = [] 
for key1 in list(dic.keys()):
    for key2 in list(dic[key1].keys()):
        for elem3 in dic[key1][key2]:
            test_list.append(elem3)
            
print(test_list)            
# tetst prints
'''
print('.')
print('├──','ACC')
print('│  ',' └──','str')
print('│          ',' └──','data1')
print('│  ',' └──','curv')
print('├──','LKA')
print('│  ',' └──','str')
'''