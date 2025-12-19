from Options import Choice
from worlds.rac3 import RAC3OPTION


class BoltAndXPMultiplier(Choice):
    """
    Determines what your bolts and xp will be multiplied by, recommended to go with x8 if you hate grinding,
    x16 if you're looking to do a sync.
    """
    display_name = RAC3OPTION.BOLT_AND_XP_MULTIPLIER
    option_x1 = 0
    option_x2 = 1
    option_x4 = 2
    option_x8 = 3
    option_x16 = 4
    default = 0
