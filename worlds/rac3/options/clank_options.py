from Options import Choice
from worlds.rac3 import RAC3OPTION


class ClankOptions(Choice):
    """
    Determines how Clank and his packs appear in the world.
    Vanilla: You start with Clank on Veldin.
    Clank item: Clank himself is randomized in the pool, findig him will give access to both packs.
    """
    display_name = RAC3OPTION.CLANK_OPTIONS
    option_vanilla = 0
    option_clank_item = 1
    default = 0
