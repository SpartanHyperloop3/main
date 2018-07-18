#local libraries
import receive_and_parse

'''
test = {
    'voltage1' : [[2],[2.0]]
}
graph.setup(test)

graph.graph()
test['voltage1'] = [[10],[2.1]]
time.sleep(3)
graph.graph()
while(True):
    time.sleep(5)
'''

receive_and_parse.setup('127.0.0.1', '6000')
print(receive_and_parse.graph_time_limit)
while(True):
    raw_input('wait...')
    receive_and_parse.receive_and_parse()