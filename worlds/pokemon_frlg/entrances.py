from enum import IntEnum
from typing import TYPE_CHECKING, List, Set
from BaseClasses import Entrance, EntranceType
from entrance_rando import (ERPlacementState, EntranceRandomizationError, disconnect_entrance_for_randomization,
                            randomize_entrances)
from .options import DungeonEntranceShuffle

if TYPE_CHECKING:
    from . import PokemonFRLGWorld

MAX_GER_ATTEMPTS = 10

kanto_single_dungeon_entrances = ["Vermilion Harbor", "Pokemon Tower", "Rocket Hideout", "Safari Zone Entrance",
                                  "Silph Co.", "Pokemon Mansion", "Cerulean Cave", "Navel Rock"]

kanto_single_dungeon_exits = ["Vermilion Harbor Exit", "Pokemon Tower 1F Exit",
                              "Rocket Hideout B1F North Stairs (West)", "Safari Zone Entrance Exit",
                              "Silph Co. 1F Exit", "Pokemon Mansion 1F Exit", "Cerulean Cave 1F Southeast Exit",
                              "Navel Rock 1F Exit"]

sevii_single_dungeon_entrances = ["Mt. Ember", "Berry Forest", "Icefall Cave", "Rocket Warehouse", "Lost Cave",
                                  "Dotted Hole", "Altering Cave", "Viapois Chamber", "Rixy Chamber", "Scufib Chamber",
                                  "Dilford Chamber", "Weepth Chamber", "Liptoo Chamber", "Monean Chamber"]

sevii_single_dungeon_exits = ["Mt. Ember Exterior South Exit", "Berry Forest Exit", "Icefall Cave Front Exit",
                              "Rocket Warehouse Exit", "Lost Cave 1F Exit", "Dotted Hole 1F Exit", "Altering Cave Exit",
                              "Viapois Chamber Exit", "Rixy Chamber Exit", "Scufib Chamber Exit",
                              "Dilford Chamber Exit", "Weepth Chamber Exit", "Liptoo Chamber Exit",
                              "Monean Chamber Exit"]

kanto_multi_dungeon_entrances = ["Viridian Forest South Gate Exit (North)", "Viridian Forest North Gate Exit (South)",
                                 "Mt. Moon (West)", "Mt. Moon (East)", "Diglett's Cave North Entrance",
                                 "Diglett's Cave South Entrance", "Rock Tunnel (North)", "Rock Tunnel (South)",
                                 "Power Plant (Front)", "Power Plant (Back)", "Seafoam Islands (North)",
                                 "Seafoam Islands (South)", "Victory Road (West)", "Victory Road (East)"]

kanto_multi_dungeon_exits = ["Viridian Forest Exit (South)", "Viridian Forest Exit (North)", "Mt. Moon 1F Exit",
                             "Mt. Moon B1F Fourth Tunnel Ladder (East)", "Diglett's Cave North Entrance Exit",
                             "Diglett's Cave South Entrance Exit", "Rock Tunnel 1F Northeast Ladder (Northwest)",
                             "Rock Tunnel 1F South Exit", "Power Plant Exit (Front)", "Power Plant Exit (Back)",
                             "Seafoam Islands 1F Exit", "Seafoam Islands 1F Southeast Exit",
                             "Victory Road 1F South Exit", "Victory Road 2F East Exit"]

sevii_multi_dungeon_entrances = ["Pattern Bush (West)", "Pattern Bush (East)"]

sevii_multi_dungeon_exits = ["Pattern Bush Exit (West)", "Pattern Bush Exit (East)"]

