"""This module contains options for limiting the total number of sewer crystal trade locations"""

from Options import Range
from worlds.rac3.constants.options import RAC3OPTION


class SewerLimitation(Range):
    """
    Determines the upper limit of the Sewer Crystal locations in the multiworld between 1 and 101.
    -----------------------------------------------------------------------------------------------
    This option has no effect when sewer_crystals are disabled.
    The locations will appear in steps the player specified in sewer_crystals.
    Setting this to 100 or above will also add "Hit the motherload" into the pool if skill_points are set to "all".
    -----------------------------------------------------------------------------------------------
    Example: If set to 40 then you only need to collect up to 40 sewer crystals. Any more won't count as checks.
    """

    display_name = RAC3OPTION.SEWER_LIMITATION
    range_start = 1
    range_end = 101
    default = 20
