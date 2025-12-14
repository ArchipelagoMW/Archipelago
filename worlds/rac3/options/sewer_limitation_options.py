from Options import Range
from worlds.rac3 import RAC3OPTION

class SewerLimitation(Range):
    """
    How many sewer crystal collected should appear in the multiworld as checks. This option is only enabled when sewer_crystals
    option is also enabled.
    Example: If set to 40 then the first 40 sewer crystal traded in counts as a check in a way the player specified it in
    sewer_crystals.
    """

    display_name = RAC3OPTION.SEWER_LIMITATION
    range_start = 1
    range_end = 99 #or 101, currently placeholder number
    default = 20