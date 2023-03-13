import networkx as nx
import matplotlib.pyplot as plt


def graphical_sequence(nodes):
    """The function checks if the sequence of integers is a graphical sequence"""
    negative = 0
    for i in nodes:
        if i % 2 == 1:
            negative += 1
    if negative % 2 == 1:
        return False

    nodes.sort(reverse=True)
    while True:
        if not any(nodes):
            return True
        
        if nodes[0] >= len(nodes):
            return False
        
        for i in range(1, nodes[0]+1):
            nodes[i] -= 1
        
        nodes = [i for i in nodes[1:] if i!=0]
        nodes.sort(reverse=True)


if __name__ == '__main__':
    # 1 3 1 2 possible input
    graph = input("Podaj listę stopni wierzchołków grafu:\t")
    graph = list(map(int, graph.split()))
    print(graphical_sequence(graph))