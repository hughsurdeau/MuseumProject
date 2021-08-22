"""

"""



class CrowdInterpretor:

    def __init__(self):
        pass

    def room_prob(self, prestige, mean_crowd_size, crowd_tolerance):
        return 1 - (1 + prestige * (mean_crowd_size/crowd_tolerance)**2)
