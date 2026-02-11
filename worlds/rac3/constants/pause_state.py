"""This module defines the possible pause states that can be read from memory"""


class RAC3PAUSESTATE:
    """Context for how the game has been paused"""
    UNPAUSED = 0
    CUTSCENE = 2
    PAUSED = 3
    QUICK_SELECT = 4
    VENDOR = 5
    PLANET_CHANGE = 6
    MINIGAME = 7
    WEAPON_UPGRADE = 8