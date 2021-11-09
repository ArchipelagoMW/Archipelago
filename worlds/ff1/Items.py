import json
from typing import Dict, Set, NamedTuple, List

from BaseClasses import Item


class ItemData(NamedTuple):
    name: str
    code: int
    item_type: str
    progression: bool


class FF1Items:
    _item_table: List[ItemData] = []
    _item_table_lookup: Dict[str, ItemData] = {}

    def _populate_item_table_from_data(self):
        with open('worlds/ff1/data/items.json') as file:
            items = json.load(file)
            # Hardcode progression and categories for now
            self._item_table = [ItemData(name, code, "FF1Item", True) for name, code in items.items()]
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
        return Item(name, item.progression, item.code, player)

    def get_item_name_to_code_dict(self) -> Dict[str, int]:
        return {name: item.code for name, item in self._get_item_table_lookup().items()}

    def get_item(self, name: str) -> ItemData:
        return self._get_item_table_lookup()[name]
