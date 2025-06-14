from typing import List, Set, Dict, Optional, Callable
from BaseClasses import CollectionState, MultiWorld, Region, Entrance, Location
from .Options import TimespinnerOptions
from .Locations import LocationData, get_location_datas
from .PreCalculatedWeights import PreCalculatedWeights
from .LogicExtensions import TimespinnerLogic


def create_regions_and_locations(world: MultiWorld, player: int, options: TimespinnerOptions,
                                 precalculated_weights: PreCalculatedWeights):

    locations_per_region: Dict[str, List[LocationData]] = split_location_datas_per_region(
        get_location_datas(player, options, precalculated_weights))

    regions = [
        create_region(world, player, locations_per_region, 'Menu'),
        create_region(world, player, locations_per_region, 'Tutorial'),
        create_region(world, player, locations_per_region, 'Lake desolation'),
        create_region(world, player, locations_per_region, 'Upper lake desolation'),
        create_region(world, player, locations_per_region, 'Lower lake desolation'),
        create_region(world, player, locations_per_region, 'Eastern lake desolation'),
        create_region(world, player, locations_per_region, 'Library'),
        create_region(world, player, locations_per_region, 'Library top'),
        create_region(world, player, locations_per_region, 'Varndagroth tower left'),
        create_region(world, player, locations_per_region, 'Varndagroth tower right (upper)'),
        create_region(world, player, locations_per_region, 'Varndagroth tower right (lower)'),
        create_region(world, player, locations_per_region, 'Varndagroth tower right (elevator)'),
        create_region(world, player, locations_per_region, 'Sealed Caves (Sirens)'),
        create_region(world, player, locations_per_region, 'Military Fortress'),
        create_region(world, player, locations_per_region, 'Military Fortress (hangar)'),
        create_region(world, player, locations_per_region, 'The lab'),
        create_region(world, player, locations_per_region, 'The lab (power off)'),
        create_region(world, player, locations_per_region, 'The lab (upper)'),
        create_region(world, player, locations_per_region, 'Emperors tower'),
        create_region(world, player, locations_per_region, 'Skeleton Shaft'),
        create_region(world, player, locations_per_region, 'Sealed Caves (Xarion)'),
        create_region(world, player, locations_per_region, 'Refugee Camp'),
        create_region(world, player, locations_per_region, 'Forest'),
        create_region(world, player, locations_per_region, 'Left Side forest Caves'),
        create_region(world, player, locations_per_region, 'Upper Lake Serene'),
        create_region(world, player, locations_per_region, 'Lower Lake Serene'),
        create_region(world, player, locations_per_region, 'Caves of Banishment (upper)'),
        create_region(world, player, locations_per_region, 'Caves of Banishment (Maw)'),
        create_region(world, player, locations_per_region, 'Caves of Banishment (Sirens)'),
        create_region(world, player, locations_per_region, 'Castle Ramparts'),
        create_region(world, player, locations_per_region, 'Castle Keep'),
        create_region(world, player, locations_per_region, 'Castle Basement'),
        create_region(world, player, locations_per_region, 'Royal towers (lower)'),
        create_region(world, player, locations_per_region, 'Royal towers'),
        create_region(world, player, locations_per_region, 'Royal towers (upper)'),
        create_region(world, player, locations_per_region, 'Temporal Gyre'),
        create_region(world, player, locations_per_region, 'Ancient Pyramid (entrance)'),
        create_region(world, player, locations_per_region, 'Ancient Pyramid (left)'),
        create_region(world, player, locations_per_region, 'Ancient Pyramid (right)'),
        create_region(world, player, locations_per_region, 'Space time continuum')
    ]

    if options.gyre_archives:
        regions.extend([
            create_region(world, player, locations_per_region, 'Ravenlord\'s Lair'),
            create_region(world, player, locations_per_region, 'Ifrit\'s Lair'),
        ])

    if __debug__:
        throwIfAnyLocationIsNotAssignedToARegion(regions, locations_per_region.keys())

    world.regions += regions

    connectStartingRegion(world, player, options)

    flooded: PreCalculatedWeights = precalculated_weights
    logic = TimespinnerLogic(player, options, precalculated_weights)

    connect(world, player, 'Lake desolation', 'Lower lake desolation', lambda state: flooded.flood_lake_desolation or logic.has_timestop(state) or state.has('Talaria Attachment', player))
    connect(world, player, 'Lake desolation', 'Upper lake desolation', lambda state: logic.has_fire(state) and state.can_reach('Upper Lake Serene', 'Region', player), "Upper Lake Serene")
    connect(world, player, 'Lake desolation', 'Skeleton Shaft', lambda state: flooded.flood_lake_desolation or logic.has_doublejump(state))
    connect(world, player, 'Lake desolation', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Upper lake desolation', 'Lake desolation')
    connect(world, player, 'Upper lake desolation', 'Eastern lake desolation')
    connect(world, player, 'Lower lake desolation', 'Lake desolation') 
    connect(world, player, 'Lower lake desolation', 'Eastern lake desolation')
    connect(world, player, 'Eastern lake desolation', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Eastern lake desolation', 'Library')
    connect(world, player, 'Eastern lake desolation', 'Lower lake desolation')
    connect(world, player, 'Eastern lake desolation', 'Upper lake desolation', lambda state: logic.has_fire(state) and state.can_reach('Upper Lake Serene', 'Region', player), "Upper Lake Serene")
    connect(world, player, 'Library', 'Eastern lake desolation')
    connect(world, player, 'Library', 'Library top', lambda state: logic.has_doublejump(state) or state.has('Talaria Attachment', player)) 
    connect(world, player, 'Library', 'Varndagroth tower left', logic.has_keycard_D)
    connect(world, player, 'Library', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Library top', 'Library')
    connect(world, player, 'Varndagroth tower left', 'Library')
    connect(world, player, 'Varndagroth tower left', 'Varndagroth tower right (upper)', logic.has_keycard_C)
    connect(world, player, 'Varndagroth tower left', 'Varndagroth tower right (lower)', logic.has_keycard_B)
    connect(world, player, 'Varndagroth tower left', 'Sealed Caves (Sirens)', lambda state: logic.has_keycard_B(state) and state.has('Elevator Keycard', player))
    connect(world, player, 'Varndagroth tower left', 'Refugee Camp', lambda state: state.has('Timespinner Wheel', player) and state.has('Timespinner Spindle', player))
    connect(world, player, 'Varndagroth tower right (upper)', 'Varndagroth tower left')
    connect(world, player, 'Varndagroth tower right (upper)', 'Varndagroth tower right (elevator)', lambda state: state.has('Elevator Keycard', player))
    connect(world, player, 'Varndagroth tower right (elevator)', 'Varndagroth tower right (upper)')
    connect(world, player, 'Varndagroth tower right (elevator)', 'Varndagroth tower right (lower)')
    connect(world, player, 'Varndagroth tower right (lower)', 'Varndagroth tower left', logic.has_keycard_B)
    connect(world, player, 'Varndagroth tower right (lower)', 'Varndagroth tower right (elevator)', lambda state: state.has('Elevator Keycard', player))
    connect(world, player, 'Varndagroth tower right (lower)', 'Sealed Caves (Sirens)', lambda state: logic.has_keycard_B(state) and state.has('Elevator Keycard', player))
    connect(world, player, 'Varndagroth tower right (lower)', 'Military Fortress', logic.can_kill_all_3_bosses)
    connect(world, player, 'Varndagroth tower right (lower)', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Sealed Caves (Sirens)', 'Varndagroth tower left', lambda state: state.has('Elevator Keycard', player))
    connect(world, player, 'Sealed Caves (Sirens)', 'Varndagroth tower right (lower)', lambda state: state.has('Elevator Keycard', player))
    connect(world, player, 'Sealed Caves (Sirens)', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Military Fortress', 'Varndagroth tower right (lower)', logic.can_kill_all_3_bosses)
    connect(world, player, 'Military Fortress', 'Temporal Gyre', lambda state: state.has('Timespinner Wheel', player) and logic.can_kill_all_3_bosses(state))
    connect(world, player, 'Military Fortress', 'Military Fortress (hangar)', logic.has_doublejump)
    connect(world, player, 'Military Fortress (hangar)', 'Military Fortress')
    connect(world, player, 'Military Fortress (hangar)', 'The lab', lambda state: logic.has_keycard_B(state) and (state.has('Water Mask', player) if flooded.flood_lab else logic.has_doublejump(state)))
    connect(world, player, 'Temporal Gyre', 'Military Fortress')
    connect(world, player, 'The lab', 'Military Fortress')
    connect(world, player, 'The lab', 'The lab (power off)', lambda state: options.lock_key_amadeus or logic.has_doublejump_of_npc(state))
    connect(world, player, 'The lab (power off)', 'The lab', lambda state: not flooded.flood_lab or state.has('Water Mask', player))
    connect(world, player, 'The lab (power off)', 'The lab (upper)', lambda state: logic.has_forwarddash_doublejump(state) and ((not options.lock_key_amadeus) or state.has('Lab Access Genza', player)))
    connect(world, player, 'The lab (upper)', 'The lab (power off)', lambda state: options.lock_key_amadeus and state.has('Lab Access Genza', player))
    connect(world, player, 'The lab (upper)', 'Emperors tower', logic.has_forwarddash_doublejump)
    connect(world, player, 'The lab (upper)', 'Ancient Pyramid (entrance)', lambda state: state.has_all({'Timespinner Wheel', 'Timespinner Spindle', 'Timespinner Gear 1', 'Timespinner Gear 2', 'Timespinner Gear 3'}, player))
    connect(world, player, 'Emperors tower', 'The lab (upper)')
    connect(world, player, 'Skeleton Shaft', 'Lake desolation')
    connect(world, player, 'Skeleton Shaft', 'Sealed Caves (Xarion)', logic.has_keycard_A)
    connect(world, player, 'Skeleton Shaft', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Sealed Caves (Xarion)', 'Skeleton Shaft')
    connect(world, player, 'Sealed Caves (Xarion)', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Refugee Camp', 'Forest')
    connect(world, player, 'Refugee Camp', 'Library', lambda state: (options.pyramid_start or options.inverted) and options.back_to_the_future and state.has_all({'Timespinner Wheel', 'Timespinner Spindle'}, player))
    connect(world, player, 'Refugee Camp', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Forest', 'Refugee Camp')
    connect(world, player, 'Forest', 'Left Side forest Caves', lambda state: flooded.flood_lake_serene_bridge or state.has('Talaria Attachment', player) or logic.has_timestop(state))
    connect(world, player, 'Forest', 'Caves of Banishment (Sirens)')
    connect(world, player, 'Forest', 'Castle Ramparts', lambda state: not options.gate_keep or state.has('Drawbridge Key', player) or logic.has_upwarddash(state))
    connect(world, player, 'Left Side forest Caves', 'Forest')
    connect(world, player, 'Left Side forest Caves', 'Upper Lake Serene', logic.has_timestop)
    connect(world, player, 'Left Side forest Caves', 'Lower Lake Serene', lambda state: not flooded.flood_lake_serene or state.has('Water Mask', player))
    connect(world, player, 'Left Side forest Caves', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Upper Lake Serene', 'Left Side forest Caves')
    connect(world, player, 'Upper Lake Serene', 'Lower Lake Serene', lambda state: not flooded.flood_lake_serene or state.has('Water Mask', player))
    connect(world, player, 'Lower Lake Serene', 'Upper Lake Serene')
    connect(world, player, 'Lower Lake Serene', 'Left Side forest Caves')
    connect(world, player, 'Lower Lake Serene', 'Caves of Banishment (upper)', lambda state: flooded.flood_lake_serene or logic.has_doublejump(state))
    connect(world, player, 'Caves of Banishment (upper)', 'Lower Lake Serene', lambda state: not flooded.flood_lake_serene or state.has('Water Mask', player))
    connect(world, player, 'Caves of Banishment (upper)', 'Caves of Banishment (Maw)', lambda state: not flooded.flood_maw or state.has('Water Mask', player))
    connect(world, player, 'Caves of Banishment (upper)', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Caves of Banishment (Maw)', 'Caves of Banishment (upper)', lambda state: logic.has_doublejump(state) if not flooded.flood_maw else state.has('Water Mask', player))
    connect(world, player, 'Caves of Banishment (Maw)', 'Caves of Banishment (Sirens)', lambda state: state.has_any({'Gas Mask', 'Talaria Attachment'}, player) )
    connect(world, player, 'Caves of Banishment (Maw)', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Caves of Banishment (Sirens)', 'Forest')
    connect(world, player, 'Castle Ramparts', 'Forest')
    connect(world, player, 'Castle Ramparts', 'Castle Keep')
    connect(world, player, 'Castle Ramparts', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Castle Keep', 'Castle Ramparts')
    connect(world, player, 'Castle Keep', 'Castle Basement', lambda state: not flooded.flood_basement or state.has('Water Mask', player))
    connect(world, player, 'Castle Keep', 'Royal towers (lower)', lambda state: logic.has_doublejump(state) and (not options.royal_roadblock or logic.has_pink(state)))
    connect(world, player, 'Castle Keep', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Royal towers (lower)', 'Castle Keep')
    connect(world, player, 'Royal towers (lower)', 'Royal towers', lambda state: state.has('Timespinner Wheel', player) or logic.has_forwarddash_doublejump(state))
    connect(world, player, 'Royal towers (lower)', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Royal towers', 'Royal towers (lower)')
    connect(world, player, 'Royal towers', 'Royal towers (upper)', logic.has_doublejump)
    connect(world, player, 'Royal towers (upper)', 'Royal towers')
    #connect(world, player, 'Ancient Pyramid (entrance)', 'The lab (upper)', lambda state: not is_option_enabled(world, player, "EnterSandman"))
    connect(world, player, 'Ancient Pyramid (entrance)', 'Ancient Pyramid (left)', logic.has_doublejump)
    connect(world, player, 'Ancient Pyramid (entrance)', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Ancient Pyramid (left)', 'Ancient Pyramid (entrance)')
    connect(world, player, 'Ancient Pyramid (left)', 'Ancient Pyramid (right)', lambda state: flooded.flood_pyramid_shaft or logic.has_upwarddash(state))
    connect(world, player, 'Ancient Pyramid (left)', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Ancient Pyramid (right)', 'Ancient Pyramid (left)', lambda state: flooded.flood_pyramid_shaft or logic.has_upwarddash(state))
    connect(world, player, 'Ancient Pyramid (right)', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Space time continuum', 'Lake desolation', lambda state: logic.can_teleport_to(state, "Present", "GateLakeDesolation"))
    connect(world, player, 'Space time continuum', 'Lower lake desolation', lambda state: logic.can_teleport_to(state, "Present", "GateKittyBoss"))
    connect(world, player, 'Space time continuum', 'Library', lambda state: logic.can_teleport_to(state, "Present", "GateLeftLibrary"))
    connect(world, player, 'Space time continuum', 'Varndagroth tower right (lower)', lambda state: logic.can_teleport_to(state, "Present", "GateMilitaryGate"))
    connect(world, player, 'Space time continuum', 'Skeleton Shaft', lambda state: logic.can_teleport_to(state, "Present", "GateSealedCaves"))
    connect(world, player, 'Space time continuum', 'Sealed Caves (Sirens)', lambda state: logic.can_teleport_to(state, "Present", "GateSealedSirensCave"))
    connect(world, player, 'Space time continuum', 'Sealed Caves (Xarion)', lambda state: logic.can_teleport_to(state, "Present", "GateXarion"))
    connect(world, player, 'Space time continuum', 'Upper Lake Serene', lambda state: logic.can_teleport_to(state, "Past", "GateLakeSereneLeft"))
    connect(world, player, 'Space time continuum', 'Left Side forest Caves', lambda state: logic.can_teleport_to(state, "Past", "GateLakeSereneRight"))
    connect(world, player, 'Space time continuum', 'Refugee Camp', lambda state: logic.can_teleport_to(state, "Past", "GateAccessToPast"))
    connect(world, player, 'Space time continuum', 'Forest', lambda state: logic.can_teleport_to(state, "Past", "GateCastleRamparts"))
    connect(world, player, 'Space time continuum', 'Castle Keep', lambda state: logic.can_teleport_to(state, "Past", "GateCastleKeep"))
    connect(world, player, 'Space time continuum', 'Royal towers (lower)', lambda state: logic.can_teleport_to(state, "Past", "GateRoyalTowers"))
    connect(world, player, 'Space time continuum', 'Caves of Banishment (Maw)', lambda state: logic.can_teleport_to(state, "Past", "GateMaw"))
    connect(world, player, 'Space time continuum', 'Caves of Banishment (upper)', lambda state: logic.can_teleport_to(state, "Past", "GateCavesOfBanishment"))
    connect(world, player, 'Space time continuum', 'Military Fortress (hangar)', lambda state: logic.can_teleport_to(state, "Present", "GateLabEntrance"))
    connect(world, player, 'Space time continuum', 'The lab (upper)', lambda state: logic.can_teleport_to(state, "Present", "GateDadsTower"))
    connect(world, player, 'Space time continuum', 'Ancient Pyramid (entrance)', lambda state: logic.can_teleport_to(state, "Time", "GateGyre") or logic.can_teleport_to(state, "Time", "GateLeftPyramid") or (not options.unchained_keys and options.enter_sandman))
    connect(world, player, 'Space time continuum', 'Ancient Pyramid (right)', lambda state: logic.can_teleport_to(state, "Time", "GateRightPyramid"))

    if options.gyre_archives:
        connect(world, player, 'The lab (upper)', 'Ravenlord\'s Lair', lambda state: state.has('Merchant Crow', player))
        connect(world, player, 'Ravenlord\'s Lair', 'The lab (upper)')
        connect(world, player, 'Library top', 'Ifrit\'s Lair', lambda state: state.has('Kobo', player) and state.can_reach('Refugee Camp', 'Region', player), "Refugee Camp")
        connect(world, player, 'Ifrit\'s Lair', 'Library top')


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


def create_region(world: MultiWorld, player: int, locations_per_region: Dict[str, List[LocationData]], name: str) -> Region:
    region = Region(name, player, world)

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region)
            region.locations.append(location)
    return region


def connectStartingRegion(world: MultiWorld, player: int, options: TimespinnerOptions):
    menu = world.get_region('Menu', player)
    tutorial = world.get_region('Tutorial', player)
    space_time_continuum = world.get_region('Space time continuum', player)

    if options.pyramid_start: 
        starting_region = world.get_region('Ancient Pyramid (entrance)', player)
    elif options.inverted:
        starting_region = world.get_region('Refugee Camp', player)
    else:
        starting_region = world.get_region('Lake desolation', player)

    menu_to_tutorial = Entrance(player, 'Tutorial', menu)
    menu_to_tutorial.connect(tutorial)
    menu.exits.append(menu_to_tutorial)
    tutorial_to_start = Entrance(player, 'Start Game', tutorial)
    tutorial_to_start.connect(starting_region)
    tutorial.exits.append(tutorial_to_start)
    teleport_back_to_start = Entrance(player, 'Teleport back to start', space_time_continuum)
    teleport_back_to_start.connect(starting_region)
    space_time_continuum.exits.append(teleport_back_to_start)


def connect(world: MultiWorld, player: int, source: str, target: str, 
            rule: Optional[Callable[[CollectionState], bool]] = None,
            indirect: str = ""):

    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)
    entrance = sourceRegion.connect(targetRegion, rule=rule)

    if indirect:
        indirectRegion = world.get_region(indirect, player)
        if indirectRegion in world.indirect_connections:
            world.indirect_connections[indirectRegion].add(entrance)
        else:
            world.indirect_connections[indirectRegion] = {entrance}


def split_location_datas_per_region(locations: List[LocationData]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]]  = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)
    return per_region
