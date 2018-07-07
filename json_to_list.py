import json

sensor1 = {'A': 7, 'B': 8, 'C': 5}
sensor2 = {'A': 71, 'B': 28, 'C': 4}
sensor3 = {'A': 7, 'B': 83, 'C': 55}
sensor4 = {'A': 74, 'B': 86, 'C': 59}
json_data = {'sensor1': sensor1, 'sensor2': sensor2, 'sensor3': sensor3, 'sensor4': sensor4}
json_data = json.dumps(json_data)
python_data = json.loads(json_data)

print(json_data)
print(python_data)

sensor_names = []
sensor_readings = {}
MAX_LIST_LENGTH = 10

def parse(python_data):
   for sensor in python_data:
       if sensor not in sensor_names:
           sensor_names.append(sensor)
       try:
           if len(sensor_readings[sensor][0]) >= MAX_LIST_LENGTH:
               sensor_readings[sensor][0].pop(0)
               sensor_readings[sensor][1].pop(0)
           sensor_readings[sensor][0].append(python_data[sensor]['A'])
           sensor_readings[sensor][1].append(python_data[sensor]['B'])
       except KeyError:
           sensor_readings[sensor] = [[],[]]
           sensor_readings[sensor][0].append(python_data[sensor]['A'])
           sensor_readings[sensor][1].append(python_data[sensor]['B'])

for i in range(0,10):
   parse(python_data)

s1 = sensor_readings['sensor1']
s2 = sensor_readings['sensor2']
s3 = sensor_readings['sensor3']
s4 = sensor_readings['sensor4']
print(s1, s2, s3, s4)
print(len(s1[0]), len(s2[1]), len(s3), len(s4))



print(sensor_names)
print(sensor_readings)

print(s1[0])
if len(s1[0]) > 5:
    s1[0].pop(0)
print(s1[0])
#print(sensor_readings['name1'])
print(s1[1])
if s1[1][-1] - s1[1][0] == 0:
    s1[1].pop(0)
    s1[0].pop(0)
print(s1[1])
print(s1[0])

print(s2[0])
if len(s2[0]) > 5:
    s2[0].pop(0)
print(s2[0])
#print(sensor_readings['name1'])
print(s2[1])
if s2[1][-1] - s2[1][0] == 0:
    s2[1].pop(0)
    s2[0].pop(0)
print(s2[1])
print(s2[0])

print(s3[0])
if len(s3[0]) > 5:
    s3[0].pop(0)
print(s3[0])
#print(sensor_readings['name1'])
print(s3[1])
if s3[1][-1] - s3[1][0] == 0:
    s3[1].pop(0)
    s3[0].pop(0)
print(s3[1])
print(s3[0])

print(s4[0])
if len(s4[0]) > 5:
    s4[0].pop(0)
print(s4[0])
#print(sensor_readings['name1'])
print(s4[1])
if s4[1][-1] - s4[1][0] == 0:
    s4[1].pop(0)
    s4[0].pop(0)
print(s4[1])
print(s4[0])