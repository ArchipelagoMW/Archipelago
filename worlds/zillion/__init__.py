from collections import deque
import functools
from typing import Any, Dict, FrozenSet, Set, TextIO, Tuple, List, Optional, cast
import os
from BaseClasses import MultiWorld, Location, Item, CollectionState, \
    RegionType, Entrance, Tutorial
from Options import AssembleOptions
from .logic import cs_to_zz_locs
from .region import ZillionLocation, ZillionRegion
from .options import ZillionItemCounts, zillion_options, validate
from .item import ZillionItem, item_id_to_zz_item, item_name_to_id as _item_name_to_id
from .patch import ZillionDeltaPatch, get_base_rom_path
from .config import base_id
from zilliandomizer.patch import Patcher as ZzPatcher
from zilliandomizer.randomizer import Randomizer as ZzRandomizer
from zilliandomizer.alarms import Alarms
from zilliandomizer.logic_components.items import RESCUE, items as zz_items
from zilliandomizer.logic_components.locations import Location as ZzLocation
from zilliandomizer.low_resources.loc_id_maps import loc_to_id
from ..AutoWorld import World, WebWorld


class ZillionWebWorld(WebWorld):
    # theme = 'jungle'  # TODO: what themes are available?
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Zillion randomizer.",  # This guide covers single-player, multiworld and related software.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["beauxq"]
    )]


