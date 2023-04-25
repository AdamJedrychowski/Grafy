import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import draw

def hamiltonian_cycle(graph, visited = None, cycle = None, node = None):
    """
    Find a hamiltonian cycle in a graph
    - graph - represented as adjacency list
    - returns: list of vertices if cycle is found, else None
    """
    if cycle is None and visited is None:
        cycle = []
        visited = {v: False for v in graph}

    if node is not None:
        visited[node] = True
        cycle.append(node)

        if len(cycle) == len(graph):
            if cycle[-1] in graph[cycle[0]]:
                cycle.append(cycle[0])
                return cycle

        for v in graph[node]:
            if not visited[v]:
                result_cycle = hamiltonian_cycle(graph, visited, cycle, v)
                if result_cycle:
                    return result_cycle

        visited[node] = False
        cycle.pop()

    else:
        for v in graph:
            if not visited[v]:
                result_cycle = hamiltonian_cycle(graph, visited, cycle, v)
                if result_cycle:
                    return result_cycle

    return None


if __name__ == '__main__':
    graphs = [{
        1:[3,5,6], 
        2:[4,5,6], 
        3:[1,5], 
        4:[2,5], 
        5:[1,3,2,4], 
        6:[1,2]},
        {
        1:[5, 6],
        2:[3, 6],
        3:[2, 5, 6, 7],
        4:[5],
        5:[1, 3, 4, 6],
        6:[1, 2, 3, 5],
        7:[3]
        }]

    for graph in graphs:
        print(graph)
        draw.draw_graph(graph)
        cycle = hamiltonian_cycle(graph)
        if cycle:
            print("Hamiltonian cycle ", cycle)
        else:
            print("Not found")
        print()

