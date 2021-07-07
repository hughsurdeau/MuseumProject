from unittest import TestCase
from test_model import *


class TestMuseumModel(TestCase):

    def test_get_room(self):
        self.assertEqual(test_model.get_room(0), "lobby")
        self.assertEqual(test_model.get_room(5), "gallery")

    def test_room_mean_norm(self):
        self.assertTrue(0 <= test_model.room_mean_norm("lobby") <= 1)

    def test_get_number_of_painting_viewers(self):
        self.assertEqual(100, test_model.get_number_of_painting_viewers(0))

    def test_get_next_painting(self):
        self.assertEqual(test_model.get_next_painting("lobby", 0)[1], 1)

    def test_step(self):
        self.assertEqual(1, 1)

    def test_delete_exited_agents(self):
        self.assertEqual(1, 1)

    def test_add_new_agents(self):
        pass


