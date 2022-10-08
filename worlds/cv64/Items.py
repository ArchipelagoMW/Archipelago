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
    ItemName.victory:          ItemData(0xC64000, True),
    ItemName.bone_mom_one:     ItemData(0xC640B0, True),
    ItemName.bone_mom_two:     ItemData(0xC640B1, True),
    ItemName.forest_weretiger: ItemData(0xC640B2, True),
    ItemName.w_dragons:        ItemData(0xC640B3, True),
    ItemName.vamp_couple:      ItemData(0xC640B4, True),
    ItemName.behemoth:         ItemData(0xC640B5, True),
    ItemName.rosamilla:        ItemData(0xC640B6, True),
    ItemName.werejaguar:       ItemData(0xC640B7, True),
    ItemName.werewolf:         ItemData(0xC640B8, True),
    ItemName.werebull:         ItemData(0xC640B9, True),
    ItemName.weretiger:        ItemData(0xC640BA, True),
    ItemName.deathtrice:       ItemData(0xC640BB, True),
    ItemName.crystal:          ItemData(0xC640C0, True),
}

# Complete item table.
item_table = {
    **junk_table,
    **main_table,
    **event_table,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
