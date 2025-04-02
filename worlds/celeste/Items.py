from typing import Dict, List, NamedTuple, Optional, Set

from BaseClasses import Item, ItemClassification
from .Names import ItemName


level_item_lists: Dict[str, Set[str]] = {
    "0a": {},

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
    "8a": {},

    # Core
    "9a": {ItemName.springs, ItemName.dash_refills, ItemName.fire_ice_balls, ItemName.bumpers, ItemName.core_toggles, ItemName.core_blocks, ItemName.coins, ItemName.badeline_boosters, ItemName.feathers, ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks},
    "9b": {ItemName.springs, ItemName.dash_refills, ItemName.fire_ice_balls, ItemName.bumpers, ItemName.core_toggles, ItemName.core_blocks, ItemName.coins, ItemName.badeline_boosters, ItemName.dream_blocks, ItemName.moving_platforms, ItemName.blue_clouds, ItemName.swap_blocks, ItemName.kevin_blocks, ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks},
    "9c": {ItemName.dash_refills, ItemName.bumpers, ItemName.core_toggles, ItemName.core_blocks, ItemName.traffic_blocks, ItemName.dream_blocks, ItemName.pink_clouds, ItemName.swap_blocks, ItemName.kevin_blocks},

    # Farewell Pre/Post Empty Space
    "10a": {ItemName.blue_clouds, ItemName.badeline_boosters, ItemName.dash_refills, ItemName.double_dash_refills, ItemName.swap_blocks, ItemName.springs, ItemName.pufferfish, ItemName.coins, ItemName.dream_blocks, ItemName.jellyfish, ItemName.red_boosters, ItemName.dash_switches, ItemName.move_blocks, ItemName.breaker_boxes, ItemName.traffic_blocks},
    "10b": {ItemName.dream_blocks, ItemName.badeline_boosters, ItemName.dash_refills, ItemName.double_dash_refills, ItemName.kevin_blocks, ItemName.coins, ItemName.traffic_blocks, ItemName.move_blocks, ItemName.blue_boosters, ItemName.springs, ItemName.feathers, ItemName.swap_blocks, ItemName.red_boosters, ItemName.core_blocks, ItemName.fire_ice_balls, ItemName.kevin_blocks, ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks, ItemName.yellow_cassette_blocks, ItemName.green_cassette_blocks, ItemName.breaker_boxes, ItemName.pufferfish, ItemName.jellyfish},
}



celeste_base_id: int = 0xCA1000


class CelesteItem(Item):
    game = "Celeste"


class CelesteItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler


collectable_item_data_table: Dict[str, CelesteItemData] = {
    ItemName.strawberry: CelesteItemData(celeste_base_id + 0x0, ItemClassification.progression_skip_balancing),
    ItemName.raspberry:  CelesteItemData(celeste_base_id + 0x1, ItemClassification.filler),
}

