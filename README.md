# 自动标注工具
自动识别视频中的目标

## 软硬件环境说明

- PYTHON :3.6
- OpenCV: 3.4.6.27
- 其中 python 是通过 Anaconda3 环境安装

## 使用方法

- 运行 demo_frame.py: 从‘test_list.csv’中读取要测试的图片名。运行目标识别和车道线识别算法。将目标识别结果存入‘obj_list.csv’中，将车道线结果存入‘lane_list.csv’中。

- 运行 multi_iou.py: 从‘obj_list.csv’中读取测试的 bounding box 结果，从‘labels.csv’中读取 bounding box的真值。计算每个目标的 IOU。

![img](/data/marked_img.png)

## 目录

- data 目录
 
测试图片,视频 

- weights 目录

yolov3 的网络结构及权重文件

## 核心文件

- test_list.csv: 待测试的图片名列表

- obj_list.csv：目标识别结果

<p>//framecout,id,type,left,top,right,bottom,confidence
0,0,person,3,197,205,547,0.9818541407585144<p>

- lane_list.csv：车道线识别结果

- iou_result.csv：测试结果与真值比较获得的IOU

- labels.csv：目标真值列表

- detector.py: 创建有一个 detector 对象。

<p>detect =
detector.detector("yolov3","weights/yolov3.cfg","weights/yolov3.weights","w
eights/coco.names")<p>

<p>objlist = detect.detect(frame)<p>

调用 detect 方法就可以得到 objlist,里面存放的是 Obj 对象。
然后就会记录结果到指定的 csv 文件。
