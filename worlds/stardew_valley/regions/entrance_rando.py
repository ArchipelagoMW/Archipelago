from random import Random
from typing import Iterable, Dict, List, Tuple, Set

from BaseClasses import Region
from .model import RegionData, ConnectionData, RandomizationFlag
from ..content import content_packs, StardewContent
from ..options import EntranceRandomization, StardewValleyOptions
from ..strings.region_names import Region


def randomize_connections(random: Random, world_options: StardewValleyOptions, content: StardewContent, regions_by_name: Dict[str, RegionData],
                          connections_by_name: Dict[str, ConnectionData]) -> Tuple[List[ConnectionData], Dict[str, str]]:
    connections_to_randomize: List[ConnectionData] = []
    if world_options.entrance_randomization == EntranceRandomization.option_pelican_town:
        connections_to_randomize = [connections_by_name[connection] for connection in connections_by_name if
                                    RandomizationFlag.PELICAN_TOWN in connections_by_name[connection].flag]
    elif world_options.entrance_randomization == EntranceRandomization.option_non_progression:
        connections_to_randomize = [connections_by_name[connection] for connection in connections_by_name if
                                    RandomizationFlag.NON_PROGRESSION in connections_by_name[connection].flag]
    elif world_options.entrance_randomization == EntranceRandomization.option_buildings or world_options.entrance_randomization == EntranceRandomization.option_buildings_without_house:
        connections_to_randomize = [connections_by_name[connection] for connection in connections_by_name if
                                    RandomizationFlag.BUILDINGS in connections_by_name[connection].flag]
    elif world_options.entrance_randomization == EntranceRandomization.option_chaos:
        connections_to_randomize = [connections_by_name[connection] for connection in connections_by_name if
                                    RandomizationFlag.BUILDINGS in connections_by_name[connection].flag]
        connections_to_randomize = remove_excluded_entrances(connections_to_randomize, content)

        # On Chaos, we just add the connections to randomize, unshuffled, and the client does it every day
        randomized_data_for_mod = {}
        for connection in connections_to_randomize:
            randomized_data_for_mod[connection.name] = connection.name
            randomized_data_for_mod[connection.reverse] = connection.reverse
        return list(connections_by_name.values()), randomized_data_for_mod

    connections_to_randomize = remove_excluded_entrances(connections_to_randomize, content)
    random.shuffle(connections_to_randomize)
    destination_pool = list(connections_to_randomize)
    random.shuffle(destination_pool)

    randomized_connections = randomize_chosen_connections(connections_to_randomize, destination_pool)
    add_non_randomized_connections(list(connections_by_name.values()), connections_to_randomize, randomized_connections)

    swap_connections_until_valid(regions_by_name, connections_by_name, randomized_connections, connections_to_randomize, random)
    randomized_connections_for_generation = create_connections_for_generation(randomized_connections)
    randomized_data_for_mod = create_data_for_mod(randomized_connections, connections_to_randomize)

    return randomized_connections_for_generation, randomized_data_for_mod


def remove_excluded_entrances(connections_to_randomize: List[ConnectionData], content: StardewContent) -> List[ConnectionData]:
    # FIXME remove when regions are handled in content packs
    if content_packs.ginger_island_content_pack.name not in content.registered_packs:
        connections_to_randomize = [connection for connection in connections_to_randomize if RandomizationFlag.GINGER_ISLAND not in connection.flag]
    if not content.features.skill_progression.are_masteries_shuffled:
        connections_to_randomize = [connection for connection in connections_to_randomize if RandomizationFlag.MASTERIES not in connection.flag]

    return connections_to_randomize


def randomize_chosen_connections(connections_to_randomize: List[ConnectionData],
                                 destination_pool: List[ConnectionData]) -> Dict[ConnectionData, ConnectionData]:
    randomized_connections = {}
    for connection in connections_to_randomize:
        destination = destination_pool.pop()
        randomized_connections[connection] = destination
    return randomized_connections


def create_connections_for_generation(randomized_connections: Dict[ConnectionData, ConnectionData]) -> List[ConnectionData]:
    connections = []
    for connection in randomized_connections:
        destination = randomized_connections[connection]
        connections.append(ConnectionData(connection.name, destination.destination, destination.reverse))
    return connections


def create_data_for_mod(randomized_connections: Dict[ConnectionData, ConnectionData],
                        connections_to_randomize: List[ConnectionData]) -> Dict[str, str]:
    randomized_data_for_mod = {}
    for connection in randomized_connections:
        if connection not in connections_to_randomize:
            continue
        destination = randomized_connections[connection]
        add_to_mod_data(connection, destination, randomized_data_for_mod)
    return randomized_data_for_mod


