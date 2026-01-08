import logging
import time
import random

from NetUtils import ClientStatus, NetworkItem, color
from worlds.AutoSNIClient import SNIClient
from .Items import trap_value_to_name, trap_name_to_value

logger = logging.getLogger("Client")
snes_logger = logging.getLogger("SNES")

# FXPAK Pro protocol memory mapping used by SNI
ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

STARTING_ID = 0xBF1000

DKC_SETTINGS = ROM_START + 0x3BF790

DKC2_EFFECT_BUFFER = WRAM_START + 0x0619
DKC2_SOUND_BUFFER = WRAM_START + 0x0622
DKC2_SPC_NEXT_INDEX = WRAM_START + 0x0634
DKC2_SPC_INDEX = WRAM_START + 0x0632
DKC2_SPC_CHANNEL_BUSY = WRAM_START + 0x0621

DKC_SRAM = SRAM_START + 0x600
DKC_RECV_INDEX = DKC_SRAM + 0x01C

DKC_IN_MAP = WRAM_START + 0x0527
DKC_CURRENT_LEVEL = WRAM_START + 0x0563
DKC_LOADED_LEVEL = WRAM_START + 0x003E

DKC_PLAY_SFX = DKC_SRAM + 0x026

DKC_BRIGHTNESS = WRAM_START + 0x051A

DKC_KONG_LETTERS = WRAM_START + 0x057F
DKC_STAGE_FLAGS = WRAM_START + 0x0583
DKC_SANITY_FLAGS = WRAM_START + 0x1F800

DKC_BARRELS = DKC_SRAM + 0x024
DKC_ENERGY_LINK_TRANSFER = DKC_SRAM + 0x020
DKC_EXCHANGE_RATE = 200000000
DK_BARREL_BANANA_COST = 20

DKC_ROMHASH_START = 0xFFC0
ROMHASH_SIZE = 0x15

UNCOLLECTABLE_LEVELS = []

