import sys
import zmq
import datetime
from Tkinter import *

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://127.0.0.1:3000')     #enter master ip, port != 5000

Value = 1


def metadrop():
    master = Tk()
    varpi = StringVar(master)
    varpi.set("Choose PI")

    option1 = OptionMenu(master, varpi, "PI one", "PI two", "PI three", "PI four")
    option1.pack()

    varsensor = StringVar(master)
    varsensor.set("Choose sensor")

    option2 = OptionMenu(master, varsensor, "Temp", "Pressure", "Velocity", "Acceleration")
    option2.pack()

    def ok():

        if varpi.get() == "PI one" and varsensor.get() == "Temp":
            print("Reading PI 1 temp ")
            timenow = datetime.datetime.now()
            time = str(timenow)
            print(time)
            socket.send_json(["Read_PI1_Temp", Value, time])

        elif varpi.get() == "PI two" and varsensor.get() == "Pressure":
            print("Reading PI 2 pressure ")
            timenow = datetime.datetime.now()
            time = str(timenow)
            print(time)
            socket.send_json(["Read_PI2_Pressure", Value, time])

        elif varpi.get() == "PI three" and varsensor.get() == "Velocity":
            print("Reading PI 3 velocity ")
            timenow = datetime.datetime.now()
            time = str(timenow)
            print(time)
            socket.send_json(["Read_PI3_Velocity", Value, time])

        elif varpi.get() == "PI four" and varsensor.get() == "Acceleration":
            print("Reading PI 4 acceleration ")
            timenow = datetime.datetime.now()
            time = str(timenow)
            print(time)
            socket.send_json(["Read_PI4_Acceleration", Value, time])

        else:
            print "",varpi.get() + " does not have " + "", varsensor.get()
            print "Choose again from PI 1: Temp, PI 2: Pressure, PI 3: Velocity, PI 4: Acceleration"
        #print "happy pi ", varpi.get()
        #print "sad sensor ", varsensor.get()
        #master.quit()

    master.title("Control station")
    master.geometry("50x150")
    master.configure(background="skyblue")
    button = Button(master, text="OK", command=ok)
    button.pack()
    mainloop()
#metadrop()
