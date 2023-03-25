import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from zestaw1.randomization import randomize_lst_prob
from zestaw1.conversions import lst2adjacency, lst2incidence
import draw


if __name__ == '__main__':
    graph = randomize_lst_prob(6, 0.3, directed=True)
    print(graph, end='\n\n')
    draw.draw_graph(graph, coding=draw.Code.DIRECTED_GRAPH)

    print(lst2adjacency(graph), end='\n\n')
    print(lst2incidence(graph, directed=True), end='\n\n')