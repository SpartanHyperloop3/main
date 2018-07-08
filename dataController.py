import commitLog
import datetime
import time
class dataController(object):
    """Creates a database of commitLogs.

    Attributes:
        dataCollectionByType creates a dictionary of commitLogs which allows for
        a tagname to be associated with each log. A new entry should be added to
        the dictionary using the createNewEntry method. updateEntry should be used
        to more concisely add to the dictionary and getCurrentReadingFor returns the
        most recently added value.
    """
    def __init__(self):
        self.dataCollectionByType = {}

    def createNewEntry(self, entryType):
        if entryType not in self.dataCollectionByType:
            self.dataCollectionByType[entryType] = commitLog.commitLog(100)

    def updateEntry(self, entryName, data):
        self.dataCollectionByType[entryName].append(data)

    def getCurrentReadingFor(self, dataType):
        try:
            return self.dataCollectionByType[dataType].retrieveMostCurrentEntry()[0]
        except TypeError:
            pass

    def getCurrentTimeFor(self, dataType):
        try:
            return self.dataCollectionByType[dataType].retrieveMostCurrentEntry()[1]
        except TypeError:
            pass

    def getCurrentTimeForAsc(self, dataType):
        try:
            return time.ctime(self.dataCollectionByType[dataType].retrieveMostCurrentEntry()[1])
        except TypeError:
            pass
