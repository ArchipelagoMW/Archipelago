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

MMX_GAME_STATE          = WRAM_START + 0x000D1
MMX_MENU_STATE          = WRAM_START + 0x000D2
MMX_GAMEPLAY_STATE      = WRAM_START + 0x000D3
MMX_LEVEL_INDEX         = WRAM_START + 0x01F7A

MMX_WEAPON_ARRAY            = WRAM_START + 0x01F88
MMX_SUB_TANK_ARRAY          = WRAM_START + 0x01F83
MMX_UPGRADES                = WRAM_START + 0x01F99
MMX_HEART_TANKS             = WRAM_START + 0x01F9C
MMX_HADOUKEN                = WRAM_START + 0x01F7E
MMX_LIFE_COUNT              = WRAM_START + 0x01F80
MMX_MAX_HP                  = WRAM_START + 0x01F9A
MMX_CURRENT_HP              = WRAM_START + 0x00BCF
MMX_UNLOCKED_CHARGED_SHOT   = WRAM_START + 0x1EE16

MMX_SFX_FLAG            = WRAM_START + 0x1EE03
MMX_SFX_NUMBER          = WRAM_START + 0x1EE04

MMX_SIGMA_ACCESS            = WRAM_START + 0x1EE02
MMX_COLLECTED_HEART_TANKS   = WRAM_START + 0x1EE05
MMX_COLLECTED_UPGRADES      = WRAM_START + 0x1EE06
MMX_COLLECTED_HADOUKEN      = WRAM_START + 0x1EE07
MMX_DEFEATED_BOSSES         = WRAM_START + 0x1EE80
MMX_COMPLETED_LEVELS        = WRAM_START + 0x1EE60
MMX_COLLECTED_PICKUPS       = WRAM_START + 0x1EEC0
MMX_UNLOCKED_LEVELS         = WRAM_START + 0x1EE40

MMX_RECV_INDEX          = WRAM_START + 0x1EE00
MMX_ENERGY_LINK_PACKET  = WRAM_START + 0x1EE09
MMX_VALIDATION_CHECK    = WRAM_START + 0x1EE13

MMX_RECEIVING_ITEM          = WRAM_START + 0x1EE15
MMX_ENABLE_HEART_TANK       = WRAM_START + 0x1EE0B
MMX_ENABLE_HP_REFILL        = WRAM_START + 0x1EE0F
MMX_HP_REFILL_AMOUNT        = WRAM_START + 0x1EE10
MMX_ENABLE_GIVE_1UP         = WRAM_START + 0x1EE12
MMX_ENABLE_WEAPON_REFILL    = WRAM_START + 0x1EE1A
MMX_WEAPON_REFILL_AMOUNT    = WRAM_START + 0x1EE1B

MMX_PAUSE_STATE        = WRAM_START + 0x01F24
MMX_CAN_MOVE           = WRAM_START + 0x01F13

MMX_PICKUPSANITY_ACTIVE    = ROM_START + 0x17FFE7
MMX_ENERGY_LINK_ENABLED    = ROM_START + 0x17FFE8
MMX_DEATH_LINK_ACTIVE      = ROM_START + 0x17FFE9
MMX_JAMMED_BUSTER_ACTIVE   = ROM_START + 0x17FFEA

EXCHANGE_RATE = 500000000

STARTING_ID = 0xBE0800

MMX_ROMHASH_START = 0x7FC0
ROMHASH_SIZE = 0x15

PICKUP_ITEMS = ["1up", "hp refill", "weapon refill"]

