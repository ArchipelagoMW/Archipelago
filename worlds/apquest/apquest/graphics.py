from enum import Enum


class Graphic(Enum):
    EMPTY = 0
    WALL = 1
    BUTTON_NOT_ACTIVATED = 2
    BUTTON_ACTIVATED = 3
    KEY_DOOR = 4
    BUTTON_DOOR = 5
    CHEST = 6
    BUSH = 7

    NORMAL_ENEMY = 10
    BOSS = 11

    PLAYER_DOWN = 20
    PLAYER_UP = 21
    PLAYER_LEFT = 22
    PLAYER_RIGHT = 23

    UNKNOWN = -1

    KEY = 31
    SWORD = 32
    SHIELD = 33
    HEALTH_UPGRADE = 34
