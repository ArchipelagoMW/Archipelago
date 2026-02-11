from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class ClankOptions(Choice):
    """
    Determines how Clank and his packs appear in the world.
    Start with: Begin with Clank and all packs already collected.
    Shuffled as one: Clank is randomized in the pool, finding him will give access to both packs.
    Shuffled Independently: Each pack is an independent item, Heli-pack is required to glide.
    Shuffled Progressive: Two Progressive packs are added, the first one gives Heli-pack and the second gives Thruster.
    Warning: Using this option while starting on Veldin may result in a restrictive start for solo seeds!
    """
    display_name = RAC3OPTION.CLANK_OPTIONS
    option_start_with = 0
    option_shuffled_as_one = 1
    option_shuffled_independently = 2
    option_shuffled_progressive = 3
    default = 0
