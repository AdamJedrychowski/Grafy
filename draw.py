import networkx as nx
import matplotlib.pyplot as plt
from enum import Enum

class Code(Enum):
    ADJACENCY_MATRIX = 1
    MATRIX_INCIDENT = 2
    NEIGHBORHOOD_LIST = 3
    GRAPHICAL_SEQUENCE = 4


def draw_graph(graph, coding=Code.NEIGHBORHOOD_LIST):
    """The function draws graph on circle layout
    - graph - representation of graph
    - coding - which representation is passed, values from Code"""
    if coding == Code.ADJACENCY_MATRIX:
        # TODO function to cast adjacency matrix to neighborhood list
        pass
    elif coding == Code.MATRIX_INCIDENT:
        # TODO function to cast matrix incident to neighborhood list
        pass
    
    G = nx.Graph()
    G.add_nodes_from(graph.keys())
    G.add_edges_from([(i,j) for i in graph.keys() for j in graph[i]])
    pos = nx.circular_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=2)
    labels = {i:j for i,j in enumerate(graph.keys(), start=1)}
    nx.draw_networkx_labels(G, pos, labels)
    plt.show()