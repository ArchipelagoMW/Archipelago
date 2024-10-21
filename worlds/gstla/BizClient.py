from collections import defaultdict
import logging
from typing import Dict, List, TYPE_CHECKING

from worlds._bizhawk.client import BizHawkClient
from worlds._bizhawk import read, write
from . import LocationName, loc_names_by_id
from .GameData import ElementType
from .gen.LocationData import all_locations

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

logger = logging.getLogger("Client")

# TODO: verify?
FLAG_START = 0x40
DJINN_FLAG_OFFSET = 0x30 >> 3
DJINN_FLAG_LOCATION = (FLAG_START + DJINN_FLAG_OFFSET, 0x0A, "EWRAM")

class GSTLAClient(BizHawkClient):
    game = 'Golden Sun The Lost Age'
    system = 'GBA'
    patch_suffix = '.apgstla'
    flag_map: defaultdict[int, List[LocationName]] = defaultdict(lambda: [])
    djinn_ram_to_rom: Dict[int, int] = dict()
    def __init__(self):
        super().__init__()
        for loc in all_locations:
            self.flag_map[loc.flag].append(loc_names_by_id[loc.id])


    async def validate_rom(self, ctx: 'BizHawkClientContext'):
        # TODO: implement
        if True:
            ctx.game = self.game
            # TODO: need to verify that the ROM is the correct one somehow
            # Possibly verify the seed; would also be nice to have the slot name encoded
            # in the rom somewhere, though not necessary
            return True
        pass

    async def is_in_game(self, ctx: 'BizHawkClientContext'):
        result = await read(ctx.bizhawk_ctx, [(0x428, 0x2, 'EWRAM')])
        flag = int.from_bytes(result[0], 'little')
        return flag > 1

    async def load_djinn(self, ctx: 'BizHawkClientContext'):
        if len(self.djinn_ram_to_rom) > 0:
            return
        result = await read(ctx.bizhawk_ctx, [(0xFA0000, 0x2*18*4, 'ROM')])
        for index in range(18*4):
            djinn_flag = 0x30 + index
            section = int.from_bytes(result[0][index*2:(index*2)+2], 'little')
            rom_flag = (section >> 8) * 0x14 + (section & 0xFF) + 0x30
            self.djinn_ram_to_rom[rom_flag] = djinn_flag


    async def game_watcher(self, ctx: 'BizHawkClientContext'):
        # TODO: implement
        # 1. Verify that the game is running (emo tracker, read 2 bytes from 0x02000428 > 1)
        # 2. Verify that a save file is loaded
        # 3. Read the ROM for location flags that have been toggled.
        # Send the appropriate items to AP
        # 4. Check AP for items that should be granted to the player.
        # Give them said items, assuming it is possible to give an item to a PC within the game
        # and save slot selected
        # if not ctx.server or not ctx.server.socket.open or ctx.server.socket.close:
        #     return
        if not await self.is_in_game(ctx):
            return
        await self.load_djinn(ctx)
        result = await read(ctx.bizhawk_ctx, [DJINN_FLAG_LOCATION])
        for i in range(5):
            index = i * 2
            part = result[0][index:index+2]
            part_int = int.from_bytes(part, "little")
            # logger.info(part_int)
            for bit in range(16):
                if part_int & 1 > 0:
                    flag = (i* 16) + bit
                    element = flag // 0x14
                    id = flag % 0x14
                    logger.info("Got Djinn id %d, element %d" % (id, element))
                    # logger.info("Flag: %s" % hex(flag))
                    locs = self.flag_map.get(flag + 0x30, None)
                    if locs is None:
                        logger.warning("no locations for flag")
                    else:
                        for loc in locs:
                            logger.info("Flag covers the following locations: " + loc + "\n")
                        shuffle_offset = 2 * ((element * 0x12) + id)
                        logger.info("shuffle_offset is %s" % hex(shuffle_offset))
                        # shuffle_result = await read(ctx.bizhawk_ctx, [(0xfa0000+shuffle_offset, 0x2, 'ROM')])
                        # shuffled_int = int.from_bytes(shuffle_result[0], 'little')
                        # logger.info("Shuffled int is: %s", hex(shuffled_int))
                        # shuffled_flag = ((shuffled_int >> 8) * 0x14) + ((shuffled_int & 0xFF) + 0x30)
                        shuffled_flag = self.djinn_ram_to_rom[flag + 0x30]
                        logger.info("Shuffled flag is: %s", hex(shuffled_flag))
                        locs = self.flag_map.get(shuffled_flag, None)
                        if locs is not None:
                            for loc in locs:
                                logger.info("Flag covers the following locations: " + loc + "\n")

                part_int >>= 1
        logger.info(result)
        # logger.info(result[0].hex())
