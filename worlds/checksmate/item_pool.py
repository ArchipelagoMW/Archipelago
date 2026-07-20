
from collections import Counter
from BaseClasses import Item
import logging
import math

from .items import (
    CMItem,
    FUNDAMENTAL_ITEMS,
    GEOMETRY_ITEMS,
    LEGACY_CHESSMEN_GROUP,
    LEGACY_MATERIAL_ITEMS,
    filler_items,
    item_allowed_in_mode,
    item_name_groups,
    item_table,
    progression_items,
    useful_items,
)
from .contract_resource import mode_item_maxima
from .locations import (
    BoardStage,
    highest_chessmen_requirement,
    highest_chessmen_requirement_small,
    location_names_for_stage,
    location_table,
)
from .rules import determine_min_material, determine_max_material
from .piece_model import PieceModel
from .material_model import MaterialModel
from .item_removal import ItemRemoval


class CMItemPool:
    """Handles the creation and management of the item pool for ChecksMate."""

    def __init__(self, world):
        self.world = world
        self.items_used: dict[int, dict[str, int]] = {}
        self.items_remaining: dict[int, dict[str, int]] = {}
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
        castlers = self.items_used[self.world.player].get("Castler", 0)
        chessmen = (
            self.items_used[self.world.player].get("Chessmen", 0)
            + locked_items.get("Chessmen", 0)
        )
        material_items = (
            self.items_used[self.world.player].get("Material", 0)
            + locked_items.get("Material", 0)
        )
        return (
            castlers < item_table["Castler"].quantity
            and chessmen > castlers
            and material_items * item_table["Material"].material >= (castlers + 1) * 500
        )

    def create_items(self) -> list[Item]:
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
        items.extend(self.initialize_remaining_geometry_unlocks())
        user_event_count = len(starter_items)
        user_event_count += 1  # Victory item is counted as part of the pool, but you don't start with it

        # Calculate material requirements
        min_material, max_material = self.material_model.calculate_material_requirements()
        logging.debug(f"Material requirements: min={min_material}, max={max_material}")

        # Handle option limits
        self.handle_option_limits()

        # Process locked items and ensure prerequisites
        locked_items = self.handle_locked_items()

        # Calculate max items
        max_items = self.get_max_items(super_sized)
        locked_items = self.fit_locked_items(
            locked_items,
            max(0, max_items - len(items) - user_event_count),
        )
        logging.debug(f"Max items: {max_items}")

        # Create progression items
        progression_items = self.create_progression_items(
            max_items=max(0, max_items - len(items)),
            min_material=min_material,
            max_material=max_material,
            locked_items=locked_items,
            user_event_count=user_event_count
        )
        items.extend(progression_items)
        logging.debug(f"Created {len(progression_items)} progression items")

        # Create useful items with remaining space
        remaining_items = max_items - len(items)
        if remaining_items > 0:
            useful_items = self.create_useful_items(
                max_items=remaining_items,
                locked_items=locked_items,
                user_event_count=user_event_count
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
                user_event_count=user_event_count
            )
            items.extend(filler_items)
            logging.debug(f"Created {len(filler_items)} filler items")

        # Add locked items
        for item in locked_items:
            if item not in self.items_used[self.world.player]:
                self.items_used[self.world.player][item] = 0
            self.items_used[self.world.player][item] += locked_items[item]
            items.extend([self.world.create_item(item) for _ in range(locked_items[item])])

        # # Ensure we don't exceed max_items + event_count
        # event_count = 2  # Play as White and Victory
        # if super_sized:
        #     event_count += 1  # Super-Size Me for non-single modes
        # max_total = max_items + event_count
        # if len(items) > max_total:
        #     # Remove excess items, prioritizing filler items
        #     excess = len(items) - max_total
        #     items = [item for item in items if item.name not in filler_items] + \
        #            [item for item in items if item.name in filler_items][:-excess]

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
            used_castlers = self.items_used[self.world.player].get("Castler", 0)
            used_chessmen = self.items_used[self.world.player].get("Chessmen", 0)
            used_material = self.items_used[self.world.player].get("Material", 0)
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
            - self.items_used[self.world.player].get("Chessmen", 0),
        )

    def initialize_remaining_geometry_unlocks(self) -> list[Item]:
        if self.world.options.goal.value == self.world.options.goal.option_single:
            return []
        items = []
        for name in ("Board Files", "Board Ranks"):
            remaining = item_table[name].quantity - self.items_used[self.world.player].get(name, 0)
            for _ in range(max(0, remaining)):
                self.consume_item(name, {})
                items.append(self.world.create_item(name))
        return items

    def initialize_item_tracking(self) -> None:
        """Initialize the item tracking dictionaries."""
        self.items_used[self.world.player] = {}
        self.items_remaining[self.world.player] = {}

    def initialize_required_items(self) -> list[Item]:
        """Initialize required items like Victory and Play as White."""
        items = []
        
        # Current-schema v2 uses independent geometry unlock items.
        if self.world.options.goal.value == self.world.options.goal.option_progressive:
            items.append(self.world.create_item("Board Files"))
            self.consume_item("Board Files", {})
            
        # Add Play as White
        items.append(self.world.create_item("Play as White"))
        self.items_used[self.world.player]["Play as White"] = 1
        
        return items

    def get_excluded_items(self) -> dict[str, int]:
        """Get items that should be excluded from the item pool."""
        excluded_items: dict[str, int] = {}

        # Handle super-sized items
        if self.world.options.goal.value == self.world.options.goal.option_super:
            item = self.world.create_item("Board Files")
            self.world.multiworld.push_precollected(item)
            # excluded_items["Super-Size Me"] = 1

        # Track precollected items
        raw_counts = Counter(
            item.name for item in self.world.multiworld.precollected_items[self.world.player]
        )
        excluded_items.update(self.normalize_counts(raw_counts))

        # TODO: Handle excluded_items_option if needed
        # excluded_items_option = getattr(multiworld, 'excluded_items', {player: []})
        # excluded_items.update(excluded_items_option[player].value)

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
            if item_name not in self.items_used[self.world.player]:
                self.items_used[self.world.player][item_name] = 0
            self.items_used[self.world.player][item_name] += excluded_items[item_name]
            starter_items.extend([self.world.create_item(item_name) for _ in range(excluded_items[item_name])])
        return starter_items

    def handle_option_limits(self) -> None:
        """Apply world options that limit the maximum copies of some items."""
        self.items_used[self.world.player]["Progressive Consul"] = (
            self.items_used[self.world.player].get("Progressive Consul", 0) +
            (3 - self.world.options.max_kings.value))
        self.items_used[self.world.player]["Progressive King Promotion"] = (
            self.items_used[self.world.player].get("Progressive King Promotion", 0) +
            (2 - self.world.options.fairy_kings.value))
        self.items_used[self.world.player]["Progressive AI Intelligence Malus"] = (
            self.items_used[self.world.player].get("Progressive AI Intelligence Malus", 0) +
            (5 - self.world.options.max_engine_penalties.value))
        self.items_used[self.world.player]["Progressive Pocket"] = (
            self.items_used[self.world.player].get("Progressive Pocket", 0) +
            (12 - min(self.world.options.max_pocket.value, 3 * self.world.options.pocket_limit_by_pocket.value)))

    def handle_locked_items(self) -> dict[str, int]:
        """Process locked items from options and ensure prerequisites are met."""
        # Get locked items from options
        yaml_locked_items: dict[str, int] = self.world.options.locked_items.value
        locked_items = self.normalize_counts(yaml_locked_items)
        maxima = mode_item_maxima(self.itemization)
        locked_items = {
            name: min(count, max(0, maxima.get(name, count) - self.items_used[self.world.player].get(name, 0)))
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
                    1
                    - self.items_used[self.world.player].get("Castler", 0),
                )
            total_castlers = (
                self.items_used[self.world.player].get("Castler", 0)
                + locked_items.get("Castler", 0)
            )
            required_chessmen = total_castlers
            required_material = math.ceil(total_castlers * 500 / item_table["Material"].material)
            locked_items["Chessmen"] = max(
                locked_items.get("Chessmen", 0),
                required_chessmen - self.items_used[self.world.player].get("Chessmen", 0),
            )
            locked_items["Material"] = max(
                locked_items.get("Material", 0),
                required_material - self.items_used[self.world.player].get("Material", 0),
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
        stage = BoardStage.Board12x12 if super_sized else BoardStage.Board8x8
        tactics_mode = (
            "none"
            if self.world.options.enable_tactics.value == self.world.options.enable_tactics.option_none
            else "turns"
            if self.world.options.enable_tactics.value == self.world.options.enable_tactics.option_turns
            else "all"
        )
        return len(location_names_for_stage(stage, tactics_mode))

    def create_progression_items(self,
                               max_items: int,
                               min_material: float = 4100,
                               max_material: float = 4600,
                               locked_items: dict[str, int] = {},
                               user_event_count: int = 0) -> list[Item]:
        """Create progression items up to material limits."""
        items = []
        material = self.calculate_current_material(items)
        my_progression_items = self.prepare_progression_item_pool()
        self.items_remaining[self.world.player] = {
            name: progression_items[name].quantity - self.items_used[self.world.player].get(name, 0) for name in my_progression_items}
        
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
                      " toward " + str(max_material) + " via items " + str(self.items_used[self.world.player]) +
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

    def create_useful_items(self, max_items: int, locked_items: dict[str, int] = {}, user_event_count: int = 0) -> list[Item]:
        """Create useful items."""
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

    def create_filler_items(self, has_pocket: bool, max_items: int, locked_items: dict[str, int] = {}, user_event_count: int = 0) -> list[Item]:
        """Create filler items up to max_items limit."""
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
            # should only ever == 0, but easier to test this way
            # TODO(chesslogic): copy this to check before and after if this impacts a decrementor property method or something wild
            if locked_items[item_name] <= 0:
                del locked_items[item_name]
            
        if item_name not in self.items_used[self.world.player]:
            self.items_used[self.world.player][item_name] = 0
        self.items_used[self.world.player][item_name] += 1

        if item_name in progression_items:
            if item_name not in self.items_remaining[self.world.player]:
                self.items_remaining[self.world.player][item_name] = progression_items[item_name].quantity
            self.items_remaining[self.world.player][item_name] -= 1

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

    def calculate_current_material(self, items: list[Item] = None) -> int:
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
            and item_name != "Progressive Pocket"
        )

    def calculate_remaining_material(self, locked_items: dict[str, int]) -> int:
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
        return self.items_used[self.world.player].get("Progressive Major To Queen", 0)

    def should_remove_item(self, chosen_item: str, material: int, min_material: float,
                           max_material: float, items: list[Item], my_progression_items: list[str],
                           locked_items: dict[str, int], user_event_count: int) -> bool:
        """Delegate item removal decision to ItemRemovalRules."""
        return self.removal_rules.should_remove_item(
            chosen_item, material, min_material, max_material,
            items, my_progression_items, locked_items, user_event_count)

    def chessmen_count(self, items: list[CMItem], pocket_limit: int) -> int:
        """Count the number of chessmen in the item pool."""
        pocket_amount = (0 if pocket_limit <= 0 else
                        math.ceil(len([item for item in items if item.name == "Progressive Pocket"]) / pocket_limit))
        chessmen_amount = (
            len([item for item in items if item.name == "Chessmen"])
            if self.is_fundamental
            else len([item for item in items if item.name in item_name_groups[LEGACY_CHESSMEN_GROUP]])
        )
        logging.debug("Found {} chessmen and {} pocket men".format(chessmen_amount, pocket_amount))
        return chessmen_amount + pocket_amount

    def lockable_material_value(self, chosen_item: str, items: list[CMItem], locked_items: dict[str, int]):
        '''if this piece was added, it might add more than its own material to the locked pool'''
        material = progression_items[chosen_item].material
        if self.world.options.accessibility.value == self.world.options.accessibility.option_minimal:
            return material
        if chosen_item == "Progressive Major To Queen" and self.material_model.unupgraded_majors_in_pool(items, locked_items) <= 2:
            material += progression_items["Progressive Major Piece"].material
        return material
