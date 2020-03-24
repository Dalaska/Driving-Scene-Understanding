# create test
import pandas as pd
from testcase import Testcase

reg_test = {'ACC':{'跟随前车':[],\
                   '前车切出':[],\
                   '前车切出':[]},\
            'AEB':{'车辆':[],\
                   '行人':[]},\
            'LKA':{'直道':[],\
                   '弯道':[]},}

# read csv
dat = pd.read_csv("scene_log.csv",encoding = "gb2312") 
dat.head() # show dat
# create test case
testcase1 = Testcase(reg_test,dat) 
testcase1.show_test() # 测试目录可视化
testcase1.add_scene2test() #将加入场景加入测试目录
testcase1.show_testcase() # 测试案例可视化
test_list,test_videoid = testcase1.get_testlist() # 生成测试案例list

# save test list
df_testvideo = pd.DataFrame(test_videoid) 
file_path = 'test_list.csv'
df_testvideo.to_csv(file_path,index=False,header=False)

pass