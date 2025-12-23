from Options import Choice
from worlds.rac3 import RAC3OPTION


class ShipNose(Choice):
    """
    Cosmetic:
    What Nose should you have on the ship?
    """
    display_name = RAC3OPTION.SHIP_NOSE
    option_standard = 0
    option_split = 1
    option_scoop = 2
    default = 0
