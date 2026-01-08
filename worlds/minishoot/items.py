from typing import Dict, List, NamedTuple
from BaseClasses import ItemClassification
import csv

from .pool import MinishootPool, get_item_pool
from . import resources

class MinishootItemData(NamedTuple):
    """Data for a Minishoot item."""
    name: str
    classification: ItemClassification
    pool: MinishootPool
    quantity_in_item_pool: int

# Chosen completely arbitrarily. Is there a better way to do this?
item_base_id = 519346400

item_table: Dict[str, MinishootItemData]={}
item_name_to_id: Dict[str, int] = {}
filler_items: List[str] = []

classification_map = {
    'Trap': ItemClassification.trap,
    'Filler': ItemClassification.filler,
    'Helpful': ItemClassification.useful,
    'Progression': ItemClassification.progression,
    'Token': ItemClassification.progression_skip_balancing,
}

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files  # noqa

with files(resources).joinpath('items.csv').open() as file:
    reader = csv.reader(file)
    for line, row in enumerate(reader):
        if line == 0:
            continue
        item_data = MinishootItemData(
            name=row[0],
            classification=classification_map[row[1]],
            pool=get_item_pool(row[2]),
            quantity_in_item_pool=int(row[3])
        )
        item_table[item_data.name] = item_data
        item_name_to_id[item_data.name] = item_base_id + line
        if item_data.classification == ItemClassification.filler:
            filler_items.append(item_data.name)
