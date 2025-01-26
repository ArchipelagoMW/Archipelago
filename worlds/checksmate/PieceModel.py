import math
from typing import Dict, List, Optional, Union
from .Items import item_table
from .Options import piece_type_limit_options, piece_limit_options
from .PieceLimitCascade import PieceLimitCascade


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
        # First check if we're under piece limits
        if not self.under_piece_limit(chosen_item, PieceLimitCascade.POTENTIAL_CHILDREN):
            return False
            
        # Then check if we're under quantity limits
        if chosen_item not in self.items_used[self.world.player]:
            return True
            
        max_count = item_table[chosen_item].quantity
        if max_count == math.inf:
            return True

        current_count = self.items_used[self.world.player][chosen_item]
        return current_count < max_count

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

        # Get base limit from options
        base_limit: int = self.piece_limit_of(chosen_item)
        
        # Get army-specific multiplier
        army_piece_types = {
            piece: sum([self.world.piece_types_by_army[army][piece] 
                       for army in self.world.armies[self.world.player]])
            for piece in set().union(*self.world.piece_types_by_army.values())}
        
        # Calculate total limit including army multiplier
        total_limit = base_limit * army_piece_types[chosen_item]
        
        # For NO_CHILDREN, return just the base limit
        if with_children == PieceLimitCascade.NO_CHILDREN:
            return total_limit
            
        # For other cascade types, consider children
        children = self.get_children(chosen_item)
        if not children:
            return total_limit
            
        if with_children == PieceLimitCascade.ACTUAL_CHILDREN:
            # Add the count of existing child items
            child_count = sum(self.items_used[self.world.player].get(child, 0) for child in children)
            return total_limit + child_count
        else:  # POTENTIAL_CHILDREN
            # Filter available children if needed
            if available_items is not None:
                children = [child for child in children if child in available_items]
            # Add the potential limits of child items
            child_limits = sum(self.find_piece_limit(child, PieceLimitCascade.NO_CHILDREN, available_items) 
                             for child in children)
            return total_limit + child_limits

    def piece_limit_of(self, chosen_item: str) -> int:
        """Get the base piece limit for this item type."""
        return piece_type_limit_options[chosen_item](self.world.options).value
