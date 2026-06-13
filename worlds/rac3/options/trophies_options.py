"""This module contains options for Trophy locations"""

from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class Trophies(Choice):
    """
    Determines which trophies are locations in the world.
    None: No trophies are locations.
    Collectables: Only the collectable trophies found on various planets are locations.
    All: All special trophies are now also locations.
    
    Note: Skill Master trophy is only included in the pool if all 30 skill points are in the world.
    NG+ trophies are only included in the pool if ngplus_start is enabled, 
    and the Nano Finder trophy is only included if the nanotech limitation is set to include level 200.
    """
    display_name = RAC3OPTION.TROPHIES
    option_none = 0
    option_collectables = 1
    option_all = 2
    default = 1
