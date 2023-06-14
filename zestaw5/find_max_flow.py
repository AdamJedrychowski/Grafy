import math

import numpy as np

from generate_flow_network import generate_flow_network, draw_flow_network


def get_residual(graph, flow):
    """
    Calculates the residual network for a flow network
    - graph - the flow network as an adjacency matrix
    - flow - matrix of flow values for the network's edges
    - returns: the residual network as an adjacency matrix
    """
    residual = [[math.inf for _ in v] for v in graph]
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if not math.isinf(graph[i][j]):
                residual[i][j] = graph[i][j] - flow[i][j]
    return residual


def BFS(graph, start, target):
    """
    Finds the shortest path from start to target
    - graph - the graph containing the path in adjacency matrix form
    - start - index of path start
    - target - index of path end
    - returns: list containing the indices of vertices on the shortest path from start to target
                or nothing if no such path exists
    """
    queue = [start]

    ds = [math.inf for _ in graph]
    ds[start] = 0
    ps = [None for _ in graph]

    while len(queue) != 0:
        v = queue.pop(0)

        neighbors = [i for i, u in enumerate(graph[v]) if not math.isinf(u) and u != 0]

        for u in neighbors:
            if math.isinf(ds[u]):
                ds[u] = ds[v] + 1
                ps[u] = v
                queue.append(u)

    path = []
    v = target
    while v != start:
        path.append(v)

        if ps[v] is None:
            return []

        v = ps[v]
    path.append(start)
    path.reverse()

    return path


def ford_fulkerson(graph):
    """
    Ford-Fulkerson's algorithm for finding the maximal flow in a network
    - graph - the flow network as a adjacency matrix
    - returns: a matrix containing the flow for every edge in the network
    """
    start = 0
    target = len(graph) - 1
    f = [[0 for _ in v] for v in graph]

    residual = get_residual(graph, f)
    path = BFS(residual, start, target)

    while len(path) != 0:
        min_cf = math.inf
        for i in range(1, len(path)):
            if not math.isinf(graph[path[i - 1]][path[i]]):
                cf = graph[path[i - 1]][path[i]] - f[path[i - 1]][path[i]]
            elif not math.isinf(graph[path[i]][path[i - 1]]):
                cf = f[path[i]][path[i - 1]]
            else:
                cf = 0
            if cf < min_cf:
                min_cf = cf

        for i in range(1, len(path)):
            if not math.isinf(graph[path[i - 1]][path[i]]):
                f[path[i - 1]][path[i]] += min_cf
            else:
                f[path[i]][path[i - 1]] -= min_cf

        residual = get_residual(graph, f)
        path = BFS(residual, start, target)

    return flow_to_network(f, graph)


def flow_to_network(flow, graph):
    """
    Converts the given flow matrix into an adjacency matrix,
    simulating a flow network with capacities equal to flow
    - flow - flow matrix
    - returns: flow network with capacities equal to flow values
    """
    network = np.array([[flow[i][j] if not math.isinf(u) else u for j, u in enumerate(v)] for i, v in enumerate(graph)])
    return network


if __name__ == '__main__':
    graph, layers = generate_flow_network(2)

    print('\nnetwork:')
    print(graph)

    flow = ford_fulkerson(graph)

    print('\nmax flow:')
    print(flow)

    draw_flow_network(flow, layers)

    print('\nMax flow value:', sum([v[-1] for v in flow if v[-1] != float('inf')]))
