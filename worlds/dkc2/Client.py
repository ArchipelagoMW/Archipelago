import logging
import asyncio
import time
import random

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient

logger = logging.getLogger("Client")
snes_logger = logging.getLogger("SNES")

# FXPAK Pro protocol memory mapping used by SNI
ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

STARTING_ID = 0xBF0000

DKC2_SETTINGS = ROM_START + 0x3DFF80

DKC2_MISC_FLAGS = WRAM_START + 0x08D2
DKC2_GAME_FLAGS = WRAM_START + 0x59B2

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

DKC2_GAME_TIME = WRAM_START + 0x00D5
DKC2_IN_LEVEL = WRAM_START + 0x01FF
DKC2_CURRENT_LEVEL = WRAM_START + 0x08A8    # 0xD3?
DKC2_LOADED_LEVEL = WRAM_START + 0x00D3
DKC2_CURRENT_MODE = WRAM_START + 0x00D0
DKC2_CURRENT_MAP = WRAM_START + 0x06B1

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

DKC2_ENERGY_LINK_TRANSFER = DKC2_SRAM + 0x04E
DKC2_EXCHANGE_RATE = 200000000
DK_BARREL_BANANA_COST = 25
DK_BARREL_MAX = 3

DKC2_ROMHASH_START = 0xFFC0
ROMHASH_SIZE = 0x15

UNCOLLECTABLE_LEVELS = [0x09, 0x21, 0x63, 0x60, 0x0D]

