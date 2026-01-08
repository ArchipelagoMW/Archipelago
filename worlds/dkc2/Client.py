import logging
import time
import random

from NetUtils import ClientStatus, NetworkItem, color
from worlds.AutoSNIClient import SNIClient
from .Items import trap_value_to_name, trap_name_to_value

logger = logging.getLogger("Client")
snes_logger = logging.getLogger("SNES")

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SNIClient import SNIContext

# FXPAK Pro protocol memory mapping used by SNI
ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

STARTING_ID = 0xBF0000

DKC2_SETTINGS = ROM_START + 0x3DFF80

DKC2_MISC_FLAGS = WRAM_START + 0x08D2
DKC2_GAME_FLAGS = WRAM_START + 0x59B2

DKC2_SOUND_PLAYBACK = WRAM_START + 0x1F7E6
DKC2_EFFECT_BUFFER = WRAM_START + 0x0619
DKC2_SOUND_BUFFER = WRAM_START + 0x0622
DKC2_SPC_NEXT_INDEX = WRAM_START + 0x0634
DKC2_SPC_INDEX = WRAM_START + 0x0632
DKC2_SPC_CHANNEL_BUSY = WRAM_START + 0x0621

DKC2_SRAM = SRAM_START + 0x800
DKC2_RECV_INDEX = DKC2_SRAM + 0x020
DKC2_INIT_FLAG = DKC2_SRAM + 0x022
DKC2_DAMAGE_FLAG = DKC2_SRAM + 0x044
DKC2_INSTA_DEATH_FLAG = DKC2_SRAM + 0x046
DKC2_DEATH_LINK_FORCE = DKC2_SRAM + 0x05A
DKC2_DEATH_LINK_FLAG = DKC2_SRAM + 0x058

DKC2_TRACKED_LEVELS = DKC2_SRAM + 0x80
DKC2_TRACKED_CLEARS = DKC2_SRAM + 0x70

DKC2_GAME_TIME = WRAM_START + 0x00D5
DKC2_IN_LEVEL = WRAM_START + 0x01FF
DKC2_CURRENT_LEVEL = WRAM_START + 0x08A8    # 0xD3?
DKC2_LOADED_LEVEL = WRAM_START + 0x00D3
DKC2_CURRENT_MODE = WRAM_START + 0x00D0
DKC2_CURRENT_MAP = WRAM_START + 0x06B1
DKC2_GAMEMODE = WRAM_START + 0x065E
DKC2_INSTANT_LEVEL_EXIT = WRAM_START + 0x06CF

DKC2_BRIGHTNESS = WRAM_START + 0x0512

DKC2_CRANKY_FLAGS = WRAM_START + 0x08D2
DKC2_WRINKLY_FLAGS = WRAM_START + 0x08E0
DKC2_FUNKY_FLAGS = WRAM_START + 0x08E7
DKC2_SWANKY_FLAGS = WRAM_START + 0x08F0
DKC2_KLUBBA_TOLLS = WRAM_START + 0x08FA
DKC2_KONG_LETTERS = WRAM_START + 0x0902
DKC2_SANITY_FLAGS = WRAM_START + 0x1FF00

DKC2_BONUS_FLAGS = WRAM_START + 0x59B2
DKC2_DK_COIN_FLAGS = WRAM_START + 0x59D2
DKC2_STAGE_FLAGS = WRAM_START + 0x59F2

DKC2_MESSAGE_TRACKER = WRAM_START + 0x1F7E4
DKC2_MESSAGE_ACTIVATE = WRAM_START + 0x1F7F6
DKC2_MESSAGE_TIMER = WRAM_START + 0x1F7F8
DKC2_MESSAGE_PHASE = WRAM_START + 0x1F7F0
DKC2_MESSAGE_RERUN  = WRAM_START + 0x1F7EE
DKC2_MESSAGE_BUFFER = WRAM_START + 0x1F600
DKC2_PALETTE_BUFFER = WRAM_START + 0x1F5C0

DKC2_ENERGY_LINK_TRANSFER = DKC2_SRAM + 0x04E
DKC2_EXCHANGE_RATE = 200000000
DK_BARREL_BANANA_COST = 20
DK_BARREL_MAX = 3

DKC2_ROMHASH_START = 0xFFC0
ROMHASH_SIZE = 0x15

UNCOLLECTABLE_LEVELS = [0x09, 0x21, 0x63, 0x60, 0x0D]
BANNED_GAMEMODES = [0x8D1F, 0x8D3D]

