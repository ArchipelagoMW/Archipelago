from Options import Choice
from worlds.rac3 import RAC3OPTION


class SewerCrystals(Choice):
    """
    Determines whether sewer crystals are locations in the world.
    None: No sewer crystals are locations.
    Every 20: Makes every 20 sewer crystals locations starting from 20 sewer crystals collected.
    Every 10: Makes every 10 sewer crystals locations starting from 10 sewer crystals collected.
    Every 5: Makes every 5 sewer crystals locations starting from 5 sewer crystals collected.
    All: All sewer crystals are locations.
    If set to anything other than none, this will also add the "Hit the motherload skillpoint" into the world
    when skill points are set to "every_skill_point".
    """
    display_name = RAC3OPTION.SEWER_CRYSTALS
    option_none = 0
    option_every_20 = 1
    option_every_10 = 2
    option_every_5 = 3
    option_all = 4
    default = 0
