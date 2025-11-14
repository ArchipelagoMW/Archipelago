from constants.data.Rac3ItemData import trap_data
from Options import ItemDict
from worlds.rac3 import RAC3OPTION

class TrapWeight(ItemDict):
    """
    Sets the relative weight of trap items in the item pool.
    A higher value increases the likelihood of traps appearing.
    Has no effect if traps are disabled.
    """
    display_name = RAC3OPTION.TRAP_WEIGHT
    min = 0
    max = 100
    valid_keys = trap_data.keys()
    default = {name: 2 for name in trap_data.keys()}