class MMXSNIClient(SNIClient):
    game = "Mega Man X"
    patch_suffix = ".apmmx"

    def __init__(self):
        super().__init__()
        self.game_state = False
        self.last_death_link = 0
        self.auto_heal = False
        self.energy_link_enabled = False
        self.heal_request_command = None
        self.weapon_refill_request_command = None
        self.trade_request = None
        self.item_queue = []


    async def deathlink_kill_player(self, ctx):
        from SNIClient import DeathState, snes_buffered_write, snes_flush_writes, snes_read

        validation = await snes_read(ctx, MMX_VALIDATION_CHECK, 0x2)
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            return

        receiving_item = await snes_read(ctx, MMX_RECEIVING_ITEM, 0x1)
        menu_state = await snes_read(ctx, MMX_MENU_STATE, 0x1)
        gameplay_state = await snes_read(ctx, MMX_GAMEPLAY_STATE, 0x1)
        can_move = await snes_read(ctx, MMX_CAN_MOVE, 0x7)
        pause_state = await snes_read(ctx, MMX_PAUSE_STATE, 0x1)
        if menu_state[0] != 0x04 or \
            gameplay_state[0] != 0x04 or \
            pause_state[0] != 0x00 or \
            can_move != b'\x00\x00\x00\x00\x00\x00\x00' or \
            receiving_item[0] != 0x00:
            return
        
        snes_buffered_write(ctx, MMX_CURRENT_HP, bytes([0x80]))
        snes_buffered_write(ctx, WRAM_START + 0x00BAA, bytes([0x0C]))
        snes_buffered_write(ctx, WRAM_START + 0x00C12, bytes([0x0C]))
        snes_buffered_write(ctx, WRAM_START + 0x00BAB, bytes([0x00]))

        await snes_flush_writes(ctx)

        ctx.death_state = DeathState.dead
        ctx.last_death_link = time.time()


    async def validate_rom(self, ctx):
        from SNIClient import snes_read

        energy_link = await snes_read(ctx, MMX_ENERGY_LINK_ENABLED, 0x1)
        rom_name = await snes_read(ctx, MMX_ROMHASH_START, ROMHASH_SIZE)
        if rom_name is None or rom_name == bytes([0] * ROMHASH_SIZE) or rom_name[:4] != b"MMX1":
            if "pool" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("pool")
            if "autoheal" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("autoheal")
            if "heal" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("heal")
            if "refill" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("refill")
            return False
        
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.receive_option = 0
        ctx.send_option = 0
        ctx.allow_collect = True
        if energy_link[0]:
            if "pool" not in ctx.command_processor.commands:
                ctx.command_processor.commands["pool"] = cmd_pool
            if "autoheal" not in ctx.command_processor.commands:
                ctx.command_processor.commands["autoheal"] = cmd_autoheal
            if "refill" not in ctx.command_processor.commands:
                ctx.command_processor.commands["heal"] = cmd_heal
            if "refill" not in ctx.command_processor.commands:
                ctx.command_processor.commands["refill"] = cmd_refill
        if "trade" not in ctx.command_processor.commands:
            ctx.command_processor.commands["trade"] = cmd_trade

        death_link = await snes_read(ctx, MMX_DEATH_LINK_ACTIVE, 1)
        if death_link[0]:
            await ctx.update_death_link(bool(death_link[0] & 0b1))

        ctx.rom = rom_name

        return True
     
    async def handle_hp_trade(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        validation = await snes_read(ctx, MMX_VALIDATION_CHECK, 0x2)
        if validation is None:
            return
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            return

        # Can only process trades during the pause state
        receiving_item = await snes_read(ctx, MMX_RECEIVING_ITEM, 0x1)
        menu_state = await snes_read(ctx, MMX_MENU_STATE, 0x1)
        gameplay_state = await snes_read(ctx, MMX_GAMEPLAY_STATE, 0x1)
        if menu_state[0] != 0x04 or \
            gameplay_state[0] != 0x04 or \
            receiving_item[0] != 0x00:
            return
        
        pause_state = await snes_read(ctx, MMX_PAUSE_STATE, 0x1)
        if pause_state[0] == 0x00:
            return

        for item in self.item_queue:
            if item[0] == "weapon refill":
                self.trade_request = None
                logger.info(f"You already have a Weapon Energy request pending to be received.")
                return

        # Can trade HP -> WPN if HP is above 1
        current_hp = await snes_read(ctx, MMX_CURRENT_HP, 0x1)
        if current_hp[0] > 0x01:
            max_trade = current_hp[0] - 1
            set_trade = self.trade_request if self.trade_request <= max_trade else max_trade
            self.add_item_to_queue("weapon refill", None, set_trade)
            new_hp = current_hp[0] - set_trade
            snes_buffered_write(ctx, MMX_CURRENT_HP, bytearray([new_hp]))
            await snes_flush_writes(ctx)
            self.trade_request = None
            logger.info(f"Traded {set_trade} HP for {set_trade} Weapon Energy.")
        else:
            logger.info("Couldn't process trade. HP is too low.")


    async def handle_energy_link(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        # Deposit heals into the pool regardless of energy_link setting
        energy_packet = await snes_read(ctx, MMX_ENERGY_LINK_PACKET, 0x2)
        if energy_packet is None:
            return
        energy_packet_raw = energy_packet[0] | (energy_packet[1] << 8)
        energy_packet = (energy_packet_raw * EXCHANGE_RATE) >> 4
        if energy_packet != 0:
            await ctx.send_msgs([{
                "cmd": "Set", "key": f"EnergyLink{ctx.team}", "operations":
                    [{"operation": "add", "value": energy_packet},
                    {"operation": "max", "value": 0}],
            }])
            pool = ((ctx.stored_data[f'EnergyLink{ctx.team}'] or 0) / EXCHANGE_RATE) + (energy_packet_raw / 16)
            logger.info(f"Deposited {energy_packet_raw / 16:.2f} into the energy pool. Energy available: {pool:.2f}")
            snes_buffered_write(ctx, MMX_ENERGY_LINK_PACKET, bytearray([0x00, 0x00]))
            await snes_flush_writes(ctx)

        energy_link = await snes_read(ctx, MMX_ENERGY_LINK_ENABLED, 0x1)
        if energy_link is None:
            return

        if energy_link[0]:
            validation = await snes_read(ctx, MMX_VALIDATION_CHECK, 0x2)
            if validation is None:
                return
            validation = validation[0] | (validation[1] << 8)
            if validation != 0xDEAD:
                return

            receiving_item = await snes_read(ctx, MMX_RECEIVING_ITEM, 0x1)
            menu_state = await snes_read(ctx, MMX_MENU_STATE, 0x1)
            gameplay_state = await snes_read(ctx, MMX_GAMEPLAY_STATE, 0x1)
            can_move = await snes_read(ctx, MMX_CAN_MOVE, 0x7)
            pause_state = await snes_read(ctx, MMX_PAUSE_STATE, 0x1)
            if menu_state[0] != 0x04 or \
                gameplay_state[0] != 0x04 or \
                pause_state[0] != 0x00 or \
                can_move != b'\x00\x00\x00\x00\x00\x00\x00' or \
                receiving_item[0] != 0x00:
                return
            
            skip_hp = False
            skip_weapon = False
            for item in self.item_queue:
                if item[0] == "hp refill":
                    skip_hp = True
                    self.heal_request_command = None
                elif item[0] == "weapon refill":
                    skip_weapon = True
                    self.weapon_refill_request_command = None
            
            pool = ctx.stored_data[f'EnergyLink{ctx.team}'] or 0
            if not skip_hp:
                # Perform auto heals
                if self.auto_heal:
                    if self.heal_request_command is None:
                        if pool < EXCHANGE_RATE:
                            return
                        current_hp = await snes_read(ctx, MMX_CURRENT_HP, 0x1)
                        max_hp = await snes_read(ctx, MMX_MAX_HP, 0x1)
                        if max_hp[0] > current_hp[0]:
                            self.heal_request_command = max_hp[0] - current_hp[0]

                # Handle heal requests
                if self.heal_request_command:
                    heal_needed = self.heal_request_command
                    heal_needed_rate = heal_needed * EXCHANGE_RATE
                    if pool < EXCHANGE_RATE:
                        logger.info(f"There's not enough Energy for your request ({heal_needed}). Energy available: {pool / EXCHANGE_RATE:.2f}")
                        self.heal_request_command = None
                        return
                    elif pool < heal_needed_rate:
                        heal_needed = int(pool / EXCHANGE_RATE)
                        heal_needed_rate = heal_needed * EXCHANGE_RATE
                    await ctx.send_msgs([{
                        "cmd": "Set", "key": f"EnergyLink{ctx.team}", "operations":
                            [{"operation": "add", "value": -heal_needed_rate},
                            {"operation": "max", "value": 0}],
                    }])
                    self.add_item_to_queue("hp refill", None, self.heal_request_command)
                    pool = (pool / EXCHANGE_RATE) - heal_needed
                    logger.info(f"Healed by {heal_needed}. Energy available: {pool:.2f}")
                    self.heal_request_command = None

            if not skip_weapon:
                # Handle weapon refill requests
                if self.weapon_refill_request_command:
                    heal_needed = self.weapon_refill_request_command
                    heal_needed_rate = heal_needed * EXCHANGE_RATE
                    if pool < EXCHANGE_RATE:
                        logger.info(f"There's not enough Energy for your request ({heal_needed}). Energy available: {pool / EXCHANGE_RATE:.2f}")
                        self.weapon_refill_request_command = None
                        return
                    elif pool < heal_needed_rate:
                        heal_needed = int(pool / EXCHANGE_RATE)
                        heal_needed_rate = heal_needed * EXCHANGE_RATE
                    await ctx.send_msgs([{
                        "cmd": "Set", "key": f"EnergyLink{ctx.team}", "operations":
                            [{"operation": "add", "value": -heal_needed_rate},
                            {"operation": "max", "value": 0}],
                    }])
                    self.add_item_to_queue("weapon refill", None, self.weapon_refill_request_command)
                    pool = (pool / EXCHANGE_RATE) - heal_needed
                    logger.info(f"Refilled current weapon by {heal_needed}. Energy available: {pool:.2f}")
                    self.weapon_refill_request_command = None


    def add_item_to_queue(self, item_type, item_id, item_additional = None):
        if not hasattr(self, "item_queue"):
            self.item_queue = []
        self.item_queue.append([item_type, item_id, item_additional])


    async def handle_item_queue(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        from worlds.mmx.Rom import weapon_rom_data, upgrades_rom_data

        if not hasattr(self, "item_queue") or len(self.item_queue) == 0:
            return

        validation = await snes_read(ctx, MMX_VALIDATION_CHECK, 0x2)
        if validation is None:
            return
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            return

        next_item = self.item_queue[0]
        item_id = next_item[1]

        if next_item[0] == "boss access":
            snes_buffered_write(ctx, MMX_SFX_FLAG, bytearray([0x01]))
            snes_buffered_write(ctx, MMX_SFX_NUMBER, bytearray([0x2D]))
            self.item_queue.pop(0)
            return
        
        # Do not give items if you can't move, are in pause state, not in the correct mode or not in gameplay state
        receiving_item = await snes_read(ctx, MMX_RECEIVING_ITEM, 0x1)
        menu_state = await snes_read(ctx, MMX_MENU_STATE, 0x1)
        gameplay_state = await snes_read(ctx, MMX_GAMEPLAY_STATE, 0x1)
        can_move = await snes_read(ctx, MMX_CAN_MOVE, 0x7)
        pause_state = await snes_read(ctx, MMX_PAUSE_STATE, 0x1)
        if menu_state[0] != 0x04 or \
           gameplay_state[0] != 0x04 or \
           pause_state[0] != 0x00 or \
           can_move != b'\x00\x00\x00\x00\x00\x00\x00' or \
           receiving_item[0] != 0x00:
            backup_item = self.item_queue.pop(0)
            self.item_queue.append(backup_item)
            return
        
        if next_item[0] in PICKUP_ITEMS:
            backup_item = self.item_queue.pop(0)
        
            if "hp refill" in next_item[0]:
                current_hp = await snes_read(ctx, MMX_CURRENT_HP, 0x1)
                max_hp = await snes_read(ctx, MMX_MAX_HP, 0x1)

                if current_hp[0] < max_hp[0]:
                    snes_buffered_write(ctx, MMX_ENABLE_HP_REFILL, bytearray([0x02]))
                    snes_buffered_write(ctx, MMX_HP_REFILL_AMOUNT, bytearray([next_item[2]]))
                    snes_buffered_write(ctx, MMX_RECEIVING_ITEM, bytearray([0x01]))
                else:
                    # TODO: Sub Tank logic
                    self.item_queue.append(backup_item)

            elif next_item[0] == "weapon refill":
                snes_buffered_write(ctx, MMX_ENABLE_WEAPON_REFILL, bytearray([0x02]))
                snes_buffered_write(ctx, MMX_WEAPON_REFILL_AMOUNT, bytearray([next_item[2]]))
                snes_buffered_write(ctx, MMX_RECEIVING_ITEM, bytearray([0x01]))

            elif next_item[0] == "1up":
                life_count = await snes_read(ctx, MMX_LIFE_COUNT, 0x1)
                if life_count[0] < 9:
                    snes_buffered_write(ctx, MMX_ENABLE_GIVE_1UP, bytearray([0x01]))
                    snes_buffered_write(ctx, MMX_RECEIVING_ITEM, bytearray([0x01]))
                    pass
                else:
                    self.item_queue.append(backup_item)

        if next_item[0] == "weapon":
            weapon = weapon_rom_data[item_id]
            snes_buffered_write(ctx, WRAM_START + weapon[0], bytearray([weapon[1]]))
            snes_buffered_write(ctx, MMX_SFX_FLAG, bytearray([0x01]))
            snes_buffered_write(ctx, MMX_SFX_NUMBER, bytearray([0x0D]))
            self.item_queue.pop(0)
            
        elif next_item[0] == "heart tank":
            heart_tanks = await snes_read(ctx, MMX_HEART_TANKS, 0x1)
            heart_tanks = heart_tanks[0]
            heart_tank_count = heart_tanks.bit_count()
            if heart_tank_count < 8:
                heart_tanks |= 1 << heart_tank_count
                snes_buffered_write(ctx, MMX_HEART_TANKS, bytearray([heart_tanks]))
                snes_buffered_write(ctx, MMX_ENABLE_HEART_TANK, bytearray([0x02]))
                snes_buffered_write(ctx, MMX_RECEIVING_ITEM, bytearray([0x01]))
            self.item_queue.pop(0)

        elif next_item[0] == "sub tank":
            upgrades = await snes_read(ctx, MMX_UPGRADES, 0x1)
            sub_tanks = await snes_read(ctx, MMX_SUB_TANK_ARRAY, 0x4)
            sub_tanks = list(sub_tanks)
            upgrade = upgrades[0]
            upgrade = upgrade & 0xF0
            sub_tank_count = upgrade.bit_count()
            if sub_tank_count < 4:
                upgrade = upgrades[0]
                upgrade |= 0x10 << sub_tank_count
                sub_tanks[sub_tank_count] = 0x8E
                snes_buffered_write(ctx, MMX_UPGRADES, bytearray([upgrade]))
                snes_buffered_write(ctx, MMX_SUB_TANK_ARRAY, bytearray(sub_tanks))
                snes_buffered_write(ctx, MMX_SFX_FLAG, bytearray([0x01]))
                snes_buffered_write(ctx, MMX_SFX_NUMBER, bytearray([0x17]))
            self.item_queue.pop(0)
        
        elif next_item[0] == "upgrade":
            upgrades = await snes_read(ctx, MMX_UPGRADES, 0x1)

            upgrade = upgrades_rom_data[item_id]
            bit = 1 << upgrade[0]
            check = upgrades[0] & bit

            if check == 0:
                # Armor
                upgrades = upgrades[0]
                upgrades |= bit
                if bit == 0x01:
                    snes_buffered_write(ctx, WRAM_START + 0x0BBE, bytearray([0x18]))
                    snes_buffered_write(ctx, MMX_UPGRADES, bytearray([upgrades]))
                elif bit == 0x02:
                    jam_check = await snes_read(ctx, MMX_JAMMED_BUSTER_ACTIVE, 0x1)
                    charge_shot_unlocked = await snes_read(ctx, MMX_UNLOCKED_CHARGED_SHOT, 0x1)
                    if jam_check[0] == 1 and charge_shot_unlocked[0] == 0:
                        snes_buffered_write(ctx, MMX_UNLOCKED_CHARGED_SHOT, bytearray([0x01]))
                    else:
                        value = await snes_read(ctx, WRAM_START + 0x0C38, 0x1)
                        snes_buffered_write(ctx, WRAM_START + 0x0C38, bytearray([value[0] + 1]))
                        snes_buffered_write(ctx, WRAM_START + 0x0C42, bytearray([0x00]))
                        snes_buffered_write(ctx, WRAM_START + 0x0C43, bytearray([0x00]))
                        snes_buffered_write(ctx, WRAM_START + 0x0C39, bytearray([0x00]))
                        snes_buffered_write(ctx, WRAM_START + 0x0C48, bytearray([0x5D]))
                        snes_buffered_write(ctx, MMX_UPGRADES, bytearray([upgrades]))
                elif bit == 0x04:
                    value = await snes_read(ctx, WRAM_START + 0x0C58, 0x1)
                    snes_buffered_write(ctx, WRAM_START + 0x0C58, bytearray([value[0] + 1]))
                    snes_buffered_write(ctx, WRAM_START + 0x0C62, bytearray([0x00]))
                    snes_buffered_write(ctx, WRAM_START + 0x0C63, bytearray([0x01]))
                    snes_buffered_write(ctx, WRAM_START + 0x0C59, bytearray([0x00]))
                    snes_buffered_write(ctx, WRAM_START + 0x0C68, bytearray([0x5D]))
                    snes_buffered_write(ctx, MMX_UPGRADES, bytearray([upgrades]))
                elif bit == 0x08:
                    value = await snes_read(ctx, WRAM_START + 0x0C78, 0x1)
                    snes_buffered_write(ctx, WRAM_START + 0x0C78, bytearray([value[0] + 1]))
                    snes_buffered_write(ctx, WRAM_START + 0x0C82, bytearray([0x00]))
                    snes_buffered_write(ctx, WRAM_START + 0x0C83, bytearray([0x02]))
                    snes_buffered_write(ctx, WRAM_START + 0x0C79, bytearray([0x00]))
                    snes_buffered_write(ctx, WRAM_START + 0x0C88, bytearray([0x5D]))
                    snes_buffered_write(ctx, MMX_UPGRADES, bytearray([upgrades]))
                snes_buffered_write(ctx, MMX_SFX_FLAG, bytearray([0x01]))
                snes_buffered_write(ctx, MMX_SFX_NUMBER, bytearray([0x2B]))
            self.item_queue.pop(0)

        await snes_flush_writes(ctx)


    async def game_watcher(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        game_state = await snes_read(ctx, MMX_GAME_STATE, 0x1)
        menu_state = await snes_read(ctx, MMX_MENU_STATE, 0x1)
        gameplay_state = await snes_read(ctx, MMX_GAMEPLAY_STATE, 0x1)

        # Discard uninitialized ROMs
        if menu_state is None:
            self.game_state = False
            self.energy_link_enabled = False
            ctx.item_queue = []
            return
    
        if game_state[0] == 0:
            self.game_state = False
            ctx.item_queue = []
            return
        
        validation = await snes_read(ctx, MMX_VALIDATION_CHECK, 0x2)
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            snes_logger.info(f'ROM not properly validated.')
            self.game_state = False
            return

        self.game_state = True
        if "DeathLink" in ctx.tags and menu_state[0] == 0x04 and ctx.last_death_link + 1 < time.time():
            currently_dead = gameplay_state[0] == 0x06
            await ctx.handle_deathlink_state(currently_dead)
            
        if self.trade_request is not None:
            await self.handle_hp_trade(ctx)

        await self.handle_item_queue(ctx)

        # This is going to be rewritten whenever SNIClient supports on_package
        energy_link = await snes_read(ctx, MMX_ENERGY_LINK_ENABLED, 0x1)
        if energy_link[0] != 0:
            if self.energy_link_enabled and f'EnergyLink{ctx.team}' in ctx.stored_data:
                await self.handle_energy_link(ctx)

            if ctx.server and ctx.server.socket.open and not self.energy_link_enabled and ctx.team is not None:
                self.energy_link_enabled = True
                ctx.set_notify(f"EnergyLink{ctx.team}")
                logger.info(f"Initialized EnergyLink{ctx.team}")

        from worlds.mmx.Rom import weapon_rom_data, upgrades_rom_data, boss_access_rom_data, refill_rom_data
        from worlds.mmx.Levels import location_id_to_level_id
        from worlds import AutoWorldRegister

        defeated_bosses_data = await snes_read(ctx, MMX_DEFEATED_BOSSES, 0x20)
        defeated_bosses = list(defeated_bosses_data)
        cleared_levels_data = await snes_read(ctx, MMX_COMPLETED_LEVELS, 0x20)
        cleared_levels = list(cleared_levels_data)
        collected_heart_tanks_data = await snes_read(ctx, MMX_COLLECTED_HEART_TANKS, 0x01)
        collected_upgrades_data = await snes_read(ctx, MMX_COLLECTED_UPGRADES, 0x01)
        collected_hadouken_data = await snes_read(ctx, MMX_COLLECTED_HADOUKEN, 0x01)
        collected_pickups_data = await snes_read(ctx, MMX_COLLECTED_PICKUPS, 0x20)
        collected_pickups = list(collected_pickups_data)
        pickupsanity_enabled = await snes_read(ctx, MMX_PICKUPSANITY_ACTIVE, 0x1)
        completed_intro_level = await snes_read(ctx, WRAM_START + 0x01F9B, 0x1)
        new_checks = []
        for loc_name, data in location_id_to_level_id.items():
            loc_id = AutoWorldRegister.world_types[ctx.game].location_name_to_id[loc_name]
            if loc_id not in ctx.locations_checked:
                internal_id = data[1]
                data_bit = data[2]

                if internal_id == 0x000:
                    # Boss clear
                    if defeated_bosses_data[data_bit] != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x001:
                    # Maverick Medal
                    if cleared_levels_data[data_bit] != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x002:
                    # Heart Tank
                    masked_data = collected_heart_tanks_data[0] & data_bit
                    if masked_data != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x003:
                    # Mega Man upgrades
                    masked_data = collected_upgrades_data[0] & data_bit
                    if masked_data != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x004:
                    # Sub Tank
                    masked_data = collected_upgrades_data[0] & data_bit
                    if masked_data != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x005:
                    # Hadouken
                    if collected_hadouken_data[0] != 0x00:
                        new_checks.append(loc_id)
                elif internal_id == 0x007:
                    # Intro
                    if game_state[0] == 0x02 and \
                       menu_state[0] == 0x00 and \
                       gameplay_state[0] == 0x01 and \
                       completed_intro_level[0] == 0x04:
                        new_checks.append(loc_id)
                elif internal_id == 0x020:
                    # Pickups
                    if not pickupsanity_enabled or pickupsanity_enabled[0] == 0:
                        continue
                    if collected_pickups_data[data_bit] != 0:
                        new_checks.append(loc_id)
 
        verify_game_state = await snes_read(ctx, MMX_GAMEPLAY_STATE, 1)
        if verify_game_state is None:
            snes_logger.info(f'Exit Game.')
            return
        
        rom = await snes_read(ctx, MMX_ROMHASH_START, ROMHASH_SIZE)
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

        recv_count = await snes_read(ctx, MMX_RECV_INDEX, 2)
        if recv_count is None:
            # Add a small failsafe in case we get a None. Other SNI games do this...
            return

        recv_index = recv_count[0] | (recv_count[1] << 8)

        if recv_index < len(ctx.items_received):
            item = ctx.items_received[recv_index]
            recv_index += 1
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names[item.item], 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names[item.location], recv_index, len(ctx.items_received)))
            
            snes_buffered_write(ctx, MMX_RECV_INDEX, bytes([recv_index]))
            await snes_flush_writes(ctx)
            
            if item.item in weapon_rom_data:
                self.add_item_to_queue("weapon", item.item)

            elif item.item == STARTING_ID + 0x0013:
                self.add_item_to_queue("heart tank", item.item)

            elif item.item == STARTING_ID + 0x0014:
                self.add_item_to_queue("sub tank", item.item)

            elif item.item in upgrades_rom_data:
                self.add_item_to_queue("upgrade", item.item)

            elif item.item in boss_access_rom_data:
                if item.item == STARTING_ID + 0x000A:
                    snes_buffered_write(ctx, MMX_SIGMA_ACCESS, bytearray([0x00]))
                boss_access = await snes_read(ctx, MMX_UNLOCKED_LEVELS, 0x20)
                boss_access = bytearray(boss_access)
                level = boss_access_rom_data[item.item]
                boss_access[level[0]] = 0x01
                snes_buffered_write(ctx, MMX_UNLOCKED_LEVELS, boss_access)
                self.add_item_to_queue("boss access", item.item)

            elif item.item in refill_rom_data:
                self.add_item_to_queue(refill_rom_data[item.item][0], item.item, refill_rom_data[item.item][1])

            elif item.item == STARTING_ID:
                # Handle goal
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True
                return
                
        # Handle collected locations
        game_state = await snes_read(ctx, MMX_GAME_STATE, 0x1)
        if game_state[0] != 0x02:
            return
        new_boss_clears = False
        new_cleared_level = False
        new_heart_tank = False
        new_upgrade = False
        new_pickup = False
        new_hadouken = False
        cleared_levels_data = await snes_read(ctx, MMX_COMPLETED_LEVELS, 0x20)
        cleared_levels = list(cleared_levels_data)
        collected_pickups_data = await snes_read(ctx, MMX_COLLECTED_PICKUPS, 0x40)
        collected_pickups = list(collected_pickups_data)
        collected_heart_tanks_data = await snes_read(ctx, MMX_COLLECTED_HEART_TANKS, 0x01)
        collected_heart_tanks_data = collected_heart_tanks_data[0]
        collected_upgrades_data = await snes_read(ctx, MMX_COLLECTED_UPGRADES, 0x01)
        collected_upgrades_data = collected_upgrades_data[0]
        defeated_bosses_data = await snes_read(ctx, MMX_DEFEATED_BOSSES, 0x20)
        defeated_bosses = list(defeated_bosses_data)
        collected_hadouken_data = await snes_read(ctx, MMX_COLLECTED_HADOUKEN, 0x01)
        collected_hadouken_data = collected_hadouken_data[0]
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

                if internal_id == 0x000:
                    # Boss clear
                    defeated_bosses[data_bit] = 1
                    new_boss_clears = True
                elif internal_id == 0x001:
                    # Maverick Medal
                    cleared_levels[data_bit] = 0xFF
                    new_cleared_level = True
                elif internal_id == 0x002:
                    # Heart Tank
                    collected_heart_tanks_data |= data_bit
                    new_heart_tank = True
                elif internal_id == 0x003:
                    # Mega Man upgrades
                    collected_upgrades_data |= data_bit
                    new_upgrade = True
                elif internal_id == 0x004:
                    # Sub Tank
                    collected_upgrades_data |= data_bit
                    new_upgrade = True
                elif internal_id == 0x005:
                    # Hadouken
                    collected_hadouken_data = 0xFF
                    new_hadouken = True
                elif internal_id >= 0x100:
                    # Pickups
                    collected_pickups[data_bit] = 0x01
                    new_pickup = True

            if new_cleared_level:
                snes_buffered_write(ctx, MMX_COMPLETED_LEVELS, bytes(cleared_levels))
            if new_boss_clears:
                snes_buffered_write(ctx, MMX_DEFEATED_BOSSES, bytes(defeated_bosses))
            if new_pickup:
                snes_buffered_write(ctx, MMX_COLLECTED_PICKUPS, bytes(collected_pickups))
            if new_hadouken:
                snes_buffered_write(ctx, MMX_COLLECTED_PICKUPS, bytearray([collected_hadouken_data]))
            if new_upgrade:
                snes_buffered_write(ctx, MMX_COLLECTED_UPGRADES, bytearray([collected_upgrades_data]))
            if new_heart_tank:
                snes_buffered_write(ctx, MMX_COLLECTED_HEART_TANKS, bytearray([collected_heart_tanks_data]))
            await snes_flush_writes(ctx)


def cmd_pool(self):
    """
    Check how much energy is in the pool.
    """
    if self.ctx.game != "Mega Man X":
        logger.warning("This command can only be used while playing Mega Man X")
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.info(f"Must be connected to server and in game.")
    else:
        pool = (self.ctx.stored_data[f'EnergyLink{self.ctx.team}'] or 0) / EXCHANGE_RATE
        logger.info(f"Energy available: {pool:.2f}")


def cmd_heal(self, amount: str = ""):
    """
    Request healing from EnergyLink.
    """
    if self.ctx.game != "Mega Man X":
        logger.warning("This command can only be used while playing Mega Man X")
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
            if amount <= 0:
                logger.info(f"You need to specify how much HP you will recover.")
                return
            self.ctx.client_handler.heal_request_command = amount
            logger.info(f"Requested {amount} HP from the energy pool.")
        else:
            logger.info(f"You need to specify how much HP you will request.")


def cmd_refill(self, amount: str = ""):
    """
    Request weapon energy from EnergyLink.
    """
    if self.ctx.game != "Mega Man X":
        logger.warning("This command can only be used while playing Mega Man X")
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.info(f"Must be connected to server and in game.")
    else:
        if self.ctx.client_handler.weapon_refill_request_command is not None:
            logger.info(f"You already placed a weapon refill request.")
            return
        if amount:
            try:
                amount = int(amount)
            except:
                logger.info(f"You need to specify how much Weapon Energy you will recover.")
                return
            if amount <= 0:
                logger.info(f"You need to specify how much Weapon Energy you will recover.")
                return
            self.ctx.client_handler.weapon_refill_request_command = amount
            logger.info(f"Requested {amount} Weapon Energy from the energy pool.")
        else:
            logger.info(f"You need to specify how much Weapon Energy you will request.")


def cmd_autoheal(self):
    """
    Enable auto heal from EnergyLink.
    """
    if self.ctx.game != "Mega Man X":
        logger.warning("This command can only be used while playing Mega Man X")
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.info(f"Must be connected to server and in game.")
    else:
        if self.ctx.client_handler.auto_heal:
            self.ctx.client_handler.auto_heal = False
            logger.info(f"Auto healing disabled.")
        else:
            self.ctx.client_handler.auto_heal = True
            logger.info(f"Auto healing enabled.")


def cmd_trade(self, amount: str = ""):
    """
    Trades HP to Weapon Energy. 1:1 ratio.
    """
    if self.ctx.game != "Mega Man X":
        logger.warning("This command can only be used while playing Mega Man X")
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.info(f"Must be connected to server and in game.")
    else:
        if self.ctx.client_handler.trade_request is not None:
            logger.info(f"You already placed a weapon refill request.")
            return
        if amount:
            try:
                amount = int(amount)
            except:
                logger.info(f"You need to specify how much Weapon Energy you will recover.")
                return
            if amount <= 0:
                logger.info(f"You need to specify how much Weapon Energy you will recover.")
                return
            self.ctx.client_handler.trade_request = amount
            logger.info(f"Set up trade for {amount} Weapon Energy. Pause the game to process the trade.")
        else:
            logger.info(f"You need to specify how much Weapon Energy you will request.")
