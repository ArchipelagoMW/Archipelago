from BaseClasses import ItemClassification
from typing import TypedDict, Dict, List, Set

class ItemDict(TypedDict):
    name: str
    id: int
    count: int
    classification: ItemClassification

base_id = 82000

item_table: List[ItemDict] = [
    {"name": "Stick", "id": base_id + 1, "count": 0, "classification": ItemClassification.progression_skip_balancing},
    {"name": "Seashell", "id": base_id + 2, "count": 23, "classification": ItemClassification.progression_skip_balancing},
    {"name": "Golden Feather", "id": base_id + 3, "count": 0, "classification": ItemClassification.progression},
    {"name": "Silver Feather", "id": base_id + 4, "count": 0, "classification": ItemClassification.useful},
    {"name": "Bucket", "id": base_id + 5, "count": 0, "classification": ItemClassification.progression},
    {"name": "Bait", "id": base_id + 6, "count": 2, "classification": ItemClassification.filler},
    {"name": "Progressive Fishing Rod", "id": base_id + 7, "count": 2, "classification": ItemClassification.progression},
    {"name": "Shovel", "id": base_id + 8, "count": 1, "classification": ItemClassification.progression},
    {"name": "Toy Shovel", "id": base_id + 9, "count": 0, "classification": ItemClassification.progression_skip_balancing},
    {"name": "Compass", "id": base_id + 10, "count": 1, "classification": ItemClassification.useful},
    {"name": "Medal", "id": base_id + 11, "count": 3, "classification": ItemClassification.filler},
    {"name": "Shell Necklace", "id": base_id + 12, "count": 1, "classification": ItemClassification.progression},
    {"name": "Wristwatch", "id": base_id + 13, "count": 1, "classification": ItemClassification.progression},
    {"name": "Motorboat Key", "id": base_id + 14, "count": 1, "classification": ItemClassification.progression},
    {"name": "Pickaxe", "id": base_id + 15, "count": 3, "classification": ItemClassification.useful},
    {"name": "Fishing Journal", "id": base_id + 16, "count": 1, "classification": ItemClassification.useful},
    {"name": "A Stormy View Map", "id": base_id + 17, "count": 1, "classification": ItemClassification.filler},
    {"name": "The King Map", "id": base_id + 18, "count": 1, "classification": ItemClassification.filler},
    {"name": "The Treasure of Sid Beach Map", "id": base_id + 19, "count": 1, "classification": ItemClassification.filler},
    {"name": "In Her Shadow Map", "id": base_id + 20, "count": 1, "classification": ItemClassification.filler},
    {"name": "Sunhat", "id": base_id + 21, "count": 1, "classification": ItemClassification.filler},
    {"name": "Baseball Cap", "id": base_id + 22, "count": 1, "classification": ItemClassification.filler},
    {"name": "Provincial Park Hat", "id": base_id + 23, "count": 1, "classification": ItemClassification.filler},
    {"name": "Headband", "id": base_id + 24, "count": 1, "classification": ItemClassification.progression},
    {"name": "Running Shoes", "id": base_id + 25, "count": 1, "classification": ItemClassification.useful},
    {"name": "Camping Permit", "id": base_id + 26, "count": 1, "classification": ItemClassification.progression},
    {"name": "Walkie Talkie", "id": base_id + 27, "count": 0, "classification": ItemClassification.useful},
    
    # Not in the item pool for now
    #{"name": "Boating Manual", "id": base_id + ~, "count": 1, "classification": ItemClassification.filler},

    # Different Coin Amounts (Fillers)
    {"name": "7 Coins", "id": base_id + 28, "count": 3, "classification": ItemClassification.filler},
    {"name": "15 Coins", "id": base_id + 29, "count": 1, "classification": ItemClassification.filler},
    {"name": "18 Coins", "id": base_id + 30, "count": 1, "classification": ItemClassification.filler},
    {"name": "21 Coins", "id": base_id + 31, "count": 2, "classification": ItemClassification.filler},
    {"name": "25 Coins", "id": base_id + 32, "count": 7, "classification": ItemClassification.filler},
    {"name": "27 Coins", "id": base_id + 33, "count": 1, "classification": ItemClassification.filler},
    {"name": "32 Coins", "id": base_id + 34, "count": 1, "classification": ItemClassification.useful},
    {"name": "33 Coins", "id": base_id + 35, "count": 6, "classification": ItemClassification.useful},
    {"name": "50 Coins", "id": base_id + 36, "count": 1, "classification": ItemClassification.useful},

    # Filler item determined by settings
    {"name": "13 Coins", "id": base_id + 37, "count": 0, "classification": ItemClassification.filler},
]

group_table: Dict[str, Set[str]] = {
    "Coins": {"7 Coins", "13 Coins", "15 Coins", "18 Coins", "21 Coins", "25 Coins", "27 Coins", "32 Coins", "33 Coins", "50 Coins"},
    "Maps": {"A Stormy View Map", "The King Map", "The Treasure of Sid Beach Map", "In Her Shadow Map"},
}
