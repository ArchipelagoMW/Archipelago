from typing import Dict, List, Set

from BaseClasses import Entrance, Region
from .Locations import KH1Location, KH1LocationData, event_location_table, location_table


REGION_EXITS: Dict[str, List[str]] = {
    "Menu":             ["Awakening", "Levels", "World Map"],
    "Awakening":        [],
    "Destiny Islands":  [],
    "Traverse Town":    [],
    "Wonderland":       [],
    "Olympus Coliseum": [],
    "Deep Jungle":      [],
    "Agrabah":          [],
    "Monstro":          [],
    "Atlantica":        [],
    "Halloween Town":   [],
    "Neverland":        [],
    "Hollow Bastion":   [],
    "End of the World": [],
    "100 Acre Wood":    [],
    "Levels":           [],
    "Homecoming":       [],
    "Accessories":      [],
    "World Map":        ["Destiny Islands", "Traverse Town", "Wonderland", "Olympus Coliseum", "Deep Jungle",
                         "Agrabah", "Monstro", "Atlantica", "Halloween Town", "Neverland", "Hollow Bastion",
                         "End of the World", "100 Acre Wood", "Homecoming", "Accessories"],
}

OPTION_DRIVEN_LOCATION_GROUPS: Set[str] = {"Levels", "Accessory", "Augment"}


def get_active_locations(kh1world) -> Dict[str, KH1LocationData]:
    option_driven_names = set(kh1world.get_level_locations())
    option_driven_names.update(kh1world.get_starting_accessory_locations())
    option_driven_names.update(kh1world.get_accessory_locations())
    active = {name: data for name, data in location_table.items()
              if OPTION_DRIVEN_LOCATION_GROUPS.isdisjoint((data.region, *data.groups)) or name in option_driven_names}
    return active | event_location_table


def create_regions(kh1world):
    player = kh1world.player
    regions = {name: Region(name, player, kh1world.multiworld) for name in REGION_EXITS}

    for name, data in get_active_locations(kh1world).items():
        region = regions[data.region]
        region.locations.append(KH1Location(player, name, data.code, region))

    for name, exits in REGION_EXITS.items():
        regions[name].exits += [Entrance(player, exit, regions[name]) for exit in exits]

    kh1world.multiworld.regions += regions.values()


def connect_entrances(kh1world):
    for exits in REGION_EXITS.values():
        for exit in exits:
            kh1world.get_entrance(exit).connect(kh1world.get_region(exit))
