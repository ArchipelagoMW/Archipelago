import logging
import asyncio
import time

from NetUtils import ClientStatus, color
from worlds import AutoWorldRegister
from SNIClient import Context, snes_buffered_write, snes_flush_writes, snes_read
from .Names.TextBox import generate_received_text
from Patch import GAME_SMW

snes_logger = logging.getLogger("SNES")

ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

SAVEDATA_START = WRAM_START + 0xF000
SAVEDATA_SIZE = 0x500

SMW_ROMHASH_START = 0x7FC0
ROMHASH_SIZE = 0x15

SMW_PROGRESS_DATA     = WRAM_START + 0x1F02
SMW_DRAGON_COINS_DATA = WRAM_START + 0x1F2F
SMW_EVENT_ROM_DATA    = ROM_START + 0x2D608

SMW_GOAL_DATA              = ROM_START + 0x01BFA0
SMW_REQUIRED_BOSSES_DATA   = ROM_START + 0x01BFA1
SMW_REQUIRED_EGGS_DATA     = ROM_START + 0x01BFA2
SMW_SEND_MSG_DATA          = ROM_START + 0x01BFA3
SMW_RECEIVE_MSG_DATA       = ROM_START + 0x01BFA4
SMW_DEATH_LINK_ACTIVE_ADDR = ROM_START + 0x01BFA5

SMW_GAME_STATE_ADDR    = WRAM_START + 0x100
SMW_MARIO_STATE_ADDR   = WRAM_START + 0x71
SMW_CURRENT_LEVEL_ADDR = WRAM_START + 0x13BF
SMW_MESSAGE_BOX_ADDR   = WRAM_START + 0x1426
SMW_EGG_COUNT_ADDR     = WRAM_START + 0xF48
SMW_SFX_ADDR           = WRAM_START + 0x1DFC
SMW_PAUSE_ADDR         = WRAM_START + 0x13D4
SMW_MESSAGE_QUEUE_ADDR = WRAM_START + 0xC391

SMW_RECV_PROGRESS_ADDR = WRAM_START + 0x1F2B

SMW_GOAL_LEVELS          = [0x28, 0x31, 0x32]
SMW_INVALID_MARIO_STATES = [0x05, 0x06, 0x0A, 0x0C, 0x0D]

async def deathlink_kill_player(ctx: Context):
    if ctx.game == GAME_SMW:
        game_state = await snes_read(ctx, SMW_GAME_STATE_ADDR, 0x1)
        if game_state[0] != 0x14:
            return

        mario_state = await snes_read(ctx, SMW_MARIO_STATE_ADDR, 0x1)
        if mario_state[0] != 0x00:
            return

        message_box = await snes_read(ctx, SMW_MESSAGE_BOX_ADDR, 0x1)
        if message_box[0] != 0x00:
            return

        pause_state = await snes_read(ctx, SMW_PAUSE_ADDR, 0x1)
        if pause_state[0] != 0x00:
            return

        snes_buffered_write(ctx, WRAM_START + 0x9D, bytes([0x30])) # Freeze Gameplay
        snes_buffered_write(ctx, WRAM_START + 0x1DFB, bytes([0x09])) # Death Music
        snes_buffered_write(ctx, WRAM_START + 0x0DDA, bytes([0xFF])) # Flush Music Buffer
        snes_buffered_write(ctx, WRAM_START + 0x1407, bytes([0x00])) # Flush Cape Fly Phase
        snes_buffered_write(ctx, WRAM_START + 0x140D, bytes([0x00])) # Flush Spin Jump Flag
        snes_buffered_write(ctx, WRAM_START + 0x188A, bytes([0x00])) # Flush Empty Byte because the game does it
        snes_buffered_write(ctx, WRAM_START + 0x7D, bytes([0x90])) # Mario Y Speed
        snes_buffered_write(ctx, WRAM_START + 0x1496, bytes([0x30])) # Death Timer
        snes_buffered_write(ctx, SMW_MARIO_STATE_ADDR, bytes([0x09])) # Mario State -> Dead

        await snes_flush_writes(ctx)

        from SNIClient import DeathState
        ctx.death_state = DeathState.dead
        ctx.last_death_link = time.time()

        return


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

        receive_option = await snes_read(ctx, SMW_RECEIVE_MSG_DATA, 0x1)
        send_option = await snes_read(ctx, SMW_SEND_MSG_DATA, 0x1)

        ctx.receive_option = receive_option[0]
        ctx.send_option = send_option[0]

        ctx.allow_collect = True

        death_link = await snes_read(ctx, SMW_DEATH_LINK_ACTIVE_ADDR, 1)
        if death_link:
            await ctx.update_death_link(bool(death_link[0] & 0b1))
    return True