trap_item_data_table: Dict[str, CelesteItemData] = {
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

checkpoint_item_data_table: Dict[str, CelesteItemData] = {}

key_item_data_table: Dict[str, CelesteItemData] = {}

old_checkpoint_item_data_table: Dict[str, CelesteItemData] = {
    ItemName.fc_a_checkpoint_1: CelesteItemData(celeste_base_id + 0x100 + 0x00, ItemClassification.progression),
    ItemName.fc_a_checkpoint_2: CelesteItemData(celeste_base_id + 0x100 + 0x01, ItemClassification.progression),

    ItemName.fc_b_checkpoint_1: CelesteItemData(celeste_base_id + 0x100 + 0x08, ItemClassification.progression),
    ItemName.fc_b_checkpoint_2: CelesteItemData(celeste_base_id + 0x100 + 0x09, ItemClassification.progression),

    ItemName.os_a_checkpoint_1: CelesteItemData(celeste_base_id + 0x100 + 0x10, ItemClassification.progression),
    ItemName.os_a_checkpoint_2: CelesteItemData(celeste_base_id + 0x100 + 0x11, ItemClassification.progression),

    ItemName.os_b_checkpoint_1: CelesteItemData(celeste_base_id + 0x100 + 0x18, ItemClassification.progression),
    ItemName.os_b_checkpoint_2: CelesteItemData(celeste_base_id + 0x100 + 0x19, ItemClassification.progression),

    ItemName.cr_a_checkpoint_1: CelesteItemData(celeste_base_id + 0x100 + 0x20, ItemClassification.progression),
    ItemName.cr_a_checkpoint_2: CelesteItemData(celeste_base_id + 0x100 + 0x21, ItemClassification.progression),
    ItemName.cr_a_checkpoint_3: CelesteItemData(celeste_base_id + 0x100 + 0x22, ItemClassification.progression),

    ItemName.cr_b_checkpoint_1: CelesteItemData(celeste_base_id + 0x100 + 0x28, ItemClassification.progression),
    ItemName.cr_b_checkpoint_2: CelesteItemData(celeste_base_id + 0x100 + 0x29, ItemClassification.progression),
    ItemName.cr_b_checkpoint_3: CelesteItemData(celeste_base_id + 0x100 + 0x2A, ItemClassification.progression),

    ItemName.gr_a_checkpoint_1: CelesteItemData(celeste_base_id + 0x100 + 0x30, ItemClassification.progression),
    ItemName.gr_a_checkpoint_2: CelesteItemData(celeste_base_id + 0x100 + 0x31, ItemClassification.progression),
    ItemName.gr_a_checkpoint_3: CelesteItemData(celeste_base_id + 0x100 + 0x32, ItemClassification.progression),

    ItemName.gr_b_checkpoint_1: CelesteItemData(celeste_base_id + 0x100 + 0x38, ItemClassification.progression),
    ItemName.gr_b_checkpoint_2: CelesteItemData(celeste_base_id + 0x100 + 0x39, ItemClassification.progression),
    ItemName.gr_b_checkpoint_3: CelesteItemData(celeste_base_id + 0x100 + 0x3A, ItemClassification.progression),

    ItemName.mt_a_checkpoint_1: CelesteItemData(celeste_base_id + 0x100 + 0x40, ItemClassification.progression),
    ItemName.mt_a_checkpoint_2: CelesteItemData(celeste_base_id + 0x100 + 0x41, ItemClassification.progression),
    ItemName.mt_a_checkpoint_3: CelesteItemData(celeste_base_id + 0x100 + 0x42, ItemClassification.progression),
    ItemName.mt_a_checkpoint_4: CelesteItemData(celeste_base_id + 0x100 + 0x43, ItemClassification.progression),

    ItemName.mt_b_checkpoint_1: CelesteItemData(celeste_base_id + 0x100 + 0x48, ItemClassification.progression),
    ItemName.mt_b_checkpoint_2: CelesteItemData(celeste_base_id + 0x100 + 0x49, ItemClassification.progression),
    ItemName.mt_b_checkpoint_3: CelesteItemData(celeste_base_id + 0x100 + 0x4A, ItemClassification.progression),

    ItemName.ref_a_checkpoint_1: CelesteItemData(celeste_base_id + 0x100 + 0x50, ItemClassification.progression),
    ItemName.ref_a_checkpoint_2: CelesteItemData(celeste_base_id + 0x100 + 0x51, ItemClassification.progression),
    ItemName.ref_a_checkpoint_3: CelesteItemData(celeste_base_id + 0x100 + 0x52, ItemClassification.progression),
    ItemName.ref_a_checkpoint_4: CelesteItemData(celeste_base_id + 0x100 + 0x53, ItemClassification.progression),
    ItemName.ref_a_checkpoint_5: CelesteItemData(celeste_base_id + 0x100 + 0x54, ItemClassification.progression),

    ItemName.ref_b_checkpoint_1: CelesteItemData(celeste_base_id + 0x100 + 0x58, ItemClassification.progression),
    ItemName.ref_b_checkpoint_2: CelesteItemData(celeste_base_id + 0x100 + 0x59, ItemClassification.progression),
    ItemName.ref_b_checkpoint_3: CelesteItemData(celeste_base_id + 0x100 + 0x5A, ItemClassification.progression),

    ItemName.sum_a_checkpoint_1: CelesteItemData(celeste_base_id + 0x100 + 0x60, ItemClassification.progression),
    ItemName.sum_a_checkpoint_2: CelesteItemData(celeste_base_id + 0x100 + 0x61, ItemClassification.progression),
    ItemName.sum_a_checkpoint_3: CelesteItemData(celeste_base_id + 0x100 + 0x62, ItemClassification.progression),
    ItemName.sum_a_checkpoint_4: CelesteItemData(celeste_base_id + 0x100 + 0x63, ItemClassification.progression),
    ItemName.sum_a_checkpoint_5: CelesteItemData(celeste_base_id + 0x100 + 0x64, ItemClassification.progression),
    ItemName.sum_a_checkpoint_6: CelesteItemData(celeste_base_id + 0x100 + 0x65, ItemClassification.progression),

    ItemName.sum_b_checkpoint_1: CelesteItemData(celeste_base_id + 0x100 + 0x68, ItemClassification.progression),
    ItemName.sum_b_checkpoint_2: CelesteItemData(celeste_base_id + 0x100 + 0x69, ItemClassification.progression),
    ItemName.sum_b_checkpoint_3: CelesteItemData(celeste_base_id + 0x100 + 0x6A, ItemClassification.progression),
    ItemName.sum_b_checkpoint_4: CelesteItemData(celeste_base_id + 0x100 + 0x6B, ItemClassification.progression),
    ItemName.sum_b_checkpoint_5: CelesteItemData(celeste_base_id + 0x100 + 0x6C, ItemClassification.progression),
    ItemName.sum_b_checkpoint_6: CelesteItemData(celeste_base_id + 0x100 + 0x6D, ItemClassification.progression),

    ItemName.core_a_checkpoint_1: CelesteItemData(celeste_base_id + 0x100 + 0x70, ItemClassification.progression),
    ItemName.core_a_checkpoint_2: CelesteItemData(celeste_base_id + 0x100 + 0x71, ItemClassification.progression),
    ItemName.core_a_checkpoint_3: CelesteItemData(celeste_base_id + 0x100 + 0x72, ItemClassification.progression),

    ItemName.core_b_checkpoint_1: CelesteItemData(celeste_base_id + 0x100 + 0x78, ItemClassification.progression),
    ItemName.core_b_checkpoint_2: CelesteItemData(celeste_base_id + 0x100 + 0x79, ItemClassification.progression),
    ItemName.core_b_checkpoint_3: CelesteItemData(celeste_base_id + 0x100 + 0x7A, ItemClassification.progression),

    ItemName.farewell_checkpoint_1: CelesteItemData(celeste_base_id + 0x100 + 0x80, ItemClassification.progression),
    ItemName.farewell_checkpoint_2: CelesteItemData(celeste_base_id + 0x100 + 0x81, ItemClassification.progression),
    ItemName.farewell_checkpoint_3: CelesteItemData(celeste_base_id + 0x100 + 0x82, ItemClassification.progression),
    ItemName.farewell_checkpoint_4: CelesteItemData(celeste_base_id + 0x100 + 0x83, ItemClassification.progression),
    ItemName.farewell_checkpoint_5: CelesteItemData(celeste_base_id + 0x100 + 0x84, ItemClassification.progression),
    ItemName.farewell_checkpoint_6: CelesteItemData(celeste_base_id + 0x100 + 0x85, ItemClassification.progression),
    ItemName.farewell_checkpoint_7: CelesteItemData(celeste_base_id + 0x100 + 0x86, ItemClassification.progression),
    ItemName.farewell_checkpoint_8: CelesteItemData(celeste_base_id + 0x100 + 0x87, ItemClassification.progression),
}

interactable_item_data_table: Dict[str, CelesteItemData] = {
    ItemName.springs:              CelesteItemData(celeste_base_id + 0x200 + 0x00, ItemClassification.progression),
    ItemName.traffic_blocks:       CelesteItemData(celeste_base_id + 0x200 + 0x01, ItemClassification.progression),
    ItemName.pink_cassette_blocks: CelesteItemData(celeste_base_id + 0x200 + 0x02, ItemClassification.progression),
    ItemName.blue_cassette_blocks: CelesteItemData(celeste_base_id + 0x200 + 0x03, ItemClassification.progression),

    ItemName.dream_blocks:     CelesteItemData(celeste_base_id + 0x200 + 0x04, ItemClassification.progression),
    ItemName.coins:            CelesteItemData(celeste_base_id + 0x200 + 0x05, ItemClassification.progression),
    ItemName.strawberry_seeds: CelesteItemData(celeste_base_id + 0x200 + 0x1F, ItemClassification.progression),

    ItemName.sinking_platforms: CelesteItemData(celeste_base_id + 0x200 + 0x20, ItemClassification.progression),

    ItemName.moving_platforms: CelesteItemData(celeste_base_id + 0x200 + 0x06, ItemClassification.progression),
    ItemName.blue_boosters:    CelesteItemData(celeste_base_id + 0x200 + 0x07, ItemClassification.progression),
    ItemName.blue_clouds:      CelesteItemData(celeste_base_id + 0x200 + 0x08, ItemClassification.progression),
    ItemName.move_blocks:      CelesteItemData(celeste_base_id + 0x200 + 0x09, ItemClassification.progression),
    ItemName.white_block:      CelesteItemData(celeste_base_id + 0x200 + 0x21, ItemClassification.progression),

    ItemName.swap_blocks:  CelesteItemData(celeste_base_id + 0x200 + 0x0A, ItemClassification.progression),
    ItemName.red_boosters: CelesteItemData(celeste_base_id + 0x200 + 0x0B, ItemClassification.progression),
    ItemName.torches:      CelesteItemData(celeste_base_id + 0x200 + 0x22, ItemClassification.filler),
    ItemName.theo_crystal: CelesteItemData(celeste_base_id + 0x200 + 0x0C, ItemClassification.progression),

    ItemName.feathers:     CelesteItemData(celeste_base_id + 0x200 + 0x0D, ItemClassification.progression),
    ItemName.bumpers:      CelesteItemData(celeste_base_id + 0x200 + 0x0E, ItemClassification.progression),
    ItemName.kevin_blocks: CelesteItemData(celeste_base_id + 0x200 + 0x0F, ItemClassification.progression),

    ItemName.pink_clouds:       CelesteItemData(celeste_base_id + 0x200 + 0x10, ItemClassification.progression),
    ItemName.badeline_boosters: CelesteItemData(celeste_base_id + 0x200 + 0x11, ItemClassification.progression),

    ItemName.fire_ice_balls: CelesteItemData(celeste_base_id + 0x200 + 0x12, ItemClassification.progression),
    ItemName.core_toggles:   CelesteItemData(celeste_base_id + 0x200 + 0x13, ItemClassification.progression),
    ItemName.core_blocks:    CelesteItemData(celeste_base_id + 0x200 + 0x14, ItemClassification.progression),

    ItemName.pufferfish:             CelesteItemData(celeste_base_id + 0x200 + 0x15, ItemClassification.progression),
    ItemName.jellyfish:              CelesteItemData(celeste_base_id + 0x200 + 0x16, ItemClassification.progression),
    ItemName.breaker_boxes:          CelesteItemData(celeste_base_id + 0x200 + 0x17, ItemClassification.progression),
    ItemName.dash_refills:           CelesteItemData(celeste_base_id + 0x200 + 0x18, ItemClassification.progression),
    ItemName.double_dash_refills:    CelesteItemData(celeste_base_id + 0x200 + 0x19, ItemClassification.progression),
    ItemName.yellow_cassette_blocks: CelesteItemData(celeste_base_id + 0x200 + 0x1A, ItemClassification.progression),
    ItemName.green_cassette_blocks:  CelesteItemData(celeste_base_id + 0x200 + 0x1B, ItemClassification.progression),
    ItemName.bird:                   CelesteItemData(celeste_base_id + 0x200 + 0x23, ItemClassification.progression),

    ItemName.dash_switches: CelesteItemData(celeste_base_id + 0x200 + 0x1C, ItemClassification.progression),
    ItemName.seekers:       CelesteItemData(celeste_base_id + 0x200 + 0x1D, ItemClassification.progression),
}

def add_checkpoint_to_table(id: int, name: str):
    checkpoint_item_data_table[name] = CelesteItemData(id, ItemClassification.progression)

def add_key_to_table(id: int, name: str):
    key_item_data_table[name] = CelesteItemData(id, ItemClassification.progression)

def generate_item_data_table() -> Dict[int, CelesteItemData]:
    return {**collectable_item_data_table,
            **trap_item_data_table,
            **checkpoint_item_data_table,
            **key_item_data_table,
            **interactable_item_data_table}

def generate_item_table() -> Dict[str, int]:
    return {name: data.code for name, data in generate_item_data_table().items() if data.code is not None}
