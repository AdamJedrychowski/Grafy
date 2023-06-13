import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from zestaw1.conversions import lst2adjacency
import random
import numpy as np
import draw

def check_list_dangling(lst):
    for out in lst.values():
        if not out:
            raise Exception("Dangling nodes!")

def random_walk(lst, *, N, d=0.15):
    check_list_dangling(lst)

    ks = list(lst.keys())
    node = random.choice(ks)

    visited = {k: 1 if k==node else 0 for k in ks}

    for _ in range(N):
        if random.random() < d:
            node = random.choice(ks)#[n for n in ks  if n!=node])
        else:
            node = random.choice(lst[node])
        visited[node] += 1
    
    for n in lst:
        visited[n] /= N
    
    return dict(sorted(visited.items(), key=lambda item: item[1], reverse=True))
    


def vector_iteration(lst, *, eps=1e-6, d=0.15):
    check_list_dangling(lst)
    lst_nums = {ord(i)-ord('A')+1: [ord(j)-ord('A')+1 for j in lst[i]] for i in lst}
    
    A = lst2adjacency(lst_nums, direct=True)
    n = len(A)
    P = np.array([[(1-d)*A[i,j]/len(lst_nums[i+1]) + d/n for j in range(n)] for i in range(n)]) # adjastency list indexes >0 - i+1
    p_t = np.array([1/n for _ in range(n)])

    it = 0
    while True:
        it += 1
        p_next = p_t.dot(P)

        if np.linalg.norm(p_next-p_t) < eps:
            break
        
        p_t = p_next


    visited = {chr(ord('A')+i): p_next[i] for i in range(n)}
    return dict(sorted(visited.items(), key=lambda item: item[1], reverse=True)), it

if __name__ == '__main__':
    sites = [\
        {'A':['D','E','B'], 'B':['E','C'], 'C':['B','D','F'], 'D':['B'], 'E':['D','B','F'], 'F':['B']},\
        {'A':['E','F','I'], 'B':['A','C','F'], 'C':['B','D','E','L'], 'D':['C','E','H','I','K'], 'E':['C','G','H','I'], 'F':['B','G'], 'G':['E','F','H'], 'H':['D','G','I','L'], 'I':['D','E','H','J'], 'J':['I'], 'K':['D','I'], 'L':['A','H']}\
        ]

    n = 100_000
    for www in sites:
        print(f"Graf: {www}\n")

        rank = random_walk(www, N=n)
        print("Błądzenie losowe:")
        for p in rank.items():
            print(f'   {p[0]}: {p[1]:.5f}')

        rank,zb = vector_iteration(www, eps=1e-9)
        print("\nMetoda iteracji wektora obsadzeń:")
        for p in rank.items():
            print(f'   {p[0]}: {p[1]:.5f}')
        print(f'   Zbieżność po {zb} iteracjach.')


        draw.draw_graph(www, coding=draw.Code.DIRECTED_GRAPH)
        n*=10
        print('')