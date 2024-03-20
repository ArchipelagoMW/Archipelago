import base64
import logging

from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient, BizHawkClientContext
from worlds._bizhawk import read, write, guarded_write

from .rom_addresses import rom_addresses

logger = logging.getLogger("Client")

BANK_EXCHANGE_RATE = 20000000000


class MarioLand2Client(BizHawkClient):
    system = ("GB", "SGB")
    patch_suffix = ".apsml2"
    game = "Super Mario Land 2"

    def __init__(self):
        super().__init__()
        self.locations_array = []

    async def validate_rom(self, ctx):
        game_name = await read(ctx.bizhawk_ctx, [(0x134, 10, "ROM")])
        game_name = game_name[0].decode("ascii")
        if game_name == "MARIOLAND2":
            ctx.game = self.game
            ctx.items_handling = 0b111
            return True
        return False

    async def set_auth(self, ctx):
        auth_name = await read(ctx.bizhawk_ctx, [(0x77777, 21, "ROM")])
        auth_name = base64.b64encode(auth_name[0]).decode()
        ctx.auth = auth_name

    async def game_watcher(self, ctx: BizHawkClientContext):
        from . import START_IDS
        from .items import items
        from .locations import locations

        (game_loaded_check, level_data, music, auto_scroll_enabled, auto_scroll_levels, current_level, midway_point,
         bcd_lives) = \
            await read(ctx.bizhawk_ctx, [(0x0046, 10, "CartRAM"), (0x0848, 42, "CartRAM"), (0x0469, 1, "CartRAM"),
                                         (rom_addresses["Auto_Scroll_Disable"], 1, "ROM"),
                                         (rom_addresses["Auto_Scroll_Levels"], 32, "ROM"),
                                         (0x0269, 1, "CartRAM"),
                                         (0x02A0, 1, "CartRAM"),
                                         (0x022C, 1, "CartRAM")])

        current_level = int.from_bytes(current_level, "big")
        midway_point = int.from_bytes(midway_point, "big")
        music = int.from_bytes(music, "big")
        auto_scroll_enabled = int.from_bytes(auto_scroll_enabled, "big")
        level_data = list(level_data)
        lives = bcd_lives.hex()

        # there is no music in the title screen demos, this is how we guard against anything in the demos registering.
        if game_loaded_check != b'\x124Vx\xff\xff\xff\xff\xff\xff' or music == 0:
            return

        items_received = [list(items.keys())[item.item - START_IDS] for item in ctx.items_received]

        level_progression = {
            "Space Zone Progression",
            "Tree Zone Progression",
            "Macro Zone Progression",
            "Pumpkin Zone Progression",
            "Mario Zone Progression",
            "Turtle Zone Progression",
        }
        for level_item in level_progression:
            for _ in range(items_received.count(level_item + " x2")):
                items_received += ([level_item] * 2)

        if "Pipe Traversal" in items_received:
            items_received += ["Pipe Traversal - Left", "Pipe Traversal - Right",
                               "Pipe Traversal - Up", "Pipe Traversal - Down"]

        locations_checked = []
        modified_level_data = level_data.copy()
        for ID, (location, data) in enumerate(locations.items(), START_IDS):
            if "clear_condition" in data:
                if items_received.count(data["clear_condition"][0]) >= data["clear_condition"][1]:
                    modified_level_data[data["ram_index"]] |= (0x08 if data["type"] == "bell"
                                                               else 0x01 if data["type"] == "secret" else 0x80)

            if data["type"] == "level" and level_data[data["ram_index"]] & 0x40:
                locations_checked.append(ID)
            if data["type"] == "secret" and level_data[data["ram_index"]] & 0x02:
                locations_checked.append(ID)
            elif data["type"] == "bell" and data["id"] == current_level and midway_point == 0xFF:
                locations_checked.append(ID)

        if ctx.slot_data:
            total_stars = ctx.slot_data["stars"]
        else:
            total_stars = 5

        invincibility_length = int((832.0 / (total_stars + 1))
                                   * (items_received.count("Super Star Duration Increase") + 1))

        if "Easy Mode" in items_received:
            difficulty_mode = 1
        elif "Normal Mode" in items_received:
            difficulty_mode = 0
        elif ctx.slot_data:
            difficulty_mode = ctx.slot_data["mode"] & 1
        else:
            difficulty_mode = 0

        new_lives = int(lives)
        energy_link_add = None
        if ctx.slot_data and ctx.slot_data["energy_link"]:
            if new_lives == 0:
                if (f"EnergyLink{ctx.team}" in ctx.stored_data
                        and ctx.stored_data[f"EnergyLink{ctx.team}"]
                        and ctx.stored_data[f"EnergyLink{ctx.team}"] >= BANK_EXCHANGE_RATE):
                    new_lives = 1
                    energy_link_add = -BANK_EXCHANGE_RATE
            elif new_lives > 1:
                energy_link_add = BANK_EXCHANGE_RATE * (new_lives - 1)
                new_lives = 1
        # convert back to binary-coded-decimal
        new_lives = int(str(new_lives), 16)

        data_writes = [
            (rom_addresses["Space_Physics"], [0x7e] if "Space Physics" in items_received else [0xaf], "ROM"),
            (rom_addresses["Get_Hurt_To_Big_Mario"], [1] if "Mushroom" in items_received else [0], "ROM"),
            (rom_addresses["Get_Mushroom_A"], [0xea, 0x16, 0xa2] if "Mushroom" in items_received else [0, 0, 0], "ROM"),
            (rom_addresses["Get_Mushroom_B"], [0xea, 0x16, 0xa2] if "Mushroom" in items_received else [0, 0, 0], "ROM"),
            (rom_addresses["Get_Mushroom_C"], [00] if "Mushroom" in items_received else [0xd8], "ROM"),
            (rom_addresses["Get_Carrot_A"], [0xea, 0x16, 0xa2] if "Carrot" in items_received else [0, 0, 0], "ROM"),
            (rom_addresses["Get_Carrot_B"], [0xea, 0x16, 0xa2] if "Carrot" in items_received else [0, 0, 0], "ROM"),
            (rom_addresses["Get_Carrot_C"], [00] if "Carrot" in items_received else [0xc8], "ROM"),
            (rom_addresses["Get_Fire_Flower_A"], [0xea, 0x16, 0xa2] if "Fire Flower" in items_received else [0, 0, 0], "ROM"),
            (rom_addresses["Get_Fire_Flower_B"], [0xea, 0x16, 0xa2] if "Fire Flower" in items_received else [0, 0, 0], "ROM"),
            (rom_addresses["Get_Fire_Flower_C"], [00] if "Fire Flower" in items_received else [0xc8], "ROM"),
            (rom_addresses["Invincibility_Star_A"], [(invincibility_length >> 8) + 1], "ROM"),
            (rom_addresses["Invincibility_Star_B"], [invincibility_length & 0xFF], "ROM"),
            (rom_addresses["Enable_Bubble"], [0xcb, 0xd7] if "Hippo Bubble" in items_received else [0, 0], "ROM"),
            (rom_addresses["Enable_Swim"], [0xcb, 0xcf] if "Swim" in items_received else [0, 0], "ROM"),
            (rom_addresses["Pipe_Traversal_A"], [16] if "Pipe Traversal - Down" in items_received else [0], "ROM"),
            (rom_addresses["Pipe_Traversal_B"], [32] if "Pipe Traversal - Up" in items_received else [10], "ROM"),
            (rom_addresses["Pipe_Traversal_C"], [48] if "Pipe Traversal - Right" in items_received else [0], "ROM"),
            (rom_addresses["Pipe_Traversal_D"], [64] if "Pipe Traversal - Left" in items_received else [0], "ROM"),
            (rom_addresses["Pipe_Traversal_SFX_A"], [5] if "Pipe Traversal - Down" in items_received else [0], "ROM"),
            (rom_addresses["Pipe_Traversal_SFX_B"], [5] if "Pipe Traversal - Up" in items_received else [0], "ROM"),
            (rom_addresses["Pipe_Traversal_SFX_C"], [5] if "Pipe Traversal - Right" in items_received else [0], "ROM"),
            (rom_addresses["Pipe_Traversal_SFX_D"], [5] if "Pipe Traversal - Left" in items_received else [0], "ROM"),
            (0x022c, [new_lives], "CartRAM"),
            (0x02E4, [difficulty_mode], "CartRAM"),
            (0x0848, modified_level_data, "CartRAM")
        ]

        if midway_point == 0xFF and ctx.slot_data and ctx.slot_data["midway_bells"]:
            # after registering the check for the midway bell, clear the value just for safety.
            data_writes.append((0x02A0, [0], "CartRAM"))

        if "Auto Scroll" in items_received:
            if auto_scroll_enabled == 0xaf:  # auto scroll has not yet been enabled
                data_writes.append((rom_addresses["Auto_Scroll_Disable"], [0x7e], "ROM"))
                # if the current level is an auto scroll level, turn on auto scrolling now
                if auto_scroll_levels[current_level] == 1:
                    data_writes.append((0x02C8, [0x01], "CartRAM"))

        success = await guarded_write(ctx.bizhawk_ctx, data_writes, [(0x0848, level_data, "CartRAM"),
                                                                     (0x022C, [int.from_bytes(bcd_lives, "big")],
                                                                      "CartRAM")])

        if success and energy_link_add is not None:
            await ctx.send_msgs([{
                "cmd": "Set", "key": f"EnergyLink{ctx.team}", "operations":
                    [{"operation": "add", "value": energy_link_add},
                     {"operation": "max", "value": 0}],
            }])

        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed:
            return

        if locations_checked and locations_checked != self.locations_array:
            self.locations_array = locations_checked
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locations_checked}])

        if music == 0x18:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

    def on_package(self, ctx: BizHawkClientContext, cmd: str, args: dict):
        super().on_package(ctx, cmd, args)
        if cmd == 'Connected':
            if ctx.slot_data["energy_link"]:
                ctx.set_notify(f"EnergyLink{ctx.team}")
                if ctx.ui:
                    ctx.ui.enable_energy_link()
                    ctx.ui.energy_link_label.text = "Lives: Standby"
        elif cmd == "SetReply" and args["key"].startswith("EnergyLink"):
            if ctx.ui:
                ctx.ui.energy_link_label.text = f"Lives: {int(args['value'] / BANK_EXCHANGE_RATE)}"
        elif cmd == "Retrieved":
            if f"EnergyLink{ctx.team}" in args["keys"] and args['keys'][f'EnergyLink{ctx.team}'] and ctx.ui:
                ctx.ui.energy_link_label.text = f"Lives: {int(args['keys'][f'EnergyLink{ctx.team}'] / BANK_EXCHANGE_RATE)}"
