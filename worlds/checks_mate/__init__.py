from typing import List

from BaseClasses import Tutorial, Region, RegionType, ItemClassification
from worlds.AutoWorld import WebWorld, World
from .Options import cm_options
from .Items import CMItem, item_table
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
        ["rft50"]
    )]


class CMWorld(World):
    """
    Checksmate is a game where you play chess, but all of your pieces were scattered across the multiworld.
    You win when you checkmate the opposing king!
    """
    game: str = "ChecksMate"
    option_definitions = cm_options
    data_version = 0
    required_client_version = (0, 4, 3)
    web = CMWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}

    item_name_groups = {
        "Pawn": {"Pawn A", "Pawn B", "Pawn C", "Pawn D", "Pawn E", "Pawn F", "Pawn G", "Pawn H"}
    }

    item_pool: List[CMItem] = []
    prefill_items: List[CMItem] = []

    def setting(self, name: str):
        return getattr(self.multiworld, name)[self.player]

    def fill_slot_data(self) -> dict:
        return {option_name: self.setting(option_name).value for option_name in cm_options}

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
