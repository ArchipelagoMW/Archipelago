from argparse import Namespace
from typing import Type, Tuple

from BaseClasses import MultiWorld
from Options import Option
from worlds.AutoWorld import call_all, World
from worlds.clique import CliqueWorld

gen_steps = ("generate_early", "create_regions", "create_items", "set_rules", "generate_basic", "pre_fill")


def setup_solo_multiworld(world_type: Type[World], steps: Tuple[str, ...] = gen_steps) -> MultiWorld:
    multiworld = MultiWorld(1)
    multiworld.game[1] = world_type.game
    multiworld.player_name = {1: "Tester"}
    multiworld.set_seed()
    args = Namespace()
    for name, option in world_type.option_definitions.items():
        setattr(args, name, {1: option.from_any(option.default)})
    multiworld.set_options(args)
    multiworld.set_default_common_options()
    for step in steps:
        call_all(multiworld, step)
    return multiworld


def setup_duo_multiworld(world_type: Type[World], steps: Tuple[str, ...] = gen_steps) -> MultiWorld:
    """ player 2 is a Clique World """
    multiworld = MultiWorld(2)
    multiworld.game[1] = world_type.game
    multiworld.game[2] = "Clique"
    multiworld.player_name = {1: "Tester 1", 2: "Tester 2"}
    multiworld.set_seed()
    args = Namespace()
    for name, option in world_type.option_definitions.items():
        assert issubclass(option, Option)
        setattr(args, name, {1: option.from_any(option.default)})
    for name, option in CliqueWorld.option_definitions.items():
        assert issubclass(option, Option)
        set_from_player_1 = getattr(args, name, {})
        set_from_player_1.update({2: option.from_any(option.default)})
        setattr(args, name, set_from_player_1)
    multiworld.set_options(args)
    multiworld.set_default_common_options()
    for step in steps:
        call_all(multiworld, step)
    return multiworld
