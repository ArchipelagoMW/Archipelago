from typing import List, Set, Dict, Tuple, Optional, Callable
from BaseClasses import MultiWorld, Region, Entrance, Location, RegionType
from .Locations import LocationData


def create_regions(world: MultiWorld, player: int, locations: Tuple[LocationData, ...], location_cache: List[Location]):
    locations_per_region = get_locations_per_region(locations)

    regions = [
        create_region(world, player, locations_per_region, location_cache, 'Menu'),
        create_region(world, player, locations_per_region, location_cache, 'Forest of Silence - start'),
        create_region(world, player, locations_per_region, location_cache, 'Forest of Silence - switch 1'),
        create_region(world, player, locations_per_region, location_cache, 'Forest of Silence - switch 2'),
        create_region(world, player, locations_per_region, location_cache, 'Forest of Silence - switch 3'),
        create_region(world, player, locations_per_region, location_cache, 'Forest of Silence - end'),
        create_region(world, player, locations_per_region, location_cache, 'Castle Wall main - start'),
        create_region(world, player, locations_per_region, location_cache, 'Castle Wall main - exit to Villa'),
        create_region(world, player, locations_per_region, location_cache, 'Castle Wall main - Bone Dragon switch'),
        create_region(world, player, locations_per_region, location_cache, 'Castle Wall main - Dracula switch'),
        create_region(world, player, locations_per_region, location_cache, 'Castle Wall main - descent'),
        create_region(world, player, locations_per_region, location_cache, 'Castle Wall - left tower'),
        create_region(world, player, locations_per_region, location_cache, 'Castle Wall - right tower'),
        #create_region(world, player, locations_per_region, location_cache, 'Villa front yard - cerberus side'),
        #create_region(world, player, locations_per_region, location_cache, 'Villa front yard - fountain side'),
        #create_region(world, player, locations_per_region, location_cache, 'Villa foyer - main'),
        #create_region(world, player, locations_per_region, location_cache, 'Villa foyer - servant entrance'),
        #create_region(world, player, locations_per_region, location_cache, 'Villa living area - main'),
        #create_region(world, player, locations_per_region, location_cache, 'Villa living area - storeroom'),
        #create_region(world, player, locations_per_region, location_cache, 'Villa living area - archives'),
        #create_region(world, player, locations_per_region, location_cache, 'Villa maze - front entrance'),
        #create_region(world, player, locations_per_region, location_cache, 'Villa maze - back entrance'),
        #create_region(world, player, locations_per_region, location_cache, 'Villa maze - crypt entrance'),
        #create_region(world, player, locations_per_region, location_cache, 'Villa maze - main'),
        #create_region(world, player, locations_per_region, location_cache, 'Villa vampire crypt'),
        #create_region(world, player, locations_per_region, location_cache, 'Tunnel'),
        #create_region(world, player, locations_per_region, location_cache, 'Underground Waterway - main'),
        #create_region(world, player, locations_per_region, location_cache, 'Underground Waterway - mid'),
        #create_region(world, player, locations_per_region, location_cache, 'Underground Waterway - Carrie crawlspace'),
        #create_region(world, player, locations_per_region, location_cache, 'Fan meeting room'),
        #create_region(world, player, locations_per_region, location_cache, 'Castle Center basement - main'),
        #create_region(world, player, locations_per_region, location_cache, 'Castle Center basement - giant crystal'),
        #create_region(world, player, locations_per_region, location_cache, 'Castle Center basement - torture chamber'),
        #create_region(world, player, locations_per_region, location_cache, 'Castle Center elevator bottom'),
        #create_region(world, player, locations_per_region, location_cache, 'Castle Center elevator top'),
        #create_region(world, player, locations_per_region, location_cache, 'Castle Center factory floor'),
        #create_region(world, player, locations_per_region, location_cache, 'Castle Center lizard lab - main'),
        #create_region(world, player, locations_per_region, location_cache, 'Castle Center lizard lab - cracked wall'),
        #create_region(world, player, locations_per_region, location_cache, 'Castle Center library'),
        #create_region(world, player, locations_per_region, location_cache, 'Castle Center inventions - main'),
        #create_region(world, player, locations_per_region, location_cache, 'Castle Center inventions - lizard exit'),
        #create_region(world, player, locations_per_region, location_cache, 'Duel Tower'),
        #create_region(world, player, locations_per_region, location_cache, 'Tower of Sorcery'),
        #create_region(world, player, locations_per_region, location_cache, 'Tower of Execution - main'),
        #create_region(world, player, locations_per_region, location_cache, 'Tower of Execution - gated ledge'),
        #create_region(world, player, locations_per_region, location_cache, 'Tower of Science - main turret room'),
        #create_region(world, player, locations_per_region, location_cache, 'Tower of Science - key2 hallway'),
        #create_region(world, player, locations_per_region, location_cache, 'Tower of Science - spiky conveyors'),
        #create_region(world, player, locations_per_region, location_cache, 'Tower of Science - locked key3 room'),
        #create_region(world, player, locations_per_region, location_cache, 'Room of Clocks'),
        #create_region(world, player, locations_per_region, location_cache, 'Clock Tower - start'),
        #create_region(world, player, locations_per_region, location_cache, 'Clock Tower - middle'),
        #create_region(world, player, locations_per_region, location_cache, 'Clock Tower - end'),
        #create_region(world, player, locations_per_region, location_cache, 'Castle Keep - staircase'),
        #create_region(world, player, locations_per_region, location_cache, 'Castle Keep - story boss tower'),
        #create_region(world, player, locations_per_region, location_cache, 'Drac chamber'),
        #create_region(world, player, locations_per_region, location_cache, 'Stage Select'),
    ]

    if __debug__:
        throwIfAnyLocationIsNotAssignedToARegion(regions, locations_per_region.keys())
        
    world.regions += regions

    names: Dict[str, int] = {}

    connect(world, player, names, 'Menu', 'Forest of Silence - start')
    connect(world, player, names, 'Forest of Silence - start', 'Forest of Silence - switch 1')
    connect(world, player, names, 'Forest of Silence - switch 1', 'Forest of Silence - switch 2')
    connect(world, player, names, 'Forest of Silence - switch 2', 'Forest of Silence - switch 3')
    connect(world, player, names, 'Forest of Silence - switch 3', 'Forest of Silence - end')
    connect(world, player, names, 'Forest of Silence - end', 'Castle Wall main - start')
    connect(world, player, names, 'Castle Wall main - start', 'Castle Wall - right tower')
    connect(world, player, names, 'Castle Wall main - start', 'Castle Wall - left tower',
            lambda state: state.has('Left Tower Key', player))
    connect(world, player, names, 'Castle Wall - right tower', 'Castle Wall main - Bone Dragon switch')
    connect(world, player, names, 'Castle Wall - left tower', 'Castle Wall main - Dracula switch')
    connect(world, player, names, 'Castle Wall main - Bone Dragon switch', 'Castle Wall main - descent')
    connect(world, player, names, 'Castle Wall main - Dracula switch', 'Castle Wall main - descent')
    connect(world, player, names, 'Castle Wall main - Bone Dragon switch', 'Castle Wall main - exit to Villa')


def throwIfAnyLocationIsNotAssignedToARegion(regions: List[Region], regionNames: Set[str]):
    existingRegions = set()

    for region in regions:
        existingRegions.add(region.name)

    if regionNames - existingRegions:
        raise Exception("Castlevania: the following regions are used in locations: {}, but no such region exists".format(regionNames - existingRegions))


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


def connect(world: MultiWorld, player: int, used_names: Dict[str, int], source: str, target: str, rule: Optional[Callable] = None):
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (' ' * used_names[target])

    connection = Entrance(player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)


def get_locations_per_region(locations: Tuple[LocationData, ...]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]]  = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region
