from typing import List, Tuple
from .Items import item_table
from BaseClasses import Item


def get_parents(item_name: str) -> List[Tuple[str, int]]:
    """Get the parent items and their required quantities for an item.
    
    Args:
        item_name: The name of the item to get parents for
        
    Returns:
        List of tuples containing (parent_name, required_quantity)
    """
    return item_table[item_name].parents


def get_children(item_name: str) -> List[str]:
    """Get the child items for an item.
    
    Args:
        item_name: The name of the item to get children for
        
    Returns:
        List of child item names
    """
    return [child for child in item_table if item_name in [parent[0] for parent in item_table[child].parents]] 

def chessmen_count(items: List[Item], pocket_limit_by_pocket: int) -> int:
    """Count the number of chessmen in the item list, including pocket pieces."""
    chessmen = len([item for item in items if "Progressive" in item.name and "Pocket" not in item.name])
    if pocket_limit_by_pocket > 0:
        pocket_count = len([item for item in items if item.name == "Progressive Pocket"])
        chessmen += pocket_count // pocket_limit_by_pocket
    return chessmen
