import logging
import time
import random
from enum import Enum
from NetUtils import ClientStatus, NetworkItem, color
from worlds.AutoSNIClient import SNIClient, SnesReader, SnesData, Read
from .Names.TextBox import generate_received_text, generate_received_trap_link_text
from .Items import trap_value_to_name, trap_name_to_value
from .Locations import sorted_locations_table
from .Levels import level_info_dict

snes_logger = logging.getLogger("SNES")

from typing import TYPE_CHECKING, Dict, Any, Set

if TYPE_CHECKING:
    from SNIClient import SNIContext

# FXPAK Pro protocol memory mapping used by SNI
ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

SMW_BWRAM = SRAM_START + 0x4000

SMW_ROMHASH_START = 0x7FC0
ROMHASH_SIZE = 0x15

SMW_PROGRESS_DATA           = SRAM_START + 0x1F02
SMW_DRAGON_COINS_DATA       = SRAM_START + 0x1F2F
SMW_PATH_DATA               = SRAM_START + 0x1EA2
SMW_EVENT_ROM_DATA          = ROM_START + 0x2D608
SMW_ACTIVE_LEVEL_DATA       = ROM_START + 0x37F70
SMW_MOON_DATA               = SRAM_START + 0x1FEE
SMW_HIDDEN_1UP_DATA         = SRAM_START + 0x1F3C
SMW_BONUS_BLOCK_DATA        = SMW_BWRAM + 0x0000
SMW_BLOCKSANITY_DATA        = SMW_BWRAM + 0x0400
SMW_BLOCKSANITY_FLAGS       = SMW_BWRAM + 0x0010
SMW_MIDWAY_POINT_FLAGS      = SMW_BWRAM + 0x0020
SMW_LEVEL_CLEAR_FLAGS       = SMW_BWRAM + 0x0200
SMW_SPECIAL_WORLD_CLEAR     = SRAM_START + 0x1F1E
SMW_ENERGY_LINK_TRANSFER    = SMW_BWRAM + 0x0CF6
SMW_ENERGY_LINK_PURCHASE    = SMW_BWRAM + 0x0CF8
SMW_ENERGY_LINK_ITEM        = SMW_BWRAM + 0x0CFA
SMW_ENERGY_LINK_REPLY       = SMW_BWRAM + 0x0CFB
SMW_ENERGY_LINK_COUNT       = SMW_BWRAM + 0x0CFC
SMW_TRAP_REPELLENT          = SMW_BWRAM + 0x0383

SMW_GOAL_DATA                = ROM_START + 0x01BFA0
SMW_REQUIRED_BOSSES_DATA     = ROM_START + 0x01BFA1
SMW_REQUIRED_EGGS_DATA       = ROM_START + 0x01BFA2
SMW_SEND_MSG_DATA            = ROM_START + 0x01BFA3
SMW_RECEIVE_MSG_DATA         = ROM_START + 0x01BFA4
SMW_DEATH_LINK_ACTIVE_ADDR   = ROM_START + 0x01BFA5
SMW_DRAGON_COINS_ACTIVE_ADDR = ROM_START + 0x01BFA6
SMW_SWAMP_DONUT_GH_ADDR      = ROM_START + 0x01BFA7
SMW_MOON_ACTIVE_ADDR         = ROM_START + 0x01BFA8
SMW_HIDDEN_1UP_ACTIVE_ADDR   = ROM_START + 0x01BFA9
SMW_BONUS_BLOCK_ACTIVE_ADDR  = ROM_START + 0x01BFAA
SMW_BLOCKSANITY_ACTIVE_ADDR  = ROM_START + 0x01BFAB
SMW_ENERGY_LINK_ENABLED      = ROM_START + 0x01BFB4
SMW_TRAP_LINK_ACTIVE_ADDR    = ROM_START + 0x01BFB7
SMW_RING_LINK_ACTIVE_ADDR    = ROM_START + 0x01BFB8
SMW_SWAPPED_EXITS_DATA       = ROM_START + 0x1189DF

SMW_GAME_STATE_ADDR       = SRAM_START + 0x0100
SMW_MARIO_STATE_ADDR      = SRAM_START + 0x71
SMW_BOSS_STATE_ADDR       = SRAM_START + 0x0D9B
SMW_ACTIVE_BOSS_ADDR      = SRAM_START + 0x13FC
SMW_CURRENT_LEVEL_ADDR    = SRAM_START + 0x13BF
SMW_CURRENT_SUBLEVEL_ADDR = SRAM_START + 0x010B
SMW_MESSAGE_BOX_ADDR      = SRAM_START + 0x1426
SMW_BONUS_STAR_ADDR       = SRAM_START + 0x0F48
SMW_EGG_COUNT_ADDR        = SRAM_START + 0x1F24
SMW_BOSS_COUNT_ADDR       = SRAM_START + 0x1F26
SMW_NUM_EVENTS_ADDR       = SRAM_START + 0x1F2E
SMW_SFX_ADDR              = SRAM_START + 0x1DFC
SMW_PAUSE_ADDR            = SRAM_START + 0x13D4
SMW_MESSAGE_QUEUE_ADDR    = SMW_BWRAM + 0x1000 + 0x0191
SMW_ACTIVE_THWIMP_ADDR    = SMW_BWRAM + 0x0303
SMW_GOAL_ITEM_COUNT       = SMW_BWRAM + 0x01E
SMW_COIN_COUNT_ADDR       = SMW_BWRAM + 0x0DBE

SMW_STATE_MIRROR = SRAM_START + 0x18000
SMW_BWRAM_PROGRESS = SRAM_START + 0x1F00

SMW_RECV_PROGRESS_ADDR = SRAM_START + 0x01F2B

SMW_BLOCKSANITY_BLOCK_COUNT = 652

SMW_EXCHANGE_RATE = 300000000

