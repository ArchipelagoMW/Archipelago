from BaseClasses import ItemClassification
from typing import TypedDict, Dict, List, Set


class ItemDict(TypedDict):
    name: str
    id: int
    count: int
    classification: ItemClassification

base_id = 82000

item_table: List[ItemDict] = [
    {"name": "Stick", "id": base_id + 1, "count": 125, "classification": ItemClassification.useful}
]