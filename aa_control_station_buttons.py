import sys
import zmq
import datetime

from Tkinter import *
import Tkinter as Tk
import tkMessageBox

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://*:5000')     #enter master ip, port 5010

Value = 1

def create_window():
    import tkinception

def State3():
    print("Sending state 3: Hover spin up")
    timenow = datetime.datetime.now()
    time = str(timenow)
    print(time)
    socket.send_json(["Hover_Spin_Up", Value, time])

def State4():
    print("Sending state 4: Accelerate forward")
    timenow = datetime.datetime.now()
    time = str(timenow)
    print(time)
    socket.send_json(["Accelerate_Forward", Value, time])

def State5():
    print("Sending state 5: Braking 1")
    timenow = datetime.datetime.now()
    time = str(timenow)
    print(time)
    socket.send_json(["Braking_1", Value, time])

def State13():
    print("Sending state 13: Emergency_Shutdown")
    timenow = datetime.datetime.now()
    time = str(timenow)
    print(time)
    socket.send_json(["Exit_Track", Value, time])

def State99():
    result = tkMessageBox.askyesno("Warning","Are you sure?")
    if result == True:
        print("Sending emergency override")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["Emergency_Override", Value, time])
    else:
        print("You cancelled emergency override")

window = Tk.Tk()
window.title("Control station")
window.geometry("300x200")
window.configure(background = "bisque2")

button3 = Tk.Button(window, text = "State 3: Hover Spin Up", fg = "black", bg = "deep sky blue", command = State3)
button4 = Tk.Button(window, text = "State 4: Accelerate Forward", command = State4)
button5 = Tk.Button(window, text = "State 2: Braking 1",fg = "black", bg = "green",command = State5)
button99 = Tk.Button(window, text = "Emerrgency Override", fg = "black", bg = "gold", command = State99)
button13 = Tk.Button(window, text = "State 13: Emergency Shutdown",fg = "black", bg = "red", command = State13)
button56 = Tk.Button(window, text= "Manual Operation Mode", command=create_window)

button56.pack()
button3.pack()
button4.pack()
button5.pack()
button13.pack()
button99.pack()


window.mainloop()

