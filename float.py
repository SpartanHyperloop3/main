import sys
import time
import binascii

data = '\x42\x86\xc0\xde'

def float32(dataIn):
    hex = binascii.hexlify(data)
    num = int(hex, 16)
    sign = (num & 0x80000000) >> 31
    exp = computeExponent(num)
    fraction = computeFraction(num)
    if sign == 1:
        result = -(2**exp * fraction)
    else:
        result = 2**exp * fraction

    return result



def computeExponent(dataIn):
    exp = dataIn & 0x7f800000
    exp = exp >> 23
    exp = exp - 127
    return exp

def computeFraction(dataIn):
    result = 0.0
    bitmask = 0x400000
    for i in range(1,22):
        if dataIn & bitmask == bitmask:
            result += 2**-i
        bitmask = bitmask >> 1
    result = 1 + result
    return result




print float32(data)
