import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemName


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    trap: bool = False
    quantity: int = 1

STARTING_ID = 0xBE0C00

class MMX2Item(Item):
    game = "Mega Man X2"

# Item tables
event_table = {
    ItemName.victory:           ItemData(STARTING_ID + 0x00, True),
    ItemName.maverick_medal:    ItemData(STARTING_ID + 0x01, True),
}

access_codes_table = {
    ItemName.stage_wheel_gator:         ItemData(STARTING_ID + 0x02, True),
    ItemName.stage_bubble_crab:         ItemData(STARTING_ID + 0x03, True),
    ItemName.stage_flame_stag:          ItemData(STARTING_ID + 0x04, True),
    ItemName.stage_morph_moth:          ItemData(STARTING_ID + 0x05, True),
    ItemName.stage_magna_centipede:     ItemData(STARTING_ID + 0x06, True),
    ItemName.stage_crystal_snail:       ItemData(STARTING_ID + 0x07, True),
    ItemName.stage_overdrive_ostrich:   ItemData(STARTING_ID + 0x08, True),
    ItemName.stage_wire_sponge:         ItemData(STARTING_ID + 0x09, True),
    ItemName.stage_x_hunter:            ItemData(STARTING_ID + 0x0A, True),
    ItemName.stage_sigma:               ItemData(STARTING_ID + 0x35, True),
}

weapons = {
    ItemName.spin_wheel:        ItemData(STARTING_ID + 0x0B, True),
    ItemName.bubble_splash:     ItemData(STARTING_ID + 0x0C, True),
    ItemName.speed_burner:      ItemData(STARTING_ID + 0x0D, True),
    ItemName.silk_shot:         ItemData(STARTING_ID + 0x0E, True),
    ItemName.magnet_mine:       ItemData(STARTING_ID + 0x0F, True),
    ItemName.crystal_hunter:    ItemData(STARTING_ID + 0x10, True),
    ItemName.sonic_slicer:      ItemData(STARTING_ID + 0x11, True),
    ItemName.strike_chain:      ItemData(STARTING_ID + 0x12, True),
    ItemName.shoryuken:         ItemData(STARTING_ID + 0x1A, True),
}

tanks_table = {
    ItemName.heart_tank:        ItemData(STARTING_ID + 0x13, True),
    ItemName.sub_tank:          ItemData(STARTING_ID + 0x14, True),
}

armor_table = {
    ItemName.helmet:    ItemData(STARTING_ID + 0x1C, True), 
    ItemName.body:      ItemData(STARTING_ID + 0x1D, True), 
    ItemName.arms:      ItemData(STARTING_ID + 0x1E, True), 
    ItemName.legs:      ItemData(STARTING_ID + 0x1F, True), 
}

junk_table = {
    ItemName.small_hp:      ItemData(STARTING_ID + 0x30, False),
    ItemName.large_hp:      ItemData(STARTING_ID + 0x31, False),
    ItemName.life:          ItemData(STARTING_ID + 0x34, False),
}

item_groups = {
    "Weapons": {
        ItemName.spin_wheel,
        ItemName.bubble_splash,
        ItemName.speed_burner,
        ItemName.silk_shot,
        ItemName.magnet_mine,
        ItemName.crystal_hunter,
        ItemName.sonic_slicer,
        ItemName.strike_chain,
    },
    "Armor Upgrades": {
        ItemName.helmet,
        ItemName.body,
        ItemName.arms,
        ItemName.legs,
    },
    "Access Codes": {
        ItemName.stage_wheel_gator,
        ItemName.stage_bubble_crab,
        ItemName.stage_flame_stag,
        ItemName.stage_morph_moth,
        ItemName.stage_magna_centipede,
        ItemName.stage_crystal_snail,
        ItemName.stage_overdrive_ostrich,
        ItemName.stage_wire_sponge,
        ItemName.stage_x_hunter,
    }
}

# Complete item table.
item_table = {
    **event_table,
    **access_codes_table,
    **weapons,
    **tanks_table,
    **armor_table,
    **junk_table,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}