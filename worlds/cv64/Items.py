import typing

from BaseClasses import Item
from .Names import IName


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool


class CV64Item(Item):
    game: str = "Castlevania 64"
    item_byte = int


# Separate tables for each type of item.
tier1_junk_table = {
    IName.red_jewel_s:        ItemData(0xC64002, False),
    IName.red_jewel_l:        ItemData(0xC64003, False),
    IName.five_hundred_gold:  ItemData(0xC6401A, False),
    IName.three_hundred_gold: ItemData(0xC6401B, False),
    IName.one_hundred_gold:   ItemData(0xC6401C, False),
}

tier2_junk_table = {
    IName.roast_chicken:        ItemData(0xC64006, False),
    IName.roast_beef:           ItemData(0xC64007, False),
    IName.healing_kit:          ItemData(0xC64008, False),
    IName.purifying:            ItemData(0xC64009, False),
    IName.cure_ampoule:         ItemData(0xC6400A, False),
    IName.powerup:              ItemData(0xC6400C, False),
    IName.sun_card:             ItemData(0xC64017, False),
    IName.moon_card:            ItemData(0xC64018, False),
}

key_table = {
    IName.magical_nitro:        ItemData(0xC64015, True),
    IName.mandragora:           ItemData(0xC64016, True),
    IName.archives_key:         ItemData(0xC6401D, True),
    IName.left_tower_key:       ItemData(0xC6401E, True),
    IName.storeroom_key:        ItemData(0xC6401F, True),
    IName.garden_key:           ItemData(0xC64020, True),
    IName.copper_key:           ItemData(0xC64021, True),
    IName.chamber_key:          ItemData(0xC64022, True),
    IName.execution_key:        ItemData(0xC64023, True),
    IName.science_key_one:      ItemData(0xC64024, True),
    IName.science_key_two:      ItemData(0xC64025, True),
    IName.science_key_three:    ItemData(0xC64026, True),
    IName.clocktower_key_one:   ItemData(0xC64027, True),
    IName.clocktower_key_two:   ItemData(0xC64028, True),
    IName.clocktower_key_three: ItemData(0xC64029, True),
}

special_table = {
    IName.special_one: ItemData(0xC64004, True),
    IName.special_two: ItemData(0xC64005, True),
}

event_table = {
    IName.victory:          ItemData(None, True),
}

# Complete item table.
item_table = {
    **tier1_junk_table,
    **tier2_junk_table,
    **special_table,
    **key_table,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
