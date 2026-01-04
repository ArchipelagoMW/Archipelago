from typing import NamedTuple, Optional

from BaseClasses import Item, ItemClassification
from .Names import ItemName


level_item_lists: dict[str, set[str]] = {
    "0a": set(),

    "1a": {ItemName.springs, ItemName.traffic_blocks, ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks},
    "1b": {ItemName.springs, ItemName.traffic_blocks, ItemName.dash_refills, ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks},
    "1c": {ItemName.traffic_blocks, ItemName.dash_refills, ItemName.coins},

    "2a": {ItemName.springs, ItemName.dream_blocks, ItemName.traffic_blocks, ItemName.strawberry_seeds, ItemName.dash_refills, ItemName.coins},
    "2b": {ItemName.springs, ItemName.dream_blocks, ItemName.dash_refills, ItemName.coins, ItemName.blue_cassette_blocks},
    "2c": {ItemName.springs, ItemName.dream_blocks, ItemName.dash_refills, ItemName.coins},

    "3a": {ItemName.springs, ItemName.moving_platforms, ItemName.sinking_platforms, ItemName.dash_refills, ItemName.coins, ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks},
    "3b": {ItemName.springs, ItemName.dash_refills, ItemName.sinking_platforms, ItemName.coins, ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks},
    "3c": {ItemName.dash_refills, ItemName.sinking_platforms, ItemName.coins},

    "4a": {ItemName.blue_clouds, ItemName.blue_boosters, ItemName.moving_platforms, ItemName.coins, ItemName.strawberry_seeds, ItemName.springs, ItemName.move_blocks, ItemName.pink_clouds, ItemName.white_block, ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks},
    "4b": {ItemName.blue_boosters, ItemName.moving_platforms, ItemName.move_blocks, ItemName.springs, ItemName.coins, ItemName.blue_clouds, ItemName.pink_clouds, ItemName.dash_refills, ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks},
    "4c": {ItemName.blue_boosters, ItemName.move_blocks, ItemName.dash_refills, ItemName.pink_clouds},

    "5a": {ItemName.swap_blocks, ItemName.red_boosters, ItemName.dash_switches, ItemName.dash_refills, ItemName.coins, ItemName.springs, ItemName.torches, ItemName.seekers, ItemName.theo_crystal, ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks},
    "5b": {ItemName.swap_blocks, ItemName.red_boosters, ItemName.dash_switches, ItemName.dash_refills, ItemName.coins, ItemName.springs, ItemName.torches, ItemName.seekers, ItemName.theo_crystal, ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks},
    "5c": {ItemName.swap_blocks, ItemName.red_boosters, ItemName.dash_switches, ItemName.dash_refills},

    "6a": {ItemName.feathers, ItemName.kevin_blocks, ItemName.dash_refills, ItemName.bumpers, ItemName.springs, ItemName.coins, ItemName.badeline_boosters, ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks},
    "6b": {ItemName.feathers, ItemName.kevin_blocks, ItemName.dash_refills, ItemName.bumpers, ItemName.coins, ItemName.springs, ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks},
    "6c": {ItemName.feathers, ItemName.kevin_blocks, ItemName.dash_refills, ItemName.bumpers},

    "7a": {ItemName.springs, ItemName.dash_refills, ItemName.badeline_boosters, ItemName.traffic_blocks, ItemName.coins, ItemName.dream_blocks, ItemName.sinking_platforms, ItemName.blue_boosters, ItemName.blue_clouds, ItemName.pink_clouds, ItemName.move_blocks, ItemName.moving_platforms, ItemName.swap_blocks, ItemName.red_boosters, ItemName.dash_switches, ItemName.feathers, ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks},
    "7b": {ItemName.springs, ItemName.dash_refills, ItemName.badeline_boosters, ItemName.traffic_blocks, ItemName.coins, ItemName.dream_blocks, ItemName.moving_platforms, ItemName.blue_boosters, ItemName.blue_clouds, ItemName.pink_clouds, ItemName.move_blocks, ItemName.swap_blocks, ItemName.red_boosters, ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks},
    "7c": {ItemName.springs, ItemName.dash_refills, ItemName.badeline_boosters, ItemName.coins, ItemName.pink_clouds},

    # Epilogue
    "8a": set(),

    # Core
    "9a": {ItemName.springs, ItemName.dash_refills, ItemName.fire_ice_balls, ItemName.bumpers, ItemName.core_toggles, ItemName.core_blocks, ItemName.coins, ItemName.badeline_boosters, ItemName.feathers, ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks},
    "9b": {ItemName.springs, ItemName.dash_refills, ItemName.fire_ice_balls, ItemName.bumpers, ItemName.core_toggles, ItemName.core_blocks, ItemName.coins, ItemName.badeline_boosters, ItemName.dream_blocks, ItemName.moving_platforms, ItemName.blue_clouds, ItemName.swap_blocks, ItemName.kevin_blocks, ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks},
    "9c": {ItemName.dash_refills, ItemName.bumpers, ItemName.core_toggles, ItemName.core_blocks, ItemName.traffic_blocks, ItemName.dream_blocks, ItemName.pink_clouds, ItemName.swap_blocks, ItemName.kevin_blocks},

    # Farewell Pre/Post Empty Space
    "10a": {ItemName.blue_clouds, ItemName.badeline_boosters, ItemName.dash_refills, ItemName.double_dash_refills, ItemName.swap_blocks, ItemName.springs, ItemName.pufferfish, ItemName.coins, ItemName.dream_blocks, ItemName.jellyfish, ItemName.red_boosters, ItemName.dash_switches, ItemName.move_blocks, ItemName.breaker_boxes, ItemName.traffic_blocks},
    "10b": {ItemName.dream_blocks, ItemName.badeline_boosters, ItemName.bird, ItemName.dash_refills, ItemName.double_dash_refills, ItemName.kevin_blocks, ItemName.coins, ItemName.traffic_blocks, ItemName.move_blocks, ItemName.blue_boosters, ItemName.springs, ItemName.feathers, ItemName.swap_blocks, ItemName.red_boosters, ItemName.core_blocks, ItemName.fire_ice_balls, ItemName.kevin_blocks, ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks, ItemName.yellow_cassette_blocks, ItemName.green_cassette_blocks, ItemName.breaker_boxes, ItemName.pufferfish, ItemName.jellyfish},
    "10c": {ItemName.badeline_boosters, ItemName.double_dash_refills, ItemName.springs, ItemName.pufferfish, ItemName.jellyfish},
}

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


