import logging

from BaseClasses import ItemClassification, Location, Item
from .data import iname
from .options import CVCotMOptions, Countdown
from .locations import get_location_info, base_id
from .regions import get_region_info
from .items import get_item_info, item_info

from typing import TYPE_CHECKING, Dict, List, Tuple, Union, Iterable

if TYPE_CHECKING:
    from . import CVCotMWorld

# 0 = Holy water  22
# 1 = Axe         24
# 2 = Knife       32
# 3 = Cross        6
# 4 = Stopwatch   12
# 5 = Small heart
# 6 = Big heart
rom_sub_weapon_offsets = {
    0xD034E: b"\x01",
    0xD0462: b"\x02",
    0xD064E: b"\x00",
    0xD06F6: b"\x02",
    0xD0882: b"\x00",
    0xD0912: b"\x02",
    0xD0C2A: b"\x02",
    0xD0C96: b"\x01",
    0xD0D92: b"\x02",
    0xD0DCE: b"\x01",
    0xD1332: b"\x00",
    0xD13AA: b"\x01",
    0xD1722: b"\x02",
    0xD17A6: b"\x01",
    0xD1926: b"\x01",
    0xD19AA: b"\x02",
    0xD1A9A: b"\x02",
    0xD1AA6: b"\x00",
    0xD1EBA: b"\x00",
    0xD1ED2: b"\x01",
    0xD2262: b"\x02",
    0xD23B2: b"\x03",
    0xD256E: b"\x02",
    0xD2742: b"\x02",
    0xD2832: b"\x04",
    0xD2862: b"\x01",
    0xD2A2A: b"\x01",
    0xD2DBA: b"\x04",
    0xD2DC6: b"\x00",
    0xD2E02: b"\x02",
    0xD2EFE: b"\x04",
    0xD2F0A: b"\x02",
    0xD302A: b"\x00",
    0xD3042: b"\x01",
    0xD304E: b"\x04",
    0xD3066: b"\x02",
    0xD322E: b"\x04",
    0xD334E: b"\x04",
    0xD3516: b"\x03",
    0xD35CA: b"\x02",
    0xD371A: b"\x01",
    0xD38EE: b"\x00",
    0xD3BE2: b"\x02",
    0xD3D1A: b"\x01",
    0xD3D56: b"\x02",
    0xD3ECA: b"\x00",
    0xD3EE2: b"\x02",
    0xD4056: b"\x01",
    0xD40E6: b"\x04",
    0xD413A: b"\x04",
    0xD4326: b"\x00",
    0xD460E: b"\x00",
    0xD48D2: b"\x00",
    0xD49E6: b"\x01",
    0xD4ABE: b"\x02",
    0xD4B8A: b"\x01",
    0xD4D0A: b"\x04",
    0xD4EAE: b"\x02",
    0xD4F0E: b"\x00",
    0xD4F92: b"\x02",
    0xD4FB6: b"\x01",
    0xD503A: b"\x03",
    0xD5646: b"\x01",
    0xD5682: b"\x02",
    0xD57C6: b"\x02",
    0xD57D2: b"\x02",
    0xD58F2: b"\x00",
    0xD5922: b"\x01",
    0xD5B9E: b"\x02",
    0xD5E26: b"\x01",
    0xD5E56: b"\x02",
    0xD5E7A: b"\x02",
    0xD5F5E: b"\x00",
    0xD69EA: b"\x02",
    0xD69F6: b"\x01",
    0xD6A02: b"\x00",
    0xD6A0E: b"\x04",
    0xD6A1A: b"\x03",
    0xD6BE2: b"\x00",
    0xD6CBA: b"\x01",
    0xD6CDE: b"\x02",
    0xD6EEE: b"\x00",
    0xD6F1E: b"\x02",
    0xD6F42: b"\x01",
    0xD6FC6: b"\x04",
    0xD706E: b"\x00",
    0xD716A: b"\x02",
    0xD72AE: b"\x01",
    0xD75BA: b"\x03",
    0xD76AA: b"\x04",
    0xD76B6: b"\x00",
    0xD76C2: b"\x01",
    0xD76CE: b"\x02",
    0xD76DA: b"\x03",
    0xD7D46: b"\x00",
    0xD7D52: b"\x00",
}


def shuffle_sub_weapons(world: "CVCotMWorld") -> Dict[int, bytes]:
    """Shuffles the sub-weapons amongst themselves."""
    sub_bytes = list(rom_sub_weapon_offsets.values())
    world.random.shuffle(sub_bytes)
    return dict(zip(rom_sub_weapon_offsets, sub_bytes))


