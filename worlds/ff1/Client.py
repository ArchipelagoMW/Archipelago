import logging
from collections import deque
from copy import deepcopy
from typing import TYPE_CHECKING

from MultiServer import Client
from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


base_id = 7000
nes_logger = logging.getLogger("NES")
logger = logging.getLogger("Client")


rom_name_location = 0x07FFE3
locations_array_start = 0x200
locations_array_length = 0x100
items_obtained = 0x03
gp_location_low = 0x1C
gp_location_middle = 0x1D
gp_location_high = 0x1E
weapons_arrays_starts = [0x118, 0x158, 0x198, 0x1D8]
armors_arrays_starts = [0x11C, 0x15C, 0x19C, 0x1DC]

key_items = ["Lute", "Crown", "Crystal", "Herb", "Key", "Tnt", "Adamant", "Slab", "Ruby", "Rod",
             "Floater", "Chime", "Tail", "Cube", "Bottle", "Oxyale", "EarthOrb", "FireOrb", "WaterOrb", "AirOrb"]

consumables = ["Shard", "Tent", "Cabin", "House", "Heal", "Pure", "Soft"]

weapons = ["WoodenNunchucks", "SmallKnife", "WoodenRod", "Rapier", "IronHammer", "ShortSword", "HandAxe", "Scimitar",
           "IronNunchucks", "LargeKnife", "IronStaff", "Sabre", "LongSword", "GreatAxe", "Falchon", "SilverKnife",
           "SilverSword", "SilverHammer", "SilverAxe", "FlameSword", "IceSword", "DragonSword", "GiantSword",
           "SunSword", "CoralSword", "WereSword", "RuneSword", "PowerRod", "LightAxe", "HealRod", "MageRod", "Defense",
           "WizardRod", "Vorpal", "CatClaw", "ThorHammer", "BaneSword", "Katana", "Xcalber", "Masamune"]

armor = ["Cloth", "WoodenArmor", "ChainArmor", "IronArmor", "SteelArmor", "SilverArmor", "FlameArmor", "IceArmor",
         "OpalArmor", "DragonArmor", "Copper", "Silver", "Gold", "Opal", "WhiteShirt", "BlackShirt", "WoodenShield",
         "IronShield", "SilverShield", "FlameShield", "IceShield", "OpalShield", "AegisShield", "Buckler", "ProCape",
         "Cap", "WoodenHelm", "IronHelm", "SilverHelm", "OpalHelm", "HealHelm", "Ribbon", "Gloves", "CopperGauntlets",
         "IronGauntlets", "SilverGauntlets", "ZeusGauntlets", "PowerGauntlets", "OpalGauntlets", "ProRing"]

gold_items = ["Gold10", "Gold20", "Gold25", "Gold30", "Gold55", "Gold70", "Gold85", "Gold110", "Gold135", "Gold155",
              "Gold160", "Gold180", "Gold240", "Gold255", "Gold260", "Gold295", "Gold300", "Gold315", "Gold330",
              "Gold350", "Gold385", "Gold400", "Gold450", "Gold500", "Gold530", "Gold575", "Gold620", "Gold680",
              "Gold750", "Gold795", "Gold880", "Gold1020", "Gold1250", "Gold1455", "Gold1520", "Gold1760", "Gold1975",
              "Gold2000", "Gold2750", "Gold3400", "Gold4150", "Gold5000", "Gold5450", "Gold6400", "Gold6720",
              "Gold7340", "Gold7690", "Gold7900", "Gold8135", "Gold9000", "Gold9300", "Gold9500", "Gold9900",
              "Gold10000", "Gold12350", "Gold13000", "Gold13450", "Gold14050", "Gold14720", "Gold15000", "Gold17490",
              "Gold18010", "Gold19990", "Gold20000", "Gold20010", "Gold26000", "Gold45000", "Gold65000"]

extended_consumables = ["Smoke", "FullCure", "Blast", "Phoenix",
                        "Flare", "Black", "Refresh", "Guard",
                        "Wizard", "HighPotion", "Cloak", "Quick"]

ext_consumables_lookup = {"Smoke": "Ext1", "FullCure": "Ext2", "Blast": "Ext3", "Phoenix": "Ext4",
                          "Flare": "Ext1", "Black": "Ext2", "Refresh": "Ext3", "Guard": "Ext4",
                          "Wizard": "Ext1", "HighPotion": "Ext2", "Cloak": "Ext3", "Quick": "Ext4"}

ext_consumables_locations = {"Ext1": 0x3C, "Ext2": 0x3D, "Ext3": 0x3E, "Ext4": 0x3F}


movement_items = ["Ship", "Bridge", "Canal", "Canoe"]

no_overworld_items = ["Sigil", "Mark"]


