from collections import deque, Counter
from contextlib import redirect_stdout
import functools
import settings
import threading
import typing
from typing import Any, Dict, List, Literal, Set, Tuple, Optional, cast
import os
import logging

from BaseClasses import ItemClassification, LocationProgressType, \
    MultiWorld, Item, CollectionState, Entrance, Tutorial
from .logic import cs_to_zz_locs
from .region import ZillionLocation, ZillionRegion
from .options import ZillionOptions, ZillionStartChar, validate
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


class ZillionSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Zillion US rom"""
        description = "Zillion US ROM File"
        copy_to = "Zillion (UE) [!].sms"
        assert ZillionDeltaPatch.hash
        md5s = [ZillionDeltaPatch.hash]

    class RomStart(str):
        """
        Set this to false to never autostart a rom (such as after patching)
        True for operating system default program
        Alternatively, a path to a program to open the .sfc file with
        RetroArch doesn't make it easy to launch a game from the command line.
        You have to know the path to the emulator core library on the user's computer.
        """

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: typing.Union[RomStart, bool] = RomStart("retroarch")


class ZillionWebWorld(WebWorld):
    theme = "stone"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Zillion randomizer.",
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

    options_dataclass = ZillionOptions
    options: ZillionOptions  # type: ignore

    settings: typing.ClassVar[ZillionSettings]  # type: ignore
    # these type: ignore are because of this issue: https://github.com/python/typing/discussions/1486

    topology_present = True  # indicate if world type has any meaningful layout/pathing

    # map names to their IDs
    item_name_to_id = _item_name_to_id
    location_name_to_id = _loc_name_to_id

    # increment this every time something in your world's names/id mappings changes.
    # While this is set to 0 in *any* AutoWorld, the entire DataPackage is considered in testing mode and will be
    # retrieved by clients on every connection.
    data_version = 1

    logger: logging.Logger

    class LogStreamInterface:
        logger: logging.Logger
        buffer: List[str]

        def __init__(self, logger: logging.Logger) -> None:
            self.logger = logger
            self.buffer = []

        def write(self, msg: str) -> None:
            if msg.endswith('\n'):
                self.buffer.append(msg[:-1])
                self.logger.debug("".join(self.buffer))
                self.buffer = []
            else:
                self.buffer.append(msg)

        def flush(self) -> None:
            pass

    lsi: LogStreamInterface

    id_to_zz_item: Optional[Dict[int, ZzItem]] = None
    zz_system: System
    _item_counts: "Counter[str]" = Counter()
    """
    These are the items counts that will be in the game,
    which might be different from the item counts the player asked for in options
    (if the player asked for something invalid).
    """
    my_locations: List[ZillionLocation] = []
    """ This is kind of a cache to avoid iterating through all the multiworld locations in logic. """
    slot_data_ready: threading.Event
    """ This event is set in `generate_output` when the data is ready for `fill_slot_data` """

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.logger = logging.getLogger("Zillion")
        self.lsi = ZillionWorld.LogStreamInterface(self.logger)
        self.zz_system = System()
        self.slot_data_ready = threading.Event()

    def _make_item_maps(self, start_char: Chars) -> None:
        _id_to_name, _id_to_zz_id, id_to_zz_item = make_id_to_others(start_char)
        self.id_to_zz_item = id_to_zz_item

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        """Checks that a game is capable of generating, usually checks for some base file like a ROM.
        Not run for unittests since they don't produce output"""
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def generate_early(self) -> None:
        if not hasattr(self.multiworld, "zillion_logic_cache"):
            setattr(self.multiworld, "zillion_logic_cache", {})

        zz_op, item_counts = validate(self.options)

        if zz_op.early_scope:
            self.multiworld.early_items[self.player]["Scope"] = 1

        self._item_counts = item_counts

        with redirect_stdout(self.lsi):  # type: ignore
            self.zz_system.make_randomizer(zz_op)

            self.zz_system.seed(self.multiworld.seed)
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
        w = self.multiworld
        self.my_locations = []

        self.zz_system.randomizer.place_canister_gun_reqs()
        # low probability that place_canister_gun_reqs() results in empty 1st sphere
        # testing code to force low probability event:
        # for zz_room_name in ["r01c2", "r02c0", "r02c7", "r03c5"]:
        #     for zz_loc in self.zz_system.randomizer.regions[zz_room_name].locations:
        #         zz_loc.req.gun = 2
        if len(self.zz_system.randomizer.get_locations(Req(gun=1, jump=1))) == 0:
            self.logger.info("Zillion avoided rare empty 1st sphere.")
            for zz_loc in self.zz_system.randomizer.regions["r03c5"].locations:
                zz_loc.req.gun = 1
            assert len(self.zz_system.randomizer.get_locations(Req(gun=1, jump=1))) != 0

        start = self.zz_system.randomizer.regions['start']

        all: Dict[str, ZillionRegion] = {}
        for here_zz_name, zz_r in self.zz_system.randomizer.regions.items():
            here_name = "Menu" if here_zz_name == "start" else zz_reg_name_to_reg_name(here_zz_name)
            all[here_name] = ZillionRegion(zz_r, here_name, here_name, p, w)
            self.multiworld.regions.append(all[here_name])

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
                # if local gun reqs didn't place "keyword" item
                if not zz_loc.item:

                    def access_rule_wrapped(zz_loc_local: ZzLocation,
                                            p: int,
                                            zz_r: ZzRandomizer,
                                            id_to_zz_item: Dict[int, ZzItem],
                                            cs: CollectionState) -> bool:
                        accessible = cs_to_zz_locs(cs, p, zz_r, id_to_zz_item)
                        return zz_loc_local in accessible

                    access_rule = functools.partial(access_rule_wrapped,
                                                    zz_loc, self.player, self.zz_system.randomizer, self.id_to_zz_item)

                    loc_name = self.zz_system.randomizer.loc_name_2_pretty[zz_loc.name]
                    loc = ZillionLocation(zz_loc, self.player, loc_name, here)
                    loc.access_rule = access_rule
                    if not (limited_skill >= zz_loc.req):
                        loc.progress_type = LocationProgressType.EXCLUDED
                        self.multiworld.exclude_locations[p].value.add(loc.name)
                    here.locations.append(loc)
                    self.my_locations.append(loc)

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
        item_counts = self._item_counts
        self.logger.debug(item_counts)

        for item_name, item_id in self.item_name_to_id.items():
            zz_item = self.id_to_zz_item[item_id]
            if item_id >= (4 + base_id):  # normal item
                if item_name in item_counts:
                    count = item_counts[item_name]
                    self.logger.debug(f"Zillion Items: {item_name}  {count}")
                    self.multiworld.itempool += [self.create_item(item_name) for _ in range(count)]
            elif item_id < (3 + base_id) and zz_item.code == RESCUE:
                # One of the 3 rescues will not be in the pool and its zz_item will be 'empty'.
                self.logger.debug(f"Zillion Items: {item_name}  1")
                self.multiworld.itempool.append(self.create_item(item_name))

    def set_rules(self) -> None:
        # logic for this game is in create_regions
        pass

    def generate_basic(self) -> None:
        assert self.zz_system.randomizer, "generate_early hasn't been called"
        # main location name is an alias
        main_loc_name = self.zz_system.randomizer.loc_name_2_pretty[self.zz_system.randomizer.locations['main'].name]

        self.multiworld.get_location(main_loc_name, self.player)\
            .place_locked_item(self.create_item("Win"))
        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has("Win", self.player)

    @staticmethod
    def stage_generate_basic(multiworld: MultiWorld, *args: Any) -> None:
        # item link pools are about to be created in main
        # JJ can't be an item link unless all the players share the same start_char
        # (The reason for this is that the JJ ZillionItem will have a different ZzItem depending
        #  on whether the start char is Apple or Champ, and the logic depends on that ZzItem.)
        for group in multiworld.groups.values():
            # TODO: remove asserts on group when we can specify which members of TypedDict are optional
            assert "game" in group
            if group["game"] == "Zillion":
                assert "item_pool" in group
                item_pool = group["item_pool"]
                to_stay: Literal['Apple', 'Champ', 'JJ'] = "JJ"
                if "JJ" in item_pool:
                    assert "players" in group
                    group_players = group["players"]
                    start_chars = cast(Dict[int, ZillionStartChar], getattr(multiworld, "start_char"))
                    players_start_chars = [
                        (player, start_chars[player].current_option_name)
                        for player in group_players
                    ]
                    start_char_counts = Counter(sc for _, sc in players_start_chars)
                    # majority rules
                    if start_char_counts["Apple"] > start_char_counts["Champ"]:
                        to_stay = "Apple"
                    elif start_char_counts["Champ"] > start_char_counts["Apple"]:
                        to_stay = "Champ"
                    else:  # equal
                        choices: Tuple[Literal['Apple', 'Champ', 'JJ'], ...] = ("Apple", "Champ")
                        to_stay = multiworld.random.choice(choices)

                    for p, sc in players_start_chars:
                        if sc != to_stay:
                            group_players.remove(p)
                assert "world" in group
                cast(ZillionWorld, group["world"])._make_item_maps(to_stay)

    def post_fill(self) -> None:
        """Optional Method that is called after regular fill. Can be used to do adjustments before output generation.
        This happens before progression balancing,  so the items may not be in their final locations yet."""

        self.zz_system.post_fill()

    def finalize_item_locations(self) -> None:
        """
        sync zilliandomizer item locations with AP item locations
        """
        rom_dir_name = os.path.dirname(get_base_rom_path())
        self.zz_system.make_patcher(rom_dir_name)
        assert self.zz_system.randomizer and self.zz_system.patcher, "generate_early hasn't been called"
        zz_options = self.zz_system.randomizer.options

        # debug_zz_loc_ids: Dict[str, int] = {}
        empty = zz_items[4]
        multi_item = empty  # a different patcher method differentiates empty from ap multi item
        multi_items: Dict[str, Tuple[str, str]] = {}  # zz_loc_name to (item_name, player_name)
        for loc in self.multiworld.get_locations(self.player):
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
                    self.multiworld.get_player_name(z_loc.item.player)
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

        zz_patcher.write_locations(self.zz_system.randomizer.regions,
                                   zz_options.start_char,
                                   self.zz_system.randomizer.loc_name_2_pretty)
        self.slot_data_ready.set()
        rm = self.zz_system.resource_managers
        assert rm, "missing resource_managers from generate_early"
        zz_patcher.all_fixes_and_options(zz_options, rm)
        zz_patcher.set_external_item_interface(zz_options.start_char, zz_options.max_level)
        zz_patcher.set_multiworld_items(multi_items)
        game_id = self.multiworld.player_name[self.player].encode() + b'\x00' + self.multiworld.seed_name[-6:].encode()
        zz_patcher.set_rom_to_ram_data(game_id)

    def generate_output(self, output_directory: str) -> None:
        """This method gets called from a threadpool, do not use world.random here.
        If you need any last-second randomization, use MultiWorld.per_slot_randoms[slot] instead."""
        self.finalize_item_locations()

        assert self.zz_system.patcher, "didn't get patcher from finalize_item_locations"
        # original_rom_bytes = self.zz_patcher.rom
        patched_rom_bytes = self.zz_system.patcher.get_patched_bytes()

        out_file_base = self.multiworld.get_out_file_name_base(self.player)

        filename = os.path.join(
            output_directory,
            f'{out_file_base}{ZillionDeltaPatch.result_file_ending}'
        )
        with open(filename, "wb") as binary_file:
            binary_file.write(patched_rom_bytes)
        patch = ZillionDeltaPatch(
            os.path.splitext(filename)[0] + ZillionDeltaPatch.patch_file_ending,
            player=self.player,
            player_name=self.multiworld.player_name[self.player],
            patched_path=filename
        )
        patch.write()
        os.remove(filename)

    def fill_slot_data(self) -> Dict[str, Any]:  # json of WebHostLib.models.Slot
        """Fill in the `slot_data` field in the `Connected` network package.
        This is a way the generator can give custom data to the client.
        The client will receive this as JSON in the `Connected` response."""

        # TODO: share a TypedDict data structure with client

        # TODO: tell client which canisters are keywords
        # so it can open and get those when restoring doors

        assert self.zz_system.randomizer, "didn't get randomizer from generate_early"

        rescues: Dict[str, Any] = {}
        self.slot_data_ready.wait()
        zz_patcher = self.zz_system.patcher
        assert zz_patcher, "didn't get patcher from generate_output"
        for i in (0, 1):
            if i in zz_patcher.rescue_locations:
                ri = zz_patcher.rescue_locations[i]
                rescues[str(i)] = {
                    "start_char": ri.start_char,
                    "room_code": ri.room_code,
                    "mask": ri.mask
                }
        return {
            "start_char": self.zz_system.randomizer.options.start_char,
            "rescues": rescues,
            "loc_mem_to_id": zz_patcher.loc_memory_to_loc_id
        }

    # def modify_multidata(self, multidata: Dict[str, Any]) -> None:
    #     """For deeper modification of server multidata."""
    #     # not modifying multidata, just want to call this at the end of the generation process
    #     cache = getattr(self.multiworld, "zillion_logic_cache")
    #     import sys
    #     print(sys.getsizeof(cache))

    # end of ordered Main.py calls

    def create_item(self, name: str) -> Item:
        """Create an item for this world type and player.
        Warning: this may be called with self.multiworld = None, for example by MultiServer"""
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
