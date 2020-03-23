import pandas as pd
from scene import Scene

class Testcase():
    def __init__(self,test,dat):
        self.test = test
        self.dat = dat

    # show test        
    def test_content(self):
        print('.test')
        for key1 in list(self.test.keys()): # 一级目录
            print('├──',key1)
            for key2 in list(self.test[key1].keys()): # 二级目录
                print('│  ',' └──',key2)
    
    # add_scene2test
    def add_scene2test(self):
        for row in self.dat.iterrows():
            # get data
            video_id = row[1][ 'video_id']
            time_start = row[1][ 'time_start']
            time_end = row[1][ 'time_end']
            tag = eval(row[1][ 'tag'])# 输出每一行
            desc = row[1][ 'desc']
            scene = Scene(video_id, time_start, time_end,\
                        tag,desc)  
            # add scne to test case  
            for key1 in list(self.test.keys()): # 一级目录
                for key2 in list(self.test[key1].keys()): # 二级目录
                    tag_needed = [key1,key2]
                    if set(tag_needed) <= set(scene.tag): # has all requiredd tags
                        self.test[key1][key2].append(scene)
        
    # show test case
    def show_testcase(self):
        print('.test_data')
        for key1 in list(self.test.keys()):
            print('├──',key1)
            for key2 in list(self.test[key1].keys()):
                print('│  ',' └──',key2)
                for scene3 in self.test[key1][key2]:
                    print('│       ',' └──',scene3.video_id,\
                        scene3.time_start,'-',scene3.time_end,scene3.tag,scene3.desc)
  

#=========================================
reg_test = {'ACC':{'目标误识别':[],\
              '弯道':[]},\
            'AEB':{'车辆':[],\
                '行人':[]}}
# read csv
dat = pd.read_csv("log.csv",encoding = "gb2312") 

testcase1 = Testcase(reg_test,dat)
testcase1.test_content()
testcase1.add_scene2test()
testcase1.show_testcase()
pass