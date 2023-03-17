import random
import numpy as np
from zestaw1 import conversions


def randomize_lst(n, l):
    """
    Randomize a graph based on the provided number of edges
    - n - number of vertices
    - l - number of edges
    - returns: a generated graph G(n, l) represented as an adjacency list
    """
    if l > (n * (n - 1)) / 2 or l < 0:
        raise ValueError("Invalid edge amount!")

    graph = {idx: [] for idx in range(1, n + 1)}

    destinations = {idx: [i for i in range(1, n + 1) if i != idx] for idx in range(1, n + 1)}

    for _ in range(l):
        origin = random.choice(list(destinations.keys()))
        end = random.choice(destinations[origin])

        destinations[origin].remove(end)
        destinations[end].remove(origin)

        # If a vertex has no more available connections we remove it from the possible origin dict
        if not destinations[origin]:
            del destinations[origin]
        if not destinations[end]:
            del destinations[end]

        graph[origin].append(end)
        graph[end].append(origin)

    return graph


def randomize_adj(n, l):
    """
    Randomize a graph based on the provided number of edges
    - n - number of vertices
    - l - number of edges
    - returns: a generated graph G(n, l) represented as an adjacency matrix
    """
    graph = randomize_lst(n, l)
    return conversions.lst2adjacency(graph)


def randomize_inc(n, l):
    """
        Randomize a graph based on the provided number of edges
        - n - number of vertices
        - l - number of edges
        - returns: a generated graph G(n, l) represented as an incidence matrix
        """
    graph = randomize_lst(n, l)
    return conversions.lst2incidence(graph)


def randomize_lst_prob(n, p):
    """
    Randomize a graph based on the provided probability of an edge existing
    - n - number of vertices
    - p - probability of an edge existing
    - returns: a generated graph G(n, p) represented as an adjacency list
    """
    if p > 1 or p < 0:
        raise ValueError("Invalid probability value!")

    graph = {idx: [] for idx in range(1, n + 1)}

    for vert in graph.keys():
        for end in [i for i in range(1, n + 1) if i != vert]:
            # Avoid duplicates
            if end in graph[vert]:
                continue

            rng = random.random()
            if rng <= p:
                graph[vert].append(end)
                graph[end].append(vert)

    return graph


def randomize_adj_prob(n, p):
    """
        Randomize a graph based on the provided probability of an edge existing
        - n - number of vertices
        - p - probability of an edge existing
        - returns: a generated graph G(n, p) represented as an adjacency matrix
        """
    graph = randomize_lst_prob(n, p)
    return conversions.lst2adjacency(graph)


def randomize_inc_prob(n, p):
    """
        Randomize a graph based on the provided probability of an edge existing
        - n - number of vertices
        - p - probability of an edge existing
        - returns: a generated graph G(n, p) represented as an incidency matrix
        """
    graph = randomize_lst_prob(n, p)
    return conversions.lst2incidence(graph)


if __name__ == '__main__':
    print(randomize_adj(5, 10))
    print(randomize_adj_prob(5, 0.5))
