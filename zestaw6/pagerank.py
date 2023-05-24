import random

def check_list_dangling(lst):
    for out in lst.values():
        if not out:
            raise Exception("Dangling nodes!")

def random_walk(lst, N, d=0.15):
    check_list_dangling(lst)

    ks = list(lst.keys())
    node = random.choice(ks)

    visited = {k: 1 if k==node else 0 for k in ks}

    for _ in range(N):
        if random.random() < d:
            node = random.choice(ks)
        else:
            node = random.choice(lst[node])
        visited[node] += 1
    
    for n in lst:
        visited[n] /= N
    
    return dict(sorted(visited.items(), key=lambda item: item[1], reverse=True))
    


def vector_iteration(lst):
    check_list_dangling(lst)
    pass

if __name__ == '__main__':
    www = {'A':['D','E','B'], 'B':['E','C'], 'C':['B','D','F'], 'D':['B'], 'E':['D','B','F'], 'F':['B']}

    print(random_walk(www, N=100_000))