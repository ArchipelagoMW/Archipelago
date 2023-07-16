import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemName
from worlds.alttp import ALTTPWorld


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    trap: bool = False
    quantity: int = 1
    event: bool = False


class SA2BItem(Item):
    game: str = "Sonic Adventure 2: Battle"

    def __init__(self, name, classification: ItemClassification, code: int = None, player: int = None):
        super(SA2BItem, self).__init__(name, classification, code, player)


# Separate tables for each type of item.
emblems_table = {
    ItemName.emblem:  ItemData(0xFF0000, True),
}

upgrades_table = {
    ItemName.sonic_gloves:          ItemData(0xFF0001, False),
    ItemName.sonic_light_shoes:     ItemData(0xFF0002, True),
    ItemName.sonic_ancient_light:   ItemData(0xFF0003, False),
    ItemName.sonic_bounce_bracelet: ItemData(0xFF0004, True),
    ItemName.sonic_flame_ring:      ItemData(0xFF0005, True),
    ItemName.sonic_mystic_melody:   ItemData(0xFF0006, True),
    
    ItemName.tails_laser_blaster: ItemData(0xFF0007, False),
    ItemName.tails_booster:       ItemData(0xFF0008, True),
    ItemName.tails_mystic_melody: ItemData(0xFF0009, True),
    ItemName.tails_bazooka:       ItemData(0xFF000A, True),

    ItemName.knuckles_mystic_melody: ItemData(0xFF000B, True),
    ItemName.knuckles_shovel_claws:  ItemData(0xFF000C, True),
    ItemName.knuckles_air_necklace:  ItemData(0xFF000D, True),
    ItemName.knuckles_hammer_gloves: ItemData(0xFF000E, True),
    ItemName.knuckles_sunglasses:    ItemData(0xFF000F, True),
    
    ItemName.shadow_flame_ring:    ItemData(0xFF0010, True),
    ItemName.shadow_air_shoes:     ItemData(0xFF0011, True),
    ItemName.shadow_ancient_light: ItemData(0xFF0012, False),
    ItemName.shadow_mystic_melody: ItemData(0xFF0013, True),
    
    ItemName.eggman_laser_blaster:    ItemData(0xFF0014, False),
    ItemName.eggman_mystic_melody:    ItemData(0xFF0015, True),
    ItemName.eggman_jet_engine:       ItemData(0xFF0016, True),
    ItemName.eggman_large_cannon:     ItemData(0xFF0017, True),
    ItemName.eggman_protective_armor: ItemData(0xFF0018, False),

    ItemName.rouge_mystic_melody:  ItemData(0xFF0019, True),
    ItemName.rouge_pick_nails:     ItemData(0xFF001A, True),
    ItemName.rouge_treasure_scope: ItemData(0xFF001B, True),
    ItemName.rouge_iron_boots:     ItemData(0xFF001C, True),
}

junk_table = {
    ItemName.five_rings:      ItemData(0xFF0020, False),
    ItemName.ten_rings:       ItemData(0xFF0021, False),
    ItemName.twenty_rings:    ItemData(0xFF0022, False),
    ItemName.extra_life:      ItemData(0xFF0023, False),
    ItemName.shield:          ItemData(0xFF0024, False),
    ItemName.magnetic_shield: ItemData(0xFF0025, False),
    ItemName.invincibility:   ItemData(0xFF0026, False),
}

trap_table = {
    ItemName.omochao_trap:    ItemData(0xFF0030, False, True),
    ItemName.timestop_trap:   ItemData(0xFF0031, False, True),
    ItemName.confuse_trap:    ItemData(0xFF0032, False, True),
    ItemName.tiny_trap:       ItemData(0xFF0033, False, True),
    ItemName.gravity_trap:    ItemData(0xFF0034, False, True),
    ItemName.exposition_trap: ItemData(0xFF0035, False, True),
    #ItemName.darkness_trap:   ItemData(0xFF0036, False, True),
    ItemName.ice_trap:        ItemData(0xFF0037, False, True),
    ItemName.slow_trap:       ItemData(0xFF0038, False, True),
    ItemName.cutscene_trap:   ItemData(0xFF0039, False, True),

    ItemName.pong_trap:       ItemData(0xFF0050, False, True),
}

