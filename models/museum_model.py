"""
Represent museum as a graph with each node having a graph itself
"""
from __future__ import annotations
import statistics
from models.agents.attendee import *
from models.environments.basic_museum import *

class MuseumModel(ap.Model):

    def setup(self):
        """ Initialize the agents and network of the model. """

        self.start_painting = 0
        self.start_room = self.get_room(self.start_painting)
        self.last_painting = 9 #TODO replace with actual method to get last painting

        # Create agents and network
        self.agents = ap.AgentList(self, self.p.population, MuseumGuest)
        self.network = self.agents.network = ap.Network(self, museum_graph)
        self.network.add_agents(self.agents, self.network.nodes)

    def get_room(self, painting_number: int) -> str:
        """
        Returns the room a given painting is in
        TODO might want to switch this into a normal func
        or as part of a wider rework of the museum_graph
        shit move somewhere else

        :param painting_number: int
            Painting to investigate
        :return: str
            Name of the room the painting is in
        """
        return museum_graph.nodes[painting_number]['room']

    def update(self):
        """
        Record variables after setup and each step.
        TODO: Add recording for the room/artwork
        """
        self.record("wanderers", len(self.agents.select(self.agents.norm == 1)))
        self.record("linear walkers", len(self.agents.select(self.agents.norm == 0)))
        self.record("lobby", len(self.agents.select(self.agents.current_room == "lobby")))
        self.record("gallery", len(self.agents.select(self.agents.current_room == "gallery")))
        self.record("gallery 2", len(self.agents.select(self.agents.current_room == "gallery2")))
        self.record("exit", len(self.agents.select(self.agents.current_room == "exit")))

    def room_mean_norm(self, room: str) -> float:
        """
        Returns the mean norm of all agents in a specified room

        :param room: str
            Name of the room to find the mean norm of
        :return: float
            The mean norm of all agents in the room
        """
        agent_norms = self.agents.select(self.agents.current_room == room).norm
        return statistics.mean(agent_norms)

    def get_number_of_painting_viewers(self, painting: int) -> int:
        """
        Returns the number of agents at a given painting

        :param painting: int
            Painting to get number of agents at
        :return: int
            Number of agents at specified painting
        """
        return len(self.agents.select(self.agents.current_painting == painting))

    def get_next_painting(self, room: str, painting: int) -> tuple[str, int]:
        """
        Returns the next painting in designated painting order

        :param room: str
            Current room
        :param painting: int
            Current painting
        :return: tuple
            Tuple of new (room, painting)
        """
        succesor_paintings = list(museum_graph.successors(painting))
        if not succesor_paintings:
            return (room, painting)
        painting = random.choice(succesor_paintings)
        return (self.get_room(painting), painting)

    def get_last_painting(self) -> tuple[str, int]:
        """
        Returns the last painting in the gallery

        :return: tuple
            Tuple of final (room, painting)
        """
        return (self.get_room(self.last_painting), self.last_painting)

    def get_random_painting(self) -> tuple[str, int]:
        """
        Returns a random painting in the gallery

        :return: tuple
            Tuple of random (room, painting)
        """
        painting = random.choice(list(museum_graph.nodes))
        room = self.get_room(painting)
        return (room, painting)

    def step(self):
        """ Define the models' events per simulation step. """

        # Call move for each agent
        self.agents.move()

    def end(self):
        """ Record evaluation measures at the end of the simulation. """

        # Record final evaluation measures
        pass

parameters = {
    'population': 100,
    'steps' : 100,
}

model = MuseumModel(parameters)
results = model.run()
print(results.variables.MuseumModel)