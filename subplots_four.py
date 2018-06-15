import time
import matplotlib.pyplot as plt
import random
from drawnow import *

sensors = 4
x = dict([(s,[]) for s in range(0,sensors)])   # initialise dictionary of sensor stream values
def makePlot():
    plt.subplot(411)
    plt.plot(x[0],'r')
    plt.subplot(412)
    plt.plot(x[1],'g')
    plt.subplot(413)
    plt.plot(x[2],'b')
    plt.subplot(414)
    plt.plot(x[3],'c')


for i in range(0,100):  #time
    time.sleep(0.1)
    for s in range(0,sensors):
        x[s].append(random.randint(20,80))
    drawnow(makePlot)