SMW_GOAL_LEVELS                = [0x28, 0x31, 0x32]
SMW_INVALID_MARIO_STATES       = [0x05, 0x06, 0x0A, 0x0C, 0x0D]
SMW_BAD_TEXT_BOX_LEVELS        = [0x00, 0x26, 0x02, 0x4B]
SMW_BOSS_STATES                = [0x80, 0xC0, 0xC1]
SMW_UNCOLLECTABLE_LEVELS       = []
SMW_UNCOLLECTABLE_DRAGON_COINS = [0x24]
LEVELS_WITHOUT_CHECKS          = [0x00, 0x03, 0x31, 0x32, 0x28]
TRAPLESS_LEVELS                = [0x00, 0x03, 0x28]

class SMWMemory(Enum):
    settings = Read(SMW_GOAL_DATA, 0x20)
    recv_count = Read(SMW_RECV_PROGRESS_ADDR, 0x02)
    state_mirror = Read(SMW_STATE_MIRROR, 0x10)
    game_progress = Read(SMW_BWRAM_PROGRESS, 0x0100)
    event_count = Read(SMW_NUM_EVENTS_ADDR, 0x01)
    event_data = Read(SMW_EVENT_ROM_DATA, 0x60)
    path_data = Read(SMW_PATH_DATA, 0x60)
    active_level_data = Read(SMW_ACTIVE_LEVEL_DATA, 0x60)
    flags_data = Read(SMW_BWRAM, 0x0400)
    blocksanity_data = Read(SMW_BLOCKSANITY_DATA, SMW_BLOCKSANITY_BLOCK_COUNT)
    current_coins = Read(SMW_COIN_COUNT_ADDR, 0x01)
    current_lives = Read(SRAM_START + 0x18E4, 0x01)
    energy_link_packet = Read(SMW_ENERGY_LINK_TRANSFER, 0x02)
    inventory_reply = Read(SMW_ENERGY_LINK_REPLY, 0x01)
    inventory_item = Read(SMW_ENERGY_LINK_ITEM, 0x01)
    inventory_purchase = Read(SMW_ENERGY_LINK_PURCHASE, 0x02)
    trap_repellent = Read(SMW_TRAP_REPELLENT, 0x01)

class ConnectMemory(Enum):
    settings = Read(SMW_GOAL_DATA, 0x20)
    rom_name = Read(SMW_ROMHASH_START, ROMHASH_SIZE)

class TrapMemory(Enum):
    ice_trap = Read(SRAM_START + 0x4308, 0x01)
    stun_trap = Read(SRAM_START + 0x18BD, 0x01)
    timer_trap = Read(SRAM_START + 0x0F31, 0x03)
    reverse_trap = Read(SRAM_START + 0x4300, 0x01)
    thwimp_trap = Read(SRAM_START + 0x4302, 0x01)
    thwimp_trap_active = Read(SRAM_START + 0x4303, 0x01)
    fishing_boo_trap = Read(SRAM_START + 0x4305, 0x01)
    screen_flip_trap = Read(SRAM_START + 0x430A, 0x01)
    sticky_floor_trap = Read(SRAM_START + 0x430C, 0x01)
    sticky_hands_trap = Read(SRAM_START + 0x430E, 0x01)
    pixelate_trap = Read(SRAM_START + 0x4310, 0x01)
    spotlight_trap = Read(SRAM_START + 0x4312, 0x01)

