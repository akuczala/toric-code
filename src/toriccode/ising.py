from enum import Enum


class Ising(Enum):
    UP = 1
    DOWN = 0

    def __str__(self):
        return self.value