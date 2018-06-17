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
import subprocess

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
        def __init__(self, control, zmqSock):
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

        def run(self):
            while not self._killFlagIn.is_set():
                if self.poller.poll(1000):
                    message = self.sock.recv_json()
                    if message[0] == "state":
                        self.control.currentState = message[1]
                        self.control.currentStateHasChanged.set()
                        self.control._killFuncs.set()
                    elif message[0] == "cmd":
                        pass

        def stop(self):
            self._killFlagIn.set()


    class outputsThread(threading.Thread):
        """Controls setting outputs on state updates

        Waits fro currentStateHasChanged event to be set then sets outputs
        according to the state.
        """
        def __init__(self, control):
            threading.Thread.__init__(self)
            self._killFlagOut = threading.Event()
            self.control = control
            self.name = "output_control"

        def run(self):
            while not self._killFlagOut.is_set():
                if self.control.currentStateHasChanged.wait(5.0):
                    self.control.currentStateHasChanged.clear()
                    self.control.setOutputsByState()

        def stop(self):
            self._killFlagOut.set()


    class I2Cconsumer(threading.Thread):
        """Gets readings from the ADCs.

        Takes a request for a reading from a queue which holds the chip
        address and channel to read from and sends the data to the master.
        """
        def __init__(self, control, I2Cqueue):
            threading.Thread.__init__(self)
            self.name = "I2C_consumer_thread"
            self._killFlag = threading.Event()
            self.control = control
            self.queue = I2Cqueue
            self.reading = []


        def run(self):
            #switch = {
            #    0 : self.getI2Creading(),
            #    1 : self.updateAndSendADCreading(next)
            #}
            while not self._killFlag.is_set():
                try:
                    nextJob = self.queue.get(True, 2.0)
                    #print nextJob[0], nextJob[1], nextJob[2]
                except Queue.Empty:
                    pass
                else:
                    if nextJob["operations"] == "ini":
                        self.writeByteData(nextJob["address"], nextJob["cmd"], nextJob["data"])

                    elif nextJob["operations"] == "RW":
                        self.writeOps(nextJob)
                        self.reading = self.readOps(nextJob)
                        timeOfReading = time.time()
                        packet = [nextJob["sensor_name"], self.reading, timeOfReading]
                        self.control.rawData.updateEntry(nextJob["sensor_name"], [self.reading, timeOfReading])
                        with globalLock:
                            self.control.sendData(packet)

                    elif nextJob["operations"] == "R":
                        self.reading = self.readOps(nextJob)
                        timeOfReading = time.time()
                        packet = [nextJob["sensor_name"], self.reading, timeOfReading]
                        self.control.rawData.updateEntry(nextJob["sensor_name"], [self.reading, timeOfReading])
                        with globalLock:
                            self.control.sendData(packet)


                    elif nextJob["operations"] == "W":
                        self.writeOps(nextJob)







        def readByteData(self, nextJob):
            bus = smbus.SMBus(1)
            result = bus.read_byte_data(nextJob["address"], nextJob["read"][0])
            return result

        def readByteData2C(self, nextJob):
            data = self.readByteData(nextJob)
            if data >= 0x80:
                data = -((data^0xff)+1)
            return data

        def readWord(self, nextJob):
            bus = smbus.SMBus(1)
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

        def ADCtoVolts12Bit(self, reading):
            upper = (reading[0] & 15)
            upper = (upper << 8)
            total = upper + reading[1]
            voltage = float(total * .001)
            return voltage

        def convertAccel(self, reading, lsb):
            result = reading/lsb
            return result

        def writeByte(self, addr, data):
            bus = smbus.SMBus(1)
            bus.write_byte(addr, data)

        def writeByteData(self, addr, cmd, data):
            bus = smbus.SMBus(1)
            bus.write_byte_data(addr, cmd, data)


        def writeOps(self, nextJob):
            pass

        def readOps(self, nextJob):
            if nextJob["data_length"] == "byte":
                if nextJob["data_type"] == "2c":
                    reading = self.readByte2C(nextJob)
                    reading = getattr(self, nextJob["callback"])(reading)

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

            return reading


        def stop(self):
            self._killFlag.set()





    class I2Cthread(threading.Thread):

        def __init__(self, control, name, configData, sensorList, I2Cqueue):
            threading.Thread.__init__(self)
            self.name = name
            self._killFlag = threading.Event()
            self.queue = I2Cqueue
            self.samplingPeriod = configData["sample_rate"]
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
                                "address" : init["location"],
                                "cmd" : init["reg"],
                                "data" : init["data"],
                                "operation" : "ini"
                            })
            except:
                pass
            while not self._killFlag.is_set():
                for sensor,attr in self.sensorList.items():
                    self.queue.put(
                            {
                                "operations" : attr["operations"],
                                "address" : attr["location"],
                                "write" : attr["write"],
                                "read" : attr["read"],
                                "sensor_name" : sensor,
                                "data_length" : attr["data_length"],
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








    def __init__(self, setInitialState = 0, stateOutputsJSONfile = None, sensorInitializationJSONfile = None, buttonInitializationJSONfile = None, incomingSocket = None, outgoingSocket = None):
        """stateMachineDataPath constructor.

        Args:
            setInitialState: sets the initial stat attribute.
            stateOutputsJSONfile: contains information on outputs for each state.
            sensorInitializationJSONfile: contains information about which ADC channels
            and GPIO pins will be used for sensor readings and inputs.
            incomingSocket: incoming data socket.
            outgoingSocket: outgoind data socket.
        """

        GPIO.setmode(GPIO.BCM)

        self.currentState = setInitialState
        self.currentStateHasChanged = threading.Event()
        self.incomingSocket = incomingSocket
        self.outgoingSocket = outgoingSocket
        self.ADCthreads = []
        self.I2Cthreads = []
        self.I2Cqueue = Queue.Queue()
        self.I2CconsumerThread = self.I2Cconsumer(self, self.I2Cqueue)
        self.rawData = dataController.dataController()

        self.manualMode = 0
        self._killFuncs = threading.Event()

        self.incomingDataThread = self.incomingDataThread(self, self.incomingSocket)
        self.outputsThread = self.outputsThread(self)
        self.lock = threading.Lock()


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
                if func["threaded"] == 1:
                    t = self.functionThread(self, func["name"], func["arguments"])
                    t.start()
                else:
                    self.startFunc(func["name"], func["arguments"])


        except KeyError:
            print "No state in JSON file"



    def initializeInputsAndSensors(self):
        """Initializes inputs and sensors"""
        for names in self.inputNames:
            self.rawData.createNewEntry(names)

        for thread,setup in self.inputsfile.items():
            if setup[0]["bus"] == "i2c":
                t = self.I2Cthread(self, thread, setup[0], setup[1], self.I2Cqueue)
                self.I2Cthreads.append(t)

        for key,val in self.digitalInputs.items():
            GPIO.setup(val["location"], GPIO.IN, pull_up_down=getattr(GPIO, val["PUD"]) )
            GPIO.add_event_detect(val["location"], GPIO.RISING, bouncetime=200)
            cb = lambda channel, arg1 = key, arg2 = 1: self.GPIOevent(arg1, arg2)
            GPIO.add_event_callback(val["location"], cb)


    def initializeOutputs(self):
        """Initializes outputs"""
        for output in self.outputsGPIO:
            GPIO.setup(output, GPIO.OUT)

        for pwm in self.outputsPWM:
            GPIO.setup(pwm[0], GPIO.OUT)
            self.PWMobjects[pwm[0]] = GPIO.PWM(pwm[0],pwm[1])
            #start PWM at 0% duty cycle
            self.PWMobjects[pwm[0]].start(0)
        print self.PWMobjects



    def startThreads(self):
        self.incomingDataThread.start()
        self.outputsThread.start()
        self.I2CconsumerThread.start()
        for thread in self.I2Cthreads:
            thread.start()


    def stopThreads(self):
        print "Killing ADC consumer thread.."
        #for t in self.ADCthreads:
        #    print threading.active_count()
        #    print t.getName()
        #    t.stop()
        #    t.join()
        #    print "done.."
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
        print "done..goodbye"



    def setGPIOlistener(self, pin):
        pass

    def manualCmd(self):
        pass


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



    def accelerationSetPoint(self, input1, input2):
        """Test func"""
        print "Setting Acceleration"

    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def PWMtest(self):
        print "starting PWM test..."
        #while self.currentState == 2:
        self._killFuncs.clear()

        self.PWMobjects[14].ChangeDutyCycle(11)
        while True:
            if self._killFuncs.is_set():
                self.PWMobjects[14].ChangeDutyCycle(0)
                self._killFuncs.clear()
                return
            #obj = getattr(self, self.PWMobjects["14"])
            #obj = self.PWMobjects[14]
           # self.PWMobjects[14].ChangeDutyCycle(dc)
           # for dc in range(0, 101, 5):
            #    if self._killFuncs.is_set():
             #       self.PWMobjects[14].ChangeDutyCycle(0)
              #      self._killFuncs.clear()
               #     return
                #obj = getattr(self, self.PWMobjects["14"])
                #obj = self.PWMobjects[14]
               # self.PWMobjects[14].ChangeDutyCycle(dc)
                #obj.ChangeDutyCycle(dc)
                time.sleep(0.1)



    def startFunc(self, name, args):
        """Starts a function"""
        getattr(self, name)(*args)



    def GPIOevent(self, arg1, arg2):
        """Called when a GPIO event occurs.

        Args:
            arg1: sensor or input name.
            arg2: sensor or input reading.
        """
        self.sendData([arg1,arg2,time.time()])



    def sendData(self, data):
        self.outgoingSocket.send_json(data)



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




if __name__ == "__main__":
    exitFlag = 0
    context = zmq.Context()
    outsock = context.socket(zmq.PUB)
    outsock.bind("tcp://*:5000")

    insock = context.socket(zmq.SUB)
    insock.setsockopt(zmq.SUBSCRIBE, '')
    insock.connect("tcp://%s:6000"%sys.argv[1])

    dataPath = stateMachineDataPath(1, "PI_1_Outputs.json", "PI_1_Sensors_Grpthds.json", "PI_1_Buttons.json", insock, outsock)

    globalLock = threading.Lock()
    dataPath.initializeInputsAndSensors()
    dataPath.initializeOutputs()
    dataPath.startThreads()

    while True:
        try:
            exitFlag = input()
            if exitFlag == 1:
                print "Stopping Threads.."
                dataPath.stopThreads()
                GPIO.cleanup()
                sys.exit()
        except (SyntaxError, NameError):
            pass
