from typing import Dict, List, Union, Tuple
from BaseClasses import CollectionState, Item
from .Items import item_table, progression_items
from .ItemUtils import get_parents, get_children
import logging


class CMCollectionState:
    """Handles the state management for ChecksMate while items are being placed in locations, including
    collecting and removing items, and tracking material values. This work is after items are created.
    
    Pretty much the entire reason this exists is to handle the items:
    - Progressive Major Piece
    - Progressive Major To Queen

    Major To Queen is a "child" of the Major Piece, which means it only has a game effect if a Major Piece
    is collected and can be upgraded. This means they need to pair off, and if we can't find a pair, the upgrade
    is not applied. However, a Major Piece is always counted.
    
    This means when we add a Major Piece, we need to check if there is a Major To Queen that can be upgraded, and count it too.
    Also, when we remove a Major Piece, we need to check if there is a Major To Queen that can be downgraded, and count it too.
    Finally, when we add or remove a Major To Queen, we need to check if there is a Major Piece, otherwise the new upgrade
    should have a material value of 0 - until we add that Major Piece, which will be worth more.
    """
    
    def __init__(self, world):
        self.world = world

    def collect(self, state: CollectionState, item: Item) -> int:
        """Calculate the material value gained from collecting this item."""
        item_count = state.prog_items[self.world.player][item.name]
        
        # Check upgrades from existing children
        child_material = self._check_children(state, item, item_count)
        
        # Check if this is an upgrade for existing parents
        parent_material = self._check_self_and_parents(state, item, item_count)
        
        total_material = child_material + parent_material
        logging.debug(f"Adding {item.name} with material value {total_material}")
        return total_material

    def remove(self, state: CollectionState, item: Item) -> int:
        """Calculate the material value lost from removing this item."""
        item_count = state.prog_items[self.world.player].get(item.name, 0)
        if item_count <= 0:
            return 0
        item_count -= 1

        # Check downgrades from existing children
        child_material = self._check_children(state, item, item_count)
        
        # Only remove base material if not being immediately downgraded
        parent_material = self._check_self_and_parents(state, item, item_count)
        
        total_material = child_material + parent_material
        logging.debug(f"Removing {item.name} with material value {total_material}")
        return total_material

    def _check_children(self, state: CollectionState, item: Item, item_count: int) -> Tuple[int, bool]:
        """Check child upgrades and calculate material value."""
        material = 0
        children = get_children(item.name)
        
        for child in children:
            if item_table[child].material == 0:
                continue
            if item_count < state.prog_items[self.world.player].get(child, 0):
                material += item_table[child].material
                logging.debug(f"Applying child {child} having count: {state.prog_items[self.world.player].get(child, 0)}")
            else:
                logging.debug(f"{item.name} had insufficient chilren {child} to modify it")
                
        return material

    def _check_self_and_parents(self, state: CollectionState, item: Item, item_count: int) -> int:
        """Check parent relationships and calculate material value."""
        material = 0
        parents = get_parents(item.name)
        
        if len(parents) == 0 or item_table[item.name].material == 0:
            # Root element or zero material - add/remove base value
            material = item_table[item.name].material
        else:
            # Check if we can apply upgrade to a parent
            fewest_parents = min([state.prog_items[self.world.player].get(parent[0], 0) for parent in parents])
            # TODO: when a parent could have multiple children, check that this is also the least child
            if item_count < fewest_parents * parents[0][1]:
                material = item_table[item.name].material
                logging.debug(f"{item.name} had sufficient parents {fewest_parents} to be affected")
            else:
                logging.debug(f"{item.name} had insufficient parents {fewest_parents}")
                
        return material
