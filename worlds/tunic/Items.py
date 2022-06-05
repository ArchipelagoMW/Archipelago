import json
from pathlib import Path
from typing import Dict, Set, NamedTuple, List

from BaseClasses import Item


class ItemData(NamedTuple):
    name: str
    code: int
    item_type: str
    progression: bool

TUNIC_PROGRESSION_ITEMS = [
    ""
]

TUNIC_ITEM_CATEGORIES_WITHOUT_INGAME_NAME = [
    ItemData("Money", 1, "MONEY", False),
    ItemData("Empty Chest", 2, "OTHER", False)
]


class TunicItems:
    _item_table: List[ItemData] = []
    _item_table_lookup: Dict[str, ItemData] = {}
    _item_table_quantity: Dict[str, int] = {}

    def _populate_item_table_from_data(self):
        base_path = Path(__file__).parent
        file_path = (base_path / "data/ItemLocations.json").resolve()
        with open(file_path) as file:
            exported_items = json.load(file)
            self._item_table = [ItemData(item_type, code, item_type, progression)
                                for name, code, item_type, progression
                                in TUNIC_ITEM_CATEGORIES_WITHOUT_INGAME_NAME]
            self._item_table_lookup = {item.item_type: item for item in self._item_table}
            self._item_table_quantity = {item.item_type: 0 for item in self._item_table}

            starting_item_numbering = len(TUNIC_ITEM_CATEGORIES_WITHOUT_INGAME_NAME) + 1
            for tunic_item in exported_items:
                if "itemName" in tunic_item and tunic_item["itemName"] not in self._item_table_lookup.keys():
                    new_item = ItemData(tunic_item["itemName"], starting_item_numbering, tunic_item["itemType"],
                                        tunic_item["itemName"] in TUNIC_PROGRESSION_ITEMS)
                    self._item_table.append(new_item)
                    self._item_table_lookup[tunic_item["itemName"]] = new_item

                if "itemName" in tunic_item:
                    if tunic_item["itemName"] in self._item_table_quantity:
                        self._item_table_quantity[tunic_item["itemName"]] += 1
                    else:
                        self._item_table_quantity[tunic_item["itemName"]] = 1
                elif "itemType" in tunic_item:
                    if tunic_item["itemType"] in self._item_table_quantity:
                        self._item_table_quantity[tunic_item["itemType"]] += 1
                    else:
                        self._item_table_quantity[tunic_item["itemType"]] = 1

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
        return TunicItemWrapper(name, item.progression, item.code, player)

    def get_item_name_to_code_dict(self) -> Dict[str, int]:
        return {name: item.code for name, item in self._get_item_table_lookup().items()}

    def get_item(self, name: str) -> ItemData:
        return self._get_item_table_lookup()[name]

    def get_all_item_names(self) -> [str]:
        if not self._item_table or not self._item_table_lookup:
            self._populate_item_table_from_data()
        return [value.name for value in self._item_table]

    def get_item_quantity(self, name) -> int:
        if not self._item_table or not self._item_table_lookup:
            self._populate_item_table_from_data()
        return self._item_table_quantity[name] if name in self._item_table_quantity else 0


class TunicItemWrapper(Item):
    game: str = "Tunic"
