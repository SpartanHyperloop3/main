import numpy as np
import matplotlib.pyplot as plt
import random
from drawnow import *
plt.axis([0, 10, 0,65])
cnt = 0
ys=[]
for j in range(100):
    ysj=random.randint(10,60)
    ys.append(ysj)
print(ys)


def makeFig():  # Create a function that makes our desired plot
    plt.ylim(0, 90)  # Set y min and max values
    plt.title('My Live Streaming Sensor Data')  # Plot the title
    #plt.grid(True)  # Turn the grid on
    plt.ylabel('Temp C')  # Set ylabels
    plt.plot(tempy, 'ro-', label='Degrees C')  # plot the temperature
    plt.legend(loc='upper left')  # plot the legend


for k in ys:
    tempy=[]
    tempy.append(k)
    drawnow(makeFig)
    print(tempy)
    for i in tempy:
        # y = np.random.random()
        plt.scatter(i, tempy)
        plt.pause(0.5)

    #plt.show()
    cnt = cnt + 1
    if (cnt > 10):  # If you have 10 or more points, delete the first one from the array
        tempy.pop(0)  # This allows us to just see the last 10 data points
    #print(tempy)

