from typing import Dict, List, Optional
from BaseClasses import Item
from .Items import (CMItem, item_table, filler_items, progression_items,
                   useful_items, item_name_groups)
from .Rules import determine_min_material, determine_max_material
from .Locations import location_table, Tactic
import logging


class CMItemPool:
    """Handles the creation and management of the item pool for ChecksMate."""

    def __init__(self, world):
        self.world = world
        self.items_used: Dict[int, Dict[str, int]] = {}
        self.items_remaining: Dict[int, Dict[str, int]] = {}

    def initialize_item_tracking(self) -> None:
        """Initialize the item tracking dictionaries."""
        self.items_used[self.world.player] = {}
        self.items_remaining[self.world.player] = {}

    def handle_excluded_items(self, excluded_items: Dict[str, int]) -> List[Item]:
        """Process excluded items and return starter items."""
        starter_items = []
        for item_name in excluded_items:
            if item_name not in self.items_used[self.world.player]:
                self.items_used[self.world.player][item_name] = 0
            self.items_used[self.world.player][item_name] += excluded_items[item_name]
            starter_items.extend([self.world.create_item(item_name) for _ in range(excluded_items[item_name])])
        return starter_items

    def calculate_material_requirements(self, super_sized: bool) -> tuple[int, int]:
        """Calculate minimum and maximum material requirements."""
        min_material = determine_min_material(self.world.options)
        max_material = determine_max_material(self.world.options)
        if super_sized:
            endgame_multiplier = (location_table["Checkmate Maxima"].material_expectations_grand /
                                location_table["Checkmate Minima"].material_expectations_grand)
            min_material *= endgame_multiplier
            max_material *= endgame_multiplier
        return min_material, max_material

    def handle_option_limits(self) -> None:
        """Apply limits based on world options."""
        self.items_used[self.world.player]["Progressive Consul"] = (
            self.items_used[self.world.player].get("Progressive Consul", 0) +
            (3 - self.world.options.max_kings.value))
        self.items_used[self.world.player]["Progressive King Promotion"] = (
            self.items_used[self.world.player].get("Progressive King Promotion", 0) +
            (2 - self.world.options.fairy_kings.value))
        self.items_used[self.world.player]["Progressive Engine ELO Lobotomy"] = (
            self.items_used[self.world.player].get("Progressive Engine ELO Lobotomy", 0) +
            (5 - self.world.options.max_engine_penalties.value))
        self.items_used[self.world.player]["Progressive Pocket"] = (
            self.items_used[self.world.player].get("Progressive Pocket", 0) +
            (12 - min(self.world.options.max_pocket.value, 3 * self.world.options.pocket_limit_by_pocket.value)))
        self.items_used[self.world.player]["Super-Size Me"] = 1

    def get_max_items(self, super_sized: bool) -> int:
        """Calculate the maximum number of items based on world options."""
        max_items = len(location_table)
        if not super_sized:
            max_items -= len([loc for loc in location_table if location_table[loc].material_expectations == -1])
        if self.world.options.enable_tactics.value == self.world.options.enable_tactics.option_none:
            max_items -= len([loc for loc in location_table if location_table[loc].is_tactic is not None])
        elif self.world.options.enable_tactics.value == self.world.options.enable_tactics.option_turns:
            max_items -= len([loc for loc in location_table if location_table[loc].is_tactic == Tactic.Fork])
        return max_items

    def create_progression_items(self, min_material: int, max_material: int) -> List[Item]:
        """Create progression items up to material limits."""
        items = []
        material = 0
        my_progression_items = self.prepare_progression_item_pool()
        
        while len(my_progression_items) > 0:
            chosen_item = self.world.random.choice(my_progression_items)
            if self.should_remove_item(chosen_item, material, min_material, max_material):
                my_progression_items.remove(chosen_item)
                continue
            
            if not self.world.has_prereqs(chosen_item):
                continue
                
            if self.world.can_add_more(chosen_item):
                try_item = self.world.create_item(chosen_item)
                self.consume_item(chosen_item)
                items.append(try_item)
                material += progression_items[chosen_item].material
            elif material >= min_material:
                my_progression_items.remove(chosen_item)
                
        return items

    def prepare_progression_item_pool(self) -> List[str]:
        """Prepare the pool of progression items with adjusted frequencies."""
        items = list(progression_items.keys())
        items.remove("Victory")
        # Adjust frequencies
        items.extend(["Progressive Pawn"] * 3)  # More pawn chance
        items.extend(["Progressive Pocket"] * 2)  # More pocket chance
        items.extend([item for item in items if item != "Progressive Major To Queen"])  # Halve queen promotion chance
        items.append("Progressive Minor Piece")  # Extra minor piece
        return items

    def create_useful_items(self) -> List[Item]:
        """Create useful items."""
        items = []
        my_useful_items = list(useful_items.keys())
        while len(my_useful_items) > 0:
            chosen_item = self.world.random.choice(my_useful_items)
            if not self.world.has_prereqs(chosen_item):
                continue
            if self.world.can_add_more(chosen_item):
                self.consume_item(chosen_item)
                try_item = self.world.create_item(chosen_item)
                items.append(try_item)
            else:
                my_useful_items.remove(chosen_item)
        return items

    def create_filler_items(self, has_pocket: bool) -> List[Item]:
        """Create filler items."""
        items = []
        my_filler_items = list(filler_items.keys())
        if not has_pocket:
            my_filler_items = [item for item in my_filler_items if "Pocket" not in item]
        
        while len(my_filler_items) > 0:
            if len(my_filler_items) == 0:
                my_filler_items = ["Progressive Pocket Gems"]
            chosen_item = self.world.random.choice(my_filler_items)
            if not has_pocket and not self.world.has_prereqs(chosen_item):
                continue
            if has_pocket or self.world.can_add_more(chosen_item):
                self.consume_item(chosen_item)
                try_item = self.world.create_item(chosen_item)
                items.append(try_item)
            else:
                my_filler_items.remove(chosen_item)
        return items

    def consume_item(self, item_name: str, locked_items: Dict[str, int]) -> None:
        """Track item consumption in the pool."""
        if item_name not in self.items_used[self.world.player]:
            self.items_used[self.world.player][item_name] = 0
        self.items_used[self.world.player][item_name] += 1

        if item_name in progression_items:
            if item_name not in self.items_remaining[self.world.player]:
                self.items_remaining[self.world.player][item_name] = progression_items[item_name].quantity
            self.items_remaining[self.world.player][item_name] -= 1

        self.lock_new_items(item_name, [], locked_items)

    def lock_new_items(self, chosen_item: str, items: List[Item], locked_items: Dict[str, int]) -> None:
        """Ensures the Castling location is reachable by locking necessary items."""
        if self.world.options.accessibility.value == self.world.options.accessibility.option_minimal:
            return
        if chosen_item == "Progressive Major To Queen":
            if self.unupgraded_majors_in_pool(items, locked_items) < 2:
                if "Progressive Major Piece" not in locked_items:
                    locked_items["Progressive Major Piece"] = 0
                locked_items["Progressive Major Piece"] += 1

    def unupgraded_majors_in_pool(self, items: List[Item], locked_items: Dict[str, int]) -> int:
        """Returns the number of unupgraded major pieces in the pool."""
        total_majors = len([item for item in items if item.name == "Progressive Major Piece"]) + len(
            [item for item in locked_items if item == "Progressive Major Piece"])
        total_upgrades = len([item for item in items if item.name == "Progressive Major To Queen"]) + len(
            [item for item in locked_items if item == "Progressive Major To Queen"])

        return total_majors - total_upgrades 

    def should_remove_item(self, item: str, current_material: int, min_material: int, max_material: int) -> bool:
        """Determine if an item should be removed from the pool."""
        if item not in progression_items:
            return False
        if current_material >= max_material:
            return True
        return False 