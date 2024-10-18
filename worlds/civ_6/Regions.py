from typing import TYPE_CHECKING, Dict, List, Optional
from BaseClasses import CollectionState, Region
from .Data import get_era_required_items_data, get_progressive_districts_data
from .Items import CivVIItemData, format_item_name, get_item_by_civ_name
from .Enum import EraType
from .Locations import CivVILocation
from .ProgressiveDistricts import get_flat_progressive_districts

if TYPE_CHECKING:
    from . import CivVIWorld


def get_prereqs_for_era(end_era: EraType, exclude_progressive_items: bool, item_table: Dict[str, CivVIItemData]) -> List[CivVIItemData]:
    """Gets the specific techs/civics that are required for the specified era"""
    era_required_items = get_era_required_items_data()[end_era.value].copy()

    # If we are excluding progressive items, we need to remove them from the list of expected items (TECH_BRONZE_WORKING won't be here since it will be PROGRESSIVE_ENCAMPMENT)
    if exclude_progressive_items:
        flat_progressive_items = get_flat_progressive_districts()
        prereqs_without_progressive_items: List[str] = []
        for item in era_required_items:
            if item in flat_progressive_items:
                continue
            prereqs_without_progressive_items.append(item)

        return [get_item_by_civ_name(prereq, item_table) for prereq in prereqs_without_progressive_items]

    return [get_item_by_civ_name(prereq, item_table) for prereq in era_required_items]


def has_required_progressive_districts(state: CollectionState, era: EraType, player: int) -> bool:
    """ If player has progressive items enabled, it will count how many progressive techs it should have, otherwise return the default array"""
    progressive_districts = get_progressive_districts_data()

    item_table = state.multiworld.worlds[player].item_table
    # Verify we can still reach non progressive items
    all_previous_items_no_progressives = get_prereqs_for_era(
        era, True, item_table)
    if not state.has_all([item.name for item in all_previous_items_no_progressives], player):
        return False

    # Verify we have the correct amount of progressive items
    all_previous_items = get_prereqs_for_era(
        era, False, item_table)
    required_counts: Dict[str, int] = {}

    for key, value in progressive_districts.items():
        required_counts[key] = 0
        for item in all_previous_items:
            if item.civ_name in value:
                required_counts[key] += 1

    return state.has_all_counts({format_item_name(key): value for key, value in required_counts.items()}, player)


def has_required_progressive_eras(state: CollectionState, era: EraType, player: int) -> bool:
    """Checks, for the given era, how many are required to proceed to the next era. Ancient = 0, Classical = 1, etc."""
    if era == EraType.ERA_FUTURE or era == EraType.ERA_INFORMATION:
        return True

    eras = [e.value for e in EraType]
    era_index = eras.index(era.value)
    return state.has(format_item_name("PROGRESSIVE_ERA"), player, era_index + 1)


def has_required_items(state: CollectionState, era: EraType, world: 'CivVIWorld') -> bool:
    player = world.player
    has_progressive_districts = world.options.progression_style != "none"
    has_progressive_eras = world.options.progression_style == "eras_and_districts"

    if has_progressive_districts:
        required_items = has_required_progressive_districts(state, era, player)
    else:
        era_required_items = [get_item_by_civ_name(item, world.item_table).name for item in get_era_required_items_data()[era.value]]
        required_items = state.has_all(era_required_items, player)

    if not required_items:
        return False

    return not has_progressive_eras or has_required_progressive_eras(state, era, player)


def create_regions(world: 'CivVIWorld'):
    menu = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu)

    has_progressive_eras = world.options.progression_style == "eras_and_districts"
    has_goody_huts = world.options.shuffle_goody_hut_rewards
    has_boosts = world.options.boostsanity

    regions: List[Region] = []
    for era in EraType:
        era_region = Region(era.value, world.player, world.multiworld)
        era_locations: Dict[str, Optional[int]] = {location.name: location.code for _key,
                                                   location in world.location_by_era[era.value].items()}

        if not has_progressive_eras:
            era_locations = {key: value for key, value in era_locations.items() if key.split("_")[0] != "ERA"}
        if not has_goody_huts:
            era_locations = {key: value for key, value in era_locations.items() if key.split("_")[0] != "GOODY"}
        if not has_boosts:
            era_locations = {key: value for key, value in era_locations.items() if key.split("_")[0] != "BOOST"}

        era_region.add_locations(era_locations, CivVILocation)

        regions.append(era_region)
        world.multiworld.regions.append(era_region)

    menu.connect(world.get_region(EraType.ERA_ANCIENT.value))

    world.get_region(EraType.ERA_ANCIENT.value).connect(
        world.get_region(EraType.ERA_CLASSICAL.value), None,
        lambda state: has_required_items(
            state, EraType.ERA_ANCIENT, world)
    )

    world.get_region(EraType.ERA_CLASSICAL.value).connect(
        world.get_region(EraType.ERA_MEDIEVAL.value), None, lambda state: has_required_items(
            state, EraType.ERA_CLASSICAL, world)
    )

    world.get_region(EraType.ERA_MEDIEVAL.value).connect(
        world.get_region(EraType.ERA_RENAISSANCE.value), None, lambda state: has_required_items(
            state, EraType.ERA_MEDIEVAL, world)
    )

    world.get_region(EraType.ERA_RENAISSANCE.value).connect(
        world.get_region(EraType.ERA_INDUSTRIAL.value), None, lambda state: has_required_items(
            state, EraType.ERA_RENAISSANCE, world)
    )

    world.get_region(EraType.ERA_INDUSTRIAL.value).connect(
        world.get_region(EraType.ERA_MODERN.value), None, lambda state: has_required_items(
            state, EraType.ERA_INDUSTRIAL, world)
    )

    world.get_region(EraType.ERA_MODERN.value).connect(
        world.get_region(EraType.ERA_ATOMIC.value), None, lambda state: has_required_items(
            state, EraType.ERA_MODERN, world)
    )

    world.get_region(EraType.ERA_ATOMIC.value).connect(
        world.get_region(EraType.ERA_INFORMATION.value), None, lambda state: has_required_items(
            state, EraType.ERA_ATOMIC, world)
    )

    world.get_region(EraType.ERA_INFORMATION.value).connect(
        world.get_region(EraType.ERA_FUTURE.value), None, lambda state: has_required_items(
            state, EraType.ERA_INFORMATION, world)
    )

    world.multiworld.completion_condition[world.player] = lambda state: state.can_reach(
        EraType.ERA_FUTURE.value, "Region", world.player)
