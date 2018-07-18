import zmq
import time
import json
import random

def read_json(read_file):
    with open(read_file, 'r') as file:
        return json.loads(file.read())

def initialize_zmq_outgoing(address, port):
    context = zmq.Context()
    outgoing_socket = context.socket(zmq.PUB)
    outgoing_socket.bind('tcp://'+address+':'+port)
    return outgoing_socket

class generateSensorJson():

    def __init__(self, data, chunk_size=10):
        self._data = data
        self.chunkSize = chunk_size
        self._currentIndex = {}
        self._listLength = {}
        for key in self._data:
            self._currentIndex[key] = 0
            self._listLength[key] = len(self._data[key][0])

    def generateJson(self):
        output_json = {}
        for key in self._data:
            # the next increase will go beyond end of list, reset index
            if self._currentIndex[key]+self.chunkSize > self._listLength[key]:
                self._currentIndex[key] = 0

            output_json[key] = {'reading' : self._data[key][0][self._currentIndex[key]:self._currentIndex[key] + self.chunkSize],
                                'time' : self._data[key][1][self._currentIndex[key]:self._currentIndex[key] + self.chunkSize]}
            self._currentIndex[key] = self._currentIndex[key] + self.chunkSize
        return output_json


generate_sensor_json = generateSensorJson(read_json('sensor_data_raw_test.json'), 3)
out_sock = initialize_zmq_outgoing('127.0.0.1', '6000')

while (True):
    #raw_input('wait...')
    generate_sensor_json.chunkSize = random.randint(1, 5)
    out_sock.send_json(generate_sensor_json.generateJson())
    time.sleep(random.random()*4)