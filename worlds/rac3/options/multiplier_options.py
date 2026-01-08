from Options import Choice
from worlds.rac3 import RAC3OPTION


class BoltAndXPMultiplier(Choice):
    """
    Determines what your base bolt and xp multiplier will be set to,
    recommended to use x8 if you're looking to do a sync.
    """
    display_name = RAC3OPTION.BOLT_AND_XP_MULTIPLIER
    option_x1 = 0
    option_x2 = 1
    option_x4 = 2
    option_x8 = 3
    option_x16 = 4
    default = 2
