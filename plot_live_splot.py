import matplotlib.pyplot as plt
import random

#jsontemp = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
jsontemp = []
for k in range(100):
    jsontempp = random.randint(30,80)
    jsontemp.append(jsontempp)

plotpp = []
for j in range(100):
    jsonp = random.randint(100,180)
    plotpp.append(jsonp)
#print(plotpp)
jsontime = [-4,-3,-2,-1,0]
print(len(jsontemp))

ploty=[]
plotp=[]
f, axarr = plt.subplots(1, 1)

for i in jsontemp:
    ploty.append(i)
    #plotp.append(p)
    if len(ploty) > 5:
        ploty.pop(0)
        #print(ploty)
        plt.ylim(30, 80)  # Set y min and max values
        plt.xlim(-4,1)
        plt.title('Live Streaming Sensor Data: Temperature')
        plt.grid(True)
        plt.ylabel('Temp C')  # Set ylabels
        plt.xlabel('Time')
        plt.plot(jsontime,ploty,label='Degrees C')
        #axarr[0,1].plot(jsontime,plotp,label='Pressure psi')
        plt.legend(loc='upper left')  # plot the legend
        plt.pause(0.2)
        plt.clf()
        #plt.show()
    #print(ploty)


"""
axarr[0, 0].plot(x, y)
axarr[0, 0].set_title('Axis [0,0]')
axarr[0, 1].scatter(x, y)
axarr[0, 1].set_title('Axis [0,1]')
axarr[1, 0].plot(x, y ** 2)
axarr[1, 0].set_title('Axis [1,0]')
axarr[1, 1].scatter(x, y ** 2)
axarr[1, 1].set_title('Axis [1,1]')"""