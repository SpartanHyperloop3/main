import sys
import zmq
import datetime
import time
import Tkinter
from Tkinter import *
window = Tkinter.Tk()
import json

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://*:5020')         #broadcast at 5020

socket_r = context.socket(zmq.SUB)
socket_r.bind('tcp://*:5010')       #receive at 5010

Value = 1

window.title("Debugging commands")
window.geometry("400x400")
window.configure(background = "light blue")

def oksensor():

    if varpi.get() == "PI A" and varsensor.get() == "Temperature":
        print("Reading PI A Hover temperature ")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["PI_A", "i2c", {
                               "bus" : "i2c",
                               "operations" : "R",
                               "address" : 16,
                               "write" : [],
                               "read" : [7],
                               "sensor_name" : "PI_A_temp_hover_1",
                               "data_length" : "block",
                               "data_type" : "pos",
                               "callback" : {
                                   "function" : "ADCtoVolts12Bit",
                                   "args" : []
                                            },
                               "pec" : 0,
                               "manual_cmd" : 1

                                    }])

        socket.send_json(["PI_A", "i2c", {
                               "bus" : "i2c",
                               "operations" : "R",
                               "address" : 17,
                               "write" : [],
                               "read" : [7],
                               "sensor_name" : "PI_A_temp_hover_2",
                               "data_length" : "block",
                               "data_type" : "pos",
                               "callback" : {
                                   "function" : "ADCtoVolts12Bit",
                                   "args" : []
                               },
                               "pec" : 0,
                               "manual_cmd" : 1

                                    }])
        socket.send_json(["PI_A", "i2c", {
                               "bus" : "i2c",
                               "operations" : "R",
                               "address" : 105,
                               "write" : [],
                               "read" : [16],
                               "sensor_name" : "PI_A_temp_bms_1",
                               "data_length" : "block",
                               "data_type" : "pos",
                               "callback" : {
                                   "function" : "ADCtoVolts12Bit",
                                   "args" : []
                               },
                               "pec" : 0,
                               "manual_cmd" : 1

                                    }])

    elif varpi.get() == "PI A" and varsensor.get() == "Levitation":
        print("Reading PI A proximity sensor ")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["PI_A", "i2c", {
                               "bus" : "i2c",
                               "operations" : "R",
                               "address" : 105,
                               "write" : [],
                               "read" : [48],
                               "sensor_name" : "PI_A_proximity_1",
                               "data_length" : "block",
                               "data_type" : "pos",
                               "callback" : {
                                   "function" : "ADCtoVolts12Bit",
                                   "args" : []
                               },
                               "pec" : 0,
                               "manual_cmd" : 1
                        }])

        socket.send_json(["PI_A", "i2c", {
                               "bus" : "i2c",
                               "operations" : "R",
                               "address" : 105,
                               "write" : [],
                               "read" : [64],
                               "sensor_name" : "PI_A_proximity_2",
                               "data_length" : "block",
                               "data_type" : "pos",
                               "callback" : {
                                   "function" : "ADCtoVolts12Bit",
                                   "args" : []
                               },
                               "pec" : 0,
                               "manual_cmd" : 1
                        }])

    elif varpi.get() == "PI A" and varsensor.get() == "Voltage":
        print("Reading PI A proximity sensor ")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["PI_A", "i2c", {
                               "bus" : "i2c",
                               "operations" : "R",
                               "address" : 106,
                               "write" : [],
                               "read" : [16],
                               "sensor_name" : "PI_A_voltage_1",
                               "data_length" : "block",
                               "data_type" : "pos",
                               "callback" : {
                                   "function" : "ADCtoVolts12Bit",
                                   "args" : []
                               },
                               "pec" : 0,
                               "manual_cmd" : 1
                        }])

    elif varpi.get() == "PI A" and varsensor.get() == "Current":
        print("Reading PI A proximity sensor ")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["PI_A", "i2c", {
                               "bus" : "i2c",
                               "operations" : "R",
                               "address" : 106,
                               "write" : [],
                               "read" : [48],
                               "sensor_name" : "PI_A_current_1",
                               "data_length" : "block",
                               "data_type" : "pos",
                               "callback" : {
                                   "function" : "ADCtoVolts12Bit",
                                   "args" : []
                               },
                               "pec" : 0,
                               "manual_cmd" : 1
                        }])

    elif varpi.get() == "PI B" and varsensor.get() == "Pressure":
        print("Reading PI B pressure ")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["PI_B", "i2c", {
                               "bus" : "i2c",
                               "operations" : "R",
                               "address" : 105,
                               "write" : [],
                               "read" : [16],
                               "sensor_name" : "PI_B_pressure",
                               "data_length" : "block",
                               "data_type" : "pos",
                               "callback" : {
                                   "function" : "ADCtoVolts12Bit",
                                   "args" : []
                               },
                               "pec" : 0,
                               "manual_cmd" : 1
                        }])
    elif varpi.get() == "PI B" and varsensor.get() == "Temperature":
        print("Reading PI B scissor temperature ")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)  #send for 6 cyl
        socket.send_json(["PI_B", "i2c", {
                               "bus" : "i2c",
                               "operations" : "R",
                               "address" : 16,
                               "write" : [],
                               "read" : [7],
                               "sensor_name" : "PI_B_temp_cyl_1",
                               "data_length" : "block",
                               "data_type" : "pos",
                               "callback" : {
                                   "function" : "ADCtoVolts12Bit",
                                   "args" : []
                               },
                               "pec" : 0,
                               "manual_cmd" : 1
                        }])
        socket.send_json(["PI_B", "i2c", {
            "bus": "i2c",
            "operations": "R",
            "address": 17,
            "write": [],
            "read": [7],
            "sensor_name": "PI_B_temp_cyl_2",
            "data_length": "block",
            "data_type": "pos",
            "callback": {
                "function": "ADCtoVolts12Bit",
                "args": []
            },
            "pec": 0,
            "manual_cmd": 1
        }])
        socket.send_json(["PI_B", "i2c", {
            "bus": "i2c",
            "operations": "R",
            "address": 18,
            "write": [],
            "read": [7],
            "sensor_name": "PI_B_temp_cyl_3",
            "data_length": "block",
            "data_type": "pos",
            "callback": {
                "function": "ADCtoVolts12Bit",
                "args": []
            },
            "pec": 0,
            "manual_cmd": 1
        }])
        socket.send_json(["PI_B", "i2c", {
            "bus": "i2c",
            "operations": "R",
            "address": 19,
            "write": [],
            "read": [7],
            "sensor_name": "PI_B_temp_cyl_4",
            "data_length": "block",
            "data_type": "pos",
            "callback": {
                "function": "ADCtoVolts12Bit",
                "args": []
            },
            "pec": 0,
            "manual_cmd": 1
        }])
        socket.send_json(["PI_B", "i2c", {
            "bus": "i2c",
            "operations": "R",
            "address": 20,
            "write": [],
            "read": [7],
            "sensor_name": "PI_B_temp_cyl_5",
            "data_length": "block",
            "data_type": "pos",
            "callback": {
                "function": "ADCtoVolts12Bit",
                "args": []
            },
            "pec": 0,
            "manual_cmd": 1
        }])
        socket.send_json(["PI_B", "i2c", {
            "bus": "i2c",
            "operations": "R",
            "address": 21,
            "write": [],
            "read": [7],
            "sensor_name": "PI_B_temp_cyl_6",
            "data_length": "block",
            "data_type": "pos",
            "callback": {
                "function": "ADCtoVolts12Bit",
                "args": []
            },
            "pec": 0,
            "manual_cmd": 1
        }])

    elif varpi.get() == "PI C" and varsensor.get() == "Temperature":
        print("Reading PI C scissor temperature ")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["PI_c", "i2c", {
            "bus": "i2c",
            "operations": "R",
            "address": 16,
            "write": [],
            "read": [7],
            "sensor_name": "PI_C_temp_cyl_7",
            "data_length": "block",
            "data_type": "pos",
            "callback": {
                "function": "ADCtoVolts12Bit",
                "args": []
            },
            "pec": 0,
            "manual_cmd": 1
        }])
        socket.send_json(["PI_C", "i2c", {
            "bus": "i2c",
            "operations": "R",
            "address": 17,
            "write": [],
            "read": [7],
            "sensor_name": "PI_C_temp_cyl_8",
            "data_length": "block",
            "data_type": "pos",
            "callback": {
                "function": "ADCtoVolts12Bit",
                "args": []
            },
            "pec": 0,
            "manual_cmd": 1
        }])
        socket.send_json(["PI_C", "i2c", {
            "bus": "i2c",
            "operations": "R",
            "address": 18,
            "write": [],
            "read": [7],
            "sensor_name": "PI_C_temp_cyl_9",
            "data_length": "block",
            "data_type": "pos",
            "callback": {
                "function": "ADCtoVolts12Bit",
                "args": []
            },
            "pec": 0,
            "manual_cmd": 1
        }])
        socket.send_json(["PI_C", "i2c", {
            "bus": "i2c",
            "operations": "R",
            "address": 19,
            "write": [],
            "read": [7],
            "sensor_name": "PI_C_temp_cyl_10",
            "data_length": "block",
            "data_type": "pos",
            "callback": {
                "function": "ADCtoVolts12Bit",
                "args": []
            },
            "pec": 0,
            "manual_cmd": 1
        }])
        socket.send_json(["PI_C", "i2c", {
            "bus": "i2c",
            "operations": "R",
            "address": 20,
            "write": [],
            "read": [7],
            "sensor_name": "PI_C_temp_cyl_11",
            "data_length": "block",
            "data_type": "pos",
            "callback": {
                "function": "ADCtoVolts12Bit",
                "args": []
            },
            "pec": 0,
            "manual_cmd": 1
        }])
        socket.send_json(["PI_C", "i2c", {
            "bus": "i2c",
            "operations": "R",
            "address": 21,
            "write": [],
            "read": [7],
            "sensor_name": "PI_C_temp_cyl_12",
            "data_length": "block",
            "data_type": "pos",
            "callback": {
                "function": "ADCtoVolts12Bit",
                "args": []
            },
            "pec": 0,
            "manual_cmd": 1
        }])
    elif varpi.get() == "PI D" and varsensor.get() == "Temperature":
        print("Reading PI D Hover temperature ")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["PI_D", "i2c", {
            "bus": "i2c",
            "operations": "R",
            "address": 16,
            "write": [],
            "read": [7],
            "sensor_name": "PI_D_temp_hover_3",
            "data_length": "block",
            "data_type": "pos",
            "callback": {
                "function": "ADCtoVolts12Bit",
                "args": []
            },
            "pec": 0,
            "manual_cmd": 1

        }])

        socket.send_json(["PI_D", "i2c", {
            "bus": "i2c",
            "operations": "R",
            "address": 17,
            "write": [],
            "read": [7],
            "sensor_name": "PI_D_temp_hover_4",
            "data_length": "block",
            "data_type": "pos",
            "callback": {
                "function": "ADCtoVolts12Bit",
                "args": []
            },
            "pec": 0,
            "manual_cmd": 1

        }])
        socket.send_json(["PI_D", "i2c", {
            "bus": "i2c",
            "operations": "R",
            "address": 105,
            "write": [],
            "read": [16],
            "sensor_name": "PI_D_temp_bms_2",
            "data_length": "block",
            "data_type": "pos",
            "callback": {
                "function": "ADCtoVolts12Bit",
                "args": []
            },
            "pec": 0,
            "manual_cmd": 1

        }])

    elif varpi.get() == "PI D" and varsensor.get() == "Levitation":
        print("Reading PI D proximity sensor ")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["PI_D", "i2c", {
            "bus": "i2c",
            "operations": "R",
            "address": 105,
            "write": [],
            "read": [48],
            "sensor_name": "PI_D_proximity_3",
            "data_length": "block",
            "data_type": "pos",
            "callback": {
                "function": "ADCtoVolts12Bit",
                "args": []
            },
            "pec": 0,
            "manual_cmd": 1
        }])

        socket.send_json(["PI_D", "i2c", {
            "bus": "i2c",
            "operations": "R",
            "address": 105,
            "write": [],
            "read": [64],
            "sensor_name": "PI_D_proximity_4",
            "data_length": "block",
            "data_type": "pos",
            "callback": {
                "function": "ADCtoVolts12Bit",
                "args": []
            },
            "pec": 0,
            "manual_cmd": 1
        }])

    elif varpi.get() == "PI D" and varsensor.get() == "Voltage":
        print("Reading PI A proximity sensor ")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["PI_D", "i2c", {
                               "bus" : "i2c",
                               "operations" : "R",
                               "address" : 106,
                               "write" : [],
                               "read" : [16],
                               "sensor_name" : "PI_D_voltage_2",
                               "data_length" : "block",
                               "data_type" : "pos",
                               "callback" : {
                                   "function" : "ADCtoVolts12Bit",
                                   "args" : []
                               },
                               "pec" : 0,
                               "manual_cmd" : 1
                        }])

    elif varpi.get() == "PI D" and varsensor.get() == "Current":
        print("Reading PI A proximity sensor ")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["PI_D", "i2c", {
                               "bus" : "i2c",
                               "operations" : "R",
                               "address" : 106,
                               "write" : [],
                               "read" : [48],
                               "sensor_name" : "PI_D_current_2",
                               "data_length" : "block",
                               "data_type" : "pos",
                               "callback" : {
                                   "function" : "ADCtoVolts12Bit",
                                   "args" : []
                               },
                               "pec" : 0,
                               "manual_cmd" : 1
                        }])


    else:
        print "", varpi.get() + " does not have " + "", varsensor.get()
        print " Choose again from" \
              " PI A: Temperature, Proximity; " \
              " PI B: Temperature, Pressure;" \
              " PI C: Temperature, Pressure;" \
              " PI D: Temperature, Proximity;"

