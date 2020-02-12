# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 17:18:58 2019

@author: wangning
"""
from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
 
car_center = np.array([10, 100])
lane_left_y = np.array([2,50,80,100,130,195])
lane_left_x = np.array([0,30,60,80,100,130])
lane_right_x = np.array([500, 460,415,380,290,250])
lane_right_y = np.array([1,20, 50,90, 150,200])

# decide whitch lane
def jud_lane_which(lane_right_x=[],lane_right_y=[],lane_left_x=[],lane_left_y=[],car_center=[]):
    '''
    还需要输入数据合法性检查
    '''
    plt.plot(lane_right_x, lane_right_y) 
    plt.plot(lane_left_x, lane_left_y) 
    a=min(np.max(lane_right_y),np.max(lane_left_y))
    b=max(np.min(lane_right_y),np.min(lane_left_y))
    n=car_center[0]
    m=car_center[1]
    #判断检测目标合法性
    if m>a or m<b:
        print("输入目标越界")
        plt.plot(car_center[0],car_center[1],  color="c",marker="*")
        return -1
    else:
            
        f_right = interp1d(lane_right_y, lane_right_x,'linear')
        f_left = interp1d(lane_left_y, lane_left_x,'linear')
        x_right = f_right(m)
        x_left  = f_left(m)
        if n>x_right:
            print("3333")
            plt.plot(car_center[0],car_center[1],  color="k",marker="*")
            plt.plot(x_right, car_center[1],  color="m",marker="*")
            return 3  #右车道
        elif n<=x_right and n>x_left:
            print("1111")
            plt.plot(car_center[0],car_center[1],  color="r",marker="*")
            plt.plot(x_right, car_center[1],  color="m",marker="*")
            plt.plot(x_left, car_center[1],  color="b",marker="*")
            return 1  #本车道
        else:
            print("2222")
            plt.plot(car_center[0],car_center[1],  color="y",marker="*")
            plt.plot(x_left, car_center[1],  color="b",marker="*")
            return 2   #左车道 
        
# lane input
lane=jud_lane_which(lane_right_x,lane_right_y,lane_left_x,lane_left_y,car_center)
print(lane)  

