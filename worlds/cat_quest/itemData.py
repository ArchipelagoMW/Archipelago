from BaseClasses import ItemClassification
from typing import TypedDict, List

class Item(TypedDict):
    name: str
    inGameId: str
    classification: ItemClassification


royal_arts: List[Item] = [
    {"name": "Royal Art of Water Walking", "inGameId": "art.water", "classification": ItemClassification.progression},
    {"name": "Royal Art of Flight", "inGameId": "art.flight", "classification": ItemClassification.progression},
]

skills: List[Item] = [
    {"name": "Flamepurr", "inGameId": "skill.flamepurr", "classification": ItemClassification.progression},
    {"name": "Healing Paw", "inGameId": "skill.healing_paw", "classification": ItemClassification.useful},
    {"name": "Lightnyan", "inGameId": "skill.lightnyan", "classification": ItemClassification.progression},
    {"name": "Cattrap", "inGameId": "skill.cattrap", "classification": ItemClassification.progression},
    {"name": "Purrserk", "inGameId": "skill.purrserk", "classification": ItemClassification.useful},
    {"name": "Astropaw", "inGameId": "skill.astropaw", "classification": ItemClassification.progression},
    {"name": "Freezepaw", "inGameId": "skill.freezepaw", "classification": ItemClassification.progression},
]

prog_skills: List[Item] = [
    {"name": "Progressive Flamepurr", "inGameId": "skill.flamepurr", "classification": ItemClassification.progression},
    {"name": "Progressive Healing Paw", "inGameId": "skill.healing_paw", "classification": ItemClassification.useful},
    {"name": "Progressive Lightnyan", "inGameId": "skill.lightnyan", "classification": ItemClassification.progression},
    {"name": "Progressive Cattrap", "inGameId": "skill.cattrap", "classification": ItemClassification.progression},
    {"name": "Progressive Purrserk", "inGameId": "skill.purrserk", "classification": ItemClassification.useful},
    {"name": "Progressive Astropaw", "inGameId": "skill.astropaw", "classification": ItemClassification.progression},
    {"name": "Progressive Freezepaw", "inGameId": "skill.freezepaw", "classification": ItemClassification.progression},
]

prog_skill_uprades: List[Item] = [
    {"name": "Progressive Flamepurr Upgrade", "inGameId": "skillupgrade.flamepurr", "classification": ItemClassification.useful},
    {"name": "Progressive Healing Paw Upgrade", "inGameId": "skillupgrade.healing_paw", "classification": ItemClassification.useful},
    {"name": "Progressive Lightnyan Upgrade", "inGameId": "skillupgrade.lightnyan", "classification": ItemClassification.useful},
    {"name": "Progressive Cattrap Upgrade", "inGameId": "skillupgrade.cattrap", "classification": ItemClassification.useful},
    {"name": "Progressive Purrserk Upgrade", "inGameId": "skillupgrade.purrserk", "classification": ItemClassification.useful},
    {"name": "Progressive Astropaw Upgrade", "inGameId": "skillupgrade.astropaw", "classification": ItemClassification.useful},
    {"name": "Progressive Freezepaw Upgrade", "inGameId": "skillupgrade.freezepaw", "classification": ItemClassification.useful},
]

prog_magic_levels: List[Item] = [
    {"name": "Progressive Magic Level", "inGameId": "magiclevel.magiclevel", "classification": ItemClassification.useful},
]

misc: List[Item] = [
    # Golden Key
    {"name": "Golden Key", "inGameId": "key.golden", "classification": ItemClassification.useful},
]

fillers: List[Item] = [
    # Gold
    {"name": "50 Gold", "inGameId": "gold.50", "classification": ItemClassification.filler},
    {"name": "500 Gold", "inGameId": "gold.500", "classification": ItemClassification.filler},
    {"name": "750 Gold", "inGameId": "gold.750", "classification": ItemClassification.filler},
    {"name": "1000 Gold", "inGameId": "gold.1000", "classification": ItemClassification.filler},
    {"name": "5000 Gold", "inGameId": "gold.5000", "classification": ItemClassification.filler},

    # Exp
    {"name": "500 Exp", "inGameId": "exp.500", "classification": ItemClassification.filler},
    {"name": "1000 Exp", "inGameId": "exp.1000", "classification": ItemClassification.filler},
    {"name": "5000 Exp", "inGameId": "exp.5000", "classification": ItemClassification.filler},
    {"name": "7500 Exp", "inGameId": "exp.7500", "classification": ItemClassification.filler},
    {"name": "10K Exp", "inGameId": "exp.10000", "classification": ItemClassification.filler},
    {"name": "20K Exp", "inGameId": "exp.20000", "classification": ItemClassification.filler},
]