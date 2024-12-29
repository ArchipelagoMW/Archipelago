from typing import TYPE_CHECKING

from BaseClasses import Region
from entrance_rando import EntranceType, randomize_entrances
from .connections import RANDOMIZED_CONNECTIONS, TRANSITIONS
from .options import ShuffleTransitions, TransitionPlando

if TYPE_CHECKING:
    from . import MessengerWorld


def connect_plando(world: "MessengerWorld", plando_connections: TransitionPlando) -> None:
    def remove_dangling_exit(region: Region) -> None:
        # find the disconnected exit and remove references to it
        for _exit in region.exits:
            if not _exit.connected_region:
                break
        else:
            raise ValueError(f"Unable to find randomized transition for {plando_connection}")
        region.exits.remove(_exit)

    def remove_dangling_entrance(region: Region) -> None:
        # find the disconnected entrance and remove references to it
        for _entrance in region.entrances:
            if not _entrance.parent_region:
                break
        else:
            raise ValueError(f"Invalid target region for {plando_connection}")
        region.entrances.remove(_entrance)

    multiworld = world.multiworld
    player = world.player
    for plando_connection in plando_connections:
        # get the connecting regions
        reg1 = multiworld.get_region(plando_connection.entrance, player)
        reg2 = multiworld.get_region(plando_connection.exit, player)

        remove_dangling_exit(reg1)
        remove_dangling_entrance(reg2)
        # connect the regions
        reg1.connect(reg2)

        # pretend the user set the direction as "both" regardless of what they actually put on coupled
        if ((world.options.shuffle_transitions == ShuffleTransitions.option_coupled
             or plando_connection.direction == "both")
                and plando_connection.exit in RANDOMIZED_CONNECTIONS):
            remove_dangling_exit(reg2)
            remove_dangling_entrance(reg1)
            reg2.connect(reg1)


def shuffle_transitions(world: "MessengerWorld") -> None:
    multiworld = world.multiworld
    player = world.player
    coupled = world.options.shuffle_transitions == ShuffleTransitions.option_coupled

    def disconnect_entrance() -> None:
        child_region.entrances.remove(entrance)
        entrance.connected_region = None

        er_type = EntranceType.ONE_WAY if child == "Glacial Peak - Left" else \
            EntranceType.TWO_WAY if child in RANDOMIZED_CONNECTIONS else EntranceType.ONE_WAY
        if er_type == EntranceType.TWO_WAY:
            mock_entrance = parent_region.create_er_target(entrance.name)
        else:
            mock_entrance = child_region.create_er_target(child)

        entrance.randomization_type = er_type
        mock_entrance.randomization_type = er_type

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

    plando = world.options.plando_connections
    if plando:
        connect_plando(world, plando)

    result = randomize_entrances(world, coupled, {0: [0]})

    world.transitions = sorted(result.placements, key=lambda entrance: TRANSITIONS.index(entrance.parent_region.name))

    for transition in world.transitions:
        if "->" not in transition.name:
            continue
        transition.parent_region.exits.remove(transition)
        transition.name = f"{transition.parent_region} -> {transition.connected_region}"
        transition.parent_region.exits.append(transition)
