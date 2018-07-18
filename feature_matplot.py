import matplotlib.pyplot as plt
from drawnow import *
import json

# ----- Start of test _data and functions -----
import time


import time
import matplotlib.pyplot as plt
from drawnow import *

import json

position = {'reading': 7, 'time': 8}
velocity = {'reading': 72, 'time': 9}
proximity1 = {'reading': 73, 'time': 10}
proximity2 = {'reading': 74, 'time': 11}
temperature1 = {'reading': 75, 'time': 12}
temperature2 = {'reading': 76, 'time': 13}
voltage1 = {'reading': 77, 'time': 14}
voltage2 = {'reading': 78, 'time': 15}
voltage3 = {'reading': 79, 'time': 16}

json_data = {'position': position, 'velocity': velocity, 'proximity1': proximity1, 'proximity2': proximity2, 'temperature1': temperature1, 'temperature2': temperature2, 'voltage1': voltage1, 'voltage2': voltage2, 'voltage3': voltage3}
json_data = json.dumps(json_data)
python_data = json.loads(json_data)

print "i send  ", json_data
print "i get   ", python_data

sensor_names = []
sensor_readings = {}
MAX_LIST_LENGTH = 5


def read_json(read_file):
    with open(read_file, 'r') as file:
        return json.loads(file.read())

plot_details = read_json('plot_details.json')

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

print("sensor name", sensor_names)
print "sensors reading = ", sensor_readings

sensors_json = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
print sensors_json
def read_json(read_file):
    with open(read_file, 'r') as file:
        return json.loads(file.read())

plot_details = read_json('plot_details.json')

sensor_time_dict = {}


def create_sensor_time_dict():
    #global sensor_time_dict
    #sensor_time_dict = {}
    for i in plot_details:
        #timelen = plot_details[i]['time']
        for j in plot_details[i]['sensors']:
            #sensor_refresh = {j:timelen}
            #sensor_time_dict = dict(sensor_refresh.items() + sensor_time_dict.items())
            sensor_time_dict[j] = plot_details[i]['time']
    print("sensor time dictionary  ", sensor_time_dict)
#print("sensors_json = ", sensors_json)

def maintain_list():
    #global sensor_data_dict
    #sensor_data_dict = {}
    #for h in sensors_json:
        #print(h[1])
        #print(h[0])
        #sensordata = {}
    for sensor_name in sensor_time_dict:
        timelength = sensor_time_dict[sensor_name]
        #print(timelength)
        if sensor_readings[sensor_name][1][-1] - sensor_readings[sensor_name][1][0] == 0:
            sensor_readings[sensor_name][0].pop()
            sensor_readings[sensor_name][1].pop()
            #sensor_readings1 = sensor_readings
    print sensor_readings
    return sensor_readings


create_sensor_time_dict()
#maintain_list()






sensor_data = sensor_readings
#index_trend = 0
#index_trend_leap = 7
#trend_length = 30
#total_trend_length = 60

#index_line = 0
#total_line_length = 33

#sensor_details = []
"""
def index_update():
    global index_trend, index_line
    for key, value in plot_details.items():

        if value['type'] == 'trend':
            for n in value['sensors']:
                sensor_data[n] = [sensor_data_raw[n][0][index_trend:index_trend + trend_length],
                                  sensor_data_raw[n][1][index_trend:index_trend + trend_length]]

        if value['type'] == 'line':
            for n in value['sensors']:
                sensor_data[n] = sensor_data_raw[n][index_line]
        print sensor_data

    index_trend += index_trend_leap
    if index_trend >= total_trend_length:
        index_trend = 0

    index_line += 1
    if index_line >= total_line_length:
        index_line = 0

# ----- End of test _data and functions -----
"""
class BasicPlot():

    def __init__(self, plot_details, sensor_data):
        self.plotDetails = plot_details
        self.sensorData = sensor_data

    def drawBasics(self, key, value):
        '''These are the key and values for the plot_details dictionary'''
        plt.subplot(key)
        plt.title(value['title'])

