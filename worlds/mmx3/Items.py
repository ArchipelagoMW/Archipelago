import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemName


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    trap: bool = False
    quantity: int = 1


class MMX3Item(Item):
    game = "Mega Man X3"

# Item tables
event_table = {
    ItemName.victory:           ItemData(0xBD0000, True),
    ItemName.maverick_medal:    ItemData(0xBD0001, True),
}

access_codes_table = {
    ItemName.stage_toxic_seahorse:      ItemData(0xBD0002, True),
    ItemName.stage_volt_catfish:        ItemData(0xBD0003, True),
    ItemName.stage_tunnel_rhino:        ItemData(0xBD0004, True),
    ItemName.stage_blizzard_buffalo:    ItemData(0xBD0005, True),
    ItemName.stage_crush_crawfish:      ItemData(0xBD0006, True),
    ItemName.stage_neon_tiger:          ItemData(0xBD0007, True),
    ItemName.stage_gravity_beetle:      ItemData(0xBD0008, True),
    ItemName.stage_blast_hornet:        ItemData(0xBD0009, True),
    ItemName.stage_doppler_lab:         ItemData(0xBD000A, True),
    ItemName.stage_vile:                ItemData(0xBD0019, True),
}

weapons = {
    ItemName.frost_shield:      ItemData(0xBD000B, True),
    ItemName.acid_burst:        ItemData(0xBD000C, True),
    ItemName.tornado_fang:      ItemData(0xBD000D, True),
    ItemName.triad_thunder:     ItemData(0xBD000E, True),
    ItemName.spinning_blade:    ItemData(0xBD000F, True),
    ItemName.ray_splasher:      ItemData(0xBD0010, True),
    ItemName.gravity_well:      ItemData(0xBD0011, True),
    ItemName.parasitic_bomb:    ItemData(0xBD0012, True),
    ItemName.z_saber:           ItemData(0xBD001A, True)
}

tanks_table = {
    ItemName.heart_tank:        ItemData(0xBD0013, True),
    ItemName.sub_tank:          ItemData(0xBD0014, True),
}

ride_table = {
    ItemName.ride_chimera:      ItemData(0xBD0015, True),
    ItemName.ride_kangaroo:     ItemData(0xBD0016, True),
    ItemName.ride_hawk:         ItemData(0xBD0017, True),
    ItemName.ride_frog:         ItemData(0xBD0018, True),
}

third_armor_table = {
    ItemName.third_armor_helmet:    ItemData(0xBD001C, True), 
    ItemName.third_armor_body:      ItemData(0xBD001D, True), 
    ItemName.third_armor_arms:      ItemData(0xBD001E, True), 
    ItemName.third_armor_legs:      ItemData(0xBD001F, True), 
}

junk_table = {
    ItemName.small_hp:      ItemData(0xBD0030, False),
    ItemName.large_hp:      ItemData(0xBD0031, False),
    ItemName.life:          ItemData(0xBD0034, False),
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
    **junk_table,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}