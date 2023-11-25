# Regions are areas in your game that you travel to.
from typing import Dict, Set, List

from BaseClasses import Entrance, MultiWorld, Region
from . import Locations


def add_location(player: int, loc_name: str, id: int, region: Region) -> None:
    location = Locations.NoitaLocation(player, loc_name, id, region)
    region.locations.append(location)


def add_locations(multiworld: MultiWorld, player: int, region: Region) -> None:
    locations = Locations.location_region_mapping.get(region.name, {})
    for location_name, location_data in locations.items():
        location_type = location_data.ltype
        flag = location_data.flag

        opt_orbs = multiworld.orbs_as_checks[player].value
        opt_bosses = multiworld.bosses_as_checks[player].value
        opt_paths = multiworld.path_option[player].value
        opt_num_chests = multiworld.hidden_chests[player].value
        opt_num_pedestals = multiworld.pedestal_checks[player].value

        is_orb_allowed = location_type == "orb" and flag <= opt_orbs
        is_boss_allowed = location_type == "boss" and flag <= opt_bosses
        if flag == Locations.LocationFlag.none or is_orb_allowed or is_boss_allowed:
            add_location(player, location_name, location_data.id, region)
        elif location_type == "chest" and flag <= opt_paths:
            for i in range(opt_num_chests):
                add_location(player, f"{location_name} {i+1}", location_data.id + i, region)
        elif location_type == "pedestal" and flag <= opt_paths:
            for i in range(opt_num_pedestals):
                add_location(player, f"{location_name} {i+1}", location_data.id + i, region)


# Creates a new Region with the locations found in `location_region_mapping` and adds them to the world.
def create_region(multiworld: MultiWorld, player: int, region_name: str) -> Region:
    new_region = Region(region_name, player, multiworld)
    add_locations(multiworld, player, new_region)
    return new_region


def create_regions(multiworld: MultiWorld, player: int) -> Dict[str, Region]:
    return {name: create_region(multiworld, player, name) for name in noita_regions}


# An "Entrance" is really just a connection between two regions
def create_entrance(player: int, source: str, destination: str, regions: Dict[str, Region]):
    entrance = Entrance(player, f"From {source} To {destination}", regions[source])
    entrance.connect(regions[destination])
    return entrance


# Creates connections based on our access mapping in `noita_connections`.
def create_connections(player: int, regions: Dict[str, Region]) -> None:
    for source, destinations in noita_connections.items():
        new_entrances = [create_entrance(player, source, destination, regions) for destination in destinations]
        regions[source].exits = new_entrances


# Creates all regions and connections. Called from NoitaWorld.
def create_all_regions_and_connections(multiworld: MultiWorld, player: int) -> None:
    created_regions = create_regions(multiworld, player)
    create_connections(player, created_regions)

    multiworld.regions += created_regions.values()


# Oh, what a tangled web we weave
# Notes to create artificial spheres:
# - Shaft is excluded to disconnect Mines from the Snowy Depths
# - Lukki Lair is disconnected from The Vault
# - Overgrown Cavern is connected to the Underground Jungle instead of the Desert due to similar difficulty
# - Powerplant is disconnected from the Sandcave due to difficulty and sphere creation
# - Snow Chasm is disconnected from the Snowy Wasteland
# - Pyramid is connected to the Hiisi Base instead of the Desert due to similar difficulty
# - Frozen Vault is connected to the Vault instead of the Snowy Wasteland due to similar difficulty
# - Lake is connected to The Laboratory, since the boss is hard without specific set-ups (which means late game)
# - Snowy Depths connects to Lava Lake orb since you need digging for it, so fairly early is acceptable
# - Ancient Laboratory is connected to the Coal Pits, so that Ylialkemisti isn't sphere 1
noita_connections: Dict[str, List[str]] = {
    "Menu": ["Forest"],
    "Forest": ["Mines", "Floating Island", "Desert", "Snowy Wasteland"],
    "Frozen Vault": ["The Vault"],
    "Overgrown Cavern": ["Sandcave"],

    ###
    "Mines": ["Collapsed Mines", "Coal Pits Holy Mountain", "Lava Lake"],
    "Lava Lake": ["Abyss Orb Room"],

    ###
    "Coal Pits Holy Mountain": ["Coal Pits"],
    "Coal Pits": ["Fungal Caverns", "Snowy Depths Holy Mountain", "Ancient Laboratory"],

    ###
    "Snowy Depths Holy Mountain": ["Snowy Depths"],
    "Snowy Depths": ["Hiisi Base Holy Mountain", "Magical Temple", "Below Lava Lake"],

    ###
    "Hiisi Base Holy Mountain": ["Hiisi Base"],
    "Hiisi Base": ["Secret Shop", "Pyramid", "Underground Jungle Holy Mountain"],

    ###
    "Underground Jungle Holy Mountain": ["Underground Jungle"],
    "Underground Jungle": ["Dragoncave", "Overgrown Cavern", "Vault Holy Mountain", "Lukki Lair", "Snow Chasm"],

    ###
    "Vault Holy Mountain": ["The Vault"],
    "The Vault": ["Frozen Vault", "Temple of the Art Holy Mountain"],

    ###
    "Temple of the Art Holy Mountain": ["Temple of the Art"],
    "Temple of the Art": ["Laboratory Holy Mountain", "The Tower", "Wizards' Den"],
    "Wizards' Den": ["Powerplant"],
    "Powerplant": ["Deep Underground"],

    ###
    "Laboratory Holy Mountain": ["The Laboratory"],
    "The Laboratory": ["The Work", "Friend Cave", "The Work (Hell)", "Lake"],
    ###
}

noita_regions: List[str] = sorted(set(noita_connections.keys()).union(*noita_connections.values()))
