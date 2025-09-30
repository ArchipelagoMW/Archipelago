from typing import cast

from BaseClasses import ItemClassification

from . import static_logic as static_witness_logic
from .item_definition_classes import DoorItemDefinition, ItemCategory, ItemData
from .static_locations import ID_START

ITEM_DATA: dict[str, ItemData] = {}
ITEM_GROUPS: dict[str, set[str]] = {}

# Useful items that are treated specially at generation time and should not be automatically added to the player's
# item list during get_progression_items.
_special_usefuls: list[str] = ["Puzzle Skip"]

ALWAYS_GOOD_SYMBOL_ITEMS: set[str] = {"Dots", "Black/White Squares", "Symmetry", "Shapers", "Stars"}

MODE_SPECIFIC_GOOD_ITEMS: dict[str, set[str]] = {
    "none": set(),
    "sigma_normal": set(),
    "sigma_expert": {"Triangles"},
    "umbra_variety": {"Triangles"}
}

MODE_SPECIFIC_GOOD_DISCARD_ITEMS: dict[str, set[str]] = {
    "none": {"Triangles"},
    "sigma_normal": {"Triangles"},
    "sigma_expert": {"Arrows"},
    "umbra_variety": set()  # Variety Discards use both Arrows and Triangles, so neither of them are that useful alone
}


def populate_items() -> None:
    for item_name, definition in static_witness_logic.ALL_ITEMS.items():
        ap_item_code = definition.local_code + ID_START
        classification: ItemClassification = ItemClassification.filler
        local_only: bool = False

        if definition.category is ItemCategory.SYMBOL:
            classification = ItemClassification.progression
            ITEM_GROUPS.setdefault("Symbols", set()).add(item_name)
        elif definition.category is ItemCategory.DOOR:
            classification = ItemClassification.progression

            first_entity_hex = cast(DoorItemDefinition, definition).panel_id_hexes[0]
            entity_type = static_witness_logic.ENTITIES_BY_HEX[first_entity_hex]["entityType"]

            if entity_type == "Door":
                ITEM_GROUPS.setdefault("Doors", set()).add(item_name)
            elif entity_type == "Panel":
                ITEM_GROUPS.setdefault("Panel Keys", set()).add(item_name)
            elif entity_type in {"EP", "Obelisk Side", "Obelisk"}:
                ITEM_GROUPS.setdefault("Obelisk Keys", set()).add(item_name)
            else:
                raise ValueError(f"Couldn't figure out what type of door item {definition} is.")

        elif definition.category is ItemCategory.LASER:
            classification = ItemClassification.progression_skip_balancing
            ITEM_GROUPS.setdefault("Lasers", set()).add(item_name)
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


def get_item_to_door_mappings() -> dict[int, list[int]]:
    output: dict[int, list[int]] = {}
    for item_data in ITEM_DATA.values():
        if not isinstance(item_data.definition, DoorItemDefinition) or item_data.ap_code is None:
            continue
        output[item_data.ap_code] = [int(hex_string, 16) for hex_string in item_data.definition.panel_id_hexes]
    return output


populate_items()
