import struct
import time
import serial
import binascii

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0)


for _ in range(0,4):
    ser.write('\x01\x14\x00\x2f')
    time.sleep(0.01)
    result = ser.read(20)

    try:
        data = struct.unpack('<xxfxx', result)[0]
    except:
        data = 0

    print data
    time.sleep(0.01)

