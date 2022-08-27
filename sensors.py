import networkx as nx
import random, os, time
import matplotlib.pyplot as plt
from itertools import count
import json
import socket
import sys
#--------------------

def draw(G, dynamic = False):
    plt.clf()
    temperatures = set(nx.get_node_attributes(G,'temperature').values())
    mapping = dict(zip(sorted(temperatures),count()))
    nodes = G.nodes()
    colors = [G.nodes[n]['temperature'] for n in nodes]
    pos = nx.circular_layout(G)
    #pos = nx.kamada_kawai_layout(G)
    ec = nx.draw_networkx_edges(G, pos, alpha=0.2)
    lab = nx.draw_networkx_labels(G, pos)
    nc = nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color=colors, cmap=plt.cm.jet)
    plt.colorbar(nc)
    if (dynamic):
        plt.ion()
        plt.draw()
        plt.show(block=False)
        plt.pause(0.1)
    else:
        plt.show()

def create_graph(nodes_num, edge_prop=None, seed=None):
    if(seed):
        random.seed(seed)
    print("Creating graph with properties: with {} nodes and edge probability of {}" .format(str(nodes_num), str(edge_prop)))
    G = nx.Graph()
    for i in range (0, nodes_num):
        G.add_node(i, temperature = 0)
    for i in range(0, nodes_num):
        if edge_prop:
            for j in range(i+i, nodes_num):
                #create a random network
                prop = random.uniform(0,1)
                if prop >= edge_prop:
                   G.add_edge(i, j, weight=1)
        else:
            for j in range(0,3):
                target = random.randint(i+1,nodes_num)
                G.add_edge(i, target, weight=abs(target - i))
    return G

def update_temps(G):
    for n in G.nodes:
        new_temp = random.randint(18, 50)
        G.nodes[n]["temperature"] = new_temp
    return G

def format_temperatures_str(temperatures):
   new_str = temperatures.replace("{", "")
   new_str = new_str.replace("}", "")
   new_str = new_str.replace("\"", "")
   new_str = new_str.replace(" ", "")
   new_str+='\n'
   return new_str

def run(sleep_interval = 30, host="127.0.0.1", port=9999):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            G = create_graph(10)
            running = True
            while(running):
                G = update_temps(G)
                #draw(G, True)
                current_temperatures = nx.get_node_attributes(G, "temperature")
                str_to_send = format_temperatures_str(json.dumps(current_temperatures))
                b = bytes(str_to_send, 'utf-8')
                print(str_to_send)
                try:
                    conn.sendall(b)
                except Exception:
                    pass
                time.sleep(sleep_interval)
    

run(sleep_interval=20)