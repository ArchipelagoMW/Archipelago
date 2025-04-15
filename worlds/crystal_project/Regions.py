from typing import List, Dict, TYPE_CHECKING
from BaseClasses import Region, Location
from .Locations import LocationData
if TYPE_CHECKING:
    from . import CrystalProjectWorld

class CrystalProjectLocation(Location):
    game: str = "CrystalProject"

    def __init__(self, player: int, name: str = " ", address: int = None, parent=None):
        super().__init__(player, name, address, parent)

def init_areas(world: "CrystalProjectWorld", locations: List[LocationData]) -> None:
    multiworld = world.multiworld
    player = world.player

    locations_per_region = get_locations_per_region(locations)

    regions = [
        create_region(world, player, locations_per_region, "Menu"),
        create_region(world, player, locations_per_region, "Spawning Meadow")
    ]

    multiworld.regions += regions
    connect_menu_region(world)

def get_locations_per_region(locations: List[LocationData]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]] = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region

def create_region(world: "CrystalProjectWorld", player: int, locations_per_region: Dict[str, List[LocationData]], name: str) -> Region:
    region = Region(name, player, world.multiworld)

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region)
            region.locations.append(location)

    return region

def create_location(player: int, location_data: LocationData, region: Region) -> Location:
    location = CrystalProjectLocation(player, location_data.name, location_data.code, region)
    location.region = location_data.region

    return location

def connect_menu_region(world: "CrystalProjectWorld") -> None:
    starting_region_list = {
        0: "Spawning Meadow"
    }

    world.starting_region = starting_region_list[0]
    menu = world.multiworld.get_region("Menu", world.player)
    spawningMeadow = world.multiworld.get_region("Spawning Meadow", world.player)
    menu.connect(spawningMeadow)