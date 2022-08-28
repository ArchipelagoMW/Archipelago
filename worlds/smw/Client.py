import logging
import asyncio

from NetUtils import ClientStatus, color
from worlds import AutoWorldRegister
from SNIClient import Context, snes_buffered_write, snes_flush_writes, snes_read
from Patch import GAME_SMW

snes_logger = logging.getLogger("SNES")

ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

SAVEDATA_START = WRAM_START + 0xF000
SAVEDATA_SIZE = 0x500

DKC3_ROMNAME_START = 0x00FFC0
SMW_ROMHASH_START = 0x7FC0
ROMNAME_SIZE = 0x15
ROMHASH_SIZE = 0x15

SMW_PROGRESS_DATA = 0x1F02
SMW_EVENT_ROM_DATA = ROM_START + 0x2D608

SMW_GAME_STATE_ADDR = WRAM_START + 0x100
SMW_SFX_ADDR = WRAM_START + 0x1DFC

SMW_RECV_PROGRESS_ADDR = WRAM_START + 0x1F2B     # SMW_TODO: Find a permanent home for this
DKC3_FILE_NAME_ADDR = WRAM_START + 0x5D9
DEATH_LINK_ACTIVE_ADDR = DKC3_ROMNAME_START + 0x15     # SMW_TODO: Find a permanent home for this


async def deathlink_kill_player(ctx: Context):
    pass
    #if ctx.game == GAME_SMW:
        # SMW_TODO: Handle Receiving Deathlink


async def smw_rom_init(ctx: Context):
    if not ctx.rom:
        ctx.finished_game = False
        ctx.death_link_allow_survive = False
        game_hash = await snes_read(ctx, SMW_ROMHASH_START, ROMHASH_SIZE)
        if game_hash is None or game_hash == bytes([0] * ROMHASH_SIZE) or game_hash[:3] != b"SMW":
            return False
        else:
            ctx.game = GAME_SMW
            ctx.items_handling = 0b111  # remote items

        ctx.rom = game_hash

        #death_link = await snes_read(ctx, DEATH_LINK_ACTIVE_ADDR, 1)
        ## SMW_TODO: Handle Deathlink
        #if death_link:
        #    ctx.allow_collect = bool(death_link[0] & 0b100)
        #    await ctx.update_death_link(bool(death_link[0] & 0b1))
    return True