def add_to_mod_data(connection: ConnectionData, destination: ConnectionData, randomized_data_for_mod: Dict[str, str]):
    randomized_data_for_mod[connection.name] = destination.name
    randomized_data_for_mod[destination.reverse] = connection.reverse


def add_non_randomized_connections(all_connections: List[ConnectionData], connections_to_randomize: List[ConnectionData],
                                   randomized_connections: Dict[ConnectionData, ConnectionData]):
    for connection in all_connections:
        if connection in connections_to_randomize:
            continue
        randomized_connections[connection] = connection


def swap_connections_until_valid(regions_by_name, connections_by_name: Dict[str, ConnectionData], randomized_connections: Dict[ConnectionData, ConnectionData],
                                 connections_to_randomize: List[ConnectionData], random: Random):
    while True:
        reachable_regions, unreachable_regions = find_reachable_regions(regions_by_name, connections_by_name, randomized_connections)
        if not unreachable_regions:
            return randomized_connections
        swap_one_random_connection(regions_by_name, connections_by_name, randomized_connections, reachable_regions,
                                   unreachable_regions, connections_to_randomize, random)


def region_should_be_reachable(region_name: str, connections_in_slot: Iterable[ConnectionData]) -> bool:
    if region_name == Region.menu:
        return True
    for connection in connections_in_slot:
        if region_name == connection.destination:
            return True
    return False


def find_reachable_regions(regions_by_name, connections_by_name,
                           randomized_connections: Dict[ConnectionData, ConnectionData]):
    reachable_regions = {Region.menu}
    unreachable_regions = {region for region in regions_by_name.keys()}
    # unreachable_regions = {region for region in regions_by_name.keys() if region_should_be_reachable(region, connections_by_name.values())}
    unreachable_regions.remove(Region.menu)
    exits_to_explore = list(regions_by_name[Region.menu].exits)
    while exits_to_explore:
        exit_name = exits_to_explore.pop()
        # if exit_name not in connections_by_name:
        #     continue
        exit_connection = connections_by_name[exit_name]
        replaced_connection = randomized_connections[exit_connection]
        target_region_name = replaced_connection.destination
        if target_region_name in reachable_regions:
            continue

        target_region = regions_by_name[target_region_name]
        reachable_regions.add(target_region_name)
        unreachable_regions.remove(target_region_name)
        exits_to_explore.extend(target_region.exits)
    return reachable_regions, unreachable_regions


def swap_one_random_connection(regions_by_name, connections_by_name, randomized_connections: Dict[ConnectionData, ConnectionData],
                               reachable_regions: Set[str], unreachable_regions: Set[str],
                               connections_to_randomize: List[ConnectionData], random: Random):
    randomized_connections_already_shuffled = {connection: randomized_connections[connection]
                                               for connection in randomized_connections
                                               if connection != randomized_connections[connection]}
    unreachable_regions_names_leading_somewhere = tuple([region for region in unreachable_regions
                                                         if len(regions_by_name[region].exits) > 0])
    unreachable_regions_leading_somewhere = [regions_by_name[region_name] for region_name in unreachable_regions_names_leading_somewhere]
    unreachable_regions_exits_names = [exit_name for region in unreachable_regions_leading_somewhere for exit_name in region.exits]
    unreachable_connections = [connections_by_name[exit_name] for exit_name in unreachable_regions_exits_names]
    unreachable_connections_that_can_be_randomized = [connection for connection in unreachable_connections if connection in connections_to_randomize]

    chosen_unreachable_entrance = random.choice(unreachable_connections_that_can_be_randomized)

    chosen_reachable_entrance = None
    while chosen_reachable_entrance is None or chosen_reachable_entrance not in randomized_connections_already_shuffled:
        chosen_reachable_region_name = random.choice(sorted(reachable_regions))
        chosen_reachable_region = regions_by_name[chosen_reachable_region_name]
        if not any(chosen_reachable_region.exits):
            continue
        chosen_reachable_entrance_name = random.choice(chosen_reachable_region.exits)
        chosen_reachable_entrance = connections_by_name[chosen_reachable_entrance_name]

    swap_two_connections(chosen_reachable_entrance, chosen_unreachable_entrance, randomized_connections)


def swap_two_connections(entrance_1, entrance_2, randomized_connections):
    reachable_destination = randomized_connections[entrance_1]
    unreachable_destination = randomized_connections[entrance_2]
    randomized_connections[entrance_1] = unreachable_destination
    randomized_connections[entrance_2] = reachable_destination
