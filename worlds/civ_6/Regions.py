from typing import TYPE_CHECKING, Dict, List, Optional, Set, Union
from BaseClasses import CollectionState, LocationProgressType, Region
from worlds.generic.Rules import add_rule, set_rule
from .Data import (
    get_boosts_data,
)
from .Enum import EraType
from .Locations import GOODY_HUT_LOCATION_NAMES, CivVILocation

if TYPE_CHECKING:
    from . import CivVIWorld


def has_progressive_eras(
    state: CollectionState, era: EraType, world: "CivVIWorld"
) -> bool:
    return state.has(
        "Progressive Era", world.player, world.era_required_progressive_era_counts[era]
    )


def has_non_progressive_items(
    state: CollectionState, era: EraType, world: "CivVIWorld"
) -> bool:
    return state.has_all(world.era_required_non_progressive_items[era], world.player)


def has_progressive_items(
    state: CollectionState, era: EraType, world: "CivVIWorld"
) -> bool:
    return state.has_all_counts(
        world.era_required_progressive_items_counts[era], world.player
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
    previous_era: EraType = EraType.ERA_ANCIENT
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

        # Connect era to previous era if not ancient era
        if era == EraType.ERA_ANCIENT:
            menu.connect(world.get_region(EraType.ERA_ANCIENT.value))
            continue

        connection = world.get_region(previous_era.value).connect(
            world.get_region(era.value)
        )

        #  Access rules for eras
        add_rule(
            connection,
            lambda state, previous_era=previous_era, world=world: has_non_progressive_items(
                state, previous_era, world
            ),
        )
        if world.options.progression_style == "eras_and_districts":
            add_rule(
                connection,
                lambda state, previous_era=previous_era, world=world: has_progressive_eras(
                    state, previous_era, world
                ),
            )
        if world.options.progression_style != "none":
            add_rule(
                connection,
                lambda state, previous_era=previous_era, world=world: has_progressive_items(
                    state, previous_era, world
                ),
            )
        previous_era = era

    future_era = world.get_region(EraType.ERA_FUTURE.value)
    victory = CivVILocation(world.player, "Complete a victory type", None, future_era)
    victory.place_locked_item(world.create_event("Victory"))
    future_era.locations.append(victory)

    set_rule(
        victory,
        lambda state: state.can_reach_region(EraType.ERA_FUTURE.value, world.player),
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
