import typing

from BaseClasses import Item, ItemClassification
from worlds.AutoWorld import World
from .Names import ItemName

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    trap: bool = False
    quantity: int = 1

STARTING_ID = 0xBE0800

class MMXItem(Item):
    game = "Mega Man X"

# Item tables
event_table = {
    ItemName.victory:           ItemData(STARTING_ID + 0x0000, True),
    ItemName.maverick_medal:    ItemData(STARTING_ID + 0x0001, True),
}

access_codes_table = {
    ItemName.stage_armored_armadillo:   ItemData(STARTING_ID + 0x0002, True),
    ItemName.stage_boomer_kuwanger:     ItemData(STARTING_ID + 0x0003, True),
    ItemName.stage_chill_penguin:       ItemData(STARTING_ID + 0x0004, True),
    ItemName.stage_flame_mammoth:       ItemData(STARTING_ID + 0x0005, True),
    ItemName.stage_launch_octopus:      ItemData(STARTING_ID + 0x0006, True),
    ItemName.stage_spark_mandrill:      ItemData(STARTING_ID + 0x0007, True),
    ItemName.stage_sting_chameleon:     ItemData(STARTING_ID + 0x0008, True),
    ItemName.stage_storm_eagle:         ItemData(STARTING_ID + 0x0009, True),
    ItemName.stage_sigma_fortress:      ItemData(STARTING_ID + 0x000A, True),
}

weapons = {
    ItemName.shotgun_ice:       ItemData(STARTING_ID + 0x000B, True),
    ItemName.electric_spark:    ItemData(STARTING_ID + 0x000C, True),
    ItemName.rolling_shield:    ItemData(STARTING_ID + 0x000D, True),
    ItemName.homing_torpedo:    ItemData(STARTING_ID + 0x000E, True),
    ItemName.boomerang_cutter:  ItemData(STARTING_ID + 0x000F, True),
    ItemName.chameleon_sting:   ItemData(STARTING_ID + 0x0010, True),
    ItemName.storm_tornado:     ItemData(STARTING_ID + 0x0011, True),
    ItemName.fire_wave:         ItemData(STARTING_ID + 0x0012, True),
}

special_weapons = {
    ItemName.hadouken:          ItemData(STARTING_ID + 0x001A, True)
}

tanks_table = {
    ItemName.heart_tank:        ItemData(STARTING_ID + 0x0013, True),
    ItemName.sub_tank:          ItemData(STARTING_ID + 0x0014, True),
}

upgrade_table = {
    ItemName.helmet:    ItemData(STARTING_ID + 0x001C, True), 
    ItemName.body:      ItemData(STARTING_ID + 0x001D, True), 
    ItemName.arms:      ItemData(STARTING_ID + 0x001E, True), 
    ItemName.legs:      ItemData(STARTING_ID + 0x001F, True), 
}

junk_table = {
    ItemName.small_hp:      ItemData(STARTING_ID + 0x0030, False),
    ItemName.large_hp:      ItemData(STARTING_ID + 0x0031, False),
    ItemName.life:          ItemData(STARTING_ID + 0x0034, False),
}

junk_weapon_table = {
    ItemName.small_weapon:  ItemData(STARTING_ID + 0x0032, False), 
    ItemName.large_weapon:  ItemData(STARTING_ID + 0x0033, False), 
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
    **special_weapons,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}