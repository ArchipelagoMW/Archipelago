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
        create_region(world, player, locations_per_region, "Spawning Meadows"),
        create_region(world, player, locations_per_region, "Delende"),
        create_region(world, player, locations_per_region, "Soiled Den"),
        create_region(world, player, locations_per_region, "Pale Grotto"),
        create_region(world, player, locations_per_region, "Seaside Cliffs"),
        create_region(world, player, locations_per_region, "Draft Shaft Conduit"),
        create_region(world, player, locations_per_region, "Mercury Shrine"),
        create_region(world, player, locations_per_region, "Proving Meadows"),
        create_region(world, player, locations_per_region, "Skumparadise"),
        create_region(world, player, locations_per_region, "Yamagawa M.A."),
        create_region(world, player, locations_per_region, "Capital Sequoia"),
        create_region(world, player, locations_per_region, "Jojo Sewers"),
        create_region(world, player, locations_per_region, "Boomer Society"),
        create_region(world, player, locations_per_region, "Rolling Quintar Fields"),
        create_region(world, player, locations_per_region, "Capital Jail"),
        create_region(world, player, locations_per_region, "Lake Delende")
        
    ]

    multiworld.regions += regions
    connect_menu_region(world)

    multiworld.get_region("Spawning Meadows", player).add_exits(["Delende"])
    multiworld.get_region("Delende", player).add_exits(["Soiled Den", "Pale Grotto", "Yamagawa M.A."])
    multiworld.get_region("Pale Grotto", player).add_exits(["Proving Meadows"])

    ## examples
    # multiworld.get_region("Onett", player).add_exits(["Giant Step", "Twoson", "Northern Onett", "Global ATM Access"],
    #                                              {"Giant Step": lambda state: state.has("Key to the Shack", player),
    #                                               "Twoson": lambda state: state.has("Police Badge", player),
    #                                               "Northern Onett": lambda state: state.has("Police Badge", player)})
    # multiworld.get_region("Happy-Happy Village", player).add_exits(["Peaceful Rest Valley", "Lilliput Steps", "Global ATM Access"])

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
        0: "Spawning Meadows"
    }

    world.starting_region = starting_region_list[0]
    menu = world.multiworld.get_region("Menu", world.player)
    spawningMeadow = world.multiworld.get_region("Spawning Meadows", world.player)
    menu.connect(spawningMeadow)