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

MMX2_RAM = WRAM_START + 0x1F800

MMX2_GAME_STATE         = WRAM_START + 0x000D0
MMX2_MENU_STATE         = WRAM_START + 0x000D1
MMX2_GAMEPLAY_STATE     = WRAM_START + 0x000D2
MMX2_PAUSE_STATE        = WRAM_START + 0x01F37
MMX2_SCREEN_BRIGHTNESS  = WRAM_START + 0x000B4
MMX2_LEVEL_INDEX        = WRAM_START + 0x01FAD
MMX2_WEAPON_ARRAY       = WRAM_START + 0x01FBB
MMX2_HEART_TANKS        = WRAM_START + 0x01FD3
MMX2_SUB_TANK_ARRAY     = WRAM_START + 0x01FB6
MMX2_UPGRADES           = WRAM_START + 0x01FD0
MMX2_CURRENT_HP         = WRAM_START + 0x009FF
MMX2_CURRENT_WEAPON     = WRAM_START + 0x00A0B
MMX2_MAX_HP             = WRAM_START + 0x01FD1
MMX2_LIFE_COUNT         = WRAM_START + 0x01FB3
MMX2_SHORYUKEN          = WRAM_START + 0x01FB1
MMX2_CAN_MOVE           = WRAM_START + 0x01F25
MMX2_ON_RIDE_ARMOR      = WRAM_START + 0x00A54
MMX2_ZERO_PARTS         = WRAM_START + 0x01FD6

MMX2_ENABLE_HEART_TANK      = MMX2_RAM + 0x00009
MMX2_ENABLE_HP_REFILL       = MMX2_RAM + 0x0000D
MMX2_HP_REFILL_AMOUNT       = MMX2_RAM + 0x0000E
MMX2_ENABLE_GIVE_1UP        = MMX2_RAM + 0x00010
MMX2_ENABLE_WEAPON_REFILL   = MMX2_RAM + 0x00017
MMX2_WEAPON_REFILL_AMOUNT   = MMX2_RAM + 0x00018
MMX2_RECEIVING_ITEM         = MMX2_RAM + 0x00008
MMX2_UNLOCKED_CHARGED_SHOT  = MMX2_RAM + 0x00013
MMX2_UNLOCKED_CHECKPOINTS   = MMX2_RAM + 0x00016
MMX2_ENERGY_LINK_COUNT      = MMX2_RAM + 0x0001F
MMX2_GLOBAL_TIMER           = MMX2_RAM + 0x00025
MMX2_GLOBAL_DEATHS          = MMX2_RAM + 0x00029
MMX2_GLOBAL_DMG_DEALT       = MMX2_RAM + 0x0002B
MMX2_GLOBAL_DMG_TAKEN       = MMX2_RAM + 0x0002D
MMX2_CHECKPOINTS_REACHED    = MMX2_RAM + 0x001E0
MMX2_REFILL_REQUEST         = MMX2_RAM + 0x0002F
MMX2_REFILL_TARGET          = MMX2_RAM + 0x00030
MMX2_ARSENAL_SYNC           = MMX2_RAM + 0x0003E

MMX2_SFX_FLAG   = MMX2_RAM + 0x00003
MMX2_SFX_NUMBER = MMX2_RAM + 0x00004

MMX2_VALIDATION_CHECK = MMX2_RAM + 0x00011

MMX2_LEVEL_CLEARED          = MMX2_RAM + 0x00080
MMX2_UNLOCKED_LEVELS        = MMX2_RAM + 0x00060
MMX2_DEFEATED_BOSSES        = MMX2_RAM + 0x000A0
MMX2_BASE_ACCESS            = MMX2_RAM + 0x00002
MMX2_COLLECTED_HEART_TANKS  = MMX2_RAM + 0x00040
MMX2_COLLECTED_UPGRADES     = MMX2_RAM + 0x00041
MMX2_COLLECTED_PICKUPS      = MMX2_RAM + 0x000C0
MMX2_COMPLETED_REMATCHES    = MMX2_RAM + 0x00000
MMX2_ENERGY_LINK_PACKET     = MMX2_RAM + 0x00006
MMX2_COLLECTED_SHORYUKEN    = MMX2_RAM + 0x00042
MMX2_COLLECTED_SIGMA_ACCESS = MMX2_RAM + 0x00046

MMX2_PICKUPSANITY_ACTIVE    = ROM_START + 0x17FFE7
MMX2_REQUIRED_REMATCHES     = ROM_START + 0x17FFE3
MMX2_ENERGY_LINK_ENABLED    = ROM_START + 0x17FFE8
MMX2_DEATH_LINK_ACTIVE      = ROM_START + 0x17FFE9
MMX2_JAMMED_BUSTER_ACTIVE   = ROM_START + 0x17FFEA

EXCHANGE_RATE = 500000000

STARTING_ID = 0xBE0C00

MMX2_RECV_INDEX = MMX2_RAM + 0x00000

MMX2_ROMHASH_START = 0x7FC0
ROMHASH_SIZE = 0x15

X_Z_ITEMS = ["1up", "hp refill", "weapon refill"]

