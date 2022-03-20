from __future__ import annotations

import logging
from typing import Dict, Set, Tuple, List, Optional, TextIO, Any, Callable, Union

from BaseClasses import MultiWorld, Item, CollectionState, Location
from Options import Option


class AutoWorldRegister(type):
    world_types: Dict[str, World] = {}

    def __new__(cls, name: str, bases, dct: Dict[str, Any]):
        # filter out any events
        dct["item_name_to_id"] = {name: id for name, id in dct["item_name_to_id"].items() if id}
        dct["location_name_to_id"] = {name: id for name, id in dct["location_name_to_id"].items() if id}
        # build reverse lookups
        dct["item_id_to_name"] = {code: name for name, code in dct["item_name_to_id"].items()}
        dct["location_id_to_name"] = {code: name for name, code in dct["location_name_to_id"].items()}

        # build rest
        dct["item_names"] = frozenset(dct["item_name_to_id"])
        dct["item_name_groups"] = dct.get("item_name_groups", {})
        dct["item_name_groups"]["Everything"] = dct["item_names"]
        dct["location_names"] = frozenset(dct["location_name_to_id"])
        dct["all_item_and_group_names"] = frozenset(dct["item_names"] | set(dct.get("item_name_groups", {})))

        # construct class
        new_class = super().__new__(cls, name, bases, dct)
        if "game" in dct:
            AutoWorldRegister.world_types[dct["game"]] = new_class
        return new_class


class AutoLogicRegister(type):
    def __new__(cls, name, bases, dct):
        new_class = super().__new__(cls, name, bases, dct)
        function: Callable
        for item_name, function in dct.items():
            if item_name == "copy_mixin":
                CollectionState.additional_copy_functions.append(function)
            elif item_name == "init_mixin":
                CollectionState.additional_init_functions.append(function)
            elif not item_name.startswith("__"):
                if hasattr(CollectionState, item_name):
                    raise Exception(f"Name conflict on Logic Mixin {name} trying to overwrite {item_name}")
                setattr(CollectionState, item_name, function)
        return new_class


def call_single(world: MultiWorld, method_name: str, player: int, *args):
    method = getattr(world.worlds[player], method_name)
    return method(*args)


def call_all(world: MultiWorld, method_name: str, *args):
    world_types = set()
    for player in world.player_ids:
        world_types.add(world.worlds[player].__class__)
        call_single(world, method_name, player, *args)

    for world_type in world_types:
        stage_callable = getattr(world_type, f"stage_{method_name}", None)
        if stage_callable:
            stage_callable(world, *args)


def call_stage(world: MultiWorld, method_name: str, *args):
    world_types = {world.worlds[player].__class__ for player in world.player_ids}
    for world_type in world_types:
        stage_callable = getattr(world_type, f"stage_{method_name}", None)
        if stage_callable:
            stage_callable(world, *args)


class WebWorld:
    """Webhost integration"""
    # display a settings page. Can be a link to an out-of-ap settings tool too.
    settings_page: Union[bool, str] = True

    # Choose a theme for your /game/* pages
    # Available: dirt, grass, grassFlowers, ice, jungle
    theme = "grass"


