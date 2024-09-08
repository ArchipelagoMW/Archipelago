from typing import Dict, Tuple, List

from BaseClasses import Region, MultiWorld, LocationProgressType, ItemClassification, CollectionState
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
    "Blueprint Achievements",
    "MAM needed",
    "All Buildings Shapes"
] + [
  f"Shapesanity {processing} {coloring}"
  for processing in ["Unprocessed", "Cut", "Cut Rotated", "Stitched", "Half-Half"]
  for coloring in ["Uncolored", "Mixed", "Painted"]
]


def has_cutter(state: CollectionState, player: int) -> bool:
    return state.has("Cutter", player)


def has_rotator(state: CollectionState, player: int) -> bool:
    return state.has_any(["Rotator", "Rotator (CCW)"], player)


def has_stacker(state: CollectionState, player: int) -> bool:
    return state.has("Stacker", player)


def has_painter(state: CollectionState, player: int) -> bool:
    return (state.has_any(["Painter", "Double Painter"], player) or
            (state.has_all(["Quad Painter", "Wires"], player) and
             state.has_any(["Switch", "Constant Signal"], player)))


def has_mixer(state: CollectionState, player: int) -> bool:
    return state.has("Color Mixer", player)


def has_tunnel(state: CollectionState, player: int) -> bool:
    return state.has_any(["Tunnel", "Tunnel Tier II"], player)


def has_balancer(state: CollectionState, player: int) -> bool:
    return state.has("Balancer", player) or state.has_all(["Compact Merger", "Compact Splitter"], player)


def can_build_mam(state: CollectionState, player: int) -> bool:
    return has_cutter(state, player) and has_rotator(state, player) and has_stacker(state, player) and \
           has_painter(state, player) and has_mixer(state, player) and has_balancer(state, player) and \
           has_tunnel(state, player) and state.has_all(["Belt Reader", "Storage", "Item Filter", "Wires",
                                                        "Logic Gates", "Virtual Processing"], player)


def has_cutter_rotator(state: CollectionState, player: int) -> bool:
    return (has_cutter(state, player) and has_rotator(state, player)) or state.has("Quad Cutter", player)


def has_logic_list_building(state: CollectionState, player: int, buildings: str, includeuseful: bool) -> bool:
    if includeuseful:
        useful = state.has("Trash", player) and has_balancer(state, player) and has_tunnel(state, player)
    else:
        useful = True
    if buildings == "Cutter":
        return useful and has_cutter(state, player)
    elif buildings == "Rotator":
        return useful and has_cutter_rotator(state, player)
    elif buildings == "Stacker":
        return useful and has_stacker(state, player)
    elif buildings == "Painter":
        return useful and has_painter(state, player)
    elif buildings == "Color Mixer":
        return useful and has_mixer(state, player)


