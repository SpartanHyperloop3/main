import sys
sys.path.append("/home/pi/.local/lib/python2.7/site-packages")
from struct import *
from serial import Serial
from math import exp, expm1
import TMCL
from motor_drivers import *
import time

motor0.send(5,31,0,0)
motor1.send(5,31,0,0)
motor2.send(5,31,0,0)
motor3.send(5,31,0,0)

motor0Param() ##initialize motor0
motor1Param() ##initialize motor1
motor2Param()
motor3Param()

fwdtest()
readIIT0()
readIIT1()
readIIT2()
readIIT3()
readErrorFlags0()
readErrorFlags1()
readErrorFlags2()
readErrorFlags3()
readModule0RunTime()
readModule1RunTime()
readModule2RunTime()
readModule3RunTime()
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

time.sleep(5)
    
motor0.send(3,0,0,0)   ##motorstop
motor1.send(3,0,0,0)   ##motorstop
motor2.send(3,0,0,0)
motor3.send(3,0,0,0)

time.sleep(1)
revtest()

readIIT0()
readIIT1()
readIIT2()
readIIT3()
readErrorFlags0()
readErrorFlags1()
readErrorFlags2()
readErrorFlags3()
readModule0RunTime()
readModule1RunTime()
readModule2RunTime()
readModule3RunTime()
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

time.sleep(5)

motor0.send(3,0,0,0)   ##motorstop
motor1.send(3,0,0,0)   ##motorstop
motor2.send(3,0,0,0)
motor3.send(3,0,0,0)