from zilliandomizer.logic_components.items import Item as ZzItem

from BaseClasses import Item
from BaseClasses import ItemClassification as IC


class ZillionItem(Item):
    game = "Zillion"
    __slots__ = ("zz_item",)
    zz_item: ZzItem

    def __init__(self, name: str, classification: IC, code: int, player: int, zz_item: ZzItem) -> None:
        super().__init__(name, classification, code, player)
        self.zz_item = zz_item
