from collections import Counter
from BaseClasses import Item
import logging
import math

from .items import (
    FUNDAMENTAL_ITEMS,
    GEOMETRY_ITEMS,
    LEGACY_MATERIAL_ITEMS,
    filler_items,
    item_allowed_in_mode,
    item_table,
    progression_items,
    useful_items,
)
from .contract_resource import mode_item_maxima
from .locations import (
    highest_chessmen_requirement,
    highest_chessmen_requirement_small,
)
from .piece_model import PieceModel
from .material_model import MaterialModel
from .item_removal import ItemRemoval
from .pool_state import PoolAccounting, PoolCapacity


class CMItemPool:
    """Handles the creation and management of the item pool for ChecksMate."""

    def __init__(
        self,
        world,
        accounting: PoolAccounting | None = None,
        piece_model: PieceModel | None = None,
        material_model: MaterialModel | None = None,
    ):
        self.world = world
        existing_pool = getattr(world, "_item_pool", None)
        if accounting is None and existing_pool is not None:
            accounting = existing_pool.accounting
        if accounting is None:
            accounting = getattr(world, "pool_accounting", None)
        self.accounting = accounting if accounting is not None else PoolAccounting()
        reuse_existing_models = (
            existing_pool is not None
            and existing_pool.accounting is self.accounting
        )

        if piece_model is None and reuse_existing_models:
            piece_model = existing_pool.piece_model
        self.piece_model = (
            piece_model
            if piece_model is not None
            else PieceModel(world, self.accounting)
        )

        if material_model is None and reuse_existing_models:
            material_model = existing_pool.material_model
        self.material_model = (
            material_model
            if material_model is not None
            else MaterialModel(world, self.accounting)
        )
        self.removal_rules = ItemRemoval(self.world, self.piece_model)

    @property
    def items_used(self) -> dict[int, dict[str, int]]:
        """Compatibility view for callers that still expect a player key."""
        return self.accounting.used_player_view(self.world.player)

    @property
    def items_remaining(self) -> dict[int, dict[str, int]]:
        """Compatibility view for callers that still expect a player key."""
        return self.accounting.remaining_player_view(self.world.player)

    @property
    def is_fundamental(self) -> bool:
        option = getattr(self.world.options, "progression_itemization", None)
        return option is not None and option.value == option.option_fundamental

    @property
    def itemization(self) -> str:
        return "fundamental" if self.is_fundamental else "legacy"

    def normalize_counts(self, counts) -> dict[str, int]:
        maxima = mode_item_maxima(self.itemization)
        normalized = {}
        for name, raw_count in counts.items():
            if name not in item_table or not item_allowed_in_mode(name, self.itemization):
                continue
            if (
                name in GEOMETRY_ITEMS
                and self.world.options.goal.value == self.world.options.goal.option_single
            ):
                continue
            count = max(0, int(raw_count))
            maximum = maxima.get(name, item_table[name].quantity)
            if maximum > 0:
                count = min(count, maximum)
            if count:
                normalized[name] = count
        return normalized

    def has_prereqs(self, item_name: str, locked_items: dict[str, int]) -> bool:
        if item_name != "Castler":
            return self.piece_model.has_prereqs(item_name)
        castlers = self.accounting.used_count("Castler")
        chessmen = (
            self.accounting.used_count("Chessmen")
            + locked_items.get("Chessmen", 0)
        )
        material_items = (
            self.accounting.used_count("Material")
            + locked_items.get("Material", 0)
        )
        return (
            castlers < item_table["Castler"].quantity
            and chessmen > castlers
            and material_items * item_table["Material"].material >= (castlers + 1) * 500
        )

    def create_items(self, reserved_locations: int = 1) -> list[Item]:
        super_sized = self.world.options.goal.value != self.world.options.goal.option_single
        self.initialize_item_tracking()

        # Initialize items that must remain in the randomized pool.
        items = self.initialize_required_items()

        # Handle excluded items and starter items
        excluded_items = self.get_excluded_items()
        starter_items = self.assign_starter_items(excluded_items, self.world.locked_locations)
        for item in starter_items:
            self.consume_item(item.name, {})
        self.handle_excluded_items(excluded_items)
        items.extend(self.initialize_remaining_geometry_unlocks())

        # Calculate material requirements
        min_material, max_material = self.material_model.calculate_material_requirements()
        logging.debug(f"Material requirements: min={min_material}, max={max_material}")

        # Handle option limits
        self.handle_option_limits()

        # Process locked items and ensure prerequisites
        locked_items = self.handle_locked_items()

        capacity = PoolCapacity.for_world(
            self.world,
            super_sized,
            reserved_locations=reserved_locations + len(starter_items),
        )
        max_items = capacity.item_limit
        locked_items = self.fit_locked_items(
            locked_items,
            capacity.available(len(items)),
        )
        logging.debug(
            "Pool capacity: %s locations, %s reserved, %s randomized items",
            capacity.location_count,
            capacity.reserved_locations,
            capacity.item_limit,
        )

        # Create progression items
        progression_items = self.create_progression_items(
            max_items=max(0, max_items - len(items)),
            min_material=min_material,
            max_material=max_material,
            locked_items=locked_items,
        )
        items.extend(progression_items)
        logging.debug(f"Created {len(progression_items)} progression items")

        # Create useful items with remaining space
        remaining_items = max_items - len(items)
        if remaining_items > 0:
            useful_items = self.create_useful_items(
                max_items=remaining_items,
                locked_items=locked_items,
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
            )
            items.extend(filler_items)
            logging.debug(f"Created {len(filler_items)} filler items")

        # Add locked items
        for item in locked_items:
            self.accounting.add_used(item, locked_items[item])
            items.extend([self.world.create_item(item) for _ in range(locked_items[item])])

        return items

    def fit_locked_items(self, locked_items: dict[str, int], capacity: int) -> dict[str, int]:
        if capacity <= 0:
            return {}
        fitted: dict[str, int] = {}
        remaining = capacity
        if self.is_fundamental:
            mandatory_chessmen = min(
                locked_items.get("Chessmen", 0),
                self._fundamental_accessibility_chessmen_requirement(),
                remaining,
            )
            if mandatory_chessmen:
                fitted["Chessmen"] = mandatory_chessmen
                remaining -= mandatory_chessmen
        if self.is_fundamental and locked_items.get("Castler", 0):
            requested = locked_items["Castler"]
            used_castlers = self.accounting.used_count("Castler")
            used_chessmen = self.accounting.used_count("Chessmen")
            used_material = self.accounting.used_count("Material")
            for castlers in range(requested, 0, -1):
                total_castlers = used_castlers + castlers
                chessmen = max(
                    0,
                    total_castlers
                    - used_chessmen
                    - fitted.get("Chessmen", 0),
                )
                material = max(
                    0,
                    math.ceil(total_castlers * 500 / item_table["Material"].material)
                    - used_material
                    - fitted.get("Material", 0),
                )
                if castlers + chessmen + material <= remaining:
                    fitted["Castler"] = castlers
                    if chessmen:
                        fitted["Chessmen"] = (
                            fitted.get("Chessmen", 0) + chessmen
                        )
                    if material:
                        fitted["Material"] = (
                            fitted.get("Material", 0) + material
                        )
                    remaining -= castlers + chessmen + material
                    break
        if (
            self.is_fundamental
            and self._fundamental_accessibility_chessmen_requirement()
        ):
            remaining_names = [
                "Material",
                *sorted(
                    name
                    for name in locked_items
                    if name not in {"Castler", "Chessmen", "Material"}
                ),
                "Chessmen",
            ]
        else:
            remaining_names = list(locked_items)
        for name in remaining_names:
            count = locked_items.get(name, 0)
            if self.is_fundamental and name == "Castler":
                continue
            already = fitted.get(name, 0)
            add = min(max(0, count - already), remaining)
            if add:
                fitted[name] = already + add
                remaining -= add
            if remaining <= 0:
                break
        return fitted

    def _fundamental_accessibility_chessmen_requirement(self) -> int:
        if (
            not self.is_fundamental
            or self.world.options.accessibility.value
            == self.world.options.accessibility.option_minimal
        ):
            return 0
        required_chessmen = (
            highest_chessmen_requirement_small
            if self.world.options.goal.value == self.world.options.goal.option_single
            else highest_chessmen_requirement
        )
        return max(
            0,
            required_chessmen
            - self.accounting.used_count("Chessmen"),
        )

    def initialize_remaining_geometry_unlocks(self) -> list[Item]:
        if self.world.options.goal.value == self.world.options.goal.option_single:
            return []
        items = []
        for name in ("Board Files", "Board Ranks"):
            remaining = (
                item_table[name].quantity
                - self.accounting.used_count(name)
            )
            for _ in range(max(0, remaining)):
                self.consume_item(name, {})
                items.append(self.world.create_item(name))
        return items

    def initialize_item_tracking(self) -> None:
        """Reset this world's item accounting."""
        self.accounting.reset()

    def initialize_required_items(self) -> list[Item]:
        """Initialize required items that remain in the randomized pool."""
        items = []
        
        # Current-schema v2 uses independent geometry unlock items.
        if self.world.options.goal.value == self.world.options.goal.option_progressive:
            items.append(self.world.create_item("Board Files"))
            self.consume_item("Board Files", {})
            
        # Add Play as White
        items.append(self.world.create_item("Play as White"))
        self.accounting.set_used("Play as White", 1)
        
        return items

    def get_excluded_items(self) -> dict[str, int]:
        """Get items that should be excluded from the item pool."""
        excluded_items: dict[str, int] = {}

        # Handle super-sized items
        if self.world.options.goal.value == self.world.options.goal.option_super:
            item = self.world.create_item("Board Files")
            self.world.multiworld.push_precollected(item)

        # Track precollected items
        raw_counts = Counter(
            item.name for item in self.world.multiworld.precollected_items[self.world.player]
        )
        excluded_items.update(self.normalize_counts(raw_counts))

        return excluded_items

    def assign_starter_items(self,
                             excluded_items: dict[str, int],
                             locked_locations: list[str]) -> list[Item]:
        """Assign starter items based on game options."""
        user_items = []
        
        # Handle ordered progression
        if self.world.options.goal.value == self.world.options.goal.option_ordered_progressive:
            ordered_unlocks = (
                ("Checkmate Minima", "Board Files"),
                ("Checkmate Maxima", "Board Ranks"),
                ("Checkmate 10x10", "Board Files"),
                ("Checkmate 12x10", "Board Ranks"),
            )
            for location_name, item_name in ordered_unlocks:
                item = self.world.create_item(item_name)
                self.world.multiworld.get_location(
                    location_name, self.world.player
                ).place_locked_item(item)
                locked_locations.append(location_name)
                user_items.append(item)

        # Handle early material option
        early_material_option = self.world.options.early_material.value
        if early_material_option > 0:
            if self.is_fundamental:
                early_units = ["Chessmen"]
            else:
                early_units = []
                if early_material_option == 1 or early_material_option > 4:
                    early_units.append("Progressive Pawn")
                if early_material_option == 2 or early_material_option > 3:
                    early_units.append("Progressive Minor Piece")
                if early_material_option > 2:
                    early_units.append("Progressive Major Piece")
                    if self.world.options.asymmetric_trades.value != self.world.options.asymmetric_trades.option_disabled:
                        early_units.append("Progressive Jack")

            # Filter out non-local and excluded items
            non_local_items = getattr(
                getattr(self.world.options, "non_local_items", None),
                "value",
                set(),
            )
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

    def handle_excluded_items(self, excluded_items: dict[str, int]) -> list[Item]:
        """Process excluded items and return starter items."""
        starter_items = []
        for item_name in excluded_items:
            self.accounting.add_used(item_name, excluded_items[item_name])
            starter_items.extend([self.world.create_item(item_name) for _ in range(excluded_items[item_name])])
        return starter_items

    def handle_option_limits(self) -> None:
        """Apply world options that limit the maximum copies of some items."""
        self.accounting.add_used(
            "Progressive Consul",
            3 - self.world.options.max_kings.value,
        )
        self.accounting.add_used(
            "Progressive King Promotion",
            2 - self.world.options.fairy_kings.value,
        )
        self.accounting.add_used(
            "Progressive AI Intelligence Malus",
            5 - self.world.options.max_engine_penalties.value,
        )
        self.accounting.add_used(
            "Progressive Pocket",
            12
            - min(
                self.world.options.max_pocket.value,
                3 * self.world.options.pocket_limit_by_pocket.value,
            ),
        )

    def handle_locked_items(self) -> dict[str, int]:
        """Process locked items from options and ensure prerequisites are met."""
        # Get locked items from options
        yaml_locked_items: dict[str, int] = self.world.options.locked_items.value
        locked_items = self.normalize_counts(yaml_locked_items)
        maxima = mode_item_maxima(self.itemization)
        locked_items = {
            name: min(
                count,
                max(0, maxima.get(name, count) - self.accounting.used_count(name)),
            )
            for name, count in locked_items.items()
        }
        locked_items = {name: count for name, count in locked_items.items() if count > 0}

        if self.is_fundamental:
            if (
                self.world.options.accessibility.value
                != self.world.options.accessibility.option_minimal
            ):
                locked_items["Castler"] = max(
                    locked_items.get("Castler", 0),
                    1 - self.accounting.used_count("Castler"),
                )
            total_castlers = (
                self.accounting.used_count("Castler")
                + locked_items.get("Castler", 0)
            )
            required_chessmen = total_castlers
            required_material = math.ceil(total_castlers * 500 / item_table["Material"].material)
            locked_items["Chessmen"] = max(
                locked_items.get("Chessmen", 0),
                required_chessmen - self.accounting.used_count("Chessmen"),
            )
            locked_items["Material"] = max(
                locked_items.get("Material", 0),
                required_material - self.accounting.used_count("Material"),
            )
            required_chessmen = (
                self._fundamental_accessibility_chessmen_requirement()
            )
            if required_chessmen:
                locked_items["Chessmen"] = max(
                    locked_items.get("Chessmen", 0),
                    required_chessmen,
                )
            return {name: count for name, count in locked_items.items() if count > 0}

        # Ensure locked items have enough parents
        player_queens = (
            locked_items.get("Progressive Major To Queen", 0)
            + self.accounting.used_count("Progressive Major To Queen")
        )
        locked_items["Progressive Major Piece"] = max(
            player_queens, locked_items.get("Progressive Major Piece", 0))

        # Ensure castling is possible
        if self.world.options.accessibility.value != self.world.options.accessibility.option_minimal:
            required_majors = (
                2
                - self.accounting.used_count("Progressive Major Piece")
                + player_queens
            )
            locked_items["Progressive Major Piece"] = max(
                required_majors, locked_items.get("Progressive Major Piece", 0))

        # Calculate and log remaining material
        remaining_material = sum([locked_items[item] * progression_items[item].material 
                                for item in locked_items if item in progression_items])
        logging.debug(f"{self.world.player} pre-fill granted total material of {remaining_material} " +
                     f"via locked items {locked_items} with excluded items {self.accounting.used}")

        return locked_items

    def get_max_items(self, super_sized: bool) -> int:
        """Calculate the maximum number of items based on world options."""
        return PoolCapacity.for_world(
            self.world,
            super_sized,
        ).location_count

    def create_progression_items(
        self,
        max_items: int,
        min_material: float = 4100,
        max_material: float = 4600,
        locked_items: dict[str, int] | None = None,
        user_event_count: int = 0,
    ) -> list[Item]:
        """Create progression items up to material limits."""
        if locked_items is None:
            locked_items = {}
        items = []
        material = self.material_model.calculate_items_material(items)
        my_progression_items = self.prepare_progression_item_pool()
        self.accounting.remaining.clear()
        self.accounting.remaining.update({
            name: (
                progression_items[name].quantity
                - self.accounting.used_count(name)
            )
            for name in my_progression_items
        })

        while ((len(items) + user_event_count + sum(locked_items.values())) < max_items and
               len(my_progression_items) > 0):
            chosen_item = self.world.random.choice(my_progression_items)
            
            # Check if we should remove this item from consideration (limits, material, accessibility)
            if self.should_remove_item(chosen_item, material, min_material, max_material,
                                     items, my_progression_items, locked_items, user_event_count):
                my_progression_items.remove(chosen_item)
                continue
            
            if (self.has_prereqs(chosen_item, locked_items) and
                    self.piece_model.can_add_more(chosen_item)):
                try_item = self.world.create_item(chosen_item)
                was_locked = self.consume_item(chosen_item, locked_items)
                items.append(try_item)
                material += (
                    0
                    if chosen_item == "Progressive Pocket"
                    else progression_items[chosen_item].material
                )
                if not was_locked:
                    self.lock_new_items(chosen_item, items, locked_items)
                
        all_material = sum([locked_items[item] * progression_items[item].material for item in locked_items if item in progression_items]) + material
        logging.debug(str(self.world.player) + " granted total material of " + str(all_material) +
                      " toward " + str(max_material) + " via items " + str(self.accounting.used) +
                      " having generated " + str(Counter(items)))
        return items

    def prepare_progression_item_pool(self) -> list[str]:
        """Prepare the pool of progression items with adjusted frequencies."""
        # Start with all progression items except Victory and those with quantity=0
        items = [
            item for item in progression_items
            if item not in {"Victory", "Super-Size Me"}
            and item not in GEOMETRY_ITEMS
            and progression_items[item].quantity > 0
            and item_allowed_in_mode(item, self.itemization)
        ]

        if self.is_fundamental:
            items.extend(["Chessmen"] * 3)
            items.extend(["Material"] * 2)
            items.extend(["Progressive Pocket"] * 2)
            return items
        
        if self.world.options.asymmetric_trades.value != self.world.options.asymmetric_trades.option_jacks:
            items.remove("Progressive Jack")

        # Adjust frequencies
        items.extend(["Progressive Pawn"] * 3)  # More pawn chance
        items.extend(["Progressive Pocket"] * 2)  # More pocket chance
        items.extend([item for item in items if item != "Progressive Major To Queen"])  # Halve queen promotion chance
        items.append("Progressive Minor Piece")  # Extra minor piece
        return items

    def create_useful_items(
        self,
        max_items: int,
        locked_items: dict[str, int] | None = None,
        user_event_count: int = 0,
    ) -> list[Item]:
        """Create useful items."""
        if locked_items is None:
            locked_items = {}
        items = []
        my_useful_items = list(useful_items.keys())

        while ((len(items) + user_event_count + sum(locked_items.values())) < max_items and
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

    def create_filler_items(
        self,
        has_pocket: bool,
        max_items: int,
        locked_items: dict[str, int] | None = None,
        user_event_count: int = 0,
    ) -> list[Item]:
        """Create filler items up to max_items limit."""
        if locked_items is None:
            locked_items = {}
        items = []
        my_filler_items = list(filler_items.keys())
        if self.is_fundamental:
            my_filler_items = [
                item for item in my_filler_items
                if item not in LEGACY_MATERIAL_ITEMS
            ]
        
        # Filter out pocket-related items if pocket is disabled
        if not has_pocket:
            my_filler_items = [item for item in my_filler_items if "Pocket" not in item]
        
        while (len(items) + user_event_count + sum(locked_items.values())) < max_items:
            # If we have no valid filler items, use pocket gems as fallback
            if not my_filler_items:
                # Fill all remaining slots with Progressive Pocket Gems
                remaining_slots = max_items - (len(items) + user_event_count + sum(locked_items.values()))
                for _ in range(remaining_slots):
                    self.consume_item("Progressive Pocket Gems", locked_items)
                    try_item = self.world.create_item("Progressive Pocket Gems")
                    items.append(try_item)
                break
            
            chosen_item = self.world.random.choice(my_filler_items)
            if not has_pocket and not self.piece_model.has_prereqs(chosen_item):
                my_filler_items.remove(chosen_item)  # Remove items we can't use
                continue
                
            if self.piece_model.can_add_more(chosen_item):
                self.consume_item(chosen_item, locked_items)
                try_item = self.world.create_item(chosen_item)
                items.append(try_item)
            else:
                my_filler_items.remove(chosen_item)  # Remove items we can't add
                
        return items

    def consume_item(self, item_name: str, locked_items: dict[str, int]) -> bool:
        """Track item consumption in the pool. Returns True if the item was locked."""
        was_locked = item_name in locked_items
        if was_locked:
            locked_items[item_name] -= 1
            if locked_items[item_name] <= 0:
                del locked_items[item_name]
            
        quantity = (
            progression_items[item_name].quantity
            if item_name in progression_items
            else None
        )
        self.accounting.consume(item_name, quantity)

        return was_locked

    def lock_new_items(self, chosen_item: str, items: list[Item], locked_items: dict[str, int]) -> None:
        """Ensures the Castling location is reachable by locking necessary items."""
        if self.world.options.accessibility.value == self.world.options.accessibility.option_minimal:
            return
        if chosen_item == "Progressive Major To Queen":
            if self.material_model.castling_pieces_in_pool(items, locked_items) < 2:
                if "Progressive Major Piece" not in locked_items:
                    locked_items["Progressive Major Piece"] = 0
                # TODO(chesslogic): Choose between Progressive Jack and Progressive Major Piece
                locked_items["Progressive Major Piece"] += 1

    def calculate_possible_queens(self) -> int:
        """Calculate the maximum number of queen upgrades that will be in the game.
        This is used to determine the minimum number of major pieces needed for castling.
        We use the minimum possible number to avoid the 'Oh no, Terraria Hard Mode' problem, where
        getting more items (queen upgrades) could make a location (castling) harder to access."""
        return self.accounting.used_count("Progressive Major To Queen")

    def should_remove_item(self, chosen_item: str, material: int, min_material: float,
                           max_material: float, items: list[Item], my_progression_items: list[str],
                           locked_items: dict[str, int], user_event_count: int) -> bool:
        """Delegate item removal decision to ItemRemovalRules."""
        return self.removal_rules.should_remove_item(
            chosen_item, material, min_material, max_material,
            items, my_progression_items, locked_items, user_event_count)
