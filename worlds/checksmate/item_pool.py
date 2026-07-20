from collections import Counter
import logging

from BaseClasses import Item
from Options import OptionError

from .items import (
    GEOMETRY_ITEMS,
    INTERNAL_ITEMS,
    LEGACY_MATERIAL_ITEMS,
    ItemizationMode,
    filler_items,
    item_allowed_in_mode,
    item_table,
    itemization_mode,
    progression_items,
    useful_items,
)
from .item_utils import (
    castling_requirement,
    collection_item_maximum,
    generated_item_maximum,
    occupied_pockets,
    pocket_item_limit,
    required_castler_material_items,
)
from .locations import (
    highest_chessmen_requirement,
    highest_chessmen_requirement_small,
)
from .options import early_material_candidates
from .piece_model import PieceModel
from .material_model import MaterialModel
from .item_removal import ItemRemoval
from .pool_state import PoolAccounting, PoolCapacity


logger = logging.getLogger(__name__)


class CMItemPool:
    """Handles the creation and management of the item pool for ChecksMate."""

    def __init__(
        self,
        world,
        accounting: PoolAccounting | None = None,
        piece_model: PieceModel | None = None,
        material_model: MaterialModel | None = None,
    ) -> None:
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
        return self.itemization is ItemizationMode.FUNDAMENTAL

    @property
    def itemization(self) -> ItemizationMode:
        return itemization_mode(self.world.options)

    def normalize_counts(self, counts) -> dict[str, int]:
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
            maximum = generated_item_maximum(self.world, name)
            count = min(count, maximum)
            if count:
                normalized[name] = count
        return normalized

    def resolve_early_material_item(self) -> str | None:
        cached = getattr(self.world, "_early_material_item_name", None)
        if cached is not None:
            return cached

        candidates = early_material_candidates(self.world.options)
        if not candidates:
            self.world._early_material_item_name = None
            return None

        non_local_items = getattr(
            getattr(self.world.options, "non_local_items", None),
            "value",
            set(),
        )
        if getattr(self.world.multiworld, "players", None) == 1:
            non_local_items = set()
        else:
            local_items = getattr(
                getattr(self.world.options, "local_items", None),
                "value",
                set(),
            )
            local_early_items = getattr(
                self.world.multiworld,
                "local_early_items",
                {},
            ).get(self.world.player, {})
            non_local_items = (
                set(non_local_items)
                - set(local_items)
                - set(local_early_items)
            )
        available = tuple(
            name
            for name in candidates
            if name not in non_local_items
            and generated_item_maximum(self.world, name) > 0
        )
        if not available:
            requested = self.world.options.early_material.current_key
            raise OptionError(
                "ChecksMate Early Material "
                f"'{requested}' has no local candidate for the selected "
                "itemization and item options."
            )

        chosen = self.world.random.choice(available)
        self.world._early_material_item_name = chosen
        return chosen

    def validate_options(self) -> None:
        self.resolve_early_material_item()
        locked = dict(self.world.options.locked_items.value)
        from_pool = dict(
            getattr(
                self.world.options,
                "start_inventory_from_pool",
                {},
            ).value
            if hasattr(
                getattr(
                    self.world.options,
                    "start_inventory_from_pool",
                    None,
                ),
                "value",
            )
            else {}
        )

        self._validate_requested_items("Locked Items", locked, locked=True)
        self._validate_requested_items(
            "Start Inventory from Pool",
            from_pool,
            locked=False,
        )

        fixed, planned = self._minimum_pool_plan(locked, from_pool)
        for name, count in (fixed + planned).items():
            maximum = generated_item_maximum(self.world, name)
            if count > maximum:
                raise OptionError(
                    f"ChecksMate pool requirements need {count} '{name}' "
                    f"items, but the selected options support at most "
                    f"{maximum}."
                )

        super_sized = (
            self.world.options.goal.value
            != self.world.options.goal.option_single
        )
        reserved_locations = 1 + int(
            self.resolve_early_material_item() is not None
        )
        if (
            self.world.options.goal.value
            == self.world.options.goal.option_ordered_progressive
        ):
            reserved_locations += 4
        capacity = PoolCapacity.for_world(
            self.world,
            super_sized,
            reserved_locations=reserved_locations,
        ).item_limit
        required_slots = sum(planned.values())
        if required_slots > capacity:
            raise OptionError(
                "ChecksMate Locked Items and Start Inventory from Pool "
                f"require at least {required_slots} generated pool slots, "
                f"but only {capacity} are available after reserved "
                "locations."
            )

    def _validate_requested_items(
        self,
        option_name: str,
        requested: dict[str, int],
        *,
        locked: bool,
    ) -> None:
        fixed, mandatory = self._pool_profiles()
        from_pool = dict(
            getattr(
                getattr(
                    self.world.options,
                    "start_inventory_from_pool",
                    None,
                ),
                "value",
                {},
            )
        )
        for name, count in requested.items():
            if count < 0:
                raise OptionError(
                    f"ChecksMate {option_name}: '{name}' has negative count "
                    f"{count}; counts must be zero or greater."
                )
            if name not in item_table:
                raise OptionError(
                    f"ChecksMate {option_name}: '{name}' is not a valid "
                    "ChecksMate item."
                )
            if name in INTERNAL_ITEMS:
                raise OptionError(
                    f"ChecksMate {option_name}: '{name}' is an internal/event "
                    "item and cannot be requested from the generated pool."
                )
            if not locked and name == self.world.get_filler_item_name():
                raise OptionError(
                    f"ChecksMate {option_name}: '{name}' is the world's "
                    "replacement item and cannot be removed from the pool."
                )
            if not item_allowed_in_mode(name, self.itemization):
                raise OptionError(
                    f"ChecksMate {option_name}: '{name}' is unavailable with "
                    f"progression_itemization '{self.itemization.value}'."
                )
            if (
                name in GEOMETRY_ITEMS
                and self.world.options.goal.value
                == self.world.options.goal.option_single
            ):
                raise OptionError(
                    f"ChecksMate {option_name}: '{name}' is unavailable for "
                    "goal 'single'."
                )

            maximum = generated_item_maximum(self.world, name)
            if locked:
                from_pool_addition = max(
                    0,
                    from_pool.get(name, 0) - mandatory.get(name, 0),
                )
                maximum -= (
                    fixed.get(name, 0)
                    + mandatory.get(name, 0)
                    + from_pool_addition
                )
            else:
                maximum -= fixed.get(name, 0)
            maximum = max(0, maximum)
            if count > maximum:
                raise OptionError(
                    f"ChecksMate {option_name}: requested {count} '{name}', "
                    f"but at most {maximum} remain available with the "
                    "selected options."
                )

    def _pool_profiles(self) -> tuple[Counter[str], Counter[str]]:
        fixed: Counter[str] = Counter()
        mandatory: Counter[str] = Counter({"Play as White": 1})
        early_item = self.resolve_early_material_item()
        if early_item is not None:
            fixed[early_item] += 1

        goal = self.world.options.goal
        if goal.value == goal.option_ordered_progressive:
            fixed.update({"Board Files": 2, "Board Ranks": 2})
        elif goal.value == goal.option_progressive:
            mandatory.update({"Board Files": 2, "Board Ranks": 2})
        elif goal.value == goal.option_super:
            fixed["Board Files"] += 1
            mandatory.update({"Board Files": 1, "Board Ranks": 2})
        return fixed, mandatory

    def _minimum_pool_plan(
        self,
        locked: dict[str, int],
        from_pool: dict[str, int],
    ) -> tuple[Counter[str], Counter[str]]:
        fixed, planned = self._pool_profiles()
        for name, count in from_pool.items():
            planned[name] = max(planned[name], count)
        planned.update(locked)

        def total(name: str) -> int:
            return fixed[name] + planned[name]

        def ensure_total(name: str, target: int) -> None:
            planned[name] += max(0, target - total(name))

        start_inventory = getattr(
            getattr(
                self.world.options,
                "start_inventory",
                None,
            ),
            "value",
            {},
        )

        def starting_count(name: str) -> int:
            return min(
                max(0, int(start_inventory.get(name, 0))),
                collection_item_maximum(self.world.options, name),
            )

        def effective_total(name: str) -> int:
            return min(
                total(name) + starting_count(name),
                collection_item_maximum(self.world.options, name),
            )

        def ensure_effective_total(name: str, target: int) -> None:
            ensure_total(
                name,
                total(name) + max(0, target - effective_total(name)),
            )

        if self.is_fundamental:
            if (
                self.world.options.accessibility.value
                != self.world.options.accessibility.option_minimal
            ):
                ensure_effective_total(
                    "Castler",
                    castling_requirement(self.world.options),
                )
            total_castlers = effective_total("Castler")
            ensure_effective_total("Chessmen", total_castlers)
            ensure_effective_total(
                "Material",
                required_castler_material_items(total_castlers),
            )
            if (
                self.world.options.accessibility.value
                != self.world.options.accessibility.option_minimal
            ):
                pocket_chessmen = occupied_pockets(
                    effective_total("Progressive Pocket"),
                    self.world.options.pocket_limit_by_pocket.value,
                )
                ensure_effective_total(
                    "Chessmen",
                    max(
                        0,
                        (
                            highest_chessmen_requirement_small
                            if self.world.options.goal.value
                            == self.world.options.goal.option_single
                            else highest_chessmen_requirement
                        )
                        - pocket_chessmen,
                    ),
                )
        else:
            generated_queen_upgrades = total(
                "Progressive Major To Queen"
            )
            obtainable_queen_upgrades = min(
                generated_queen_upgrades
                + starting_count("Progressive Major To Queen"),
                collection_item_maximum(
                    self.world.options,
                    "Progressive Major To Queen",
                ),
            )
            ensure_effective_total(
                "Progressive Major Piece",
                obtainable_queen_upgrades,
            )
            if (
                self.world.options.accessibility.value
                != self.world.options.accessibility.option_minimal
            ):
                potential_castlers = (
                    effective_total("Progressive Major Piece")
                    + effective_total("Progressive Jack")
                )
                missing_castlers = max(
                    0,
                    obtainable_queen_upgrades
                    + castling_requirement(self.world.options)
                    - potential_castlers,
                )
                for name in (
                    "Progressive Major Piece",
                    "Progressive Jack",
                ):
                    capacity = max(
                        0,
                        min(
                            generated_item_maximum(self.world, name)
                            - total(name),
                            collection_item_maximum(
                                self.world.options,
                                name,
                            )
                            - effective_total(name),
                        ),
                    )
                    addition = min(missing_castlers, capacity)
                    planned[name] += addition
                    missing_castlers -= addition
                if missing_castlers:
                    raise OptionError(
                        "ChecksMate selected piece limits cannot provide "
                        "enough Majors or Jacks to keep castling obtainable "
                        "after every Queen upgrade."
                    )
        return fixed, planned

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
            and material_items
            >= required_castler_material_items(castlers + 1)
        )

    def create_items(self, reserved_locations: int = 1) -> list[Item]:
        super_sized = self.world.options.goal.value != self.world.options.goal.option_single
        self.validate_options()
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
        logger.debug(
            "Material requirements: min=%s, max=%s",
            min_material,
            max_material,
        )

        # Handle option limits
        self.handle_option_limits()

        # Process locked items and ensure prerequisites
        locked_items = self.handle_locked_items(Counter(
            item.name for item in items
        ))

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
        logger.debug(
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
        logger.debug("Created %s progression items", len(progression_items))

        # Create useful items with remaining space
        remaining_items = max_items - len(items)
        if remaining_items > 0:
            useful_items = self.create_useful_items(
                max_items=remaining_items,
                locked_items=locked_items,
            )
            items.extend(useful_items)
            logger.debug("Created %s useful items", len(useful_items))

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
            logger.debug("Created %s filler items", len(filler_items))

        # Add locked items
        for item in locked_items:
            self.accounting.add_used(item, locked_items[item])
            items.extend([self.world.create_item(item) for _ in range(locked_items[item])])

        return items

    def fit_locked_items(self, locked_items: dict[str, int], capacity: int) -> dict[str, int]:
        required = sum(locked_items.values())
        if required > capacity:
            raise OptionError(
                "ChecksMate pool requirements need "
                f"{required} additional items, but only {capacity} slots "
                "remain."
            )
        return dict(locked_items)

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
        """Account for world-owned precollected items, not user inventory."""
        if self.world.options.goal.value == self.world.options.goal.option_super:
            item = self.world.create_item("Board Files")
            self.world.multiworld.push_precollected(item)
            return {"Board Files": 1}
        return {}

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
        early_material_item = self.resolve_early_material_item()
        if early_material_item is not None:
            item = self.world.create_item(early_material_item)
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
            12 - pocket_item_limit(self.world.options),
        )

    def handle_locked_items(
        self,
        existing_pool_counts: Counter[str] | None = None,
    ) -> dict[str, int]:
        """Return additional items required by pool-origin options."""
        if existing_pool_counts is None:
            existing_pool_counts = Counter()
        locked = dict(self.world.options.locked_items.value)
        from_pool = dict(
            getattr(
                getattr(
                    self.world.options,
                    "start_inventory_from_pool",
                    None,
                ),
                "value",
                {},
            )
        )
        _, planned = self._minimum_pool_plan(locked, from_pool)
        additional = {
            name: count - existing_pool_counts.get(name, 0)
            for name, count in planned.items()
            if count > existing_pool_counts.get(name, 0)
        }
        remaining_material = sum(
            count * progression_items[name].material
            for name, count in additional.items()
            if name in progression_items
        )
        logger.debug(
            "%s pre-fill requires material %s via additional items %s",
            self.world.player,
            remaining_material,
            additional,
        )
        return additional

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
            
            if self.should_remove_item(
                chosen_item,
                material,
                max_material,
                items,
                my_progression_items,
                locked_items,
            ):
                my_progression_items.remove(chosen_item)
                continue
            
            if (self.has_prereqs(chosen_item, locked_items) and
                    self.piece_model.can_add_more(chosen_item)):
                try_item = self.world.create_item(chosen_item)
                self.consume_item(chosen_item, locked_items)
                items.append(try_item)
                material += (
                    0
                    if chosen_item == "Progressive Pocket"
                    else progression_items[chosen_item].material
                )
                
        all_material = sum([locked_items[item] * progression_items[item].material for item in locked_items if item in progression_items]) + material
        logger.debug(
            "%s granted total material %s toward %s via items %s, "
            "having generated %s",
            self.world.player,
            all_material,
            max_material,
            self.accounting.used,
            Counter(items),
        )
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

    def should_remove_item(
        self,
        chosen_item: str,
        material: int,
        max_material: float,
        items: list[Item],
        my_progression_items: list[str],
        locked_items: dict[str, int],
    ) -> bool:
        """Delegate item removal decision to ItemRemovalRules."""
        return self.removal_rules.should_remove_item(
            chosen_item,
            material,
            max_material,
            items,
            my_progression_items,
            locked_items,
        )
