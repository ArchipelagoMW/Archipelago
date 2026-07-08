"""This module defines the possible pause states that can be read from memory"""
from enum import IntEnum


class RAC3PAUSESTATE(IntEnum):
    """Context for how the game has been paused"""
    INVALID = -1
    UNPAUSED = 0
    CUTSCENE = 2
    PAUSED = 3
    QUICK_SELECT = 4
    VENDOR = 5
    PLANET_CHANGE = 6
    MINIGAME = 7
    WEAPON_UPGRADE = 8
    CREDITS = 9
