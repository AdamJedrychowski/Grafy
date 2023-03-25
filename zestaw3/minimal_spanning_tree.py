from connected import generate_connected_graph
import numpy as np
from zestaw1.conversions import adj2list
import draw

def minimal_spanning_tree(graph):
    """Function which is searching for minimal spanning tree
    - graph - weight adjacency matrix
    - return: minimal spanning tree (weight adjacency matrix)"""
    length = len(graph)
    tree = np.full((length, length), np.inf)
    visited = [0]
    edges = [(0,j,graph[0][j]) for j in range(length) if graph[0][j] != np.inf]

    while len(visited) != length:     
        short = min(edges, key = lambda x: x[2])
        tree[short[1]][short[0]] = tree[short[0]][short[1]] = short[2]
        visited.append(short[1])
        edges = [j for j in edges if j[1] != short[1]]
        edges.extend([(short[1],j,graph[short[1]][j]) for j in range(length) if graph[short[1]][j] != np.inf and j not in visited])

    draw.draw_graph(tree, coding=draw.Code.WEIGHTED_GRAPH)
    return tree



if __name__ == '__main__':
    minimal_spanning_tree(generate_connected_graph(6))