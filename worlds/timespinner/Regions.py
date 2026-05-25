from typing import List, Set, Dict, Optional, Callable
from BaseClasses import CollectionState, MultiWorld, Region, Entrance, Location
from .Options import TimespinnerOptions
from .Locations import LocationData, get_location_datas
from .PreCalculatedWeights import PreCalculatedWeights
from .LogicExtensions import TimespinnerLogic


def create_regions_and_locations(multiworld: MultiWorld, player: int, options: TimespinnerOptions,
                                 precalculated_weights: PreCalculatedWeights):

    locations_per_region: Dict[str, List[LocationData]] = split_location_datas_per_region(
        get_location_datas(player, options, precalculated_weights))

    regions = [
        create_region(multiworld, player, locations_per_region, 'Menu'),
        create_region(multiworld, player, locations_per_region, 'Tutorial'),
        create_region(multiworld, player, locations_per_region, 'Lake desolation'),
        create_region(multiworld, player, locations_per_region, 'Upper lake desolation'),
        create_region(multiworld, player, locations_per_region, 'Lower lake desolation'),
        create_region(multiworld, player, locations_per_region, 'Eastern lake desolation'),
        create_region(multiworld, player, locations_per_region, 'Library'),
        create_region(multiworld, player, locations_per_region, 'Library top'),
        create_region(multiworld, player, locations_per_region, 'Varndagroth tower left'),
        create_region(multiworld, player, locations_per_region, 'Varndagroth tower right (upper)'),
        create_region(multiworld, player, locations_per_region, 'Varndagroth tower right (lower)'),
        create_region(multiworld, player, locations_per_region, 'Varndagroth tower right (elevator)'),
        create_region(multiworld, player, locations_per_region, 'Sealed Caves (Sirens)'),
        create_region(multiworld, player, locations_per_region, 'Military Fortress'),
        create_region(multiworld, player, locations_per_region, 'Military Fortress (hangar)'),
        create_region(multiworld, player, locations_per_region, 'Lab Entrance'),
        create_region(multiworld, player, locations_per_region, 'Main Lab'),
        create_region(multiworld, player, locations_per_region, 'Lab Research'),
        create_region(multiworld, player, locations_per_region, 'The lab (upper)'),
        create_region(multiworld, player, locations_per_region, 'Emperors tower (courtyard)'),
        create_region(multiworld, player, locations_per_region, 'Emperors tower'),
        create_region(multiworld, player, locations_per_region, 'Skeleton Shaft'),
        create_region(multiworld, player, locations_per_region, 'Sealed Caves (Xarion)'),
        create_region(multiworld, player, locations_per_region, 'Refugee Camp'),
        create_region(multiworld, player, locations_per_region, 'Forest'),
        create_region(multiworld, player, locations_per_region, 'Left Side forest Caves'),
        create_region(multiworld, player, locations_per_region, 'Upper Lake Serene'),
        create_region(multiworld, player, locations_per_region, 'Lower Lake Serene'),
        create_region(multiworld, player, locations_per_region, 'Caves of Banishment (upper)'),
        create_region(multiworld, player, locations_per_region, 'Caves of Banishment (Maw)'),
        create_region(multiworld, player, locations_per_region, 'Caves of Banishment (Flooded)'),
        create_region(multiworld, player, locations_per_region, 'Caves of Banishment (Sirens)'),
        create_region(multiworld, player, locations_per_region, 'Castle Ramparts'),
        create_region(multiworld, player, locations_per_region, 'Castle Keep'),
        create_region(multiworld, player, locations_per_region, 'Castle Basement'),
        create_region(multiworld, player, locations_per_region, 'Royal towers (lower)'),
        create_region(multiworld, player, locations_per_region, 'Royal towers'),
        create_region(multiworld, player, locations_per_region, 'Royal towers (upper)'),
        create_region(multiworld, player, locations_per_region, 'Temporal Gyre'),
        create_region(multiworld, player, locations_per_region, 'Ancient Pyramid (entrance)'),
        create_region(multiworld, player, locations_per_region, 'Ancient Pyramid (left)'),
        create_region(multiworld, player, locations_per_region, 'Ancient Pyramid (right)'),
        create_region(multiworld, player, locations_per_region, 'Space time continuum')
    ]

    if options.gyre_archives:
        regions.extend([
            create_region(multiworld, player, locations_per_region, 'Ravenlord\'s Lair'),
            create_region(multiworld, player, locations_per_region, 'Ifrit\'s Lair'),
        ])

    if __debug__:
        throwIfAnyLocationIsNotAssignedToARegion(regions, locations_per_region.keys())

    multiworld.regions += regions

    connectStartingRegion(multiworld, player, options)

    flooded: PreCalculatedWeights = precalculated_weights
    logic = TimespinnerLogic(player, options, precalculated_weights)

    connect(multiworld, player, 'Lake desolation', 'Lower lake desolation', lambda state: flooded.flood_lake_desolation or logic.has_timestop(state) or state.has('Talaria Attachment', player))
    connect(multiworld, player, 'Lake desolation', 'Upper lake desolation', lambda state: logic.has_fire(state) and state.can_reach('Upper Lake Serene', 'Region', player), "Upper Lake Serene")
    connect(multiworld, player, 'Lake desolation', 'Skeleton Shaft', lambda state: flooded.flood_lake_desolation or logic.has_doublejump(state))
    connect(multiworld, player, 'Lake desolation', 'Space time continuum', logic.has_teleport)
    connect(multiworld, player, 'Upper lake desolation', 'Lake desolation')
    connect(multiworld, player, 'Upper lake desolation', 'Eastern lake desolation')
    connect(multiworld, player, 'Lower lake desolation', 'Lake desolation')
    connect(multiworld, player, 'Lower lake desolation', 'Eastern lake desolation')
    connect(multiworld, player, 'Eastern lake desolation', 'Space time continuum', logic.has_teleport)
    connect(multiworld, player, 'Eastern lake desolation', 'Library')
    connect(multiworld, player, 'Eastern lake desolation', 'Lower lake desolation')
    connect(multiworld, player, 'Eastern lake desolation', 'Upper lake desolation', lambda state: logic.has_fire(state) and state.can_reach('Upper Lake Serene', 'Region', player), "Upper Lake Serene")
    connect(multiworld, player, 'Library', 'Eastern lake desolation')
    connect(multiworld, player, 'Library', 'Library top', lambda state: logic.has_doublejump(state) or state.has('Talaria Attachment', player))
    connect(multiworld, player, 'Library', 'Varndagroth tower left', logic.has_keycard_D)
    connect(multiworld, player, 'Library', 'Space time continuum', logic.has_teleport)
    connect(multiworld, player, 'Library top', 'Library')
    connect(multiworld, player, 'Varndagroth tower left', 'Library')
    connect(multiworld, player, 'Varndagroth tower left', 'Varndagroth tower right (upper)', logic.has_keycard_C)
    connect(multiworld, player, 'Varndagroth tower left', 'Varndagroth tower right (lower)', logic.has_keycard_B)
    connect(multiworld, player, 'Varndagroth tower left', 'Sealed Caves (Sirens)', lambda state: logic.has_keycard_B(state) and state.has('Elevator Keycard', player))
    connect(multiworld, player, 'Varndagroth tower left', 'Refugee Camp', lambda state: state.has('Timespinner Wheel', player) and state.has('Timespinner Spindle', player))
    connect(multiworld, player, 'Varndagroth tower right (upper)', 'Varndagroth tower left')
    connect(multiworld, player, 'Varndagroth tower right (upper)', 'Varndagroth tower right (elevator)', lambda state: state.has('Elevator Keycard', player))
    connect(multiworld, player, 'Varndagroth tower right (elevator)', 'Varndagroth tower right (upper)')
    connect(multiworld, player, 'Varndagroth tower right (elevator)', 'Varndagroth tower right (lower)')
    connect(multiworld, player, 'Varndagroth tower right (lower)', 'Varndagroth tower left', logic.has_keycard_B)
    connect(multiworld, player, 'Varndagroth tower right (lower)', 'Varndagroth tower right (elevator)', lambda state: state.has('Elevator Keycard', player))
    connect(multiworld, player, 'Varndagroth tower right (lower)', 'Sealed Caves (Sirens)', lambda state: logic.has_keycard_B(state) and state.has('Elevator Keycard', player))
    connect(multiworld, player, 'Varndagroth tower right (lower)', 'Military Fortress', logic.can_kill_all_3_bosses)
    connect(multiworld, player, 'Varndagroth tower right (lower)', 'Space time continuum', logic.has_teleport)
    connect(multiworld, player, 'Sealed Caves (Sirens)', 'Varndagroth tower left', lambda state: state.has('Elevator Keycard', player))
    connect(multiworld, player, 'Sealed Caves (Sirens)', 'Varndagroth tower right (lower)', lambda state: state.has('Elevator Keycard', player))
    connect(multiworld, player, 'Sealed Caves (Sirens)', 'Space time continuum', logic.has_teleport)
    connect(multiworld, player, 'Military Fortress', 'Varndagroth tower right (lower)', logic.can_kill_all_3_bosses)
    connect(multiworld, player, 'Military Fortress', 'Temporal Gyre', lambda state: state.has('Timespinner Wheel', player) and logic.can_kill_all_3_bosses(state))
    connect(multiworld, player, 'Military Fortress', 'Military Fortress (hangar)', logic.has_doublejump)
    connect(multiworld, player, 'Military Fortress (hangar)', 'Military Fortress')
    connect(multiworld, player, 'Military Fortress (hangar)', 'Lab Entrance', lambda state: state.has('Water Mask', player) if flooded.flood_lab else logic.has_doublejump(state))
    connect(multiworld, player, 'Lab Entrance', 'Main Lab', lambda state: logic.has_keycard_B(state))
    connect(multiworld, player, 'Main Lab', 'Lab Entrance')
    connect(multiworld, player, 'Lab Entrance', 'Military Fortress (hangar)')
    connect(multiworld, player, 'Temporal Gyre', 'Military Fortress')
    connect(multiworld, player, 'Main Lab', 'Lab Research', lambda state: state.has('Lab Access Research', player) if options.lock_key_amadeus else logic.has_doublejump_of_npc(state))
    connect(multiworld, player, 'Main Lab', 'The lab (upper)', lambda state: logic.has_forwarddash_doublejump(state) and ((not options.lock_key_amadeus) or state.has('Lab Access Genza', player)))
    connect(multiworld, player, 'The lab (upper)', 'Main Lab', lambda state: options.lock_key_amadeus and state.has('Lab Access Genza', player))
    connect(multiworld, player, 'The lab (upper)', 'Emperors tower (courtyard)', logic.has_forwarddash_doublejump)
    connect(multiworld, player, 'The lab (upper)', 'Ancient Pyramid (entrance)', lambda state: state.has_all({'Timespinner Wheel', 'Timespinner Spindle', 'Timespinner Gear 1', 'Timespinner Gear 2', 'Timespinner Gear 3'}, player))
    connect(multiworld, player, 'Emperors tower (courtyard)', 'The lab (upper)')
    connect(multiworld, player, 'Emperors tower (courtyard)', 'Emperors tower', logic.has_doublejump)
    connect(multiworld, player, 'Emperors tower', 'Emperors tower (courtyard)')
    connect(multiworld, player, 'Skeleton Shaft', 'Lake desolation')
    connect(multiworld, player, 'Skeleton Shaft', 'Sealed Caves (Xarion)', logic.has_keycard_A)
    connect(multiworld, player, 'Skeleton Shaft', 'Space time continuum', logic.has_teleport)
    connect(multiworld, player, 'Sealed Caves (Xarion)', 'Skeleton Shaft')
    connect(multiworld, player, 'Sealed Caves (Xarion)', 'Space time continuum', logic.has_teleport)
    connect(multiworld, player, 'Refugee Camp', 'Forest')
    connect(multiworld, player, 'Refugee Camp', 'Library', lambda state: (options.pyramid_start or options.inverted) and options.back_to_the_future and state.has_all({'Timespinner Wheel', 'Timespinner Spindle'}, player))
    connect(multiworld, player, 'Refugee Camp', 'Space time continuum', logic.has_teleport)
    connect(multiworld, player, 'Forest', 'Refugee Camp')
    connect(multiworld, player, 'Forest', 'Left Side forest Caves', lambda state: flooded.flood_lake_serene_bridge or state.has('Talaria Attachment', player) or logic.has_timestop(state))
    connect(multiworld, player, 'Forest', 'Caves of Banishment (Sirens)')
    connect(multiworld, player, 'Forest', 'Castle Ramparts', lambda state: not options.gate_keep or state.has('Drawbridge Key', player) or logic.has_upwarddash(state))
    connect(multiworld, player, 'Left Side forest Caves', 'Forest')
    connect(multiworld, player, 'Left Side forest Caves', 'Upper Lake Serene', logic.has_timestop)
    connect(multiworld, player, 'Left Side forest Caves', 'Lower Lake Serene', lambda state: not flooded.flood_lake_serene or state.has('Water Mask', player))
    connect(multiworld, player, 'Left Side forest Caves', 'Space time continuum', logic.has_teleport)
    connect(multiworld, player, 'Upper Lake Serene', 'Left Side forest Caves')
    connect(multiworld, player, 'Upper Lake Serene', 'Lower Lake Serene', lambda state: not flooded.flood_lake_serene or state.has('Water Mask', player))
    connect(multiworld, player, 'Lower Lake Serene', 'Upper Lake Serene')
    connect(multiworld, player, 'Lower Lake Serene', 'Left Side forest Caves')
    connect(multiworld, player, 'Lower Lake Serene', 'Caves of Banishment (upper)', lambda state: flooded.flood_lake_serene or logic.has_doublejump(state))
    connect(multiworld, player, 'Caves of Banishment (upper)', 'Lower Lake Serene', lambda state: not flooded.flood_lake_serene or state.has('Water Mask', player))
    connect(multiworld, player, 'Caves of Banishment (upper)', 'Caves of Banishment (Maw)', lambda state: not flooded.flood_maw or state.has('Water Mask', player))
    connect(multiworld, player, 'Caves of Banishment (upper)', 'Space time continuum', logic.has_teleport)
    connect(multiworld, player, 'Caves of Banishment (Maw)', 'Caves of Banishment (upper)', lambda state: logic.has_doublejump(state) if not flooded.flood_maw else state.has('Water Mask', player))
    connect(multiworld, player, 'Caves of Banishment (Maw)', 'Caves of Banishment (Sirens)', lambda state: state.has_any({'Gas Mask', 'Talaria Attachment'}, player) )
    connect(multiworld, player, 'Caves of Banishment (Maw)', 'Caves of Banishment (Flooded)', lambda state: flooded.flood_maw or state.has('Water Mask', player))
    connect(multiworld, player, 'Caves of Banishment (Maw)', 'Space time continuum', logic.has_teleport)
    connect(multiworld, player, 'Caves of Banishment (Sirens)', 'Forest')
    connect(multiworld, player, 'Castle Ramparts', 'Forest')
    connect(multiworld, player, 'Castle Ramparts', 'Castle Keep')
    connect(multiworld, player, 'Castle Ramparts', 'Space time continuum', logic.has_teleport)
    connect(multiworld, player, 'Castle Keep', 'Castle Ramparts')
    connect(multiworld, player, 'Castle Keep', 'Castle Basement', lambda state: not flooded.flood_basement or state.has('Water Mask', player))
    connect(multiworld, player, 'Castle Keep', 'Royal towers (lower)', lambda state: logic.has_doublejump(state) and (not options.royal_roadblock or logic.has_pink(state)))
    connect(multiworld, player, 'Castle Keep', 'Space time continuum', logic.has_teleport)
    connect(multiworld, player, 'Royal towers (lower)', 'Castle Keep')
    connect(multiworld, player, 'Royal towers (lower)', 'Royal towers', lambda state: state.has('Timespinner Wheel', player) or logic.has_forwarddash_doublejump(state))
    connect(multiworld, player, 'Royal towers (lower)', 'Space time continuum', logic.has_teleport)
    connect(multiworld, player, 'Royal towers', 'Royal towers (lower)')
    connect(multiworld, player, 'Royal towers', 'Royal towers (upper)', logic.has_doublejump)
    connect(multiworld, player, 'Royal towers (upper)', 'Royal towers')
    #connect(multiworld, player, 'Ancient Pyramid (entrance)', 'The lab (upper)', lambda state: not is_option_enabled(multiworld, player, "EnterSandman"))
    connect(multiworld, player, 'Ancient Pyramid (entrance)', 'Ancient Pyramid (left)', logic.has_doublejump)
    connect(multiworld, player, 'Ancient Pyramid (entrance)', 'Space time continuum', logic.has_teleport)
    connect(multiworld, player, 'Ancient Pyramid (left)', 'Ancient Pyramid (entrance)')
    connect(multiworld, player, 'Ancient Pyramid (left)', 'Ancient Pyramid (right)', lambda state: flooded.flood_pyramid_shaft or logic.has_upwarddash(state))
    connect(multiworld, player, 'Ancient Pyramid (left)', 'Space time continuum', logic.has_teleport)
    connect(multiworld, player, 'Ancient Pyramid (right)', 'Ancient Pyramid (left)', lambda state: flooded.flood_pyramid_shaft or logic.has_upwarddash(state))
    connect(multiworld, player, 'Ancient Pyramid (right)', 'Space time continuum', logic.has_teleport)
    connect(multiworld, player, 'Space time continuum', 'Lake desolation', lambda state: logic.can_teleport_to(state, "Present", "GateLakeDesolation"))
    connect(multiworld, player, 'Space time continuum', 'Lower lake desolation', lambda state: logic.can_teleport_to(state, "Present", "GateKittyBoss"))
    connect(multiworld, player, 'Space time continuum', 'Library', lambda state: logic.can_teleport_to(state, "Present", "GateLeftLibrary"))
    connect(multiworld, player, 'Space time continuum', 'Varndagroth tower right (lower)', lambda state: logic.can_teleport_to(state, "Present", "GateMilitaryGate"))
    connect(multiworld, player, 'Space time continuum', 'Skeleton Shaft', lambda state: logic.can_teleport_to(state, "Present", "GateSealedCaves"))
    connect(multiworld, player, 'Space time continuum', 'Sealed Caves (Sirens)', lambda state: logic.can_teleport_to(state, "Present", "GateSealedSirensCave"))
    connect(multiworld, player, 'Space time continuum', 'Sealed Caves (Xarion)', lambda state: logic.can_teleport_to(state, "Present", "GateXarion"))
    connect(multiworld, player, 'Space time continuum', 'Upper Lake Serene', lambda state: logic.can_teleport_to(state, "Past", "GateLakeSereneLeft"))
    connect(multiworld, player, 'Space time continuum', 'Left Side forest Caves', lambda state: logic.can_teleport_to(state, "Past", "GateLakeSereneRight"))
    connect(multiworld, player, 'Space time continuum', 'Refugee Camp', lambda state: logic.can_teleport_to(state, "Past", "GateAccessToPast"))
    connect(multiworld, player, 'Space time continuum', 'Forest', lambda state: logic.can_teleport_to(state, "Past", "GateCastleRamparts"))
    connect(multiworld, player, 'Space time continuum', 'Castle Keep', lambda state: logic.can_teleport_to(state, "Past", "GateCastleKeep"))
    connect(multiworld, player, 'Space time continuum', 'Royal towers (lower)', lambda state: logic.can_teleport_to(state, "Past", "GateRoyalTowers"))
    connect(multiworld, player, 'Space time continuum', 'Caves of Banishment (Maw)', lambda state: logic.can_teleport_to(state, "Past", "GateMaw"))
    connect(multiworld, player, 'Space time continuum', 'Caves of Banishment (upper)', lambda state: logic.can_teleport_to(state, "Past", "GateCavesOfBanishment"))
    connect(multiworld, player, 'Space time continuum', 'Military Fortress (hangar)', lambda state: logic.can_teleport_to(state, "Present", "GateLabEntrance"))
    connect(multiworld, player, 'Space time continuum', 'The lab (upper)', lambda state: logic.can_teleport_to(state, "Present", "GateDadsTower"))
    connect(multiworld, player, 'Space time continuum', 'Ancient Pyramid (entrance)', lambda state: logic.can_teleport_to(state, "Time", "GateGyre") or logic.can_teleport_to(state, "Time", "GateLeftPyramid") or (not options.unchained_keys and options.enter_sandman))
    connect(multiworld, player, 'Space time continuum', 'Ancient Pyramid (right)', lambda state: logic.can_teleport_to(state, "Time", "GateRightPyramid"))

    if options.gyre_archives:
        connect(multiworld, player, 'The lab (upper)', 'Ravenlord\'s Lair', lambda state: state.has('Merchant Crow', player))
        connect(multiworld, player, 'Ravenlord\'s Lair', 'The lab (upper)')
        connect(multiworld, player, 'Library top', 'Ifrit\'s Lair', lambda state: state.has('Kobo', player) and state.can_reach('Refugee Camp', 'Region', player), "Refugee Camp")
        connect(multiworld, player, 'Ifrit\'s Lair', 'Library top')


