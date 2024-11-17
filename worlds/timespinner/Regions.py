from typing import List, Set, Dict, Optional, Callable
from BaseClasses import CollectionState, MultiWorld, Region, Entrance, Location
from BaseRules import AllReq, AnyReq, Req, complex_reqs_to_rule, RULE_ALWAYS_FALSE
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

    # rule can be None instead of BaseRules.RULE_ALWAYS_TRUE
    connect(world, player, 'Lake desolation', 'Lower lake desolation', complex_reqs_to_rule(player, AnyReq([logic.timestop_req, Req('Talaria Attachment')])) if not flooded.flood_lake_desolation else None)
    connect(world, player, 'Lake desolation', 'Upper lake desolation', lambda state: logic.has_fire(state) and state.can_reach('Upper Lake Serene', 'Region', player), "Upper Lake Serene")
    connect(world, player, 'Lake desolation', 'Skeleton Shaft', logic.has_doublejump if not flooded.flood_lake_desolation else None)
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
    connect(world, player, 'Library', 'Library top', complex_reqs_to_rule(player, AnyReq([logic.doublejump_req, Req('Talaria Attachment')]))) 
    connect(world, player, 'Library', 'Varndagroth tower left', logic.has_keycard_D)
    connect(world, player, 'Library', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Library top', 'Library')
    connect(world, player, 'Varndagroth tower left', 'Library')
    connect(world, player, 'Varndagroth tower left', 'Varndagroth tower right (upper)', logic.has_keycard_C)
    connect(world, player, 'Varndagroth tower left', 'Varndagroth tower right (lower)', logic.has_keycard_B)
    connect(world, player, 'Varndagroth tower left', 'Sealed Caves (Sirens)', complex_reqs_to_rule(player, AllReq([logic.keycard_B_req, Req('Elevator Keycard')])))
    connect(world, player, 'Varndagroth tower left', 'Refugee Camp', complex_reqs_to_rule(player, logic.wheel_and_spindle_req))
    connect(world, player, 'Varndagroth tower right (upper)', 'Varndagroth tower left')
    connect(world, player, 'Varndagroth tower right (upper)', 'Varndagroth tower right (elevator)', complex_reqs_to_rule(player, Req('Elevator Keycard')))
    connect(world, player, 'Varndagroth tower right (elevator)', 'Varndagroth tower right (upper)')
    connect(world, player, 'Varndagroth tower right (elevator)', 'Varndagroth tower right (lower)')
    connect(world, player, 'Varndagroth tower right (lower)', 'Varndagroth tower left', logic.has_keycard_B)
    connect(world, player, 'Varndagroth tower right (lower)', 'Varndagroth tower right (elevator)', complex_reqs_to_rule(player, Req('Elevator Keycard')))
    connect(world, player, 'Varndagroth tower right (lower)', 'Sealed Caves (Sirens)', complex_reqs_to_rule(player, AllReq([logic.keycard_B_req, Req('Elevator Keycard')])))
    connect(world, player, 'Varndagroth tower right (lower)', 'Military Fortress', logic.can_kill_all_3_bosses)
    connect(world, player, 'Varndagroth tower right (lower)', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Sealed Caves (Sirens)', 'Varndagroth tower left', complex_reqs_to_rule(player, Req('Elevator Keycard')))
    connect(world, player, 'Sealed Caves (Sirens)', 'Varndagroth tower right (lower)', complex_reqs_to_rule(player, Req('Elevator Keycard')))
    connect(world, player, 'Sealed Caves (Sirens)', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Military Fortress', 'Varndagroth tower right (lower)', logic.can_kill_all_3_bosses)
    connect(world, player, 'Military Fortress', 'Temporal Gyre', complex_reqs_to_rule(player, Req('Timespinner Wheel')))
    connect(world, player, 'Military Fortress', 'Military Fortress (hangar)', logic.has_doublejump)
    connect(world, player, 'Military Fortress (hangar)', 'Military Fortress')
    connect(world, player, 'Military Fortress (hangar)', 'The lab', complex_reqs_to_rule(player, AllReq([logic.keycard_B_req, Req('Water Mask') if flooded.flood_lab else logic.doublejump_req])))
    connect(world, player, 'Temporal Gyre', 'Military Fortress')
    connect(world, player, 'The lab', 'Military Fortress')
    connect(world, player, 'The lab', 'The lab (power off)', logic.has_doublejump_of_npc)
    connect(world, player, 'The lab (power off)', 'The lab', complex_reqs_to_rule(player, Req('Water Mask')) if flooded.flood_lab else None)
    connect(world, player, 'The lab (power off)', 'The lab (upper)', logic.has_forwarddash_doublejump)
    connect(world, player, 'The lab (upper)', 'The lab (power off)')
    connect(world, player, 'The lab (upper)', 'Emperors tower', logic.has_forwarddash_doublejump)
    connect(world, player, 'The lab (upper)', 'Ancient Pyramid (entrance)', complex_reqs_to_rule(player, logic.all_timespinner_pieces_req))
    connect(world, player, 'Emperors tower', 'The lab (upper)')
    connect(world, player, 'Skeleton Shaft', 'Lake desolation')
    connect(world, player, 'Skeleton Shaft', 'Sealed Caves (Xarion)', logic.has_keycard_A)
    connect(world, player, 'Skeleton Shaft', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Sealed Caves (Xarion)', 'Skeleton Shaft')
    connect(world, player, 'Sealed Caves (Xarion)', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Refugee Camp', 'Forest')
    connect(world, player, 'Refugee Camp', 'Library', complex_reqs_to_rule(player, logic.wheel_and_spindle_req) if options.inverted and options.back_to_the_future else RULE_ALWAYS_FALSE)
    connect(world, player, 'Refugee Camp', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Forest', 'Refugee Camp')
    connect(world, player, 'Forest', 'Left Side forest Caves', complex_reqs_to_rule(player, AnyReq([Req('Talaria Attachment'), logic.timestop_req])) if not flooded.flood_lake_serene_bridge else None)
    connect(world, player, 'Forest', 'Caves of Banishment (Sirens)')
    connect(world, player, 'Forest', 'Castle Ramparts')
    connect(world, player, 'Left Side forest Caves', 'Forest')
    connect(world, player, 'Left Side forest Caves', 'Upper Lake Serene', logic.has_timestop)
    connect(world, player, 'Left Side forest Caves', 'Lower Lake Serene', complex_reqs_to_rule(player, Req('Water Mask')) if flooded.flood_lake_serene else None)
    connect(world, player, 'Left Side forest Caves', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Upper Lake Serene', 'Left Side forest Caves')
    connect(world, player, 'Upper Lake Serene', 'Lower Lake Serene', complex_reqs_to_rule(player, Req('Water Mask')) if flooded.flood_lake_serene else None)
    connect(world, player, 'Lower Lake Serene', 'Upper Lake Serene')
    connect(world, player, 'Lower Lake Serene', 'Left Side forest Caves')
    connect(world, player, 'Lower Lake Serene', 'Caves of Banishment (upper)', logic.has_doublejump if not flooded.flood_lake_serene else None)
    connect(world, player, 'Caves of Banishment (upper)', 'Lower Lake Serene', complex_reqs_to_rule(player, Req('Water Mask')) if flooded.flood_lake_serene else None)
    connect(world, player, 'Caves of Banishment (upper)', 'Caves of Banishment (Maw)', complex_reqs_to_rule(player, AnyReq([logic.doublejump_req, Req('Gas Mask'), Req('Talaria Attachment'), logic.teleport_req])))
    connect(world, player, 'Caves of Banishment (upper)', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Caves of Banishment (Maw)', 'Caves of Banishment (upper)', logic.has_doublejump if not flooded.flood_maw else complex_reqs_to_rule(player, Req('Water Mask')))
    connect(world, player, 'Caves of Banishment (Maw)', 'Caves of Banishment (Sirens)', complex_reqs_to_rule(player, AnyReq([Req('Gas Mask'), Req('Talaria Attachment')])))
    connect(world, player, 'Caves of Banishment (Maw)', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Caves of Banishment (Sirens)', 'Forest')
    connect(world, player, 'Castle Ramparts', 'Forest')
    connect(world, player, 'Castle Ramparts', 'Castle Keep')
    connect(world, player, 'Castle Ramparts', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Castle Keep', 'Castle Ramparts')
    connect(world, player, 'Castle Keep', 'Castle Basement', complex_reqs_to_rule(player, Req('Water Mask')) if flooded.flood_basement else None)
    connect(world, player, 'Castle Keep', 'Royal towers (lower)', logic.has_doublejump)
    connect(world, player, 'Castle Keep', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Royal towers (lower)', 'Castle Keep')
    connect(world, player, 'Royal towers (lower)', 'Royal towers', complex_reqs_to_rule(player, AnyReq([Req('Timespinner Wheel'), logic.forwarddash_doublejump_req])))
    connect(world, player, 'Royal towers (lower)', 'Space time continuum', logic.has_teleport)
    connect(world, player, 'Royal towers', 'Royal towers (lower)')
    connect(world, player, 'Royal towers', 'Royal towers (upper)', logic.has_doublejump)
    connect(world, player, 'Royal towers (upper)', 'Royal towers')
    #connect(world, player, 'Ancient Pyramid (entrance)', 'The lab (upper)', lambda state: not is_option_enabled(world, player, "EnterSandman"))
    connect(world, player, 'Ancient Pyramid (entrance)', 'Ancient Pyramid (left)', logic.has_doublejump)
    connect(world, player, 'Ancient Pyramid (left)', 'Ancient Pyramid (entrance)')
    connect(world, player, 'Ancient Pyramid (left)', 'Ancient Pyramid (right)', logic.has_upwarddash if not flooded.flood_pyramid_shaft else None)
    connect(world, player, 'Ancient Pyramid (right)', 'Ancient Pyramid (left)', logic.has_upwarddash if not flooded.flood_pyramid_shaft else None)
    connect(world, player, 'Space time continuum', 'Lake desolation', logic.make_rule_can_teleport_to("Present", "GateLakeDesolation"))
    connect(world, player, 'Space time continuum', 'Lower lake desolation', logic.make_rule_can_teleport_to("Present", "GateKittyBoss"))
    connect(world, player, 'Space time continuum', 'Library', logic.make_rule_can_teleport_to("Present", "GateLeftLibrary"))
    connect(world, player, 'Space time continuum', 'Varndagroth tower right (lower)', logic.make_rule_can_teleport_to("Present", "GateMilitaryGate"))
    connect(world, player, 'Space time continuum', 'Skeleton Shaft', logic.make_rule_can_teleport_to("Present", "GateSealedCaves"))
    connect(world, player, 'Space time continuum', 'Sealed Caves (Sirens)', logic.make_rule_can_teleport_to("Present", "GateSealedSirensCave"))
    connect(world, player, 'Space time continuum', 'Sealed Caves (Xarion)', logic.make_rule_can_teleport_to("Present", "GateXarion"))
    connect(world, player, 'Space time continuum', 'Upper Lake Serene', logic.make_rule_can_teleport_to("Past", "GateLakeSereneLeft"))
    connect(world, player, 'Space time continuum', 'Left Side forest Caves', logic.make_rule_can_teleport_to("Past", "GateLakeSereneRight"))
    connect(world, player, 'Space time continuum', 'Refugee Camp', logic.make_rule_can_teleport_to("Past", "GateAccessToPast"))
    connect(world, player, 'Space time continuum', 'Castle Ramparts', logic.make_rule_can_teleport_to("Past", "GateCastleRamparts"))
    connect(world, player, 'Space time continuum', 'Castle Keep', logic.make_rule_can_teleport_to("Past", "GateCastleKeep"))
    connect(world, player, 'Space time continuum', 'Royal towers (lower)', logic.make_rule_can_teleport_to("Past", "GateRoyalTowers"))
    connect(world, player, 'Space time continuum', 'Caves of Banishment (Maw)', logic.make_rule_can_teleport_to("Past", "GateMaw"))
    connect(world, player, 'Space time continuum', 'Caves of Banishment (upper)', logic.make_rule_can_teleport_to("Past", "GateCavesOfBanishment"))
    connect(world, player, 'Space time continuum', 'Ancient Pyramid (entrance)', logic.make_rule_can_teleport_to("Time", "GateGyre") if options.unchained_keys or not options.enter_sandman else None)
    connect(world, player, 'Space time continuum', 'Ancient Pyramid (left)', logic.make_rule_can_teleport_to("Time", "GateLeftPyramid"))
    connect(world, player, 'Space time continuum', 'Ancient Pyramid (right)', logic.make_rule_can_teleport_to("Time", "GateRightPyramid"))

    if options.gyre_archives:
        connect(world, player, 'The lab (upper)', 'Ravenlord\'s Lair', complex_reqs_to_rule(player, Req('Merchant Crow')))
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

    if options.inverted:
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