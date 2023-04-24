from typing import List
from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .Options import ls_options
from .Items import *
from .Regions import *
from .Locations import *
from .Rules import *

# TODO: Docs
class LandstalkerWeb(WebWorld):
    theme = "grass"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Landstalker Randomizer software on your computer. This guide covers single-player, "
        "multiworld, and related software.",
        "English",
        "landstalker_en.md",
        "landstalker/en",
        ["Dinopony"]
    )]
    bug_report_page = "https://github.com/Dinopony/randstalker/issues/"


class LandstalkerWorld(World):
    """
    Landstalker: The Treasures of King Nole is a classic Action-RPG with an isometric view (also known as "2.5D").
    You play Nigel, a treasure hunter exploring the island of Mercator trying to find the legendary treasure.
    Roam freely on the island, get stronger to beat dungeons and gather the required key items in order to reach the
    hidden palace and claim the treasure.
    """
    game = "Landstalker"
    option_definitions = ls_options
    topology_present = True
    data_version = 0
    required_client_version = (0, 3, 8)
    web = LandstalkerWeb()

    item_name_to_id = build_item_name_to_id_table()
    location_name_to_id = build_location_name_to_id_table()

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.regions_table: Dict[str, Region] = {}
        self.dark_dungeon_id = "None"
        self.dark_region_ids = []

    def get_setting(self, name: str):
        return getattr(self.multiworld, name)[self.player]

    def fill_slot_data(self) -> dict:
        # Put options, locations' contents and some additional data inside slot data
        slot_data = {option_name: self.get_setting(option_name).value for option_name in ls_options}
        slot_data["seed"] = self.multiworld.per_slot_randoms[self.player].randint(0, 4294967295)
        slot_data["dark_region"] = self.dark_dungeon_id
        slot_data["locations"] = {}
        for location in self.multiworld.get_locations(self.player):
            slot_data['locations'][location.name] = {
                "item": location.item.name,
                "player": self.multiworld.get_player_name(location.item.player)
            }
        return slot_data

    def generate_early(self):
        # Randomly pick a set of dark regions where Lantern is needed
        darkenable_regions = get_darkenable_regions()
        self.dark_dungeon_id = self.multiworld.random.choices(list(darkenable_regions.keys()))[0]
        self.dark_region_ids = darkenable_regions[self.dark_dungeon_id]

    def create_item(self, name: str) -> LandstalkerItem:
        data = item_table[name]
        return LandstalkerItem(name, data.classification, BASE_ITEM_ID + data.id, self.player)

    def create_items(self):
        item_pool: List[LandstalkerItem] = []
        for name, data in item_table.items():
            item_pool += [self.create_item(name) for _ in range(0, data.quantity)]

        # Add jewels to the item pool depending on the number of jewels set in generation settings
        jewel_count = self.multiworld.jewel_count[self.player].value
        required_jewels = ["Red Jewel", "Purple Jewel", "Green Jewel", "Blue Jewel", "Yellow Jewel"]
        del required_jewels[jewel_count:]
        item_pool += [self.create_item(name) for name in required_jewels]

        # Fill the rest of the item pool with empty items
        unfilled_location_count = len(self.multiworld.get_unfilled_locations(self.player))
        while len(item_pool) < unfilled_location_count:
            item_pool.append(self.create_item("No Item"))

        self.multiworld.itempool += item_pool

    def create_regions(self):
        self.regions_table = Regions.create_regions(self.multiworld, self.player)
        Locations.create_locations(self.player, self.regions_table, self.location_name_to_id)

    def set_rules(self):
        Rules.create_rules(self.multiworld, self.player, self.regions_table, self.dark_region_ids)

#   def get_filler_item_name(self) -> str:
#       fillers = get_weighted_filler_item_names()
#       return self.multiworld.random.choices(fillers)[0]