class DKC2SNIClient(SNIClient):
    game = "Donkey Kong Country 2"
    patch_suffix = ".apdkc2"

    def __init__(self):
        super().__init__()
        self.game_state = False
        self.using_newer_client = False
        self.energy_link_enabled = False
        self.barrel_request = ""
        self.current_map = 0

    async def deathlink_kill_player(self, ctx):
        from SNIClient import DeathState, snes_buffered_write, snes_flush_writes, snes_read

        traps = await snes_read(ctx, DKC2_SRAM + 0x46, 0x02)
        if traps is None:
            return
        
        traps = int.from_bytes(traps, "little") + 1
        traps &= 0x00FF
        snes_buffered_write(ctx, DKC2_SRAM + + 0x46, bytes([traps]))

        await snes_flush_writes(ctx)

        ctx.death_state = DeathState.dead
        ctx.last_death_link = time.time()


    async def validate_rom(self, ctx):
        from SNIClient import snes_read

        setting_data = await snes_read(ctx, DKC2_SETTINGS, 0x40)
        rom_name = await snes_read(ctx, DKC2_ROMHASH_START, ROMHASH_SIZE)

        if rom_name is None or setting_data is None or rom_name == bytes([0] * ROMHASH_SIZE) or rom_name[:4] != b"DKC2":
            if "barrel" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("barrel")
            return False
        
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.receive_option = 0
        ctx.send_option = 0
        ctx.allow_collect = True

        energy_link = setting_data[0x19]
        if energy_link:
            if "barrel" not in ctx.command_processor.commands:
                ctx.command_processor.commands["barrel"] = cmd_barrel

        death_link = setting_data[0x18]
        if death_link:
            await ctx.update_death_link(bool(death_link & 0b1))

        ctx.rom = rom_name

        return True


    async def game_watcher(self, ctx):
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
            currently_dead = player_state[0] & 0x20
            await ctx.handle_deathlink_state(currently_dead)

        # This is going to be rewritten whenever SNIClient supports on_package
        energy_link = setting_data[0x19]
        if self.using_newer_client:
            if energy_link != 0:
                await self.handle_energy_link(ctx)
        else:
            if energy_link != 0:
                if self.energy_link_enabled and f'EnergyLink{ctx.team}' in ctx.stored_data:
                    await self.handle_energy_link(ctx)

                if ctx.server and ctx.server.socket.open and not self.energy_link_enabled and ctx.team is not None:
                    self.energy_link_enabled = True
                    ctx.set_notify(f"EnergyLink{ctx.team}")
                    ctx.barrel_request = ""
                    snes_logger.info(f"Initialized EnergyLink{ctx.team}")

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

        dk_coins_as_checks = setting_data[0x1A]
        kong_as_checks = setting_data[0x1B]
        balloons_as_checks = setting_data[0x1C]
        coins_as_checks = setting_data[0x1D]
        bunches_as_checks = setting_data[0x1E]
        swanky_as_checks = setting_data[0x1F]

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

        # Send current map to poptracker
        if nmi_pointer == 0x8CE9 or nmi_pointer == 0x8CF1:
            current_map = int.from_bytes(current_map, "little")
            if self.current_map != current_map:
                self.current_map = current_map
                await ctx.send_msgs([{
                    "cmd": "Set", 
                    "key": f"dkc2_current_map_{ctx.team}_{ctx.slot}", 
                    "default": 0,
                    "want_reply": False,
                    "operations":
                        [{"operation": "replace", "value": self.current_map}],
                }])

        # Receive items
        rom = await snes_read(ctx, DKC2_ROMHASH_START, ROMHASH_SIZE)
        if rom != ctx.rom:
            ctx.rom = None
            snes_logger.info(f'Exit ROM.')
            return
        
        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
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
                currency = await snes_read(ctx, addr, 0x02)
                if currency is None:
                    recv_index -= 1
                    return
                currency = int.from_bytes(currency, "little")
                currency &= 0x00FF
                if currency < 99:
                    currency += 1
                    snes_buffered_write(ctx, addr, currency.to_bytes(1, "little"))

            # Give traps 
            elif item.item in trap_data:
                offset = trap_data[item.item][0]
                sfx = trap_data[item.item][1]
                traps = await snes_read(ctx, DKC2_SRAM + offset, 0x02)
                if traps is None:
                    recv_index -= 1
                    return
                traps = (int.from_bytes(traps, "little") + 1) & 0xFFF
                snes_buffered_write(ctx, DKC2_SRAM + offset, bytes([traps]))

            if sfx:
                snes_buffered_write(ctx, DKC2_SOUND_BUFFER, bytearray([sfx, 0x05]))
                snes_buffered_write(ctx, DKC2_EFFECT_BUFFER + 0x05, bytearray([sfx]))
                snes_buffered_write(ctx, DKC2_SPC_INDEX, bytearray([0x00]))
                snes_buffered_write(ctx, DKC2_SPC_NEXT_INDEX, bytearray([0x00]))

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

    async def handle_energy_link(self, ctx):
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
        
        if unlocked_kongs[0] == 0x03:
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
                snes_buffered_write(ctx, DKC2_SRAM + + 0x48, bytes([barrels]))
                self.barrel_request = ""
                logger.info(f"Delivered DK Barrel! You have {barrels}/{DK_BARREL_MAX} barrels pending to be actually delivered in game.")
            
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


    async def deathlink_kill_player(self, ctx):
        from SNIClient import DeathState, snes_buffered_write, snes_flush_writes, snes_read

        addr = DKC2_INSTA_DEATH_FLAG
        currency = await snes_read(ctx, addr, 0x02)
        if currency is None:
            return
        currency = int.from_bytes(currency, "little") + 1
        currency &= 0x0FFF
        snes_buffered_write(ctx, addr, bytes([currency]))

        await snes_flush_writes(ctx)

        ctx.death_state = DeathState.dead
        ctx.last_death_link = time.time()


    def on_package(self, ctx, cmd: str, args: dict):
        super().on_package(ctx, cmd, args)

        if cmd == "Connected":
            slot_data = args.get("slot_data", None)
            self.using_newer_client = True
            self.barrel_request = ""
            if slot_data["energy_link"]:
                ctx.set_notify(f"EnergyLink{ctx.team}")
                if ctx.ui:
                    ctx.ui.enable_energy_link()
                    ctx.ui.energy_link_label.text = "Bananas: Standby"
                    snes_logger.info(f"Initialized EnergyLink{ctx.team}")

        elif cmd == "SetReply" and args["key"].startswith("EnergyLink"):
            if self.barrel_request == "pending":
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

def cmd_barrel(self):
    """
    Request a DK Barrel from the banana pool (EnergyLink).
    """
    if self.ctx.game != "Donkey Kong Country 2":
        logger.warning("This command can only be used while playing Donkey Kong Country 2")
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.info(f"Must be connected to server and in game.")
    else:
        if self.ctx.client_handler.using_newer_client is False:
            logger.info(f"This function is only enabled for Archipelago 0.6.0.")
            return
        if self.ctx.client_handler.barrel_request != "":
            logger.info(f"You already have a DK Barrel in queue.")
            return
        else:
            self.ctx.client_handler.barrel_request = "place_request"
            logger.info(f"Placing a DK barrel request...")
