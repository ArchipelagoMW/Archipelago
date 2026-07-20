from collections import Counter
import random
from typing import ClassVar, Type

from BaseClasses import Tutorial, Region, MultiWorld, Item, CollectionState
from Options import PerGameCommonOptions, OptionError
from worlds.AutoWorld import WebWorld, World

from .options import CMOptions, resolve_piece_upgrade_preferences, resolve_piece_upgrade_ratio
from .items import MATERIAL_TOTAL_KEY, CMItem, item_table, item_name_groups
from .contract_resource import (
    UNLOCK_ITEM_ROLES,
    load_production_contract,
    production_contract_document,
)
from .locations import BoardStage, CMLocation, location_names_for_stage, location_table
from .presets import checksmate_option_presets
from .rules import set_rules
from .collection_state import CMCollectionState
from .item_pool import CMItemPool
from .piece_model import PieceModel, PieceLimitCascade
from .material_model import MaterialModel
from .logic_projection import WorldLogicProjection
from .semantic_projection import SemanticSeeds


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
    items_used: ClassVar[dict[int, dict[str, int]]] = {}
    items_remaining: ClassVar[dict[int, dict[str, int]]] = {}
    armies: ClassVar[dict[int, list[int]]] = {}

    item_pool: list[CMItem] = []
    prefill_items: list[CMItem] = []

    piece_types_by_army: dict[int, dict[str, int]] = {
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
        self.items_used = {}
        self.items_remaining = {}
        self._item_pool = CMItemPool(self)
        self._item_pool.items_used = self.items_used
        self._piece_model = PieceModel(self)
        self._piece_model.items_used = self.items_used
        self._material_model = MaterialModel(self)
        self._material_model.items_used = self.items_used
        self._collection_state = CMCollectionState(self)
        self._logic_projection: WorldLogicProjection | None = None
        self._semantic_seed_values: dict[str, int] | None = None


    def generate_early(self) -> None:
        self._ensure_semantic_seeds()
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
            self.armies[self.player] = [self.random.choice(army_options)]
        else:
            self.armies[self.player] = army_options

    def fill_slot_data(self) -> dict:
        contract = load_production_contract()
        self._ensure_semantic_seeds()
        cursed_knowledge = dict(self._semantic_seed_values)
        potential_pockets = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2]
        self.random.shuffle(potential_pockets)
        cursed_knowledge["pocket_order"] = potential_pockets
        cursed_knowledge["total_queens"] = self.items_used[self.player].get("Progressive Major To Queen", 0)
        cursed_knowledge["required_chess_client_version"] = self.required_chess_client_version
        cursed_knowledge["apmw_contract"] = production_contract_document()
        cursed_knowledge["material_item_value"] = contract.expected_material["material_item"]
        cursed_knowledge["castling_location_count"] = contract.castler.maximum
        cursed_knowledge["geometry_unlock_items"] = dict(UNLOCK_ITEM_ROLES)
        if self.player in self.armies:
            cursed_knowledge["army"] = self.armies[self.player]
        option_names = ["goal", "death_link", "difficulty", "piece_locations", "piece_types",
                        "fairy_chess_army", "fairy_chess_pieces", "fairy_chess_pieces_configure", "fairy_chess_pawns", "fairy_chess_pawn_upgrades",
                        "minor_piece_limit_by_type", "major_piece_limit_by_type", "queen_piece_limit_by_type",
                        "pocket_limit_by_pocket", "fair_board_guarantee"]
        slot_options = self.options.as_dict(*option_names)
        slot_options["progression_itemization"] = (
            "fundamental"
            if self.options.progression_itemization.value
            == self.options.progression_itemization.option_fundamental
            else "legacy"
        )
        upgrade_preferences = resolve_piece_upgrade_preferences(
            self.options.fairy_chess_pawn_upgrades, self.options.piece_upgrade_preferences,
            self.options.piece_upgrade_priority)
        if (
            self.options.progression_itemization.value
            == self.options.progression_itemization.option_fundamental
            and not self.options.piece_upgrade_priority.value
            and self.options.fairy_chess_pawn_upgrades.value
            != self.options.fairy_chess_pawn_upgrades.option_configure
        ):
            upgrade_preferences = []
        slot_options["piece_upgrade_preferences"] = upgrade_preferences
        slot_options["piece_upgrade_ratio"] = resolve_piece_upgrade_ratio(self.options.piece_upgrade_ratio)
        return dict(cursed_knowledge, **slot_options)

    def create_item(self, name: str) -> CMItem:
        data = item_table[name]
        return CMItem(name, data.classification, data.code, self.player)

    def set_rules(self) -> None:
        set_rules(self)

    def create_items(self) -> None:
        items = self._item_pool.create_items()
        self.multiworld.itempool += items
        obtainable = Counter(item.name for item in items)
        obtainable.update(
            item.name
            for item in self.multiworld.precollected_items[self.player]
        )
        obtainable.update(
            location.item.name
            for location in self.multiworld.get_locations(self.player)
            if location.locked and location.item is not None
        )
        self.logic_projection.set_obtainable_counts(obtainable)

    def create_regions(self) -> None:
        region = Region("Menu", self.player, self.multiworld)
        super_sized = self.options.goal.value != self.options.goal.option_single
        stage = BoardStage.Board12x12 if super_sized else BoardStage.Board8x8
        tactics_mode = (
            "none"
            if self.options.enable_tactics.value == self.options.enable_tactics.option_none
            else "turns"
            if self.options.enable_tactics.value == self.options.enable_tactics.option_turns
            else "all"
        )

        for loc_name in location_names_for_stage(stage, tactics_mode):
            loc_data = location_table[loc_name]
            region.locations.append(CMLocation(self.player, loc_name, loc_data.code, region))

        self.multiworld.regions.append(region)

    def generate_basic(self) -> None:
        if self.options.goal.value == self.options.goal.option_single:
            victory_item = self.create_item("Victory")
            self.multiworld.get_location("Checkmate Minima", self.player).place_locked_item(victory_item)
        else:
            victory_item = self.create_item("Victory")
            self.multiworld.get_location("Checkmate 12x12", self.player).place_locked_item(victory_item)

    def collect(self, state: CollectionState, item: Item) -> bool:
        """Collect an item and update material value."""
        if not self._collection_state.is_effective_collection(state, item):
            self._collection_state.record_excess_collection(state, item)
            return False
        # Calculate material value before state change
        material = self._collection_state.collect(state, item)

        # Update state through parent class
        change = super().collect(state, item)
        if change:
            # we actually collected the item, so we must gain the material
            state.prog_items[self.player][MATERIAL_TOTAL_KEY] += material

        return change

    def remove(self, state: CollectionState, item: Item) -> bool:
        """Remove an item and update material value."""
        if self._collection_state.remove_excess_collection(state, item):
            return False

        # Calculate material value before state change
        material = self._collection_state.remove(state, item)

        # Update state through parent class
        change = super().remove(state, item)
        if change:
            # we actually removed the item, so we must lose the material
            state.prog_items[self.player][MATERIAL_TOTAL_KEY] -= material

        return change

    def find_piece_limit(self, piece_name: str, cascade_type: PieceLimitCascade) -> int:
        """Delegate piece limit finding to the PieceModel."""
        return self._piece_model.find_piece_limit(piece_name, cascade_type)

    @property
    def logic_projection(self) -> WorldLogicProjection:
        if self._logic_projection is None:
            self._ensure_semantic_seeds()
            seeds = SemanticSeeds(**{
                name: str(value)
                for name, value in self._semantic_seed_values.items()
            })
            self._logic_projection = WorldLogicProjection(self.options, seeds)
        return self._logic_projection

    def _ensure_semantic_seeds(self) -> None:
        if self._semantic_seed_values is not None:
            return
        probe = random.Random()
        probe.setstate(self.random.getstate())
        self._semantic_seed_values = {
            name: probe.getrandbits(31)
            for name in (
                "pocket_seed",
                "pawn_seed",
                "minor_seed",
                "major_seed",
                "queen_seed",
            )
        }
