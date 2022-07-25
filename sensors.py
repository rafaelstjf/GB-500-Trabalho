import networkx as nx
import random, os, time
import matplotlib.pyplot as plt
from itertools import count
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

def run(sleep_interval = 30):
    G = create_graph(10)
    running = True
    while(running):
        G = update_temps(G)
        draw(G, True)
        #time.sleep(sleep_interval)

run()