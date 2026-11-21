from typing import NamedTuple, Optional

from BaseClasses import Item, ItemClassification
from .Levels import level_id_to_name
from .Names import ItemName


level_cassette_items: dict[str, str] = {
    "0a": ItemName.prologue_cassette,
    "1a": ItemName.fc_a_cassette,
    "1b": ItemName.fc_b_cassette,
    "1c": ItemName.fc_c_cassette,
    "2a": ItemName.os_a_cassette,
    "2b": ItemName.os_b_cassette,
    "2c": ItemName.os_c_cassette,
    "3a": ItemName.cr_a_cassette,
    "3b": ItemName.cr_b_cassette,
    "3c": ItemName.cr_c_cassette,
    "4a": ItemName.gr_a_cassette,
    "4b": ItemName.gr_b_cassette,
    "4c": ItemName.gr_c_cassette,
    "5a": ItemName.mt_a_cassette,
    "5b": ItemName.mt_b_cassette,
    "5c": ItemName.mt_c_cassette,
    "6a": ItemName.ref_a_cassette,
    "6b": ItemName.ref_b_cassette,
    "6c": ItemName.ref_c_cassette,
    "7a": ItemName.sum_a_cassette,
    "7b": ItemName.sum_b_cassette,
    "7c": ItemName.sum_c_cassette,
    "8a": ItemName.epilogue_cassette,
    "9a": ItemName.core_a_cassette,
    "9b": ItemName.core_b_cassette,
    "9c": ItemName.core_c_cassette,
    "10a":ItemName.farewell_cassette,
}


celeste_base_id: int = 0xCA10000
celeste_cassette_id: int = celeste_base_id + 0x1000
celeste_interactable_id: int = celeste_base_id + 0x2000
celeste_car_id: int = celeste_base_id + 0x2A00
celeste_crystal_heart_id: int = celeste_base_id + 0x3000
celeste_checkpoint_id: int = celeste_base_id + 0x4000
celeste_key_id: int = celeste_base_id + 0x6000
celeste_gem_id: int = celeste_base_id + 0x6A00


class CelesteItem(Item):
    game = "Celeste (Open World)"


class CelesteItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler


collectable_item_data_table: dict[str, CelesteItemData] = {
    ItemName.strawberry:     CelesteItemData(celeste_base_id + 0x0, ItemClassification.progression_skip_balancing),
    ItemName.gold_raspberry: CelesteItemData(celeste_base_id + 0x8, ItemClassification.progression_skip_balancing | ItemClassification.useful | ItemClassification.deprioritized),
}

filler_item_data_table: dict[str, CelesteItemData] = {
    ItemName.raspberry:      CelesteItemData(celeste_base_id + 0x1, ItemClassification.filler),
    ItemName.blue_raspberry: CelesteItemData(celeste_base_id + 0x2, ItemClassification.filler),
    ItemName.blueberry:      CelesteItemData(celeste_base_id + 0x3, ItemClassification.filler),
    ItemName.blackberry:     CelesteItemData(celeste_base_id + 0x4, ItemClassification.filler),
    ItemName.boysenberry:    CelesteItemData(celeste_base_id + 0x5, ItemClassification.filler),
    ItemName.bananaberry:    CelesteItemData(celeste_base_id + 0x6, ItemClassification.filler),
    ItemName.cranberry:      CelesteItemData(celeste_base_id + 0x7, ItemClassification.filler),
}

