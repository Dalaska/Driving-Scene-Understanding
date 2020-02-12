import  cv2  as cv
import numpy as np
import sys
import argparse
import os
import detector
import csv
import object


# Draw the predicted bounding box
def drawBox(frame,obj):
    # Draw a bounding box.
    cv.rectangle(frame, (obj.left, obj.top), (obj.right, obj.bottom), (0, 0, 255))

    label = '%.2f' % obj.confidence

    # Display the label at the top of the bounding box
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(obj.top, labelSize[1])
    cv.putText(frame, label, (obj.left, obj.top), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))


def detect(args):

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

    detect = detector.detector("yolov3","weights/yolov3.cfg","weights/yolov3.weights","weights/coco.names")

    framecout = 0

    while cv.waitKey(1) < 0:

        # get frame from the video
        hasFrame, frame = cap.read()

        # Stop the program if reached end of video
        if not hasFrame:
            print("Done processing !!!")
            cv.waitKey(3000)
            break

        objlist = detect.detect(frame)

        for obj in objlist:
            drawBox(frame,obj)
            logwriter.writerow({'framecout':framecout,'id':obj.id,'type':obj.type,'left':obj.left,'top':obj.top,'right':obj.right,'bottom':obj.bottom,'confidence':obj.confidence})

        framecout += 1

        cv.imshow('detect',frame)
       

    #cv.destroyAllWindows()
    return objlist


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    #parser.add_argument("video", help="type the path of videos to detect", type=str)
    #parser.add_argument("logpath", help="the path of logfile", type=str)

    args = parser.parse_args()

    args.video = "data/camera.avi"
    args.logpath = "logs.csv"

    objlist = detect(args)
