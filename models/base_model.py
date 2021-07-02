"""
Model of the museum
"""
import agentpy as ap

class BaseModel(ap.Model):

    def setup(self):
        """ Initiate a list of new agents. """
        self.agents = ap.AgentList(self, self.p.agents, MyAgent)

    def step(self):
        """ Call a method for every agent. """
        self.agents.agent_method()

    def update(self):
        """ Record a dynamic variable. """
        self.agents.record('my_attribute')

    def end(self):
        """ Repord an evaluation measure. """
        self.report('my_measure', 1)