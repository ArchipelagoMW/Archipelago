from typing import List, Set, Dict, Tuple, Optional, Callable
from BaseClasses import MultiWorld, Region, Entrance, Location
from .Locations import LocationData
from .Options import get_option_value, MissionOrder
from .MissionTables import MissionInfo, mission_orders, vanilla_mission_req_table, alt_final_mission_locations, \
    MissionPools, vanilla_shuffle_order
from .PoolFilter import filter_missions

PROPHECY_CHAIN_MISSION_COUNT = 4

VANILLA_SHUFFLED_FIRST_PROPHECY_MISSION = 21

def create_regions(multiworld: MultiWorld, player: int, locations: Tuple[LocationData, ...], location_cache: List[Location])\
        -> Tuple[Dict[str, MissionInfo], int, str]:
    locations_per_region = get_locations_per_region(locations)

    mission_order_type = get_option_value(multiworld, player, "mission_order")
    mission_order = mission_orders[mission_order_type]

    mission_pools = filter_missions(multiworld, player)

    regions = [create_region(multiworld, player, locations_per_region, location_cache, "Menu")]

    names: Dict[str, int] = {}

    if mission_order_type == MissionOrder.option_vanilla:

        # Generating all regions and locations
        for region_name in vanilla_mission_req_table.keys():
            regions.append(create_region(multiworld, player, locations_per_region, location_cache, region_name))
        multiworld.regions += regions

        connect(multiworld, player, names, 'Menu', 'Liberation Day'),
        connect(multiworld, player, names, 'Liberation Day', 'The Outlaws',
                lambda state: state.has("Beat Liberation Day", player)),
        connect(multiworld, player, names, 'The Outlaws', 'Zero Hour',
                lambda state: state.has("Beat The Outlaws", player)),
        connect(multiworld, player, names, 'Zero Hour', 'Evacuation',
                lambda state: state.has("Beat Zero Hour", player)),
        connect(multiworld, player, names, 'Evacuation', 'Outbreak',
                lambda state: state.has("Beat Evacuation", player)),
        connect(multiworld, player, names, "Outbreak", "Safe Haven",
                lambda state: state._sc2wol_cleared_missions(multiworld, player, 7) and
                              state.has("Beat Outbreak", player)),
        connect(multiworld, player, names, "Outbreak", "Haven's Fall",
                lambda state: state._sc2wol_cleared_missions(multiworld, player, 7) and
                              state.has("Beat Outbreak", player)),
        connect(multiworld, player, names, 'Zero Hour', 'Smash and Grab',
                lambda state: state.has("Beat Zero Hour", player)),
        connect(multiworld, player, names, 'Smash and Grab', 'The Dig',
                lambda state: state._sc2wol_cleared_missions(multiworld, player, 8) and
                              state.has("Beat Smash and Grab", player)),
        connect(multiworld, player, names, 'The Dig', 'The Moebius Factor',
                lambda state: state._sc2wol_cleared_missions(multiworld, player, 11) and
                              state.has("Beat The Dig", player)),
        connect(multiworld, player, names, 'The Moebius Factor', 'Supernova',
                lambda state: state._sc2wol_cleared_missions(multiworld, player, 14) and
                              state.has("Beat The Moebius Factor", player)),
        connect(multiworld, player, names, 'Supernova', 'Maw of the Void',
                lambda state: state.has("Beat Supernova", player)),
        connect(multiworld, player, names, 'Zero Hour', "Devil's Playground",
                lambda state: state._sc2wol_cleared_missions(multiworld, player, 4) and
                              state.has("Beat Zero Hour", player)),
        connect(multiworld, player, names, "Devil's Playground", 'Welcome to the Jungle',
                lambda state: state.has("Beat Devil's Playground", player)),
        connect(multiworld, player, names, "Welcome to the Jungle", 'Breakout',
                lambda state: state._sc2wol_cleared_missions(multiworld, player, 8) and
                              state.has("Beat Welcome to the Jungle", player)),
        connect(multiworld, player, names, "Welcome to the Jungle", 'Ghost of a Chance',
                lambda state: state._sc2wol_cleared_missions(multiworld, player, 8) and
                              state.has("Beat Welcome to the Jungle", player)),
        connect(multiworld, player, names, "Zero Hour", 'The Great Train Robbery',
                lambda state: state._sc2wol_cleared_missions(multiworld, player, 6) and
                              state.has("Beat Zero Hour", player)),
        connect(multiworld, player, names, 'The Great Train Robbery', 'Cutthroat',
                lambda state: state.has("Beat The Great Train Robbery", player)),
        connect(multiworld, player, names, 'Cutthroat', 'Engine of Destruction',
                lambda state: state.has("Beat Cutthroat", player)),
        connect(multiworld, player, names, 'Engine of Destruction', 'Media Blitz',
                lambda state: state.has("Beat Engine of Destruction", player)),
        connect(multiworld, player, names, 'Media Blitz', 'Piercing the Shroud',
                lambda state: state.has("Beat Media Blitz", player)),
        connect(multiworld, player, names, 'The Dig', 'Whispers of Doom',
                lambda state: state.has("Beat The Dig", player)),
        connect(multiworld, player, names, 'Whispers of Doom', 'A Sinister Turn',
                lambda state: state.has("Beat Whispers of Doom", player)),
        connect(multiworld, player, names, 'A Sinister Turn', 'Echoes of the Future',
                lambda state: state.has("Beat A Sinister Turn", player)),
        connect(multiworld, player, names, 'Echoes of the Future', 'In Utter Darkness',
                lambda state: state.has("Beat Echoes of the Future", player)),
        connect(multiworld, player, names, 'Maw of the Void', 'Gates of Hell',
                lambda state: state.has("Beat Maw of the Void", player)),
        connect(multiworld, player, names, 'Gates of Hell', 'Belly of the Beast',
                lambda state: state.has("Beat Gates of Hell", player)),
        connect(multiworld, player, names, 'Gates of Hell', 'Shatter the Sky',
                lambda state: state.has("Beat Gates of Hell", player)),
        connect(multiworld, player, names, 'Gates of Hell', 'All-In',
                lambda state: state.has('Beat Gates of Hell', player) and (
                        state.has('Beat Shatter the Sky', player) or state.has('Beat Belly of the Beast', player)))

        return vanilla_mission_req_table, 29, 'All-In: Victory'

    else:
        missions = []

        remove_prophecy = mission_order_type == 1 and not get_option_value(multiworld, player, "shuffle_protoss")

        final_mission = mission_pools[MissionPools.FINAL][0]

        # Determining if missions must be removed
        mission_pool_size = sum(len(mission_pool) for mission_pool in mission_pools.values())
        removals = len(mission_order) - mission_pool_size
        # Removing entire Prophecy chain on vanilla shuffled when not shuffling protoss
        if remove_prophecy:
            removals -= PROPHECY_CHAIN_MISSION_COUNT

        # Initial fill out of mission list and marking all-in mission
        for mission in mission_order:
            # Removing extra missions if mission pool is too small
            # Also handle lower removal priority than Prophecy
            if 0 < mission.removal_priority <= removals or mission.category == 'Prophecy' and remove_prophecy \
                    or (remove_prophecy and mission_order_type == MissionOrder.option_vanilla_shuffled
                        and mission.removal_priority > vanilla_shuffle_order[
                            VANILLA_SHUFFLED_FIRST_PROPHECY_MISSION].removal_priority
                        and 0 < mission.removal_priority <= removals + PROPHECY_CHAIN_MISSION_COUNT):
                missions.append(None)
            elif mission.type == MissionPools.FINAL:
                missions.append(final_mission)
            else:
                missions.append(mission.type)

        no_build_slots = []
        easy_slots = []
        medium_slots = []
        hard_slots = []

        # Search through missions to find slots needed to fill
        for i in range(len(missions)):
            if missions[i] is None:
                continue
            if missions[i] == MissionPools.STARTER:
                no_build_slots.append(i)
            elif missions[i] == MissionPools.EASY:
                easy_slots.append(i)
            elif missions[i] == MissionPools.MEDIUM:
                medium_slots.append(i)
            elif missions[i] == MissionPools.HARD:
                hard_slots.append(i)

        # Add no_build missions to the pool and fill in no_build slots
        missions_to_add = mission_pools[MissionPools.STARTER]
        if len(no_build_slots) > len(missions_to_add):
            raise Exception("There are no valid No-Build missions.  Please exclude fewer missions.")
        for slot in no_build_slots:
            filler = multiworld.random.randint(0, len(missions_to_add) - 1)

            missions[slot] = missions_to_add.pop(filler)

        # Add easy missions into pool and fill in easy slots
        missions_to_add = missions_to_add + mission_pools[MissionPools.EASY]
        if len(easy_slots) > len(missions_to_add):
            raise Exception("There are not enough Easy missions to fill the campaign.  Please exclude fewer missions.")
        for slot in easy_slots:
            filler = multiworld.random.randint(0, len(missions_to_add) - 1)

            missions[slot] = missions_to_add.pop(filler)

        # Add medium missions into pool and fill in medium slots
        missions_to_add = missions_to_add + mission_pools[MissionPools.MEDIUM]
        if len(medium_slots) > len(missions_to_add):
            raise Exception("There are not enough Easy and Medium missions to fill the campaign.  Please exclude fewer missions.")
        for slot in medium_slots:
            filler = multiworld.random.randint(0, len(missions_to_add) - 1)

            missions[slot] = missions_to_add.pop(filler)

        # Add hard missions into pool and fill in hard slots
        missions_to_add = missions_to_add + mission_pools[MissionPools.HARD]
        if len(hard_slots) > len(missions_to_add):
            raise Exception("There are not enough missions to fill the campaign.  Please exclude fewer missions.")
        for slot in hard_slots:
            filler = multiworld.random.randint(0, len(missions_to_add) - 1)

            missions[slot] = missions_to_add.pop(filler)

        # Generating regions and locations from selected missions
        for region_name in missions:
            regions.append(create_region(multiworld, player, locations_per_region, location_cache, region_name))
        multiworld.regions += regions

        # Mapping original mission slots to shifted mission slots when missions are removed
        slot_map = []
        slot_offset = 0
        for position, mission in enumerate(missions):
            slot_map.append(position - slot_offset + 1)
            if mission is None:
                slot_offset += 1

        # Loop through missions to create requirements table and connect regions
        # TODO: Handle 'and' connections
        mission_req_table = {}

        def build_connection_rule(mission_names: List[str], missions_req: int) -> Callable:
            if len(mission_names) > 1:
                return lambda state: state.has_all({f"Beat {name}" for name in mission_names}, player) and \
                                     state._sc2wol_cleared_missions(multiworld, player, missions_req)
            else:
                return lambda state: state.has(f"Beat {mission_names[0]}", player) and \
                                     state._sc2wol_cleared_missions(multiworld, player, missions_req)

        for i, mission in enumerate(missions):
            if mission is None:
                continue
            connections = []
            all_connections = []
            for connection in mission_order[i].connect_to:
                if connection == -1:
                    continue
                while missions[connection] is None:
                    connection -= 1
                all_connections.append(missions[connection])
            for connection in mission_order[i].connect_to:
                required_mission = missions[connection]
                if connection == -1:
                    connect(multiworld, player, names, "Menu", mission)
                else:
                    if required_mission is None and not mission_order[i].completion_critical:  # Drop non-critical null slots
                        continue
                    while required_mission is None:  # Substituting null slot with prior slot
                        connection -= 1
                        required_mission = missions[connection]
                    required_missions = [required_mission] if mission_order[i].or_requirements else all_connections
                    connect(multiworld, player, names, required_mission, mission,
                            build_connection_rule(required_missions, mission_order[i].number))
                    connections.append(slot_map[connection])

            mission_req_table.update({mission: MissionInfo(
                vanilla_mission_req_table[mission].id, connections, mission_order[i].category,
                number=mission_order[i].number,
                completion_critical=mission_order[i].completion_critical,
                or_requirements=mission_order[i].or_requirements)})

        final_mission_id = vanilla_mission_req_table[final_mission].id

        # Changing the completion condition for alternate final missions into an event
        if final_mission != 'All-In':
            final_location = alt_final_mission_locations[final_mission]
            # Final location should be near the end of the cache
            for i in range(len(location_cache) - 1, -1, -1):
                if location_cache[i].name == final_location:
                    location_cache[i].locked = True
                    location_cache[i].event = True
                    location_cache[i].address = None
                    break
        else:
            final_location = 'All-In: Victory'

        return mission_req_table, final_mission_id, final_location

def create_location(player: int, location_data: LocationData, region: Region,
                    location_cache: List[Location]) -> Location:
    location = Location(player, location_data.name, location_data.code, region)
    location.access_rule = location_data.rule

    if id is None:
        location.event = True
        location.locked = True

    location_cache.append(location)

    return location


def create_region(multiworld: MultiWorld, player: int, locations_per_region: Dict[str, List[LocationData]],
                  location_cache: List[Location], name: str) -> Region:
    region = Region(name, player, multiworld)

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region, location_cache)
            region.locations.append(location)

    return region


def connect(world: MultiWorld, player: int, used_names: Dict[str, int], source: str, target: str,
            rule: Optional[Callable] = None):
    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (' ' * used_names[target])

    connection = Entrance(player, name, sourceRegion)

    if rule:
        connection.access_rule = rule

    sourceRegion.exits.append(connection)
    connection.connect(targetRegion)


def get_locations_per_region(locations: Tuple[LocationData, ...]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]] = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region
