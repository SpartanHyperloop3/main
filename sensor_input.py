import csv
import datetime
import random
import time

# Create a new sensors.csv/txt file that will contain a set of randomly generated
# fake sensor readings.

while True:
    # Make some fake sensor data.
    reading_time = datetime.datetime.now()
    temperature = random.uniform(0, 100)
    # Print out the data and write to the CSV file.
    file = open("sensorsi.txt", "a")
    print('Time: {0},Temperature: {1}'.format(reading_time, temperature))
    file.write('{1}, {0}\n'.format(temperature, reading_time))
    time.sleep(1)
#file.close()
