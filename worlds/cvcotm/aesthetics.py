import logging

from BaseClasses import ItemClassification, Location, Item
from .data import iname
from .options import CVCotMOptions, Countdown, ItemDropRandomization
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

easy_items = [
    1,   # Leather Armor
    12,  # Cotton Robe
    17,  # Cotton Clothes
    34,  # Wristband
    41,  # Potion
    46,  # Antidote
    47,  # Cure Curse
    48,  # Mind Restore
    51   # Heart
]

common_items = easy_items + [
    2,   # Bronze Armor
    3,   # Gold Armor
    4,   # Chainmail
    5,   # Steel Armor

    13,  # Silk Robe
    14,  # Rainbow Robe

    18,  # Prison Garb
    19,  # Stylish Suit

    23,  # Double Grips
    24,  # Star Bracelet
    25,  # Strength Ring
    26,  # Hard Ring
    27,  # Intelligence Ring
    28,  # Luck Ring
    29,  # Cursed Ring

    35,  # Gauntlet
    36,  # Arm Guard
    37,  # Magic Gauntlet
    38,  # Miracle Armband
    40,  # Bear Ring
    39,  # Toy Ring

    42,  # Meat
    43,  # Spiced Meat

    52,  # Heart High
]

rare_items = [
    6,   # Platinum Armor
    7,   # Diamond Armor
    8,   # Mirror Armor
    9,   # Needle Armor
    10,  # Dark Armor

    15,  # Magic Robe
    16,  # Sage Robe

    20,  # Nightsuit
    21,  # Ninja Garb
    22,  # Soldier Fatigues

    30,  # Strength Armband
    31,  # Defense Armband
    32,  # Sage Armband
    33,  # Gambler Armband

    44,  # Potion High
    45,  # Potion Ex

    49,  # Mind High
    50,  # Mind Ex

    53,  # Heart Ex
    54,  # Heart Mega
]

all_items = rare_items + common_items

easily_farmable_enemies = [
    0,   # Medusa Head
    1,   # Zombie
    2,   # Ghoul
    3,   # Wight
    7,   # Skeleton Bomber
    14,  # Fleaman
    16,  # Bat
    17,  # Spirit
    18,  # Ectoplasm
    19,  # Specter
    40,  # Devil Tower
    46,  # Gargoyle
    50,  # Poison Worm
    51,  # Myconid
    54,  # Merman
    58,  # Gremlin
    59,  # Hopper
    82,  # Evil Hand
    87,  # Mummy
]

below_150_hp_enemies = easily_farmable_enemies + [
    4,    # Clinking Man
    5,    # Zombie Thief
    8,    # Electric Skeleton
    9,    # Skeleton Spear
    10,   # Skeleton Boomerang
    11,   # Skeleton Soldier
    12,   # Skeleton Knight
    13,   # Bone Tower
    15,   # Poltergeist
    20,   # Axe Armor
    26,   # Earth Armor
    29,   # Stone Armor
    35,   # Bloody Sword
    41,   # Skeleton Athlete
    42,   # Harpy
    44,   # Imp
    45,   # Mudman
    47,   # Slime
    48,   # Frozen Shade
    49,   # Heat Shade
    52,   # Will-O-Wisp
    53,   # Spearfish
    57,   # Marionette
    60,   # Evil Pillar
    63,   # Bone Head
    64,   # Fox Archer
    65,   # Fox Hunter
    77,   # Hyena
    78,   # Fishhead
    79,   # Dryad
    81,   # Brain Float
    83,   # Abiondarg
    86,   # Witch
    93,   # King Moth
    94,   # Killer Bee
    96,   # Lizard-man
    113,  # Devil Tower (Battle Arena)
    119,  # Bone Tower (Battle Arena)
    122,  # Bloody Sword (Battle Arena)
    133,  # Evil Pillar (Battle Arena)
]

bosses = [
    68,   # Cerberus
    76,   # Necromancer
    84,   # Iron Golem
    89,   # Adramelech
    95,   # Zombie Dragon
    100,  # Death
    101,  # Camilla
    102,  # Hugh
    103,  # Dracula I
]

candles = [
    136,  # Scary Candle
    137,  # Trick Candle
    80,   # Mimic Candle
]

NUMBER_ENEMIES = 141
NUMBER_ITEMS = 55

