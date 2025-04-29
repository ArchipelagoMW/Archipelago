from typing import Dict, Tuple, List

from BaseClasses import Region, MultiWorld, LocationProgressType, ItemClassification, CollectionState
from .items import ShapezItem
from .locations import ShapezLocation
from .data.strings import ITEMS, REGIONS, GOALS, LOCATIONS, OPTIONS
from worlds.generic.Rules import add_rule

shapesanity_processing = [REGIONS.full, REGIONS.half, REGIONS.piece, REGIONS.stitched, REGIONS.east_wind,
                          REGIONS.half_half, REGIONS.col_east_wind, REGIONS.col_half_half, REGIONS.col_full,
                          REGIONS.col_half]
shapesanity_coloring = [REGIONS.uncol, REGIONS.painted, REGIONS.mixed]

all_regions = [
    REGIONS.menu, REGIONS.belt, REGIONS.extract, REGIONS.main,
    REGIONS.levels_1, REGIONS.levels_2, REGIONS.levels_3, REGIONS.levels_4, REGIONS.levels_5,
    REGIONS.upgrades_1, REGIONS.upgrades_2, REGIONS.upgrades_3, REGIONS.upgrades_4, REGIONS.upgrades_5,
    REGIONS.paint_not_quad, REGIONS.cut_not_quad, REGIONS.rotate_cw, REGIONS.stack_shape, REGIONS.store_shape,
    REGIONS.trash_shape, REGIONS.blueprint, REGIONS.wiring, REGIONS.mam, REGIONS.any_building,
    REGIONS.all_buildings, REGIONS.all_buildings_x1_6_belt,
    *[REGIONS.sanity(processing, coloring)
      for processing in shapesanity_processing
      for coloring in shapesanity_coloring],
]


def can_cut_half(state: CollectionState, player: int) -> bool:
    return state.has(ITEMS.cutter, player)


def can_rotate_90(state: CollectionState, player: int) -> bool:
    return state.has_any((ITEMS.rotator, ITEMS.rotator_ccw), player)


def can_rotate_180(state: CollectionState, player: int) -> bool:
    return state.has_any((ITEMS.rotator, ITEMS.rotator_ccw, ITEMS.rotator_180), player)


def can_stack(state: CollectionState, player: int) -> bool:
    return state.has(ITEMS.stacker, player)


def can_paint(state: CollectionState, player: int) -> bool:
    return state.has_any((ITEMS.painter, ITEMS.painter_double), player) or can_use_quad_painter(state, player)


def can_mix_colors(state: CollectionState, player: int) -> bool:
    return state.has(ITEMS.color_mixer, player)


def has_tunnel(state: CollectionState, player: int) -> bool:
    return state.has_any((ITEMS.tunnel, ITEMS.tunnel_tier_ii), player)


def has_balancer(state: CollectionState, player: int) -> bool:
    return state.has(ITEMS.balancer, player) or state.has_all((ITEMS.comp_merger, ITEMS.comp_splitter), player)


def can_use_quad_painter(state: CollectionState, player: int) -> bool:
    return (state.has_all((ITEMS.painter_quad, ITEMS.wires), player) and
            state.has_any((ITEMS.switch, ITEMS.const_signal), player))


def can_make_stitched_shape(state: CollectionState, player: int, floating: bool) -> bool:
    return (can_stack(state, player) and
            ((state.has(ITEMS.cutter_quad, player) and not floating) or
             (can_cut_half(state, player) and can_rotate_90(state, player))))


def can_build_mam(state: CollectionState, player: int, floating: bool) -> bool:
    return (can_make_stitched_shape(state, player, floating) and can_paint(state, player) and
            can_mix_colors(state, player) and has_balancer(state, player) and has_tunnel(state, player) and
            state.has_all((ITEMS.belt_reader, ITEMS.storage, ITEMS.item_filter,
                           ITEMS.wires, ITEMS.logic_gates, ITEMS.virtual_proc), player))


def can_make_east_windmill(state: CollectionState, player: int) -> bool:
    # Only used for shapesanity => single layers
    return (can_stack(state, player) and
            (state.has(ITEMS.cutter_quad, player) or (can_cut_half(state, player) and can_rotate_180(state, player))))


