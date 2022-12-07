from typing import NamedTuple, List, Dict

from BaseClasses import MultiWorld, Region, Entrance, RegionType
from . import V6Location, location_table

v6_areas = ["Laboratory", "The Tower", "Space Station 2", "Warp Zone"]


class V6RegionData(NamedTuple):
    exits: List[str]
    locations: List[str]


regions_table: Dict[str, V6RegionData] = {
    "Menu": V6RegionData(["Dimension VVVVVV"], []),

    "Dimension VVVVVV": V6RegionData(["Laboratory", "The Tower", "Space Station 2", "Warp Zone"], [
        "Overworld (Pipe-shaped Segment)", "Overworld (Left of Ship)", "Overworld (Square Room)",
        "Overworld (Sad Elephant)", "It's a Secret to Nobody", "Trench Warfare", "NPC Trinket", "V"]),

    "Laboratory": V6RegionData([], [
        "Young Man, It's Worth the Challenge", "Overworld (Outside Entanglement Generator)", "The Tantalizing Trinket",
        "Purest Unobtainium"]),

    "The Tower": V6RegionData([], ["The Tower 1", "The Tower 2"]),

    "Space Station 2": V6RegionData([], [
        "One Way Room", "You Just Keep Coming Back", "Clarion Call", "Prize for the Reckless",
        "Doing things the hard way"]),

    "Warp Zone": V6RegionData([], ["Edge Games"]),
}


def create_regions(multiworld: MultiWorld, player: int):
    regions: List[Region] = []
    for region_name, region_data in regions_table.items():
        region = Region(region_name, RegionType.Generic, region_name, player, multiworld)
        for location in region_data.locations:
            region.locations.append(V6Location(player, location, location_table[location], region))

        for region_exit in region_data.exits:
            region.exits.append(Entrance(player, region_exit, region))

        regions.append(region)

    # Assign regions.
    multiworld.regions += regions

    # Connect regions.
    multiworld.get_entrance("Dimension VVVVVV", player).connect(multiworld.get_region("Dimension VVVVVV", player))
    multiworld.get_entrance("Laboratory", player).connect(multiworld.get_region("Laboratory", player))
    multiworld.get_entrance("The Tower", player).connect(multiworld.get_region("The Tower", player))
    multiworld.get_entrance("Space Station 2", player).connect(multiworld.get_region("Space Station 2", player))
    multiworld.get_entrance("Dimension VVVVVV", player).connect(multiworld.get_region("Dimension VVVVVV", player))
    multiworld.get_entrance("Warp Zone", player).connect(multiworld.get_region("Warp Zone", player))
