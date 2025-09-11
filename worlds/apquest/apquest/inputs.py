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

    ZERO = 1000
    ONE = 1001
    TWO = 1002
    THREE = 1003
    FOUR = 1004
    FIVE = 1005
    SIX = 1006
    SEVEN = 1007
    EIGHT = 1008
    NINE = 1009

    BACKSPACE = 2000


DIGIT_INPUTS_TO_DIGITS = {
    Input.ZERO: 0,
    Input.ONE: 1,
    Input.TWO: 2,
    Input.THREE: 3,
    Input.FOUR: 4,
    Input.FIVE: 5,
    Input.SIX: 6,
    Input.SEVEN: 7,
    Input.EIGHT: 8,
    Input.NINE: 9,
}
