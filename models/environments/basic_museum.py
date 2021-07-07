import networkx as nx
import random
from math import ceil

class MuseumLayout:
    """
    A class to wrap the museum graph network + provide some util
    TODO implement some way of generating the graph + last graph better
    """

    def __init__(self):
        self._museum_graph = nx.DiGraph()
        rooms = ["lobby", "gallery", "gallery2", "exit"]
        self.styles = {"lobby":"modern", "gallery":"classic",
                       "gallery2":"jazzy", "exit":"none"}
        self._last_painting = 9 #TODO better method
        self._first_painting = 0

        div = ceil(10 / len(rooms))
        for i in range(0, 10, 2):
            self._museum_graph.add_node(i, room=rooms[i // div], prestige=random.uniform(0, 10))
            self._museum_graph.add_node(i + 1, room=rooms[(i + 1) // div], prestige=random.uniform(0, 10))
            self._museum_graph.add_edge(i, i + 1)
            if i > 0:
                self._museum_graph.add_edge(i - 1, i)

    @property
    def last_painting(self):
        return self._last_painting

    @property
    def first_painting(self):
        return self._first_painting

    @property
    def museum_graph(self):
        return self._museum_graph

    def get_style(self, room: str) -> str:
        """
        Returns the style of paintings in the room
        :param room: str
            The name of the room being investigated
        :return: str
            Name of the art style in the room
        """
        return self.styles[room]

    def get_room(self, painting_number: int) -> str:
        """
        Gets the name of the room the painting is in
        :param painting_number: int
            The painting ID to investigate
        :return: str
            Name of the room the painting is in
        """
        return self._museum_graph.nodes[painting_number]['room']

    def get_prestige(self, painting_number: int) -> int:
        """
        Returns the painting's prestige value
        :param painting_number: int
            The painting ID being investigated
        :return: int
            The prestige value of the painting (0-10)
        """
        return self._museum_graph.nodes[painting_number]['prestige']

    def random_painting(self) -> int:
        """
        Returns a randomly selected painting in the museum
        :return: int
            The painting ID of the randomly selected painting
        """
        return random.choice(self.museum_graph_list())

    def museum_graph_list(self) -> list:
        """
        Returns all paintings in the museum as a list
        :return: list
            A list of all paintings in the museum
        """
        return list(self._museum_graph)

    def get_successor_list(self, painting_number: int) -> list:
        """
        Returns a list of the painting's successors
        :param painting_number: int
            The painting ID to get next paintings for
        :return: list
            List of all successor paintings
        """
        return list(self._museum_graph.successors(painting_number))






