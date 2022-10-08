import logging
import asyncio
import time

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient
from .Rom import ROM_PLAYER_LIMIT as SMZ3_ROM_PLAYER_LIMIT

snes_logger = logging.getLogger("SNES")

# FXPAK Pro protocol memory mapping used by SNI
ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

# SMZ3
SMZ3_ROMNAME_START = ROM_START + 0x00FFC0
ROMNAME_SIZE = 0x15

SAVEDATA_START = WRAM_START + 0xF000

SMZ3_INGAME_MODES = {0x07, 0x09, 0x0B}
ENDGAME_MODES = {0x19, 0x1A}
SM_ENDGAME_MODES = {0x26, 0x27}
SMZ3_DEATH_MODES = {0x15, 0x17, 0x18, 0x19, 0x1A}

SMZ3_RECV_PROGRESS_ADDR = SRAM_START + 0x4000         # 2 bytes
SMZ3_RECV_ITEM_ADDR = SAVEDATA_START + 0x4D2          # 1 byte
SMZ3_RECV_ITEM_PLAYER_ADDR = SAVEDATA_START + 0x4D3   # 1 byte


class SMZ3SNIClient(SNIClient):
    game = "SMZ3"

    async def validate_rom(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        rom_name = await snes_read(ctx, SMZ3_ROMNAME_START, ROMNAME_SIZE)
        if rom_name is None or rom_name == bytes([0] * ROMNAME_SIZE) or rom_name[:3] != b"ZSM":
            return False

        ctx.game = self.game
        ctx.items_handling = 0b101  # local items and remote start inventory

        ctx.rom = rom_name

        return True


    async def game_watcher(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        if ctx.server is None or ctx.slot is None:
            # not successfully connected to a multiworld server, cannot process the game sending items
            return

        currentGame = await snes_read(ctx, SRAM_START + 0x33FE, 2)
        if (currentGame is not None):
            if (currentGame[0] != 0):
                gamemode = await snes_read(ctx, WRAM_START + 0x0998, 1)
                endGameModes = SM_ENDGAME_MODES
            else:
                gamemode = await snes_read(ctx, WRAM_START + 0x10, 1)
                endGameModes = ENDGAME_MODES

        if gamemode is not None and (gamemode[0] in endGameModes):
            if not ctx.finished_game:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True
            return

        data = await snes_read(ctx, SMZ3_RECV_PROGRESS_ADDR + 0x680, 4)
        if data is None:
            return

        recv_index = data[0] | (data[1] << 8)
        recv_item = data[2] | (data[3] << 8)

        while (recv_index < recv_item):
            item_address = recv_index * 8
            message = await snes_read(ctx, SMZ3_RECV_PROGRESS_ADDR + 0x700 + item_address, 8)
            is_z3_item = ((message[5] & 0x80) != 0)
            masked_part = (message[5] & 0x7F) if is_z3_item else message[5]
            item_index = ((message[4] | (masked_part << 8)) >> 3) + (256 if is_z3_item else 0)

            recv_index += 1
            snes_buffered_write(ctx, SMZ3_RECV_PROGRESS_ADDR + 0x680, bytes([recv_index & 0xFF, (recv_index >> 8) & 0xFF]))

            from worlds.smz3.TotalSMZ3.Location import locations_start_id
            from worlds.smz3 import convertLocSMZ3IDToAPID
            location_id = locations_start_id + convertLocSMZ3IDToAPID(item_index)

            ctx.locations_checked.add(location_id)
            location = ctx.location_names[location_id]
            snes_logger.info(f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [location_id]}])

        data = await snes_read(ctx, SMZ3_RECV_PROGRESS_ADDR + 0x600, 4)
        if data is None:
            return

        item_out_ptr = data[2] | (data[3] << 8)

        from worlds.smz3.TotalSMZ3.Item import items_start_id
        if item_out_ptr < len(ctx.items_received):
            item = ctx.items_received[item_out_ptr]
            item_id = item.item - items_start_id

            player_id = item.player if item.player <= SMZ3_ROM_PLAYER_LIMIT else 0
            snes_buffered_write(ctx, SMZ3_RECV_PROGRESS_ADDR + item_out_ptr * 4, bytes([player_id & 0xFF, (player_id >> 8) & 0xFF, item_id & 0xFF, (item_id >> 8) & 0xFF]))
            item_out_ptr += 1
            snes_buffered_write(ctx, SMZ3_RECV_PROGRESS_ADDR + 0x602, bytes([item_out_ptr & 0xFF, (item_out_ptr >> 8) & 0xFF]))
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names[item.item], 'red', 'bold'), color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names[item.location], item_out_ptr, len(ctx.items_received)))

        await snes_flush_writes(ctx)

