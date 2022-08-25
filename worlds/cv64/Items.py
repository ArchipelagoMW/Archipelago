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
    ItemName.special_one:    ItemData(0xC64004, True),
    ItemName.roast_beef:     ItemData(0xC64007, False),
    ItemName.powerup:        ItemData(0xC6400C, False),
    ItemName.sun_card:       ItemData(0xC64017, False),
    ItemName.moon_card:      ItemData(0xC64018, False),
    ItemName.left_tower_key: ItemData(0xC6401E, True),
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