def throwIfAnyLocationIsNotAssignedToARegion(regions: List[Region], regionNames: Set[str]):
    existingRegions: Set[str] = set()

    for region in regions:
        existingRegions.add(region.name)

    if (regionNames - existingRegions):
        raise Exception("Timespinner: the following regions are used in locations: {}, but no such region exists".format(regionNames - existingRegions))


def create_location(player: int, location_data: LocationData, region: Region) -> Location:
    location = Location(player, location_data.name, location_data.code, region)

    if location_data.rule:
        location.access_rule = location_data.rule

    if id is None:
        location.locked = True
    return location


def create_region(multiworld: MultiWorld, player: int, locations_per_region: Dict[str, List[LocationData]], name: str) -> Region:
    region = Region(name, player, multiworld)

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region)
            region.locations.append(location)
    return region


def connectStartingRegion(multiworld: MultiWorld, player: int, options: TimespinnerOptions):
    menu = multiworld.get_region('Menu', player)
    tutorial = multiworld.get_region('Tutorial', player)
    space_time_continuum = multiworld.get_region('Space time continuum', player)

    if options.pyramid_start: 
        starting_region = multiworld.get_region('Ancient Pyramid (entrance)', player)
    elif options.inverted:
        starting_region = multiworld.get_region('Refugee Camp', player)
    else:
        starting_region = multiworld.get_region('Lake desolation', player)

    menu_to_tutorial = Entrance(player, 'Tutorial', menu)
    menu_to_tutorial.connect(tutorial)
    menu.exits.append(menu_to_tutorial)
    tutorial_to_start = Entrance(player, 'Start Game', tutorial)
    tutorial_to_start.connect(starting_region)
    tutorial.exits.append(tutorial_to_start)
    teleport_back_to_start = Entrance(player, 'Teleport back to start', space_time_continuum)
    teleport_back_to_start.connect(starting_region)
    space_time_continuum.exits.append(teleport_back_to_start)


def connect(multiworld: MultiWorld, player: int, source: str, target: str,
            rule: Optional[Callable[[CollectionState], bool]] = None,
            indirect: str = ""):

    sourceRegion = multiworld.get_region(source, player)
    targetRegion = multiworld.get_region(target, player)
    entrance = sourceRegion.connect(targetRegion, rule=rule)

    if indirect:
        indirectRegion = multiworld.get_region(indirect, player)
        if indirectRegion in multiworld.indirect_connections:
            multiworld.indirect_connections[indirectRegion].add(entrance)
        else:
            multiworld.indirect_connections[indirectRegion] = {entrance}


def split_location_datas_per_region(locations: List[LocationData]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]]  = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)
    return per_region
