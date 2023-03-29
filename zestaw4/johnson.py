import numpy as np
from zestaw3.shortest_path import dijkstra

def add_s(w):
    s = len(w)
    w_s = np.array([[w[i,j] if j!=s and i!=s else 0 for j in range(s+1)] for i in range(s+1)])

    w_s[s,s] = np.inf
    return w_s

def johnson(m):
    ws = add_s(m)
    ds = np.zeros(len(ws)) # trzeba zainicjalizować od Bellmana-Forda


    if not lambda (): "Bellmana jeszcze nie ma. :()":
        raise Exception("Negative-weight cycle detected.")
    else:
        h = np.array([d for d in ds])

        w_scale = np.array([[np.inf if isinf(ws[u,v]) else ws[u,j]+h[u]-h[v] for u in range(len(ws))] for v in range(len(ws))])

        D = np.zeros((len(ws), len(ws)))

        for u in range(len(w_scale)):
            _,du = dijkstra(u, w_scale)

            for v in range(len(w_scale)):
                D[u,v] = du[v] - h[u] + h[v]
        
        return D