movement_item_data_table: dict[str, CelesteItemData] = {
    ItemName.dash:    CelesteItemData(celeste_base_id + 0x80, ItemClassification.progression),
    ItemName.u_dash:  CelesteItemData(celeste_base_id + 0x81, ItemClassification.progression),
    ItemName.ur_dash: CelesteItemData(celeste_base_id + 0x82, ItemClassification.progression),
    ItemName.r_dash:  CelesteItemData(celeste_base_id + 0x83, ItemClassification.progression),
    ItemName.dr_dash: CelesteItemData(celeste_base_id + 0x84, ItemClassification.progression),
    ItemName.d_dash:  CelesteItemData(celeste_base_id + 0x85, ItemClassification.progression),
    ItemName.dl_dash: CelesteItemData(celeste_base_id + 0x86, ItemClassification.progression),
    ItemName.l_dash:  CelesteItemData(celeste_base_id + 0x87, ItemClassification.progression),
    ItemName.ul_dash: CelesteItemData(celeste_base_id + 0x88, ItemClassification.progression),

    ItemName.climb:   CelesteItemData(celeste_base_id + 0x89, ItemClassification.progression),
    ItemName.r_climb: CelesteItemData(celeste_base_id + 0x8A, ItemClassification.progression),
    ItemName.l_climb: CelesteItemData(celeste_base_id + 0x8B, ItemClassification.progression),

    ItemName.crouch: CelesteItemData(celeste_base_id + 0x8C, ItemClassification.progression),
}

goal_item_data_table: dict[str, CelesteItemData] = {
    ItemName.house_keys: CelesteItemData(celeste_base_id + 0x10, ItemClassification.progression_skip_balancing),
}

trap_item_data_table: dict[str, CelesteItemData] = {
    ItemName.bald_trap:        CelesteItemData(celeste_base_id + 0x20, ItemClassification.trap),
    ItemName.literature_trap:  CelesteItemData(celeste_base_id + 0x21, ItemClassification.trap),
    ItemName.stun_trap:        CelesteItemData(celeste_base_id + 0x22, ItemClassification.trap),
    ItemName.invisible_trap:   CelesteItemData(celeste_base_id + 0x23, ItemClassification.trap),
    ItemName.fast_trap:        CelesteItemData(celeste_base_id + 0x24, ItemClassification.trap),
    ItemName.slow_trap:        CelesteItemData(celeste_base_id + 0x25, ItemClassification.trap),
    ItemName.ice_trap:         CelesteItemData(celeste_base_id + 0x26, ItemClassification.trap),
    ItemName.reverse_trap:     CelesteItemData(celeste_base_id + 0x28, ItemClassification.trap),
    ItemName.screen_flip_trap: CelesteItemData(celeste_base_id + 0x29, ItemClassification.trap),
    ItemName.laughter_trap:    CelesteItemData(celeste_base_id + 0x2A, ItemClassification.trap),
    ItemName.hiccup_trap:      CelesteItemData(celeste_base_id + 0x2B, ItemClassification.trap),
    ItemName.zoom_trap:        CelesteItemData(celeste_base_id + 0x2C, ItemClassification.trap),
    ItemName.tiny_trap:        CelesteItemData(celeste_base_id + 0x2D, ItemClassification.trap),
}

checkpoint_item_data_table: dict[str, CelesteItemData] = {}

key_item_data_table: dict[str, CelesteItemData] = {}
gem_item_data_table: dict[str, CelesteItemData] = {}

