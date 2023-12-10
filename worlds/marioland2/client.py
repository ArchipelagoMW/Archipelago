import base64
import logging

from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient, BizHawkClientContext
from worlds._bizhawk import read, write, guarded_write

logger = logging.getLogger("Client")

from .rom_addresses import rom_addresses

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
        from . import locations, items, START_IDS
        game_loaded_check, level_data, music = await read(ctx.bizhawk_ctx, [(0x0046, 10, "CartRAM"), (0x0848, 42, "CartRAM"), (0x0469, 1, "CartRAM")])
        if game_loaded_check != b'\x124Vx\xff\xff\xff\xff\xff\xff':
            return

        level_data = list(level_data)

        items_received = [list(items.keys())[item.item - START_IDS] for item in ctx.items_received]

        progressive_coins = {
            "Progressive Space Zone": 3,
            "Progressive Tree Zone": 4,
            "Progressive Macro Zone": 4,
            "Progressive Pumpkin Zone": 4,
            "Progressive Mario Zone": 4,
            "Progressive Turtle Zone": 3
        }
        for level_item, count in progressive_coins.items():
            if items_received.count(level_item) >= count:
                items_received.append(level_item.split(" ")[1] + " Coin")

        locations_checked = []
        modified_level_data = level_data.copy()
        for ID, (location, data) in enumerate(locations.items(), START_IDS):
            if "clear_condition" in data:
                if items_received.count(data["clear_condition"][0]) >= data["clear_condition"][1]:
                    modified_level_data[data["ram_index"]] |= 0x80
                elif (ctx.slot_data and ctx.slot_data["vanilla_coins"] and "Coin" in data["clear_condition"][0]
                      and modified_level_data[data["ram_index"]] & 0x40):
                    modified_level_data[data["ram_index"]] |= 0x80

            if level_data[data["ram_index"]] & 0x41:
                locations_checked.append(ID)

        if ctx.slot_data:
            total_stars = ctx.slot_data["stars"]
        else:
            total_stars = 5

        invincibility_length = int((832.0 / total_stars) * items_received.count("Progressive Invincibility Star"))

        if "Easy Mode" in items_received:
            difficulty_mode = 1
        elif "Normal Mode" in items_received:
            difficulty_mode = 0
        elif ctx.slot_data:
            difficulty_mode = ctx.slot_data["mode"] & 1
        else:
            difficulty_mode = 0

        data_writes = [
            (rom_addresses["Space_Physics"], [0xea, 0x87, 0xa2] if "Space Physics" in items_received else [0, 0, 0], "ROM"),
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
            (rom_addresses["Invincibility_Star_C"], [4] if "Progressive Invincibility Star" in items_received else [0], "ROM"),
            (rom_addresses["Enable_Bubble"], [0xcb, 0xd7] if "Progressive Space Zone" in items_received else [0, 0], "ROM"),
            (0x02E4, [difficulty_mode], "CartRAM"),
            (0x0848, modified_level_data, "CartRAM")
        ]

        success = await guarded_write(ctx.bizhawk_ctx, data_writes, [(0x0848, level_data, "CartRAM")])

        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed:
            return

        if locations_checked and locations_checked != self.locations_array:
            self.locations_array = locations_checked
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locations_checked}])

        if music == b'\x18':
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True