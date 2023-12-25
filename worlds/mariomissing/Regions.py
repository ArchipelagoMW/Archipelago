from typing import List, Dict, Tuple
from BaseClasses import MultiWorld, Region, Location
from .Locations import LocationData

class YILocation(Location):
    game: str = "Mario is Missing"

def __init__(player: int, name: str = " ", address: int = None, parent=None):
    super().__init__(player, name, address, parent)


def create_regions(multiworld: MultiWorld, player: int, locations: Tuple[LocationData, ...], location_cache: List[Location], world):

    locations_per_region = get_locations_per_region(locations)

    regions = [
        create_region(multiworld, player, locations_per_region, location_cache, 'Menu'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Castle Floor 1'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Castle Floor 2'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Castle Floor 3'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Castle Floor 4'),

        create_region(multiworld, player, locations_per_region, location_cache, 'Rome'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Paris'),
        create_region(multiworld, player, locations_per_region, location_cache, 'London'),
        create_region(multiworld, player, locations_per_region, location_cache, 'New York'),
        create_region(multiworld, player, locations_per_region, location_cache, 'San Francisco'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Athens'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Sydney'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Tokyo'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Nairobi'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Rio de Janeiro'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Cairo'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Moscow'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Beijing'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Buenos Aires'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Mexico City')

    ]
    multiworld.regions += regions
    multiworld.get_region('Menu', player).add_exits(["Castle Floor 1"])
    multiworld.get_region('Castle Floor 1', player).add_exits(["Castle Floor 2"],
        {"Castle Floor 2": lambda state: state.has_any({'Castle Floor Key'}, player)})
    multiworld.get_region('Castle Floor 2', player).add_exits(["Castle Floor 3"],
        {"Castle Floor 3": lambda state: state.has('Castle Floor Key', player, 2)})
    multiworld.get_region('Castle Floor 3', player).add_exits(["Castle Floor 4"],
        {"Castle Floor 4": lambda state: state.has('Artifact Secured', player, world.options.required_artifacts.value)})

    multiworld.get_region('Castle Floor 1', player).add_exits([world.city_list[0]])
    multiworld.get_region('Castle Floor 1', player).add_exits([world.city_list[1]])
    multiworld.get_region('Castle Floor 1', player).add_exits([world.city_list[2]])
    multiworld.get_region('Castle Floor 1', player).add_exits([world.city_list[3]])
    multiworld.get_region('Castle Floor 1', player).add_exits([world.city_list[4]])

    multiworld.get_region('Castle Floor 2', player).add_exits([world.city_list[5]])
    multiworld.get_region('Castle Floor 2', player).add_exits([world.city_list[6]])
    multiworld.get_region('Castle Floor 2', player).add_exits([world.city_list[7]])
    multiworld.get_region('Castle Floor 2', player).add_exits([world.city_list[8]])
    multiworld.get_region('Castle Floor 2', player).add_exits([world.city_list[9]])

    multiworld.get_region('Castle Floor 3', player).add_exits([world.city_list[10]])
    multiworld.get_region('Castle Floor 3', player).add_exits([world.city_list[11]])
    multiworld.get_region('Castle Floor 3', player).add_exits([world.city_list[12]])
    multiworld.get_region('Castle Floor 3', player).add_exits([world.city_list[13]])
    multiworld.get_region('Castle Floor 3', player).add_exits([world.city_list[14]])

def create_location(player: int, location_data: LocationData, region: Region, location_cache: List[Location]) -> Location:
    location = YILocation(player, location_data.name, location_data.code, region)
    location.access_rule = location_data.rule

    if id is None:
        location.event = True
        location.locked = True

    location_cache.append(location)

    return location

def create_region(multiworld: MultiWorld, player: int, locations_per_region: Dict[str, List[LocationData]], location_cache: List[Location], name: str) -> Region:
    region = Region(name, player, multiworld)
    region.world = multiworld

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region, location_cache)
            region.locations.append(location)

    return region


def get_locations_per_region(locations: Tuple[LocationData, ...]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]] = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region
