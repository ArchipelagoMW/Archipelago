from Options import ItemDict
from worlds.rac3 import RAC3OPTION
from worlds.rac3.constants.data.item import default_starting_weapons


class StartingWeapons(ItemDict):
    """
    Determines which weapons you will be starting the game with,
    provide a count of the weapons you want to be picked between,
    two are selected to be placed on Veldin.
    """
    display_name = RAC3OPTION.STARTING_WEAPONS
    min = 0
    max = 5
    default = default_starting_weapons
    valid_keys = default_starting_weapons.keys()
