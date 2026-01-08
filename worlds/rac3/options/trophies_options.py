from Options import Choice
from worlds.rac3 import RAC3OPTION


class Trophies(Choice):
    """
    Determines which trophies are locations in the world.
    None: No trophies are locations.
    Collectables: Only the collectable trophies found on various planets are locations.
    Every Trophy: All special trophies that do not require NG+ are now also locations.
    Long Term Trophy: Skill Master is only included in the pool if all 30 skill points are in the world.
    """
    display_name = RAC3OPTION.TROPHIES
    option_none = 0
    option_collectables = 1
    option_every_trophy = 2
    default = 1
