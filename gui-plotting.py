import matplotlib.pyplot as plt
from drawnow import *
import json

# ----- Start of test data and functions -----
import time

sensor_data = {}
index_trend = 0
index_trend_leap = 7
trend_length = 30
total_trend_length = 60

index_line = 0
total_line_length = 33

sensor_details = []

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

    index_trend += index_trend_leap
    if index_trend >= total_trend_length:
        index_trend = 0

    index_line += 1
    if index_line >= total_line_length:
        index_line = 0

# ----- End of test data and functions -----

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
            for sensor in value['sensors']:
                plt.plot(self.sensorData[sensor][1], self.sensorData[sensor][0])

class LinePlot(BasicPlot):

    def __init__(self, plot_details, sensor_data):
        temp_plot_details = {}
        for key, value in plot_details.items():
            if value['type'] == 'line':
                temp_plot_details[key] = value
        BasicPlot.__init__(self, temp_plot_details, sensor_data)

        self.lineBottom = 0.2
        self.lineTop = 0.8
        self.lineReadingHeight = 0.85

    def drawLine(self):
        for key, value in self.plotDetails.items():
            self.drawBasics(key, value)
            for i, sensor in list(enumerate(value['sensors'])):
                plt.plot([self.sensorData[sensor], self.sensorData[sensor]], [i+self.lineBottom, i+self.lineTop])
                plt.text(self.sensorData[sensor], i+self.lineReadingHeight, self.sensorData[sensor], horizontalalignment='center')

def all_plots():
    trend_plot.drawTrend()
    line_plot.drawLine()

def read_json(read_file):
    with open(read_file, 'r') as file:
        return json.loads(file.read())

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


plot_details = read_json('plot_details.json')
sensor_data_raw = read_json('sensor_data_raw_test.json')
process_sensor_ranges()

trend_plot = TrendPlot(plot_details, sensor_data)
line_plot = LinePlot(plot_details, sensor_data)


while(True):
    index_start = time.time()
    index_update()
    index_end = time.time()
    print('index_trend: %.5f' % (index_end - index_start))
    plot_start = time.time()
    drawnow(all_plots)
    plot_end = time.time()
    print('plot: %.5f' % (plot_end - plot_start))
    #time.sleep(1)
