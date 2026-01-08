from typing import TYPE_CHECKING, Tuple, Dict

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from NetUtils import ClientStatus, NetworkItem

if TYPE_CHECKING:
    from world._bizhawk.context import BizHawkClientContext, BizHawkClientCommandProcessor

SADV2_ZONE_SELECT_TABLE = 0xd7508 #rom
SADV2_UPDATE_ZONE_SELECT_BOSS = 0x30EB0 #rom
SADV2_UPDATE_ZONE_SELECT_LEVEL = 0x30f92 #rom
SADV2_UPDATE_EMERALDS = 0x6c5d4 #rom
SADV2_CHARACTERS_UNLOCKED = 0x266b #ewram
SADV2_SONIC_EMERALDS = 0x2664 #ewram
SADV2_SONIC_LEVELS_UNLOCKED = 0x265f #ewram
SADV2_AREA_53_UNLOCKED = 0x2672 #ewram
SADV2_LEVEL_COMPLETE = 0x54a8 #iwram
SADV2_STAGE_FLAGS = 0x5424 #iwram, seventh bit is demo mode (i think)
SADV2_CURRENT_LEVEL = 0x55b4 #iwram
SADV2_CURRENT_CHARACTER = 0x54f0 #iwram


zone_data: Dict[int, Tuple[int, int, int, int]] = {
    # ID: (Act 1 ID, Act 1 Offset, Act 2 ID, Act 2 Offset)
    200: [0x00, 0x00, 0x01, 0x01], # Leaf Forest
    201: [0x04, 0x02, 0x05, 0x03], # Hot Crater
    202: [0x08, 0x04, 0x09, 0x05], # Music Plant
    203: [0x0c, 0x06, 0x0d, 0x07], # Ice Paradise
    204: [0x10, 0x08, 0x11, 0x09], # Sky Canyon
    205: [0x14, 0x0a, 0x15, 0x0b], # Techno Base
    206: [0x18, 0x0c, 0x19, 0x0d], # Egg Utopia
    207: [0x1c, 0x0e] # XX
}

masks: Dict[int, int] = {
    0: 0x01,
    1: 0x02,
    2: 0x04,
    3: 0x08,
    4: 0x10,
    5: 0x20,
    6: 0x40
}

