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