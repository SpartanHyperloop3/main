import threading
from threading import Thread
import time
from multiprocessing import Process
import sys

import matplotlib.pyplot as plt
import random

jsontimea = [-9,-8,-7,-6,-5,-4,-3,-2,-1,0]
jsontimeb = [-9,-8,-7,-6,-5,-4,-3,-2,-1,0]

def plot_temp_a():
    jsontempa = []
    ay = []
    for k in range(100):
        jsontempaval = random.randint(30, 80)
        jsontempa.append(jsontempaval)
        print(len(jsontempa))

    for i in jsontempa:
        ay.append(i)
        #plt.subplot(211)
        if len(ay) > 10:
            ay.pop(0)
            plt.subplot(211)
            plt.ylim(30, 80)
            plt.xlim(-9, 1)
            plt.title('Live Streaming Sensor Data: Temperature')
            plt.grid(True)
            plt.ylabel('Temp C')
            plt.xlabel('Time')
            plt.plot(jsontimea, ay, label='Degrees C')
            plt.pause(0.3)
            plt.clf()


def plot_press_b():
    jsonpressb = []
    by = []
    for j in range(100):
        jsonpressbval = random.randint(50, 100)
        jsonpressb.append(jsonpressbval)


    for l in jsonpressb:
        by.append(l)
        #plt.subplot(212)
        if len(by) > 10:
            by.pop(0)
            plt.subplot(212)
            plt.ylim(45, 105)
            plt.xlim(-9, 1)
            plt.title('Live Streaming Sensor Data: Pressure b')
            plt.grid(True)
            plt.ylabel('Pressure psi')
            plt.xlabel('Time')
            plt.plot(jsontimeb, by, label='psi')
            plt.pause(0.5)
            plt.clf()



if __name__ == '__main__':
    p1 = Process(target=plot_temp_a)
    p1.start()
    p2 = Process(target=plot_press_b)
    p2.start()


    """
    Thread(target = plot_temp_a).start()
    Thread(target = plot_press_b).start()"""