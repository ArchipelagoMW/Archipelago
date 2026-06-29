"""This module contains options for New Game Plus purchase locations"""

from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class NGPlusVendor(Choice):
    """
    Determines if the RY3NO Purchase should be a location in the vendor or not.
    **Disabled**: It is not purchasable.
    **Enabled**: It is purchasable.
    """
    display_name = RAC3OPTION.NGPLUS_VENDOR
    option_disabled = 0
    option_enabled = 1
    default = 0
