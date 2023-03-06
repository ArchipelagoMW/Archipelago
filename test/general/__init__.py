from argparse import Namespace
from typing import Type, Tuple

from BaseClasses import MultiWorld, CollectionState
from worlds.AutoWorld import call_all, World

gen_steps = ("generate_early", "create_regions", "create_items", "set_rules", "generate_basic", "pre_fill")


def setup_solo_multiworld(world_type: Type[World], steps: Tuple[str, ...] = gen_steps) -> MultiWorld:
    multiworld = MultiWorld(1)
    multiworld.game[1] = world_type.game
    multiworld.player_name = {1: "Tester"}
    multiworld.set_seed()
    multiworld.state = CollectionState(multiworld)
    args = Namespace()
    for name, option in world_type.options_dataclass.type_hints.items():
        setattr(args, name, {1: option.from_any(option.default)})
    multiworld.set_options(args)
    for step in steps:
        call_all(multiworld, step)
    return multiworld
