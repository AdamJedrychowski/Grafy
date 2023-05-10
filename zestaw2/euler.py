import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import random
from draw import draw_graph
from zestaw2.components import component_count_lst
from zestaw1.randomization import randomize_lst


def _get_degrees_lst(graph):
    """
    Count the components of a graph
    - graph - the graph to count the components of, represented as an adjacency list
    - returns: amount of components in the graph
    """
    degrees = {}
    for v, dests in graph.items():
        degrees[v] = len(dests)

    return degrees


def generate_euler_graph_lst(n):
    """
    Generates a random graph containing a euler cycle
    - n - number of vertices
    - returns: the generated graph, represented as an adjacency list
    """
    graph = {i: [] for i in range(1, n + 1)}

    # randomize a path through all vertices
    path = [i for i in range(1, n + 1)]
    random.shuffle(path)

    for i, v in enumerate(path[:-1]):
        graph[v].append(path[i + 1])
        graph[path[i + 1]].append(v)

    degrees = _get_degrees_lst(graph)

    # repeat until all vertices have an even degree
    while any(map(lambda x: x % 2, degrees.values())):
        for v, dests in graph.items():
            # add edges to an odd degree vertex
            if degrees[v] % 2 and degrees[v] < n - 2:
                choices = [i for i in range(1, n + 1) if degrees[i] < n - 2 and i not in dests and i != v]

                if not len(choices):
                    continue

                dest = random.choice(choices)
                graph[v].append(dest)
                graph[dest].append(v)
                degrees = _get_degrees_lst(graph)
        degrees = _get_degrees_lst(graph)

    return graph


def find_euler_cycle_lst(graph):
    """
    Finds an Euler cycle in a graph
    - graph - the graph to find an Euler cycle in
    - returns: a list containing the found Euler cycle
    """

    for v in graph:
        if len(graph[v]) % 2 != 0:
            raise ValueError("Podany graf nie jest eulerowski!")

    graph_cpy = {v: [u for u in v_dests] for v, v_dests in graph.items()}

    cycle = [1]

    while len(graph_cpy.keys()) > 0:
        for v in graph_cpy[cycle[-1]].copy():
            graph_cpy[cycle[-1]].remove(v)
            if component_count_lst(graph_cpy) > 1:
                graph_cpy[cycle[-1]].append(v)
                continue
            graph_cpy[v].remove(cycle[-1])
            cycle.append(v)
            break
        else:
            v = graph_cpy[cycle[-1]].pop()
            graph_cpy[v].remove(cycle[-1])
            cycle.append(v)
            break

        for v in tuple(graph_cpy.keys()):
            if not len(graph_cpy[v]):
                graph_cpy.pop(v)

    return cycle


if __name__ == '__main__':
    graph = generate_euler_graph_lst(6)
    #graph = randomize_lst(5, 6)
    draw_graph(graph)
    print(graph)
    try:
        print(find_euler_cycle_lst(graph))
    except ValueError as e:
        print(e)
