from argparse import Namespace
from typing import Type, Tuple, List

import Options
from BaseClasses import MultiWorld, CollectionState, Region, Location, Item, ItemClassification
from worlds.AutoWorld import call_all, World

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


def generate_multiworld(players: int = 1) -> MultiWorld:
    multiworld = MultiWorld(players)
    multiworld.player_name = {}
    multiworld.state = CollectionState(multiworld)
    for i in range(players):
        player_id = i+1
        world = World(multiworld, player_id)
        multiworld.game[player_id] = f"Game {player_id}"
        multiworld.worlds[player_id] = world
        multiworld.player_name[player_id] = "Test Player " + str(player_id)
        region = Region("Menu", player_id, multiworld, "Menu Region Hint")
        multiworld.regions.append(region)
        for option_key, option in Options.PerGameCommonOptions.type_hints.items():
            if hasattr(multiworld, option_key):
                getattr(multiworld, option_key).setdefault(player_id, option.from_any(getattr(option, "default")))
            else:
                setattr(multiworld, option_key, {player_id: option.from_any(getattr(option, "default"))})
        # TODO - remove this loop once all worlds use options dataclasses
        world.options = world.options_dataclass(**{option_key: getattr(multiworld, option_key)[player_id]
                                                   for option_key in world.options_dataclass.type_hints})

    multiworld.set_seed(0)

    return multiworld


def generate_locations(count: int, player_id: int, address: int = None, region: Region = None, tag: str = "") -> List[Location]:
    locations = []
    prefix = "player" + str(player_id) + tag + "_location"
    for i in range(count):
        name = prefix + str(i)
        location = Location(player_id, name, address, region)
        locations.append(location)
        region.locations.append(location)
    return locations


def generate_items(count: int, player_id: int, advancement: bool = False, code: int = None) -> List[Item]:
    items = []
    item_type = "prog" if advancement else ""
    for i in range(count):
        name = "player" + str(player_id) + "_" + item_type + "item" + str(i)
        items.append(Item(name,
                          ItemClassification.progression if advancement else ItemClassification.filler,
                          code, player_id))
    return items
