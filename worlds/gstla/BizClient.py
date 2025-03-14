from __future__ import annotations

import base64
from collections import defaultdict
import logging
from enum import IntEnum, Enum
from typing import Dict, List, TYPE_CHECKING, Set, Tuple, Mapping, Optional

from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient
from worlds._bizhawk import read, write, guarded_write
from .gen.LocationNames import loc_names_by_id
from .gen.ItemData import djinn_items, mimics, ItemData
from .gen.LocationData import all_locations, LocationType, djinn_locations

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext, BizHawkClientCommandProcessor

logger = logging.getLogger("Client")

FLAG_START = 0x40
FORCE_ENCOUNTER_ADDR = 0x30164
PREVENT_FLEEING_ADDR = 0x48B
IN_BATTLE_ADDR = 0x60


class _MemDomain(str, Enum):
    EWRAM = 'EWRAM'
    ROM = 'ROM'


class _DataLocations(IntEnum):
    IN_GAME = (0x428, 0x2, 0x0, _MemDomain.EWRAM)
    DJINN_FLAGS = (FLAG_START + (0x30 >> 3), 0x0A, 0x30, _MemDomain.EWRAM)
    AP_ITEM_SLOT = (0xA96, 0x2, 0x0, _MemDomain.EWRAM)
    # two unused bytes in save data
    AP_ITEMS_RECEIVED = (0xA72, 0x2, 0x0, _MemDomain.EWRAM)
    INITIAL_INVENTORY = (FLAG_START + 0x0, 0x1, 0x0, _MemDomain.EWRAM)
    SUMMONS = (FLAG_START + (0x10 >> 3), 0x2, 0x10, _MemDomain.EWRAM)
    TREASURE_8_FLAGS = (FLAG_START + (0x800 >> 3), 0x20, 0x800, _MemDomain.EWRAM)
    TREASURE_9_FLAGS = (FLAG_START + (0x900 >> 3), 0x20, 0x900, _MemDomain.EWRAM)
    TREASURE_A_FLAGS = (FLAG_START + (0xA00 >> 3), 0x20, 0xA00, _MemDomain.EWRAM)
    TREASURE_B_FLAGS = (FLAG_START + (0xB00 >> 3), 0x20, 0xB00, _MemDomain.EWRAM)
    TREASURE_C_FLAGS = (FLAG_START + (0xC00 >> 3), 0x20, 0xC00, _MemDomain.EWRAM)
    TREASURE_D_FLAGS = (FLAG_START + (0xD00 >> 3), 0x20, 0xD00, _MemDomain.EWRAM)
    TREASURE_E_FLAGS = (FLAG_START + (0xE00 >> 3), 0x20, 0xE00, _MemDomain.EWRAM)
    TREASURE_F_FLAGS = (FLAG_START + (0xF00 >> 3), 0x20, 0xF00, _MemDomain.EWRAM)
    DOOM_DRAGON = (FLAG_START + (0x778 >> 3), 0x1, 0x778, _MemDomain.EWRAM)

    def __new__(cls, addr: int, length: int, initial_flag: int, domain: _MemDomain):
        value = len(cls.__members__)
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.addr = addr
        obj.length = length
        obj.initial_flag = initial_flag
        obj.domain = domain
        return obj

    def to_request(self) -> Tuple[int, int, _MemDomain]:
        return self.addr, self.length, self.domain


def _handle_common_cmd(self: 'BizHawkClientCommandProcessor') -> Optional[GSTLAClient]:
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Golden Sun The Lost Age":
        logger.warning("This command can only be used when playing GSTLA")
        return None

    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command")
        return None
    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, GSTLAClient)
    return client


def cmd_unchecked_djinn(self: 'BizHawkClientCommandProcessor') -> None:
    """Prints djinn locations that have not yet been checked"""
    client = _handle_common_cmd(self)
    if client is None:
        return
    for djinn in djinn_locations:
        djinn_name = loc_names_by_id[djinn.id]
        if djinn_name not in client.checked_djinn:
            logger.info(djinn_name)


def cmd_checked_djinn(self: 'BizHawkClientCommandProcessor') -> None:
    """Prints djinn locations that have been checked"""
    client = _handle_common_cmd(self)
    if client is None:
        return
    for djinn in client.checked_djinn:
        logger.info(djinn)


commands = [
    ("unchecked_djinn", cmd_unchecked_djinn),
    ("djinn", cmd_checked_djinn)
]


class StartingItemHandler:

    def __init__(self, starting_data: Mapping[str, int]):
        self.starting_data = []
        self.count = sum(starting_data.values())

        keys = list(starting_data.keys())
        keys.sort()

        for key in keys:
            c = starting_data[key]
            for i in range(c):
                self.starting_data.append(int(key))
        logger.debug("Starting data: %s", self.starting_data)
        logger.debug("Starting count: %s", self.count)

    def __getitem__(self, n: int):
        return self.starting_data[n]


