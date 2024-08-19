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
MMX_UNLOCKED_AIR_DASH       = WRAM_START + 0x1EE22

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
MMX_ABILITIES_FLAGS        = ROM_START + 0x17FFF1

EXCHANGE_RATE = 500000000

STARTING_ID = 0xBE0800

MMX_ROMHASH_START = 0x7FC0
ROMHASH_SIZE = 0x15

class DKC2SNIClient(SNIClient):
    game = "Donkey Kong Country 2"
    patch_suffix = ".apdkc2"

    def __init__(self):
        super().__init__()
        self.game_state = False


    async def deathlink_kill_player(self, ctx):
        from SNIClient import DeathState, snes_buffered_write, snes_flush_writes, snes_read

        await snes_flush_writes(ctx)

        ctx.death_state = DeathState.dead
        ctx.last_death_link = time.time()


    async def validate_rom(self, ctx):
        from SNIClient import snes_read

        energy_link = await snes_read(ctx, MMX_ENERGY_LINK_ENABLED, 0x1)
        rom_name = await snes_read(ctx, MMX_ROMHASH_START, ROMHASH_SIZE)
        if rom_name is None or rom_name == bytes([0] * ROMHASH_SIZE) or rom_name[:4] != b"DKC2":
            return False
        
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.receive_option = 0
        ctx.send_option = 0
        ctx.allow_collect = True

        death_link = await snes_read(ctx, MMX_DEATH_LINK_ACTIVE, 1)
        if death_link[0]:
            await ctx.update_death_link(bool(death_link[0] & 0b1))

        ctx.rom = rom_name

        return True
     

    async def game_watcher(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        game_state = await snes_read(ctx, MMX_GAME_STATE, 0x1)
        menu_state = await snes_read(ctx, MMX_MENU_STATE, 0x1)
        # Discard uninitialized ROMs
        if menu_state is None:
            self.game_state = False
            return
    
        if game_state[0] == 0:
            self.game_state = False
            return
        
        validation = await snes_read(ctx, MMX_VALIDATION_CHECK, 0x2)
        validation = validation[0] | (validation[1] << 8)
        if validation != 0xDEAD:
            snes_logger.info(f'ROM not properly validated.')
            self.game_state = False
            return

        from .Levels import location_id_to_level_id
        from worlds import AutoWorldRegister

        new_checks = []
        for loc_name, data in location_id_to_level_id.items():
            loc_id = AutoWorldRegister.world_types[ctx.game].location_name_to_id[loc_name]
            if loc_id not in ctx.locations_checked:
                pass
 
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
            location = ctx.location_names.lookup_in_game(new_check_id)
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
            sending_game = ctx.slot_info[item.player].game
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_game(item.item), 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), recv_index, len(ctx.items_received)))
            
            snes_buffered_write(ctx, MMX_RECV_INDEX, bytes([recv_index]))
            await snes_flush_writes(ctx)
            
            if item.item in 0x0:
                pass
                
        # Handle collected locations
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


    def on_package(self, ctx, cmd: str, args: dict):
        super().on_package(ctx, cmd, args)
        pass