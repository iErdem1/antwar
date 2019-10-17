from ants import *
from abc import *


class Room(ABC):
    @abstractmethod
    def produce_ant(self):
        pass


class WorkerRoom(Room):
    def produce_ant(self):
        return WorkerAnt()


class ForagerRoom(Room):
    def produce_ant(self):
        return ForagerAnt()


class WarriorRoom(Room):
    def produce_ant(self):
        return WarriorAnt()