import numpy as np

class NotSimpleGraph(Exception):
    def __init__(self, message='', *, r=None):
        super().__init__(f'{message}\nRepresentation:\n{r}' if r is not None else message)
        self.message=message
        self.represent=r

def check_if_simple_adj(matrix):
    """The function checks if the adjacency matrix (parameter) represents a simple graph"""
    
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
    """The function checks if the adjacency list (parameter as dict - nodes counting from 1) represents a simple graph"""

    for k in lst:
        if k in lst[k]:
            raise NotSimpleGraph(message="This is not simple graph! - Contains loop.",r=lst)
        
        prev = None
        for node in sorted(lst[k]):
            if node == prev:
               raise NotSimpleGraph(message="This is not simple graph! - Contains multiple egde.",r=lst)
            prev = node

def check_if_simple_inc(matrix):
    """The function checks if the incidence matrix (parameter as np.ndarray) represents a simple graph"""

    for i in range(len(matrix[0])):
        if sum(matrix[:,i]) > 2:
            raise NotSimpleGraph(message="This is not simple graph! This is a hypergraph.",r=matrix)
        elif sum(matrix[:,i]) == 1:
            raise NotSimpleGraph(message="This is not simple graph! Only one node in the egde.",r=matrix)
        elif sum(matrix[:,i]) < 0:
            raise NotSimpleGraph(message="Unknown coding! Negative numbers.",r=matrix)
        elif sum(matrix[:,i]) == 0:
            for v in matrix[:,i]:
                if v != 0:
                    break
            else:
                raise NotSimpleGraph(message="Empty edge.",r=matrix)
    
    for row in matrix:
        for v in row:
            if v!=1 and v!=0 and v!=-1:
                raise NotSimpleGraph(message="Unknown coding! Only 0/1 values supported.",r=matrix)
    
    for i in range(len(matrix[0])):
        for j in range(i+1,len(matrix[0])):
            if np.allclose(matrix[:,i], matrix[:,j]):
                raise NotSimpleGraph(message="This is not simple graph! Multiple edge found.",r=matrix)




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


def lst2incidence(lst, directed=False):
    """Conversion from adjacency list into incidence matrix
    - lst - dcitionary parameter that represents adjacency list (with node numbers from 1)
    - returns: matrix (np.ndarray) that is incidence matrix
    - raises NotSimpleGraph if the graph represented by list is not simple"""

    check_if_simple_lst(lst)

    s = max(lst)
    if not directed:
        e = int( sum((len(l) for l in lst.values())) )//2
        inc = np.zeros((s,e), dtype=int)
        edge_n=0

        for i in sorted(lst):
            for j in lst[i]:
                if j > i:
                    inc[i-1,edge_n]=1
                    inc[j-1,edge_n]=1
                    edge_n += 1

    else:
        e = int( sum((len(l) for l in lst.values())) )
        inc = np.zeros((s,e), dtype=int)
        edge_n=0

        for i in sorted(lst):
            for j in lst[i]:
                inc[i-1,edge_n]=-1
                inc[j-1,edge_n]=1
                edge_n += 1
    return inc

def inc2list(matrix, directed=False):
    """Conversion from incidence matrix into adjacency list
    - matrix - parameter of type np.ndarray that represents incidence matrix (rows - nodes, columns - edges)
    - returns: lst (dictionary) that is adjacency list
    - raises NotSimpleGraph if the graph represented by matrix is not simple"""

    check_if_simple_inc(matrix)

    lst = {i+1: [] for i in range(len(matrix))}

    for edge in matrix.T:
        i, = edge.nonzero() # coma for unpacking a tuple
        if not directed:
            lst[i[1] +1].append(i[0] +1)
            lst[i[0] +1].append(i[1] +1)
        else:
            if edge[i[0]] == -1:
                lst[i[0] +1].append(i[1] +1)
            else:
                lst[i[1] +1].append(i[0] +1)
    
    for l in lst.values():
        l.sort()

    return lst



def lst2adjacency(lst):
    """Conversion from adjacency list into adjacency matrix
    - lst - dcitionary parameter that represents adjacency list (with node numbers from 1)
    - returns: matrix (np.ndarray) that is adjacency matrix
    - raises NotSimpleGraph if the graph represented by list is not simple"""

    check_if_simple_lst(lst)

    size = max(lst)
    adj = np.zeros((size, size), dtype=int)

    for i in lst:
        for j in lst[i]:
            adj[i-1][j-1]=1

    return adj

def adj2list(matrix, wighted_graph=False):
    """Conversion from adjacency matrix into adjacency list
    - matrix - parameter of type np.ndarray that represents adjacency matrix (rows, cols - number of vertices)
    - returns: list (dictionary) that is adjacency list
    - raises NotSimpleGraph if the graph represented by matrix is not simple"""

    check_if_simple_adj(matrix)

    rows, cols = matrix.shape[:2]
    lst = {}

    for i in range(rows):
        key = i+1
        if not wighted_graph:
            vertices = [j+1 for j in range(cols) if matrix[i][j] == 1]
        else:
            vertices = [(j+1, matrix[i][j]) for j in range(cols) if matrix[i][j] != np.inf]
        lst[key] = vertices

    return lst


