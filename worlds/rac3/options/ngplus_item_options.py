"""This module contains options for New Game Plus items in the item pool"""

from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class NGPlusItems(Choice):
    """
    Determines if the RY3NO should be an item in the item pool or not.
    **Disable**: It is available.
    **Enable**: It is not available.
    """
    display_name = RAC3OPTION.NGPLUS_ITEMS
    option_disable = 0
    option_enable = 1
    default = 0
