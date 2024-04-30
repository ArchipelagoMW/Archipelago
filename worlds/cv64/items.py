from BaseClasses import Item
from .data import iname
from .locations import base_id, get_location_info
from .options import DraculasCondition, SpareKeys

from typing import TYPE_CHECKING, Dict, Union

if TYPE_CHECKING:
    from . import CV64World

import math


class CV64Item(Item):
    game: str = "Castlevania 64"


# # #    KEY    # # #
# "code" = The unique part of the Item's AP code attribute, as well as the value to call the in-game "prepare item
#          textbox" function with to give the Item in-game. Add this + base_id to get the actual AP code.
# "default classification" = The AP Item Classification that gets assigned to instances of that Item in create_item
#                            by default, unless I deliberately override it (as is the case for some Special1s).
# "inventory offset" = What offset from the start of the in-game inventory array (beginning at 0x80389C4B) stores the
#                      current count for that Item. Used for start inventory purposes.
# "pickup actor id" = The ID for the Item's in-game Item pickup actor. If it's not in the Item's data dict, it's the
#                     same as the Item's code. This is what gets written in the ROM to replace non-NPC/shop items.
# "sub equip id" = For sub-weapons specifically, this is the number to put in the game's "current sub-weapon" value to
#                  indicate the player currently having that weapon. Used for start inventory purposes.
item_info = {
    # White jewel
    iname.red_jewel_s:        {"code": 0x02,  "default classification": "filler"},
    iname.red_jewel_l:        {"code": 0x03,  "default classification": "filler"},
    iname.special_one:        {"code": 0x04,  "default classification": "progression_skip_balancing",
                               "inventory offset": 0},
    iname.special_two:        {"code": 0x05,  "default classification": "progression_skip_balancing",
                               "inventory offset": 1},
    iname.roast_chicken:      {"code": 0x06,  "default classification": "filler", "inventory offset": 2},
    iname.roast_beef:         {"code": 0x07,  "default classification": "filler", "inventory offset": 3},
    iname.healing_kit:        {"code": 0x08,  "default classification": "useful", "inventory offset": 4},
    iname.purifying:          {"code": 0x09,  "default classification": "filler", "inventory offset": 5},
    iname.cure_ampoule:       {"code": 0x0A,  "default classification": "filler", "inventory offset": 6},
    # pot-pourri
    iname.powerup:            {"code": 0x0C,  "default classification": "filler"},
    iname.permaup:            {"code": 0x10C, "default classification": "useful", "pickup actor id": 0x0C,
                               "inventory offset": 8},
    iname.knife:              {"code": 0x0D,  "default classification": "filler", "pickup actor id": 0x10,
                               "sub equip id": 1},
    iname.holy_water:         {"code": 0x0E,  "default classification": "filler", "pickup actor id": 0x0D,
                               "sub equip id": 2},
    iname.cross:              {"code": 0x0F,  "default classification": "filler", "pickup actor id": 0x0E,
                               "sub equip id": 3},
    iname.axe:                {"code": 0x10,  "default classification": "filler", "pickup actor id": 0x0F,
                               "sub equip id": 4},
    # Wooden stake (AP item)
    iname.ice_trap:           {"code": 0x12,  "default classification": "trap"},
    # The contract
    # engagement ring
    iname.magical_nitro:      {"code": 0x15,  "default classification": "progression", "inventory offset": 17},
    iname.mandragora:         {"code": 0x16,  "default classification": "progression", "inventory offset": 18},
    iname.sun_card:           {"code": 0x17,  "default classification": "filler", "inventory offset": 19},
    iname.moon_card:          {"code": 0x18,  "default classification": "filler", "inventory offset": 20},
    # Incandescent gaze
    iname.archives_key:       {"code": 0x1A,  "default classification": "progression", "pickup actor id": 0x1D,
                               "inventory offset": 22},
    iname.left_tower_key:     {"code": 0x1B,  "default classification": "progression", "pickup actor id": 0x1E,
                               "inventory offset": 23},
    iname.storeroom_key:      {"code": 0x1C,  "default classification": "progression", "pickup actor id": 0x1F,
                               "inventory offset": 24},
    iname.garden_key:         {"code": 0x1D,  "default classification": "progression", "pickup actor id": 0x20,
                               "inventory offset": 25},
    iname.copper_key:         {"code": 0x1E,  "default classification": "progression", "pickup actor id": 0x21,
                               "inventory offset": 26},
    iname.chamber_key:        {"code": 0x1F,  "default classification": "progression", "pickup actor id": 0x22,
                               "inventory offset": 27},
    iname.execution_key:      {"code": 0x20,  "default classification": "progression", "pickup actor id": 0x23,
                               "inventory offset": 28},
    iname.science_key1:       {"code": 0x21,  "default classification": "progression", "pickup actor id": 0x24,
                               "inventory offset": 29},
    iname.science_key2:       {"code": 0x22,  "default classification": "progression", "pickup actor id": 0x25,
                               "inventory offset": 30},
    iname.science_key3:       {"code": 0x23,  "default classification": "progression", "pickup actor id": 0x26,
                               "inventory offset": 31},
    iname.clocktower_key1:    {"code": 0x24,  "default classification": "progression", "pickup actor id": 0x27,
                               "inventory offset": 32},
    iname.clocktower_key2:    {"code": 0x25,  "default classification": "progression", "pickup actor id": 0x28,
                               "inventory offset": 33},
    iname.clocktower_key3:    {"code": 0x26,  "default classification": "progression", "pickup actor id": 0x29,
                               "inventory offset": 34},
    iname.five_hundred_gold:  {"code": 0x27,  "default classification": "filler", "pickup actor id": 0x1A},
    iname.three_hundred_gold: {"code": 0x28,  "default classification": "filler", "pickup actor id": 0x1B},
    iname.one_hundred_gold:   {"code": 0x29,  "default classification": "filler", "pickup actor id": 0x1C},
    iname.crystal:            {"default classification": "progression"},
    iname.trophy:             {"default classification": "progression"},
    iname.victory:            {"default classification": "progression"}
}

