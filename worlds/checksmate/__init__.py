from collections import Counter
from collections.abc import Mapping
import random
from typing import ClassVar, Type

from BaseClasses import Tutorial, Region, MultiWorld, Item, CollectionState
from Options import PerGameCommonOptions, OptionError
from worlds.AutoWorld import WebWorld, World

from .options import CMOptions, resolve_piece_upgrade_preferences, resolve_piece_upgrade_ratio
from .items import (
    CMItem,
    ItemizationMode,
    item_table,
    item_name_groups,
    itemization_mode,
)
from .contract_resource import (
    UNLOCK_ITEM_ROLES,
    load_production_contract,
    production_contract_document,
)
from .locations import (
    BoardStage,
    CMLocation,
    location_names_for_stage,
    location_table,
    tactics_mode_for_options,
)
from .presets import checksmate_option_presets
from .rules import set_rules
from .collection_state import CMCollectionState
from .item_pool import CMItemPool
from .piece_limit_cascade import PieceLimitCascade
from .pool_state import PoolAccounting
from .logic_projection import WorldLogicProjection
from .semantic_projection import SemanticSeeds
from .item_utils import collection_item_maximum


_SEMANTIC_SEED_NAMES = (
    "pocket_seed",
    "pawn_seed",
    "minor_seed",
    "major_seed",
    "queen_seed",
)


class CMWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the ChecksMate software on your computer. This guide covers single-player, "
        "multiworld, and related software.",
        "English",
        "checksmate_en.md",
        "checks-mate/en",
        ["roty", "rft50"]
    )]

    options_presets = checksmate_option_presets


