# save scene data into csv
from testcase import Scene

video_id = 'DR2330322'
time_start = 11.1
time_end = 20.5
tag = ['ACC','目标误识别',]
desc = '' # description

scene = Scene(video_id,time_start,time_end,tag,desc)
scene.save('scene_log.csv')

pass