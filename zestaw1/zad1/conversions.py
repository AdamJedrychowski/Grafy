import numpy as np

class NotSimpleGrapth(Exception):
    def __init__(self, message='', *, m=None):
        super().__init__(f'{message}\nMatrix:\n{m}' if m is not None else message)
        self.message=message
        self.matrix=m

def check_if_simpe(matrix):
    """The function checks if the matrix (parameter) represents simple graph"""

    if not np.allclose(matrix, matrix.T) or matrix.sum()%2 != 0:
        raise NotSimpleGrapth(message="This is not simple graph!",m=matrix)
    
    for r in matrix:
        for v in r:
            if v != 0 and v != 1:
                raise NotSimpleGrapth(message="This is not simple graph!",m=matrix)
    
    for d in matrix.diagonal():
        if d!=0:
            raise NotSimpleGrapth(message="This is not simple graph!",m=matrix)


def adj2incidence(matrix):
    """Conversion from adjacency matrix into incidence matrix
    - matrix - parameter of type np.ndarray that represents adjacency matrix
    - returns: matrix (np.ndarray) that is incidence matrix"""

    check_if_simpe(matrix)

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