
import pandas as pd

class Scene():
    def __init__(self,video_id,time_start,time_end,tags,description):
        self.video_id = video_id
        self.time_start = time_start
        self.time_end = time_end
        self.id = hash(str(time_start+time_end))
        self.tags = tags
        self.description = description
    def save(self,file_path):
        data ={'id':[self.video_id],'time_start':[self.time_start],\
               'time_end':[self.time_end],'tags':[self.tags],\
               'description':description}
        frame = pd.DataFrame(data)
        frame.to_csv(file_path, mode='a',index=False,encoding="gb2312")#不将索引和列名写入数据 # 追加写入

# ==========================================================

# save scene data into csv
video_id = 'DR2330322'
time_start = 11.1
time_end = 20.5
tags = ['ACC','目标误识别',]# 'AEB','straight'
description = 'good dat'

scene = Scene(video_id,time_start,time_end,tags,description)
scene.save('log.csv')

pass
