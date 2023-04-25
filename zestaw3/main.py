import connected
import shortest_path
import minimal_spanning_tree

G = connected.generate_connected_graph(4)
shortest_path.dijkstra(1, G)
print()
shortest_path.shortest_path_matrix(G)

print()
shortest_path.graph_center(G)
shortest_path.graph_minimax(G)

minimal_spanning_tree.minimal_spanning_tree(G)