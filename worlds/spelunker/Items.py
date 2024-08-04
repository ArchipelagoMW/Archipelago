from typing import Dict, Set, List, NamedTuple, Optional
from BaseClasses import ItemClassification

class ItemData(NamedTuple):
    category: str
    code: Optional[int]
    classification: ItemClassification
    amount: Optional[int] = 1

item_table: Dict[str, ItemData] = {
    "Money Bag": ItemData("Treasure", 0x696969, ItemClassification.filler, 0),
    "Coin": ItemData("Treasure", 0x69696A, ItemClassification.filler, 0),
    "Miracle": ItemData("Treasure", 0x69696B, ItemClassification.filler, 0),
    "Diamond": ItemData("Treasure", 0x69696C, ItemClassification.filler, 0),
    "Dynamite": ItemData("Equipment", 0x69696D, ItemClassification.progression, 18),
    "Flare": ItemData("Equipment", 0x69696E, ItemClassification.progression, 9),
    "Blue Key": ItemData("Equipment", 0x69696F, ItemClassification.progression, 9),
    "Red Key": ItemData("Equipment", 0x696970, ItemClassification.progression, 6),

    "1-Up": ItemData("Powerups", 0x696971, ItemClassification.useful, 0),
    "Multiplier": ItemData("Powerups", 0x696972, ItemClassification.useful, 0),
    "Potion": ItemData("Powerups", 0x696973, ItemClassification.useful, 0),
    "Invincibility": ItemData("Powerups", 0x696974, ItemClassification.useful, 0),

    "Golden Pyramid": ItemData("Events", None, ItemClassification.progression, 0)
}

filler_items: List[str] = [
    "Money Bag",
    "Coin",
    "Diamond",
    "Miracle"
]
useful_items: List[str] = [
    "1-Up",
    "Multiplier",
    "Potion",
    "Invincibility"
]

def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        if data.category != "Events":
            categories.setdefault(data.category, set()).add(name)

    return categories
