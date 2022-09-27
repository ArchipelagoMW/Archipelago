from BaseClasses import Item, ItemClassification as IC
from zilliandomizer.logic_components.items import Item as ZzItem


class ZillionItem(Item):
    game = "Zillion"
    zz_item: ZzItem

    def __init__(self, name: str, classification: IC, code: int, player: int, zz_item: ZzItem) -> None:
        super().__init__(name, classification, code, player)
        self.zz_item = zz_item