class CelesteItem(Item):
    game = "Celeste"


class CelesteItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler


collectable_item_data_table: dict[str, CelesteItemData] = {
    ItemName.strawberry: CelesteItemData(celeste_base_id + 0x0, ItemClassification.progression_skip_balancing),
    ItemName.raspberry:  CelesteItemData(celeste_base_id + 0x1, ItemClassification.filler),
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
}

checkpoint_item_data_table: dict[str, CelesteItemData] = {}

key_item_data_table: dict[str, CelesteItemData] = {}
gem_item_data_table: dict[str, CelesteItemData] = {}

interactable_item_data_table: dict[str, CelesteItemData] = {
    ItemName.springs:              CelesteItemData(celeste_base_id + 0x2000 + 0x00, ItemClassification.progression),
    ItemName.traffic_blocks:       CelesteItemData(celeste_base_id + 0x2000 + 0x01, ItemClassification.progression),
    ItemName.pink_cassette_blocks: CelesteItemData(celeste_base_id + 0x2000 + 0x02, ItemClassification.progression),
    ItemName.blue_cassette_blocks: CelesteItemData(celeste_base_id + 0x2000 + 0x03, ItemClassification.progression),

    ItemName.dream_blocks:     CelesteItemData(celeste_base_id + 0x2000 + 0x04, ItemClassification.progression),
    ItemName.coins:            CelesteItemData(celeste_base_id + 0x2000 + 0x05, ItemClassification.progression),
    ItemName.strawberry_seeds: CelesteItemData(celeste_base_id + 0x2000 + 0x1F, ItemClassification.progression),

    ItemName.sinking_platforms: CelesteItemData(celeste_base_id + 0x2000 + 0x20, ItemClassification.progression),

    ItemName.moving_platforms: CelesteItemData(celeste_base_id + 0x2000 + 0x06, ItemClassification.progression),
    ItemName.blue_boosters:    CelesteItemData(celeste_base_id + 0x2000 + 0x07, ItemClassification.progression),
    ItemName.blue_clouds:      CelesteItemData(celeste_base_id + 0x2000 + 0x08, ItemClassification.progression),
    ItemName.move_blocks:      CelesteItemData(celeste_base_id + 0x2000 + 0x09, ItemClassification.progression),
    ItemName.white_block:      CelesteItemData(celeste_base_id + 0x2000 + 0x21, ItemClassification.progression),

    ItemName.swap_blocks:  CelesteItemData(celeste_base_id + 0x2000 + 0x0A, ItemClassification.progression),
    ItemName.red_boosters: CelesteItemData(celeste_base_id + 0x2000 + 0x0B, ItemClassification.progression),
    ItemName.torches:      CelesteItemData(celeste_base_id + 0x2000 + 0x22, ItemClassification.useful),
    ItemName.theo_crystal: CelesteItemData(celeste_base_id + 0x2000 + 0x0C, ItemClassification.progression),

    ItemName.feathers:     CelesteItemData(celeste_base_id + 0x2000 + 0x0D, ItemClassification.progression),
    ItemName.bumpers:      CelesteItemData(celeste_base_id + 0x2000 + 0x0E, ItemClassification.progression),
    ItemName.kevin_blocks: CelesteItemData(celeste_base_id + 0x2000 + 0x0F, ItemClassification.progression),

    ItemName.pink_clouds:       CelesteItemData(celeste_base_id + 0x2000 + 0x10, ItemClassification.progression),
    ItemName.badeline_boosters: CelesteItemData(celeste_base_id + 0x2000 + 0x11, ItemClassification.progression),

    ItemName.fire_ice_balls: CelesteItemData(celeste_base_id + 0x2000 + 0x12, ItemClassification.progression),
    ItemName.core_toggles:   CelesteItemData(celeste_base_id + 0x2000 + 0x13, ItemClassification.progression),
    ItemName.core_blocks:    CelesteItemData(celeste_base_id + 0x2000 + 0x14, ItemClassification.progression),

    ItemName.pufferfish:             CelesteItemData(celeste_base_id + 0x2000 + 0x15, ItemClassification.progression),
    ItemName.jellyfish:              CelesteItemData(celeste_base_id + 0x2000 + 0x16, ItemClassification.progression),
    ItemName.breaker_boxes:          CelesteItemData(celeste_base_id + 0x2000 + 0x17, ItemClassification.progression),
    ItemName.dash_refills:           CelesteItemData(celeste_base_id + 0x2000 + 0x18, ItemClassification.progression),
    ItemName.double_dash_refills:    CelesteItemData(celeste_base_id + 0x2000 + 0x19, ItemClassification.progression),
    ItemName.yellow_cassette_blocks: CelesteItemData(celeste_base_id + 0x2000 + 0x1A, ItemClassification.progression),
    ItemName.green_cassette_blocks:  CelesteItemData(celeste_base_id + 0x2000 + 0x1B, ItemClassification.progression),
    ItemName.bird:                   CelesteItemData(celeste_base_id + 0x2000 + 0x23, ItemClassification.progression),

    ItemName.dash_switches: CelesteItemData(celeste_base_id + 0x2000 + 0x1C, ItemClassification.progression),
    ItemName.seekers:       CelesteItemData(celeste_base_id + 0x2000 + 0x1D, ItemClassification.progression),
}

