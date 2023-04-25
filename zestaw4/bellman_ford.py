import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from kosaraju import kosaraju, generate_random_strongly_connected_graph
import draw

def bellman_ford(graph, weights, start):
    """
    Finds the shortest paths from starting vertex to all vertices to the others
    - graph - random strongly connected graph represented as adjacency list
    - weights - dictionary of edge weights
    - start - number of first vertex
    - returns: dist as a dictionary where the keys are vertices and values are lengths are shortes paths, prev as a dictionary where the keys are vertices and value for each of them is a list represented as all vertices from the path, True or False
    """
    n = len(graph)
    dist = {i: float('inf') for i in graph}
    dist[start] = 0
    prev = {v: [] for v in graph}
    for i in range(1, n-1):
        for u in graph:
            for v in graph[u]:
                if dist[v] > dist[u] + weights[(u, v)]:
                    dist[v] = dist[u] + weights[(u, v)]
                    prev[v] = prev[u] + [v]
    for u in graph:
        for v in graph[u]:
            if dist[v] > dist[u] + weights[(u, v)]:
                return {}, {}, False
    return dist, prev, True


if __name__ == '__main__':
    while True:
        graph, weights = generate_random_strongly_connected_graph(5)
        dist, prev, status = bellman_ford(graph, weights, 1)
        if status == True:
            print("Losowy silnie spójny graf:")
            print(graph)
            print("Silnie spójne składowe:")
            print(kosaraju(graph))
            print("Wagi krawędzi:")
            print(weights)
            print("Najkrótsze ścieżki:")
            print(bellman_ford(graph, weights, 1))
            print()
            for i in range(1,len(graph)+1):
                dist, prev, status = bellman_ford(graph, weights, i)
                print(dist)
            
            draw.draw_graph(graph, draw.Code.DIRECTED_GRAPH)
            break