class TrendPlot(BasicPlot):

    def __init__(self, plot_details, sensor_data):
        temp_plot_details = {}
        for key, value in plot_details.items():
            if value['type'] == 'trend':
                temp_plot_details[key] = value
        BasicPlot.__init__(self, temp_plot_details, sensor_data)

    def drawTrend(self):
        for key, value in self.plotDetails.items():
            self.drawBasics(key, value)
            if value.has_key('range'):
                # may want to change to allow multiple ranges per subplot that way multiple types of graphs can be included
                nominal_range = value['range']
                emergency_range = []
                emergency_range.append(nominal_range[0] - (nominal_range[1] - nominal_range[0]) / 2)
                emergency_range.append(nominal_range[1] + (nominal_range[1] - nominal_range[0]) / 2)
            x_min_temp = []
            x_max_temp = []
            for sensor in value['sensors']:
                plt.plot(self.sensorData[sensor][1], self.sensorData[sensor][0])
                x_min_temp.append(min(self.sensorData[sensor][1]))
                x_max_temp.append(max(self.sensorData[sensor][1]))
            plt.legend(value['sensors'], loc='lower left')
            x_min = min(x_min_temp)
            x_max = max(x_max_temp)
            if value.has_key('range'):
                plt.fill_between([x_min, x_max], [emergency_range[0], emergency_range[0]],
                                 [nominal_range[0], nominal_range[0]], alpha=0.3, color='red')
                plt.fill_between([x_min, x_max], [emergency_range[1], emergency_range[1]],
                                 [nominal_range[1], nominal_range[1]], alpha=0.3, color='red')
                plt.fill_between([x_min, x_max], [nominal_range[0], nominal_range[0]],
                                 [nominal_range[1], nominal_range[1]], alpha=0.3, color='green')


class LinePlot(BasicPlot):

    def __init__(self, plot_details, sensor_data):
        temp_plot_details = {}
        for key, value in plot_details.items():
            if value['type'] == 'line':
                temp_plot_details[key] = value
        BasicPlot.__init__(self, temp_plot_details, sensor_data)

        self.lineBottom = 0.05
        self.lineTop = 0.65
        self.textReadingHeight = 0.7
        self.textLimitHeight = 0.35
        self.textLabelHeight = 0.35
        self.textLabelMargin = 1.005

    def drawLine(self):
        for key, value in self.plotDetails.items():
            self.drawBasics(key, value)
            if value.has_key('range'):
                # may want to change to allow multiple ranges per subplot that way multiple types of graphs can be included
                nominal_range = value['range']
                emergency_range = []
                emergency_range.append(nominal_range[0] - (nominal_range[1] - nominal_range[0]) / 2)
                emergency_range.append(nominal_range[1] + (nominal_range[1] - nominal_range[0]) / 2)
            for i, sensor in list(enumerate(value['sensors'])):
                plt.plot([self.sensorData[sensor], self.sensorData[sensor]], [i+self.lineBottom, i+self.lineTop], color='black')
                plt.text(self.sensorData[sensor], i + self.textReadingHeight, self.sensorData[sensor], horizontalalignment='center')
                if value.has_key('range'):
                    plt.text(nominal_range[0], i+self.textLimitHeight, nominal_range[0], horizontalalignment='right')
                    plt.text(nominal_range[1], i + self.textLimitHeight, nominal_range[1], horizontalalignment='left')
                    plt.text(emergency_range[0] * self.textLabelMargin, i + self.textLabelHeight, sensor, horizontalalignment='left')
                    plt.fill_between([emergency_range[0], nominal_range[0]], [i, i], [i+1, i+1], alpha=0.3, color='red')
                    plt.fill_between([nominal_range[1], emergency_range[1]], [i, i], [i + 1, i + 1], alpha=0.3, color='red')
                    plt.fill_between([nominal_range[0], nominal_range[1]], [i, i], [i+1, i+1], alpha=0.3, color='green')



def all_plots():
    trend_plot.drawTrend()
    line_plot.drawLine()


def process_sensor_ranges(file_input='stateInputLogic_test.json'):
    sensor_details = read_json(file_input)
    temp = {}

    for key, value in sensor_details.items():
        if value[1]['typeOfLogic'] == 'range':
            for key in value[1]['raw_data_names']:
                temp[key] = value[1]['raw_data_names'][key]['params']

    for key1, value1 in plot_details.items():
        for key2, value2 in temp.items():
            if key2 in value1['sensors']:
                value1['range'] = value2


sensor_data_raw = read_json('sensor_data_raw_test.json')
process_sensor_ranges()

trend_plot = TrendPlot(plot_details, sensor_data)
line_plot = LinePlot(plot_details, sensor_data)


while(True):
    index_start = time.time()
    #index_update()
    index_end = time.time()
    print('index_trend: %.5f' % (index_end - index_start))
    plot_start = time.time()
    drawnow(all_plots)
    plot_end = time.time()
    print('plot: %.5f' % (plot_end - plot_start))
    #time.sleep(1)
