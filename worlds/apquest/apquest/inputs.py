from enum import Enum


class Direction(Enum):
    LEFT = (-1, 0)
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)


class Input(Enum):
    LEFT = 1
    UP = 2
    RIGHT = 3
    DOWN = 4
    ACTION = 5
    CONFETTI = 6
