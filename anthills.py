from room import *


class Anthill:
    def __init__(self, anthill_name=None):
        self.anthill_name = anthill_name
        self.room_number = 1
        self.worker_number = 3
        self.food_number = 0
        self.ant_number = 3
        self.init_room = WorkerRoom()
        self.rooms = []
        self.rooms.append(self.init_room)
