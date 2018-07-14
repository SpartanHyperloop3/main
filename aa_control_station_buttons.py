import sys
import zmq
import datetime
import Tkinter as Tk
import tkMessageBox


context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://127.0.0.1:5000')     #enter master ip, port 5000

Value = 1

"""
def State54():
    userentry = str(textbox.get())
    while userentry:
        print("Sending state " + userentry)
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json([userentry, Value, time])
        break
"""
def State1():
    print("Sendinng state 1: Initialise and test sensors")
    timenow = datetime.datetime.now()
    time = str(timenow)
    print(time)
    socket.send_json(["Initialize_and_Test_Sensors", Value, time])

def State14():
    print("Sendinng state 14: Initialise and test actuators")
    timenow = datetime.datetime.now()
    time = str(timenow)
    print(time)
    socket.send_json(["Initialize_and_Test_Actuators", Value, time])

def State2():
    print("Sendinng state 2: Enter Track")
    timenow = datetime.datetime.now()
    time = str(timenow)
    print(time)
    socket.send_json(["Enter_Track", Value, time])

def State10():
    print("Sendinng state 10: Exit Track")
    timenow = datetime.datetime.now()
    time = str(timenow)
    print(time)
    socket.send_json(["Exit_Track", Value, time])

def State11():
    print("Sendinng state 11: Shutdown")
    timenow = datetime.datetime.now()
    time = str(timenow)
    print(time)
    socket.send_json(["Shutdown", Value, time])

def State17():
    print("Sendinng state 17: Waiting")
    timenow = datetime.datetime.now()
    time = str(timenow)
    print(time)
    socket.send_json(["Waiting", Value, time])

def State2():
    print("Sendinng state 2: Enter Track")
    timenow = datetime.datetime.now()
    time = str(timenow)
    print(time)
    socket.send_json(["Enter_Track", Value, time])

def State13():
    print("Sendinng state 13: Emerrgency Shutdown")
    timenow = datetime.datetime.now()
    time = str(timenow)
    print(time)
    socket.send_json(["Emergency_Shutdown", Value, time])

def create_window():
    import meta_drop_down
    meta_drop_down.metadrop()

def State99():
    result = tkMessageBox.askyesno("Warning","Are you sure?")
    if result == True:
        print("Sending emergency override")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["Emergency_Override", Value, time])
    else:
        print("Thanks")


window = Tk.Tk()
window.title("Control station")
window.geometry("350x350")
window.configure(background = "bisque2")

#textbox = Tk.Entry(window, fg = "black", bg = "snow")
#userentry = str(textbox.get())
#button54 = Tk.Button(window, text = "Enter", command = State54)

button1 = Tk.Button(window, text = "State 1: Initialise and test sensors", fg = "black", bg = "deep sky blue", command = State1)
button14 = Tk.Button(window, text = "State 14: Initialise and test actuators", command = State14)
button2 = Tk.Button(window, text = "State 2: Enter track",fg = "black", bg = "green",command = State2)
button99 = Tk.Button(window, text = "Emerrgency Override", fg = "black", bg = "gold", command = State99)
button17 = Tk.Button(window, text = "State 17: Waiting", command = State17)
button10 = Tk.Button(window, text = "State 10: Exit track", command = State10)
button11 = Tk.Button(window, text = "State 11: Shutdown", command = State11)
button13 = Tk.Button(window, text = "State 13: Emergency Shutdown", fg = "black", bg = "orange red", command = State13)
button56 = Tk.Button(window, text= "Manual Operation Mode", command=create_window)

button1.pack()
button14.pack()
button2.pack()
button10.pack()
button11.pack()
#textbox.pack()
#button54.pack()
button13.pack()
button99.pack()
button56.pack()

window.mainloop()