class FF1Client(BizHawkClient):
    game = "Final Fantasy"
    system = "NES"

    def __init__(self):
        self.wram = "RAM"
        self.sram = "WRAM"
        self.rom = "PRG ROM"
        self.consumable_stack_amounts = None
        self.weapons_queue = deque()
        self.armor_queue = deque()


    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(rom_name_location, 0x0D, self.rom)]))[0])
            rom_name = rom_name.decode("ascii")
            if rom_name != "FINAL FANTASY":
                return False  # Not a Final Fantasy 1 ROM
        except bizhawk.RequestFailedError:
            return False  # Not able to get a response, say no for now

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True

        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None:
            return

        if ctx.slot is None:
            return
        try:
            if await self.check_status_okay_to_process(ctx):
                if self.consumable_stack_amounts is None:
                    self.consumable_stack_amounts = {}
                    self.consumable_stack_amounts["Shard"] = 1
                    self.consumable_stack_amounts["Tent"] = (await self.read_rom(ctx, 0x47400, 1))[0] + 1
                    self.consumable_stack_amounts["Cabin"] = (await self.read_rom(ctx, 0x47401, 1))[0] + 1
                    self.consumable_stack_amounts["House"] = (await self.read_rom(ctx, 0x47402, 1))[0] + 1
                    self.consumable_stack_amounts["Heal"] = (await self.read_rom(ctx, 0x47403, 1))[0] + 1
                    self.consumable_stack_amounts["Pure"] = (await self.read_rom(ctx, 0x47404, 1))[0] + 1
                    self.consumable_stack_amounts["Soft"] = (await self.read_rom(ctx, 0x47405, 1))[0] + 1
                    self.consumable_stack_amounts["Ext1"] = (await self.read_rom(ctx, 0x47406, 1))[0] + 1
                    self.consumable_stack_amounts["Ext2"] = (await self.read_rom(ctx, 0x47407, 1))[0] + 1
                    self.consumable_stack_amounts["Ext3"] = (await self.read_rom(ctx, 0x47408, 1))[0] + 1
                    self.consumable_stack_amounts["Ext4"] = (await self.read_rom(ctx, 0x47409, 1))[0] + 1

                await self.location_check(ctx)
                await self.received_items_check(ctx)
                await self.process_weapons_queue(ctx)
                await self.process_armor_queue(ctx)

        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass

    async def check_status_okay_to_process(self, ctx):
        """
            local A = u8(0x102) -- Party Made
            local B = u8(0x0FC)
            local C = u8(0x0A3)
            return A ~= 0x00 and not (A== 0xF2 and B == 0xF2 and C == 0xF2)
        """
        status_a = await self.read_sram_value(ctx, 0x102)
        status_b = await self.read_sram_value(ctx, 0x0FC)
        status_c = await self.read_sram_value(ctx, 0x0A3)
        return (status_a != 0x00) and not (status_a == 0xF2 and status_b == 0xF2 and status_c == 0xF2)

    async def location_check(self, ctx):
        locations_data = await self.read_sram_values(ctx, locations_array_start, locations_array_length)
        locations_checked = []
        if len(locations_data) > 0xFE and locations_data[0xFE] & 0x02 != 0 and not ctx.finished_game:
            await ctx.send_msgs([
                {"cmd": "StatusUpdate",
                 "status": ClientStatus.CLIENT_GOAL}
            ])
            ctx.finished_game = True
        for location in ctx.missing_locations:
            # index will be - 0x100 or 0x200
            index = location
            if location < 0x200:
                # Location is a chest
                index -= 0x100
                flag = 0x04
            else:
                # Location is an NPC
                index -= 0x200
                flag = 0x02
            # print(f"Location: {ctx.location_names[location]}")
            # print(f"Index: {str(hex(index))}")
            # print(f"value: {locations_array[index] & flag != 0}")
            if locations_data[index] & flag != 0:
                locations_checked.append(location)

        for location in locations_checked:
            if location not in ctx.locations_checked:
                ctx.locations_checked.add(location)
                location_name = ctx.location_names.lookup_in_game(location)
                nes_logger.info(
                    f'New Check: {location_name} ({len(ctx.locations_checked)}/'
                    f'{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location]}])



    async def received_items_check(self, ctx):
        items_received_count = await self.read_sram_value(ctx, items_obtained)
        if items_received_count < len(ctx.items_received):
            current_item = ctx.items_received[items_received_count]
            current_item_id = current_item.item
            current_item_name = ctx.item_names.lookup_in_game(current_item_id, ctx.game)
            if current_item_name in key_items:
                location = current_item_id - 0xE0
                await self.write_sram(ctx, location, 1)
            elif current_item_name in movement_items:
                location = current_item_id - 0x1E0
                if current_item_name != "Canal":
                    await self.write_sram(ctx, location, 1)
                else:
                    await self.write_sram(ctx, location, 0)
            elif current_item_name in no_overworld_items:
                if current_item_name == "Sigil":
                    location = 0x28
                else:
                    location = 0x12
                await self.write_sram(ctx, location, 1)
            elif current_item_name in gold_items:
                gold_amount = int(current_item_name[4:])
                current_gold = int.from_bytes(await self.read_sram_values(ctx, gp_location_low, 3), "little")
                new_gold = min(gold_amount + current_gold, 999999)
                lower_byte = new_gold % (2 ** 8)
                middle_byte = (new_gold // (2 ** 8)) % (2 ** 8)
                upper_byte = new_gold // (2 ** 16)
                await self.write_sram(ctx, gp_location_low, lower_byte)
                await self.write_sram(ctx, gp_location_middle, middle_byte)
                await self.write_sram(ctx, gp_location_high, upper_byte)
            elif current_item_name in consumables:
                location = current_item_id - 0xE0
                current_value = await self.read_sram_value(ctx, location)
                amount_to_add = self.consumable_stack_amounts[current_item_name]
                new_value = min(current_value + amount_to_add, 99)
                await self.write_sram(ctx, location, new_value)
            elif current_item_name in extended_consumables:
                ext_name = ext_consumables_lookup[current_item_name]
                location = ext_consumables_locations[ext_name]
                current_value = await self.read_sram_value(ctx, location)
                amount_to_add = self.consumable_stack_amounts[ext_name]
                new_value = min(current_value + amount_to_add, 99)
                await self.write_sram(ctx, location, new_value)
            elif current_item_name in weapons:
                self.weapons_queue.appendleft(current_item_id - 0x11B)
            elif current_item_name in armor:
                self.armor_queue.appendleft(current_item_id - 0x143)
            await self.write_sram(ctx, items_obtained, items_received_count + 1)

    async def process_weapons_queue(self, ctx):
        empty_slots = deque()
        char1_slots = await self.read_sram_values(ctx, weapons_arrays_starts[0], 4)
        char2_slots = await self.read_sram_values(ctx, weapons_arrays_starts[1], 4)
        char3_slots = await self.read_sram_values(ctx, weapons_arrays_starts[2], 4)
        char4_slots = await self.read_sram_values(ctx, weapons_arrays_starts[3], 4)
        for i, slot in enumerate(char1_slots):
            if slot == 0:
                empty_slots.appendleft(weapons_arrays_starts[0] + i)
        for i, slot in enumerate(char2_slots):
            if slot == 0:
                empty_slots.appendleft(weapons_arrays_starts[1] + i)
        for i, slot in enumerate(char3_slots):
            if slot == 0:
                empty_slots.appendleft(weapons_arrays_starts[2] + i)
        for i, slot in enumerate(char4_slots):
            if slot == 0:
                empty_slots.appendleft(weapons_arrays_starts[3] + i)
        while len(empty_slots) > 0 and len(self.weapons_queue) > 0:
            current_slot = empty_slots.pop()
            current_weapon = self.weapons_queue.pop()
            await self.write_sram(ctx, current_slot, current_weapon)

    async def process_armor_queue(self, ctx):
        empty_slots = deque()
        char1_slots = await self.read_sram_values(ctx, armors_arrays_starts[0], 4)
        char2_slots = await self.read_sram_values(ctx, armors_arrays_starts[1], 4)
        char3_slots = await self.read_sram_values(ctx, armors_arrays_starts[2], 4)
        char4_slots = await self.read_sram_values(ctx, armors_arrays_starts[3], 4)
        for i, slot in enumerate(char1_slots):
            if slot == 0:
                empty_slots.appendleft(armors_arrays_starts[0] + i)
        for i, slot in enumerate(char2_slots):
            if slot == 0:
                empty_slots.appendleft(armors_arrays_starts[1] + i)
        for i, slot in enumerate(char3_slots):
            if slot == 0:
                empty_slots.appendleft(armors_arrays_starts[2] + i)
        for i, slot in enumerate(char4_slots):
            if slot == 0:
                empty_slots.appendleft(armors_arrays_starts[3] + i)
        while len(empty_slots) > 0 and len(self.armor_queue) > 0:
            current_slot = empty_slots.pop()
            current_armor = self.armor_queue.pop()
            await self.write_sram(ctx, current_slot, current_armor)

    async def read_ram_values(self, ctx, location, size):
        return (await bizhawk.read(ctx.bizhawk_ctx, [(location, size, self.wram)]))[0]

    async def read_ram_value(self, ctx, location):
        value = ((await bizhawk.read(ctx.bizhawk_ctx, [(location, 1, self.wram)]))[0])
        return int.from_bytes(value)

    async def read_sram_values(self, ctx, location, size):
        return (await bizhawk.read(ctx.bizhawk_ctx, [(location, size, self.sram)]))[0]

    async def read_sram_value(self, ctx, location):
        value = ((await bizhawk.read(ctx.bizhawk_ctx, [(location, 1, self.sram)]))[0])
        return int.from_bytes(value)

    async def read_rom(self, ctx, location, size):
        return (await bizhawk.read(ctx.bizhawk_ctx, [(location, size, self.rom)]))[0]

    async def write(self, ctx, location, value):
        return await bizhawk.write(ctx.bizhawk_ctx, [(location, [value], self.wram)])

    async def write_sram(self, ctx, location, value):
        return await bizhawk.write(ctx.bizhawk_ctx, [(location, [value], self.sram)])