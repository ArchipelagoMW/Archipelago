"""This module contains options for Weapon Level locations"""

from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class WeaponLevels(Choice):
    """
    Determines whether weapon levels should be locations or not.
    **Disable**: No weapon levels are locations.
    **V5**: Only V5 weapon levels are locations.
    **All**: All weapon levels are locations (including V6, V7, V8 if ngplus_items are enabled).

    Note: If progressive weapons are enabled, leveling will be forced to manual leveling instead of automatic leveling.
    """
    display_name = RAC3OPTION.WEAPON_LEVEL_LOCATIONS
    option_disable = 0
    option_v5 = 1
    option_all = 2
    default = 1
