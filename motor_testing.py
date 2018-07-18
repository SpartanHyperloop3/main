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

motor_position(motor0)
readIIT0()
readIIT1()
readIIT2()
readIIT3()
readErrorFlags0()
readErrorFlags1()
readErrorFlags2()
readErrorFlags3()
readModule0Runtime()
readModule1Runtime()
readModule2Runtime()
readModule3Runtime()
readBoard0Voltage()
readBoard1Voltage()
readBoard2Voltage()
readBoard3Voltage()
readBoard0Temp()
readBoard1Temp()
readBoard2Temp()
readBoard3Temp()
readMotor0Current()
readMotor1Current()
readMotor2Current()
readMotor3Current()
readMotor0Pos()
readMotor1Pos()
readMotor2Pos()
readMotor3Pos()
readMotor0RPM()
readMotor1RPM()
readMotor2RPM()
readMotor3RPM()

time.sleep(5)          ##pause 5seconds
motor0.send(3,0,0,0)   ##motorstop
motor1.send(3,0,0,0)   ##motorstop