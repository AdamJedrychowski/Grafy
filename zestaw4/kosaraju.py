import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from zestaw1.randomization import randomize_lst_prob
from zestaw4.directed_graph import transpose
import draw
import random


def kosaraju(graph):
    """
    Calculates the graph's strongly connected components
    - graph - directional graph represented as an adjacency list
    - returns: dictionary in format dict[v] = n where v - the vertex index and n - id number of the component
    """
    d = {i: -1 for i in graph}
    stack = []

    for v in graph:
        if d[v] == -1:
            _DFS_visit(v, graph, d, stack)

    graph_t = transpose(graph)
    nr = 0

    comp = {i: -1 for i in graph_t}

    stack.reverse()

    for v in stack:
        if comp[v] == -1:
            nr += 1
            comp[v] = nr
            _components_r(nr, v, graph_t, comp)

    return comp


def _DFS_visit(v, graph, d, stack):
    d[v] = 0
    for u in graph[v]:
        if d[u] == -1:
            _DFS_visit(u, graph, d, stack)

    stack.append(v)


def _components_r(nr, v, graph_t, comp):
    for u in graph_t[v]:
        if comp[u] == -1:
            comp[u] = nr
            _components_r(nr, u, graph_t, comp)


def generate_random_strongly_connected_graph(n, p=0.6):
    """
    Generate random strongly connected graph
    - n - number of vertices
    - returns: graph as an adjacency list and weights as a dictionary (v_s, v_e): w
                where v_s is start and v_e end of the edge, w is weight of edge
    """
    graph = randomize_lst_prob(n, p, directed=True)
    comp = kosaraju(graph)
    while not all(val == 1 for val in comp.values()):
        graph = randomize_lst_prob(n, p, directed=True)
        comp = kosaraju(graph)
    weights = {}
    for i in range(1, n+1):
        for j in graph[i]:
            weight = random.randint(-5, 10)
            edge = (i, j)
            weights[edge] = weight
    return graph, weights


if __name__ == '__main__':
    graph = randomize_lst_prob(6, 0.3, directed=True)
    components = kosaraju(graph)
    print(components, end="\n\n")

    groups = {}
    for v, g in components.items():
        groups.setdefault(g, []).append(v)

    for group in sorted(groups.keys()):
        print(group, groups[group], sep=": ")

    draw.draw_graph(graph, coding=draw.Code.DIRECTED_GRAPH)