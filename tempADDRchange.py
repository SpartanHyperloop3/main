
import smbus
import time

#default i2c address
DEVICE_ADDRESS = 0x5A

#register address masks
RAM_ACCESS_MASK = 0b00000000
EEPROM_ACCESS_MASK = 0b00100000
READ_FLAGS = 0b11110000

#RAM addresses
DATA_IR_CHANNEL_1 = 0x04
TA = 0x06 #ambient temp Tareg * 0.02 = temp in kelvin
T_OBJ1 = 0x07 # object temp Toreg * 0.02 = temp in kelvin | MSB is an error flag (it should be 0)

#EEPROM addresses
SMBUS = 0x0E
EMISSIVITY = 0x04

#commands
ir_temp_register = RAM_ACCESS_MASK | T_OBJ1
ambient_temp_register = RAM_ACCESS_MASK | TA
emissivity_register = EEPROM_ACCESS_MASK | EMISSIVITY
smbus_register = EEPROM_ACCESS_MASK | SMBUS
flags_register = READ_FLAGS

#emissivity
PAPER_EMISSIVITY = 0.68
HUMAN_EMISSIVITY = 0.97
#OBJECT_EMISSIVITY = int(round(65535 * PAPER_EMISSIVITY))
OBJECT_EMISSIVITY = int(round(65535 * HUMAN_EMISSIVITY))

bus = smbus.SMBus(1)
bus.pec = True

#change emissivity
#write 0
#bus.write_word_data(DEVICE_ADDRESS, emissivity_register, 0x0000)
#time.sleep(1)
#write actual
#bus.write_word_data(DEVICE_ADDRESS, emissivity_register, OBJECT_EMISSIVITY)
#time.sleep(1)

#figure out how to have multiple temp sensors on one i2c bus (page 14)
#bus.write_word_data(DEVICE_ADDRESS, smbus_register, 0x00)
#time.sleep(1)
bus.write_word_data(0x00, smbus_register, 0x0000)
time.sleep(0.1)
bus.write_word_data(0x00, smbus_register, 0x0015)
result = bus.read_word_data(0x00, smbus_register)
#result = bus.read_word_data(DEVICE_ADDRESS, smbus_register)
print hex(result)
#print "got here"
#time.sleep(1)

