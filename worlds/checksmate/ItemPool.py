from typing import Dict, List
from collections import Counter
from BaseClasses import Item
import logging
import math

from .Items import (CMItem, item_table, filler_items, progression_items,
                   useful_items, item_name_groups)
from .Locations import location_table, Tactic
from .Rules import determine_min_material, determine_max_material
from .PieceModel import PieceModel
from .MaterialModel import MaterialModel
from .ItemRemoval import ItemRemoval


class CMItemPool:
    """Handles the creation and management of the item pool for ChecksMate."""

    def __init__(self, world):
        self.world = world
        self.items_used: Dict[int, Dict[str, int]] = {}
        self.items_remaining: Dict[int, Dict[str, int]] = {}
        self._piece_model = None
        self._material_model = None
        self._removal = None

    @property
    def piece_model(self) -> PieceModel:
        """Lazy initialization of piece model to avoid circular dependencies."""
        if self._piece_model is None:
            self._piece_model = PieceModel(self.world)
            self._piece_model.items_used = self.items_used
        return self._piece_model

    @property
    def material_model(self) -> MaterialModel:
        """Lazy initialization of material model to avoid circular dependencies."""
        if self._material_model is None:
            self._material_model = MaterialModel(self.world)
            self._material_model.items_used = self.items_used
        return self._material_model

    @property
    def removal_rules(self) -> ItemRemoval:
        """Lazy initialization of removal rules to avoid circular dependencies."""
        if self._removal is None:
            self._removal = ItemRemoval(self.world, self.piece_model)
        return self._removal

    def create_items(self) -> None:
        super_sized = self.world.options.goal.value != self.world.options.goal.option_single
        self.initialize_item_tracking()

        # Initialize required items (Victory and Play as White)
        items = self.initialize_required_items()
        
        # Handle excluded items and starter items
        excluded_items = self.get_excluded_items()
        starter_items = self.assign_starter_items(excluded_items, self.world.locked_locations)
        for item in starter_items:
            self.consume_item(item.name, {})
        self.handle_excluded_items(excluded_items)
        user_location_count = len(starter_items)
        user_location_count += 1  # Victory item is counted as part of the pool, but you don't start with it

        # Calculate material requirements
        min_material, max_material = self.material_model.calculate_material_requirements(super_sized)
        logging.debug(f"Material requirements: min={min_material}, max={max_material}")

        # Handle option limits
        self.handle_option_limits()

        # Process locked items and ensure prerequisites
        locked_items = self.handle_locked_items()

        # Calculate max items
        max_items = self.get_max_items(super_sized)
        logging.debug(f"Max items: {max_items}")

        # Create progression items
        progression_items = self.create_progression_items(
            max_items=max_items,
            min_material=min_material,
            max_material=max_material,
            locked_items=locked_items,
            user_location_count=user_location_count
        )
        items.extend(progression_items)
        logging.debug(f"Created {len(progression_items)} progression items")

        # Create useful items with remaining space
        remaining_items = max_items - len(items)
        if remaining_items > 0:
            useful_items = self.create_useful_items(
                max_items=remaining_items,
                locked_items=locked_items,
                user_location_count=user_location_count
            )
            items.extend(useful_items)
            logging.debug(f"Created {len(useful_items)} useful items")

        # Check for pocket items
        has_pocket = any("Pocket" in item.name for item in items)

        # Create filler items with remaining space
        remaining_items = max_items - len(items)
        if remaining_items > 0:
            filler_items = self.create_filler_items(
                has_pocket=has_pocket,
                max_items=remaining_items,
                locked_items=locked_items,
                user_location_count=user_location_count
            )
            items.extend(filler_items)
            logging.debug(f"Created {len(filler_items)} filler items")

        for item in locked_items:
            if item not in self.items_used[self.world.player]:
                self.items_used[self.world.player][item] = 0
            self.items_used[self.world.player][item] += locked_items[item]
            items.extend([self.world.create_item(item) for _ in range(locked_items[item])])

        return items

    def initialize_item_tracking(self) -> None:
        """Initialize the item tracking dictionaries."""
        self.items_used[self.world.player] = {}
        self.items_remaining[self.world.player] = {}

    def initialize_required_items(self) -> List[Item]:
        """Initialize required items like Victory and Play as White."""
        items = []
        
        # Add Super-Size Me for progressive mode
        if self.world.options.goal.value == self.world.options.goal.option_progressive:
            items.append(self.world.create_item("Super-Size Me"))
            
        # Add Play as White
        items.append(self.world.create_item("Play as White"))
        self.items_used[self.world.player]["Play as White"] = 1
        
        return items

    def get_excluded_items(self) -> Dict[str, int]:
        """Get items that should be excluded from the item pool."""
        excluded_items: Dict[str, int] = {}

        # Handle super-sized items
        if self.world.options.goal.value == self.world.options.goal.option_super:
            item = self.world.create_item("Super-Size Me")
            self.world.multiworld.push_precollected(item)

        # Track precollected items
        for item in self.world.multiworld.precollected_items[self.world.player]:
            if item.name not in excluded_items:
                excluded_items[item.name] = 0
            excluded_items[item.name] += 1

        # TODO: Handle excluded_items_option if needed
        # excluded_items_option = getattr(multiworld, 'excluded_items', {player: []})
        # excluded_items.update(excluded_items_option[player].value)

        return excluded_items

    def assign_starter_items(self,
                             excluded_items: Dict[str, int],
                             locked_locations: List[str]) -> List[Item]:
        """Assign starter items based on game options."""
        user_items = []
        
        # Handle ordered progression
        if self.world.options.goal.value == self.world.options.goal.option_ordered_progressive:
            item = self.world.create_item("Super-Size Me")
            self.world.multiworld.get_location("Checkmate Minima", self.world.player).place_locked_item(item)
            locked_locations.append("Checkmate Minima")
            user_items.append(item)

        # Handle early material option
        early_material_option = self.world.options.early_material.value
        if early_material_option > 0:
            early_units = []
            if early_material_option == 1 or early_material_option > 4:
                early_units.append("Progressive Pawn")
            if early_material_option == 2 or early_material_option > 3:
                early_units.append("Progressive Minor Piece")
            if early_material_option > 2:
                early_units.append("Progressive Major Piece")

            # Filter out non-local and excluded items
            non_local_items = self.world.options.non_local_items.value
            local_basic_unit = sorted(item for item in early_units if
                                    item not in non_local_items and (
                                        item not in excluded_items or
                                        excluded_items[item] < item_table[item].quantity))
            
            if not local_basic_unit:
                raise Exception("At least one early chessman must be local")

            # Place early material item
            item = self.world.create_item(self.world.random.choice(local_basic_unit))
            self.world.multiworld.get_location("King to E2/E7 Early", self.world.player).place_locked_item(item)
            locked_locations.append("King to E2/E7 Early")
            user_items.append(item)

        return user_items

    def handle_excluded_items(self, excluded_items: Dict[str, int]) -> List[Item]:
        """Process excluded items and return starter items."""
        starter_items = []
        for item_name in excluded_items:
            if item_name not in self.items_used[self.world.player]:
                self.items_used[self.world.player][item_name] = 0
            self.items_used[self.world.player][item_name] += excluded_items[item_name]
            starter_items.extend([self.world.create_item(item_name) for _ in range(excluded_items[item_name])])
        return starter_items

    def calculate_material_requirements(self, super_sized: bool) -> tuple[float, float]:
        """Calculate the minimum and maximum material requirements based on world options."""
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

    def handle_locked_items(self) -> Dict[str, int]:
        """Process locked items from options and ensure prerequisites are met."""
        # Get locked items from options
        yaml_locked_items: Dict[str, int] = self.world.options.locked_items.value
        locked_items = dict(yaml_locked_items)

        # Ensure locked items have enough parents
        player_queens: int = (locked_items.get("Progressive Major To Queen", 0) +
                            self.items_used[self.world.player].get("Progressive Major To Queen", 0))
        locked_items["Progressive Major Piece"] = max(
            player_queens, locked_items.get("Progressive Major Piece", 0))

        # Ensure castling is possible
        if self.world.options.accessibility.value != self.world.options.accessibility.option_minimal:
            required_majors: int = 2 - self.items_used[self.world.player].get("Progressive Major Piece", 0) + player_queens
            locked_items["Progressive Major Piece"] = max(
                required_majors, locked_items.get("Progressive Major Piece", 0))

        # Calculate and log remaining material
        remaining_material = sum([locked_items[item] * progression_items[item].material 
                                for item in locked_items if item in progression_items])
        logging.debug(f"{self.world.player} pre-fill granted total material of {remaining_material} " +
                     f"via locked items {locked_items} with excluded items {self.items_used[self.world.player]}")

        return locked_items

    def get_max_items(self, super_sized: bool) -> int:
        """Calculate the maximum number of items based on world options."""
        # Start with all locations that are valid for the current game mode
        valid_locations = [loc for loc in location_table if 
                         (super_sized or location_table[loc].material_expectations != -1)]
        
        # Filter out tactics based on options
        if self.world.options.enable_tactics.value == self.world.options.enable_tactics.option_none:
            valid_locations = [loc for loc in valid_locations if location_table[loc].is_tactic is None]
        elif self.world.options.enable_tactics.value == self.world.options.enable_tactics.option_turns:
            valid_locations = [loc for loc in valid_locations if 
                             location_table[loc].is_tactic is None or 
                             location_table[loc].is_tactic == Tactic.Turns]

        return len(valid_locations)

    def create_progression_items(self,
                               max_items: int,
                               min_material: float = 4100,
                               max_material: float = 4600,
                               locked_items: Dict[str, int] = {},
                               user_location_count: int = 0) -> List[Item]:
        """Create progression items up to material limits."""
        items = []
        material = self.calculate_current_material(items)
        my_progression_items = self.prepare_progression_item_pool()
        self.items_remaining[self.world.player] = {
            name: progression_items[name].quantity - self.items_used[self.world.player].get(name, 0) for name in my_progression_items}
        
        while ((len(items) + user_location_count + sum(locked_items.values())) < max_items and
               len(my_progression_items) > 0):
            chosen_item = self.world.random.choice(my_progression_items)
            
            # Check if we should remove this item from consideration (limits, material, accessibility)
            if self.should_remove_item(chosen_item, material, min_material, max_material,
                                     items, my_progression_items, locked_items):
                my_progression_items.remove(chosen_item)
                continue
            
            if (self.piece_model.has_prereqs(chosen_item) and
                    self.piece_model.can_add_more(chosen_item)):
                try_item = self.world.create_item(chosen_item)
                was_locked = self.consume_item(chosen_item, locked_items)
                items.append(try_item)
                material += progression_items[chosen_item].material
                if not was_locked:
                    self.lock_new_items(chosen_item, items, locked_items)
                
        all_material = sum([locked_items[item] * progression_items[item].material for item in locked_items if item in progression_items]) + material
        logging.debug(str(self.world.player) + " granted total material of " + str(all_material) +
                      " toward " + str(max_material) + " via items " + str(self.items_used[self.world.player]) +
                      " having generated " + str(Counter(items)))
        return items

    def prepare_progression_item_pool(self) -> List[str]:
        """Prepare the pool of progression items with adjusted frequencies."""
        # Start with all progression items except Victory and those with quantity=0
        items = [item for item in progression_items.keys() 
                if item != "Victory" and progression_items[item].quantity > 0]
        
        # Adjust frequencies
        items.extend(["Progressive Pawn"] * 3)  # More pawn chance
        items.extend(["Progressive Pocket"] * 2)  # More pocket chance
        items.extend([item for item in items if item != "Progressive Major To Queen"])  # Halve queen promotion chance
        items.append("Progressive Minor Piece")  # Extra minor piece
        return items

    def create_useful_items(self, max_items: int, locked_items: Dict[str, int] = {}, user_location_count: int = 0) -> List[Item]:
        """Create useful items."""
        items = []
        my_useful_items = list(useful_items.keys())

        while ((len(items) + user_location_count + sum(locked_items.values())) < max_items and
               len(my_useful_items) > 0):
            chosen_item = self.world.random.choice(my_useful_items)
            if not self.piece_model.has_prereqs(chosen_item):
                continue
            if self.piece_model.can_add_more(chosen_item):
                self.consume_item(chosen_item, locked_items)
                try_item = self.world.create_item(chosen_item)
                items.append(try_item)
            else:
                my_useful_items.remove(chosen_item)
        return items

    def create_filler_items(self, has_pocket: bool, max_items: int, locked_items: Dict[str, int] = {}, user_location_count: int = 0) -> List[Item]:
        """Create filler items up to max_items limit."""
        items = []
        my_filler_items = list(filler_items.keys())
        
        # Filter out pocket-related items if pocket is disabled
        if not has_pocket:
            my_filler_items = [item for item in my_filler_items if "Pocket" not in item]
        
        while (len(items) + user_location_count + sum(locked_items.values())) < max_items:
            # If we have no valid filler items, use pocket gems as fallback
            if not my_filler_items:
                # Fill all remaining slots with Progressive Pocket Gems
                remaining_slots = max_items - (len(items) + user_location_count + sum(locked_items.values()))
                for _ in range(remaining_slots):
                    self.consume_item("Progressive Pocket Gems", locked_items)
                    try_item = self.world.create_item("Progressive Pocket Gems")
                    items.append(try_item)
                break
            
            chosen_item = self.world.random.choice(my_filler_items)
            if not has_pocket and not self.piece_model.has_prereqs(chosen_item):
                my_filler_items.remove(chosen_item)  # Remove items we can't use
                continue
                
            if has_pocket or self.piece_model.can_add_more(chosen_item):
                self.consume_item(chosen_item, locked_items)
                try_item = self.world.create_item(chosen_item)
                items.append(try_item)
            else:
                my_filler_items.remove(chosen_item)  # Remove items we can't add
                
        return items

    def consume_item(self, item_name: str, locked_items: Dict[str, int]) -> bool:
        """Track item consumption in the pool. Returns True if the item was locked."""
        was_locked = item_name in locked_items
        if was_locked:
            locked_items[item_name] -= 1
            if locked_items[item_name] == 0:
                del locked_items[item_name]
            
        if item_name not in self.items_used[self.world.player]:
            self.items_used[self.world.player][item_name] = 0
        self.items_used[self.world.player][item_name] += 1

        if item_name in progression_items:
            if item_name not in self.items_remaining[self.world.player]:
                self.items_remaining[self.world.player][item_name] = progression_items[item_name].quantity
            self.items_remaining[self.world.player][item_name] -= 1

        return was_locked

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

    def calculate_current_material(self, items: List[Item] = None) -> int:
        """Calculate the total material value of currently generated items.
        
        Args:
            items: List of items to calculate material from. If None, calculates from items_used (for backward compatibility).
        """
        # Calculate based on actual items
        item_counts = Counter(item.name for item in items)
        return sum(
            min(progression_items[item_name].material * count,
                progression_items[item_name].material * progression_items[item_name].quantity)
            for item_name, count in item_counts.items()
            if item_name in progression_items
        )

    def calculate_remaining_material(self, locked_items: Dict[str, int]) -> int:
        """Calculate the material value of locked items that have material value."""
        return sum([
            locked_items[item] * progression_items[item].material 
            for item in locked_items 
            if item in progression_items and progression_items[item].material > 0
        ])

    def calculate_possible_queens(self) -> int:
        """Calculate the maximum number of queen upgrades that will be in the game.
        This is used to determine the minimum number of major pieces needed for castling.
        We use the minimum possible number to avoid the 'Oh no, Terraria Hard Mode' problem, where
        getting more items (queen upgrades) could make a location (castling) harder to access."""
        if self.world.options.accessibility.value == self.world.options.accessibility.option_minimal:
            return 0
        return self.items_used[self.world.player].get("Progressive Major To Queen", 0)

    def should_remove_item(self, chosen_item: str, material: int, min_material: float,
                         max_material: float, items: List[Item], my_progression_items: List[str],
                         locked_items: Dict[str, int]) -> bool:
        """Delegate item removal decision to ItemRemovalRules."""
        return self.removal_rules.should_remove_item(
            chosen_item, material, min_material, max_material,
            items, my_progression_items, locked_items)

    def chessmen_count(self, items: List[CMItem], pocket_limit: int) -> int:
        """Count the number of chessmen in the item pool."""
        pocket_amount = (0 if pocket_limit <= 0 else
                        math.ceil(len([item for item in items if item.name == "Progressive Pocket"]) / pocket_limit))
        chessmen_amount = len([item for item in items if item.name in item_name_groups["Chessmen"]])
        logging.debug("Found {} chessmen and {} pocket men".format(chessmen_amount, pocket_amount))
        return chessmen_amount + pocket_amount

    def lockable_material_value(self, chosen_item: str, items: List[CMItem], locked_items: Dict[str, int]):
        '''if this piece was added, it might add more than its own material to the locked pool'''
        material = progression_items[chosen_item].material
        if self.world.options.accessibility.value == self.world.options.accessibility.option_minimal:
            return material
        if chosen_item == "Progressive Major To Queen" and self.unupgraded_majors_in_pool(items, locked_items) <= 2:
            material += progression_items["Progressive Major Piece"].material
        return material
