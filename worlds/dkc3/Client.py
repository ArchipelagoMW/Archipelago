import logging

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient

snes_logger = logging.getLogger("SNES")

# FXPAK Pro protocol memory mapping used by SNI
ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

DKC3_ROMNAME_START = 0x00FFC0
DKC3_ROMHASH_START = 0x7FC0
ROMNAME_SIZE = 0x15
ROMHASH_SIZE = 0x15

DKC3_RECV_PROGRESS_ADDR = WRAM_START + 0x632
DKC3_FILE_NAME_ADDR = WRAM_START + 0x5D9
DEATH_LINK_ACTIVE_ADDR = DKC3_ROMNAME_START + 0x15     # DKC3_TODO: Find a permanent home for this


class DKC3SNIClient(SNIClient):
    game = "Donkey Kong Country 3"
    patch_suffix = ".apdkc3"

    async def deathlink_kill_player(self, ctx):
        pass
        # DKC3_TODO: Handle Receiving Deathlink


    async def validate_rom(self, ctx):
        from SNIClient import snes_read

        rom_name = await snes_read(ctx, DKC3_ROMHASH_START, ROMHASH_SIZE)
        if rom_name is None or rom_name == bytes([0] * ROMHASH_SIZE) or rom_name[:2] != b"D3":
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111  # remote items

        ctx.rom = rom_name

        #death_link = await snes_read(ctx, DEATH_LINK_ACTIVE_ADDR, 1)
        ## DKC3_TODO: Handle Deathlink
        #if death_link:
        #    ctx.allow_collect = bool(death_link[0] & 0b100)
        #    await ctx.update_death_link(bool(death_link[0] & 0b1))
        return True


    async def game_watcher(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        # DKC3_TODO: Handle Deathlink
        save_file_name = await snes_read(ctx, DKC3_FILE_NAME_ADDR, 0x5)
        if save_file_name is None or save_file_name[0] == 0x00 or save_file_name == bytes([0x55] * 0x05):
            # We haven't loaded a save file
            return

        new_checks = []
        from .Rom import location_rom_data, item_rom_data, boss_location_ids, level_unlock_map
        location_ram_data = await snes_read(ctx, WRAM_START + 0x5FE, 0x81)
        for loc_id, loc_data in location_rom_data.items():
            if loc_id not in ctx.locations_checked:
                data = location_ram_data[loc_data[0] - 0x5FE]
                masked_data = data & (1 << loc_data[1])
                bit_set = (masked_data != 0)
                invert_bit = ((len(loc_data) >= 3) and loc_data[2])
                if bit_set != invert_bit:
                    # DKC3_TODO: Handle non-included checks
                    new_checks.append(loc_id)

        verify_save_file_name = await snes_read(ctx, DKC3_FILE_NAME_ADDR, 0x5)
        if verify_save_file_name is None or verify_save_file_name[0] == 0x00 or verify_save_file_name == bytes([0x55] * 0x05) or verify_save_file_name != save_file_name:
            # We have somehow exited the save file (or worse)
            ctx.rom = None
            return

        rom = await snes_read(ctx, DKC3_ROMHASH_START, ROMHASH_SIZE)
        if rom != ctx.rom:
            ctx.rom = None
            # We have somehow loaded a different ROM
            return

        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names.lookup_in_game(new_check_id)
            snes_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])

        # DKC3_TODO: Make this actually visually display new things received (ASM Hook required)
        recv_count = await snes_read(ctx, DKC3_RECV_PROGRESS_ADDR, 1)
        recv_index = recv_count[0]

        if recv_index < len(ctx.items_received):
            item = ctx.items_received[recv_index]
            recv_index += 1
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_game(item.item), 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), recv_index, len(ctx.items_received)))

            snes_buffered_write(ctx, DKC3_RECV_PROGRESS_ADDR, bytes([recv_index]))
            if item.item in item_rom_data:
                item_count = await snes_read(ctx, WRAM_START + item_rom_data[item.item][0], 0x1)
                new_item_count = item_count[0] + 1
                for address in item_rom_data[item.item]:
                    snes_buffered_write(ctx, WRAM_START + address, bytes([new_item_count]))

                # Handle Coin Displays
                current_level = await snes_read(ctx, WRAM_START + 0x5E3, 0x5)
                overworld_locked = ((await snes_read(ctx, WRAM_START + 0x5FC, 0x1))[0] == 0x01)
                if item.item == 0xDC3002 and not overworld_locked and (current_level[0] == 0x0A and current_level[2] == 0x00 and current_level[4] == 0x03):
                    # Bazaar and Barter
                    item_count = await snes_read(ctx, WRAM_START + 0xB02, 0x1)
                    new_item_count = item_count[0] + 1
                    snes_buffered_write(ctx, WRAM_START + 0xB02, bytes([new_item_count]))
                elif item.item == 0xDC3002 and not overworld_locked and current_level[0] == 0x04:
                    # Swanky
                    item_count = await snes_read(ctx, WRAM_START + 0xA26, 0x1)
                    new_item_count = item_count[0] + 1
                    snes_buffered_write(ctx, WRAM_START + 0xA26, bytes([new_item_count]))
                elif item.item == 0xDC3003 and not overworld_locked and (current_level[0] == 0x0A and current_level[2] == 0x08 and current_level[4] == 0x01):
                    # Boomer
                    item_count = await snes_read(ctx, WRAM_START + 0xB02, 0x1)
                    new_item_count = item_count[0] + 1
                    snes_buffered_write(ctx, WRAM_START + 0xB02, bytes([new_item_count]))
            else:
                # Handle Patch and Skis
                if item.item == 0xDC3007:
                    num_upgrades = 1
                    inventory = await snes_read(ctx, WRAM_START + 0x605, 0xF)

                    if (inventory[0] & 0x02):
                        num_upgrades = 3
                    elif (inventory[13] & 0x08) or (inventory[0] & 0x01):
                        num_upgrades = 2

                    if num_upgrades == 1:
                        snes_buffered_write(ctx, WRAM_START + 0x605, bytes([inventory[0] | 0x01]))
                        if inventory[4] == 0:
                            snes_buffered_write(ctx, WRAM_START + 0x609, bytes([0x01]))
                        elif inventory[6] == 0:
                            snes_buffered_write(ctx, WRAM_START + 0x60B, bytes([0x01]))
                        elif inventory[8] == 0:
                            snes_buffered_write(ctx, WRAM_START + 0x60D, bytes([0x01]))
                        elif inventory[10] == 0:
                            snes_buffered_write(ctx, WRAM_START + 0x60F, bytes([0x01]))

                        cove_mekanos_progress = await snes_read(ctx, WRAM_START + 0x691, 0x2)
                        snes_buffered_write(ctx, WRAM_START + 0x691, bytes([cove_mekanos_progress[0] | 0x01]))
                        snes_buffered_write(ctx, WRAM_START + 0x692, bytes([cove_mekanos_progress[1] | 0x01]))
                    elif num_upgrades == 2:
                        snes_buffered_write(ctx, WRAM_START + 0x605, bytes([inventory[0] | 0x02]))
                        if inventory[4] == 0:
                            snes_buffered_write(ctx, WRAM_START + 0x609, bytes([0x02]))
                        elif inventory[6] == 0:
                            snes_buffered_write(ctx, WRAM_START + 0x60B, bytes([0x02]))
                        elif inventory[8] == 0:
                            snes_buffered_write(ctx, WRAM_START + 0x60D, bytes([0x02]))
                        elif inventory[10] == 0:
                            snes_buffered_write(ctx, WRAM_START + 0x60F, bytes([0x02]))
                    elif num_upgrades == 3:
                        snes_buffered_write(ctx, WRAM_START + 0x606, bytes([inventory[1] | 0x20]))

                        k3_ridge_progress = await snes_read(ctx, WRAM_START + 0x693, 0x2)
                        snes_buffered_write(ctx, WRAM_START + 0x693, bytes([k3_ridge_progress[0] | 0x01]))
                        snes_buffered_write(ctx, WRAM_START + 0x694, bytes([k3_ridge_progress[1] | 0x01]))
                elif item.item == 0xDC3000:
                    # Handle Victory
                    if not ctx.finished_game:
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                        ctx.finished_game = True
                else:
                    print("Item Not Recognized: ", item.item)
                pass

            await snes_flush_writes(ctx)

        # Handle Collected Locations
        levels_to_tiles = await snes_read(ctx, ROM_START + 0x3FF800, 0x60)
        tiles_to_levels = await snes_read(ctx, ROM_START + 0x3FF860, 0x60)
        for loc_id in ctx.checked_locations:
            if loc_id not in ctx.locations_checked and loc_id not in boss_location_ids:
                loc_data = location_rom_data[loc_id]
                data = await snes_read(ctx, WRAM_START + loc_data[0], 1)
                invert_bit = ((len(loc_data) >= 3) and loc_data[2])
                if not invert_bit:
                    masked_data = data[0] | (1 << loc_data[1])
                    snes_buffered_write(ctx, WRAM_START + loc_data[0], bytes([masked_data]))

                    if (loc_data[1] == 1):
                        # Make the next levels accessible
                        level_id = loc_data[0] - 0x632
                        tile_id = levels_to_tiles[level_id] if levels_to_tiles[level_id] != 0xFF else level_id
                        tile_id = tile_id + 0x632
                        if tile_id in level_unlock_map:
                            for next_level_address in level_unlock_map[tile_id]:
                                next_level_id = next_level_address - 0x632
                                next_tile_id = tiles_to_levels[next_level_id] if tiles_to_levels[next_level_id] != 0xFF else next_level_id
                                next_tile_id = next_tile_id + 0x632
                                next_data = await snes_read(ctx, WRAM_START + next_tile_id, 1)
                                snes_buffered_write(ctx, WRAM_START + next_tile_id, bytes([next_data[0] | 0x01]))

                    await snes_flush_writes(ctx)
                else:
                    masked_data = data[0] & ~(1 << loc_data[1])
                    snes_buffered_write(ctx, WRAM_START + loc_data[0], bytes([masked_data]))
                    await snes_flush_writes(ctx)
                ctx.locations_checked.add(loc_id)

        # Calculate Boomer Cost Text
        boomer_cost_text = await snes_read(ctx, WRAM_START + 0xAAFD, 2)
        if boomer_cost_text[0] == 0x31 and boomer_cost_text[1] == 0x35:
            boomer_cost = await snes_read(ctx, ROM_START + 0x349857, 1)
            boomer_cost_tens = int(boomer_cost[0]) // 10
            boomer_cost_ones = int(boomer_cost[0]) % 10
            snes_buffered_write(ctx, WRAM_START + 0xAAFD, bytes([0x30 + boomer_cost_tens, 0x30 + boomer_cost_ones]))
            await snes_flush_writes(ctx)

        boomer_final_cost_text = await snes_read(ctx, WRAM_START + 0xAB9B, 2)
        if boomer_final_cost_text[0] == 0x32 and boomer_final_cost_text[1] == 0x35:
            boomer_cost = await snes_read(ctx, ROM_START + 0x349857, 1)
            boomer_cost_tens = boomer_cost[0] // 10
            boomer_cost_ones = boomer_cost[0] % 10
            snes_buffered_write(ctx, WRAM_START + 0xAB9B, bytes([0x30 + boomer_cost_tens, 0x30 + boomer_cost_ones]))
            await snes_flush_writes(ctx)
