from typing import TYPE_CHECKING

from BaseClasses import Region, Entrance
from entrance_rando import EntranceType, randomize_entrances, disconnect_entrance_for_randomization
from .connections import RANDOMIZED_CONNECTIONS, TRANSITIONS, ONE_WAY_EXITS, ONE_WAY_ENTRANCES
from .options import ShuffleTransitions, TransitionPlando

if TYPE_CHECKING:
    from . import MessengerWorld


def disconnect_entrances(world: "MessengerWorld") -> None:
    for region_exit, vanilla_connected_region in RANDOMIZED_CONNECTIONS.items():
        entrance = world.get_entrance(region_exit)
        entrance.randomization_type = EntranceType.ONE_WAY if region_exit in ONE_WAY_EXITS else EntranceType.TWO_WAY
        disconnect_entrance_for_randomization(entrance, one_way_target_name=vanilla_connected_region)


def connect_plando(world: "MessengerWorld", plando_connections: TransitionPlando) -> None:
    def find_dangling_exit(region: Region) -> Entrance:
        """Find the disconnected exit and return it."""
        for _exit in region.exits:
            if not _exit.connected_region:
                break
        else:
            raise ValueError(f"Unable to find randomized transition for {plando_connection}")
        return _exit

    def remove_dangling_entrance(region: Region) -> None:
        """Find the disconnected entrance and remove references to it."""
        for _entrance in region.entrances:
            if not _entrance.parent_region:
                break
        else:
            raise ValueError(f"Invalid target region for {plando_connection}")
        region.entrances.remove(_entrance)

    for plando_connection in plando_connections:
        plando_entrance = world.get_entrance(plando_connection.entrance)
        destination = world.get_region(plando_connection.exit)

        if plando_entrance.connected_region == destination:
            # The connection was already made bidirectional, skipping.
            continue

        remove_dangling_entrance(destination)
        plando_entrance.connect(destination)

        # pretend the user set the plando direction as "both" regardless of what they actually put on coupled
        if ((world.options.shuffle_transitions == ShuffleTransitions.option_coupled
             or plando_connection.direction == "both")
                and plando_connection.entrance not in ONE_WAY_EXITS
                and plando_connection.exit not in ONE_WAY_ENTRANCES):
            plando_reversed_entrance = find_dangling_exit(destination)
            source = plando_entrance.parent_region
            remove_dangling_entrance(source)
            plando_reversed_entrance.connect(source)


def shuffle_transitions(world: "MessengerWorld") -> None:
    coupled = world.options.shuffle_transitions == ShuffleTransitions.option_coupled

    plando = world.options.plando_connections
    if plando:
        connect_plando(world, plando)

    er_result = randomize_entrances(world, coupled, {0: [0]})

    world.transitions = sorted(er_result.placements,
                               key=lambda entrance: TRANSITIONS.index(entrance.name if " exit" not in entrance.name else entrance.name.replace(" exit", "")))
