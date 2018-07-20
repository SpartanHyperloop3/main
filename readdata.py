from Tkinter import *
import tkMessageBox
import Tkinter as Tk
import time
import json
import zmq
import datetime
context = zmq.Context()
socket_r = context.socket(zmq.SUB)
socket_r.connect('tcp://192.168.0.13:5010')       #receive at 5010
socket_r.setsockopt(zmq.SUBSCRIBE,'')
Value = 1
time.sleep(3)
incoming_json = socket_r.recv_json()
data_read = incoming_json

#data_read = {"a":[1,2]}
print(data_read)
#tkinter.messagebox.showinfo("Sensor reading: ",data_read)

result = tkMessageBox.showinfo("Sensor data: ", data_read)


#window = Tk.Tk()
#window.quit