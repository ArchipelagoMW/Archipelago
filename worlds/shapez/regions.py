from typing import Callable, Dict, Tuple, List

from BaseClasses import Entrance, Region, CollectionState, MultiWorld, LocationProgressType, ItemClassification
from .items import ShapezItem
from .locations import ShapezLocation

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
    # "Cut Shape Achievements",
    # "Rotated Shape Achievements",
    # "Stacked Shape Achievements",
    # "Painted Shape Achievements",
    # "Stored Shape Achievements",
    # "Trashed Shape Achievements",
    # "Wiring Achievements",
    "All Buildings Shapes"
] + [
  f"Shapesanity {processing} {coloring}"
  for processing in ["Unprocessed", "Cut", "Cut Rotated", "Stitched", "Half-Half"]
  for coloring in ["Uncolored", "Mixed", "Painted"]
]


def create_entrance(player: int, name: str, parent: Region, connects: Region,
                    rule: Callable[[CollectionState], bool]) -> None:
    """Creates an entrance with a given access rule and connects both regions"""
    # Create conditional entrance further into the game
    entr = Entrance(player, name, parent)
    entr.connected_region = connects
    entr.access_rule = rule
    parent.exits.append(entr)
    connects.entrances.append(entr)
    # Create open entrance that leads back
    entrback = Entrance(player, name + " back", connects)
    entrback.connected_region = parent
    connects.exits.append(entrback)
    parent.entrances.append(entrback)


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
    goal_region.locations.append(goal_location)
    multiworld.completion_condition[player] = lambda state: state.has("Goal", player)

    # Create Entrances for regions
#    create_entrance(player, "Cutter needed", regions["Main"], regions["Cut Shape Achievements"],
#                    lambda state: state.has("Cutter", player))
#    create_entrance(player, "Rotator needed", regions["Main"], regions["Rotated Shape Achievements"],
#                    lambda state: state.has("Rotator", player))
#    create_entrance(player, "Stacker needed", regions["Main"], regions["Stacked Shape Achievements"],
#                    lambda state: state.has("Stacker", player))
#    create_entrance(player, "Painter needed", regions["Main"], regions["Painted Shape Achievements"],
#                    lambda state: state.has("Painter", player))
#    create_entrance(player, "Storage needed", regions["Main"], regions["Stored Shape Achievements"],
#                    lambda state: state.has("Storage", player))
#    create_entrance(player, "Trash needed", regions["Main"], regions["Trashed Shape Achievements"],
#                    lambda state: state.has("Trash", player))
#    create_entrance(player, "Wires needed", regions["Main"], regions["Wiring Achievements"],
#                    lambda state: state.has("Wires", player))

