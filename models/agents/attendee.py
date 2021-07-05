from __future__ import annotations
import agentpy as ap
import random

class MuseumGuest(ap.Agent):

    def setup(self):
        """ Initialize a new variable at agent creation. """
        self.norm = random.randint(0, 1)  # Linear flow = 0 Wandering = 1
        self.current_room = self.model.start_room
        self.current_painting = self.model.first_painting
        self.boredom_threshold = (random.randint(1,10)) ** -1 #Reciprocal of desired amount of time
        self.crowd_threshold = random.randint(10, 100)
        self.desire_to_leave = random.uniform(0.90, 0.99)

    def update_norms(self):
        """
        Updates the agent's norms. Does so by taking the mean of the
        other agent's normative behaviour with a probability weighting

        Possible extensions - an intermediary or have the linearity be
        a bit more of a spectrum.
        """
        if self.current_room != "exit":
            mean_room_norm = self.model.room_mean_norm(self.current_room)
            seed = random.uniform(0, 1)
            self.norm = int(seed < mean_room_norm)

    def check_if_bored(self) -> bool:
        """
        Checks if the agent is bored of the current painting

        :return: bool
        """
        return random.uniform(0, 1) < self.boredom_threshold

    def check_if_wants_to_leave(self) -> bool:
        """
        Check if the wandering agents wants to leave the museum

        :return: bool
        """
        return random.uniform(0, 1) > self.desire_to_leave

    def move(self):
        """
        Updates the agent's location
        """
        if self.check_if_bored():
            if self.norm == 0:
                self.current_room, self.current_painting = self.linear_move()
            else:
                self.current_room, self.current_painting = self.wander_move()
        self.update_norms()

    def wander_move(self) -> tuple[str, int]:
        """
        Updates the agent's location
        :return: tuple
            A tuple of the agent's new (room, painting)
        """
        if self.check_if_wants_to_leave():
            self.norm = 0
            return self.model.get_last_painting()
        room, painting = self.model.get_random_painting()
        while self.model.get_number_of_painting_viewers(painting) > self.crowd_threshold:
            room, painting = self.model.get_random_painting()
        return (room, painting)

    def linear_move(self) -> tuple[str, int]:
        """
        Updates the agent's location
        :return: tuple
            A tuple of the agent's new (room, painting)
        """
        room, painting = self.model.get_next_painting(self.current_room, self.current_painting)
        while self.model.get_number_of_painting_viewers(painting) > self.crowd_threshold:
            if painting == self.model.last_painting: return (room, painting)
            room, painting = self.model.get_next_painting(room, painting)
        return (room, painting)
