import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from zestaw1.randomization import randomize_lst_prob
from zestaw1.conversions import lst2adjacency, lst2incidence
import draw


def transpose(graph):
    """
    Creates a transpose version of the directed graph
    - graph - directed graph represented as an adjacency list
    - returns: the transpose of the provided graph
    """
    graph_t = {v: [] for v in graph}

    for v in graph:
        for u in graph[v]:
            graph_t[u].append(v)

    return graph_t


if __name__ == '__main__':
    graph = randomize_lst_prob(6, 0.3, directed=True)
    print(graph, end='\n\n')
    draw.draw_graph(graph, coding=draw.Code.DIRECTED_GRAPH)

    print(lst2adjacency(graph), end='\n\n')
    print(lst2incidence(graph, directed=True), end='\n\n')