interactable_item_data_table: dict[str, CelesteItemData] = {
    ItemName.springs:              CelesteItemData(celeste_interactable_id + 0x00, ItemClassification.progression),
    ItemName.traffic_blocks:       CelesteItemData(celeste_interactable_id + 0x01, ItemClassification.progression),
    ItemName.pink_cassette_blocks: CelesteItemData(celeste_interactable_id + 0x02, ItemClassification.progression),
    ItemName.blue_cassette_blocks: CelesteItemData(celeste_interactable_id + 0x03, ItemClassification.progression),

    ItemName.dream_blocks:     CelesteItemData(celeste_interactable_id + 0x04, ItemClassification.progression),
    ItemName.coins:            CelesteItemData(celeste_interactable_id + 0x05, ItemClassification.progression),
    ItemName.strawberry_seeds: CelesteItemData(celeste_interactable_id + 0x1F, ItemClassification.progression),

    ItemName.sinking_platforms: CelesteItemData(celeste_interactable_id + 0x20, ItemClassification.progression),

    ItemName.moving_platforms: CelesteItemData(celeste_interactable_id + 0x06, ItemClassification.progression),
    ItemName.blue_boosters:    CelesteItemData(celeste_interactable_id + 0x07, ItemClassification.progression),
    ItemName.blue_clouds:      CelesteItemData(celeste_interactable_id + 0x08, ItemClassification.progression),
    ItemName.move_blocks:      CelesteItemData(celeste_interactable_id + 0x09, ItemClassification.progression),
    ItemName.white_block:      CelesteItemData(celeste_interactable_id + 0x21, ItemClassification.progression),

    ItemName.swap_blocks:    CelesteItemData(celeste_interactable_id + 0x0A, ItemClassification.progression),
    ItemName.red_boosters:   CelesteItemData(celeste_interactable_id + 0x0B, ItemClassification.progression),
    ItemName.torches:        CelesteItemData(celeste_interactable_id + 0x22, ItemClassification.useful),
    ItemName.yellow_torches: CelesteItemData(celeste_interactable_id + 0x24, ItemClassification.useful),
    ItemName.theo_crystal:   CelesteItemData(celeste_interactable_id + 0x0C, ItemClassification.progression),

    ItemName.feathers:     CelesteItemData(celeste_interactable_id + 0x0D, ItemClassification.progression),
    ItemName.bumpers:      CelesteItemData(celeste_interactable_id + 0x0E, ItemClassification.progression),
    ItemName.kevin_blocks: CelesteItemData(celeste_interactable_id + 0x0F, ItemClassification.progression),

    ItemName.pink_clouds:       CelesteItemData(celeste_interactable_id + 0x10, ItemClassification.progression),
    ItemName.badeline_boosters: CelesteItemData(celeste_interactable_id + 0x11, ItemClassification.progression),

    ItemName.fire_ice_balls: CelesteItemData(celeste_interactable_id + 0x12, ItemClassification.progression),
    ItemName.core_toggles:   CelesteItemData(celeste_interactable_id + 0x13, ItemClassification.progression),
    ItemName.core_blocks:    CelesteItemData(celeste_interactable_id + 0x14, ItemClassification.progression),

    ItemName.pufferfish:             CelesteItemData(celeste_interactable_id + 0x15, ItemClassification.progression),
    ItemName.jellyfish:              CelesteItemData(celeste_interactable_id + 0x16, ItemClassification.progression),
    ItemName.breaker_boxes:          CelesteItemData(celeste_interactable_id + 0x17, ItemClassification.progression),
    ItemName.dash_refills:           CelesteItemData(celeste_interactable_id + 0x18, ItemClassification.progression),
    ItemName.double_dash_refills:    CelesteItemData(celeste_interactable_id + 0x19, ItemClassification.progression),
    ItemName.yellow_cassette_blocks: CelesteItemData(celeste_interactable_id + 0x1A, ItemClassification.progression),
    ItemName.green_cassette_blocks:  CelesteItemData(celeste_interactable_id + 0x1B, ItemClassification.progression),
    ItemName.bird:                   CelesteItemData(celeste_interactable_id + 0x23, ItemClassification.progression),

    ItemName.dash_switches: CelesteItemData(celeste_interactable_id + 0x1C, ItemClassification.progression),
    ItemName.seekers:       CelesteItemData(celeste_interactable_id + 0x1D, ItemClassification.progression),
}

