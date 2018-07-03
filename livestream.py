import time
import matplotlib.pyplot as plt
import random
from drawnow import *
#xs=[-9,-8,-7,-6,-5,-4,-3-2,-1,0]
sensors = 4
x = dict([(s,[]) for s in range(0,sensors)])   # initialise dictionary of sensor stream values
def makePlot():
    plt.subplot(411)
    plt.plot(x[0],'r')
    plt.title('Live Streaming Sensor Data: Temperature')
    plt.grid(True)
    plt.ylabel('Temp C')
    plt.xlabel('Time')
    plt.subplot(412)
    plt.plot(x[1],'g')
    plt.title('Pressure')
    plt.grid(True)
    plt.ylabel('Pressure psi')
    plt.xlabel('Time')
    plt.subplot(413)
    plt.plot(x[2],'b')
    plt.title('Velocity')
    plt.grid(True)
    plt.ylabel('Velocity m/s')
    plt.xlabel('Time')
    plt.subplot(414)
    plt.plot(x[3],'c')
    plt.title('Distance')
    plt.grid(True)
    plt.ylabel('Distance m')
    plt.xlabel('Time')
    #wm = plt.get_current_fig_manager()
    #wm.window.state('zoomed')

for i in range(0,100):  #time
    time.sleep(0.001)
    for s in range(0,sensors):
        x[s].append(random.randint(20,80))

    for i in range(4):
        if len(x[i]) > 11:
            x[i].pop(0)
    #if len(x[s]) > 10:
        #x[s].pop(0)
    drawnow(makePlot)