class DKCSNIClient(SNIClient):
    game = "Donkey Kong Country"
    patch_suffix = ".apdkc"
    slot_data: dict

    def __init__(self):
        super().__init__()
        self.game_state = False
        self.energy_link_enabled = False
        self.received_trap_link = False
        self.barrel_request = ""
        self.current_map = 0
        self.barrel_label = None

    async def validate_rom(self, ctx):
        from SNIClient import snes_read

        setting_data = await snes_read(ctx, DKC_SETTINGS, 0x40)
        rom_name = await snes_read(ctx, DKC_ROMHASH_START, ROMHASH_SIZE)

        if rom_name is None or setting_data is None or rom_name == bytes([0] * ROMHASH_SIZE) or rom_name[:4] != b"DKC1":
            if "request" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("request")
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.receive_option = 0
        ctx.send_option = 0
        ctx.allow_collect = True

        update_tags = False

        energy_link = setting_data[0x18]
        if energy_link and "EnergyLink" not in ctx.tags:
            ctx.tags.add("EnergyLink")
            update_tags = True
            if "request" not in ctx.command_processor.commands:
                ctx.command_processor.commands["request"] = cmd_request

        trap_link = setting_data[0x19]
        if trap_link and "TrapLink" not in ctx.tags:
            ctx.tags.add("TrapLink")
            update_tags = True

        if update_tags:
            await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}])

        ctx.rom = rom_name

        return True


    async def game_watcher(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        setting_data = await snes_read(ctx, DKC_SETTINGS, 0x40)
        if setting_data is None:
            self.game_state = False
            return
        
        nmi_pointer = await snes_read(ctx, WRAM_START + 0x001C, 0x2)
        if nmi_pointer is None:
            self.game_state = False
            return
        nmi_pointer = int.from_bytes(nmi_pointer, "little")
        if nmi_pointer == 0xE6B1:
            self.game_state = True
            
        if not self.game_state:
            self.current_map = 0
            return

        current_level = await snes_read(ctx, DKC_CURRENT_LEVEL, 0x01)
        loaded_level = await snes_read(ctx, DKC_LOADED_LEVEL, 0x01)
        brightness = await snes_read(ctx, DKC_BRIGHTNESS, 0x01)
        is_in_map = await snes_read(ctx, DKC_IN_MAP, 0x01)
        kong_flags = await snes_read(ctx, DKC_KONG_LETTERS, 0x01)

        if current_level is None or loaded_level is None or brightness is None or is_in_map is None:
            return
        
        from .Levels import location_id_to_level_id
        from worlds import AutoWorldRegister

        new_checks = []
        current_level = int.from_bytes(current_level, "little")
        loaded_level = int.from_bytes(loaded_level, "little")
        brightness = int.from_bytes(brightness, "little")

        level_flags = await snes_read(ctx, DKC_STAGE_FLAGS, 0x100)
        sanity_flags = await snes_read(ctx, DKC_SANITY_FLAGS, 0x100)
        if level_flags is None or sanity_flags is None:
            return

        level_flags = list(level_flags)
        sanity_flags = list(sanity_flags)

        # Fix Reptile Rumble having two different IDs
        if current_level == 0xEA:
            current_level = 0x01

        kong_as_checks = setting_data[0x21]
        tokens_as_checks = setting_data[0x21]
        balloons_as_checks = setting_data[0x21]
        bunches_as_checks = setting_data[0x21]

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
                    if level_num == current_level and kong_flags[0] & 0x10 == 0x10:
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

        # Trigger goal
        if loaded_level == 0x004C:
            if not ctx.finished_game:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True
                return

        if "EnergyLink" in ctx.tags:
            await self.handle_energy_link(ctx)

        if "TrapLink" in ctx.tags:
            await self.handle_trap_link(ctx)
            
        # Add a label that shows how many Barrels are left
        await self.handle_barrel_label(ctx)

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
        rom = await snes_read(ctx, DKC_ROMHASH_START, ROMHASH_SIZE)
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

        recv_count = await snes_read(ctx, DKC_RECV_INDEX, 2)
        if recv_count is None:
            # Add a small failsafe in case we get a None. Other SNI games do this...
            return

        # Only receive items if we're at full brightness
        if brightness & 0x0F == 0x0F:
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
                    if "TrapLink" in ctx.tags and item.item in trap_value_to_name:
                        await self.send_trap_link(ctx, trap_value_to_name[item.item])

                if sfx:
                    snes_buffered_write(ctx, DKC_PLAY_SFX, bytearray([sfx, 0x80]))
                    
                snes_buffered_write(ctx, DKC_RECV_INDEX, recv_index.to_bytes(2, "little"))

                await snes_flush_writes(ctx)
                
        # Handle collected locations
        nmi_pointer = await snes_read(ctx, WRAM_START + 0x0020, 0x2)
        if nmi_pointer is None:
            return
        nmi_pointer = int.from_bytes(nmi_pointer, "little")
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

    async def handle_energy_link(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        # Deposits EnergyLink into pool
        energy_packet = await snes_read(ctx, DKC_ENERGY_LINK_TRANSFER, 0x2)
        if energy_packet is not None:
            energy_packet = int.from_bytes(energy_packet, "little")
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

        unlocked_kongs = await snes_read(ctx, DKC_SRAM + 0x00, 0x01)
        barrels = await snes_read(ctx, DKC_BARRELS, 0x02)
        if unlocked_kongs is None or barrels is None:
            return
    
        barrels = int.from_bytes(barrels, "little")
        
        if self.barrel_request == "place_request":
            self.barrel_request_tag = f"dkc2-dkbarrel-{ctx.team}-{ctx.slot}-{random.randint(0, 0xFFFFFFFF)}"
            value = DK_BARREL_BANANA_COST * DKC_EXCHANGE_RATE
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
            snes_buffered_write(ctx, DKC_BARRELS, bytes([barrels]))
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

    async def handle_barrel_label(self, ctx):
        try:
            from kvui import MDLabel as Label
        except ImportError:
            from kvui import Label
        from SNIClient import snes_read

        if not self.barrel_label:
            self.barrel_label = Label(text=f"", size_hint_x=None, width=120, halign="center")
            ctx.ui.connect_layout.add_widget(self.barrel_label)

        barrels = await snes_read(ctx, DKC_BARRELS, 0x02)
        if barrels is not None:
            barrel_count = int.from_bytes(barrels, "little")
            self.barrel_label.text = f"Barrels: {barrel_count}"

    async def handle_trap_link(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        from .Rom import trap_data
        
        setting_data = await snes_read(ctx, DKC_SETTINGS, 0x40)
        if setting_data is None:
            return

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

    def on_package(self, ctx, cmd: str, args: dict):
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
                    dk_barrel_cost = DKC_EXCHANGE_RATE * DK_BARREL_BANANA_COST
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
        
def cmd_request(self):
    """
    Request a DK Barrel from the banana pool (EnergyLink).
    """
    if self.ctx.game != "Donkey Kong Country":
        logger.warning("This command can only be used while playing Donkey Kong Country")
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.info(f"Must be connected to server and in game.")
    else:
        if self.ctx.client_handler.barrel_request != "":
            logger.info(f"You already have a DK Barrel in queue.")
            return
        else:
            self.ctx.client_handler.barrel_request = "place_request"
            logger.info(f"Placing a DK barrel request...")
