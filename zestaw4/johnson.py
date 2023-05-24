import numpy as np
from copy import copy
import sys
import os
from bellman_ford import bellman_ford
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from zestaw3.shortest_path import dijkstra
import draw
import zestaw1.conversions as conv

def add_s(G,w):
    s = max(G)+1

    g_s = copy(G)
    g_s[s] = []

    w_s = copy(w)

    for v in G:
        g_s[s].append(v)

        w_s[(s,v)] = 0

    return g_s, w_s, s


def johnson(G, w):
    """
    Johnson algorithm finds distances bewtween all nodes in directed grapth with negative weights.
    G - adjastency matrix
    w - weights dict
    return D - matrix of distances
    """
    Gs, ws, s = add_s(G, w)

    ds,_,without_neg_c = bellman_ford(Gs, ws, s)
    
    if not without_neg_c:
        raise Exception("Negative cycle detected.")

    else:
        h = {v: ds[v] for v in Gs}

        w_daszek = {(u,v): ws[(u,v)] + h[u] - h[v] for u,v in ws}

        n = len(G)
        D = np.zeros((n,n))

        G_matrix = np.array([[w_daszek[(j,i)] if i!=j and (j,i) in w_daszek else np.inf for i in range(1,n+1)] for j in range(1,n+1)])
        
        for u in G:
            _,du = dijkstra(u,G_matrix, False)
            for v in G:
                D[u-1,v-1] = du[v-1] - h[u] + h[v]

        return D


if __name__ == '__main__':
    G = {1: [2,3], 2: [1], 3: [2]}
    w = {(1,2): -1, (2,1): 4, (1,3): -4, (3,2): 2}

    print(w)

    print(johnson(G,w))
    draw.draw_graph(G, draw.Code.DIRECTED_GRAPH)