from typing import List, Set, Dict, Tuple, Optional, Callable
from BaseClasses import CollectionState, MultiWorld, Region, Entrance, Location
from .Options import is_option_enabled
from .Locations import LocationData, get_location_datas
from .PreCalculatedWeights import PreCalculatedWeights
from .LogicExtensions import TimespinnerLogic


def create_regions_and_locations(world: MultiWorld, player: int, precalculated_weights: PreCalculatedWeights):
    region_names = [
        'Menu',
        "Tutorial",
        "Lake desolation",
        "Upper lake desolation",
        "Lower lake desolation",
        "Eastern lake desolation",
        "Library",
        "Library top",
        "Varndagroth tower left",
        "Varndagroth tower right (upper)",
        "Varndagroth tower right (lower)",
        "Varndagroth tower right (elevator)",
        "Sealed Caves (Sirens)",
        "Military Fortress",
        "Military Fortress (hangar)",
        "The lab",
        "The lab (power off)",
        "The lab (upper)",
        "Emperors tower",
        "Skeleton Shaft",
        "Sealed Caves (upper)",
        "Sealed Caves (Xarion)",
        "Refugee Camp",
        "Forest",
        "Left Side forest Caves",
        "Upper Lake Serene",
        "Lower Lake Serene",
        "Caves of Banishment (upper)",
        "Caves of Banishment (Maw)",
        "Caves of Banishment (Sirens)",
        "Castle Ramparts",
        "Castle Keep",
        "Castle Basement",
        "Royal towers (lower)",
        "Royal towers",
        "Royal towers (upper)",
        "Temporal Gyre",
        "Ancient Pyramid (entrance)",
        "Ancient Pyramid (left)",
        "Ancient Pyramid (right)",
        "Space time continuum"
    ]

    if is_option_enabled(world, player, "GyreArchives"):
        region_names.extend((
            "Ravenlord\'s Lair",
            "Ifrit\'s Lair"
        ))

    locationn_datas: List[LocationData] = get_location_datas(world, player, precalculated_weights)
    locations_per_region: Dict[str, List[LocationData]] = split_location_datas_per_region(locationn_datas)
    regions = create_regions(world, player, locations_per_region, region_names)

    if __debug__:
        throwIfAnyLocationIsNotAssignedToARegion(regions, locations_per_region.keys())

    world.regions.extend(regions.values())

    connectStartingRegion(world, player)

    flooded: PreCalculatedWeights = precalculated_weights
    logic = TimespinnerLogic(world, player, precalculated_weights)

    connect(player, regions, 'Lake desolation', 'Lower lake desolation', lambda state: logic.has_timestop(state) or state.has('Talaria Attachment', player) or flooded.flood_lake_desolation)
    connect(player, regions, 'Lake desolation', 'Upper lake desolation', lambda state: logic.has_fire(state) and state.can_reach('Upper Lake Serene', 'Region', player))
    connect(player, regions, 'Lake desolation', 'Skeleton Shaft', lambda state: logic.has_doublejump(state) or flooded.flood_lake_desolation)
    connect(player, regions, 'Lake desolation', 'Space time continuum', logic.has_teleport)
    connect(player, regions, 'Upper lake desolation', 'Lake desolation')
    connect(player, regions, 'Upper lake desolation', 'Eastern lake desolation')
    connect(player, regions, 'Lower lake desolation', 'Lake desolation') 
    connect(player, regions, 'Lower lake desolation', 'Eastern lake desolation')
    connect(player, regions, 'Eastern lake desolation', 'Space time continuum', logic.has_teleport)
    connect(player, regions, 'Eastern lake desolation', 'Library')
    connect(player, regions, 'Eastern lake desolation', 'Lower lake desolation')
    connect(player, regions, 'Eastern lake desolation', 'Upper lake desolation', lambda state: logic.has_fire(state) and state.can_reach('Upper Lake Serene', 'Region', player))
    connect(player, regions, 'Library', 'Eastern lake desolation')
    connect(player, regions, 'Library', 'Library top', lambda state: logic.has_doublejump(state) or state.has('Talaria Attachment', player)) 
    connect(player, regions, 'Library', 'Varndagroth tower left', logic.has_keycard_D)
    connect(player, regions, 'Library', 'Space time continuum', logic.has_teleport)
    connect(player, regions, 'Library top', 'Library')
    connect(player, regions, 'Varndagroth tower left', 'Library')
    connect(player, regions, 'Varndagroth tower left', 'Varndagroth tower right (upper)', logic.has_keycard_C)
    connect(player, regions, 'Varndagroth tower left', 'Varndagroth tower right (lower)', logic.has_keycard_B)
    connect(player, regions, 'Varndagroth tower left', 'Sealed Caves (Sirens)', lambda state: logic.has_keycard_B(state) and state.has('Elevator Keycard', player))
    connect(player, regions, 'Varndagroth tower left', 'Refugee Camp', lambda state: state.has('Timespinner Wheel', player) and state.has('Timespinner Spindle', player))
    connect(player, regions, 'Varndagroth tower right (upper)', 'Varndagroth tower left')
    connect(player, regions, 'Varndagroth tower right (upper)', 'Varndagroth tower right (elevator)', lambda state: state.has('Elevator Keycard', player))
    connect(player, regions, 'Varndagroth tower right (elevator)', 'Varndagroth tower right (upper)')
    connect(player, regions, 'Varndagroth tower right (elevator)', 'Varndagroth tower right (lower)')
    connect(player, regions, 'Varndagroth tower right (lower)', 'Varndagroth tower left', logic.has_keycard_B)
    connect(player, regions, 'Varndagroth tower right (lower)', 'Varndagroth tower right (elevator)', lambda state: state.has('Elevator Keycard', player))
    connect(player, regions, 'Varndagroth tower right (lower)', 'Sealed Caves (Sirens)', lambda state: logic.has_keycard_B(state) and state.has('Elevator Keycard', player))
    connect(player, regions, 'Varndagroth tower right (lower)', 'Military Fortress', logic.can_kill_all_3_bosses)
    connect(player, regions, 'Varndagroth tower right (lower)', 'Space time continuum', logic.has_teleport)
    connect(player, regions, 'Sealed Caves (Sirens)', 'Varndagroth tower left', lambda state: state.has('Elevator Keycard', player))
    connect(player, regions, 'Sealed Caves (Sirens)', 'Varndagroth tower right (lower)', lambda state: state.has('Elevator Keycard', player))
    connect(player, regions, 'Sealed Caves (Sirens)', 'Space time continuum', logic.has_teleport)
    connect(player, regions, 'Military Fortress', 'Varndagroth tower right (lower)', logic.can_kill_all_3_bosses)
    connect(player, regions, 'Military Fortress', 'Temporal Gyre', lambda state: state.has('Timespinner Wheel', player))
    connect(player, regions, 'Military Fortress', 'Military Fortress (hangar)', logic.has_doublejump)
    connect(player, regions, 'Military Fortress (hangar)', 'Military Fortress')
    connect(player, regions, 'Military Fortress (hangar)', 'The lab', lambda state: logic.has_keycard_B(state) and logic.has_doublejump(state))
    connect(player, regions, 'Temporal Gyre', 'Military Fortress')
    connect(player, regions, 'The lab', 'Military Fortress')
    connect(player, regions, 'The lab', 'The lab (power off)', logic.has_doublejump_of_npc)
    connect(player, regions, 'The lab (power off)', 'The lab')
    connect(player, regions, 'The lab (power off)', 'The lab (upper)', logic.has_forwarddash_doublejump)
    connect(player, regions, 'The lab (upper)', 'The lab (power off)')
    connect(player, regions, 'The lab (upper)', 'Emperors tower', logic.has_forwarddash_doublejump)
    connect(player, regions, 'The lab (upper)', 'Ancient Pyramid (entrance)', lambda state: state.has_all({'Timespinner Wheel', 'Timespinner Spindle', 'Timespinner Gear 1', 'Timespinner Gear 2', 'Timespinner Gear 3'}, player))
    connect(player, regions, 'Emperors tower', 'The lab (upper)')
    connect(player, regions, 'Skeleton Shaft', 'Lake desolation')
    connect(player, regions, 'Skeleton Shaft', 'Sealed Caves (upper)', logic.has_keycard_A)
    connect(player, regions, 'Skeleton Shaft', 'Space time continuum', logic.has_teleport)
    connect(player, regions, 'Sealed Caves (upper)', 'Skeleton Shaft')
    connect(player, regions, 'Sealed Caves (upper)', 'Sealed Caves (Xarion)', lambda state: logic.has_teleport(state) or logic.has_doublejump(state))
    connect(player, regions, 'Sealed Caves (Xarion)', 'Sealed Caves (upper)', logic.has_doublejump)
    connect(player, regions, 'Sealed Caves (Xarion)', 'Space time continuum', logic.has_teleport)
    connect(player, regions, 'Refugee Camp', 'Forest')
    #connect(player, regions, 'Refugee Camp', 'Library', lambda state: not is_option_enabled(player, regions, "Inverted"))
    connect(player, regions, 'Refugee Camp', 'Space time continuum', logic.has_teleport)
    connect(player, regions, 'Forest', 'Refugee Camp')
    connect(player, regions, 'Forest', 'Left Side forest Caves', lambda state: state.has('Talaria Attachment', player) or logic.has_timestop(state))
    connect(player, regions, 'Forest', 'Caves of Banishment (Sirens)')
    connect(player, regions, 'Forest', 'Castle Ramparts')
    connect(player, regions, 'Left Side forest Caves', 'Forest')
    connect(player, regions, 'Left Side forest Caves', 'Upper Lake Serene', logic.has_timestop)
    connect(player, regions, 'Left Side forest Caves', 'Lower Lake Serene', lambda state: state.has('Water Mask', player) or flooded.dry_lake_serene)
    connect(player, regions, 'Left Side forest Caves', 'Space time continuum', logic.has_teleport)
    connect(player, regions, 'Upper Lake Serene', 'Left Side forest Caves')
    connect(player, regions, 'Upper Lake Serene', 'Lower Lake Serene', lambda state: state.has('Water Mask', player) or flooded.dry_lake_serene)
    connect(player, regions, 'Lower Lake Serene', 'Upper Lake Serene')
    connect(player, regions, 'Lower Lake Serene', 'Left Side forest Caves')
    connect(player, regions, 'Lower Lake Serene', 'Caves of Banishment (upper)', lambda state: not flooded.dry_lake_serene or logic.has_doublejump(state))
    connect(player, regions, 'Caves of Banishment (upper)', 'Upper Lake Serene', lambda state: state.has('Water Mask', player) or flooded.dry_lake_serene)
    connect(player, regions, 'Caves of Banishment (upper)', 'Caves of Banishment (Maw)', lambda state: logic.has_doublejump(state) or state.has_any({'Gas Mask', 'Talaria Attachment'} or logic.has_teleport(state), player))
    connect(player, regions, 'Caves of Banishment (upper)', 'Space time continuum', logic.has_teleport)
    connect(player, regions, 'Caves of Banishment (Maw)', 'Caves of Banishment (upper)', lambda state: logic.has_doublejump(state) if not flooded.flood_maw else state.has('Water Mask', player))
    connect(player, regions, 'Caves of Banishment (Maw)', 'Caves of Banishment (Sirens)', lambda state: state.has_any({'Gas Mask', 'Talaria Attachment'}, player) )
    connect(player, regions, 'Caves of Banishment (Maw)', 'Space time continuum', logic.has_teleport)
    connect(player, regions, 'Caves of Banishment (Sirens)', 'Forest')
    connect(player, regions, 'Castle Ramparts', 'Forest')
    connect(player, regions, 'Castle Ramparts', 'Castle Keep')
    connect(player, regions, 'Castle Ramparts', 'Space time continuum', logic.has_teleport)
    connect(player, regions, 'Castle Keep', 'Castle Ramparts')
    connect(player, regions, 'Castle Keep', 'Castle Basement', lambda state: state.has('Water Mask', player) or not flooded.flood_basement)
    connect(player, regions, 'Castle Keep', 'Royal towers (lower)', logic.has_doublejump)
    connect(player, regions, 'Castle Keep', 'Space time continuum', logic.has_teleport)
    connect(player, regions, 'Royal towers (lower)', 'Castle Keep')
    connect(player, regions, 'Royal towers (lower)', 'Royal towers', lambda state: state.has('Timespinner Wheel', player) or logic.has_forwarddash_doublejump(state))
    connect(player, regions, 'Royal towers (lower)', 'Space time continuum', logic.has_teleport)
    connect(player, regions, 'Royal towers', 'Royal towers (lower)')
    connect(player, regions, 'Royal towers', 'Royal towers (upper)', logic.has_doublejump)
    connect(player, regions, 'Royal towers (upper)', 'Royal towers')
    #connect(player, regions, 'Ancient Pyramid (entrance)', 'The lab (upper)', lambda state: not is_option_enabled(player, regions, "EnterSandman"))
    connect(player, regions, 'Ancient Pyramid (entrance)', 'Ancient Pyramid (left)', logic.has_doublejump)
    connect(player, regions, 'Ancient Pyramid (left)', 'Ancient Pyramid (entrance)')
    connect(player, regions, 'Ancient Pyramid (left)', 'Ancient Pyramid (right)', lambda state: logic.has_upwarddash(state) or flooded.flood_pyramid_shaft)
    connect(player, regions, 'Ancient Pyramid (right)', 'Ancient Pyramid (left)', lambda state: logic.has_upwarddash(state) or flooded.flood_pyramid_shaft)
    connect(player, regions, 'Space time continuum', 'Lake desolation', lambda state: logic.can_teleport_to(state, "Present", "GateLakeDesolation"))
    connect(player, regions, 'Space time continuum', 'Lower lake desolation', lambda state: logic.can_teleport_to(state, "Present", "GateKittyBoss"))
    connect(player, regions, 'Space time continuum', 'Library', lambda state: logic.can_teleport_to(state, "Present", "GateLeftLibrary"))
    connect(player, regions, 'Space time continuum', 'Varndagroth tower right (lower)', lambda state: logic.can_teleport_to(state, "Present", "GateMilitaryGate"))
    connect(player, regions, 'Space time continuum', 'Skeleton Shaft', lambda state: logic.can_teleport_to(state, "Present", "GateSealedCaves"))
    connect(player, regions, 'Space time continuum', 'Sealed Caves (Sirens)', lambda state: logic.can_teleport_to(state, "Present", "GateSealedSirensCave"))
    connect(player, regions, 'Space time continuum', 'Upper Lake Serene', lambda state: logic.can_teleport_to(state, "Past", "GateLakeSereneLeft"))
    connect(player, regions, 'Space time continuum', 'Left Side forest Caves', lambda state: logic.can_teleport_to(state, "Past", "GateLakeSereneRight"))
    connect(player, regions, 'Space time continuum', 'Refugee Camp', lambda state: logic.can_teleport_to(state, "Past", "GateAccessToPast"))
    connect(player, regions, 'Space time continuum', 'Castle Ramparts', lambda state: logic.can_teleport_to(state, "Past", "GateCastleRamparts"))
    connect(player, regions, 'Space time continuum', 'Castle Keep', lambda state: logic.can_teleport_to(state, "Past", "GateCastleKeep"))
    connect(player, regions, 'Space time continuum', 'Royal towers (lower)', lambda state: logic.can_teleport_to(state, "Past", "GateRoyalTowers"))
    connect(player, regions, 'Space time continuum', 'Caves of Banishment (Maw)', lambda state: logic.can_teleport_to(state, "Past", "GateMaw"))
    connect(player, regions, 'Space time continuum', 'Caves of Banishment (upper)', lambda state: logic.can_teleport_to(state, "Past", "GateCavesOfBanishment"))
    connect(player, regions, 'Space time continuum', 'Ancient Pyramid (entrance)', lambda state: logic.can_teleport_to(state, "Time", "GateGyre") or (not is_option_enabled(player, regions, "UnchainedKeys") and is_option_enabled(player, regions, "EnterSandman")))
    connect(player, regions, 'Space time continuum', 'Ancient Pyramid (left)', lambda state: logic.can_teleport_to(state, "Time", "GateLeftPyramid"))
    connect(player, regions, 'Space time continuum', 'Ancient Pyramid (right)', lambda state: logic.can_teleport_to(state, "Time", "GateRightPyramid"))

    if is_option_enabled(player, regions, "GyreArchives"):
        connect(player, regions, 'The lab (upper)', 'Ravenlord\'s Lair', lambda state: state.has('Merchant Crow', player))
        connect(player, regions, 'Ravenlord\'s Lair', 'The lab (upper)')
        connect(player, regions, 'Library top', 'Ifrit\'s Lair', lambda state: state.has('Kobo', player) and state.can_reach('Refugee Camp', 'Region', player))
        connect(player, regions, 'Ifrit\'s Lair', 'Library top')


