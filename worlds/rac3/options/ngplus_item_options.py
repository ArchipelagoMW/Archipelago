"""This module contains options for New Game Plus items in the item pool"""

from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class NGPlusItems(Choice):
    """
    Determines if the RY3NO should be an item in the item pool or not.
    **Disable**: It is available.
    **Enable**: It is not available.

    This option when enabled also puts mega versions of weapons in the vendor if you have a V5.
    For progressive weapons, it will instead add 3 more upgrades to the pool, up to V8.
    """
    display_name = RAC3OPTION.NGPLUS_ITEMS
    option_disable = 0
    option_enable = 1
    default = 0
