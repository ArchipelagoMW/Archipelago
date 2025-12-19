from Options import Choice
from worlds.rac3 import RAC3OPTION


class ShipWings(Choice):
    """
    Cosmetic:
    What Wings should you have on the ship?
    """
    display_name = RAC3OPTION.SHIP_WINGS
    option_standard = 0
    option_hi_lift = 4
    option_heavy_ordinance = 8
    default = 0
