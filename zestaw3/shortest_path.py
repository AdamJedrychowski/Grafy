import numpy as np

def init(matrix, s):
    """initialization of ds and ps arrays for shortest path algorithm
    matrix - adjacency matrix (with weights) of given graph (np.ndarray)
    s - first node in the path (reference to other nodes)
    returns initialized arrays"""

    ds = np.array([np.Inf for _ in range(len(matrix))], dtype=float)
    ps = np.array([np.NaN for _ in range(len(matrix))], dtype=float)
    ds[s] = 0

    return ds,ps

def relax(u,v, matrix, /, ps, ds):
    """ relaxation for shortest path
    u,v - heighbour nodes (to be relaxed)
    matrix - adjacency matrix (with weights) of given graph (np.ndarray)
    ps - previous node in shortest path array
    ds - array of shortest path lengths starting from beginning of path"""

    if ds[v] > ds[u] + matrix[u,v]:
        ds[v] = ds[u] + matrix[u,v]
        ps[v] = u

def dijkstra(beg, matrix, show=True):
    """ Dijkstra's algorithm finding shorthest path in a graph
    matrix - adjacency matrix (with weights) of the graph (np.ndarray)
    beg - the first node in the path"""

    if len(matrix) != matrix[0].size:
        raise Exception("Wrong matrix sizes")
    if beg <= 0 or beg > len(matrix):
        raise Exception("Node index out of range")
    
    ds,ps = init(matrix,beg-1)

    notS = list(range(len(matrix)))

    while notS:
        u = notS[0]
        for node in notS[1:]:
            if ds[node] < ds[u]:
                u = node
                m = ds[u]
        notS.remove(u)

        for v in notS:
            if matrix[u,v] == np.Inf:
                continue
            
            relax(u,v,matrix, ds=ds, ps=ps)

    all_paths = []
    for i in range(ps.size):
        path = [i,]
            
        while not np.isnan(ps[path[-1]]):
            path.append(int(ps[path[-1]]))
            path[-2] += 1
        path[-1] += 1

        all_paths.append(path)
        if show:
            print(f'{beg} -> {i+1}: {list(reversed(path))}; len: {int(ds[i])}')
    
    return all_paths, ds


def shortest_path_matrix(graph, show=True):
    """Algorithm to create matrix of paths cost from each node to others
    - graph - adjacency matrix (with weights) of the graph (np.ndarray)
    - matrix - conatins paths cost from each node to others"""
    matrix = []
    for i in range(len(graph)):
        matrix.append(dijkstra(i+1, graph, False)[1])
        if show:
            print(matrix[i])

    return matrix

def graph_center(graph):
    paths_cost = shortest_path_matrix(graph, False)
    sum = (-1, np.Inf)
    for i in range(len(paths_cost)):
        tmp = np.sum(paths_cost[i])
        if sum[1] > tmp:
            sum = (i+1, tmp)
    print(f'Centrum: {sum[0]}')

def graph_minimax(graph):
    length = shortest_path_matrix(graph, False)
    minmax = (-1, np.Inf)
    for i in range(len(length)):
        tmp = np.max(length[i])
        if minmax[1] > tmp:
            minmax = (i+1, tmp)
    print(f'Centrum minimax: {minmax[0]}')

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from zestaw3.connected import generate_connected_graph
if __name__ == '__main__':
    G = np.array([[np.Inf, 8, np.Inf, 9, 3, 9, 5],
                [8, np.Inf, np.Inf, 2, 4, np.Inf, 1],
                [np.Inf, np.Inf, np.Inf, np.Inf, np.Inf, 4, np.Inf],
                [9, 2, np.Inf, np.Inf, np.Inf, 9, np.Inf],
                [3, 4, np.Inf, np.Inf, np.Inf, 4, np.Inf],
                [9, np.Inf, 4, 9, 4, np.Inf, np.Inf],
                [5, 1, np.Inf, np.Inf, np.Inf, np.Inf, np.Inf]], dtype=float)

    dijkstra(1, G)

    print()
    shortest_path_matrix(G)

    print()
    graph_center(G)
    graph_minimax(G)

    ###
    print("\n---random---\n")

    G = generate_connected_graph(5)
    print(G,'\n')

    dijkstra(1, G)

    print()
    shortest_path_matrix(G)

    print()
    graph_center(G)
    graph_minimax(G)