class CMWorld(World):
    """
    ChecksMate is a game where you play chess, but all of your pieces were scattered across the multiworld.
    You win when you checkmate the opposing king!
    """
    game: ClassVar[str] = "ChecksMate"
    web = CMWeb()
    required_chess_client_version = "0.4.0"
    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = CMOptions
    options: CMOptions

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}
    locked_locations: list[str]

    item_name_groups = item_name_groups
    piece_types_by_army: ClassVar[dict[int, dict[str, int]]] = {
        # Vanilla
        0: {"Progressive Minor Piece": 2, "Progressive Major Piece": 1, "Progressive Major To Queen": 1},
        # Colorbound Clobberers (the War Elephant is rather powerful)
        1: {"Progressive Minor Piece": 1, "Progressive Major Piece": 2, "Progressive Major To Queen": 1},
        # Remarkable Rookies
        2: {"Progressive Minor Piece": 2, "Progressive Major Piece": 1, "Progressive Major To Queen": 1},
        # Nutty Knights (although the Short Rook and Half Duck swap potency)
        3: {"Progressive Minor Piece": 2, "Progressive Major Piece": 1, "Progressive Major To Queen": 1},
        # Eurasian pieces
        4: {"Progressive Minor Piece": 2, "Progressive Major Piece": 1, "Progressive Major To Queen": 1},
        # Camel pieces
        5: {"Progressive Minor Piece": 2, "Progressive Major Piece": 1, "Progressive Major To Queen": 1},
        # Petal pieces
        6: {"Progressive Minor Piece": 2, "Progressive Major Piece": 1, "Progressive Major To Queen": 1},
    }

    def __init__(self, multiworld: MultiWorld, player: int) -> None:
        super(CMWorld, self).__init__(multiworld, player)
        self.locked_locations = []
        self.army_ids: list[int] = []
        self.pool_accounting = PoolAccounting()
        self._item_pool = CMItemPool(self, accounting=self.pool_accounting)
        self._collection_state = CMCollectionState(self)
        self._logic_projection: WorldLogicProjection | None = None
        self._logic_obtainable_counts: dict[str, int] | None = None
        self._semantic_seed_values: dict[str, int] | None = None
        self._pocket_order: tuple[int, ...] | None = None
        self._early_material_item_name: str | None = None

    def generate_early(self) -> None:
        self._ensure_semantic_seeds()
        if (
            self.options.fairy_chess_pawns.value
            == self.options.fairy_chess_pawns.option_reserved
        ):
            raise OptionError(
                "ChecksMate Fairy Chess Pawns 'reserved' is not implemented; "
                "choose a supported named value."
            )
        piece_collection = self.options.fairy_chess_pieces.value
        army_options = []
        if piece_collection == self.options.fairy_chess_pieces.option_fide:
            army_options = [0]
        elif piece_collection == self.options.fairy_chess_pieces.option_betza:
            army_options = [0, 1, 2, 3]
        elif piece_collection == self.options.fairy_chess_pieces.option_full:
            army_options = [0, 1, 2, 3, 4, 5, 6]
        elif piece_collection == self.options.fairy_chess_pieces.option_configure:
            which_pieces = self.options.fairy_chess_pieces_configure
            if (which_pieces.value is None or which_pieces.value == 'None' or
                    None in which_pieces.value or 'None' in which_pieces.value):
                raise OptionError(
                    "This ChecksMate YAML is invalid! Add text after fairy_chess_piece_collection_configure.")
            if "FIDE" in which_pieces.value:
                army_options += [0]
            if "Clobberers" in which_pieces.value:
                army_options += [1]
            if "Rookies" in which_pieces.value:
                army_options += [2]
            if "Nutty" in which_pieces.value:
                army_options += [3]
            if "Cannon" in which_pieces.value:
                army_options += [4]
            if "Camel" in which_pieces.value:
                army_options += [5]
            if "Petal" in which_pieces.value:
                army_options += [6]
            if not army_options:
                army_options = [0]

        army_constraint = self.options.fairy_chess_army
        if army_constraint != self.options.fairy_chess_army.option_chaos:
            self.army_ids = [self.random.choice(army_options)]
        else:
            self.army_ids = army_options
        self._item_pool.validate_options()

    def fill_slot_data(self) -> dict:
        contract = load_production_contract()
        self._ensure_semantic_seeds()
        cursed_knowledge = dict(self._semantic_seed_values)
        cursed_knowledge["pocket_order"] = self._stable_pocket_order()
        cursed_knowledge["total_queens"] = (
            self._total_obtainable_queen_upgrades()
        )
        logic_obtainable_counts = (
            self._tracker_logic_obtainable_counts()
            or self._logic_obtainable_counts
        )
        if logic_obtainable_counts is not None:
            cursed_knowledge["logic_obtainable_counts"] = dict(
                logic_obtainable_counts
            )
        cursed_knowledge["required_chess_client_version"] = self.required_chess_client_version
        cursed_knowledge["apmw_contract"] = production_contract_document()
        cursed_knowledge["material_item_value"] = contract.expected_material["material_item"]
        cursed_knowledge["castling_location_count"] = contract.castler.maximum
        cursed_knowledge["geometry_unlock_items"] = dict(UNLOCK_ITEM_ROLES)
        if self.army_ids:
            cursed_knowledge["army"] = list(self.army_ids)
        option_names = ["goal", "death_link", "difficulty", "enable_tactics", "piece_locations", "piece_types",
                        "fairy_chess_army", "fairy_chess_pieces", "fairy_chess_pieces_configure", "fairy_chess_pawns", "fairy_chess_pawn_upgrades",
                        "max_pocket", "piece_upgrade_priority",
                        "minor_piece_limit_by_type", "major_piece_limit_by_type", "queen_piece_limit_by_type",
                        "pocket_limit_by_pocket", "fair_board_guarantee"]
        slot_options = self.options.as_dict(*option_names)
        slot_options["progression_itemization"] = itemization_mode(
            self.options
        ).value
        upgrade_preferences = resolve_piece_upgrade_preferences(
            self.options.fairy_chess_pawn_upgrades, self.options.piece_upgrade_preferences,
            self.options.piece_upgrade_priority)
        if (
            itemization_mode(self.options) is ItemizationMode.FUNDAMENTAL
            and not self.options.piece_upgrade_priority.value
            and self.options.fairy_chess_pawn_upgrades.value
            != self.options.fairy_chess_pawn_upgrades.option_configure
        ):
            upgrade_preferences = []
        slot_options["piece_upgrade_preferences"] = upgrade_preferences
        slot_options["piece_upgrade_priority"] = dict(
            self.options.piece_upgrade_priority.value
        )
        slot_options["piece_upgrade_ratio"] = resolve_piece_upgrade_ratio(self.options.piece_upgrade_ratio)
        return dict(cursed_knowledge, **slot_options)

    @staticmethod
    def interpret_slot_data(slot_data: dict) -> dict:
        """Preserve generated values required for Universal Tracker rules."""
        return slot_data

    def create_item(self, name: str) -> CMItem:
        data = item_table[name]
        return CMItem(name, data.classification, data.code, self.player)

    def set_rules(self) -> None:
        set_rules(self)

    def create_items(self) -> None:
        self._place_victory()
        items = self._item_pool.create_items(reserved_locations=1)
        self.multiworld.itempool += items
        obtainable = Counter(item.name for item in items)
        obtainable.update(self.options.start_inventory.value)
        obtainable.update(
            location.item.name
            for location in self.multiworld.get_locations(self.player)
            if location.locked and location.item is not None
        )
        self._set_logic_obtainable_counts(obtainable)

    def create_regions(self) -> None:
        region = Region("Menu", self.player, self.multiworld)
        super_sized = self.options.goal.value != self.options.goal.option_single
        stage = BoardStage.Board12x12 if super_sized else BoardStage.Board8x8
        tactics_mode = tactics_mode_for_options(self.options)

        for loc_name in location_names_for_stage(stage, tactics_mode):
            loc_data = location_table[loc_name]
            region.locations.append(CMLocation(self.player, loc_name, loc_data.code, region))

        self.multiworld.regions.append(region)

    def generate_basic(self) -> None:
        """All item placement is completed during create_items."""

    def collect(self, state: CollectionState, item: Item) -> bool:
        """Collect an effective item and retain removable excess copies."""
        if not self._collection_state.is_effective_collection(state, item):
            self._collection_state.record_excess_collection(state, item)
            return False
        return super().collect(state, item)

    def remove(self, state: CollectionState, item: Item) -> bool:
        """Remove excess copies before effective AP progression."""
        if self._collection_state.remove_excess_collection(state, item):
            return False
        return super().remove(state, item)

    def get_filler_item_name(self) -> str:
        return "Progressive Pocket Gems"

    def find_piece_limit(self, piece_name: str, cascade_type: PieceLimitCascade) -> int:
        """Delegate piece limit finding to the PieceModel."""
        return self._item_pool.piece_model.find_piece_limit(piece_name, cascade_type)

    @property
    def items_used(self) -> dict[int, dict[str, int]]:
        """Compatibility view for legacy callers that still expect a player key."""
        return self.pool_accounting.used_player_view(self.player)

    @property
    def items_remaining(self) -> dict[int, dict[str, int]]:
        """Compatibility view for legacy callers that still expect a player key."""
        return self.pool_accounting.remaining_player_view(self.player)

    @property
    def logic_projection(self) -> WorldLogicProjection:
        if self._logic_projection is None:
            self._ensure_semantic_seeds()
            seeds = SemanticSeeds(**{
                name: str(value)
                for name, value in self._semantic_seed_values.items()
            })
            self._logic_projection = WorldLogicProjection(self.options, seeds)
            self._apply_tracker_projection_overrides(self._logic_projection)
        return self._logic_projection

    def _total_obtainable_queen_upgrades(self) -> int:
        tracker_total = self._tracker_total_queen_upgrades()
        if tracker_total is not None:
            return tracker_total
        return min(
            (
                self.pool_accounting.used_count("Progressive Major To Queen")
                + self.options.start_inventory.value.get(
                    "Progressive Major To Queen",
                    0,
                )
            ),
            collection_item_maximum(
                self.options,
                "Progressive Major To Queen",
            ),
        )

    def _set_logic_obtainable_counts(
        self,
        counts: Mapping[str, int],
    ) -> None:
        projection = self.logic_projection
        projection.set_obtainable_counts(counts)
        self._apply_tracker_projection_overrides(projection)
        self._logic_obtainable_counts = projection.obtainable_counts()

    def _apply_tracker_projection_overrides(
        self,
        projection: WorldLogicProjection,
    ) -> None:
        tracker_counts = self._tracker_logic_obtainable_counts()
        if tracker_counts is not None:
            projection.set_obtainable_counts(tracker_counts)
            return
        tracker_total_queens = self._tracker_total_queen_upgrades()
        if (
            projection.itemization is ItemizationMode.LEGACY
            and tracker_total_queens is not None
        ):
            projection.set_obtainable_count(
                "Progressive Major To Queen",
                tracker_total_queens,
            )

    def _tracker_logic_obtainable_counts(self) -> dict[str, int] | None:
        slot_data = self._tracker_slot_data()
        if slot_data is None:
            return None
        counts = slot_data.get("logic_obtainable_counts")
        if counts is None:
            return None
        if not isinstance(counts, dict):
            raise ValueError(
                "ChecksMate slot data logic_obtainable_counts must be a mapping"
            )
        normalized = {}
        for name, count in counts.items():
            if (
                not isinstance(name, str)
                or name not in item_table
                or not isinstance(count, int)
                or isinstance(count, bool)
                or count < 0
            ):
                raise ValueError(
                    "ChecksMate slot data logic_obtainable_counts must contain "
                    "known item names with non-negative integer counts"
                )
            normalized[name] = count
        return normalized

    def _tracker_total_queen_upgrades(self) -> int | None:
        slot_data = self._tracker_slot_data()
        if slot_data is None:
            return None
        total_queens = slot_data.get("total_queens")
        if total_queens is None:
            return None
        if (
            not isinstance(total_queens, int)
            or isinstance(total_queens, bool)
            or total_queens < 0
        ):
            raise ValueError(
                "ChecksMate slot data total_queens must be a non-negative integer"
            )
        return total_queens

    def _tracker_semantic_seeds(self) -> dict[str, int] | None:
        slot_data = self._tracker_slot_data()
        if slot_data is None:
            return None
        present = tuple(name in slot_data for name in _SEMANTIC_SEED_NAMES)
        if not any(present):
            return None
        if not all(present):
            raise ValueError(
                "ChecksMate slot data must include every semantic projection seed"
            )
        seeds = {}
        for name in _SEMANTIC_SEED_NAMES:
            value = slot_data[name]
            if (
                not isinstance(value, int)
                or isinstance(value, bool)
                or not 0 <= value < 2 ** 31
            ):
                raise ValueError(
                    f"ChecksMate slot data {name} must be a 31-bit "
                    "non-negative integer"
                )
            seeds[name] = value
        return seeds

    def _tracker_slot_data(self) -> dict | None:
        passthrough = getattr(self.multiworld, "re_gen_passthrough", None)
        if not isinstance(passthrough, dict):
            return None
        slot_data = passthrough.get(self.game)
        return slot_data if isinstance(slot_data, dict) else None

    def _ensure_semantic_seeds(self) -> None:
        if self._semantic_seed_values is not None:
            return
        tracker_seeds = self._tracker_semantic_seeds()
        if tracker_seeds is not None:
            self._semantic_seed_values = tracker_seeds
            return
        probe = random.Random()
        probe.setstate(self.random.getstate())
        self._semantic_seed_values = {
            name: probe.getrandbits(31)
            for name in _SEMANTIC_SEED_NAMES
        }

    def _stable_pocket_order(self) -> list[int]:
        self._ensure_semantic_seeds()
        if self._pocket_order is None:
            pocket_random = random.Random(
                self._semantic_seed_values["pocket_seed"]
            )
            pocket_order = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2]
            pocket_random.shuffle(pocket_order)
            self._pocket_order = tuple(pocket_order)
        return list(self._pocket_order)

    def _place_victory(self) -> None:
        location_name = (
            "Checkmate Minima"
            if self.options.goal.value == self.options.goal.option_single
            else "Checkmate 12x12"
        )
        location = self.multiworld.get_location(location_name, self.player)
        if location.item is None:
            location.place_locked_item(self.create_item("Victory"))
        elif location.item.name != "Victory":
            raise RuntimeError(
                f"{location_name} is already occupied before Victory placement"
            )
