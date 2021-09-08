from __future__ import annotations
import agentpy as ap
import random
from prism_interpretors.basic_wanderer_interpretor import *

class MuseumGuest(ap.Agent):

    def setup(self):
        """ Initialize a new variable at agent creation. """
        self.norm = self.assign_initial_norm() #Linear = 0, wandering = 1
        self.internalised_norm = self.norm #Linear = 0, wandering = 1
        self._current_room = self.model.start_room
        self.current_painting = self.model.first_painting
        self.assign_style_preference(["classic", "abstract", "modern", "romantic", "sculpture"])
        self._boredom_threshold = guassian_dist(8, 2, 2, 12) ** -1 #Reciprocal of desired amount of time
        self.crowd_threshold = random.randint(1, 15) #Crowd tolerance
        self._desire_to_leave = guassian_dist(250, 25, 100, 400)
        self.prism_decision_making = self.model.prism_integration
        self.adhering_reward = random.uniform(0, 8) #Reward an agent gets from adhering to the norm
        self.volume_norm = self.assign_initial_volume() # 0=Silent, 1=Quiet talking, 2=Loud talking

    def assign_initial_norm(self, seed=random.seed()):
        return int(self.model.asshole_ratio > random.uniform(0, 1))

    def assign_initial_volume(self, seed=random.seed()):
        return random.randint(0, 2)

    def assign_style_preference(self, style_options):
        self.preference = random.choice(style_options)
        style_options.remove(self.preference)
        self.dislike = random.choice(style_options)

    @property
    def desire_to_leave(self):
        return self._desire_to_leave

    @desire_to_leave.setter
    def desire_to_leave(self, new_desire):
        if (0 <= new_desire and new_desire <= 1):
            self._desire_to_leave = new_desire

    @property
    def current_room(self):
        return self._current_room

    @current_room.setter
    def current_room(self, new_room):
        self._current_room = new_room

    @property
    def boredom_threshold(self):
        return self._boredom_threshold

    @boredom_threshold.setter
    def boredom_threshold(self, new_threshold):
        if (0 <= new_threshold and new_threshold <= 1):
            self._boredom_threshold = new_threshold

    def get_room_crowd_ratio(self):
        crowd_size = self.model.get_number_of_viewers(self.current_room) / 10 #10 paintings per room
        crowd_tolerance = self.crowd_threshold
        return (crowd_size / crowd_tolerance) ** 2

    def get_prism_left_room_prob(self):
        """
        Returns the probability of an agent choosing the left room when deciding
        between two pathways.
        :return:
        """
        crowd_ratio = self.get_room_crowd_ratio()
        print(self.current_room)
        print(self.current_room, crowd_ratio)
        return get_room_probability(self.current_room, crowd_ratio)


    def update_norms(self, room_mean_norm: float, seed=random.seed()) -> None:
        """
        Updates the agent's norms. Does so by taking the mean of the
        other agent's normative behaviour with a probability weighting

        Possible extensions - an intermediary or have the linearity be
        a bit more of a spectrum.
        """
        if self.current_room != "exit":
            seed = random.uniform(0, 1)
            self.internalised_norm = int(seed < room_mean_norm)

    def check_if_bored(self, seed=random.seed()) -> bool:
        """
        Checks if the agent is bored of the current painting

        :return: bool
        """
        #Check if the agent still considers the painting worth staying at
        current_painting_score = self.get_painting_enjoyment(self.current_painting)
        return True if (current_painting_score < 0) else (random.uniform(0, 1) < self.boredom_threshold)

    def check_if_wants_to_leave(self, seed=random.seed()) -> bool:
        """
        Check if the wandering agents wants to leave the museum

        :return: bool
        """
        return random.uniform(0, 1) > self.desire_to_leave

    def move(self, seed=random.seed()) -> None:
        """
        Updates the agent's location
        """
        self.normative_decision_making()  # Update acting norm
        if self.check_if_bored():
            if self.norm == 0:
                self.current_room, self.current_painting = self.linear_move()
            else:
                self.current_room, self.current_painting = self.wander_move(seed)

        room_norm = self.model.room_mean_norm(self.current_room)
        self.update_norms(room_norm) #Update internalised norm

    def wander_move(self, seed=random.seed()) -> tuple[str, int]:
        """
        Updates the agent's location
        :return: tuple
            A tuple of the agent's new (room, painting)
        """
        if self.check_if_wants_to_leave():
            self.norm = 0
            return self.model.get_last_painting()
        possible_paintings = [self.model.get_random_painting() for i in range(3)] #Choose from 3 paintings
        curr_score = -99 #Low score to ensure at least one painting will beat it
        for curr_room, curr_painting in possible_paintings:
            if self.get_painting_enjoyment(curr_painting) > curr_score:
                curr_score = self.get_painting_enjoyment(curr_painting)
                room, painting = curr_room, curr_painting
        return (room, painting)

    def linear_move(self) -> tuple[str, int]:
        """
        Updates the agent's location
        :return: tuple
            A tuple of the agent's new (room, painting)
        """
        painting = self.get_next_step(self.current_room, self.current_painting)
        room = self.model.museum_layout.get_room(painting)
        return (room, painting)

    def get_painting_enjoyment(self, painting: int) -> int:
        """
        Returns a score for the agent's enjoyment of the painting
        :param painting: int
            Painting ID to investigate
        :return: int
            The enjoyment score of the painting for the agent
        """
        prestige = self.model.museum_layout.get_prestige(painting)
        room = self.model.museum_layout.get_room(painting)
        style = self.model.museum_layout.get_style(room)
        crowd_size = self.model.get_number_of_painting_viewers(painting)

        score = 5 if style == self.preference else 0
        score -= -5 * (style == self.dislike)
        score += prestige
        score += (self.crowd_threshold - crowd_size)
        return score

    def normative_decision_making(self):
        """
        Agent decides on movement mode based on internalised norms + circumstances

        :return:
        """
        adhering_score = self.internalised_norm * (self.model.wandering_reward - self.model.wandering_cost) + self.adhering_reward
        breaking_score = (1 - self.internalised_norm) * (self.model.wandering_reward - self.model.wandering_cost)
        if breaking_score >= adhering_score:
            self.norm = (1 - self.internalised_norm) # Flips norm


    def get_next_step(self, current_room: str, current_painting: int) -> int:
        """
        Returns the next acceptable painting for the agent. Covers three cases:
            1 - Current painting has one successor paintings. If the enjoyment rating
                is positive, return it. Else, continue to paintings' successor node
            2 - Current painting has no successor paintings. Exit
            3 - Current painting has numerous successor paintings. Each possible
                route is investigated and the one returning the maximum overall
                score is returned
        :param current_room: str
            Current room the agent is in
        :param current_painting: int
            Current painting the agent is looking at
        :return: int
            The next acceptable painting for the agent
        """
        successors = self.model.museum_layout.get_successor_list(current_painting)
        if len(successors) == 1: #when there is only 1 neighbour
            next_room, next_painting = self.model.get_next_painting(current_room, current_painting)
            if self.get_painting_enjoyment(next_painting) > 0:
                return next_painting #TODO should this be changed to next painting?
            else:
                return self.get_next_step(next_room, next_painting)
        if len(successors) == 0:
            return current_painting
        if self.prism_decision_making:
            left_prob = self.get_prism_left_room_prob()
            if random.uniform(0,1) < left_prob:
                return successors[0]
            else:
                return successors[-1]
        else:
            score, next_painting = self.route_evaluator(current_painting)
            return next_painting

    def route_evaluator(self, painting: int) -> tuple[int, str]:
        """
        Evaluates the score of different possible routes
        :param succesors:
        :return:
        """
        successors = self.model.museum_layout.get_successor_list(painting)
        curr_score = self.get_painting_enjoyment(painting)
        if not successors:
            return max(0, curr_score), painting
        successor_scores = []
        sucessor_paintings = {}
        for painting_option in successors:
            curr_score, curr_best = self.route_evaluator(painting_option)
            successor_scores.append(curr_score)
            sucessor_paintings[curr_score] = painting_option
        return (max(curr_score, 0) + max(successor_scores), sucessor_paintings[max(successor_scores)])
