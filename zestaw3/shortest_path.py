import numpy as np

def init(matrix, s):
    ds = np.array([np.Inf for _ in range(len(matrix))], dtype=float)
    ps = np.array([np.NaN for _ in range(len(matrix))], dtype=float)
    ds[s] = 0

    return ds,ps

def relax(u,v, matrix, /, ps, ds):
    if ds[v] > ds[u] + matrix[u,v]:
        ds[v] = ds[u] + matrix[u,v]
        ps[v] = u

def dijkstra(beg, matrix):
    if len(matrix) != matrix[0].size:
        raise Exception("Wrong matrix sizes")
    if beg <= 0 or beg > len(matrix):
        raise Exception("Node index out of range")
    
    ds,ps = init(matrix,beg-1)

    notS = list(range(len(matrix)))

    while notS:
        u = notS[0]
        for node in notS[1:]:
            if ds[node] < ds[u]:
                u = node
                m = ds[u]
        notS.remove(u)

        for v in notS:
            if matrix[u,v] == np.Inf:
                continue
            
            relax(u,v,matrix, ds=ds, ps=ps)

    for i in range(ps.size):
        path = [i,]
        
        while not np.isnan(ps[path[-1]]):
            path.append(int(ps[path[-1]]))
            path[-2] += 1
        path[-1] += 1

        print(f'{beg} -> {i+1}: {list(reversed(path))}; len: {int(ds[i])}')


if __name__ == '__main__':
    G = np.array([[np.Inf, 8, np.Inf, 9, 3, 9, 5],
                [8, np.Inf, np.Inf, 2, 4, np.Inf, 1],
                [np.Inf, np.Inf, np.Inf, np.Inf, np.Inf, 4, np.Inf],
                [9, 2, np.Inf, np.Inf, np.Inf, 9, np.Inf],
                [3, 4, np.Inf, np.Inf, np.Inf, 4, np.Inf],
                [9, np.Inf, 4, 9, 4, np.Inf, np.Inf],
                [5, 1, np.Inf, np.Inf, np.Inf, np.Inf, np.Inf]], dtype=float)

    dijkstra(1, G)