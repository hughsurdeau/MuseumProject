"""
A module which determines how many mean people are entering in each 5 minute period.
"""
from scipy.stats import norm
from math import ceil

class TimePiper:
    def __init__(self, day_length=144, people_scale=100):
        self.people_scale = people_scale
        self.day_length = day_length

    def get_mean_visitors(self, time: int) -> int:
        """
        Returns the mean number of visitors at the time.
        Does so by taking the CDF of a normal dist with mean of 1/2 length of day and sigma
        1/4 length of day from time to time+1. This is then multiplied by a constant factor
        (people_scale) to get the mean number of people (which is then rounded up using
        ceil func).
        :param time:   int
            The time of day the visitors are entering at
        :return: int
            Mean number of visitors at time
        """
        mu = self.day_length // 2
        sigma = mu // 2
        cdf = norm.cdf(time + 1, mu, sigma) - norm.cdf(time, mu, sigma)
        return ceil(cdf * self.people_scale)

    def mean_entered_visitors(self, time, mean_stay_duration=50) -> int:
        """
        TODO Get the real mean stay duration from data or set it
        Gets the mean number of visitors entering the museum in the
        period of time the average visitor takes i.e. the expected
        number of visitors in the whole museum at time T
        :param time:
        :return:
        """
        total_visitors = 0
        start = max(time-mean_stay_duration, 0)
        for i in range(start, time):
            total_visitors += self.get_mean_visitors(i)
        return total_visitors
