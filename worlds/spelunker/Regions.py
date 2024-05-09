from typing import List, Dict, TYPE_CHECKING
from BaseClasses import Region, Location
from .Locations import LocationData
if TYPE_CHECKING:
    from . import YoshisIslandWorld


class SpelunkerLocation(Location):
    game: str = "Spelunker"

    def __init__(self, player: int, name: str = " ", address: int = None, parent=None):
        super().__init__(player, name, address, parent)


def init_areas(world: "SpelunkerWorld", locations: List[LocationData]) -> None:
    multiworld = world.multiworld
    player = world.player

    locations_per_region = get_locations_per_region(locations)

    regions = [
        create_region(world, player, locations_per_region, "Menu"),
        create_region(world, player, locations_per_region, "Area 1"),
        create_region(world, player, locations_per_region, "Area 2"),
        create_region(world, player, locations_per_region, "Area 3"),
        create_region(world, player, locations_per_region, "Area 4"),
    ]
    multiworld.regions += regions

    multiworld.get_region("Menu", player).add_exits(["Area 1"])

    multiworld.get_region("Area 1", player).add_exits(["Area 2"],{"Area 2": lambda state: state.has("Dynamite", player, 1) and state.has("Blue Key", player, 2) and state.has("Red Key", player, 1)})
    multiworld.get_region("Area 2", player).add_exits(["Area 3"],{"Area 3": lambda state: state.has("Dynamite", player, 3) and state.has("Blue Key", player, 3) and state.has("Red Key", player, 2)})
    multiworld.get_region("Area 3", player).add_exits(["Area 4"],{"Area 4": lambda state: state.has("Dynamite", player, 3) and state.has("Blue Key", player, 4) and state.has("Red Key", player, 3)})

def create_location(player: int, location_data: LocationData, region: Region) -> Location:
    location = SpelunkerLocation(player, location_data.name, location_data.code, region)
    location.access_rule = location_data.rule

    return location


def create_region(world: "SpelunkerWorld", player: int, locations_per_region: Dict[str, List[LocationData]], name: str) -> Region:
    region = Region(name, player, world.multiworld)

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region)
            region.locations.append(location)

    return region

def get_locations_per_region(locations: List[LocationData]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]] = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region
