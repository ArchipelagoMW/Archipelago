from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class ShipVendors(Choice):
    """
    Determines whether ship vendor cosmetics are locations in the world.
    Disabled: No ship vendor cosmetics are locations.
    Enabled: Ship vendor cosmetics are added as locations.

    Note: Each planet you have will put the next 3 items in the ship vendor in order of how they would appear in the vanilla game.
    You cannot change ship cosmetics with this option enabled.
    """
    display_name = RAC3OPTION.SHIP_VENDOR
    option_disabled = 0
    option_enabled = 1
    default = 1
