import json
import pkgutil
from typing import Dict, Set, NamedTuple, List

from BaseClasses import Item, ItemClassification


class ItemData(NamedTuple):
    name: str
    code: int
    item_type: str
    classification: ItemClassification

FF1_BRIDGE = 'Bridge'


FF1_STARTER_ITEMS = [
    "Ship"
]

FF1_PROGRESSION_LIST = [
    "Rod", "Cube", "Lute", "Key", "Chime", "Oxyale",
    "Ship", "Canoe", "Floater", "Mark", "Sigil", "Canal",
    "Crown", "Crystal", "Herb", "Tnt", "Adamant", "Slab", "Ruby", "Bottle",
    "Shard",
    "EarthOrb", "FireOrb", "WaterOrb", "AirOrb"
]

FF1_USEFUL_LIST = [
    "Tail", "Masamune", "Xcalber", "Katana", "Vorpal",
    "DragonArmor", "Opal", "AegisShield",  "Ribbon"
]


class FF1Items:
    _item_table: List[ItemData] = []
    _item_table_lookup: Dict[str, ItemData] = {}

    def _populate_item_table_from_data(self):
        file = pkgutil.get_data(__name__, "data/items.json").decode("utf-8")
        items = json.loads(file)
        # Hardcode progression and categories for now
        self._item_table = [ItemData(name, code, "FF1Item", ItemClassification.progression if name in
                            FF1_PROGRESSION_LIST else ItemClassification.useful if name in FF1_USEFUL_LIST else
                            ItemClassification.filler) for name, code in items.items()]
        self._item_table_lookup = {item.name: item for item in self._item_table}

    def _get_item_table(self) -> List[ItemData]:
        if not self._item_table or not self._item_table_lookup:
            self._populate_item_table_from_data()
        return self._item_table

    def _get_item_table_lookup(self) -> Dict[str, ItemData]:
        if not self._item_table or not self._item_table_lookup:
            self._populate_item_table_from_data()
        return self._item_table_lookup

    def get_item_names_per_category(self) -> Dict[str, Set[str]]:
        categories: Dict[str, Set[str]] = {}

        for item in self._get_item_table():
            categories.setdefault(item.item_type, set()).add(item.name)

        return categories

    def generate_item(self, name: str, player: int) -> Item:
        item = self._get_item_table_lookup().get(name)
        return Item(name, item.classification,
                    item.code, player)

    def get_item_name_to_code_dict(self) -> Dict[str, int]:
        return {name: item.code for name, item in self._get_item_table_lookup().items()}

    def get_item(self, name: str) -> ItemData:
        return self._get_item_table_lookup()[name]
