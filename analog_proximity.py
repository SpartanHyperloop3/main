import smbus
import time

device_address = 0x6a
read_register = 48

bus = smbus.SMBus(1)
bus.pec = True

# per calibration and testing,
#   0.2717V  <= 30CM range.
#   0.8745V  ~= 100CM range.
#
# Recommendation: Redo testing... make sure it's calibrated until it
#   is as accurate as needed. Recalibrate for every sensor.
#   Preferrably with in uV level (6-7 digits past decimal point)

#   eg. minSens1, minSens2, minSens3, minSens4
#       maxSens1, maxSens2, maxSens3, maxSens4
#   over 1 meter range calibration

#   NOTE: The 0 mark starts at the PCB BOARD. Not at the lid of the
#         emitter.

#   This has to be manually calibrated as we can't remove
#   the sensors off the pod during initialization sequence.
#

#   Works but it seems like it flickers 2mm every 3-4 readings... you can
#   see it... use a moving average of 5 or 10 readings with
#   pop and append. Check the debugging script in serial i sent you.


# minSens <= 30CM
# maxSens = 100CM
minSens1 = 0.2717
maxSens1 = 0.8745

minSens2 = 0
maxSens2 = 0

minSens3 = 0
maxSens3 = 0

minSens4 = 0
maxSens4 = 0
correlationValue = [0] * 4

sensor1 = [minSens1, maxSens1]
sensor2 = [minSens2, maxSens2]
sensor3 = [minSens3, maxSens3]
sensor4 = [minSens4, maxSens4]


def read():
    bus.read_i2c_block_data(device_address, read_register)
    time.sleep(0.001)
    return bus.read_i2c_block_data(device_address, read_register)


def convert():
    reading = read()
    upper = (reading[0] & 15)
    upper = (upper << 8)
    total = upper + reading[1]
    voltage = float(total * .001)
    voltageDivider = 6.8 / (6.8 + 10)
    return voltage / voltageDivider


# Let sensor be a list of 2 values: minSens, maxSens
def map(sensor, reading):
    zeroReading = reading - sensor[0]  # zero out the reading
    if (zeroReading <= 0):
        return 0  # why? It's out of range, unreliable value.
    else:
        mapValue = reading / 4.444015
        result = mapValue * 5000  # 5000mm max range
        # 4.444015 seems to be like the max value, past 5000mm

        # Comment this out if you need to operate past 1m range.
        # thi is just to keep glitches out since we won't need
        # data past 1m anyway.
        if (result >= 1000):
            return 1000.000000
        else:
            return result


while (True):
    time.sleep(0.05)
    print(map(sensor1, convert()))
    time.sleep(0.05)
#   print("ADC TEST")