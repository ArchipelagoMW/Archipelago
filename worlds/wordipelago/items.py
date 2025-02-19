from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from . import WordipelagoWorld


class WordipelagoItem(Item):
    game = "Wordipelago"


class WordipelagoItemData(NamedTuple):
    count: Callable[["WordipelagoWorld"], int] = lambda world: 1
    code: Optional[int] = None
    name: Optional[str] = None
    type: ItemClassification = ItemClassification.filler
    can_create: Callable[["WordipelagoWorld"], bool] = lambda world: True


item_data_table: Dict[str, WordipelagoItemData] = {
    "The Letter A": WordipelagoItemData(code=1,type=ItemClassification.progression | ItemClassification.useful),
    "The Letter B": WordipelagoItemData(code=2,type=ItemClassification.progression),
    "The Letter C": WordipelagoItemData(code=3,type=ItemClassification.progression),
    "The Letter D": WordipelagoItemData(code=4,type=ItemClassification.progression),
    "The Letter E": WordipelagoItemData(code=5,type=ItemClassification.progression | ItemClassification.useful),
    "The Letter F": WordipelagoItemData(code=6,type=ItemClassification.progression),
    "The Letter G": WordipelagoItemData(code=7,type=ItemClassification.progression),
    "The Letter H": WordipelagoItemData(code=8,type=ItemClassification.progression),
    "The Letter I": WordipelagoItemData(code=9,type=ItemClassification.progression),
    "The Letter J": WordipelagoItemData(code=10,type=ItemClassification.progression),
    "The Letter K": WordipelagoItemData(code=11,type=ItemClassification.progression),
    "The Letter L": WordipelagoItemData(code=12,type=ItemClassification.progression | ItemClassification.useful),
    "The Letter M": WordipelagoItemData(code=13,type=ItemClassification.progression),
    "The Letter N": WordipelagoItemData(code=14,type=ItemClassification.progression),
    "The Letter O": WordipelagoItemData(code=15,type=ItemClassification.progression | ItemClassification.useful),
    "The Letter P": WordipelagoItemData(code=16,type=ItemClassification.progression | ItemClassification.useful),
    "The Letter Q": WordipelagoItemData(code=17,type=ItemClassification.progression),
    "The Letter R": WordipelagoItemData(code=18,type=ItemClassification.progression | ItemClassification.useful),
    "The Letter S": WordipelagoItemData(code=19,type=ItemClassification.progression | ItemClassification.useful),
    "The Letter T": WordipelagoItemData(code=20,type=ItemClassification.progression | ItemClassification.useful),
    "The Letter U": WordipelagoItemData(code=21,type=ItemClassification.progression),
    "The Letter V": WordipelagoItemData(code=22,type=ItemClassification.progression),
    "The Letter W": WordipelagoItemData(code=23,type=ItemClassification.progression),
    "The Letter X": WordipelagoItemData(code=24,type=ItemClassification.progression),
    "The Letter Y": WordipelagoItemData(code=25,type=ItemClassification.progression),
    "The Letter Z": WordipelagoItemData(code=26,type=ItemClassification.progression),

    "Guess": WordipelagoItemData(code=100,type=ItemClassification.progression | ItemClassification.useful, count = lambda world: 6 - world.options.starting_guesses ),
    "Time": WordipelagoItemData(code=200,type=ItemClassification.filler),
    
    "Yellow Letters": WordipelagoItemData(code=301,type=ItemClassification.progression | ItemClassification.useful, can_create = lambda world: not world.options.yellow_unlocked),
    "Unused Letters": WordipelagoItemData(code=302,type=ItemClassification.useful, can_create = lambda world: not world.options.unused_letters_unlocked),
    
    "Not Much": WordipelagoItemData(code=150,type=ItemClassification.filler, can_create = lambda world: False),
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