emeralds_table = {
    ItemName.white_emerald:  ItemData(0xFF0040, True),
    ItemName.red_emerald:    ItemData(0xFF0041, True),
    ItemName.cyan_emerald:   ItemData(0xFF0042, True),
    ItemName.purple_emerald: ItemData(0xFF0043, True),
    ItemName.green_emerald:  ItemData(0xFF0044, True),
    ItemName.yellow_emerald: ItemData(0xFF0045, True),
    ItemName.blue_emerald:   ItemData(0xFF0046, True),
}

eggs_table = {
    ItemName.normal_egg:              ItemData(0xFF0100, False),
    ItemName.yellow_monotone_egg:     ItemData(0xFF0101, False),
    ItemName.white_monotone_egg:      ItemData(0xFF0102, False),
    ItemName.brown_monotone_egg:      ItemData(0xFF0103, False),
    ItemName.sky_blue_monotone_egg:   ItemData(0xFF0104, False),
    ItemName.pink_monotone_egg:       ItemData(0xFF0105, False),
    ItemName.blue_monotone_egg:       ItemData(0xFF0106, False),
    ItemName.grey_monotone_egg:       ItemData(0xFF0107, False),
    ItemName.green_monotone_egg:      ItemData(0xFF0108, False),
    ItemName.red_monotone_egg:        ItemData(0xFF0109, False),
    ItemName.lime_green_monotone_egg: ItemData(0xFF010A, False),
    ItemName.purple_monotone_egg:     ItemData(0xFF010B, False),
    ItemName.orange_monotone_egg:     ItemData(0xFF010C, False),
    ItemName.black_monotone_egg:      ItemData(0xFF010D, False),

    ItemName.yellow_twotone_egg:     ItemData(0xFF010E, False),
    ItemName.white_twotone_egg:      ItemData(0xFF010F, False),
    ItemName.brown_twotone_egg:      ItemData(0xFF0110, False),
    ItemName.sky_blue_twotone_egg:   ItemData(0xFF0111, False),
    ItemName.pink_twotone_egg:       ItemData(0xFF0112, False),
    ItemName.blue_twotone_egg:       ItemData(0xFF0113, False),
    ItemName.grey_twotone_egg:       ItemData(0xFF0114, False),
    ItemName.green_twotone_egg:      ItemData(0xFF0115, False),
    ItemName.red_twotone_egg:        ItemData(0xFF0116, False),
    ItemName.lime_green_twotone_egg: ItemData(0xFF0117, False),
    ItemName.purple_twotone_egg:     ItemData(0xFF0118, False),
    ItemName.orange_twotone_egg:     ItemData(0xFF0119, False),
    ItemName.black_twotone_egg:      ItemData(0xFF011A, False),

    ItemName.normal_shiny_egg:     ItemData(0xFF011B, False),
    ItemName.yellow_shiny_egg:     ItemData(0xFF011C, False),
    ItemName.white_shiny_egg:      ItemData(0xFF011D, False),
    ItemName.brown_shiny_egg:      ItemData(0xFF011E, False),
    ItemName.sky_blue_shiny_egg:   ItemData(0xFF011F, False),
    ItemName.pink_shiny_egg:       ItemData(0xFF0120, False),
    ItemName.blue_shiny_egg:       ItemData(0xFF0121, False),
    ItemName.grey_shiny_egg:       ItemData(0xFF0122, False),
    ItemName.green_shiny_egg:      ItemData(0xFF0123, False),
    ItemName.red_shiny_egg:        ItemData(0xFF0124, False),
    ItemName.lime_green_shiny_egg: ItemData(0xFF0125, False),
    ItemName.purple_shiny_egg:     ItemData(0xFF0126, False),
    ItemName.orange_shiny_egg:     ItemData(0xFF0127, False),
    ItemName.black_shiny_egg:      ItemData(0xFF0128, False),

}

event_table = {
    ItemName.maria: ItemData(0xFF001D, True),
}

# Complete item table.
item_table = {
    **emblems_table,
    **upgrades_table,
    **junk_table,
    **trap_table,
    **emeralds_table,
    **eggs_table,
    **event_table,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}

item_groups: typing.Dict[str, str] = {
    "Chaos Emeralds": [item_name for item_name, data in emeralds_table.items()],
    "Eggs":           [item_name for item_name, data in eggs_table.items()],
}

ALTTPWorld.pedestal_credit_texts[item_table[ItemName.sonic_light_shoes].code] = "and the Soap Shoes"
ALTTPWorld.pedestal_credit_texts[item_table[ItemName.shadow_air_shoes].code] = "and the Soap Shoes"
