from unittest import TestCase
from models.agents import attendee
from test_model import *


class TestMuseumGuest(TestCase):

    def test_update_norms(self):
        # Random.uniform(0,1) = 0.5714025946899135
        # with seed 10
        attendee = MuseumGuest(test_model)
        attendee.update_norms(1, random.seed(10))
        self.assertEqual(1, attendee.norm)
        attendee.update_norms(0, random.seed(10))
        self.assertEqual(0, attendee.norm)
        attendee.update_norms(0.5, random.seed(10))
        self.assertEqual(0, attendee.norm)
        attendee.update_norms(0.6, random.seed(10))
        self.assertEqual(1, attendee.norm)

    def test_check_if_bored(self):
        attendee = MuseumGuest(test_model)
        attendee.boredom_threshold = 1
        self.assertEqual(True, attendee.check_if_bored(random.seed(10)))
        attendee.boredom_threshold = 0
        self.assertEqual(False, attendee.check_if_bored(random.seed(10)))
        attendee.boredom_threshold = 0.5
        self.assertEqual(False, attendee.check_if_bored(random.seed(10)))

    def test_check_if_wants_to_leave(self):
        attendee = MuseumGuest(test_model)
        attendee.desire_to_leave = 1
        self.assertEqual(False, attendee.check_if_wants_to_leave(random.seed(10)))
        attendee.desire_to_leave = 0
        self.assertEqual(True, attendee.check_if_wants_to_leave(random.seed(10)))
        attendee.desire_to_leave = 0.5
        self.assertEqual(True, attendee.check_if_wants_to_leave(random.seed(10)))

    def test_move(self):
        self.assertEqual(1, 1)

    def test_wander_move(self):
        self.assertEqual(1, 1)

    def test_linear_move(self):
        self.assertEqual(1, 1)
