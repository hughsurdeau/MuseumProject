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

class MuseumGraph:
    """
    A class to wrap the museum graph network + provide some util
    """

    def __init__(self):
        self.graph = nx.DiGraph()
        rooms = ["lobby", "gallery", "gallery2", "exit"]
        self.styles = {"lobby":"modern", "gallery":"classic",
                       "gallery2":"jazzy", "exit":"none"}
        self._last_painting = 9 #TODO better method

        div = ceil(10 / len(rooms))
        for i in range(0, 10, 2):
            self.graph.add_node(i, room=rooms[i // div])
            self.graph.add_node(i + 1, room=rooms[(i + 1) // div])
            self.graph.add_edge(i, i + 1)
            if i > 0:
                self.graph.add_edge(i - 1, i)

    def get_style(self, room):
        return self.styles[room]

    @property
    def last_painting(self):
        return self._last_painting





