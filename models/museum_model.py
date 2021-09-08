"""
Represent museum as a graph with each node having a graph itself
"""
from __future__ import annotations
import statistics
import datetime
from models.agents.attendee import *
from models.environments.basic_museum import *
from numpy.random import poisson
from models.time_piper import TimePiper
from models.prism_interpretors.basic_wanderer_interpretor import *

day_length = 1000 # Length of day (in time steps)
number_of_days = 1 # Number of days to simulates

class MuseumModel(ap.Model):

    def setup(self, prism_integrated=False, wanderer_ratio=0.5) -> None:
        """ Initialize the agents and network of the model. """
        self.museum_layout = MuseumLayout()
        self.asshole_ratio = wanderer_ratio #Fraction of fellas who are assholes
        self.time_piper = TimePiper(day_length=day_length)
        self.day_length = day_length
        self.current_time = 0
        self.wandering_cost = 2
        self.wandering_reward = 4 # Mean prestige of museum paintings i.e. expected reward
        self._prism_integration = prism_integrated

        self.first_painting = self.museum_layout.first_painting
        self.start_room = self.get_room(self.first_painting)
        self.last_painting = self.museum_layout.last_painting
        self.added = 0
        self.removed = 0
        self.total_removed = 0

        # Create agents and network
        self.agents = ap.AgentList(self, self.p.population, MuseumGuest)
        self.network = self.agents.network = ap.Network(self, self.museum_layout.museum_graph)
        self.network.add_agents(self.agents, self.network.nodes)

    @property
    def prism_integration(self):
        return self._prism_integration

    @prism_integration.setter
    def boredom_threshold(self, new_prism_integration: bool):
        self._prism_integration = new_prism_integration

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
        self.record("left_gallery", len(self.agents.select(self.agents.current_room == "left_gallery")))
        self.record("right_gallery", len(self.agents.select(self.agents.current_room == "right_gallery")))
        self.record("left_gallery1", len(self.agents.select(self.agents.current_room == "left_gallery1")))
        self.record("left_gallery2", len(self.agents.select(self.agents.current_room == "left_gallery2")))
        self.record("right_gallery1", len(self.agents.select(self.agents.current_room == "right_gallery1")))
        self.record("right_gallery2", len(self.agents.select(self.agents.current_room == "right_gallery2")))
        self.record("exit", len(self.agents.select(self.agents.current_room == "exit")))
        self.record("removed", self.removed)
        self.record("total_removed", self.total_removed)
        self.record("total_added", self.added)
        self.record("Viewer Numbers", self.get_painting_viewers_list())
        self.record("Wanderer Numbers", self.get_wanderers_list())

    def room_mean_norm(self, room: str) -> float:
        """
        Returns the mean norm of all agents in a specified room
        Note that w has to be between 1 and 4 (inclusive)

        :param room: str
            Name of the room to find the mean norm of
        :return: float
            The mean norm of all agents in the room
        """
        agent_norms = self.agents.select(self.agents.current_room == room).norm
        if self.prism_integration:
            s = ceil(statistics.mean(agent_norms * 2))
            w = max(min(ceil(self.get_room_surpluss_viewers(room)*2), 4), 1) # x5 to fit into categories I used
            return get_wanderer_probability(w, s)
        else:
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

    def delete_all_agents(self) -> None:
        """
        Removes all agents from the museum
        """
        for agent in self.agents:
            self.agents.remove(agent)

    def delete_exited_agents(self) -> None:
        """
        Removes all agents at the exit
        """
        self.removed = 0
        for agent in self.agents.select(self.agents.current_room == "exit"):
            self.removed += 1
            self.total_removed += 1
            self.agents.remove(agent)

    def add_new_agents(self) -> None:
        """
        Adds new agents to the simulation
        """
        mean_new_agents = self.time_piper.get_mean_visitors(self.current_time)
        number_of_new_visitors = poisson(mean_new_agents)
        print("\n%i new agents on day %i " % (number_of_new_visitors,self.current_time))
        for i in range(number_of_new_visitors):
            self.added += 1
            self.agents += ap.AgentList(self, 1, MuseumGuest)
            self.network.add_agents(self.agents, self.network.nodes)

    def get_number_of_viewers(self, room: str) -> int:
        """
        Returns the total number of viewers in a given room
        :param room:
        :return:
        """
        return len(self.agents.select(self.agents.current_room == room))

    def get_expected_viewers(self) -> int:
        """
        Returns the expected number of viewers in each room
        at the given time of day.

        Expect that the lobby will have a surpluss of people
        Perhaps ~30% of total for now (to fix)
        :return:
        """
        number_of_rooms = len(self.museum_layout.rooms)
        return self.time_piper.mean_entered_visitors(self.current_time) / number_of_rooms

    def get_room_surpluss_viewers(self, room: str) -> float:
        """
        Gets the relative surpluss of viewers in a room
        Expressed as a fraction of expected vs actual
        :param room:
        :return:
        """
        curr_viewers = self.get_number_of_viewers(room)
        expected_viewers = max(self.get_expected_viewers(), 1)
        return (curr_viewers / expected_viewers)


    def step(self) -> None:
        """ Define the models' events per simulation step. """

        # Call move for each agent
        self.agents.move()
        self.delete_exited_agents()
        self.add_new_agents()

        if self.current_time == self.day_length:
            self.delete_all_agents()
            self.current_time = 0
        else:
            self.current_time += 1

    def end(self) -> None:
        """ Record evaluation measures at the end of the simulation. """

        # Record final evaluation measures
        pass