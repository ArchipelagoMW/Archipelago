from typing import Dict, Tuple, List

from BaseClasses import Region, MultiWorld, LocationProgressType, ItemClassification, CollectionState
from . import ShapezItem
from .locations import ShapezLocation
from .data.strings import ITEMS
from worlds.generic.Rules import add_rule

shapesanity_processing = ["Full", "Half", "Piece", "Stitched", "East Windmill", "Half-Half",
                          "Colorful East Windmill", "Colorful Half-Half", "Colorful Full", "Colorful Half"]

all_regions = [
    "Menu",
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
  for processing in shapesanity_processing
  for coloring in ["Uncolored", "Mixed", "Painted"]
]


def has_cutter(state: CollectionState, player: int) -> bool:
    return state.has("Cutter", player)


def has_rotator(state: CollectionState, player: int) -> bool:
    # 180 is excluded because of limited functionality
    return state.has_any(["Rotator", "Rotator (CCW)"], player)


def has_stacker(state: CollectionState, player: int) -> bool:
    return state.has("Stacker", player)


def has_painter(state: CollectionState, player: int) -> bool:
    return state.has_any(["Painter", "Double Painter"], player) or can_use_quad_painter(state, player)


def has_mixer(state: CollectionState, player: int) -> bool:
    return state.has("Color Mixer", player)


def has_tunnel(state: CollectionState, player: int) -> bool:
    return state.has_any(["Tunnel", "Tunnel Tier II"], player)


def has_balancer(state: CollectionState, player: int) -> bool:
    return state.has("Balancer", player) or state.has_all(["Compact Merger", "Compact Splitter"], player)


def can_use_quad_painter(state: CollectionState, player: int) -> bool:
    return state.has_all(["Quad Painter", "Wires"], player) and state.has_any(["Switch", "Constant Signal"], player)


def can_build_mam(state: CollectionState, player: int) -> bool:
    return (has_cutter(state, player) and has_rotator(state, player) and has_stacker(state, player) and
            has_painter(state, player) and has_mixer(state, player) and has_balancer(state, player) and
            has_tunnel(state, player) and state.has_all(["Belt Reader", "Storage", "Item Filter", "Wires",
                                                         "Logic Gates", "Virtual Processing"], player))


def can_make_stitched_shape(state: CollectionState, player: int) -> bool:
    return (state.has_any(["Cutter", "Quad Cutter"], player) and
            has_rotator(state, player) and has_stacker(state, player))


def can_make_east_windmill(state: CollectionState, player: int) -> bool:
    return (state.has_any(["Cutter", "Quad Cutter"], player) and
            state.has_any(["Rotator", "Rotator (CCW)", "Rotator (180°)"], player) and
            has_stacker(state, player))


def can_make_half_half_shape(state: CollectionState, player: int) -> bool:
    return state.has_any(["Cutter", "Quad Cutter"], player) and has_stacker(state, player)


def can_make_half_shape(state: CollectionState, player: int) -> bool:
    return has_cutter(state, player) or state.has_all(["Quad Cutter", "Stacker"], player)


def has_8x_belt_multiplier(state: CollectionState, player: int) -> bool:
    # One gigantic upgrade (+10) is enough
    if state.has(ITEMS.upgrade_gigantic_belt, player):
        return True
    multiplier = 1.0
    # Rising upgrades do the least improvement if received before other upgrades
    for _ in range(state.count(ITEMS.upgrade_rising_belt, player)):
        multiplier *= 2
    multiplier += state.count(ITEMS.upgrade_big_belt, player)
    multiplier += state.count(ITEMS.upgrade_small_belt, player)*0.1
    return multiplier >= 8


def has_logic_list_building(state: CollectionState, player: int, buildings: List[str], index: int,
                            includeuseful: bool) -> bool:

    # Includes balancer, tunnel, and trash in logic in order to make them appear in earlier spheres
    if includeuseful and not (state.has("Trash", player) and has_balancer(state, player) and has_tunnel(state, player)):
        return False

    if buildings[index] == "Cutter":
        if buildings.index("Stacker") < index:
            return state.has_any(["Cutter", "Quad Cutter"], player)
        else:
            return has_cutter(state, player)
    elif buildings[index] == "Rotator":
        return has_rotator(state, player)
    elif buildings[index] == "Stacker":
        return has_stacker(state, player)
    elif buildings[index] == "Painter":
        return has_painter(state, player)
    elif buildings[index] == "Color Mixer":
        return has_mixer(state, player)


