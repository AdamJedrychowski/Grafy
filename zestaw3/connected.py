import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import random
from zestaw1.randomization import randomize_lst
from zestaw1.conversions import lst2adjacency
import draw
import numpy as np

def dfs(graph, start=1, visited=None):
    """recursive function which checks if graph is connected
    - graph - neighborhood list
    - start - starting node
    - visited - set of visited nodes"""
    if visited is None:
        visited = set()
    visited.add(start)
    for next in set(graph[start]) - visited:
        dfs(graph, next, visited)
    return len(visited) == len(graph)

def generate_connected_graph(n):
    """function which generates random connected graph
    - n - number of nodes"""
    while True:
        graph = randomize_lst(n, random.randint(n-1, n*(n-1)/2))
        if dfs(graph):
            break
    graph = lst2adjacency(graph)

    length = len(graph)
    matrix_graph = np.full((length, length), np.inf)
    for i in range(length):
        for j in range(i+1, length):
            if graph[i][j]:
                rand = random.randint(1,10)
                matrix_graph[i][j] = rand
                matrix_graph[j][i] = rand

    draw.draw_graph(matrix_graph, coding=draw.Code.WEIGHTED_GRAPH)

    return matrix_graph


if __name__ == '__main__':
    generate_connected_graph(int(input('Podaj liczbe węzłów: ')))