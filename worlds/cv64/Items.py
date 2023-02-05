import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemName


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    quantity: int = 1


class CV64Item(Item):
    game: str = "Castlevania 64"
    item_byte = int


# Separate tables for each type of item.
junk_table = {
    ItemName.red_jewel_s:        ItemData(0xC64002, False),
    ItemName.red_jewel_l:        ItemData(0xC64003, False),
    ItemName.five_hundred_gold:  ItemData(0xC6401A, False),
    ItemName.three_hundred_gold: ItemData(0xC6401B, False),
    ItemName.one_hundred_gold:   ItemData(0xC6401C, False),
}

special_table = {
    ItemName.special_one: ItemData(0xC64004, True),
    ItemName.special_two: ItemData(0xC64005, True, 0),
}

main_table = {
    ItemName.roast_chicken:        ItemData(0xC64006, False, 21),
    ItemName.roast_beef:           ItemData(0xC64007, False, 24),
    ItemName.healing_kit:          ItemData(0xC64008, False, 4),
    ItemName.purifying:            ItemData(0xC64009, False, 14),
    ItemName.cure_ampoule:         ItemData(0xC6400A, False, 5),
    ItemName.powerup:              ItemData(0xC6400C, False, 10),
    ItemName.magical_nitro:        ItemData(0xC64015, True, 2),
    ItemName.mandragora:           ItemData(0xC64016, True, 2),
    ItemName.sun_card:             ItemData(0xC64017, False, 9),
    ItemName.moon_card:            ItemData(0xC64018, False, 8),
    ItemName.five_hundred_gold:    ItemData(0xC6401A, False),
    ItemName.archives_key:         ItemData(0xC6401D, True),
    ItemName.left_tower_key:       ItemData(0xC6401E, True),
    ItemName.storeroom_key:        ItemData(0xC6401F, True),
    ItemName.garden_key:           ItemData(0xC64020, True),
    ItemName.copper_key:           ItemData(0xC64021, True),
    ItemName.chamber_key:          ItemData(0xC64022, True),
    ItemName.execution_key:        ItemData(0xC64023, True),
    ItemName.science_key_one:      ItemData(0xC64024, True),
    ItemName.science_key_two:      ItemData(0xC64025, True),
    ItemName.science_key_three:    ItemData(0xC64026, True),
    ItemName.clocktower_key_one:   ItemData(0xC64027, True),
    ItemName.clocktower_key_two:   ItemData(0xC64028, True),
    ItemName.clocktower_key_three: ItemData(0xC64029, True),
}

event_table = {
    ItemName.victory:          ItemData(None, True, 0),
}

# Complete item table.
item_table = {
    **junk_table,
    **special_table,
    **main_table,
    **event_table,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
