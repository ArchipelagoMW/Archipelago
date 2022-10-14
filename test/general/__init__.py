from argparse import Namespace

from BaseClasses import MultiWorld
from worlds.AutoWorld import call_all

gen_steps = ["generate_early", "create_regions", "create_items", "set_rules", "generate_basic", "pre_fill"]


def setup_default_world(world_type) -> MultiWorld:
    world = MultiWorld(1)
    world.game[1] = world_type.game
    world.player_name = {1: "Tester"}
    world.set_seed()
    args = Namespace()
    for name, option in world_type.option_definitions.items():
        setattr(args, name, {1: option.from_any(option.default)})
    world.set_options(args)
    world.set_default_common_options()
    for step in gen_steps:
        call_all(world, step)
    return world
