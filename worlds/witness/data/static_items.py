from typing import Dict, List

from BaseClasses import ItemClassification

from . import static_logic as static_witness_logic
from .item_definition_classes import DoorItemDefinition, ItemCategory, ItemData
from .static_locations import ID_START

ITEM_DATA: Dict[str, ItemData] = {}
ITEM_GROUPS: Dict[str, List[str]] = {}

# Useful items that are treated specially at generation time and should not be automatically added to the player's
# item list during get_progression_items.
_special_usefuls: List[str] = ["Puzzle Skip"]


def populate_items() -> None:
    for item_name, definition in static_witness_logic.ALL_ITEMS.items():
        ap_item_code = definition.local_code + ID_START
        classification: ItemClassification = ItemClassification.filler
        local_only: bool = False

        if definition.category is ItemCategory.SYMBOL:
            classification = ItemClassification.progression
            ITEM_GROUPS.setdefault("Symbols", []).append(item_name)
        elif definition.category is ItemCategory.DOOR:
            classification = ItemClassification.progression
            ITEM_GROUPS.setdefault("Doors", []).append(item_name)
        elif definition.category is ItemCategory.LASER:
            classification = ItemClassification.progression_skip_balancing
            ITEM_GROUPS.setdefault("Lasers", []).append(item_name)
        elif definition.category is ItemCategory.USEFUL:
            classification = ItemClassification.useful
        elif definition.category is ItemCategory.FILLER:
            if item_name in ["Energy Fill (Small)"]:
                local_only = True
            classification = ItemClassification.filler
        elif definition.category is ItemCategory.TRAP:
            classification = ItemClassification.trap
        elif definition.category is ItemCategory.JOKE:
            classification = ItemClassification.filler

        ITEM_DATA[item_name] = ItemData(ap_item_code, definition,
                                        classification, local_only)


def get_item_to_door_mappings() -> Dict[int, List[int]]:
    output: Dict[int, List[int]] = {}
    for item_name, item_data in ITEM_DATA.items():
        if not isinstance(item_data.definition, DoorItemDefinition):
            continue
        output[item_data.ap_code] = [int(hex_string, 16) for hex_string in item_data.definition.panel_id_hexes]
    return output


populate_items()