class MMX2SNIClient(SNIClient):
    game = "Mega Man X2"
    patch_suffix = ".apmmx2"

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

        validation = await snes_read(ctx, MMX2_VALIDATION_CHECK, 0x2)
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            return

        receiving_item = await snes_read(ctx, MMX2_RECEIVING_ITEM, 0x1)
        menu_state = await snes_read(ctx, MMX2_MENU_STATE, 0x1)
        gameplay_state = await snes_read(ctx, MMX2_GAMEPLAY_STATE, 0x1)
        can_move = await snes_read(ctx, MMX2_CAN_MOVE, 0x7)
        pause_state = await snes_read(ctx, MMX2_PAUSE_STATE, 0x1)
        screen_brightness = await snes_read(ctx, MMX2_SCREEN_BRIGHTNESS, 0x1)
        if menu_state[0] != 0x04 or \
            screen_brightness[0] != 0x0F or \
            gameplay_state[0] != 0x04 or \
            can_move != b'\x00\x00\x00\x00\x00\x00\x00' or \
            pause_state[0] != 0x00 or \
            receiving_item[0] != 0x00:
            return
        
        snes_buffered_write(ctx, MMX2_CURRENT_HP, bytearray([0x80]))
        snes_buffered_write(ctx, WRAM_START + 0x00A7B, bytearray([0x8C]))
        ram_0A7D = await snes_read(ctx, WRAM_START + 0x00A7D, 1)
        ram_0A7D = ram_0A7D[0] & 0x7F
        snes_buffered_write(ctx, WRAM_START + 0x00A7D, bytearray([ram_0A7D]))

        await snes_flush_writes(ctx)

        ctx.death_state = DeathState.dead
        ctx.last_death_link = time.time()


    async def validate_rom(self, ctx):
        from SNIClient import snes_read

        energy_link = await snes_read(ctx, MMX2_ENERGY_LINK_ENABLED, 0x1)
        rom_name = await snes_read(ctx, MMX2_ROMHASH_START, ROMHASH_SIZE)
        if rom_name is None or rom_name == bytes([0] * ROMHASH_SIZE) or rom_name[:4] != b"MMX2":
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
            if "refill" not in ctx.command_processor.commands:
                ctx.command_processor.commands["heal"] = cmd_heal
            if "refill" not in ctx.command_processor.commands:
                ctx.command_processor.commands["refill"] = cmd_refill
        if "trade" not in ctx.command_processor.commands:
            ctx.command_processor.commands["trade"] = cmd_trade
        if "resync" not in ctx.command_processor.commands:
            ctx.command_processor.commands["resync"] = cmd_resync

        death_link = await snes_read(ctx, MMX2_DEATH_LINK_ACTIVE, 1)
        if death_link[0]:
            await ctx.update_death_link(bool(death_link[0] & 0b1))

        ctx.rom = rom_name

        return True
    

    def on_package(self, ctx, cmd: str, args: dict):
        super().on_package(ctx, cmd, args)

        if cmd == "Connected":
            slot_data = args.get("slot_data", None)
            self.using_newer_client = True
            ctx.set_notify(f"mmx2_global_timer_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx2_deaths_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx2_damage_taken_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx2_damage_dealt_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx2_checkpoints_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx2_arsenal_{ctx.team}_{ctx.slot}")
            if slot_data["energy_link"]:
                ctx.set_notify(f"EnergyLink{ctx.team}")
                if ctx.ui:
                    ctx.ui.enable_energy_link()
                    ctx.ui.energy_link_label.text = "Energy: Standby"
                    logger.info(f"Initialized EnergyLink{ctx.team}, use /help to get information about the EnergyLink commands.")

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

        game_state = await snes_read(ctx, MMX2_GAME_STATE, 0x1)
        menu_state = await snes_read(ctx, MMX2_MENU_STATE, 0x1)
        gameplay_state = await snes_read(ctx, MMX2_GAMEPLAY_STATE, 0x1)

        # Discard uninitialized ROMs
        if menu_state is None:
            self.game_state = False
            self.energy_link_enabled = False
            self.current_level_value = 42
            self.item_queue = []
            return
    
        validation = await snes_read(ctx, MMX2_VALIDATION_CHECK, 0x2)
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            snes_logger.info(f'ROM not properly validated.')
            self.game_state = False
            return

        if game_state[0] == 0:
            self.game_state = False
            self.current_level_value = 42
            self.item_queue = []
            ctx.locations_checked = set()

            # Resync data if solicited 
            if self.resync_request:
                await ctx.send_msgs([{
                    "cmd": "Set", "key": f"mmx2_arsenal_{ctx.team}_{ctx.slot}", "operations":
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
            ctx.set_notify(f"mmx2_global_timer_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx2_deaths_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx2_damage_taken_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx2_damage_dealt_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx2_checkpoints_{ctx.team}_{ctx.slot}")
            ctx.set_notify(f"mmx2_arsenal_{ctx.team}_{ctx.slot}")

        if self.trade_request is not None:
            await self.handle_hp_trade(ctx)

        await self.handle_item_queue(ctx)

        # This is going to be rewritten whenever SNIClient supports on_package
        energy_link = await snes_read(ctx, MMX2_ENERGY_LINK_ENABLED, 0x1)
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

        from .Rom import weapon_rom_data, upgrades_rom_data, boss_access_rom_data, refill_rom_data
        from .Levels import location_id_to_level_id
        from worlds import AutoWorldRegister

        defeated_bosses = list(await snes_read(ctx, MMX2_DEFEATED_BOSSES, 0x20))
        cleared_levels = list(await snes_read(ctx, MMX2_LEVEL_CLEARED, 0x20))
        collected_heart_tanks_data = await snes_read(ctx, MMX2_COLLECTED_HEART_TANKS, 0x01)
        collected_upgrades_data = await snes_read(ctx, MMX2_COLLECTED_UPGRADES, 0x01)
        collected_shoryuken_data = await snes_read(ctx, MMX2_COLLECTED_SHORYUKEN, 0x01)
        collected_pickups_data = list(await snes_read(ctx, MMX2_COLLECTED_PICKUPS, 0x4E))
        collected_sigma_access = await snes_read(ctx, MMX2_COLLECTED_SIGMA_ACCESS, 0x01)
        pickupsanity_enabled = await snes_read(ctx, MMX2_PICKUPSANITY_ACTIVE, 0x1)
        new_checks = []
        for loc_name, data in location_id_to_level_id.items():
            loc_id = AutoWorldRegister.world_types[ctx.game].location_name_to_id[loc_name]
            if loc_id not in ctx.locations_checked:
                internal_id = data[1]
                data_bit = data[2]

                if internal_id == 0x000:
                    # Boss clear
                    if defeated_bosses[data_bit] != 0:
                        new_checks.append(loc_id)
                elif internal_id == 0x001:
                    # Maverick Medal
                    if cleared_levels[data_bit] != 0:
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
                    # Shoryuken
                    if collected_shoryuken_data[0] != 0x00:
                        new_checks.append(loc_id)
                elif internal_id == 0x006:
                    if collected_sigma_access[0] != 0x00:
                        new_checks.append(loc_id)
                elif internal_id == 0x007:
                    # Intro
                    if game_state[0] == 0x02 and \
                       menu_state[0] == 0x00 and \
                       gameplay_state[0] == 0x01:
                        new_checks.append(loc_id)
                elif internal_id == 0x020:
                    # Pickups
                    if not pickupsanity_enabled or pickupsanity_enabled[0] == 0:
                        continue
                    if collected_pickups_data[data_bit] != 0:
                        new_checks.append(loc_id)
        
        verify_game_state = await snes_read(ctx, MMX2_GAMEPLAY_STATE, 1)
        if verify_game_state is None:
            snes_logger.info(f'Exit Game.')
            return
        
        rom = await snes_read(ctx, MMX2_ROMHASH_START, ROMHASH_SIZE)
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
        current_level = int.from_bytes(await snes_read(ctx, MMX2_LEVEL_INDEX, 0x1), "little")

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
                        "key": f"mmx2_level_id_{ctx.team}_{ctx.slot}",
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

        recv_count = await snes_read(ctx, MMX2_RECV_INDEX, 2)
        if recv_count is None:
            # Add a small failsafe in case we get a None. Other SNI games do this...
            return

        recv_index = int.from_bytes(recv_count, "little")
        sync_arsenal = int.from_bytes(await snes_read(ctx, MMX2_ARSENAL_SYNC, 0x2), "little")

        if recv_index < len(ctx.items_received) and sync_arsenal != 0x1337:
            item = ctx.items_received[recv_index]
            recv_index += 1
            sending_game = ctx.slot_info[item.player].game
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_game(item.item), 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), recv_index, len(ctx.items_received)))
            
            snes_buffered_write(ctx, MMX2_RECV_INDEX, bytearray([recv_index]))
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
                boss_access = bytearray(await snes_read(ctx, MMX2_UNLOCKED_LEVELS, 0x20))
                level = boss_access_rom_data[item.item]
                boss_access[level[0] * 2] = 0x01
                snes_buffered_write(ctx, MMX2_UNLOCKED_LEVELS, boss_access)
                if item.item == STARTING_ID + 0x000A:
                    snes_buffered_write(ctx, MMX2_BASE_ACCESS, bytearray([0x00]))
                snes_buffered_write(ctx, MMX2_SFX_FLAG, bytearray([0x01]))
                snes_buffered_write(ctx, MMX2_SFX_NUMBER, bytearray([0x1D]))
                self.save_arsenal = True
                
            elif item.item in refill_rom_data:
                self.add_item_to_queue(refill_rom_data[item.item][0], item.item, refill_rom_data[item.item][1])
                self.save_arsenal = True

            elif item.item == STARTING_ID:
                # Handle goal
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True
                self.save_arsenal = True
                return
                
        # Handle collected locations
        game_state = await snes_read(ctx, MMX2_GAME_STATE, 0x1)
        if game_state[0] != 0x02:
            ctx.locations_checked = set()
            return
        new_boss_clears = False
        new_cleared_level = False
        new_heart_tank = False
        new_upgrade = False
        new_pickup = False
        new_shoryuken = False
        new_sigma_access = False
        cleared_levels = list(await snes_read(ctx, MMX2_LEVEL_CLEARED, 0x20))
        collected_pickups = list(await snes_read(ctx, MMX2_COLLECTED_PICKUPS, 0x4E))
        collected_heart_tanks_data = int.from_bytes(await snes_read(ctx, MMX2_COLLECTED_HEART_TANKS, 0x01))
        collected_upgrades_data = int.from_bytes(await snes_read(ctx, MMX2_COLLECTED_UPGRADES, 0x01))
        defeated_bosses = list(await snes_read(ctx, MMX2_DEFEATED_BOSSES, 0x20))
        collected_shoryuken_data = int.from_bytes(await snes_read(ctx, MMX2_COLLECTED_SHORYUKEN, 0x01))
        collected_sigma_access =  int.from_bytes(await snes_read(ctx, MMX2_COLLECTED_SIGMA_ACCESS, 0x01))
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
                    # Shoryuken
                    collected_shoryuken_data = 0xFF
                    new_shoryuken = True
                elif internal_id == 0x006:
                    # Sigma Access
                    collected_sigma_access = 0x01
                    new_sigma_access = True
                elif internal_id == 0x20:
                    # Pickups
                    collected_pickups[data_bit] = 0x01
                    new_pickup = True

        if new_cleared_level:
            snes_buffered_write(ctx, MMX2_LEVEL_CLEARED, bytes(cleared_levels))
        if new_boss_clears:
            snes_buffered_write(ctx, MMX2_DEFEATED_BOSSES, bytes(defeated_bosses))
        if new_pickup:
            snes_buffered_write(ctx, MMX2_COLLECTED_PICKUPS, bytes(collected_pickups))
        if new_shoryuken:
            snes_buffered_write(ctx, MMX2_COLLECTED_SHORYUKEN, bytearray([collected_shoryuken_data]))
        if new_sigma_access:
            snes_buffered_write(ctx, MMX2_COLLECTED_SIGMA_ACCESS, bytearray([collected_sigma_access]))
        if new_upgrade:
            snes_buffered_write(ctx, MMX2_COLLECTED_UPGRADES, bytearray([collected_upgrades_data]))
        if new_heart_tank:
            snes_buffered_write(ctx, MMX2_COLLECTED_HEART_TANKS, bytearray([collected_heart_tanks_data]))
        await snes_flush_writes(ctx)


    async def handle_hp_trade(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        validation = await snes_read(ctx, MMX2_VALIDATION_CHECK, 0x2)
        if validation is None:
            return
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            return

        # Can only process trades during the pause state
        menu_state = await snes_read(ctx, MMX2_MENU_STATE, 0x1)
        gameplay_state = await snes_read(ctx, MMX2_GAMEPLAY_STATE, 0x1)
        can_move = await snes_read(ctx, MMX2_CAN_MOVE, 0x7)
        if menu_state[0] != 0x04 or \
            gameplay_state[0] != 0x04 or \
            can_move != b'\x00\x00\x00\x00\x00\x00\x00':
            return
        
        pause_state = await snes_read(ctx, MMX2_PAUSE_STATE, 0x1)
        screen_brightness = await snes_read(ctx, MMX2_SCREEN_BRIGHTNESS, 0x1)
        if pause_state[0] == 0x00 or screen_brightness[0] != 0x0F:
            return

        for item in self.item_queue:
            if item[0] == "weapon refill":
                self.trade_request = None
                logger.info(f"You already have a Weapon Energy request pending to be received.")
                return

        # Can trade HP -> WPN if HP is above 1
        current_hp = await snes_read(ctx, MMX2_CURRENT_HP, 0x1)
        if current_hp[0] > 0x01:
            max_trade = current_hp[0] - 1
            set_trade = self.trade_request if self.trade_request <= max_trade else max_trade
            self.add_item_to_queue("weapon refill", None, set_trade)
            new_hp = current_hp[0] - set_trade
            snes_buffered_write(ctx, MMX2_CURRENT_HP, bytearray([new_hp]))
            await snes_flush_writes(ctx)
            self.trade_request = None
            logger.info(f"Traded {set_trade} HP for {set_trade} Weapon Energy.")
        else:
            logger.info("Couldn't process trade. HP is too low.")
        

    async def handle_energy_link(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        # Handle validation
        validation = await snes_read(ctx, MMX2_VALIDATION_CHECK, 0x2)
        if validation is None:
            return
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            return
        
        # Deposit heals into the pool regardless of energy_link setting
        energy_packet = await snes_read(ctx, MMX2_ENERGY_LINK_PACKET, 0x2)
        energy_packet_raw = energy_packet[0] | (energy_packet[1] << 8)
        energy_packet = (energy_packet_raw * EXCHANGE_RATE) >> 4
        if energy_packet != 0:
            await ctx.send_msgs([{
                "cmd": "Set", "key": f"EnergyLink{ctx.team}", "operations":
                    [{"operation": "add", "value": energy_packet},
                    {"operation": "max", "value": 0}],
            }])
            pool = ((ctx.stored_data[f'EnergyLink{ctx.team}'] or 0) / EXCHANGE_RATE) + (energy_packet_raw / 16)
            snes_buffered_write(ctx, MMX2_ENERGY_LINK_PACKET, bytearray([0x00, 0x00]))
            await snes_flush_writes(ctx)
        
        # Expose EnergyLink to the ROM
        pause_state = await snes_read(ctx, MMX2_PAUSE_STATE, 0x1)
        screen_brightness = await snes_read(ctx, MMX2_SCREEN_BRIGHTNESS, 0x1)
        if pause_state[0] != 0x00 or screen_brightness[0] == 0x0F:
            pool = ctx.stored_data[f'EnergyLink{ctx.team}'] or 0
            total_energy = int(pool / EXCHANGE_RATE)
            if total_energy < 9999:
                snes_buffered_write(ctx, MMX2_ENERGY_LINK_COUNT, bytearray([total_energy & 0xFF, (total_energy >> 8) & 0xFF]))
            else:
                snes_buffered_write(ctx, MMX2_ENERGY_LINK_COUNT, bytearray([0x0F, 0x27]))

        receiving_item = await snes_read(ctx, MMX2_RECEIVING_ITEM, 0x1)
        menu_state = await snes_read(ctx, MMX2_MENU_STATE, 0x1)
        gameplay_state = await snes_read(ctx, MMX2_GAMEPLAY_STATE, 0x1)
        can_move = await snes_read(ctx, MMX2_CAN_MOVE, 0x7)
        on_ride_armor = await snes_read(ctx, MMX2_ON_RIDE_ARMOR, 0x1)
        if menu_state[0] != 0x04 or \
            gameplay_state[0] != 0x04 or \
            can_move != b'\x00\x00\x00\x00\x00\x00\x00' or \
            on_ride_armor[0] == 0x0A or \
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
        if not skip_hp or not skip_weapon:
            # Handle in-game requests
            request = int.from_bytes(await snes_read(ctx, MMX2_REFILL_REQUEST, 0x1), "little")
            target = int.from_bytes(await snes_read(ctx, MMX2_REFILL_TARGET, 0x1), "little")
            if request != 0:
                if target == 0:
                    if self.heal_request_command is None:
                        self.heal_request_command = request
                else: 
                    if self.weapon_refill_request_command is None:
                        self.weapon_refill_request_command = request
                snes_buffered_write(ctx, MMX2_REFILL_REQUEST, bytearray([0x00]))

            # Handle heal requests
        if not skip_hp:
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
        from .Rom import weapon_rom_data, upgrades_rom_data

        if not hasattr(self, "item_queue") or len(self.item_queue) == 0:
            return

        validation = await snes_read(ctx, MMX2_VALIDATION_CHECK, 0x2)
        if validation is None:
            return
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            return

        # Do not give items if you can't move, are in pause state, not in the correct mode or not in gameplay state
        receiving_item = await snes_read(ctx, MMX2_RECEIVING_ITEM, 0x1)
        menu_state = await snes_read(ctx, MMX2_MENU_STATE, 0x1)
        gameplay_state = await snes_read(ctx, MMX2_GAMEPLAY_STATE, 0x1)
        hp_refill = await snes_read(ctx, MMX2_ENABLE_HP_REFILL, 0x1)
        weapon_refill = await snes_read(ctx, MMX2_ENABLE_WEAPON_REFILL, 0x1)
        can_move = await snes_read(ctx, MMX2_CAN_MOVE, 0x7)
        on_ride_armor = await snes_read(ctx, MMX2_ON_RIDE_ARMOR, 0x1)
        if menu_state[0] != 0x04 or \
           gameplay_state[0] != 0x04 or \
           hp_refill[0] != 0x00 or \
           weapon_refill[0] != 0x00 or \
           can_move != b'\x00\x00\x00\x00\x00\x00\x00' or \
           on_ride_armor[0] == 0x0A or \
           receiving_item[0] != 0x00:
            return
        
        next_item = self.item_queue[0]
        item_id = next_item[1]
        
        # Handle items that Zero can also get
        if next_item[0] in X_Z_ITEMS:
            backup_item = self.item_queue.pop(0)
            
            if next_item[0] == "hp refill":
                current_hp = await snes_read(ctx, MMX2_CURRENT_HP, 0x1)
                max_hp = await snes_read(ctx, MMX2_MAX_HP, 0x1)

                if current_hp[0] < max_hp[0]:
                    snes_buffered_write(ctx, MMX2_ENABLE_HP_REFILL, bytearray([0x02]))
                    snes_buffered_write(ctx, MMX2_HP_REFILL_AMOUNT, bytearray([next_item[2]]))
                    snes_buffered_write(ctx, MMX2_RECEIVING_ITEM, bytearray([0x01]))
                else:
                    # TODO: Sub Tank logic
                    self.item_queue.append(backup_item)
                    
            elif next_item[0] == "weapon refill":
                snes_buffered_write(ctx, MMX2_ENABLE_WEAPON_REFILL, bytearray([0x02]))
                snes_buffered_write(ctx, MMX2_WEAPON_REFILL_AMOUNT, bytearray([next_item[2]]))
                snes_buffered_write(ctx, MMX2_RECEIVING_ITEM, bytearray([0x01]))
                self.save_arsenal = True

            elif next_item[0] == "1up":
                life_count = await snes_read(ctx, MMX2_LIFE_COUNT, 0x1)
                if life_count[0] < 99:
                    snes_buffered_write(ctx, MMX2_ENABLE_GIVE_1UP, bytearray([0x01]))
                    snes_buffered_write(ctx, MMX2_RECEIVING_ITEM, bytearray([0x01]))
                    self.save_arsenal = True
                else:
                    self.item_queue.append(backup_item)

        pause_state = await snes_read(ctx, MMX2_PAUSE_STATE, 0x1)
        screen_brightness = await snes_read(ctx, MMX2_SCREEN_BRIGHTNESS, 0x1)
        if pause_state[0] != 0x00 or screen_brightness[0] != 0x0F:
            await snes_flush_writes(ctx)
            if len(self.item_queue) != 0:
                backup_item = self.item_queue.pop(0)
                self.item_queue.append(backup_item)
            return

        if next_item[0] == "weapon":
            weapon = weapon_rom_data[item_id]
            snes_buffered_write(ctx, WRAM_START + weapon[0], bytearray([weapon[1]]))
            snes_buffered_write(ctx, MMX2_SFX_FLAG, bytearray([0x01]))
            snes_buffered_write(ctx, MMX2_SFX_NUMBER, bytearray([0x16]))
            self.item_queue.pop(0)
            self.save_arsenal = True
            
        elif next_item[0] == "heart tank":
            heart_tanks = await snes_read(ctx, MMX2_HEART_TANKS, 0x1)
            heart_tanks = heart_tanks[0]
            heart_tank_count = heart_tanks.bit_count()
            if heart_tank_count < 8:
                heart_tanks |= 1 << heart_tank_count
                snes_buffered_write(ctx, MMX2_HEART_TANKS, bytearray([heart_tanks]))
                snes_buffered_write(ctx, MMX2_ENABLE_HEART_TANK, bytearray([0x02]))
                snes_buffered_write(ctx, MMX2_RECEIVING_ITEM, bytearray([0x01]))
            self.item_queue.pop(0)
            self.save_arsenal = True

        elif next_item[0] == "sub tank":
            upgrades = await snes_read(ctx, MMX2_UPGRADES, 0x1)
            sub_tanks = await snes_read(ctx, MMX2_SUB_TANK_ARRAY, 0x4)
            sub_tanks = list(sub_tanks)
            upgrade = upgrades[0]
            upgrade = upgrade & 0xF0
            sub_tank_count = upgrade.bit_count()
            if sub_tank_count < 4:
                upgrade = upgrades[0]
                upgrade |= 0x10 << sub_tank_count
                sub_tanks[sub_tank_count] = 0x8E
                snes_buffered_write(ctx, MMX2_UPGRADES, bytearray([upgrade]))
                snes_buffered_write(ctx, MMX2_SUB_TANK_ARRAY, bytearray(sub_tanks))
                snes_buffered_write(ctx, MMX2_SFX_FLAG, bytearray([0x01]))
                snes_buffered_write(ctx, MMX2_SFX_NUMBER, bytearray([0x17]))
            self.item_queue.pop(0)
            self.save_arsenal = True
        
        elif next_item[0] == "upgrade":
            upgrades = await snes_read(ctx, MMX2_UPGRADES, 0x1)

            upgrade = upgrades_rom_data[item_id]
            bit = 1 << upgrade[0]
            check = upgrades[0] & bit

            if check == 0:
                # Armor
                upgrades = upgrades[0]
                upgrades |= bit
                if bit == 0x01:
                    snes_buffered_write(ctx, WRAM_START + 0x09EE, bytearray([0x18]))
                    snes_buffered_write(ctx, WRAM_START + 0x1FCD, bytearray([0xFF]))
                    snes_buffered_write(ctx, MMX2_UPGRADES, bytearray([upgrades]))
                    snes_buffered_write(ctx, MMX2_UNLOCKED_CHECKPOINTS, bytearray([0x80]))
                elif bit == 0x02:
                    jam_check = await snes_read(ctx, MMX2_JAMMED_BUSTER_ACTIVE, 0x1)
                    charge_shot_unlocked = await snes_read(ctx, MMX2_UNLOCKED_CHARGED_SHOT, 0x1)
                    if jam_check[0] == 1 and charge_shot_unlocked[0] == 0:
                        snes_buffered_write(ctx, MMX2_UNLOCKED_CHARGED_SHOT, bytearray([0x01]))
                    else:
                        value = await snes_read(ctx, WRAM_START + 0x0AE8, 0x1)
                        snes_buffered_write(ctx, WRAM_START + 0x0AE8, bytearray([value[0] + 1]))
                        snes_buffered_write(ctx, WRAM_START + 0x0AF2, bytearray([0x00]))
                        snes_buffered_write(ctx, WRAM_START + 0x0AF3, bytearray([0x00]))
                        snes_buffered_write(ctx, WRAM_START + 0x0AE9, bytearray([0x00]))
                        snes_buffered_write(ctx, WRAM_START + 0x0AF8, bytearray([0x5D]))
                        snes_buffered_write(ctx, MMX2_UPGRADES, bytearray([upgrades]))
                elif bit == 0x04:
                    value = await snes_read(ctx, WRAM_START + 0x0B08, 0x1)
                    snes_buffered_write(ctx, WRAM_START + 0x0B08, bytearray([value[0] + 1]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B12, bytearray([0x00]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B13, bytearray([0x01]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B09, bytearray([0x00]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B18, bytearray([0x5D]))
                    snes_buffered_write(ctx, WRAM_START + 0x1FCB, bytearray([0xFF]))
                    snes_buffered_write(ctx, MMX2_UPGRADES, bytearray([upgrades]))
                elif bit == 0x08:
                    value = await snes_read(ctx, WRAM_START + 0x0B28, 0x1)
                    snes_buffered_write(ctx, WRAM_START + 0x0B28, bytearray([value[0] + 1]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B32, bytearray([0x00]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B33, bytearray([0x02]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B29, bytearray([0x00]))
                    snes_buffered_write(ctx, WRAM_START + 0x0B38, bytearray([0x5D]))
                    snes_buffered_write(ctx, MMX2_UPGRADES, bytearray([upgrades]))
                snes_buffered_write(ctx, MMX2_SFX_FLAG, bytearray([0x01]))
                snes_buffered_write(ctx, MMX2_SFX_NUMBER, bytearray([0x1B]))
            self.item_queue.pop(0)
            self.save_arsenal = True

        await snes_flush_writes(ctx)


    async def handle_data_storage(self, ctx):
        from SNIClient import snes_read, snes_buffered_write, snes_flush_writes
        # Only do arsenal after the map's initial load
        menu_state = int.from_bytes(await snes_read(ctx, MMX2_MENU_STATE, 0x1))
        gameplay_state = int.from_bytes(await snes_read(ctx, MMX2_GAMEPLAY_STATE, 0x1))
        map_state = int.from_bytes(await snes_read(ctx, WRAM_START + 0x1E59, 0x1))
        sync_arsenal = int.from_bytes(await snes_read(ctx, MMX2_ARSENAL_SYNC, 0x2), "little")
        if (menu_state == 0x00 and map_state == 0x0A) or (menu_state == 0x04 and gameplay_state == 0x04):
            # Load Arsenal
            if sync_arsenal == 0x1337:
                arsenal = ctx.stored_data[f"mmx2_arsenal_{ctx.team}_{ctx.slot}"] or dict()
                if arsenal:
                    # Data in arsenal
                    snes_buffered_write(ctx, MMX2_RECV_INDEX, bytes(arsenal["recv_index"].to_bytes(2, 'little')))
                    snes_buffered_write(ctx, MMX2_LIFE_COUNT, bytes(arsenal["life_count"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX2_UPGRADES, bytes(arsenal["upgrades"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX2_MAX_HP, bytes(arsenal["max_hp"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX2_HEART_TANKS, bytes(arsenal["heart_tanks"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX2_SUB_TANK_ARRAY, bytearray(arsenal["sub_tanks"]))
                    snes_buffered_write(ctx, MMX2_UNLOCKED_CHARGED_SHOT, bytes(arsenal["unlocked_buster"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX2_WEAPON_ARRAY, bytearray(arsenal["weapons"]))
                    snes_buffered_write(ctx, MMX2_SHORYUKEN, bytes(arsenal["shoryuken"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX2_UNLOCKED_LEVELS, bytearray(arsenal["levels"]))
                    snes_buffered_write(ctx, MMX2_BASE_ACCESS, bytes(arsenal["base_access"].to_bytes(1, 'little')))
                    snes_buffered_write(ctx, MMX2_COLLECTED_SIGMA_ACCESS, bytes(arsenal["sigma_access"].to_bytes(1, 'little')))

                snes_buffered_write(ctx, MMX2_ARSENAL_SYNC, bytearray([0x00,0x00]))
                await snes_flush_writes(ctx)

        # Save Arsenal
        if self.save_arsenal and sync_arsenal != 0x1337:
            arsenal = dict()
            arsenal["recv_index"] = int.from_bytes(await snes_read(ctx, MMX2_RECV_INDEX, 0x2), "little")
            arsenal["life_count"] = int.from_bytes(await snes_read(ctx, MMX2_LIFE_COUNT, 0x1), "little")
            arsenal["upgrades"] = int.from_bytes(await snes_read(ctx, MMX2_UPGRADES, 0x1), "little")
            arsenal["max_hp"] = int.from_bytes(await snes_read(ctx, MMX2_MAX_HP, 0x1), "little")
            arsenal["heart_tanks"] = int.from_bytes(await snes_read(ctx, MMX2_HEART_TANKS, 0x1), "little")
            arsenal["sub_tanks"] = list(await snes_read(ctx, MMX2_SUB_TANK_ARRAY, 0x4))
            arsenal["unlocked_buster"] = int.from_bytes(await snes_read(ctx, MMX2_UNLOCKED_CHARGED_SHOT, 0x1), "little")
            arsenal["weapons"] = list(await snes_read(ctx, MMX2_WEAPON_ARRAY, 0x10))
            arsenal["shoryuken"] = int.from_bytes(await snes_read(ctx, MMX2_SHORYUKEN, 0x1), "little")
            arsenal["levels"] = list(await snes_read(ctx, MMX2_UNLOCKED_LEVELS, 0x20))
            arsenal["base_access"] = int.from_bytes(await snes_read(ctx, MMX2_BASE_ACCESS, 0x1), "little")
            arsenal["sigma_access"] = int.from_bytes(await snes_read(ctx, MMX2_COLLECTED_SIGMA_ACCESS, 0x1), "little")
            
            # Attempt to not lose any previously saved data in case of RAM corruption
            saved_arsenal = ctx.stored_data[f"mmx2_arsenal_{ctx.team}_{ctx.slot}"] or dict()
            if saved_arsenal:
                if saved_arsenal["recv_index"] > arsenal["recv_index"]:
                    arsenal["recv_index"] = saved_arsenal["recv_index"]
                if saved_arsenal["life_count"] > arsenal["life_count"]:
                    arsenal["life_count"] = saved_arsenal["life_count"]
                if saved_arsenal["max_hp"] > arsenal["max_hp"]:
                    arsenal["max_hp"] = saved_arsenal["max_hp"]
                for i in range(0x10):
                    arsenal["weapons"][i] |= saved_arsenal["weapons"][i] & 0x40
                for level in range(0x20):
                    arsenal["levels"][level] |= saved_arsenal["levels"][level]
                arsenal["base_access"] = min(saved_arsenal["base_access"], arsenal["base_access"])
                arsenal["sigma_access"] = min(saved_arsenal["sigma_access"], arsenal["sigma_access"])
                    
                arsenal["upgrades"] |= saved_arsenal["upgrades"]
                arsenal["unlocked_buster"] |= saved_arsenal["unlocked_buster"]
                arsenal["shoryuken"] |= saved_arsenal["shoryuken"] & 0xE0
                arsenal["heart_tanks"] |= saved_arsenal["heart_tanks"]
                for i in range(0x4):
                    arsenal["sub_tanks"][i] |= saved_arsenal["sub_tanks"][i] & 0x80

            await ctx.send_msgs([{
                "cmd": "Set", "key": f"mmx2_arsenal_{ctx.team}_{ctx.slot}", "operations":
                    [{"operation": "replace", "value": arsenal}],
            }])
            self.save_arsenal = False

        keys = {
            f"mmx2_checkpoints_{ctx.team}_{ctx.slot}",
            f"mmx2_global_timer_{ctx.team}_{ctx.slot}",
            f"mmx2_deaths_{ctx.team}_{ctx.slot}",
            f"mmx2_damage_dealt_{ctx.team}_{ctx.slot}",
            f"mmx2_damage_taken_{ctx.team}_{ctx.slot}",
        }
        if not all(key in ctx.stored_data.keys() for key in keys):
            return

        # Checkpoints reached
        checkpoints = list(await snes_read(ctx, MMX2_CHECKPOINTS_REACHED, 0xF))
        data_storage_checkpoints = ctx.stored_data[f"mmx2_checkpoints_{ctx.team}_{ctx.slot}"] or [0 for _ in range(0xF)]
        computed_checkpoints = list()
        for i in range(0xF):
            if checkpoints[i] >= data_storage_checkpoints[i]:
                computed_checkpoints.append(checkpoints[i])
            else:
                computed_checkpoints.append(data_storage_checkpoints[i])
        await ctx.send_msgs([{
            "cmd": "Set", "key": f"mmx2_checkpoints_{ctx.team}_{ctx.slot}", "operations":
                [{"operation": "replace", "value": computed_checkpoints}],
        }])
        snes_buffered_write(ctx, MMX2_CHECKPOINTS_REACHED, bytes(computed_checkpoints))

        # Global timer
        timer = int.from_bytes(await snes_read(ctx, MMX2_GLOBAL_TIMER, 0x4), "little")
        data_storage_timer = ctx.stored_data[f"mmx2_global_timer_{ctx.team}_{ctx.slot}"] or 0
        if timer >= data_storage_timer:
            await ctx.send_msgs([{
                "cmd": "Set", "key": f"mmx2_global_timer_{ctx.team}_{ctx.slot}", "operations":
                    [{"operation": "replace", "value": timer},
                        {"operation": "min", "value": 0x03E73B3B}],
            }])
        else:
            snes_buffered_write(ctx, MMX2_GLOBAL_TIMER, data_storage_timer.to_bytes(4, "little"))

        # Death count
        deaths = int.from_bytes(await snes_read(ctx, MMX2_GLOBAL_DEATHS, 0x2), "little")
        data_storage_deaths = ctx.stored_data[f"mmx2_deaths_{ctx.team}_{ctx.slot}"] or 0
        if deaths >= data_storage_deaths:
            await ctx.send_msgs([{
                "cmd": "Set", "key": f"mmx2_deaths_{ctx.team}_{ctx.slot}", "operations":
                    [{"operation": "replace", "value": deaths},
                        {"operation": "min", "value": 9999}],
            }])
        else:
            snes_buffered_write(ctx, MMX2_GLOBAL_DEATHS, data_storage_deaths.to_bytes(2, "little"))

        # Damage dealt
        dmg_dealt = int.from_bytes(await snes_read(ctx, MMX2_GLOBAL_DMG_DEALT, 0x2), "little")
        data_storage_dmg_dealt = ctx.stored_data[f"mmx2_damage_dealt_{ctx.team}_{ctx.slot}"] or 0
        if dmg_dealt >= data_storage_dmg_dealt:
            await ctx.send_msgs([{
                "cmd": "Set", "key": f"mmx2_damage_dealt_{ctx.team}_{ctx.slot}", "operations":
                    [{"operation": "replace", "value": dmg_dealt},
                        {"operation": "min", "value": 9999}],
            }])
        else:
            snes_buffered_write(ctx, MMX2_GLOBAL_DMG_DEALT, data_storage_dmg_dealt.to_bytes(2, "little"))
        
        # Damage taken
        dmg_taken = int.from_bytes(await snes_read(ctx, MMX2_GLOBAL_DMG_TAKEN, 0x2), "little")
        data_storage_dmg_taken = ctx.stored_data[f"mmx2_damage_taken_{ctx.team}_{ctx.slot}"] or 0
        if dmg_taken >= data_storage_dmg_taken:
            await ctx.send_msgs([{
                "cmd": "Set", "key": f"mmx2_damage_taken_{ctx.team}_{ctx.slot}", "operations":
                    [{"operation": "replace", "value": dmg_taken},
                        {"operation": "min", "value": 9999}],
            }])
        else:
            snes_buffered_write(ctx, MMX2_GLOBAL_DMG_TAKEN, data_storage_dmg_taken.to_bytes(2, "little"))
        
        await snes_flush_writes(ctx)


def cmd_heal(self, amount: str = ""):
    """
    Request healing from EnergyLink.
    """
    if self.ctx.game != "Mega Man X2":
        logger.warning("This command can only be used while playing Mega Man X2")
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
    if self.ctx.game != "Mega Man X2":
        logger.warning("This command can only be used while playing Mega Man X2")
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
    if self.ctx.game != "Mega Man X2":
        logger.warning("This command can only be used while playing Mega Man X2")
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
    if self.ctx.game != "Mega Man X2":
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
