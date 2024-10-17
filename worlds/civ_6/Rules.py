from typing import TYPE_CHECKING, List, Dict
from BaseClasses import CollectionState
from .Items import get_item_by_civ_name
from .Data import get_boosts_data
from .Enum import CivVICheckType
from .ProgressiveDistricts import convert_items_to_have_progression

from worlds.generic.Rules import forbid_item, set_rule


if TYPE_CHECKING:
    from . import CivVIWorld


def create_boost_rules(world: 'CivVIWorld'):
    boost_data_list = get_boosts_data()
    boost_locations = [location for location in world.location_table.values() if location.location_type == CivVICheckType.BOOST]
    for location in boost_locations:
        boost_data = next((boost for boost in boost_data_list if boost.Type == location.name), None)
        world_location = world.get_location(location.name)
        forbid_item(world_location, "Progressive Era", world.player)
        if not boost_data or boost_data.PrereqRequiredCount == 0:
            continue

        set_rule(world_location, lambda state, prereqs=boost_data.Prereq, required_count=boost_data.PrereqRequiredCount: has_required_items(state, prereqs, required_count, world))


def has_required_items(state: CollectionState, prereqs: List[str], required_count: int, world: 'CivVIWorld') -> bool:
    player = world.player
    has_progressive_items = world.options.progression_style != "none"
    if has_progressive_items:
        count = 0
        items = [get_item_by_civ_name(item, world.item_table).name for item in convert_items_to_have_progression(prereqs)]
        progressive_items: Dict[str, int] = {}
        for item in items:
            if "Progressive" in item:
                if not progressive_items.get(item):
                    progressive_items[item] = 0
                progressive_items[item] += 1
            else:
                if state.has(item, player):
                    count += 1
                    # early out if we've already gotten enough
                    if count >= required_count:
                        return True
        for item, required_progressive_item_count in progressive_items.items():
            if state.has(item, player, required_progressive_item_count):
                count += required_progressive_item_count
                # early out if we've already gotten enough
                if count >= required_count:
                    return True
        return False
    else:
        return state.has_from_list_unique(
            [
                get_item_by_civ_name(prereq, world.item_table).name for prereq in prereqs
            ], player, required_count)
