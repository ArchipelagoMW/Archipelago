from typing import Dict, Tuple, List

from BaseClasses import Region, MultiWorld, LocationProgressType, ItemClassification
from .items import ShapezItem
from .locations import ShapezLocation
from worlds.generic.Rules import add_rule

all_regions = [
    "Main",
    "Levels with 1 Building",
    "Levels with 2 Buildings",
    "Levels with 3 Buildings",
    "Levels with 4 Buildings",
    "Levels with 5 Buildings",
    "Upgrades with 1 Building",
    "Upgrades with 2 Buildings",
    "Upgrades with 3 Buildings",
    "Upgrades with 4 Buildings",
    "Upgrades with 5 Buildings",
    "Cut Shape Achievements",
    "Rotated Shape Achievements",
    "Stacked Shape Achievements",
    "Painted Shape Achievements",
    "Stored Shape Achievements",
    "Trashed Shape Achievements",
    "Wiring Achievements",
    "All Buildings Shapes"
] + [
  f"Shapesanity {processing} {coloring}"
  for processing in ["Unprocessed", "Cut", "Cut Rotated", "Stitched", "Half-Half"]
  for coloring in ["Uncolored", "Mixed", "Painted"]
]


def create_shapez_regions(player: int, multiworld: MultiWorld,
                          included_locations: Dict[str, Tuple[str, LocationProgressType]],
                          location_name_to_id: Dict[str, int], level_logic_buildings: List[str],
                          upgrade_logic_buildings: List[str], early_useful: str, goal: str) -> List[Region]:
    """Creates and returns a list of all regions with entrances and all locations placed correctly."""
    regions: Dict[str, Region] = {name: Region(name, player, multiworld) for name in all_regions}

    # Creates ShapezLocations for every included location and puts them into the correct region
    for name, data in included_locations.items():
        regions[data[0]].locations.append(ShapezLocation(player, name, location_name_to_id[name],
                                                         regions[data[0]], data[1]))

    if goal in ["vanilla", "mam"]:
        goal_region = regions["Levels with 5 Buildings"]
    elif goal == "even_fasterer":
        goal_region = regions["Upgrades with 5 Buildings"]
    else:
        goal_region = regions["All Buildings Shapes"]
    goal_location = ShapezLocation(player, "Goal", None, goal_region,
                                   LocationProgressType.DEFAULT)
    goal_location.place_locked_item(ShapezItem("Goal", ItemClassification.progression, None, player))
    if goal == "efficiency_iii":
        add_rule(goal_location, lambda state: state.has("Big Belt Upgrade", player, 7))
    goal_region.locations.append(goal_location)
    multiworld.completion_condition[player] = lambda state: state.has("Goal", player)

    # Create Entrances for regions
    regions["Main"].connect(regions["Cut Shape Achievements"], "Cutter needed",
                            lambda state: state.has("Cutter", player))
    regions["Main"].connect(regions["Rotated Shape Achievements"], "Rotator needed",
                            lambda state: state.has("Rotator", player))
    regions["Main"].connect(regions["Stacked Shape Achievements"], "Stacker needed",
                            lambda state: state.has("Stacker", player))
    regions["Main"].connect(regions["Painted Shape Achievements"], "Painter needed",
                            lambda state: state.has("Painter", player))
    regions["Main"].connect(regions["Stored Shape Achievements"], "Storage needed",
                            lambda state: state.has("Storage", player))
    regions["Main"].connect(regions["Trashed Shape Achievements"], "Trash needed",
                            lambda state: state.has("Trash", player))
    regions["Main"].connect(regions["Wiring Achievements"], "Wires needed",
                            lambda state: state.has("Wires", player))

    regions["Main"].connect(regions["All Buildings Shapes"], "All buildings needed",
                            lambda state: state.has_all(["Cutter", "Rotator", "Stacker",
                                                         "Painter", "Color Mixer"], player))

    # Add balancer, tunnel, and trash to early items if options say so
    level_buildings_3_needed: List[str] = [level_logic_buildings[2]]
    level_buildings_5_needed: List[str] = [level_logic_buildings[4]]
    upgrade_buildings_3_needed: List[str] = [upgrade_logic_buildings[2]]
    upgrade_buildings_5_needed: List[str] = [upgrade_logic_buildings[4]]
    if early_useful == "3_buildings":
        level_buildings_3_needed.extend(["Balancer", "Tunnel", "Trash"])
        upgrade_buildings_3_needed.extend(["Balancer", "Tunnel", "Trash"])
    elif early_useful == "5_buildings":
        level_buildings_5_needed.extend(["Balancer", "Tunnel", "Trash"])
        upgrade_buildings_5_needed.extend(["Balancer", "Tunnel", "Trash"])

    regions["Main"].connect(regions["Levels with 1 Building"], "First level building needed",
                            lambda state: state.has(level_logic_buildings[0], player))
    regions["Levels with 1 Building"].connect(regions["Levels with 2 Buildings"], "Second level building needed",
                                              lambda state: state.has(level_logic_buildings[1], player))
    regions["Levels with 2 Buildings"].connect(regions["Levels with 3 Buildings"], "Third level building needed",
                                               lambda state: state.has_all(level_buildings_3_needed, player))
    regions["Levels with 3 Buildings"].connect(regions["Levels with 4 Buildings"], "Fourth level building needed",
                                               lambda state: state.has(level_logic_buildings[3], player))
    regions["Levels with 4 Buildings"].connect(regions["Levels with 5 Buildings"], "Fifth level building needed",
                                               lambda state: state.has_all(level_buildings_5_needed, player))
    regions["Main"].connect(regions["Upgrades with 1 Building"], "First upgrade building needed",
                            lambda state: state.has(upgrade_logic_buildings[0], player))
    regions["Upgrades with 1 Building"].connect(regions["Upgrades with 2 Buildings"], "Second upgrade building needed",
                                                lambda state: state.has(upgrade_logic_buildings[1], player))
    regions["Upgrades with 2 Buildings"].connect(regions["Upgrades with 3 Buildings"], "Third upgrade building needed",
                                                 lambda state: state.has_all(upgrade_buildings_3_needed, player))
    regions["Upgrades with 3 Buildings"].connect(regions["Upgrades with 4 Buildings"], "Fourth upgrade building needed",
                                                 lambda state: state.has(upgrade_logic_buildings[3], player))
    regions["Upgrades with 4 Buildings"].connect(regions["Upgrades with 5 Buildings"], "Fifth upgrade building needed",
                                                 lambda state: state.has_all(upgrade_buildings_5_needed, player))

    regions["Main"].connect(regions["Shapesanity Unprocessed Uncolored"], "Shapesanity nothing",
                            lambda state: True)
    regions["Main"].connect(regions["Shapesanity Unprocessed Painted"], "Shapesanity painting",
                            lambda state: state.has("Painter", player))
    regions["Shapesanity Unprocessed Painted"].connect(regions["Shapesanity Unprocessed Mixed"], "Shapesanity mixing",
                                                       lambda state: state.has("Color Mixer", player))
    regions["Main"].connect(regions["Shapesanity Cut Uncolored"], "Shapesanity cutting",
                            lambda state: state.has("Cutter", player))
    regions["Shapesanity Cut Uncolored"].connect(regions["Shapesanity Cut Painted"], "Shapesanity painting cut",
                                                 lambda state: state.has("Painter", player))
    regions["Shapesanity Cut Painted"].connect(regions["Shapesanity Cut Mixed"], "Shapesanity mixing cut",
                                               lambda state: state.has("Color Mixer", player))
    regions["Shapesanity Cut Uncolored"].connect(regions["Shapesanity Cut Rotated Uncolored"],
                                                 "Shapesanity rotating cut",
                                                 lambda state: state.has("Rotator", player))
    regions["Shapesanity Cut Painted"].connect(regions["Shapesanity Cut Rotated Painted"],
                                               "Shapesanity rotating cut painted",
                                               lambda state: state.has("Rotator", player))
    regions["Shapesanity Cut Mixed"].connect(regions["Shapesanity Cut Rotated Mixed"], "Shapesanity rotating cut mixed",
                                             lambda state: state.has("Rotator", player))
    regions["Shapesanity Cut Uncolored"].connect(regions["Shapesanity Half-Half Uncolored"], "Shapesanity stacking cut",
                                                 lambda state: state.has("Stacker", player))
    regions["Shapesanity Cut Painted"].connect(regions["Shapesanity Half-Half Painted"],
                                               "Shapesanity stacking cut painted",
                                               lambda state: state.has("Stacker", player))
    regions["Shapesanity Cut Mixed"].connect(regions["Shapesanity Half-Half Mixed"], "Shapesanity stacking cut mixed",
                                             lambda state: state.has("Stacker", player))
    regions["Shapesanity Cut Rotated Uncolored"].connect(regions["Shapesanity Stitched Uncolored"],
                                                         "Shapesanity stitching",
                                                         lambda state: state.has("Stacker", player))
    regions["Shapesanity Stitched Uncolored"].connect(regions["Shapesanity Stitched Painted"],
                                                      "Shapesanity painting stitched",
                                                      lambda state: state.has("Painter", player))
    regions["Shapesanity Stitched Painted"].connect(regions["Shapesanity Stitched Mixed"],
                                                    "Shapesanity mixing stitched",
                                                    lambda state: state.has("Color Mixer", player))

    return list(regions.values())
