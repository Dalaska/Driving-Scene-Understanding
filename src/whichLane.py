#车道
#车
#input
#output
#比较x,y的位置

from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt

# object input
car_center = np.array([200, 100])

# lane input
lane_x = np.array([300, 180, 50])
lane_y = np.array([1, 50, 150])

# plot
#from matplotlib.figure import Figure
#from matplotlib.backends.backend_agg import FigureCanvasAgg

#fig = Figure(figsize=[6,6])
#ax = fig.add_axes([.1,.1,.8,.8])

#canvas = FigureCanvasAgg(fig)
plt.plot(lane_x, lane_y) 
plt.plot(car_center[0],car_center[1],  color="r",marker="*")
#plt.plot(x, y, color="r", linestyle="--", marker="*", linewidth=1.0)

#plt.show()
#ax.scatter(car_center[0],car_center[1], marker="*")


#plt.savefig("test.png", dpi=120)
# plot函数作图


# interpolate
#x = np.linspace(0, 10, num=11, endpoint=True)
#y = np.cos(-x**2/9.0)
f = interp1d(lane_x, lane_y)
new_x = f(car_center[1])
plt.plot(new_x, car_center[1],  color="g",marker="*")
#type(car_pos)

# decide whitch lane


# outuput text


# config
# 添加路径，选择哪个文件读取， 运行， 类型setup
# 图片和车道自己实现一遍，这样可以问问题
# 目标识别训练的部分

