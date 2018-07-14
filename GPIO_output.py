import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

OUTPUTS = [36, 38, 40]

for n in OUTPUTS:
	GPIO.setup(n, GPIO.OUT)

while(True):
	pin_choice = input('Choose pin '+str(OUTPUTS)+': ')
	level_choice = input('Choose level 0/1: ')
	if pin_choice in OUTPUTS and level_choice in [0, 1]:
		GPIO.output(pin_choice, level_choice)
		print('Pin '+str(pin_choice)+' is now set to '+str(level_choice))