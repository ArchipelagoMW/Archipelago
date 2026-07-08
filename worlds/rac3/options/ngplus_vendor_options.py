"""This module contains options for New Game Plus purchase locations"""

from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class NGPlusVendor(Choice):
    """
    Determines if the RY3N0 Purchase should be a location in the vendor or not.
    ------------------------------------------------------------------------------------
    Disabled: The RY3N0 is not a purchasable location.
    Enabled:  The RY3N0 is a purchasable location.
    ------------------------------------------------------------------------------------
    """
    display_name = RAC3OPTION.NGPLUS_VENDOR
    option_disabled = 0
    option_enabled = 1
    default = 0
