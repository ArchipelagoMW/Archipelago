import logging
import asyncio
import time

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient

logger = logging.getLogger("Client")
snes_logger = logging.getLogger("SNES")

# FXPAK Pro protocol memory mapping used by SNI
ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

MMX3_GAME_STATE         = WRAM_START + 0x000D0
MMX3_MENU_STATE         = WRAM_START + 0x000D1
MMX3_GAMEPLAY_STATE     = WRAM_START + 0x000D2
MMX3_PAUSE_STATE        = WRAM_START + 0x01F37
MMX3_LEVEL_INDEX        = WRAM_START + 0x01FAE
MMX3_WEAPON_ARRAY       = WRAM_START + 0x01FBC
MMX3_HEART_TANKS        = WRAM_START + 0x01FD4
MMX3_SUB_TANK_ARRAY     = WRAM_START + 0x01FB7
MMX3_RIDE_CHIPS         = WRAM_START + 0x01FD7
MMX3_UPGRADES           = WRAM_START + 0x01FD1
MMX3_CURRENT_HP         = WRAM_START + 0x009FF
MMX3_MAX_HP             = WRAM_START + 0x01FD2
MMX3_LIFE_COUNT         = WRAM_START + 0x01FB4
MMX3_ACTIVE_CHARACTER   = WRAM_START + 0x00A8E
MMX3_ZSABER             = WRAM_START + 0x01FB2
MMX3_CAN_MOVE           = WRAM_START + 0x01F45
MMX3_GOING_THROUGH_GATE = WRAM_START + 0x01F25
MMX3_HYPER_CANNON       = WRAM_START + 0x01FCC

MMX3_ENABLE_HEART_TANK  = WRAM_START + 0x0F4E0
MMX3_ENABLE_HP_REFILL   = WRAM_START + 0x0F4E4
MMX3_HP_REFILL_AMOUNT   = WRAM_START + 0x0F4E5
MMX3_ENABLE_GIVE_1UP    = WRAM_START + 0x0F4E7
MMX3_RECEIVING_ITEM     = WRAM_START + 0x0F4FF

MMX3_SFX_FLAG   = WRAM_START + 0x0F469
MMX3_SFX_NUMBER = WRAM_START + 0x0F46A

MMX3_VALIDATION_CHECK = WRAM_START + 0x0F43D

MMX3_BIT_BYTE_VILE          = WRAM_START + 0x01FD8
MMX3_LEVEL_CLEARED          = WRAM_START + 0x0F400
MMX3_UNLOCKED_LEVELS        = WRAM_START + 0x0F420
MMX3_DEFEATED_BOSSES        = WRAM_START + 0x0F440
MMX3_DOPPLER_ACCESS         = WRAM_START + 0x0F461
MMX3_VILE_ACCESS            = WRAM_START + 0x0F466
MMX3_COLLECTED_HEART_TANKS  = WRAM_START + 0x0F462
MMX3_COLLECTED_UPGRADES     = WRAM_START + 0x0F463
MMX3_COLLECTED_RIDE_CHIPS   = WRAM_START + 0x0F464
MMX3_COLLECTED_SUB_TANKS    = WRAM_START + 0x0F465
MMX3_COLLECTED_PICKUPS      = WRAM_START + 0x0F480
MMX3_COMPLETED_REMATCHES    = WRAM_START + 0x01FDA
MMX3_ENERGY_LINK_PACKET     = WRAM_START + 0x0F467

MMX3_PICKUPSANITY_ACTIVE    = ROM_START + 0x17FFE7
MMX3_REQUIRED_REMATCHES     = ROM_START + 0x17FFF3
MMX3_ENERGY_LINK_ENABLED    = ROM_START + 0x17FFF7

HP_EXCHANGE_RATE = 1500000

MMX3_RECV_INDEX = WRAM_START + 0x0F460

MMX3_ROMHASH_START = 0x7FC0
ROMHASH_SIZE = 0x15

X_Z_ITEMS = ["small hp refill", "large hp refill", "1up", "hp refill"]
HP_REFILLS = ["small hp refill", "large hp refill", "hp refill"]

