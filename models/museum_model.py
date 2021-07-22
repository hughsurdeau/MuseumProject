"""
Represent museum as a graph with each node having a graph itself
"""
from __future__ import annotations
import statistics
import datetime
from models.agents.attendee import *
from models.environments.basic_museum import *
from numpy.random import poisson
from models.agents.route_panner import *

class MuseumModel(ap.Model):

    def setup(self) -> None:
        """ Initialize the agents and network of the model. """
        self.museum_layout = MuseumLayout()
        self.asshole_ratio = 0.45 #Fraction of fellas who are assholes

        self.first_painting = self.museum_layout.first_painting
        self.start_room = self.get_room(self.first_painting)
        self.last_painting = self.museum_layout.last_painting
        self.added = 0
        self.removed = 0

        # Create agents and network
        self.agents = ap.AgentList(self, self.p.population, MuseumGuest)
        self.network = self.agents.network = ap.Network(self, self.museum_layout.museum_graph)
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
        return self.museum_layout.get_room(painting_number)

    def update(self) -> None:
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
        self.record("Viewer Numbers", self.get_painting_viewers_list())
        self.record("Wanderer Numbers", self.get_wanderers_list())

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

    def get_painting_viewers_list(self) -> list:
        """
        Returns a list of the number of all paintings
        :return:
        """
        painting_numbers = []
        for i in range(self.last_painting):
            painting_numbers.append(self.get_number_of_painting_viewers(i))
        return painting_numbers

    def get_wanderers_list(self) -> list:
        wanderer_numbers = []
        for i in range(self.last_painting):
            wanderer_numbers.append(self.get_number_of_wanderer_viewers(i))
        return wanderer_numbers

    def get_number_of_wanderer_viewers(self, painting: int) -> int:
        return len(self.agents.select(self.agents.current_painting == painting).select(self.agents.norm == 1))

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
        succesor_paintings = self.museum_layout.get_successor_list(painting)
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
        painting = self.museum_layout.random_painting()
        room = self.get_room(painting)
        return (room, painting)

    def delete_exited_agents(self) -> None:
        """
        Removes all agents at the exit
        """
        for agent in self.agents.select(self.agents.current_room == "exit"):
            self.removed += 1
            self.agents.remove(agent)

    def add_new_agents(self, mean_new_agents=2) -> None:
        """
        Adds new agents to the simulation
        """
        number_of_new_visitors = poisson(mean_new_agents)
        print(number_of_new_visitors)
        for i in range(number_of_new_visitors):
            self.added += 1
            self.agents += ap.AgentList(self, 1, MuseumGuest)
            self.network.add_agents(self.agents, self.network.nodes)


    def step(self) -> None:
        """ Define the models' events per simulation step. """

        # Call move for each agent
        self.agents.move()
        self.delete_exited_agents()
        self.add_new_agents()

    def end(self) -> None:
        """ Record evaluation measures at the end of the simulation. """

        # Record final evaluation measures
        pass

if __name__ == "__main__":

    parameters = {
        'population': 20,
        'steps': 1000,
    }

    model = MuseumModel(parameters)
    results = model.run()
    print(results.variables.MuseumModel)
    curr_time = str(datetime.datetime.now())
    file_path = "/Users/hughsurdeau/PycharmProjects/MuseumProject/data/csv/linear_museum_45AT.csv"
    results.variables.MuseumModel.to_csv(file_path)