def can_make_half_half_shape(state: CollectionState, player: int) -> bool:
    # Only used for shapesanity => single layers
    return can_stack(state, player) and state.has_any((ITEMS.cutter, ITEMS.cutter_quad), player)


def can_make_half_shape(state: CollectionState, player: int) -> bool:
    # Only used for shapesanity => single layers
    return can_cut_half(state, player) or state.has_all((ITEMS.cutter_quad, ITEMS.stacker), player)


def has_x_belt_multiplier(state: CollectionState, player: int, needed: float) -> bool:
    # Assumes there are no upgrade traps
    multiplier = 1.0
    # Rising upgrades do the least improvement if received before other upgrades
    for _ in range(state.count(ITEMS.upgrade_rising_belt, player)):
        multiplier *= 2
    multiplier += state.count(ITEMS.upgrade_gigantic_belt, player)*10
    multiplier += state.count(ITEMS.upgrade_big_belt, player)
    multiplier += state.count(ITEMS.upgrade_small_belt, player)*0.1
    return multiplier >= needed


def has_logic_list_building(state: CollectionState, player: int, buildings: List[str], index: int,
                            includeuseful: bool) -> bool:

    # Includes balancer, tunnel, and trash in logic in order to make them appear in earlier spheres
    if includeuseful and not (state.has(ITEMS.trash, player) and has_balancer(state, player) and
                              has_tunnel(state, player)):
        return False

    if buildings[index] == ITEMS.cutter:
        if buildings.index(ITEMS.stacker) < index:
            return state.has_any((ITEMS.cutter, ITEMS.cutter_quad), player)
        else:
            return can_cut_half(state, player)
    elif buildings[index] == ITEMS.rotator:
        return can_rotate_90(state, player)
    elif buildings[index] == ITEMS.stacker:
        return can_stack(state, player)
    elif buildings[index] == ITEMS.painter:
        return can_paint(state, player)
    elif buildings[index] == ITEMS.color_mixer:
        return can_mix_colors(state, player)


