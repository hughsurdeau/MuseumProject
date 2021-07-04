"""
Main TODO:
    1 - Add ability to remove/introduce new attendees at different time periods in the experiment
    3 - Begin introducing dynamics.

Possible approach to decision point on staying in each section:
    Each visitor has a mean time to stay in each one - viewing wise
    Each visitor then has a threshold of how many people on the next one it likes
        if there are too many it skips over to the one after that or until it meets
        one that matches its threshold criteria


"""
from models.museum_model import MuseumModel

