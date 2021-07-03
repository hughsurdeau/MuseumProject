import agentpy as ap
import networkx as nx
import random

class Person(ap.Agent):

    def setup(self):
        """ Initialize a new variable at agent creation. """
        self.norm = random.randint(0, 1)  # Linear flow = 0 Wandering = 1
        self.current_painting = self.model.start_painting

    def move(self):
        pass