class WaffleSNIClient(SNIClient):
    game = "SMW: Spicy Mycena Waffles"
    patch_suffix = ".apwaffle"
    slot_data: Dict[str, Any]
    snes_reader = SnesReader(SMWMemory)
    connect_reader = SnesReader(ConnectMemory)
    trap_reader = SnesReader(TrapMemory)
    locations_checked: Set[int]
    priority_trap: NetworkItem | None
    energy_link_enabled: bool
    current_sublevel_value: int
    inventory_purchase: str
    inventory_tag: str
    inventory_refund: int
    inventory_cost: int
    locations_checked: Set[int]
    visited_levels: Set[int]

    def __init__(self):
        super().__init__()
        self.priority_trap = None
        self.energy_link_enabled = False
        self.inventory_purchase = ""
        self.inventory_tag = ""
        self.inventory_refund = 0
        self.inventory_cost = 0
        self.visited_levels = set()

    async def deathlink_kill_player(self, ctx: "SNIContext"):
        from SNIClient import DeathState, snes_buffered_write, snes_flush_writes

        snes_data = await self.snes_reader.read(ctx)
        if snes_data is None:
            return
        
        state_mirror = snes_data.get(SMWMemory.state_mirror)

        # If were not in a level
        if state_mirror[0x00] != 0x14:
            return
        # Or Mario isn't in a playable state
        if state_mirror[0x01] != 0x00:
            return
        # Or a Message Box is showing
        if state_mirror[0x07] != 0x00:
            return
        # Or are in pause
        if state_mirror[0x09] != 0x00:
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

        ctx.death_state = DeathState.dead
        ctx.last_death_link = time.time()


    async def validate_rom(self, ctx: "SNIContext"):
        snes_data = await self.connect_reader.read(ctx)
        if snes_data is None:
            return False
        
        rom_name = snes_data.get(ConnectMemory.rom_name)
        settings = snes_data.get(ConnectMemory.settings)

        if rom_name == bytes([0] * ROMHASH_SIZE) or rom_name[:7] != b"WAFFLES":
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111  # remote items

        ctx.receive_option = settings[0x04]
        ctx.send_option = settings[0x03]

        ctx.allow_collect = True

        #if bool(settings[0x05] & 0b1):
        #    await ctx.update_death_link(True)

        if bool(settings[0x14] & 0b1) and "EnergyLink" not in ctx.tags:
            ctx.tags.add("EnergyLink")
            await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}])

        if bool(settings[0x17] & 0b1) and "TrapLink" not in ctx.tags:
            ctx.tags.add("TrapLink")
            await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}])

        if bool(settings[0x18] & 0b1) and "RingLink" not in ctx.tags:
            ctx.tags.add("RingLink")
            await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}])

        if ctx.rom != rom_name:
            ctx.current_sublevel_value = 0
            ctx.visited_levels = []

        ctx.rom = rom_name

        return True


    async def handle_ring_link(self, ctx: "SNIContext", snes_data: SnesData[SMWMemory]):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        if "RingLink" not in ctx.tags:
            return

        if not hasattr(self, "prev_coins"):
            self.prev_coins = 0

        curr_coins = int.from_bytes(snes_data.get(SMWMemory.current_coins), "little")
        curr_lives = int.from_bytes(snes_data.get(SMWMemory.current_lives), "little")

        if curr_coins < self.prev_coins:
            # Coins rolled over from 1-Up
            curr_coins += 100

        coins_diff = curr_coins - self.prev_coins
        if coins_diff > 0:
            await self.send_ring_link(ctx, snes_data, coins_diff)
            self.prev_coins = curr_coins % 100

        new_coins = curr_coins
        if not hasattr(self, "pending_ring_link"):
            self.pending_ring_link = 0

        if self.pending_ring_link != 0:
            new_coins += self.pending_ring_link
            new_coins = max(new_coins, 0)

            new_1_ups = 0
            while new_coins >= 100:
                new_1_ups += 1
                new_coins -= 100

            if new_1_ups > 0:
                new_lives_inc = curr_lives + new_1_ups
                snes_buffered_write(ctx, SRAM_START + 0x18E4, bytes([new_lives_inc]))

            snes_buffered_write(ctx, SMW_COIN_COUNT_ADDR, bytes([new_coins]))
            if self.pending_ring_link > 0:
                snes_buffered_write(ctx, SMW_SFX_ADDR, bytes([0x01]))
            else:
                snes_buffered_write(ctx, SMW_SFX_ADDR, bytes([0x2A]))
            self.pending_ring_link = 0
            self.prev_coins = new_coins

            await snes_flush_writes(ctx)

    async def game_watcher(self, ctx: "SNIContext"):
        from SNIClient import snes_buffered_write, snes_flush_writes

        snes_data = await self.snes_reader.read(ctx)
        if snes_data is None:
            return
        
        rom_settings_data = snes_data.get(SMWMemory.settings)
        state_mirror = snes_data.get(SMWMemory.state_mirror)
        game_progress = snes_data.get(SMWMemory.game_progress)
        
        game_state = state_mirror[0x00]
        mario_state = state_mirror[0x01]

        if game_state >= 0x18:
            if not ctx.finished_game:
                current_level = state_mirror[0x04]

                if current_level in SMW_GOAL_LEVELS:
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    ctx.finished_game = True
            return
        elif game_state < 0x0B:
            # We haven't loaded a save file
            ctx.current_sublevel_value = 0
            ctx.visited_levels = []
            return
        elif mario_state in SMW_INVALID_MARIO_STATES:
            # Mario can't come to the phone right now
            return

        #if "DeathLink" in ctx.tags and game_state == 0x14 and ctx.last_death_link + 1 < time.time():
        #    currently_dead = mario_state == 0x09
        #    await ctx.handle_deathlink_state(currently_dead)

        # Check for Egg Hunt ending
        goal = rom_settings_data[0x00]
        current_level = state_mirror[0x04]

        egg_count = game_progress[0x24]
        boss_count = game_progress[0x26]
        display_count = state_mirror[0x08]
        
        if goal & 0x02 and egg_count > display_count:
            snes_buffered_write(ctx, SMW_BONUS_STAR_ADDR, bytes([egg_count]))
            await snes_flush_writes(ctx)
        elif goal & 0x01 and boss_count > display_count:
            snes_buffered_write(ctx, SMW_BONUS_STAR_ADDR, bytes([boss_count]))
            await snes_flush_writes(ctx)

        await self.handle_message_queue(ctx)

        trap_repellent = int.from_bytes(snes_data.get(SMWMemory.trap_repellent), "little")
        if current_level not in TRAPLESS_LEVELS and trap_repellent == 0:
            await self.handle_trap_queue(ctx)

        await self.handle_ring_link(ctx, snes_data)

        if "EnergyLink" in ctx.tags and f"EnergyLink{ctx.team}" in ctx.stored_data and game_state >= 0x0D:
            await self.handle_energy_link(ctx, snes_data)

        event_data = list(snes_data.get(SMWMemory.event_data))
        flags_data = list(snes_data.get(SMWMemory.flags_data))
        blocksanity_data = list(snes_data.get(SMWMemory.blocksanity_data))

        new_checks = []
        progress_data = list(game_progress[0x02:0x02+0x0F])
        dragon_coins_data = list(game_progress[0x2F:0x2F+0x0C])
        moon_data = list(game_progress[0xEE:0xEE+0x0C])
        hidden_1up_data = list(game_progress[0x3C:0x3C+0x0C])
        prize_block_data = list(flags_data[0x00:0x00+0x0C])
        blocksanity_flags = list(flags_data[0x10:0x10+0x0C])
        dragon_coins_active = rom_settings_data[0x06]
        moon_active = rom_settings_data[0x08]
        hidden_1up_active = rom_settings_data[0x09]
        prize_block_active = rom_settings_data[0x0A]
        blocksanity_active = rom_settings_data[0x0B]
        midway_points_active = rom_settings_data[0x0C]
        rooms_active = rom_settings_data[0x0D]
        midway_point_data = list(flags_data[0x20:0x20+0x0C])

        current_sublevel_value = int.from_bytes(state_mirror[0x05:0x07], "little")

        # Do not process ANYTHING if the level is 0 or outside of the usual range
        if current_level not in LEVELS_WITHOUT_CHECKS and current_level < 0x60:
            # Preprocess some indexes
            progress_byte = current_level // 8
            progress_bit = 7 - (current_level % 8)

            for loc_id in sorted_locations_table[current_level]:
                # Early discard already checked locations
                if loc_id in ctx.locations_checked:
                    continue

                # Get info from the location ID
                level_id = loc_id >> 24
                loc_type = (loc_id >> 20 & 0x0F)
                loc_data = loc_id & 0x000FFFFF
                data = 0

                # Exits
                if loc_type == 0x00 or loc_type == 0x01:
                    event_id = event_data[level_id] + (loc_type & 0x01)
                    event_progress_byte = event_id // 8
                    event_progress_bit = 7 - (event_id % 8)
                    data = progress_data[event_progress_byte]
                    masked_data = data & (1 << event_progress_bit)
                    if masked_data:
                        new_checks.append(loc_id)
                        new_checks.append(loc_id | 0x01)
                    continue
                # Item from block
                elif loc_type == 0x0A and blocksanity_active:
                    block_index = loc_data & 0x0FFFF
                    if blocksanity_data[block_index]:
                        new_checks.append(loc_id)
                    continue
                # Room visited
                elif loc_type == 0x08 and rooms_active:
                    room_type = (loc_data & 0xF000) >> 12
                    # Regular rooms
                    if room_type == 0x00:
                        if loc_data == current_sublevel_value:
                            new_checks.append(loc_id)
                    # Similar rooms
                    elif room_type == 0x01:
                        loc_data &= 0x0FFF
                        if loc_data == current_sublevel_value or loc_data + 0x01 == current_sublevel_value:
                            new_checks.append(loc_id)
                    # Wing rooms 
                    elif room_type == 0x02:
                        if loc_data & 0x00FF == current_sublevel_value & 0x00FF:
                            new_checks.append(loc_id)
                    else:
                        continue
                # Dragon coins
                elif loc_type == 0x03 and dragon_coins_active:
                    data = dragon_coins_data[progress_byte]
                # 3-Up Moon
                elif loc_type == 0x04 and moon_active:
                    data = moon_data[progress_byte]
                # Hidden 1-Ups
                elif loc_type == 0x05 and hidden_1up_active:
                    data = hidden_1up_data[progress_byte]
                # Midway Point
                elif loc_type == 0x06 and midway_points_active:
                    data = midway_point_data[progress_byte]
                # Prizes from Star Blocks
                elif loc_type == 0x07 and prize_block_active:
                    data = prize_block_data[progress_byte]
                else:
                    continue
                
                masked_data = data & (1 << progress_bit)
                if masked_data:
                    new_checks.append(loc_id)

            for new_check_id in new_checks:
                ctx.locations_checked.add(new_check_id)
                await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])

        # Store visited OW levels for UT
        active_level_data = list(snes_data.get(SMWMemory.active_level_data))
        shuffled_level = state_mirror[0x0A]
        tile_id = 0x100
        if shuffled_level in active_level_data:
            tile_id = active_level_data[shuffled_level]
        if game_state == 0x14 and tile_id not in self.visited_levels and tile_id in level_info_dict:
            self.visited_levels.add(tile_id)
            level_key = level_info_dict[tile_id].levelName
            await ctx.send_msgs([{
                "cmd": "Set", 
                "key": f"smw_{ctx.team}_{ctx.slot}_{level_key}",
                "slot": ctx.slot,
                "default": 0,
                "operations":
                    [{"operation": "replace", "value": 1}],
            }])

        # Send Current Room for Tracker
        if game_state != 0x14:
            current_sublevel_value = 0

        if ctx.current_sublevel_value != current_sublevel_value:
            ctx.current_sublevel_value = current_sublevel_value

            # Send level id data to tracker
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"smw_curlevelid_{ctx.team}_{ctx.slot}",
                "default": 0,
                "want_reply": False,
                "operations":
                    [{"operation": "replace", "value": ctx.current_sublevel_value}],
            }])
            if ctx.current_sublevel_value not in ctx.visited_levels:
                ctx.visited_levels.append(ctx.current_sublevel_value)
                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"smw_visitedlevels_{ctx.team}_{ctx.slot}",
                    "default": [],
                    "want_reply": False,
                    "operations":
                        [{"operation": "update", "value": ctx.visited_levels}],
                }])
        
        if game_state != 0x14:
            # Don't receive items or collect locations outside of in-level mode
            return

        # Receive items
        # TODO: Rewrite it to use SnesReader
        from .Rom import trap_rom_data, item_rom_data, icon_rom_data, ability_rom_data, progressive_items
        from SNIClient import snes_read
        recv_count = snes_data.get(SMWMemory.recv_count)
        recv_index = int.from_bytes(recv_count, "little")

        if recv_index < len(ctx.items_received):
            item = ctx.items_received[recv_index]
            recv_index += 1
            sending_game = ctx.slot_info[item.player].game
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_game(item.item), 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), recv_index, len(ctx.items_received)))

            if self.should_show_message(ctx, item):
                if item.item != 0xBC0012 and item.item != 0xBC0015 and item.item not in trap_rom_data:
                    # Don't send messages for Boss Tokens
                    item_name =ctx.item_names.lookup_in_game(item.item)
                    player_name = ctx.player_names[item.player]

                    receive_message = generate_received_text(item_name, player_name)
                    self.add_message_to_queue(receive_message)

            snes_buffered_write(ctx, SMW_RECV_PROGRESS_ADDR, bytes([recv_index&0xFF, (recv_index>>8)&0xFF]))

            if item.item in trap_rom_data or item.item == 0xBC0015:
                item_name = ctx.item_names.lookup_in_game(item.item)
                player_name = ctx.player_names[item.player]

                receive_message = generate_received_text(item_name, player_name)
                self.add_trap_to_queue(item, receive_message)
            elif item.item in item_rom_data:
                item_count = await snes_read(ctx, SRAM_START + item_rom_data[item.item][0], 0x1)
                increment = item_rom_data[item.item][1]

                new_item_count = item_count[0]
                if increment > 1:
                    new_item_count = increment
                else:
                    new_item_count += increment

                if game_state == 0x14 and len(item_rom_data[item.item]) > 2:
                    snes_buffered_write(ctx, SMW_SFX_ADDR, bytes([item_rom_data[item.item][2]]))

                snes_buffered_write(ctx, SRAM_START + item_rom_data[item.item][0], bytes([new_item_count]))
            elif item.item in icon_rom_data:
                queue_addr = await snes_read(ctx, SRAM_START + icon_rom_data[item.item][0], 2)
                queue_addr = queue_addr[0] + (queue_addr[1] << 8)
                queue_addr += 1
                snes_buffered_write(ctx, SRAM_START + icon_rom_data[item.item][0], bytes([queue_addr&0xFF, (queue_addr>>8)&0xFF]))
                if item.item == 0xBC0002:
                    goal_item_count = await snes_read(ctx, SMW_GOAL_ITEM_COUNT, 1)
                    snes_buffered_write(ctx, SMW_GOAL_ITEM_COUNT, bytes([goal_item_count[0] + 1]))

            elif item.item == 0xBC0026:
                # Handle Progressive Swim
                data = await snes_read(ctx, SMW_BWRAM + 0x03E0, 0x01)
                if data is None:
                    recv_index -= 1
                    snes_buffered_write(ctx, SMW_RECV_PROGRESS_ADDR, bytes([recv_index&0xFF, (recv_index>>8)&0xFF]))
                else:
                    data = int.from_bytes(data, "little")
                    data = ((data << 1) | 1) & 0x03
                    snes_buffered_write(ctx, SMW_BWRAM + 0x03E0, bytes([data]))

            elif item.item in progressive_items:
                # Handle Progressive items
                offset = progressive_items[item.item][0]
                data = await snes_read(ctx, SMW_BWRAM + offset, 0x01)
                if data is None:
                    recv_index -= 1
                    snes_buffered_write(ctx, SMW_RECV_PROGRESS_ADDR, bytes([recv_index&0xFF, (recv_index>>8)&0xFF]))
                else:
                    data = int.from_bytes(data, "little")
                    data = min(data+1, progressive_items[item.item][1])
                    snes_buffered_write(ctx, SMW_BWRAM + offset, bytes([data]))
                    snes_buffered_write(ctx, SMW_SFX_ADDR, bytes([0x3E]))

            elif item.item in ability_rom_data:
                # Handle Upgrades
                for rom_data in ability_rom_data[item.item]:
                    data = await snes_read(ctx, SRAM_START + rom_data[0], 1)
                    masked_data = data[0] | (1 << rom_data[1])
                    snes_buffered_write(ctx, SRAM_START + rom_data[0], bytes([masked_data]))
                    snes_buffered_write(ctx, SMW_SFX_ADDR, bytes([0x3E]))
                    await snes_flush_writes(ctx)
                    
            elif item.item == 0xBC000A:
                # Handle Progressive Powerup
                data = await snes_read(ctx, SRAM_START + 0x1F2D, 1)
                mushroom_data = data[0] & (1 << 0)
                fire_flower_data = data[0] & (1 << 1)
                cape_data = data[0] & (1 << 2)
                if mushroom_data == 0:
                    masked_data = data[0] | (1 << 0)
                    snes_buffered_write(ctx, SRAM_START + 0x1F2D, bytes([masked_data]))
                    snes_buffered_write(ctx, SMW_SFX_ADDR, bytes([0x3E]))
                elif fire_flower_data == 0:
                    masked_data = data[0] | (1 << 1)
                    snes_buffered_write(ctx, SRAM_START + 0x1F2D, bytes([masked_data]))
                    snes_buffered_write(ctx, SMW_SFX_ADDR, bytes([0x3E]))
                elif cape_data == 0:
                    masked_data = data[0] | (1 << 2)
                    snes_buffered_write(ctx, SRAM_START + 0x1F2D, bytes([masked_data]))
                    snes_buffered_write(ctx, SMW_SFX_ADDR, bytes([0x41]))
                else:
                    # Extra Powerup?
                    pass
            elif item.item == 0xBC0082:
                # Handle Literature Trap
                from .Names.LiteratureTrap import lit_trap_text_list
                import random
                rand_trap = random.choice(lit_trap_text_list)

                for message in rand_trap:
                    self.add_message_to_queue(message)

            await snes_flush_writes(ctx)

        # Handle Collected Locations
        path_data = list(snes_data.get(SMWMemory.path_data))
        level_clear_flags = list(flags_data[0x200:0x260])
        
        new_events = 0
        new_dragon_coin = False
        new_moon = False
        new_hidden_1up = False
        new_prize_block = False
        new_blocksanity = False
        new_midway_point = False
        for loc_id in ctx.checked_locations:
            if loc_id in ctx.locations_checked:
                continue
            ctx.locations_checked.add(loc_id)

            level_id = loc_id >> 24
            loc_type = (loc_id >> 20 & 0x0F)
            loc_data = loc_id & 0x000FFFFF
            progress_byte = (level_id // 8)
            progress_bit  = 7 - (level_id % 8)

            # Exits
            if loc_type == 0x00 or loc_type == 0x01:
                flag = 1 + (loc_type & 0x01)
                level_clear_flags[level_id] |= flag

                event_id = event_data[level_id] + (loc_type & 0x01)
                progress_byte = event_id >> 3
                progress_bit  = 7 - (event_id & 0x07)

                data = progress_data[progress_byte]
                masked_data = data & (1 << progress_bit)

                if masked_data:
                    continue

                new_events += 1
                new_data = data | (1 << progress_bit)
                progress_data[progress_byte] = new_data
                tile_id = active_level_data[level_id]
                level_info = level_info_dict[tile_id]
                path = level_info.exit1Path if loc_type == 0 else level_info.exit2Path

                if not path: 
                    continue
                
                if tile_id < 0x60:
                    this_end_path = path_data[tile_id]
                    new_data = this_end_path | path.thisEndDirection
                    path_data[tile_id] = new_data
                if path.otherLevelID < 0x60:
                    other_end_path = path_data[path.otherLevelID]
                    new_data = other_end_path | path.otherEndDirection
                    path_data[path.otherLevelID] = new_data

            # Dragon coins
            elif loc_type == 0x03 and dragon_coins_active:
                if level_id in SMW_UNCOLLECTABLE_DRAGON_COINS:
                    continue
                data = dragon_coins_data[progress_byte]
                new_data = data | (1 << progress_bit)
                dragon_coins_data[progress_byte] = new_data
                new_dragon_coin = True

            # 3-Up Moon
            elif loc_type == 0x04 and moon_active:
                data = moon_data[progress_byte]
                new_data = data | (1 << progress_bit)
                moon_data[progress_byte] = new_data
                new_moon = True

            # Hidden 1-Ups
            elif loc_type == 0x05 and hidden_1up_active:
                data = hidden_1up_data[progress_byte]
                new_data = data | (1 << progress_bit)
                hidden_1up_data[progress_byte] = new_data
                new_hidden_1up = True

            # Prizes from Star Blocks
            elif loc_type == 0x07 and prize_block_active:
                data = midway_point_data[progress_byte]
                new_data = data | (1 << progress_bit)
                midway_point_data[progress_byte] = new_data
                new_midway_point = True

            # Prizes from Star Blocks
            elif loc_type == 0x07 and prize_block_active:
                data = prize_block_data[progress_byte]
                new_data = data | (1 << progress_bit)
                prize_block_data[progress_byte] = new_data
                new_prize_block = True

            # Item from block
            elif loc_type == 0x0A and blocksanity_active:
                block_index = loc_data & 0x0FFFF
                blocksanity_data[block_index] = 1
                new_blocksanity = True
                for loc_id in sorted_locations_table[level_id]:
                    loc_type = (loc_id >> 20 & 0x0F)
                    if loc_type == 0x0A:
                        block_index = loc_id & 0x0000FFFF
                        if blocksanity_data[block_index] != 1:
                            break
                else:
                    data = blocksanity_flags[progress_byte]
                    new_data = data | (1 << progress_bit)
                    blocksanity_flags[progress_byte] = new_data


        if new_dragon_coin:
            snes_buffered_write(ctx, SMW_DRAGON_COINS_DATA, bytearray(dragon_coins_data))
        if new_moon:
            snes_buffered_write(ctx, SMW_MOON_DATA, bytearray(moon_data))
        if new_hidden_1up:
            snes_buffered_write(ctx, SMW_HIDDEN_1UP_DATA, bytearray(hidden_1up_data))
        if new_prize_block:
            snes_buffered_write(ctx, SMW_BONUS_BLOCK_DATA, bytearray(prize_block_data))
        if new_midway_point:
            snes_buffered_write(ctx, SMW_MIDWAY_POINT_FLAGS, bytearray(midway_point_data))
        if new_blocksanity:
            snes_buffered_write(ctx, SMW_BLOCKSANITY_DATA, bytearray(blocksanity_data))
            snes_buffered_write(ctx, SMW_BLOCKSANITY_FLAGS, bytearray(blocksanity_flags))
        if new_events > 0:
            snes_buffered_write(ctx, SMW_LEVEL_CLEAR_FLAGS, bytearray(level_clear_flags))
            snes_buffered_write(ctx, SMW_PROGRESS_DATA, bytearray(progress_data))
            snes_buffered_write(ctx, SMW_PATH_DATA, bytearray(path_data))
            event_count = int.from_bytes(snes_data.get(SMWMemory.event_count), "little")
            snes_buffered_write(ctx, SMW_NUM_EVENTS_ADDR, bytes([event_count + new_events]))

        await snes_flush_writes(ctx)
        
    async def handle_energy_link(self, ctx: "SNIContext", snes_data: SnesData[SMWMemory]):
        from SNIClient import snes_buffered_write, snes_flush_writes

        # Expose EnergyLink to the ROM
        pool = ctx.stored_data[f'EnergyLink{ctx.team}'] or 0
        total_energy = int(pool / SMW_EXCHANGE_RATE)
        if total_energy < 9999:
            snes_buffered_write(ctx, SMW_ENERGY_LINK_COUNT, bytearray([total_energy & 0xFF, (total_energy >> 8) & 0xFF]))
        else:
            snes_buffered_write(ctx, SMW_ENERGY_LINK_COUNT, bytearray([0x0F, 0x27]))

        # Deposits EnergyLink into pool
        energy_packet = snes_data.get(SMWMemory.energy_link_packet)
        energy_packet = int.from_bytes(energy_packet, "little")
        energy_packet = int((energy_packet * SMW_EXCHANGE_RATE) / 4)
        if energy_packet != 0:
            await ctx.send_msgs([{
                "cmd": "Set", 
                "key": f"EnergyLink{ctx.team}", 
                "slot": ctx.slot,
                "default": 0,
                "operations":
                    [{"operation": "add", "value": energy_packet}],
            }])
            snes_buffered_write(ctx, SMW_ENERGY_LINK_TRANSFER, bytearray([0x00, 0x00]))

        # Purchase from EnergyLink
        purchase_reply = snes_data.get(SMWMemory.inventory_reply)
        purchased_item = snes_data.get(SMWMemory.inventory_item)
        energy_purchase = snes_data.get(SMWMemory.inventory_purchase)
        energy_purchase = int.from_bytes(energy_purchase, "little") * SMW_EXCHANGE_RATE
        purchase_reply = int.from_bytes(purchase_reply, "little")
        purchased_item = int.from_bytes(purchased_item, "little")
        if purchase_reply == 0x00 and purchased_item != 0x00 and energy_purchase != 0 and self.inventory_purchase == "":
            self.inventory_tag = f"smw-inventory-{ctx.team}-{ctx.slot}-{random.randint(0, 0xFFFFFFFF)}"
            self.inventory_cost = energy_purchase
            await ctx.send_msgs([{ 
                "cmd": "Set", 
                "key": f"EnergyLink{ctx.team}", 
                "slot": ctx.slot,
                "tag": self.inventory_tag,
                "default": 0,
                "want_reply": True,
                "operations":
                    [{"operation": "add", "value": -energy_purchase},
                    {"operation": "max", "value": 0}],
            }])
            self.inventory_purchase = "pending"
        
        elif self.inventory_purchase == "successful":
            snes_buffered_write(ctx, SMW_ENERGY_LINK_REPLY, bytearray([purchased_item]))
            snes_buffered_write(ctx, SMW_ENERGY_LINK_PURCHASE, bytearray([0x00, 0x00]))
            self.inventory_purchase = ""
            
        elif self.inventory_purchase == "not_enough_funds":
            snes_buffered_write(ctx, SMW_ENERGY_LINK_REPLY, bytearray([0xFF]))
            snes_buffered_write(ctx, SMW_ENERGY_LINK_PURCHASE, bytearray([0x00, 0x00]))
            await ctx.send_msgs([{
                "cmd": "Set", 
                "key": f"EnergyLink{ctx.team}", 
                "slot": ctx.slot,
                "default": 0,
                "operations":
                    [{"operation": "add", "value": self.inventory_refund}],
            }])
            self.inventory_refund = 0
            self.inventory_purchase = ""
                
        await snes_flush_writes(ctx)

    def on_package(self, ctx: "SNIContext", cmd: str, args: dict):
        super().on_package(ctx, cmd, args)

        if cmd == "Connected":
            self.slot_data = args.get("slot_data", None) # type: ignore
            if self.slot_data:
                if self.slot_data["energy_link"]:
                    ctx.set_notify(f"EnergyLink{ctx.team}")
                    if ctx.ui:
                        ctx.ui.enable_energy_link()
                        ctx.ui.energy_link_label.text = "Coins: Standby"
                        snes_logger.info(f"Initialized EnergyLink{ctx.team}")

        elif cmd == "SetReply" and args["key"].startswith("EnergyLink"):
            if self.inventory_purchase == "pending" and "tag" in args:
                if args["tag"] == self.inventory_tag:
                    self.inventory_tag = ""
                    if args["original_value"] < self.inventory_cost:
                        # send back the original value
                        value = args["original_value"]
                        self.inventory_purchase = "not_enough_funds"
                        self.inventory_refund = value
                    else:
                        value = args["value"]
                        self.inventory_purchase = "successful"

            else:
                value = args["value"]

            if ctx.ui:
                pool = (value or 0) / SMW_EXCHANGE_RATE
                ctx.ui.energy_link_label.text = f"Coins: {int(pool)}"

        elif cmd == "Retrieved":
            if f"EnergyLink{ctx.team}" in args["keys"] and args["keys"][f"EnergyLink{ctx.team}"] and ctx.ui:
                pool = (args["keys"][f"EnergyLink{ctx.team}"] or 0) / SMW_EXCHANGE_RATE
                ctx.ui.energy_link_label.text = f"Coins: {int(pool)}"

        elif cmd == "Bounced":
            if self.slot_data is None and "tags" not in args:
                return 
            
            if not hasattr(self, "instance_id"):
                self.instance_id = time.time()

            if "data" not in args:
                return

            source_name = args["data"]["source"]
            if "TrapLink" in ctx.tags and "TrapLink" in args["tags"] and source_name != ctx.slot_info[ctx.slot].name:
                trap_name: str = args["data"]["trap_name"]
                if trap_name not in trap_name_to_value:
                    # We don't know how to handle this trap, ignore it
                    return

                trap_id: int = trap_name_to_value[trap_name]

                if "trap_weights" not in self.slot_data.keys():
                    return

                if f"{trap_id}" not in self.slot_data["trap_weights"]:
                    return

                if self.slot_data["trap_weights"][f"{trap_id}"] == 0:
                    # The player disabled this trap type
                    return

                self.priority_trap = NetworkItem(trap_id, 0, 0)
                self.priority_trap_message = generate_received_trap_link_text(trap_name, source_name)
                self.priority_trap_message_str = f"Received linked {trap_name} from {source_name}"
            elif "RingLink" in ctx.tags and "RingLink" in args["tags"] and source_name != self.instance_id:
                if not hasattr(self, "pending_ring_link"):
                    self.pending_ring_link = 0
                self.pending_ring_link += args["data"]["amount"]

    async def send_trap_link(self, ctx: "SNIContext", trap_name: str):
        if "TrapLink" not in ctx.tags or ctx.slot == None:
            return

        await ctx.send_msgs([{
            "cmd": "Bounce", "tags": ["TrapLink"],
            "data": {
                "time": time.time(),
                "source": ctx.slot_info[ctx.slot].name,
                "trap_name": trap_name
            }
        }])
        snes_logger.info(f"Sent linked {trap_name}")

    async def send_ring_link(self, ctx: "SNIContext", snes_data: SnesData[SMWMemory], amount: int):
        if "RingLink" not in ctx.tags or ctx.slot == None:
            return

        state_mirror = snes_data.get(SMWMemory.state_mirror)
        game_state = state_mirror[0x00]
        
        if game_state != 0x14:
            return

        if not hasattr(self, "instance_id"):
            self.instance_id = time.time()

        await ctx.send_msgs([{
            "cmd": "Bounce", "tags": ["RingLink"],
            "data": {
                "time": time.time(),
                "source": self.instance_id,
                "amount": amount
            }
        }])

    def add_message_to_queue(self, new_message):

        if not hasattr(self, "message_queue"):
            self.message_queue = []

        self.message_queue.append(new_message)


    def add_message_to_queue_front(self, new_message):
        if not hasattr(self, "message_queue"):
            self.message_queue = []

        self.message_queue.insert(0, new_message)

    async def handle_message_queue(self, ctx: "SNIContext"):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        if not hasattr(self, "message_queue") or len(self.message_queue) == 0:
            return

        state_mirror = await snes_read(ctx, SMW_STATE_MIRROR, 0x0A)

        if state_mirror is None:
            return

        game_state = state_mirror[0x00]
        if game_state != 0x14:
            return

        mario_state = state_mirror[0x01]
        if mario_state != 0x00:
            return
        
        message_box = state_mirror[0x07]
        if message_box != 0x00:
            return
        
        pause_state = state_mirror[0x09]
        if pause_state != 0x00:
            return
        
        current_level = state_mirror[0x04]
        if current_level in SMW_BAD_TEXT_BOX_LEVELS:
            return

        boss_state = state_mirror[0x02]
        if boss_state in SMW_BOSS_STATES:
            return

        active_boss = state_mirror[0x03]
        if active_boss != 0x00:
            return

        next_message = self.message_queue.pop(0)

        snes_buffered_write(ctx, SMW_MESSAGE_QUEUE_ADDR, bytes(next_message))
        snes_buffered_write(ctx, SMW_MESSAGE_BOX_ADDR, bytes([0x03]))
        snes_buffered_write(ctx, SMW_SFX_ADDR, bytes([0x22]))

        await snes_flush_writes(ctx)

    def add_trap_to_queue(self, trap_item, trap_msg):
        self.trap_queue = getattr(self, "trap_queue", [])

        self.trap_queue.append((trap_item, trap_msg))

    def should_show_message(self, ctx, next_item):
        return ctx.receive_option == 1 or \
                (ctx.receive_option == 2 and ((next_item.flags & 1) != 0)) or \
                (ctx.receive_option == 3 and ((next_item.flags & 1) != 0 and next_item.item != 0xBC0002))


    async def handle_trap_queue(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        if (not hasattr(self, "trap_queue") or len(self.trap_queue) == 0) and\
            (not hasattr(self, "priority_trap") or self.priority_trap == 0):
            return

        ram_mirror = await snes_read(ctx, SMW_STATE_MIRROR, 0x0A)

        if ram_mirror is None:
            return

        game_state = ram_mirror[0x00]
        mario_state = ram_mirror[0x01]
        pause_state = ram_mirror[0x09]

        if game_state != 0x14 or mario_state != 0x00 or pause_state != 0x00:
            return

        next_trap = None
        message = bytearray()
        message_str = ""
        from_queue = False

        if getattr(self, "priority_trap", None) and self.priority_trap.item != 0:
            next_trap = self.priority_trap
            message = self.priority_trap_message
            message_str = self.priority_trap_message_str
            self.priority_trap = None
            self.priority_trap_message = bytearray()
            self.priority_trap_message_str = ""
        elif hasattr(self, "trap_queue") and len(self.trap_queue) > 0:
            from_queue = True
            next_trap, message = self.trap_queue.pop(0)
        else:
            return
        
        from .Rom import trap_rom_data
        if next_trap.item in trap_rom_data:
            trap_active = await snes_read(ctx, SRAM_START + trap_rom_data[next_trap.item][0], 0x3)

            if next_trap.item == 0xBC0083:
                # Timer Trap
                if trap_active[0] == 0 or (trap_active[0] == 1 and trap_active[1] == 0 and trap_active[2] == 0):
                    # Trap already active
                    if from_queue:
                        self.add_trap_to_queue(next_trap, message)
                    return
                else:
                    if len(message_str) > 0:
                        snes_logger.info(message_str)
                    if "TrapLink" in ctx.tags and from_queue:
                        await self.send_trap_link(ctx, trap_value_to_name[next_trap.item])
                    snes_buffered_write(ctx, SRAM_START + trap_rom_data[next_trap.item][0], bytes([0x01]))
                    snes_buffered_write(ctx, SRAM_START + trap_rom_data[next_trap.item][0] + 1, bytes([0x00]))
                    snes_buffered_write(ctx, SRAM_START + trap_rom_data[next_trap.item][0] + 2, bytes([0x00]))
            else:
                if (next_trap.item != 0xBC008E and trap_active[0] > 0) or (next_trap.item == 0xBC008E and trap_active[0] == 0):
                    # Trap already active
                    if from_queue:
                        self.add_trap_to_queue(next_trap, message)
                    return
                else:
                    if next_trap.item == 0xBC0085:
                        # Special case thwimp trap
                        # Do not fire if the previous thwimp hasn't reached the player's Y pos
                        active_thwimp = await snes_read(ctx, SMW_ACTIVE_THWIMP_ADDR, 0x1)
                        if active_thwimp[0] != 0xFF:
                            if from_queue:
                                self.add_trap_to_queue(next_trap, message)
                            return
                    if game_state == 0x14 and len(trap_rom_data[next_trap.item]) > 2:
                        snes_buffered_write(ctx, SMW_SFX_ADDR, bytes([trap_rom_data[next_trap.item][2]]))
                    
                    if len(message_str) > 0:
                        snes_logger.info(message_str)
                    if "TrapLink" in ctx.tags and from_queue:
                        await self.send_trap_link(ctx, trap_value_to_name[next_trap.item])
                        
                    new_item_count = trap_rom_data[next_trap.item][1]
                    snes_buffered_write(ctx, SRAM_START + trap_rom_data[next_trap.item][0], bytes([new_item_count]))

            current_level = ram_mirror[0x04]
            if current_level in SMW_BAD_TEXT_BOX_LEVELS:
                return

            boss_state = ram_mirror[0x02]
            if boss_state in SMW_BOSS_STATES:
                return

            active_boss = ram_mirror[0x03]
            if active_boss != 0x00:
                return

            if self.should_show_message(ctx, next_trap):
                self.add_message_to_queue_front(message)

        elif next_trap.item == 0xBC0082:
            if self.should_show_message(ctx, next_trap):
                self.add_message_to_queue_front(message)
            if len(message_str) > 0:
                snes_logger.info(message_str)
            if "TrapLink" in ctx.tags and from_queue:
                await self.send_trap_link(ctx, trap_value_to_name[next_trap.item])

            # Handle Literature Trap
            from .Names.LiteratureTrap import lit_trap_text_list
            import random
            rand_trap = random.choice(lit_trap_text_list)

            for message in rand_trap:
                self.add_message_to_queue(message)
    
        await snes_flush_writes(ctx)
