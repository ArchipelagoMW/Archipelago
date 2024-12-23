from typing import Dict, List

from .Rules import determine_max_material, determine_min_material
from .Locations import location_table
from .Items import progression_items, CMItem

class MaterialModel:
    """Handles material value calculations and requirements."""
    
    def __init__(self, world):
        self.world = world
        self.items_used: Dict[int, Dict[str, int]] = {}

    def calculate_current_material(self) -> int:
        """Calculate the total material value of currently used items."""
        return sum([
            progression_items[item].material * self.items_used[self.world.player][item]
            for item in self.items_used[self.world.player] if item in progression_items
        ])

    def calculate_remaining_material(self, locked_items: Dict[str, int]) -> int:
        """Calculate the material value of locked items that have material value."""
        return sum([
            locked_items[item] * progression_items[item].material 
            for item in locked_items 
            if item in progression_items and progression_items[item].material > 0
        ])

    def calculate_material_requirements(self, super_sized: bool) -> tuple[float, float]:
        """Calculate the minimum and maximum material requirements based on world options."""
        min_material = determine_min_material(self.world.options)
        max_material = determine_max_material(self.world.options)
        
        if super_sized:
            endgame_multiplier = (location_table["Checkmate Maxima"].material_expectations_grand /
                                location_table["Checkmate Minima"].material_expectations_grand)
            min_material *= endgame_multiplier
            max_material *= endgame_multiplier
            
        # We already handle 50 material due to Play as White being forced into the item pool
        min_material -= 50
        max_material -= 50
        return min_material, max_material

    def unupgraded_majors_in_pool(self, items: List[CMItem], locked_items: Dict[str, int]) -> int:
        """Returns the number of unupgraded major pieces in the pool."""
        # Count majors in items list
        majors_in_items = len([item for item in items if item.name == "Progressive Major Piece"])
        # Count majors in locked items (using the count value)
        majors_in_locked = locked_items.get("Progressive Major Piece", 0)
        total_majors = majors_in_items + majors_in_locked

        # Count upgrades in items list
        upgrades_in_items = len([item for item in items if item.name == "Progressive Major To Queen"])
        # Count upgrades in locked items (using the count value)
        upgrades_in_locked = locked_items.get("Progressive Major To Queen", 0)
        total_upgrades = upgrades_in_items + upgrades_in_locked

        return total_majors - total_upgrades

    def lockable_material_value(self, chosen_item: str, items: List[CMItem], 
                              locked_items: Dict[str, int]) -> float:
        """Calculate the total material value if this item was added, including cascading effects."""
        material = progression_items[chosen_item].material
        if self.world.options.accessibility.value == self.world.options.accessibility.option_minimal:
            return material
            
        if (chosen_item == "Progressive Major To Queen" and 
                self.unupgraded_majors_in_pool(items, locked_items) <= 2):
            material += progression_items["Progressive Major Piece"].material
            
        return material 