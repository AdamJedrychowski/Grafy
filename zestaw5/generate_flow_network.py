import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def draw_flow_network(graph, partitions):
    """The function draws graph on multipartite layout
    - graph - adjacency matrix with weight of edges
    - partitions - list of number of nodes in each partition excluding start and end partition"""
    G = nx.DiGraph()
    length = len(graph)
    G.add_node(1, layer=0)
    index = 2
    for i,j in enumerate(partitions, start=1):
        G.add_nodes_from(range(index,index+j+1), layer=i)
        index += j
    G.add_node(index, layer=len(partitions)+1)

    G.add_weighted_edges_from([(i+1,j+1,graph[i][j]) for i in range(length) for j in range(length) if graph[i][j] != np.inf])
    labels = {i:i for i in range(1,length+1)}
    pos = nx.multipartite_layout(G, subset_key="layer")
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, verticalalignment='bottom', font_size=12)
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=2)
    nx.draw_networkx_labels(G, pos, labels)
    plt.show()

def generate_flow_network(N):
    """The function generates flow network
    - N - number of partitions
    - return: adjacency matrix with weight of edges and list of number of nodes in each partition excluding start and end partition"""
    if N < 2:
        print('Za mała liczba warstw pośrednich')
        return
    
    layers = [random.randint(2,N) for _ in range(N)]
    graph = np.zeros((sum(layers)+2, sum(layers)+2))

    for i in range(layers[0]):
        graph[0][1+i] = 1
    
    index = 1
    for i in range(0,len(layers)-1):
        for j in range(layers[i]):
            graph[index+j][index + layers[i] + random.randrange(0,layers[i+1])] = 1
        for j in range(index+layers[i], index+layers[i]+layers[i+1]):
            if not np.any(graph[:,j]):
                graph[index+random.randrange(0,layers[i])][j] = 1
        index += layers[i]
    
    for i in range(layers[-1]):
        graph[-2-i][-1] = 1
    
    selected = 0
    while selected < 2*N:
        i = random.randrange(len(graph))
        j = random.randrange(len(graph))
        if (not graph[i][j]) & (not graph[j][i]) & (i != j) & (j != 0) & (i != len(graph)-1):
            graph[i][j] = 1
            selected += 1

    graph = np.array([[random.randint(1,10) if graph[i][j] else np.inf for j in range(len(graph))] for i in range(len(graph))])
    draw_flow_network(graph, layers)
    return graph, layers


if __name__ == '__main__':
    generate_flow_network(int(input('Podaj liczbe warstw: ')))