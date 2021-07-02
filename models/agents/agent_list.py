from agents.base_agent import *

class AgentList:

    def __init__(self, agent_list=[]):
        self.agents = agent_list

    def timestep(self):
        for agent in self.agents:
            agent.timestep()

