from BaseClasses import ItemClassification
from typing import TypedDict, List

class Item(TypedDict):
    name: str
    id: int
    inGameId: str
    count: int
    classification: ItemClassification

base_id = 123000

items: List[Item] = [
    # Royal Arts
    {"name": "Royal Art of Water Walking", "id": base_id + 1, "inGameId": "art.water", "count": 1, "classification": ItemClassification.progression},
    {"name": "Royal Art of Flight", "id": base_id + 2, "inGameId": "art.flight", "count": 1, "classification": ItemClassification.progression},

    # Skills
    {"name": "Flamepurr", "id": base_id + 3, "inGameId": "skill.flamepurr", "count": 1, "classification": ItemClassification.useful},
    {"name": "Healing Paw", "id": base_id + 4, "inGameId": "skill.healing_paw", "count": 1, "classification": ItemClassification.useful},
    {"name": "Lightnyan", "id": base_id + 5, "inGameId": "skill.lightnyan", "count": 1, "classification": ItemClassification.useful},
    {"name": "Cattrap", "id": base_id + 6, "inGameId": "skill.cattrap", "count": 1, "classification": ItemClassification.useful},
    {"name": "Purrserk", "id": base_id + 7, "inGameId": "skill.purrserk", "count": 1, "classification": ItemClassification.useful},
    {"name": "Astropaw", "id": base_id + 8, "inGameId": "skill.astropaw", "count": 1, "classification": ItemClassification.useful},
    {"name": "Freezepaw", "id": base_id + 8, "inGameId": "skill.freezepaw", "count": 1, "classification": ItemClassification.useful},
    
    # Golden Key
    {"name": "Golden Key", "id": base_id + 9, "inGameId": "key.golden", "count": 1, "classification": ItemClassification.useful},

    # Gold
    {"name": "50 Gold", "id": base_id + 10, "inGameId": "gold.50", "count": 2, "classification": ItemClassification.filler},
    {"name": "200 Gold", "id": base_id + 11, "inGameId": "gold.200", "count": 3, "classification": ItemClassification.filler},
    {"name": "500 Gold", "id": base_id + 12, "inGameId": "gold.500", "count": 5, "classification": ItemClassification.filler},
    {"name": "750 Gold", "id": base_id + 13, "inGameId": "gold.750", "count": 2, "classification": ItemClassification.filler},
    {"name": "1000 Gold", "id": base_id + 14, "inGameId": "gold.1000", "count": 1, "classification": ItemClassification.filler},

    # Exp
    {"name": "500 Exp", "id": base_id + 15, "inGameId": "exp.500", "count": 5, "classification": ItemClassification.filler},
    {"name": "1000 Exp", "id": base_id + 16, "inGameId": "exp.1000", "count": 5, "classification": ItemClassification.filler},
    {"name": "5000 Exp", "id": base_id + 17, "inGameId": "exp.5000", "count": 5, "classification": ItemClassification.filler},
    {"name": "7500 Exp", "id": base_id + 18, "inGameId": "exp.7500", "count": 5, "classification": ItemClassification.filler},
    {"name": "10000 Exp", "id": base_id + 19, "inGameId": "exp.10000", "count": 5, "classification": ItemClassification.filler},
    {"name": "20000 Exp", "id": base_id + 20, "inGameId": "exp.20000", "count": 2, "classification": ItemClassification.filler},

    # Balancing filler
    {"name": "500 Exp", "id": base_id + 21, "inGameId": "exp.500", "count": 0, "classification": ItemClassification.filler},
]