from __future__ import annotations

import logging
import sys
from typing import Dict, FrozenSet, Set, Tuple, List, Optional, TextIO, Any, Callable, Union, NamedTuple

from BaseClasses import MultiWorld, Item, CollectionState, Location, Tutorial
from Options import Option


class AutoWorldRegister(type):
    world_types: Dict[str, type(World)] = {}

    def __new__(mcs, name: str, bases: Tuple[type, ...], dct: Dict[str, Any]) -> AutoWorldRegister:
        if "web" in dct:
            assert isinstance(dct["web"], WebWorld), "WebWorld has to be instantiated."
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

        # move away from get_required_client_version function
        if "game" in dct:
            assert "get_required_client_version" not in dct, f"{name}: required_client_version is an attribute now"
        # set minimum required_client_version from bases
        if "required_client_version" in dct and bases:
            for base in bases:
                if "required_client_version" in base.__dict__:
                    dct["required_client_version"] = max(dct["required_client_version"],
                                                         base.__dict__["required_client_version"])

        # construct class
        new_class = super().__new__(mcs, name, bases, dct)
        if "game" in dct:
            AutoWorldRegister.world_types[dct["game"]] = new_class
        new_class.__file__ = sys.modules[new_class.__module__].__file__
        return new_class


class AutoLogicRegister(type):
    def __new__(cls, name: str, bases: Tuple[type, ...], dct: Dict[str, Any]) -> AutoLogicRegister:
        new_class = super().__new__(cls, name, bases, dct)
        function: Callable[..., Any]
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


def call_single(world: MultiWorld, method_name: str, player: int, *args: Any) -> Any:
    method = getattr(world.worlds[player], method_name)
    return method(*args)


def call_all(world: MultiWorld, method_name: str, *args: Any) -> None:
    world_types: Set[AutoWorldRegister] = set()
    for player in world.player_ids:
        world_types.add(world.worlds[player].__class__)
        call_single(world, method_name, player, *args)

    for world_type in world_types:
        stage_callable = getattr(world_type, f"stage_{method_name}", None)
        if stage_callable:
            stage_callable(world, *args)


def call_stage(world: MultiWorld, method_name: str, *args: Any) -> None:
    world_types = {world.worlds[player].__class__ for player in world.player_ids}
    for world_type in world_types:
        stage_callable = getattr(world_type, f"stage_{method_name}", None)
        if stage_callable:
            stage_callable(world, *args)


class WebWorld:
    """Webhost integration"""
    # display a settings page. Can be a link to an out-of-ap settings tool too.
    settings_page: Union[bool, str] = True

    # docs folder will be scanned for game info pages using this list in the format '{language}_{game_name}.md'
    game_info_languages: List[str] = ['en']

    # docs folder will also be scanned for tutorial guides given the relevant information in this list. Each Tutorial
    # class is to be used for one guide.
    tutorials: List[Tutorial]

    # Choose a theme for your /game/* pages
    # Available: dirt, grass, grassFlowers, ice, jungle, ocean, partyTime, stone
    theme = "grass"

    # display a link to a bug report page, most likely a link to a GitHub issue page.
    bug_report_page: Optional[str]


