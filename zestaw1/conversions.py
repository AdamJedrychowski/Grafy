import numpy as np

class NotSimpleGraph(Exception):
    def __init__(self, message='', *, r=None):
        super().__init__(f'{message}\nRepresentation:\n{r}' if r is not None else message)
        self.message=message
        self.represent=r

def check_if_simple_adj(matrix):
    """The function checks if the adjacency matrix (parameter) represents simple graph"""

    # symetric matrix and even sum of degrees
    if not np.allclose(matrix, matrix.T) or matrix.sum()%2 != 0:
        raise NotSimpleGraph(message="This is not simple graph! Some egde is direct.",r=matrix)
    
    # without multiple egdes
    for r in matrix:
        for v in r:
            if v != 0 and v != 1:
                raise NotSimpleGraph(message="This is not simple graph! Contains multiple egde.",r=matrix)
    
    # without loops
    for d in matrix.diagonal():
        if d!=0:
            raise NotSimpleGraph(message="This is not simple graph! Countains loop.",r=matrix)

def check_if_simple_lst(lst):
    """The function checks if the adjacency list (parameter as dict) represents simple graph"""

    for k in lst:
        if k in lst[k]:
            raise NotSimpleGraph(message="This is not simple graph! - Contains loop.",r=lst)
        
        prev = None
        for node in sorted(lst[k]):
            if node == prev:
               raise NotSimpleGraph(message="This is not simple graph! - Contains multiple egde.",r=lst)
            prev = node

            if k not in lst[node]:
                raise NotSimpleGraph(message="This is not simple graph! Some egde is direct.",r=lst)



def adj2incidence(matrix):
    """Conversion from adjacency matrix into incidence matrix
    - matrix - parameter of type np.ndarray that represents adjacency matrix
    - returns: matrix (np.ndarray) that is incidence matrix
    - raises NotSimpleGraph if the graph represented by matrix is not simple"""

    check_if_simple_adj(matrix)

    s = len(matrix)
    inc = np.zeros((s, int(matrix.sum())//2), dtype=int)
    edge_n = 0
    for i in range(s):
        for j in range(i+1, s):
            if int(matrix[i,j]) == 1:
                inc[i,edge_n]=1
                inc[j,edge_n]=1
                edge_n += 1
    
    return inc


def lst2incidence(lst):
    check_if_simple_lst(lst)




if __name__ == '__main__':
    graphs = [np.array([[1,2],[3,4]]),\
    np.array([[1,2],[2,1]]),\
    np.array([[1,0],[0,1]]),\
    np.array([[0,1],[1,0]]),\
    np.array([[0,1,1,1],[1,0,0,0],[1,0,0,1],[1,0,1,0]]),\
    np.array([[0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],[1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],[0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],[0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],[1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],[1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],[0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0],[0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1],[0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]]),\
    ]

    for m in graphs:
        try:
            print(adj2incidence(m), '\n')
        except Exception as e:
            print(e, '\n')


    graphs = [{1: [2,3,3], 2:[1], 3:[1,1]},\
    {1:[1,2], 2: [1]}, {1:[3], 2:[1], 3:[1]}]

    for l in graphs:
        try:
            check_if_simple_lst(l)
        except Exception as e:
            print(e,'\n')
        else:
            print("OK\n")