def throwIfAnyLocationIsNotAssignedToARegion(regions: List[Region], regionNames: Set[str]):
    existingRegions: Set[str] = set()

    for region in regions:
        existingRegions.add(region.name)

    if (regionNames - existingRegions):
        raise Exception("Timespinner: the following regions are used in locations: {}, but no such region exists".format(regionNames - existingRegions))


def create_location(player: int, location_data: LocationData, region: Region) -> Location:
    location = Location(player, location_data.name, location_data.code, region)

    if (location_data.rule):
        location.access_rule = location_data.rule

    if id is None:
        location.event = True
        location.locked = True

    return location


def create_regions(world: MultiWorld, player: int, locations_per_region: Dict[str, List[LocationData]],
                    region_names: List[str]) -> Dict[str, Region]:
    
    regions: Dict[str, Region] = {}

    for name in region_names:
        regions[name] = create_region(world, player, locations_per_region, name)

    return regions


def create_region(world: MultiWorld, player: int, locations_per_region: Dict[str, List[LocationData]], name: str) -> Region:
    region = Region(name, player, world)

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region)
            region.locations.append(location)

    return region


def connectStartingRegion(world: MultiWorld, player: int, regions: Dict[str, Region]):
    menu = regions["Menu"]
    tutorial = regions["Tutorial"]
    space_time_continuum = regions["Space time continuum"]

    if is_option_enabled(world, player, "Inverted"):
        starting_region = regions["Refugee Camp"]
    else:
        starting_region = regions["Lake desolation"]

    menu_to_tutorial = Entrance(player, 'Tutorial', menu)
    menu_to_tutorial.connect(tutorial)
    menu.exits.append(menu_to_tutorial)

    tutorial_to_start = Entrance(player, 'Start Game', tutorial)
    tutorial_to_start.connect(starting_region)
    tutorial.exits.append(tutorial_to_start)

    teleport_back_to_start = Entrance(player, 'Teleport back to start', space_time_continuum)
    teleport_back_to_start.connect(starting_region)
    space_time_continuum.exits.append(teleport_back_to_start)


def connect(player: int, regions: Dict[str, Region], source: str, target: str,
            rule: Optional[Callable[[CollectionState], bool]] = None):
    
    sourceRegion = regions[source]
    targetRegion = regions[target]

    connection = Entrance(player, "", sourceRegion)

    if rule:
        connection.access_rule = rule

    sourceRegion.exits.append(connection)
    connection.connect(targetRegion)


def split_location_datas_per_region(locations: List[LocationData]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]]  = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region
