from typing import List
from BaseClasses import Item
from .Items import item_name_groups
import math

class ChessmenModel:
    """Handles chessmen counting and requirements."""
    
    def __init__(self, world):
        self.world = world

    def count_chessmen(self, items: List[Item], pocket_limit: int) -> int:
        """Count the number of chessmen in the item pool."""
        pocket_amount = (0 if pocket_limit <= 0 else
                        math.ceil(len([item for item in items if item.name == "Progressive Pocket"]) / pocket_limit))
        chessmen_amount = len([item for item in items if item.name in item_name_groups["Chessmen"]])
        return chessmen_amount + pocket_amount

    def meets_chessmen_expectations(self, count: int, items: List[Item]) -> bool:
        """Check if the current chessmen count meets expectations."""
        current_count = self.count_chessmen(items, self.world.options.pocket_limit_by_pocket.value)
        return current_count >= count 