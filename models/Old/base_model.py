"""
Model of the museum

What do I want to record:
    1 - Number of agents at each room?
    2 - Number of agents at each painting?
    3 - Number of agents conforming to each behavioural standard?


"""
from models.agents.Old.base_agent import BaseAgent
from models.environments.Old.art_museum import *
from models.agents.Old.agent_list import AgentList
from models.environments.Old.exit import Exit

class BaseModel:
    def __init__(self, museum, n_agents=5):
        self.museum = museum
        self.agents = self.create_agent_list(n_agents)
        self.data = []

    def create_agent_list(self, n_agents):
        agent_list = AgentList()
        for i in range(n_agents):
            agent = BaseAgent(i, "jazzy", self)
            agent_list.agents.append(agent)
        return agent_list


    def step(self):
        """Call a method for every agent."""
        self.agents.timestep()

    def update(self, time):
        """ Record a dynamic variable. """
        norm_data = self.agents.get_agent_norms()
        self.data.append((time, norm_data['flow'], norm_data['wander']))

    def run(self, range=50):
        count = 0
        while count < range:
            self.update(count)
            self.step()
            count += 1



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
print(modle.data)
