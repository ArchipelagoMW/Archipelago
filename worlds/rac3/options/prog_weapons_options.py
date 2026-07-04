"""This module contains options for Progressive weapons in the item pool"""

from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class ProgressiveWeapons(Choice):
    """
    Determines whether weapon level-ups are progressive items or not.
    ------------------------------------------------------------------------------------
    Disable:            Weapon leveling and exp functions like in the vanilla game.
    Manual Leveling:    Weapon level caps are increased when a progressive item is collected, weapon exp past the cap is disabled.
    Automatic Leveling: Weapons level-up when its progressive item is collected, weapon exp is disabled.
    ------------------------------------------------------------------------------------
    Note: If Weapon Level Locations are enabled, Automatic Leveling will be forced to Manual Leveling instead.
    """
    display_name = RAC3OPTION.PROGRESSIVE_WEAPONS
    option_disable = 0
    option_manual_leveling = 1
    option_automatic_leveling = 2
    default = 0
