import sys
sys.path.append("/home/pi/.local/lib/python2.7/site-packages")
from struct import *
from serial import Serial
from math import exp, expm1
import TMCL
from motorcontrol import *
import time

motor0Param()
motor1Param()

motor0.send(1,0,0,500)
motor1.send(1,0,0,500)
time.sleep(5)
motor0.send(3,0,0,0)
motor1.send(3,0,0,0)