cassette_item_data_table: dict[str, CelesteItemData] = {
    ItemName.prologue_cassette: CelesteItemData(celeste_base_id + 0x1000 + 0x00, ItemClassification.filler),
    ItemName.fc_a_cassette:     CelesteItemData(celeste_base_id + 0x1000 + 0x01, ItemClassification.filler),
    ItemName.fc_b_cassette:     CelesteItemData(celeste_base_id + 0x1000 + 0x02, ItemClassification.filler),
    ItemName.fc_c_cassette:     CelesteItemData(celeste_base_id + 0x1000 + 0x03, ItemClassification.filler),
    ItemName.os_a_cassette:     CelesteItemData(celeste_base_id + 0x1000 + 0x04, ItemClassification.filler),
    ItemName.os_b_cassette:     CelesteItemData(celeste_base_id + 0x1000 + 0x05, ItemClassification.filler),
    ItemName.os_c_cassette:     CelesteItemData(celeste_base_id + 0x1000 + 0x06, ItemClassification.filler),
    ItemName.cr_a_cassette:     CelesteItemData(celeste_base_id + 0x1000 + 0x07, ItemClassification.filler),
    ItemName.cr_b_cassette:     CelesteItemData(celeste_base_id + 0x1000 + 0x08, ItemClassification.filler),
    ItemName.cr_c_cassette:     CelesteItemData(celeste_base_id + 0x1000 + 0x09, ItemClassification.filler),
    ItemName.gr_a_cassette:     CelesteItemData(celeste_base_id + 0x1000 + 0x0A, ItemClassification.filler),
    ItemName.gr_b_cassette:     CelesteItemData(celeste_base_id + 0x1000 + 0x0B, ItemClassification.filler),
    ItemName.gr_c_cassette:     CelesteItemData(celeste_base_id + 0x1000 + 0x0C, ItemClassification.filler),
    ItemName.mt_a_cassette:     CelesteItemData(celeste_base_id + 0x1000 + 0x0D, ItemClassification.filler),
    ItemName.mt_b_cassette:     CelesteItemData(celeste_base_id + 0x1000 + 0x0E, ItemClassification.filler),
    ItemName.mt_c_cassette:     CelesteItemData(celeste_base_id + 0x1000 + 0x0F, ItemClassification.filler),
    ItemName.ref_a_cassette:    CelesteItemData(celeste_base_id + 0x1000 + 0x10, ItemClassification.filler),
    ItemName.ref_b_cassette:    CelesteItemData(celeste_base_id + 0x1000 + 0x11, ItemClassification.filler),
    ItemName.ref_c_cassette:    CelesteItemData(celeste_base_id + 0x1000 + 0x12, ItemClassification.filler),
    ItemName.sum_a_cassette:    CelesteItemData(celeste_base_id + 0x1000 + 0x13, ItemClassification.filler),
    ItemName.sum_b_cassette:    CelesteItemData(celeste_base_id + 0x1000 + 0x14, ItemClassification.filler),
    ItemName.sum_c_cassette:    CelesteItemData(celeste_base_id + 0x1000 + 0x15, ItemClassification.filler),
    ItemName.epilogue_cassette: CelesteItemData(celeste_base_id + 0x1000 + 0x16, ItemClassification.filler),
    ItemName.core_a_cassette:   CelesteItemData(celeste_base_id + 0x1000 + 0x17, ItemClassification.filler),
    ItemName.core_b_cassette:   CelesteItemData(celeste_base_id + 0x1000 + 0x18, ItemClassification.filler),
    ItemName.core_c_cassette:   CelesteItemData(celeste_base_id + 0x1000 + 0x19, ItemClassification.filler),
    ItemName.farewell_cassette: CelesteItemData(celeste_base_id + 0x1000 + 0x1A, ItemClassification.filler),
}

