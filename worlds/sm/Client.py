import logging
import asyncio
import time

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient
from .Rom import SM_ROM_MAX_PLAYERID

snes_logger = logging.getLogger("SNES")

GAME_SM = "Super Metroid"

# FXPAK Pro protocol memory mapping used by SNI
ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

# SM
SM_ROMNAME_START = ROM_START + 0x007FC0
ROMNAME_SIZE = 0x15

SM_INGAME_MODES = {0x07, 0x09, 0x0b}
SM_ENDGAME_MODES = {0x26, 0x27}
SM_DEATH_MODES = {0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A}

# RECV and SEND are from the gameplay's perspective: SNIClient writes to RECV queue and reads from SEND queue
SM_RECV_QUEUE_START  = SRAM_START + 0x2000
SM_RECV_QUEUE_WCOUNT = SRAM_START + 0x2602
SM_SEND_QUEUE_START  = SRAM_START + 0x2700
SM_SEND_QUEUE_RCOUNT = SRAM_START + 0x2680
SM_SEND_QUEUE_WCOUNT = SRAM_START + 0x2682

SM_DEATH_LINK_ACTIVE_ADDR = ROM_START + 0x277F04    # 1 byte
SM_REMOTE_ITEM_FLAG_ADDR = ROM_START + 0x277F06    # 1 byte


class SMSNIClient(SNIClient):
    game = "Super Metroid"
    patch_suffix = [".apsm", ".apm3"]

    async def deathlink_kill_player(self, ctx):
        from SNIClient import DeathState, snes_buffered_write, snes_flush_writes, snes_read
        snes_buffered_write(ctx, WRAM_START + 0x09C2, bytes([1, 0]))  # set current health to 1 (to prevent saving with 0 energy)
        snes_buffered_write(ctx, WRAM_START + 0x0A50, bytes([255])) # deal 255 of damage at next opportunity
        if not ctx.death_link_allow_survive:
            snes_buffered_write(ctx, WRAM_START + 0x09D6, bytes([0, 0]))  # set current reserve to 0

        await snes_flush_writes(ctx)
        await asyncio.sleep(1)

        gamemode = await snes_read(ctx, WRAM_START + 0x0998, 1)
        health = await snes_read(ctx, WRAM_START + 0x09C2, 2)
        if health is not None:
            health = health[0] | (health[1] << 8)
        if not gamemode or gamemode[0] in SM_DEATH_MODES or (
                ctx.death_link_allow_survive and health is not None and health > 0):
            ctx.death_state = DeathState.dead


    async def validate_rom(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        rom_name = await snes_read(ctx, SM_ROMNAME_START, ROMNAME_SIZE)
        if rom_name is None or rom_name == bytes([0] * ROMNAME_SIZE) or rom_name[:2] != b"SM" or rom_name[2] not in b"1234567890":
            return False

        ctx.game = self.game

        # versions lower than 0.3.0 dont have item handling flag nor remote item support
        romVersion = int(rom_name[2:5].decode('UTF-8'))
        if romVersion < 30:
            ctx.items_handling = 0b001 # full local
        else:
            item_handling = await snes_read(ctx, SM_REMOTE_ITEM_FLAG_ADDR, 1)
            ctx.items_handling = 0b001 if item_handling is None else item_handling[0]

        ctx.rom = rom_name

        death_link = await snes_read(ctx, SM_DEATH_LINK_ACTIVE_ADDR, 1)

        if death_link:
            ctx.allow_collect = bool(death_link[0] & 0b100)
            ctx.death_link_allow_survive = bool(death_link[0] & 0b10)
            await ctx.update_death_link(bool(death_link[0] & 0b1))

        return True


    async def game_watcher(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        if ctx.server is None or ctx.slot is None:
            # not successfully connected to a multiworld server, cannot process the game sending items
            return

        gamemode = await snes_read(ctx, WRAM_START + 0x0998, 1)
        if "DeathLink" in ctx.tags and gamemode and ctx.last_death_link + 1 < time.time():
            currently_dead = gamemode[0] in SM_DEATH_MODES
            await ctx.handle_deathlink_state(currently_dead)
        if gamemode is not None and gamemode[0] in SM_ENDGAME_MODES:
            if not ctx.finished_game:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True
            return

        data = await snes_read(ctx, SM_SEND_QUEUE_RCOUNT, 4)
        if data is None:
            return

        recv_index = data[0] | (data[1] << 8)
        recv_item = data[2] | (data[3] << 8) # this is actually SM_SEND_QUEUE_WCOUNT

        while (recv_index < recv_item):
            item_address = recv_index * 8
            message = await snes_read(ctx, SM_SEND_QUEUE_START + item_address, 8)
            item_index = (message[4] | (message[5] << 8)) >> 3

            recv_index += 1
            snes_buffered_write(ctx, SM_SEND_QUEUE_RCOUNT,
                                bytes([recv_index & 0xFF, (recv_index >> 8) & 0xFF]))

            from . import locations_start_id
            location_id = locations_start_id + item_index

            ctx.locations_checked.add(location_id)
            location = ctx.location_names.lookup_in_game(location_id)
            snes_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [location_id]}])

        data = await snes_read(ctx, SM_RECV_QUEUE_WCOUNT, 2)
        if data is None:
            return

        item_out_ptr = data[0] | (data[1] << 8)

        from . import items_start_id
        from . import locations_start_id
        if item_out_ptr < len(ctx.items_received):
            item = ctx.items_received[item_out_ptr]
            item_id = item.item - items_start_id
            if bool(ctx.items_handling & 0b010) or item.location < 0: # item.location < 0 for !getitem to work
                location_id = (item.location - locations_start_id) if (item.location >= 0 and item.player == ctx.slot) else 0xFF
            else:
                location_id = 0x00 #backward compat

            player_id = item.player if item.player <= SM_ROM_MAX_PLAYERID else 0
            snes_buffered_write(ctx, SM_RECV_QUEUE_START + item_out_ptr * 4, bytes(
                [player_id & 0xFF, (player_id >> 8) & 0xFF, item_id & 0xFF, location_id & 0xFF]))
            item_out_ptr += 1
            snes_buffered_write(ctx, SM_RECV_QUEUE_WCOUNT,
                                bytes([item_out_ptr & 0xFF, (item_out_ptr >> 8) & 0xFF]))
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_game(item.item), 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), item_out_ptr, len(ctx.items_received)))

        await snes_flush_writes(ctx)
