import typing
from BaseClasses import CollectionState, LocationProgressType, Region
from .Data import get_era_required_items_data, get_progressive_districts_data
from .Items import format_item_name, get_item_by_civ_name
from .Enum import CivVICheckType, EraType
from .Locations import CivVILocation
from .ProgressiveDistricts import get_flat_progressive_districts
from .Options import CivVIOptions

if typing.TYPE_CHECKING:
    from . import CivVIWorld
    from Items import CivVIItemData


def get_required_items_for_era(era: EraType):
    """Gets the specific techs/civics that are required for the specified era"""
    era_required_items = {}
    era_required_items = get_era_required_items_data()
    return era_required_items[era.value]


def get_cumulative_prereqs_for_era(end_era: EraType, exclude_progressive_items: bool = True, item_table: typing.Dict[str, 'CivVIItemData'] = None) -> typing.List['CivVIItemData']:
    """Gets the specific techs/civics that are required for the specified era as well as all previous eras"""
    cumulative_prereqs = []
    era_required_items = {}
    era_required_items = get_era_required_items_data()

    for era in EraType:
        cumulative_prereqs += era_required_items[era.value]
        if era == end_era:
            break
    # If we are excluding progressive items, we need to remove them from the list of expected items (TECH_BRONZE_WORKING won't be here since it will be PROGRESSIVE_ENCAMPMENT)
    if exclude_progressive_items:
        flat_progressive_items = get_flat_progressive_districts()
        prereqs_without_progressive_items = []
        for item in cumulative_prereqs:
            if item in flat_progressive_items:
                continue
            else:
                prereqs_without_progressive_items.append(item)

        return [get_item_by_civ_name(prereq, item_table) for prereq in prereqs_without_progressive_items]

    return [get_item_by_civ_name(prereq, item_table) for prereq in cumulative_prereqs]


def has_required_progressive_districts(state: CollectionState, era: EraType, player: int):
    """ If player has progressive items enabled, it will count how many progressive techs it should have, otherwise return the default array"""
    progressive_districts = get_progressive_districts_data()

    item_table = state.multiworld.worlds[player].item_table
    # Verify we can still reach non progressive items
    all_previous_items_no_progression = get_cumulative_prereqs_for_era(
        era, True, item_table)
    if not state.has_all([item.name for item in all_previous_items_no_progression], player):
        return False

    # Verify we have the correct amount of progressive items
    all_previous_items = get_cumulative_prereqs_for_era(
        era, False, item_table)
    required_counts: typing.Dict[str, int] = {}

    for key, value in progressive_districts.items():
        required_counts[key] = 0
        for item in all_previous_items:
            if item.civ_name in value:
                required_counts[key] += 1

    for key, value in required_counts.items():
        has_amount = state.has(format_item_name(key), player, required_counts[key])
        if not has_amount:
            return False
    return True


def has_required_progressive_eras(state: CollectionState, era: EraType, player: int):
    """Checks, for the given era, how many are required to proceed to the next era. Ancient = 1, Classical = 2, etc. Assumes 2 required for classical and starts from there so as to decrease odds of hard locking without the turns to get the items"""
    if era == EraType.ERA_FUTURE or era == EraType.ERA_INFORMATION:
        return True

    eras = [e.value for e in EraType]
    era_index = eras.index(era.value)
    return state.has(format_item_name("PROGRESSIVE_ERA"), player, era_index + 2)


def has_required_items(state: CollectionState, era: EraType, player: int, has_progressive_districts: bool, has_progressive_eras: bool):
    required_items = False
    required_eras = False
    if has_progressive_districts:
        required_items = has_required_progressive_districts(state, era, player)
    else:
        era_required_items = [get_item_by_civ_name(item, state.multiworld.worlds[player].item_table).name for item in get_era_required_items_data()[era.value]]
        required_items = state.has_all(era_required_items, player)

    if has_progressive_eras:
        required_eras = has_required_progressive_eras(state, era, player)
    else:
        required_eras = True

    return required_items and required_eras


def create_regions(world: 'CivVIWorld', options: CivVIOptions, player: int):
    menu = Region("Menu", player, world.multiworld)
    world.multiworld.regions.append(menu)

    has_progressive_items = options.progression_style.current_key != "none"
    has_progressive_eras = options.progression_style.current_key == "eras_and_districts"
    has_goody_huts = options.shuffle_goody_hut_rewards.value
    has_boosts = options.boostsanity.value

    regions: typing.List[Region] = []
    for era in EraType:
        era_region = Region(era.value, player, world.multiworld)
        era_locations = {location.name: location.code for key,
                         location in world.location_by_era[era.value].items()}

        # If progressive_eras is not enabled, then era check types from the era_locations
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
            state, EraType.ERA_ANCIENT, player, has_progressive_items, has_progressive_eras)
    )

    world.get_region(EraType.ERA_CLASSICAL.value).connect(
        world.get_region(EraType.ERA_MEDIEVAL.value), None, lambda state:  has_required_items(
            state, EraType.ERA_CLASSICAL, player, has_progressive_items, has_progressive_eras)
    )

    world.get_region(EraType.ERA_MEDIEVAL.value).connect(
        world.get_region(EraType.ERA_RENAISSANCE.value), None, lambda state:  has_required_items(
            state, EraType.ERA_MEDIEVAL, player, has_progressive_items, has_progressive_eras)
    )

    world.get_region(EraType.ERA_RENAISSANCE.value).connect(
        world.get_region(EraType.ERA_INDUSTRIAL.value), None, lambda state:  has_required_items(
            state, EraType.ERA_RENAISSANCE, player, has_progressive_items, has_progressive_eras)
    )

    world.get_region(EraType.ERA_INDUSTRIAL.value).connect(
        world.get_region(EraType.ERA_MODERN.value), None, lambda state:  has_required_items(
            state, EraType.ERA_INDUSTRIAL, player, has_progressive_items, has_progressive_eras)
    )

    world.get_region(EraType.ERA_MODERN.value).connect(
        world.get_region(EraType.ERA_ATOMIC.value), None, lambda state:  has_required_items(
            state, EraType.ERA_MODERN, player, has_progressive_items, has_progressive_eras)
    )

    world.get_region(EraType.ERA_ATOMIC.value).connect(
        world.get_region(EraType.ERA_INFORMATION.value), None, lambda state:  has_required_items(
            state, EraType.ERA_ATOMIC, player, has_progressive_items, has_progressive_eras)
    )

    world.get_region(EraType.ERA_INFORMATION.value).connect(
        world.get_region(EraType.ERA_FUTURE.value), None, lambda state:  has_required_items(state, EraType.ERA_INFORMATION, player, has_progressive_items, has_progressive_eras))

    world.multiworld.completion_condition[player] = lambda state: state.can_reach(
        EraType.ERA_FUTURE.value, "Region", player)

    if world.options.boostsanity.value and not world.options.exclude_missable_boosts.value:
        _update_boost_locations_to_include_missable(world)


def _update_boost_locations_to_include_missable(world: 'CivVIWorld'):
    """If the player has exclude missable boosts disabled, set them all to default if they are excluded"""
    for loc_data in world.location_table.values():
        if loc_data.location_type == CivVICheckType.BOOST:
            location = world.get_location(loc_data.name)
            if location.progress_type == LocationProgressType.EXCLUDED:
                location.progress_type = LocationProgressType.DEFAULT
