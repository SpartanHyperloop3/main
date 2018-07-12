import zmq
import time
import threading
import sys
import commitLog
import dataController
import json
import Queue
import logging
import copy
import datetime
import pdb

logging.basicConfig(level=logging.DEBUG,
                   format='(%(threadName)-10s) %(message)s',)


class stateMachineControl(object):
    """State machine control thread.

    This class contains all of the methods and sub-classes necessary to
    handle incoming data. The controller takes the raw data and applies
    corresponding logic to produce boolean values that are used to determine
    the next the state to transistion to. Once the state has changed the controller
    broadcasts the change to all connected datapath devices.
    """
    class incomingDataThread(threading.Thread):
        """Retrieves incoming data from all subscribed devices.

        Continuously runs in the background collecting data from slaves.
        Data is assumed to be in a list form with two entries, a string
        in the first entry that signifies the sensor or input from which
        the reading came, and a numerical value as the second entry. The
        second entry can be floating point. The thread puts the sensor name
        in a storage object of type dataController and also updates a work
        queue with name of the sensor which was updated. The work queue is later
        consumed by another thread to check if the new reading which was entered
        will have changed the corresponding logic associated with the sensor value
        or input value.
        """
        def __init__(self, control, zmqSock):
            """incomingDataThread constructor.

            Args:
                control: must pass outer class object to obtain access to methods.
                zmqSock: current socket for incoming data
            """
            threading.Thread.__init__(self)
            self._killFlag = threading.Event()
            self.control = control
            self.sock = zmqSock
            self.poller = zmq.Poller()
            self.poller.register(self.sock, zmq.POLLIN)



        def run(self):
            while not self._killFlag.is_set():
                if self.poller.poll(1000):
                    message = self.sock.recv_json()
                    #self.control.sendDataToControlStation(self.sock)
                    try:
                        self.control.rawData.updateEntry(message[0], [message[1], message[2]])
                        if message[3] == "logic":
                            self.control.inputLogicQueue.put(message[0])
                        elif message[3] == "broadcast":
                            pass
                        #if message[0] == "state_13_start_time":
                        #    print message[0],message[1],message[2]
                        #    print self.control.rawData.getCurrentTimeFor(message[0])
                        #elif message[0] == "PI_1_U1_CH1":
                        #    print message[0], message[1]
                    except:
                        pass


        def stop(self):
            self._killFlag.set()



    class consumerThread(threading.Thread):
        """reads sensor names from the work queue and updates logic if necessary.

        Runs in the background retrieving the names of sensors currently updated
        by the incomingDataThread. Only the name is needed to retrieve the most
        current entry by using methods of the dataController class. The sensor
        reading is ran through logic that has been predetermined in a corresponding
        JSON initialization file. If the current logic entry associated with the
        sensor reading has updated an event is set to notify the next thread to
        evaluate if the new logic signifies a state change.
        """
        def __init__(self, control):
            """consumerThread constructor.

            Args:
                control: must pass outer class object to obtain access to methods.
            """
            threading.Thread.__init__(self)
            self._killFlag = threading.Event()
            self.control = control
        def run(self):
            while not self._killFlag.is_set():
                try:
                    slaveState = self.control.updateSlaveStateQueue.get(False)
                except Queue.Empty:
                    pass
                try:
                    dataName = self.control.inputLogicQueue.get(True, 1.0)
                    inputStateNameList = self.control.inputLogicNameByDataName[dataName]

                    for inputStateName in inputStateNameList:
                        if self.control.setStateInputLogic(inputStateName, dataName):
                            self.control.inputLogicHasBeenUpdated.set()
                    self.control.inputLogicQueue.task_done()

                except:
                    pass

        def stop(self):
            self._killFlag.set()



    class slaveStateConsumerThread(threading.Thread):

        def __init__(self, control):
            """consumerThread constructor.

            Args:
                control: must pass outer class object to obtain access to methods.
            """
            threading.Thread.__init__(self)
            self._killFlag = threading.Event()
            self.control = control
        def run(self):
            while not self._killFlag.is_set():
                try:
                    slaveState = self.control.updateSlaveStateQueue.get(True, 1.0)
                except Queue.Empty:
                    pass
                else:
                    self.updateSlaveState(slaveState)
                    self.checkAllSlaveStates()


        def updateSlaveState(self, SlaveState):
            pass

        def checkAllSlaveStates(self):
            pass

        def stop(self):
            self._killFlag.set()



    class updateStateThread(threading.Thread):
        """Reevaluates current state based on logic.

        Waits for the inputLogicHasBeenUpdated event to be set by consumerThread
        which signifies a change in a logic variable. Once the event is set the
        fucntion setNextState of the outer controller class is called to reevaluate
        the state logic. If the state has changed the function setNextState returns
        true and an stateHasChanged is set to notify broadcastStateThread of the change.
        """
        def __init__(self, control):
            """updateStateThread constructor.

            Args:
                control: must pass outer class object to obtain access to methods.
            """
            threading.Thread.__init__(self)
            self._killFlag = threading.Event()
            self.control = control

        def run(self):
            while not self._killFlag.is_set():
                if self.control.inputLogicHasBeenUpdated.wait(5.0):
                    self.control.inputLogicHasBeenUpdated.clear()
                    if self.control.setNextState():
                        #self.control.stateHasChanged.set()
                        self.control.broadcastStateQueue.put(["state", self.control.currentState])

        def stop(self):
            self._killFlag.set()





    class broadcastStateThread(threading.Thread):
        """Broadcasts state changes to clients.

        If the thread is notified of a state change the new state is sent out
        to all clients.
        """
        def __init__(self, control, zmqSock, broadcastStateQueue):
            """broadcastStateThread constructor.

            Args:
                control: must pass outer class object to obtain access to methods.
                zmqSock: current socket for incoming data
            """
            threading.Thread.__init__(self)
            self._killFlag = threading.Event()
            self.control = control
            self.sock = zmqSock
            self.poller = zmq.Poller()
            self.poller.register(self.sock, zmq.POLLOUT)
            self.queue = broadcastStateQueue

        def run(self):
            while not self._killFlag.is_set():
                try:
                    dataToSend = self.queue.get(True, 1.0)
                except Queue.Empty:
                    pass
                else:
                #if self.control.stateHasChanged.wait(5.0):
                #    self.control.stateHasChanged.clear()
                    print "state has changed - sending to slaves - Current State: %s" %self.control.currentState
                    if self.poller.poll(1000):
                        #self.sock.send_json(["state", self.control.currentState])
                        print "sent",dataToSend
                        self.sock.send_json(dataToSend)
                    self.queue.task_done()

        def stop(self):
            self._killFlag.set()





    def __init__(self, setInitialState = 0, stateDataJSONfile = None, inputLogicJSONfile = None, incomingSocket = None, outgoingSocket = None):
        """stateMachineControl constructor.

        Initializes the stateMachineControl object.

        Args:
            setInitialState: set the initial state.

            stateDataJSONfile: JSON file that contains the input logic and current
            state combinations and the state change they signify.

            inputLogicJSONfile: JSON file the contains relates expected raw data from
            clients with the type of logic that should be performed on the data, and the
            name of the logic value that it will be stored in.

            incomingSocket: The socket used for incoming data.

            outgoingSocket: The socket used for outgoing data.
        """

        self.currentState = setInitialState

        #events for notifying threads of data changes
        self.inputLogicHasBeenUpdated = threading.Event()
        self.stateHasChanged = threading.Event()

        #storage for raw data
        self.rawData = dataController.dataController()

        #work queue
        self.inputLogicQueue = Queue.Queue()

        self.broadcastStateQueue = Queue.Queue()

        self.updateSlaveStateQueue = Queue.Queue()

        connections = {
                "PI_1" : {
                    "ip" : "192.168.10.2",
                    "curent_state" : None
                },
                "PI_2" : {
                    "ip" : "192.168.10.3",
                    "current_state" : None
                },
                "PI_3" : {
                    "ip" : "192.168.10.4",
                    "curent_state" : None
                },
                "PI_4" : {
                    "ip" : "192.168.10.5",
                    "current_state" : None
                }
        }
        #initialize threads
        self.consumerThread = self.consumerThread(self)
        self.incomingDataThread = self.incomingDataThread(self, incomingSocket)
        self.broadcastStateThread = self.broadcastStateThread(self, outgoingSocket, self.broadcastStateQueue)
        self.stateUpdateThread = self.updateStateThread(self)

        #sockets
        self.incomingSocket = incomingSocket
        self.outgoingSocket = outgoingSocket


        #JSON file parsing begins here, data is extracted for ease of use
        try:
            f = open(stateDataJSONfile, "r")

            stateJSON = json.loads(f.read())
            
            self.stateList = []
            for state in stateJSON.keys():
                self.stateList.append(state)
            #validTransitions holds the valid state changes per current state
            self.validTransitions = {}
            arr = []
            for key,val in stateJSON.items():
                for i in val:
                    arr.append(i[0])
                #key is the current state arr holds a list of the valid states
                self.validTransitions[key] = copy.deepcopy(arr)
                del arr[:]

            #statTransitionLogic creates a hash table where the current logic
            #for the current active state can be iterated per valid transistion
            #by creating a key for each list of logic in the for of 
            #[currentstate+validTransistionState]. To explain further, the
            #currentstate is the active state and the validTransitionState
            #is a possible state that can be transitioned to from the current
            #active state. Accessing the key yields a list of known input logic
            #variables and their state, or boolean value (0 or 1), which must equal
            #the values of the current boolean values found in the 
            #hash table, inputLogicState, (which is intiliazed in the next section,
            #and constantly updated by the consumerThread), for the transition to take place.
            self.stateTransitionLogic = {}
            arr = []
            for key,val in stateJSON.items():
                for i in val:
                    self.stateTransitionLogic["%s+%s"%(key,i[0])] = i[1]

            f.close()
        except IOError:
            print "Could not open JSON file"


        try:
            f = open(inputLogicJSONfile, "r")

            cont = json.loads(f.read())

            #inputLogicState holds the current input logic state used for next state logic
            self.inputLogicState = {}
            for key,val in cont.items():
                self.inputLogicState[key] = val[0]

            #rawDataUnits returns units of data for each sensor input.
            self.rawDataUnits = {}
            for key,val in cont.items():
                for sensor, properties in val[1]["raw_data_names"].items():
                    self.rawDataUnits[sensor] = properties["raw_data_units"]
                if not val[1]["raw_data_names"]:
                    self.rawDataUnits[key] = "none"
            #inputLogicParams holds the parameters for the logic type. For example,
            #a list of 2 numbers is used for the upper and lower bounds of a range
            #logic type
            self.inputLogicParams = {}
            for key,val in cont.items():
                for sensor, properties in val[1]["raw_data_names"].items():
                    self.inputLogicParams[key] = properties["params"]
            #print self.inputLogicParams
            #inputLogicNameByDataName allows for the input logic variables associated
            #with a rawData value to be found by the rawData name. Because a rawData
            #value may belong to more than one input logic variable (variables found
            #and updated in the inputLogicState hash table) this returns a list.
            #When more than one input logic variable is found it can be iterated, and
            #is done so in the consumerThread to allow for updating each input variable
            #that is associated with the current rawData name taken from the work queue.
            self.inputLogicNameByDataName = {}
            for key,val in cont.items():
                if not val[1]["raw_data_names"]:
                    self.inputLogicNameByDataName[key] = [key]
                for sensor, properties in val[1]["raw_data_names"].items():
                    self.inputLogicNameByDataName.setdefault(sensor, []).append(key)
            #dataValuesPerInputState returns the list of rawData names associated with
            #an input state variable when entered as a key.
            self.dataValuesPerInputState = {}
            sensors = []
            for key,val in cont.items():
                for name,sen in val[1]["raw_data_names"].items():
                    sensors.append(name)
                self.dataValuesPerInputState[key] = copy.deepcopy(sensors)
                del sensors[:]
                if not val[1]["raw_data_names"]:
                    self.dataValuesPerInputState[key] = [key]

            self.sensorInfo = {}
            for key,val in cont.items():
                self.sensorInfo[key] = val[1]["raw_data_names"]
            f.close()
            
            #print self.dataValuesPerInputState
            #print self.inputLogicNameByDataName

        except IOError:
            print "Could not open JSON file"

    def varCheck(self):
        arr = []
        for obj in self.stateTransitionLogic.values():
            for obj2 in obj:
                for key in obj2.keys():
                    if key not in self.inputLogicState.keys():
                        arr.append(key)
        if arr:
            print "Missing Vars:"
            for m in arr:
                print m

    def initialRawDataBase(self):
        for inputLogic in self.dataValuesPerInputState.values():
            for sensor in inputLogic:
                self.rawData.createNewEntry(sensor)

        for state in self.stateList:
            self.rawData.createNewEntry("state_%s_start_time"%state)
            self.rawData.createNewEntry("state_%s_curr_time"%state)
        #print self.rawData.dataCollectionByType

    def startThreads(self):
        """Starts all threads, called in main"""
        self.consumerThread.start()
        self.incomingDataThread.start()
        self.stateUpdateThread.start()
        self.broadcastStateThread.start()

    def updateState(self, state):
        self.currentState = state
        self.broadcastStateQueue.put(["state", state])

    def stopThreads(self):
        """stops all threads"""
        print "killing incoming data thread.."
        self.incomingDataThread.stop()
        self.incomingDataThread.join()
        print "done"

        print "killing consumer thread.."
        self.consumerThread.stop()
        self.consumerThread.join()
        print "done"

        print "killing state update thread.."
        self.stateUpdateThread.stop()
        self.stateUpdateThread.join()
        print "done"

        print "killing broadcast thread.."
        self.broadcastStateThread.stop()
        self.broadcastStateThread.join()
        print "done..Goodbye"



    def setNextState(self):
        """Sets the next state if the transition logic is detected.

        This function begins by testing logic for the "all" key, which is 
        done prior to detecting a state transition based on current state.
        Transitions listed in the "all" section are preliminary for all states
        and so will be the more critical logic that detects a system failure,
        or logic that allows for transition to a custom state such as a manual
        override mode. Once the "all" conditions have been considered, the 
        function moves on to the state transition logic by current state,
        and is evaluated if possible.

        Returns:
            True is the state has changed
        """
        try:
            #returns list of valid state transition numbers
            ifAllCondition = self.validTransitions["all"]

            for goto in ifAllCondition:
                try:
                    currLogic = self.stateTransitionLogic["all+%s"%(goto)]
                except KeyError as e:
                    print "Invalid Transistion Request"
                    return False

                #if not currLogic:
                #print currLogic
                for possibilities in currLogic:
                    result = 1
                    #evaluate AND logic
                    for key,val in possibilities.items():
                        if (self.inputLogicState[key] != val):
                            result = 0
                    #if the result is true, stop evaluating OR logic
                    if result == 1:
                        break
                #if the all state transition is to take place and the current
                #state doesn't already equal that state return true to signal a
                #state change
                if result == 1 and self.currentState != goto:
                    self.currentState = goto
                    return True
                #if the logic values are still valid for signaling an all state 
                #transition but the state is activated, return false. This ensures
                #that all states take precedence over normal state transitions. Eg.
                #so that if an emergency state has been activated any further calls
                #to this function will not proceed to evaluate any further state 
                #transitions
                elif result == 1 and self.currentState == goto:
                    return False

        except KeyError:
            #consider logging here
            pass


        try:
            currConditions = self.validTransitions["%s"%self.currentState]
            for goto in currConditions:
                try:
                    currLogic = self.stateTransitionLogic["%s+%s"%(self.currentState,goto)]
                except KeyError as e:
                    print "Invalid Transistion Request"
                    return

                for possibilities in currLogic:
                    result = 1
                    for key,val in possibilities.items():
                        if (self.inputLogicState[key] != val):
                            result = 0

                    #if the result is true no need to continue evaluating OR logic
                    if result == 1:
                        break

                if result == 1 and self.currentState != goto:
                    self.currentState = goto
                    return True
        except KeyError:
            #consider logging here
            pass

        return False



    def setStateInputLogic(self, inputLogicName, dataName):
        """Takes the rawData and logic type and updates the input logic.

        Returns:
            True if the logic has changed.
        TODO:
            add support for logic other than range
        """
        #print self.sensorInfo
        #print inputLogicName
        for sensor in self.dataValuesPerInputState[inputLogicName]:
            #print sensor
            #print self.sensorInfo[inputLogicName][sensor]["type_of_logic"]
            if self.sensorInfo[inputLogicName][sensor]["type_of_logic"] == "range":
                self.inputLogicState[inputLogicName] = self.outOfRange(sensor, self.sensorInfo[inputLogicName][sensor]["params"])
            elif self.sensorInfo[inputLogicName][sensor]["type_of_logic"] == "boolean":
                try:
                    self.inputLogicState[inputLogicName] = self.rawData.getCurrentReadingFor(sensor)
                except:
                    print sys.exc_info()[0]
                #print self.inputLogicState[inputLogicName],self.rawData.getCurrentReadingFor(sensor)
            elif self.sensorInfo[inputLogicName][sensor]["type_of_logic"] == "time_diff":
                self.inputLogicState[inputLogicName] = self.timeDifference(sensor, self.sensorInfo[inputLogicName][sensor]["params"])

            return True




    def checkIfStateShouldChange(self, inputLogicName):
        """checks if atleast one of the current rawData entries is true

        Only returns 0 is all rawData entries per input logic are 0
        """
        result = 0
        for currentValue in self.dataValuesPerInputState[inputLogicName]:
            result = result | self.outOfRange(currentValue, self.inputLogicParams[inputLogicName])
        #if currentValue == "PI_1_U1_CH1":
            #print result
        return result

    def timeDifference(self, sensorName, params):
        startTime = self.rawData.getCurrentTimeFor(params[0])
        currTime = self.rawData.getCurrentTimeFor(sensorName)
 
        try:
            diff = currTime - startTime
      
        except:
            return 0
       
        if currTime == None:
            return 0
        if diff > params[1]:
            return 1
        else:
            return 0



    def outOfRange(self, sensorName, rangeParams):
        """Detects if reading is out of range"""
        data = self.rawData.getCurrentReadingFor(sensorName)
        if data == None:
            return 0
        if data > rangeParams[1] or data < rangeParams[0]:
            return 1
        else:
            return 0



    def sendDataToControlStation(self, sock):
        dataToSend = {}
        for key,val in self.rawData.dataCollectionByType.items():
            dataToSend[key] = {
                "reading" : self.rawData.getCurrentReadingFor(key),
                "time" : self.rawData.getCurrentTimeForAsc(key),
                "units" : self.rawDataUnits[key]
            }

        f = open("JSONdata.json","w+")
        f.write(json.dumps(dataToSend))
        f.close






if __name__ == "__main__":
    sensorData = zmq.Context()

    sensorDataSocket = sensorData.socket(zmq.SUB)

    sensorDataSocket.connect("tcp://192.168.10.2:5000")
    sensorDataSocket.setsockopt(zmq.SUBSCRIBE, '')

    outSock = sensorData.socket(zmq.PUB)
    outSock.bind("tcp://192.168.10.1:6000")



    master = stateMachineControl(1, "nextStateInfo.json", "stateInputLogic.json", sensorDataSocket, outSock)


    master.initialRawDataBase()
    master.startThreads()
    master.varCheck()
    menuOpt = 0
    while True:
        try:
            print "Enter a state number (-1 to exit):"
            menuOpt = raw_input()
            try:
                num = int(menuOpt)
            except ValueError:
                pass
            else:
                if num == -1:
                    master.stopThreads()
                    sys.exit()
                else:
                    if num >= 0:
                        master.updateState(num)
                    else:
                        print "invalid state number"
        except (SyntaxError, NameError):
            pass
