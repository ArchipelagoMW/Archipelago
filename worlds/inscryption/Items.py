from BaseClasses import ItemClassification
from typing import TypedDict, List

from BaseClasses import Item


base_id = 147000


class InscryptionItem(Item):
    name: str = "Inscryption"


class ItemDict(TypedDict):
    name: str
    count: int
    classification: ItemClassification


act1_items: List[ItemDict] = [
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
    {'name': "Oil Painting's Clover Plant",
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
     'classification': ItemClassification.useful}
]


act2_items: List[ItemDict] = [
    {'name': "Camera Replica",
     'count': 1,
     'classification': ItemClassification.progression},
    {'name': "Pile Of Meat",
     'count': 1,
     'classification': ItemClassification.progression},
    {'name': "Epitaph Piece",
     'count': 9,
     'classification': ItemClassification.progression},
    {'name': "Epitaph Pieces",
     'count': 3,
     'classification': ItemClassification.progression},
    {'name': "Monocle",
     'count': 1,
     'classification': ItemClassification.progression},
    {'name': "Bone Lord Femur",
     'count': 1,
     'classification': ItemClassification.useful},
    {'name': "Bone Lord Horn",
     'count': 1,
     'classification': ItemClassification.useful},
    {'name': "Bone Lord Holo Key",
     'count': 1,
     'classification': ItemClassification.progression},
    {'name': "Mycologists Holo Key",
     'count': 1,
     'classification': ItemClassification.progression},
    {'name': "Ancient Obol",
     'count': 1,
     'classification': ItemClassification.progression},
    {'name': "Great Kraken Card",
     'count': 1,
     'classification': ItemClassification.useful},
    {'name': "Drowned Soul Card",
     'count': 1,
     'classification': ItemClassification.useful},
    {'name': "Salmon Card",
     'count': 1,
     'classification': ItemClassification.useful},
    {'name': "Dock's Clover Plant",
     'count': 1,
     'classification': ItemClassification.useful}
]


act3_items: List[ItemDict] = [
    {'name': "Extra Battery",
     'count': 1,
     'classification': ItemClassification.useful},
    {'name': "Nano Armor Generator",
     'count': 1,
     'classification': ItemClassification.useful},
    {'name': "Mrs. Bomb's Remote",
     'count': 1,
     'classification': ItemClassification.useful},
    {'name': "Inspectometer Battery",
     'count': 1,
     'classification': ItemClassification.progression},
    {'name': "Gems Module",
     'count': 1,
     'classification': ItemClassification.progression},
    {'name': "Lonely Wizbot Card",
     'count': 1,
     'classification': ItemClassification.useful},
    {'name': "Fishbot Card",
     'count': 1,
     'classification': ItemClassification.useful},
    {'name': "Ourobot Card",
     'count': 1,
     'classification': ItemClassification.useful},
    {'name': "Holo Pelt",
     'count': 5,
     'classification': ItemClassification.progression},
    {'name': "Quill",
     'count': 1,
     'classification': ItemClassification.progression},
]

filler_items: List[ItemDict] = [
    {'name': "Currency",
     'count': 1,
     'classification': ItemClassification.filler},
    {'name': "Card Pack",
     'count': 1,
     'classification': ItemClassification.filler}
]
