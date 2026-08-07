"""This module contains options for the Progressive OmniWrench in the item pool"""

from Options import Range
from worlds.rac3.constants.options import RAC3OPTION


class ProgressiveWrench(Range):
    """
    Determines how many Progressive Armor items are included in the item pool.
    ------------------------------------------------------------------------------------
    Set to 0 for No Wrench Upgrades.
    Set to 7 for all OmniWrench upgrades to be available.
    Set above 7 to add extra OmniWrench Upgrades copies into the item pool.
    Collecting more than 7 Progressive OmniWrench items will do nothing.
    ------------------------------------------------------------------------------------
    Note: Experimental feature.
    """
    display_name = RAC3OPTION.PROGRESSIVE_WRENCH
    range_start = 0
    range_end = 9
    default = 7
