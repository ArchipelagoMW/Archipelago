import logging
from collections import defaultdict
from typing import TYPE_CHECKING, List

from BaseClasses import CollectionState

from .Data import Items, Locations, Events
from .Data.Locations import LocationData
from .Data.Regions import RegionEnum

if TYPE_CHECKING:
    from . import AnodyneWorld

debug_mode: bool = False


def location_ids():
    id_counter = defaultdict(int)

    def l_id(location: LocationData):
        nonlocal id_counter
        lookup = (location.region.__class__, location.type)
        val = id_counter[lookup]
        id_counter[lookup] += 1
        # 10**9 addition to avoid being able to generate id 0
        return 10 ** 9 + location.region.area_id() * 10 ** 6 + location.type.value * 1000 + val

    return {location.name: l_id(location) for location in Locations.all_locations}


item_name_to_id = {name: item.item_id for name, item in Items.all_items.items()}
location_name_to_id = location_ids()


def get_small_key_count():
    ret: defaultdict[type[RegionEnum], int] = defaultdict(int)
    for location in Locations.all_locations:
        if location.small_key:
            ret[location.region.__class__] += 1
    return ret


small_key_count = get_small_key_count()

groups = {
    **Items.item_groups,
    "Bosses": [f"Defeat {c}" for c in ["Seer", "The Wall", "Rogue", "Watcher", "Servants", "Manager", "Sage", "Briar"]],
    "Combat": Items.item_groups["Brooms"]
}


def check_access(state: CollectionState, world: "AnodyneWorld", rule: str, map_name: str) -> bool:
    if len(world.proxy_rules) == 0:
        return True  # Shut up warnings when running all_state before our set_rules has run
    if rule in world.proxy_rules:
        return all(check_access(state, world, subrule, map_name) for subrule in world.proxy_rules[rule])
    elif rule in groups:
        return state.has_any(groups[rule], world.player)
    elif ':' in rule:
        item, count = rule.split(':')
        count = int(count)
        if item in groups:
            return state.has_from_list(groups[item], world.player, count)

        if item not in Items.all_items and item not in Events.all_event_names:
            logging.warning(f"Rule {rule} does not exist")
        return state.has(item, world.player, count)
    else:
        logging.debug(f"Item {rule} check in {map_name} ({world.player})")
        if rule not in Items.all_items and rule not in Events.all_event_names:
            logging.warning(f"Rule {rule} does not exist")
        return state.has(item=rule, player=world.player)


class AccessRule:
    def __init__(self, reqs: List[str], region_name: str, world: "AnodyneWorld"):
        self.reqs = reqs
        self.region_name = region_name
        self.world = world

    def __call__(self, state: CollectionState):
        return all(check_access(state, self.world, item, self.region_name) for item in self.reqs)


def get_access_rule(reqs: List[str], region_name: str, world: "AnodyneWorld"):
    return AccessRule(reqs, region_name, world)
