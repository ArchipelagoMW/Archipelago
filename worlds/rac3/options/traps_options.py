from Options import Choice
from worlds.rac3 import RAC3OPTION


class EnableTraps(Choice):
    """
    Determines whether trap items are included in the item pool.
    Disabled: No traps will be included in the item pool.
    Enabled: Traps will be included in the item pool.
    """
    display_name = RAC3OPTION.ENABLE_TRAPS
    option_disabled = 0
    option_enabled = 1
    default = 0
