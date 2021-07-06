"""
A test model to perform tests on. Sets up scenarios to be tested
"""
from models.museum_model import *

class TestModel(MuseumModel):

    def set_agents_location(self):
        self.agents.select(self.agents.norm == 1)
        self.agents.select(self.agents.norm == 0)

    def set_agents_norms(self, room, new_norm=1):
        """
        Sets the norms of the agent's norms
        :param room:
        :return:
        """
        pass


parameters = {
    'population': 100,
    'steps' : 0,
}
test_model = TestModel(parameters)
test_model.run()
test_model.set_agents_location()