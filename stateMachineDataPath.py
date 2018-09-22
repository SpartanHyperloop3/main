#!/usr/bin/python
import serial
import zmq
import time
import threading
import copy
import sys
import json
import RPi.GPIO as GPIO
import smbus
import Queue
import dataController
import pdb
import pigpio
import struct
import math

class stateMachineDataPath(object):
    """Sets the outputs based on state and reports feedback.


    """
    class incomingDataThread(threading.Thread):
        """Retrieves incoming data from master.

        Creates a thread object that collects data from the master
        controller. Data should be sent as a list with the first object
        being a string identifying the type of data sent ["data_type", data].
        State data is denoted by string "state", and upon recieving state data
        an event in outer class stateMachineDataPath (currentStateHasChanged)
        is set to notify the outputsThread that the states has changed.
        """
        def __init__(self, control, zmqSock, incomingDataQueue):
            """incomingDataThread constructor.

            Initializes dataThread

            Args:
                control: must pass outer class object to obtain access to methods.
                zmqSock: current socket for incoming data
            """
            threading.Thread.__init__(self)
            self.name = "incoming_data"
            self._killFlagIn = threading.Event()
            self.control = control
            self.sock = zmqSock
            self.poller = zmq.Poller()
            self.poller.register(self.sock, zmq.POLLIN)
            self.queue = incomingDataQueue

        def run(self):
            while not self._killFlagIn.is_set():
                if self.poller.poll(1000):
                    message = self.sock.recv_json()
                    self.queue.put(message)
                    print message



        def stop(self):
            self._killFlagIn.set()




    class outgoingDataThread(threading.Thread):

        def __init__(self, control, zmqSock, outgoingDataQueue, stateCheckQueue):
            threading.Thread.__init__(self)
            self._killFlag = threading.Event()
            self.control = control
            self.name = "data_send_thread"
            self.sock = zmqSock
            self.poller = zmq.Poller()
            self.poller.register(self.sock, zmq.POLLOUT)
            self.queue = outgoingDataQueue
            self.stateCheckQueue = stateCheckQueue

        def run(self):
            while not self._killFlag.is_set():
                if self.poller.poll(1000):
                    try:
                        data = self.stateCheckQueue.get(False)
                        #data = self.stateCheckQueue.get(True,0.01)
                    except Queue.Empty:
                        pass
                    else:
                        print "got here",data
                        self.sock.send_json(data)
                        self.stateCheckQueue.task_done()

                    try:
                        data = self.queue.get(False)
                        #data = self.queue.get(True,0.01)
                    except Queue.Empty:
                        pass
                    else:
                        self.sock.send_json(data)
                        self.queue.task_done()

        def stop(self):
            self._killFlag.set()





    class outputsThread(threading.Thread):
        """Controls setting outputs on state updates

        Waits for currentStateHasChanged event to be set then sets outputs
        according to the state.
        """
        def __init__(self, control, incomingDataQueue):
            threading.Thread.__init__(self)
            self._killFlagOut = threading.Event()
            self.control = control
            self.name = "output_control"
            self.queue = incomingDataQueue


        def run(self):
            while not self._killFlagOut.is_set():
                try:
                    data = self.queue.get(True, 2.0)
                except Queue.Empty:
                    pass
                else:
                    if data[0] == "state":
                        self.control.currentState = data[1]
                        self.control.stateCheckQueue.put(["slave_state", self.control.piName, self.control.currentState])
                        #if self.control.okForOutputChange.is_set():
                        self.control.setOutputsByState()
                    elif data[0] == "cmd":
                        pass
                    self.queue.task_done()


        def stop(self):
            self._killFlagOut.set()




    class I2Cconsumer(threading.Thread):
        """Gets readings from the ADCs.

        Takes a request for a reading from a queue which holds the chip
        address and channel to read from and sends the data to the master.
        """
        def __init__(self, control, I2Cqueue, manualCmdI2C):
            threading.Thread.__init__(self)
            self.name = "I2C_consumer_thread"
            self._killFlag = threading.Event()
            self.control = control
            self.queue = I2Cqueue
            self.manualQueue = manualCmdI2C
            self.reading = []
            self.manualCmd = 0

        def run(self):
            while not self._killFlag.is_set():
                self.manualCmd = 0
                try:
                    nextJob = self.manualQueue.get(True, 0.01)
                    self.manualCmd = nextJob["manual_cmd"]
                except Queue.Empty:
                    self.manualCmd = 0
                else:
                    #print "manual:"
                    #print nextJob
                    switch = {
                            "i2c" : self.I2Cops,
                            "serial" : self.SERops
                    }
                    switch.get(nextJob["bus"], "invalid function")(nextJob)
                    self.manualQueue.task_done()
                    #print "manual task done"
                    self.manualCmd = 0

                try:
                    nextJob = self.queue.get(True, 0.01)
                    #print "state i2c:", nextJob[0]
                    #print nextJob[0], nextJob[1], nextJob[2]
                except Queue.Empty:
                    pass
                except:
                    pass
                else:
                    switch = {
                            "i2c" : self.I2Cops,
                            "serial" : self.SERops
                    }
                    switch.get(nextJob["bus"], "invalid function")(nextJob)
                    self.queue.task_done()






        ########################################################
        # I2C Bus read functions                               #
        ########################################################
        def readByteData(self, nextJob):
            bus = smbus.SMBus(1)
            if nextJob["pec"] == 1:
                bus.pec = True
            else:
                bus.pec = False
            result = bus.read_byte_data(nextJob["address"], nextJob["read"][0])
            return result

        def readByteData2C(self, nextJob):
            data = self.readByteData(nextJob)
            if data >= 0x80:
                data = -((data^0xff)+1)
            return data

        def readWord(self, nextJob):
            bus = smbus.SMBus(1)
            if nextJob["pec"] == 1:
                bus.pec = True
            else:
                bus.pec = False

            result = bus.read_word_data(nextJob["address"], nextJob["read"][0])
            return result

        def readWord2C(self, nextJob):
            data = self.readWord(nextJob)
            if data >= 0x8000:
                data = -((data^0xffff)+1)
            return data

        def readBlock(self, nextJob):
            #print nextJob["address"], nextJob["read"]
            bus = smbus.SMBus(1)
            if nextJob["pec"] == 1:
                bus.pec = True
            else:
                bus.pec = False
            result = bus.read_i2c_block_data(nextJob["address"], nextJob["read"][0])
            time.sleep(0.001)
            result = bus.read_i2c_block_data(nextJob["address"], nextJob["read"][0])
            return result

        def readBlock2C(self, nextJob):
            data = self.readBlock(nextJob)
            for byte in data:
                if byte >= 0x80:
                    byte = -((byte^0xff)+1)
            return data


        ########################################################
        # I2C Bus write functions                              #
        ########################################################
        def writeByte(self, addr, data):
            bus = smbus.SMBus(1)
            if nextJob["pec"] == 1:
                bus.pec = True
            else:
                bus.pec = False
            bus.write_byte(addr, data)

        def writeByteData(self, addr, cmd, data):
            bus = smbus.SMBus(1)
            if nextJob["pec"] == 1:
                bus.pec = True
            else:
                bus.pec = False
            bus.write_byte_data(addr, cmd, data)

        def writeWordData(self, nextJob):
            bus = smbus.SMBus(1)
            if nextJob["pec"] == 1:
                bus.pec = True
            else:
                bus.pec = False
            bus.write_word_data(nextJob["address"], nextJob["cmd"], nextJob["data"])
        ###########################################################
        # Serial write functions
        ###########################################################
        def writeSER(self, dev, addr, data, crc):
            dev.write(data)
            time.sleep(0.01)


        ###########################################################
        # Serial read functions
        ###########################################################
        def readSER(self, dev, addr, dataLen, crc):
            reading = ""
            reading = dev.read(4)
            time.sleep(0.01)
            try:
                s = struct.unpack('>I', reading)
            except:
                pass
            reading = getattr(self, callback)(reading, *callbackArgs)
            try:
                return s[0]
            except:
                return s
        ############################################################
        # R/W automation functions
        ############################################################
        def writeOps(self, nextJob):
            for writeData in nextJob["write"]:
                if len(writeData) == 2:
                    self.writeByteData(nextJob["address"], writeData[0], writeData[1])
                    time.sleep(0.1)
                elif len(writeData) == 1:
                    self.writeByte(nextJob["address"], writeData[0])


        def readOps(self, nextJob):
            if nextJob["data_length"] == "byte":
                if nextJob["data_type"] == "2c":
                    reading = self.readByte2C(nextJob)
                    reading = getattr(self, nextJob["callback"]["function"])(reading,*nextJob["callback"]["args"])

                elif nextJob["data_type"] == "pos":
                    reading = self.readByte(nextJob)
                    reading = getattr(self, nextJob["callback"]["function"])(reading,*nextJob["callback"]["args"])

            elif nextJob["data_length"] == "word":
                if nextJob["data_type"] == "2c":
                    reading = self.readWord2C(nextJob)
                    reading = getattr(self, nextJob["callback"]["function"])(reading,*nextJob["callback"]["args"])

                elif nextJob["data_type"] == "pos":
                    reading = self.readWord(nextJob)
                    reading = getattr(self, nextJob["callback"]["function"])(reading,*nextJob["callback"]["args"])

            elif nextJob["data_length"] == "block":
                if nextJob["data_type"] == "2c":
                    reading = self.readBlock2C(nextJob)
                    reading = getattr(self, nextJob["callback"]["function"])(reading,*nextJob["callback"]["args"])

                elif nextJob["data_type"] == "pos":
                    reading = self.readBlock(nextJob)
                    reading = getattr(self, nextJob["callback"]["function"])(reading,*nextJob["callback"]["args"])

            #print nextJob["sensor_name"],reading
            return reading



        def SERops(self, nextJob):
            if nextJob["write"]:
                self.writeSER(nextJob["dev"], nextJob["reg"], nextJob["write"], nextJob["crc_write"])
            if nextJob["readLen"] > 0:
                self.reading = self.readSER(nextJob["dev"], nextJob["reg"], nextJob["readLen"], nextJob["crc_read"])
                timeOfReading = time.time()
                packet = ["logic", nextJob["sensor_name"], self.reading, timeOfReading]
                self.control.rawData.updateEntry(nextJob["sensor_name"], [self.reading, timeOfReading])
                self.control.sendQueue.put(packet)


        def I2Cops(self, nextJob):
            #print "I2Cops"
            if nextJob["operations"] == "ini":
                if nextJob["data_type"] == "byte":
                    self.writeByteData(nextJob["address"], nextJob["cmd"], nextJob["data"])
                elif nextJob["data_type"] == "word":
                    self.writeWordData(nextJob)

            elif nextJob["operations"] == "RW":
                self.writeOps(nextJob)
                self.reading = self.readOps(nextJob)
                timeOfReading = time.time()
                #packet = [nextJob["sensor_name"], self.reading, timeOfReading]
                #self.control.rawData.updateEntry(nextJob["sensor_name"], [self.reading, timeOfReading])
                #self.control.sendQueue.put(packet)

            elif nextJob["operations"] == "R":
                self.reading = self.readOps(nextJob)
                timeOfReading = time.time()
                #packet = [nextJob["sensor_name"], self.reading, timeOfReading]
                #self.control.rawData.updateEntry(nextJob["sensor_name"], [self.reading, timeOfReading])
                #self.control.sendQueue.put(packet)

            elif nextJob["operations"] == "W":
                self.writeOps(nextJob)

            #if nextJob["sensor_name"] == "PI_1_U1_CH2":
            #    print nextJob["sensor_name"],self.reading
            packet = ["logic", nextJob["sensor_name"], self.reading, timeOfReading]
            self.control.rawData.updateEntry(nextJob["sensor_name"], [self.reading, timeOfReading])

            self.averagedReading(nextJob["sensor_name"], 100)
            if self.manualCmd == 1:
                #print "this is a manual packet"
                #print packet
                self.control.manualCmdOutSocket.send_json(packet)
                #self.control.manualCmdSendQueue.put(packet)
                #print "========================================\n\n"
            else:
                #print "this is a sensor packet"
                #print packet
                self.control.sendQueue.put(packet)
                #print "========================================\n\n"

        #################################################
        # data processing callback functions start here #
        #################################################
        def ADCtoVolts12Bit(self, reading):
            upper = (reading[0] & 15)
            upper = (upper << 8)
            total = upper + reading[1]
            voltage = float(total * .001)
            return voltage

        def pressureSen(self, reading):
            voltage = self.ADCtoVolts12Bit(reading)
            current = self.control.map(voltage, 0.59046, 2.97, 0.004023, 0.019979)
            pressure = self.control.map(current, 0.004023, 0.02, 0.000, 300.000)
            return pressure

        def proxRead(self, reading):
            pass

        def convertByLSB(self, reading, lsb):
            result = reading/lsb
            return result

        def convertIRtemp(self, reading):
            result = (reading * 0.02) - 273.15
            return result
            #return hex(reading)

        def raw(self, reading):
            return reading

        def thermistor100k(self, reading, resistance):
            voltage = self.ADCtoVolts12Bit(reading)
            try:
                rth = resistance*(2.023/voltage - 1)
                denom = 100000*math.exp(-3950/298.15)
                result = 3950/math.log(rth/denom)
                result = result - 273.15
            except:
                result = 0

            return result

        def averagedReading(self, sensorName, n):
            i = -1 
            result = 0.0
            for _ in range(0,n):
                reading = None
                try:
                    reading = self.control.rawData.retrieveEntryByOffset(sensorName, i)[0]
                except:
                    pass
                if reading == None or reading == "I":
                    reading = 0
                    n -= 1
                #print i,reading
                result += reading
                #print "result ", result
                i -= 1
            try:
                result = float(result/n)
            except:
                result = 0
            #print "reading %f"%result
            return result


        def BMSvoltage(self, reading):
            voltage = self.ADCtoVolts12Bit(reading)
            vout = voltage * 960800 / 6800
            return vout


        def batteryCurrent(self, reading):
            vout = self.BMSvoltage(reading)
            current_read = (( 5 / 5.188) * (vout - 2.589)) * (1/0.025016)
            return current_read


        def stop(self):
            self._killFlag.set()





    class I2Cthread(threading.Thread):

        def __init__(self, control, name, configData, sensorList, I2Cqueue):
            threading.Thread.__init__(self)
            self.name = name
            self._killFlag = threading.Event()
            self.queue = I2Cqueue
            self.samplingPeriod = configData["sample_rate"]
            self.bus = configData["bus"]
            try:
                self.initData = configData["init"]
            except KeyError:
                pass
            self.sensorList = sensorList
            self.daemon = True

        def run(self):
            try:
                for init in self.initData:
                    self.queue.put(
                            {
                                "bus" : self.bus,
                                "address" : init["location"],
                                "cmd" : init["register"],
                                "data" : init["data"],
                                "data_type" : init["data_type"],
                                "operations" : "ini",
                                "pec" : init["pec"]
                            })
            except:
                pass
            while not self._killFlag.is_set():
                for sensor,attr in self.sensorList.items():
                    self.queue.put(
                            {
                                "bus" : self.bus,
                                "operations" : attr["operations"],
                                "address" : attr["location"],
                                "write" : attr["write"],
                                "read" : attr["read"],
                                "sensor_name" : sensor,
                                "data_length" : attr["data_length"],
                                "data_type" : attr["data_type"],
                                "callback" : attr["data_processing_callback"],
                                "pec" : attr["pec"]
                            })
                time.sleep(self.samplingPeriod)




    class SERthread(threading.Thread):

        def __init__(self, control, name, configData, sensorList, I2Cqueue):
            threading.Thread.__init__(self)
            self.name = name
            self._killFlag = threading.Event()
            self.queue = I2Cqueue
            self.samplingPeriod = configData["sample_rate"]
            self.ser = serial.Serial(configData["device"], configData["baud"], serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=0)
            self.baud = configData["baud"]
            self.bus = configData["bus"]

            self.bytes = {}


            try:
                self.initData = configData["init"]
            except KeyError:
                pass

            self.sensorList = sensorList
            self.daemon = True

            for sensor,attr in self.sensorList.items():
                data = bytearray.fromhex(attr["write"])
                self.bytes[sensor] = data

        def run(self):
            try:
                for init in self.initData:
                    self.queue.put(
                            {
                                "address" : init["location"],
                                "cmd" : init["reg"],
                                "data" : init["data"],
                                "operations" : "ini"
                            })
            except:
                pass
            while not self._killFlag.is_set():
                for sensor,attr in self.sensorList.items():
                    self.queue.put(
                            {
                                "bus" : self.bus,
                                "dev" : self.ser,
                                "reg" : attr["register"],
                                "write" : self.bytes[sensor],
                                "readLen" : attr["read_len"],
                                "sensor_name" : sensor,
                                "crc_write" : attr["crc_write"],
                                "crc_read" : attr["crc_read"],
                                "data_type" : attr["data_type"],
                                "callback" : attr["data_processing_callback"]
                            })

                time.sleep(self.samplingPeriod)





    class functionThread(threading.Thread):

        def __init__(self, control, name, args):
            threading.Thread.__init__(self)
            self.name = name
            self.args = args
            self.control = control
            self._killFlag = threading.Event()
            self.daemon = True

        def run(self):
            self.control.startFunc(self.name, self.args)



    class manualCmdInThread(threading.Thread):
        def __init__(self, control, manualCmdInSocket, manualCmdQueue):
            threading.Thread.__init__(self)
            self.control = control
            self.socket = manualCmdInSocket
            self.daemon = True
            self.queue = manualCmdQueue
            self.poller = zmq.Poller()
            self.poller.register(self.socket, zmq.POLLIN)

        def run(self):
            while 1:
                if self.poller.poll(1000):
                    message = self.socket.recv_json()
                    self.queue.put(message)


    class manualCmdOutThread(threading.Thread):
        def __init__(self, control, manualCmdSocket, manualCmdQueue, manualCmdSendQueue):
            threading.Thread.__init__(self)
            self.control = control
            self.socket = manualCmdSocket
            self.daemon = True
            self.queue = manualCmdQueue
            self.sendQueue = manualCmdSendQueue
            #self.poller = zmq.Poller()
            #self.poller.register(self.socket, zmq.POLLOUT)

        def run(self):
            while 1:
                try:
                    cmd = self.queue.get(True, 1.0)
                except Queue.Empty:
                    pass
                else:
                    self.manualCmd(self.control, cmd)
                    self.queue.task_done()

                #try:
                #    packet = self.control.manualCmdSendQueue.get(True, 0.01)
                #except Queue.Empty:
                #    pass
                #else:
                #    socket.send_json(packet)



        def manualCmd(self, control, cmd):
            try:
                if cmd[0] == self.control.piName:
                    if cmd[1] == "gpio_write":
                        self.control.writeGPIOoutput(cmd[2], cmd[3])
                    elif cmd[1] == "gpio_read":
                        #print "got here"
                        result = GPIO.input(cmd[2])
                        
                        #result = GPIO.output(cmd[2], not GPIO.input(cmd[2]))
                        #print cmd[1],result
                        self.socket.send_json(result)
                        #self.control.manualCmdSendQueue.put(result)
                    elif cmd[1] == "serial":
                        pass
                    elif cmd[1] == "i2c":
                        self.control.I2CmanualCmdQueue.put(cmd[2])
            except:
                pass




    def __init__(self, setInitialState = 0, piName="", stateOutputsJSONfile = None, sensorInitializationJSONfile = None, buttonInitializationJSONfile = None, incomingSocket = None, outgoingSocket = None):
        """stateMachineDataPath constructor.

        Args:
            setInitialState: sets the initial stat attribute.
            stateOutputsJSONfile: contains information on outputs for each state.
            sensorInitializationJSONfile: contains information about which ADC channels
            and GPIO pins will be used for sensor readings and inputs.
            incomingSocket: incoming data socket.
            outgoingSocket: outgoind data socket.
        """
        context = zmq.Context()
        self.incomingSocket = context.socket(zmq.SUB)
        self.incomingSocket.setsockopt(zmq.SUBSCRIBE, '')
        self.incomingSocket.connect("tcp://%s:6000"%sys.argv[1])

        self.outgoingSocket = context.socket(zmq.PUB)
        self.outgoingSocket.bind("tcp://*:5000")

        self.manualCmdInSocket = context.socket(zmq.SUB)
        self.manualCmdInSocket.setsockopt(zmq.SUBSCRIBE, '')
        self.manualCmdInSocket.connect("tcp://%s:5020"%sys.argv[1])
        self.manualCmdOutSocket = context.socket(zmq.PUB)
        self.manualCmdOutSocket.bind("tcp://*:5010")

        GPIO.setmode(GPIO.BCM)

        self.piName = piName
        self.pi = pigpio.pi()

        self.currentState = setInitialState
        self.currentStateHasChanged = threading.Event()
        self.ADCthreads = []
        self.I2Cthreads = []
        self.SERthreads = []
        self.rawData = dataController.dataController()

        self.I2Cqueue = Queue.Queue()
        self.sendQueue = Queue.Queue()
        self.incomingDataQueue = Queue.Queue()
        self.stateCheckQueue = Queue.Queue()
        self.manualCmdQueue = Queue.Queue()
        self.manualCmdSendQueue = Queue.Queue()
        self.I2CmanualCmdQueue = Queue.Queue()

        self.outgoingDataThread = self.outgoingDataThread(self, self.outgoingSocket, self.sendQueue, self.stateCheckQueue)
        self.manualMode = 0
        self.incomingDataThread = self.incomingDataThread(self, self.incomingSocket, self.incomingDataQueue)
        self.outputsThread = self.outputsThread(self, self.incomingDataQueue)
        self.lock = threading.Lock()
        self.I2CconsumerThread = self.I2Cconsumer(self, self.I2Cqueue, self.I2CmanualCmdQueue)

        self.manualCmdInThread = self.manualCmdInThread(self, self.manualCmdInSocket, self.manualCmdQueue)
        self.manualCmdOutThread = self.manualCmdOutThread(self, self.manualCmdOutSocket, self.manualCmdQueue, self.manualCmdSendQueue)


        #output JSON file parsing starts here
        try:
            f = open(stateOutputsJSONfile, "r")
            outputJSON = json.loads(f.read())

            self.outputsGPIObyState = {}
            for key,val in outputJSON.items():
                self.outputsGPIObyState[key] = val["GPIO"]

            self.outputFunctionsByState = {}
            for key,val in outputJSON.items():
                self.outputFunctionsByState[key] = val["function"]

            self.outputsGPIO = []
            for key,val in outputJSON.items():
                for pin in val["GPIO"]:
                    if pin[0] not in self.outputsGPIO:
                        self.outputsGPIO.append(pin[0])

            self.outputsPWMbyState = {}
            for key,val in outputJSON.items():
                self.outputsPWMbyState[key] = val["PWM"]

            self.outputsPWM = []
            for key,val in outputJSON.items():
                for pwm in val["PWM"]:
                    if [pwm[0],pwm[1]] not in self.outputsPWM:
                        self.outputsPWM.append([pwm[0],pwm[1]])

            self.PWMobjects = {}
            f.close()


        except (IOError, TypeError):
            print "Could not open state output JSON file: %s" % stateOutputsJSONfile


        #input JSON file parsing starts here
        try:
            f = open(sensorInitializationJSONfile, "r")
            self.inputsfile = json.loads(f.read())

            self.inputNames = []
            for val in self.inputsfile.values():
                for inputs in val[1]:
                    self.inputNames.append(inputs)

            f.close()

        except (IOError, TypeError):
            print "Could not open sensor and input JSON file: %s" % sensorInitializationJSONfile



        try:
            f = open(buttonInitializationJSONfile, "r")
            buttonFile = json.loads(f.read())

            self.digitalInputs = {}
            for key,val in buttonFile.items():
                self.digitalInputs[key] = { "location" : val["location"], "PUD" : val["PUD"]}

            f.close()
        except (IOError, TypeError):
            print "Could not open button initialization JSON file: %s" % buttonInitializationJSONfile 



    def setOutputsByState(self):
        """sets the outputs on state change

        When the state is changed this function is called to change outputs
        by state.
        """
        try:
            for output in self.outputsGPIObyState["%s"%self.currentState]:
                self.writeGPIOoutput(output[0], output[1])
                print "Current state of pin %s is: %s\n"%(output[0],GPIO.input(output[0]))

            for func in self.outputFunctionsByState["%s"%self.currentState]:
                if func["threaded"] == 0:
                    self.startFunc(func["name"], func["arguments"])

            for pwm in self.outputsPWMbyState["%s"%self.currentState]:
                self.PWMobjects[pwm[0]].ChangeDutyCycle(pwm[2])

        except KeyError:
            print "State number not in JSON file"



    def initializeInputsAndSensors(self):
        """Initializes inputs and sensors"""
        for names in self.inputNames:
            self.rawData.createNewEntry(names)

        for thread,setup in self.inputsfile.items():
            if setup[0]["bus"] == "i2c":
                t = self.I2Cthread(self, thread, setup[0], setup[1], self.I2Cqueue)
                self.I2Cthreads.append(t)
            elif setup[0]["bus"] == "serial":
                t = self.SERthread(self, thread, setup[0], setup[1], self.I2Cqueue)
                self.SERthreads.append(t)


        for key,val in self.digitalInputs.items():
            GPIO.setup(val["location"], GPIO.IN, pull_up_down=getattr(GPIO, val["PUD"]) )
            t = self.functionThread(self, "buttonWatch", [val["location"], key])
            t.start()
            #GPIO.add_event_detect(val["location"], GPIO.RISING, bouncetime=200)
            #GPIO.add_event_callback(val["location"], lambda channel, arg1 = key, arg2 = 1: self.GPIOevent(arg1, arg2))


    def buttonWatch(self, pin, varName):
        currentState = 0
        while True:
            if not GPIO.input(pin):
                currentState ^= 1
                self.sendQueue.put(["logic",varName,currentState,time.time()])
                time.sleep(1)

            time.sleep(0.001)


    def initializeOutputs(self):
        """Initializes outputs"""
        for output in self.outputsGPIO:
            GPIO.setup(output, GPIO.OUT)

        for pwm in self.outputsPWM:
            GPIO.setup(pwm[0], GPIO.OUT)
            self.PWMobjects[pwm[0]] = GPIO.PWM(pwm[0],pwm[1])
            #start PWM at 0% duty cycle
            self.PWMobjects[pwm[0]].start(0)

        for obj in self.outputFunctionsByState.values():
            for func in obj:
                if func["threaded"] == 1:
                    t = self.functionThread(self, func["name"], func["arguments"])
                    t.start()


    def startThreads(self):
        self.incomingDataThread.start()
        self.outgoingDataThread.start()
        self.outputsThread.start()
        self.I2CconsumerThread.start()
        self.manualCmdInThread.start()
        self.manualCmdOutThread.start()
        for thread in self.I2Cthreads:
            thread.start()
        for thread in self.SERthreads:
            thread.start()


    def stopThreads(self):
        print "Killing ADC consumer thread.."
        print "done.."
        self.I2CconsumerThread.stop()
        self.I2CconsumerThread.join()
        print "Killing output thread.."
        self.outputsThread.stop()
        self.outputsThread.join()
        print "done.."
        print "killng incoming data thread.."
        self.incomingDataThread.stop()
        self.incomingDataThread.join()
        print "done.."
        print "killng outgoing data thread.."
        self.outgoingDataThread.stop()
        self.outgoingDataThread.join()
        print "done..goodbye"



    def writeGPIOoutput(self, pin, state):
        """Writes to a pin if it is not an input"""
        if not self.isGPIOinput(pin):
            GPIO.output(pin, state)
        else:
            print "GPIO pin %s is an input"%pin



    def printState(self, *args):
        """Test func"""
        print "The current state is: %s"%self.currentState
        print "arguments passed to func:"
        print args



    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


    def PWMtest(self):
        
        #for dc in range(0, 100000, 1000):l
        #    self.pi.hardware_PWM(18, 60, dc)
        #while self.currentState == 2:
        #self.PWMobjects[14].ChangeDutyCycle(12)
        start = 0
        while True:
            if self.currentState == 2:
                if start == 0:
                    for dc in range(50000, 100000, 1000):
                        self.pi.hardware_PWM(18, 60, dc)
                    start = 1
            else:
                start = 0
                self.pi.hardware_PWM(18, 60, 0)



    def startFunc(self, name, args):
        """Starts a function"""
        getattr(self, name)(*args)



    def isGPIOinput(self, pin):
        """Determines if a pin is an input

        Args:
            pin: the pin to check.

        Returns:
            True if the pin is set as an input.
        """
        result = False
        try:
            for key in self.digitalInputs.keys():
                if pin == self.digitalInputs[key]["location"]:
                    result = True
        except KeyError:
            print "key error"
        return result
    def __enter__(self):
        return self

    def createConnections(self):
        self.outgoingSocket.bind("tcp://%s:6000"%self.connections["master"]["ip"])

        for key,conn in self.connections.items():
            if key != "master":
                print key,conn,"tcp://%s:5000"%conn["ip"]
                self.incomingSocket.connect("tcp://%s:5000"%conn["ip"])
                self.incomingSocket.setsockopt(zmq.SUBSCRIBE, '')



if __name__ == "__main__":
    exitFlag = 0
    dataPath = stateMachineDataPath(1, "PI_A", "Outputs.json", "Sensors.json", "Buttons.json")

    globalLock = threading.Lock()
    dataPath.initializeInputsAndSensors()
    dataPath.initializeOutputs()
    dataPath.startThreads()
    #GPIO.output(8,1)
    #print GPIO.input(8)
    #print GPIO.output(8, not GPIO.input(8))
    print "Enter 1 to exit.."

    while True:
        try:
            exitFlag = input()
            if exitFlag == 1:
                print "Stopping Threads.."
                dataPath.stopThreads()
                dataPath.pi.hardware_PWM(18, 60, 0)
                GPIO.cleanup()
                sys.exit()
        except (SyntaxError, NameError):
            pass
