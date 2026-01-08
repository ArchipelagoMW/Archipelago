from Options import Range
from worlds.rac3 import RAC3OPTION


class ArmorUpgrade(Range):
    """
    Determines how many Progressive Armor items are included in the item pool.
    Set to 0 for No Armor.
    Set to 4 for all vanilla Armor to be available.
    Set above 4 to add extra Armor copies into the item pool.
    Collecting more than 4 Progressive Armor items will do nothing.
    """
    display_name = RAC3OPTION.ARMOR_UPGRADE
    range_start = 0
    range_end = 8
    default = 4
