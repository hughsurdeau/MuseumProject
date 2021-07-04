"""
Contains layout of the museum.
"""
from environments.room import Room


class Museum:
    def __init__(self):
        self.rooms = []

    def start_room(self):
        return self.rooms[0]

    def start_painting(self):
        return self.rooms[0].art[0]

    def random_painting(self):
        random_room = random.choice(self.rooms)
        random_painting = random.choice(random_room.art)
        return (random_room, random_painting)

    def add_room(self, room):
        self.rooms.append(room)




