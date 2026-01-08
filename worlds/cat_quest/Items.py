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
    {"name": "Flamepurr", "id": base_id + 3, "inGameId": "skill.flamepurr", "count": 1, "classification": ItemClassification.progression},
    {"name": "Healing Paw", "id": base_id + 4, "inGameId": "skill.healing_paw", "count": 1, "classification": ItemClassification.useful},
    {"name": "Lightnyan", "id": base_id + 5, "inGameId": "skill.lightnyan", "count": 1, "classification": ItemClassification.progression},
    {"name": "Cattrap", "id": base_id + 6, "inGameId": "skill.cattrap", "count": 1, "classification": ItemClassification.progression},
    {"name": "Purrserk", "id": base_id + 7, "inGameId": "skill.purrserk", "count": 1, "classification": ItemClassification.useful},
    {"name": "Astropaw", "id": base_id + 8, "inGameId": "skill.astropaw", "count": 1, "classification": ItemClassification.progression},
    {"name": "Freezepaw", "id": base_id + 9, "inGameId": "skill.freezepaw", "count": 1, "classification": ItemClassification.progression},
    
    # Golden Key
    {"name": "Golden Key", "id": base_id + 10, "inGameId": "key.golden", "count": 1, "classification": ItemClassification.useful},

    # Gold
    {"name": "50 Gold", "id": base_id + 11, "inGameId": "gold.50", "count": 1, "classification": ItemClassification.filler},
    {"name": "500 Gold", "id": base_id + 12, "inGameId": "gold.500", "count": 3, "classification": ItemClassification.filler},
    {"name": "750 Gold", "id": base_id + 13, "inGameId": "gold.750", "count": 5, "classification": ItemClassification.filler},
    {"name": "1000 Gold", "id": base_id + 14, "inGameId": "gold.1000", "count": 7, "classification": ItemClassification.filler},
    {"name": "5000 Gold", "id": base_id + 15, "inGameId": "gold.5000", "count": 2, "classification": ItemClassification.filler},
    {"name": "10K Gold", "id": base_id + 16, "inGameId": "gold.10000", "count": 1, "classification": ItemClassification.filler},

    # Exp
    {"name": "500 Exp", "id": base_id + 17, "inGameId": "exp.500", "count": 0, "classification": ItemClassification.filler},
    {"name": "1000 Exp", "id": base_id + 18, "inGameId": "exp.1000", "count": 0, "classification": ItemClassification.filler},
    {"name": "5000 Exp", "id": base_id + 19, "inGameId": "exp.5000", "count": 5, "classification": ItemClassification.filler},
    {"name": "7500 Exp", "id": base_id + 20, "inGameId": "exp.7500", "count": 5, "classification": ItemClassification.filler},
    {"name": "10K Exp", "id": base_id + 21, "inGameId": "exp.10000", "count": 4, "classification": ItemClassification.filler},
    {"name": "20K Exp", "id": base_id + 22, "inGameId": "exp.20000", "count": 4, "classification": ItemClassification.filler},
    {"name": "50K Exp", "id": base_id + 23, "inGameId": "exp.50000", "count": 2, "classification": ItemClassification.filler},
    {"name": "100K Exp", "id": base_id + 24, "inGameId": "exp.100000", "count": 1, "classification": ItemClassification.filler},
]

filler_items: List[Item] = [
    # Balancing filler
    {"name": "500 Gold", "id": base_id + 12, "inGameId": "gold.500", "count": 0, "classification": ItemClassification.filler},
    {"name": "500 Exp", "id": base_id + 17, "inGameId": "exp.500", "count": 0, "classification": ItemClassification.filler},
    {"name": "1000 Exp", "id": base_id + 18, "inGameId": "exp.1000", "count": 0, "classification": ItemClassification.filler},
]