import typing

from typing import List, Set, Tuple, NamedTuple
from BaseClasses import Item, MultiWorld, Location, Tutorial
from ..AutoWorld import World, WebWorld
from .Items import StarcraftWoLItem, item_table, filler_items, item_name_groups, get_full_item_list, \
    basic_unit
from .Locations import get_locations
from .Regions import create_regions
from .Options import sc2wol_options, get_option_value
from .LogicMixin import SC2WoLLogic
from ..AutoWorld import World


class Starcraft2WoLWebWorld(WebWorld):
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Starcraft 2 randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["TheCondor"]
    )

    tutorials = [setup]


class SC2WoLWorld(World):
    """
    StarCraft II: Wings of Liberty is a science fiction real-time strategy video game developed and published by Blizzard Entertainment.
    Command Raynor's Raiders in collecting pieces of the Keystone in order to stop the zerg threat posed by the Queen of Blades.
    """

    game = "Starcraft 2 Wings of Liberty"
    web = Starcraft2WoLWebWorld()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {location.name: location.code for location in get_locations(None, None)}
    options = sc2wol_options

    item_name_groups = item_name_groups
    locked_locations: typing.List[str]
    location_cache: typing.List[Location]
    mission_req_table = {}

    def __init__(self, world: MultiWorld, player: int):
        super(SC2WoLWorld, self).__init__(world, player)
        self.location_cache = []
        self.locked_locations = []

    def _create_items(self, name: str):
        data = get_full_item_list()[name]
        return [self.create_item(name) for _ in range(data.quantity)]

    def create_item(self, name: str) -> Item:
        data = get_full_item_list()[name]
        return StarcraftWoLItem(name, data.progression, data.code, self.player)

    def create_regions(self):
        self.mission_req_table = create_regions(self.world, self.player, get_locations(self.world, self.player),
                                                self.location_cache)

    def generate_basic(self):
        excluded_items = get_excluded_items(self, self.world, self.player)

        assign_starter_items(self.world, self.player, excluded_items, self.locked_locations)

        pool = get_item_pool(self.world, self.player, excluded_items)

        fill_item_pool_with_dummy_items(self, self.world, self.player, self.locked_locations, self.location_cache, pool)

        self.world.itempool += pool

    def set_rules(self):
        setup_events(self.world, self.player, self.locked_locations, self.location_cache)

        self.world.completion_condition[self.player] = lambda state: state.has('All-In: Victory', self.player)

    def get_filler_item_name(self) -> str:
        return self.world.random.choice(filler_items)

    def fill_slot_data(self):
        slot_data = {}
        for option_name in sc2wol_options:
            option = getattr(self.world, option_name)[self.player]
            if type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        slot_req_table = {}
        for mission in self.mission_req_table:
            slot_req_table[mission] = self.mission_req_table[mission]._asdict()

        slot_data["mission_req"] = slot_req_table
        return slot_data


def setup_events(world: MultiWorld, player: int, locked_locations: typing.List[str], location_cache: typing.List[Location]):
    for location in location_cache:
        if location.address == None:
            item = Item(location.name, True, None, player)

            locked_locations.append(location.name)

            location.place_locked_item(item)


def get_excluded_items(self: SC2WoLWorld, world: MultiWorld, player: int) -> Set[str]:
    excluded_items: Set[str] = set()

    if get_option_value(world, player, "upgrade_bonus") == 1:
        excluded_items.add("Ultra-Capacitors")
    else:
        excluded_items.add("Vanadium Plating")

    if get_option_value(world, player, "bunker_upgrade") == 1:
        excluded_items.add("Shrike Turret")
    else:
        excluded_items.add("Fortified Bunker")

    for item in world.precollected_items[player]:
        excluded_items.add(item.name)

    return excluded_items


def assign_starter_items(world: MultiWorld, player: int, excluded_items: Set[str], locked_locations: List[str]):
    non_local_items = world.non_local_items[player].value

    local_basic_unit = tuple(item for item in basic_unit if item not in non_local_items)
    if not local_basic_unit:
        raise Exception("At least one basic unit must be local")

    # The first world should also be the starting world
    first_location = list(world.worlds[player].mission_req_table)[0]

    if first_location == "In Utter Darkness":
        first_location = first_location + ": Defeat"
    else:
        first_location = first_location + ": Victory"

    assign_starter_item(world, player, excluded_items, locked_locations, first_location,
                        local_basic_unit)


def assign_starter_item(world: MultiWorld, player: int, excluded_items: Set[str], locked_locations: List[str],
                        location: str, item_list: Tuple[str, ...]):

    item_name = world.random.choice(item_list)

    excluded_items.add(item_name)

    item = create_item_with_correct_settings(world, player, item_name)

    world.get_location(location, player).place_locked_item(item)

    locked_locations.append(location)


def get_item_pool(world: MultiWorld, player: int, excluded_items: Set[str]) -> List[Item]:
    pool: List[Item] = []

    for name, data in item_table.items():
        if name not in excluded_items:
            for _ in range(data.quantity):
                item = create_item_with_correct_settings(world, player, name)
                pool.append(item)

    return pool


def fill_item_pool_with_dummy_items(self: SC2WoLWorld, world: MultiWorld, player: int, locked_locations: List[str],
                                    location_cache: List[Location], pool: List[Item]):
    for _ in range(len(location_cache) - len(locked_locations) - len(pool)):
        item = create_item_with_correct_settings(world, player, self.get_filler_item_name())
        pool.append(item)


def create_item_with_correct_settings(world: MultiWorld, player: int, name: str) -> Item:
    data = item_table[name]

    item = Item(name, data.progression, data.code, player)
    item.never_exclude = data.never_exclude

    if not item.advancement:
        return item

    return item
