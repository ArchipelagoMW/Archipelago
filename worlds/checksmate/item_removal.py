from collections import Counter
from BaseClasses import Item
from .item_utils import (
    castling_requirement,
    chessmen_count,
    collection_item_maximum,
    occupied_pockets,
    pocket_item_limit,
)
from .items import (
    LEGACY_CHESSMEN_GROUP,
    ItemizationMode,
    item_name_groups,
    item_table,
    itemization_mode,
    progression_items,
)
from .locations import highest_chessmen_requirement_small, highest_chessmen_requirement
from .piece_limit_cascade import PieceLimitCascade


class ItemRemoval:
    """Handles the rules for when items should be removed from the pool during generation."""

    def __init__(self, world, piece_model) -> None:
        self.world = world
        self.piece_model = piece_model

    def should_remove_item(
        self,
        chosen_item: str,
        material: int,
        max_material: float,
        items: list[Item],
        progression_items_list: list[str],
        locked_items: dict[str, int],
    ) -> bool:
        """Determine if an item should be removed from the pool based on various rules."""
        if (
            chosen_item == "Progressive Major To Queen"
            and self._should_remove_queen_upgrade(items, locked_items)
        ):
            return True

        if self._exceeds_basic_limits(chosen_item, progression_items_list):
            return True

        total_material = (
            material
            + self._calculate_lockable_material(
                chosen_item,
                items,
                locked_items,
            )
            + self._calculate_remaining_material(locked_items)
        )
        if total_material > max_material:
            return True

        if (
            not self._is_minimal_accessibility()
            and self._violates_chessmen_requirements(
                chosen_item,
                max_material,
                total_material,
                items,
                locked_items,
            )
        ):
            return True

        return False

    def _exceeds_basic_limits(self, chosen_item: str, progression_items_list: list[str]) -> bool:
        """Check if the item exceeds basic quantity or piece type limits."""
        if chosen_item == "Progressive Pocket":
            pocket_limit = pocket_item_limit(self.world.options)
            if (
                pocket_limit
                and self.piece_model.accounting.used_count(chosen_item)
                >= pocket_limit
            ):
                return True

        if chosen_item in self.piece_model.accounting.used:
            if (
                self.piece_model.accounting.used[chosen_item]
                >= item_table[chosen_item].quantity
            ):
                return True

        if not self.piece_model.under_piece_limit(
            chosen_item,
            PieceLimitCascade.POTENTIAL_CHILDREN,
            progression_items_list,
        ):
            return True

        return False

    def _should_remove_queen_upgrade(self, items: list[Item], locked_items: dict[str, int]) -> bool:
        """Determine if a queen upgrade should be removed based on major piece availability."""
        total_majors = (
            len([item for item in items if item.name == "Progressive Major Piece"]) +
            locked_items.get("Progressive Major Piece", 0)
            + self._starting_count("Progressive Major Piece")
        )
        total_jacks = (
            len([item for item in items if item.name == "Progressive Jack"])
            + locked_items.get("Progressive Jack", 0)
            + self._starting_count("Progressive Jack")
        )
        total_queens = (
            len([item for item in items if item.name == "Progressive Major To Queen"]) +
            locked_items.get("Progressive Major To Queen", 0)
            + self._starting_count("Progressive Major To Queen")
        )

        if total_majors == 0:
            return True

        if total_queens >= total_majors:
            return True
        if (
            self.world.options.accessibility.value
            == self.world.options.accessibility.option_minimal
        ):
            return False
        remaining_castlers = total_majors + total_jacks - total_queens
        return remaining_castlers <= castling_requirement(self.world.options)

    def _starting_count(self, item_name: str) -> int:
        starting_inventory = getattr(
            getattr(self.world.options, "start_inventory", None),
            "value",
            {},
        )
        raw_count = starting_inventory.get(
            item_name,
            0,
        )
        return min(
            max(0, int(raw_count)),
            collection_item_maximum(self.world.options, item_name),
        )

    def _violates_chessmen_requirements(self, chosen_item: str, max_material: float, total_material: float,
                                       items: list[Item], locked_items: dict[str, int]) -> bool:
        """Check if adding this item would violate chessmen requirements."""
        chessmen_requirement = self._get_chessmen_requirement()
        necessary_chessmen = (
            chessmen_requirement
            - self._count_chessmen(items, locked_items)
        )

        if self._is_chessman(chosen_item):
            necessary_chessmen -= 1
        elif self._is_pocket_piece(chosen_item):
            if self._creates_new_pocket(chosen_item, items, locked_items):
                necessary_chessmen -= 1

        if necessary_chessmen > 0:
            minimum_possible_material = total_material + (
                item_table["Progressive Pawn"].material * necessary_chessmen)
            return minimum_possible_material > max_material

        return False

    def _is_minimal_accessibility(self) -> bool:
        """Check if we're in minimal accessibility mode."""
        return self.world.options.accessibility.value == self.world.options.accessibility.option_minimal

    def _get_chessmen_requirement(self) -> int:
        """Get the chessmen requirement based on game mode."""
        return (highest_chessmen_requirement_small 
                if self.world.options.goal.value == self.world.options.goal.option_single
                else highest_chessmen_requirement)

    def _count_chessmen(
        self,
        items: list[Item],
        locked_items: dict[str, int] | None = None,
    ) -> int:
        """Count the number of chessmen in the items list."""
        counts = Counter(item.name for item in items)
        if locked_items:
            counts.update(locked_items)
        return chessmen_count(
            counts,
            itemization_mode(self.world.options),
            self.world.options.pocket_limit_by_pocket.value,
        )

    def _is_chessman(self, item_name: str) -> bool:
        """Check if an item is a chessman."""
        return (
            item_name == "Chessmen"
            if self._is_fundamental()
            else item_name in item_name_groups[LEGACY_CHESSMEN_GROUP]
        )

    def _is_fundamental(self) -> bool:
        return (
            itemization_mode(self.world.options)
            is ItemizationMode.FUNDAMENTAL
        )

    def _is_pocket_piece(self, item_name: str) -> bool:
        """Check if an item is a pocket piece."""
        return item_name == "Progressive Pocket"

    def _creates_new_pocket(self, item_name: str, items: list[Item], locked_items: dict[str, int]) -> bool:
        """Check if adding this pocket piece would create a new pocket."""
        if not self._is_pocket_piece(item_name):
            return False
        pocket_limit = self.world.options.pocket_limit_by_pocket.value
        current = (
            locked_items.get("Progressive Pocket", 0)
            + sum(
                item.name == "Progressive Pocket"
                for item in items
            )
        )
        return occupied_pockets(
            current + 1,
            pocket_limit,
        ) > occupied_pockets(current, pocket_limit)

    def _calculate_lockable_material(self, chosen_item: str, items: list[Item], locked_items: dict[str, int]) -> int:
        """Calculate the material value if this item was added."""
        if chosen_item == "Progressive Pocket":
            return 0
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

    def _calculate_remaining_material(self, locked_items: dict[str, int]) -> int:
        """Calculate the material value of locked items."""
        return sum(locked_items[item] * progression_items[item].material 
                  for item in locked_items 
                  if item in progression_items
                  and progression_items[item].material > 0
                  and item != "Progressive Pocket")
