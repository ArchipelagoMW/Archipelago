from typing import List, Dict, TYPE_CHECKING
from BaseClasses import Region, Location
from .Locations import LocationData
if TYPE_CHECKING:
    from . import Z2World


class Z2Location(Location):
    game: str = "Zelda II: The Adventure of Link"

    def __init__(self, player: int, name: str = " ", address: int = None, parent=None):
        super().__init__(player, name, address, parent)


def init_areas(world: "Z2World", locations: List[LocationData]) -> None:
    multiworld = world.multiworld
    player = world.player

    locations_per_region = get_locations_per_region(locations)

    regions = [
        create_region(world, world.player, locations_per_region, "Menu"),
        create_region(world, world.player, locations_per_region, "Northwestern Hyrule"),
        create_region(world, world.player, locations_per_region, "Parapa Palace"),
        create_region(world, world.player, locations_per_region, "Western Hyrule"),
        create_region(world, world.player, locations_per_region, "Midoro Palace"),
        create_region(world, world.player, locations_per_region, "Death Mountain"),
        create_region(world, world.player, locations_per_region, "Western Coast"),
        create_region(world, world.player, locations_per_region, "Island Palace"),
        create_region(world, world.player, locations_per_region, "Eastern Hyrule"),
        create_region(world, world.player, locations_per_region, "Northeastern Hyrule"),
        create_region(world, world.player, locations_per_region, "Maze Palace"),
        create_region(world, world.player, locations_per_region, "Palace on the Sea"),
        create_region(world, world.player, locations_per_region, "Southeastern Hyrule"),
        create_region(world, world.player, locations_per_region, "Three-Eye Rock Palace"),
        create_region(world, world.player, locations_per_region, "Great Palace"),
    ]

    multiworld.regions += regions

    multiworld.get_region("Menu", player).add_exits(["Northwestern Hyrule"]), # Change to start location eventually
    multiworld.get_region("Northwestern Hyrule", player).add_exits(["Western Hyrule", "Parapa Palace"]),
    multiworld.get_region("Western Hyrule", player).add_exits(["Midoro Palace", "Death Mountain", "Western Coast", "Northwestern Hyrule"]),
    multiworld.get_region("Death Mountain", player).add_exits(["Western Hyrule", "Western Coast"]),
    multiworld.get_region("Western Coast", player).add_exits(["Island Palace", "Eastern Hyrule", "Death Mountain", "Western Hyrule"]),
    multiworld.get_region("Eastern Hyrule", player).add_exits(["Western Coast", "Northeastern Hyrule", "Southeastern Hyrule", "Palace on the Sea"]),
    multiworld.get_region("Northeastern Hyrule", player).add_exits(["Eastern Hyrule", "Maze Palace"]),
    multiworld.get_region("Southeastern Hyrule", player).add_exits(["Eastern Hyrule", "Three-Eye Rock Palace", "Great Palace"]),


def create_location(player: int, location_data: LocationData, region: Region) -> Location:
    location = Z2Location(player, location_data.name, location_data.code, region)
    location.region = location_data.region

    return location


def create_region(world: "Z2World", player: int, locations_per_region: Dict[str, List[LocationData]], name: str) -> Region:
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
    