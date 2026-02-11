import itertools

from entrance_rando import randomize_entrances
from ..Options import OracleOfSeasonsPortalShuffle
from ..World import OracleOfSeasonsWorld
from ..data.Constants import DUNGEON_CONNECTIONS, PORTAL_CONNECTIONS, OracleOfSeasonsConnectionType


def list_entrances_for_patch(world: OracleOfSeasonsWorld, prefix: str, vanilla_entrances: dict[str, str]):
    seen_entrances = set()
    connections = {}
    for entrance1 in itertools.chain(vanilla_entrances, vanilla_entrances.values()):  # Do them in order overworld then subrosia
        if entrance1 in seen_entrances:
            continue
        seen_entrances.add(entrance1)
        entrance2 = world.get_entrance(f"{prefix}{entrance1}").connected_region.name
        seen_entrances.add(entrance2)
        connections[entrance1] = entrance2
    return connections


def oos_randomize_entrances(world: OracleOfSeasonsWorld) -> None:
    target_group_lookup = {
        OracleOfSeasonsConnectionType.CONNECT_PORTAL_OVERWORLD: [OracleOfSeasonsConnectionType.CONNECT_PORTAL_SUBROSIA],
        OracleOfSeasonsConnectionType.CONNECT_PORTAL_SUBROSIA: [OracleOfSeasonsConnectionType.CONNECT_PORTAL_OVERWORLD],
        OracleOfSeasonsConnectionType.CONNECT_DUNGEON_OVERWORLD: [OracleOfSeasonsConnectionType.CONNECT_DUNGEON_INSIDE],
        OracleOfSeasonsConnectionType.CONNECT_DUNGEON_INSIDE: [OracleOfSeasonsConnectionType.CONNECT_DUNGEON_OVERWORLD]
    }
    if world.options.shuffle_portals == OracleOfSeasonsPortalShuffle.option_shuffle:
        target_group_lookup[OracleOfSeasonsConnectionType.CONNECT_PORTAL_OVERWORLD] \
            .append(OracleOfSeasonsConnectionType.CONNECT_PORTAL_OVERWORLD)
        target_group_lookup[OracleOfSeasonsConnectionType.CONNECT_PORTAL_SUBROSIA] \
            .append(OracleOfSeasonsConnectionType.CONNECT_PORTAL_SUBROSIA)

    placement_state = randomize_entrances(world, True, target_group_lookup)
    if world.options.shuffle_portals:
        world.portal_connections = list_entrances_for_patch(world, "enter ", PORTAL_CONNECTIONS)
    if world.options.shuffle_dungeons:
        world.dungeon_entrances = list_entrances_for_patch(world, "", world.dungeon_entrances)
