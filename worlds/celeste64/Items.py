from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification
from .Names import ItemName


celeste_64_base_id: int = 0xCA0000


class Celeste64Item(Item):
    game = "Celeste 64"


class Celeste64ItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler


collectable_item_data_table: Dict[str, Celeste64ItemData] = {
    ItemName.strawberry: Celeste64ItemData(celeste_64_base_id + 0x0, ItemClassification.progression_skip_balancing),
    ItemName.raspberry:  Celeste64ItemData(celeste_64_base_id + 0x9, ItemClassification.filler),
}

unlockable_item_data_table: Dict[str, Celeste64ItemData] = {
    ItemName.dash_refill:        Celeste64ItemData(celeste_64_base_id + 0x1, ItemClassification.progression),
    ItemName.double_dash_refill: Celeste64ItemData(celeste_64_base_id + 0x2, ItemClassification.progression),
    ItemName.feather:            Celeste64ItemData(celeste_64_base_id + 0x3, ItemClassification.progression),
    ItemName.coin:               Celeste64ItemData(celeste_64_base_id + 0x4, ItemClassification.progression),
    ItemName.cassette:           Celeste64ItemData(celeste_64_base_id + 0x5, ItemClassification.progression),
    ItemName.traffic_block:      Celeste64ItemData(celeste_64_base_id + 0x6, ItemClassification.progression),
    ItemName.spring:             Celeste64ItemData(celeste_64_base_id + 0x7, ItemClassification.progression),
    ItemName.breakables:         Celeste64ItemData(celeste_64_base_id + 0x8, ItemClassification.progression),
}

move_item_data_table: Dict[str, Celeste64ItemData] = {
    ItemName.ground_dash: Celeste64ItemData(celeste_64_base_id + 0xA, ItemClassification.progression),
    ItemName.air_dash:    Celeste64ItemData(celeste_64_base_id + 0xB, ItemClassification.progression),
    ItemName.skid_jump:   Celeste64ItemData(celeste_64_base_id + 0xC, ItemClassification.progression),
    ItemName.climb:       Celeste64ItemData(celeste_64_base_id + 0xD, ItemClassification.progression),
}

checkpoint_item_data_table: Dict[str, Celeste64ItemData] = {
    ItemName.checkpoint_1:  Celeste64ItemData(celeste_64_base_id + 0x20, ItemClassification.progression),
    ItemName.checkpoint_2:  Celeste64ItemData(celeste_64_base_id + 0x21, ItemClassification.progression),
    ItemName.checkpoint_3:  Celeste64ItemData(celeste_64_base_id + 0x22, ItemClassification.progression),
    ItemName.checkpoint_4:  Celeste64ItemData(celeste_64_base_id + 0x23, ItemClassification.progression),
    ItemName.checkpoint_5:  Celeste64ItemData(celeste_64_base_id + 0x24, ItemClassification.progression),
    ItemName.checkpoint_6:  Celeste64ItemData(celeste_64_base_id + 0x25, ItemClassification.progression),
    ItemName.checkpoint_7:  Celeste64ItemData(celeste_64_base_id + 0x26, ItemClassification.progression),
    ItemName.checkpoint_8:  Celeste64ItemData(celeste_64_base_id + 0x27, ItemClassification.progression),
    ItemName.checkpoint_9:  Celeste64ItemData(celeste_64_base_id + 0x28, ItemClassification.progression),
    ItemName.checkpoint_10: Celeste64ItemData(celeste_64_base_id + 0x29, ItemClassification.progression),
}

trap_item_data_table: Dict[str, Celeste64ItemData] = {
    ItemName.bald_trap:       Celeste64ItemData(celeste_64_base_id + 0x30, ItemClassification.trap),
    ItemName.bubble_trap:     Celeste64ItemData(celeste_64_base_id + 0x31, ItemClassification.trap),
    ItemName.hiccup_trap:     Celeste64ItemData(celeste_64_base_id + 0x32, ItemClassification.trap),
    ItemName.ice_trap:        Celeste64ItemData(celeste_64_base_id + 0x33, ItemClassification.trap),
    ItemName.invisible_trap:  Celeste64ItemData(celeste_64_base_id + 0x34, ItemClassification.trap),
    ItemName.literature_trap: Celeste64ItemData(celeste_64_base_id + 0x35, ItemClassification.trap),
    ItemName.reverse_trap:    Celeste64ItemData(celeste_64_base_id + 0x36, ItemClassification.trap),
    ItemName.stun_trap:       Celeste64ItemData(celeste_64_base_id + 0x37, ItemClassification.trap),
    ItemName.zoom_in_trap:    Celeste64ItemData(celeste_64_base_id + 0x38, ItemClassification.trap),
    ItemName.zoom_out_trap:   Celeste64ItemData(celeste_64_base_id + 0x39, ItemClassification.trap),
}

item_data_table: Dict[str, Celeste64ItemData] = {**collectable_item_data_table,
                                                 **unlockable_item_data_table,
                                                 **move_item_data_table,
                                                 **checkpoint_item_data_table,
                                                 **trap_item_data_table}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
