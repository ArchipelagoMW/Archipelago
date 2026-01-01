from Options import Range
from worlds.rac3 import RAC3OPTION


class ArmorUpgrade(Range):
    """
    Determines how many Progressive Armor items are included in the item pool.
    If you wish to play without armor upgrades set this to 0
    If you wish to play with all vanilla armor upgrades in the pool set this to 4
    Anything above 4 will add extra copies of this item so the player has more chance to get an armor upgrade.
    Collecting more than 4 Progressive Armor items will do nothing.
    """
    display_name = RAC3OPTION.ARMOR_UPGRADE
    range_start = 0
    range_end = 8
    default = 4
