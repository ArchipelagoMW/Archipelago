import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemName


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    quantity: int = 1
    event: bool = False


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

main_table = {
    ItemName.special_one:          ItemData(0xC64004, True),
    ItemName.special_two:          ItemData(0xC64005, True),
    ItemName.roast_chicken:        ItemData(0xC64006, False),
    ItemName.roast_beef:           ItemData(0xC64007, False),
    ItemName.healing_kit:          ItemData(0xC64008, True),
    ItemName.purifying:            ItemData(0xC64009, False),
    ItemName.cure_ampoule:         ItemData(0xC6400A, False),
    ItemName.powerup:              ItemData(0xC6400C, False),
    ItemName.magical_nitro:        ItemData(0xC64015, True),
    ItemName.mandragora:           ItemData(0xC64016, True),
    ItemName.sun_card:             ItemData(0xC64017, False),
    ItemName.moon_card:            ItemData(0xC64018, False),
    ItemName.left_tower_key:       ItemData(0xC6401E, True),
    ItemName.storeroom_key:        ItemData(0xC6401E, True),
    ItemName.archives_key:         ItemData(0xC6401E, True),
    ItemName.garden_key:           ItemData(0xC6401E, True),
    ItemName.copper_key:           ItemData(0xC6401E, True),
    ItemName.chamber_key:          ItemData(0xC6401E, True),
    ItemName.execution_key:        ItemData(0xC6401E, True),
    ItemName.science_key_one:      ItemData(0xC6401E, True),
    ItemName.science_key_two:      ItemData(0xC6401E, True),
    ItemName.science_key_three:    ItemData(0xC6401E, True),
    ItemName.clocktower_key_one:   ItemData(0xC6401E, True),
    ItemName.clocktower_key_two:   ItemData(0xC6401E, True),
    ItemName.clocktower_key_three: ItemData(0xC6401E, True),
}

event_table = {
    ItemName.victory: ItemData(0xC64000, True),
}

# Complete item table.
item_table = {
    **junk_table,
    **main_table,
    **event_table,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
