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

motor0.send(1,0,0,500) ##rotate right 500rpm
motor1.send(1,0,0,500) ##rotate right 500rpm
time.sleep(5)          ##pause 5seconds
motor0.send(3,0,0,0)   ##motorstop
motor1.send(3,0,0,0)   ##motorstop