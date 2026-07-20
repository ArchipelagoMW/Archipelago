from collections import Counter

from .rules import determine_max_material, determine_min_material
from .items import progression_items, CMItem
from .pool_state import PoolAccounting


class MaterialModel:
    """Handles material value calculations and requirements."""

    def __init__(self, world, accounting: PoolAccounting | None = None):
        self.world = world
        world_accounting = getattr(world, "pool_accounting", None)
        if accounting is None:
            accounting = world_accounting
        self.accounting = (
            accounting if accounting is not None else PoolAccounting()
        )

    def calculate_current_material(self) -> int:
        """Calculate the total material value of currently used items."""
        return sum(
            progression_items[item].material * count
            for item, count in self.accounting.used.items()
            if item in progression_items
        )

    def calculate_items_material(self, items: list[CMItem]) -> int:
        """Calculate material represented by an explicit generated item list."""
        item_counts = Counter(item.name for item in items)
        return sum(
            min(
                progression_items[item_name].material * count,
                progression_items[item_name].material
                * progression_items[item_name].quantity,
            )
            for item_name, count in item_counts.items()
            if item_name in progression_items
            and item_name != "Progressive Pocket"
        )

    def calculate_remaining_material(self, locked_items: dict[str, int]) -> int:
        """Calculate the material value of locked items that have material value."""
        return sum(
            locked_items[item] * progression_items[item].material
            for item in locked_items
            if item in progression_items and progression_items[item].material > 0
        )

    def calculate_material_requirements(self) -> tuple[float, float]:
        """Calculate the minimum and maximum material requirements based on world options."""
        min_material = determine_min_material(self.world.options)
        max_material = determine_max_material(self.world.options)

        # We already handle 50 material due to Play as White being forced into the item pool
        min_material -= 50
        max_material -= 50
        return min_material, max_material

    def castling_pieces_in_pool(self, items: list[CMItem], locked_items: dict[str, int]) -> int:
        """Returns the number of castling pieces in the pool."""
        # Count majors in items list
        jacks_in_items = len([item for item in items if item.name == "Progressive Jack"])
        # Count majors in locked items (using the count value)
        jacks_in_locked = locked_items.get("Progressive Jack", 0)
        total_jacks = jacks_in_items + jacks_in_locked

        return self.unupgraded_majors_in_pool(items, locked_items) + total_jacks

    def unupgraded_majors_in_pool(self, items: list[CMItem], locked_items: dict[str, int]) -> int:
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

        return max(0, total_majors - total_upgrades)
