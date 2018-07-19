import sys
sys.path.append("/home/pi/.local/lib/python2.7/site-packages")
from struct import *
from serial import Serial
from math import exp, expm1
import TMCL
from motor_drivers import *
import time

motor0Param() ##initialize motor0
motor1Param() ##initialize motor1
motor2Param()
motor3Param()


fwd()

i = 0
while i < 60:
    readMotor0RPM()
    readMotor1RPM()
    readMotor2RPM()
    readMotor3RPM()

    time.sleep(0.1)
    i = i + 1
    
rev()