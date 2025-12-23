from Options import ItemDict
from worlds.rac3 import RAC3OPTION
from worlds.rac3.constants.data.item import trap_data


class TrapWeight(ItemDict):
    """
    Sets the relative weights of trap items in the item pool.
    A higher value increases the likelihood of a particular trap to appear in the item pool.
    This option has no effect when traps are disabled.
    """
    display_name = RAC3OPTION.TRAP_WEIGHT
    min = 0
    max = 100
    valid_keys = trap_data.keys()
    default = {name: 2 for name in trap_data.keys()}
