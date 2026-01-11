from BaseClasses import ItemClassification
from .data.items import all_item_names, major_item_names, useful_item_names, nonbalanced_major_item_names


class ItemData:
    name: str
    classification: ItemClassification
    id: int

    def __init__(self, name: str, classification: ItemClassification, id: int):
        self.name = name
        self.classification = classification
        self.id = id

    def __repr__(self):
        return self.name

item_table: dict[str, ItemData] = dict()
item_table["Farlem"] = ItemData("Farlem", ItemClassification.progression, 1)

for index, item in enumerate(all_item_names, start=2):
    classification = ItemClassification.progression if item in major_item_names else ItemClassification.filler
    classification = ItemClassification.progression_skip_balancing if item in nonbalanced_major_item_names else classification
    classification = ItemClassification.useful if item in useful_item_names else classification
    item_table[item] = ItemData(item, classification, index + 1)


valid_item_names = [*all_item_names, "Zodiac Stones"]