"""
Contains layout of the museum.
"""
from environments.room import Room


class Museum:

    def __init__(self):
        self.rooms = []

    def add_room(self, room):
        self.rooms.append(room)




