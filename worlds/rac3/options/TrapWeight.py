from Options import Range
from worlds.rac3 import RAC3OPTION

class TrapWeight(Range):
    """
    Sets the relative weight of trap items in the item pool.
    A higher value increases the likelihood of traps appearing.
    Has no effect if traps are disabled.
    """
    display_name = RAC3OPTION.TRAP_WEIGHT
    range_start = 0
    range_end = 100
    default = 2