class DKC2SNIClient(SNIClient):
    game = "Donkey Kong Country 2"
    patch_suffix = ".apdkc2"
    slot_data: dict
    ctx: "SNIContext"

    def __init__(self):
        super().__init__()
        self.game_state = False
        self.energy_link_enabled = False
        self.received_trap_link = False
        self.barrel_request = ""
        self.current_map = 0
        self.barrel_label = None
        self.message_queue = []
        self.last_message = []
        self.current_session_locations = set()
        self.processed_locations = set()


    async def validate_rom(self, ctx: "SNIContext"):
        from SNIClient import snes_read

        setting_data = await snes_read(ctx, DKC2_SETTINGS, 0x40)
        rom_name = await snes_read(ctx, DKC2_ROMHASH_START, ROMHASH_SIZE)

        if rom_name is None or setting_data is None or rom_name == bytes([0] * ROMHASH_SIZE) or rom_name[:4] != b"DKC2":
            if "request" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("request")
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.receive_option = 0
        ctx.send_option = 0
        ctx.allow_collect = True

        update_tags = False

        energy_link = setting_data[0x19]
        if energy_link and "EnergyLink" not in ctx.tags:
            ctx.tags.add("EnergyLink")
            update_tags = True
            if "request" not in ctx.command_processor.commands:
                ctx.command_processor.commands["request"] = cmd_request

        trap_link = setting_data[0x1A]
        if trap_link and "TrapLink" not in ctx.tags:
            ctx.tags.add("TrapLink")
            update_tags = True

        death_link = setting_data[0x18]
        if death_link:
            await ctx.update_death_link(bool(death_link & 0b1))
        
        if update_tags:
            await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}])
        
        ctx.rom = rom_name

        return True


    async def game_watcher(self, ctx: "SNIContext"):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        setting_data = await snes_read(ctx, DKC2_SETTINGS, 0x40)
        general_data = await snes_read(ctx, WRAM_START + 0x00D0, 0x0F)
        game_flags = await snes_read(ctx, DKC2_GAME_FLAGS, 0x60)
        misc_flags = await snes_read(ctx, DKC2_MISC_FLAGS, 0x80)
        swanky_flags = await snes_read(ctx, DKC2_SWANKY_FLAGS, 0x09)
        sanity_flags = await snes_read(ctx, DKC2_SANITY_FLAGS, 0x100)

        if general_data is None or game_flags is None or misc_flags is None or setting_data is None or swanky_flags is None:
            self.game_state = False
            return

        loaded_save = int.from_bytes(general_data[0x05:0x07], "little")
        if loaded_save == 0:
            self.game_state = False
            self.current_map = 0
            return

        nmi_pointer = await snes_read(ctx, WRAM_START + 0x0020, 0x2)
        if nmi_pointer is None:
            self.game_state = False
            self.current_map = 0
            return
        nmi_pointer = int.from_bytes(nmi_pointer, "little")
        if nmi_pointer == 0x8CE9 or nmi_pointer == 0x8CF1:
            self.game_state = True
            
        if not self.game_state:
            return

        validation = int.from_bytes(await snes_read(ctx, DKC2_INIT_FLAG, 0x2), "little")
        if validation != 0xDEAD:
            snes_logger.info(f'ROM not properly validated.')
            self.game_state = False
            self.current_map = 0
            return
        
        player_state = await snes_read(ctx, WRAM_START + 0x08C3, 0x01)
        if player_state is None:
            return
        
        if "DeathLink" in ctx.tags and ctx.last_death_link + 1 < time.time():
            death_link_flag = await snes_read(ctx, DKC2_DEATH_LINK_FLAG, 0x01)
            if death_link_flag is not None:
                is_death_link_active = death_link_flag[0]
                is_player_dead = player_state[0] & 0x20
                is_map = nmi_pointer == 0x8CE9 or nmi_pointer == 0x8CF1
                currently_dead = is_player_dead and not is_death_link_active and not is_map
                await ctx.handle_deathlink_state(currently_dead)

        if "EnergyLink" in ctx.tags:
            await self.handle_energy_link(ctx)

        if "TrapLink" in ctx.tags:
            await self.handle_trap_link(ctx)

        current_level = await snes_read(ctx, DKC2_CURRENT_LEVEL, 0x01)
        loaded_level = await snes_read(ctx, DKC2_LOADED_LEVEL, 0x01)
        current_map = await snes_read(ctx, DKC2_CURRENT_MAP, 0x01)
        brightness = await snes_read(ctx, DKC2_BRIGHTNESS, 0x01)

        if current_level is None or loaded_level is None or brightness is None:
            return
        
        from .Levels import location_id_to_level_id
        from worlds import AutoWorldRegister

        new_checks = []
        current_level = int.from_bytes(current_level, "little")
        loaded_level = int.from_bytes(loaded_level, "little")
        brightness = int.from_bytes(brightness, "little")

        dk_coins_as_checks = setting_data[0x20]
        kong_as_checks = setting_data[0x21]
        balloons_as_checks = setting_data[0x22]
        coins_as_checks = setting_data[0x23]
        bunches_as_checks = setting_data[0x24]
        swanky_as_checks = setting_data[0x25]

        kong_flags = misc_flags[0x30]
        stage_flags = game_flags[0x40:0x60]
        bonus_flags = list(game_flags[0x00:0x20])
        dk_coin_flags = list(game_flags[0x20:0x40])
        sanity_flags = list(sanity_flags)
        for loc_name, data in location_id_to_level_id.items():
            # Do not process locations if in a map or a transition
            if nmi_pointer == 0x8CE9 or nmi_pointer == 0x8CF1 or brightness & 0x0F != 0x0F:
                break 
            loc_id = AutoWorldRegister.world_types[ctx.game].location_name_to_id[loc_name]
            if loc_id not in ctx.locations_checked:
                loc_type = data[0]
                level_num = data[1]
                level_offset = (level_num >> 3) & 0x1E
                level_bit = 1 << (level_num & 0x0F)

                if loc_type == 0x00:
                    # Level clear
                    level_data = int.from_bytes(stage_flags[level_offset:level_offset+2], "little")
                    if level_data & level_bit:
                        new_checks.append(loc_id)
                elif loc_type == 0x01 and kong_as_checks:
                    # KONG
                    if level_num == current_level and kong_flags & 0x0F == 0x0F:
                        new_checks.append(loc_id)
                elif loc_type == 0x02 and dk_coins_as_checks:
                    # DK Coin
                    level_data = int.from_bytes(dk_coin_flags[level_offset:level_offset+2], "little")
                    if level_data & level_bit:
                        new_checks.append(loc_id)
                elif loc_type == 0x03:
                    # Bonus
                    level_data = int.from_bytes(bonus_flags[level_offset:level_offset+2], "little")
                    if level_data & level_bit:
                        new_checks.append(loc_id)
                elif loc_type == 0x04 and swanky_as_checks:
                    # Swanky Games
                    bonus_offset = data[1] >> 4
                    bonus_data = swanky_flags[bonus_offset]
                    bonus_bit = data[1] & 0x07
                    if bonus_data & bonus_bit:
                        new_checks.append(loc_id)
                elif loc_type == 0x05 and coins_as_checks:
                    # Banana Coins
                    flag = sanity_flags[data[2]]
                    if level_num == loaded_level and flag & 0x02 == 0x02:
                        new_checks.append(loc_id)
                elif loc_type == 0x06 and bunches_as_checks:
                    # Banana Bunches
                    flag = sanity_flags[data[2]]
                    if level_num == loaded_level and flag & 0x04 == 0x04:
                        new_checks.append(loc_id)
                elif loc_type == 0x07 and balloons_as_checks:
                    # Balloons
                    flag = sanity_flags[data[2]]
                    if level_num == loaded_level and flag & 0x01 == 0x01:
                        new_checks.append(loc_id)

        # Check goals
        goal_check = 0
        selected_goal = setting_data[0x01]

        level_num = 0x61
        level_offset = (level_num >> 3) & 0x1E
        level_bit = 1 << (level_num & 0x0F)
        level_data = int.from_bytes(bonus_flags[level_offset:level_offset+2], "little")
        if level_data & level_bit:
            goal_check |= 1
        
        level_num = 0x6B
        level_offset = (level_num >> 3) & 0x1E
        level_bit = 1 << (level_num & 0x0F)
        level_data = int.from_bytes(dk_coin_flags[level_offset:level_offset+2], "little")
        if level_data & level_bit:
            goal_check |= 2

        if goal_check & selected_goal == selected_goal:
            if not ctx.finished_game:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True
                return
            
        # Add a label that shows how many Barrels are left
        await self.handle_messages(ctx)

        # Add a label that shows how many Barrels are left
        await self.handle_barrel_label(ctx)

        # Send current map to poptracker
        reached_levels = await snes_read(ctx, DKC2_TRACKED_LEVELS, 0x20)
        current_clears = await snes_read(ctx, DKC2_TRACKED_CLEARS, 0x0E)
        if reached_levels is None or current_clears is None:
            return
        
        if nmi_pointer == 0x8CE9 or nmi_pointer == 0x8CF1:
            poptracker_id = 0x100 | int.from_bytes(current_map, "little")
        else:
            poptracker_id = loaded_level & 0xFF

        if self.current_map != poptracker_id:
            self.current_map = poptracker_id

            # Save reached levels
            if poptracker_id < 0x100:
                reached_levels = bytearray(reached_levels)
                level_bit = 1 << (poptracker_id & 0x0F)
                level_offset = (poptracker_id >> 3) & 0x1E
                level_data = int.from_bytes(reached_levels[level_offset:level_offset+2], "little")
                level_data |= level_bit
                reached_levels[level_offset:level_offset+2] = level_data.to_bytes(2, "little")
                snes_buffered_write(ctx, DKC2_TRACKED_LEVELS, bytearray(reached_levels))
                await snes_flush_writes(ctx)

                await ctx.send_msgs([{
                    "cmd": "Set", 
                    "key": f"dkc2_reached_levels_{ctx.team}_{ctx.slot}", 
                    "default": 0,
                    "want_reply": False,
                    "operations":
                        [{"operation": "replace", "value": list(reached_levels)}],
                }])

            await ctx.send_msgs([{
                "cmd": "Set", 
                "key": f"dkc2_current_map_{ctx.team}_{ctx.slot}", 
                "default": 0,
                "want_reply": False,
                "operations":
                    [{"operation": "replace", "value": self.current_map}],
            }])

            level_clear_list = []
            for idx in range(0, len(current_clears), 2):
                current_world_count = int.from_bytes(current_clears[idx:idx+2], "little")
                level_clear_list.append(current_world_count)

            await ctx.send_msgs([{
                    "cmd": "Set", 
                    "key": f"dkc2_clear_count_{ctx.team}_{ctx.slot}", 
                    "default": 0,
                    "want_reply": False,
                    "operations":
                        [{"operation": "replace", "value": level_clear_list}],
                }])
        

        # Receive items
        rom = await snes_read(ctx, DKC2_ROMHASH_START, ROMHASH_SIZE)
        if rom != ctx.rom:
            ctx.rom = None
            snes_logger.info(f'Exit ROM.')
            return
        
        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            self.current_session_locations.add(new_check_id)
            location = ctx.location_names.lookup_in_game(new_check_id)
            snes_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])

        recv_count = await snes_read(ctx, DKC2_RECV_INDEX, 2)
        if recv_count is None:
            # Add a small failsafe in case we get a None. Other SNI games do this...
            return

        from .Rom import unlock_data, currency_data, trap_data
        recv_index = int.from_bytes(recv_count, "little")

        if recv_index < len(ctx.items_received):
            item = ctx.items_received[recv_index]
            recv_index += 1
            sending_game = ctx.slot_info[item.player].game
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_game(item.item), 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), recv_index, len(ctx.items_received)))
            
            self.message_queue.append([False, ctx.player_names[item.player], ctx.item_names.lookup_in_game(item.item), item.flags, True])
            
            sfx = 0
            # Give kongs
            if item.item in {STARTING_ID + 0x0010, STARTING_ID + 0x0011}:
                offset = unlock_data[item.item][0]
                sfx = unlock_data[item.item][1]
                count = await snes_read(ctx, DKC2_SRAM + offset, 0x02)
                if count is None:
                    recv_index -= 1
                    return
                count = int.from_bytes(count, "little")
                if item.item == STARTING_ID + 0x0010:
                    count |= 0x0001
                else:
                    count |= 0x0002
                count &= 0x00FF
                snes_buffered_write(ctx, DKC2_SRAM + offset, bytes([count]))

            # Give items
            elif item.item in unlock_data:
                offset = unlock_data[item.item][0]
                sfx = unlock_data[item.item][1]
                snes_buffered_write(ctx, DKC2_SRAM + offset, bytearray([0x01]))
            
            # Give currency-like items
            elif item.item in currency_data:
                offset = currency_data[item.item][0]
                if offset & 0x8000 == 0x8000:
                    addr = DKC2_SRAM + (offset & 0x7FFF)
                else:
                    addr = WRAM_START + offset
                sfx = currency_data[item.item][1]
                currency = await snes_read(ctx, addr, 0x01)
                if currency is None:
                    recv_index -= 1
                    return
                currency = min(int.from_bytes(currency, "little") + 1, 99)
                snes_buffered_write(ctx, addr, currency.to_bytes(1, "little"))

            # Give traps 
            elif item.item in trap_data:
                offset = trap_data[item.item][0]
                sfx = trap_data[item.item][1]
                traps = await snes_read(ctx, DKC2_SRAM + offset, 0x02)
                if traps is None:
                    recv_index -= 1
                    return
                if item.item == STARTING_ID + 0x0032:
                    traps = min(int.from_bytes(traps, "little") + 1, 999)
                    snes_buffered_write(ctx, DKC2_SRAM + offset, traps.to_bytes(2, "little"))
                    snes_buffered_write(ctx, DKC2_SRAM + 0x64, (90).to_bytes(2, "little"))
                else:
                    traps = min(int.from_bytes(traps, "little") + 1, 150)
                    snes_buffered_write(ctx, DKC2_SRAM + offset, traps.to_bytes(2, "little"))
                    if "TrapLink" in ctx.tags and item.item in trap_value_to_name:
                        await self.send_trap_link(ctx, trap_value_to_name[item.item])

            if sfx:
                snes_buffered_write(ctx, DKC2_SOUND_PLAYBACK, (0x0500 | sfx).to_bytes(2, "little"))

            snes_buffered_write(ctx, DKC2_RECV_INDEX, recv_index.to_bytes(2, "little"))

            await snes_flush_writes(ctx)
                
        # Handle collected locations
        nmi_pointer = await snes_read(ctx, WRAM_START + 0x0020, 0x2)
        if nmi_pointer is None:
            return
        nmi_pointer = int.from_bytes(nmi_pointer, "little")
        if nmi_pointer == 0x8CE9 or nmi_pointer == 0x8CF1:
            new_level_clear = False
            new_dk_coin = False
            new_bonus = False
            new_quiz = False
            stage_flags = list(game_flags[0x40:0x60])
            bonus_flags = list(game_flags[0x00:0x20])
            dk_coin_flags = list(game_flags[0x20:0x40])
            swanky_flags = list(swanky_flags)
            i = 0
            for loc_id in ctx.checked_locations:
                if loc_id not in ctx.locations_checked:
                    ctx.locations_checked.add(loc_id)
                    loc_name = ctx.location_names.lookup_in_game(loc_id)

                    if loc_name not in location_id_to_level_id:
                        continue

                    logging.info(f"Recovered checks ({i:03}): {loc_name}")
                    i += 1

                    data = location_id_to_level_id[loc_name]

                    loc_type = data[0]
                    level_num = data[1]
                    level_offset = (level_num >> 3) & 0x1E
                    level_bit = 1 << (level_num & 0x0F)

                    if level_num in UNCOLLECTABLE_LEVELS:
                        continue

                    if loc_type == 0x00:
                        # Level clear
                        level_data = int.from_bytes(stage_flags[level_offset:level_offset+2], "little")
                        level_data |= level_bit
                        stage_flags[level_offset:level_offset+2] = level_data.to_bytes(2, "little")
                        new_level_clear = True
                    elif loc_type == 0x02:
                        # DK Coin
                        level_data = int.from_bytes(dk_coin_flags[level_offset:level_offset+2], "little")
                        level_data |= level_bit
                        dk_coin_flags[level_offset:level_offset+2] = level_data.to_bytes(2, "little")
                        new_dk_coin = True
                    elif loc_type == 0x03:
                        # Bonus
                        level_data = int.from_bytes(bonus_flags[level_offset:level_offset+2], "little")
                        level_data |= level_bit
                        bonus_flags[level_offset:level_offset+2] = level_data.to_bytes(2, "little")
                        new_bonus = True
                    elif loc_type == 0x04:
                        # Swanky
                        bonus_offset = data[1] >> 4
                        bonus_bit = data[1] & 0x07
                        swanky_flags[bonus_offset] |= bonus_bit
                        new_quiz = True
            
            if new_level_clear:
                snes_buffered_write(ctx, DKC2_STAGE_FLAGS, bytearray(stage_flags))
            if new_dk_coin:
                snes_buffered_write(ctx, DKC2_DK_COIN_FLAGS, bytearray(dk_coin_flags))
            if new_bonus:
                snes_buffered_write(ctx, DKC2_BONUS_FLAGS, bytearray(bonus_flags))
            if new_quiz:
                snes_buffered_write(ctx, DKC2_SWANKY_FLAGS, bytearray(swanky_flags))

            await snes_flush_writes(ctx)

    async def handle_energy_link(self, ctx: "SNIContext"):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        # Deposits EnergyLink into pool
        energy_packet = await snes_read(ctx, DKC2_ENERGY_LINK_TRANSFER, 0x2)
        if energy_packet is not None:
            energy_packet = int.from_bytes(energy_packet, "little")
            energy_packet = int(energy_packet * DKC2_EXCHANGE_RATE / 10) >> 4
            if energy_packet != 0:
                await ctx.send_msgs([{
                    "cmd": "Set", 
                    "key": f"EnergyLink{ctx.team}", 
                    "slot": ctx.slot,
                    "default": 0,
                    "operations":
                        [{"operation": "add", "value": energy_packet}],
                }])
                snes_buffered_write(ctx, DKC2_ENERGY_LINK_TRANSFER, bytearray([0x00, 0x00]))

        unlocked_kongs = await snes_read(ctx, DKC2_SRAM + 0x0E, 0x01)
        barrels = await snes_read(ctx, DKC2_SRAM + 0x48, 0x02)
        if unlocked_kongs is None or barrels is None:
            return
    
        barrels = int.from_bytes(barrels, "little")
        
        if self.barrel_request == "place_request":
            self.barrel_request_tag = f"dkc2-dkbarrel-{ctx.team}-{ctx.slot}-{random.randint(0, 0xFFFFFFFF)}"
            value = DK_BARREL_BANANA_COST * DKC2_EXCHANGE_RATE
            await ctx.send_msgs([{ 
                "cmd": "Set", 
                "key": f"EnergyLink{ctx.team}", 
                "slot": ctx.slot,
                "tag": self.barrel_request_tag,
                "default": 0,
                "want_reply": True,
                "operations":
                    [{"operation": "add", "value": -value},
                    {"operation": "max", "value": 0}],
            }])
            self.barrel_request = "pending"

        elif self.barrel_request == "successful":
            barrels += 1
            barrels &= 0x00FF
            snes_buffered_write(ctx, DKC2_SRAM + 0x48, bytes([barrels]))
            self.barrel_request = ""
            logger.info(f"Delivered DK Barrel! You have {barrels} barrels pending to be actually delivered in game.")
        
        elif self.barrel_request == "not_enough_funds":
            await ctx.send_msgs([{
                "cmd": "Set", 
                "key": f"EnergyLink{ctx.team}", 
                "slot": ctx.slot,
                "default": 0,
                "operations":
                    [{"operation": "add", "value": self.barrel_request_refund}],
            }])
            self.barrel_request_refund = 0
            self.barrel_request = ""
            logger.info(f"Not enough bananas to summon a barrel! You need at least {DK_BARREL_BANANA_COST} bananas.")

        await snes_flush_writes(ctx)

    async def handle_barrel_label(self, ctx: "SNIContext"):
        try:
            from kvui import MDLabel as Label
        except ImportError:
            from kvui import Label
        from SNIClient import snes_read

        if not self.barrel_label:
            self.barrel_label = Label(text=f"", size_hint_x=None, width=120, halign="center")
            ctx.ui.connect_layout.add_widget(self.barrel_label)

        barrels = await snes_read(ctx, DKC2_SRAM + 0x48, 0x02)
        if barrels is not None:
            barrel_count = int.from_bytes(barrels, "little")
            self.barrel_label.text = f"Barrels: {barrel_count}"

    async def handle_trap_link(self, ctx: "SNIContext"):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        from .Rom import trap_data
        
        setting_data = await snes_read(ctx, DKC2_SETTINGS, 0x40)
        if setting_data is None:
            return

        if self.received_trap_link:
            trap = self.received_trap_link

            offset = trap_data[trap.item][0]
            traps = await snes_read(ctx, DKC2_SRAM + offset, 0x02)
            if traps is None:
                return
            traps = (int.from_bytes(traps, "little") + 1) & 0xFFF
            snes_buffered_write(ctx, DKC2_SRAM + offset, bytes([traps]))
            self.received_trap_link = None
            
            await snes_flush_writes(ctx)


    async def handle_messages(self, ctx: "SNIContext"):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        from .Text import message_received_to_bytes, item_names, item_order
        
        nmi_pointer = await snes_read(ctx, WRAM_START + 0x0020, 0x02)
        scene_flags = await snes_read(ctx, WRAM_START + 0x06A1, 0x02)
        gameplay_flags = await snes_read(ctx, WRAM_START + 0x08C2, 0x02)
        gamemode_pointer = await snes_read(ctx, DKC2_GAMEMODE, 0x02)
        brightness = await snes_read(ctx, DKC2_BRIGHTNESS, 0x01)
        if brightness is None or nmi_pointer is None or gamemode_pointer is None or scene_flags is None or gameplay_flags is None:
            return
        
        # Do not show messages in banned scenarios
        gamemode_pointer = int.from_bytes(gamemode_pointer, "little")
        scene_flags = int.from_bytes(scene_flags, "little")
        gameplay_flags = int.from_bytes(gameplay_flags, "little")
        if gamemode_pointer in BANNED_GAMEMODES or scene_flags & 0x3000 != 0 or gameplay_flags & 0x0040:
            return
        
        message_timer = await snes_read(ctx, DKC2_MESSAGE_TIMER, 0x02)
        message_phase = await snes_read(ctx, DKC2_MESSAGE_PHASE, 0x02)
        message_rerun = await snes_read(ctx, DKC2_MESSAGE_RERUN, 0x02)
        controller_flags = await snes_read(ctx, WRAM_START + 0x0507, 0x02)
        if message_timer is None or message_phase is None or message_rerun is None or controller_flags is None:
            return
        
        # Rerun last message if it got caught during a screen transition
        message_rerun = int.from_bytes(message_rerun, "little")
        if message_rerun:
            self.message_queue.insert(0, self.last_message.copy())
            snes_buffered_write(ctx, DKC2_MESSAGE_RERUN, (0x00).to_bytes(2, "little"))
            await snes_flush_writes(ctx)
            return 
        
        # Skip messages if the message isn't done showing up or the brightness isn't at full
        # Also add "tap SELECT" and not holding, tap action isn't cleared until the map starts fading in
        message_timer = int.from_bytes(message_timer, "little")
        message_phase = int.from_bytes(message_phase, "little")
        brightness = int.from_bytes(brightness, "little")
        controller_flags = int.from_bytes(controller_flags, "little")
        if message_phase or message_timer or brightness & 0x0F != 0x0F or controller_flags & 0x0020:
            return
        
        # Show tracker instead if it's requested from the server, only when there's not a message queue going on
        message_is_tracker = await snes_read(ctx, DKC2_MESSAGE_TRACKER, 0x02)
        save_data = await snes_read(ctx, DKC2_SRAM, 0x40)
        if message_is_tracker is None or save_data is None:
            return
        message_is_tracker = int.from_bytes(message_is_tracker, "little")
        if message_is_tracker and len(self.message_queue) == 0:
            # Build strings based on unlock data
            save_data = list(save_data)
            slot = ""
            unlocks = []
            # Special case Diddy and Dixie
            if save_data[0x0E] & 0x01:
                slot += "DIDDY "
            if save_data[0x0E] & 0x02:
                slot += "DIXIE "
            for idx in item_order:
                if not save_data[idx]:
                    continue
                current_name = item_names[idx]
                if len(slot) + len(current_name) >= 30:
                    # Split messages longer than 30 chars
                    unlocks.append(slot[:-1])
                    slot = ""
                slot += f"{current_name} "
            else:
                unlocks.append(slot[:-1])

            # Queue messages
            for msg in unlocks:
                self.message_queue.append([True, "UNLOCKED ITEMS", msg])

            # Queue token/rock data
            self.message_queue.append([True, f"BOSS TOKENS: {save_data[0x24]}", f"LOST WORLD ROCKS: {save_data[0x2F]}"])

            # Queue world unlocks
            line_1 = "WORLDS: "
            line_2 = "LOST WORLD: "
            for idy in range(0x28, 0x2F):
                if save_data[idy]:
                    line_1 += f"{item_names[idy]} "
            for idy in range(0x30, 0x35):
                if save_data[idy]:
                    line_2 += f"{item_names[idy]} "
            self.message_queue.append([True, line_1[:-1], line_2[:-1]])

            # Clear tracker flag
            snes_buffered_write(ctx, DKC2_MESSAGE_TRACKER, (0x00).to_bytes(2, "little"))
            await snes_flush_writes(ctx)

        # Return if there's not a pending queue
        if len(self.message_queue) == 0:
            return
        
        self.last_message = self.message_queue.pop(0)
        nmi_pointer = int.from_bytes(nmi_pointer, "little")
        in_map = nmi_pointer == 0x8CE9 or nmi_pointer == 0x8CF1

        # Early return for non tracker messages
        if not self.last_message[0]:
            classification = self.last_message[3]
            is_received = self.last_message[4]
            if is_received:
                if not self.slot_data["display_messages"] & 0x02:
                    return
                current_filter = self.slot_data["received_message_filter"]
            else:
                if not self.slot_data["display_messages"] & 0x01:
                    return
                current_filter = self.slot_data["sent_message_filter"]

            if classification & 0x01 and "Progression" in current_filter:
                pass
            elif classification & 0x02 and "Useful" in current_filter:
                pass
            elif classification & 0x04 and "Trap" in current_filter:
                pass
            elif classification == 0x00 and "Filler" in current_filter:
                pass
            else:
                return
        
        message_buffer = message_received_to_bytes(ctx, self.last_message, in_map)
        message_colors = self.parse_client_colors(ctx)
        
        snes_buffered_write(ctx, DKC2_MESSAGE_TIMER, (180).to_bytes(2, "little"))
        snes_buffered_write(ctx, DKC2_MESSAGE_ACTIVATE, (0x01).to_bytes(2, "little"))
        snes_buffered_write(ctx, DKC2_MESSAGE_BUFFER, message_buffer)
        snes_buffered_write(ctx, DKC2_PALETTE_BUFFER, message_colors)
        await snes_flush_writes(ctx)

    def parse_client_colors(self, ctx: "SNIContext"):
        from .Aesthetics import get_palette_bytes

        color_codes = ctx.ui.json_to_kivy_parser.color_codes
        palette = [
            "$0000","$7FFF","$0000","$6318",
            "$0000","$FFFF","$0000","$6318",
            "$0000","$FFFF","$0000","$6318",
            "$0000","$00FF","$0000","$6318",
            
            "$0000","$037F","$0000","$6318",
            "$0000","$7A76","$0000","$6318",
            "$0000","$762E","$0000","$6318",
            "$0000","$7BC0","$0000","$6318",
        ]
        palette[0x05] = f"#{color_codes['magenta']}"
        palette[0x09] = f"#{color_codes['yellow']}"
        palette[0x0D] = f"#{color_codes['salmon']}"
        if "golden" in color_codes:
            palette[0x11] = f"#{color_codes['golden']}"
        palette[0x15] = f"#{color_codes['plum']}"
        palette[0x19] = f"#{color_codes['slateblue']}"
        palette[0x1D] = f"#{color_codes['cyan']}"

        return get_palette_bytes(palette)


    async def deathlink_kill_player(self, ctx: "SNIContext"):
        from SNIClient import DeathState, snes_buffered_write, snes_flush_writes, snes_read

        # Discard killing from death link
        death_link_flag = await snes_read(ctx, DKC2_DEATH_LINK_FLAG, 0x01)
        if death_link_flag is None:
            return
        if death_link_flag[0]:
            return
        
        # Discard killing from the map
        nmi_pointer = await snes_read(ctx, WRAM_START + 0x0020, 0x2)
        if nmi_pointer is None:
            return
        nmi_pointer = int.from_bytes(nmi_pointer, "little")
        if nmi_pointer == 0x8CE9 or nmi_pointer == 0x8CF1:
            return
            
        snes_buffered_write(ctx, DKC2_DEATH_LINK_FORCE, bytes([0x01]))
        snes_buffered_write(ctx, DKC2_DEATH_LINK_FLAG, bytes([0x01]))
        await snes_flush_writes(ctx)

        ctx.death_state = DeathState.dead
        ctx.last_death_link = time.time()


    async def send_trap_link(self, ctx: SNIClient, trap_name: str):
        if "TrapLink" not in ctx.tags or ctx.slot == None:
            return

        await ctx.send_msgs([{
            "cmd": "Bounce", "tags": ["TrapLink"],
            "data": {
                "time": time.time(),
                "source": ctx.player_names[ctx.slot],
                "trap_name": trap_name
            }
        }])
        snes_logger.info(f"Sent linked {trap_name}")


    def on_package(self, ctx: "SNIContext", cmd: str, args: dict):
        super().on_package(ctx, cmd, args)

        if cmd == "Connected":
            self.slot_data = args.get("slot_data", None)
            self.barrel_request = ""
            if self.slot_data["energy_link"]:
                ctx.set_notify(f"EnergyLink{ctx.team}")
                if ctx.ui:
                    ctx.ui.enable_energy_link()
                    ctx.ui.energy_link_label.text = "Bananas: Standby"
                    snes_logger.info(f"Initialized EnergyLink{ctx.team}")

        elif cmd == "SetReply" and args["key"].startswith("EnergyLink"):
            if self.barrel_request == "pending" and "tag" in args:
                if args["tag"] == self.barrel_request_tag:
                    self.barrel_request_tag = ""
                    dk_barrel_cost = DKC2_EXCHANGE_RATE * DK_BARREL_BANANA_COST
                    if args["original_value"] < dk_barrel_cost:
                        # send back the original value
                        value = args["original_value"]
                        self.barrel_request = "not_enough_funds"
                        self.barrel_request_refund = value
                    else: 
                        value = args["value"]
                        self.barrel_request = "successful"
            else: 
                value = args["value"]
                    
            if ctx.ui:
                pool = (value or 0) /  DKC2_EXCHANGE_RATE
                ctx.ui.energy_link_label.text = f"Bananas: {float(pool):.2f}"

        elif cmd == "Retrieved":
            if f"EnergyLink{ctx.team}" in args["keys"] and args["keys"][f"EnergyLink{ctx.team}"] and ctx.ui:
                pool = (args["keys"][f"EnergyLink{ctx.team}"] or 0) / DKC2_EXCHANGE_RATE
                ctx.ui.energy_link_label.text = f"Bananas: {float(pool):.2f}"
        
        elif cmd == "Bounced":
            if "tags" not in args:
                return
            if not hasattr(self, "instance_id"):
                self.instance_id = time.time()
            
            source_name = args["data"]["source"]
            if "TrapLink" in ctx.tags and "TrapLink" in args["tags"] and source_name != ctx.slot_info[ctx.slot].name:
                trap_name: str = args["data"]["trap_name"]
                if trap_name not in trap_name_to_value:
                    return
                
                trap_id: int = trap_name_to_value[trap_name]
                if "trap_weights" not in self.slot_data:
                    return
                if f"{trap_id}" not in self.slot_data["trap_weights"]:
                    return
                if self.slot_data["trap_weights"][f"{trap_id}"] == 0:
                    # The player disabled this trap type
                    return
                
                self.received_trap_link = NetworkItem(trap_name_to_value[trap_name], None, None)
                self.message_queue.append([False, "TrapLink", trap_name, 0x04, True])

        elif cmd == "LocationInfo":
            for item in args["locations"]:
                item: NetworkItem
                if item.player != ctx.slot and item.location in self.current_session_locations and item.location not in self.processed_locations:
                    self.processed_locations.add(item.location)
                    self.message_queue.append([False, ctx.player_names[item.player], ctx.item_names.lookup_in_slot(item.item, item.player), item.flags, False])


def cmd_request(self):
    """
    Request a DK Barrel from the banana pool (EnergyLink).
    """
    if self.ctx.game != "Donkey Kong Country 2":
        logger.warning("This command can only be used while playing Donkey Kong Country 2")
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.info(f"Must be connected to server and in game.")
    else:
        if self.ctx.client_handler.barrel_request != "":
            logger.info(f"You already have a DK Barrel in queue.")
            return
        else:
            self.ctx.client_handler.barrel_request = "place_request"
            logger.info(f"Placing a DK barrel request...")
