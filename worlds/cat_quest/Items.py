from BaseClasses import ItemClassification
from typing import List, TypedDict

class Item(TypedDict):
    name: str
    id: int
    inGameId: str
    count: int
    classification: ItemClassification

Items: List[ItemDict] = [
    # Royal Arts
    {"name": "Royal Art of Water Walking", "id": base_id + 1, "inGameId": "royal.water", "count": 1, "classification": ItemClassification.progression},
    {"name": "Royal Art of Flight", "id": base_id + 1, "inGameId": "royal.flight", "count": 1, "classification": ItemClassification.progression},

    # Skills
    {"name": "Flamepurr", "id": base_id + 1, "inGameId": "skill.flamepurr", "count": 1, "classification": ItemClassification.useful},
    {"name": "Healing Paw", "id": base_id + 1, "inGameId": "skill.healing", "count": 1, "classification": ItemClassification.useful},
    {"name": "Lightnyan", "id": base_id + 1, "inGameId": "skill.lightnyan", "count": 1, "classification": ItemClassification.useful},
    {"name": "Cattrap", "id": base_id + 1, "inGameId": "skill.cattrap", "count": 1, "classification": ItemClassification.useful},
    {"name": "Purrserk", "id": base_id + 1, "inGameId": "skill.purrserk", "count": 1, "classification": ItemClassification.useful},
    {"name": "Astropaw", "id": base_id + 1, "inGameId": "skill.astropaw", "count": 1, "classification": ItemClassification.useful},
    
    # Golden Key
    {"name": "Golden Key", "id": base_id + 1, "inGameId": "key.golden", "count": 1, "classification": ItemClassification.useful},

    # Gold
    {"name": "5 Gold", "id": base_id + 1, "inGameId": "gold.5", "count": 5, "classification": ItemClassification.filler},
    {"name": "8 Gold", "id": base_id + 1, "inGameId": "gold.8", "count": 5, "classification": ItemClassification.filler},
    {"name": "10 Gold", "id": base_id + 1, "inGameId": "gold.10", "count": 5, "classification": ItemClassification.filler},
    {"name": "15 Gold", "id": base_id + 1, "inGameId": "gold.15", "count": 3, "classification": ItemClassification.filler},
    {"name": "20 Gold", "id": base_id + 1, "inGameId": "gold.20", "count": 2, "classification": ItemClassification.filler},
    {"name": "30 Gold", "id": base_id + 1, "inGameId": "gold.30", "count": 1, "classification": ItemClassification.filler},
    {"name": "50 Gold", "id": base_id + 1, "inGameId": "gold.50", "count": 1, "classification": ItemClassification.filler},

    # Exp
    {"name": "5 Exp", "id": base_id + 1, "inGameId": "exp.5", "count": 5, "classification": ItemClassification.filler},
    {"name": "8 Exp", "id": base_id + 1, "inGameId": "exp.8", "count": 5, "classification": ItemClassification.filler},
    {"name": "10 Exp", "id": base_id + 1, "inGameId": "exp.10", "count": 5, "classification": ItemClassification.filler},
    {"name": "15 Exp", "id": base_id + 1, "inGameId": "exp.15", "count": 3, "classification": ItemClassification.filler},
    {"name": "20 Exp", "id": base_id + 1, "inGameId": "exp.20", "count": 2, "classification": ItemClassification.filler},
    {"name": "30 Exp", "id": base_id + 1, "inGameId": "exp.30", "count": 1, "classification": ItemClassification.filler},
    {"name": "50 Exp", "id": base_id + 1, "inGameId": "exp.50", "count": 1, "classification": ItemClassification.filler},

    # Balancing fillers
    {"name": "10 Gold", "id": base_id + 1, "inGameId": "gold.10", "count": 0, "classification": ItemClassification.filler},
    {"name": "10 Exp", "id": base_id + 1, "inGameId": "exp.10", "count": 0, "classification": ItemClassification.filler},
]