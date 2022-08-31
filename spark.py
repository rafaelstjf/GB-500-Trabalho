
from audioop import maxpp
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import networkx as nx
from pymongo import MongoClient


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 9999  # The port used by the server
DELTA = 2
def sendToMongo(timestamp, graph):
    client = MongoClient("localhost", 27017)
    db = client["sensors"]
    sensors = db["Sensors"]
    sensor = dict()
    sensor["timestamp"] = str(timestamp)
    for g in graph:
        sensor[g[0]] = g[1]
    sensors.insert_one(sensor)

def printRdd(timestamp, rdd):
    print(f"Imprimindo rdds {timestamp}")
    dataColl=rdd.collect()
    if len(dataColl) > 0:
        max_temp = max(dataColl, key = lambda t: t[1])
        if float(max_temp[1]) >= 46:
            print(f"Risk of fire! Maximum temperature of {max_temp[1]} celsius degrees.") 
            G = nx.Graph()
            deltas = rdd.filter(lambda x: abs(float(x[1]) - float(max_temp[1])) < DELTA).collect()
            for d in deltas:
                G.add_node(d[0], temperature=float(d[1]))
            for i in range(0, len(deltas)):
                for j in range(i+1, len(deltas)):
                    d1 = deltas[i]
                    d2 = deltas[j]
                    G.add_edge(d1[0], d2[0], weight=(abs(float(d1[1]) - float(d2[1]))))
            T=nx.minimum_spanning_tree(G)
            degrees = sorted(G.degree(), key=lambda pair: pair[1])
            if len(degrees)> 1:
                T.add_edge(degrees[0][0], degrees[1][0], weight=0)
            print("Saving temperatures tree")
            nx.write_graphml(T, "forest.graphml")
    sendToMongo(timestamp, dataColl)

    
    

sc = SparkContext("local[2]", "Sensors")
ssc = StreamingContext(sc, 30)
text_stream = ssc.socketTextStream(HOST, PORT)
temperatures = text_stream.flatMap(lambda text_stream: text_stream.split(","))
#temperatures.pprint()
pairs = temperatures.map(lambda temperature: (temperature.split(":")[0], temperature.split(":")[1]))
#pairs.pprint()
pairs.foreachRDD(printRdd)
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