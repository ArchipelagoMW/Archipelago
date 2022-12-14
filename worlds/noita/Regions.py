# Regions are areas in your game that you travel to.
import itertools
from typing import Dict, List, Set
from BaseClasses import Region, Entrance, LocationProgressType, RegionType, MultiWorld
from . import Locations, Items


# Creates a new Region with the locations found in `location_region_mapping`
# and adds them to the world.
def create_region(world: MultiWorld, player: int, region_name: str) -> Region:
    new_region = Region(region_name, RegionType.Generic, region_name, player, world)

    # Chests hack, don't add more locations than we requested
    if region_name == "Forest":
        total_locations = world.total_locations[player].value - Locations.num_static_locations

        for i in range(total_locations):
            location_name = f"Chest{i+1}"
            location_id = 110000+i 

            location = Locations.NoitaLocation(player, location_name, location_id, new_region)
            location.progress_type = LocationProgressType.EXCLUDED

            new_region.locations.append(location)
    else:
        # Here we create and assign locations to the region
        for location_name, location_id in Locations.location_region_mapping.get(region_name, {}).items():
            location = Locations.NoitaLocation(player, location_name, location_id, new_region)
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
    return {name: create_region(world, player, name) for name in noita_regions}


# Creates all regions and connections. Called from NoitaWorld.
def create_all_regions_and_connections(world: MultiWorld, player: int) -> None:
    created_regions = create_regions(world, player)
    create_connections(player, created_regions)

    world.regions += created_regions.values()


noita_connections: Dict[str, Set[str]] = {
    "Menu": {"Forest"},
    "Forest": {"Mines", "Collapsed Mines"},

    "Mines": {"Collapsed Mines", "Holy Mountain 1 (To Coal Pits)", "Lava Lake", "Forest"},
    "Collapsed Mines": {"Mines", "Holy Mountain 1 (To Coal Pits)", "Dark Cave"},
    "Lava Lake": {"Mines", "Shaft", "Orb Room", "Below Lava Lake"},
    "Shaft": {"Lava Lake", "Snowy Depths", "Orb Room", "Below Lava Lake"},
    "Orb Room": {"Lava Lake", "Shaft"},
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

    ###
    "Holy Mountain 4 (To Underground Jungle)": {"Underground Jungle"},
    "Dragoncave": {"Underground Jungle"},
    "Underground Jungle": {"Holy Mountain 4 (To Underground Jungle)", "Dragoncave", "Holy Mountain 5 (To The Vault)",
                           "Lukki Lair"},
    "Lukki Lair": {"Underground Jungle", "The Vault"},

    ###
    "Holy Mountain 5 (To The Vault)": {"The Vault"},
    "The Vault": {"Holy Mountain 5 (To The Vault)", "Holy Mountain 6 (To Temple of the Art)", "Lukki Lair"},

    ###
    "Holy Mountain 6 (To Temple of the Art)": {"Temple of the Art"},
    "Temple of the Art": {"Holy Mountain 6 (To Temple of the Art)", "Holy Mountain 7 (To The Laboratory)", "The Tower"},
    "The Tower": {"Forest"},

    ###
    "Holy Mountain 7 (To The Laboratory)": {"The Laboratory"},
    "The Laboratory": {"Holy Mountain 7 (To The Laboratory)", "The Work"},
}

noita_regions: Set[str] = set(noita_connections.keys()).union(*noita_connections.values())