class World(metaclass=AutoWorldRegister):
    """A World object encompasses a game's Items, Locations, Rules and additional data or functionality required.
    A Game should have its own subclass of World in which it defines the required data structures."""

    options: Dict[str, Option[Any]] = {}  # link your Options mapping
    game: str  # name the game
    topology_present: bool = False  # indicate if world type has any meaningful layout/pathing

    # gets automatically populated with all item and item group names
    all_item_and_group_names: FrozenSet[str] = frozenset()

    # map names to their IDs
    item_name_to_id: Dict[str, int] = {}
    location_name_to_id: Dict[str, int] = {}

    # maps item group names to sets of items. Example: "Weapons" -> {"Sword", "Bow"}
    item_name_groups: Dict[str, Set[str]] = {}

    # increment this every time something in your world's names/id mappings changes.
    # While this is set to 0 in *any* AutoWorld, the entire DataPackage is considered in testing mode and will be
    # retrieved by clients on every connection.
    data_version: int = 1

    # override this if changes to a world break forward-compatibility of the client
    # The base version of (0, 1, 6) is provided for backwards compatibility and does *not* need to be updated in the
    # future. Protocol level compatibility check moved to MultiServer.min_client_version.
    required_client_version: Tuple[int, int, int] = (0, 1, 6)

    # update this if the resulting multidata breaks forward-compatibility of the server
    required_server_version: Tuple[int, int, int] = (0, 2, 4)

    hint_blacklist: FrozenSet[str] = frozenset()  # any names that should not be hintable

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

    web: WebWorld = WebWorld()

    def __init__(self, world: MultiWorld, player: int):
        self.world = world
        self.player = player

    # overridable methods that get called by Main.py, sorted by execution order
    # can also be implemented as a classmethod and called "stage_<original_name>",
    # in that case the MultiWorld object is passed as an argument and it gets called once for the entire multiworld.
    # An example of this can be found in alttp as stage_pre_fill
    @classmethod
    def assert_generate(cls) -> None:
        """Checks that a game is capable of generating, usually checks for some base file like a ROM.
        Not run for unittests since they don't produce output"""
        pass

    def generate_early(self) -> None:
        pass

    def create_regions(self) -> None:
        pass

    def create_items(self) -> None:
        pass

    def set_rules(self) -> None:
        pass

    def generate_basic(self) -> None:
        pass

    def pre_fill(self) -> None:
        """Optional method that is supposed to be used for special fill stages. This is run *after* plando."""
        pass

    @classmethod
    def fill_hook(cls,
                  progitempool: List[Item],
                  nonexcludeditempool: List[Item],
                  localrestitempool: Dict[int, List[Item]],
                  nonlocalrestitempool: Dict[int, List[Item]],
                  restitempool: List[Item],
                  fill_locations: List[Location]) -> None:
        """Special method that gets called as part of distribute_items_restrictive (main fill).
        This gets called once per present world type."""
        pass

    def post_fill(self) -> None:
        """Optional Method that is called after regular fill. Can be used to do adjustments before output generation."""

    def generate_output(self, output_directory: str) -> None:
        """This method gets called from a threadpool, do not use world.random here.
        If you need any last-second randomization, use MultiWorld.slot_seeds[slot] instead."""
        pass

    def fill_slot_data(self) -> Dict[str, Any]:  # json of WebHostLib.models.Slot
        """Fill in the slot_data field in the Connected network package."""
        return {}

    def modify_multidata(self, multidata: Dict[str, Any]) -> None:  # TODO: TypedDict for multidata?
        """For deeper modification of server multidata."""
        pass

    # Spoiler writing is optional, these may not get called.
    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        """Write to the spoiler header. If individual it's right at the end of that player's options,
        if as stage it's right under the common header before per-player options."""
        pass

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        """Write to the spoiler "middle", this is after the per-player options and before locations,
        meant for useful or interesting info."""
        pass

    def write_spoiler_end(self, spoiler_handle: TextIO) -> None:
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
        return self.world.random.choice(tuple(self.item_name_to_id.keys()))

    # decent place to implement progressive items, in most cases can stay as-is
    def collect_item(self, state: CollectionState, item: Item, remove: bool = False) -> Optional[str]:
        """Collect an item name into state. For speed reasons items that aren't logically useful get skipped.
        Collect None to skip item.
        :param state: CollectionState to collect into
        :param item: Item to decide on if it should be collected into state
        :param remove: indicate if this is meant to remove from state instead of adding."""
        if item.advancement:
            return item.name
        return None

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

    def create_filler(self) -> Item:
        return self.create_item(self.get_filler_item_name())


# any methods attached to this can be used as part of CollectionState,
# please use a prefix as all of them get clobbered together
class LogicMixin(metaclass=AutoLogicRegister):
    pass
