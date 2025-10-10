from BaseClasses import Item, Tutorial
from worlds.AutoWorld import World, WebWorld
from .locations import get_location_names, get_total_locations
from .items import create_item, create_itempool, item_table, HEXCELLS_LEVEL_ITEMS 
from .options import HexcellsInfiniteOptions, LevelUnlockType
from .regions import create_regions
from .rules import set_rules

class HexcellsInfiniteWebWorld(WebWorld):
    theme = "partyTime"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Hexcells Infinite for Archipelago. "
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "setup_en.md",
        "setup/en",
        ["ExpandedReality"]
    )]

class HexcellsInfiniteWorld(World):
    """
    Hexcells Infinite is a deterministic minesweeper puzzle game. \nIf you like Minesweeper, but hate guessing, this is the game for you.
    """
    game = "Hexcells Infinite"
    item_name_to_id = {name: data.ap_code for name, data in item_table.items()}
    location_name_to_id = get_location_names()
    options_dataclass = HexcellsInfiniteOptions
    options: HexcellsInfiniteOptions
    web = HexcellsInfiniteWebWorld()

    def generate_early(self):
        if self.options.LevelUnlockType == LevelUnlockType.option_individual:
            level_start = self.random.choice(HEXCELLS_LEVEL_ITEMS)
            self.multiworld.push_precollected(create_item(self, level_start))
    
    def create_regions(self):
        create_regions(self)

    def set_rules(self):
        set_rules(self)

    def create_items(self):
        self.multiworld.itempool += create_itempool(self)

    def create_item(self, name: str) -> Item:
        return create_item(self, name)
    
    def fill_slot_data(self) -> dict[str, object]:
        slot_data: dict[str, object] = {
            "options": {
                  "RequirePerfectClears":     self.options.RequirePerfectClears.value,
                  "PuzzleOptions":            self.options.PuzzleOptions.value,
                  "EnableShields":            self.options.EnableShields.value,
                  "LevelUnlockType":          self.options.LevelUnlockType.value,
                  "HardGeneration":           self.options.HardGeneration.value
            },
            "Seed": self.multiworld.seed_name,
            "Slot": self.player_name,
            "TotalLocations": get_total_locations(self)
        }

        return slot_data
