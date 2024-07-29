import dolphin_memory_engine
import asyncio
from CommonClient import ClientCommandProcessor, CommonContext, logger, gui_enabled
from collections import namedtuple

Item = namedtuple("Item", ["game_value", "default_wheel_position", "inventory_position"])
Location = namedtuple("Location", ["zone", "offset", "mask"])

Items = {
    "Gale Boomerang": Item(0x40, 6, 0),
    "Lantern": Item(0x48, 7, 1),
    "Spinner": Item(0x41, 3, 2),
    "Iron Boots": Item(0x45, 5, 3),
    "Hero's Bow": Item(0x43, 4, 4),
    "Hawkeye": Item(0x3e, 10, 5),
    "Ball and Chain": Item(0x42, 2, 6),
    "Dominion Rod": Item(0x46, 1, 8),
    "Clawshot": Item(0x44, 0, 9),
    "Double Clawshot": Item(0x47, 0, 10),
    "Bottle #1": Item(0x60, 14, 11),
    "Bottle #2": Item(0x60, 15, 12),
    "Bottle #3": Item(0x60, 16, 13),
    "Bottle #4": Item(0x60, 17, 14),
    "Bomb Bag #1": Item(0x50, 11, 15),
    "Bomb Bag #2": Item(0x50, 12, 16),
    "Bomb Bag #3": Item(0x50, 13, 17),
    "Fishing Rod": Item(0x4a, 9, 20),
    "Horse Call": Item(0x84, 18, 21),
    "Slingshot": Item(0x4b, 8, 23),
    "Ooccoo(FT)": Item(0x25, 24, 18),
    "Ooccoo Jr.": Item(0x27, 24, 18),
    "Ooccoo": Item(0x33, 24, 18)
}

Bottles = {
    0x60: "Empty Bottle",
    0x64: "Milk",
    0x65: "Milk(half)",
    0x66: "Lantern Oil(Shop)",
    0x67: "Water",
    0x68: "Lantern Oil(Scooped)",
    0x6f: "Lantern Refilled(Shop)"
}

Locations = {
    "Forest Temple: West Tile Worm Room Vines Chest": Location("Forest Temple", 0x0, 0x1),
    "Forest Temple: Totem Pole Chest": Location("Forest Temple", 0x0, 0x2),
    "Forest Temple: East Water Cave Chest": Location("Forest Temple", 0x0, 0x4),
    "Forest Temple: West Deku Like Chest": Location("Forest Temple", 0x0, 0x80),
    "Forest Temple: West Tile Worm Chest Behind Stairs": Location("Forest Temple", 0x1, 0x8),
    "Forest Temple: Central Chest Hanging From Web": Location("Forest Temple", 0x1, 0x10),
    "Forest Temple: Second Monkey Under Bridge Chest": Location("Forest Temple", 0x2, 0x2),
    "Forest Temple: East Tile Worm Chest": Location("Forest Temple", 0x3, 0x2),
    "Forest Temple: North Deku Like Chest": Location("Forest Temple", 0x3, 0x4),
    "Forest Temple: Windless Bridge Chest": Location("Forest Temple", 0x3, 0x10),
    "Forest Temple: Big Baba Key": Location("Forest Temple", 0x3, 0x40),
    "Forest Temple: Entrance Vines Chest": Location("Forest Temple", 0x3, 0x80),
    "Forest Temple: Central Chest Behind Stairs": Location("Forest Temple", 0x7, 0x20),
    "Forest Temple: Big Key Chest": Location("Forest Temple", 0x7, 0x40),
    "Forest Temple: Central North Chest": Location("Forest Temple", 0x7, 0x80),
    "Forest Temple: Dungeon Reward": Location("Forest Temple", 0x1d, 0x8),
    "Forest Temple: Diababa Heart Container": Location("Forest Temple", 0x1d, 0x10),
    "Forest Temple: Gale Boomerang": Location("Forest Temple", 0x1d, 0x80),
    "Wooden Sword Chest": Location("South Faron", 0x3, 0x10),
    "Link Basement Chest": Location("South Faron", 0x3, 0x2),
    "Dark alcove on North Faron tunnel passage": Location("North Faron", 0x0, 0x80),
    "Right cave before forest temple chest by torches": Location("North Faron", 0x0, 0x1),
    "Right cave before forest temple secret chest": Location("North Faron", 0x0, 0x4),
    "Chest by forest temple behind deku baba": Location("North Faron", 0x4, 0x80)
}

