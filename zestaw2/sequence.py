import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from draw import draw_graph
import numpy as np

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
    

if __name__ == '__main__':
    # 1 3 1 2 possible input
    seq = input("Podaj listę stopni wierzchołków grafu:\t")
    seq = list(map(int, seq.split()))
    flag, graph = graphical_sequence(seq)
    if flag:
        draw_graph(graph)