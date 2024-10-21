from collections import defaultdict
import logging
from typing import Dict, List, TYPE_CHECKING

from worlds._bizhawk.client import BizHawkClient
from worlds._bizhawk import read, write
from . import LocationName, loc_names_by_id
from .gen.LocationData import all_locations

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

logger = logging.getLogger("Client")

# TODO: verify?
SAVE_OFFSET = 0x02000000
DJINN_FLAG_LOCATION = (0x46, 0x08, "WRAM")

class GSTLAClient(BizHawkClient):
    game = 'Golden Sun The Lost Age'
    system = 'GBA'
    patch_suffix = '.apgstla'
    flag_map: defaultdict[int, List[LocationName]] = defaultdict(lambda: [])
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

    async def game_watcher(self, ctx: 'BizHawkClientContext'):
        # TODO: implement
        # 1. Verify that the game is running
        # 2. Verify that a save file is loaded
        # 3. Read the ROM for location flags that have been toggled.
        # Send the appropriate items to AP
        # 4. Check AP for items that should be granted to the player.
        # Give them said items, assuming it is possible to give an item to a PC within the game
        # and save slot selected
        # if not ctx.server or not ctx.server.socket.open or ctx.server.socket.close:
        #     return
        result = await read(ctx.bizhawk_ctx, [DJINN_FLAG_LOCATION])
        logger.info(result[0].hex())