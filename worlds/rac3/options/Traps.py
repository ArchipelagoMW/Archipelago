from Options import Toggle
from worlds.rac3 import RAC3OPTION

class EnableTraps(Toggle):
    """
    Determines whether trap items are included in the item pool.
    true: Traps will be included in the item pool.
    false: No traps will be included in the item pool.
    """
    display_name = RAC3OPTION.ENABLE_TRAPS