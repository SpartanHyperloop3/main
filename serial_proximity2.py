# Filename: proximityTest.py
# from the terminal: Run the following command to do direct sercom connection
#                    sudo minicom -b 9600 -o -D /dev/ttyAMA0
from time import sleep
import proxModule as ultrasonic
import numpy as np

serialPort = "/dev/ttyAMA0"
maxRange = 1000  # EZ4
minRange = 300
sleepTime = 0.01  # delay, reduce to like 0.05 or 0.01, just play around with it..
minMM = 9999  # init min reading
maxMM = 0  # init max reading
# array5 = [0]*100;
size = 5
array5 = np.zeros(size)
avg5 = 0
stepCounter = 0


def movingAvg100(reading):
    global avg5, array5, stepCounter  # global declarator
    if (stepCounter == size):
        avg5 = np.average(array5)
        stepCounter += 1

    if (stepCounter > size):  # isPopulated?
        # if (abs(avg5-reading) <= 25):            # Error filter, if reading is off too much... like 25mm + or w/e you can choose
        array5 = np.delete(array5, 0)  # pop sequence
        array5 = np.append(array5, reading)  # push sequence
        avg5 = np.average(array5)  # update moving avg

    else:  # init
        # array5[stepCounter++] = reading          # classic python... no support for int++
        array5[stepCounter] = reading
        stepCounter += 1


while True:
    readout = ultrasonic.measure(serialPort)
    movingAvg100(readout)
    # Limit catcher
    if avg5 == 0:
        print("Calibrating... %5d of %5d" % (stepCounter, size))
        sleep(sleepTime)
        continue

    if readout >= maxRange:
        print("Out of Range (MAX) [%9.2f]" % readout)
        sleep(sleepTime)
        continue

    if readout <= minRange:
        print("Out of Range (MIN) [%9.2f]" % readout)
        sleep(sleepTime)
        continue

    # Record updater
    if avg5 < minMM:
        minMM = avg5
    if avg5 > maxMM:
        maxMM = avg5

    print("distance: %9.2f    min: %9.2f    max: %9.2f" % (avg5, minMM, maxMM))
    # print("%9.2f (%9.2f cm)" % (avg5, avg5/10) )
    sleep(sleepTime)