cassette_item_data_table: dict[str, CelesteItemData] = {
    ItemName.prologue_cassette: CelesteItemData(celeste_cassette_id + 0x00, ItemClassification.filler),
    ItemName.fc_a_cassette:     CelesteItemData(celeste_cassette_id + 0x01, ItemClassification.filler),
    ItemName.fc_b_cassette:     CelesteItemData(celeste_cassette_id + 0x02, ItemClassification.filler),
    ItemName.fc_c_cassette:     CelesteItemData(celeste_cassette_id + 0x03, ItemClassification.filler),
    ItemName.os_a_cassette:     CelesteItemData(celeste_cassette_id + 0x04, ItemClassification.filler),
    ItemName.os_b_cassette:     CelesteItemData(celeste_cassette_id + 0x05, ItemClassification.filler),
    ItemName.os_c_cassette:     CelesteItemData(celeste_cassette_id + 0x06, ItemClassification.filler),
    ItemName.cr_a_cassette:     CelesteItemData(celeste_cassette_id + 0x07, ItemClassification.filler),
    ItemName.cr_b_cassette:     CelesteItemData(celeste_cassette_id + 0x08, ItemClassification.filler),
    ItemName.cr_c_cassette:     CelesteItemData(celeste_cassette_id + 0x09, ItemClassification.filler),
    ItemName.gr_a_cassette:     CelesteItemData(celeste_cassette_id + 0x0A, ItemClassification.filler),
    ItemName.gr_b_cassette:     CelesteItemData(celeste_cassette_id + 0x0B, ItemClassification.filler),
    ItemName.gr_c_cassette:     CelesteItemData(celeste_cassette_id + 0x0C, ItemClassification.filler),
    ItemName.mt_a_cassette:     CelesteItemData(celeste_cassette_id + 0x0D, ItemClassification.filler),
    ItemName.mt_b_cassette:     CelesteItemData(celeste_cassette_id + 0x0E, ItemClassification.filler),
    ItemName.mt_c_cassette:     CelesteItemData(celeste_cassette_id + 0x0F, ItemClassification.filler),
    ItemName.ref_a_cassette:    CelesteItemData(celeste_cassette_id + 0x10, ItemClassification.filler),
    ItemName.ref_b_cassette:    CelesteItemData(celeste_cassette_id + 0x11, ItemClassification.filler),
    ItemName.ref_c_cassette:    CelesteItemData(celeste_cassette_id + 0x12, ItemClassification.filler),
    ItemName.sum_a_cassette:    CelesteItemData(celeste_cassette_id + 0x13, ItemClassification.filler),
    ItemName.sum_b_cassette:    CelesteItemData(celeste_cassette_id + 0x14, ItemClassification.filler),
    ItemName.sum_c_cassette:    CelesteItemData(celeste_cassette_id + 0x15, ItemClassification.filler),
    ItemName.epilogue_cassette: CelesteItemData(celeste_cassette_id + 0x16, ItemClassification.filler),
    ItemName.core_a_cassette:   CelesteItemData(celeste_cassette_id + 0x17, ItemClassification.filler),
    ItemName.core_b_cassette:   CelesteItemData(celeste_cassette_id + 0x18, ItemClassification.filler),
    ItemName.core_c_cassette:   CelesteItemData(celeste_cassette_id + 0x19, ItemClassification.filler),
    ItemName.farewell_cassette: CelesteItemData(celeste_cassette_id + 0x1A, ItemClassification.filler),
}

crystal_heart_item_data_table: dict[str, CelesteItemData] = {
    ItemName.crystal_heart_1:  CelesteItemData(celeste_crystal_heart_id + 0x00, ItemClassification.filler),
    ItemName.crystal_heart_2:  CelesteItemData(celeste_crystal_heart_id + 0x01, ItemClassification.filler),
    ItemName.crystal_heart_3:  CelesteItemData(celeste_crystal_heart_id + 0x02, ItemClassification.filler),
    ItemName.crystal_heart_4:  CelesteItemData(celeste_crystal_heart_id + 0x03, ItemClassification.filler),
    ItemName.crystal_heart_5:  CelesteItemData(celeste_crystal_heart_id + 0x04, ItemClassification.filler),
    ItemName.crystal_heart_6:  CelesteItemData(celeste_crystal_heart_id + 0x05, ItemClassification.filler),
    ItemName.crystal_heart_7:  CelesteItemData(celeste_crystal_heart_id + 0x06, ItemClassification.filler),
    ItemName.crystal_heart_8:  CelesteItemData(celeste_crystal_heart_id + 0x07, ItemClassification.filler),
    ItemName.crystal_heart_9:  CelesteItemData(celeste_crystal_heart_id + 0x08, ItemClassification.filler),
    ItemName.crystal_heart_10: CelesteItemData(celeste_crystal_heart_id + 0x09, ItemClassification.filler),
    ItemName.crystal_heart_11: CelesteItemData(celeste_crystal_heart_id + 0x0A, ItemClassification.filler),
    ItemName.crystal_heart_12: CelesteItemData(celeste_crystal_heart_id + 0x0B, ItemClassification.filler),
    ItemName.crystal_heart_13: CelesteItemData(celeste_crystal_heart_id + 0x0C, ItemClassification.filler),
    ItemName.crystal_heart_14: CelesteItemData(celeste_crystal_heart_id + 0x0D, ItemClassification.filler),
    ItemName.crystal_heart_15: CelesteItemData(celeste_crystal_heart_id + 0x0E, ItemClassification.filler),
    ItemName.crystal_heart_16: CelesteItemData(celeste_crystal_heart_id + 0x0F, ItemClassification.filler),
}