def okcmd():
    if varcmd.get() == "Engage brakes":
        print "Sending command to engage brakes"
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["PI_X", "gpio_write", 8, 1])
        print ["PI_X", "gpio_write", 8, 1]

    elif varcmd.get() == "Disengage brakes":
        print "Sending command to disengage brakes"
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["PI_X", "gpio_write", 8, 0])

    elif varcmd.get() == "Open scissor":
        print "Sending command to open scissor mechanism"
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["PI_Y", "gpio_write", 10, 0])

    elif varcmd.get() == "Close scissor":
        print "Sending command to close scissor"
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["PI_Y", "gpio_write", 10, 1])

def inhubok():
    inhubrpm = int(textboxinhub.get())
    print "Sending inhub motor speed up command at: ", inhubrpm
    timenow = datetime.datetime.now()
    time = str(timenow)
    print(time)
    socket.send_json(["PI_Z", "pwm_write", inhubrpm])
    print ["PI_Z", "pwm_write", inhubrpm]

def hoverok():
    hoverrpm = int(textboxhover.get())
    print "Sending hover motor speed up command at: ", hoverrpm
    timenow = datetime.datetime.now()
    time = str(timenow)
    print(time)
    socket.send_json(["PI_A", "pwm_write", hoverrpm])
    socket.send_json(["PI_D", "pwm_write", hoverrpm])
    print ["PI_D", "pwm_write", hoverrpm]