COUNTDOWN_TABLE_ADDR = 0x673400


def shuffle_sub_weapons(world: "CVCotMWorld") -> Dict[int, bytes]:
    """Shuffles the sub-weapons amongst themselves."""
    sub_bytes = list(rom_sub_weapon_offsets.values())
    world.random.shuffle(sub_bytes)
    return dict(zip(rom_sub_weapon_offsets, sub_bytes))


def get_countdown_flags(world: "CVCotMWorld", active_locations: Iterable[Location]) -> Dict[int, bytes]:
    """Figures out which Countdown numbers to increase for each Location after verifying the Item on the Location should
    count towards a number.

    The exact number to increase is determined by the Location's "countdown" key in the location_info dict."""

    next_pos = COUNTDOWN_TABLE_ADDR + 0x40
    countdown_flags = [[] for _ in range(16)]
    countdown_dict = {}
    ptr_offset = COUNTDOWN_TABLE_ADDR

    # Loop over every Location and add the correct flag values of all Useful and Progression-classified Items to the
    # array of flags the Countdown will track.
    for loc in active_locations:
        if (loc.item.advancement or loc.item.classification == ItemClassification.useful) and loc.address is not None:
            countdown_index = get_location_info(loc.name, "countdown")
            # If we're looking at a locally-placed DSS Card, take the card's parameter value for the flag.
            if (loc.item.player == world.player or (loc.item.player in world.multiworld.groups and world.player in
                                                    world.multiworld.groups[loc.item.player]['players'])) \
                    and "Card" in loc.item.name:
                countdown_flags[countdown_index] += [loc.item.code & 0xFF, 0x80]
            # Otherwise, just use the Location's address.
            else:
                countdown_flags[countdown_index] += [loc.address & 0xFF, 0]

    # Write the Countdown flag arrays and array pointers correctly. Each flag list should end with a 0xFFFF to indicate
    # the end of an area's list.
    for area_flags in countdown_flags:
        countdown_dict[ptr_offset] = int.to_bytes(next_pos | 0x08000000, 4, "little")
        countdown_dict[next_pos] = bytes(area_flags + [0xFF, 0xFF])
        ptr_offset += 4
        next_pos += len(area_flags) + 2

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