def get_countdown_numbers(options: CVCotMOptions, active_locations: Iterable[Location]) -> Dict[int, int]:
    """Figures out which Countdown numbers to increase for each Location after verifying the Item on the Location should
    increase a number.

    The exact number to increase is determined by the Location's "countdown" key in the location_info dict."""
    countdown_list = [0 for _ in range(15)]
    for loc in active_locations:
        if loc.address is not None and (options.countdown == Countdown.option_all_locations or
                                        (options.countdown == Countdown.option_majors
                                         and loc.item.advancement)):

            countdown_number = get_location_info(loc.name, "countdown")

            if countdown_number is not None:
                countdown_list[countdown_number] += 1

    # Convert the Countdown list into a data dict
    countdown_dict = {}
    for i in range(len(countdown_list)):
        countdown_dict[0xBFD818 + i] = countdown_list[i]

    return countdown_dict


def get_location_data(world: "CVCotMWorld", active_locations: Iterable[Location]) -> Dict[int, bytes]:
    """Gets ALL the item data to go into the ROM. Item data consists of four bytes: the first dictates what category of
    items it belongs to (the higher byte of the item's AP code), the third is which item in that category it is (the
    lower byte of the code), and the second and fourth are always 0x01 and 0x00 respectively. Other game items will
    always appear as the unused Map item, which does nothing but set the flag for that location when picked up."""

    location_bytes = {}

    for loc in active_locations:
        # If the Location is an event, skip it.
        if loc.address is None:
            continue

        # Figure out the item ID bytes to put in each Location here. Write the item itself if either it's the player's
        # very own, or it belongs to an Item Link that the player is a part of.
        if loc.item.player == world.player or (loc.item.player in world.multiworld.groups and
                                               world.player in world.multiworld.groups[loc.item.player]['players']):
            code = get_item_info(loc.item.name, "code")
            location_bytes[get_location_info(loc.name, "offset")] = bytes([code >> 8, 0x01, code & 0x00FF, 0x00])
        else:
            # Make the item the unused Map - our multiworld item.
            location_bytes[get_location_info(loc.name, "offset")] = bytes([0xE8, 0x01, 0x05, 0x00])

    return location_bytes


def get_start_inventory_data(player: int, options: CVCotMOptions, precollected_items: List[Item]) -> Dict[int, int]:
    """Calculate and return the starting inventory values. Not every Item goes into the menu inventory, so everything
    has to be handled appropriately."""
    start_inventory_data = {0xBFD867: 0,  # Jewels
                            0xBFD87B: 0,  # PowerUps
                            0xBFD883: 0,  # Sub-weapon
                            0xBFD88B: 0}  # Ice Traps

    inventory_items_array = [0 for _ in range(35)]
    total_money = 0

    items_max = 10

    # Raise the items max if Increase Item Limit is enabled.
    if options.increase_item_limit:
        items_max = 99

    for item in precollected_items:
        if item.player != player:
            continue

        inventory_offset = get_item_info(item.name, "inventory offset")
        sub_equip_id = get_item_info(item.name, "sub equip id")
        # Starting inventory items
        if inventory_offset is not None:
            inventory_items_array[inventory_offset] += 1
            if inventory_items_array[inventory_offset] > items_max and "Special" not in item.name:
                inventory_items_array[inventory_offset] = items_max
            if item.name == iname.permaup:
                if inventory_items_array[inventory_offset] > 2:
                    inventory_items_array[inventory_offset] = 2
        # Starting sub-weapon
        elif sub_equip_id is not None:
            start_inventory_data[0xBFD883] = sub_equip_id
        # Starting PowerUps
        elif item.name == iname.powerup:
            start_inventory_data[0xBFD87B] += 1
            if start_inventory_data[0xBFD87B] > 2:
                start_inventory_data[0xBFD87B] = 2
        # Starting Gold
        elif "GOLD" in item.name:
            total_money += int(item.name[0:4])
            if total_money > 99999:
                total_money = 99999
        # Starting Jewels
        elif "jewel" in item.name:
            if "L" in item.name:
                start_inventory_data[0xBFD867] += 10
            else:
                start_inventory_data[0xBFD867] += 5
            if start_inventory_data[0xBFD867] > 99:
                start_inventory_data[0xBFD867] = 99
        # Starting Ice Traps
        else:
            start_inventory_data[0xBFD88B] += 1
            if start_inventory_data[0xBFD88B] > 0xFF:
                start_inventory_data[0xBFD88B] = 0xFF

    # Convert the inventory items into data.
    for i in range(len(inventory_items_array)):
        start_inventory_data[0xBFE518 + i] = inventory_items_array[i]

    # Convert the starting money into data. Which offset it starts from depends on how many bytes it takes up.
    if total_money <= 0xFF:
        start_inventory_data[0xBFE517] = total_money
    elif total_money <= 0xFFFF:
        start_inventory_data[0xBFE516] = total_money
    else:
        start_inventory_data[0xBFE515] = total_money

    return start_inventory_data
