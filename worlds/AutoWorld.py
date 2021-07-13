from __future__ import annotations
from typing import Dict, Set, Tuple

from BaseClasses import MultiWorld, Item, CollectionState


class AutoWorldRegister(type):
    world_types:Dict[str, World] = {}

    def __new__(cls, name, bases, dct):
        dct["all_names"] = dct["item_names"] | dct["location_names"] | set(dct.get("item_name_groups", {}))
        # filter out any events
        dct["item_name_to_id"] = {name: id for name, id in dct["item_name_to_id"].items() if id}
        dct["location_name_to_id"] = {name: id for name, id in dct["location_name_to_id"].items() if id}
        # build reverse lookups
        dct["item_id_to_name"] = {code: name for name, code in dct["item_name_to_id"].items()}
        dct["location_id_to_name"] = {code: name for name, code in dct["location_name_to_id"].items()}
        # construct class
        new_class = super().__new__(cls, name, bases, dct)
        if "game" in dct:
            AutoWorldRegister.world_types[dct["game"]] = new_class
        return new_class


def call_single(world: MultiWorld, method_name: str, player: int):
    method = getattr(world.worlds[player], method_name)
    return method()


def call_all(world: MultiWorld, method_name: str):
    for player in world.player_ids:
        call_single(world, method_name, player)


class World(metaclass=AutoWorldRegister):
    """A World object encompasses a game's Items, Locations, Rules and additional data or functionality required.
    A Game should have its own subclass of World in which it defines the required data structures."""

    world: MultiWorld
    player: int
    options: dict = {}
    topology_present: bool = False  # indicate if world type has any meaningful layout/pathing
    item_names: Set[str] = frozenset()  # set of all potential item names
    # maps item group names to sets of items. Example: "Weapons" -> {"Sword", "Bow"}
    item_name_groups: Dict[str, Set[str]] = {}
    location_names: Set[str] = frozenset()  # set of all potential location names
    all_names: Set[str] = frozenset()  # gets automatically populated with all item, item group and location names

    # map names to their IDs
    item_name_to_id: Dict[str, int] = {}
    location_name_to_id: Dict[str, int] = {}

    # reverse, automatically generated
    item_id_to_name: Dict[int, str] = {}
    location_id_to_name: Dict[int, str] = {}

    data_version = 1  # increment this every time something in your world's names/id mappings changes.

    hint_blacklist: Set[str] = frozenset()  # any names that should not be hintable

    def __init__(self, world: MultiWorld, player: int):
        self.world = world
        self.player = player

    # overwritable methods that get called by Main.py, sorted by execution order
    def create_regions(self):
        pass

    def set_rules(self):
        pass

    def generate_basic(self):
        pass

    def generate_output(self):
        """This method gets called from a threadpool, do not use world.random here.
        If you need any last-second randomization, use MultiWorld.slot_seeds[slot] instead."""
        pass

    def get_required_client_version(self) -> Tuple[int, int, int]:
        return 0, 0, 3

    # end of Main.py calls

    def collect(self, state: CollectionState, item: Item) -> bool:
        """Collect an item into state. For speed reasons items that aren't logically useful get skipped."""
        if item.advancement:
            state.prog_items[item.name, item.player] += 1
            return True  # indicate that a logical state change has occured
        return False

    def create_item(self, name: str) -> Item:
        """Create an item for this world type and player.
        Warning: this may be called with self.world = None, for example by MultiServer"""
        raise NotImplementedError
