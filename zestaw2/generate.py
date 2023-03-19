import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sequence import graphical_sequence, randomize
import random

def generate_regular_graph(n, k):
    if k >= n or (k%2 == 1 and n%2 == 1):
        return
    _, graph = graphical_sequence([k for _ in range(n)])
    if k+1 == n:
        randomize(graph, 0)
    else:
        randomize(graph, random.randint(1,2*n))

if __name__ == '__main__':
    data = input('Podaj liczbe (wierzchołków, krawędzi): ')
    generate_regular_graph(*list(map(int, data.split())))
