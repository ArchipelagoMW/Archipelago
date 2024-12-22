from typing import List, Tuple
from .Items import item_table


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