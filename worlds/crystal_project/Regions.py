from typing import List, Dict, TYPE_CHECKING
from BaseClasses import Region, Location
from .Locations import LocationData
from .rules import get_job_count
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
        create_region(world, player, locations_per_region, "Yamagawa M.A."),
        create_region(world, player, locations_per_region, "Proving Meadows"),
        create_region(world, player, locations_per_region, "Skumparadise"),
        create_region(world, player, locations_per_region, "Capital Sequoia"),
        create_region(world, player, locations_per_region, "Jojo Sewers"),
        create_region(world, player, locations_per_region, "Boomer Society"),
        create_region(world, player, locations_per_region, "Rolling Quintar Fields"),
        create_region(world, player, locations_per_region, "Quintar Nest"),
        create_region(world, player, locations_per_region, "Quintar Sanctum"),
        create_region(world, player, locations_per_region, "Capital Jail"),
        create_region(world, player, locations_per_region, "Capital Pipeline"),
        create_region(world, player, locations_per_region, "Cobblestone Crag"),
        create_region(world, player, locations_per_region, "Okimoto N.S."),
        create_region(world, player, locations_per_region, "Greenshire Reprise"),
        create_region(world, player, locations_per_region, "Salmon Pass"),
        create_region(world, player, locations_per_region, "Salmon River"),
        create_region(world, player, locations_per_region, "Poko Poko Desert"),
        create_region(world, player, locations_per_region, "Sara Sara Bazaar"),
        create_region(world, player, locations_per_region, "Sara Sara Beach"),
        create_region(world, player, locations_per_region, "Ancient Reservoir"),
        create_region(world, player, locations_per_region, "Salmon Bay"),
        create_region(world, player, locations_per_region, "The Open Sea"),
        create_region(world, player, locations_per_region, "Shoudu Waterfront"),
        create_region(world, player, locations_per_region, "Shoudu Province"),
        create_region(world, player, locations_per_region, "Ganymede Shrine"),
        create_region(world, player, locations_per_region, "Beaurior Volcano"),
        create_region(world, player, locations_per_region, "Beaurior Rock"),
        create_region(world, player, locations_per_region, "Lake Delende"),
    ]

    multiworld.regions += regions
    connect_menu_region(world)

    multiworld.get_region("Spawning Meadows", player).add_exits(["Delende"])
    multiworld.get_region("Delende", player).add_exits(["Soiled Den", "Pale Grotto", "Yamagawa M.A.", "Seaside Cliffs", "Mercury Shrine"])
    multiworld.get_region("Yamagawa M.A.", player).add_exits(["Lake Delende"])
    multiworld.get_region("Pale Grotto", player).add_exits(["Proving Meadows"])
    multiworld.get_region("Seaside Cliffs", player).add_exits(["Draft Shaft Conduit", "Beaurior Volcano"],
        {"Beaurior Volcano": lambda state: state.has_any({"Item - Ibek Bell"}, world.player)})
    multiworld.get_region("Proving Meadows", player).add_exits(["Skumparadise"], 
        {"Skumparadise": lambda state: get_job_count(player, state) >= 3})
    multiworld.get_region("Skumparadise", player).add_exits(["Capital Sequoia"])
    multiworld.get_region("Capital Sequoia", player).add_exits(["Jojo Sewers", "Boomer Society", "Rolling Quintar Fields"])
    multiworld.get_region("Jojo Sewers", player).add_exits(["Capital Jail"], 
        {"Capital Jail": lambda state: state.has_any({"Item - Progressive Quintar Flute"}, world.player)})
    multiworld.get_region("Capital Jail", player).add_exits(["Capital Pipeline"],
        {"Capital Pipeline": lambda state: state.has("Item - South Wing Key", world.player) and state.has("Item - Cell Key", world.player, 6)})
    multiworld.get_region("Rolling Quintar Fields", player).add_exits(["Quintar Nest", "Quintar Sanctum"], 
        {"Quintar Sanctum": lambda state: state.has_any({"Item - Progressive Quintar Flute"}, world.player)})
    multiworld.get_region("Quintar Nest", player).add_exits(["Cobblestone Crag"])
    multiworld.get_region("Capital Sequoia", player).add_exits(["Cobblestone Crag", "Greenshire Reprise"], 
        {#"Cobblestone Crag": lambda state: state.has_any({"Item - Courtyard Key"}, world.player), 
        "Greenshire Reprise": lambda state: get_job_count(player, state) >= 6 })
    multiworld.get_region("Cobblestone Crag", player).add_exits(["Shoudu Waterfront", "Okimoto N.S."], 
        {"Shoudu Waterfront": lambda state: state.has("Item - Progressive Quintar Flute", world.player, 2), 
        "Okimoto N.S.": lambda state: state.has("Item - Progressive Quintar Flute", world.player, 2)})
    multiworld.get_region("Shoudu Waterfront", player).add_exits(["Shoudu Province"],
        {"Shoudu Province": lambda state: state.has("Item - Ibek Bell", world.player)})
    multiworld.get_region("Greenshire Reprise", player).add_exits(["Salmon Pass"], 
        {"Salmon Pass": lambda state: state.has_any({"Item - Progressive Quintar Flute"}, world.player)})
    multiworld.get_region("Salmon Pass", player).add_exits(["Salmon River"], 
        {"Salmon River": lambda state: state.has("Item - Progressive Quintar Flute", world.player, 2)})
    multiworld.get_region("Poko Poko Desert", player).add_exits(["Sara Sara Bazaar", "Ancient Reservoir", "Salmon Bay"], 
        {"Ancient Reservoir": lambda state: state.has("Item - Pyramid Key", world.player),
        "Salmon Bay": lambda state: state.has("Item - Progressive Quintar Flute", world.player, 2) and state.has("Item - Ibek Bell", player)})
    multiworld.get_region("Sara Sara Bazaar", player).add_exits(["Sara Sara Beach", "Shoudu Province", "The Open Sea"],
        {"Shoudu Province": lambda state: state.has("Item - Ferry Pass", world.player),
        "The Open Sea": lambda state: state.has("Item - Progressive Salmon Violin", world.player)})
    multiworld.get_region("Shoudu Province", player).add_exits(["Sara Sara Bazaar", "Ganymede Shrine"],
        {"Sara Sara Bazaar": lambda state: state.has("Item - Ferry Pass", world.player),
        "Ganymede Shrine": lambda state: state.has("Item - Ibek Bell", world.player)})
    multiworld.get_region("Ganymede Shrine", player).add_exits(["Shoudu Province"])
    multiworld.get_region("Sara Sara Beach", player).add_exits(["Beaurior Volcano"],
        {"Beaurior Volcano": lambda state: state.has("Item - Ibek Bell", world.player)})
    multiworld.get_region("Beaurior Volcano", player).add_exits(["Beaurior Rock"])
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

    if location_data.rule:
        location.access_rule = location_data.rule

    return location

def connect_menu_region(world: "CrystalProjectWorld") -> None:
    starting_region_list = {
        0: "Spawning Meadows"
    }

    world.starting_region = starting_region_list[0]
    menu = world.multiworld.get_region("Menu", world.player)
    menu.add_exits(["Spawning Meadows", "Capital Sequoia", "Salmon River", "Poko Poko Desert", "Ganymede Shrine"], 
        {"Capital Sequoia": lambda state: state.has_any({"Item - Gaea Stone"}, world.player),
        "Salmon River": lambda state: state.has_any({"Item - Poseidon Stone"}, world.player),
        "Poko Poko Desert": lambda state: state.has_any({"Item - Mars Stone"}, world.player),
        "Ganymede Shrine": lambda state: state.has_any({"Item - Ganymede Stone"}, world.player)})