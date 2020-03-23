# save scene data into csv
import pandas as pd
import csv

class Scene():
    def __init__(self,video_id,time_start,time_end,tag):
        self.video_id = video_id
        self.time_start = time_start
        self.time_end = time_end
        self.id = hash(str(time_start+time_end))
        self.tags = tags
    def save(self,file_path):
        data ={'id':[self.video_id],'time_start':[self.time_start],'time_end':[self.time_end],'tags':[self.tags]}
        frame = pd.DataFrame(data)
        frame.to_csv(file_path,index=False,header=False)#不将索引和列名写入数据

video_id = 'DR20110322'
time_start = 11.1
time_end = 20.5
tags = ['ni_guang','cam_jump']

scene = Scene(video_id,time_start,time_end,tags)
scene.save('log.csv')

pass
