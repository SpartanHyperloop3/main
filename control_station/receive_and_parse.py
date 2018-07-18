import json
import zmq
import time
import math

def read_json(read_file):
    with open(read_file, 'r') as file:
        return json.loads(file.read())

def initialize_zmq_incoming(address, port):
    context = zmq.Context()
    incomingSocket = context.socket(zmq.SUB)
    incomingSocket.setsockopt(zmq.SUBSCRIBE,'')
    incomingSocket.connect('tcp://'+address+':'+port)
    return incomingSocket

def store_incoming_json(incoming_json):
    '''write incoming json to storage dictionary
    '''
    for key in incoming_json:
        if key in data_storage:
            data_storage[key][0].extend(incoming_json[key]['reading'])
            data_storage[key][1].extend(incoming_json[key]['time'])

        # check for sensors that aren't in dictionary and add them
        else:
            data_storage[key] = [incoming_json[key]['reading'], incoming_json[key]['time']]

def update_plotting_data():
    '''update the dictionary of lists that is sent to the graphing function with the right
    length as stated in the plot_details'''

    #adjust graph_slice_start and then adjust graph_data
    for sensor in graph_time_limit:

        # 0, send all data all the time, so don't adjust graph_slice_start
        if graph_time_limit[sensor] == 0:
            pass

        # adjust the slice length if the untrimmed_time is longer than the desired graph_time_limit
        else:
            untrimmed_time = abs(data_storage[sensor][1][-1] - data_storage[sensor][1][graph_slice_start[sensor]])
            #adjust if too long
            if untrimmed_time > graph_time_limit[sensor]:
                adjustment = graph_time_limit[sensor]/untrimmed_time #.70
                total_length = len(data_storage[sensor][1])
                untrimmed_length = total_length - graph_slice_start[sensor]
                trimmed_length = int(math.ceil(adjustment*untrimmed_length))
                graph_slice_start[sensor] = total_length - trimmed_length

        graph_data[sensor] = [data_storage[sensor][0][graph_slice_start[sensor]:], data_storage[sensor][1][graph_slice_start[sensor]:]]

def log_and_purge_sensor_data(buffer_factor):
    '''periodically review the dictionary storing plotting _data and store unneeded _data to CSV
    then purge from dictionary'''
    #max(dict.values())
    #only look at max sensor? then cull at that point? but skip sensors with time limit of 0
    for sensor in graph_time_limit:
        max(data_storage[sensor][1]) - min(data_storage[sensor][1])
    if
    pass

def setup(address, port):
    global data_storage, in_sock, graph_data, graph_time_limit, graph_slice_start
    data_storage = {}
    graph_data = {}
    graph_time_limit = {}
    graph_slice_start = {}
    in_sock = initialize_zmq_incoming(address, port)
    plot_details = read_json('plot_details.json')
    for key in plot_details:
        for sensor in plot_details[key]['sensors']:
            graph_time_limit[sensor] = float(plot_details[key]['time'])
            graph_slice_start[sensor] = 0

def receive_and_parse():
    incoming_json = in_sock.recv_json()
    store_incoming_json(incoming_json)
    update_plotting_data()
    log_and_purge_sensor_data(10)