import agentpy as ap
import networkx as nx
import random

class Person(ap.Agent):

    def setup(self):
        """ Initialize a new variable at agent creation. """
        self.norm = random.randint(0, 1)  # Linear flow = 0 Wandering = 1
        self.current_room = self.model.start_room
        self.current_painting = self.model.start_painting

    def move(self):
        print("Moving ")
        if self.norm == 0:
            self.current_room, self.current_painting = self.linear_move()
        else:
            self.current_room, self.current_painting = self.wander_move()

    def wander_move(self):
        return self.model.get_random_painting()



    def linear_move(self):
        return self.model.get_next_painting(self.current_room, self.current_painting)
