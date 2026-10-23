"""
Ys I Chronicles - Item Definitions

All items that can be randomized in Ys I.
Game IDs are verified from PC version (ys1plus.exe) memory at:
  Array 1 (ownership): 0x531990 + game_id * 4
  Array 2 (visibility): 0x53207C + game_id * 4
"""

from typing import Dict, NamedTuple
from enum import IntEnum
from BaseClasses import ItemClassification


class YsItemType(IntEnum):
    """Item type categories."""
    WEAPON = 0
    ARMOR = 1
    SHIELD = 2
    RING = 3
    KEY = 4
    QUEST = 5
    CONSUMABLE = 6
    BOOK = 7
    TRAP = 8
    TREASURE = 9


class YsItemData(NamedTuple):
    """Item definition."""
    code: int                  # AP item ID (YS1_BASE_ID + offset)
    item_type: YsItemType
    classification: ItemClassification
    game_id: int               # PC game internal item ID (0-51)


# Base ID for Ys I items in Archipelago
YS1_BASE_ID = 0x59530000

# =============================================================================
# Item Definitions
# =============================================================================

YS1_ITEMS: Dict[str, YsItemData] = {
    # -------------------------------------------------------------------------
    # Weapons (game_id 0-4)
    # -------------------------------------------------------------------------
    "Short Sword": YsItemData(
        code=YS1_BASE_ID + 1, item_type=YsItemType.WEAPON,
        classification=ItemClassification.useful, game_id=0,
    ),
    "Long Sword": YsItemData(
        code=YS1_BASE_ID + 2, item_type=YsItemType.WEAPON,
        classification=ItemClassification.useful, game_id=1,
    ),
    "Talwar": YsItemData(
        code=YS1_BASE_ID + 3, item_type=YsItemType.WEAPON,
        classification=ItemClassification.useful, game_id=2,
    ),
    "Silver Sword": YsItemData(
        code=YS1_BASE_ID + 4, item_type=YsItemType.WEAPON,
        classification=ItemClassification.progression, game_id=3,
    ),
    "Flame Sword": YsItemData(
        code=YS1_BASE_ID + 5, item_type=YsItemType.WEAPON,
        classification=ItemClassification.progression, game_id=4,
    ),

    # -------------------------------------------------------------------------
    # Shields (game_id 5-9)
    # -------------------------------------------------------------------------
    "Small Shield": YsItemData(
        code=YS1_BASE_ID + 20, item_type=YsItemType.SHIELD,
        classification=ItemClassification.useful, game_id=5,
    ),
    "Middle Shield": YsItemData(
        code=YS1_BASE_ID + 21, item_type=YsItemType.SHIELD,
        classification=ItemClassification.useful, game_id=6,
    ),
    "Large Shield": YsItemData(
        code=YS1_BASE_ID + 22, item_type=YsItemType.SHIELD,
        classification=ItemClassification.useful, game_id=7,
    ),
    "Battle Shield": YsItemData(
        code=YS1_BASE_ID + 23, item_type=YsItemType.SHIELD,
        classification=ItemClassification.progression, game_id=8,
    ),
    "Silver Shield": YsItemData(
        code=YS1_BASE_ID + 24, item_type=YsItemType.SHIELD,
        classification=ItemClassification.progression, game_id=9,
    ),

    # -------------------------------------------------------------------------
    # Armor (game_id 10-14)
    # -------------------------------------------------------------------------
    "Chain Mail": YsItemData(
        code=YS1_BASE_ID + 10, item_type=YsItemType.ARMOR,
        classification=ItemClassification.useful, game_id=10,
    ),
    "Plate Mail": YsItemData(
        code=YS1_BASE_ID + 11, item_type=YsItemType.ARMOR,
        classification=ItemClassification.useful, game_id=11,
    ),
    "Reflex": YsItemData(
        code=YS1_BASE_ID + 12, item_type=YsItemType.ARMOR,
        classification=ItemClassification.useful, game_id=12,
    ),
    "Battle Armor": YsItemData(
        code=YS1_BASE_ID + 13, item_type=YsItemType.ARMOR,
        classification=ItemClassification.progression, game_id=13,
    ),
    "Silver Armor": YsItemData(
        code=YS1_BASE_ID + 14, item_type=YsItemType.ARMOR,
        classification=ItemClassification.progression, game_id=14,
    ),

    # -------------------------------------------------------------------------
    # Rings (game_id 15-19)
    # -------------------------------------------------------------------------
    "Power Ring": YsItemData(
        code=YS1_BASE_ID + 30, item_type=YsItemType.RING,
        classification=ItemClassification.useful, game_id=15,
    ),
    "Shield Ring": YsItemData(
        code=YS1_BASE_ID + 31, item_type=YsItemType.RING,
        classification=ItemClassification.useful, game_id=16,
    ),
    "Timer Ring": YsItemData(
        code=YS1_BASE_ID + 32, item_type=YsItemType.RING,
        classification=ItemClassification.useful, game_id=17,
    ),
    "Heal Ring": YsItemData(
        code=YS1_BASE_ID + 33, item_type=YsItemType.RING,
        classification=ItemClassification.useful, game_id=18,
    ),
    "Evil Ring": YsItemData(
        code=YS1_BASE_ID + 34, item_type=YsItemType.RING,
        classification=ItemClassification.progression, game_id=19,
    ),

    # -------------------------------------------------------------------------
    # Books of Ys (game_id 20-25)
    # -------------------------------------------------------------------------
    "Book of Ys (Hadal)": YsItemData(
        code=YS1_BASE_ID + 40, item_type=YsItemType.BOOK,
        classification=ItemClassification.progression, game_id=20,
    ),
    "Book of Ys (Tovah)": YsItemData(
        code=YS1_BASE_ID + 41, item_type=YsItemType.BOOK,
        classification=ItemClassification.progression, game_id=21,
    ),
    "Book of Ys (Dabbie)": YsItemData(
        code=YS1_BASE_ID + 42, item_type=YsItemType.BOOK,
        classification=ItemClassification.progression, game_id=22,
    ),
    "Book of Ys (Mesa)": YsItemData(
        code=YS1_BASE_ID + 43, item_type=YsItemType.BOOK,
        classification=ItemClassification.progression, game_id=23,
    ),
    "Book of Ys (Gemma)": YsItemData(
        code=YS1_BASE_ID + 44, item_type=YsItemType.BOOK,
        classification=ItemClassification.progression, game_id=24,
    ),
    "Book of Ys (Fact)": YsItemData(
        code=YS1_BASE_ID + 45, item_type=YsItemType.BOOK,
        classification=ItemClassification.progression, game_id=25,
    ),

    # -------------------------------------------------------------------------
    # Keys (game_id 26-31)
    # -------------------------------------------------------------------------
    "Treasure Box Key": YsItemData(
        code=YS1_BASE_ID + 50, item_type=YsItemType.KEY,
        classification=ItemClassification.progression, game_id=26,
    ),
    "Prison Key": YsItemData(
        code=YS1_BASE_ID + 51, item_type=YsItemType.KEY,
        classification=ItemClassification.progression, game_id=27,
    ),
    "Shrine Key": YsItemData(
        code=YS1_BASE_ID + 52, item_type=YsItemType.KEY,
        classification=ItemClassification.progression, game_id=28,
    ),
    "Ivory Key": YsItemData(
        code=YS1_BASE_ID + 53, item_type=YsItemType.KEY,
        classification=ItemClassification.progression, game_id=29,
    ),
    "Marble Key": YsItemData(
        code=YS1_BASE_ID + 54, item_type=YsItemType.KEY,
        classification=ItemClassification.progression, game_id=30,
    ),
    "Darm Key": YsItemData(
        code=YS1_BASE_ID + 55, item_type=YsItemType.KEY,
        classification=ItemClassification.progression, game_id=31,
    ),

    # -------------------------------------------------------------------------
    # Quest Items (game_id 32-49)
    # -------------------------------------------------------------------------
    "Sara's Crystal": YsItemData(
        code=YS1_BASE_ID + 60, item_type=YsItemType.QUEST,
        classification=ItemClassification.progression, game_id=32,
    ),
    "Roda Tree Seed": YsItemData(
        code=YS1_BASE_ID + 61, item_type=YsItemType.QUEST,
        classification=ItemClassification.progression, game_id=33,
    ),
    "Silver Bell": YsItemData(
        code=YS1_BASE_ID + 62, item_type=YsItemType.QUEST,
        classification=ItemClassification.progression, game_id=34,
    ),
    "Silver Harmonica": YsItemData(
        code=YS1_BASE_ID + 63, item_type=YsItemType.QUEST,
        classification=ItemClassification.progression, game_id=35,
    ),
    "Idol": YsItemData(
        code=YS1_BASE_ID + 64, item_type=YsItemType.QUEST,
        classification=ItemClassification.progression, game_id=36,
    ),
    "Rod": YsItemData(
        code=YS1_BASE_ID + 65, item_type=YsItemType.QUEST,
        classification=ItemClassification.progression, game_id=37,
    ),
    "Monocle": YsItemData(
        code=YS1_BASE_ID + 66, item_type=YsItemType.QUEST,
        classification=ItemClassification.progression, game_id=38,
    ),
    "Blue Amulet": YsItemData(
        code=YS1_BASE_ID + 67, item_type=YsItemType.QUEST,
        classification=ItemClassification.progression, game_id=39,
    ),
    "Mask of Eyes": YsItemData(
        code=YS1_BASE_ID + 68, item_type=YsItemType.QUEST,
        classification=ItemClassification.progression, game_id=48,
    ),
    "Blue Necklace": YsItemData(
        code=YS1_BASE_ID + 69, item_type=YsItemType.QUEST,
        classification=ItemClassification.progression, game_id=49,
    ),
    "Hammer": YsItemData(
        code=YS1_BASE_ID + 70, item_type=YsItemType.QUEST,
        classification=ItemClassification.progression, game_id=46,
    ),
    "Sapphire Ring": YsItemData(
        code=YS1_BASE_ID + 71, item_type=YsItemType.QUEST,
        classification=ItemClassification.useful, game_id=41,
    ),

    # -------------------------------------------------------------------------
    # Consumables / Treasures
    # -------------------------------------------------------------------------
    "Heal Potion": YsItemData(
        code=YS1_BASE_ID + 80, item_type=YsItemType.CONSUMABLE,
        classification=ItemClassification.filler, game_id=44,
    ),
    "Wing": YsItemData(
        code=YS1_BASE_ID + 82, item_type=YsItemType.CONSUMABLE,
        classification=ItemClassification.useful, game_id=45,
    ),
    "Mirror": YsItemData(
        code=YS1_BASE_ID + 81, item_type=YsItemType.CONSUMABLE,
        classification=ItemClassification.useful, game_id=47,
    ),
    "Ruby": YsItemData(
        code=YS1_BASE_ID + 83, item_type=YsItemType.TREASURE,
        classification=ItemClassification.useful, game_id=40,
    ),
    "Golden Vase": YsItemData(
        code=YS1_BASE_ID + 84, item_type=YsItemType.TREASURE,
        classification=ItemClassification.useful, game_id=43,
    ),
    "Necklace": YsItemData(
        code=YS1_BASE_ID + 85, item_type=YsItemType.TREASURE,
        classification=ItemClassification.useful, game_id=42,
    ),
    "Bestiary Potion": YsItemData(
        code=YS1_BASE_ID + 86, item_type=YsItemType.CONSUMABLE,
        classification=ItemClassification.filler, game_id=50,
    ),
    "Piece of Paper": YsItemData(
        code=YS1_BASE_ID + 87, item_type=YsItemType.CONSUMABLE,
        classification=ItemClassification.filler, game_id=51,
    ),
}

