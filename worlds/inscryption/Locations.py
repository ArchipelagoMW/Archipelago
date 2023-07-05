from typing import List, TypedDict
from BaseClasses import Location


base_id = 147000


class InscryptionLocation(Location):
    game: str = "Inscryption"


class LocDict(TypedDict):
    name: str
    region: str


location_table: List[LocDict] = [
    {'name': "Boss Prospector",
     'region': "Act 1"},
    {'name': "Boss Angler",
     'region': "Act 1"},
    {'name': "Boss Trapper",
     'region': "Act 1"},
    {'name': "Boss Leshy",
     'region': "Act 1"},
    {'name': "Safe",
     'region': "Act 1"},
    {'name': "Cabin Clock Upper Compartment",
     'region': "Act 1"},
    {'name': "Cabin Clock Main Compartment",
     'region': "Act 1"},
    {'name': "Dagger",
     'region': "Act 1"},
    {'name': "Wardrobe Drawer 1",
     'region': "Act 1"},
    {'name': "Wardrobe Drawer 2",
     'region': "Act 1"},
    {'name': "Wardrobe Drawer 3",
     'region': "Act 1"},
    {'name': "Wardrobe Drawer 4",
     'region': "Act 1"},
    {'name': "Magnificus Eye",
     'region': "Act 1"},
    {'name': "Painting 1",
     'region': "Act 1"},
    {'name': "Painting 2",
     'region': "Act 1"},
    {'name': "Painting 3",
     'region': "Act 1"},
    {'name': "Greater Smoke",
     'region': "Act 1"},
]
