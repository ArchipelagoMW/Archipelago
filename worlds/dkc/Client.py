import logging
import time
import random

from enum import Enum
from NetUtils import ClientStatus, NetworkItem, color
from worlds.AutoSNIClient import SNIClient, SnesReader, SnesData, Read
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

STARTING_ID = 0xBF1000

DKC_STAGE_FLAGS = WRAM_START + 0x0583
DKC_SANITY_FLAGS = WRAM_START + 0x1F800

DKC_SRAM = SRAM_START + 0x600
DKC_RECV_INDEX = DKC_SRAM + 0x01C
DKC_PLAY_SFX = DKC_SRAM + 0x026
DKC_DEATH_LINK_FLAG = DKC_SRAM + 0x064
DKC_BARRELS = DKC_SRAM + 0x024
DKC_ENERGY_LINK_TRANSFER = DKC_SRAM + 0x020

DKC_EXCHANGE_RATE = 200000000
DK_BARREL_BANANA_COST = 20

DKC_ROMHASH_START = 0xFFC0
ROMHASH_SIZE = 0x15

UNCOLLECTABLE_LEVELS = []

class RAM(Enum):
    settings = Read(ROM_START + 0x3BF790, 0x40)
    recv_index = Read(DKC_RECV_INDEX, 0x02)
    nmi_pointer = Read(WRAM_START + 0x001C, 0x02)
    in_map = Read(WRAM_START + 0x0527, 0x01)
    current_level = Read(WRAM_START + 0x0563, 0x01)
    loaded_level = Read(WRAM_START + 0x003E, 0x01)
    brightness = Read(WRAM_START + 0x051A, 0x01)
    kong_letters = Read(WRAM_START + 0x057F, 0x01)
    stage_flags = Read(DKC_STAGE_FLAGS, 0x100)
    sanity_flags = Read(DKC_SANITY_FLAGS, 0x100)
    backup_barrels = Read(DKC_BARRELS, 0x02)
    energy_link_packet = Read(DKC_ENERGY_LINK_TRANSFER, 0x02)
    death_flag = Read(WRAM_START + 0x1F780, 0x02)
    death_link_flag = Read(DKC_SRAM + 0x064, 0x02)

class ValidationRAM(Enum):
    settings = Read(ROM_START + 0x3BF790, 0x40)
    rom_name = Read(DKC_ROMHASH_START, ROMHASH_SIZE)

