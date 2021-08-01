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
        self.rooms = ["lobby", "left_gallery", "right_gallery", "left_gallery1",
                 "left_gallery2", "right_gallery1", "right_gallery2", "exit"]
        self.styles = {"lobby": "modern", "left_gallery": "classic", "left_gallery1": "classic","left_gallery2": "classic",
                       "right_gallery": "jazzy", "right_gallery1": "jazzy", "right_gallery2": "jazzy", "exit": "none"}

        self._last_painting = 70  # TODO better method
        self._first_painting = 0

        # Lobby
        for i in range(0, 10, 2):
            self._museum_graph.add_node(i, room="lobby", prestige=random.uniform(0, 10))
            self._museum_graph.add_node(i + 1, room="lobby", prestige=random.uniform(0, 10))
            self._museum_graph.add_edge(i, i + 1)
            if i > 0:
                self._museum_graph.add_edge(i - 1, i)

        # left_gallery
        for i in range(10, 20, 2):
            self._museum_graph.add_node(i, room="left_gallery", prestige=random.uniform(0, 10))
            self._museum_graph.add_node(i + 1, room="left_gallery", prestige=random.uniform(0, 10))
            self._museum_graph.add_edge(i, i + 1)
            if i > 0:
                self._museum_graph.add_edge(i - 1, i)

        self._museum_graph.add_edge(9, 10)

        # right_gallery
        for i in range(20, 30, 2):
            self._museum_graph.add_node(i, room="right_gallery", prestige=random.uniform(0, 10))
            self._museum_graph.add_node(i + 1, room="right_gallery", prestige=random.uniform(0, 10))
            self._museum_graph.add_edge(i, i + 1)
            if i > 0:
                self._museum_graph.add_edge(9, i)

        self._museum_graph.add_edge(i - 1, 20)

        # left_gallery1
        for i in range(30, 40, 2):
            self._museum_graph.add_node(i, room="left_gallery1", prestige=random.uniform(0, 10))
            self._museum_graph.add_node(i + 1, room="left_gallery1", prestige=random.uniform(0, 10))
            self._museum_graph.add_edge(i, i + 1)
            if i > 0:
                self._museum_graph.add_edge(i - 1, i)

        self._museum_graph.add_edge(19, 30)

        # left_gallery2
        for i in range(40, 50, 2):
            self._museum_graph.add_node(i, room="left_gallery2", prestige=random.uniform(0, 10))
            self._museum_graph.add_node(i + 1, room="left_gallery2", prestige=random.uniform(0, 10))
            self._museum_graph.add_edge(i, i + 1)
            if i > 0:
                self._museum_graph.add_edge(i - 1, i)

        self._museum_graph.add_edge(39, 40)

        # right_gallery1
        for i in range(50, 60, 2):
            self._museum_graph.add_node(i, room="right_gallery1", prestige=random.uniform(0, 10))
            self._museum_graph.add_node(i + 1, room="right_gallery1", prestige=random.uniform(0, 10))
            self._museum_graph.add_edge(i, i + 1)
            if i > 0:
                self._museum_graph.add_edge(i - 1, i)

        self._museum_graph.add_edge(29, 50)

        # right_gallery2
        for i in range(60, 70, 2):
            self._museum_graph.add_node(i, room="right_gallery2", prestige=random.uniform(0, 10))
            self._museum_graph.add_node(i + 1, room="right_gallery2", prestige=random.uniform(0, 10))
            self._museum_graph.add_edge(i, i + 1)
            if i > 0:
                self._museum_graph.add_edge(i - 1, i)
        self._museum_graph.add_edge(59, 60)

        # exit
        self._museum_graph.add_node(70, room="exit", prestige=random.uniform(0, 10))
        self._museum_graph.add_edge(69, 70)

        """
        ############## OLD
        div = ceil(80 / len(rooms))
        for i in range(0, 80, 2):
            self._museum_graph.add_node(i, room=rooms[i // div], prestige=random.uniform(0, 10))
            self._museum_graph.add_node(i + 1, room=rooms[(i + 1) // div], prestige=random.uniform(0, 10))
            self._museum_graph.add_edge(i, i + 1)
            if i > 0:
                self._museum_graph.add_edge(i - 1, i)
        
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
        """

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