def create_shapez_regions(player: int, multiworld: MultiWorld,
                          included_locations: Dict[str, Tuple[str, LocationProgressType]],
                          location_name_to_id: Dict[str, int], level_logic_buildings: List[str],
                          upgrade_logic_buildings: List[str], early_useful: str, goal: str,
                          menu_region: Region) -> List[Region]:
    """Creates and returns a list of all regions with entrances and all locations placed correctly."""
    regions: Dict[str, Region] = {name: Region(name, player, multiworld) for name in all_regions}
    regions["Menu"] = menu_region

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
                            lambda state: has_cutter(state, player))
    regions["Main"].connect(regions["Rotated Shape Achievements"], "Rotator needed",
                            lambda state: has_rotator(state, player))
    regions["Main"].connect(regions["Stacked Shape Achievements"], "Stacker needed",
                            lambda state: has_stacker(state, player))
    regions["Main"].connect(regions["Painted Shape Achievements"], "Painter needed",
                            lambda state: has_painter(state, player))
    regions["Main"].connect(regions["Stored Shape Achievements"], "Storage needed",
                            lambda state: state.has("Storage", player))
    regions["Main"].connect(regions["Trashed Shape Achievements"], "Trash needed",
                            lambda state: state.has("Trash", player))
    regions["Main"].connect(regions["Wiring Achievements"], "Wires needed",
                            lambda state: state.has("Wires", player))
    regions["Main"].connect(regions["Blueprint Achievements"], "Blueprints needed",
                            lambda state: state.has("Blueprints", player))
    regions["Main"].connect(regions["MAM needed"], "Building a MAM",
                            lambda state: can_build_mam(state, player))

    regions["Main"].connect(regions["All Buildings Shapes"], "All buildings needed",
                            lambda state: has_cutter(state, player) and has_rotator(state, player) and
                                          has_stacker(state, player) and has_painter(state, player) and
                                          has_mixer(state, player))

    regions["Main"].connect(regions["Levels with 1 Building"], "First level building needed",
                            lambda state: has_logic_list_building(state, player, level_logic_buildings[0], False))
    regions["Levels with 1 Building"].connect(regions["Levels with 2 Buildings"], "Second level building needed",
                                              lambda state: has_logic_list_building(state, player,
                                                                                    level_logic_buildings[1], False))
    regions["Levels with 2 Buildings"].connect(regions["Levels with 3 Buildings"], "Third level building needed",
                                               lambda state: has_logic_list_building(state, player,
                                                                                     level_logic_buildings[2],
                                                                                     early_useful == "3_buildings"))
    regions["Levels with 3 Buildings"].connect(regions["Levels with 4 Buildings"], "Fourth level building needed",
                                               lambda state: has_logic_list_building(state, player,
                                                                                     level_logic_buildings[3], False))
    regions["Levels with 4 Buildings"].connect(regions["Levels with 5 Buildings"], "Fifth level building needed",
                                               lambda state: has_logic_list_building(state, player,
                                                                                     level_logic_buildings[4],
                                                                                     early_useful == "5_buildings"))
    regions["Main"].connect(regions["Upgrades with 1 Building"], "First upgrade building needed",
                            lambda state: has_logic_list_building(state, player, upgrade_logic_buildings[0], False))
    regions["Upgrades with 1 Building"].connect(regions["Upgrades with 2 Buildings"], "Second upgrade building needed",
                                                lambda state: has_logic_list_building(state, player,
                                                                                      upgrade_logic_buildings[1],
                                                                                      False))
    regions["Upgrades with 2 Buildings"].connect(regions["Upgrades with 3 Buildings"], "Third upgrade building needed",
                                                 lambda state: has_logic_list_building(state, player,
                                                                                       upgrade_logic_buildings[2],
                                                                                       early_useful == "3_buildings"))
    regions["Upgrades with 3 Buildings"].connect(regions["Upgrades with 4 Buildings"], "Fourth upgrade building needed",
                                                 lambda state: has_logic_list_building(state, player,
                                                                                       upgrade_logic_buildings[3],
                                                                                       False))
    regions["Upgrades with 4 Buildings"].connect(regions["Upgrades with 5 Buildings"], "Fifth upgrade building needed",
                                                 lambda state: has_logic_list_building(state, player,
                                                                                       upgrade_logic_buildings[4],
                                                                                       early_useful == "5_buildings"))

    regions["Main"].connect(regions["Shapesanity Unprocessed Uncolored"], "Shapesanity nothing",
                            lambda state: True)
    regions["Main"].connect(regions["Shapesanity Unprocessed Painted"], "Shapesanity painting",
                            lambda state: has_painter(state, player))
    regions["Shapesanity Unprocessed Painted"].connect(regions["Shapesanity Unprocessed Mixed"], "Shapesanity mixing",
                                                       lambda state: has_mixer(state, player))
    regions["Main"].connect(regions["Shapesanity Cut Uncolored"], "Shapesanity cutting",
                            lambda state: has_cutter(state, player))
    regions["Shapesanity Cut Uncolored"].connect(regions["Shapesanity Cut Painted"], "Shapesanity painting cut",
                                                 lambda state: has_painter(state, player))
    regions["Shapesanity Cut Painted"].connect(regions["Shapesanity Cut Mixed"], "Shapesanity mixing cut",
                                               lambda state: has_mixer(state, player))
    regions["Main"].connect(regions["Shapesanity Cut Rotated Uncolored"], "Shapesanity quad cutting",
                            lambda state: has_cutter_rotator(state, player))
    regions["Shapesanity Cut Uncolored"].connect(regions["Shapesanity Cut Rotated Uncolored"],
                                                 "Shapesanity rotating cut",
                                                 lambda state: has_rotator(state, player))
    regions["Shapesanity Cut Rotated Uncolored"].connect(regions["Shapesanity Cut Rotated Painted"],
                                                         "Shapesanity painting cut rotated",
                                                         lambda state: has_painter(state, player))
    regions["Shapesanity Cut Rotated Painted"].connect(regions["Shapesanity Cut Rotated Mixed"],
                                                       "Shapesanity mixing cut rotated",
                                                       lambda state: has_mixer(state, player))
    regions["Shapesanity Cut Uncolored"].connect(regions["Shapesanity Half-Half Uncolored"], "Shapesanity stacking cut",
                                                 lambda state: has_stacker(state, player))
    regions["Shapesanity Cut Painted"].connect(regions["Shapesanity Half-Half Painted"],
                                               "Shapesanity stacking cut painted",
                                               lambda state: has_stacker(state, player))
    regions["Shapesanity Cut Mixed"].connect(regions["Shapesanity Half-Half Mixed"], "Shapesanity stacking cut mixed",
                                             lambda state: has_stacker(state, player))
    regions["Shapesanity Cut Rotated Uncolored"].connect(regions["Shapesanity Stitched Uncolored"],
                                                         "Shapesanity stitching",
                                                         lambda state: has_stacker(state, player))
    regions["Shapesanity Stitched Uncolored"].connect(regions["Shapesanity Stitched Painted"],
                                                      "Shapesanity painting stitched",
                                                      lambda state: has_painter(state, player))
    regions["Shapesanity Stitched Painted"].connect(regions["Shapesanity Stitched Mixed"],
                                                    "Shapesanity mixing stitched",
                                                    lambda state: has_mixer(state, player))

    return list(regions.values())
