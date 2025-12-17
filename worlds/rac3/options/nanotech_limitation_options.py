from Options import Range
from worlds.rac3 import RAC3OPTION

class NanotechLimitation(Range):
    """
    Determines the upper limit of the number of nanotech milestone locations in the multiworld between 11 and 100.
    Nanotech milestone checks start from nanotech level 11 and can go up to nanotech level 100.
    This option has no effect when nanotech_milestones are disabled.
    Example: If set to 40 then you only need to level up to nanotech level 40 as any higher won't count as checks.
    The checks will appear in a way the player specified it in nanotech_milestones.
    """

    display_name = RAC3OPTION.NANOTECH_LIMITATION
    range_start = 11
    range_end = 100
    default = 100