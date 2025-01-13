from typing import TYPE_CHECKING, Dict, List, Optional, Set, Union
from BaseClasses import CollectionState, LocationProgressType, Region
from worlds.generic.Rules import set_rule
from .Data import (
    get_boosts_data,
    get_era_required_items_data,
    get_progressive_districts_data,
)
from .Items import CivVIItemData, format_item_name, get_item_by_civ_name
from .Enum import EraType
from .Locations import GOODY_HUT_LOCATION_NAMES, CivVILocation
from .ProgressiveDistricts import get_flat_progressive_districts

if TYPE_CHECKING:
    from . import CivVIWorld


def get_prereqs_for_era(
    end_era: EraType,
    exclude_progressive_items: bool,
    item_table: Dict[str, CivVIItemData],
) -> List[CivVIItemData]:
    """Gets the specific techs/civics that are required for the specified era"""
    era_required_items = get_era_required_items_data()[end_era.value].copy()

    # If we are excluding progressive items, we need to remove them from the list of expected items (TECH_BRONZE_WORKING won't be here since it will be PROGRESSIVE_ENCAMPMENT)
    if not exclude_progressive_items:  # guard clause to save an indent depth
        return [
            get_item_by_civ_name(prereq, item_table) for prereq in era_required_items
        ]

    flat_progressive_items = get_flat_progressive_districts()
    prereqs_without_progressive_items: List[str] = []
    for item in era_required_items:
        if item in flat_progressive_items:
            continue
        prereqs_without_progressive_items.append(item)

    return [
        get_item_by_civ_name(prereq, item_table)
        for prereq in prereqs_without_progressive_items
    ]


def has_required_progressive_districts(
    state: CollectionState, era: EraType, player: int
) -> bool:
    """If player has progressive items enabled, it will count how many progressive techs it should have, otherwise return the default array"""
    progressive_districts = get_progressive_districts_data()

    item_table = state.multiworld.worlds[player].item_table
    # Verify we can still reach non progressive items
    all_previous_items_no_progressives = get_prereqs_for_era(era, True, item_table)
    if not state.has_all(
        [item.name for item in all_previous_items_no_progressives], player
    ):
        return False

    # Verify we have the correct amount of progressive items
    all_previous_items = get_prereqs_for_era(era, False, item_table)
    required_counts: Dict[str, int] = {}

    for key, value in progressive_districts.items():
        required_counts[key] = 0
        for item in all_previous_items:
            if item.civ_name in value:
                required_counts[key] += 1

    return state.has_all_counts(
        {format_item_name(key): value for key, value in required_counts.items()}, player
    )


def has_required_progressive_eras(
    state: CollectionState, era: EraType, player: int
) -> bool:
    """Checks, for the given era, how many are required to proceed to the next era. Ancient = 0, Classical = 1, etc."""
    if era == EraType.ERA_FUTURE or era == EraType.ERA_INFORMATION:
        return True

    eras = [e.value for e in EraType]
    era_index = eras.index(era.value)
    return state.has(format_item_name("PROGRESSIVE_ERA"), player, era_index + 1)


def has_required_items(
    state: CollectionState, era: EraType, world: "CivVIWorld"
) -> bool:
    player = world.player
    has_progressive_districts = world.options.progression_style != "none"
    has_progressive_eras = world.options.progression_style == "eras_and_districts"

    if has_progressive_districts:
        required_items = has_required_progressive_districts(state, era, player)
    else:
        era_required_items = [
            get_item_by_civ_name(item, world.item_table).name
            for item in get_era_required_items_data()[era.value]
        ]
        required_items = state.has_all(era_required_items, player)

    return required_items and (
        not has_progressive_eras or has_required_progressive_eras(state, era, player)
    )


def create_regions(world: "CivVIWorld"):
    menu = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu)

    optional_location_inclusions: Dict[str, Union[bool, int]] = {
        "ERA": world.options.progression_style
        == world.options.progression_style.option_eras_and_districts,
        "GOODY": world.options.shuffle_goody_hut_rewards.value,
        "BOOST": world.options.boostsanity.value,
    }

    regions: List[Region] = []
    for era in EraType:
        era_region = Region(era.value, world.player, world.multiworld)
        era_locations: Dict[str, Optional[int]] = {}

        for key, location in world.location_by_era[era.value].items():
            category = key.split("_")[0]
            if optional_location_inclusions.get(category, True):
                era_locations[location.name] = location.code

        era_region.add_locations(era_locations, CivVILocation)

        regions.append(era_region)
        world.multiworld.regions.append(era_region)

    menu.connect(world.get_region(EraType.ERA_ANCIENT.value))

    world.get_region(EraType.ERA_ANCIENT.value).connect(
        world.get_region(EraType.ERA_CLASSICAL.value),
        None,
        lambda state: has_required_items(state, EraType.ERA_ANCIENT, world),
    )

    world.get_region(EraType.ERA_CLASSICAL.value).connect(
        world.get_region(EraType.ERA_MEDIEVAL.value),
        None,
        lambda state: has_required_items(state, EraType.ERA_CLASSICAL, world),
    )

    world.get_region(EraType.ERA_MEDIEVAL.value).connect(
        world.get_region(EraType.ERA_RENAISSANCE.value),
        None,
        lambda state: has_required_items(state, EraType.ERA_MEDIEVAL, world),
    )

    world.get_region(EraType.ERA_RENAISSANCE.value).connect(
        world.get_region(EraType.ERA_INDUSTRIAL.value),
        None,
        lambda state: has_required_items(state, EraType.ERA_RENAISSANCE, world),
    )

    world.get_region(EraType.ERA_INDUSTRIAL.value).connect(
        world.get_region(EraType.ERA_MODERN.value),
        None,
        lambda state: has_required_items(state, EraType.ERA_INDUSTRIAL, world),
    )

    world.get_region(EraType.ERA_MODERN.value).connect(
        world.get_region(EraType.ERA_ATOMIC.value),
        None,
        lambda state: has_required_items(state, EraType.ERA_MODERN, world),
    )

    world.get_region(EraType.ERA_ATOMIC.value).connect(
        world.get_region(EraType.ERA_INFORMATION.value),
        None,
        lambda state: has_required_items(state, EraType.ERA_ATOMIC, world),
    )

    future_era = world.get_region(EraType.ERA_INFORMATION.value)
    future_era.connect(
        world.get_region(EraType.ERA_FUTURE.value),
        None,
        lambda state: has_required_items(state, EraType.ERA_INFORMATION, world),
    )

    victory = CivVILocation(world.player, "Complete a victory type", None, future_era)
    victory.place_locked_item(world.create_event("Victory"))
    future_era.locations.append(victory)

    set_rule(
        victory,
        lambda state: state.can_reach(EraType.ERA_FUTURE.value, "Region", world.player),
    )

    world.multiworld.completion_condition[world.player] = lambda state: state.has(
        "Victory", world.player
    )
    exclude_necessary_locations(world)


def exclude_necessary_locations(world: "CivVIWorld"):
    forced_excluded_location_names: Set[str] = set()

    if world.options.shuffle_goody_hut_rewards:
        forced_excluded_location_names.update(GOODY_HUT_LOCATION_NAMES)

    if world.options.boostsanity:
        boost_data_list = get_boosts_data()
        excluded_boosts = {
            boost_data.Type
            for boost_data in boost_data_list
            if boost_data.Classification == "EXCLUDED"
        }
        forced_excluded_location_names.update(excluded_boosts)

    for location_name in forced_excluded_location_names:
        location = world.get_location(location_name)
        location.progress_type = LocationProgressType.EXCLUDED