class GSTLAClient(BizHawkClient):
    game = 'Golden Sun The Lost Age'
    system = 'GBA'
    patch_suffix = '.apgstla'

    def __init__(self):
        super().__init__()
        self.slot_name = ''
        self.flag_map: defaultdict[int, Set[int]] = defaultdict(lambda: set())
        self.djinn_ram_to_rom: Dict[int, int] = dict()
        self.djinn_flag_map: Dict[int, str] = dict()
        self.checked_djinn: Set[str] = set()
        self.mimics = {x.id: x for x in mimics}
        for loc in all_locations:
            if loc.loc_type == LocationType.Event:
                continue
            self.flag_map[loc.flag].add(loc.ap_id)
            if loc.loc_type == LocationType.Djinn:
                self.djinn_flag_map[loc.flag] = loc_names_by_id[loc.addresses[0]]
        self.temp_locs: Set[int] = set()
        self.local_locations: Set[int] = set()
        self.starting_items: StartingItemHandler = StartingItemHandler(dict())
        self.was_in_game: bool = False

    async def validate_rom(self, ctx: 'BizHawkClientContext'):
        game_name = await read(ctx.bizhawk_ctx, [(0xA0, 0x12, _MemDomain.ROM)])
        game_name = game_name[0].decode('ascii')
        logger.debug("Game loaded: %s", game_name)
        if game_name != 'GOLDEN_SUN_BAGFE01':
            for cmd, _ in commands:
                if cmd in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop(cmd)
            return False
        ctx.game = self.game
        # TODO: would like to verify that the ROM is the correct one somehow
        # Possibly verify the seed; would also be nice to have the slot name encoded
        # in the rom somewhere, though not necessary
        slot_name = await read(ctx.bizhawk_ctx, [(0xFFF000, 64, _MemDomain.ROM)])
        if not slot_name:
            logger.warning("Could not find slot name in GSTLA ROM; please double check the ROM is correct")
        else:
            self.slot_name = base64.b64decode(slot_name[0].rstrip(b'\x00'), validate=True).decode('utf-8').strip()
        for cmd, func in commands:
            if cmd not in ctx.command_processor.commands:
                ctx.command_processor.commands[cmd] = func
        ctx.items_handling = 0b001
        ctx.watcher_timeout = 1  # not sure what a reasonable setting here is; passed to asyncio.wait_for
        return True

    async def set_auth(self, ctx: 'BizHawkClientContext') -> None:
        if self.slot_name:
            ctx.auth = self.slot_name

    async def _load_djinn(self, ctx: 'BizHawkClientContext') -> None:
        if len(self.djinn_ram_to_rom) > 0:
            return
        # Don't put this in the data locations class; we don't want to check this regularly
        result = await read(ctx.bizhawk_ctx, [(0xFA0000, 0x2 * 18 * 4, _MemDomain.ROM)])
        for index in range(18 * 4):
            djinn_flag = (index // 18) * 20 + (index % 18) + _DataLocations.DJINN_FLAGS.initial_flag
            section = int.from_bytes(result[0][index * 2:(index * 2) + 2], 'little')
            rom_flag = (section >> 8) * 0x14 + (section & 0xFF) + 0x30
            self.djinn_ram_to_rom[rom_flag] = djinn_flag

    def _is_in_game(self, data: List[bytes]) -> bool:
        # What the emo tracker pack does; seems like it also verifies the player
        # has opened a save file
        flag = int.from_bytes(data[_DataLocations.IN_GAME], 'little')
        return flag > 1

    def _check_djinn_flags(self, data: List[bytes]) -> None:
        flag_bytes = data[_DataLocations.DJINN_FLAGS]
        for i in range(0, _DataLocations.DJINN_FLAGS.length, 2):
            part = flag_bytes[i:i + 2]
            part_int = int.from_bytes(part, "little")
            # logger.info(part_int)
            for bit in range(16):
                if part_int & 1 > 0:
                    flag = i * 8 + bit
                    # original_flag = flag + _DataLocations.DJINN_FLAGS.initial_flag
                    shuffled_flag = self.djinn_ram_to_rom[flag + _DataLocations.DJINN_FLAGS.initial_flag]
                    # original_djinn = self.djinn_flag_map[original_flag]
                    # shuffled_djinn = self.djinn_flag_map[shuffled_flag]
                    # TODO: this may be wrong once djinn are events
                    # logger.debug("RAM Djinn: %s, Flag: %s -> ROM Djinn: %s, Flag: %s",
                    #              original_djinn, hex(original_flag), shuffled_djinn, hex(shuffled_flag))
                    self.checked_djinn.add(self.djinn_flag_map[shuffled_flag])
                    # TODO: if djinn ever become proper items this code would be needed
                    # locs = self.flag_map.get(shuffled_flag, None)
                    # # logger.debug("orig_flag: %s, shuffle flag: %s, locs: %s", hex(flag), hex(shuffled_flag), locs)
                    # assert locs is not None, "Got null locations for flag: %s" % hex(shuffled_flag)
                    # self.temp_locs |= locs
                part_int >>= 1

    def _check_common_flags(self, data_loc: _DataLocations, data: List[bytes]) -> None:
        flag_bytes = data[data_loc]
        initial_flag = data_loc.initial_flag
        # logger.debug("Checking flags for %s" % data_loc.name)
        itr_step = 0x2 if data_loc.length > 0x1 else 0x1
        for i in range(0, data_loc.length, itr_step):
            part = flag_bytes[i:i + itr_step]
            part_int = int.from_bytes(part, 'little')
            # logger.debug("Data found: %s", hex(part_int))
            # logger.debug("Bytes: %s", part)
            for bit in range(itr_step * 8):
                # logger.debug("int %d", part_int)
                if part_int & 1 > 0:
                    flag = i * 8 + bit + initial_flag
                    locs = self.flag_map.get(flag, None)
                    # logger.debug("flag found: %s, locs: %s", hex(flag), locs)
                    if locs is not None:
                        self.temp_locs |= locs
                part_int >>= 1
        # logger.debug(self.temp_locs)

    async def _receive_items(self, ctx: 'BizHawkClientContext', data: List[bytes]) -> None:
        item_in_slot = int.from_bytes(data[_DataLocations.AP_ITEM_SLOT], byteorder="little")
        if item_in_slot != 0:
            logger.debug("AP Item slot has data in it: %d", item_in_slot)
            return
        item_index = int.from_bytes(data[_DataLocations.AP_ITEMS_RECEIVED], 'little')
        start_count = self.starting_items.count
        item_code = None
        if start_count > item_index:
            logger.debug("Starting items to give: %d, Current Item Index: %d", start_count, item_index)
            item_code = self.starting_items[item_index]
        elif len(ctx.items_received) + start_count > item_index:
            logger.debug("Items to give: %d, Current Item Index: %d", len(ctx.items_received), item_index - start_count)
            item_code = ctx.items_received[item_index - start_count].item
        if item_code is not None:
            logger.debug("Writing Item %d to Slot", item_code)
            await write(ctx.bizhawk_ctx, [(_DataLocations.AP_ITEM_SLOT.addr,
                                           item_code.to_bytes(length=2, byteorder="little"),
                                           _DataLocations.AP_ITEM_SLOT.domain)])


    async def game_watcher(self, ctx: 'BizHawkClientContext') -> None:
        # TODO: implement
        # 1. Verify that the game is running (emo tracker, read 2 bytes from 0x02000428 > 1)
        # 2. Verify that a save file is loaded
        # 3. Read the ROM for location flags that have been toggled.
        # Send the appropriate items to AP
        # 4. Check AP for items that should be granted to the player.
        # Give them said items, assuming it is possible to give an item to a PC within the game
        # and save slot selected

        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed:
            logger.debug("Not connected to server...")
            return

        result = await read(ctx.bizhawk_ctx, [data_loc.to_request() for data_loc in _DataLocations])
        if not self._is_in_game(result):
            # TODO: if the player goes back into the save file should we reset some things?
            self.local_locations = set()
            self.starting_items = StartingItemHandler(dict())
            self.was_in_game = False
            logger.debug("Not in game...")
            return

        if not self.was_in_game and ctx.slot_data is not None:
            self.was_in_game = True
            logger.debug(ctx.slot_data)
            self.starting_items = StartingItemHandler(ctx.slot_data.get('start_inventory', dict()))

        # logger.debug(
        #     f"Local locations checked: {len(self.local_locations)}; server locations checked: {len(ctx.checked_locations)}")

        self.temp_locs = set()
        await self._load_djinn(ctx)

        self._check_djinn_flags(result)
        self._check_common_flags(_DataLocations.SUMMONS, result)
        for i in range(_DataLocations.TREASURE_8_FLAGS, _DataLocations.TREASURE_F_FLAGS.value + 1):
            self._check_common_flags(_DataLocations(i), result)
        self._check_common_flags(_DataLocations.INITIAL_INVENTORY, result)

        await self._receive_items(ctx, result)

        if self.temp_locs != self.local_locations:
            if self.temp_locs:
                self.local_locations = self.temp_locs
                logger.debug("Sending locations to AP: %s", self.local_locations)
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(self.local_locations)}])

        victory_check = result[_DataLocations.DOOM_DRAGON]
        if victory_check[0] & 1 > 0 and not ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
