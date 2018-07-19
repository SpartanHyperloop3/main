#local libraries
import graph
import receive_and_parse
import time

receive_and_parse.setup('127.0.0.1', '6000')
graph.setup('plot_details.json', 'stateInputLogic_test.json', receive_and_parse.graph_data)

while(True):
    receive_start = time.time()
    receive_and_parse.receive_and_parse()
    receive_end = time.time()
    print('receive duration: %.5f' % (receive_end - receive_start))
    graph_start = time.time()
    graph.graph()
    graph_end = time.time()
    print('graph duration: %.5f' % (graph_end - graph_start))