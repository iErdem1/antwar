from random import randint
from abc import *


class Ant(ABC):
    def __init__(self, ant_type):
        self.ant_type = ant_type
        self.ant_id = ""
        self.hill_id = ""

    @abstractmethod
    def gain_attributes(self):
        pass


class WorkerAnt(Ant):
    def __init__(self):
        super().__init__("worker")
        self.base_cell_row = None
        self.base_cell_col = None
        self.current_cell_row = None
        self.current_cell_col = None
        self.pace = 0

    def gain_attributes(self):
        pass


class ForagerAnt(Ant):
    def __init__(self):
        super().__init__("forager")
        self.base_cell_row = None
        self.base_cell_col = None
        self.current_cell_row = None
        self.current_cell_col = None
        self.pace = 1
        self.collected_food = 0
        self.directions = []
        self.reverse_dir = []

    def gain_attributes(self):
            pass


class WarriorAnt(Ant):
    def __init__(self):
        super().__init__("warrior")
        self.base_cell_row = None
        self.base_cell_col = None
        self.current_cell_row = None
        self.current_cell_col = None
        self.pace = 1
        self.defence = randint(80, 100)
        self.hit = randint(50, 90)
        self.directions = []
        self.reverse_dir = []

    def gain_attributes(self):
        self.hit += 10
        self.defence += 10