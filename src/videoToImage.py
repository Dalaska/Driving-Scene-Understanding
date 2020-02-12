# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 18:03:16 2019

@author: wangning
"""

import cv2
import glob
import os
from datetime import datetime
def video_to_frames(path):
    videoCapture = cv2.VideoCapture()
    videoCapture.open(path)
    # 帧率
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    # 总帧数
    frames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    print("fps=", int(fps), "frames=", int(frames))
    for i in range(int(frames)):
         ret, frame = videoCapture.read()
         cv2.imwrite("frames/%d.jpg"%(i), frame)
    return
'''
if __name__ == '__main__':
     t1 = datetime.now()
     video_to_frames("aa.mp4")
     t2 = datetime.now()
     print("Time cost = ", (t2 - t1))
     print("SUCCEED !!!")
'''
def frames_to_video(fps, save_path, frames_path, max_index):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    videoWriter = cv2.VideoWriter(save_path, fourcc, fps, (960, 544))
    imgs = glob.glob(frames_path + "/*.jpg")
    frames_num = len(imgs)
    for i in range(max_index):
        if os.path.isfile("%s/%d.jpg"%(frames_path, i)):
            frame = cv2.imread("%s/%d.jpg"%(frames_path, i))
            videoWriter.write(frame)
    videoWriter.release()
    return

if __name__ == '__main__':
        t1 = datetime.now()
        frames_to_video(15, "result.mp4", 'out', 570)
        t2 = datetime.now()
        print("Time cost = ", (t2 - t1))
        print("SUCCEED !!!")