class DKCSNIClient(SNIClient):
    game = "Donkey Kong Country"
    patch_suffix = ".apdkc"
    slot_data: dict
    memory = SnesReader(RAM)
    validation = SnesReader(ValidationRAM)

    def __init__(self):
        super().__init__()
        self.game_state = False
        self.energy_link_enabled = False
        self.received_trap_link = False
        self.barrel_request = ""
        self.barrel_count = ""
        self.current_map = 0
        self.barrel_label = None

    async def validate_rom(self, ctx: "SNIContext"):
        dkc_data = await self.validation.read(ctx)
        if dkc_data is None:
            if "request" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("request")
            return False
        
        rom_name = dkc_data.get(ValidationRAM.rom_name)
        
        if rom_name == bytes([0] * ROMHASH_SIZE) or rom_name[:4] != b"DKC1":
            if "request" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("request")
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.receive_option = 0
        ctx.send_option = 0
        ctx.allow_collect = True

        update_tags = False

        settings = dkc_data.get(ValidationRAM.settings)
        energy_link = settings[0x18]
        if energy_link and "EnergyLink" not in ctx.tags:
            ctx.tags.add("EnergyLink")
            update_tags = True
            if "request" not in ctx.command_processor.commands:
                ctx.command_processor.commands["request"] = cmd_request

        trap_link = settings[0x19]
        if trap_link and "TrapLink" not in ctx.tags:
            ctx.tags.add("TrapLink")
            update_tags = True

        death_link = settings[0x1A]
        if death_link:
            await ctx.update_death_link(True)

        if update_tags:
            await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}])

        ctx.rom = rom_name

        return True


    async def game_watcher(self, ctx: "SNIContext"):
        if not ctx.server or ctx.server.socket.closed or ctx.slot is None:
            return

        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        dkc_ram = await self.memory.read(ctx)
        if dkc_ram is None:
            self.game_state = False
            return

        # Mark valid game state after we set foot into the map
        nmi_pointer = int.from_bytes(dkc_ram.get(RAM.nmi_pointer), "little")
        if nmi_pointer == 0xE6B1:
            self.game_state = True
            
        if not self.game_state:
            self.current_map = 0
            return

        from .Levels import location_id_to_level_id
        from worlds import AutoWorldRegister

        new_checks = []
        current_level = int.from_bytes(dkc_ram.get(RAM.current_level), "little")
        loaded_level = int.from_bytes(dkc_ram.get(RAM.loaded_level), "little")
        brightness = int.from_bytes(dkc_ram.get(RAM.brightness), "little")
        level_flags = bytearray(dkc_ram.get(RAM.stage_flags))
        sanity_flags = bytearray(dkc_ram.get(RAM.sanity_flags))
        dkc_settings = dkc_ram.get(RAM.settings)
        kong_flags = int.from_bytes(dkc_ram.get(RAM.kong_letters), "little")

        # Fix Reptile Rumble having two different IDs
        if current_level == 0xEA:
            current_level = 0x01

        kong_as_checks = dkc_settings[0x21]
        tokens_as_checks = dkc_settings[0x22]
        balloons_as_checks = dkc_settings[0x23]
        bunches_as_checks = dkc_settings[0x24]

        for loc_name, data in location_id_to_level_id.items():
            # Do not process locations if in a map or a transition
            if nmi_pointer == 0xE6B1 or brightness & 0x0F != 0x0F:
                break 
            loc_id = AutoWorldRegister.world_types[ctx.game].location_name_to_id[loc_name]
            if loc_id not in ctx.locations_checked:
                loc_type = data[0]
                level_num = data[1]

                if loc_type == 0x00:
                    # Level clear
                    if level_flags[level_num] & 0x01:
                        new_checks.append(loc_id)
                elif loc_type == 0x01 and kong_as_checks:
                    # KONG
                    if level_num == current_level and kong_flags & 0x10 == 0x10:
                        new_checks.append(loc_id)
                elif loc_type == 0x02:
                    # Bonus
                    bonus_mask = data[2]
                    if level_flags[level_num] & bonus_mask:
                        new_checks.append(loc_id)
                elif loc_type == 0x03 and tokens_as_checks:
                    # Tokens
                    flag = sanity_flags[data[2]]
                    if level_num == current_level and flag & 0x04 == 0x04:
                        new_checks.append(loc_id)
                elif loc_type == 0x04 and balloons_as_checks:
                    # Balloons
                    flag = sanity_flags[data[2]]
                    if level_num == current_level and flag & 0x01 == 0x01:
                        new_checks.append(loc_id)
                elif loc_type == 0x05 and bunches_as_checks:
                    # Bunches
                    flag = sanity_flags[data[2]]
                    if level_num == current_level and flag & 0x02 == 0x02:
                        new_checks.append(loc_id)

        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names.lookup_in_game(new_check_id)
            snes_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])

        # Trigger goal
        if loaded_level == 0x004C:
            if not ctx.finished_game:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True
                return

        if "EnergyLink" in ctx.tags:
            await self.handle_energy_link(ctx, dkc_ram)

        if "TrapLink" in ctx.tags:
            await self.handle_trap_link(ctx)

        # Only handle death link during levels, at full brightness and if we're not dead
        death_flag = int.from_bytes(dkc_ram.get(RAM.death_flag), "little")
        if "DeathLink" in ctx.tags and ctx.last_death_link + 1 < time.time():
            currently_dead = death_flag != 0 and nmi_pointer != 0xE6B1 and brightness & 0x0F == 0x0F
            await ctx.handle_deathlink_state(currently_dead)
            
        # Add a label that shows how many Barrels are left
        await self.handle_barrel_label(ctx, dkc_ram)

        # Send current map to poptracker
        if self.current_map != loaded_level:
            self.current_map = loaded_level
            await ctx.send_msgs([{
                "cmd": "Set", 
                "key": f"dkc2_current_map_{ctx.team}_{ctx.slot}", 
                "default": 0,
                "want_reply": False,
                "operations":
                    [{"operation": "replace", "value": self.current_map}],
            }])

        # Receive items
        # Only receive items if we're at full brightness
        if brightness & 0x0F == 0x0F:
            from .Rom import unlock_data, currency_data, trap_data
            recv_index = int.from_bytes(dkc_ram.get(RAM.recv_index), "little")

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
                    count = await snes_read(ctx, DKC_SRAM + offset, 0x02)
                    if count is None:
                        recv_index -= 1
                        return
                    count = int.from_bytes(count, "little")
                    if item.item == STARTING_ID + 0x0010:
                        count |= 0x0001
                    else:
                        count |= 0x0002
                    count &= 0x00FF
                    snes_buffered_write(ctx, DKC_SRAM + offset, bytes([count]))

                # Give items
                elif item.item in unlock_data:
                    offset = unlock_data[item.item][0]
                    sfx = unlock_data[item.item][1]
                    snes_buffered_write(ctx, DKC_SRAM + offset, bytearray([0x01]))
                
                # Give currency-like items
                elif item.item in currency_data:
                    offset = currency_data[item.item][0]
                    if offset & 0x8000 == 0x8000:
                        addr = DKC_SRAM + (offset & 0x7FFF)
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
                    traps = await snes_read(ctx, DKC_SRAM + offset, 0x02)
                    if traps is None:
                        recv_index -= 1
                        return
                    traps = min(int.from_bytes(traps, "little") + 1, 150)
                    snes_buffered_write(ctx, DKC_SRAM + offset, bytes([traps]))
                    if "TrapLink" in ctx.tags and item.item in trap_value_to_name and ctx.slot is not None:
                        await self.send_trap_link(ctx, trap_value_to_name[item.item])

                if sfx:
                    snes_buffered_write(ctx, DKC_PLAY_SFX, bytearray([sfx, 0x80]))
                    
                snes_buffered_write(ctx, DKC_RECV_INDEX, recv_index.to_bytes(2, "little"))

                await snes_flush_writes(ctx)
                
        # Handle collected locations
        if nmi_pointer == 0xE6B1:
            level_data_updated = False
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

                    if loc_type == 0x00:
                        # Level clear
                        level_flags[level_num] |= 0x01
                        level_data_updated = True
                    elif loc_type == 0x02:
                        # Bonus
                        bonus_mask = data[2]
                        level_flags[level_num] |= bonus_mask
                        level_data_updated = True

            if level_data_updated:
                snes_buffered_write(ctx, DKC_STAGE_FLAGS, bytearray(level_flags))


    async def deathlink_kill_player(self, ctx: "SNIContext"):
        from SNIClient import DeathState, snes_buffered_write, snes_flush_writes

        dkc_ram = await self.memory.read(ctx)
        if dkc_ram is None:
            return

        death_link_flag = int.from_bytes(dkc_ram.get(RAM.death_link_flag),"little")
        nmi_pointer = int.from_bytes(dkc_ram.get(RAM.nmi_pointer), "little")
        brightness = int.from_bytes(dkc_ram.get(RAM.brightness), "little")

        # skip death link if already dead, in map or without full brightness
        if death_link_flag or nmi_pointer == 0xE6B1 or brightness & 0x0F != 0x0F:
            return

        snes_buffered_write(ctx, DKC_DEATH_LINK_FLAG, bytes([0x01]))
        await snes_flush_writes(ctx)

        ctx.death_state = DeathState.dead
        ctx.last_death_link = time.time()


    async def handle_energy_link(self, ctx: "SNIContext", dkc_ram: SnesData[RAM]):
        from SNIClient import snes_buffered_write, snes_flush_writes

        # Deposits EnergyLink into pool
        energy_packet = int.from_bytes(dkc_ram.get(RAM.energy_link_packet), "little")
        energy_packet = int(energy_packet * DKC_EXCHANGE_RATE / 10) >> 4
        if energy_packet != 0:
            await ctx.send_msgs([{
                "cmd": "Set", 
                "key": f"EnergyLink{ctx.team}", 
                "slot": ctx.slot,
                "default": 0,
                "operations":
                    [{"operation": "add", "value": energy_packet}],
            }])
            snes_buffered_write(ctx, DKC_ENERGY_LINK_TRANSFER, bytearray([0x00, 0x00]))

        barrels = int.from_bytes(dkc_ram.get(RAM.backup_barrels), "little")
        if self.barrel_request == "place_request":
            self.barrel_request_tag = f"dkc1-dkbarrel-{ctx.team}-{ctx.slot}-{random.randint(0, 0xFFFFFFFF)}"
            value = DK_BARREL_BANANA_COST * DKC_EXCHANGE_RATE * self.barrel_count
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
            barrels += self.barrel_count
            barrels &= 0x0FFF
            snes_buffered_write(ctx, DKC_BARRELS, bytes([barrels]))
            self.barrel_request = ""
            self.barrel_count = 0
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
            logger.info(f"Not enough bananas to summon a barrel! You need at least {DK_BARREL_BANANA_COST * self.barrel_count} bananas.")
            self.barrel_count = 0

        await snes_flush_writes(ctx)

    async def handle_barrel_label(self, ctx: "SNIContext", dkc_ram: SnesData[RAM]):
        from kvui import MDLabel as Label

        if not self.barrel_label:
            self.barrel_label = Label(text=f"", size_hint_x=None, width=120, halign="center")
            ctx.ui.connect_layout.add_widget(self.barrel_label)

        barrels = int.from_bytes(dkc_ram.get(RAM.backup_barrels), "little")
        self.barrel_label.text = f"Barrels: {barrels}"

    async def handle_trap_link(self, ctx: "SNIContext"):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        from .Rom import trap_data
        
        if self.received_trap_link:
            trap = self.received_trap_link

            offset = trap_data[trap.item][0]
            traps = await snes_read(ctx, DKC_SRAM + offset, 0x02)
            if traps is None:
                return
            traps = (int.from_bytes(traps, "little") + 1) & 0xFFF
            snes_buffered_write(ctx, DKC_SRAM + offset, bytes([traps]))
            self.received_trap_link = None
            
            await snes_flush_writes(ctx)

    async def send_trap_link(self, ctx: "SNIContext", trap_name: str):
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
                    dk_barrel_cost = DKC_EXCHANGE_RATE * DK_BARREL_BANANA_COST * self.barrel_count
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
                pool = (value or 0) /  DKC_EXCHANGE_RATE
                ctx.ui.energy_link_label.text = f"Bananas: {float(pool):.2f}"

        elif cmd == "Retrieved":
            if f"EnergyLink{ctx.team}" in args["keys"] and args["keys"][f"EnergyLink{ctx.team}"] and ctx.ui:
                pool = (args["keys"][f"EnergyLink{ctx.team}"] or 0) / DKC_EXCHANGE_RATE
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
        
def cmd_request(self, amount: str = ""):
    """
    Request a DK Barrel from the banana pool (EnergyLink).
    """
    if self.ctx.game != "Donkey Kong Country":
        logger.warning("This command can only be used while playing Donkey Kong Country")
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.info(f"Must be connected to server and in game.")
    else:
        if amount:
            try:
                amount = int(amount)
            except ValueError:
                logger.info(f"Please specify a valid number.")
                return
            if amount <= 0:
                logger.info(f"Please specify a number higher than 0.")
                return
            if self.ctx.client_handler.barrel_request != "":
                logger.info(f"You already have a DK Barrel in queue.")
                return
            else:
                self.ctx.client_handler.barrel_request = "place_request"
                self.ctx.client_handler.barrel_count = amount
                logger.info(f"Placing a DK barrel request...")
        else:
            logger.info(f"You need to specify how many Barrels you will request.")