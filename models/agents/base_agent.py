"""
The base agent of the museum simulation. Has full access to all information
and makes decisions both normative and not

Attributes that the model needs to have:
    1 - Preferences of art
    2 - Internatilised norms
    3 - Information already received? Not sure

Behaviours that this agent needs to take:
    1 - Determine which painting to go to next (sequencing of paingint)
    2 - Make decisions based on norms and input information
    3 - Determine if they should adopt norms
"""
import agentpy as ap
import numpy as np

class BaseAgent(ap.Agent):

    def setup(self, preference):
        self.preference = preference
        self.norms = self.initialise_norms()
        self.path = self.initialise_painting_sequence()

    def timestep(self):
        pass


    def initialise_painting_sequence(self):
        pass

    def update_painting_sequence(self):
        pass

    def initialise_norms(self):
        pass

    def update_norms(self):
        pass



