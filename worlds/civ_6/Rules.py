from typing import TYPE_CHECKING, List
from BaseClasses import CollectionState
from .Items import get_item_by_civ_name
from .Data import get_boosts_data, get_progressive_districts_data
from .Enum import CivVICheckType
from .ProgressiveDistricts import convert_item_to_progressive_item

from worlds.generic.Rules import forbid_item, set_rule


if TYPE_CHECKING:
    from . import CivVIWorld


def create_boost_rules(world: "CivVIWorld"):
    boost_data_list = get_boosts_data()
    boost_locations = [
        location
        for location in world.location_table.values()
        if location.location_type == CivVICheckType.BOOST
    ]
    required_items_func = (
        has_required_items_progressive
        if world.options.progression_style != "none"
        else has_required_items_non_progressive
    )
    for location in boost_locations:
        boost_data = next(
            (boost for boost in boost_data_list if boost.Type == location.name), None
        )
        world_location = world.get_location(location.name)
        forbid_item(world_location, "Progressive Era", world.player)
        if boost_data and boost_data.PrereqRequiredCount > 0:
            set_rule(
                world_location,
                lambda state, prereqs=boost_data.Prereq, required_count=boost_data.PrereqRequiredCount: required_items_func(
                    state, prereqs, required_count, world
                ),
            )


def has_required_items_progressive(
    state: CollectionState, prereqs: List[str], required_count: int, world: "CivVIWorld"
) -> bool:
    collected_count = 0
    for item in prereqs:
        progressive_item_name = convert_item_to_progressive_item(item)
        ap_item_name = get_item_by_civ_name(
            progressive_item_name, world.item_table
        ).name
        if "PROGRESSIVE" in progressive_item_name:
            progression_amount = (
                get_progressive_districts_data()[progressive_item_name].index(item) + 1
            )
            if state.has(ap_item_name, world.player, progression_amount):
                collected_count += 1
        elif state.has(ap_item_name, world.player):
            collected_count += 1
        # early out if we've already gotten enough
        if collected_count >= required_count:
            return True
    return False


def has_required_items_non_progressive(
    state: CollectionState, prereqs: List[str], required_count: int, world: "CivVIWorld"
) -> bool:
    return state.has_from_list_unique(
        [get_item_by_civ_name(prereq, world.item_table).name for prereq in prereqs],
        world.player,
        required_count,
    )
