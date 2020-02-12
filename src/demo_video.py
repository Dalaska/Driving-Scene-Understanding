# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 10:14:35 2019

@author: dalaska
"""
import  cv2  as cv
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import argparse,sys, os, csv

from lanenet_label.lanenet_detector import lanenet_detector

class Obj:
    # road obj
    def __init__(self,id,type,top,left,right,bottom,confidence):
        self.id = id
        self.type = type
        self.top = top
        self.left = left
        self.right = right
        self.bottom = bottom
        self.confidence = confidence
        self.center = (round((left + right)/2), round(top + 0.8*(bottom - top )))# car center
        self.objlane = 'UNDECIDED'
        
    def print(self):
        pass

    def getObjLane(self, lane):
        # find witch lane the object is in
        '''
        还需要输入数据合法性检查
        '''
        car_center = self.center
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
            self.objlane = 'UNDECIDED'
        else:
                
            f_right = interp1d(lane.right_y, lane.right_x,'linear')
            f_left = interp1d(lane.left_y, lane.left_x,'linear')
            x_right = f_right(m)
            x_left  = f_left(m)
            if n>x_right:
                print("RIGHT")
                plt.plot(car_center[0],car_center[1],  color="k",marker="*")
                plt.plot(x_right, car_center[1],  color="m",marker="*")
                self.objlane = 'RIGHT'  #右车道
            elif n<=x_right and n>x_left:
                print("EGO")
                plt.plot(car_center[0],car_center[1],  color="r",marker="*")
                plt.plot(x_right, car_center[1],  color="m",marker="*")
                plt.plot(x_left, car_center[1],  color="b",marker="*")
                self.objlane = 'EGO'  #本车道
            else:
                print("LEFT")
                plt.plot(car_center[0],car_center[1],  color="y",marker="*")
                plt.plot(x_left, car_center[1],  color="b",marker="*")
                self.objlane = 'LEFT'   #左车道        
   
class Lane:
    # lane object
    def __init__(self,lx,ly,rx,ry):
        self.left_x = lx
        self.left_y = ly
        self.right_x = rx
        self.right_y = ry
        
class ObjDetector:
    def __init__(self,backend,cfgfile,weights,labels):


        self.backend = backend
        self.cfgfile = cfgfile
        self.weights = weights

        # Initialize the parameters
        self.confThreshold = 0.5  # Confidence threshold
        self.nmsThreshold = 0.4  # Non-maximum suppression threshold
        self.inpWidth = 416  # Width of network's input image
        self.inpHeight = 416  # Height of network's input image

        # Load names of classes
        self.classesFile = labels
        self.classes = None
        with open(self.classesFile, 'rt') as f:
            self.classes = f.read().rstrip('\n').split('\n')

        self.net = cv.dnn.readNetFromDarknet(self.cfgfile, self.weights)
        self.net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

    # Get the names of the output layers
    def getOutputsNames(self):
        # Get the names of all the layers in the network
        layersNames = self.net.getLayerNames()
        # Get the names of the output layers, i.e. the layers with unconnected outputs
        return [layersNames[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    # Remove the bounding boxes with low confidence using non-maxima suppression
    def postprocess(self,frame, outs):
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]

        classIds = []
        confidences = []
        boxes = []
        # Scan through all the bounding boxes output from the network and keep only the
        # ones with high confidence scores. Assign the box's class label as the class with the highest score.
        classIds = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.confThreshold:
                    center_x = int(detection[0] * frameWidth)
                    center_y = int(detection[1] * frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])

        # Perform non maximum suppression to eliminate redundant overlapping boxes with
        # lower confidences.
        indices = cv.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)

        objlists = []
        for index,i in enumerate(indices):
            i = i[0]
            box = boxes[i]

            obj = Obj(index,"",box[1],box[0],box[2]+box[0],box[3]+box[1],confidences[i]);

            if self.classes:
                assert (classId < len(self.classes))
                obj.type = self.classes[classIds[classId]]

            objlists.append(obj)

        return objlists


    def detect(self,frame):

        # Create a 4D blob from a frame.
        blob = cv.dnn.blobFromImage(frame, 1 / 255, (self.inpWidth, self.inpHeight), [0, 0, 0], 1, crop=False)

        # Sets the input to the network
        self.net.setInput(blob)

        # Runs the forward pass to get output of the output layers
        outs = self.net.forward(self.getOutputsNames())

        # Remove the bounding boxes with low confidence
        objlists = self.postprocess(frame, outs)

        # Put efficiency information. The function getPerfProfile returns the
        # overall time for inference(t) and the timings for each of the layers(in layersTimes)
        t, _ = self.net.getPerfProfile()
        label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
        cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

        return objlists


def detectImg(args):

    if (args.video):
        # Open the video file
        if not os.path.isfile(args.video):
            print("Input video file ", args.video, " doesn't exist")
            sys.exit(1)
        cap = cv.VideoCapture(args.video)
    else:
        # Webcam input
        cap = cv.VideoCapture(0)

    if (args.logpath):
        fieldsname = ['framecout','id','type','left','top','right','bottom','confidence']
        logfile = open(args.logpath,'w')
        logwriter = csv.DictWriter(logfile,fieldnames=fieldsname)

    framecout = 0

    while cv.waitKey(1) < 0:

        # get frame from the video
        hasFrame, frame = cap.read()

        # Stop the program if reached end of video
        if not hasFrame:
            print("Done processing !!!")
            cv.waitKey(3000)
            break

        # detect object
        objlist = args.obj_detector.detect(frame)
        
        # find lane
        img,laneList = args.lane_detector.detect_img(img = frame)
        #lane = findLane(laneList)
   
        # find obj in which lane
        for obj in objlist:
           #obj.getObjLane(lane)

        for obj in objlist:
           drawBox(frame,obj)
           # draw object center
           # cv.circle(frame, obj.center, radius = 1, color = (0,255,0), thickness = 4)
           # write csv
           logwriter.writerow({'framecout':framecout,'id':obj.id,'type':obj.type,'left':obj.left,'top':obj.top,'right':obj.right,'bottom':obj.bottom,'confidence':obj.confidence})

        #drawlane
        #frame = drawLane(frame,lane)
        frame = cv.resize(frame, (512, 256), interpolation=cv.INTER_LINEAR)
        for line in laneList:
            xa, ya, xb, yb = line[1]
            cv.line(frame, (xa, ya), (xb, yb), (255, 0, 0), 2)
    
            
        framecout += 1

        cv.imshow('detect',frame)
       

    cv.destroyAllWindows()
    return objlist

def drawLane(frame,lane):
    #drawlane
    # 起点和终点的坐标
    point_color = (255, 0, 0) # BGR
    thickness = 1 
    lineType = 4
    cv.line(frame, (lane.left_x[0],lane.left_y[0]),  (lane.left_x[-1],lane.left_y[-1]),  point_color, thickness, lineType)
    cv.line(frame, (lane.right_x[0],lane.right_y[0]), (lane.right_x[-1],lane.right_y[-1]), point_color, thickness, lineType)
    return frame

def findLane(laneList):
    # test case
    
    lane_left_x = np.array([50, 300, 500])
    lane_left_y = np.array([600, 500, 400])
    lane_right_x = np.array([650, 800, 950])
    lane_right_y = np.array([400, 500, 600])
    '''
    lane_left_x = np.array([laneList[1][1][0], laneList[1][1][2]]) # right lane
    lane_left_y = np.array([laneList[1][1][1], laneList[1][1][3]])
    lane_right_x = np.array([laneList[3][1][0], laneList[3][1][2]]) # left lane
    lane_right_y = np.array([laneList[3][1][1], laneList[3][1][3]])    
    lane = Lane(lane_left_x,lane_left_y,lane_right_x,lane_right_y)
    ''''
    return lane

# Draw the predicted bounding box
def drawBox(frame,obj):
    # Draw a bounding box.
    cv.rectangle(frame, (obj.left, obj.top), (obj.right, obj.bottom), (0, 0, 255))

    label = '%.2f' % obj.confidence

    # Display the label at the top of the bounding box
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(obj.top, labelSize[1])
    cv.putText(frame, label, (obj.left, obj.top), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
    
# ==================================== test case ======================================================
# setting
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    args.video = "data/20190326_3.mp4"
    args.logpath = "data/logs.csv"
    args.obj_detector = ObjDetector("yolov3","weights/yolov3.cfg","weights/yolov3.weights","weights/coco.names")
    args.lane_detector = lanenet_detector()
    # choose lane detector
    objlist, lane = detectImg(args)

