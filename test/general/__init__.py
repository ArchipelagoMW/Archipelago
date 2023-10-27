from argparse import Namespace
from typing import List, Tuple, Type

from BaseClasses import CollectionState, MultiWorld
from worlds.AutoWorld import World, call_all

gen_steps = ("generate_early", "create_regions", "create_items", "set_rules", "generate_basic", "pre_fill")


def setup_solo_multiworld(world_type: Type[World], steps: Tuple[str, ...] = gen_steps) -> MultiWorld:
    """
    Creates a multiworld with a single player of `world_type`, sets default options, and calls provided gen steps.
    
    :param world_type: Type of the world to generate a multiworld for
    :param steps: The gen steps that should be called on the generated multiworld before returning. Default calls
    steps through pre_fill
    """
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


def setup_multiworld(worlds: List[Type[World]], steps: Tuple[str, ...] = gen_steps) -> MultiWorld:
    """
    Creates a multiworld with a player for each provided world, allowing duplicates, setting default options, and
    calling the provided gen steps.
    
    :param worlds: list of the types of worlds to generate a multiworld for
    :param steps: gen steps that should be called before returning. Default calls through pre_fill
    """
    players = len(worlds)
    multiworld = MultiWorld(players)
    multiworld.game = {player: world_type.game for player, world_type in enumerate(worlds, 1)}
    multiworld.player_name = {player: f"Tester{player}" for player in range(1, players + 1)}
    multiworld.set_seed()
    multiworld.state = CollectionState(multiworld)
    args = Namespace()
    for player, world_type in enumerate(worlds, 1):
        for key, option in world_type.options_dataclass.type_hints.items():
            updated_options = getattr(args, key, {})
            updated_options[player] = option.from_any(option.default)
            setattr(args, key, updated_options)
    multiworld.set_options(args)
    for step in steps:
        call_all(multiworld, step)
    return multiworld
