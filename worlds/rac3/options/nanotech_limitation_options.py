"""This module contains options for limiting the total number of nanotech level locations"""

from Options import Range
from worlds.rac3.constants.options import RAC3OPTION


class NanotechLimitation(Range):
    """
    Determines the upper limit of the nanotech milestone locations in the multiworld between 11 and 200.
    -----------------------------------------------------------------------------------------------
    Nanotech milestone locations start from nanotech level 11 and can go up to nanotech level 200.
    The locations will appear in steps the player specified in nanotech_milestones.
    This option has no effect when nanotech_milestones are disabled.
    This option has no effect past 100 if ngplus_start is disabled.
    -----------------------------------------------------------------------------------------------
    Example: If set to 40 then you only need to level up to nanotech level 40 as any higher won't count as checks.
    """

    display_name = RAC3OPTION.NANOTECH_LIMITATION
    range_start = 11
    range_end = 200
    default = 100
