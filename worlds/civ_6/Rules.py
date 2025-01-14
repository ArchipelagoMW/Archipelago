from typing import TYPE_CHECKING, List, Tuple
from BaseClasses import CollectionState
from .ItemData import CivVIBoostData
from .Items import format_item_name
from .Data import get_boosts_data, get_progressive_districts_data
from .Enum import CivVICheckType
from .ProgressiveDistricts import convert_item_to_progressive_item

from worlds.generic.Rules import forbid_item, set_rule


if TYPE_CHECKING:
    from . import CivVIWorld


def generate_requirements_for_boosts(
    world: "CivVIWorld", boost_data: CivVIBoostData
) -> Tuple[List[str], List[Tuple[str, int]]]:
    required_non_progressive_items: List[str] = []
    required_progressive_item_counts: List[Tuple[str, int]] = []

    for item in boost_data.Prereq:
        progressive_item_name = convert_item_to_progressive_item(item)
        if (
            world.options.progression_style != "none"
            and "PROGRESSIVE" in progressive_item_name
        ):
            required_progressive_item_counts.append(
                (
                    format_item_name(progressive_item_name),
                    get_progressive_districts_data()[progressive_item_name].index(item)
                    + 1,
                )
            )
        else:
            ap_item_name = world.item_by_civ_name[item]
            required_non_progressive_items.append(ap_item_name)
    return required_non_progressive_items, required_progressive_item_counts


def create_boost_rules(world: "CivVIWorld"):
    boost_data_list = get_boosts_data()
    boost_locations = [
        location
        for location in world.location_table.values()
        if location.location_type == CivVICheckType.BOOST
    ]
    for location in boost_locations:
        boost_data = next(
            (boost for boost in boost_data_list if boost.Type == location.name), None
        )
        world_location = world.get_location(location.name)
        forbid_item(world_location, "Progressive Era", world.player)

        if boost_data and boost_data.PrereqRequiredCount > 0:
            required_non_progressive_items, required_progressive_item_counts = (
                generate_requirements_for_boosts(world, boost_data)
            )
            if world.options.progression_style != "none":
                set_rule(
                    world_location,
                    lambda state, non_progressive_prereqs=required_non_progressive_items, progressive_prereq_counts=required_progressive_item_counts, required_count=boost_data.PrereqRequiredCount: has_required_items_progressive(
                        state,
                        non_progressive_prereqs,
                        progressive_prereq_counts,
                        required_count,
                        world,
                    ),
                )
            else:
                set_rule(
                    world_location,
                    lambda state, prereqs=required_non_progressive_items, required_count=boost_data.PrereqRequiredCount: has_required_items_non_progressive(
                        state, prereqs, required_count, world
                    ),
                )


def has_required_items_progressive(
    state: CollectionState,
    non_progressive_prereqs: List[str],
    progressive_prereq_counts: List[Tuple[str, int]],
    required_count: int,
    world: "CivVIWorld",
) -> bool:
    collected_count = 0
    for item, count in progressive_prereq_counts:
        if state.has(item, world.player, count):
            collected_count += 1
        # early out if we've already gotten enough
        if collected_count >= required_count:
            return True
    for item in non_progressive_prereqs:
        if state.has(item, world.player):
            collected_count += 1
        # early out if we've already gotten enough
        if collected_count >= required_count:
            return True
    return False


def has_required_items_non_progressive(
    state: CollectionState, prereqs: List[str], required_count: int, world: "CivVIWorld"
) -> bool:
    return state.has_from_list_unique(
        prereqs,
        world.player,
        required_count,
    )
