from collections import deque, Counter
from contextlib import redirect_stdout
import functools
import settings
import threading
from typing import Any, ClassVar
import os
import logging

from typing_extensions import override

from BaseClasses import LocationProgressType, MultiWorld, Item, CollectionState, Entrance, Tutorial

from .gen_data import GenData
from .logic import ZillionLogicCache
from .region import ZillionLocation, ZillionRegion
from .options import ZillionOptions, validate, z_option_groups
from .id_maps import ZillionSlotInfo, get_slot_info, item_name_to_id as _item_name_to_id, \
    loc_name_to_id as _loc_name_to_id, make_id_to_others, \
    zz_reg_name_to_reg_name, base_id
from .item import ZillionItem, get_classification
from .patch import ZillionPatch

from zilliandomizer.system import System
from zilliandomizer.logic_components.items import RESCUE, items as zz_items, Item as ZzItem
from zilliandomizer.logic_components.locations import Location as ZzLocation, Req
from zilliandomizer.map_gen.region_maker import DEAD_END_SUFFIX
from zilliandomizer.options import Chars

from worlds.AutoWorld import World, WebWorld


class ZillionSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Zillion US rom"""
        description = "Zillion US ROM File"
        copy_to = "Zillion (UE) [!].sms"
        assert ZillionPatch.hash
        md5s = [ZillionPatch.hash]

    class RomStart(str):
        """
        Set this to false to never autostart a rom (such as after patching)
        True for operating system default program
        Alternatively, a path to a program to open the .sfc file with
        RetroArch doesn't make it easy to launch a game from the command line.
        You have to know the path to the emulator core library on the user's computer.
        """

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: RomStart | bool = RomStart("retroarch")


class ZillionWebWorld(WebWorld):
    theme = "stone"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Zillion randomizer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["beauxq"],
    )]

    option_groups = z_option_groups


class ZillionWorld(World):
    """
    Zillion is a metroidvania style game released in 1987 for the 8-bit Sega Master System.

    It's based on the anime Zillion (赤い光弾ジリオン, Akai Koudan Zillion).
    """
    game = "Zillion"
    web = ZillionWebWorld()

    options_dataclass = ZillionOptions
    options: ZillionOptions  # type: ignore

    settings: ClassVar[ZillionSettings]  # type: ignore
    # these type: ignore are because of this issue: https://github.com/python/typing/discussions/1486

    topology_present = True  # indicate if world type has any meaningful layout/pathing

    # map names to their IDs
    item_name_to_id = _item_name_to_id
    location_name_to_id = _loc_name_to_id

    logger: logging.Logger

    class LogStreamInterface:
        logger: logging.Logger
        buffer: list[str]

        def __init__(self, logger: logging.Logger) -> None:
            self.logger = logger
            self.buffer = []

        def write(self, msg: str) -> None:
            if msg.endswith("\n"):
                self.buffer.append(msg[:-1])
                self.logger.debug("".join(self.buffer))
                self.buffer = []
            else:
                self.buffer.append(msg)

        def flush(self) -> None:
            pass

    lsi: LogStreamInterface

    id_to_zz_item: dict[int, ZzItem] | None = None
    zz_system: System
    _item_counts: Counter[str] = Counter()
    """
    These are the items counts that will be in the game,
    which might be different from the item counts the player asked for in options
    (if the player asked for something invalid).
    """
    my_locations: list[ZillionLocation] = []
    """ This is kind of a cache to avoid iterating through all the multiworld locations in logic. """
    finalized_gen_data: GenData | None
    """ Finalized generation data needed by `generate_output` and by `fill_slot_data`. """
    item_locations_finalization_lock: threading.Lock
    """
    This lock is used in `generate_output` and `fill_slot_data` to ensure synchronized access to `finalized_gen_data`,
    so that whichever is run first can finalize the item locations while the other waits.
    """
    logic_cache: ZillionLogicCache | None = None

    def __init__(self, world: MultiWorld, player: int) -> None:
        super().__init__(world, player)
        self.logger = logging.getLogger("Zillion")
        self.lsi = ZillionWorld.LogStreamInterface(self.logger)
        self.zz_system = System()
        self.finalized_gen_data = None
        self.item_locations_finalization_lock = threading.Lock()

    def _make_item_maps(self, start_char: Chars) -> None:
        _id_to_name, _id_to_zz_id, id_to_zz_item = make_id_to_others(start_char)
        self.id_to_zz_item = id_to_zz_item

    @override
    def generate_early(self) -> None:
        zz_op, item_counts = validate(self.options)

        if zz_op.early_scope:
            self.multiworld.early_items[self.player]["Scope"] = 1

        self._item_counts = item_counts

        with redirect_stdout(self.lsi):  # type: ignore
            self.zz_system.set_options(zz_op)
            self.zz_system.seed(self.random.randrange(1999999999))
            self.zz_system.make_map()
            self.zz_system.make_randomizer()

        # just in case the options changed anything (I don't think they do)
        assert self.zz_system.randomizer, "init failed"
        for zz_name in self.zz_system.randomizer.locations:
            if zz_name != "main":
                assert self.zz_system.randomizer.loc_name_2_pretty[zz_name] in self.location_name_to_id, \
                    f"{self.zz_system.randomizer.loc_name_2_pretty[zz_name]} not in location map"

        self._make_item_maps(zz_op.start_char)

    @override
    def create_regions(self) -> None:
        assert self.zz_system.randomizer, "generate_early hasn't been called"
        assert self.id_to_zz_item, "generate_early hasn't been called"
        player = self.player
        logic_cache = ZillionLogicCache(player, self.zz_system.randomizer, self.id_to_zz_item)
        self.logic_cache = logic_cache
        w = self.multiworld
        self.my_locations = []
        dead_end_locations: list[ZillionLocation] = []

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

        start = self.zz_system.randomizer.regions["start"]

        all_regions: dict[str, ZillionRegion] = {}
        for here_zz_name, zz_r in self.zz_system.randomizer.regions.items():
            here_name = "Menu" if here_zz_name == "start" else zz_reg_name_to_reg_name(here_zz_name)
            all_regions[here_name] = ZillionRegion(zz_r, here_name, here_name, player, w)
            self.multiworld.regions.append(all_regions[here_name])

        limited_skill = Req(gun=3, jump=3, skill=self.zz_system.randomizer.options.skill, hp=940, red=1, floppy=126)
        queue = deque([start])
        done: set[str] = set()
        while len(queue):
            zz_here = queue.popleft()
            here_name = "Menu" if zz_here.name == "start" else zz_reg_name_to_reg_name(zz_here.name)
            if here_name in done:
                continue
            here = all_regions[here_name]

            for zz_loc in zz_here.locations:
                # if local gun reqs didn't place "keyword" item
                if not zz_loc.item:

                    def access_rule_wrapped(zz_loc_local: ZzLocation,
                                            lc: ZillionLogicCache,
                                            cs: CollectionState) -> bool:
                        accessible = lc.cs_to_zz_locs(cs)
                        return zz_loc_local in accessible

                    access_rule = functools.partial(access_rule_wrapped, zz_loc, logic_cache)

                    loc_name = self.zz_system.randomizer.loc_name_2_pretty[zz_loc.name]
                    loc = ZillionLocation(zz_loc, self.player, loc_name, here)
                    loc.access_rule = access_rule
                    if not (limited_skill >= zz_loc.req):
                        loc.progress_type = LocationProgressType.EXCLUDED
                        self.options.exclude_locations.value.add(loc.name)
                    here.locations.append(loc)
                    self.my_locations.append(loc)

                    if ((
                        zz_here.name.endswith(DEAD_END_SUFFIX)
                    ) or (
                        (self.options.map_gen.value != self.options.map_gen.option_full) and
                        (loc.name in self.options.priority_dead_ends.vanilla_dead_ends)
                    ) or (
                        loc.name in self.options.priority_dead_ends.always_dead_ends
                    )):
                        dead_end_locations.append(loc)

            for zz_dest in zz_here.connections.keys():
                dest_name = "Menu" if zz_dest.name == "start" else zz_reg_name_to_reg_name(zz_dest.name)
                dest = all_regions[dest_name]
                exit_ = Entrance(player, f"{here_name} to {dest_name}", here)
                here.exits.append(exit_)
                exit_.connect(dest)

                queue.append(zz_dest)
            done.add(here.name)
        if self.options.priority_dead_ends.value:
            self.options.priority_locations.value |= {loc.name for loc in dead_end_locations}

        # main location name is an alias
        main_loc_name = self.zz_system.randomizer.loc_name_2_pretty[self.zz_system.randomizer.locations["main"].name]
        self.multiworld.get_location(main_loc_name, player).place_locked_item(self.create_item("Win"))
        self.multiworld.completion_condition[player] = lambda state: state.has("Win", player)

    @override
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

    @staticmethod
    def stage_generate_basic(multiworld: MultiWorld, *args: Any) -> None:  # noqa: ANN401
        # item link pools are about to be created in main
        # JJ can't be an item link unless all the players share the same start_char
        # (The reason for this is that the JJ ZillionItem will have a different ZzItem depending
        #  on whether the start char is Apple or Champ, and the logic depends on that ZzItem.)
        for group in multiworld.groups.values():
            if group["game"] == "Zillion" and "item_pool" in group:
                item_pool = group["item_pool"]
                to_stay: Chars = "JJ"
                if "JJ" in item_pool:
                    group["players"] = group_players = set(group["players"])
                    players_start_chars: list[tuple[int, Chars]] = []
                    for player in group_players:
                        z_world = multiworld.worlds[player]
                        assert isinstance(z_world, ZillionWorld)
                        players_start_chars.append((player, z_world.options.start_char.get_char()))
                    start_char_counts = Counter(sc for _, sc in players_start_chars)
                    # majority rules
                    if start_char_counts["Apple"] > start_char_counts["Champ"]:
                        to_stay = "Apple"
                    elif start_char_counts["Champ"] > start_char_counts["Apple"]:
                        to_stay = "Champ"
                    else:  # equal
                        choices: tuple[Chars, ...] = ("Apple", "Champ")
                        to_stay = multiworld.random.choice(choices)

                    for p, sc in players_start_chars:
                        if sc != to_stay:
                            group_players.remove(p)
                group_world = group["world"]
                assert isinstance(group_world, ZillionWorld)
                group_world._make_item_maps(to_stay)

    @override
    def post_fill(self) -> None:
        """Optional Method that is called after regular fill. Can be used to do adjustments before output generation.
        This happens before progression balancing,  so the items may not be in their final locations yet."""

        self.zz_system.post_fill()

    def finalize_item_locations_thread_safe(self) -> GenData:
        """
        Call self.finalize_item_locations() and cache the result in a thread-safe manner so that either
        `generate_output` or `fill_slot_data` can finalize item locations without concern for which of the two functions
        is called first.
        """
        # The lock is acquired when entering the context manager and released when exiting the context manager.
        with self.item_locations_finalization_lock:
            # If generation data has yet to be finalized, finalize it.
            if self.finalized_gen_data is None:
                self.finalized_gen_data = self.finalize_item_locations()
        return self.finalized_gen_data

    def finalize_item_locations(self) -> GenData:
        """
        sync zilliandomizer item locations with AP item locations

        return the data needed to generate output
        """

        assert self.zz_system.randomizer, "generate_early hasn't been called"

        # debug_zz_loc_ids: dict[str, int] = {}
        empty = zz_items[4]
        multi_item = empty  # a different patcher method differentiates empty from ap multi item
        multi_items: dict[str, tuple[str, str]] = {}  # zz_loc_name to (item_name, player_name)
        for z_loc in self.multiworld.get_locations(self.player):
            assert isinstance(z_loc, ZillionLocation)
            # debug_zz_loc_ids[z_loc.zz_loc.name] = id(z_loc.zz_loc)
            if z_loc.item is None:
                self.logger.warning("generate_output location has no item - is that ok?")
                z_loc.zz_loc.item = empty
            elif z_loc.item.player == self.player:
                z_item = z_loc.item
                assert isinstance(z_item, ZillionItem)
                z_loc.zz_loc.item = z_item.zz_item
            else:  # another player's item
                # print(f"put multi item in {z_loc.zz_loc.name}")
                z_loc.zz_loc.item = multi_item
                multi_items[z_loc.zz_loc.name] = (
                    z_loc.item.name,
                    self.multiworld.get_player_name(z_loc.item.player),
                )
        # debug_zz_loc_ids.sort()
        # for name, id_ in debug_zz_loc_ids.items():
        #     print(id_)
        # print("size:", len(debug_zz_loc_ids))

        # debug_loc_to_id: dict[str, int] = {}
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

        game_id = self.multiworld.player_name[self.player].encode() + b"\x00" + self.multiworld.seed_name[-6:].encode()

        return GenData(multi_items, self.zz_system.get_game(), game_id)

    @override
    def generate_output(self, output_directory: str) -> None:
        """This method gets called from a threadpool, do not use multiworld.random here.
        If you need any last-second randomization, use self.random instead."""
        gen_data = self.finalize_item_locations_thread_safe()

        out_file_base = self.multiworld.get_out_file_name_base(self.player)

        patch_file_name = os.path.join(output_directory, f"{out_file_base}{ZillionPatch.patch_file_ending}")
        patch = ZillionPatch(patch_file_name,
                             player=self.player,
                             player_name=self.multiworld.player_name[self.player],
                             gen_data_str=gen_data.to_json())
        patch.write()

        self.logger.debug(f"Zillion player {self.player} finished generate_output")

    @override
    def fill_slot_data(self) -> ZillionSlotInfo:  # json of WebHostLib.models.Slot
        """Fill in the `slot_data` field in the `Connected` network package.
        This is a way the generator can give custom data to the client.
        The client will receive this as JSON in the `Connected` response."""

        # TODO: share a TypedDict data structure with client

        # TODO: tell client which canisters are keywords
        # so it can open and get those when restoring doors

        game = self.finalize_item_locations_thread_safe().zz_game
        return get_slot_info(game.regions, game.char_order[0], game.loc_name_2_pretty)

    # end of ordered Main.py calls

    @override
    def create_item(self, name: str) -> Item:
        """Create an item for this world type and player.
        Warning: this may be called with self.multiworld = None, for example by MultiServer"""
        item_id = _item_name_to_id[name]

        if not self.id_to_zz_item:
            self._make_item_maps("JJ")
            self.logger.warning("warning: called `create_item` without calling `generate_early` first")
        assert self.id_to_zz_item, "failed to get item maps"

        zz_item = self.id_to_zz_item[item_id]
        classification = get_classification(name, zz_item, self._item_counts)

        z_item = ZillionItem(name, classification, item_id, self.player, zz_item)
        return z_item

    @override
    def get_filler_item_name(self) -> str:
        """Called when the item pool needs to be filled with additional items to match location count."""
        return "Empty"
