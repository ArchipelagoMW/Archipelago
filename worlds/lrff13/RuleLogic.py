from typing import List
from .Items import item_data_table
from BaseClasses import CollectionState


def state_has_at_least(possible: List[bool], count: int) -> bool:
    # Returns true if at least count of the possible are true
    return possible.count(True) >= count

def item_is_category(item_name : str, category : str) -> bool:
    if item_name not in item_data_table:
        return False
    return item_data_table[item_name].category == category

def state_has_category(state : CollectionState, player : int, category: str, count: int = 1) -> bool:
    category_possible = [item_is_category(item, category) for item in state.prog_items[player]]
    return state_has_at_least(category_possible, count)