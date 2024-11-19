import logging
import math
from collections import Counter
from enum import Enum
from typing import List, Dict, ClassVar, Callable, Type, Union

from BaseClasses import Tutorial, Region, MultiWorld, Item, CollectionState
from Options import PerGameCommonOptions
from worlds.AutoWorld import WebWorld, World
from .Options import CMOptions, piece_type_limit_options, piece_limit_options
from .Items import (CMItem, item_table, filler_items, progression_items,
                    useful_items, item_name_groups, CMItemData)
from .Locations import CMLocation, location_table, highest_chessmen_requirement_small, highest_chessmen_requirement, \
    Tactic
from .Presets import checksmate_option_presets
from .Rules import set_rules, determine_difficulty, determine_relaxation, determine_min_material, determine_max_material


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

    known_pieces = {"Progressive Minor Piece": 10, "Progressive Major Piece": 6, "Progressive Major To Queen": 6, }

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

    # TODO: this probably can go in some other method now??
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
            # TODO: I am not ok with this
            if (which_pieces.value is None or which_pieces.value == 'None' or
                    None in which_pieces.value or 'None' in which_pieces.value):
                raise Exception(
                    "This ChecksMate YAML is invalid! Add text after fairy_chess_piece_collection_configure.")
            # FIDE: Contains the standard chess pieces, consisting of the Bishop, Knight, Rook, and Queen.
            if "FIDE" in which_pieces.value:
                army_options += [0]
            # CwDA: Adds the pieces from Ralph Betza's 12 Chess With Different Armies.
            if "Clobberers" in which_pieces.value:
                army_options += [1]
            if "Rookies" in which_pieces.value:
                army_options += [2]
            if "Nutty" in which_pieces.value:
                army_options += [3]
            # Cannon: Adds the Rook-like Cannon, which captures a distal chessman by leaping over an intervening
            # chessman, and the Vao, a Bishop-like Cannon, in that it moves and captures diagonally.
            if "Cannon" in which_pieces.value:
                army_options += [4]
            # Camel: Adds a custom army themed after 3,x leapers like the Camel (3,1) and Tribbabah (3,0).
            if "Camel" in which_pieces.value:
                army_options += [5]
            # An empty set disables fairy chess pieces completely.
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
        # See Archipelago.APChessV.ApmwConfig#Instantiate to observe requested parameters
        option_names = ["goal", "difficulty", "piece_locations", "piece_types",
                        "fairy_chess_army", "fairy_chess_pieces", "fairy_chess_pieces_configure", "fairy_chess_pawns",
                        "minor_piece_limit_by_type", "major_piece_limit_by_type", "queen_piece_limit_by_type",
                        "pocket_limit_by_pocket"]
        return dict(cursed_knowledge, **self.options.as_dict(*option_names))

    def create_item(self, name: str) -> CMItem:
        data = item_table[name]
        return CMItem(name, data.classification, data.code, self.player)

    def set_rules(self) -> None:
        set_rules(self.multiworld, self.player, self.options)

    def create_items(self) -> None:
        super_sized = self.options.goal.value != self.options.goal.option_single
        # for enemy_pawn in self.item_name_groups["Enemy Pawn"]:
        #     self.multiworld.push_precollected(self.create_item(enemy_pawn))
        # for enemy_piece in self.item_name_groups["Enemy Piece"]:
        #     self.multiworld.push_precollected(self.create_item(enemy_piece))

        # TODO: limit total material
        # items = [[self.create_item(item) for _ in range(item_data.quantity)]
        #                             for item, item_data in progression_items]
        excluded_items = self.get_excluded_items()
        self.items_used[self.player] = {}
        self.items_remaining[self.player] = {}

        # setup for starting_inventory generic collection and then for early_material custom option
        for item_name in excluded_items:
            if item_name not in self.items_used[self.player]:
                self.items_used[self.player][item_name] = 0
            self.items_used[self.player][item_name] += excluded_items[item_name]
        starter_items = self.assign_starter_items(excluded_items, self.locked_locations)
        for item in starter_items:
            self.consume_item(item.name, {})

        # determine how many items we need to add to the custom item_pool
        user_location_count = len(starter_items)
        user_location_count += 1  # Victory item is counted as part of the pool
        items = []
        if self.options.goal.value == self.options.goal.option_progressive:
            items.append(self.create_item("Super-Size Me"))
        items.append(self.create_item("Play as White"))
        self.items_used[self.player]["Play as White"] = 1

        # find the material value the user's army should provide once fully collected
        material = sum([
            progression_items[item].material * self.items_used[self.player][item]
            for item in self.items_used[self.player] if item in progression_items])
        min_material = determine_min_material(self.options)
        max_material = determine_max_material(self.options)
        if super_sized:
            endgame_multiplier = (location_table["Checkmate Maxima"].material_expectations_grand /
                                  location_table["Checkmate Minima"].material_expectations_grand)
            min_material *= endgame_multiplier
            max_material *= endgame_multiplier

        # remove items player does not want
        # TODO: tie these "magic numbers" to the corresponding Item.quantity
        self.items_used[self.player]["Progressive Consul"] = (
                self.items_used[self.player].get("Progressive Consul", 0) +
                (3 - self.options.max_kings.value))
        self.items_used[self.player]["Progressive King Promotion"] = (
                self.items_used[self.player].get("Progressive King Promotion", 0) +
                (2 - self.options.fairy_kings.value))
        self.items_used[self.player]["Progressive Engine ELO Lobotomy"] = (
                self.items_used[self.player].get("Progressive Engine ELO Lobotomy", 0) +
                (5 - self.options.max_engine_penalties.value))
        self.items_used[self.player]["Progressive Pocket"] = (
                self.items_used[self.player].get("Progressive Pocket", 0) +
                (12 - min(self.options.max_pocket.value, 3 * self.options.pocket_limit_by_pocket.value)))
        # if self.options.goal.value != self.options.goal.option_progressive:
        self.items_used[self.player]["Super-Size Me"] = 1

        # add items player really wants
        yaml_locked_items: Dict[str, int] = self.options.locked_items.value
        locked_items = dict(yaml_locked_items)
        # ensure locked items have enough parents
        player_queens: int = (locked_items.get("Progressive Major To Queen", 0) +
                              self.items_used[self.player].get("Progressive Major To Queen", 0))
        locked_items["Progressive Major Piece"] = max(
            player_queens, locked_items.get("Progressive Major Piece", 0))
        # ensure castling
        if self.options.accessibility.value != self.options.accessibility.option_minimal:
            required_majors: int = 2 - self.items_used[self.player].get("Progressive Major Piece", 0) + player_queens
            locked_items["Progressive Major Piece"] = max(
                required_majors, locked_items.get("Progressive Major Piece", 0))
        # TODO(chesslogic): I can instead remove items from locked_items during the corresponding loop, until we would
        #  reach min_material by adding the remaining contents of locked_items. We would also need to check remaining
        #  locations, e.g. because the locked_items might contain some filler items like Progressive Pocket Range.
        remaining_material = sum([locked_items[item] * progression_items[item].material for item in locked_items])
        logging.debug(str(self.player) + " pre-fill granted total material of " + str(material + remaining_material) +
                      " toward " + str(max_material) + " via items " + str(self.items_used[self.player]) +
                      " having set " + str(starter_items) + " and generated " + str(Counter(items)))

        my_progression_items = list(progression_items.keys())
        self.items_remaining[self.player] = {
            name: progression_items[name].quantity - self.items_used.get(name, 0) for name in my_progression_items}

        # prevent victory event from being added to general pool
        my_progression_items.remove("Victory")

        # more pawn chance
        my_progression_items.append("Progressive Pawn")
        my_progression_items.append("Progressive Pawn")
        # I am proud of this feature, so I want players to see more of it. Fight me.
        my_progression_items.append("Progressive Pocket")
        my_progression_items.append("Progressive Pocket")
        # halve chance of queen promotion - with an equal distribution, user will end up with no majors and only queens
        my_progression_items.extend([item for item in my_progression_items if item != "Progressive Major To Queen"])
        # add an extra minor piece... there are so many types ...
        my_progression_items.append("Progressive Minor Piece")
        my_progression_items.append("Progressive Pawn")

        # items are now in a distribution of 1 queen:1 major:3 minor:7 pawn:6 pocket (material 9 + 5 + 9 + 7 + 6 = 36)
        # note that queens require that a major precede them, which increases the likelihood of the other types

        max_items = len(location_table)
        if not super_sized:
            max_items -= len([loc for loc in location_table if location_table[loc].material_expectations == -1])
        if self.options.enable_tactics.value == self.options.enable_tactics.option_none:
            max_items -= len([loc for loc in location_table if location_table[loc].is_tactic is not None])
        elif self.options.enable_tactics.value == self.options.enable_tactics.option_turns:
            max_items -= len([loc for loc in location_table if location_table[loc].is_tactic == Tactic.Fork])

        while ((len(items) + user_location_count + sum(locked_items.values())) < max_items and
               material < max_material and len(my_progression_items) > 0):
            chosen_item = self.random.choice(my_progression_items)
            # obey user's wishes
            if (self.should_remove(chosen_item, material, min_material, max_material,
                                   items, my_progression_items, locked_items)):
                my_progression_items.remove(chosen_item)
                continue
            # add item
            if not self.has_prereqs(chosen_item):
                continue
            if self.can_add_more(chosen_item):
                try_item = self.create_item(chosen_item)
                was_locked = self.consume_item(chosen_item, locked_items)
                items.append(try_item)
                material += progression_items[chosen_item].material
                if not was_locked:
                    self.lock_new_items(chosen_item, items, locked_items)
            elif material >= min_material:
                my_progression_items.remove(chosen_item)
        all_material = sum([locked_items[item] * progression_items[item].material for item in locked_items]) + material
        logging.debug(str(self.player) + " granted total material of " + str(all_material) +
                      " toward " + str(max_material) + " via items " + str(self.items_used[self.player]) +
                      " having generated " + str(Counter(items)))

        # exclude inaccessible locations
        # (all locations should be accessible if accessibility != minimal)
        # (I might change this later I guess, Archipelago is supposed to tolerate inaccessible items being swallowed up)
        if self.options.accessibility.value == self.options.accessibility.option_minimal:
            # castle
            if (len([item for item in items if item.name == "Progressive Major Piece"]) < 2 +
                    len([item for item in items if item.name == "Progressive Major To Queen"])):
                for location in ["O-O-O Castle", "O-O Castle"]:
                    if location not in self.options.exclude_locations.value:
                        self.options.exclude_locations.value.add(location)
            # material
            for location in location_table:
                if location not in self.options.exclude_locations.value:
                    if material < location_table[location].material_expectations:
                        self.options.exclude_locations.value.add(location)
            # chessmen
            chessmen = chessmen_count(items, self.options.pocket_limit_by_pocket.value)
            for location in location_table:
                if location not in self.options.exclude_locations.value:
                    if chessmen < location_table[location].chessmen_expectations:
                        self.options.exclude_locations.value.add(location)

        my_useful_items = list(useful_items.keys())
        while ((len(items) + user_location_count + sum(locked_items.values())) < max_items and
               len(my_useful_items) > 0):
            chosen_item = self.random.choice(my_useful_items)
            if not self.has_prereqs(chosen_item):
                continue
            if self.can_add_more(chosen_item):
                self.consume_item(chosen_item, locked_items)
                try_item = self.create_item(chosen_item)
                items.append(try_item)
            else:
                my_useful_items.remove(chosen_item)

        my_filler_items = list(filler_items.keys())
        # get whether any item mentions "pocket" in the current items pool
        has_pocket = False
        for item in list(locked_items.keys()):
            if "Pocket" in item:
                has_pocket = True
                break
        if not has_pocket:
            for item in items:
                if "Pocket" in item.name:
                    has_pocket = True
                    break
        # remove "pocket" fillers from the list of filler items
        if not has_pocket:
            my_filler_items = [item for item in my_filler_items if "Pocket" not in item]
        while (len(items) + user_location_count + sum(locked_items.values())) < max_items:
            if len(my_filler_items) == 0:
                my_filler_items = ["Progressive Pocket Gems"]
            chosen_item = self.random.choice(my_filler_items)
            if not has_pocket and not self.has_prereqs(chosen_item):
                continue
            if has_pocket or self.can_add_more(chosen_item):
                self.consume_item(chosen_item, locked_items)
                try_item = self.create_item(chosen_item)
                items.append(try_item)
            else:
                my_filler_items.remove(chosen_item)

        # TODO: Check that there are enough chessmen. (Player may have locked too much material.)
        for item in locked_items:
            if item not in self.items_used[self.player]:
                self.items_used[self.player][item] = 0
            self.items_used[self.player][item] += locked_items[item]
            items.extend([self.create_item(item) for i in range(locked_items[item])])
            material += progression_items[item].material * locked_items[item]

        self.multiworld.itempool += items

    def consume_item(self, chosen_item: str, locked_items: Dict[str, int]) -> bool:
        if chosen_item not in self.items_used[self.player]:
            self.items_used[self.player][chosen_item] = 0
        self.items_used[self.player][chosen_item] += 1
        if chosen_item in self.items_remaining[self.player]:
            self.items_remaining[self.player][chosen_item] -= 1
            if self.items_remaining[self.player][chosen_item] <= 0:
                del (self.items_remaining[self.player][chosen_item])
        if chosen_item in locked_items and locked_items[chosen_item] > 0:
            locked_items[chosen_item] -= 1
            if locked_items[chosen_item] <= 0:
                del (locked_items[chosen_item])
            return True
        return False

    # this method assumes we cannot run out of pawns... we don't support excluded_items{pawn}
    # there is no maximum number of chessmen... just minimum chessmen and maximum material.
    def should_remove(self,
                      chosen_item: str,
                      material: int,
                      min_material: float,
                      max_material: float,
                      items: List[CMItem],
                      my_progression_items: List[Union[str, CMItemData]],
                      locked_items: Dict[str, int]) -> bool:
        if chosen_item == "Progressive Major To Queen" and "Progressive Major Piece" not in my_progression_items:
            # TODO: there is a better way, probably next step is a "one strike" mechanism
            return True

        if self.items_used[self.player].get(chosen_item, 0) >= item_table[chosen_item].quantity:
            return True
        if not self.under_piece_limit(chosen_item, self.PieceLimitCascade.POTENTIAL_CHILDREN):
            return True

        chosen_material = self.lockable_material_value(chosen_item, items, locked_items)
        remaining_material = sum([locked_items[item] * progression_items[item].material for item in locked_items])
        total_material = material + chosen_material + remaining_material
        exceeds_max = total_material > max_material

        if self.options.accessibility.value == self.options.accessibility.option_minimal:
            enough_yet = material + remaining_material >= min_material
            return exceeds_max and enough_yet

        chessmen_requirement = highest_chessmen_requirement_small if \
            self.options.goal.value == self.options.goal.option_single else \
            highest_chessmen_requirement
        necessary_chessmen = (chessmen_requirement - chessmen_count(items, self.options.pocket_limit_by_pocket.value))
        if chosen_item in item_name_groups["Chessmen"]:
            necessary_chessmen -= 1
        elif chosen_item == "Progressive Pocket":
            # We know pocket_limit > 0, because pockets are not disabled, because we checked items_used
            pocket_limit = self.options.pocket_limit_by_pocket.value
            next_pocket = locked_items.get("Progressive Pocket", 0) + \
                len([item for item in items if item.name == "Progressive Pocket"]) + \
                1
            if next_pocket % pocket_limit == 1:
                necessary_chessmen -= 1
        if necessary_chessmen <= 0:
            return exceeds_max
        minimum_possible_material = total_material + (
            item_table["Progressive Pawn"].material * necessary_chessmen)
        return minimum_possible_material > max_material

    # if this piece was added, it might add more than its own material to the locked pool
    def lockable_material_value(self, chosen_item: str, items: List[CMItem], locked_items: Dict[str, int]):
        material = progression_items[chosen_item].material
        if self.options.accessibility.value == self.options.accessibility.option_minimal:
            return material
        if chosen_item == "Progressive Major To Queen" and self.unupgraded_majors_in_pool(items, locked_items) <= 2:
            material += progression_items["Progressive Major Piece"].material
        return material

    # ensures the Castling location is reachable
    def lock_new_items(self, chosen_item: str, items: List[CMItem], locked_items: Dict[str, int]) -> None:
        if self.options.accessibility.value == self.options.accessibility.option_minimal:
            return
        if chosen_item == "Progressive Major To Queen":
            if self.unupgraded_majors_in_pool(items, locked_items) < 2:
                if "Progressive Major Piece" not in locked_items:
                    locked_items["Progressive Major Piece"] = 0
                locked_items["Progressive Major Piece"] += 1

    def unupgraded_majors_in_pool(self, items: List[CMItem], locked_items: Dict[str, int]) -> int:
        total_majors = len([item for item in items if item.name == "Progressive Major Piece"]) + len(
            [item for item in locked_items if item == "Progressive Major Piece"])
        total_upgrades = len([item for item in items if item.name == "Progressive Major To Queen"]) + len(
            [item for item in locked_items if item == "Progressive Major To Queen"])

        return total_majors - total_upgrades

    def create_regions(self) -> None:
        region = Region("Menu", self.player, self.multiworld)
        for loc_name in location_table:
            loc_data = location_table[loc_name]
            if self.options.goal.value == self.options.goal.option_single:
                if loc_data.material_expectations == -1:
                    continue
            if self.options.enable_tactics.value == self.options.enable_tactics.option_none:
                if loc_data.is_tactic:
                    continue
            if self.options.enable_tactics.value == self.options.enable_tactics.option_turns:
                if loc_data.is_tactic == Tactic.Fork:
                    continue
            region.locations.append(CMLocation(self.player, loc_name, loc_data.code, region))
        self.multiworld.regions.append(region)

    def get_filler_item_name(self) -> str:
        if self.player not in self.items_used:
            return "Progressive Pawn Forwardness"
        if self.items_used[self.player].get("Progressive Pocket", 0) > 0 and \
                self.items_used[self.player].get("Progressive Pocket Range", 0) < \
                item_table["Progressive Pocket Range"].quantity:
            return "Progressive Pocket Range"
        if self.items_used[self.player].get("Progressive Pawn Forwardness", 0) < \
                min(item_table["Progressive Pawn Forwardness"].quantity,
                    item_table["Progressive Pawn Forwardness"].parents[0][1]
                    * self.items_used[self.player].get("Progressive Pawn", 0)):
            return "Progressive Pawn Forwardness"
        return "Progressive Pocket Gems"

    def generate_basic(self) -> None:
        if self.options.goal.value == self.options.goal.option_single:
            victory_item = self.create_item("Victory")
            self.multiworld.get_location("Checkmate Minima", self.player).place_locked_item(victory_item)
        else:
            victory_item = self.create_item("Victory")
            self.multiworld.get_location("Checkmate Maxima", self.player).place_locked_item(victory_item)

    def fewest_parents(self, parents: List[List[Union[str, int]]]):
        # TODO: this concept doesn't work if a parent can have multiple children and another can't, e.g. forwardness
        return min([self.items_used[self.player].get(item[0], 0) for item in parents])

    def has_prereqs(self, chosen_item: str) -> bool:
        parents = get_parents(chosen_item)
        if parents:
            fewest_parents = self.fewest_parents(parents) * get_parents(chosen_item)[0][1]
            if fewest_parents is None:
                return True
            enough_parents = fewest_parents > self.items_used[self.player].get(chosen_item, 0)
            if not enough_parents:
                return False
        return self.under_piece_limit(chosen_item, self.PieceLimitCascade.ACTUAL_CHILDREN)

    class PieceLimitCascade(Enum):
        NO_CHILDREN = 1
        ACTUAL_CHILDREN = 2
        POTENTIAL_CHILDREN = 3

    def can_add_more(self, chosen_item: str) -> bool:
        if not self.under_piece_limit(chosen_item, self.PieceLimitCascade.POTENTIAL_CHILDREN):
            return False
        return chosen_item not in self.items_used[self.player] or \
            item_table[chosen_item].quantity == -1 or \
            self.items_used[self.player][chosen_item] < item_table[chosen_item].quantity

    def under_piece_limit(self, chosen_item: str, with_children: PieceLimitCascade) -> bool:
        if self.player not in self.items_used:
            # this can be the case during push_precollected
            return True
        piece_limit = self.find_piece_limit(chosen_item, with_children)
        pieces_used = self.items_used[self.player].get(chosen_item, 0)
        if 0 < piece_limit <= pieces_used:
            # Intentionally ignore "parents" property: player might receive parent items after all children
            # The player ending up with bounded parents on the upper end is handled in has_prereqs
            return False
        # Limit pieces placed by total number
        if chosen_item in piece_limit_options:
            piece_total_limit = piece_limit_options[chosen_item](self.options).value
            pieces_used = self.items_used[self.player].get(chosen_item, 0)
            if 0 < piece_total_limit <= pieces_used:
                return False
        return True

    def find_piece_limit(self, chosen_item: str, with_children: PieceLimitCascade) -> int:
        """Limit pieces placed by individual variety. This applies the Piece Type Limit setting."""
        if chosen_item not in piece_type_limit_options:
            return 0

        piece_limit: int = self.piece_limit_of(chosen_item)
        army_piece_types = {
            piece: sum([self.piece_types_by_army[army][piece] for army in self.armies[self.player]])
            for piece in set().union(*self.piece_types_by_army.values())}
        limit_multiplier = get_limit_multiplier_for_item(army_piece_types)
        piece_limit = piece_limit * limit_multiplier(chosen_item)
        if piece_limit > 0 and with_children != self.PieceLimitCascade.NO_CHILDREN:
            children = get_children(chosen_item)
            if children:
                if with_children == self.PieceLimitCascade.ACTUAL_CHILDREN:
                    piece_limit = piece_limit + sum([self.items_used[self.player].get(child, 0) for child in children])
                elif with_children == self.PieceLimitCascade.POTENTIAL_CHILDREN:
                    piece_limit = piece_limit + sum([self.find_piece_limit(child, with_children) for child in children])
        return piece_limit

    def piece_limit_of(self, chosen_item: str):
        return piece_type_limit_options[chosen_item](self.options).value

    def get_excluded_items(self) -> Dict[str, int]:
        excluded_items: Dict[str, int] = {}

        if self.options.goal.value == self.options.goal.option_super:
            item = self.create_item("Super-Size Me")
            self.multiworld.push_precollected(item)
        for item in self.multiworld.precollected_items[self.player]:
            if item.name not in excluded_items:
                excluded_items[item.name] = 0
            excluded_items[item.name] += 1

        # excluded_items_option = getattr(multiworld, 'excluded_items', {player: []})

        # excluded_items.update(excluded_items_option[player].value)

        return excluded_items

    def assign_starter_items(self, excluded_items: Dict[str, int],
                             locked_locations: List[str]) -> List[Item]:
        multiworld = self.multiworld
        player = self.player
        cmoptions: CMOptions = self.options
        non_local_items = self.options.non_local_items.value
        early_material_option = cmoptions.early_material.value

        user_items = []
        if self.options.goal.value == self.options.goal.option_ordered_progressive:
            item = self.create_item("Super-Size Me")
            multiworld.get_location("Checkmate Minima", player).place_locked_item(item)
            locked_locations.append("Checkmate Minima")
            user_items.append(item)
        if early_material_option > 0:
            early_units = []
            if early_material_option == 1 or early_material_option > 4:
                early_units.append("Progressive Pawn")
            if early_material_option == 2 or early_material_option > 3:
                early_units.append("Progressive Minor Piece")
            if early_material_option > 2:
                early_units.append("Progressive Major Piece")
            local_basic_unit = sorted(item for item in early_units if
                                      item not in non_local_items and (
                                              item not in excluded_items or
                                              excluded_items[item] < item_table[item].quantity))
            if not local_basic_unit:
                raise Exception("At least one early chessman must be local")

            item = self.create_item(self.random.choice(local_basic_unit))
            multiworld.get_location("King to E2/E7 Early", player).place_locked_item(item)
            locked_locations.append("King to E2/E7 Early")
            user_items.append(item)

        return user_items

    def collect(self, state: CollectionState, item: Item) -> bool:
        material = 0
        item_count = state.prog_items[self.player][item.name]
        # check if there are existing unused upgrades to this piece which are immediately satisfied
        children = get_children(item.name)
        for child in children:
            if item_table[child].material == 0:
                continue
            # TODO: when a child could have multiple parents, check that this is also the least parent
            if item_count < state.prog_items[self.player][child]:
                # we had an upgrade, so add that upgrade to the material count
                material += item_table[child].material
                logging.debug("Adding child " + child + " having count: " + str(state.prog_items[self.player][child]))
            else:
                # not immediately upgraded, but maybe later
                logging.debug("Added item " + item.name + " had insufficient children " + child + " to upgrade it")
        # check if this is an upgrade which is immediately satisfied by applying it to an existing piece
        parents = get_parents(item.name)
        if len(parents) == 0 or item_table[item.name].material == 0:
            # this is a root element (like a piece), not an upgrade, so we can use it immediately
            material += item_table[item.name].material
        else:
            # this is an upgrade, so we can only apply it if it can find an unsatisfied parent
            fewest_parents = min([state.prog_items[self.player].get(parent[0], 0) for parent in parents])
            # TODO: when a parent could have multiple children, check that this is also the least child
            if item_count < fewest_parents * parents[0][1]:
                # found a piece we could upgrade, so apply the upgrade
                material += item_table[item.name].material
                logging.debug("Item " + item.name + " had sufficient parents " + str(fewest_parents) + " to be tried")
            else:
                # not upgrading anything, but maybe later
                logging.debug("Added item " + item.name + " had insufficient parents " + str(fewest_parents))
        change = super().collect(state, item)
        if change:
            # we actually collected the item, so we must gain the material
            state.prog_items[self.player]["Material"] += material
        logging.debug("Adding " + item.name + " with " + str(state.prog_items[self.player].get("Material", 0)) +
                      " having " + str(state.prog_items))
        return change

    # TODO: extremely similar - refactor to pass lt/lte comparator and an arithmetic lambda +/-
    def remove(self, state: CollectionState, item: Item) -> bool:
        # if state.prog_items[self.player].get(item.name, 0) == 0:
        #     return False  # TODO(chesslogic): I think this should be base behaviour, and doing this probably breaks it
        material = 0
        item_count = state.prog_items[self.player][item.name]
        children = get_children(item.name)
        for child in children:
            if item_table[child].material == 0:
                continue
            # TODO: when a child could have multiple parents, check that this is also the least parent
            if item_count <= state.prog_items[self.player][child]:
                material -= item_table[child].material
                logging.debug("Removing child " + child + " having count: " + str(state.prog_items[self.player][child]))
            else:
                logging.debug("Removed item " + item.name + " had insufficient children " + child)
        parents = get_parents(item.name)
        if len(parents) == 0 or item_table[item.name].material == 0:
            material -= item_table[item.name].material
        else:
            fewest_parents = min([state.prog_items[self.player].get(parent[0], 0) for parent in parents])
            if item_count <= fewest_parents:
                material -= item_table[item.name].material
                logging.debug("Item " + item.name + " had sufficient parents " + str(fewest_parents) + " to be removed")
            else:
                logging.debug("Removed item " + item.name + " had insufficient parents " + str(fewest_parents))
        change = super().remove(state, item)
        if change:
            state.prog_items[self.player]["Material"] += material
        logging.debug("Removing " + item.name + " with " + str(state.prog_items[self.player].get("Material", 0)) +
                      " having " + str(state.prog_items))
        return change


def get_limit_multiplier_for_item(item_dictionary: Dict[str, int]) -> Callable[[str], int]:
    return lambda item_name: item_dictionary[item_name]


def get_parents(chosen_item: str) -> List[List[Union[str, int]]]:
    return item_table[chosen_item].parents


def get_children(chosen_item: str) -> List[str]:
    return [item for item in item_table
            if item_table[item].parents is not None and chosen_item in map(
            lambda x: x[0], item_table[item].parents)]


def chessmen_count(items: List[CMItem], pocket_limit: int) -> int:
    pocket_amount = (0 if pocket_limit <= 0 else
                     math.ceil(len([item for item in items if item.name == "Progressive Pocket"]) / pocket_limit))
    chessmen_amount = len([item for item in items if item.name in item_name_groups["Chessmen"]])
    logging.debug("Found {} chessmen and {} pocket men".format(chessmen_amount, pocket_amount))
    return chessmen_amount + pocket_amount
