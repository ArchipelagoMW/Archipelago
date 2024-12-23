import math
from enum import Enum
from typing import Dict, List, Optional, Union, Callable
from .Items import item_table, progression_items, item_name_groups
from .Options import piece_type_limit_options, piece_limit_options


class PieceLimitCascade(Enum):
    """Controls how child pieces are considered when checking piece limits."""
    NO_CHILDREN = 1  # Only consider the piece itself
    ACTUAL_CHILDREN = 2  # Consider the piece and its existing children
    POTENTIAL_CHILDREN = 3  # Consider the piece and all possible children


class PieceModel:
    """Handles piece relationships, limits, and cascading effects."""
    
    def __init__(self, world):
        self.world = world
        self.items_used: Dict[int, Dict[str, int]] = {}

    def get_parents(self, chosen_item: str) -> List[List[Union[str, int]]]:
        """Get the parent items required for this item."""
        return item_table[chosen_item].parents

    def get_children(self, chosen_item: str) -> List[str]:
        """Get the items that can be created from this item."""
        return [item for item in item_table
                if item_table[item].parents is not None and chosen_item in map(
                lambda x: x[0], item_table[item].parents)]

    def fewest_parents(self, parents: List[List[Union[str, int]]]) -> Optional[int]:
        """Get the minimum number of parent items available."""
        return min([self.items_used[self.world.player].get(item[0], 0) for item in parents])

    def has_prereqs(self, chosen_item: str) -> bool:
        """Check if the prerequisites for this item are met."""
        parents = self.get_parents(chosen_item)
        if parents:
            fewest_parents = self.fewest_parents(parents) * parents[0][1]
            if fewest_parents is None:
                return True
            enough_parents = fewest_parents > self.items_used[self.world.player].get(chosen_item, 0)
            if not enough_parents:
                return False
        return self.under_piece_limit(chosen_item, PieceLimitCascade.ACTUAL_CHILDREN)

    def can_add_more(self, chosen_item: str) -> bool:
        """Check if more of this item can be added to the pool."""
        if not self.under_piece_limit(chosen_item, PieceLimitCascade.POTENTIAL_CHILDREN):
            return False
        return chosen_item not in self.items_used[self.world.player] or \
            item_table[chosen_item].quantity == math.inf or \
            self.items_used[self.world.player][chosen_item] < item_table[chosen_item].quantity

    def under_piece_limit(self, chosen_item: str, with_children: PieceLimitCascade,
                         available_items: Optional[List[str]] = None) -> bool:
        """Check if adding this item would exceed piece limits."""
        if self.world.player not in self.items_used:
            return True
        piece_limit = self.find_piece_limit(chosen_item, with_children, available_items)
        pieces_used = self.items_used[self.world.player].get(chosen_item, 0)
        if 0 < piece_limit <= pieces_used:
            return False
        if chosen_item in piece_limit_options:
            piece_total_limit = piece_limit_options[chosen_item](self.world.options).value
            if 0 < piece_total_limit <= pieces_used:
                return False
        return True

    def find_piece_limit(self, chosen_item: str, with_children: PieceLimitCascade,
                        available_items: Optional[List[str]] = None) -> int:
        """Find the piece limit for this item type."""
        if chosen_item not in piece_type_limit_options:
            return 0

        piece_limit: int = self.piece_limit_of(chosen_item)
        army_piece_types = {
            piece: sum([self.world.piece_types_by_army[army][piece] 
                       for army in self.world.armies[self.world.player]])
            for piece in set().union(*self.world.piece_types_by_army.values())}
        limit_multiplier = get_limit_multiplier_for_item(army_piece_types)
        piece_limit = piece_limit * limit_multiplier(chosen_item)
        
        if piece_limit > 0 and with_children != PieceLimitCascade.NO_CHILDREN:
            children = self.get_children(chosen_item)
            if children:
                if with_children == PieceLimitCascade.ACTUAL_CHILDREN:
                    piece_limit = piece_limit + sum([
                        self.items_used[self.world.player].get(child, 0) for child in children])
                elif with_children == PieceLimitCascade.POTENTIAL_CHILDREN:
                    if available_items is not None:
                        children = [child for child in children if child in available_items]
                    piece_limit = piece_limit + sum([
                        self.find_piece_limit(child, with_children, available_items) for child in children])
        return piece_limit

    def piece_limit_of(self, chosen_item: str) -> int:
        """Get the base piece limit for this item type."""
        return piece_type_limit_options[chosen_item](self.world.options).value


def get_limit_multiplier_for_item(item_dictionary: Dict[str, int]) -> Callable[[str], int]:
    """Get a function that returns the limit multiplier for a given item."""
    return lambda item_name: item_dictionary[item_name] 