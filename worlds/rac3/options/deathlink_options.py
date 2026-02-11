from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class Deathlink(Choice):
    """
    Any players with "Death Link" who die in their game will
    cause all other players with this option enabled to also die
    """
    display_name = RAC3OPTION.DEATHLINK
    option_off = 0
    option_on = 1
    default = 0
