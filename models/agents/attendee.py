import agentpy as ap
import random

class MuseumGuest(ap.Agent):

    def setup(self):
        """ Initialize a new variable at agent creation. """
        self.norm = random.randint(0, 1)  # Linear flow = 0 Wandering = 1
        self.current_room = self.model.start_room
        self.current_painting = self.model.start_painting

    def update_norms(self):
        """
        Updates the agent's norms. Does so by taking the mean of the
        other agent's normative behaviour with a probability weighting

        Possible extensions - an intermediary or have the linearity be
        a bit more of a spectrum.
        :return:
        """
        mean_room_norm = self.model.room_mean_norm(self.current_room)
        seed = random.uniform(0, 1)
        self.norm = int(seed < mean_room_norm)


    def move(self):
        if self.norm == 0:
            self.current_room, self.current_painting = self.linear_move()
        else:
            self.current_room, self.current_painting = self.wander_move()
        if self.current_room != "exit":
            self.update_norms()

    def wander_move(self):
        return self.model.get_random_painting()

    def linear_move(self):
        if True:
            return self.model.get_next_painting(self.current_room, self.current_painting)
        else:
            return (self.current_room, self.current_painting)
