import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from draw import draw_graph, Code
import random
import math
from zestaw1.conversions import inc2list, adj2list

def graphical_sequence(nodes):
    """The function checks if the sequence of integers is a graphical sequence
    - nodes - list of integers, example: 2 2 4 3 7 3 1 1
    - returns: False, None if sequence is not graphical else True and dictionary {node: [neighbors]}"""
    negative = 0
    for i in nodes:
        if i % 2 == 1:
            negative += 1
    if negative % 2 == 1:
        return False, None

    neighbors = {i: [] for i in range(1, len(nodes)+1)}
    nodes = [[i, j] for i, j in enumerate(nodes, start=1)]
    nodes.sort(reverse=True, key=lambda x: x[1])
    while True:
        if not nodes or not any(list(zip(*nodes))[1]):
            return True, neighbors
        
        if nodes[0][1] >= len(nodes):
            return False, None
        
        for i in range(1, nodes[0][1]+1):
            nodes[i][1] -= 1
            neighbors[nodes[0][0]].append(nodes[i][0])
            neighbors[nodes[i][0]].append(nodes[0][0])
        
        nodes = [[i[0], i[1]] for i in nodes[1:] if i[1]!=0]
        nodes.sort(reverse=True, key=lambda x: x[1])


def randomize(nodes, shuffle_num=1, coding=Code.NEIGHBORHOOD_LIST):
    """The function randomizes graph edges
    - nodes - representation of graph
    - shuffle_num - number of shuffles
    - coding - which representation is passed, values from Code"""
    if coding == Code.ADJACENCY_MATRIX:
        adj2list(nodes)
    elif coding == Code.MATRIX_INCIDENT:
        inc2list(nodes)
    elif coding == Code.GRAPHICAL_SEQUENCE:
        _, nodes = graphical_sequence(nodes)

    for _ in range(shuffle_num):
        for _ in range(math.factorial(len(nodes))):
            node = random.sample(list(nodes.keys()), 2)
            edges = [(node[0], random.choice(nodes[node[0]])), (node[1], random.choice(nodes[node[1]]))]
            if not (edges[0][0] == edges[1][1] or edges[0][1] in edges[1] or edges[1][1] in nodes[edges[0][1]] or edges[0][0] in nodes[edges[1][0]]):
                break
        else:
            return None 

        tmp = nodes[edges[0][0]]
        tmp[tmp.index(edges[0][1])] = edges[1][0]
        tmp = nodes[edges[1][0]]
        tmp[tmp.index(edges[1][1])] = edges[0][0]
        tmp = nodes[edges[0][1]]
        tmp[tmp.index(edges[0][0])] = edges[1][1]
        tmp = nodes[edges[1][1]]
        tmp[tmp.index(edges[1][0])] = edges[0][1]

    draw_graph(nodes)



if __name__ == '__main__':
    # 1 3 1 2 possible input
    seq = input("Podaj listę stopni wierzchołków grafu: ")
    seq = list(map(int, seq.split()))
    flag, graph = graphical_sequence(seq)
    if flag:
        draw_graph(graph)
        num = input("Podaj liczbę przetasowań: ")
        randomize(graph, int(num))