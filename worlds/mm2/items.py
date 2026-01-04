from BaseClasses import Item
from typing import NamedTuple, Dict
from . import names


class ItemData(NamedTuple):
    code: int
    progression: bool
    useful: bool = False  # primarily use this for incredibly useful items of their class, like Metal Blade
    skip_balancing: bool = False


class MM2Item(Item):
    game = "Mega Man 2"


robot_master_weapon_table = {
    names.atomic_fire: ItemData(0x880001, True),
    names.air_shooter: ItemData(0x880002, True),
    names.leaf_shield: ItemData(0x880003, True),
    names.bubble_lead: ItemData(0x880004, True),
    names.quick_boomerang: ItemData(0x880005, True),
    names.time_stopper: ItemData(0x880006, True, True),
    names.metal_blade: ItemData(0x880007, True, True),
    names.crash_bomber: ItemData(0x880008, True),
}

stage_access_table = {
    names.heat_man_stage: ItemData(0x880101, True),
    names.air_man_stage: ItemData(0x880102, True),
    names.wood_man_stage: ItemData(0x880103, True),
    names.bubble_man_stage: ItemData(0x880104, True),
    names.quick_man_stage: ItemData(0x880105, True),
    names.flash_man_stage: ItemData(0x880106, True),
    names.metal_man_stage: ItemData(0x880107, True),
    names.crash_man_stage: ItemData(0x880108, True),
}

item_item_table = {
    names.item_1: ItemData(0x880011, True, True, True),
    names.item_2: ItemData(0x880012, True, True, True),
    names.item_3: ItemData(0x880013, True, True, True)
}

filler_item_table = {
    names.one_up: ItemData(0x880020, False),
    names.weapon_energy: ItemData(0x880021, False),
    names.health_energy: ItemData(0x880022, False),
    names.e_tank: ItemData(0x880023, False, True),
}

filler_item_weights = {
    names.one_up: 1,
    names.weapon_energy: 4,
    names.health_energy: 1,
    names.e_tank: 2,
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

lookup_item_to_id: Dict[str, int] = {item_name: data.code for item_name, data in item_table.items()}