multi_dungeon_pairs = {
    "Viridian Forest South Gate Exit (North)": "Viridian Forest North Gate Exit (South)",
    "Mt. Moon (West)": "Mt. Moon (East)",
    "Diglett's Cave North Entrance": "Diglett's Cave South Entrance",
    "Rock Tunnel (North)": "Rock Tunnel (South)",
    "Power Plant (Front)": "Power Plant (Back)",
    "Seafoam Islands (North)": "Seafoam Islands (South)",
    "Victory Road (West)": "Victory Road (East)",
    "Pattern Bush (West)": "Pattern Bush (East)",
    "Viridian Forest Exit (South)": "Viridian Forest Exit (North)",
    "Mt. Moon 1F Exit": "Mt. Moon B1F Fourth Tunnel Ladder (East)",
    "Diglett's Cave North Entrance Exit": "Diglett's Cave South Entrance Exit",
    "Rock Tunnel 1F Northeast Ladder (Northwest)": "Rock Tunnel 1F South Exit",
    "Power Plant Exit (Front)": "Power Plant Exit (Back)",
    "Seafoam Islands 1F Exit": "Seafoam Islands 1F Southeast Exit",
    "Victory Road 1F South Exit": "Victory Road 2F East Exit",
    "Pattern Bush Exit (West)": "Pattern Bush Exit (East)"
}
multi_dungeon_pairs_reverse = {k: v for v, k in multi_dungeon_pairs.items()}


class EntranceGroups(IntEnum):
    UNSHUFFLED = 0
    DUNGEON_ENTRANCE = 1
    SINGLE_DUNGEON_ENTRANCE = 2
    MULTI_DUNGEON_ENTRANCE = 3
    DUNGEON_EXIT = 4
    SINGLE_DUNGEON_EXIT = 5
    MULTI_DUNGEON_EXIT = 6


dungeon_group_lookup = {
    EntranceGroups.DUNGEON_ENTRANCE: [EntranceGroups.DUNGEON_EXIT],
    EntranceGroups.SINGLE_DUNGEON_ENTRANCE: [EntranceGroups.SINGLE_DUNGEON_EXIT],
    EntranceGroups.MULTI_DUNGEON_ENTRANCE: [EntranceGroups.MULTI_DUNGEON_EXIT],
    EntranceGroups.DUNGEON_EXIT: [EntranceGroups.DUNGEON_ENTRANCE],
    EntranceGroups.SINGLE_DUNGEON_EXIT: [EntranceGroups.SINGLE_DUNGEON_ENTRANCE],
    EntranceGroups.MULTI_DUNGEON_EXIT: [EntranceGroups.MULTI_DUNGEON_ENTRANCE]
}


