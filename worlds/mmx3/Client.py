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

MMX3_RAM = WRAM_START + 0x0F400

MMX3_GAME_STATE         = WRAM_START + 0x000D0
MMX3_MENU_STATE         = WRAM_START + 0x000D1
MMX3_GAMEPLAY_STATE     = WRAM_START + 0x000D2
MMX3_PAUSE_STATE        = WRAM_START + 0x01F37
MMX3_SCREEN_BRIGHTNESS  = WRAM_START + 0x000B4
MMX3_LEVEL_INDEX        = WRAM_START + 0x01FAE
MMX3_WEAPON_ARRAY       = WRAM_START + 0x01FBC
MMX3_HEART_TANKS        = WRAM_START + 0x01FD4
MMX3_SUB_TANK_ARRAY     = WRAM_START + 0x01FB7
MMX3_RIDE_CHIPS         = WRAM_START + 0x01FD7
MMX3_UPGRADES           = WRAM_START + 0x01FD1
MMX3_CURRENT_HP         = WRAM_START + 0x009FF
MMX3_CURRENT_WEAPON     = WRAM_START + 0x00A0B
MMX3_MAX_HP             = WRAM_START + 0x01FD2
MMX3_LIFE_COUNT         = WRAM_START + 0x01FB4
MMX3_ACTIVE_CHARACTER   = WRAM_START + 0x00A8E
MMX3_ZSABER             = WRAM_START + 0x01FB2
MMX3_CAN_MOVE           = WRAM_START + 0x01F45
MMX3_ON_RIDE_ARMOR      = WRAM_START + 0x01F22
MMX3_FROZEN_SYSTEMS     = WRAM_START + 0x01F25
MMX3_HYPER_CANNON       = WRAM_START + 0x01FCC
MMX3_VICTORY            = WRAM_START + 0x0F46B

MMX3_ENABLE_HEART_TANK      = MMX3_RAM + 0x000E0
MMX3_ENABLE_HP_REFILL       = MMX3_RAM + 0x000E4
MMX3_HP_REFILL_AMOUNT       = MMX3_RAM + 0x000E5
MMX3_ENABLE_GIVE_1UP        = MMX3_RAM + 0x000E7
MMX3_ENABLE_WEAPON_REFILL   = MMX3_RAM + 0x000E8
MMX3_WEAPON_REFILL_AMOUNT   = MMX3_RAM + 0x000E9
MMX3_RECEIVING_ITEM         = MMX3_RAM + 0x000FF
MMX3_UNLOCKED_CHARGED_SHOT  = MMX3_RAM + 0x0006C

MMX3_ENERGY_LINK_COUNT      = MMX3_RAM + 0x00128
MMX3_GLOBAL_TIMER           = MMX3_RAM + 0x0012E
MMX3_GLOBAL_DEATHS          = MMX3_RAM + 0x00132
MMX3_GLOBAL_DMG_DEALT       = MMX3_RAM + 0x00134
MMX3_GLOBAL_DMG_TAKEN       = MMX3_RAM + 0x00136
MMX3_CHECKPOINTS_REACHED    = MMX3_RAM + 0x00100
MMX3_REFILL_REQUEST         = MMX3_RAM + 0x00138
MMX3_REFILL_TARGET          = MMX3_RAM + 0x00139
MMX3_ARSENAL_SYNC           = MMX3_RAM + 0x0013A
MMX3_UNLOCKED_CHIPS         = MMX3_RAM + 0x00180
MMX3_PROCESS_UNLOCKS        = MMX3_RAM + 0x000FE

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
MMX3_DEATH_LINK_ACTIVE      = ROM_START + 0x17FFF8
MMX3_JAMMED_BUSTER_ACTIVE   = ROM_START + 0x17FFF9

EXCHANGE_RATE = 500000000

MMX3_RECV_INDEX = MMX3_RAM + 0x0006E

MMX3_ROMHASH_START = 0x7FC0
ROMHASH_SIZE = 0x15

X_Z_ITEMS = ["1up", "hp refill", "weapon refill"]

