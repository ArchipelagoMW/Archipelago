import math
import random
from typing import List, Set

from BaseClasses import Tutorial, Region, RegionType, ItemClassification, MultiWorld, Item
from worlds.AutoWorld import WebWorld, World
from .Options import cm_options, get_option_value
from .Items import CMItem, item_table, create_item_with_correct_settings
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

    item_name_groups = {
        # "Pawn": {"Pawn A", "Pawn B", "Pawn C", "Pawn D", "Pawn E", "Pawn F", "Pawn G", "Pawn H"},
        "Enemy Pawn": {"Enemy Pawn A", "Enemy Pawn B", "Enemy Pawn C", "Enemy Pawn D",
                       "Enemy Pawn E", "Enemy Pawn F", "Enemy Pawn G", "Enemy Pawn H"},
        "Enemy Piece": {"Enemy Piece A", "Enemy Piece B", "Enemy Piece C", "Enemy Piece D",
                        "Enemy Piece F", "Enemy Piece G", "Enemy Piece H"},
    }

    item_pool: List[CMItem] = []
    prefill_items: List[CMItem] = []

    def setting(self, name: str):
        return getattr(self.multiworld, name)[self.player]

    def fill_slot_data(self) -> dict:
        seeds = {name: self.multiworld.random.getrandbits(31) for name in [
            "pocketSeed", "pawnSeed", "minorSeed", "majorSeed", "queenSeed"]}
        return dict(seeds, **{option_name: self.setting(option_name).value for option_name in cm_options})

    def create_item(self, name: str) -> CMItem:
        data = item_table[name]
        return CMItem(name, data.classification, data.code, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def create_items(self):

        self.multiworld.itempool += [self.create_item(item) for item in item_table]

    def create_regions(self):
        region = Region("Menu", RegionType.Generic, "Menu", self.player)
        region.multiworld = self.multiworld
        for loc_name in location_table:
            loc_data = location_table[loc_name]
            region.locations.append(CMLocation(self.player, loc_name, loc_data.code, region))
        self.multiworld.regions.append(region)

    def generate_basic(self):
        (self.multiworld.get_location("Checkmate Maxima", self.player).
         place_locked_item(CMItem("Victory", ItemClassification.progression, 4_065, self.player)))

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)


def get_excluded_items(multiworld: MultiWorld, player: int) -> Set[str]:
    excluded_items: Set[str] = set()

    for item in multiworld.precollected_items[player]:
        excluded_items.add(item.name)

    excluded_items_option = getattr(multiworld, 'excluded_items', [])

    excluded_items.update(excluded_items_option[player].value)

    return excluded_items


def assign_starter_items(multiworld: MultiWorld, player: int, excluded_items: Set[str],
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
                                  item not in non_local_items and item not in excluded_items)
        if not local_basic_unit:
            raise Exception("At least one early chessman must be local")

        item = create_item_with_correct_settings(player, multiworld.random.choice(local_basic_unit))
        multiworld.get_location("Bongcloud Once", player).place_locked_item(item)
        locked_locations.append("Bongcloud Once")

        return [item]
    else:
        return []
