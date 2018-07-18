import json
import zmq
import time

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
    for sensor in graph_time_limit:
        # 0, send all data all the time
        # need to search and splice
        # need to send all cause too short

        untrimmed_time = data_storage[sensor][1][-1] - data_storage[sensor][1][graph_slice_start[sensor]]
        adjustment = graph_time_limit[sensor]/untrimmed_time
        untrimmed_length = len(data_storage[sensor][1]) - graph_slice_start[sensor] - 1
        trimmed_length = int(adjustment*untrimmed_length)
        # this function incomplete

        if graph_time_limit[sensor] == 0:
            pass
    pass

def log_and_purge_sensor_data():
    '''periodically review the dictionary storing plotting _data and store unneeded _data to CSV
    then purge from dictionary'''
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
    log_and_purge_sensor_data()