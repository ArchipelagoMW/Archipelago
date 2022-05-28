from typing import List, Set, Dict, Tuple, Optional, Callable, NamedTuple
from BaseClasses import MultiWorld, Region, Entrance, Location, RegionType
from .Locations import LocationData
from .Options import get_option_value
from worlds.sc2wol.MissionTables import MissionInfo, vanilla_shuffle_order, vanilla_mission_req_table, \
    no_build_regions_list, easy_regions_list, medium_regions_list, hard_regions_list
import random


def create_regions(world: MultiWorld, player: int, locations: Tuple[LocationData, ...], location_cache: List[Location]):
    locations_per_region = get_locations_per_region(locations)

    regions = [
        create_region(world, player, locations_per_region, location_cache, "Menu"),
        create_region(world, player, locations_per_region, location_cache, "Liberation Day"),
        create_region(world, player, locations_per_region, location_cache, "The Outlaws"),
        create_region(world, player, locations_per_region, location_cache, "Zero Hour"),
        create_region(world, player, locations_per_region, location_cache, "Evacuation"),
        create_region(world, player, locations_per_region, location_cache, "Outbreak"),
        create_region(world, player, locations_per_region, location_cache, "Safe Haven"),
        create_region(world, player, locations_per_region, location_cache, "Haven's Fall"),
        create_region(world, player, locations_per_region, location_cache, "Smash and Grab"),
        create_region(world, player, locations_per_region, location_cache, "The Dig"),
        create_region(world, player, locations_per_region, location_cache, "The Moebius Factor"),
        create_region(world, player, locations_per_region, location_cache, "Supernova"),
        create_region(world, player, locations_per_region, location_cache, "Maw of the Void"),
        create_region(world, player, locations_per_region, location_cache, "Devil's Playground"),
        create_region(world, player, locations_per_region, location_cache, "Welcome to the Jungle"),
        create_region(world, player, locations_per_region, location_cache, "Breakout"),
        create_region(world, player, locations_per_region, location_cache, "Ghost of a Chance"),
        create_region(world, player, locations_per_region, location_cache, "The Great Train Robbery"),
        create_region(world, player, locations_per_region, location_cache, "Cutthroat"),
        create_region(world, player, locations_per_region, location_cache, "Engine of Destruction"),
        create_region(world, player, locations_per_region, location_cache, "Media Blitz"),
        create_region(world, player, locations_per_region, location_cache, "Piercing the Shroud"),
        create_region(world, player, locations_per_region, location_cache, "Whispers of Doom"),
        create_region(world, player, locations_per_region, location_cache, "A Sinister Turn"),
        create_region(world, player, locations_per_region, location_cache, "Echoes of the Future"),
        create_region(world, player, locations_per_region, location_cache, "In Utter Darkness"),
        create_region(world, player, locations_per_region, location_cache, "Gates of Hell"),
        create_region(world, player, locations_per_region, location_cache, "Belly of the Beast"),
        create_region(world, player, locations_per_region, location_cache, "Shatter the Sky"),
        create_region(world, player, locations_per_region, location_cache, "All-In")
    ]

    if __debug__:
        throwIfAnyLocationIsNotAssignedToARegion(regions, locations_per_region.keys())

    world.regions += regions

    names: Dict[str, int] = {}

    if get_option_value(world, player, "mission_order") == 0:
        connect(world, player, names, 'Menu', 'Liberation Day'),
        connect(world, player, names, 'Liberation Day', 'The Outlaws',
                lambda state: state.has("Beat Liberation Day", player)),
        connect(world, player, names, 'The Outlaws', 'Zero Hour',
                lambda state: state.has("Beat The Outlaws", player)),
        connect(world, player, names, 'Zero Hour', 'Evacuation',
                lambda state: state.has("Beat Zero Hour", player)),
        connect(world, player, names, 'Evacuation', 'Outbreak',
                lambda state: state.has("Beat Evacuation", player)),
        connect(world, player, names, "Outbreak", "Safe Haven",
                lambda state: state._sc2wol_cleared_missions(world, player, 7) and
                              state.has("Beat Outbreak", player)),
        connect(world, player, names, "Outbreak", "Haven's Fall",
                lambda state: state._sc2wol_cleared_missions(world, player, 7) and
                              state.has("Beat Outbreak", player)),
        connect(world, player, names, 'Zero Hour', 'Smash and Grab',
                lambda state: state.has("Beat Zero Hour", player)),
        connect(world, player, names, 'Smash and Grab', 'The Dig',
                lambda state: state._sc2wol_cleared_missions(world, player, 8) and
                              state.has("Beat Smash and Grab", player)),
        connect(world, player, names, 'The Dig', 'The Moebius Factor',
                lambda state: state._sc2wol_cleared_missions(world, player, 11) and
                              state.has("Beat The Dig", player)),
        connect(world, player, names, 'The Moebius Factor', 'Supernova',
                lambda state: state._sc2wol_cleared_missions(world, player, 14) and
                              state.has("Beat The Moebius Factor", player)),
        connect(world, player, names, 'Supernova', 'Maw of the Void',
                lambda state: state.has("Beat Supernova", player)),
        connect(world, player, names, 'Zero Hour', "Devil's Playground",
                lambda state: state._sc2wol_cleared_missions(world, player, 4) and
                              state.has("Beat Zero Hour", player)),
        connect(world, player, names, "Devil's Playground", 'Welcome to the Jungle',
                lambda state: state.has("Beat Devil's Playground", player)),
        connect(world, player, names, "Welcome to the Jungle", 'Breakout',
                lambda state: state._sc2wol_cleared_missions(world, player, 8) and
                              state.has("Beat Welcome to the Jungle", player)),
        connect(world, player, names, "Welcome to the Jungle", 'Ghost of a Chance',
                lambda state: state._sc2wol_cleared_missions(world, player, 8) and
                              state.has("Beat Welcome to the Jungle", player)),
        connect(world, player, names, "Zero Hour", 'The Great Train Robbery',
                lambda state: state._sc2wol_cleared_missions(world, player, 6) and
                              state.has("Beat Zero Hour", player)),
        connect(world, player, names, 'The Great Train Robbery', 'Cutthroat',
                lambda state: state.has("Beat The Great Train Robbery", player)),
        connect(world, player, names, 'Cutthroat', 'Engine of Destruction',
                lambda state: state.has("Beat Cutthroat", player)),
        connect(world, player, names, 'Engine of Destruction', 'Media Blitz',
                lambda state: state.has("Beat Engine of Destruction", player)),
        connect(world, player, names, 'Media Blitz', 'Piercing the Shroud',
                lambda state: state.has("Beat Media Blitz", player)),
        connect(world, player, names, 'The Dig', 'Whispers of Doom',
                lambda state: state.has("Beat The Dig", player)),
        connect(world, player, names, 'Whispers of Doom', 'A Sinister Turn',
                lambda state: state.has("Beat Whispers of Doom", player)),
        connect(world, player, names, 'A Sinister Turn', 'Echoes of the Future',
                lambda state: state.has("Beat A Sinister Turn", player)),
        connect(world, player, names, 'Echoes of the Future', 'In Utter Darkness',
                lambda state: state.has("Beat Echoes of the Future", player)),
        connect(world, player, names, 'Maw of the Void', 'Gates of Hell',
                lambda state: state.has("Beat Maw of the Void", player)),
        connect(world, player, names, 'Gates of Hell', 'Belly of the Beast',
                lambda state: state.has("Beat Gates of Hell", player)),
        connect(world, player, names, 'Gates of Hell', 'Shatter the Sky',
                lambda state: state.has("Beat Gates of Hell", player)),
        connect(world, player, names, 'Gates of Hell', 'All-In',
                lambda state: state.has('Beat Gates of Hell', player) and (
                        state.has('Beat Shatter the Sky', player) or state.has('Beat Belly of the Beast', player)))

        return vanilla_mission_req_table

    elif get_option_value(world, player, "mission_order") == 1:
        missions = []
        no_build_pool = no_build_regions_list[:]
        easy_pool = easy_regions_list[:]
        medium_pool = medium_regions_list[:]
        hard_pool = hard_regions_list[:]

        # Initial fill out of mission list and marking all-in mission
        for mission in vanilla_shuffle_order:
            if mission.type == "all_in":
                missions.append("All-In")
            else:
                missions.append(mission.type)

        # Place Protoss Missions if we are not using ShuffleProtoss
        if get_option_value(world, player, "shuffle_protoss") == 0:
            missions[22] = "A Sinister Turn"
            medium_pool.remove("A Sinister Turn")
            missions[23] = "Echoes of the Future"
            medium_pool.remove("Echoes of the Future")
            missions[24] = "In Utter Darkness"
            hard_pool.remove("In Utter Darkness")

        no_build_slots = []
        easy_slots = []
        medium_slots = []
        hard_slots = []

        # Search through missions to find slots needed to fill
        for i in range(len(missions)):
            if missions[i] == "no_build":
                no_build_slots.append(i)
            elif missions[i] == "easy":
                easy_slots.append(i)
            elif missions[i] == "medium":
                medium_slots.append(i)
            elif missions[i] == "hard":
                hard_slots.append(i)

        # Add no_build missions to the pool and fill in no_build slots
        missions_to_add = no_build_pool
        for slot in no_build_slots:
            filler = random.randint(0, len(missions_to_add)-1)

            missions[slot] = missions_to_add.pop(filler)

        # Add easy missions into pool and fill in easy slots
        missions_to_add = missions_to_add + easy_pool
        for slot in easy_slots:
            filler = random.randint(0, len(missions_to_add) - 1)

            missions[slot] = missions_to_add.pop(filler)

        # Add medium missions into pool and fill in medium slots
        missions_to_add = missions_to_add + medium_pool
        for slot in medium_slots:
            filler = random.randint(0, len(missions_to_add) - 1)

            missions[slot] = missions_to_add.pop(filler)

        # Add hard missions into pool and fill in hard slots
        missions_to_add = missions_to_add + hard_pool
        for slot in hard_slots:
            filler = random.randint(0, len(missions_to_add) - 1)

            missions[slot] = missions_to_add.pop(filler)

        # Loop through missions to create requirements table and connect regions
        # TODO: Handle 'and' connections
        mission_req_table = {}
        for i in range(len(missions)):
            connections = []
            for connection in vanilla_shuffle_order[i].connect_to:
                if connection == -1:
                    connect(world, player, names, "Menu", missions[i])
                else:
                    connect(world, player, names, missions[connection], missions[i],
                            (lambda name: (lambda state: state.has(f"Beat {name}", player)))(missions[connection]))
                    connections.append(connection + 1)

            mission_req_table.update({missions[i]: MissionInfo(
                vanilla_mission_req_table[missions[i]].id, vanilla_mission_req_table[missions[i]].extra_locations,
                connections, completion_critical=vanilla_shuffle_order[i].completion_critical,
                number=vanilla_shuffle_order[i].number, or_requirements=vanilla_shuffle_order[i].or_requirements)})

        return mission_req_table


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


def create_region(world: MultiWorld, player: int, locations_per_region: Dict[str, List[LocationData]],
                  location_cache: List[Location], name: str) -> Region:
    region = Region(name, RegionType.Generic, name, player)
    region.world = world

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
