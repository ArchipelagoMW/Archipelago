import typing

from BaseClasses import Item
from .Names import IName


class CV64Item(Item):
    game: str = "Castlevania 64"
    item_byte = int


# Separate tables for each type of item.
filler_junk_table = {
    IName.red_jewel_s:        0x02,
    IName.red_jewel_l:        0x03,
    IName.five_hundred_gold:  0x27,
    IName.three_hundred_gold: 0x28,
    IName.one_hundred_gold:   0x29
}

non_filler_junk_table = {
    IName.roast_chicken:        0x06,
    IName.roast_beef:           0x07,
    IName.purifying:            0x09,
    IName.cure_ampoule:         0x0A,
    IName.powerup:              0x0C,
    IName.sun_card:             0x17,
    IName.moon_card:            0x18
}

useful_table = {
    IName.healing_kit: 0x08,
    IName.permaup:     0x10C
}

key_table = {
    IName.magical_nitro:        0x15,
    IName.mandragora:           0x16,
    IName.archives_key:         0x1A,
    IName.left_tower_key:       0x1B,
    IName.storeroom_key:        0x1C,
    IName.garden_key:           0x1D,
    IName.copper_key:           0x1E,
    IName.chamber_key:          0x1F,
    IName.execution_key:        0x20,
    IName.science_key_one:      0x21,
    IName.science_key_two:      0x22,
    IName.science_key_three:    0x23,
    IName.clocktower_key_one:   0x24,
    IName.clocktower_key_two:   0x25,
    IName.clocktower_key_three: 0x26
}

special_table = {
    IName.special_one: 0x04,
    IName.special_two: 0x05
}

sub_weapon_table = {
    IName.knife:      0x0D,
    IName.holy_water: 0x0E,
    IName.cross:      0x0F,
    IName.axe:        0x10
}

trap_table = {
    IName.ice_trap: 0x12
}

# Every in-game item pickup actor that has a different ID from its actual item code.
pickup_item_discrepancies = {
    IName.permaup:              0x0C,
    IName.holy_water:           0x0D,
    IName.cross:                0x0E,
    IName.axe:                  0x0F,
    IName.knife:                0x10,
    IName.archives_key:         0x1D,
    IName.left_tower_key:       0x1E,
    IName.storeroom_key:        0x1F,
    IName.garden_key:           0x20,
    IName.copper_key:           0x21,
    IName.chamber_key:          0x22,
    IName.execution_key:        0x23,
    IName.science_key_one:      0x24,
    IName.science_key_two:      0x25,
    IName.science_key_three:    0x26,
    IName.clocktower_key_one:   0x27,
    IName.clocktower_key_two:   0x28,
    IName.clocktower_key_three: 0x29,
    IName.five_hundred_gold:    0x1A,
    IName.three_hundred_gold:   0x1B,
    IName.one_hundred_gold:     0x1C
}

# Every inventory item's offset in the inventory array, starting at 0x80389C4B. Used to write start_inventory.
inventory_item_offsets = {
    IName.special_one:          0,
    IName.special_two:          1,
    IName.roast_chicken:        2,
    IName.roast_beef:           3,
    IName.healing_kit:          4,
    IName.purifying:            5,
    IName.cure_ampoule:         6,
    # IName.pot_pourri:           7,
    IName.permaup:              8,
    # IName.the_contract:         15,
    # IName.engagement_ring:      16,
    IName.magical_nitro:        17,
    IName.mandragora:           18,
    IName.sun_card:             19,
    IName.moon_card:            20,
    # IName.incandescent_gaze:    21,
    IName.archives_key:         22,
    IName.left_tower_key:       23,
    IName.storeroom_key:        24,
    IName.garden_key:           25,
    IName.copper_key:           26,
    IName.chamber_key:          27,
    IName.execution_key:        28,
    IName.science_key_one:      29,
    IName.science_key_two:      30,
    IName.science_key_three:    31,
    IName.clocktower_key_one:   32,
    IName.clocktower_key_two:   33,
    IName.clocktower_key_three: 34
}

# Every sub-weapon's ID when currently equipped. For start_inventory.
sub_weapon_ids = {
    IName.knife:        1,
    IName.holy_water:   2,
    IName.cross:        3,
    IName.axe:          4
}

# Complete item table.
item_table = {
    **filler_junk_table,
    **non_filler_junk_table,
    **useful_table,
    **key_table,
    **special_table,
    **trap_table,
    **sub_weapon_table
}

lookup_id_to_name: typing.Dict[int, str] = {code: item_name for item_name, code in item_table.items() if code}