def add_message_to_queue(ctx: Context, new_message):

    if not hasattr(ctx, "message_queue"):
        ctx.message_queue = []

    ctx.message_queue.append(new_message)

    return


async def handle_message_queue(ctx: Context):

    game_state = await snes_read(ctx, SMW_GAME_STATE_ADDR, 0x1)
    if game_state[0] != 0x14:
        return

    mario_state = await snes_read(ctx, SMW_MARIO_STATE_ADDR, 0x1)
    if mario_state[0] != 0x00:
        return

    message_box = await snes_read(ctx, SMW_MESSAGE_BOX_ADDR, 0x1)
    if message_box[0] != 0x00:
        return

    pause_state = await snes_read(ctx, SMW_PAUSE_ADDR, 0x1)
    if pause_state[0] != 0x00:
        return

    if not hasattr(ctx, "message_queue") or len(ctx.message_queue) == 0:
        return

    next_message = ctx.message_queue.pop(0)

    snes_buffered_write(ctx, SMW_MESSAGE_QUEUE_ADDR, bytes(next_message))
    snes_buffered_write(ctx, SMW_MESSAGE_BOX_ADDR, bytes([0x03]))
    snes_buffered_write(ctx, SMW_SFX_ADDR, bytes([0x22]))

    await snes_flush_writes(ctx)

    return


