import typing

from BaseClasses import Item
from .Names import IName


class CV64Item(Item):
    game: str = "Castlevania 64"
    item_byte = int


# Separate tables for each type of item.
tier1_junk_table = {
    IName.red_jewel_s:        0xC64002,
    IName.red_jewel_l:        0xC64003,
    IName.five_hundred_gold:  0xC6401A,
    IName.three_hundred_gold: 0xC6401B,
    IName.one_hundred_gold:   0xC6401C
}

tier2_junk_table = {
    IName.roast_chicken:        0xC64006,
    IName.roast_beef:           0xC64007,
    IName.healing_kit:          0xC64008,
    IName.purifying:            0xC64009,
    IName.cure_ampoule:         0xC6400A,
    IName.powerup:              0xC6400C,
    IName.sun_card:             0xC64017,
    IName.moon_card:            0xC64018
}

key_table = {
    IName.magical_nitro:        0xC64015,
    IName.mandragora:           0xC64016,
    IName.archives_key:         0xC6401D,
    IName.left_tower_key:       0xC6401E,
    IName.storeroom_key:        0xC6401F,
    IName.garden_key:           0xC64020,
    IName.copper_key:           0xC64021,
    IName.chamber_key:          0xC64022,
    IName.execution_key:        0xC64023,
    IName.science_key_one:      0xC64024,
    IName.science_key_two:      0xC64025,
    IName.science_key_three:    0xC64026,
    IName.clocktower_key_one:   0xC64027,
    IName.clocktower_key_two:   0xC64028,
    IName.clocktower_key_three: 0xC64029,
    IName.victory:              None
}

special_table = {
    IName.special_one: 0xC64004,
    IName.special_two: 0xC64005
}

sub_weapon_table = {
    IName.holy_water: 0xC6400D,
    IName.cross:      0xC6400E,
    IName.axe:        0xC6400F,
    IName.knife:      0xC64010
}

# Complete item table.
item_table = {
    **tier1_junk_table,
    **tier2_junk_table,
    **key_table,
    **special_table,
    **sub_weapon_table
}

lookup_id_to_name: typing.Dict[int, str] = {code: item_name for item_name, code in item_table.items() if code}
