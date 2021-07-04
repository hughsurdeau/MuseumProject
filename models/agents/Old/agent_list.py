from agents.base_agent import *
from collections import defaultdict

class AgentList:
    def __init__(self, agent_list=[]):
        self.agents = agent_list

    def timestep(self):
        for agent in self.agents:
            agent.timestep()

    def get_agent_norms(self):
        agent_norms = defaultdict(int)
        for agent in self.agents:
            agent_norms[agent.norms] += 1
        return agent_norms