crystal_heart_item_data_table: dict[str, CelesteItemData] = {
    ItemName.crystal_heart_1:  CelesteItemData(celeste_base_id + 0x3000 + 0x00, ItemClassification.filler),
    ItemName.crystal_heart_2:  CelesteItemData(celeste_base_id + 0x3000 + 0x01, ItemClassification.filler),
    ItemName.crystal_heart_3:  CelesteItemData(celeste_base_id + 0x3000 + 0x02, ItemClassification.filler),
    ItemName.crystal_heart_4:  CelesteItemData(celeste_base_id + 0x3000 + 0x03, ItemClassification.filler),
    ItemName.crystal_heart_5:  CelesteItemData(celeste_base_id + 0x3000 + 0x04, ItemClassification.filler),
    ItemName.crystal_heart_6:  CelesteItemData(celeste_base_id + 0x3000 + 0x05, ItemClassification.filler),
    ItemName.crystal_heart_7:  CelesteItemData(celeste_base_id + 0x3000 + 0x06, ItemClassification.filler),
    ItemName.crystal_heart_8:  CelesteItemData(celeste_base_id + 0x3000 + 0x07, ItemClassification.filler),
    ItemName.crystal_heart_9:  CelesteItemData(celeste_base_id + 0x3000 + 0x08, ItemClassification.filler),
    ItemName.crystal_heart_10: CelesteItemData(celeste_base_id + 0x3000 + 0x09, ItemClassification.filler),
    ItemName.crystal_heart_11: CelesteItemData(celeste_base_id + 0x3000 + 0x0A, ItemClassification.filler),
    ItemName.crystal_heart_12: CelesteItemData(celeste_base_id + 0x3000 + 0x0B, ItemClassification.filler),
    ItemName.crystal_heart_13: CelesteItemData(celeste_base_id + 0x3000 + 0x0C, ItemClassification.filler),
    ItemName.crystal_heart_14: CelesteItemData(celeste_base_id + 0x3000 + 0x0D, ItemClassification.filler),
    ItemName.crystal_heart_15: CelesteItemData(celeste_base_id + 0x3000 + 0x0E, ItemClassification.filler),
    ItemName.crystal_heart_16: CelesteItemData(celeste_base_id + 0x3000 + 0x0F, ItemClassification.filler),
}

def add_checkpoint_to_table(id: int, name: str):
    checkpoint_item_data_table[name] = CelesteItemData(id, ItemClassification.progression)

def add_key_to_table(id: int, name: str):
    key_item_data_table[name] = CelesteItemData(id, ItemClassification.progression)

def add_gem_to_table(id: int, name: str):
    gem_item_data_table[name] = CelesteItemData(id, ItemClassification.progression)

def generate_item_data_table() -> dict[str, CelesteItemData]:
    return {**collectable_item_data_table,
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
        "Collectables":   list(collectable_item_data_table.keys()),
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
    }

    return item_groups
