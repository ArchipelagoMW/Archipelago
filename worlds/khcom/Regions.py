from typing import Dict, List, NamedTuple, Optional

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import KHCOMLocation, location_table, get_locations_by_category


class KHCOMRegionData(NamedTuple):
    locations: Optional[List[str]]
    region_exits: Optional[List[str]]


def create_regions(multiworld: MultiWorld, player: int):
    regions: Dict[str, RLRegionData] = {
        "Menu": KHCOMRegionData(None, ["Floor 1"]),
        "Floor 1": KHCOMRegionData([], ["Warp 1"]),
        "Warp 1": KHCOMRegionData([], ["Floor 2", "Floor 3", "Floor 4", "Floor 5", "Floor 6"]),
        "Floor 2": KHCOMRegionData([], []),
        "Floor 3": KHCOMRegionData([], []),
        "Floor 4": KHCOMRegionData([], []),
        "Floor 5": KHCOMRegionData([], []),
        "Floor 6": KHCOMRegionData([], ["Warp 2"]),
        "Warp 2": KHCOMRegionData([], ["Floor 7", "Floor 8", "Floor 9"]),
        "Floor 7": KHCOMRegionData([], []),
        "Floor 8": KHCOMRegionData([], []),
        "Floor 9": KHCOMRegionData([], ["Floor 10"]),
        "Floor 10": KHCOMRegionData([], ["Floor 11"]),
        "Floor 11": KHCOMRegionData([], ["Floor 12"]),
        "Floor 12": KHCOMRegionData([], ["Floor 13"]),
        "Floor 13": KHCOMRegionData([], ["Floor 14"]),
    }

    # Manor & Special
    for manor in get_locations_by_category("Manor").keys():
        regions["The Manor"].locations.append(manor)
    for special in get_locations_by_category("Special").keys():
        regions["Castle Hamson"].locations.append(special)

    # Boss Rewards
    regions["Castle Hamson"].locations.append("Castle Hamson Boss Reward")
    regions["Forest Abkhazia"].locations.append("Forest Abkhazia Boss Reward")
    regions["The Maya"].locations.append("The Maya Boss Reward")
    regions["Land of Darkness"].locations.append("Land of Darkness Boss Reward")

    # Events
    regions["Castle Hamson"].locations.append("Castle Hamson Boss Room")
    regions["Forest Abkhazia"].locations.append("Forest Abkhazia Boss Room")
    regions["The Maya"].locations.append("The Maya Boss Room")
    regions["Land of Darkness"].locations.append("Land of Darkness Boss Room")
    regions["The Fountain Room"].locations.append("Fountain Room")

    # Chests
    chests = int(multiworld.chests_per_zone[player])
    for i in range(0, chests):
        if multiworld.universal_chests[player]:
            regions["Castle Hamson"].locations.append(f"Chest {i + 1}")
            regions["Forest Abkhazia"].locations.append(f"Chest {i + 1 + chests}")
            regions["The Maya"].locations.append(f"Chest {i + 1 + (chests * 2)}")
            regions["Land of Darkness"].locations.append(f"Chest {i + 1 + (chests * 3)}")
        else:
            regions["Castle Hamson"].locations.append(f"Castle Hamson - Chest {i + 1}")
            regions["Forest Abkhazia"].locations.append(f"Forest Abkhazia - Chest {i + 1}")
            regions["The Maya"].locations.append(f"The Maya - Chest {i + 1}")
            regions["Land of Darkness"].locations.append(f"Land of Darkness - Chest {i + 1}")

    # Fairy Chests
    chests = int(multiworld.fairy_chests_per_zone[player])
    for i in range(0, chests):
        if multiworld.universal_fairy_chests[player]:
            regions["Castle Hamson"].locations.append(f"Fairy Chest {i + 1}")
            regions["Forest Abkhazia"].locations.append(f"Fairy Chest {i + 1 + chests}")
            regions["The Maya"].locations.append(f"Fairy Chest {i + 1 + (chests * 2)}")
            regions["Land of Darkness"].locations.append(f"Fairy Chest {i + 1 + (chests * 3)}")
        else:
            regions["Castle Hamson"].locations.append(f"Castle Hamson - Fairy Chest {i + 1}")
            regions["Forest Abkhazia"].locations.append(f"Forest Abkhazia - Fairy Chest {i + 1}")
            regions["The Maya"].locations.append(f"The Maya - Fairy Chest {i + 1}")
            regions["Land of Darkness"].locations.append(f"Land of Darkness - Fairy Chest {i + 1}")

    # Set up the regions correctly.
    for name, data in regions.items():
        multiworld.regions.append(create_region(multiworld, player, name, data))

    multiworld.get_entrance("Castle Hamson", player).connect(multiworld.get_region("Castle Hamson", player))
    multiworld.get_entrance("The Manor", player).connect(multiworld.get_region("The Manor", player))
    multiworld.get_entrance("Forest Abkhazia", player).connect(multiworld.get_region("Forest Abkhazia", player))
    multiworld.get_entrance("The Maya", player).connect(multiworld.get_region("The Maya", player))
    multiworld.get_entrance("Land of Darkness", player).connect(multiworld.get_region("Land of Darkness", player))
    multiworld.get_entrance("The Fountain Room", player).connect(multiworld.get_region("The Fountain Room", player))


def create_region(multiworld: MultiWorld, player: int, name: str, data: RLRegionData):
    region = Region(name, player, multiworld)
    if data.locations:
        for loc_name in data.locations:
            loc_data = location_table.get(loc_name)
            location = RLLocation(player, loc_name, loc_data.code if loc_data else None, region)
            region.locations.append(location)

    if data.region_exits:
        for exit in data.region_exits:
            entrance = Entrance(player, exit, region)
            region.exits.append(entrance)

    return region
