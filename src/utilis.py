# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 15:30:02 2019

@author: dalaska
"""

import  cv2  as cv
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import detector

# Draw the predicted bounding box
def drawBox(frame,obj):
    # Draw a bounding box.
    cv.rectangle(frame, (obj.left, obj.top), (obj.right, obj.bottom), (0, 0, 255))

    label = '%.2f' % obj.confidence

    # Display the label at the top of the bounding box
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(obj.top, labelSize[1])
    cv.putText(frame, label, (obj.left, obj.top), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
    

# decide whitch lane
def jud_lane_which(lane,car_center=[]):
    '''
    还需要输入数据合法性检查
    '''
    plt.plot(lane.right_x, lane.right_y) 
    plt.plot(lane.left_x, lane.left_y) 
    a=min(np.max(lane.right_y),np.max(lane.left_y))
    b=max(np.min(lane.right_y),np.min(lane.left_y))
    n=car_center[0]
    m=car_center[1]
    #判断检测目标合法性
    if m>a or m<b:
        print("UNDECIDED")
        plt.plot(car_center[0],car_center[1],  color="c",marker="*")
        return 4
    else:
            
        f_right = interp1d(lane.right_y, lane.right_x,'linear')
        f_left = interp1d(lane.left_y, lane.left_x,'linear')
        x_right = f_right(m)
        x_left  = f_left(m)
        if n>x_right:
            print("RIGHT")
            plt.plot(car_center[0],car_center[1],  color="k",marker="*")
            plt.plot(x_right, car_center[1],  color="m",marker="*")
            return 3  #右车道
        elif n<=x_right and n>x_left:
            print("EGO")
            plt.plot(car_center[0],car_center[1],  color="r",marker="*")
            plt.plot(x_right, car_center[1],  color="m",marker="*")
            plt.plot(x_left, car_center[1],  color="b",marker="*")
            return 1  #本车道
        else:
            print("LEFT")
            plt.plot(car_center[0],car_center[1],  color="y",marker="*")
            plt.plot(x_left, car_center[1],  color="b",marker="*")
            return 2   #左车道 


def detectImg(frame,detector):
    # find object
    objlist = detect.detect(frame)
    
    # find lane
    lane_left_x, lane_left_y, lane_right_x, lane_right_y = findLane(frame)
    
    # find carcenter
    car_center = findCarCenter(objlist,lane_left_x, lane_left_y, lane_right_x, lane_right_y)
    
    # find obj in which lane
    objLane = findObjLane(objlist, lane_right_x,lane_right_y,lane_left_x,lane_left_y)
    
    return objlist, car_center, objLane, lane_left_x, lane_left_y, lane_right_x, lane_right_y

def findLane(frame):
    # test case
    lane_left_x = np.array([50, 300, 500])
    lane_left_y = np.array([600, 500, 400])
    lane_right_x = np.array([650, 800, 950])
    lane_right_y = np.array([400, 500, 600])
    return lane_left_x, lane_left_y, lane_right_x, lane_right_y

def findCarCenter(objlist,lane_left_x, lane_left_y, lane_right_x, lane_right_y):
    car_center = []
    for obj in objlist:
        center = (round((obj.left + obj.right)/2), round(obj.top + 0.8*(obj.bottom -obj.top ))) 
        car_center.append(center) 
    return car_center

def findObjLane(objlist, lane_right_x,lane_right_y,lane_left_x,lane_left_y):
    # lane input
    objLane = []
    for obj in objlist:
        car_center = (round((obj.left + obj.right)/2), round(obj.top + 0.8*(obj.bottom -obj.top ))) 
        lane = jud_lane_which(lane_right_x,lane_right_y,lane_left_x,lane_left_y,car_center)
        objLane.append(lane)
    return objLane

# ==================================================================
def drawImg(frame, objlist, car_center,lane_left_x, lane_left_y, lane_right_x, lane_right_y):
    #drawCarCenter
    for obj in objlist:
        drawBox(frame,obj)
        # draw car center
        car_center = (round((obj.left + obj.right)/2), round(obj.top + 0.8*(obj.bottom -obj.top ))) 
        point_size = 1
        point_color = (0, 255, 0) # BGR
        thickness = 4 # 可以为 0 、4、8
        cv.circle(frame, car_center, point_size, point_color, thickness)
    
    #drawlane
    # 起点和终点的坐标
    point_color = (255, 0, 0) # BGR
    thickness = 1 
    lineType = 4
    cv.line(frame, (lane_left_x[0],lane_left_y[0]),  (lane_left_x[-1],lane_left_y[-1]),  point_color, thickness, lineType)
    cv.line(frame, (lane_right_x[0],lane_right_y[0]), (lane_right_x[-1],lane_right_y[-1]), point_color, thickness, lineType)
    
    for obj in objlist:
        drawBox(frame,obj)
        # draw car center
        car_center = (round((obj.left + obj.right)/2), round(obj.top + 0.8*(obj.bottom -obj.top ))) 
        point_size = 1
        point_color = (0, 255, 0) # BGR
        thickness = 4 # 可以为 0 、4、8
        cv.circle(frame, car_center, point_size, point_color, thickness)
    return frame  


def findObjLane(objlist, lane):
    # lane input
    objLane = []
    for obj in objlist:
        whichlane = jud_lane_which(lane, obj.center)
        objLane.append(whichlane)
    return objLane