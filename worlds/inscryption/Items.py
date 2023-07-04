from BaseClasses import ItemClassification
from typing import TypedDict, Set, List

from BaseClasses import Item


base_id = 147000


class InscryptionItem(Item):
    name: str = "Inscryption"


class ItemDict(TypedDict):
    name: str
    count: int
    classification: ItemClassification


item_table: List[ItemDict] = [
    {'name': "Stinkbug Card",
     'count': 1,
     'classification': ItemClassification.useful},
    {'name': "Stunted Wolf Card",
     'count': 1,
     'classification': ItemClassification.useful},
    {'name': "Wardrobe Key",
     'count': 1,
     'classification': ItemClassification.progression},
    {'name': "Skink Card",
     'count': 1,
     'classification': ItemClassification.useful},
    {'name': "Ant Cards",
     'count': 1,
     'classification': ItemClassification.useful},
    {'name': "Caged Wolf Card",
     'count': 1,
     'classification': ItemClassification.progression},
    {'name': "Squirrel Totem Head",
     'count': 1,
     'classification': ItemClassification.useful},
    {'name': "Dagger",
     'count': 1,
     'classification': ItemClassification.progression},
    {'name': "Film Roll",
     'count': 1,
     'classification': ItemClassification.progression},
    {'name': "Ring",
     'count': 1,
     'classification': ItemClassification.useful},
    {'name': "Magnificus Eye",
     'count': 1,
     'classification': ItemClassification.progression},
    {'name': "Clover Plant",
     'count': 1,
     'classification': ItemClassification.useful},
    {'name': "Extra Candle",
     'count': 1,
     'classification': ItemClassification.useful},
    {'name': "Bee Figurine",
     'count': 1,
     'classification': ItemClassification.useful},
    {'name': "Greater Smoke",
     'count': 1,
     'classification': ItemClassification.useful},
    {'name': "Angler Hook",
     'count': 1,
     'classification': ItemClassification.useful},
    {'name': "Currency",
     'count': 1,
     'classification': ItemClassification.filler},

]
