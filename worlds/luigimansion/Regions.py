from typing import List, Set, Dict, Tuple, Optional, Callable, Union
from BaseClasses import MultiWorld, Region, Entrance, Location, RegionType
from .Locations import LocationData


def create_regions(multiworld: MultiWorld, player: int, locations: tuple[LocationData, ...],
                   location_cache: List[Location]):
    locations_per_region = get_locations_per_region(locations)

    regions = [
        create_region(multiworld, player, locations_per_region, location_cache, 'Menu'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Foyer'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Parlor'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Anteroom'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Wardrobe'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Wardrobe Balcony'),
        create_region(multiworld, player, locations_per_region, location_cache, '2F Front Hallway'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Study'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Master Bedroom'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Nursery'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Twins\' Room'),
        create_region(multiworld, player, locations_per_region, location_cache, '1F Hallway'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Laundry Room'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Butler\'s Room'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Hidden Room'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Fortune-Teller\'s Room'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Mirror Room'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Ballroom'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Storage Room'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Dining Room'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Kitchen'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Boneyard'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Graveyard'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Billiards Room'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Projection Room'),
        create_region(multiworld, player, locations_per_region, location_cache, '1F Bathroom'),
        create_region(multiworld, player, locations_per_region, location_cache, '1F Washroom'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Conservatory'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Courtyard'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Rec Room'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Basement Stairwell'),
        create_region(multiworld, player, locations_per_region, location_cache, '2F Stairwell'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Tea Room'),
        create_region(multiworld, player, locations_per_region, location_cache, '2F Rear Hallway'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Nana\'s Room'),
        create_region(multiworld, player, locations_per_region, location_cache, '2F Bathroom'),
        create_region(multiworld, player, locations_per_region, location_cache, '2F Washroom'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Astral Hall'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Observatory'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Sealed Room'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Sitting Room'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Guest Room'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Safari Room'),
        create_region(multiworld, player, locations_per_region, location_cache, '3F Right Hallway'),
        create_region(multiworld, player, locations_per_region, location_cache, '3F Left Hallway'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Artist\'s Studio'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Balcony'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Armory'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Ceramics Studio'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Telephone Room'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Clockwork Room'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Roof'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Breaker Room'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Celler'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Basement Hallway'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Cold Storage'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Pipe Room'),
        create_region(multiworld, player, locations_per_region, location_cache, 'The Well'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Secret Altar')
    ]

    if __debug__:
        throwIfAnyLocationIsNotAssignedToARegion(regions, locations_per_region.keys())

    multiworld.regions += regions

    connectStartingRegion(multiworld, player)

    names: Dict[str, int] = {}

    connect(multiworld, player, names, 'Menu', 'Foyer')
    connect(multiworld, player, names, 'Foyer', 'Parlor')
    connect(multiworld, player, names, 'Parlor', 'Anteroom', lambda state: state.has("Anteroom Key", player))
    connect(multiworld, player, names, 'Anteroom', 'Wardrobe')
    connect(multiworld, player, names, 'Wardrobe', 'Wardrobe Balcony')
    connect(multiworld, player, names, 'Foyer', '2F Front Hallway',
            lambda state: state.has("Front Hallway Key", player))
    connect(multiworld, player, names, '2F Front Hallway', 'Study')
    connect(multiworld, player, names, '2F Front Hallway', 'Master Bedroom',
            lambda state: state.has("Master Bedroom Key", player))
    connect(multiworld, player, names, '2F Front Hallway', 'Nursery', lambda state: state.has("Nursery Key", player))
    connect(multiworld, player, names, '2F Front Hallway', 'Twins\' Room',
            lambda state: state.has("Twins Bedroom Key", player))
    connect(multiworld, player, names, 'Foyer', '1F Hallway', lambda state: state.has("Heart Key", player))
    connect(multiworld, player, names, '1F Hallway', 'Basement Stairwell')
    connect(multiworld, player, names, '1F Hallway', '2F Stairwell',
            lambda state: state.has("2F Stairwell Key", player))
    connect(multiworld, player, names, '1F Hallway', 'Courtyard', lambda state: state.has("Club Key", player))
    connect(multiworld, player, names, '1F Hallway', '1F Bathroom')
    connect(multiworld, player, names, '1F Hallway', 'Conservatory',
            lambda state: state.has("Conservatory Key", player))
    connect(multiworld, player, names, '1F Hallway', 'Billiards Room', lambda state: state.has("Billiards Key", player))
    connect(multiworld, player, names, '1F Hallway', '1F Washroom',
            lambda state: state.has("Boo", player, multiworld.WashroomBooCount[player]))
    connect(multiworld, player, names, '1F Hallway', 'Ballroom', lambda state: state.has("Ballroom Key", player))
    connect(multiworld, player, names, '1F Hallway', 'Dining Room', lambda state: state.has("Dining Room Key", player))
    connect(multiworld, player, names, '1F Hallway', 'Laundry Room', lambda state: state.has("Laundry Key", player))
    connect(multiworld, player, names, '1F Hallway', 'Fortune-Teller\'s Room',
            lambda state: state.has("Fortune Teller Key", player))
    connect(multiworld, player, names, 'Courtyard', 'Rec Room', lambda state: state.has("Rec Room Key", player))
    connect(multiworld, player, names, 'Rec Room', 'Courtyard', lambda state: state.has("Rec Room Key", player))
    connect(multiworld, player, names, 'Ballroom', 'Storage Room', lambda state: state.has("Storage Room Key", player))
    connect(multiworld, player, names, 'Dining Room', 'Kitchen')
    connect(multiworld, player, names, 'Kitchen', 'Boneyard', lambda state: state.has("Water Element Medal", player))
    connect(multiworld, player, names, 'Boneyard', 'Graveyard', lambda state: state.has("Water Element Medal", player))
    connect(multiworld, player, names, 'Billiards Room', 'Projection Room')
    connect(multiworld, player, names, 'Fortune-Teller\'s Room', 'Mirror Room')
    connect(multiworld, player, names, 'Laundry Room', 'Butler\'s Room')
    connect(multiworld, player, names, 'Butler\'s Room', 'Hidden Room')
    connect(multiworld, player, names, 'Courtyard', 'The Well')
    connect(multiworld, player, names, 'Rec Room', '2F Stairwell')
    connect(multiworld, player, names, '2F Stairwell', 'Tea Room',
            lambda state: state.has("Water Element Medal", player))
    connect(multiworld, player, names, '2F Stairwell', 'Rec Room')
    connect(multiworld, player, names, '2F Stairwell', '2F Rear Hallway')
    connect(multiworld, player, names, '2F Rear Hallway', '2F Bathroom')
    connect(multiworld, player, names, '2F Rear Hallway', '2F Washroom')
    connect(multiworld, player, names, '2F Rear Hallway', 'Nana\'s Room')
    connect(multiworld, player, names, '2F Rear Hallway', 'Astral Hall')
    connect(multiworld, player, names, '2F Rear Hallway', 'Sitting Room',
            lambda state: state.has("Sitting Room Key", player))
    connect(multiworld, player, names, '2F Rear Hallway', 'Safari Room', lambda state: state.has("Safari Key", player))
    connect(multiworld, player, names, 'Astral Hall', 'Observatory',
            lambda state: state.has("Fire Element Medal", player))
    connect(multiworld, player, names, 'Sitting Room', 'Guest Room')
    connect(multiworld, player, names, 'Safari Room', '3F Right Hallway')
    connect(multiworld, player, names, '3F Right Hallway', 'Artist\'s Studio',
            lambda state: state.has("Art Studio Key", player))
    connect(multiworld, player, names, '3F Right Hallway', 'Balcony',
            lambda state: state.has("Balcony Key", player) and state.has("Boo", player,
                                                                         multiworld.BalconyBooCount[player]))
    connect(multiworld, player, names, 'Balcony', '3F Left Hallway', lambda state: state.has("Diamond Key", player))
    connect(multiworld, player, names, '3F Left Hallway', 'Armory', lambda state: state.has("Armory Key", player))
    connect(multiworld, player, names, '3F Left Hallway', 'Telephone Room')
    connect(multiworld, player, names, 'Telephone Room', 'Clockwork Room',
            lambda state: state.has("Clockwork Key", player))
    connect(multiworld, player, names, 'Armory', 'Ceramics Studio')
    connect(multiworld, player, names, 'Clockwork Room', 'Roof')
    connect(multiworld, player, names, 'Roof', 'Sealed Room')
    connect(multiworld, player, names, 'Basement Stairwell', 'Breaker room')
    connect(multiworld, player, names, 'Basement Stairwell', 'Cellar', lambda state: state.has("Cellar Key", player))
    connect(multiworld, player, names, 'Cellar', 'Basement Hallway')
    connect(multiworld, player, names, 'Basement Hallway', 'Cold Storage',
            lambda state: state.has("Cold Storage Key", player))
    connect(multiworld, player, names, 'Basement Hallway', 'Pipe Room',
            lambda state: state.has("Pipe Room Key", player))
    connect(multiworld, player, names, 'Basement Hallway', 'Secret Altar',
            lambda state: state.has("Spade Key", player) and state.has("Boo", player, multiworld.FinalBooCount[player]))


def throwIfAnyLocationIsNotAssignedToARegion(regions: List[Region], regionNames: Set[str]):
    existingRegions = set()

    for region in regions:
        existingRegions.add(region.name)

    if (regionNames - existingRegions):
        raise Exception(
            "LuigiMansion: the following regions are used in locations: {}, but no such region exists".format(
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
    region = Region(name, RegionType.Generic, name, player)
    region.multiworld = multiworld

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region, location_cache)
            region.locations.append(location)

    return region


def connectStartingRegion(multiworld: MultiWorld, player: int):
    menu = multiworld.get_region('Menu', player)
    tutorial = multiworld.get_region('Tutorial', player)
    space_time_continuum = multiworld.get_region('Space time continuum', player)

    if is_option_enabled(multiworld, player, "Inverted"):
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


def connect(multiworld: MultiWorld, player: int, used_names: Dict[str, int], source: str, target: str,
            rule: Optional[Callable] = None):
    sourceRegion = multiworld.get_region(source, player)
    targetRegion = multiworld.get_region(target, player)

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
        per_region.setdefault(location.parent_region, []).append(location)

    return per_region


def is_option_enabled(world: MultiWorld, player: int, name: str) -> bool:
    return get_option_value(world, player, name) > 0


def get_option_value(world: MultiWorld, player: int, name: str) -> Union[int, dict]:
    option = getattr(world, name, None)
    if option == None:
        return 0

    return option[player].value
