from BaseClasses import Item
import typing
import Names


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool


class MM2Item(Item):
    game = "Mega Man 2"


robot_master_weapon_table = {
    Names.atomic_fire: ItemData(0x880001, True),
    Names.air_shooter: ItemData(0x880002, True),
    Names.leaf_shield: ItemData(0x880003, True),
    Names.bubble_lead: ItemData(0x880004, True),
    Names.quick_boomerang: ItemData(0x880005, True),
    Names.time_stopper: ItemData(0x880006, True),
    Names.metal_blade: ItemData(0x880007, True),
    Names.crash_bomber: ItemData(0x880008, True),
}

stage_access_table = {
    Names.heat_man_stage: ItemData(0x880101, True),
    Names.air_man_stage: ItemData(0x880102, True),
    Names.wood_man_stage: ItemData(0x880103, True),
    Names.bubble_man_stage: ItemData(0x880104, True),
    Names.quick_man_stage: ItemData(0x880105, True),
    Names.flash_man_stage: ItemData(0x880106, True),
    Names.metal_man_stage: ItemData(0x880107, True),
    Names.crash_man_stage: ItemData(0x880108, True),
}

item_item_table = {
    Names.item_1: ItemData(0x880011, True),
    Names.item_2: ItemData(0x880012, True),
    Names.item_3: ItemData(0x880013, True)
}

filler_item_table = {
    Names.one_up: ItemData(0x880020, False),
    Names.weapon_energy: ItemData(0x880021, False),
    Names.health_energy: ItemData(0x880022, False),
    Names.e_tank: ItemData(0x880023, False),
}

filler_item_weights = {
    Names.one_up: 4,
    Names.weapon_energy: 1,
    Names.health_energy: 1,
    Names.e_tank: 2,
}

item_table = {
    **robot_master_weapon_table,
    **stage_access_table,
    **item_item_table,
    **filler_item_table,
}

item_names = {
    "Weapons": {name for name in robot_master_weapon_table.keys()},
    "Stages": {name for name in stage_access_table.keys()},
    "Items": {name for name in item_item_table.keys()}
}

lookup_name_to_id: typing.Dict[str, int] = {item_name: data.code for item_name, data in item_table.items() if data.code}