class ZillionWorld(World):
    """
    Zillion is a metroidvania style game released in 1987 for the 8-bit Sega Master System.

    It's based on the anime Zillion (赤い光弾ジリオン, Akai Koudan Zillion).
    """
    game = "Zillion"

    options: Dict[str, AssembleOptions] = zillion_options  # link your Options mapping
    topology_present: bool = True  # indicate if world type has any meaningful layout/pathing

    # gets automatically populated with all item and item group names
    all_item_and_group_names: FrozenSet[str] = frozenset()

    # map names to their IDs
    item_name_to_id: Dict[str, int] = _item_name_to_id
    location_name_to_id: Dict[str, int] = {
        loc: _id + base_id
        for loc, _id in loc_to_id.items()
    }
    # TODO: make this a static resource,
    # then in `generate_early`, use the dynamic resources to verify that it hasn't changed

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
    remote_start_inventory: bool = False

    # For games where after a victory it is impossible to go back in and get additional/remaining Locations checked.
    # this forces forfeit:  auto for those games.
    forced_auto_forfeit: bool = True

    # Hide World Type from various views. Does not remove functionality.
    hidden: bool = False

    zz_randomizer: ZzRandomizer
    zz_patcher: ZzPatcher

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)

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
        self.zz_patcher = ZzPatcher(rom_dir_name)
        self.zz_randomizer = ZzRandomizer(zz_op)

        # just in case the options changed anything (I don't think they do)
        for name in self.zz_randomizer.locations:
            if name != 'main':
                assert name in self.location_name_to_id, f"{name} not in location map"

    def create_regions(self) -> None:
        p = self.player
        w = self.world

        self.zz_randomizer.place_canister_gun_reqs()

        start = self.zz_randomizer.start

        all: Dict[str, ZillionRegion] = {}
        for here_name, zz_r in start.all.items():
            here_name = "Menu" if here_name == "start" else here_name
            all[here_name] = ZillionRegion(zz_r, here_name, RegionType.Generic, here_name, p, w)
            self.world.regions.append(all[here_name])

        queue = deque([start])
        done: Set[str] = set()
        while len(queue):
            zz_here = queue.popleft()
            here_name = "Menu" if zz_here.name == "start" else zz_here.name
            if here_name in done:
                continue
            here = all[here_name]

            for zz_loc in zz_here.locations:
                # if local gun reqs didn't place item
                if not zz_loc.item:

                    def access_rule_wrapped(zz_loc_local: ZzLocation,
                                            p: int,
                                            zz_r: ZzRandomizer,
                                            cs: CollectionState) -> bool:
                        # print(f"checking access to {zz_loc_local}")
                        accessible = cs_to_zz_locs(cs, p, zz_r)
                        return zz_loc_local in accessible

                    access_rule = functools.partial(access_rule_wrapped,
                                                    zz_loc, self.player, self.zz_randomizer)

                    loc = ZillionLocation(zz_loc, self.player, zz_loc.name, None, here)
                    loc.access_rule = access_rule  # type: ignore
                    here.locations.append(loc)

            for zz_dest in zz_here.connections.keys():
                dest_name = "Menu" if zz_dest.name == 'start' else zz_dest.name
                dest = all[dest_name]
                exit = Entrance(p, f"{here_name}-to-{dest_name}", here)
                here.exits.append(exit)
                exit.connect(dest)

                queue.append(zz_dest)
            done.add(here.name)

    def create_items(self) -> None:
        # in zilliandomizer, the Randomizer class puts empties in the item pool to fill space,
        # but here in AP, empties are in the options from options.validate
        item_counts = cast(ZillionItemCounts, getattr(self.world, "item_counts")[self.player])
        for zz_item in item_id_to_zz_item.values():
            if zz_item.debug_name in item_counts.value:
                count = item_counts.value[zz_item.debug_name]
                for _ in range(count):
                    self.world.itempool.append(self.create_item(zz_item.debug_name))
            elif zz_item.code == RESCUE:
                self.world.itempool.append(self.create_item(zz_item.debug_name))

    def set_rules(self) -> None:
        # logic for this game is in create_regions
        pass

    def generate_basic(self) -> None:
        # main location name is an alias
        main_loc_name = self.zz_randomizer.locations['main'].name

        self.world.get_location(main_loc_name, self.player)\
            .place_locked_item(self.create_item("main"))
        self.world.completion_condition[self.player] = \
            lambda state: state.has("main", self.player)

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
        """Optional Method that is called after regular fill. Can be used to do adjustments before output generation."""
        zz_options = self.zz_randomizer.options

        empty = zz_items[4]
        multi_item = empty  # a different patcher method differentiates empty from ap multi item
        multi_items: Dict[str, Tuple[str, str]] = {}
        for loc in self.world.get_locations():
            if loc.player == self.player:
                z_loc = cast(ZillionLocation, loc)
                if z_loc.item is None:
                    # TODO: log a warning? I think this shouldn't happen
                    z_loc.zz_loc.item = empty
                elif z_loc.item.player == self.player:
                    z_item = cast(ZillionItem, z_loc.item)
                    z_loc.zz_loc.item = z_item.zz_item
                else:  # another player's item
                    z_loc.zz_loc.item = multi_item
                    multi_items[z_loc.zz_loc.name] = (
                        z_loc.item.name,
                        self.world.get_player_name(z_loc.item.player)
                    )

        # verify that every location got an item
        for zz_loc in self.zz_randomizer.locations.values():
            assert zz_loc.item, f"not every location in world {self.player} got an item"

        if zz_options.randomize_alarms:
            a = Alarms(self.zz_patcher.tc, self.zz_randomizer.logger)
            a.choose_all()

        self.zz_patcher.write_locations(self.zz_randomizer.locations, zz_options.start_char)
        self.zz_patcher.all_fixes_and_options(zz_options)
        self.zz_patcher.set_external_item_interface(zz_options.start_char, zz_options.max_level)
        self.zz_patcher.set_multiworld_items(multi_items)

    def generate_output(self, output_directory: str) -> None:
        """This method gets called from a threadpool, do not use world.random here.
        If you need any last-second randomization, use MultiWorld.slot_seeds[slot] instead."""
        # original_rom_bytes = self.zz_patcher.rom
        patched_rom_bytes = self.zz_patcher.get_patched_bytes()

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
        item_id = _item_name_to_id[name]
        zz_item = item_id_to_zz_item[item_id]
        prog = zz_item.is_progression or zz_item.required
        skip_in_prog_bal = not zz_item.is_progression

        # for the rescue hint text
        start_char = self.zz_randomizer.options.start_char

        z_item = ZillionItem(name, prog, item_id, self.player, start_char)
        z_item.skip_in_prog_balancing = skip_in_prog_bal
        return z_item

    def get_filler_item_name(self) -> str:
        """Called when the item pool needs to be filled with additional items to match location count."""
        return "empty"

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
