import logging
from collections import deque
from typing import TYPE_CHECKING

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


base_id = 7000
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
status_a_location = 0x102
status_b_location = 0x0FC
status_c_location = 0x0A3

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

extended_consumables = ["FullCure", "Phoenix", "Blast", "Smoke",
                        "Refresh", "Flare", "Black", "Guard",
                        "Quick", "HighPotion", "Wizard", "Cloak"]

ext_consumables_lookup = {"FullCure": "Ext1", "Phoenix": "Ext2", "Blast": "Ext3", "Smoke": "Ext4",
                          "Refresh": "Ext1", "Flare": "Ext2", "Black": "Ext3", "Guard": "Ext4",
                          "Quick": "Ext1", "HighPotion": "Ext2", "Wizard": "Ext3", "Cloak": "Ext4"}

ext_consumables_locations = {"Ext1": 0x3C, "Ext2": 0x3D, "Ext3": 0x3E, "Ext4": 0x3F}


movement_items = ["Ship", "Bridge", "Canal", "Canoe"]

no_overworld_items = ["Sigil", "Mark"]


class FF1Client(BizHawkClient):
    game = "Final Fantasy"
    system = "NES"

    weapons_queue: deque[int]
    armor_queue: deque[int]
    consumable_stack_amounts: dict[str, int] | None

    def __init__(self) -> None:
        self.wram = "RAM"
        self.sram = "WRAM"
        self.rom = "PRG ROM"
        self.consumable_stack_amounts = None
        self.weapons_queue = deque()
        self.armor_queue = deque()
        self.guard_character = 0x00

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
        # Resetting these in case of switching ROMs
        self.consumable_stack_amounts = None
        self.weapons_queue = deque()
        self.armor_queue = deque()

        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None:
            return

        if ctx.slot is None:
            return
        try:
            self.guard_character = await self.read_sram_value(ctx, status_a_location)
            # If the first character's name starts with a 0 value, we're at the title screen/character creation.
            # In that case, don't allow any read/writes.
            # We do this by setting the guard to 1 because that's neither a valid character nor the initial value.
            if self.guard_character == 0:
                self.guard_character = 0x01

            if self.consumable_stack_amounts is None:
                self.consumable_stack_amounts = {}
                self.consumable_stack_amounts["Shard"] = 1
                other_consumable_amounts = await self.read_rom(ctx, 0x47400, 10)
                self.consumable_stack_amounts["Tent"] = other_consumable_amounts[0] + 1
                self.consumable_stack_amounts["Cabin"] = other_consumable_amounts[1] + 1
                self.consumable_stack_amounts["House"] = other_consumable_amounts[2] + 1
                self.consumable_stack_amounts["Heal"] = other_consumable_amounts[3] + 1
                self.consumable_stack_amounts["Pure"] = other_consumable_amounts[4] + 1
                self.consumable_stack_amounts["Soft"] = other_consumable_amounts[5] + 1
                self.consumable_stack_amounts["Ext1"] = other_consumable_amounts[6] + 1
                self.consumable_stack_amounts["Ext2"] = other_consumable_amounts[7] + 1
                self.consumable_stack_amounts["Ext3"] = other_consumable_amounts[8] + 1
                self.consumable_stack_amounts["Ext4"] = other_consumable_amounts[9] + 1

            await self.location_check(ctx)
            await self.received_items_check(ctx)
            await self.process_weapons_queue(ctx)
            await self.process_armor_queue(ctx)

        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass

    async def location_check(self, ctx: "BizHawkClientContext"):
        locations_data = await self.read_sram_values_guarded(ctx, locations_array_start, locations_array_length)
        if locations_data is None:
            return
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
            if locations_data[index] & flag != 0:
                locations_checked.append(location)

        found_locations = await ctx.check_locations(locations_checked)
        for location in found_locations:
            ctx.locations_checked.add(location)
            location_name = ctx.location_names.lookup_in_game(location)
            logger.info(
                f'New Check: {location_name} ({len(ctx.locations_checked)}/'
                f'{len(ctx.missing_locations) + len(ctx.checked_locations)})')


    async def received_items_check(self, ctx: "BizHawkClientContext") -> None:
        assert self.consumable_stack_amounts, "shouldn't call this function without reading consumable_stack_amounts"
        write_list: list[tuple[int, list[int], str]] = []
        items_received_count = await self.read_sram_value_guarded(ctx, items_obtained)
        if items_received_count is None:
            return
        if items_received_count < len(ctx.items_received):
            current_item = ctx.items_received[items_received_count]
            current_item_id = current_item.item
            current_item_name = ctx.item_names.lookup_in_game(current_item_id, ctx.game)
            if current_item_name in key_items:
                location = current_item_id - 0xE0
                write_list.append((location, [1], self.sram))
            elif current_item_name in movement_items:
                location = current_item_id - 0x1E0
                if current_item_name != "Canal":
                    write_list.append((location, [1], self.sram))
                else:
                    write_list.append((location, [0], self.sram))
            elif current_item_name in no_overworld_items:
                if current_item_name == "Sigil":
                    location = 0x28
                else:
                    location = 0x12
                write_list.append((location, [1], self.sram))
            elif current_item_name in gold_items:
                gold_amount = int(current_item_name[4:])
                current_gold_value = await self.read_sram_values_guarded(ctx, gp_location_low, 3)
                if current_gold_value is None:
                    return
                current_gold = int.from_bytes(current_gold_value, "little")
                new_gold = min(gold_amount + current_gold, 999999)
                lower_byte = new_gold % (2 ** 8)
                middle_byte = (new_gold // (2 ** 8)) % (2 ** 8)
                upper_byte = new_gold // (2 ** 16)
                write_list.append((gp_location_low, [lower_byte], self.sram))
                write_list.append((gp_location_middle, [middle_byte], self.sram))
                write_list.append((gp_location_high, [upper_byte], self.sram))
            elif current_item_name in consumables:
                location = current_item_id - 0xE0
                current_value = await self.read_sram_value_guarded(ctx, location)
                if current_value is None:
                    return
                amount_to_add = self.consumable_stack_amounts[current_item_name]
                new_value = min(current_value + amount_to_add, 99)
                write_list.append((location, [new_value], self.sram))
            elif current_item_name in extended_consumables:
                ext_name = ext_consumables_lookup[current_item_name]
                location = ext_consumables_locations[ext_name]
                current_value = await self.read_sram_value_guarded(ctx, location)
                if current_value is None:
                    return
                amount_to_add = self.consumable_stack_amounts[ext_name]
                new_value = min(current_value + amount_to_add, 99)
                write_list.append((location, [new_value], self.sram))
            elif current_item_name in weapons:
                self.weapons_queue.appendleft(current_item_id - 0x11B)
            elif current_item_name in armor:
                self.armor_queue.appendleft(current_item_id - 0x143)
            write_list.append((items_obtained, [items_received_count + 1], self.sram))
            write_successful = await self.write_sram_values_guarded(ctx, write_list)
            if write_successful:
                await bizhawk.display_message(ctx.bizhawk_ctx, f"Received {current_item_name}")

    async def process_weapons_queue(self, ctx: "BizHawkClientContext"):
        empty_slots = deque()
        char1_slots = await self.read_sram_values_guarded(ctx, weapons_arrays_starts[0], 4)
        char2_slots = await self.read_sram_values_guarded(ctx, weapons_arrays_starts[1], 4)
        char3_slots = await self.read_sram_values_guarded(ctx, weapons_arrays_starts[2], 4)
        char4_slots = await self.read_sram_values_guarded(ctx, weapons_arrays_starts[3], 4)
        if char1_slots is None or char2_slots is None or char3_slots is None or char4_slots is None:
            return
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
            await self.write_sram_guarded(ctx, current_slot, current_weapon)

    async def process_armor_queue(self, ctx: "BizHawkClientContext"):
        empty_slots = deque()
        char1_slots = await self.read_sram_values_guarded(ctx, armors_arrays_starts[0], 4)
        char2_slots = await self.read_sram_values_guarded(ctx, armors_arrays_starts[1], 4)
        char3_slots = await self.read_sram_values_guarded(ctx, armors_arrays_starts[2], 4)
        char4_slots = await self.read_sram_values_guarded(ctx, armors_arrays_starts[3], 4)
        if char1_slots is None or char2_slots is None or char3_slots is None or char4_slots is None:
            return
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
            await self.write_sram_guarded(ctx, current_slot, current_armor)


    async def read_sram_value(self, ctx: "BizHawkClientContext", location: int):
        value = ((await bizhawk.read(ctx.bizhawk_ctx, [(location, 1, self.sram)]))[0])
        return int.from_bytes(value, "little")

    async def read_sram_values_guarded(self, ctx: "BizHawkClientContext", location: int, size: int):
        value = await bizhawk.guarded_read(ctx.bizhawk_ctx,
                                           [(location, size, self.sram)],
                                           [(status_a_location, [self.guard_character], self.sram)])
        if value is None:
            return None
        return value[0]

    async def read_sram_value_guarded(self, ctx: "BizHawkClientContext", location: int):
        value = await bizhawk.guarded_read(ctx.bizhawk_ctx,
                                           [(location, 1, self.sram)],
                                           [(status_a_location, [self.guard_character], self.sram)])
        if value is None:
            return None
        return int.from_bytes(value[0], "little")

    async def read_rom(self, ctx: "BizHawkClientContext", location: int, size: int):
        return (await bizhawk.read(ctx.bizhawk_ctx, [(location, size, self.rom)]))[0]

    async def write_sram_guarded(self, ctx: "BizHawkClientContext", location: int, value: int):
        return await bizhawk.guarded_write(ctx.bizhawk_ctx,
                                           [(location, [value], self.sram)],
                                           [(status_a_location, [self.guard_character], self.sram)])

    async def write_sram_values_guarded(self, ctx: "BizHawkClientContext", write_list):
        return await bizhawk.guarded_write(ctx.bizhawk_ctx,
                                           write_list,
                                           [(status_a_location, [self.guard_character], self.sram)])
