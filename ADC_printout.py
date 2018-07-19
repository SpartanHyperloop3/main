import smbus
import time

device_address = 0x69
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

def binary_out(total_bits=12):
    shift = 11-total_bits
    reading = read()
    upper = (reading[0] & 15)
    upper = (upper << 8)
    total = (upper + reading[1]) >> shift
    return total

def distance(zero_level, average_window_size, reading_function, total_bits):
    add_adjust = 60 - zero_level
    window = []
    for n in range(0, average_window_size):
        window.append(reading_function(total_bits)+add_adjust)
    return float(sum(window))/len(window)

while (True):
    #time.sleep(0.5)
    print("ADC Out:")
    #print(convert())
    print(distance(59, 50, binary_out, 10)*5)