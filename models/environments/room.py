"""
Contains the room behaviour
"""


class Room:
    def __init__(self, name, art, style):
        self.name = name
        self.prev = []
        self.next = []
        self.art = art
        self.style = style

    def __repr__(self):
        return self.name

    def add_prev_room(self, new_room):
        self.prev.append(new_room)

    def add_next_room(self, new_room):
        self.next.append(new_room)

    def get_next_painting(self, current_painting):
        curr_index = self.art.index(current_painting)
        return -1 if curr_index == (len(self.art)-1) else self.art[curr_index+1]

