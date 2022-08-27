
from audioop import maxpp
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import networkx as nx


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 9999  # The port used by the server
DELTA = 2
def print_rdd(timestamp, rdd):
    print(f"Imprimindo rdds {timestamp}")
    dataColl=rdd.collect()
    if len(dataColl) > 0:
        max_temp = max(dataColl, key = lambda t: t[1])
        if float(max_temp[1]) >= 46:
            print(f"Risk of fire! Maximum temperature of {max_temp[1]} celsius degrees.") 
            G = nx.Graph()
            deltas = rdd.filter(lambda x: abs(float(x[1]) - float(max_temp[1])) < 5).collect()
            for d in deltas:
                G.add_node(d[0], temperature=float(d[1]))
            for d in deltas:
                G.add_edge(d[0], max_temp[0], weight=(abs(float(d[1]) - float(max_temp[1]))))
            nx.write_graphml(G, "forest.graphml")
        

    
    

sc = SparkContext("local[2]", "Sensors")
ssc = StreamingContext(sc, 30)
text_stream = ssc.socketTextStream(HOST, PORT)
temperatures = text_stream.flatMap(lambda text_stream: text_stream.split(","))
#temperatures.pprint()
pairs = temperatures.map(lambda temperature: (temperature.split(":")[0], temperature.split(":")[1]))
#pairs.pprint()
pairs.foreachRDD(print_rdd)
ssc.start()
ssc.awaitTermination()

'''
import socket, json

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        data = s.recv(1024).decode()
        print((lambda data: data.split(",")))
        
'''