"""change send_json format, 
check if while loop is needed for continuous sending of json
"""




from tkinter import Tk, Label, Button             #change line 8 to "from Tkinter import Tk, Label, Button" for python27
import sys
import zmq
import time
import datetime

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://127.0.0.1:5000')               #enter master ip, at port 5000

Value = 1

class ControlButtonGUI:
    def __init__(self, master):
        self.master = master
        master.title("Off-pod Control System")
        master.geometry("300x275")  
        master.resizable(1, 1)  

        self.label = Label(master, text="Off-pod Control System")
        self.label.pack()

        self.stateone_button = Button(master, text="1) Initialize and test sensors", command=self.test_sensors, bg="yellow")
        self.stateone_button.pack()

        self.statefourteen_button = Button(master, text="14) Initialize and test actuators", command=self.test_actuators, bg="blue")
        self.statefourteen_button.pack()

        self.statetwo_button = Button(master, text="2) Enter track", command=self.enter_track, bg="green")
        self.statetwo_button.pack()

        self.stateten_button = Button(master, text="10) Exit track", command=self.exit_track, bg="cyan")
        self.stateten_button.pack()

        self.stateeleven_button = Button(master, text="11) Shutdown", command=self.shutdown, bg="magenta")
        self.stateeleven_button.pack()

        self.stateseventeen_button = Button(master, text="17) Waiting", command=self.wait)
        self.stateseventeen_button.pack()

        self.statefiftyfour_button = Button(master, text="54) Manual operation mode", command=self.manual_operation, bg="yellow")
        self.statefiftyfour_button.pack()


        self.statethirteen_button = Button(master, text = "13) Emergency shutdown", command=self.emergency, bg = "red")
        self.statethirteen_button.pack()

        self.close_button = Button(master, text = "Close the window", command=master.quit)
        self.close_button.pack()


    def test_sensors(self):
        print("Sending state 1")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["Initialize_and_Test_Sensors", Value, time])               


    def test_actuators(self):
        print("Sending state 14")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["Initialize_and_Test_Actuators", Value, time])                        

    def enter_track(self):
        print("Sending state 2")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["Enter_Track", Value, time])

    def exit_track(self):
        print("Sending state 10")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["Exit_Track", Value, time])

    def shutdown(self):
        print("Sendinng state 11")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["Shutdown", Value, time])

    def wait(self):
        print("Sending state 17")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["Waiting", Value, time])

    def manual_operation(self):
        print("Sending state 54")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["Enter_Manual_State", Value, time])

    def emergency(self):
        print("Sending state 13")
        timenow = datetime.datetime.now()
        time = str(timenow)
        print(time)
        socket.send_json(["Emergency_Override", Value, time])

root = Tk()
my_gui = ControlButtonGUI(root)
root.mainloop()