def shuffle_entrances(world: "PokemonFRLGWorld"):
    single_dungeon_entrances = []
    single_dungeon_exits = []
    multi_dungeon_entrances = []
    multi_dungeon_exits = []
    single_dungeon_entrances.extend(kanto_single_dungeon_entrances)
    single_dungeon_exits.extend(kanto_single_dungeon_exits)
    multi_dungeon_entrances.extend(kanto_multi_dungeon_entrances)
    multi_dungeon_exits.extend(kanto_multi_dungeon_exits)
    if not world.options.kanto_only:
        single_dungeon_entrances.extend(sevii_single_dungeon_entrances)
        single_dungeon_exits.extend(sevii_single_dungeon_exits)
        multi_dungeon_entrances.extend(sevii_multi_dungeon_entrances)
        multi_dungeon_exits.extend(sevii_multi_dungeon_exits)
    for entrance_name in single_dungeon_entrances:
        entrance = world.get_entrance(entrance_name)
        if world.options.dungeon_entrance_shuffle == DungeonEntranceShuffle.option_full:
            entrance.randomization_group = EntranceGroups.DUNGEON_ENTRANCE
        else:
            entrance.randomization_group = EntranceGroups.SINGLE_DUNGEON_ENTRANCE
        entrance.randomization_type = EntranceType.TWO_WAY
        disconnect_entrance_for_randomization(entrance, entrance.randomization_group)
    for entrance_name in single_dungeon_exits:
        entrance = world.get_entrance(entrance_name)
        if world.options.dungeon_entrance_shuffle == DungeonEntranceShuffle.option_full:
            entrance.randomization_group = EntranceGroups.DUNGEON_EXIT
        else:
            entrance.randomization_group = EntranceGroups.SINGLE_DUNGEON_EXIT
        entrance.randomization_type = EntranceType.TWO_WAY
        disconnect_entrance_for_randomization(entrance, entrance.randomization_group)
    for entrance_name in multi_dungeon_entrances:
        entrance = world.get_entrance(entrance_name)
        if world.options.dungeon_entrance_shuffle == DungeonEntranceShuffle.option_full:
            entrance.randomization_group = EntranceGroups.DUNGEON_ENTRANCE
        else:
            entrance.randomization_group = EntranceGroups.MULTI_DUNGEON_ENTRANCE
        entrance.randomization_type = EntranceType.TWO_WAY
        disconnect_entrance_for_randomization(entrance, entrance.randomization_group)
    for entrance_name in multi_dungeon_exits:
        entrance = world.get_entrance(entrance_name)
        if world.options.dungeon_entrance_shuffle == DungeonEntranceShuffle.option_full:
            entrance.randomization_group = EntranceGroups.DUNGEON_EXIT
        else:
            entrance.randomization_group = EntranceGroups.MULTI_DUNGEON_EXIT
        entrance.randomization_type = EntranceType.TWO_WAY
        disconnect_entrance_for_randomization(entrance, entrance.randomization_group)

    available_shuffle_types: Set[EntranceGroups] = set()
    if world.options.dungeon_entrance_shuffle == DungeonEntranceShuffle.option_full:
        available_shuffle_types.add(EntranceGroups.DUNGEON_ENTRANCE)
        available_shuffle_types.add(EntranceGroups.DUNGEON_EXIT)
    else:
        available_shuffle_types.add(EntranceGroups.SINGLE_DUNGEON_ENTRANCE)
        available_shuffle_types.add(EntranceGroups.SINGLE_DUNGEON_EXIT)
        available_shuffle_types.add(EntranceGroups.MULTI_DUNGEON_ENTRANCE)
        available_shuffle_types.add(EntranceGroups.MULTI_DUNGEON_EXIT)

    world.logic.randomizing_entrances = True
    for i in range(MAX_GER_ATTEMPTS):
        try:
            world.er_placement_state = randomize_entrances(world, True, dungeon_group_lookup,
                                                           on_connect=connect_simple_entrances)
            world.er_spoiler_names.extend(single_dungeon_entrances + multi_dungeon_entrances)
            world.logic.randomizing_entrances = False
            # Make the Pokemon Mansion other exit match the shuffled exit
            cinnabar_region = world.get_region("Cinnabar Island")
            mansion_shuffled_entrance = world.get_entrance("Pokemon Mansion 1F Exit")
            mansion_other_entrance = world.get_entrance("Pokemon Mansion 1F Southeast Exit")
            cinnabar_region.entrances.remove(mansion_other_entrance)
            mansion_other_entrance.connected_region = mansion_shuffled_entrance.connected_region
            mansion_shuffled_entrance.connected_region.entrances.append(mansion_other_entrance)
            for source, dest in world.er_placement_state.pairings:
                if source == "Pokemon Mansion 1F Exit":
                    world.er_placement_state.pairings.append((mansion_other_entrance.name, dest))
                    break
            break
        except EntranceRandomizationError as error:
            if i >= MAX_GER_ATTEMPTS - 1:
                raise EntranceRandomizationError(f"Pokemon FRLG: GER failed for player {world.player} "
                                                 f"({world.player_name}) after {MAX_GER_ATTEMPTS} attempts. Final "
                                                 f"error here: \n\n{error}")
            for region in world.get_regions():
                for exit in region.get_exits():
                    if (exit.randomization_group in available_shuffle_types and
                            exit.parent_region and
                            exit.connected_region):
                        exit.connected_entrance_name = None
                        disconnect_entrance_for_randomization(exit, exit.randomization_group)


def connect_simple_entrances(er_state: ERPlacementState, placed_entrances: List[Entrance]):
    world: "PokemonFRLGWorld" = er_state.world
    if world.options.dungeon_entrance_shuffle != DungeonEntranceShuffle.option_simple:
        return

    dungeon_pairs = multi_dungeon_pairs | multi_dungeon_pairs_reverse

    if placed_entrances[0].name not in dungeon_pairs or placed_entrances[1].name not in dungeon_pairs:
        return

    entrance = world.get_entrance(dungeon_pairs[placed_entrances[0].name])
    exit = world.get_entrance(dungeon_pairs[placed_entrances[1].name])
    entrance.connected_entrance_name = exit.name
    exit.connected_entrance_name = entrance.name
