from Options import Choice
from worlds.rac3 import RAC3OPTION


class Deathlink(Choice):
    """
    If the current player character dies, other players with "Death Link" enabled with also die, and vice versa.
    """
    display_name = RAC3OPTION.DEATHLINK
    option_off = 0
    option_on = 1
    default = 0
