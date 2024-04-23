import logging
import struct
import typing
import time
from struct import pack
from .local_data import location_list, scout_location_map, plain_encoding_table, shop_scouts, special_chests, hud_encoding_table, sprite_visuals

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient

if typing.TYPE_CHECKING:
    from SNIClient import SNIContext
else:
    SNIContext = typing.Any

snes_logger = logging.getLogger("SNES")

ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

SAI2_ROMHASH_START = 0x00FFC0
ROMHASH_SIZE = 0x15

ITEMQUEUE_HIGH = WRAM_START + 0x4D6
ITEM_RECEIVED = WRAM_START + 0x0485
DEMO_FLAG = WRAM_START + 0x03F5
CHEST_SCOUT_MODE = WRAM_START + 0x04F9
SPECIAL_CHEST_SCOUT = SRAM_START + 0x7DE7
LOCATIONS_SCOUTED_FLAG = WRAM_START + 0x04C4
IN_GAME = WRAM_START + 0x045A
GOALFLAG = WRAM_START + 0x0034

SHOP_SCOUTS = [0xA7D7, 0xA82D, 0xA883]

class SAI2SNIClient(SNIClient):
    game = "Super Adventure Island II"

    async def validate_rom(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        rom_name = await snes_read(ctx, SAI2_ROMHASH_START, ROMHASH_SIZE)
        if rom_name is None or rom_name[:6] != b"SAI2AP":
            return False

        ctx.game = self.game
        ctx.items_handling = 0b001
        ctx.rom = rom_name
        return True

    async def game_watcher(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        item_received = await snes_read(ctx, ITEM_RECEIVED, 0x1)
        goal_flag = await snes_read(ctx, GOALFLAG, 0x1)
        scout_flag = await snes_read(ctx, CHEST_SCOUT_MODE, 2)
        scout_id = struct.unpack("H", scout_flag)[0]
        special_scout_flag = await snes_read(ctx, SPECIAL_CHEST_SCOUT, 2)
        special_scout_id = struct.unpack("H", special_scout_flag)[0]
        in_game = await snes_read(ctx, IN_GAME, 0x1)
        locations_scouted_flag = await snes_read(ctx, LOCATIONS_SCOUTED_FLAG, 0x1)

        if in_game is None:
            return

        elif in_game[0] != 0x01:
            return

        elif item_received[0] > 0x00:
            return

        from .Rom import input_item_ids
        rom = await snes_read(ctx, SAI2_ROMHASH_START, ROMHASH_SIZE)
        if rom != ctx.rom:
            ctx.rom = None
            return

        if goal_flag[0] != 0x00:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

        if locations_scouted_flag[0] == 0x00:
            for location in location_list:
                await ctx.send_msgs([{"cmd": 'LocationScouts', "locations": location_list, "create_as_hint": 0}])
                snes_buffered_write(ctx, WRAM_START + 0x04C4, bytes([0x01]))

        if scout_id != 0x0000:
            scout_id = hex(scout_id)
            scout_id = scout_id[2:]
            scout_id = int(scout_id, 16)
            if scout_id in scout_location_map:
                location = ctx.locations_info[scout_location_map[scout_id]] #convert the stored internal ID to the corresponding AP location id
                item = ctx.item_names[location.item]
                if item in sprite_visuals:
                    local_sprite = bytearray(0)
                    local_sprite.extend(sprite_visuals[item])
                    snes_buffered_write(ctx, WRAM_START + 0x04FC, local_sprite)#If the item is a nonlocal SAI2 item, use its in-game sprite but act like an ap item
                    snes_buffered_write(ctx, WRAM_START + 0x04FB, bytes([0x01]))
                else:
                    snes_buffered_write(ctx, WRAM_START + 0x04FB, bytes([0x00]))
                item = item.upper()
                sai2_item = bytearray(0)
                for char in item:
                    if char in hud_encoding_table:
                        sai2_item.extend (hud_encoding_table[char])
                    else:
                        sai2_item.extend ([0x8F, 0x2C])
                if len(item) <= 16:
                    for _ in range(16 - len(item)):
                        sai2_item.extend([0x90, 0x28])
                snes_buffered_write(ctx, SRAM_START + 0x7E4D, sai2_item)#write item name as ingame text
            snes_buffered_write(ctx, CHEST_SCOUT_MODE, bytes([0x00]))
            snes_buffered_write(ctx, CHEST_SCOUT_MODE + 1, bytes([0x00]))

        if special_scout_id != 0x000:
            special_scout_id = hex(special_scout_id)
            special_scout_id = special_scout_id[2:]
            special_scout_id = int(special_scout_id, 16)
            print(special_scout_id)
            if special_scout_id in shop_scouts:
                location = ctx.locations_info[shop_scouts[special_scout_id]] #I can probably make a function out of this and the normal one
                item = ctx.item_names[location.item]
                item = item[:21]
                player = ctx.player_names[location.player]
                player = player[:21]
                sai2_item = bytearray(0)
                sai2_player = bytearray(0)
                for char in item: #I can probably make a function out of this
                    if char in plain_encoding_table:
                        sai2_item.extend (plain_encoding_table[char])
                    else:
                        sai2_item.extend ([0x8F, 0x2C])
                sai2_item.extend([0xFF, 0x03])
                for char in player: #I can probably make a function out of this
                    if char in plain_encoding_table:
                        sai2_player.extend (plain_encoding_table[char])
                    else:
                        sai2_player.extend ([0x8F, 0x2C])
                        
                sai2_player.extend([0xFF, 0x03])
                snes_buffered_write(ctx, SRAM_START + 0x7DF0, sai2_item)#write item name as ingame text
                snes_buffered_write(ctx, SRAM_START + 0x7E44, sai2_player)#write item name as ingame text
            elif special_scout_id in special_chests:
                location = ctx.locations_info[special_chests[special_scout_id]] #I can probably make a function out of this and the normal one
                print(location)
                item = ctx.item_names[location.item]
                if item in sprite_visuals:
                    print(item)
                    local_sprite = bytearray(0)
                    local_sprite.extend(sprite_visuals[item])
                    print(local_sprite)
                    snes_buffered_write(ctx, WRAM_START + 0x04FC, local_sprite)#If the item is a nonlocal SAI2 item, use its in-game sprite but act like an ap item
                    snes_buffered_write(ctx, WRAM_START + 0x04FB, bytes([0x01]))
                else:
                    snes_buffered_write(ctx, WRAM_START + 0x04FB, bytes([0x00]))
                item = item.upper()
                sai2_item = bytearray(0)
                for char in item:
                    if char in hud_encoding_table:
                        sai2_item.extend (hud_encoding_table[char])
                    else:
                        sai2_item.extend ([0x8F, 0x2C])
                if len(item) <= 16:
                    for _ in range(16 - len(item)):
                        sai2_item.extend([0x90, 0x28])
                snes_buffered_write(ctx, SRAM_START + 0x7E4D, sai2_item)#write item name as ingame text
            snes_buffered_write(ctx, SPECIAL_CHEST_SCOUT, bytes([0x00]))
            snes_buffered_write(ctx, SPECIAL_CHEST_SCOUT + 1, bytes([0x00]))

        new_checks = []
        from .Rom import location_flag_table

        location_ram_data = await snes_read(ctx, WRAM_START + 0x460, 0xF0)
        for loc_id, loc_data in location_flag_table.items():
            if loc_id not in ctx.locations_checked:
                data = location_ram_data[loc_data[0] - 0x460]
                masked_data = data & (1 << loc_data[1])
                bit_set = masked_data != 0
                invert_bit = ((len(loc_data) >= 3) and loc_data[2])
                if bit_set != invert_bit:
                    new_checks.append(loc_id)
        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names[new_check_id]
            snes_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])

        recv_count = await snes_read(ctx, ITEMQUEUE_HIGH, 2)
        recv_index = struct.unpack("H", recv_count)[0]
        if recv_index < len(ctx.items_received):
            item = ctx.items_received[recv_index]
            recv_index += 1
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names[item.item], 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names[item.location], recv_index, len(ctx.items_received)))

            snes_buffered_write(ctx, ITEMQUEUE_HIGH, pack("H", recv_index))
            if item.item in input_item_ids:
                item_count = await snes_read(ctx, WRAM_START + input_item_ids[item.item][0], 0x1)
                increment = input_item_ids[item.item][1]
                new_item_count = item_count[0]
                if increment > 1:
                    new_item_count = increment
                else:
                    new_item_count += increment

                snes_buffered_write(ctx, WRAM_START + input_item_ids[item.item][0], bytes([new_item_count]))
        await snes_flush_writes(ctx)

def get_shop_text(special_id, ctx, SRAM_START):
    location = ctx.locations_info[shop_scouts[special_id]]
    item = ctx.item_names[location.item]
    player = ctx.player_names[location.player]
    sai2_item = bytearray(0)
    for char in item:
        if char in hud_encoding_table:
            sai2_item.extend (hud_encoding_table[char])
        else:
            sai2_item.extend ([0x8F, 0x2C])
    if len(item) <= 16:
        for _ in range(16 - len(item)):
            sai2_item.extend([0x90, 0x28])
    snes_buffered_write(ctx, SRAM_START + 0x7E4D, sai2_item)#write item name as ingame text