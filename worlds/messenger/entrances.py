import logging
from typing import List, TYPE_CHECKING

from BaseClasses import Entrance, Region
from EntranceRando import randomize_entrances
from .connections import RANDOMIZED_CONNECTIONS, TRANSITIONS
from .options import ShuffleTransitions

if TYPE_CHECKING:
    from . import MessengerRegion, MessengerWorld


def shuffle_entrances(world: "MessengerWorld") -> None:
    multiworld = world.multiworld
    player = world.player
    coupled = world.options.shuffle_transitions == ShuffleTransitions.option_coupled

    def disconnect_entrance() -> None:
        child_region.entrances.remove(entrance)
        entrance.connected_region = None

        er_type = Entrance.EntranceType.ONE_WAY if child == "Glacial Peak - Left" else \
            Entrance.EntranceType.TWO_WAY if child in RANDOMIZED_CONNECTIONS else Entrance.EntranceType.ONE_WAY
        if er_type == Entrance.EntranceType.TWO_WAY:
            mock_entrance = parent_region.create_er_target(entrance.name)
        else:
            mock_entrance = child_region.create_er_target(child)

        entrance.er_type = er_type
        mock_entrance.er_type = er_type

    regions_to_shuffle: List[MessengerRegion] = []
    for parent, child in RANDOMIZED_CONNECTIONS.items():

        if child == "Corrupted Future":
            entrance = multiworld.get_entrance("Artificer's Portal", player)
        elif child == "Tower of Time - Left":
            entrance = multiworld.get_entrance("Artificer's Challenge", player)
        else:
            entrance = multiworld.get_entrance(f"{parent} -> {child}", player)
        parent_region = entrance.parent_region
        child_region = entrance.connected_region
        entrance.world = world
        disconnect_entrance()
        regions_to_shuffle += [parent_region, child_region]

    result = randomize_entrances(world, set(regions_to_shuffle), coupled, lambda group: ["Default"])

    world.transitions = sorted(result.placements, key=lambda entrance: TRANSITIONS.index(entrance.parent_region.name))

    for transition in world.transitions:
        if "->" not in transition.name:
            continue
        transition.parent_region.exits.remove(transition)
        transition.name = f"{transition.parent_region} -> {transition.connected_region}"
        transition.parent_region.exits.append(transition)
