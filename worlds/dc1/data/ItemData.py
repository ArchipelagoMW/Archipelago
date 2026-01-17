from BaseClasses import ItemClassification
from worlds.dc1 import DarkCloudItem


class ItemData:
    classification = ItemClassification.trap
    name = None
    ap_id = 0
    count = 0

    def __init__(self, name: str, ap_id: int, classification: int, count: int):
        self.name = name
        self.ap_id = ap_id
        self.count = count
        if classification == 0:
            self.classification = ItemClassification.filler
        elif classification == 1:
            self.classification = ItemClassification.useful
        elif classification == 2:
            self.classification = ItemClassification.progression

    def to_items(self, player: int) -> list[DarkCloudItem]:
        items = []

        for i in range(self.count):
            items.append(DarkCloudItem(self.name, self.classification, self.ap_id, player))

        return items