import typing

from BaseClasses import CollectionState
from .Items import get_item_by_civ_name
from .Data import get_boosts_data
from .Enum import CivVICheckType
from .ProgressiveDistricts import convert_items_to_have_progression

from worlds.generic.Rules import forbid_item, set_rule


if typing.TYPE_CHECKING:
    from . import CivVIWorld


def generate_has_required_items_lambda(prereqs: typing.List[str], required_count: int, has_progressive_items: bool, player: int):
    def has_required_items_lambda(state: CollectionState):
        return has_required_items(state, prereqs, required_count, has_progressive_items, player)
    return has_required_items_lambda


def create_boost_rules(world: 'CivVIWorld'):
    boost_data_list = get_boosts_data()
    boost_locations = [location for location in world.location_table.values() if location.location_type == CivVICheckType.BOOST]
    for location in boost_locations:
        boost_data = next((boost for boost in boost_data_list if boost.Type == location.name), None)
        world_location = world.multiworld.get_location(location.name, world.player)
        forbid_item(world_location, "Progressive Era", world.player)
        if not boost_data or boost_data.PrereqRequiredCount == 0:
            continue

        has_progressive_items = world.options.progression_style.current_key != "none"
        set_rule(world_location,
                 generate_has_required_items_lambda(boost_data.Prereq, boost_data.PrereqRequiredCount, has_progressive_items, world.player)
                 )


def has_required_items(state: CollectionState, prereqs: typing.List[str], required_count: int, has_progressive_items: bool, player: int):
    if has_progressive_items:
        items = [get_item_by_civ_name(item, state.multiworld.worlds[player].item_table).name for item in convert_items_to_have_progression(prereqs)]
        progressive_items: typing.Dict[str, int] = {}
        count = 0
        for item in items:
            if "Progressive" in item:
                if not progressive_items.get(item):
                    progressive_items[item] = 0
                progressive_items[item] += 1
            else:
                if state.has(item, player):
                    count += 1

        for item, required_progressive_item_count in progressive_items.items():
            if state.count(item, player) >= required_progressive_item_count:
                count += required_progressive_item_count
        if count > 0:
            pass
        return count >= required_count
    else:
        count = 0
        for prereq in prereqs:
            if state.has(get_item_by_civ_name(prereq, state.multiworld.worlds[player].item_table).name, player):
                count += 1
        return count >= required_count
