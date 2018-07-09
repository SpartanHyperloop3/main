import sys
import time
import binascii

data = '\xaa\x14\xa2\x05\x86\x42\xf9\xfa'
#data = '\xaa\x14\x42\x86\x05\xa2'

def sliceData(dataIn, start, end):
    hex = binascii.hexlify(dataIn)
    cut = hex[start:end]
    end = len(cut)
    
    cut1 = cut[0:2]
    cut2 = cut[2:4]
    cut3 = cut[4:6]
    cut4 = cut[6:8]
    
    result = cut4 + cut3 + cut2 + cut1
    return result


def float32(dataIn):
    num = int(dataIn, 16)
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




#print float32(data)

final = sliceData(data, 4, 12)

print float32(final)
