from enum import Enum

from .generate_math_problem import MathProblemType


class Graphic(Enum):
    EMPTY = 0
    WALL = 1
    BUTTON_NOT_ACTIVATED = 2
    BUTTON_ACTIVATED = 3
    KEY_DOOR = 4
    BUTTON_DOOR = 5
    CHEST = 6
    BUSH = 7
    BREAKABLE_BLOCK = 8

    NORMAL_ENEMY_1_HEALTH = 10
    NORMAL_ENEMY_2_HEALTH = 11

    BOSS_1_HEALTH = 20
    BOSS_2_HEALTH = 21
    BOSS_3_HEALTH = 22
    BOSS_4_HEALTH = 23
    BOSS_5_HEALTH = 24

    PLAYER_DOWN = 30
    PLAYER_UP = 31
    PLAYER_LEFT = 32
    PLAYER_RIGHT = 33

    KEY = 41
    SWORD = 42
    SHIELD = 43
    HAMMER = 44

    HEART = 50
    HALF_HEART = 51
    EMPTY_HEART = 52

    CONFETTI_CANNON = 60

    REMOTE_ITEM = 70

    ITEMS_TEXT = 80

    MATH_TRAP = CONFETTI_CANNON

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

    PLUS = 1100
    MINUS = 1101
    TIMES = 1102
    DIVIDE = 1103

    LETTER_A = 2000
    LETTER_E = 2005
    LETTER_H = 2008
    LETTER_I = 2009
    LETTER_M = 2013
    LETTER_T = 2019

    EQUALS = 2050
    NO = 2060

    UNKNOWN = -1


DIGIT_TO_GRAPHIC = {
    None: Graphic.EMPTY,
    0: Graphic.ZERO,
    1: Graphic.ONE,
    2: Graphic.TWO,
    3: Graphic.THREE,
    4: Graphic.FOUR,
    5: Graphic.FIVE,
    6: Graphic.SIX,
    7: Graphic.SEVEN,
    8: Graphic.EIGHT,
    9: Graphic.NINE,
}

DIGIT_TO_GRAPHIC_ZERO_EMPTY = DIGIT_TO_GRAPHIC.copy()
DIGIT_TO_GRAPHIC_ZERO_EMPTY[0] = Graphic.EMPTY

MATH_PROBLEM_TYPE_TO_GRAPHIC = {
    MathProblemType.PLUS: Graphic.PLUS,
    MathProblemType.MINUS: Graphic.MINUS,
    MathProblemType.TIMES: Graphic.TIMES,
    MathProblemType.DIVIDE: Graphic.DIVIDE,
}