def create_shapez_regions(player: int, multiworld: MultiWorld,
                          included_locations: Dict[str, Tuple[str, LocationProgressType]],
                          location_name_to_id: Dict[str, int], level_logic_buildings: List[str],
                          upgrade_logic_buildings: List[str], early_useful: str, goal: str,
                          lock_belt_and_extractor: bool) -> List[Region]:
    """Creates and returns a list of all regions with entrances and all locations placed correctly."""
    regions: Dict[str, Region] = {name: Region(name, player, multiworld) for name in all_regions}

    # Creates ShapezLocations for every included location and puts them into the correct region
    for name, data in included_locations.items():
        regions[data[0]].locations.append(ShapezLocation(player, name, location_name_to_id[name],
                                                         regions[data[0]], data[1]))

    # Create goal event
    if goal in ["vanilla", "mam"]:
        goal_region = regions["Levels with 5 Buildings"]
    elif goal == "even_fasterer":
        goal_region = regions["Upgrades with 5 Buildings"]
    else:
        goal_region = regions["All Buildings Shapes"]
    goal_location = ShapezLocation(player, "Goal", None, goal_region, LocationProgressType.DEFAULT)
    goal_location.place_locked_item(ShapezItem("Goal", ItemClassification.progression_skip_balancing, None, player))
    if goal == "efficiency_iii":
        add_rule(goal_location, lambda state: has_8x_belt_multiplier(state, player))
    goal_region.locations.append(goal_location)
    multiworld.completion_condition[player] = lambda state: state.has("Goal", player)

    # Connect Menu to rest of regions
    regions["Menu"].connect(regions["Main"], "Transportation",
                            lambda state: state.has_any(["Extractor", "Chaining Extractor"], player) and
                                          state.has_any(["Belt", "Compact Merger", "Compact Splitter"], player))

    # Connect Main to achievement regions
    regions["Main"].connect(regions["Cut Shape Achievements"], "Cutter needed",
                            lambda state: has_cutter(state, player))
    regions["Main"].connect(regions["Rotated Shape Achievements"], "Rotator needed",
                            lambda state: state.has("Rotator", player))
    regions["Main"].connect(regions["Stacked Shape Achievements"], "Stacker needed",
                            lambda state: has_stacker(state, player))
    regions["Main"].connect(regions["Painted Shape Achievements"], "Painter needed",
                            lambda state: state.has("Painter", player))
    regions["Main"].connect(regions["Stored Shape Achievements"], "Storage needed",
                            lambda state: state.has("Storage", player))
    regions["Main"].connect(regions["Trashed Shape Achievements"], "Trash needed",
                            lambda state: state.has("Trash", player))
    regions["Main"].connect(regions["Wiring Achievements"], "Wires needed",
                            lambda state: state.has("Wires", player))
    regions["Main"].connect(regions["Blueprint Achievements"], "Blueprints needed",
                            lambda state: state.has("Blueprints", player) and has_cutter(state, player) and
                                          has_rotator(state, player) and has_stacker(state, player) and
                                          has_painter(state, player) and has_mixer(state, player))
    regions["Main"].connect(regions["MAM needed"], "Building a MAM",
                            lambda state: can_build_mam(state, player))
    regions["Main"].connect(regions["All Buildings Shapes"], "All buildings needed",
                            lambda state: has_cutter(state, player) and has_rotator(state, player) and
                                          has_stacker(state, player) and has_painter(state, player) and
                                          has_mixer(state, player))

    # Progressively connect level and upgrade regions
    regions["Main"].connect(regions["Levels with 1 Building"], "First level building needed",
                            lambda state: has_logic_list_building(state, player, level_logic_buildings, 0, False))
    regions["Levels with 1 Building"].connect(regions["Levels with 2 Buildings"], "Second level building needed",
                                              lambda state: has_logic_list_building(state, player,
                                                                                    level_logic_buildings, 1, False))
    regions["Levels with 2 Buildings"].connect(regions["Levels with 3 Buildings"], "Third level building needed",
                                               lambda state: has_logic_list_building(state, player,
                                                                                     level_logic_buildings, 2,
                                                                                     early_useful == "3_buildings"))
    regions["Levels with 3 Buildings"].connect(regions["Levels with 4 Buildings"], "Fourth level building needed",
                                               lambda state: has_logic_list_building(state, player,
                                                                                     level_logic_buildings, 3, False))
    regions["Levels with 4 Buildings"].connect(regions["Levels with 5 Buildings"], "Fifth level building needed",
                                               lambda state: has_logic_list_building(state, player,
                                                                                     level_logic_buildings, 4,
                                                                                     early_useful == "5_buildings"))
    regions["Main"].connect(regions["Upgrades with 1 Building"], "First upgrade building needed",
                            lambda state: has_logic_list_building(state, player, upgrade_logic_buildings, 0, False))
    regions["Upgrades with 1 Building"].connect(regions["Upgrades with 2 Buildings"], "Second upgrade building needed",
                                                lambda state: has_logic_list_building(state, player,
                                                                                      upgrade_logic_buildings, 1,
                                                                                      False))
    regions["Upgrades with 2 Buildings"].connect(regions["Upgrades with 3 Buildings"], "Third upgrade building needed",
                                                 lambda state: has_logic_list_building(state, player,
                                                                                       upgrade_logic_buildings, 2,
                                                                                       early_useful == "3_buildings"))
    regions["Upgrades with 3 Buildings"].connect(regions["Upgrades with 4 Buildings"], "Fourth upgrade building needed",
                                                 lambda state: has_logic_list_building(state, player,
                                                                                       upgrade_logic_buildings, 3,
                                                                                       False))
    regions["Upgrades with 4 Buildings"].connect(regions["Upgrades with 5 Buildings"], "Fifth upgrade building needed",
                                                 lambda state: has_logic_list_building(state, player,
                                                                                       upgrade_logic_buildings, 4,
                                                                                       early_useful == "5_buildings"))

    # Connect Uncolored shapesanity regions to Main
    regions["Main"].connect(regions["Shapesanity Full Uncolored"], "Shapesanity always", lambda state: True)
    regions["Main"].connect(regions["Shapesanity Half Uncolored"], "Shapesanity cutting half",
                            lambda state: can_make_half_shape(state, player))
    regions["Main"].connect(regions["Shapesanity Piece Uncolored"], "Shapesanity cutting quarter",
                            lambda state: (has_cutter(state, player) and has_rotator(state, player)) or
                                          state.has("Quad Cutter", player))
    regions["Main"].connect(regions["Shapesanity Half-Half Uncolored"], "Shapesanity cutting half-half",
                            lambda state: can_make_half_half_shape(state, player))
    regions["Main"].connect(regions["Shapesanity Stitched Uncolored"], "Shapesanity stitching",
                            lambda state: can_make_stitched_shape(state, player))
    regions["Main"].connect(regions["Shapesanity East Windmill Uncolored"], "Shapesanity rotating windmill half",
                            lambda state: can_make_east_windmill(state, player))
    regions["Main"].connect(regions["Shapesanity Colorful Full Uncolored"], "Shapesanity quad painting",
                            lambda state: can_make_stitched_shape(state, player) or can_use_quad_painter(state, player))
    regions["Main"].connect(regions["Shapesanity Colorful East Windmill Uncolored"], "Shapesanity why windmill why",
                            lambda state: can_make_stitched_shape(state, player) or
                                          (can_use_quad_painter(state, player) and
                                           can_make_east_windmill(state, player)))
    regions["Main"].connect(regions["Shapesanity Colorful Half-Half Uncolored"], "Shapesanity quad painting half-half",
                            lambda state: can_make_stitched_shape(state, player) or
                                          (can_use_quad_painter(state, player) and
                                           can_make_half_half_shape(state, player)))
    regions["Main"].connect(regions["Shapesanity Colorful Half Uncolored"], "Shapesanity quad painting half",
                            lambda state: can_make_stitched_shape(state, player) or
                                          (can_use_quad_painter(state, player) and
                                           can_make_half_shape(state, player)))

    # Progressively connect colored shapesanity regions
    for processing in shapesanity_processing:
        regions[f"Shapesanity {processing} Uncolored"].connect(regions[f"Shapesanity {processing} Painted"],
                                                               f"Shapesanity {processing} painting",
                                                               lambda state: has_painter(state, player))
        regions[f"Shapesanity {processing} Painted"].connect(regions[f"Shapesanity {processing} Mixed"],
                                                             f"Shapesanity {processing} mixing",
                                                             lambda state: has_mixer(state, player))

    return [region for region in regions.values() if len(region.locations) or region.name == "Menu"]