def create_shapez_regions(player: int, multiworld: MultiWorld, floating: bool,
                          included_locations: Dict[str, Tuple[str, LocationProgressType]],
                          location_name_to_id: Dict[str, int], level_logic_buildings: List[str],
                          upgrade_logic_buildings: List[str], early_useful: str, goal: str) -> List[Region]:
    """Creates and returns a list of all regions with entrances and all locations placed correctly."""
    regions: Dict[str, Region] = {name: Region(name, player, multiworld) for name in all_regions}

    # Creates ShapezLocations for every included location and puts them into the correct region
    for name, data in included_locations.items():
        regions[data[0]].locations.append(ShapezLocation(player, name, location_name_to_id[name],
                                                         regions[data[0]], data[1]))

    # Create goal event
    if goal in [GOALS.vanilla, GOALS.mam]:
        goal_region = regions[REGIONS.levels_5]
    elif goal == GOALS.even_fasterer:
        goal_region = regions[REGIONS.upgrades_5]
    else:
        goal_region = regions[REGIONS.all_buildings]
    goal_location = ShapezLocation(player, LOCATIONS.goal, None, goal_region, LocationProgressType.DEFAULT)
    goal_location.place_locked_item(ShapezItem(ITEMS.goal, ItemClassification.progression_skip_balancing, None, player))
    if goal == GOALS.efficiency_iii:
        add_rule(goal_location, lambda state: has_x_belt_multiplier(state, player, 8))
    goal_region.locations.append(goal_location)
    multiworld.completion_condition[player] = lambda state: state.has(ITEMS.goal, player)

    # Connect Menu to rest of regions
    regions[REGIONS.menu].connect(regions[REGIONS.belt], "Placing belts", lambda state: state.has(ITEMS.belt, player))
    regions[REGIONS.menu].connect(regions[REGIONS.extract], "Extracting shapes from patches",
                                  lambda state: state.has_any((ITEMS.extractor, ITEMS.extractor_chain), player))
    regions[REGIONS.extract].connect(
        regions[REGIONS.main], "Transporting shapes over the canvas",
        lambda state: state.has_any((ITEMS.belt, ITEMS.comp_merger, ITEMS.comp_splitter), player)
    )

    # Connect achievement regions
    regions[REGIONS.main].connect(regions[REGIONS.paint_not_quad], "Painting with (double) painter",
                                  lambda state: state.has_any((ITEMS.painter, ITEMS.painter_double), player))
    regions[REGIONS.extract].connect(regions[REGIONS.cut_not_quad], "Cutting with half cutter",
                                     lambda state: can_cut_half(state, player))
    regions[REGIONS.extract].connect(regions[REGIONS.rotate_cw], "Rotating clockwise",
                                     lambda state: state.has(ITEMS.rotator, player))
    regions[REGIONS.extract].connect(regions[REGIONS.stack_shape], "Stacking shapes",
                                     lambda state: can_stack(state, player))
    regions[REGIONS.extract].connect(regions[REGIONS.store_shape], "Storing shapes",
                                     lambda state: state.has(ITEMS.storage, player))
    regions[REGIONS.extract].connect(regions[REGIONS.trash_shape], "Trashing shapes",
                                     lambda state: state.has(ITEMS.trash, player))
    regions[REGIONS.main].connect(regions[REGIONS.blueprint], "Copying and placing blueprints",
                                  lambda state: state.has(ITEMS.blueprints, player) and
                                                can_make_stitched_shape(state, player, floating) and
                                                can_paint(state, player) and can_mix_colors(state, player))
    regions[REGIONS.menu].connect(regions[REGIONS.wiring], "Using the wires layer",
                                  lambda state: state.has(ITEMS.wires, player))
    regions[REGIONS.main].connect(regions[REGIONS.mam], "Building a MAM",
                                  lambda state: can_build_mam(state, player, floating))
    regions[REGIONS.menu].connect(regions[REGIONS.any_building], "Placing any building", lambda state: state.has_any((
        ITEMS.belt, ITEMS.balancer, ITEMS.comp_merger, ITEMS.comp_splitter, ITEMS.tunnel, ITEMS.tunnel_tier_ii,
        ITEMS.extractor, ITEMS.extractor_chain, ITEMS.cutter, ITEMS.cutter_quad, ITEMS.rotator, ITEMS.rotator_ccw,
        ITEMS.rotator_180, ITEMS.stacker, ITEMS.painter, ITEMS.painter_double, ITEMS.painter_quad, ITEMS.color_mixer,
        ITEMS.trash, ITEMS.belt_reader, ITEMS.storage, ITEMS.switch, ITEMS.item_filter, ITEMS.display, ITEMS.wires
    ), player))
    regions[REGIONS.main].connect(regions[REGIONS.all_buildings], "Using all main buildings",
                                  lambda state: can_make_stitched_shape(state, player, floating) and
                                                can_paint(state, player) and can_mix_colors(state, player))
    regions[REGIONS.all_buildings].connect(regions[REGIONS.all_buildings_x1_6_belt],
                                           "Delivering per second with 1.6x belt speed",
                                           lambda state: has_x_belt_multiplier(state, player, 1.6))

    # Progressively connect level and upgrade regions
    regions[REGIONS.main].connect(
        regions[REGIONS.levels_1], "Using first level building",
        lambda state: has_logic_list_building(state, player, level_logic_buildings, 0, False))
    regions[REGIONS.levels_1].connect(
        regions[REGIONS.levels_2], "Using second level building",
        lambda state: has_logic_list_building(state, player, level_logic_buildings, 1, False))
    regions[REGIONS.levels_2].connect(
        regions[REGIONS.levels_3], "Using third level building",
        lambda state: has_logic_list_building(state, player, level_logic_buildings, 2,
                                              early_useful == OPTIONS.buildings_3))
    regions[REGIONS.levels_3].connect(
        regions[REGIONS.levels_4], "Using fourth level building",
        lambda state: has_logic_list_building(state, player, level_logic_buildings, 3, False))
    regions[REGIONS.levels_4].connect(
        regions[REGIONS.levels_5], "Using fifth level building",
        lambda state: has_logic_list_building(state, player, level_logic_buildings, 4,
                                              early_useful == OPTIONS.buildings_5))
    regions[REGIONS.main].connect(
        regions[REGIONS.upgrades_1], "Using first upgrade building",
        lambda state: has_logic_list_building(state, player, upgrade_logic_buildings, 0, False))
    regions[REGIONS.upgrades_1].connect(
        regions[REGIONS.upgrades_2], "Using second upgrade building",
        lambda state: has_logic_list_building(state, player, upgrade_logic_buildings, 1, False))
    regions[REGIONS.upgrades_2].connect(
        regions[REGIONS.upgrades_3], "Using third upgrade building",
        lambda state: has_logic_list_building(state, player, upgrade_logic_buildings, 2,
                                              early_useful == OPTIONS.buildings_3))
    regions[REGIONS.upgrades_3].connect(
        regions[REGIONS.upgrades_4], "Using fourth upgrade building",
        lambda state: has_logic_list_building(state, player, upgrade_logic_buildings, 3, False))
    regions[REGIONS.upgrades_4].connect(
        regions[REGIONS.upgrades_5], "Using fifth upgrade building",
        lambda state: has_logic_list_building(state, player, upgrade_logic_buildings, 4,
                                              early_useful == OPTIONS.buildings_5))

    # Connect Uncolored shapesanity regions to Main
    regions[REGIONS.main].connect(
        regions[REGIONS.sanity(REGIONS.full, REGIONS.uncol)], "Delivering unprocessed", lambda state: True)
    regions[REGIONS.main].connect(
        regions[REGIONS.sanity(REGIONS.half, REGIONS.uncol)], "Cutting in single half",
        lambda state: can_make_half_shape(state, player))
    regions[REGIONS.main].connect(
        regions[REGIONS.sanity(REGIONS.piece, REGIONS.uncol)], "Cutting in single piece",
        lambda state: (can_cut_half(state, player) and can_rotate_90(state, player)) or
                      state.has(ITEMS.cutter_quad, player))
    regions[REGIONS.main].connect(
        regions[REGIONS.sanity(REGIONS.half_half, REGIONS.uncol)], "Cutting and stacking into two halves",
        lambda state: can_make_half_half_shape(state, player))
    regions[REGIONS.main].connect(
        regions[REGIONS.sanity(REGIONS.stitched, REGIONS.uncol)], "Stitching complex shapes",
        lambda state: can_make_stitched_shape(state, player, floating))
    regions[REGIONS.main].connect(
        regions[REGIONS.sanity(REGIONS.east_wind, REGIONS.uncol)], "Rotating and stitching a single windmill half",
        lambda state: can_make_east_windmill(state, player))
    regions[REGIONS.main].connect(
        regions[REGIONS.sanity(REGIONS.col_full, REGIONS.uncol)], "Painting with a quad painter or stitching",
        lambda state: can_make_stitched_shape(state, player, floating) or can_use_quad_painter(state, player))
    regions[REGIONS.main].connect(
        regions[REGIONS.sanity(REGIONS.col_east_wind, REGIONS.uncol)], "Why windmill, why?",
        lambda state: can_make_stitched_shape(state, player, floating) or
                      (can_use_quad_painter(state, player) and can_make_east_windmill(state, player)))
    regions[REGIONS.main].connect(
        regions[REGIONS.sanity(REGIONS.col_half_half, REGIONS.uncol)], "Quad painting a half-half shape",
        lambda state: can_make_stitched_shape(state, player, floating) or
                      (can_use_quad_painter(state, player) and can_make_half_half_shape(state, player)))
    regions[REGIONS.main].connect(
        regions[REGIONS.sanity(REGIONS.col_half, REGIONS.uncol)], "Quad painting a half shape",
        lambda state: can_make_stitched_shape(state, player, floating) or
                      (can_use_quad_painter(state, player) and can_make_half_shape(state, player)))

    # Progressively connect colored shapesanity regions
    for processing in shapesanity_processing:
        regions[REGIONS.sanity(processing, REGIONS.uncol)].connect(
            regions[REGIONS.sanity(processing, REGIONS.painted)], f"Painting a {processing.lower()} shape",
            lambda state: can_paint(state, player))
        regions[REGIONS.sanity(processing, REGIONS.painted)].connect(
            regions[REGIONS.sanity(processing, REGIONS.mixed)], f"Mixing colors for a {processing.lower()} shape",
            lambda state: can_mix_colors(state, player))

    return [region for region in regions.values() if len(region.locations) or len(region.exits)]
