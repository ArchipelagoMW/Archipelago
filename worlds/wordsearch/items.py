from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from . import WordSearchWorld


class WordSearchItem(Item):
    game = "WordSearch"


class WordSearchItemData(NamedTuple):
    count: Callable[["WordSearchWorld"], int] = lambda world: 1
    code: Optional[int] = None
    name: Optional[str] = None
    type: ItemClassification = ItemClassification.filler
    can_create: Callable[["WordSearchWorld"], bool] = lambda world: True


item_data_table: Dict[str, WordSearchItemData] = {

    "Word": WordSearchItemData(code=100,type=ItemClassification.progression),
    "2 Words": WordSearchItemData(code=101,type=ItemClassification.progression),
    "3 Words": WordSearchItemData(code=102,type=ItemClassification.progression),
    "Word and Loop": WordSearchItemData(code=109,type=ItemClassification.progression),
    "Loop": WordSearchItemData(code=200,type=ItemClassification.progression),
    "2 Loops": WordSearchItemData(code=201,type=ItemClassification.progression),
    "3 Loops": WordSearchItemData(code=202,type=ItemClassification.progression),
    
    "Word Master": WordSearchItemData(code=1000,type=ItemClassification.progression, can_create = lambda world: False),
    
    "Filler": WordSearchItemData(code=150,type=ItemClassification.filler, can_create = lambda world: False),
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