async def smw_game_watcher(ctx: Context):
    if ctx.game == GAME_SMW:
        # SMW_TODO: Handle Deathlink
        game_state = await snes_read(ctx, SMW_GAME_STATE_ADDR, 0x1)
        mario_state = await snes_read(ctx, SMW_MARIO_STATE_ADDR, 0x1)
        if game_state is None:
            # We're not properly connected
            return
        elif game_state[0] >= 0x18:
            if not ctx.finished_game:
                current_level = await snes_read(ctx, SMW_CURRENT_LEVEL_ADDR, 0x1)

                if current_level[0] in SMW_GOAL_LEVELS:
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    ctx.finished_game = True
            return
        elif game_state[0] < 0x0B:
            # We haven't loaded a save file
            return
        elif mario_state[0] in SMW_INVALID_MARIO_STATES:
            # Mario can't come to the phonee right now
            return

        if "DeathLink" in ctx.tags and game_state[0] == 0x14 and ctx.last_death_link + 1 < time.time():
            currently_dead = mario_state[0] == 0x09
            await ctx.handle_deathlink_state(currently_dead)

        # Check for Egg Hunt ending
        goal = await snes_read(ctx, SMW_GOAL_DATA, 0x1)
        if game_state[0] == 0x14 and goal[0] == 1:
            current_level = await snes_read(ctx, SMW_CURRENT_LEVEL_ADDR, 0x1)
            message_box = await snes_read(ctx, SMW_MESSAGE_BOX_ADDR, 0x1)
            egg_count = await snes_read(ctx, SMW_EGG_COUNT_ADDR, 0x1)
            required_egg_count = await snes_read(ctx, SMW_REQUIRED_EGGS_DATA, 0x1)

            if current_level[0] == 0x28 and message_box[0] == 0x01 and egg_count[0] >= required_egg_count[0]:
                snes_buffered_write(ctx, WRAM_START + 0x13C6, bytes([0x08]))
                snes_buffered_write(ctx, WRAM_START + 0x13CE, bytes([0x01]))
                snes_buffered_write(ctx, WRAM_START + 0x1DE9, bytes([0x01]))
                snes_buffered_write(ctx, SMW_GAME_STATE_ADDR, bytes([0x18]))

                await snes_flush_writes(ctx)
                return

        await handle_message_queue(ctx)

        new_checks = []
        event_data = await snes_read(ctx, SMW_EVENT_ROM_DATA, 0x60)
        progress_data = await snes_read(ctx, SMW_PROGRESS_DATA, 0x0F)
        dragon_coins_data = await snes_read(ctx, SMW_DRAGON_COINS_DATA, 0x0C)
        from worlds.smw.Rom import item_rom_data, ability_rom_data
        from worlds.smw.Levels import location_id_to_level_id
        for loc_name, level_data in location_id_to_level_id.items():
            loc_id = AutoWorldRegister.world_types[ctx.game].location_name_to_id[loc_name]
            if loc_id not in ctx.locations_checked:

                event_id = event_data[level_data[0]]

                if level_data[1] == 2:
                    # Dragon Coins Check

                    progress_byte = (level_data[0] // 8)
                    progress_bit  = 7 - (level_data[0] % 8)

                    data = dragon_coins_data[progress_byte]
                    masked_data = data & (1 << progress_bit)
                    bit_set = (masked_data != 0)

                    if bit_set:
                        # SMW_TODO: Handle non-included checks
                        new_checks.append(loc_id)
                else:
                    event_id_value = event_id + level_data[1]

                    progress_byte = (event_id_value // 8)
                    progress_bit  = 7 - (event_id_value % 8)

                    data = progress_data[progress_byte]
                    masked_data = data & (1 << progress_bit)
                    bit_set = (masked_data != 0)

                    if bit_set:
                        # SMW_TODO: Handle non-included checks
                        new_checks.append(loc_id)

        verify_game_state = await snes_read(ctx, SMW_GAME_STATE_ADDR, 0x1)
        if verify_game_state is None or verify_game_state[0] < 0x0B or verify_game_state[0] > 0x29:
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

        if game_state[0] != 0x14:
            # Don't receive items outside of in-level mode
            return

        recv_count = await snes_read(ctx, SMW_RECV_PROGRESS_ADDR, 1)
        recv_index = recv_count[0]

        if recv_index < len(ctx.items_received):
            item = ctx.items_received[recv_index]
            recv_index += 1
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names[item.item], 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names[item.location], recv_index, len(ctx.items_received)))

            if ctx.receive_option == 1 or (ctx.receive_option == 2 and ((item.flags & 1) != 0)):
                item_name = ctx.item_names[item.item]
                player_name = ctx.player_names[item.player]

                receive_message = generate_received_text(item_name, player_name)
                add_message_to_queue(ctx, receive_message)

            snes_buffered_write(ctx, SMW_RECV_PROGRESS_ADDR, bytes([recv_index]))
            if item.item in item_rom_data:
                if not (item.item == 0xBC0002 and goal[0] != 1) and not (item.item == 0xBC0012 and goal[0] != 0):
                    # Don't handle Yoshi Eggs in Bowser Goal or Boss Tokens in Yoshi Egg Hunt Goal

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
            elif item.item in ability_rom_data:
                # Handle Upgrades
                for rom_data in ability_rom_data[item.item]:
                    data = await snes_read(ctx, WRAM_START + rom_data[0], 1)
                    masked_data = data[0] | (1 << rom_data[1])
                    snes_buffered_write(ctx, WRAM_START + rom_data[0], bytes([masked_data]))
                    snes_buffered_write(ctx, SMW_SFX_ADDR, bytes([0x3E])) # SMW_TODO: Custom sounds for each
            elif item.item == 0xBC000A:
                # Handle Progressive Powerup
                data = await snes_read(ctx, WRAM_START + 0x1F2D, 1)
                mushroom_data = data[0] & (1 << 0)
                fire_flower_data = data[0] & (1 << 1)
                cape_data = data[0] & (1 << 2)
                if mushroom_data == 0:
                    masked_data = data[0] | (1 << 0)
                    snes_buffered_write(ctx, WRAM_START + 0x1F2D, bytes([masked_data]))
                    snes_buffered_write(ctx, SMW_SFX_ADDR, bytes([0x3E]))
                elif fire_flower_data == 0:
                    masked_data = data[0] | (1 << 1)
                    snes_buffered_write(ctx, WRAM_START + 0x1F2D, bytes([masked_data]))
                    snes_buffered_write(ctx, SMW_SFX_ADDR, bytes([0x3E]))
                elif cape_data == 0:
                    masked_data = data[0] | (1 << 2)
                    snes_buffered_write(ctx, WRAM_START + 0x1F2D, bytes([masked_data]))
                    snes_buffered_write(ctx, SMW_SFX_ADDR, bytes([0x41]))
                else:
                    # Extra Powerup?
                    pass
            elif item.item == 0xBC0015:
                # Handle Literature Trap
                from .Names.LiteratureTrap import lit_trap_text_list
                import random
                rand_trap = random.choice(lit_trap_text_list)

                for message in rand_trap:
                    add_message_to_queue(ctx, message)

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

