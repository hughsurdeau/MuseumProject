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
from agents.base_agent import BaseAgent
from environments.art_museum import *
from agents.agent_list import AgentList
from environments.exit import Exit

class BaseModel:
    def __init__(self, museum, n_agents=5):
        self.museum = museum
        self.agents = self.create_agent_list(n_agents)

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

    def run(self, range=50):
        while range > 0:
            self.step()
            range -= 1



ArtMuseum = Museum()
room1 = Room("lobby", [1,2,3], "modern")
room2 = Room("gallery", [4,5,6], "classic")
room3 = Room("end", [7,8,9], "funky")
room1.add_next_room(room2)
room2.add_next_room(room3)
room2.add_prev_room(room1)
room3.add_prev_room(room2)
exit = Exit()
room3.add_next_room(exit)
exit.add_prev_room(room3)

ArtMuseum.add_room(room1)
ArtMuseum.add_room(room2)
ArtMuseum.add_room(room3)
ArtMuseum.add_room(exit)

modle = BaseModel(ArtMuseum)
modle.run()
print(modle.agents.get_agent_norms())
