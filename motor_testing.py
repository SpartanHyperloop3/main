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

readIIT0()
readIIT1()
##readIIT2()
##readIIT3()
readErrorFlags0()
readErrorFlags1()
##readErrorFlags2()
##readErrorFlags3()
readModule0RunTime()
readModule1RunTime()
##readModule2Runtime()
##readModule3Runtime()
readBoard0Voltage()
readBoard1Voltage()
##readBoard2Voltage()
##readBoard3Voltage()
readBoard0Temp()
readBoard1Temp()
##readBoard2Temp()
##readBoard3Temp()
readMotor0Current()
readMotor1Current()
##readMotor2Current()
##readMotor3Current()
readMotor0Pos()
readMotor1Pos()
##readMotor2Pos()
##readMotor3Pos()

i = 0
while i < 50:
    readMotor0RPM()
    readMotor1RPM()
    ##readMotor2RPM()
    ##readMotor3RPM()

    time.sleep(0.1)
    i = i + 1

motor0.send(3,0,0,0)   ##motorstop
motor1.send(3,0,0,0)   ##motorstop