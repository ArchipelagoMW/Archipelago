import math
import random
from typing import List, Set, Dict

from BaseClasses import Tutorial, Region, ItemClassification, MultiWorld, Item
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
        "checks-mate_en.md",
        "checks-mate/en",
        ["roty", "rft50"]
    )]


class CMWorld(World):
    """
    Checksmate is a game where you play chess, but all of your pieces were scattered across the multiworld.
    You win when you checkmate the opposing king!
    """
    game: str = "ChecksMate"
    option_definitions = cm_options
    data_version = 0
    web = CMWeb()
    required_client_version = (0, 2, 2) # TODO: what does it mean

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
    items_used: Dict[str, int] = {}

    item_pool: List[CMItem] = []
    prefill_items: List[CMItem] = []

    def __init__(self, multiworld: MultiWorld, player: int):
        super(CMWorld, self).__init__(multiworld, player)
        self.locked_locations = []

    def generate_early(self) -> None:
        # TODO: if goal is not option_single do not add all enemies (requires add client support)
        for enemy_pawn in self.item_name_groups["Enemy Pawn"]:
            self.multiworld.start_inventory[self.player].value[enemy_pawn] = 1
        for enemy_piece in self.item_name_groups["Enemy Piece"]:
            self.multiworld.start_inventory[self.player].value[enemy_piece] = 1

    def setting(self, name: str):
        return getattr(self.multiworld, name)[self.player]

    def fill_slot_data(self) -> dict:
        seeds = {name: self.multiworld.per_slot_randoms[self.player].getrandbits(31) for name in [
            "pocketSeed", "pawnSeed", "minorSeed", "majorSeed", "queenSeed"]}
        return dict(seeds, **{option_name: self.setting(option_name).value for option_name in cm_options})

    def create_item(self, name: str) -> CMItem:
        data = item_table[name]
        return CMItem(name, data.classification, data.code, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def create_items(self):
        # TODO: limit total material
        #items = [[self.create_item(item) for _ in range(item_data.quantity)]
        #                             for item, item_data in progression_items]0
        excluded_items = get_excluded_items(self.multiworld, self.player)
        for item_name in excluded_items:
            if item_name not in self.items_used:
                self.items_used[item_name] = 0
            self.items_used[item_name] += excluded_items[item_name]
        starter_items = assign_starter_items(self.multiworld, self.player, excluded_items, self.locked_locations)
        for item in starter_items:
            if item.name not in self.items_used:
                self.items_used[item.name] = 0
            self.items_used[item.name] += 1

        items = []

        material = 0
        my_progression_items = set(progression_items.keys())
        min_material_option = get_option_value(self.multiworld, self.player, "min_material") * 100
        max_material_option = get_option_value(self.multiworld, self.player, "max_material") * 100
        while material < min_material_option and len(my_progression_items) > 0:
            chosen_item = self.multiworld.random.choice(list(my_progression_items))
            # obey user's wishes
            if progression_items[chosen_item].material + material > max_material_option:
                my_progression_items.remove(chosen_item)
                continue
            # add item
            if self.can_add_more(chosen_item):
                try_item = self.create_item(chosen_item)
                if chosen_item not in self.items_used:
                    self.items_used[chosen_item] = 0
                self.items_used[chosen_item] += 1
                items.append(try_item)
                material += progression_items[chosen_item].material
            else:
                my_progression_items.remove(chosen_item)

        max_material_actual = (
                self.multiworld.random.random() * (max_material_option - min_material_option) + max_material_option)
        while material < max_material_actual and len(my_progression_items) > 0:
            chosen_item = self.multiworld.random.choice(list(my_progression_items))
            # obey user's wishes
            if progression_items[chosen_item].material + material > max_material_option:
                break
            # add item
            if self.can_add_more(chosen_item):
                try_item = self.create_item(chosen_item)
                if chosen_item not in self.items_used:
                    self.items_used[chosen_item] = 0
                self.items_used[chosen_item] += 1
                items.append(try_item)
                material += progression_items[chosen_item].material
            else:
                my_progression_items.remove(chosen_item)

        my_useful_items = set(useful_items.keys())
        while len(items) < len(location_table) and len(my_useful_items) > 0:
            chosen_item = self.multiworld.random.choice(list(my_useful_items))
            if self.can_add_more(chosen_item):
                if chosen_item not in self.items_used:
                    self.items_used[chosen_item] = 0
                self.items_used[chosen_item] += 1
                try_item = self.create_item(chosen_item)
                items.append(try_item)
            else:
                my_useful_items.remove(chosen_item)

        my_filler_items = set(filler_items.keys())
        while len(items) < len(location_table):
            chosen_item = self.multiworld.random.choice(list(my_filler_items))
            if self.can_add_more(chosen_item):
                if chosen_item not in self.items_used:
                    self.items_used[chosen_item] = 0
                self.items_used[chosen_item] += 1
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
        (self.multiworld.get_location("Checkmate Maxima", self.player).
         place_locked_item(CMItem("Victory", ItemClassification.progression, 4_065, self.player)))

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def can_add_more(self, chosen_item: str) -> bool:
        return chosen_item not in self.items_used or \
            item_table[chosen_item].quantity == -1 or \
            self.items_used[chosen_item] < item_table[chosen_item].quantity


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

        item = create_item_with_correct_settings(player, multiworld.random.choice(local_basic_unit))
        multiworld.get_location("Bongcloud Once", player).place_locked_item(item)
        locked_locations.append("Bongcloud Once")

        return [item]
    else:
        return []
