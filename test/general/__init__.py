import random
from argparse import Namespace
from typing import Optional, Type, Tuple

from BaseClasses import MultiWorld, CollectionState
from worlds.AutoWorld import call_all, World

gen_steps = ("generate_early", "create_regions", "create_items", "set_rules", "generate_basic", "pre_fill")


def setup_solo_multiworld(world_type: Type[World], steps: Tuple[str, ...] = gen_steps,
                          seed: Optional[int] = None) -> MultiWorld:
    """
    Creates a multiworld with a single player of `world_type`, sets default options, and calls provided gen steps.

    :param world_type: Type of the world to generate a multiworld for
    :param steps: The gen steps that should be called on the generated multiworld before returning. Default calls
    steps through pre_fill
    :param seed: seed for the random number generator
    """
    multiworld = MultiWorld(1)
    multiworld.game[1] = world_type.game
    multiworld.player_name = {1: "Tester"}
    # option resolution uses global random
    random.seed(seed)
    multiworld.state = CollectionState(multiworld)
    args = Namespace()
    for name, option in world_type.options_dataclass.type_hints.items():
        setattr(args, name, {1: option.from_any(option.default)})
    # set the seed after resolving options to mimic normal generation
    multiworld.set_seed(seed)
    # reinitialize global random since it's unsafe for worlds to use
    random.seed(None)
    multiworld.set_options(args)
    for step in steps:
        call_all(multiworld, step)
    return multiworld
