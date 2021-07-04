import networkx as nx
from math import ceil

museum_graph = nx.DiGraph()
rooms = ["lobby", "gallery", "gallery2", "exit"]
div = ceil(10/len(rooms))
for i in range(0, 10, 2):
    museum_graph.add_node(i, room=rooms[i // div])
    museum_graph.add_node(i + 1, room=rooms[(i + 1) // div])
    museum_graph.add_edge(i, i + 1)
    if i > 0:
        museum_graph.add_edge(i-1, i)




