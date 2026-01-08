import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemName


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classsification: ItemClassification
    quantity: int = 1

STARTING_ID = 0xBE0C00

class MMX2Item(Item):
    game = "Mega Man X2"

# Item tables
event_table = {
    ItemName.victory:           ItemData(STARTING_ID + 0x00, ItemClassification.progression_skip_balancing | ItemClassification.useful),
    ItemName.maverick_medal:    ItemData(STARTING_ID + 0x01, ItemClassification.progression_skip_balancing),
}

access_codes_table = {
    ItemName.stage_wheel_gator:         ItemData(STARTING_ID + 0x02, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_bubble_crab:         ItemData(STARTING_ID + 0x03, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_flame_stag:          ItemData(STARTING_ID + 0x04, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_morph_moth:          ItemData(STARTING_ID + 0x05, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_magna_centipede:     ItemData(STARTING_ID + 0x06, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_crystal_snail:       ItemData(STARTING_ID + 0x07, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_overdrive_ostrich:   ItemData(STARTING_ID + 0x08, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_wire_sponge:         ItemData(STARTING_ID + 0x09, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_x_hunter:            ItemData(STARTING_ID + 0x0A, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_sigma:               ItemData(STARTING_ID + 0x35, ItemClassification.progression | ItemClassification.useful),
}

weapons = {
    ItemName.spin_wheel:        ItemData(STARTING_ID + 0x0B, ItemClassification.progression),
    ItemName.bubble_splash:     ItemData(STARTING_ID + 0x0C, ItemClassification.progression),
    ItemName.speed_burner:      ItemData(STARTING_ID + 0x0D, ItemClassification.progression),
    ItemName.silk_shot:         ItemData(STARTING_ID + 0x0E, ItemClassification.progression),
    ItemName.magnet_mine:       ItemData(STARTING_ID + 0x0F, ItemClassification.progression),
    ItemName.crystal_hunter:    ItemData(STARTING_ID + 0x10, ItemClassification.progression),
    ItemName.sonic_slicer:      ItemData(STARTING_ID + 0x11, ItemClassification.progression),
    ItemName.strike_chain:      ItemData(STARTING_ID + 0x12, ItemClassification.progression),
    ItemName.shoryuken:         ItemData(STARTING_ID + 0x1A, ItemClassification.useful),
}

tanks_table = {
    ItemName.heart_tank:        ItemData(STARTING_ID + 0x13, ItemClassification.progression),
    ItemName.sub_tank:          ItemData(STARTING_ID + 0x14, ItemClassification.progression),
}

armor_table = {
    ItemName.helmet:    ItemData(STARTING_ID + 0x1C, ItemClassification.progression),
    ItemName.body:      ItemData(STARTING_ID + 0x1D, ItemClassification.progression),
    ItemName.arms:      ItemData(STARTING_ID + 0x1E, ItemClassification.progression),
    ItemName.legs:      ItemData(STARTING_ID + 0x1F, ItemClassification.progression),
}

junk_table = {
    ItemName.small_hp:      ItemData(STARTING_ID + 0x30, ItemClassification.filler),
    ItemName.large_hp:      ItemData(STARTING_ID + 0x31, ItemClassification.filler),
    ItemName.life:          ItemData(STARTING_ID + 0x34, ItemClassification.filler),
}

enhancements_table = {
    ItemName.chip_quick_charge:        ItemData(STARTING_ID + 0x40, ItemClassification.useful),
    ItemName.chip_speedster:           ItemData(STARTING_ID + 0x41, ItemClassification.useful),
    ItemName.chip_super_recover:       ItemData(STARTING_ID + 0x42, ItemClassification.useful),
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
    **enhancements_table,
    **junk_table,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}