def populate_enemy_drops(world: "CVCotMWorld") -> Dict[int, bytes]:
    """Randomizes the enemy-dropped items throughout the game within each other. There are three tiers of drops: Easy,
    Common, and Rare. Easier enemies will only have Easy drops, bosses and candle enemies will be guaranteed to have
    Rare drops, and everything else can have Easy or Common items in its Common drop slot and any item in its Rare drop
    slot.

    If Item Drop Randomization is set to Hard, more enemies will be considered "easy" in addition to the ones that
    already are, and all Rare drops assigned to candles and bosses will be exclusive to them."""
    placed_easy_items = [0] * len(easy_items)
    placed_common_items = [0] * len(common_items)
    forced_rares = [0] * len(rare_items)

    regular_drops = [0] * NUMBER_ENEMIES
    regular_drop_chances = [0] * NUMBER_ENEMIES
    rare_drops = [0] * NUMBER_ENEMIES
    rare_drop_chances = [0] * NUMBER_ENEMIES

    # Set boss and candle items first to prevent boss drop duplicates.
    # If item hard mode is enabled, make these items exclusive to these enemies by adding an arbitrary integer larger
    # than could be reached normally (e.g.the total number of enemies).
    # Bosses
    for boss_id in bosses:
        regular_drops[boss_id] = select_drop(world, rare_items, forced_rares, True)

    # Candles
    for candle_id in candles:
        regular_drops[candle_id] = select_drop(world, rare_items, forced_rares, True)
        rare_drops[candle_id] = select_drop(world, rare_items, forced_rares, True)

    # Add the forced rare items onto the main placed rare items list.
    placed_rare_items = ([0] * len(common_items)) + forced_rares

    for i in range(NUMBER_ENEMIES):
        # Give Dracula II Shining Armor occasionally as a joke.
        if i == 104:
            regular_drops[i] = rare_drops[i] = 11
            regular_drop_chances[i] = rare_drop_chances[i] = 5000
        # Set bosses' secondary item to none since we already set the primary item earlier.
        elif i in bosses:
            # Set rare drop to none.
            rare_drops[i] = 0

            # Max out rare boss drops (normally, drops are hard capped to 50 % and 25 % respectively regardless of drop
            # rate, but fusecavator's patch AllowAlwaysDrop.ips allows setting the regular item drop chance to 10000 to
            # force a drop always).
            regular_drop_chances[i] = 10000
            rare_drop_chances[i] = 0

        # Trivially easy enemies that can be easily farmed AND we are NOT using the hard mode option
        # OR
        # We ARE using the hard mode option and the enemy is below 150 HP.
        elif (world.options.item_drop_randomization == ItemDropRandomization.option_normal and i in
              easily_farmable_enemies) or (world.options.item_drop_randomization == ItemDropRandomization.option_hard
                                           and i in below_150_hp_enemies):
            regular_drops[i] = select_drop(world, easy_items, placed_easy_items)
            rare_drops[i] = select_drop(world, easy_items, placed_easy_items)

            # Level 1 rate between 5-10 % and rare between 3-8%.
            regular_drop_chances[i] = 500 + world.random.randint(0, 500)
            rare_drop_chances[i] = 300 + world.random.randint(0, 500)

        # It is a "Candle" enemy.
        elif i in candles:
            # Set a regular drop chance between 20-30 % and a rare drop chance between 15-20%.
            regular_drop_chances[i] = 2000 + world.random.randint(0, 1000)
            rare_drop_chances[i] = 1500 + world.random.randint(0, 500)

        # Regular enemies
        else:
            # Select a random regular and rare drop for every enemy from their respective lists.
            regular_drops[i] = select_drop(world, common_items, placed_common_items)
            rare_drops[i] = select_drop(world, all_items, placed_rare_items)

            # Otherwise, set a regular drop chance between 5-10 % and a rare drop chance between 3-5%.
            regular_drop_chances[i] = 500 + world.random.randint(0, 500)
            rare_drop_chances[i] = 300 + world.random.randint(0, 200)

    # Return the randomized drop data as bytes with their respective offsets.
    enemy_address = 0xCB2C4
    drop_data = {}
    for i in range(NUMBER_ENEMIES):
        drop_data[enemy_address] = bytes([regular_drops[i], 0, regular_drop_chances[i] & 0xFF,
                                          regular_drop_chances[i] >> 8, rare_drops[i], 0, rare_drop_chances[i] & 0xFF,
                                          rare_drop_chances[i] >> 8])
        enemy_address += 20

    return drop_data


def select_drop(world: "CVCotMWorld", drop_list: List[int], drops_placed: List[int], exclusive_drop: bool = False) \
        -> int:
    """Chooses a drop from a given list of drops based on another given list of how many drops from that list were
    selected before. In order to ensure an even number of drops are distributed, drops that were selected the least are
    the ones that will be picked from.

    If Item Drop Randomization is set to Hard, calling this with True as the exclusive_drop param will force the number
    of the chosen item really high to ensure it will never be picked again."""

    number_valid_drops = 0
    eligible_items = [0] * NUMBER_ITEMS
    lowest_number = drops_placed[0]

    # Only make eligible drops which we have placed the least
    i = 0
    while i < len(drop_list):
        # A drop with the priority we are expecting is available to add as a candidate
        if drops_placed[i] == lowest_number:
            eligible_items[number_valid_drops] = i
            number_valid_drops += 1
            i += 1

        # If this condition is met, there is at least one item that hasn't been placed as many times as the others.
        # We have to lower the lowest number and start from the beginning of the loop to capture all the valid indices.
        elif drops_placed[i] < lowest_number:
            lowest_number = drops_placed[i]
            number_valid_drops = i = 0

        else:
            i += 1

    # Post-condition: Our array eligible_items has number_valid_drops many valid item indices as its elements

    # Select a random valid item from the index of valid choices
    random_result = world.random.randrange(number_valid_drops)

    # Increment the number of this item placed, unless it should be exclusive to the boss / candle, in which case
    # set it to an arbitrarily large number to make it exclusive (use NUMBER_ENEMIES for simplicity)
    if world.options.item_drop_randomization == ItemDropRandomization.option_hard and exclusive_drop:
        drops_placed[eligible_items[random_result]] += NUMBER_ENEMIES
    else:
        drops_placed[eligible_items[random_result]] += 1

    # Return the item ID
    return drop_list[eligible_items[random_result]]
