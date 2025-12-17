from Options import Range
from worlds.rac3 import RAC3OPTION

class SewerLimitation(Range):
    """
    Determines the upper limit of the number of Sewer Crystal locations in the multiworld between 1 and 99.
    This option has no effect when sewer_crystals are disabled.
    Example: If set to 40 then you only need to collect up to 40 sewer crystals. Any more won't count as checks.
    The checks will appear in a way the player specified it in sewer_crystals.
    Setting this to 100 will also add "Hit the motherload" into the pool if skill_points are set to "every_skill_point".
    """

    display_name = RAC3OPTION.SEWER_LIMITATION
    range_start = 1
    range_end = 100
    default = 20