class World(metaclass=AutoWorldRegister):
    """A World object encompasses a game's Items, Locations, Rules and additional data or functionality required.
    A Game should have its own subclass of World in which it defines the required data structures."""

    options: Dict[str, type(Option)] = {}  # link your Options mapping
    game: str  # name the game
    topology_present: bool = False  # indicate if world type has any meaningful layout/pathing
    all_item_and_group_names: Set[str] = frozenset()  # gets automatically populated with all item and item group names

    # map names to their IDs
    item_name_to_id: Dict[str, int] = {}
    location_name_to_id: Dict[str, int] = {}

    # maps item group names to sets of items. Example: "Weapons" -> {"Sword", "Bow"}
    item_name_groups: Dict[str, Set[str]] = {}

    # increment this every time something in your world's names/id mappings changes.
    # While this is set to 0 in *any* AutoWorld, the entire DataPackage is considered in testing mode and will be
    # retrieved by clients on every connection.
    data_version: int = 1

    hint_blacklist: Set[str] = frozenset()  # any names that should not be hintable

    # NOTE: remote_items and remote_start_inventory are now available in the network protocol for the client to set.
    # These values will be removed.
    # if a world is set to remote_items, then it just needs to send location checks to the server and the server
    # sends back the items
    # if a world is set to remote_items = False, then the server never sends an item where receiver == finder,
    # the client finds its own items in its own world.
    remote_items: bool = True

    # If remote_start_inventory is true, the start_inventory/world.precollected_items is sent on connection,
    # otherwise the world implementation is in charge of writing the items to their output data.
    remote_start_inventory: bool = True

    # For games where after a victory it is impossible to go back in and get additional/remaining Locations checked.
    # this forces forfeit:  auto for those games.
    forced_auto_forfeit: bool = False

    # Hide World Type from various views. Does not remove functionality.
    hidden: bool = False

    # autoset on creation:
    world: MultiWorld
    player: int

    # automatically generated
    item_id_to_name: Dict[int, str]
    location_id_to_name: Dict[int, str]

    item_names: Set[str]  # set of all potential item names
    location_names: Set[str]  # set of all potential location names

    # If the game displays all contained items to the user, this flag pre-fills the hint system with this information
    # For example the "full" tech tree information option in Factorio
    sending_visible: bool = False

    web: WebWorld = WebWorld()

    def __init__(self, world: MultiWorld, player: int):
        self.world = world
        self.player = player

    # overridable methods that get called by Main.py, sorted by execution order
    # can also be implemented as a classmethod and called "stage_<original_name>",
    # in that case the MultiWorld object is passed as an argument and it gets called once for the entire multiworld.
    # An example of this can be found in alttp as stage_pre_fill
    def generate_early(self):
        pass

    def create_regions(self):
        pass

    def create_items(self):
        pass

    def set_rules(self):
        pass

    def generate_basic(self):
        pass

    def pre_fill(self):
        """Optional method that is supposed to be used for special fill stages. This is run *after* plando."""
        pass

    @classmethod
    def fill_hook(cls, progitempool: List[Item], nonexcludeditempool: List[Item],
                  localrestitempool: Dict[int, List[Item]], nonlocalrestitempool: Dict[int, List[Item]],
                  restitempool: List[Item], fill_locations: List[Location]):
        """Special method that gets called as part of distribute_items_restrictive (main fill).
        This gets called once per present world type."""
        pass

    def post_fill(self):
        """Optional Method that is called after regular fill. Can be used to do adjustments before output generation."""

    def generate_output(self, output_directory: str):
        """This method gets called from a threadpool, do not use world.random here.
        If you need any last-second randomization, use MultiWorld.slot_seeds[slot] instead."""
        pass

    def fill_slot_data(self) -> dict:
        """Fill in the slot_data field in the Connected network package."""
        return {}

    def modify_multidata(self, multidata: dict):
        """For deeper modification of server multidata."""
        pass

    def get_required_client_version(self) -> Tuple[int, int, int]:
        return 0, 1, 6

    # Spoiler writing is optional, these may not get called.
    def write_spoiler_header(self, spoiler_handle: TextIO):
        """Write to the spoiler header. If individual it's right at the end of that player's options,
        if as stage it's right under the common header before per-player options."""
        pass

    def write_spoiler(self, spoiler_handle: TextIO):
        """Write to the spoiler "middle", this is after the per-player options and before locations,
        meant for useful or interesting info."""
        pass

    def write_spoiler_end(self, spoiler_handle: TextIO):
        """Write to the end of the spoiler"""
        pass

    # end of ordered Main.py calls

    def create_item(self, name: str) -> Item:
        """Create an item for this world type and player.
        Warning: this may be called with self.world = None, for example by MultiServer"""
        raise NotImplementedError

    def get_filler_item_name(self) -> str:
        """Called when the item pool needs to be filled with additional items to match location count."""
        logging.warning(f"World {self} is generating a filler item without custom filler pool.")
        return self.world.random.choice(self.item_name_to_id)

    # decent place to implement progressive items, in most cases can stay as-is
    def collect_item(self, state: CollectionState, item: Item, remove: bool = False) -> Optional[str]:
        """Collect an item name into state. For speed reasons items that aren't logically useful get skipped.
        Collect None to skip item.
        :param state: CollectionState to collect into
        :param item: Item to decide on if it should be collected into state
        :param remove: indicate if this is meant to remove from state instead of adding."""
        if item.advancement:
            return item.name

    # called to create all_state, return Items that are created during pre_fill
    def get_pre_fill_items(self) -> List[Item]:
        return []

    # following methods should not need to be overridden.
    def collect(self, state: CollectionState, item: Item) -> bool:
        name = self.collect_item(state, item)
        if name:
            state.prog_items[name, self.player] += 1
            return True
        return False

    def remove(self, state: CollectionState, item: Item) -> bool:
        name = self.collect_item(state, item, True)
        if name:
            state.prog_items[name, self.player] -= 1
            if state.prog_items[name, self.player] < 1:
                del (state.prog_items[name, self.player])
            return True
        return False

    def create_filler(self):
        self.world.itempool.append(self.create_item(self.get_filler_item_name()))


# any methods attached to this can be used as part of CollectionState,
# please use a prefix as all of them get clobbered together
class LogicMixin(metaclass=AutoLogicRegister):
    pass

