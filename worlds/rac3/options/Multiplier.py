from Options import Choice
from worlds.rac3 import RAC3OPTION


class BoltAndXPMultiplier(Choice):
    """
    Determines what your bolts and xp will be multiplied by, recommended to go with x6 if you hate grinding,
    x10 if you're looking to do a sync.
    Dev comment: This currently uses the NG+ multiplier so only bolt gain is affected, weapon xp gain is not.
    """
    display_name = RAC3OPTION.BOLT_AND_XP_MULTIPLIER
    option_x1 = 1
    option_x2 = 2
    option_x4 = 4
    option_x6 = 6
    option_x8 = 8
    option_x10 = 10
    default = 1
