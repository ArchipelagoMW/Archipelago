import math
import random
from enum import Enum
from typing import List, Dict, ClassVar, Callable

from BaseClasses import Tutorial, Region, MultiWorld, Item
from worlds.AutoWorld import WebWorld, World
from .Options import cm_options, get_option_value
from .Items import CMItem, item_table, create_item_with_correct_settings, filler_items, progression_items, useful_items
from .Locations import CMLocation, location_table
from .Options import cm_options
from .Rules import set_rules


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


class CMWorld(World):
    """
    ChecksMate is a game where you play chess, but all of your pieces were scattered across the multiworld.
    You win when you checkmate the opposing king!
    """
    game: ClassVar[str] = "ChecksMate"
    option_definitions = cm_options
    data_version = 0
    web = CMWeb()
    required_client_version = (0, 3, 4)

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}
    locked_locations: List[str]

    item_name_groups = {
        # "Pawn": {"Pawn A", "Pawn B", "Pawn C", "Pawn D", "Pawn E", "Pawn F", "Pawn G", "Pawn H"},
        "Enemy Pawn": {"Enemy Pawn A", "Enemy Pawn B", "Enemy Pawn C", "Enemy Pawn D",
                       "Enemy Pawn E", "Enemy Pawn F", "Enemy Pawn G", "Enemy Pawn H"},
        "Enemy Piece": {"Enemy Piece A", "Enemy Piece B", "Enemy Piece C", "Enemy Piece D",
                        "Enemy Piece F", "Enemy Piece G", "Enemy Piece H"},
    }
    items_used: Dict[int, Dict[str, int]] = {}
    army: Dict[int, int] = {}

    item_pool: List[CMItem] = []
    prefill_items: List[CMItem] = []

    known_pieces = {"Progressive Minor Piece": 9, "Progressive Major Piece": 5, "Progressive Major To Queen": 4, }
    piece_type_limit_options = {
        "Progressive Minor Piece": "minor_piece_limit_by_type",
        "Progressive Major Piece": "major_piece_limit_by_type",
        "Progressive Major To Queen": "queen_piece_limit_by_type",
    }
    piece_limit_options = {
        "Progressive Major To Queen": "queen_piece_limit",
    }
    piece_types_by_army = {
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
    }

    def __init__(self, multiworld: MultiWorld, player: int):
        super(CMWorld, self).__init__(multiworld, player)
        self.locked_locations = []

    def generate_early(self) -> None:
        army_constraint = get_option_value(self.multiworld, self.player, "fairy_chess_army")
        if army_constraint != 0:
            which_pieces = get_option_value(self.multiworld, self.player, "fairy_chess_pieces")
            # Full: Adds the 12 Chess With Different Armies pieces, the Cannon, and the Vao.
            if which_pieces == 1:
                army_options = [0, 1, 2, 3, 4]
            # CwDA: Adds the pieces from Ralph Betza's 12 Chess With Different Armies.
            elif which_pieces == 2:
                army_options = [0, 1, 2, 3]
            # Cannon: Adds a Rook-like piece, which captures a distal chessman by leaping over an intervening chessman.
            # Eurasian: Adds the Cannon and the Vao, a Bishop-like Cannon, in that it moves and captures diagonally.
            elif which_pieces > 2:
                army_options = [0, 4]
            # Vanilla: Disables fairy chess pieces completely.
            else:
                army_options = [0]
            self.army[self.player] = self.multiworld.per_slot_randoms[self.player].choice(army_options)
        is_single = get_option_value(self.multiworld, self.player, "goal") == 0
        if not is_single:
            return
        for enemy_pawn in self.item_name_groups["Enemy Pawn"]:
            self.multiworld.start_inventory[self.player].value[enemy_pawn] = 1
        for enemy_piece in self.item_name_groups["Enemy Piece"]:
            self.multiworld.start_inventory[self.player].value[enemy_piece] = 1

    def setting(self, name: str):
        return getattr(self.multiworld, name)[self.player]

    def fill_slot_data(self) -> dict:
        cursed_knowledge = {name: self.multiworld.per_slot_randoms[self.player].getrandbits(31) for name in [
            "pocketSeed", "pawnSeed", "minorSeed", "majorSeed", "queenSeed"]}
        if self.player in self.army:
            cursed_knowledge["army"] = self.army[self.player]
        return dict(cursed_knowledge, **{option_name: self.setting(option_name).value for option_name in cm_options})

    def create_item(self, name: str) -> CMItem:
        data = item_table[name]
        return CMItem(name, data.classification, data.code, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def create_items(self):
        # TODO: limit total material
        # items = [[self.create_item(item) for _ in range(item_data.quantity)]
        #                             for item, item_data in progression_items]0
        excluded_items = get_excluded_items(self.multiworld, self.player)
        self.items_used[self.player] = {}
        for item_name in excluded_items:
            if item_name not in self.items_used[self.player]:
                self.items_used[self.player][item_name] = 0
            self.items_used[self.player][item_name] += excluded_items[item_name]
        starter_items = assign_starter_items(self.multiworld, self.player, excluded_items, self.locked_locations)
        for item in starter_items:
            if item.name not in self.items_used[self.player]:
                self.items_used[self.player][item.name] = 0
            self.items_used[self.player][item.name] += 1

        # print(self.items_used)
        starter_dict = {item.name: 1 for item in starter_items}
        excluded_dict = {
            item: excluded_items[item] for item in excluded_items if not (
                    not (item not in self.item_name_groups["Enemy Pawn"]) or not (
                    item not in self.item_name_groups["Enemy Piece"]))}
        user_items = {key: starter_dict.get(key, 0) + excluded_dict.get(key, 0)
                      for key in set(starter_dict) | set(excluded_dict)}
        user_item_count = len(user_items)
        user_item_count += 1  # Victory item is counted as part of the pool
        items = []

        material = sum([
            progression_items[item].material * self.items_used[self.player][item]
            for item in self.items_used[self.player].keys() if item in progression_items])
        min_material_option = get_option_value(self.multiworld, self.player, "min_material") * 100
        max_material_option = get_option_value(self.multiworld, self.player, "max_material") * 100
        if max_material_option < min_material_option:
            max_material_option = min_material_option
        max_material_actual = (
            self.multiworld.per_slot_randoms[self.player].random() * (
                max_material_option - min_material_option) + max_material_option)
        max_material_actual += progression_items["Play as White"].material

        my_progression_items = list(progression_items.keys())
        my_progression_items.remove("Victory")
        # more pawn chance (1 major:1 minor:2 pawn distribution)
        my_progression_items.append("Progressive Pawn")
        # I am proud of this feature, so I want players to see more of it. Fight me.
        my_progression_items.append("Progressive Pocket")
        # halve chance of queen promotion - with an equal distribution, user will end up with no majors and only queens
        my_progression_items.extend([item for item in my_progression_items if item != "Progressive Major To Queen"])
        while (len(items) + user_item_count) < len(location_table) and material < max_material_actual and len(
                my_progression_items) > 0:
            chosen_item = self.multiworld.per_slot_randoms[self.player].choice(my_progression_items)
            # obey user's wishes
            if (material > min_material_option and
                    progression_items[chosen_item].material + material > max_material_option):
                my_progression_items.remove(chosen_item)
                continue
            # add item
            if not self.has_prereqs(chosen_item):
                continue
            if self.can_add_more(chosen_item):
                try_item = self.create_item(chosen_item)
                if chosen_item not in self.items_used[self.player]:
                    self.items_used[self.player][chosen_item] = 0
                self.items_used[self.player][chosen_item] += 1
                items.append(try_item)
                material += progression_items[chosen_item].material
            else:
                my_progression_items.remove(chosen_item)

        my_useful_items = list(useful_items.keys())
        while (len(items) + user_item_count) < len(location_table) and len(my_useful_items) > 0:
            chosen_item = self.multiworld.per_slot_randoms[self.player].choice(my_useful_items)
            if not self.has_prereqs(chosen_item):
                continue
            if self.can_add_more(chosen_item):
                if chosen_item not in self.items_used[self.player]:
                    self.items_used[self.player][chosen_item] = 0
                self.items_used[self.player][chosen_item] += 1
                try_item = self.create_item(chosen_item)
                items.append(try_item)
            else:
                my_useful_items.remove(chosen_item)

        my_filler_items = list(filler_items.keys())
        while (len(items) + user_item_count) < len(location_table):
            chosen_item = self.multiworld.per_slot_randoms[self.player].choice(my_filler_items)
            if not self.has_prereqs(chosen_item):
                continue
            if self.can_add_more(chosen_item):
                if chosen_item not in self.items_used[self.player]:
                    self.items_used[self.player][chosen_item] = 0
                self.items_used[self.player][chosen_item] += 1
                try_item = self.create_item(chosen_item)
                items.append(try_item)
            else:
                my_filler_items.remove(chosen_item)
        self.multiworld.itempool += items

    def create_regions(self):
        region = Region("Menu", self.player, self.multiworld)
        for loc_name in location_table:
            loc_data = location_table[loc_name]
            region.locations.append(CMLocation(self.player, loc_name, loc_data.code, region))
        self.multiworld.regions.append(region)

    def generate_basic(self):
        victory_item = create_item_with_correct_settings(self.player, "Victory")
        self.multiworld.get_location("Checkmate Maxima", self.player).place_locked_item(victory_item)

    def has_prereqs(self, chosen_item: str) -> bool:
        parents = get_parents(chosen_item)
        if parents:
            fewest_parents = min([self.items_used[self.player].get(item, 0) for item in parents])
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
        piece_limit = self.find_piece_limit(chosen_item, with_children)
        pieces_used = self.items_used[self.player].get(chosen_item, 0)
        if 0 < piece_limit <= pieces_used:
            # Intentionally ignore "parents" property: player might receive parent items after all children
            # The player ending up with bounded parents on the upper end is handled in has_prereqs
            return False
        # Limit pieces placed by total number
        if chosen_item in self.piece_limit_options:
            piece_total_limit = get_option_value(self.multiworld, self.player, self.piece_limit_options[chosen_item])
            pieces_used = self.items_used[self.player].get(chosen_item, 0)
            if 0 < piece_total_limit <= pieces_used:
                return False
        return True

    def find_piece_limit(self, chosen_item: str, with_children: PieceLimitCascade) -> int:
        """Limit pieces placed by individual variety. This applies the Piece Type Limit setting."""
        if chosen_item not in self.piece_type_limit_options:
            return 0

        piece_limit: int = self.piece_limit_of(chosen_item)
        limit_multiplier = get_limit_multiplier_for_item({chosen_item: 1})
        is_army_constrained = get_option_value(self.multiworld, self.player, "fairy_chess_army")
        # Chaos: Chooses random enabled options.
        if is_army_constrained == 0:
            limit_multiplier = get_limit_multiplier_for_item(self.known_pieces)
        # Limited: Chooses within your army, but in any distribution.
        if is_army_constrained == 1:
            army = self.army[self.player]
            limit_multiplier = get_limit_multiplier_for_item(self.piece_types_by_army[army])
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
        return get_option_value(self.multiworld, self.player, self.piece_type_limit_options[chosen_item])


def get_limit_multiplier_for_item(item_dictionary: Dict[str, int]) -> Callable[[str], int]:
    return lambda item_name: item_dictionary[item_name]


def get_parents(chosen_item: str) -> list[str]:
    return [item for item in item_table
            if item_table[chosen_item].parents is not None and item in item_table[chosen_item].parents]


def get_children(chosen_item: str) -> list[str]:
    return [item for item in item_table
            if item_table[item].parents is not None and chosen_item in item_table[item].parents]


def get_excluded_items(multiworld: MultiWorld, player: int) -> Dict[str, int]:
    excluded_items: Dict[str, int] = {}

    for item in multiworld.precollected_items[player]:
        if item.name not in excluded_items:
            excluded_items[item.name] = 0
        excluded_items[item.name] += 1

    # excluded_items_option = getattr(multiworld, 'excluded_items', {player: []})

    # excluded_items.update(excluded_items_option[player].value)

    return excluded_items


def assign_starter_items(multiworld: MultiWorld, player: int, excluded_items: Dict[str, int],
                         locked_locations: List[str]) -> List[Item]:
    non_local_items = multiworld.non_local_items[player].value
    early_material_option = get_option_value(multiworld, player, "early_material")
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

        item = create_item_with_correct_settings(player, multiworld.per_slot_randoms[player].choice(local_basic_unit))
        multiworld.get_location("Bongcloud Once", player).place_locked_item(item)
        locked_locations.append("Bongcloud Once")

        return [item]
    else:
        return []
