import string
import typing

from BaseClasses import Item
from typing import Dict

class ItemData(typing.NamedTuple):
    code: str
    progression: bool

item_table: Dict[str, ItemData] = {
    'Item 1': ItemData(1337000, True),
    'Item 2': ItemData(1337001, True),
    'Item 3': ItemData(1337002, True),
    'Item 4': ItemData(1337003, True),
    'Item 5': ItemData(1337004, True),
    'Item 6': ItemData(1337005, True),
    'Item 7': ItemData(1337006, True),
    'Item 8': ItemData(1337007, True),
    'Item 9': ItemData(1337008, True),
    'Item 10': ItemData(1337009, True),
    'Item 11': ItemData(1337010, True),
    'Item 12': ItemData(1337011, True),
    'Potion': ItemData(1337012, True),
    'Potion': ItemData(1337012, True),
    'Potion': ItemData(1337012, True),
    'Potion': ItemData(1337012, True),
}

melee_weapons = [
    'Item 4',
    'Item 5',
    'Item 6'
]

spells = [
    'Item 6',
    'Item 10',
    'Item 11'
]