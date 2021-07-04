"""
Represent museum as a graph with each node having a graph itself
"""
import statistics
from models.agents.attendee import *
from models.environments.basic_museum import *

class MuseumModel(ap.Model):

    def setup(self):
        """ Initialize the agents and network of the model. """

        self.start_painting = 0
        self.start_room = self.get_room(self.start_painting)

        # Create agents and network
        self.agents = ap.AgentList(self, self.p.population, MuseumGuest)
        self.network = self.agents.network = ap.Network(self, museum_graph)
        self.network.add_agents(self.agents, self.network.nodes)

    def get_room(self, painting_number):
        return museum_graph.nodes[painting_number]['room']

    def update(self):
        """ Record variables after setup and each step.
        TODO: Add recording for the room/artwork
        """
        self.record("wanderers", len(self.agents.select(self.agents.norm == 1)))
        self.record("linear walkers", len(self.agents.select(self.agents.norm == 0)))
        self.record("lobby", len(self.agents.select(self.agents.current_room == "lobby")))
        self.record("gallery", len(self.agents.select(self.agents.current_room == "gallery")))
        self.record("gallery 2", len(self.agents.select(self.agents.current_room == "gallery2")))
        self.record("exit", len(self.agents.select(self.agents.current_room == "exit")))

    def room_mean_norm(self, room):
        """Get the mean norm (i.e. wanderer or flow) for a given room"""
        agent_norms = self.agents.select(self.agents.current_room == room).norm
        return statistics.mean(agent_norms)



    def get_next_painting(self, room, painting):
        """
        Returns the next painting in designated painting order
        :param room:
        :param painting:
        :return:
        """
        succesor_paintings = list(museum_graph.successors(painting))
        if not succesor_paintings: return (room, painting)
        painting = random.choice(succesor_paintings)
        return (self.get_room(painting), painting)

    def get_random_painting(self):
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