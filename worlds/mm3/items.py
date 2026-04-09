from BaseClasses import Item
from typing import NamedTuple
from .names import (needle_cannon, magnet_missile, gemini_laser, hard_knuckle, top_spin, search_snake, spark_shock,
                    shadow_blade, rush_coil, rush_marine, rush_jet, needle_man_stage, magnet_man_stage,
                    gemini_man_stage, hard_man_stage, top_man_stage, snake_man_stage, spark_man_stage, shadow_man_stage,
                    doc_needle_stage, doc_gemini_stage, doc_spark_stage, doc_shadow_stage, e_tank, weapon_energy,
                    health_energy, one_up)


class ItemData(NamedTuple):
    code: int
    progression: bool
    useful: bool = False  # primarily use this for incredibly useful items of their class, like Metal Blade
    skip_balancing: bool = False


class MM3Item(Item):
    game = "Mega Man 3"


robot_master_weapon_table = {
    needle_cannon: ItemData(0x0001, True),
    magnet_missile: ItemData(0x0002, True, True),
    gemini_laser: ItemData(0x0003, True),
    hard_knuckle: ItemData(0x0004, True),
    top_spin: ItemData(0x0005, True, True),
    search_snake: ItemData(0x0006, True),
    spark_shock: ItemData(0x0007, True),
    shadow_blade: ItemData(0x0008, True, True),
}

stage_access_table = {
    needle_man_stage: ItemData(0x0101, True),
    magnet_man_stage: ItemData(0x0102, True),
    gemini_man_stage: ItemData(0x0103, True),
    hard_man_stage: ItemData(0x0104, True),
    top_man_stage: ItemData(0x0105, True),
    snake_man_stage: ItemData(0x0106, True),
    spark_man_stage: ItemData(0x0107, True),
    shadow_man_stage: ItemData(0x0108, True),
    doc_needle_stage: ItemData(0x0111, True, True),
    doc_gemini_stage: ItemData(0x0113, True, True),
    doc_spark_stage: ItemData(0x0117, True, True),
    doc_shadow_stage: ItemData(0x0118, True, True),
}

rush_item_table = {
    rush_coil: ItemData(0x0011, True, True),
    rush_marine: ItemData(0x0012, True),
    rush_jet: ItemData(0x0013, True, True),
}

filler_item_table = {
    one_up: ItemData(0x0020, False),
    weapon_energy: ItemData(0x0021, False),
    health_energy: ItemData(0x0022, False),
    e_tank: ItemData(0x0023, False, True),
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
    **rush_item_table,
    **filler_item_table,
}

item_names = {
    "Weapons": {name for name in robot_master_weapon_table.keys()},
    "Stages": {name for name in stage_access_table.keys()},
    "Rush": {name for name in rush_item_table.keys()}
}

lookup_item_to_id: dict[str, int] = {item_name: data.code for item_name, data in item_table.items() if data.code}
