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
                    plt.fill_between([emergency_range[0], nominal_range[0]], [i, i], [i+1, i+1], alpha=0.3, color='red')
                    plt.fill_between([nominal_range[1], emergency_range[1]], [i, i], [i + 1, i + 1], alpha=0.3, color='red')
                    plt.fill_between([nominal_range[0], nominal_range[1]], [i, i], [i+1, i+1], alpha=0.3, color='green')

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
