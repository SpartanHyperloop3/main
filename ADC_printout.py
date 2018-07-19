'''
import smbus
import time
import numpy as np

class ADC(smbus):

    def __init__(self, device_address, read_register):
        smbus.__init__(self, 1)
        self.pec = True
        self.deviceAddress = device_address
        self.readRegister = read_register

    def read_i2c_block_data(self):
        super(ADC, self).read_i2c_block_data(self.deviceAddress, self.readRegister)
        time.sleep(0.001)
        return super(ADC, self).read_i2c_block_data(self.deviceAddress, self.readRegister)

    def ADCToVolts12Bit(self):
        reading = self.read_i2c_block_data()
        upper = (reading[0] & 15)
        upper = (upper << 8)
        total = upper + reading[1]
        voltage = float(total * .001)
        return voltage

class PressureSensor():

    def __init__(self, resistor_value, current_interpolation_list, pressure_interpolation_list,
                 device_address, read_register):
        self._voltageInterpolationList = [x * resistor_value for x in current_interpolation_list]
        self._pressureInterpolationList = pressure_interpolation_list
        self.ADC = ADC(device_address, read_register)

    def read(self):
        voltage = ADC.ADCToVolts12Bit()
        return np.interp(voltage, self._voltageInterpolationList, self._pressureInterpolationList)

pressure_sensor = PressureSensor(resistor_value=200, current_interpolation_list=[4.014, 15, 20],
                                 pressure_interpolation_list=[0.01, 200, 500],
                                 device_address=105, read_register=48)
print(pressure_sensor.read())
'''

import smbus
import time

device_address = 0x6c
ADC_channel = 1 #1-4
read_register = ((ADC_channel-1) << 4) + 16

bus = smbus.SMBus(1)
bus.pec = True


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
    voltage_divider = (6.8 + 10) / 6.8
    return voltage * voltage_divider


while (True):
    time.sleep(0.5)
    print("ADC Out:")
    print(convert())