Regions = {
    "Forest Temple": [b'D_MN05\x00\x00', b'D_MN05A\x00', b'D_MN05B\x00'],
    "South Faron": [b'F_SP00\x00\x00', b'F_SP103\x00', b'F_SP104\x00', b'R_SP01\x00\x00'],
    "North Faron": [b'F_SP108\x00', b'D_SB10\x00\x00']
}

item_id_to_name = {value.game_value: key for key, value in Items.items()}
item_wheel_start = 0x80406274
item_inventory_start = 0x8040625c
region_node = 0x80406b18


class TPCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)


class TPContext(CommonContext):
    def __init__(self):
        super().__init__("", "")
        self.dolphin_sync_task = None

    def run_gui(self):
        from kvui import GameManager

        class TPManager(GameManager):
            logging_pairs = [("Client", "Archipelago")]
            base_title = "Archipelago TP Client"

        self.ui = TPManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


async def dolphin_sync_task(ctx: TPContext):
    current_inventory = list(dolphin_memory_engine.read_bytes(item_wheel_start, 24))
    last_checked_locations = set()
    checked_locations = set()

    logger.info("Current inventory:")
    for item in current_inventory:
        if item == 0xff:
            continue
        current_item = dolphin_memory_engine.read_byte(item_inventory_start + item)
        try:
            item_name = item_id_to_name[current_item]
        except KeyError:
            item_name = Bottles[current_item]
        logger.info(item_name)

    while not ctx.exit_event.is_set():
        current_zone = dolphin_memory_engine.read_bytes(0x8040afc0, 8)
        zone_name = ""
        for k, v in Regions.items():
            if zone_name != "":
                break
            for a in v:
                if current_zone == a:
                    zone_name = k
                    break

        last_offset = 0xffff
        for k, v in Locations.items():
            if zone_name == v.zone:
                if v.offset != last_offset:
                    last_offset = v.offset
                    flag_read = dolphin_memory_engine.read_byte(region_node + last_offset)

                if flag_read & v.mask:
                    checked_locations.add(k)

        if checked_locations != last_checked_locations:
            difference = checked_locations.difference(last_checked_locations)
            for check in difference:
                logger.info(f"New check: {check}")
                last_checked_locations.add(check)
        await asyncio.sleep(0.2)


def grant_item(item_name: str) -> None:
    item_to_grant: Item
    try:
        item_to_grant = Items[item_name]
    except KeyError:
        print(f"Error! {item_name} not found")
        return

    mem_read = dolphin_memory_engine.read_byte(item_to_grant.inventory_position + item_inventory_start)
    if mem_read != 0xFF:
        print("Error! Already have item")
        return

    item_wheel_list = list(dolphin_memory_engine.read_bytes(item_wheel_start, 24))

    for i, item in enumerate(item_wheel_list):
        if item == 0xff:
            # Reach an empty space
            item_wheel_list[i] = item_to_grant.inventory_position
            dolphin_memory_engine.write_byte(item_inventory_start + item_to_grant.inventory_position,
                                             item_to_grant.game_value)
            dolphin_memory_engine.write_bytes(item_wheel_start, bytes(item_wheel_list))
            break
        else:
            cur_item_id = dolphin_memory_engine.read_byte(item_inventory_start + item)
            if cur_item_id in Bottles.keys():
                cur_item = Items["Bottle #1"]
            else:
                cur_item = Items[item_id_to_name[cur_item_id]]

            if cur_item.default_wheel_position > item_to_grant.default_wheel_position:
                # WE MIGHT LOSE LAST ITEM. NEED MORE RESEARCH
                item_wheel_list = item_wheel_list[0:i] + [item_to_grant.inventory_position] + item_wheel_list[i:-1]
                dolphin_memory_engine.write_byte(item_inventory_start + item_to_grant.inventory_position,
                                                 item_to_grant.game_value)
                dolphin_memory_engine.write_bytes(item_wheel_start, bytes(item_wheel_list))
                break


def main():
    async def _main():
        ctx = TPContext()
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        dolphin_memory_engine.hook()
        if dolphin_memory_engine.is_hooked():
            logger.info("Hooked to Dolphin")

        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="DolphinSync")
        await ctx.dolphin_sync_task
        await asyncio.sleep(.25)

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        await asyncio.sleep(.5)

    import colorama

    colorama.init()
    asyncio.run(_main())
    colorama.deinit()


if __name__ == "__main__":
    main()
