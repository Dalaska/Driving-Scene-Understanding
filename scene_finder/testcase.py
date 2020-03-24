import pandas as pd

class Scene():
    def __init__(self,video_id,time_start,time_end,tag,desc):
        self.video_id = video_id
        self.time_start = time_start
        self.time_end = time_end
        self.tag = tag
        self.desc = desc
    def save(self,file_path):
        data ={'video_id':[self.video_id],\
               'time_start':[self.time_start],\
               'time_end':[self.time_end],\
               'tag':[self.tag],\
               'desc':[self.desc]}   
        frame = pd.DataFrame(data) # make pandas data frame
        frame.to_csv(file_path, mode='a',index = False,\
            header = False, encoding = "gb2312")#不将索引和列名写入数据 # 追加写入

class Testcase():
    def __init__(self,test,dat):
        self.test = test
        self.dat = dat

    # show test        
    def show_test(self):
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
        print('.test_case')
        for key1 in list(self.test.keys()):
            print('├──',key1)
            for key2 in list(self.test[key1].keys()):
                print('│  ',' └──',key2)
                for scene3 in self.test[key1][key2]:
                    print('│       ',' └──',scene3.video_id,\
                        scene3.time_start,'-',scene3.time_end,scene3.tag,scene3.desc)
    
        # get test list
    def get_testlist(self):
        test_list = [] 
        test_videoid = []
        for key1 in list(self.test.keys()):
            for key2 in list(self.test[key1].keys()):
                for elem3 in self.test[key1][key2]:
                    test_list.append(elem3)
                    test_videoid.append(elem3.video_id)
        return(test_list,test_videoid)  
  

