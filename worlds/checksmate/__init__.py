import logging
from collections import Counter
from typing import List, Dict, ClassVar, Type, Optional

from BaseClasses import Tutorial, Region, MultiWorld, Item, CollectionState
from Options import PerGameCommonOptions
from worlds.AutoWorld import WebWorld, World

from .Options import CMOptions
from .Items import CMItem, item_table, item_name_groups
from .Locations import CMLocation, location_table, Tactic
from .Presets import checksmate_option_presets
from .Rules import set_rules
from .CollectionState import CMCollectionState
from .ItemPool import CMItemPool
from .PieceModel import PieceModel
from .MaterialModel import MaterialModel


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
    data_version = 0
    web = CMWeb()
    required_client_version = (0, 2, 11)
    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = CMOptions
    options: CMOptions

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}
    locked_locations: List[str]

    item_name_groups = item_name_groups
    items_used: Dict[int, Dict[str, int]] = {}
    items_remaining: Dict[int, Dict[str, int]] = {}
    armies: Dict[int, List[int]] = {}

    item_pool: List[CMItem] = []
    prefill_items: List[CMItem] = []

    piece_types_by_army: Dict[int, Dict[str, int]] = {
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


    def generate_early(self) -> None:
        piece_collection = self.options.fairy_chess_pieces.value
        army_options = []
        if piece_collection == self.options.fairy_chess_pieces.option_fide:
            army_options = [0]
        elif piece_collection == self.options.fairy_chess_pieces.option_betza:
            army_options = [0, 1, 2, 3]
        elif piece_collection == self.options.fairy_chess_pieces.option_full:
            army_options = [0, 1, 2, 3, 4, 5]
        elif piece_collection == self.options.fairy_chess_pieces.option_configure:
            which_pieces = self.options.fairy_chess_pieces_configure
            if (which_pieces.value is None or which_pieces.value == 'None' or
                    None in which_pieces.value or 'None' in which_pieces.value):
                raise Exception(
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
            if not army_options:
                army_options = [0]

        army_constraint = self.options.fairy_chess_army
        if army_constraint != self.options.fairy_chess_army.option_chaos:
            self.armies[self.player] = [self.random.choice(army_options)]
        else:
            self.armies[self.player] = army_options

    def fill_slot_data(self) -> dict:
        cursed_knowledge = {name: self.random.getrandbits(31) for name in [
            "pocket_seed", "pawn_seed", "minor_seed", "major_seed", "queen_seed"]}
        potential_pockets = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2]
        self.random.shuffle(potential_pockets)
        cursed_knowledge["pocket_order"] = potential_pockets
        cursed_knowledge["total_queens"] = self.items_used[self.player].get("Progressive Major To Queen", 0)
        if self.player in self.armies:
            cursed_knowledge["army"] = self.armies[self.player]
        option_names = ["goal", "death_link", "difficulty", "piece_locations", "piece_types",
                        "fairy_chess_army", "fairy_chess_pieces", "fairy_chess_pieces_configure", "fairy_chess_pawns",
                        "minor_piece_limit_by_type", "major_piece_limit_by_type", "queen_piece_limit_by_type",
                        "pocket_limit_by_pocket"]
        return dict(cursed_knowledge, **self.options.as_dict(*option_names))

    def create_item(self, name: str) -> CMItem:
        data = item_table[name]
        return CMItem(name, data.classification, data.code, self.player)

    def set_rules(self) -> None:
        set_rules(self)

    def create_items(self) -> None:
        super_sized = self.options.goal.value != self.options.goal.option_single
        self._item_pool.initialize_item_tracking()

        # Handle excluded items and starter items
        excluded_items = self._item_pool.get_excluded_items()
        starter_items = self._item_pool.assign_starter_items(excluded_items, self.locked_locations)
        self._item_pool.handle_excluded_items(excluded_items)
        user_location_count = len(starter_items)

        # Calculate material requirements
        min_material, max_material = self._material_model.calculate_material_requirements(super_sized)
        logging.debug(f"Material requirements: min={min_material}, max={max_material}")

        # Handle option limits
        self._item_pool.handle_option_limits()

        # Calculate max items
        max_items = self._item_pool.get_max_items(super_sized)
        logging.debug(f"Max items: {max_items}")

        # Create progression items
        items = self._item_pool.create_progression_items(
            max_items=max_items,
            min_material=min_material,
            max_material=max_material,
            user_location_count=user_location_count
        )
        logging.debug(f"Created {len(items)} progression items")

        # Create useful items
        items.extend(self._item_pool.create_useful_items(
            max_items=max_items,
            user_location_count=user_location_count
        ))

        # Check for pocket items
        has_pocket = any("Pocket" in item.name for item in items)

        # Create filler items
        items.extend(self._item_pool.create_filler_items(
            has_pocket=has_pocket,
            max_items=max_items,
            user_location_count=user_location_count
        ))

        self.multiworld.itempool += items

    def create_regions(self) -> None:
        region = Region("Menu", self.player, self.multiworld)
        super_sized = self.options.goal.value != self.options.goal.option_single

        for loc_name in location_table:
            loc_data = location_table[loc_name]
            if not super_sized and loc_data.material_expectations == -1:
                continue
            if loc_data.is_tactic is not None:
                if self.options.enable_tactics.value == self.options.enable_tactics.option_none:
                    continue
                elif self.options.enable_tactics.value == self.options.enable_tactics.option_turns and \
                        loc_data.is_tactic == Tactic.Fork:
                    continue
            region.locations.append(CMLocation(self.player, loc_name, loc_data.code, region))

        self.multiworld.regions.append(region)

    def generate_basic(self) -> None:
        if self.options.goal.value == self.options.goal.option_single:
            victory_item = self.create_item("Victory")
            self.multiworld.get_location("Checkmate Minima", self.player).place_locked_item(victory_item)
        else:
            victory_item = self.create_item("Victory")
            self.multiworld.get_location("Checkmate Maxima", self.player).place_locked_item(victory_item)

    def collect(self, state: CollectionState, item: Item) -> bool:
        return self._collection_state.collect(state, item)

    def remove(self, state: CollectionState, item: Item) -> bool:
        return self._collection_state.remove(state, item)
