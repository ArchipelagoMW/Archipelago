from typing import Dict, List
from BaseClasses import Item
from .Items import item_table, progression_items, item_name_groups
from .Locations import highest_chessmen_requirement_small, highest_chessmen_requirement


class ItemRemoval:
    """Handles the rules for when items should be removed from the pool during generation."""

    def __init__(self, world, piece_model):
        self.world = world
        self.piece_model = piece_model

    def should_remove_item(self, chosen_item: str, material: int, min_material: float,
                          max_material: float, items: List[Item], progression_items_list: List[str],
                          locked_items: Dict[str, int], user_location_count: int) -> bool:
        """Determine if an item should be removed from the pool based on various rules."""
        # Check queen upgrade rules
        if chosen_item == "Progressive Major To Queen":
            if self._should_remove_queen_upgrade(items, locked_items):
                return True

        # Check piece type and quantity limits first
        if self._exceeds_basic_limits(chosen_item, progression_items_list):
            return True
        
        # Check material limits
        total_material = (material + 
                        self._calculate_lockable_material(chosen_item, items, locked_items) +
                        self._calculate_remaining_material(locked_items))
        if total_material > max_material:
            return True

        # Check chessmen requirements for full accessibility
        if not self._is_minimal_accessibility():
            if self._violates_chessmen_requirements(chosen_item, max_material, total_material, items, locked_items):
                return True

        # Check material requirements when few locations remain under a large material deficit
        if self._violates_material_requirements(
                chosen_item, min_material, total_material, items, locked_items, user_location_count):
            return True

        return False

    def _exceeds_basic_limits(self, chosen_item: str, progression_items_list: List[str]) -> bool:
        """Check if the item exceeds basic quantity or piece type limits."""
        # Check quantity limits
        if chosen_item in self.piece_model.items_used[self.world.player]:
            if self.piece_model.items_used[self.world.player][chosen_item] >= item_table[chosen_item].quantity:
                return True

        # Check piece type limits
        if not self.piece_model.under_piece_limit(chosen_item, "POTENTIAL_CHILDREN", progression_items_list):
            return True

        return False

    def _should_remove_queen_upgrade(self, items: List[Item], locked_items: Dict[str, int]) -> bool:
        """Determine if a queen upgrade should be removed based on major piece availability."""
        total_majors = (
            len([item for item in items if item.name == "Progressive Major Piece"]) +
            locked_items.get("Progressive Major Piece", 0)
        )
        total_queens = (
            len([item for item in items if item.name == "Progressive Major To Queen"]) +
            locked_items.get("Progressive Major To Queen", 0)
        )

        # No majors means no queens
        if total_majors == 0:
            return True

        # In minimal accessibility, each queen needs a major
        if self._is_minimal_accessibility():
            return total_queens >= total_majors

        # In full accessibility, need 2 unupgraded majors for castling
        return total_queens + 2 >= total_majors

    def _violates_chessmen_requirements(self, chosen_item: str, max_material: float, total_material: float,
                                       items: List[Item], locked_items: Dict[str, int]) -> bool:
        """Check if adding this item would violate chessmen requirements."""
        chessmen_requirement = self._get_chessmen_requirement()
        necessary_chessmen = chessmen_requirement - self._count_chessmen(items)

        # Adjust for the chosen item
        if self._is_chessman(chosen_item):
            necessary_chessmen -= 1
        elif self._is_pocket_piece(chosen_item):
            if self._creates_new_pocket(chosen_item, items, locked_items):
                necessary_chessmen -= 1

        # If we need more chessmen, check if we can afford them
        if necessary_chessmen > 0:
            minimum_possible_material = total_material + (
                item_table["Progressive Pawn"].material * necessary_chessmen)
            return minimum_possible_material > max_material

        return False

    def _violates_material_requirements(self, chosen_item: str, min_material: float, total_material: float,
                                        items: List[Item], locked_items: Dict[str, int],
                                        user_location_count: int) -> bool:
        """Check if adding this item would violate material requirements."""
        # TODO(chesslogic): In games with many pawns, check that we have enough locations for high-value items
        # Imagine the player added 40 pawns for 80 locations, but needed 100 material. If we added another 40 pawns,
        # we could never reach the goal. So, we need to check if we have enough locations that we can add some sort of
        # high-value item, while respecting piece limits. For example, if the player has 1 army with 1 major piece and
        # major piece limit of 1, and perhaps a queen limit of 1, we would have to add only bishops to reach the
        # min_material. That would mean among those 40 locations we need to add 10 bishops and 30 pawns, which also
        # results in having no Useful or Filler items. For the benefit of the player, I would prefer to reserve another
        # 5 locations (or fewer, if the player sets an AI reduction limit) for Useful items. Also, keep in mind
        # that a few of the locations are locked with progression items like Victory and Super-Size Me, but that might
        # be accounted for by the items list.
        return False

    def _is_minimal_accessibility(self) -> bool:
        """Check if we're in minimal accessibility mode."""
        return self.world.options.accessibility.value == self.world.options.accessibility.option_minimal

    def _get_chessmen_requirement(self) -> int:
        """Get the chessmen requirement based on game mode."""
        return (highest_chessmen_requirement_small 
                if self.world.options.goal.value == self.world.options.goal.option_single
                else highest_chessmen_requirement)

    def _count_chessmen(self, items: List[Item]) -> int:
        """Count the number of chessmen in the items list."""
        pocket_limit = self.world.options.pocket_limit_by_pocket.value
        pocket_amount = (0 if pocket_limit <= 0 else
                        len([item for item in items if item.name == "Progressive Pocket"]) // pocket_limit)
        chessmen_amount = len([item for item in items if item.name in item_name_groups["Chessmen"]])
        return chessmen_amount + pocket_amount

    def _is_chessman(self, item_name: str) -> bool:
        """Check if an item is a chessman."""
        return item_name in item_name_groups["Chessmen"]

    def _is_pocket_piece(self, item_name: str) -> bool:
        """Check if an item is a pocket piece."""
        return item_name == "Progressive Pocket"

    def _creates_new_pocket(self, item_name: str, items: List[Item], locked_items: Dict[str, int]) -> bool:
        """Check if adding this pocket piece would create a new pocket."""
        if not self._is_pocket_piece(item_name):
            return False
        pocket_limit = self.world.options.pocket_limit_by_pocket.value
        next_pocket = (locked_items.get("Progressive Pocket", 0) +
                      len([item for item in items if item.name == "Progressive Pocket"]) + 1)
        return next_pocket % pocket_limit == 1

    def _calculate_lockable_material(self, chosen_item: str, items: List[Item], locked_items: Dict[str, int]) -> int:
        """Calculate the material value if this item was added."""
        material = progression_items[chosen_item].material
        if self._is_minimal_accessibility():
            return material

        if chosen_item == "Progressive Major To Queen":
            total_majors = (len([item for item in items if item.name == "Progressive Major Piece"]) +
                          locked_items.get("Progressive Major Piece", 0))
            total_queens = (len([item for item in items if item.name == "Progressive Major To Queen"]) +
                          locked_items.get("Progressive Major To Queen", 0))
            if total_majors - total_queens <= 2:
                material += progression_items["Progressive Major Piece"].material

        return material

    def _calculate_remaining_material(self, locked_items: Dict[str, int]) -> int:
        """Calculate the material value of locked items."""
        return sum(locked_items[item] * progression_items[item].material 
                  for item in locked_items 
                  if item in progression_items and progression_items[item].material > 0)
