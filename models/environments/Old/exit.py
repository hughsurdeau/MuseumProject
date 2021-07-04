from environments.room import Room

class Exit(Room):

    def __init__(self):
        super().__init__('exit', [-1], "none")

    def get_next_painting(self, current_painting):
        return -1