class MMX3SNIClient(SNIClient):
    game = "Mega Man X3"
    patch_suffix = ".apmmx3"

    def __init__(self):
        super().__init__()
        self.game_state = False
        self.last_death_link = 0
        self.energy_link_enabled = False
        self.heal_request_command = None
        self.weapon_refill_request_command = None
        self.using_newer_client = False
        self.trade_request = None
        self.data_storage_enabled = False
        self.save_arsenal = False
        self.resync_request = False
        self.current_level_value = 42
        self.item_queue = []


    async def deathlink_kill_player(self, ctx):
        from SNIClient import DeathState, snes_buffered_write, snes_flush_writes, snes_read

        validation = await snes_read(ctx, MMX3_VALIDATION_CHECK, 0x2)
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            return

        receiving_item = await snes_read(ctx, MMX3_RECEIVING_ITEM, 0x1)
        menu_state = await snes_read(ctx, MMX3_MENU_STATE, 0x1)
        gameplay_state = await snes_read(ctx, MMX3_GAMEPLAY_STATE, 0x1)
        can_move = await snes_read(ctx, MMX3_CAN_MOVE, 0x1)
        frozen_systems = await snes_read(ctx, MMX3_FROZEN_SYSTEMS, 0x7)
        pause_state = await snes_read(ctx, MMX3_PAUSE_STATE, 0x1)
        if menu_state[0] != 0x04 or \
            gameplay_state[0] != 0x04 or \
            can_move[0] != 0x00 or \
            pause_state[0] != 0x00 or \
            receiving_item[0] != 0x00 or \
            frozen_systems != b'\x00\x00\x00\x00\x00\x00\x00':
            return
        
        snes_buffered_write(ctx, MMX3_CURRENT_HP, bytes([0x80]))
        snes_buffered_write(ctx, WRAM_START + 0x00A7B, bytes([0x8C]))
        ram_0A7D = await snes_read(ctx, WRAM_START + 0x00A7D, 1)
        ram_0A7D = ram_0A7D[0] & 0x7F
        snes_buffered_write(ctx, WRAM_START + 0x00A7D, bytes([ram_0A7D]))

        await snes_flush_writes(ctx)

        ctx.death_state = DeathState.dead
        ctx.last_death_link = time.time()


    async def validate_rom(self, ctx):
        from SNIClient import snes_read

        energy_link = await snes_read(ctx, MMX3_ENERGY_LINK_ENABLED, 0x1)
        rom_name = await snes_read(ctx, MMX3_ROMHASH_START, ROMHASH_SIZE)
        if rom_name is None or rom_name == bytes([0] * ROMHASH_SIZE) or rom_name[:4] != b"MMX3":
            if "heal" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("heal")
            if "refill" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("refill")
            if "trade" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("trade")
            if "resync" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("resync")
            return False
        
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.receive_option = 0
        ctx.send_option = 0
        ctx.allow_collect = True
        if energy_link[0]:
            if "heal" not in ctx.command_processor.commands:
                ctx.command_processor.commands["heal"] = cmd_heal
            if "refill" not in ctx.command_processor.commands:
                ctx.command_processor.commands["refill"] = cmd_refill
        if "trade" not in ctx.command_processor.commands:
            ctx.command_processor.commands["trade"] = cmd_trade
        if "resync" not in ctx.command_processor.commands:
            ctx.command_processor.commands["resync"] = cmd_resync

        death_link = await snes_read(ctx, MMX3_DEATH_LINK_ACTIVE, 1)
        if death_link[0]:
            await ctx.update_death_link(bool(death_link[0] & 0b1))

        ctx.rom = rom_name

        return True
    

    def on_package(self, ctx, cmd: str, args: dict):
        super().on_package(ctx, cmd, args)

        if cmd == "Connected":
            slot_data = args.get("slot_data", None)
            self.using_newer_client = True
            ctx.set_notify(f"mmx3_global_timer_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx3_deaths_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx3_damage_taken_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx3_damage_dealt_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx3_checkpoints_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx3_arsenal_{ctx.team}_{ctx.slot}")
            if slot_data["energy_link"]:
                ctx.set_notify(f"EnergyLink{ctx.team}")
                if ctx.ui:
                    ctx.ui.enable_energy_link()
                    ctx.ui.energy_link_label.text = "Energy: Standby"
                    logger.info(f"Initialized EnergyLink{ctx.team}")

        elif cmd == "SetReply" and args["key"].startswith("EnergyLink"):
            if ctx.ui:
                pool = (args["value"] or 0) / EXCHANGE_RATE
                ctx.ui.energy_link_label.text = f"Energy: {pool:.2f}"

        elif cmd == "Retrieved":
            if f"EnergyLink{ctx.team}" in args["keys"] and args["keys"][f"EnergyLink{ctx.team}"] and ctx.ui:
                pool = (args["keys"][f"EnergyLink{ctx.team}"] or 0) / EXCHANGE_RATE
                ctx.ui.energy_link_label.text = f"Energy: {pool:.2f}"


    async def game_watcher(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        game_state = await snes_read(ctx, MMX3_GAME_STATE, 0x1)
        menu_state = await snes_read(ctx, MMX3_MENU_STATE, 0x1)
        gameplay_state = await snes_read(ctx, MMX3_GAMEPLAY_STATE, 0x1)

        # Discard uninitialized ROMs
        if menu_state is None:
            self.game_state = False
            self.energy_link_enabled = False
            self.item_queue = []
            self.current_level_value = 42
            return
    
        validation = await snes_read(ctx, MMX3_VALIDATION_CHECK, 0x2)
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            snes_logger.info(f'ROM not properly validated.')
            self.game_state = False
            return

        if game_state[0] == 0:
            self.game_state = False
            self.item_queue = []
            self.current_level_value = 42
            ctx.locations_checked = set()
            
            # Resync data if solicited 
            if self.resync_request:
                await ctx.send_msgs([{
                    "cmd": "Set", "key": f"mmx3_arsenal_{ctx.team}_{ctx.slot}", "operations":
                        [{"operation": "replace", "value": dict()}],
                }])
                self.resync_request = False
                logger.info(f"Successfully cleared save data!")
            return
        
        if self.resync_request:
            self.resync_request = False
            logger.info(f"Invalid environment for a resync. Please try again during the Title Menu screen.")
        
        self.game_state = True
        if "DeathLink" in ctx.tags and menu_state[0] == 0x04 and ctx.last_death_link + 1 < time.time():
            currently_dead = gameplay_state[0] == 0x06
            await ctx.handle_deathlink_state(currently_dead)

        if game_state[0] != 0x00 and self.data_storage_enabled is True:
            await self.handle_data_storage(ctx)

        # Handle DataStorage
        if ctx.server and ctx.server.socket.open and not self.data_storage_enabled and ctx.team is not None:
            self.data_storage_enabled = True
            ctx.set_notify(f"mmx3_global_timer_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx3_deaths_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx3_damage_taken_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx3_damage_dealt_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx3_checkpoints_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx3_arsenal_{ctx.team}_{ctx.slot}")

        if self.trade_request is not None:
            await self.handle_hp_trade(ctx)

        await self.handle_item_queue(ctx)

        # This is going to be rewritten whenever SNIClient supports on_package
        energy_link = await snes_read(ctx, MMX3_ENERGY_LINK_ENABLED, 0x1)
        if self.using_newer_client:
            if energy_link[0] != 0:
                await self.handle_energy_link(ctx)
        else:
            if energy_link[0] != 0:
                if self.energy_link_enabled and f'EnergyLink{ctx.team}' in ctx.stored_data:
                    await self.handle_energy_link(ctx)

                if ctx.server and ctx.server.socket.open and not self.energy_link_enabled and ctx.team is not None:
                    self.energy_link_enabled = True
                    ctx.set_notify(f"EnergyLink{ctx.team}")
                    logger.info(f"Initialized EnergyLink{ctx.team}, use /help to get information about the EnergyLink commands.")

        from .Rom import weapon_rom_data, ride_armor_rom_data, upgrades_rom_data, boss_access_rom_data, refill_rom_data, chip_rom_data
        from .Levels import location_id_to_level_id
        from worlds import AutoWorldRegister

        bit_byte_vile = await snes_read(ctx, MMX3_BIT_BYTE_VILE, 0x01)
        defeated_bosses = list(await snes_read(ctx, MMX3_DEFEATED_BOSSES, 0x20))
        cleared_levels = list(await snes_read(ctx, MMX3_LEVEL_CLEARED, 0x20))
        victory_ram = await snes_read(ctx, MMX3_VICTORY, 0x1)
        collected_heart_tanks = await snes_read(ctx, MMX3_COLLECTED_HEART_TANKS, 0x01)
        collected_ride_chips = await snes_read(ctx, MMX3_COLLECTED_RIDE_CHIPS, 0x01)
        collected_upgrades = await snes_read(ctx, MMX3_COLLECTED_UPGRADES, 0x01)
        collected_pickups = list(await snes_read(ctx, MMX3_COLLECTED_PICKUPS, 0x40))
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
                    masked_data = collected_heart_tanks[0] & bit
                    if masked_data != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x03:
                    # Sub Tank
                    masked_data = collected_upgrades[0] & data_bit
                    if masked_data != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x04:
                    # Mega Man upgrades
                    masked_data = collected_upgrades[0] & data_bit
                    if masked_data != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x05:
                    # Ride Armor
                    masked_data = collected_ride_chips[0] & data_bit
                    if masked_data != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x06:
                    # Mega Man chips
                    masked_data = collected_ride_chips[0] & data_bit
                    if masked_data != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x09:
                    # Vile Defeated
                    vile_defeated = bit_byte_vile[0] & 0x30
                    if vile_defeated != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x0A:
                    # Byte Defeated
                    byte_defeated = bit_byte_vile[0] & 0x0C
                    if byte_defeated != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x0B:
                    # Bit Defeated
                    bit_defeated = bit_byte_vile[0] & 0x03
                    if bit_defeated != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x0E:
                    # Victory
                    if victory_ram[0]:
                        new_checks.append(loc_id)
                elif internal_id >= 0x300:
                    # Maverick Medal
                    if cleared_levels[data_bit] != 0:
                        new_checks.append(loc_id)
                elif internal_id >= 0x200:
                    # Boss clear
                    boss_id = internal_id & 0x1F
                    if defeated_bosses[boss_id] != 0:
                        new_checks.append(loc_id)
                elif internal_id >= 0x100:
                    # Pickups
                    if not pickupsanity_enabled or pickupsanity_enabled[0] == 0:
                        continue
                    pickup_id = internal_id & 0x3F
                    if collected_pickups[pickup_id] != 0:
                        new_checks.append(loc_id)
        
                        
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
            location = ctx.location_names.lookup_in_game(new_check_id)
            snes_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])

        # Send Current Room for Tracker
        current_level = int.from_bytes(await snes_read(ctx, MMX3_LEVEL_INDEX, 0x1), "little")

        if game_state[0] == 0x00 or \
           (game_state[0] == 0x02 and menu_state[0] != 0x04):
            current_level = -1

        if self.current_level_value != (current_level + 1):
            self.current_level_value = current_level + 1

            # Send level id data to tracker
            await ctx.send_msgs(
                [
                    {
                        "cmd": "Set",
                        "key": f"mmx3_level_id_{ctx.team}_{ctx.slot}",
                        "default": 0,
                        "want_reply": False,
                        "operations": [
                            {
                                "operation": "replace",
                                "value": self.current_level_value,
                            }
                        ],
                    }
                ]
            )

        recv_count = await snes_read(ctx, MMX3_RECV_INDEX, 2)
        if recv_count is None:
            # Add a small failsafe in case we get a None. Other SNI games do this...
            return

        recv_index = int.from_bytes(recv_count, "little")
        sync_arsenal = int.from_bytes(await snes_read(ctx, MMX3_ARSENAL_SYNC, 0x2), "little")

        if recv_index < len(ctx.items_received) and sync_arsenal != 0x1337:
            item = ctx.items_received[recv_index]
            recv_index += 1
            sending_game = ctx.slot_info[item.player].game
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_game(item.item), 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), recv_index, len(ctx.items_received)))

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

            elif item.item in chip_rom_data:
                self.add_item_to_queue("enhancement", item.item)

            elif item.item in boss_access_rom_data:
                boss_access = bytearray(await snes_read(ctx, MMX3_UNLOCKED_LEVELS, 0x20))
                level = boss_access_rom_data[item.item]
                boss_access[level[0] * 2] = 0x01
                snes_buffered_write(ctx, MMX3_UNLOCKED_LEVELS, boss_access)
                if item.item == 0xBD000A:
                    snes_buffered_write(ctx, MMX3_DOPPLER_ACCESS, bytearray([0x00]))
                snes_buffered_write(ctx, MMX3_SFX_FLAG, bytearray([0x01]))
                snes_buffered_write(ctx, MMX3_SFX_NUMBER, bytearray([0x1D]))
                self.save_arsenal = True

            elif item.item == 0xBD0019:
                # Unlock vile stage
                snes_buffered_write(ctx, MMX3_VILE_ACCESS, bytearray([0x00]))
                snes_buffered_write(ctx, MMX3_SFX_FLAG, bytearray([0x01]))
                snes_buffered_write(ctx, MMX3_SFX_NUMBER, bytearray([0x1D]))
                self.save_arsenal = True
                
            elif item.item in refill_rom_data:
                self.add_item_to_queue(refill_rom_data[item.item][0], item.item, refill_rom_data[item.item][1])
                self.save_arsenal = True

            elif item.item == 0xBD0000:
                # Handle goal
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                self.save_arsenal = True
                ctx.finished_game = True
                return
                
        # Handle collected locations
        game_state = await snes_read(ctx, MMX3_GAME_STATE, 0x1)
        if game_state[0] != 0x02:
            ctx.locations_checked = set()
            return
        new_boss_clears = False
        new_cleared_level = False
        new_heart_tank = False
        new_upgrade = False
        new_ride_chip = False
        new_bit_byte_vile = False
        new_pickup = False
        cleared_levels = list(await snes_read(ctx, MMX3_LEVEL_CLEARED, 0x20))
        collected_pickups = list(await snes_read(ctx, MMX3_COLLECTED_PICKUPS, 0x40))
        collected_heart_tanks = int.from_bytes(await snes_read(ctx, MMX3_COLLECTED_HEART_TANKS, 0x01))
        collected_upgrades = int.from_bytes(await snes_read(ctx, MMX3_COLLECTED_UPGRADES, 0x01))
        collected_ride_chips = int.from_bytes(await snes_read(ctx, MMX3_COLLECTED_RIDE_CHIPS, 0x01))
        defeated_bosses = list(await snes_read(ctx, MMX3_DEFEATED_BOSSES, 0x20))
        bit_byte_vile = int.from_bytes(await snes_read(ctx, MMX3_BIT_BYTE_VILE, 0x01))
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
                level_id = data[0]
                internal_id = data[1]
                data_bit = data[2]

                if internal_id == 0x02:
                    # Heart Tank
                    bit = 0x01 << (level_id - 1)
                    collected_heart_tanks |= bit
                    new_heart_tank = True
                elif internal_id == 0x03:
                    # Sub Tank
                    collected_upgrades |= data_bit
                    new_upgrade = True
                elif internal_id == 0x04:
                    # Mega Man upgrades
                    collected_upgrades |= data_bit
                    new_upgrade = True
                elif internal_id == 0x05:
                    # Ride Armor
                    collected_ride_chips |= data_bit
                    new_ride_chip = True
                elif internal_id == 0x06:
                    # Mega Man chips
                    collected_ride_chips |= data_bit
                    new_ride_chip = True
                elif internal_id == 0x09:
                    # Vile Defeated
                    bit_byte_vile |= 0x30
                    new_bit_byte_vile = True
                elif internal_id == 0x0A:
                    # Byte Defeated
                    bit_byte_vile |= 0x0C
                    new_bit_byte_vile = True
                elif internal_id == 0x0B:
                    # Bit Defeated
                    bit_byte_vile |= 0x03
                    new_bit_byte_vile = True
                elif internal_id == 0x0E:
                    # Victory
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
                elif internal_id >= 0x100:
                    # Pickups
                    pickup_id = internal_id & 0x3F
                    collected_pickups[pickup_id] = 0xFF
                    new_pickup = True

        if new_cleared_level:
            snes_buffered_write(ctx, MMX3_LEVEL_CLEARED, bytes(cleared_levels))
        if new_boss_clears:
            snes_buffered_write(ctx, MMX3_DEFEATED_BOSSES, bytes(defeated_bosses))
        if new_bit_byte_vile:
            snes_buffered_write(ctx, MMX3_BIT_BYTE_VILE, bytearray([bit_byte_vile]))
        if new_pickup:
            snes_buffered_write(ctx, MMX3_COLLECTED_PICKUPS, bytes(collected_pickups))
        if new_upgrade:
            snes_buffered_write(ctx, MMX3_COLLECTED_UPGRADES, bytearray([collected_upgrades]))
        if new_heart_tank:
            snes_buffered_write(ctx, MMX3_COLLECTED_HEART_TANKS, bytearray([collected_heart_tanks]))
        if new_ride_chip:
            snes_buffered_write(ctx, MMX3_COLLECTED_RIDE_CHIPS, bytearray([collected_ride_chips]))
        await snes_flush_writes(ctx)


    async def handle_hp_trade(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        validation = await snes_read(ctx, MMX3_VALIDATION_CHECK, 0x2)
        if validation is None:
            return
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            return

        # Can only process trades during the pause state
        menu_state = await snes_read(ctx, MMX3_MENU_STATE, 0x1)
        gameplay_state = await snes_read(ctx, MMX3_GAMEPLAY_STATE, 0x1)
        can_move = await snes_read(ctx, MMX3_CAN_MOVE, 0x1)
        if menu_state[0] != 0x04 or \
            gameplay_state[0] != 0x04 or \
            can_move[0] != 0x00:
            return
        
        pause_state = await snes_read(ctx, MMX3_PAUSE_STATE, 0x1)
        if pause_state[0] == 0x00:
            return

        for item in self.item_queue:
            if item[0] == "weapon refill":
                self.trade_request = None
                logger.info(f"You already have a Weapon Energy request pending to be received.")
                return

        # Can trade HP -> WPN if HP is above 1
        current_hp = await snes_read(ctx, MMX3_CURRENT_HP, 0x1)
        if current_hp[0] > 0x01:
            max_trade = current_hp[0] - 1
            set_trade = self.trade_request if self.trade_request <= max_trade else max_trade
            self.add_item_to_queue("weapon refill", None, set_trade)
            new_hp = current_hp[0] - set_trade
            snes_buffered_write(ctx, MMX3_CURRENT_HP, bytearray([new_hp]))
            await snes_flush_writes(ctx)
            self.trade_request = None
            logger.info(f"Traded {set_trade} HP for {set_trade} Weapon Energy.")
        else:
            logger.info("Couldn't process trade. HP is too low.")
        

    async def handle_energy_link(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        # Handle validation
        validation = await snes_read(ctx, MMX3_VALIDATION_CHECK, 0x2)
        if validation is None:
            return
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            return
        
        # Deposit heals into the pool regardless of energy_link setting
        energy_packet = await snes_read(ctx, MMX3_ENERGY_LINK_PACKET, 0x2)
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
            snes_buffered_write(ctx, MMX3_ENERGY_LINK_PACKET, bytearray([0x00, 0x00]))
            await snes_flush_writes(ctx)

        # Expose EnergyLink to the ROM
        pause_state = await snes_read(ctx, MMX3_PAUSE_STATE, 0x1)
        screen_brightness = await snes_read(ctx, MMX3_SCREEN_BRIGHTNESS, 0x1)
        if pause_state[0] != 0x00 or screen_brightness[0] == 0x0F:
            pool = ctx.stored_data[f'EnergyLink{ctx.team}'] or 0
            total_energy = int(pool / EXCHANGE_RATE)
            if total_energy < 9999:
                snes_buffered_write(ctx, MMX3_ENERGY_LINK_COUNT, bytearray([total_energy & 0xFF, (total_energy >> 8) & 0xFF]))
            else:
                snes_buffered_write(ctx, MMX3_ENERGY_LINK_COUNT, bytearray([0x0F, 0x27]))

        receiving_item = await snes_read(ctx, MMX3_RECEIVING_ITEM, 0x1)
        menu_state = await snes_read(ctx, MMX3_MENU_STATE, 0x1)
        gameplay_state = await snes_read(ctx, MMX3_GAMEPLAY_STATE, 0x1)
        can_move = await snes_read(ctx, MMX3_CAN_MOVE, 0x1)
        frozen_systems = await snes_read(ctx, MMX3_FROZEN_SYSTEMS, 0x7)
        if menu_state[0] != 0x04 or \
            gameplay_state[0] != 0x04 or \
            can_move[0] != 0x00 or \
            receiving_item[0] != 0x00 or \
            frozen_systems != b'\x00\x00\x00\x00\x00\x00\x00':
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
        if not skip_hp or not skip_weapon:
            # Handle in-game requests
            request = int.from_bytes(await snes_read(ctx, MMX3_REFILL_REQUEST, 0x1), "little")
            target = int.from_bytes(await snes_read(ctx, MMX3_REFILL_TARGET, 0x1), "little")
            if request != 0:
                if target == 0:
                    if self.heal_request_command is None:
                        self.heal_request_command = request
                else: 
                    if self.weapon_refill_request_command is None:
                        self.weapon_refill_request_command = request
                snes_buffered_write(ctx, MMX3_REFILL_REQUEST, bytearray([0x00]))

        if not skip_hp:
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
                self.add_item_to_queue("hp refill", None, heal_needed)
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
                self.add_item_to_queue("weapon refill", None, heal_needed)
                pool = (pool / EXCHANGE_RATE) - heal_needed
                logger.info(f"Refilled current weapon by {heal_needed}. Energy available: {pool:.2f}")
                self.weapon_refill_request_command = None


    def add_item_to_queue(self, item_type, item_id, item_additional = None):
        if not hasattr(self, "item_queue"):
            self.item_queue = []
        self.item_queue.append([item_type, item_id, item_additional])


    async def handle_item_queue(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        from .Rom import weapon_rom_data, ride_armor_rom_data, upgrades_rom_data, chip_rom_data

        if not hasattr(self, "item_queue") or len(self.item_queue) == 0:
            return

        validation = await snes_read(ctx, MMX3_VALIDATION_CHECK, 0x2)
        if validation is None:
            return
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            return

        # Do not give items if you can't move, are in pause state, not in the correct mode or not in gameplay state
        receiving_item = await snes_read(ctx, MMX3_RECEIVING_ITEM, 0x1)
        menu_state = await snes_read(ctx, MMX3_MENU_STATE, 0x1)
        gameplay_state = await snes_read(ctx, MMX3_GAMEPLAY_STATE, 0x1)
        hp_refill = await snes_read(ctx, MMX3_ENABLE_HP_REFILL, 0x1)
        weapon_refill = await snes_read(ctx, MMX3_ENABLE_WEAPON_REFILL, 0x1)
        can_move = await snes_read(ctx, MMX3_CAN_MOVE, 0x1)
        on_ride_armor = await snes_read(ctx, MMX3_ON_RIDE_ARMOR, 0x1)
        frozen_systems = await snes_read(ctx, MMX3_FROZEN_SYSTEMS, 0x7)
        if menu_state[0] != 0x04 or \
           gameplay_state[0] != 0x04 or \
           can_move[0] != 0x00 or \
           hp_refill[0] != 0x00 or \
           weapon_refill[0] != 0x00 or \
           on_ride_armor[0] == 0x0A or \
           receiving_item[0] != 0x00 or \
           frozen_systems != b'\x00\x00\x00\x00\x00\x00\x00':
            return
        
        next_item = self.item_queue[0]
        item_id = next_item[1]
        
        # Handle items that Zero can also get
        if next_item[0] in X_Z_ITEMS:
            backup_item = self.item_queue.pop(0)
            
            if next_item[0] == "hp refill":
                current_hp = await snes_read(ctx, MMX3_CURRENT_HP, 0x1)
                max_hp = await snes_read(ctx, MMX3_MAX_HP, 0x1)

                if current_hp[0] < max_hp[0]:
                    snes_buffered_write(ctx, MMX3_ENABLE_HP_REFILL, bytearray([0x02]))
                    snes_buffered_write(ctx, MMX3_HP_REFILL_AMOUNT, bytearray([next_item[2]]))
                    snes_buffered_write(ctx, MMX3_RECEIVING_ITEM, bytearray([0x01]))
                else:
                    # TODO: Sub Tank logic
                    self.item_queue.append(backup_item)
                    
            elif next_item[0] == "weapon refill":
                snes_buffered_write(ctx, MMX3_ENABLE_WEAPON_REFILL, bytearray([0x02]))
                snes_buffered_write(ctx, MMX3_WEAPON_REFILL_AMOUNT, bytearray([next_item[2]]))
                snes_buffered_write(ctx, MMX3_RECEIVING_ITEM, bytearray([0x01]))

            elif next_item[0] == "1up":
                life_count = await snes_read(ctx, MMX3_LIFE_COUNT, 0x1)
                if life_count[0] < 99:
                    snes_buffered_write(ctx, MMX3_ENABLE_GIVE_1UP, bytearray([0x01]))
                    snes_buffered_write(ctx, MMX3_RECEIVING_ITEM, bytearray([0x01]))
                    self.save_arsenal = True
                else:
                    self.item_queue.append(backup_item)

        # Ignore Zero for the following items
        pause_state = await snes_read(ctx, MMX3_PAUSE_STATE, 0x1)
        screen_brightness = await snes_read(ctx, MMX3_SCREEN_BRIGHTNESS, 0x1)
        active_character = await snes_read(ctx, MMX3_ACTIVE_CHARACTER, 0x1)
        if active_character[0] != 0x00 and (pause_state[0] != 0x00 or screen_brightness[0] != 0x0F):
            await snes_flush_writes(ctx)
            if len(self.item_queue) != 0:
                backup_item = self.item_queue.pop(0)
                self.item_queue.append(backup_item)
            return

        if next_item[0] == "weapon":
            weapon = weapon_rom_data[item_id]
            snes_buffered_write(ctx, WRAM_START + weapon[0], bytearray([weapon[1]]))
            snes_buffered_write(ctx, MMX3_SFX_FLAG, bytearray([0x01]))
            snes_buffered_write(ctx, MMX3_SFX_NUMBER, bytearray([0x16]))
            self.item_queue.pop(0)
            self.save_arsenal = True
            
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
            self.save_arsenal = True

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
            self.item_queue.pop(0)
            self.save_arsenal = True
        
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
                if bit == 0x01:
                    snes_buffered_write(ctx, WRAM_START + 0x09EE, bytearray([0x18]))
                    snes_buffered_write(ctx, MMX3_UPGRADES, bytearray([upgrades]))
                    snes_buffered_write(ctx, WRAM_START + 0x0F4ED, bytearray([0x80]))
                elif bit == 0x02:
                    jam_check = await snes_read(ctx, MMX3_JAMMED_BUSTER_ACTIVE, 0x1)
                    charge_shot_unlocked = await snes_read(ctx, MMX3_UNLOCKED_CHARGED_SHOT, 0x1)
                    if jam_check[0] == 1 and charge_shot_unlocked[0] == 0:
                        snes_buffered_write(ctx, MMX3_UNLOCKED_CHARGED_SHOT, bytearray([0x01]))
                    else:
                        value = await snes_read(ctx, WRAM_START + 0x0AE8, 0x1)
                        snes_buffered_write(ctx, WRAM_START + 0x0AE8, bytearray([value[0] + 1]))
                        snes_buffered_write(ctx, WRAM_START + 0x0AF2, bytearray([0x00]))
                        snes_buffered_write(ctx, WRAM_START + 0x0AF3, bytearray([0x00]))
                        snes_buffered_write(ctx, WRAM_START + 0x0AE9, bytearray([0x00]))
                        snes_buffered_write(ctx, WRAM_START + 0x0AF8, bytearray([0x5D]))
                        snes_buffered_write(ctx, MMX3_UPGRADES, bytearray([upgrades]))
                elif bit == 0x04:
                    value = await snes_read(ctx, WRAM_START + 0x0B08, 0x1)
                    snes_buffered_write(ctx, WRAM_START + 0x0B08, bytearray([value[0] + 1]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B12, bytearray([0x00]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B13, bytearray([0x01]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B09, bytearray([0x00]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B18, bytearray([0x5D]))
                    snes_buffered_write(ctx, MMX3_UPGRADES, bytearray([upgrades]))
                elif bit == 0x08:
                    value = await snes_read(ctx, WRAM_START + 0x0B28, 0x1)
                    snes_buffered_write(ctx, WRAM_START + 0x0B28, bytearray([value[0] + 1]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B32, bytearray([0x00]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B33, bytearray([0x02]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B29, bytearray([0x00]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B38, bytearray([0x5D]))
                    snes_buffered_write(ctx, MMX3_UPGRADES, bytearray([upgrades]))
                snes_buffered_write(ctx, MMX3_SFX_FLAG, bytearray([0x01]))
                snes_buffered_write(ctx, MMX3_SFX_NUMBER, bytearray([0x1B]))
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
            self.item_queue.pop(0)
            self.save_arsenal = True

        elif next_item[0] == "ride":
            ride = await snes_read(ctx, MMX3_RIDE_CHIPS, 0x1)
            ride = ride[0]
            upgrade = ride_armor_rom_data[item_id]
            bit = 1 << upgrade[0]
            check = ride & bit
            if check == 0:
                ride |= bit
                snes_buffered_write(ctx, MMX3_RIDE_CHIPS, bytearray([ride]))
                snes_buffered_write(ctx, MMX3_SFX_FLAG, bytearray([0x01]))
                snes_buffered_write(ctx, MMX3_SFX_NUMBER, bytearray([0x32]))
            self.item_queue.pop(0)
            self.save_arsenal = True

        elif next_item[0] == "enhancement":
            chip_offset = chip_rom_data[item_id][0]
            snes_buffered_write(ctx, MMX3_RAM + chip_offset, bytearray([0x80]))
            snes_buffered_write(ctx, MMX3_SFX_FLAG, bytearray([0x01]))
            snes_buffered_write(ctx, MMX3_SFX_NUMBER, bytearray([0x1B]))
            self.save_arsenal = True
            self.item_queue.pop(0)

        await snes_flush_writes(ctx)


    async def handle_data_storage(self, ctx):
        from SNIClient import snes_read, snes_buffered_write, snes_flush_writes
        # Only do arsenal after the map's initial load or the intro stage is selected
        menu_state = int.from_bytes(await snes_read(ctx, MMX3_MENU_STATE, 0x1))
        gameplay_state = int.from_bytes(await snes_read(ctx, MMX3_GAMEPLAY_STATE, 0x1))
        map_state = int.from_bytes(await snes_read(ctx, WRAM_START + 0x1E59, 0x1))
        sync_arsenal = int.from_bytes(await snes_read(ctx, MMX3_ARSENAL_SYNC, 0x2), "little")
        if (menu_state == 0x00 and map_state == 0x0A) or (menu_state == 0x04 and gameplay_state == 0x04):
            # Load Arsenal
            if sync_arsenal == 0x1337:
                arsenal = ctx.stored_data[f"mmx3_arsenal_{ctx.team}_{ctx.slot}"] or dict()
                if arsenal:
                    # Data in arsenal
                    snes_buffered_write(ctx, MMX3_RECV_INDEX, bytes(arsenal["recv_index"].to_bytes(2, 'little')))
                    snes_buffered_write(ctx, MMX3_LIFE_COUNT, bytes(arsenal["life_count"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX3_UPGRADES, bytes(arsenal["upgrades"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX3_RIDE_CHIPS, bytes(arsenal["ride_chips"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX3_MAX_HP, bytes(arsenal["max_hp"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX3_HEART_TANKS, bytes(arsenal["heart_tanks"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX3_SUB_TANK_ARRAY, bytearray(arsenal["sub_tanks"]))
                    snes_buffered_write(ctx, MMX3_UNLOCKED_CHARGED_SHOT, bytes(arsenal["unlocked_buster"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX3_WEAPON_ARRAY, bytearray(arsenal["weapons"]))
                    snes_buffered_write(ctx, MMX3_UNLOCKED_CHIPS, bytearray(arsenal["enhancements"]))
                    snes_buffered_write(ctx, MMX3_HYPER_CANNON, bytes(arsenal["hyper_cannon"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX3_ZSABER, bytes(arsenal["z_saber"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX3_UNLOCKED_LEVELS, bytearray(arsenal["levels"]))
                    snes_buffered_write(ctx, MMX3_DOPPLER_ACCESS, bytes(arsenal["doppler_access"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX3_VILE_ACCESS, bytes(arsenal["vile_access"].to_bytes(1, 'little')))

                snes_buffered_write(ctx, MMX3_ARSENAL_SYNC, bytearray([0x00,0x00]))
                await snes_flush_writes(ctx)

        # Save Arsenal
        if self.save_arsenal and sync_arsenal != 0x1337:
            arsenal = dict()
            arsenal["recv_index"] = int.from_bytes(await snes_read(ctx, MMX3_RECV_INDEX, 0x2), "little")
            arsenal["life_count"] = int.from_bytes(await snes_read(ctx, MMX3_LIFE_COUNT, 0x1), "little")
            arsenal["upgrades"] = int.from_bytes(await snes_read(ctx, MMX3_UPGRADES, 0x1), "little")
            arsenal["ride_chips"] = int.from_bytes(await snes_read(ctx, MMX3_RIDE_CHIPS, 0x1), "little")
            arsenal["max_hp"] = int.from_bytes(await snes_read(ctx, MMX3_MAX_HP, 0x1), "little")
            arsenal["heart_tanks"] = int.from_bytes(await snes_read(ctx, MMX3_HEART_TANKS, 0x1), "little")
            arsenal["sub_tanks"] = list(await snes_read(ctx, MMX3_SUB_TANK_ARRAY, 0x4))
            arsenal["unlocked_buster"] = int.from_bytes(await snes_read(ctx, MMX3_UNLOCKED_CHARGED_SHOT, 0x1), "little")
            arsenal["weapons"] = list(await snes_read(ctx, MMX3_WEAPON_ARRAY, 0x10))
            arsenal["enhancements"] = list(await snes_read(ctx, MMX3_UNLOCKED_CHIPS, 0x18))
            arsenal["hyper_cannon"] = int.from_bytes(await snes_read(ctx, MMX3_HYPER_CANNON, 0x1), "little")
            arsenal["z_saber"] = int.from_bytes(await snes_read(ctx, MMX3_ZSABER, 0x1), "little")
            arsenal["levels"] = list(await snes_read(ctx, MMX3_UNLOCKED_LEVELS, 0x20))
            arsenal["doppler_access"] = int.from_bytes(await snes_read(ctx, MMX3_DOPPLER_ACCESS, 0x1), "little")
            arsenal["vile_access"] = int.from_bytes(await snes_read(ctx, MMX3_VILE_ACCESS, 0x1), "little")
            
            # Attempt to not lose any previously saved data in case of RAM corruption
            saved_arsenal = ctx.stored_data[f"mmx3_arsenal_{ctx.team}_{ctx.slot}"] or dict()
            if saved_arsenal:
                if saved_arsenal["recv_index"] > arsenal["recv_index"]:
                    arsenal["recv_index"] = saved_arsenal["recv_index"]
                if saved_arsenal["life_count"] > arsenal["life_count"]:
                    arsenal["life_count"] = saved_arsenal["life_count"]
                if saved_arsenal["max_hp"] > arsenal["max_hp"]:
                    arsenal["max_hp"] = saved_arsenal["max_hp"]
                for i in range(0x10):
                    arsenal["weapons"][i] |= saved_arsenal["weapons"][i] & 0x40
                for i in range(0x18):
                    arsenal["enhancements"][i] |= saved_arsenal["enhancements"][i] & 0x80
                for level in range(0x20):
                    arsenal["levels"][level] |= saved_arsenal["levels"][level]
                arsenal["doppler_access"] = min(saved_arsenal["doppler_access"], arsenal["doppler_access"])
                arsenal["vile_access"] = min(saved_arsenal["doppler_access"], arsenal["vile_access"])
                    
                arsenal["upgrades"] |= saved_arsenal["upgrades"]
                arsenal["unlocked_buster"] |= saved_arsenal["unlocked_buster"]
                arsenal["hyper_cannon"] |= saved_arsenal["hyper_cannon"] & 0x40
                arsenal["z_saber"] |= saved_arsenal["z_saber"] & 0xE0
                arsenal["ride_chips"] |= saved_arsenal["ride_chips"]
                arsenal["heart_tanks"] |= saved_arsenal["heart_tanks"]
                for i in range(0x4):
                    arsenal["sub_tanks"][i] |= saved_arsenal["sub_tanks"][i] & 0x80

            await ctx.send_msgs([{
                "cmd": "Set", "key": f"mmx3_arsenal_{ctx.team}_{ctx.slot}", "operations":
                    [{"operation": "replace", "value": arsenal}],
            }])
            self.save_arsenal = False
            
            snes_buffered_write(ctx, MMX3_PROCESS_UNLOCKS, bytearray([0x03]))
            await snes_flush_writes(ctx)
        
        keys = {
            f"mmx3_checkpoints_{ctx.team}_{ctx.slot}",
            f"mmx3_global_timer_{ctx.team}_{ctx.slot}",
            f"mmx3_deaths_{ctx.team}_{ctx.slot}",
            f"mmx3_damage_dealt_{ctx.team}_{ctx.slot}",
            f"mmx3_damage_taken_{ctx.team}_{ctx.slot}",
        }
        if not all(key in ctx.stored_data.keys() for key in keys):
            return

        # Checkpoints reached
        checkpoints = list(await snes_read(ctx, MMX3_CHECKPOINTS_REACHED, 0xF))
        data_storage_checkpoints = ctx.stored_data[f"mmx3_checkpoints_{ctx.team}_{ctx.slot}"] or [0 for _ in range(0xF)]
        computed_checkpoints = list()
        for i in range(0xF):
            if checkpoints[i] >= data_storage_checkpoints[i]:
                computed_checkpoints.append(checkpoints[i])
            else:
                computed_checkpoints.append(data_storage_checkpoints[i])
        await ctx.send_msgs([{
            "cmd": "Set", "key": f"mmx3_checkpoints_{ctx.team}_{ctx.slot}", "operations":
                [{"operation": "replace", "value": computed_checkpoints}],
        }])
        snes_buffered_write(ctx, MMX3_CHECKPOINTS_REACHED, bytes(computed_checkpoints))

        # Global timer
        timer = int.from_bytes(await snes_read(ctx, MMX3_GLOBAL_TIMER, 0x4), "little")
        data_storage_timer = ctx.stored_data[f"mmx3_global_timer_{ctx.team}_{ctx.slot}"] or 0
        if timer >= data_storage_timer:
            await ctx.send_msgs([{
                "cmd": "Set", "key": f"mmx3_global_timer_{ctx.team}_{ctx.slot}", "operations":
                    [{"operation": "replace", "value": timer},
                        {"operation": "min", "value": 0x03E73B3B}],
            }])
        else:
            snes_buffered_write(ctx, MMX3_GLOBAL_TIMER, data_storage_timer.to_bytes(4, "little"))

        # Death count
        deaths = int.from_bytes(await snes_read(ctx, MMX3_GLOBAL_DEATHS, 0x2), "little")
        data_storage_deaths = ctx.stored_data[f"mmx3_deaths_{ctx.team}_{ctx.slot}"] or 0
        if deaths >= data_storage_deaths:
            await ctx.send_msgs([{
                "cmd": "Set", "key": f"mmx3_deaths_{ctx.team}_{ctx.slot}", "operations":
                    [{"operation": "replace", "value": deaths},
                        {"operation": "min", "value": 9999}],
            }])
        else:
            snes_buffered_write(ctx, MMX3_GLOBAL_DEATHS, data_storage_deaths.to_bytes(2, "little"))

        # Damage dealt
        dmg_dealt = int.from_bytes(await snes_read(ctx, MMX3_GLOBAL_DMG_DEALT, 0x2), "little")
        data_storage_dmg_dealt = ctx.stored_data[f"mmx3_damage_dealt_{ctx.team}_{ctx.slot}"] or 0
        if dmg_dealt >= data_storage_dmg_dealt:
            await ctx.send_msgs([{
                "cmd": "Set", "key": f"mmx3_damage_dealt_{ctx.team}_{ctx.slot}", "operations":
                    [{"operation": "replace", "value": dmg_dealt},
                        {"operation": "min", "value": 9999}],
            }])
        else:
            snes_buffered_write(ctx, MMX3_GLOBAL_DMG_DEALT, data_storage_dmg_dealt.to_bytes(2, "little"))
        
        # Damage taken
        dmg_taken = int.from_bytes(await snes_read(ctx, MMX3_GLOBAL_DMG_TAKEN, 0x2), "little")
        data_storage_dmg_taken = ctx.stored_data[f"mmx3_damage_taken_{ctx.team}_{ctx.slot}"] or 0
        if dmg_taken >= data_storage_dmg_taken:
            await ctx.send_msgs([{
                "cmd": "Set", "key": f"mmx3_damage_taken_{ctx.team}_{ctx.slot}", "operations":
                    [{"operation": "replace", "value": dmg_taken},
                        {"operation": "min", "value": 9999}],
            }])
        else:
            snes_buffered_write(ctx, MMX3_GLOBAL_DMG_TAKEN, data_storage_dmg_taken.to_bytes(2, "little"))
        
        await snes_flush_writes(ctx)


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
    if self.ctx.game != "Mega Man X3":
        logger.warning("This command can only be used while playing Mega Man X3")
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


def cmd_trade(self, amount: str = ""):
    """
    Trades HP to Weapon Energy. 1:1 ratio.
    """
    if self.ctx.game != "Mega Man X3":
        logger.warning("This command can only be used while playing Mega Man X3")
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


def cmd_resync(self):
    """
    Resets the save data to force Archipelago to send over every item again. Locations reached aren't affected.
    """
    if self.ctx.game != "Mega Man X3":
        logger.warning("This command can only be used while playing Mega Man X3")
    if (not self.ctx.server) or self.ctx.server.socket.closed or self.ctx.client_handler.game_state:
        logger.info(f"Must be connected to server and in the title screen.")
    else:
        if self.ctx.client_handler.resync_request:
            logger.info(f"You already placed a resync request.")
            return
        else:
            self.ctx.client_handler.resync_request = True
            logger.info(f"Placing a resync request...")
