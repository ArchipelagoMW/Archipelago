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

item_data_table: Dict[str, CelesteItemData] = {**collectable_item_data_table, **interactable_item_data_table}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
