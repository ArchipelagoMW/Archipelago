from typing import List, Set, Dict, Tuple, Optional, Callable, Union
from BaseClasses import MultiWorld, Region, Entrance, Location, ItemClassification
from .Items import LMItem
from .Locations import LocationData
from worlds.generic.Rules import add_rule


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
        create_region(multiworld, player, locations_per_region, location_cache, 'Cellar'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Basement Hallway'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Cold Storage'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Pipe Room'),
        create_region(multiworld, player, locations_per_region, location_cache, 'The Well'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Secret Altar')
    ]

    if __debug__:
        throwIfAnyLocationIsNotAssignedToARegion(regions, locations_per_region.keys())

    multiworld.regions += regions

    connect(multiworld, player, "Menu -> Foyer", 'Menu', 'Foyer')  # name all connections
    connect(multiworld, player, "Foyer -> Parlor", 'Foyer', 'Parlor')
    connect(multiworld, player, "Parlor -> Anteroom", 'Parlor', 'Anteroom',
            lambda state: state.has("Anteroom Key", player))
    connect(multiworld, player, "Anteroom -> Wardrobe", 'Anteroom', 'Wardrobe')
    connect(multiworld, player, "Wardrobe -> Wardrobe Balcony", 'Wardrobe', 'Wardrobe Balcony')
    connect(multiworld, player, "Foyer -> 2F Front Hallway", 'Foyer', '2F Front Hallway',
            lambda state: state.has("Front Hallway Key", player))
    connect(multiworld, player, "2F Front Hallway -> Study", '2F Front Hallway', 'Study')
    connect(multiworld, player, "2F Front Hallway -> Master Bedroom", '2F Front Hallway', 'Master Bedroom',
            lambda state: state.has("Master Bedroom Key", player))
    connect(multiworld, player, "2F Front Hallway -> Nursery", '2F Front Hallway', 'Nursery',
            lambda state: state.has("Nursery Key", player))
    connect(multiworld, player, "2F Front Hallway -> Twins' Room", '2F Front Hallway', 'Twins\' Room',
            lambda state: state.has("Twins Bedroom Key", player))
    connect(multiworld, player, "Foyer -> 1F Hallway", 'Foyer', '1F Hallway',
            lambda state: state.has("Heart Key", player))
    connect(multiworld, player, "1F Hallway -> Basement Stairwell", '1F Hallway', 'Basement Stairwell')
    connect(multiworld, player, "1F Hallway -> 2F Stairwell", '1F Hallway', '2F Stairwell',
            lambda state: state.has("2F Stairwell Key", player))
    connect(multiworld, player, "1F Hallway -> Courtyard", '1F Hallway', 'Courtyard',
            lambda state: state.has("Club Key", player))
    connect(multiworld, player, "1F Hallway -> 1F Bathroom", '1F Hallway', '1F Bathroom')
    connect(multiworld, player, "1F Hallway -> Conservatory", '1F Hallway', 'Conservatory',
            lambda state: state.has("Conservatory Key", player))
    connect(multiworld, player, "1F Hallway -> Billiards Room", '1F Hallway', 'Billiards Room',
            lambda state: state.has("Billiards Key", player))
    connect(multiworld, player, "1F Hallway -> 1F Washroom", '1F Hallway', '1F Washroom',
            lambda state: state.has("Boo", player, multiworld.WashroomBooCount[player]))
    connect(multiworld, player, "1F Hallway -> Ballroom", '1F Hallway', 'Ballroom',
            lambda state: state.has("Ballroom Key", player))
    connect(multiworld, player, "1F Hallway -> Dining Room", '1F Hallway', 'Dining Room',
            lambda state: state.has("Dining Room Key", player))
    connect(multiworld, player, "1F Hallway -> Laundry Room", '1F Hallway', 'Laundry Room',
            lambda state: state.has("Laundry Key", player))
    connect(multiworld, player, "1F Hallway -> Fortune-Teller's Room", '1F Hallway', 'Fortune-Teller\'s Room',
            lambda state: state.has("Fortune Teller Key", player))
    connect(multiworld, player, "Courtyard -> Rec Room", 'Courtyard', 'Rec Room',
            lambda state: state.has("Rec Room Key", player))
    connect(multiworld, player, "Rec Room -> Courtyard", 'Rec Room', 'Courtyard',
            lambda state: state.has("Rec Room Key", player))
    connect(multiworld, player, "Ballroom -> Storage Room", 'Ballroom', 'Storage Room',
            lambda state: state.has("Storage Room Key", player))
    connect(multiworld, player, "Dining Room -> Kitchen", 'Dining Room', 'Kitchen')
    connect(multiworld, player, "Kitchen -> Boneyard", 'Kitchen', 'Boneyard',
            lambda state: state.has("Water Element Medal", player))
    connect(multiworld, player, "Boneyard -> Graveyard", 'Boneyard', 'Graveyard',
            lambda state: state.has("Water Element Medal", player))
    connect(multiworld, player, "Billiards Room -> Projection Room", 'Billiards Room', 'Projection Room')
    connect(multiworld, player, "Fortune-Teller's Room -> Mirror Room", 'Fortune-Teller\'s Room', 'Mirror Room',
            lambda state: state.has("Fire Element Medal", player))
    connect(multiworld, player, "Laundry Room -> Butler's Room", 'Laundry Room', 'Butler\'s Room')
    connect(multiworld, player, "Butler's Room -> Hidden Room", 'Butler\'s Room', 'Hidden Room')
    connect(multiworld, player, "Courtyard -> The Well", 'Courtyard', 'The Well')
    connect(multiworld, player, "Rec Room -> 2F Stairwell", 'Rec Room', '2F Stairwell')
    connect(multiworld, player, "2F Stairwell -> Tea Room", '2F Stairwell', 'Tea Room',
            lambda state: state.has("Water Element Medal", player))
    connect(multiworld, player, "2F Stairwell -> Rec Room", '2F Stairwell', 'Rec Room')
    connect(multiworld, player, "2F Stairwell -> 2F Rear Hallway", '2F Stairwell', '2F Rear Hallway')
    connect(multiworld, player, "2F Rear Hallway -> 2F Bathroom", '2F Rear Hallway', '2F Bathroom')
    connect(multiworld, player, "2F Rear Hallway -> 2F Washroom", '2F Rear Hallway', '2F Washroom')
    connect(multiworld, player, "2F Rear Hallway -> Nana's Room", '2F Rear Hallway', 'Nana\'s Room')
    connect(multiworld, player, "2F Rear Hallway -> Astral Hall", '2F Rear Hallway', 'Astral Hall')
    connect(multiworld, player, "2F Rear Hallway -> Sitting Room", '2F Rear Hallway', 'Sitting Room',
            lambda state: state.has("Sitting Room Key", player))
    connect(multiworld, player, "2F Rear Hallway -> Safari Room", '2F Rear Hallway', 'Safari Room',
            lambda state: state.has("Safari Key", player))
    connect(multiworld, player, "Astral Hall -> Observatory", 'Astral Hall', 'Observatory',
            lambda state: state.has("Fire Element Medal", player))
    connect(multiworld, player, "Sitting Room -> Guest Room", 'Sitting Room', 'Guest Room',
            lambda state: state.has("Fire Element Medal", player) and state.has("Water Element Medal", player))
    connect(multiworld, player, "Safari Room -> 3F Right Hallway", 'Safari Room', '3F Right Hallway')
    connect(multiworld, player, "3F Right Hallway -> Artist's Studio", '3F Right Hallway', 'Artist\'s Studio',
            lambda state: state.has("Art Studio Key", player))
    connect(multiworld, player, "3F Right Hallway -> Balcony", '3F Right Hallway', 'Balcony',
            lambda state: state.has("Balcony Key", player) and state.has("Boo", player,
                                                                         multiworld.BalconyBooCount[player]))
    connect(multiworld, player, "Balcony -> 3F Left Hallway", 'Balcony', '3F Left Hallway',
            lambda state: state.has("Diamond Key", player))
    connect(multiworld, player, "3F Left Hallway -> Armory", '3F Left Hallway', 'Armory',
            lambda state: state.has("Armory Key", player))
    connect(multiworld, player, "3F Left Hallway -> Telephone Room", '3F Left Hallway', 'Telephone Room')
    connect(multiworld, player, "Telephone Room -> Clockwork Room", 'Telephone Room', 'Clockwork Room',
            lambda state: state.has("Clockwork Key", player))
    connect(multiworld, player, "Armory -> Ceramics Studio", 'Armory', 'Ceramics Studio')
    connect(multiworld, player, "Clockwork Room -> Roof", 'Clockwork Room', 'Roof')
    connect(multiworld, player, "Roof -> Sealed Room", 'Roof', 'Sealed Room')
    connect(multiworld, player, "Basement Stairwell -> Breaker Room", 'Basement Stairwell', 'Breaker Room')
    connect(multiworld, player, "Basement Stairwell -> Cellar", 'Basement Stairwell', 'Cellar',
            lambda state: state.has("Cellar Key", player))
    connect(multiworld, player, "Cellar -> Basement Hallway", 'Cellar', 'Basement Hallway')
    connect(multiworld, player, "Basement Hallway -> Cold Storage", 'Basement Hallway', 'Cold Storage',
            lambda state: state.has("Cold Storage Key", player))
    connect(multiworld, player, "Basement Hallway -> Pipe Room", 'Basement Hallway', 'Pipe Room',
            lambda state: state.has("Pipe Room Key", player))
    connect(multiworld, player, "Basement Hallway -> Secret Altar", 'Basement Hallway', 'Secret Altar',
            lambda state: state.has("Spade Key", player) and state.has("Boo", player, multiworld.FinalBooCount[player]))


def throwIfAnyLocationIsNotAssignedToARegion(regions: List[Region], regionnames: Set[str]):
    existingRegions = set()

    for region in regions:
        existingRegions.add(region.name)

    if (regionnames - existingRegions):
        raise Exception(
            "LuigiMansion: the following regions are used in locations: {}, but no such region exists".format(
                regionnames - existingRegions))


def create_location(player: int, location_data: LocationData, region: Region,  # check where event items are assigned
                    location_cache: List[Location]) -> Location:
    location = Location(player, location_data.name, location_data.code, region)
    location.access_rule = location_data.rule

    if location_data.code is None:
        location.event = True
        location.locked = True
        location.place_locked_item(LMItem(location_data.locked_item, ItemClassification.progression, None, player))

    location_cache.append(location)

    return location


def create_region(multiworld: MultiWorld, player: int, locations_per_region: Dict[str, List[LocationData]],
                  location_cache: List[Location], name: str) -> Region:
    region = Region(name, player, multiworld)
    region.multiworld = multiworld

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region, location_cache)
            if location.locked == True:
                multiworld.worlds[player].locked_locations.append(location.name)
            region.locations.append(location)

    return region


def connect(multiworld: MultiWorld, player: int, name: str, source: str, target: str,
            rule: Optional[Callable] = None):
    source_region = multiworld.get_region(source, player)
    target_region = multiworld.get_region(target, player)

    connection = Entrance(player, name, source_region)

    if rule:
        connection.access_rule = rule

    for region_to_type in multiworld.worlds[player].ghost_affected_regions:
        if region_to_type == target_region.name:
            if multiworld.worlds[player].ghost_affected_regions[region_to_type] == "Fire":
                add_rule(connection, lambda state: state.has("Water Element Medal", player), "and")
            elif multiworld.worlds[player].ghost_affected_regions[region_to_type] == "Water":
                add_rule(connection, lambda state: state.has("Ice Element Medal", player), "and")
            elif multiworld.worlds[player].ghost_affected_regions[region_to_type] == "Ice":
                add_rule(connection, lambda state: state.has("Fire Element Medal", player), "and")

    source_region.exits.append(connection)
    connection.connect(target_region)


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