class MMX3SNIClient(SNIClient):
    game = "Mega Man X3"

    def __init__(self):
        super().__init__()
        self.game_state = False
        self.last_death_link = 0
        self.auto_heal = False
        self.energy_link_enabled = False
        self.heal_request_command = None
        self.item_queue = []


    async def deathlink_kill_player(self, ctx):
        from SNIClient import DeathState, snes_buffered_write, snes_flush_writes, snes_read

        validation = await snes_read(ctx, MMX3_VALIDATION_CHECK, 0x2)
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            return
        menu_state = await snes_read(ctx, MMX3_MENU_STATE, 0x1)
        if menu_state[0] != 0x04:
            return
        gameplay_state = await snes_read(ctx, MMX3_GAMEPLAY_STATE, 0x1)
        if gameplay_state[0] != 0x04:
            return
        pause_state = await snes_read(ctx, MMX3_PAUSE_STATE, 0x1)
        if pause_state[0] != 0x00:
            return
        
        snes_buffered_write(ctx, MMX3_CURRENT_HP, bytes([0x80]))
        snes_buffered_write(ctx, WRAM_START + 0x00A7B, bytes([0x80]))
        ram_0A7D = await snes_read(ctx, WRAM_START + 0x00A7D, 1)
        ram_0A7D = ram_0A7D[0] & 0x7F
        snes_buffered_write(ctx, WRAM_START + 0x00A7D, bytes([ram_0A7D]))

        await snes_flush_writes(ctx)

        ctx.death_state = DeathState.dead
        ctx.last_death_link = time.time()


    async def validate_rom(self, ctx):
        from SNIClient import snes_read

        rom_name = await snes_read(ctx, MMX3_ROMHASH_START, ROMHASH_SIZE)
        if rom_name is None or rom_name == bytes([0] * ROMHASH_SIZE) or rom_name[:4] != b"MMX3":
            if "pool" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("pool")
            if "heal" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("heal")
            if "autoheal" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("autoheal")
            return False
        
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.receive_option = 0
        ctx.send_option = 0
        ctx.allow_collect = True
        if "pool" not in ctx.command_processor.commands:
            ctx.command_processor.commands["pool"] = cmd_pool
        if "heal" not in ctx.command_processor.commands:
            ctx.command_processor.commands["heal"] = cmd_heal
        if "autoheal" not in ctx.command_processor.commands:
            ctx.command_processor.commands["autoheal"] = cmd_autoheal

        death_link = False
        if death_link:
            await ctx.update_death_link(bool(death_link[0] & 0b1))

        ctx.rom = rom_name

        return True
    
            
    async def handle_energy_link(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        
        # Deposit heals into the pool regardless of energy_link setting
        energy_packet = await snes_read(ctx, MMX3_ENERGY_LINK_PACKET, 0x2)
        if energy_packet is None:
            return
        energy_packet_raw = energy_packet[0] | (energy_packet[1] << 8)
        energy_packet = (energy_packet_raw * HP_EXCHANGE_RATE) >> 4
        if energy_packet != 0:
            await ctx.send_msgs([{
                "cmd": "Set", "key": f"EnergyLink{ctx.team}", "operations":
                    [{"operation": "add", "value": energy_packet},
                    {"operation": "max", "value": 0}],
            }])
            pool = (ctx.stored_data[f"EnergyLink{ctx.team}"] / HP_EXCHANGE_RATE) + (energy_packet_raw / 16)
            logger.info(f"Deposited {energy_packet_raw / 16:.2f} into the healing pool. Healing available: {pool:.2f}")
            snes_buffered_write(ctx, MMX3_ENERGY_LINK_PACKET, bytearray([0x00, 0x00]))
            await snes_flush_writes(ctx)

        energy_link = await snes_read(ctx, MMX3_ENERGY_LINK_ENABLED, 0x1)
        if energy_link is None:
            return

        if energy_link[0]:
            validation = await snes_read(ctx, MMX3_VALIDATION_CHECK, 0x2)
            if validation is None:
                return
            validation = validation[0] | (validation[1] << 8)
            if validation != 0xDEAD:
                return

            receiving_item = await snes_read(ctx, MMX3_RECEIVING_ITEM, 0x1)
            menu_state = await snes_read(ctx, MMX3_MENU_STATE, 0x1)
            gameplay_state = await snes_read(ctx, MMX3_GAMEPLAY_STATE, 0x1)
            can_move = await snes_read(ctx, MMX3_CAN_MOVE, 0x1)
            going_through_gate = await snes_read(ctx, MMX3_GOING_THROUGH_GATE, 0x4)
            pause_state = await snes_read(ctx, MMX3_PAUSE_STATE, 0x1)
            if menu_state[0] != 0x04 or \
                gameplay_state[0] != 0x04 or \
                can_move[0] != 0x00 or \
                pause_state[0] != 0x00 or \
                receiving_item[0] != 0x00 or \
                (
                    going_through_gate[0] != 0x00 and \
                    going_through_gate[1] != 0x00 and \
                    going_through_gate[2] != 0x00 and \
                    going_through_gate[3] != 0x00 \
                ):
                return

            if any(item in self.item_queue for item in HP_REFILLS):
                logger.info(f"Can't provide a heal. You already have a heal in queue.")
                self.heal_request_command = None
                return

            # Perform auto heals
            if self.auto_heal:
                if self.heal_request_command is None:
                    if ctx.stored_data[f"EnergyLink{ctx.team}"] < HP_EXCHANGE_RATE:
                        return
                    current_hp = await snes_read(ctx, MMX3_CURRENT_HP, 0x1)
                    max_hp = await snes_read(ctx, MMX3_MAX_HP, 0x1)
                    if max_hp[0] > current_hp[0]:
                        self.heal_request_command = max_hp[0] - current_hp[0]

            # Handle manual heal requests
            if self.heal_request_command:
                heal_needed = self.heal_request_command
                heal_needed_rate = heal_needed * HP_EXCHANGE_RATE
                if f"EnergyLink{ctx.team}" in ctx.stored_data and ctx.stored_data[f"EnergyLink{ctx.team}"]:
                    if ctx.stored_data[f"EnergyLink{ctx.team}"] < heal_needed_rate:
                        heal_needed = int(ctx.stored_data[f"EnergyLink{ctx.team}"] / HP_EXCHANGE_RATE)
                        if heal_needed == 0:
                            logger.info(f"There's not enough healing for your request ({heal_needed}). Healing available: 0")
                            self.heal_request_command = None
                            return 
                        heal_needed_rate = heal_needed * HP_EXCHANGE_RATE
                    await ctx.send_msgs([{
                        "cmd": "Set", "key": f"EnergyLink{ctx.team}", "operations":
                            [{"operation": "add", "value": -heal_needed_rate},
                            {"operation": "max", "value": 0}],
                    }])
                    self.add_item_to_queue("hp refill", None, self.heal_request_command)
                    pool = (ctx.stored_data[f"EnergyLink{ctx.team}"] / HP_EXCHANGE_RATE) - heal_needed
                    logger.info(f"Healed by {heal_needed}. Healing available: {pool:.2f}")
                else: 
                    logger.info(f"Failed to initialize EnergyLink.")
                self.heal_request_command = None


    def add_item_to_queue(self, item_type, item_id, item_additional = None):
        if not hasattr(self, "item_queue"):
            self.item_queue = []
        self.item_queue.append([item_type, item_id, item_additional])

    async def handle_item_queue(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        from worlds.mmx3.Rom import weapon_rom_data, ride_armor_rom_data, upgrades_rom_data

        if not hasattr(self, "item_queue") or len(self.item_queue) == 0:
            return

        validation = await snes_read(ctx, MMX3_VALIDATION_CHECK, 0x2)
        if validation is None:
            return
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            return

        next_item = self.item_queue[0]
        item_id = next_item[1]
        
        if next_item[0] == "boss access":
            snes_buffered_write(ctx, MMX3_SFX_FLAG, bytearray([0x01]))
            snes_buffered_write(ctx, MMX3_SFX_NUMBER, bytearray([0x1D]))
            self.item_queue.pop(0)
            return
        
        # Do not give items if you can't move, are in pause state, not in the correct mode or not in gameplay state
        receiving_item = await snes_read(ctx, MMX3_RECEIVING_ITEM, 0x1)
        menu_state = await snes_read(ctx, MMX3_MENU_STATE, 0x1)
        gameplay_state = await snes_read(ctx, MMX3_GAMEPLAY_STATE, 0x1)
        can_move = await snes_read(ctx, MMX3_CAN_MOVE, 0x1)
        going_through_gate = await snes_read(ctx, MMX3_GOING_THROUGH_GATE, 0x4)
        pause_state = await snes_read(ctx, MMX3_PAUSE_STATE, 0x1)
        if menu_state[0] != 0x04 or \
            gameplay_state[0] != 0x04 or \
            can_move[0] != 0x00 or \
            pause_state[0] != 0x00 or \
            receiving_item[0] != 0x00 or \
            (
                going_through_gate[0] != 0x00 and \
                going_through_gate[1] != 0x00 and \
                going_through_gate[2] != 0x00 and \
                going_through_gate[3] != 0x00 \
            ):
            return
        
        # Handle items that Zero can also get
        if next_item[0] in X_Z_ITEMS:
            backup_item = self.item_queue.pop(0)
            if "hp refill" in next_item[0]:
                current_hp = await snes_read(ctx, MMX3_CURRENT_HP, 0x1)
                max_hp = await snes_read(ctx, MMX3_MAX_HP, 0x1)

                if current_hp[0] < max_hp[0]:
                    snes_buffered_write(ctx, MMX3_ENABLE_HP_REFILL, bytearray([0x02]))
                    if next_item[0] == "small hp refill":
                        snes_buffered_write(ctx, MMX3_HP_REFILL_AMOUNT, bytearray([0x02]))
                    elif next_item[0] == "large hp refill":
                        snes_buffered_write(ctx, MMX3_HP_REFILL_AMOUNT, bytearray([0x08]))
                    else:
                        snes_buffered_write(ctx, MMX3_HP_REFILL_AMOUNT, bytearray([next_item[2]]))
                    snes_buffered_write(ctx, MMX3_RECEIVING_ITEM, bytearray([0x01]))
                else:
                    # TODO: Sub Tank logic
                    self.item_queue.append(backup_item)

            elif next_item[0] == "1up":
                life_count = await snes_read(ctx, MMX3_LIFE_COUNT, 0x1)
                if life_count[0] < 9:
                    snes_buffered_write(ctx, MMX3_ENABLE_GIVE_1UP, bytearray([0x01]))
                    snes_buffered_write(ctx, MMX3_RECEIVING_ITEM, bytearray([0x01]))
                else:
                    self.item_queue.append(backup_item)

        # Ignore Zero for the following items
        active_character = await snes_read(ctx, MMX3_ACTIVE_CHARACTER, 0x1)
        if active_character[0] != 0x00:
            await snes_flush_writes(ctx)
            return

        if next_item[0] == "weapon":
            # TODO: Send a signal to play back a SFX
            weapon = weapon_rom_data[item_id]
            snes_buffered_write(ctx, WRAM_START + weapon[0], bytearray([weapon[1]]))
            snes_buffered_write(ctx, MMX3_SFX_FLAG, bytearray([0x01]))
            snes_buffered_write(ctx, MMX3_SFX_NUMBER, bytearray([0x16]))
            self.item_queue.pop(0)
            
        elif next_item[0] == "heart tank":
            heart_tanks = await snes_read(ctx, MMX3_HEART_TANKS, 0x1)
            heart_tanks = heart_tanks[0]
            heart_tank_count = heart_tanks.bit_count()
            if heart_tank_count < 8:
                heart_tanks |= 1 << heart_tank_count
                snes_buffered_write(ctx, MMX3_HEART_TANKS, bytearray([heart_tanks]))
                snes_buffered_write(ctx, MMX3_ENABLE_HEART_TANK, bytearray([0x02]))
                snes_buffered_write(ctx, MMX3_RECEIVING_ITEM, bytearray([0x01]))
            self.item_queue.pop(0)

        elif next_item[0] == "sub tank":
            upgrades = await snes_read(ctx, MMX3_UPGRADES, 0x1)
            sub_tanks = await snes_read(ctx, MMX3_SUB_TANK_ARRAY, 0x4)
            sub_tanks = list(sub_tanks)
            upgrade = upgrades[0]
            upgrade = upgrade & 0xF0
            sub_tank_count = upgrade.bit_count()
            if sub_tank_count < 4:
                upgrade = upgrades[0]
                upgrade |= 0x10 << sub_tank_count
                sub_tanks[sub_tank_count] = 0x8E
                snes_buffered_write(ctx, MMX3_UPGRADES, bytearray([upgrade]))
                snes_buffered_write(ctx, MMX3_SUB_TANK_ARRAY, bytearray(sub_tanks))
                snes_buffered_write(ctx, MMX3_SFX_FLAG, bytearray([0x01]))
                snes_buffered_write(ctx, MMX3_SFX_NUMBER, bytearray([0x17]))
                #snes_buffered_write(ctx, MMX3_RECEIVING_ITEM, bytearray([0x01]))
            self.item_queue.pop(0)
        
        elif next_item[0] == "upgrade":
            upgrades = await snes_read(ctx, MMX3_UPGRADES, 0x1)
            chips = await snes_read(ctx, MMX3_RIDE_CHIPS, 0x1)

            upgrade = upgrades_rom_data[item_id]
            bit = 1 << upgrade[0]
            check = upgrades[0] & bit

            if check == 0:
                # Armor
                upgrades = upgrades[0]
                upgrades |= bit
                snes_buffered_write(ctx, MMX3_UPGRADES, bytearray([upgrades]))
                if bit == 0x01:
                    snes_buffered_write(ctx, WRAM_START + 0x09EE, bytearray([0x18]))
                elif bit == 0x02:
                    value = await snes_read(ctx, WRAM_START + 0x0B28, 0x1)
                    snes_buffered_write(ctx, WRAM_START + 0x0AE8, bytearray([value[0] + 1]))
                    snes_buffered_write(ctx, WRAM_START + 0x0AF2, bytearray([0x00]))
                    snes_buffered_write(ctx, WRAM_START + 0x0AF3, bytearray([0x00]))
                    snes_buffered_write(ctx, WRAM_START + 0x0AE9, bytearray([0x00]))
                    snes_buffered_write(ctx, WRAM_START + 0x0AF8, bytearray([0x5D]))
                elif bit == 0x04:
                    value = await snes_read(ctx, WRAM_START + 0x0B28, 0x1)
                    snes_buffered_write(ctx, WRAM_START + 0x0B08, bytearray([value[0] + 1]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B12, bytearray([0x00]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B13, bytearray([0x01]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B09, bytearray([0x00]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B18, bytearray([0x5D]))
                elif bit == 0x08:
                    value = await snes_read(ctx, WRAM_START + 0x0B28, 0x1)
                    snes_buffered_write(ctx, WRAM_START + 0x0B28, bytearray([value[0] + 1]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B32, bytearray([0x00]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B33, bytearray([0x02]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B29, bytearray([0x00]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B38, bytearray([0x5D]))
                snes_buffered_write(ctx, MMX3_SFX_FLAG, bytearray([0x01]))
                snes_buffered_write(ctx, MMX3_SFX_NUMBER, bytearray([0x1B]))
                #snes_buffered_write(ctx, MMX3_RECEIVING_ITEM, bytearray([0x01]))
            else:
                # Chip
                bit = bit << 4
                if bit == 0x20:
                    snes_buffered_write(ctx, MMX3_HYPER_CANNON, bytearray([0xFF]))
                    snes_buffered_write(ctx, WRAM_START + 0x0A84, bytearray([0x02]))
                chips = chips[0]
                chips |= bit
                snes_buffered_write(ctx, MMX3_RIDE_CHIPS, bytearray([chips]))
                snes_buffered_write(ctx, MMX3_SFX_FLAG, bytearray([0x01]))
                snes_buffered_write(ctx, MMX3_SFX_NUMBER, bytearray([0x1B]))
                #snes_buffered_write(ctx, MMX3_RECEIVING_ITEM, bytearray([0x01]))
            self.item_queue.pop(0)

        elif next_item[0] == "ride":
            ride = await snes_read(ctx, MMX3_RIDE_CHIPS, 0x1)
            ride = ride[0]
            upgrade = ride_armor_rom_data[item_id]
            bit = 1 << upgrade[0]
            check = ride & bit
            if check == 0:
                ride |= bit
                snes_buffered_write(ctx, MMX3_RIDE_CHIPS, bytearray([ride]))
                #snes_buffered_write(ctx, MMX3_RECEIVING_ITEM, bytearray([0x01]))
                snes_buffered_write(ctx, MMX3_SFX_FLAG, bytearray([0x01]))
                snes_buffered_write(ctx, MMX3_SFX_NUMBER, bytearray([0x32]))
            self.item_queue.pop(0)

        await snes_flush_writes(ctx)


    async def game_watcher(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        game_state = await snes_read(ctx, MMX3_GAME_STATE, 0x1)
        menu_state = await snes_read(ctx, MMX3_MENU_STATE, 0x1)
        gameplay_state = await snes_read(ctx, MMX3_GAMEPLAY_STATE, 0x1)

        # Discard uninitialized ROMs
        if menu_state is None:
            self.game_state = False
            ctx.item_queue = []
            return
    
        if game_state[0] == 0:
            self.game_state = False
            return
        
        validation = await snes_read(ctx, MMX3_VALIDATION_CHECK, 0x2)
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            snes_logger.info(f'ROM not properly validated.')
            self.game_state = False
            return
        
        # Enable notifications on EnergyLink
        # TODO: Determine if this is an actual good spot for setting up this notification
        if ctx.server and ctx.slot:
            if not self.energy_link_enabled:
                ctx.set_notify(f"EnergyLink{ctx.team}")
                self.energy_link_enabled = True
                logger.info("EnergyLink connected")

        self.game_state = True
        
        if "DeathLink" in ctx.tags and menu_state == 0x04 and ctx.last_death_link + 1 < time.time():
            currently_dead = gameplay_state[0] == 0x06
            await ctx.handle_death_link_state(currently_dead)
            
        if menu_state[0] == 0x06:
            # Handle goal
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
            return

        await self.handle_energy_link(ctx)
        await self.handle_item_queue(ctx)
        
        from worlds.mmx3.Rom import weapon_rom_data, ride_armor_rom_data, upgrades_rom_data, boss_access_rom_data, refill_rom_data
        from worlds.mmx3.Levels import location_id_to_level_id
        from worlds import AutoWorldRegister

        bit_byte_vile_data = await snes_read(ctx, MMX3_BIT_BYTE_VILE, 0x01)
        defeated_bosses_data = await snes_read(ctx, MMX3_DEFEATED_BOSSES, 0x20)
        completed_rematches = await snes_read(ctx, MMX3_COMPLETED_REMATCHES, 0x1)
        completed_rematches = completed_rematches[0]
        required_rematches = await snes_read(ctx, MMX3_REQUIRED_REMATCHES, 0x1)
        required_rematches = required_rematches[0]
        defeated_bosses = list(defeated_bosses_data)
        cleared_levels_data = await snes_read(ctx, MMX3_LEVEL_CLEARED, 0x20)
        cleared_levels = list(cleared_levels_data)
        collected_heart_tanks_data = await snes_read(ctx, MMX3_COLLECTED_HEART_TANKS, 0x01)
        collected_ride_chips_data = await snes_read(ctx, MMX3_COLLECTED_RIDE_CHIPS, 0x01)
        collected_upgrades_data = await snes_read(ctx, MMX3_COLLECTED_UPGRADES, 0x01)
        collected_pickups_data = await snes_read(ctx, MMX3_COLLECTED_PICKUPS, 0x40)
        collected_pickups = list(collected_pickups_data)
        pickupsanity_enabled = await snes_read(ctx, MMX3_PICKUPSANITY_ACTIVE, 0x1)
        new_checks = []
        for loc_name, data in location_id_to_level_id.items():
            loc_id = AutoWorldRegister.world_types[ctx.game].location_name_to_id[loc_name]
            if loc_id not in ctx.locations_checked:
                level_id = data[0]
                internal_id = data[1]
                data_bit = data[2]

                if internal_id == 0x02:
                    # Heart Tank
                    bit = 0x01 << (level_id - 1)
                    masked_data = collected_heart_tanks_data[0] & bit
                    if masked_data != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x03:
                    # Sub Tank
                    masked_data = collected_upgrades_data[0] & data_bit
                    if masked_data != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x04:
                    # Mega Man upgrades
                    masked_data = collected_upgrades_data[0] & data_bit
                    if masked_data != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x05:
                    # Ride Armor
                    masked_data = collected_ride_chips_data[0] & data_bit
                    if masked_data != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x06:
                    # Mega Man chips
                    masked_data = collected_ride_chips_data[0] & data_bit
                    if masked_data != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x09:
                    # Vile Defeated
                    vile_defeated = bit_byte_vile_data[0] & 0x30
                    if vile_defeated != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x0A:
                    # Byte Defeated
                    byte_defeated = bit_byte_vile_data[0] & 0x0C
                    if byte_defeated != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x0B:
                    # Bit Defeated
                    bit_defeated = bit_byte_vile_data[0] & 0x03
                    if bit_defeated != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x0E:
                    # Gold Armor
                    pass
                elif internal_id >= 0x300:
                    # Maverick Medal
                    if cleared_levels_data[data_bit] != 0:
                        new_checks.append(loc_id)
                elif internal_id >= 0x200:
                    # Boss clear
                    boss_id = internal_id & 0x1F
                    if defeated_bosses_data[boss_id] != 0:
                        new_checks.append(loc_id)
                    else:
                        if boss_id >= 0x13 and boss_id <= 0x1A: 
                            # Auto complete every rematch boss if the required amount was reached
                            if completed_rematches.bit_count() >= required_rematches:
                                defeated_bosses[boss_id] = 0xFF
                                completed_rematches = 0xFF
                                new_checks.append(loc_id)
                elif internal_id >= 0x100:
                    # Pickups
                    if not pickupsanity_enabled or pickupsanity_enabled[0] == 0:
                        continue
                    pickup_id = internal_id & 0x3F
                    if collected_pickups_data[pickup_id] != 0:
                        new_checks.append(loc_id)
        
        snes_buffered_write(ctx, MMX3_COMPLETED_REMATCHES, bytearray([completed_rematches]))
        snes_buffered_write(ctx, MMX3_DEFEATED_BOSSES, bytes(defeated_bosses))
        await snes_flush_writes(ctx)
                        
        verify_game_state = await snes_read(ctx, MMX3_GAMEPLAY_STATE, 1)
        if verify_game_state is None:
            snes_logger.info(f'Exit Game.')
            return
        
        rom = await snes_read(ctx, MMX3_ROMHASH_START, ROMHASH_SIZE)
        if rom != ctx.rom:
            ctx.rom = None
            snes_logger.info(f'Exit ROM.')
            return
        
        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names[new_check_id]
            snes_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])

        recv_count = await snes_read(ctx, MMX3_RECV_INDEX, 1)
        if recv_count is None:
            # Add a small failsafe in case we get a None. Other SNI games do this...
            return

        recv_index = recv_count[0]

        if recv_index < len(ctx.items_received):
            item = ctx.items_received[recv_index]
            recv_index += 1
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names[item.item], 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names[item.location], recv_index, len(ctx.items_received)))
            
            snes_buffered_write(ctx, MMX3_RECV_INDEX, bytes([recv_index]))
            await snes_flush_writes(ctx)
            
            if item.item in weapon_rom_data:
                self.add_item_to_queue("weapon", item.item)

            elif item.item == 0xBD0013:
                self.add_item_to_queue("heart tank", item.item)

            elif item.item == 0xBD0014:
                self.add_item_to_queue("sub tank", item.item)

            elif item.item in upgrades_rom_data:
                self.add_item_to_queue("upgrade", item.item)

            elif item.item in ride_armor_rom_data:
                self.add_item_to_queue("ride", item.item)

            elif item.item in boss_access_rom_data:
                boss_access = await snes_read(ctx, MMX3_UNLOCKED_LEVELS, 0x20)
                boss_access = bytearray(boss_access)
                level = boss_access_rom_data[item.item]
                boss_access[level[0] * 2] = 0x01
                snes_buffered_write(ctx, MMX3_UNLOCKED_LEVELS, boss_access)
                if item.item == 0xBD000A:
                    snes_buffered_write(ctx, MMX3_DOPPLER_ACCESS, bytearray([0x00]))
                self.add_item_to_queue("boss access", item.item)

            elif item.item == 0xBD0019:
                # Unlock vile stage
                snes_buffered_write(ctx, MMX3_VILE_ACCESS, bytearray([0x01]))
                self.add_item_to_queue("boss access", item.item)
                
            elif item.item in refill_rom_data:
                self.add_item_to_queue(refill_rom_data[item.item][0], item.item)

        # Handle collected locations
        # Do not collect locations if you can't move, are in pause state, not in the correct mode or not in gameplay state
        receiving_item = await snes_read(ctx, MMX3_RECEIVING_ITEM, 0x1)
        menu_state = await snes_read(ctx, MMX3_MENU_STATE, 0x1)
        gameplay_state = await snes_read(ctx, MMX3_GAMEPLAY_STATE, 0x1)
        can_move = await snes_read(ctx, MMX3_CAN_MOVE, 0x1)
        going_through_gate = await snes_read(ctx, MMX3_GOING_THROUGH_GATE, 0x4)
        pause_state = await snes_read(ctx, MMX3_PAUSE_STATE, 0x1)
        if menu_state[0] != 0x04 or \
            gameplay_state[0] != 0x04 or \
            can_move[0] != 0x00 or \
            pause_state[0] != 0x00 or \
            receiving_item[0] != 0x00 or \
            (
                going_through_gate[0] != 0x00 and \
                going_through_gate[1] != 0x00 and \
                going_through_gate[2] != 0x00 and \
                going_through_gate[3] != 0x00 \
            ):
            return
        new_boss_clears = False
        new_cleared_level = False
        new_heart_tank = False
        new_upgrade = False
        new_ride_chip = False
        new_bit_byte_vile = False
        new_pickup = False
        collected_heart_tanks_data = collected_heart_tanks_data[0]
        collected_upgrades_data = collected_upgrades_data[0]
        collected_ride_chips_data = collected_ride_chips_data[0]
        bit_byte_vile_data = bit_byte_vile_data[0]
        i = 0
        for loc_id in ctx.checked_locations:
            if loc_id not in ctx.locations_checked:
                ctx.locations_checked.add(loc_id)
                loc_name = ctx.location_names[loc_id]

                if loc_name not in location_id_to_level_id:
                    continue

                logging.info(f"Recovered checks ({i:03}): {loc_name}")
                i += 1

                data = location_id_to_level_id[loc_name]
                level_id = data[0]
                internal_id = data[1]
                data_bit = data[2]

                if internal_id == 0x02:
                    # Heart Tank
                    bit = 0x01 << (level_id - 1)
                    collected_heart_tanks_data |= bit
                    new_heart_tank = True
                elif internal_id == 0x03:
                    # Sub Tank
                    collected_upgrades_data |= data_bit
                    new_upgrade = True
                elif internal_id == 0x04:
                    # Mega Man upgrades
                    collected_upgrades_data |= data_bit
                    new_upgrade = True
                elif internal_id == 0x05:
                    # Ride Armor
                    collected_ride_chips_data |= data_bit
                    new_ride_chip = True
                elif internal_id == 0x06:
                    # Mega Man chips
                    collected_ride_chips_data |= data_bit
                    new_ride_chip = True
                elif internal_id == 0x09:
                    # Vile Defeated
                    bit_byte_vile_data |= 0x30
                    new_bit_byte_vile = True
                elif internal_id == 0x0A:
                    # Byte Defeated
                    bit_byte_vile_data |= 0x0C
                    new_bit_byte_vile = True
                elif internal_id == 0x0B:
                    # Bit Defeated
                    bit_byte_vile_data |= 0x03
                    new_bit_byte_vile = True
                elif internal_id == 0x0E:
                    # Gold Armor
                    pass
                elif internal_id >= 0x300:
                    # Maverick Medal
                    cleared_levels[data_bit] = 0xFF
                    new_cleared_level = True
                elif internal_id >= 0x200:
                    # Boss clear
                    boss_id = internal_id & 0x1F
                    defeated_bosses[boss_id] = 0xFF
                    new_boss_clears = True
                    if boss_id >= 0x13 and boss_id <= 0x1A: 
                        completed_rematches |= 0x1 << (boss_id - 0x13)
                elif internal_id >= 0x100:
                    # Pickups
                    pickup_id = internal_id & 0x3F
                    collected_pickups[pickup_id] = 0xFF
                    new_pickup = True
                    
            if new_cleared_level:
                snes_buffered_write(ctx, MMX3_LEVEL_CLEARED, bytes(cleared_levels))
            if new_boss_clears:
                snes_buffered_write(ctx, MMX3_DEFEATED_BOSSES, bytes(defeated_bosses))
                snes_buffered_write(ctx, MMX3_COMPLETED_REMATCHES, bytearray([completed_rematches]))
            if new_bit_byte_vile:
                snes_buffered_write(ctx, MMX3_BIT_BYTE_VILE, bytearray([bit_byte_vile_data]))
            if new_pickup:
                snes_buffered_write(ctx, MMX3_COLLECTED_PICKUPS, bytes(collected_pickups))
            if new_upgrade:
                snes_buffered_write(ctx, MMX3_COLLECTED_UPGRADES, bytearray([collected_upgrades_data]))
            if new_heart_tank:
                snes_buffered_write(ctx, MMX3_COLLECTED_HEART_TANKS, bytearray([collected_heart_tanks_data]))
            if new_ride_chip:
                snes_buffered_write(ctx, MMX3_COLLECTED_RIDE_CHIPS, bytearray([collected_ride_chips_data]))
            await snes_flush_writes(ctx)

def cmd_pool(self):
    """
    Check how much healing is in the pool.
    """
    if self.ctx.game != "Mega Man X3":
        logger.warning("This command can only be used while playing Mega Man X3")
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.info(f"Must be connected to server and in game.")
    else:
        pool = self.ctx.stored_data[f'EnergyLink{self.ctx.team}'] / HP_EXCHANGE_RATE
        logger.info(f"Healing available: {pool:.2f}")

def cmd_heal(self, amount: str = ""):
    """
    Request healing from EnergyLink.
    """
    if self.ctx.game != "Mega Man X3":
        logger.warning("This command can only be used while playing Mega Man X3")
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.info(f"Must be connected to server and in game.")
    else:
        if self.ctx.client_handler.heal_request_command is not None:
            logger.info(f"You already placed a healing request.")
            return
        if amount:
            try:
                amount = int(amount)
            except:
                logger.info(f"You need to specify how much HP you will recover.")
                return
            if amount > 16:
                self.ctx.client_handler.heal_request_command = 16
            self.ctx.client_handler.heal_request_command = amount
            logger.info(f"Requested {amount} HP from the healing pool.")
        else:
            logger.info(f"You need to specify how much HP you will request.")

def cmd_autoheal(self):
    """
    Enable auto heal from EnergyLink.
    """
    if self.ctx.game != "Mega Man X3":
        logger.warning("This command can only be used while playing Mega Man X3")
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.info(f"Must be connected to server and in game.")
    else:
        if self.ctx.client_handler.auto_heal:
            self.ctx.client_handler.auto_heal = False
            logger.info(f"Auto healing disabled.")
        else:
            self.ctx.client_handler.auto_heal = True
            logger.info(f"Auto healing enabled.")
