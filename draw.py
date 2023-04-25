import networkx as nx
import matplotlib.pyplot as plt
from enum import Enum
from zestaw1.conversions import inc2list, adj2list
import numpy as np
import atexit

class Code(Enum):
    ADJACENCY_MATRIX = 1
    MATRIX_INCIDENT = 2
    NEIGHBORHOOD_LIST = 3
    GRAPHICAL_SEQUENCE = 4
    WEIGHTED_GRAPH = 5
    DIRECTED_GRAPH = 6


def draw_graph(graph, coding=Code.NEIGHBORHOOD_LIST):
    """The function draws graph on circle layout
    - graph - representation of graph
    - coding - which representation is passed, values from Code"""
    plt.figure()
    if coding == Code.ADJACENCY_MATRIX:
        graph = adj2list(graph)
    elif coding == Code.MATRIX_INCIDENT:
        graph = inc2list(graph)

    if coding == Code.DIRECTED_GRAPH:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    if coding == Code.WEIGHTED_GRAPH:
        length = len(graph)
        G.add_nodes_from(range(1,length+1))
        G.add_weighted_edges_from([(i+1,j+1,graph[i][j]) for i in range(length) for j in range(length) if graph[i][j] != np.inf])
        labels = {i:i for i in range(1,length+1)}
        pos = nx.circular_layout(G)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, verticalalignment='bottom', font_size=12)
    else:
        G.add_nodes_from(graph.keys())
        G.add_edges_from([(i,j) for i in graph.keys() for j in graph[i]])
        labels = {i:j for i,j in enumerate(graph.keys(), start=1)}
        pos = nx.circular_layout(G)

    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=2)
    nx.draw_networkx_labels(G, pos, labels)
    plt.show(block=False)


def cleanup():
    if plt.get_fignums():
        plt.pause(120)
        plt.close()

atexit.register(cleanup)