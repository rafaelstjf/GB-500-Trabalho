
from pyspark import SparkContext
from pyspark.streaming import StreamingContext


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 9999  # The port used by the server

def print_rdd(timestamp, rdd):
    print(f"Imprimindo rdds {timestamp}")
    dataColl=rdd.collect()
    for row in dataColl:
        print(row[0] + "," +str(row[1]))

sc = SparkContext("local[2]", "Sensors")
ssc = StreamingContext(sc, 7)
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