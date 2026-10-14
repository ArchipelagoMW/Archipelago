from typing import Dict, List, NamedTuple, Set, Tuple
from BaseClasses import Item, ItemClassification
from . import Data


class KH1Item(Item):
    game: str = "Kingdom Hearts"


class KH1ItemData(NamedTuple):
    groups: Tuple[str, ...]
    code: int
    classification: ItemClassification = ItemClassification.filler
    max_quantity: int = 1
    weight: int = 1


def get_items_by_group(group: str) -> Dict[str, KH1ItemData]:
    return {name: data for name, data in item_table.items() if group in data.groups}

def build_item_table(rows: List[Dict[str, str]]) -> Dict[str, KH1ItemData]:
    table: Dict[str, KH1ItemData] = {}
    for row in rows:
        if not int(row["active"]):
            continue
        table[row["name"]] = KH1ItemData(
            tuple(row["groups"].split(";")),
            code=int(row["id"]) if row["id"] else None,
            classification=ItemClassification[row["classification"]],
            max_quantity=int(row["max_quantity"]),
        )
    return table


def build_item_name_groups(table: Dict[str, KH1ItemData]) -> Dict[str, Set[str]]:
    groups: Dict[str, Set[str]] = {}
    for name, item in table.items():
        for group in item.groups:
            groups.setdefault(group, set()).add(name)
    return groups


item_table: Dict[str, KH1ItemData] = build_item_table(Data.items)
event_item_table: Dict[str, KH1ItemData] = build_item_table(Data.event_items)
item_name_groups: Dict[str, Set[str]] = build_item_name_groups(item_table)
