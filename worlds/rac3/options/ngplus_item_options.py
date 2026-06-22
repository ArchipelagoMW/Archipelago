"""This module contains options for New Game Plus items in the item pool"""

from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class NGPlusItems(Choice):
    """
    Determines how New Game Plus items appear in the multiworld.
    This option when enabled puts the RY3N0 into the item pool and the mega versions of weapons in the vendor
    if you have a V5 weapon.
    For progressive weapons, it will instead add 3 more upgrades to the pool, up to V8.
    **Disable**: The RY3N0 will not appear in the multiworld, the mega versions of weapons are not purchasable.
    **Enable**: The RY3N0 will appear in the multiworld, the mega versions of weapons are purchasable.

    This option when enabled will not grant checks for the mega weapon vendor purchases, it'll provide the mega version
    of the weapon only.
    """
    display_name = RAC3OPTION.NGPLUS_ITEMS
    option_disable = 0
    option_enable = 1
    default = 0
