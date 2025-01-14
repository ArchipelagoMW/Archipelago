from typing import TYPE_CHECKING, Dict, List, Optional, Set, Union
from BaseClasses import CollectionState, LocationProgressType, Region
from worlds.generic.Rules import set_rule
from .Data import (
    get_boosts_data,
)
from .Enum import EraType
from .Locations import GOODY_HUT_LOCATION_NAMES, CivVILocation

if TYPE_CHECKING:
    from . import CivVIWorld


def has_required_items(
    state: CollectionState, era: EraType, world: "CivVIWorld"
) -> bool:
    # Progressive Eras
    if world.options.progression_style == "eras_and_districts" and not state.has(
        "Progressive Era", world.player, world.era_required_progressive_era_counts[era]
    ):
        return False

    #  Non Progressive Items (all items for era if no progressive districts)
    if not state.has_all(world.era_required_non_progressive_items[era], world.player):
        return False

    # Progressive Items (if any)
    if world.options.progression_style != "none" and not state.has_all_counts(
        world.era_required_progressive_items_counts[era], world.player
    ):
        return False

    return True


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
