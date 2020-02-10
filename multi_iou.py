import pandas as pd
import csv


def find_objlist(frame_name,frame,xmin, xmax, ymin, ymax):
    box_list =[]
    for i in range(len(frame)):  # traverse test list frame
        if frame[i] == frame_name: 
        # create new bbox list when frame name changed         
            bbox = [xmin[i], xmax[i], ymin[i], ymax[i]]
            box_list.append(bbox)
    return box_list

def intersection_over_union(boxA, boxB):  #first_point为真值，last_point为测试值
    """
    # determine the (x, y)-coordinates of the intersection rectangle 
    args:
    returns:
    """
    xA = max(boxA[0], boxB[0])  
    yA = max(boxA[1], boxB[1]) 
    xB = min(boxA[2], boxB[2])   
    yB = min(boxA[3], boxB[3])
    
    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    # compute the area of both the prediction and ground-truth
    # rectangles 
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
    # compute the intersection over union by taking the intersection 
    # area and dividing it by the sum of prediction + ground-truth  
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
    #iou = interArea / float(boxAArea)
    # return the intersection over union value  
    return iou

def multi_iou(blist_true,blist_test):
    iou_list = []
    for i in range(len(blist_test)):
        obj_test = blist_test[i]
        iou_max = 0
        for j in range(len(blist_true)):
            obj_true = blist_true[j]
            iou = intersection_over_union(obj_true, obj_test)
            iou_max = max(iou,iou_max) # find best match
        iou_list.append(iou_max)
    return iou_list

if __name__ == '__main__':
    # read ground truth
    file = pd.read_csv("labels.csv")
    xmin = file['xmin']
    xmax = file['xmax']
    ymin = file['ymin']
    ymax = file['ymax']
    frame = file['Frame']
    label = file['Label']

    # read csv
    file2 = pd.read_csv("obj_list.csv")
    left = file2['left']
    top = file2['top']
    right = file2['right']
    bottom = file2['bottom']
    frame_test = file2['framecout']

    # load test list
    file = pd.read_csv("test_list.csv")
    frame_list = file['Frame']
    header1 = True # write first row

    for i in range(len(frame_list)):
        frame_name = frame_list[i]
        #frame_name = '1479498890501073948.jpg'
        blist_true = find_objlist(frame_name,frame,xmin, xmax, ymin, ymax)
        blist_test = find_objlist(frame_name,frame_test, left, top,right,  bottom) # need fix order

        #obj_true = blist_true[0]
        #obj_test = blist_test[0]
        #iou = intersection_over_union(obj_true, obj_test)
        try:
            iou_list = multi_iou(blist_true,blist_test)
        except:
            pass

        # write objlist in csv file
        fieldnames = ['frame','id','iou']
        with open('iou_result.csv', mode='a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if header1:
                writer.writeheader()
                header1 = False
            for i in range(len(iou_list)):
                # write csv
                writer.writerow({'frame':frame_name,'id':i,'iou':iou_list[i]})

pass