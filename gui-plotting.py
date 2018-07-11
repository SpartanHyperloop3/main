import matplotlib.pyplot as plt
from drawnow import *
import json

# ----- Start of test data and functions -----
import time

#dummy sensor data
sensor_data_raw = {
    'position' : [[2.3, 2.4, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.3, 3.4, 3.5, 3.7, 3.8, 3.9, 3.3, 3.4, 3.5, 3.7, 3.8, 3.9,
                   2.3, 2.4, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.3, 3.4, 3.5, 3.7, 3.8, 3.9, 3.3, 3.4, 3.5, 3.7, 3.8, 3.9,
                   2.3, 2.4, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.3, 3.4, 3.5, 3.7, 3.8, 3.9, 3.3, 3.4, 3.5, 3.7, 3.8, 3.9],
                  [4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3,
                   5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1, 7.2, 7.3,
                   7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8.0, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 9.0, 9.1, 9.2, 9.3,
                   9.4, 9.5, 9.6, 9.7, 9.8, 9.9]],
    'velocity' : [[3.7, 3.7, 3.8, 3.8, 3.7, 3.7, 3.7, 3.7, 3.8, 3.8, 3.7, 3.8, 3.7, 3.9, 3.8, 3.8, 3.7, 3.8, 3.7, 3.9,
                   3.7, 3.7, 3.8, 3.8, 3.7, 3.7, 3.7, 3.7, 3.8, 3.8, 3.7, 3.8, 3.7, 3.9, 3.8, 3.8, 3.7, 3.8, 3.7, 3.9,
                   3.7, 3.7, 3.8, 3.8, 3.7, 3.7, 3.7, 3.7, 3.8, 3.8, 3.7, 3.8, 3.7, 3.9, 3.8, 3.8, 3.7, 3.8, 3.7, 3.9],
                  [4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3,
                   5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1, 7.2, 7.3,
                   7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8.0, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 9.0, 9.1, 9.2, 9.3,
                   9.4, 9.5, 9.6, 9.7, 9.8, 9.9]],
    'proximity 1' : [[7, 8, 7, 7, 8, 7, 8, 8, 8, 8, 9, 8, 7, 8, 8, 8, 9, 8, 7, 8,
                      7, 8, 7, 7, 8, 7, 8, 8, 8, 8, 9, 8, 7, 8, 8, 8, 9, 8, 7, 8,
                      7, 8, 7, 7, 8, 7, 8, 8, 8, 8, 9, 8, 7, 8, 8, 8, 9, 8, 7, 8],
                     [4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2,
                      5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1,
                      7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8.0, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 9.0,
                      9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9]],
    'proximity 2' : [[8, 8, 8, 7, 7, 9, 6, 7, 7, 8, 8, 7, 9, 8, 7, 8, 8, 7, 9, 8,
                      8, 8, 8, 7, 7, 9, 6, 7, 7, 8, 8, 7, 9, 8, 7, 8, 8, 7, 9, 8,
                      8, 8, 8, 7, 7, 9, 6, 7, 7, 8, 8, 7, 9, 8, 7, 8, 8, 7, 9, 8],
                     [4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2,
                      5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1,
                      7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8.0, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 9.0,
                      9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9]],
    'temperature 1' : [[40, 40, 40, 40, 40, 40, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42,
                        40, 40, 40, 40, 40, 40, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42,
                        40, 40, 40, 40, 40, 40, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42],
                       [4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2,
                        5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1,
                        7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8.0, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 9.0,
                        9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9]],
    'temperature 2': [[43, 43, 43, 43, 43, 43, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44,
                       43, 43, 47, 43, 43, 43, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44,
                       43, 43, 43, 43, 43, 43, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44],
                      [4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2,
                       5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1,
                       7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8.0, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 9.0,
                       9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9]],
    'voltage 1' : [12.0, 12.3, 12.2, 12.1, 12.0, 11.9, 11.9, 12.0, 12.1, 12.1, 12.2,
                   12.0, 12.3, 12.2, 12.1, 12.0, 11.9, 11.9, 12.0, 12.1, 12.1, 12.2,
                   12.0, 12.3, 12.2, 12.1, 12.0, 11.9, 11.9, 12.0, 12.1, 12.1, 12.2],
    'voltage 2' : [11.9, 11.7, 11.8, 12.1, 11.9, 11.9, 11.9, 11.9, 12.1, 12.1, 11.8,
                   11.9, 11.7, 11.8, 12.1, 11.9, 11.9, 11.9, 11.9, 12.1, 12.1, 11.8,
                   11.9, 11.7, 11.8, 12.1, 11.9, 11.9, 11.9, 11.9, 12.1, 12.1, 11.8],
    'voltage 3': [12.0, 12.3, 12.2, 12.1, 12.0, 11.9, 11.9, 12.0, 12.1, 12.1, 12.2,
                  12.0, 12.3, 12.2, 12.1, 12.0, 11.9, 11.9, 12.0, 12.1, 12.1, 12.2,
                  12.0, 12.3, 12.2, 12.1, 12.0, 11.9, 11.9, 12.0, 12.1, 12.1, 12.2],
}

sensor_data = {}
index_trend = 0
index_trend_leap = 7
trend_length = 30
total_trend_length = 60

index_line = 0
total_line_length = 33

plot_details = {
    221 : {'type' : 'trend',
           'sensors' : ['position', 'velocity'],
           'title' : 'Position & Velocity'},
    224 : {'type' : 'trend',
           'sensors' : ['proximity 1', 'proximity 2'],
           'title' : 'Proximity'},
    222 : {'type' : 'trend',
           'sensors' : ['temperature 1', 'temperature 2'],
           'title' : 'Temperature'},
    223 : {'type' : 'line',
           'sensors' : ['voltage 1', 'voltage 2', 'voltage 3'],
           'title' : 'Voltage'}
}

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

    def __init__(self, plot_details, sensor_details, sensor_data):
        self.plotDetails = plot_details
        self.sensorDetails = sensor_details
        self.sensorData = sensor_data

    def drawBasics(self, key, value):
        '''These are the key and values for the plot_details dictionary'''
        plt.subplot(key)
        plt.title(value['title'])

class TrendPlot(BasicPlot):

    def __init__(self, plot_details, sensor_details, sensor_data):
        temp_plot_details = {}
        for key, value in plot_details.items():
            if value['type'] == 'trend':
                temp_plot_details[key] = value
        BasicPlot.__init__(self, temp_plot_details, sensor_details, sensor_data)

    def drawTrend(self):
        for key, value in self.plotDetails.items():
            self.drawBasics(key, value)
            for sensor in value['sensors']:
                plt.plot(self.sensorData[sensor][1], self.sensorData[sensor][0])

class LinePlot(BasicPlot):

    def __init__(self, plot_details, sensor_details, sensor_data):
        temp_plot_details = {}
        for key, value in plot_details.items():
            if value['type'] == 'line':
                temp_plot_details[key] = value
        BasicPlot.__init__(self, temp_plot_details, sensor_details, sensor_data)

    def drawLine(self):
        for key, value in self.plotDetails.items():
            self.drawBasics(key, value)
            for i, sensor in list(enumerate(value['sensors'])):
                plt.plot([self.sensorData[sensor], self.sensorData[sensor]], [i+0.2, i+0.8])


trend_plot = TrendPlot(plot_details, sensor_details, sensor_data)
line_plot = LinePlot(plot_details, sensor_details, sensor_data)

def all_plots():
    trend_plot.drawTrend()
    line_plot.drawLine()

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
