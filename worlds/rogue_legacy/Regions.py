from typing import Dict, List, NamedTuple, Optional

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import RLLocation, location_table, get_locations_by_category


class RLRegionData(NamedTuple):
    locations: Optional[List[str]]
    region_exits: Optional[List[str]]


def create_regions(multiworld: MultiWorld, player: int):
    regions: Dict[str, RLRegionData] = {
        "Menu":              RLRegionData(None, ["Castle Hamson"]),
        "The Manor":         RLRegionData([],   []),
        "Castle Hamson":     RLRegionData([],   ["Forest Abkhazia", "The Maya", "Land of Darkness",
                                                 "The Fountain Room", "The Manor"]),
        "Forest Abkhazia":   RLRegionData([],   []),
        "The Maya":          RLRegionData([],   []),
        "Land of Darkness":  RLRegionData([],   []),
        "The Fountain Room": RLRegionData([],   None),
    }

    # Artificially stagger diary spheres for progression.
    for diary in range(0, 25):
        region: str
        if 0 <= diary < 6:
            region = "Castle Hamson"
        elif 6 <= diary < 12:
            region = "Forest Abkhazia"
        elif 12 <= diary < 18:
            region = "The Maya"
        elif 18 <= diary < 24:
            region = "Land of Darkness"
        else:
            region = "The Fountain Room"
        regions[region].locations.append(f"Diary {diary + 1}")

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
