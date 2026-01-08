from typing import Dict

from BaseClasses import Item, ItemClassification as IClass
from .data.strings import SPZ

delivery_unlocks: Dict[str, IClass] = {
    SPZ.item_shape_0: IClass.progression,
    SPZ.item_shape_1: IClass.progression,
    SPZ.item_shape_2: IClass.progression,
    SPZ.item_shape_3: IClass.progression,
}

filler_items: Dict[str, IClass] = {
    SPZ.item_filler: IClass.filler,
}

item_table: Dict[str, IClass] = {
    **delivery_unlocks,
    **filler_items,
}


class Shapez2Item(Item):
    game = SPZ.game_name
