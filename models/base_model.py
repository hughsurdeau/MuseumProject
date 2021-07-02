"""
Model of the museum

What do I want to record:
    1 - Number of agents at each room?
    2 - Number of agents at each painting?
    3 - Number of agents conforming to each behavioural standard?

TODO
    1 - Fix up the museum class for usability
    2 - fix up agent list
"""
import agentpy as ap
from agents.base_agent import BaseAgent
from environments.art_museum import *
from agents.agent_list import AgentList

class BaseModel:
    def __init__(self, rooms,n_agents=5):
        self.rooms = rooms
        self.agents = self.create_agent_list(n_agents)
        self.remaining = 50

    def create_agent_list(self, n_agents):
        agent_list = AgentList()
        for i in range(n_agents):
            agent = BaseAgent(i, "jazzy", self)
            agent_list.agents.append(agent)
        return agent_list


    def step(self):
        """Call a method for every agent."""
        self.agents.timestep()

    def update(self):
        """ Record a dynamic variable. """
        self.agents.record('my_attribute')



ArtMuseum = Museum()
room1 = Room("lobby", [1,2,3], "modern")
room2 = Room("gallery", [4,5,6], "classic")
room3 = Room("end", [7,8,9], "funky")


modle = BaseModel([room1, room2, room3])
modle.step()
