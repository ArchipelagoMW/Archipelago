from collections import deque
import functools
from typing import Any, Dict, FrozenSet, Set, TextIO, Tuple, List, Optional, cast
import os
import logging

from BaseClasses import ItemClassification, LocationProgressType, \
    MultiWorld, Location, Item, CollectionState, RegionType, \
    Entrance, Tutorial
from Options import AssembleOptions
from .logic import clear_cache, cs_to_zz_locs
from .region import ZillionLocation, ZillionRegion
from .options import ZillionItemCounts, zillion_options, validate
from .id_maps import item_name_to_id as _item_name_to_id, \
    loc_name_to_id as _loc_name_to_id, make_id_to_others, \
    zz_reg_name_to_reg_name, base_id
from .item import ZillionItem
from .patch import ZillionDeltaPatch, get_base_rom_path

from zilliandomizer.randomizer import Randomizer as ZzRandomizer
from zilliandomizer.system import System
from zilliandomizer.logic_components.items import RESCUE, items as zz_items, Item as ZzItem
from zilliandomizer.logic_components.locations import Location as ZzLocation, Req
from zilliandomizer.options import Chars

from ..AutoWorld import World, WebWorld


class ZillionWebWorld(WebWorld):
    # theme = 'jungle'  # TODO: what themes are available?
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Zillion randomizer.",  # This guide covers single-player, multiworld and related software.",
        "English",
        "setup_en.md",
        "setup/en",
        ["beauxq"]
    )]


