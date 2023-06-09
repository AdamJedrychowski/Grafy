import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from zestaw1 import randomization, conversions
import draw

def components_lst(graph):
    """
    Find components of a graph
    - graph - the graph to find components of, represented as an adjacency list
    - returns: a dictionary in format comp[v] = n, where v is the vertex index and n is its component's number
    """
    nr = 0
    comp = {i: -1 for i in graph.keys()}

    for vert in graph.keys():
        if comp[vert] == -1:
            nr += 1
            comp[vert] = nr
            _components_lst_R(nr, vert, graph, comp)

    return comp


def _components_lst_R(nr, v, graph, comp):
    for u in graph[v]:
        if comp[u] == -1:
            comp[u] = nr
            _components_lst_R(nr, u, graph, comp)


def components_adj(graph):
    """
    Find components of a graph
    - graph - the graph to find components of, represented as an adjacency matrix
    - returns: a dictionary in format comp[v] = n, where v is the vertex index and n is its component's number
    """
    return components_lst(conversions.adj2list(graph))


def components_inc(graph):
    """
    Find components of a graph
    - graph - the graph to find components of, represented as an incidence matrix
    - returns: a dictionary in format comp[v] = n, where v is the vertex index and n is its component's number
    """
    return components_lst(conversions.inc2list(graph))


def component_count_lst(graph):
    """
    Count components of a graph
    - graph - the graph to find components of, represented as an incidence matrix
    - returns: the number of the graph's components
    """
    components = components_lst(graph)
    return max(components.values())


if __name__ == '__main__':
    graph = randomization.randomize_lst(5, 3)
    draw.draw_graph(graph)
    components = components_lst(graph)

    vertices_by_component = {i: [v for v, j in components.items() if j == i] for i in components.values()}
    for component in vertices_by_component.items():
        print(component[0], component[1])

    component_counts = {i: 0 for i in components.values()}
    for component in components:
        component_counts[components[component]] += 1

    print("Największa składowa ma numer", max(component_counts.items(), key=lambda x: x[1])[0])