filler_item_names = [iname.red_jewel_s, iname.red_jewel_l, iname.five_hundred_gold, iname.three_hundred_gold,
                     iname.one_hundred_gold]


def get_item_info(item: str, info: str) -> Union[str, int, None]:
    return item_info[item].get(info, None)


def get_item_names_to_ids() -> Dict[str, int]:
    return {name: get_item_info(name, "code")+base_id for name in item_info if get_item_info(name, "code") is not None}


def get_item_counts(world: "CV64World") -> Dict[str, Dict[str, int]]:

    active_locations = world.multiworld.get_unfilled_locations(world.player)

    item_counts = {
        "progression": {},
        "progression_skip_balancing": {},
        "useful": {},
        "filler": {},
        "trap": {}
    }
    total_items = 0
    extras_count = 0

    # Get from each location its vanilla item and add it to the default item counts.
    for loc in active_locations:
        if loc.address is None:
            continue

        if world.options.hard_item_pool and get_location_info(loc.name, "hard item") is not None:
            item_to_add = get_location_info(loc.name, "hard item")
        else:
            item_to_add = get_location_info(loc.name, "normal item")

        classification = get_item_info(item_to_add, "default classification")

        if item_to_add not in item_counts[classification]:
            item_counts[classification][item_to_add] = 1
        else:
            item_counts[classification][item_to_add] += 1
        total_items += 1

    # Replace all but 2 PowerUps with junk if Permanent PowerUps is on and mark those two PowerUps as Useful.
    if world.options.permanent_powerups:
        for i in range(item_counts["filler"][iname.powerup] - 2):
            item_counts["filler"][world.get_filler_item_name()] += 1
        del(item_counts["filler"][iname.powerup])
        item_counts["useful"][iname.permaup] = 2

    # Add the total Special1s.
    item_counts["progression_skip_balancing"][iname.special_one] = world.options.total_special1s.value
    extras_count += world.options.total_special1s.value

    # Add the total Special2s if Dracula's Condition is Special2s.
    if world.options.draculas_condition == DraculasCondition.option_specials:
        item_counts["progression_skip_balancing"][iname.special_two] = world.options.total_special2s.value
        extras_count += world.options.total_special2s.value

    # Determine the extra key counts if applicable. Doing this before moving Special1s will ensure only the keys and
    # bomb components are affected by this.
    for key in item_counts["progression"]:
        spare_keys = 0
        if world.options.spare_keys == SpareKeys.option_on:
            spare_keys = item_counts["progression"][key]
        elif world.options.spare_keys == SpareKeys.option_chance:
            if item_counts["progression"][key] > 0:
                for i in range(item_counts["progression"][key]):
                    spare_keys += world.random.randint(0, 1)
        item_counts["progression"][key] += spare_keys
        extras_count += spare_keys

    # Move the total number of Special1s needed to warp everywhere to normal progression balancing if S1s per warp is
    # 3 or lower.
    if world.s1s_per_warp <= 3:
        item_counts["progression_skip_balancing"][iname.special_one] -= world.s1s_per_warp * 7
        item_counts["progression"][iname.special_one] = world.s1s_per_warp * 7

    # Determine the total amounts of replaceable filler and non-filler junk.
    total_filler_junk = 0
    total_non_filler_junk = 0
    for junk in item_counts["filler"]:
        if junk in filler_item_names:
            total_filler_junk += item_counts["filler"][junk]
        else:
            total_non_filler_junk += item_counts["filler"][junk]

    # Subtract from the filler counts total number of "extra" items we've added. get_filler_item_name() filler will be
    # subtracted from first until we run out of that, at which point we'll start subtracting from the rest. At this
    # moment, non-filler item name filler cannot run out no matter the settings, so I haven't bothered adding handling
    # for when it does yet.
    available_filler_junk = filler_item_names.copy()
    for i in range(extras_count):
        if total_filler_junk > 0:
            total_filler_junk -= 1
            item_to_subtract = world.random.choice(available_filler_junk)
        else:
            total_non_filler_junk -= 1
            item_to_subtract = world.random.choice(list(item_counts["filler"].keys()))

        item_counts["filler"][item_to_subtract] -= 1
        if item_counts["filler"][item_to_subtract] == 0:
            del(item_counts["filler"][item_to_subtract])
            if item_to_subtract in available_filler_junk:
                available_filler_junk.remove(item_to_subtract)

    # Determine the Ice Trap count by taking a certain % of the total filler remaining at this point.
    item_counts["trap"][iname.ice_trap] = math.floor((total_filler_junk + total_non_filler_junk) *
                                                     (world.options.ice_trap_percentage.value / 100.0))
    for i in range(item_counts["trap"][iname.ice_trap]):
        # Subtract the remaining filler after determining the ice trap count.
        item_to_subtract = world.random.choice(list(item_counts["filler"].keys()))
        item_counts["filler"][item_to_subtract] -= 1
        if item_counts["filler"][item_to_subtract] == 0:
            del (item_counts["filler"][item_to_subtract])

    return item_counts
