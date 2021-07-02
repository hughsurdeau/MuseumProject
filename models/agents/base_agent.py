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
import numpy as np
import random

class BaseAgent:

    def __init__(self, id, preference, model, details=True):
        self.id = id
        self.preference = preference
        self.model = model

        self.norms = self.initialise_norms()
        self.path = self.initialise_painting_sequence()
        self.current_room = self.model.museum.start_room()
        self.current_art = self.model.museum.start_painting()
        self.details = details

    def timestep(self):
        """
        Timesteps the agent based on certain behaviour.
        Need to add in stuff that accounts for
        :return:
        """
        if self.norms == "wander":
            self.wandering_timestep()
        else:
            self.flow_timestep()
        if self.details:
            print("Agent " + str(self.id) + " currently in room " +
                  self.current_room.name + " looking at painting " +
                  str(self.current_art))


    def initialise_painting_sequence(self):
        pass

    def update_painting_sequence(self):
        pass

    def initialise_norms(self):
        """
        Initialises the norms of the agent.
        For now - 50/50 chance of flow or wander
        :return:
        """
        return "wander" if np.random.randint(0, 100) < 50 else "flow"

    def update_norms(self):
        pass

    def wandering_timestep(self):
        self.current_room = random.choice(self.model.museum.rooms)
        self.current_art = random.choice(self.current_room.art)

    def flow_timestep(self):
        new_art = self.current_room.get_next_painting(self.current_art)
        if new_art != -1:
            self.current_art = new_art
        else:
            if len(self.current_room.next)>0:
                self.current_room = random.choice(self.current_room.next)
                self.current_art = self.current_room.art[0]

