import sys
import zmq
import datetime
import Tkinter
from Tkinter import *
window = Tkinter.Tk()

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://*:5020')     #broadcast at 5020

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
        socket.send_json(["Read_PI_A_temp", Value, time])

    elif varpi.get() == "PI A" and varsensor.get() == "Levitation":
        print("Reading PI A proximity sensor ")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["Read_PI_A_proximity", Value, time])

    elif varpi.get() == "PI B" and varsensor.get() == "Pressure":
        print("Reading PI B pressure ")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["Read_PI_B_pressure", Value, time])

    elif varpi.get() == "PI B" and varsensor.get() == "Temperature":
        print("Reading PI B scissor temperature ")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["Read_PI_B_temp", Value, time])

    elif varpi.get() == "PI C" and varsensor.get() == "Pressure":
        print("Reading PI C pressure ")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["Read_PI_C_pressure", Value, time])

    elif varpi.get() == "PI C" and varsensor.get() == "Temperature":
        print("Reading PI C scissor temperature ")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["Read_PI_C_temp", Value, time])

    elif varpi.get() == "PI D" and varsensor.get() == "Temperature":
        print("Reading PI D Hover temperature ")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["Read_PI_D_temp", Value, time])

    elif varpi.get() == "PI D" and varsensor.get() == "Levitation":
        print("Reading PI D proximity sensor ")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["Read_PI_D_proximity", Value, time])

    else:
        print "", varpi.get() + " does not have " + "", varsensor.get()
        print "Choose again from" \
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
        socket.send_json(["PI_X_EngageBrakes", Value, time])

    elif varcmd.get() == "Disengage brakes":
        print "Sending command to disengage brakes"
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["PI_X_DisengageBrakes", Value, time])

    elif varcmd.get() == "Open scissor":
        print "Sending command to open scissor mechanism"
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["PI_X_OpenScissor", Value, time])

    elif varcmd.get() == "Close scissor":
        print "Sending command to close scissor"
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["PI_X_CloseScissor", Value, time])

def inhubok():
    inhubrpm = int(textboxinhub.get())
    print "Sending inhub motor speed up command at: ", inhubrpm
    timenow = datetime.datetime.now()
    time = str(timenow)
    print(time)
    socket.send_json(["InhubOn", inhubrpm, time])

def hoverok():
    hoverrpm = int(textboxhover.get())
    print "Sending hover motor speed up command at: ", hoverrpm
    timenow = datetime.datetime.now()
    time = str(timenow)
    print(time)
    socket.send_json(["HoverOn", hoverrpm, time])

label_sensor = Tkinter.Label(window, text = "Choose Pi and its corresponding sensor: ", fg = "black", bg="light blue")
label_cmd = Tkinter.Label(window, text = "Choose actuator commands: ", fg = "black", bg = "light blue")

label_sensor.pack()

varpi = StringVar(window)
varpi.set("Choose PI")
option1 = OptionMenu(window, varpi, "PI A", "PI B", "PI C", "PI D")
option1.pack()

varsensor = StringVar(window)
varsensor.set("Choose sensor")
option2 = OptionMenu(window, varsensor, "Temperature", "Pressure", "Levitation")
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

labelinhub.pack()
textboxinhub.pack()
buttoninhub.pack()
labelhover.pack()
textboxhover.pack()
buttonhover.pack()

window.mainloop()



