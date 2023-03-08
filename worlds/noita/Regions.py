# Regions are areas in your game that you travel to.
import itertools
from typing import Dict, List, Set
from BaseClasses import Region, Entrance, LocationProgressType, MultiWorld
from . import Locations, Items


# Creates a new Region with the locations found in `location_region_mapping`
# and adds them to the world.
def create_region(world: MultiWorld, player: int, region_name: str) -> Region:
    new_region = Region(region_name, player, world)

    # Here we create and assign locations to the region
    for location_name, location_data in Locations.location_region_mapping.get(region_name, {}).items():
        location = Locations.NoitaLocation(player, location_name, location_data.id, new_region)
        opt_orbs = world.orbs_as_checks[player].value
        opt_bosses = world.bosses_as_checks[player].value
        opt_paths = world.path_option[player].value
        opt_hc = world.hidden_chests[player].value
        ltype = location_data.ltype
        flag = location_data.flag

        if flag == 0 or ltype == "orb" and flag <= opt_orbs or ltype == "boss" and flag <= opt_bosses or ltype == "hc":
            new_region.locations.append(location)

        if ltype == "hc" and flag <= opt_paths:
            for i in range(opt_hc):
                location_name_num = f"{location_name} {i+1}"
                location_id = location_data.id + i
                location = Locations.NoitaLocation(player, location_name_num, location_id, new_region)
                location.progress_type = LocationProgressType.DEFAULT
                new_region.locations.append(location)

    return new_region


# Creates chest locations in the Forest region (HACK), making sure not to generate more locations than requested
def create_chests(world: MultiWorld, player: int, num_locations: int) -> Region:
    new_region = Region("Forest", player, world)
    total_locations = world.total_locations[player].value - num_locations

    for i in range(total_locations):
        location_name = f"Chest{i+1}"
        location_id = 110000+i

        location = Locations.NoitaLocation(player, location_name, location_id, new_region)
        location.progress_type = LocationProgressType.DEFAULT

        new_region.locations.append(location)

    return new_region


# Creates connections based on our access mapping in `noita_connections`.
def create_connections(player: int, regions: Dict[str, Region]) -> None:
    for source, destinations in noita_connections.items():
        new_entrances = []

        for destination in destinations:
            # An "Entrance" is really just a connection between two regions
            entrance = Entrance(player, f"From {source} To {destination}", regions[source])
            entrance.connect(regions[destination])
            new_entrances.append(entrance)

        regions[source].exits = new_entrances


def create_regions(world: MultiWorld, player: int) -> Dict[str, Region]:
    # NOTE: Forest hack is for chests
    regions = {name: create_region(world, player, name) for name in noita_regions}

    num_locations = sum(len(region.locations) for region in regions.values())
    regions.update({"Forest": create_chests(world, player, num_locations)})

    return regions


# Creates all regions and connections. Called from NoitaWorld.
def create_all_regions_and_connections(world: MultiWorld, player: int) -> None:
    created_regions = create_regions(world, player)
    create_connections(player, created_regions)

    world.regions += created_regions.values()


noita_connections: Dict[str, Set[str]] = {
    "Menu": {"Forest"},
    "Forest": {"Mines", "Floating Island", "Desert", "Snowy Wasteland"},
    "Snowy Wasteland": {"Frozen Vault", "Lake", "Forest"},
    "Frozen Vault": {"Snowy Wasteland"},
    "Lake": {"Snowy Wasteland", "Desert"},
    "Desert": {"Lake", "Pyramid", "Overgrown Cavern"},
    "Floating Island": {"Forest"},
    "Pyramid": {"Desert"},
    "Overgrown Cavern": {"Sandcave"},
    "Sandcave": {"Powerplant"},

    "Mines": {"Collapsed Mines", "Holy Mountain 1 (To Coal Pits)", "Lava Lake", "Forest"},
    "Collapsed Mines": {"Mines", "Holy Mountain 1 (To Coal Pits)", "Dark Cave"},
    "Lava Lake": {"Mines", "Shaft", "Abyss Orb Room", "Below Lava Lake"},
    "Shaft": {"Lava Lake", "Snowy Depths", "Abyss Orb Room", "Below Lava Lake"},
    "Abyss Orb Room": {"Lava Lake", "Shaft"},
    "Below Lava Lake": {"Lava Lake", "Shaft"},
    "Dark Cave": {"Ancient Laboratory", "Collapsed Mines"},
    "Ancient Laboratory": {"Dark Cave"},

    ###
    "Holy Mountain 1 (To Coal Pits)": {"Coal Pits"},
    "Coal Pits": {"Holy Mountain 1 (To Coal Pits)", "Fungal Caverns", "Holy Mountain 2 (To Snowy Depths)"},
    "Fungal Caverns": {"Coal Pits"},

    ###
    "Holy Mountain 2 (To Snowy Depths)": {"Snowy Depths"},
    "Snowy Depths": {"Shaft", "Holy Mountain 2 (To Snowy Depths)", "Holy Mountain 3 (To Hiisi Base)", "Magical Temple"},
    "Magical Temple": {"Snowy Depths"},

    ###
    "Holy Mountain 3 (To Hiisi Base)": {"Hiisi Base"},
    "Hiisi Base": {"Holy Mountain 3 (To Hiisi Base)", "Secret Shop", "Holy Mountain 4 (To Underground Jungle)"},
    "Secret Shop": {"Hiisi Base"},

    ###
    "Holy Mountain 4 (To Underground Jungle)": {"Underground Jungle"},
    "Underground Jungle": {"Holy Mountain 4 (To Underground Jungle)", "Dragoncave", "Holy Mountain 5 (To The Vault)",
                           "Lukki Lair"},
    "Dragoncave": {"Underground Jungle"},
    "Lukki Lair": {"Underground Jungle", "The Vault", "Snow Chasm"},
    "Snow Chasm": {},

    ###
    "Holy Mountain 5 (To The Vault)": {"The Vault"},
    "The Vault": {"Holy Mountain 5 (To The Vault)", "Holy Mountain 6 (To Temple of the Art)", "Lukki Lair"},

    ###
    "Holy Mountain 6 (To Temple of the Art)": {"Temple of the Art"},
    "Temple of the Art": {"Holy Mountain 6 (To Temple of the Art)", "Holy Mountain 7 (To The Laboratory)", "The Tower",
                          "Wizard's Den"},
    "Wizard's Den": {"Temple of the Art", "Powerplant"},
    "Powerplant": {"Wizard's Den", "Deep Underground"},
    "The Tower": {"Forest"},
    "Deep Underground": {},

    ###
    "Holy Mountain 7 (To The Laboratory)": {"The Laboratory"},
    "The Laboratory": {"Holy Mountain 7 (To The Laboratory)", "The Work", "Friend Cave", "The Work (Hell)"},
    "Friend Cave": {},
    "The Work": {},
    "The Work (Hell)": {},
    ###
}

noita_regions: Set[str] = set(noita_connections.keys()).union(*noita_connections.values())
