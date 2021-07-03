"""
Represent museum as a graph with each node having a graph itself
"""
import agentpy as ap
import networkx as nx
import random
from attendee import *

museum_graph = nx.DiGraph()
museum_graph.add_node(1, art=(0, 1, 2))
museum_graph.add_node(2, art=(3, 4, 5))
museum_graph.add_node(3, art=(6, 7, 8))
museum_graph.add_edge(1, 2)
museum_graph.add_edge(2, 3)


class MuseumModel(ap.Model):

    def setup(self):
        """ Initialize the agents and network of the model. """

        self.start_painting = museum_graph.nodes[1]['art'][0]
        self.start_room = 1

        # Create agents and network
        self.agents = ap.AgentList(self, self.p.population, Person)

        self.network = self.agents.network = ap.Network(self, museum_graph)

        self.network.add_agents(self.agents, self.network.nodes)

        # Infect a random share of the population
        I0 = int(self.p.initial_infection_share * self.p.population)
        self.agents.random(I0).condition = 1

    def update(self):
        """ Record variables after setup and each step. """
        pass
        """
        # Record share of agents with each condition
        for i, c in enumerate(('S', 'I', 'R')):
            n_agents = len(self.agents.select(self.agents.condition == i))
            self[c] = n_agents / self.p.population
            self.record(c)

        # Stop simulation if disease is gone
        if self.I == 0:
            self.stop()
        """

    def get_next_painting(self, room, painting):
        """
        Returns the next painting in orderly procession
        :param room:
        :param painting:
        :return:
        """
        index = museum_graph.nodes[room]['art'].index(painting)
        if index == (len(museum_graph.nodes[room]['art']) - 1):
            if not museum_graph.successors(self.start_room): return (room, painting)
            room = random.choice(list(museum_graph.successors(self.start_room)))
            painting = museum_graph.nodes[room]['art'][0]
        else:
            painting = museum_graph.nodes[room]['art'][index+1]
        return (room, painting)

    def get_random_painting(self):
        room = random.choice(list(museum_graph.nodes))
        painting = random.choice(museum_graph.nodes[room]['art'])
        return (room, painting)

    def step(self):
        """ Define the models' events per simulation step. """

        # Call move for each agent
        self.agents.move()

    def end(self):
        """ Record evaluation measures at the end of the simulation. """

        # Record final evaluation measures
        #self.report('Total share infected', self.I + self.R)
        #self.report('Peak share infected', max(self.log['I']))
        pass

parameters = {
    'population': 10,
    'infection_chance': 0.3,
    'recovery_chance': 0.1,
    'initial_infection_share': 0.1,
    'number_of_neighbors': 2,
    'network_randomness': 0.5
}

model = MuseumModel(parameters)
results = model.run()
print(results)