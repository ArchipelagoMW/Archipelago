import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemName

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classsification: ItemClassification
    quantity: int = 1

STARTING_ID = 0xBE0800

class MMXItem(Item):
    game = "Mega Man X"

# Item tables
event_table = {
    ItemName.victory:           ItemData(STARTING_ID + 0x0000, ItemClassification.progression_skip_balancing | ItemClassification.useful),
    ItemName.maverick_medal:    ItemData(STARTING_ID + 0x0001, ItemClassification.progression_skip_balancing),
}

access_codes_table = {
    ItemName.stage_armored_armadillo:   ItemData(STARTING_ID + 0x0002, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_boomer_kuwanger:     ItemData(STARTING_ID + 0x0003, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_chill_penguin:       ItemData(STARTING_ID + 0x0004, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_flame_mammoth:       ItemData(STARTING_ID + 0x0005, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_launch_octopus:      ItemData(STARTING_ID + 0x0006, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_spark_mandrill:      ItemData(STARTING_ID + 0x0007, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_sting_chameleon:     ItemData(STARTING_ID + 0x0008, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_storm_eagle:         ItemData(STARTING_ID + 0x0009, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_sigma_fortress:      ItemData(STARTING_ID + 0x000A, ItemClassification.progression | ItemClassification.useful),
}

weapons = {
    ItemName.shotgun_ice:       ItemData(STARTING_ID + 0x000B, ItemClassification.progression),
    ItemName.electric_spark:    ItemData(STARTING_ID + 0x000C, ItemClassification.progression),
    ItemName.rolling_shield:    ItemData(STARTING_ID + 0x000D, ItemClassification.progression),
    ItemName.homing_torpedo:    ItemData(STARTING_ID + 0x000E, ItemClassification.progression),
    ItemName.boomerang_cutter:  ItemData(STARTING_ID + 0x000F, ItemClassification.progression),
    ItemName.chameleon_sting:   ItemData(STARTING_ID + 0x0010, ItemClassification.progression),
    ItemName.storm_tornado:     ItemData(STARTING_ID + 0x0011, ItemClassification.progression),
    ItemName.fire_wave:         ItemData(STARTING_ID + 0x0012, ItemClassification.progression),
}

special_weapons = {
    ItemName.hadouken:          ItemData(STARTING_ID + 0x001A, ItemClassification.useful),
}

tanks_table = {
    ItemName.heart_tank:        ItemData(STARTING_ID + 0x0013, ItemClassification.progression),
    ItemName.sub_tank:          ItemData(STARTING_ID + 0x0014, ItemClassification.progression),
}

upgrade_table = {
    ItemName.helmet:    ItemData(STARTING_ID + 0x001C, ItemClassification.progression),
    ItemName.body:      ItemData(STARTING_ID + 0x001D, ItemClassification.progression),
    ItemName.arms:      ItemData(STARTING_ID + 0x001E, ItemClassification.progression),
    ItemName.legs:      ItemData(STARTING_ID + 0x001F, ItemClassification.progression),
}

junk_table = {
    ItemName.small_hp:      ItemData(STARTING_ID + 0x0030, ItemClassification.filler),
    ItemName.large_hp:      ItemData(STARTING_ID + 0x0031, ItemClassification.filler),
    ItemName.life:          ItemData(STARTING_ID + 0x0034, ItemClassification.filler),
}

junk_weapon_table = {
    ItemName.small_weapon:  ItemData(STARTING_ID + 0x0032, ItemClassification.filler),
    ItemName.large_weapon:  ItemData(STARTING_ID + 0x0033, ItemClassification.filler),
}

enhancements_table = {
    ItemName.chip_quick_charge:        ItemData(STARTING_ID + 0x40, ItemClassification.useful),
    ItemName.chip_speedster:           ItemData(STARTING_ID + 0x41, ItemClassification.useful),
    ItemName.chip_super_recover:       ItemData(STARTING_ID + 0x42, ItemClassification.useful),
}

item_groups = {
    "Weapons": {
        ItemName.shotgun_ice,
        ItemName.electric_spark,
        ItemName.rolling_shield,
        ItemName.homing_torpedo,
        ItemName.boomerang_cutter,
        ItemName.chameleon_sting,
        ItemName.storm_tornado,
        ItemName.fire_wave,
    },
    "Armor Upgrades": {
        ItemName.helmet,
        ItemName.body,
        ItemName.arms,
        ItemName.legs,
    },
    "Access Codes": {
        ItemName.stage_armored_armadillo,
        ItemName.stage_boomer_kuwanger,
        ItemName.stage_chill_penguin,
        ItemName.stage_flame_mammoth,
        ItemName.stage_launch_octopus,
        ItemName.stage_spark_mandrill,
        ItemName.stage_sting_chameleon,
        ItemName.stage_storm_eagle,
        ItemName.stage_sigma_fortress,
    }
}

item_table = {
    **event_table,
    **access_codes_table,
    **weapons,
    **upgrade_table,
    **tanks_table,
    **junk_table,
    **junk_weapon_table,
    **enhancements_table,
    **special_weapons,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}