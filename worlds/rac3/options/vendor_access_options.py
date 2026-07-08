"""This module contains options for item availability in the vendors"""

from Options import Choice
from worlds.rac3 import RAC3OPTION


class VendorAccess(Choice):
    """
    Determines if vendor items should become available after a planet is visited or once its infobot has been collected.
    ------------------------------------------------------------------------------
    Visit:      Vendor items are available after visiting a planet.
    Infobot:    Vendor items are available when the infobot is collected.
    ------------------------------------------------------------------------------
    The Holo-shield glove is normally accessible after defeating the Noid Queen on Tyhrranosis instead of just visiting.
    """
    display_name = RAC3OPTION.VENDOR_ACCESS
    option_visit = 0
    option_infobot = 1
    default = 0
