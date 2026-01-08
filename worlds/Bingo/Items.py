from typing import NamedTuple, Optional
from BaseClasses import Item, ItemClassification


class BingoItem(Item):
    game = "APBingo"


class BingoItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler


item_data_table = {
    f"{chr(row)}{col}": BingoItemData(code=code, type=ItemClassification.progression)
    for code, (row, col) in enumerate(((ord('A') + r, c) for r in range(10) for c in range(1, 11)), start=1)
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
