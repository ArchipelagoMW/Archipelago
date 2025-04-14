from typing import Dict, Set, Tuple, NamedTuple

class ItemData(NamedTuple):
    category: str
    code: int
    count: int = 1
    progression: bool = False
    useful: bool = False
    trap: bool = False

# A lot of items arent normally dropped by the randomizer as they are mostly enemy drops, but they can be enabled if desired
item_table: Dict[str, ItemData] = {
    'Owl Drum': ItemData('Equipment', 0, progression=True)
}

starter_melee_weapons: Tuple[str, ...] = (
)

starter_spells: Tuple[str, ...] = (
)

# weighted
starter_progression_items: Tuple[str, ...] = (
)

pyramid_start_starter_progression_items: Tuple[str, ...] = (
)

filler_items: Tuple[str, ...] = (
)

def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        categories.setdefault(data.category, set()).add(name)

    return categories
