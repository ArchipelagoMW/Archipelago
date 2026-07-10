"""This module contains options for hinting locations in the vendor when scouted"""

from Options import OptionCounter
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.constants.vendors.name import VENDOR_TYPES


class ScoutVendors(OptionCounter):
    """
    Determines which vendors should send out hints about the items inside them.
    --------------------------------------------------------------------------------
    Armor:  Armor vendor sends out hints.
    Ship:   Ship vendor sends out hints.
    Weapon: Gadgetron vendors and Slim Cognito's shop send out hints.
    --------------------------------------------------------------------------------
    The vendors will always show the item names inside them in game, regardless of this option.

    0 = Disabled, Any other value = Enabled
    """
    min = 0
    display_name = RAC3OPTION.SCOUT_VENDORS
    default = dict.fromkeys(VENDOR_TYPES, 0)
    valid_keys = VENDOR_TYPES
