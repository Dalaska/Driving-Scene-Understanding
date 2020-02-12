from multi_iou import multi_iou,find_objlist
import pandas as pd
import argparse,sys, os, csv

file = pd.read_csv("labels.csv")
xmin = file['xmin']
xmax = file['xmax']
ymin = file['ymin']
ymax = file['ymax']
frame = file['Frame']
label = file['Label']

# read csv
file2 = pd.read_csv("test_result.csv")
left = file2['left']
top = file2['top']
right = file2['right']
bottom = file2['bottom']
frame_test = file2['framecout']

# read frame name 
frame_name = '1479498890501073948.jpg'


blist_true = find_objlist(frame_name,frame,xmin, xmax, ymin, ymax)
blist_test = find_objlist(frame_name,frame_test, left, top,right,  bottom) # need fix order


iou_list = multi_iou(blist_true,blist_test)

pass