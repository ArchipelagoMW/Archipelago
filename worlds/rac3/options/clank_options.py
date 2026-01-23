from Options import Choice
from worlds.rac3 import RAC3OPTION


class ClankOptions(Choice):
    """
    Determines how Clank and his packs appear in the world.
    Vanilla: You start with Clank and all of his packs.
    Clank item: Clank himself is randomized in the pool, findig him will give access to both packs.
    Clank Packs: The heli-pack and thruster-pack are randomized as separate items in the pool.
    Warning: Using this option while starting on Veldin may result in a restrictive start for solo seeds!
    """
    display_name = RAC3OPTION.CLANK_OPTIONS
    option_vanilla = 0
    option_clank_item = 1
    option_clank_packs = 2
    default = 0
