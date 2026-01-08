import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemName


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classsification: ItemClassification
    quantity: int = 1


class MMX3Item(Item):
    game = "Mega Man X3"

# Item tables
event_table = {
    ItemName.victory:           ItemData(0xBD0000, ItemClassification.progression_skip_balancing | ItemClassification.useful),
    ItemName.maverick_medal:    ItemData(0xBD0001, ItemClassification.progression_skip_balancing),
}

access_codes_table = {
    ItemName.stage_toxic_seahorse:      ItemData(0xBD0002, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_volt_catfish:        ItemData(0xBD0003, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_tunnel_rhino:        ItemData(0xBD0004, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_blizzard_buffalo:    ItemData(0xBD0005, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_crush_crawfish:      ItemData(0xBD0006, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_neon_tiger:          ItemData(0xBD0007, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_gravity_beetle:      ItemData(0xBD0008, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_blast_hornet:        ItemData(0xBD0009, ItemClassification.progression | ItemClassification.useful),
    ItemName.stage_doppler_lab:         ItemData(0xBD000A, ItemClassification.progression_skip_balancing | ItemClassification.useful),
    ItemName.stage_vile:                ItemData(0xBD0019, ItemClassification.progression | ItemClassification.useful),
}

weapons = {
    ItemName.frost_shield:      ItemData(0xBD000B, ItemClassification.progression),
    ItemName.acid_burst:        ItemData(0xBD000C, ItemClassification.progression),
    ItemName.tornado_fang:      ItemData(0xBD000D, ItemClassification.progression),
    ItemName.triad_thunder:     ItemData(0xBD000E, ItemClassification.progression),
    ItemName.spinning_blade:    ItemData(0xBD000F, ItemClassification.progression),
    ItemName.ray_splasher:      ItemData(0xBD0010, ItemClassification.progression),
    ItemName.gravity_well:      ItemData(0xBD0011, ItemClassification.progression),
    ItemName.parasitic_bomb:    ItemData(0xBD0012, ItemClassification.progression),
    ItemName.z_saber:           ItemData(0xBD001A, ItemClassification.useful),
}

tanks_table = {
    ItemName.heart_tank:        ItemData(0xBD0013, ItemClassification.progression),
    ItemName.sub_tank:          ItemData(0xBD0014, ItemClassification.progression),
}

ride_table = {
    ItemName.ride_chimera:      ItemData(0xBD0015, ItemClassification.progression),
    ItemName.ride_kangaroo:     ItemData(0xBD0016, ItemClassification.progression),
    ItemName.ride_hawk:         ItemData(0xBD0017, ItemClassification.progression),
    ItemName.ride_frog:         ItemData(0xBD0018, ItemClassification.progression),
}

third_armor_table = {
    ItemName.third_armor_helmet:    ItemData(0xBD001C, ItemClassification.progression),
    ItemName.third_armor_body:      ItemData(0xBD001D, ItemClassification.progression),
    ItemName.third_armor_arms:      ItemData(0xBD001E, ItemClassification.progression),
    ItemName.third_armor_legs:      ItemData(0xBD001F, ItemClassification.progression),
}

junk_table = {
    ItemName.small_hp:      ItemData(0xBD0030, ItemClassification.filler),
    ItemName.large_hp:      ItemData(0xBD0031, ItemClassification.filler),
    ItemName.life:          ItemData(0xBD0034, ItemClassification.filler),
}

junk_weapons_table = {
    ItemName.small_weapon:  ItemData(0xBD0032, ItemClassification.filler),
    ItemName.large_weapon:  ItemData(0xBD0033, ItemClassification.filler),
}

enhancements_table = {
    ItemName.chip_quick_charge:        ItemData(0xBD0040, ItemClassification.useful),
    ItemName.chip_speedster:           ItemData(0xBD0041, ItemClassification.useful),
    ItemName.chip_super_recover:       ItemData(0xBD0042, ItemClassification.useful),
    ItemName.chip_rapid_five:          ItemData(0xBD0043, ItemClassification.useful),
    ItemName.chip_speed_shot:          ItemData(0xBD0044, ItemClassification.useful),
    ItemName.chip_weapon_plus:         ItemData(0xBD0045, ItemClassification.useful),
    ItemName.chip_buster_plus:         ItemData(0xBD0046, ItemClassification.useful),
    ItemName.chip_item_plus:           ItemData(0xBD0047, ItemClassification.useful),
}

item_groups = {
    "Weapons": {
        ItemName.frost_shield,
        ItemName.acid_burst,
        ItemName.tornado_fang,
        ItemName.triad_thunder,
        ItemName.spinning_blade,
        ItemName.ray_splasher,
        ItemName.gravity_well,
        ItemName.parasitic_bomb,
    },
    "Ride Armors": {
        ItemName.ride_chimera,
        ItemName.ride_kangaroo,
        ItemName.ride_hawk,
        ItemName.ride_frog,
    },
    "Armor Upgrades": {
        ItemName.third_armor_helmet,
        ItemName.third_armor_body,
        ItemName.third_armor_arms,
        ItemName.third_armor_legs,
    },
    "Access Codes": {
        ItemName.stage_toxic_seahorse,
        ItemName.stage_volt_catfish,
        ItemName.stage_tunnel_rhino,
        ItemName.stage_blizzard_buffalo,
        ItemName.stage_crush_crawfish,
        ItemName.stage_neon_tiger,
        ItemName.stage_gravity_beetle,
        ItemName.stage_blast_hornet,
        ItemName.stage_doppler_lab,
        ItemName.stage_vile,
    }
}

# Complete item table.
item_table = {
    **event_table,
    **access_codes_table,
    **weapons,
    **tanks_table,
    **ride_table,
    **third_armor_table,
    **enhancements_table,
    **junk_table,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}