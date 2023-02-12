from typing import List, Set, Dict, Tuple, Optional, Callable
from BaseClasses import MultiWorld, Region, Entrance, Location
from .Locations import LocationData
from .Options import get_option_value
from .MissionTables import MissionInfo, mission_orders, vanilla_mission_req_table, alt_final_mission_locations
from .PoolFilter import filter_missions


def create_regions(multiworld: MultiWorld, player: int, locations: Tuple[LocationData, ...], location_cache: List[Location])\
        -> Tuple[Dict[str, MissionInfo], int, str]:
    locations_per_region = get_locations_per_region(locations)

    mission_order_type = get_option_value(multiworld, player, "mission_order")
    mission_order = mission_orders[mission_order_type]

    mission_pools = filter_missions(multiworld, player)
    final_mission = mission_pools['all_in'][0]

    used_regions = [mission for mission_pool in mission_pools.values() for mission in mission_pool]
    regions = [create_region(multiworld, player, locations_per_region, location_cache, "Menu")]
    for region_name in used_regions:
        regions.append(create_region(multiworld, player, locations_per_region, location_cache, region_name))
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

    if __debug__:
        if mission_order_type in (0, 1):
            throwIfAnyLocationIsNotAssignedToARegion(regions, locations_per_region.keys())

    multiworld.regions += regions

    names: Dict[str, int] = {}

    if mission_order_type == 0:
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

        return vanilla_mission_req_table, 29, final_location

    else:
        missions = []

        # Initial fill out of mission list and marking all-in mission
        for mission in mission_order:
            if mission is None:
                missions.append(None)
            elif mission.type == "all_in":
                missions.append(final_mission)
            elif mission.relegate and not get_option_value(multiworld, player, "shuffle_no_build"):
                missions.append("no_build")
            else:
                missions.append(mission.type)

        # Place Protoss Missions if we are not using ShuffleProtoss and are in Vanilla Shuffled
        if get_option_value(multiworld, player, "shuffle_protoss") == 0 and mission_order_type == 1:
            missions[22] = "A Sinister Turn"
            mission_pools['medium'].remove("A Sinister Turn")
            missions[23] = "Echoes of the Future"
            mission_pools['medium'].remove("Echoes of the Future")
            missions[24] = "In Utter Darkness"
            mission_pools['hard'].remove("In Utter Darkness")

        no_build_slots = []
        easy_slots = []
        medium_slots = []
        hard_slots = []

        # Search through missions to find slots needed to fill
        for i in range(len(missions)):
            if missions[i] is None:
                continue
            if missions[i] == "no_build":
                no_build_slots.append(i)
            elif missions[i] == "easy":
                easy_slots.append(i)
            elif missions[i] == "medium":
                medium_slots.append(i)
            elif missions[i] == "hard":
                hard_slots.append(i)

        # Add no_build missions to the pool and fill in no_build slots
        missions_to_add = mission_pools['no_build']
        for slot in no_build_slots:
            filler = multiworld.random.randint(0, len(missions_to_add) - 1)

            missions[slot] = missions_to_add.pop(filler)

        # Add easy missions into pool and fill in easy slots
        missions_to_add = missions_to_add + mission_pools['easy']
        for slot in easy_slots:
            filler = multiworld.random.randint(0, len(missions_to_add) - 1)

            missions[slot] = missions_to_add.pop(filler)

        # Add medium missions into pool and fill in medium slots
        missions_to_add = missions_to_add + mission_pools['medium']
        for slot in medium_slots:
            filler = multiworld.random.randint(0, len(missions_to_add) - 1)

            missions[slot] = missions_to_add.pop(filler)

        # Add hard missions into pool and fill in hard slots
        missions_to_add = missions_to_add + mission_pools['hard']
        for slot in hard_slots:
            filler = multiworld.random.randint(0, len(missions_to_add) - 1)

            missions[slot] = missions_to_add.pop(filler)

        # Loop through missions to create requirements table and connect regions
        # TODO: Handle 'and' connections
        mission_req_table = {}
        for i in range(len(missions)):
            connections = []
            for connection in mission_order[i].connect_to:
                if connection == -1:
                    connect(multiworld, player, names, "Menu", missions[i])
                else:
                    connect(multiworld, player, names, missions[connection], missions[i],
                            (lambda name, missions_req: (lambda state: state.has(f"Beat {name}", player) and
                                                                       state._sc2wol_cleared_missions(multiworld, player,
                                                                                                      missions_req)))
                            (missions[connection], mission_order[i].number))
                    connections.append(connection + 1)

            mission_req_table.update({missions[i]: MissionInfo(
                vanilla_mission_req_table[missions[i]].id, connections, mission_order[i].category,
                number=mission_order[i].number,
                completion_critical=mission_order[i].completion_critical,
                or_requirements=mission_order[i].or_requirements)})

        final_mission_id = vanilla_mission_req_table[final_mission].id
        return mission_req_table, final_mission_id, final_mission + ': Victory'


def throwIfAnyLocationIsNotAssignedToARegion(regions: List[Region], regionNames: Set[str]):
    existingRegions = set()

    for region in regions:
        existingRegions.add(region.name)

    if (regionNames - existingRegions):
        raise Exception("Starcraft: the following regions are used in locations: {}, but no such region exists".format(
            regionNames - existingRegions))


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
