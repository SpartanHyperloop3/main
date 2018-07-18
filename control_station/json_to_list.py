import time
import matplotlib.pyplot as plt
from drawnow import *

import json


position = {'reading': 7, 'time': 8, 'units': 5}
velocity = {'reading': 71, 'time': 28, 'units': 4}
proximity1 = {'reading': 7, 'time': 83, 'units': 55}
proximity2 = {'reading': 74, 'time': 86, 'units': 59}
temperature1 = {'reading': 7, 'time': 83, 'units': 55}
temperature2 = {'reading': 74, 'time': 86, 'units': 59}
voltage1 = {'reading': 7, 'time': 83, 'units': 55}
voltage2 = {'reading': 74, 'time': 86, 'units': 59}
voltage3 = {'reading': 7, 'time': 83, 'units': 55}

json_data = {'position': position, 'velocity': velocity, 'proximity1': proximity1, 'proximity2': proximity2, 'temperature1': temperature1, 'temperature2': temperature2, 'voltage1': voltage1, 'voltage2': voltage2, 'voltage3': voltage3}
json_data = json.dumps(json_data)
python_data = json.loads(json_data)

print(json_data)
print(python_data)

sensor_names = []
sensor_readings = {}
MAX_LIST_LENGTH = 5

def parse(python_data):
   for sensor in python_data:
       if sensor not in sensor_names:
           sensor_names.append(sensor)
       try:
           if len(sensor_readings[sensor][0]) >= MAX_LIST_LENGTH:
               sensor_readings[sensor][0].pop(0)
               sensor_readings[sensor][1].pop(0)
           sensor_readings[sensor][0].append(python_data[sensor]['reading'])
           sensor_readings[sensor][1].append(python_data[sensor]['time'])
       except KeyError:
           sensor_readings[sensor] = [[],[]]
           sensor_readings[sensor][0].append(python_data[sensor]['reading'])
           sensor_readings[sensor][1].append(python_data[sensor]['time'])

for i in range(0,10):
   parse(python_data)

s1 = sensor_readings['position']
s2 = sensor_readings['velocity']
s3 = sensor_readings['proximity1']
s4 = sensor_readings['proximity2']
s5 = sensor_readings['temperature1']
s6 = sensor_readings['temperature2']
s7 = sensor_readings['voltage1']
s8 = sensor_readings['voltage2']
s9 = sensor_readings['voltage3']

#print(s1, s2, s3, s4)
#print(len(s1[0]), len(s2[1]), len(s3), len(s4))


print(sensor_names)
print(sensor_readings)

sensors_json = [s1, s2, s3, s4, s5, s6, s7, s8, s9]

#print(sensor_names)
#print(position)
#print(s1)
#print(sensors_json)

def read_json(read_file):
    with open(read_file, 'r') as file:
        return json.loads(file.read())

plot_details = read_json('plot_details.json')


def create_sensor_time_dict():
    global sensor_time_dict
    sensor_time_dict = {}
    for i in plot_details:
        timelen = plot_details[i]['time']
        for j in plot_details[i]['sensors']:
            sensor_refresh = {j:timelen}
            sensor_time_dict = dict(sensor_refresh.items() + sensor_time_dict.items())
    #print(sensor_time_dict)


def maintain_list():
    for h in sensors_json:
        print(h[1])
        print(h[0])
        for sensor_name in sensor_names:
            timelength = sensor_time_dict[sensor_name]
            #print(timelength)
            if h[1][-1] - h[1][0] == timelength:
                h[1].pop(0)
                h[0].pop
            #print(h[1])
            #print(h[0])


create_sensor_time_dict()
maintain_list()

