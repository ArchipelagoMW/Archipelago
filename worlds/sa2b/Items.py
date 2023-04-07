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
    **event_table,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}

item_groups: typing.Dict[str, str] = {"Chaos Emeralds": [item_name for item_name, data in emeralds_table.items()]}

ALTTPWorld.pedestal_credit_texts[item_table[ItemName.sonic_light_shoes].code] = "and the Soap Shoes"
ALTTPWorld.pedestal_credit_texts[item_table[ItemName.shadow_air_shoes].code] = "and the Soap Shoes"