#    create_entrance(player, "More than cutter needed",
#                    regions["Cut Shape Achievements"], regions["All Buildings Shapes"],
#                    lambda state: state.has_all(["Rotator", "Stacker", "Painter", "Color Mixer"], player))
#    create_entrance(player, "More than rotator needed",
#                    regions["Rotated Shape Achievements"], regions["All Buildings Shapes"],
#                    lambda state: state.has_all(["Cutter", "Stacker", "Painter", "Color Mixer"], player))
#    create_entrance(player, "More than stacker needed",
#                    regions["Stacked Shape Achievements"], regions["All Buildings Shapes"],
#                    lambda state: state.has_all(["Rotator", "Cutter", "Painter", "Color Mixer"], player))
#    create_entrance(player, "More than painter needed",
#                    regions["Painted Shape Achievements"], regions["All Buildings Shapes"],
#                    lambda state: state.has_all(["Rotator", "Stacker", "Cutter", "Color Mixer"], player))

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

    # regions["Main"].connect(regions["Levels with 1 Building"], "First level building needed",
    #                         lambda state: state.has(level_logic_buildings[0], player))

    create_entrance(player, "First level building needed",
                    regions["Main"], regions["Levels with 1 Building"],
                    lambda state: state.has(level_logic_buildings[0], player))
    create_entrance(player, "Second level building needed",
                    regions["Levels with 1 Building"], regions["Levels with 2 Buildings"],
                    lambda state: state.has(level_logic_buildings[1], player))
    create_entrance(player, "Third level building needed",
                    regions["Levels with 2 Buildings"], regions["Levels with 3 Buildings"],
                    lambda state: state.has_all(level_buildings_3_needed, player))
    create_entrance(player, "Fourth level building needed",
                    regions["Levels with 3 Buildings"], regions["Levels with 4 Buildings"],
                    lambda state: state.has(level_logic_buildings[3], player))
    create_entrance(player, "Fifth level building needed",
                    regions["Levels with 4 Buildings"], regions["Levels with 5 Buildings"],
                    lambda state: state.has_all(level_buildings_5_needed, player))

    create_entrance(player, "First upgrade building needed",
                    regions["Main"], regions["Upgrades with 1 Building"],
                    lambda state: state.has(upgrade_logic_buildings[0], player))
    create_entrance(player, "Second upgrade building needed",
                    regions["Upgrades with 1 Building"], regions["Upgrades with 2 Buildings"],
                    lambda state: state.has(upgrade_logic_buildings[1], player))
    create_entrance(player, "Third upgrade building needed",
                    regions["Upgrades with 2 Buildings"], regions["Upgrades with 3 Buildings"],
                    lambda state: state.has_all(upgrade_buildings_3_needed, player))
    create_entrance(player, "Fourth upgrade building needed",
                    regions["Upgrades with 3 Buildings"], regions["Upgrades with 4 Buildings"],
                    lambda state: state.has(upgrade_logic_buildings[3], player))
    create_entrance(player, "Fifth upgrade building needed",
                    regions["Upgrades with 4 Buildings"], regions["Upgrades with 5 Buildings"],
                    lambda state: state.has_all(upgrade_buildings_5_needed, player))

    create_entrance(player, "All buildings needed",
                    regions["Main"], regions["All Buildings Shapes"],
                    lambda state: state.has_all(["Cutter", "Rotator", "Stacker", "Painter", "Color Mixer"], player))

    create_entrance(player, "Shapesanity nothing",
                    regions["Main"], regions["Shapesanity Unprocessed Uncolored"], lambda state: True)
    create_entrance(player, "Shapesanity basic painting Unprocessed",
                    regions["Shapesanity Unprocessed Uncolored"], regions["Shapesanity Unprocessed Painted"],
                    lambda state: state.has("Painter", player))
    create_entrance(player, "Shapesanity cutting Uncolored",
                    regions["Shapesanity Unprocessed Uncolored"], regions["Shapesanity Cut Uncolored"],
                    lambda state: state.has("Cutter", player))
    create_entrance(player, "Shapesanity mixed painting Unprocessed",
                    regions["Shapesanity Unprocessed Painted"], regions["Shapesanity Unprocessed Mixed"],
                    lambda state: state.has("Color Mixer", player))
    create_entrance(player, "Shapesanity cutting Painted",
                    regions["Shapesanity Unprocessed Painted"], regions["Shapesanity Cut Painted"],
                    lambda state: state.has("Cutter", player))
    create_entrance(player, "Shapesanity cutting Mixed",
                    regions["Shapesanity Unprocessed Mixed"], regions["Shapesanity Cut Mixed"],
                    lambda state: state.has("Cutter", player))
    create_entrance(player, "Shapesanity basic painting Cut",
                    regions["Shapesanity Cut Uncolored"], regions["Shapesanity Cut Painted"],
                    lambda state: state.has("Painter", player))
    create_entrance(player, "Shapesanity rotating Uncolored",
                    regions["Shapesanity Cut Uncolored"], regions["Shapesanity Cut Rotated Uncolored"],
                    lambda state: state.has("Rotator", player))
    create_entrance(player, "Shapesanity stacking Uncolored",
                    regions["Shapesanity Cut Uncolored"], regions["Shapesanity Half-Half Uncolored"],
                    lambda state: state.has("Stacker", player))
    create_entrance(player, "Shapesanity mixed painting Cut",
                    regions["Shapesanity Cut Painted"], regions["Shapesanity Cut Mixed"],
                    lambda state: state.has("Color Mixer", player))
    create_entrance(player, "Shapesanity rotating Painted",
                    regions["Shapesanity Cut Painted"], regions["Shapesanity Cut Rotated Painted"],
                    lambda state: state.has("Rotator", player))
    create_entrance(player, "Shapesanity stacking Painted",
                    regions["Shapesanity Cut Painted"], regions["Shapesanity Half-Half Painted"],
                    lambda state: state.has("Stacker", player))
    create_entrance(player, "Shapesanity rotating Mixed",
                    regions["Shapesanity Cut Mixed"], regions["Shapesanity Cut Rotated Mixed"],
                    lambda state: state.has("Rotator", player))
    create_entrance(player, "Shapesanity stacking Mixed",
                    regions["Shapesanity Cut Mixed"], regions["Shapesanity Half-Half Mixed"],
                    lambda state: state.has("Stacker", player))
    create_entrance(player, "Shapesanity basic painting Rotated",
                    regions["Shapesanity Cut Rotated Uncolored"], regions["Shapesanity Cut Rotated Painted"],
                    lambda state: state.has("Painter", player))
    create_entrance(player, "Shapesanity stacking Cut Rotated Uncolored",
                    regions["Shapesanity Cut Rotated Uncolored"], regions["Shapesanity Stitched Uncolored"],
                    lambda state: state.has("Stacker", player))
    create_entrance(player, "Shapesanity mixed painting Rotated",
                    regions["Shapesanity Cut Rotated Painted"], regions["Shapesanity Cut Rotated Mixed"],
                    lambda state: state.has("Color Mixer", player))
    create_entrance(player, "Shapesanity stacking Cut Rotated Painted",
                    regions["Shapesanity Cut Rotated Painted"], regions["Shapesanity Stitched Painted"],
                    lambda state: state.has("Stacker", player))
    create_entrance(player, "Shapesanity stacking Cut Rotated Mixed",
                    regions["Shapesanity Cut Rotated Mixed"], regions["Shapesanity Stitched Mixed"],
                    lambda state: state.has("Stacker", player))
    create_entrance(player, "Shapesanity basic painting Stitched",
                    regions["Shapesanity Stitched Uncolored"], regions["Shapesanity Stitched Painted"],
                    lambda state: state.has("Painter", player))
    create_entrance(player, "Shapesanity mixed painting Stitched",
                    regions["Shapesanity Stitched Painted"], regions["Shapesanity Stitched Mixed"],
                    lambda state: state.has("Color Mixer", player))
    create_entrance(player, "Shapesanity basic painting Half-Half",
                    regions["Shapesanity Half-Half Uncolored"], regions["Shapesanity Half-Half Painted"],
                    lambda state: state.has("Painter", player))
    create_entrance(player, "Shapesanity rotating Half-Half Uncolored",
                    regions["Shapesanity Half-Half Uncolored"], regions["Shapesanity Stitched Uncolored"],
                    lambda state: state.has("Rotator", player))
    create_entrance(player, "Shapesanity mixed painting Half-Half",
                    regions["Shapesanity Half-Half Painted"], regions["Shapesanity Half-Half Mixed"],
                    lambda state: state.has("Color Mixer", player))
    create_entrance(player, "Shapesanity rotating Half-Half Painted",
                    regions["Shapesanity Half-Half Painted"], regions["Shapesanity Stitched Painted"],
                    lambda state: state.has("Rotator", player))
    create_entrance(player, "Shapesanity rotating Half-Half Mixed",
                    regions["Shapesanity Half-Half Mixed"], regions["Shapesanity Stitched Mixed"],
                    lambda state: state.has("Rotator", player))

    return list(regions.values())
