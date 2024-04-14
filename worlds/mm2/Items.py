from BaseClasses import Item
from typing import NamedTuple, Dict
from .Names import *


class ItemData(NamedTuple):
    code: int
    progression: bool
    useful: bool = False  # primarily use this for incredibly useful items of their class, like Metal Blade
    skip_balancing: bool = False


class MM2Item(Item):
    game = "Mega Man 2"


robot_master_weapon_table = {
    atomic_fire: ItemData(0x880001, True),
    air_shooter: ItemData(0x880002, True),
    leaf_shield: ItemData(0x880003, True),
    bubble_lead: ItemData(0x880004, True),
    quick_boomerang: ItemData(0x880005, True),
    time_stopper: ItemData(0x880006, True, True),
    metal_blade: ItemData(0x880007, True, True),
    crash_bomber: ItemData(0x880008, True),
}

stage_access_table = {
    heat_man_stage: ItemData(0x880101, True),
    air_man_stage: ItemData(0x880102, True),
    wood_man_stage: ItemData(0x880103, True),
    bubble_man_stage: ItemData(0x880104, True),
    quick_man_stage: ItemData(0x880105, True),
    flash_man_stage: ItemData(0x880106, True),
    metal_man_stage: ItemData(0x880107, True),
    crash_man_stage: ItemData(0x880108, True),
}

item_item_table = {
    item_1: ItemData(0x880011, True, True, True),
    item_2: ItemData(0x880012, True, True, True),
    item_3: ItemData(0x880013, True, True, True)
}

filler_item_table = {
    one_up: ItemData(0x880020, False),
    weapon_energy: ItemData(0x880021, False),
    health_energy: ItemData(0x880022, False),
    e_tank: ItemData(0x880023, False, True),
}

filler_item_weights = {
    one_up: 1,
    weapon_energy: 4,
    health_energy: 1,
    e_tank: 2,
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

lookup_item_to_id: Dict[str, int] = {item_name: data.code for item_name, data in item_table.items() if data.code}