async def smw_game_watcher(ctx: Context):
    if ctx.game == GAME_SMW:
        # SMW_TODO: Handle Deathlink
        game_state = await snes_read(ctx, SMW_GAME_STATE_ADDR, 0x1)
        if game_state is None or game_state[0] != 0x14:
            # We haven't loaded a save file
            return

        new_checks = []
        from worlds.smw.Rom import item_rom_data, ability_rom_data
        from worlds.smw.Levels import location_id_to_level_id
        for loc_name, level_data in location_id_to_level_id.items():
            loc_id = AutoWorldRegister.world_types[ctx.game].location_name_to_id[loc_name]
            if loc_id not in ctx.locations_checked:

                event_id = await snes_read(ctx, SMW_EVENT_ROM_DATA + level_data[0], 0x1)

                if level_data[1] == 2:
                    # Dragon Coins Check
                    pass
                else:
                    event_id_value = event_id[0] + level_data[1]

                    progress_byte = (event_id_value // 8) + SMW_PROGRESS_DATA
                    progress_bit  = 7 - (event_id_value % 8)

                    data = await snes_read(ctx, WRAM_START + progress_byte, 1)
                    masked_data = data[0] & (1 << progress_bit)
                    bit_set = (masked_data != 0)

                    if bit_set:
                        # SMW_TODO: Handle non-included checks
                        new_checks.append(loc_id)

        verify_game_state = await snes_read(ctx, SMW_GAME_STATE_ADDR, 0x1)
        if verify_game_state is None or verify_game_state[0] != 0x14 or verify_game_state != game_state:
            # We have somehow exited the save file (or worse)
            print("Exit Save File")
            return

        rom = await snes_read(ctx, SMW_ROMHASH_START, ROMHASH_SIZE)
        if rom != ctx.rom:
            ctx.rom = None
            print("Exit ROM")
            # We have somehow loaded a different ROM
            return

        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names[new_check_id]
            snes_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])

        recv_count = await snes_read(ctx, SMW_RECV_PROGRESS_ADDR, 1)
        recv_index = recv_count[0]

        if recv_index < len(ctx.items_received):
            item = ctx.items_received[recv_index]
            recv_index += 1
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names[item.item], 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names[item.location], recv_index, len(ctx.items_received)))

            snes_buffered_write(ctx, SMW_RECV_PROGRESS_ADDR, bytes([recv_index]))
            if item.item in item_rom_data:
                item_count = await snes_read(ctx, WRAM_START + item_rom_data[item.item][0], 0x1)
                increment = item_rom_data[item.item][1]

                new_item_count = item_count[0]
                if increment > 1:
                    new_item_count = increment
                else:
                    new_item_count += increment

                if verify_game_state[0] == 0x14 and len(item_rom_data[item.item]) > 2:
                    snes_buffered_write(ctx, SMW_SFX_ADDR, bytes([item_rom_data[item.item][2]]))

                snes_buffered_write(ctx, WRAM_START + item_rom_data[item.item][0], bytes([new_item_count]))
            else:
                if item.item in ability_rom_data:
                    # Handle Upgrades
                    for rom_data in ability_rom_data[item.item]:
                        data = await snes_read(ctx, WRAM_START + rom_data[0], 1)
                        masked_data = data[0] | (1 << rom_data[1])
                        snes_buffered_write(ctx, WRAM_START + rom_data[0], bytes([masked_data]))
                elif item.item == 0xBC000A:
                    # Handle Progressive Powerup
                    data = await snes_read(ctx, WRAM_START + 0x1F2D, 1)
                    mushroom_data = data[0] & (1 << 0)
                    fire_flower_data = data[0] & (1 << 1)
                    cape_data = data[0] & (1 << 2)
                    if mushroom_data == 0:
                        masked_data = data[0] | (1 << 0)
                        snes_buffered_write(ctx, WRAM_START + 0x1F2D, bytes([masked_data]))
                    elif fire_flower_data == 0:
                        masked_data = data[0] | (1 << 1)
                        snes_buffered_write(ctx, WRAM_START + 0x1F2D, bytes([masked_data]))
                    elif cape_data == 0:
                        masked_data = data[0] | (1 << 2)
                        snes_buffered_write(ctx, WRAM_START + 0x1F2D, bytes([masked_data]))
                    else:
                        # Extra Powerup?
                        pass

            await snes_flush_writes(ctx)

        # DKC3_TODO: This method of collect should work, however it does not unlock the next level correctly when previous is flagged
        # Handle Collected Locations
        #for loc_id in ctx.checked_locations:
        #    if loc_id not in ctx.locations_checked:
        #        loc_data = location_rom_data[loc_id]
        #        data = await snes_read(ctx, WRAM_START + loc_data[0], 1)
        #        invert_bit = ((len(loc_data) >= 3) and loc_data[2])
        #        if not invert_bit:
        #            masked_data = data[0] | (1 << loc_data[1])
        #            print("Collected Location: ", hex(loc_data[0]), " | ", loc_data[1])
        #            snes_buffered_write(ctx, WRAM_START + loc_data[0], bytes([masked_data]))
        #            await snes_flush_writes(ctx)
        #        else:
        #            masked_data = data[0] & ~(1 << loc_data[1])
        #            print("Collected Inverted Location: ", hex(loc_data[0]), " | ", loc_data[1])
        #            snes_buffered_write(ctx, WRAM_START + loc_data[0], bytes([masked_data]))
        #            await snes_flush_writes(ctx)
        #        ctx.locations_checked.add(loc_id)