def add_checkpoint_to_table(id: int, name: str):
    checkpoint_item_data_table[name] = CelesteItemData(id, ItemClassification.progression)

def add_key_to_table(id: int, name: str):
    key_item_data_table[name] = CelesteItemData(id, ItemClassification.progression)

def add_gem_to_table(id: int, name: str):
    gem_item_data_table[name] = CelesteItemData(id, ItemClassification.progression)

def add_interactable_to_table(name: str, level: str = None, side: str = None):
    shared_id: int = interactable_item_data_table[name].code
    shared_type: ItemClassification = interactable_item_data_table[name].type

    if level == None:
        base_id_offset: int = 0x5000  # 0xCA17000 base

        side_id_offset: int = 0x000
        if side == "b":
            side_id_offset = 0x100
        elif side == "c":
            side_id_offset = 0x200

        full_id = shared_id + base_id_offset + side_id_offset

        interactable_item_data_table[side.upper() + "-Side " + name] = CelesteItemData(full_id, shared_type)
    elif side == None:
        base_id_offset: int = 0x6000  # 0xCA18000 base

        level_id_offset: int = 0x40 * int(level)

        full_id = shared_id + base_id_offset + level_id_offset

        interactable_item_data_table[level_id_to_name[level] + " - " + name] = CelesteItemData(full_id, shared_type)
    else:
        base_id_offset: int = 0x7000  # 0xCA19000 base

        side_id_offset: int = 0x00
        if side == "b":
            side_id_offset = 0x40
        elif side == "c":
            side_id_offset = 0x80

        level_id_offset: int = 0x100 * int(level)

        full_id = shared_id + base_id_offset + level_id_offset + side_id_offset

        interactable_item_data_table[level_id_to_name[level] + " " + side.upper() + " - " + name] = CelesteItemData(full_id, shared_type)


def generate_item_data_table() -> dict[str, CelesteItemData]:
    return {**collectable_item_data_table,
            **filler_item_data_table,
            **movement_item_data_table,
            **goal_item_data_table,
            **trap_item_data_table,
            **checkpoint_item_data_table,
            **key_item_data_table,
            **gem_item_data_table,
            **cassette_item_data_table,
            **crystal_heart_item_data_table,
            **interactable_item_data_table}


def generate_item_table() -> dict[str, int]:
    return {name: data.code for name, data in generate_item_data_table().items() if data.code is not None}


def generate_item_groups() -> dict[str, list[str]]:
    item_groups: dict[str, list[str]] = {
        "Movement":       list(movement_item_data_table.keys()),
        "Dashes":         [ItemName.dash, ItemName.u_dash, ItemName.ur_dash, ItemName.r_dash, ItemName.dr_dash, ItemName.d_dash, ItemName.dl_dash, ItemName.l_dash, ItemName.ul_dash],
        "Climbs":         [ItemName.climb, ItemName.r_climb, ItemName.l_climb],
        "Filler":         list(filler_item_data_table.keys()),
        "Traps":          list(trap_item_data_table.keys()),
        "Checkpoints":    list(checkpoint_item_data_table.keys()),
        "Keys":           list(key_item_data_table.keys()),
        "Gems":           list(gem_item_data_table.keys()),
        "Cassettes":      list(cassette_item_data_table.keys()),
        "Crystal Hearts": list(crystal_heart_item_data_table.keys()),
        "Interactables":  list(interactable_item_data_table.keys()),

        # Commonly mistaken names
        "Green Boosters": [ItemName.blue_boosters],
        "Green Bubbles":  [ItemName.blue_boosters],
        "Blue Bubbles":   [ItemName.blue_boosters],
        "Red Bubbles":    [ItemName.red_boosters],
        "Touch Switches": [ItemName.coins],
        "Shields":        [ItemName.coins],
    }

    return item_groups