# =============================================================================
# Lookup Helpers
# =============================================================================

# AP item code -> item name
YS1_ITEM_ID_TO_NAME: Dict[int, str] = {
    data.code: name for name, data in YS1_ITEMS.items()
}

# Item name -> AP item code
item_name_to_id: Dict[str, int] = {
    name: data.code for name, data in YS1_ITEMS.items()
}

# Game ID -> AP item name
GAME_ID_TO_AP_NAME: Dict[int, str] = {
    data.game_id: name for name, data in YS1_ITEMS.items()
}

# AP item code -> game ID
AP_CODE_TO_GAME_ID: Dict[int, int] = {
    data.code: data.game_id for data in YS1_ITEMS.values()
}


def get_item_classification(item_name: str) -> ItemClassification:
    """Get the classification for an item."""
    if item_name in YS1_ITEMS:
        return YS1_ITEMS[item_name].classification
    return ItemClassification.filler


def get_progression_items() -> list:
    return [n for n, d in YS1_ITEMS.items() if d.classification == ItemClassification.progression]


def get_useful_items() -> list:
    return [n for n, d in YS1_ITEMS.items() if d.classification == ItemClassification.useful]


def get_filler_items() -> list:
    return [n for n, d in YS1_ITEMS.items() if d.classification == ItemClassification.filler]
