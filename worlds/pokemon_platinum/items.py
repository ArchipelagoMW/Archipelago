# items.py
#
# Copyright (C) 2025 James Petersen <m@jamespetersen.ca>
# Licensed under MIT. See LICENSE

from BaseClasses import Item, ItemClassification
from typing import Dict, Set

from .data import items as itemdata

class PokemonPlatinumItem(Item):
    game: str = "Pokemon Platinum"

raw_id_to_const_name = { item.get_raw_id():name for name, item in itemdata.items.items() }

def create_item_label_to_code_map() -> Dict[str, int]:
    return {v.label:v.get_raw_id() for v in itemdata.items.values()}

def get_item_groups() -> Dict[str, Set[str]]:
    return itemdata.item_groups

def get_item_classification(id: int) -> ItemClassification:
    return itemdata.items[raw_id_to_const_name[id]].classification
