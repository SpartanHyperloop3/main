import json
import zmq
import time

def initialize_zmq_incoming(address, port):
    context = zmq.Context()
    incomingSocket = context.socket(zmq.SUB)
    incomingSocket.setsockopt(zmq.SUBSCRIBE,'')
    incomingSocket.connect('tcp://'+address+':'+port)
    return incomingSocket

def store_incoming_json(incoming_json):
    '''write incoming json to storage dictionary
    #check for sensors that aren't in dictionary and add them'''
    pass

def update_plotting_data():
    '''update the dictionary of lists that is sent to the graphing function with the right
    length as stated in the plot_details'''
    pass

def log_and_purse_sensor_data():
    '''periodically review the dictionary storing plotting _data and store unneeded _data to CSV
    then purge from dictionary'''
    pass

def setup(address, port):
    global sensor_data_storage, in_sock
    sensor_data_storage = {}
    in_sock = initialize_zmq_incoming(address, port)

def receive_and_parse():
    incoming_json = in_sock.recv_json()
    print(incoming_json)