class ZillionWorld(World):
    """
    Zillion is a metroidvania style game released in 1987 for the 8-bit Sega Master System.

    It's based on the anime Zillion (赤い光弾ジリオン, Akai Koudan Zillion).
    """
    game = "Zillion"
    web = ZillionWebWorld()

    option_definitions: Dict[str, AssembleOptions] = zillion_options
    topology_present: bool = True  # indicate if world type has any meaningful layout/pathing

    # gets automatically populated with all item and item group names
    all_item_and_group_names: FrozenSet[str] = frozenset()

    # map names to their IDs
    item_name_to_id: Dict[str, int] = _item_name_to_id
    location_name_to_id: Dict[str, int] = _loc_name_to_id

    # maps item group names to sets of items. Example: "Weapons" -> {"Sword", "Bow"}
    item_name_groups: Dict[str, Set[str]] = {}

    # increment this every time something in your world's names/id mappings changes.
    # While this is set to 0 in *any* AutoWorld, the entire DataPackage is considered in testing mode and will be
    # retrieved by clients on every connection.
    data_version: int = 0
    # TODO: move out of testing
    # The same code that generates the static resource for the id maps
    # could manage the version number

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
    remote_items: bool = False

    # If remote_start_inventory is true, the start_inventory/world.precollected_items is sent on connection,
    # otherwise the world implementation is in charge of writing the items to their output data.
    remote_start_inventory: bool = True

    # For games where after a victory it is impossible to go back in and get additional/remaining Locations checked.
    # this forces forfeit:  auto for those games.
    forced_auto_forfeit: bool = False

    # Hide World Type from various views. Does not remove functionality.
    hidden: bool = False

    logger: logging.Logger

    id_to_zz_item: Optional[Dict[int, ZzItem]] = None
    zz_system: System

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.logger = logging.getLogger("Zillion")
        self.zz_system = System()

    def _make_item_maps(self, start_char: Chars) -> None:
        _id_to_name, _id_to_zz_id, id_to_zz_item = make_id_to_others(start_char)
        self.id_to_zz_item = id_to_zz_item

    @classmethod
    def stage_assert_generate(cls, world: MultiWorld) -> None:
        """Checks that a game is capable of generating, usually checks for some base file like a ROM.
        Not run for unittests since they don't produce output"""
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def generate_early(self) -> None:
        zz_op = validate(self.world, self.player)

        rom_dir_name = os.path.dirname(get_base_rom_path())
        self.zz_system.make_patcher(rom_dir_name)
        self.zz_system.make_randomizer(zz_op)

        self.zz_system.make_map()

        # just in case the options changed anything (I don't think they do)
        assert self.zz_system.randomizer, "init failed"
        for zz_name in self.zz_system.randomizer.locations:
            if zz_name != 'main':
                assert self.zz_system.randomizer.loc_name_2_pretty[zz_name] in self.location_name_to_id, \
                    f"{self.zz_system.randomizer.loc_name_2_pretty[zz_name]} not in location map"

        self._make_item_maps(zz_op.start_char)

    def create_regions(self) -> None:
        assert self.zz_system.randomizer, "generate_early hasn't been called"
        assert self.id_to_zz_item, "generate_early hasn't been called"
        p = self.player
        w = self.world

        self.zz_system.randomizer.place_canister_gun_reqs()

        start = self.zz_system.randomizer.regions['start']

        all: Dict[str, ZillionRegion] = {}
        for here_zz_name, zz_r in self.zz_system.randomizer.regions.items():
            here_name = "Menu" if here_zz_name == "start" else zz_reg_name_to_reg_name(here_zz_name)
            all[here_name] = ZillionRegion(zz_r, here_name, RegionType.Generic, here_name, p, w)
            self.world.regions.append(all[here_name])

        limited_skill = Req(gun=3, jump=3, skill=self.zz_system.randomizer.options.skill, hp=940, red=1, floppy=126)
        queue = deque([start])
        done: Set[str] = set()
        while len(queue):
            zz_here = queue.popleft()
            here_name = "Menu" if zz_here.name == "start" else zz_reg_name_to_reg_name(zz_here.name)
            if here_name in done:
                continue
            here = all[here_name]

            for zz_loc in zz_here.locations:
                # if local gun reqs didn't place item
                if not zz_loc.item:

                    def access_rule_wrapped(zz_loc_local: ZzLocation,
                                            p: int,
                                            zz_r: ZzRandomizer,
                                            id_to_zz_item: Dict[int, ZzItem],
                                            cs: CollectionState) -> bool:
                        # print(f"checking access to {zz_loc_local}")
                        accessible = cs_to_zz_locs(cs, p, zz_r, id_to_zz_item)
                        return zz_loc_local in accessible

                    access_rule = functools.partial(access_rule_wrapped,
                                                    zz_loc, self.player, self.zz_system.randomizer, self.id_to_zz_item)

                    loc_name = self.zz_system.randomizer.loc_name_2_pretty[zz_loc.name]
                    loc = ZillionLocation(zz_loc, self.player, loc_name, here)
                    loc.access_rule = access_rule
                    if not (limited_skill >= zz_loc.req):
                        loc.progress_type = LocationProgressType.EXCLUDED
                        self.world.exclude_locations[p].value.add(loc.name)
                    here.locations.append(loc)

            for zz_dest in zz_here.connections.keys():
                dest_name = "Menu" if zz_dest.name == 'start' else zz_reg_name_to_reg_name(zz_dest.name)
                dest = all[dest_name]
                exit = Entrance(p, f"{here_name} to {dest_name}", here)
                here.exits.append(exit)
                exit.connect(dest)

                queue.append(zz_dest)
            done.add(here.name)

    def create_items(self) -> None:
        if not self.id_to_zz_item:
            self._make_item_maps("JJ")
            self.logger.warning("warning: called `create_items` without calling `generate_early` first")
        assert self.id_to_zz_item, "failed to get item maps"

        # in zilliandomizer, the Randomizer class puts empties in the item pool to fill space,
        # but here in AP, empties are in the options from options.validate
        item_counts = cast(ZillionItemCounts, getattr(self.world, "item_counts")[self.player])
        self.logger.debug(item_counts)

        for item_name, item_id in self.item_name_to_id.items():
            zz_item = self.id_to_zz_item[item_id]
            if item_id >= (4 + base_id):  # normal item
                if item_name in item_counts.value:
                    count = item_counts.value[item_name]
                    self.logger.debug(f"Zillion Items: {item_name}  {count}")
                    for _ in range(count):
                        self.world.itempool.append(self.create_item(item_name))
            elif item_id < (3 + base_id) and zz_item.code == RESCUE:
                # One of the 3 rescues will not be in the pool and its zz_item will be 'empty'.
                self.logger.debug(f"Zillion Items: {item_name}  1")
                self.world.itempool.append(self.create_item(item_name))

    def set_rules(self) -> None:
        # logic for this game is in create_regions
        pass

    def generate_basic(self) -> None:
        assert self.zz_system.randomizer, "generate_early hasn't been called"
        # main location name is an alias
        main_loc_name = self.zz_system.randomizer.loc_name_2_pretty[self.zz_system.randomizer.locations['main'].name]

        self.world.get_location(main_loc_name, self.player)\
            .place_locked_item(self.create_item("Win"))
        self.world.completion_condition[self.player] = \
            lambda state: state.has("Win", self.player)

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

    # def place_item_hook(self, location: Location) -> None:
    #     if isinstance(location, ZillionLocation):
    #         placed_item = cast(ZillionItem, location.item)
    #         location.zz_loc.item = placed_item.zz_item

    def post_fill(self) -> None:
        """Optional Method that is called after regular fill. Can be used to do adjustments before output generation.
        This happens before progression balancing,  so the items may not be in their final locations yet."""

        self.zz_system.post_fill()

    def finalize_item_locations(self) -> None:
        """
        sync zilliandomizer item locations with AP item locations
        """
        assert self.zz_system.randomizer, "generate_early hasn't been called"
        zz_options = self.zz_system.randomizer.options

        # debug_zz_loc_ids: Dict[str, int] = {}
        empty = zz_items[4]
        multi_item = empty  # a different patcher method differentiates empty from ap multi item
        multi_items: Dict[str, Tuple[str, str]] = {}  # zz_loc_name to (item_name, player_name)
        for loc in self.world.get_locations():
            if loc.player == self.player:
                z_loc = cast(ZillionLocation, loc)
                # debug_zz_loc_ids[z_loc.zz_loc.name] = id(z_loc.zz_loc)
                if z_loc.item is None:
                    self.logger.warn("generate_output location has no item - is that ok?")
                    z_loc.zz_loc.item = empty
                elif z_loc.item.player == self.player:
                    z_item = cast(ZillionItem, z_loc.item)
                    z_loc.zz_loc.item = z_item.zz_item
                else:  # another player's item
                    # print(f"put multi item in {z_loc.zz_loc.name}")
                    z_loc.zz_loc.item = multi_item
                    multi_items[z_loc.zz_loc.name] = (
                        z_loc.item.name,
                        self.world.get_player_name(z_loc.item.player)
                    )
        # debug_zz_loc_ids.sort()
        # for name, id_ in debug_zz_loc_ids.items():
        #     print(id_)
        # print("size:", len(debug_zz_loc_ids))

        # debug_loc_to_id: Dict[str, int] = {}
        # regions = self.zz_randomizer.regions
        # for region in regions.values():
        #     for loc in region.locations:
        #         if loc.name not in self.zz_randomizer.locations:
        #             print(f"region {region.name} had location {loc.name} not in locations")
        #         debug_loc_to_id[loc.name] = id(loc)

        # verify that every location got an item
        for zz_loc in self.zz_system.randomizer.locations.values():
            assert zz_loc.item, (
                f"location {self.zz_system.randomizer.loc_name_2_pretty[zz_loc.name]} "
                f"in world {self.player} didn't get an item"
            )

        zz_patcher = self.zz_system.patcher
        assert zz_patcher, "generate_early didn't set patcher"

        zz_patcher.write_locations(self.zz_system.randomizer.regions,
                                   zz_options.start_char,
                                   self.zz_system.randomizer.loc_name_2_pretty)
        zz_patcher.all_fixes_and_options(zz_options)
        zz_patcher.set_external_item_interface(zz_options.start_char, zz_options.max_level)
        zz_patcher.set_multiworld_items(multi_items)
        zz_patcher.set_rom_to_ram_data(self.world.player_name[self.player].replace(' ', '_').encode())

    def generate_output(self, output_directory: str) -> None:
        """This method gets called from a threadpool, do not use world.random here.
        If you need any last-second randomization, use MultiWorld.slot_seeds[slot] instead."""
        self.finalize_item_locations()

        assert self.zz_system.patcher, "didn't get patcher from generate_early"
        # original_rom_bytes = self.zz_patcher.rom
        patched_rom_bytes = self.zz_system.patcher.get_patched_bytes()

        out_file_base = 'AP_' + self.world.seed_name
        out_file_p_name = f'_P{self.player}'
        out_file_p_name += f"_{self.world.get_file_safe_player_name(self.player).replace(' ', '_')}"

        filename = os.path.join(
            output_directory,
            f'{out_file_base}{out_file_p_name}{ZillionDeltaPatch.result_file_ending}'
        )
        with open(filename, "wb") as binary_file:
            binary_file.write(patched_rom_bytes)
        patch = ZillionDeltaPatch(
            os.path.splitext(filename)[0] + ZillionDeltaPatch.patch_file_ending,
            player=self.player,
            player_name=self.world.player_name[self.player],
            patched_path=filename
        )
        patch.write()
        os.remove(filename)
        clear_cache()

    def fill_slot_data(self) -> Dict[str, Any]:  # json of WebHostLib.models.Slot
        """Fill in the `slot_data` field in the `Connected` network package.
        This is a way the generator can give custom data to the client.
        The client will receive this as JSON in the `Connected` response."""

        # TODO: share a TypedDict data structure with client

        # TODO: tell client which canisters are keywords
        # so it can open and get those when restoring doors

        zz_patcher = self.zz_system.patcher
        assert zz_patcher, "didn't get patcher from generate_early"
        assert self.zz_system.randomizer, "didn't get randomizer from generate_early"

        rescues: Dict[str, Any] = {}
        for i in (0, 1):
            if i in zz_patcher.rescue_locations:
                ri = zz_patcher.rescue_locations[i]
                rescues[str(i)] = {
                    "start_char": ri.start_char,
                    "room_code": ri.room_code,
                    "mask": ri.mask
                }
        zz_patcher.loc_memory_to_loc_id
        return {
            "start_char": self.zz_system.randomizer.options.start_char,
            "rescues": rescues,
            "loc_mem_to_id": zz_patcher.loc_memory_to_loc_id
        }

    def modify_multidata(self, multidata: Dict[str, Any]) -> None:
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
        item_id = _item_name_to_id[name]

        if not self.id_to_zz_item:
            self._make_item_maps("JJ")
            self.logger.warning("warning: called `create_item` without calling `generate_early` first")
        assert self.id_to_zz_item, "failed to get item maps"

        classification = ItemClassification.filler
        zz_item = self.id_to_zz_item[item_id]
        if zz_item.required:
            classification = ItemClassification.progression
            if not zz_item.is_progression:
                classification = ItemClassification.progression_skip_balancing

        z_item = ZillionItem(name, classification, item_id, self.player, zz_item)
        return z_item

    def get_filler_item_name(self) -> str:
        """Called when the item pool needs to be filled with additional items to match location count."""
        return "Empty"

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
