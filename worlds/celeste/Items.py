from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification
from .Names import ItemName


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

checkpoint_item_data_table: Dict[str, CelesteItemData] = {
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

    ItemName.dream_blocks: CelesteItemData(celeste_base_id + 0x200 + 0x04, ItemClassification.progression),
    ItemName.coins:        CelesteItemData(celeste_base_id + 0x200 + 0x05, ItemClassification.progression),

    ItemName.moving_platforms:  CelesteItemData(celeste_base_id + 0x200 + 0x06, ItemClassification.progression),

    ItemName.blue_boosters: CelesteItemData(celeste_base_id + 0x200 + 0x07, ItemClassification.progression),
    ItemName.blue_clouds:   CelesteItemData(celeste_base_id + 0x200 + 0x08, ItemClassification.progression),
    ItemName.move_blocks:   CelesteItemData(celeste_base_id + 0x200 + 0x09, ItemClassification.progression),

    ItemName.swap_blocks:  CelesteItemData(celeste_base_id + 0x200 + 0x0A, ItemClassification.progression),
    ItemName.red_boosters: CelesteItemData(celeste_base_id + 0x200 + 0x0B, ItemClassification.progression),
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

    ItemName.dash_switch: CelesteItemData(celeste_base_id + 0x200 + 0x1C, ItemClassification.progression),
    ItemName.seeker:      CelesteItemData(celeste_base_id + 0x200 + 0x1D, ItemClassification.progression),
    ItemName.keys:        CelesteItemData(celeste_base_id + 0x200 + 0x1E, ItemClassification.progression),
}

item_data_table: Dict[str, CelesteItemData] = {**collectable_item_data_table,
                                               **checkpoint_item_data_table,
                                               **interactable_item_data_table}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
