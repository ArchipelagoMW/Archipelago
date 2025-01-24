from typing import Counter
from BaseClasses import Item, ItemClassification as IC
from zilliandomizer.logic_components.items import Item as ZzItem

_useful_thresholds = {
    "Apple": 9999,
    "Champ": 9999,
    "JJ": 9999,
    "Win": 9999,
    "Empty": 0,
    "ID Card": 10,
    "Red ID Card": 2,
    "Floppy Disk": 7,
    "Bread": 0,
    "Opa-Opa": 20,
    "Zillion": 8,
    "Scope": 8,
}
""" make the item useful if the number in the item pool is below this number """


def get_classification(name: str, zz_item: ZzItem, item_counts: Counter[str]) -> IC:
    classification = IC.filler
    if zz_item.required:
        classification = IC.progression
        if not zz_item.is_progression:
            classification = IC.progression_skip_balancing
    if item_counts[name] < _useful_thresholds.get(name, 0):
        classification |= IC.useful
    return classification


class ZillionItem(Item):
    game = "Zillion"
    __slots__ = ("zz_item",)
    zz_item: ZzItem

    def __init__(self, name: str, classification: IC, code: int, player: int, zz_item: ZzItem) -> None:
        super().__init__(name, classification, code, player)
        self.zz_item = zz_item
