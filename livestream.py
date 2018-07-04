import time
import matplotlib.pyplot as plt
import random
from drawnow import *

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

plot_layout = {
    221 : {'type' : 'trend',
           'sensors' : ['position', 'velocity']},
    224 : {'type' : 'trend',
           'sensors' : ['proximity 1', 'proximity 2']},
    222 : {'type' : 'trend',
           'sensors' : ['temperature 1', 'temperature 2']},
    223 : {'type' : 'line',
           'sensors' : ['voltage 1', 'voltage 2', 'voltage 3']}
}

def index_update():
    global index_trend, index_line
    for key, value in plot_layout.items():

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

def trend_plot():
    for key, value in plot_layout.items():
        if value['type'] == 'trend':
            plt.subplot(key)
            plt.title(value['sensors'][0])
            for sensor in value['sensors']:
                plt.plot(sensor_data[sensor][1], sensor_data[sensor][0])
                x_min = min(sensor_data[sensor][1])
                x_max = max(sensor_data[sensor][1])
            plt.fill_between([x_min, x_max], [45, 45], [50, 50], alpha=0.3, color='red')
            plt.fill_between([x_min, x_max], [35, 35], [40, 40], alpha=0.3, color='red')
            plt.fill_between([x_min, x_max], [40, 40], [45, 45], alpha=0.3, color='green')
            # parse the sensor json to determine the color limits

def line_plot():
    for key, value in plot_layout.items():
        if value['type'] == 'line':
            plt.subplot(key)
            plt.title(value['sensors'][0])
            lower_limit = 11.5
            upper_limit = 12.5
            for i, sensor in list(enumerate(value['sensors'])):
                plt.plot([sensor_data[sensor], sensor_data[sensor]], [i+0.2, i+0.8])
                plt.text(sensor_data[sensor], i+0.85, sensor_data[sensor], horizontalalignment='center')
                plt.text(lower_limit, i+0.5, lower_limit, horizontalalignment='right')
                plt.text(upper_limit, i+0.5, upper_limit, horizontalalignment='left')
            plt.fill_between([lower_limit-1, lower_limit], [0, 0], [3, 3], alpha=0.3, color='red')
            plt.fill_between([upper_limit, upper_limit+1], [0, 0], [3, 3], alpha=0.3, color='red')
            plt.fill_between([lower_limit, upper_limit], [0, 0], [3, 3], alpha=0.3, color='green')
            #parse the sensor json to determine the color limits

def all_plots():
    trend_plot()
    line_plot()

#for n in range(0,round(total_trend_length/index_trend_leap)):
while(True):
    index_start = time.time()
    index_update()
    index_end = time.time()
    print('index_trend: %.5f' % (index_end - index_start))
    plot_start = time.time()
    drawnow(all_plots)
    plot_end = time.time()
    print('plot: %.5f' % (plot_end - plot_start))
    #time.sleep(5)