def inc2adjacency(matrix):
    """Conversion from incidence matrix into adjacency matrix
    - matrix - parameter of type np.ndarray that represents adjacency matrix (rows, cols - number of vertices)
    - returns: matrix (np.ndarray) that is adjacency matrix
    - raises NotSimpleGraph if the graph represented by matrix is not simple"""

    check_if_simple_inc(matrix)

    list = inc2list(matrix)
    adj = lst2adjacency(list)

    return adj




if __name__ == '__main__':

    print('* Adjastency matrix to incidence matrix *\n')

    graphs = [np.array([[1,2],[3,4]]),\
    np.array([[1,2],[2,1]]),\
    np.array([[1,0],[0,1]]),\
    np.array([[0,1],[1,0]]),\
    np.array([[0,1,1,1,1],[1,0,0,0,0],[1,0,0,1,0],[1,0,1,0,1], [1,0,0,1,0]]),\
    np.array([[0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],[1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],[0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],[0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],[1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],[1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],[0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0],[0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1],[0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]]),\
    np.array([[0, 0, 0],[0,0,1],[0,1,0]])
    ]

    for m in graphs:
        try:
            print(m, '\n \\/\n \\/\n', adj2incidence(m), '\n')
        except NotSimpleGraph as e:
            print(e, '\n')

    print('* Adjastency list to incidence matrix *\n')

    graphs = [{1: [2,3,3], 2:[1], 3:[1,1]},\
    {1:[1,2], 2: [1]},\
    {1:[2,3,4], 2:[1], 3:[1,4], 4:[1,3]},
    {1:[], 2:[3], 3:[2]},\
    {1:[2,5,6], 2:[1,3,6], 3:[2,4,5,12], 4:[3,8,9,11],\
    5:[1,3,7,9], 6:[1,2,7], 7:[5,6,8], 8:[4,7,9,12],\
    9:[4,5,8,10], 10:[9], 11:[4], 12:[3,8]} ]

    for l in graphs:
        try:
            # check_if_simple_lst(l)
            print(l, '\n \\/\n \\/\n', lst2incidence(l), '\n')
        except NotSimpleGraph as e:
            print(e,'\n')
        # else:
        #     print("OK\n")

    print('* Incidence matrix to adjastency list *\n')
    
    graphs = [np.array([[1,0],[1,1]]),\
    np.array([[1,0, 2],[1,1,0], [0,1,0]]),\
    np.array([[1, 1, 0],[1,1,1], [0,0,1]]),\
    np.array([[1, 1],[1,1], [0,1]]),\

    np.array([[1, 0, 0],[1,0,1], [0,0,1]]),\
    np.array([[1, 1, 0],[1,0,1], [0,1,1]]),\
    np.array([[1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],\
        [1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],\
        [0,1,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0],\
        [0,0,1,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0],\
        [0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0],\
        [0,0,0,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0],\
        [0,0,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0],\
        [0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,1],\
        [0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,1,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],\
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],\
        ])
    ]

    for m in graphs:
        try:
            print(m, '\n \\/\n \\/\n', inc2list(m), '\n')
        except NotSimpleGraph as e:
            print(e, '\n')


    graphs = [{1: [2,3,3], 2:[1], 3:[1,1]},\
        {1:[1,2], 2: [1]},\
        {1:[2,3,4], 2:[1,3,4,5], 3:[1,2,5], 4:[1,2,5], 5:[2,3,4]},
        {1:[], 2:[3], 3:[2]}, ]
    
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    # import draw
    # draw.draw_graph(graphs[-1])

    # print('* Adjacency list to adjacency matrix *', '\n')
    # for l in graphs:
    #     try:
    #         print(l, '\n \\/\n \\/\n', lst2adjacency(l), '\n')
    #     except Exception as e:
    #         print(e,'\n')



    graphs = [np.array([[1,2],[3,4]]),\
    np.array([[1,2],[2,1]]),\
    np.array([[1,0],[0,1]]),\
    np.array([[0,1],[1,0]]),\
    np.array([[0,1,1,1],[1,0,0,0],[1,0,0,1],[1,0,1,0]]),\
    np.array([[0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],[1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],[0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],[0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],[1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],[1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],[0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0],[0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1],[0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]]),\
    np.array([[0,1,1,1,0],[1,0,1,1,1],[1,1,0,0,1],[1,1,0,0,1],[0,1,1,1,0]]),\
    np.array([[0, 0, 0],[0,0,1],[0,1,0]])
    ]

    print('* Adjacency matrix to adjacency list *', '\n')
    for m in graphs:
        try:
            print(m, '\n \\/\n \\/\n', adj2list(m), '\n')
        except Exception as e:
            print(e, '\n')

    graphs = [np.array([[1,0,0,0,0,0,1,1],[1,1,1,1,0,0,0,0],[0,0,0,1,1,0,0,1],[0,1,0,0,0,1,1,0],[0,0,1,0,1,1,0,0]]),\
    np.array([[1,0, 2],[1,1,0], [0,1,0]]),\
    
    ]

    print('* Incidence matrix to adjacency matrix *', '\n')
    for m in graphs:
        try:
            print(m, '\n \\/\n \\/\n', inc2adjacency(m), '\n')
        except Exception as e:
            print(e, '\n')
