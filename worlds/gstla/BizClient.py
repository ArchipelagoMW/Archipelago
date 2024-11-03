from __future__ import annotations
from collections import defaultdict
import logging
from enum import IntEnum, Enum
from typing import Dict, List, TYPE_CHECKING, Set, Tuple

from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient
from worlds._bizhawk import read, write
from .gen.LocationData import all_locations

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

logger = logging.getLogger("Client")

FLAG_START = 0x40

class _MemDomain(str, Enum):
    EWRAM = 'EWRAM'
    ROM = 'ROM'

class _DataLocations(IntEnum):
    IN_GAME = (0x428, 0x2, 0x0, _MemDomain.EWRAM)
    DJINN_FLAGS = (FLAG_START + (0x30 >> 3), 0x0A, 0x30, _MemDomain.EWRAM)
    # TODO: we haven't agreed on an address, but this location should have
    # is two bytes enough?
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


class GSTLAClient(BizHawkClient):
    game = 'Golden Sun The Lost Age'
    system = 'GBA'
    # patch_suffix = '.apgstla'

    flag_map: defaultdict[int, Set[int]] = defaultdict(lambda: set())
    djinn_ram_to_rom: Dict[int, int] = dict()
    local_locations: Set[int] = set()
    temp_locs: Set[int] = set()

    def __init__(self):
        super().__init__()
        for loc in all_locations:
            self.flag_map[loc.flag].add(loc.ap_id)

    async def validate_rom(self, ctx: 'BizHawkClientContext'):
        game_name = await read(ctx.bizhawk_ctx, [(0xA0, 0x12, _MemDomain.ROM)])
        game_name = game_name[0].decode('ascii')
        logger.debug("Game loaded: %s", game_name)
        if game_name != 'GOLDEN_SUN_BAGFE01':
            return False
        ctx.game = self.game
        # TODO: would like to verify that the ROM is the correct one somehow
        # Possibly verify the seed; would also be nice to have the slot name encoded
        # in the rom somewhere, though not necessary
        ctx.items_handling = 0b001
        ctx.watcher_timeout = 1 # not sure what a reasonable setting here is; passed to asyncio.wait_for
        return True

    async def _load_djinn(self, ctx: 'BizHawkClientContext'):
        if len(self.djinn_ram_to_rom) > 0:
            return
        # Don't put this in the data locations class; we don't want to check this regularly
        result = await read(ctx.bizhawk_ctx, [(0xFA0000, 0x2*18*4, _MemDomain.ROM)])
        for index in range(18*4):
            djinn_flag = index + _DataLocations.DJINN_FLAGS.initial_flag
            section = int.from_bytes(result[0][index*2:(index*2)+2], 'little')
            rom_flag = (section >> 8) * 0x14 + (section & 0xFF) + 0x30
            self.djinn_ram_to_rom[rom_flag] = djinn_flag

    def _is_in_game(self, data: List[bytes]):
        # What the emo tracker pack does; seems like it also verifies the player
        # has opened a save file
        flag = int.from_bytes(data[_DataLocations.IN_GAME], 'little')
        return flag > 1

    def _check_djinn_flags(self, data: List[bytes]):
        flag_bytes = data[_DataLocations.DJINN_FLAGS]
        for i in range(0,_DataLocations.DJINN_FLAGS.length,2):
            part = flag_bytes[i:i+2]
            part_int = int.from_bytes(part, "little")
            # logger.info(part_int)
            for bit in range(16):
                if part_int & 1 > 0:
                    flag = i * 8 + bit
                    shuffled_flag = self.djinn_ram_to_rom[flag + _DataLocations.DJINN_FLAGS.initial_flag]
                    locs = self.flag_map.get(shuffled_flag, None)
                    # logger.debug("orig_flag: %s, shuffle flag: %s, locs: %s", hex(flag), hex(shuffled_flag), locs)
                    assert locs is not None, "Got null locations for flag: %s" % hex(shuffled_flag)
                    self.temp_locs |= locs
                part_int >>= 1

    def _check_common_flags(self, data_loc: _DataLocations, data: List[bytes]):
        flag_bytes = data[data_loc]
        initial_flag = data_loc.initial_flag
        # logger.debug("Checking flags for %s" % data_loc.name)
        itr_step = 0x2 if data_loc.length > 0x1 else 0x1
        for i in range(0, data_loc.length, itr_step):
            part = flag_bytes[i:i+itr_step]
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


    async def _receive_items(self, ctx: 'BizHawkClientContext', data: List[bytes]):
        item_in_slot = int.from_bytes(data[_DataLocations.AP_ITEM_SLOT], byteorder="little")
        if item_in_slot != 0:
            logger.debug("AP Item slot has data in it: %d", item_in_slot)
            return
        item_index = int.from_bytes(data[_DataLocations.AP_ITEMS_RECEIVED], 'little')
        logger.debug("Items to give: %d, Current Item Index: %d", len(ctx.items_received), item_index)
        if len(ctx.items_received) > item_index:
            item_code = ctx.items_received[item_index].item
            logger.debug("Writing Item %d to Slot", item_code)
            await write(ctx.bizhawk_ctx, [(_DataLocations.AP_ITEM_SLOT.addr,
                                           item_code.to_bytes(length=2, byteorder="little"),
                                           _DataLocations.AP_ITEM_SLOT.domain)])

    async def game_watcher(self, ctx: 'BizHawkClientContext'):
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
            logger.debug("Not in game...")
            return

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
                await ctx.send_msgs([{ "cmd": "LocationChecks", "locations": list(self.local_locations) }])

        victory_check = result[_DataLocations.DOOM_DRAGON]
        if victory_check[0] & 1 > 0 and not ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