class SonicAdvance2Client(BizHawkClient):
    game = "Sonic Advance 2"
    system = "GBA"

    starting_zone: int
    did_setup: bool = False
    emeralds: int = 0x00
    characters: int = 0x00
    xx_coords: int = 0
    last_item_idx = 0
    dont_check_levels = 1

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            game_code: bytes = ((await bizhawk.read(ctx.bizhawk_ctx, [(0xac, 4, "ROM")])))
            
            if game_code[0] != b"A2NE":
                return False
        except bizhawk.RequestFailedError:
            return False
        
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True

        return True
    
    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ((ctx.server is None) or (ctx.server.socket.closed) or (ctx.slot_data is None)):
            return
        
        if not self.did_setup:
            starting_zone = ctx.slot_data["starting_zone"]
            starting_zone += 200
            starting_character = masks[ctx.slot_data["starting_character"]]

            sz_act1 = zone_data[starting_zone][0]
            sz_act2 = zone_data[starting_zone][2]
            sz_list = [sz_act1, sz_act2, sz_act1, sz_act2, sz_act1, sz_act2, sz_act1, sz_act2,
                        sz_act1, sz_act2, sz_act1, sz_act2, sz_act1, sz_act2, sz_act1]

            # Update the zone table to only point to our starting zone
            await bizhawk.write(ctx.bizhawk_ctx, [(SADV2_ZONE_SELECT_TABLE, sz_list, "ROM")])
            # Update unlocked characters to only allow our starting character
            await bizhawk.write(ctx.bizhawk_ctx, [(SADV2_CHARACTERS_UNLOCKED, [starting_character], "EWRAM")])
            # This NOPs the instruction that awards chaos emeralds
            await bizhawk.write(ctx.bizhawk_ctx, [(SADV2_UPDATE_EMERALDS, [0x00, 0x00], "ROM")])
            # Full level select access up to XX
            await bizhawk.write(ctx.bizhawk_ctx, [(SADV2_SONIC_LEVELS_UNLOCKED, [0x1d, 0x1d, 0x1d, 0x1d, 0x1d], "EWRAM")])
            # Set everyone's emeralds to zero
            await bizhawk.write(ctx.bizhawk_ctx, [(SADV2_SONIC_EMERALDS, [0x00, 0x00, 0x00, 0x00, 0x00], "EWRAM")])
            # Block off True Area 53
            await bizhawk.write(ctx.bizhawk_ctx, [(SADV2_AREA_53_UNLOCKED, [0x00], "EWRAM")])

            self.did_setup = True

        try:
            level_complete, demo_mode, act_id, character_id, xx_complete = await bizhawk.read(ctx.bizhawk_ctx, [
                (SADV2_LEVEL_COMPLETE, 1, "IWRAM"), (SADV2_STAGE_FLAGS, 1, "IWRAM"),
                (SADV2_CURRENT_LEVEL, 1, "IWRAM"), (SADV2_CURRENT_CHARACTER, 1, "IWRAM"), 
                (SADV2_STAGE_FLAGS + 0x01, 1, "IWRAM")])
            
            await self.add_items(ctx.items_received, ctx)
            
            if(self.dont_check_levels == 0):
                if not (int.from_bytes(demo_mode, "little") & 0x40):
                    if (int.from_bytes(level_complete, "little") == 0xFF and int.from_bytes(act_id) < 0x1c):
                        location_id = 0x10000 + (int.from_bytes(character_id) * 0x1000) + (int.from_bytes(act_id) * 0x10)
                        if location_id not in ctx.checked_locations:
                            await ctx.send_msgs([{
                                "cmd": "LocationChecks",
                                "locations": [location_id]
                            }])

                        # Special stages send next act's check. Stop sending checks until next act
                        self.dont_check_levels = 1
                    elif(int.from_bytes(level_complete, "little") == 0xFF and int.from_bytes(act_id) == 0x1d):
                        await ctx.send_msgs([{
                            "cmd": "StatusUpdate",
                            "status": ClientStatus.CLIENT_GOAL
                        }])
                    # XX messes with the usual level completion code but we can use this stage flag to check it
                    elif(int.from_bytes(xx_complete) == 0x04 and int.from_bytes(act_id) == 0x1c):
                        location_id = 0x10000 + (int.from_bytes(character_id) * 0x1000) + (0x1c * 0x10)
                        if location_id not in ctx.checked_locations:
                            await ctx.send_msgs([{
                                "cmd": "LocationChecks",
                                "locations": [location_id]
                            }])
                        
                        # The credits don't clear the address. Stop sending checks until the player enters gameplay again.
                        self.dont_check_levels = 1
                else:
                    # Demo mode sends Leaf Forest upon exit. Stop sending checks
                    self.dont_check_levels = 1
            else:
                # Resume checking locations once the player is in a valid game state
                if (int.from_bytes(level_complete) == 0x0) and not (int.from_bytes(demo_mode, "little") & 0x40):
                    self.dont_check_levels = 0

            
        except bizhawk.RequestFailedError:
            pass

    async def add_items(self, item_list: list[NetworkItem], ctx: "BizHawkClientContext") -> None:
        
        # Take items, convert them to their in-game ids and place them where they belong.
        # Only the emeralds variable matters for logic
        # Setting emeralds in game is visual only for tracking purposes
        

        if self.last_item_idx >= len(item_list):
            # Don't process more items until we reach a new one
            return
        
        for item in item_list[self.last_item_idx:]:

            item_id = item.item
            if (item_id // 100 == 1):
                self.characters = self.characters | masks[item_id % 100]

                await bizhawk.write(ctx.bizhawk_ctx, [(SADV2_CHARACTERS_UNLOCKED, [self.characters], "EWRAM")])

            elif (item_id // 100 == 2):
                if item_id % 100 == 7:
                    self.xx_coords += 1

                    if self.xx_coords == ctx.slot_data["xx_coords"]:
                        await bizhawk.write(ctx.bizhawk_ctx, [(SADV2_ZONE_SELECT_TABLE + 0x0e, [0x1c], "ROM")])
                else:
                    await bizhawk.write(ctx.bizhawk_ctx, [(SADV2_ZONE_SELECT_TABLE + zone_data[item_id][1],
                                                     [zone_data[item_id][0], zone_data[item_id][2]], "ROM")])
                    
            elif (item_id // 100 == 3 and self.emeralds != 0x7f):
                self.emeralds = self.emeralds | masks[item_id % 100]

                if(self.emeralds == 0x7F):
                    # This value means we've obtained all emeralds and can open the path to True Area 53
                    await bizhawk.write(ctx.bizhawk_ctx, [(SADV2_AREA_53_UNLOCKED, [0x02], "EWRAM")])
                    
                await bizhawk.write(ctx.bizhawk_ctx, [(SADV2_SONIC_EMERALDS, [self.emeralds, self.emeralds,
                                                    self.emeralds, self.emeralds, self.emeralds], "EWRAM")])
            self.last_item_idx += 1