def readdata():
    time.sleep(3)
    incoming_json = socket_r.recv_json()
    data_read = json.load(incoming_json)
    if data_read != "":
        w = Label(window, text=data_read)
        w.pack()
    else:
        print "No sensor data found"



label_sensor = Tkinter.Label(window, text = "Choose Pi and its corresponding sensor: ", fg = "black", bg="light blue")
label_cmd = Tkinter.Label(window, text = "Choose actuator commands: ", fg = "black", bg = "light blue")

label_sensor.pack()

varpi = StringVar(window)
varpi.set("Choose PI")
option1 = OptionMenu(window, varpi, "PI A", "PI B", "PI C", "PI D")
option1.pack()

varsensor = StringVar(window)
varsensor.set("Choose sensor")
option2 = OptionMenu(window, varsensor, "Temperature", "Pressure", "Levitation", "Voltage", "Current")
option2.pack()
buttonpi = Button(window, text="OK", command=oksensor)
buttonpi.pack()

label_cmd.pack()

varcmd = StringVar(window)
varcmd.set("Choose command")
option3 = OptionMenu(window, varcmd, "Engage brakes", "Disengage brakes", "Open scissor", "Close scissor")
option3.pack()
buttoncommand = Button(window, text="OK", command=okcmd)
buttoncommand.pack()

labelinhub = Tkinter.Label(window, text = "Enter in-hub speed in rpm: ")
textboxinhub = Tkinter.Entry(window, fg = "black", bg = "white")
inhubrpm = str(textboxinhub.get())
buttoninhub = Tkinter.Button(window, text = "OK", command = inhubok)

labelhover = Tkinter.Label(window, text = "Enter hover engine speed in rpm")
textboxhover = Tkinter.Entry(window, fg = "black", bg = "white")
hoverrpm = str(textboxhover.get())
buttonhover = Tkinter.Button(window, text = "OK", command = hoverok)
labelresult = Tkinter.Button(window, text = " Read data:                  " ,fg = "black", bg = "white", command = readdata)

labelinhub.pack()
textboxinhub.pack()
buttoninhub.pack()
labelhover.pack()
textboxhover.pack()
buttonhover.pack()
labelresult.pack()
window.mainloop()



