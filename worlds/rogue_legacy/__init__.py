from typing import List

from BaseClasses import Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import RLItem, RLItemData, filler_items, item_groups, item_table
from .Locations import RLLocation, location_groups, location_table
from .Options import rl_options
from .Regions import region_table


class RLWeb(WebWorld):
    theme = "stone"
    tutorials = [Tutorial(
        "Rogue Legacy Randomizer - Setup Guide",
        "A guide to setting up the Rogue Legacy Randomizer software on your computer. This guide covers single-player, "
        "multiworld, and related software.",
        "English",
        "rogue-legacy_en.md",
        "rogue-legacy/en",
        ["Phar"]
    )]
    bug_report_page = "https://github.com/ThePhar/RogueLegacyRandomizer/issues/new?assignees=&labels=bug&template=" \
                      "report-an-issue---.md&title=%5BIssue%5D"


class RLWorld(World):
    """
    Rogue Legacy is a genealogical rogue-"LITE" where anyone can be a hero. Each time you die, your child will succeed
    you. Every child is unique. One child might be colorblind, another might have vertigo-- they could even be a dwarf.
    But that's OK, because no one is perfect, and you don't have to be to succeed.
    """
    game = "Rogue Legacy"
    option_definitions = rl_options
    data_version = 5
    required_client_version = (0, 4, 2)
    web = RLWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items() if not data.event}
    location_name_to_id = {name: data.address for name, data in location_table.items() if not data.event}
    item_name_groups = item_groups
    location_name_groups = location_groups

    def generate_early(self):
        # Set starting items.
        self.multiworld.push_precollected(self.create_item("Blacksmith"))
        self.multiworld.push_precollected(self.create_item("Enchantress"))
        if self.get_setting("architect") == "start_unlocked":
            self.multiworld.push_precollected(self.create_item("Architect"))

    def create_item(self, name: str) -> RLItem:
        item_data = item_table[name]
        return RLItem(name, item_data.classification, item_data.code, self.player)

    def create_items(self):
        item_pool: List[RLItem] = []
        location_count = len(self.multiworld.get_unfilled_locations(self.player))

        # Create each item we can create.
        for item_data in item_table.values():
            item_pool += [
                self.create_item(item_data.name)
                for _ in range(item_data.creation_quantity(self.multiworld, self.player))
            ]

        # If we didn't generate enough items to fill our locations, generate some filler!
        while len(item_pool) < location_count:
            item_pool.append(self.create_item(self.get_filler_item_name()))

        self.multiworld.itempool += item_pool

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Defeat The Fountain", self.player)

    def create_regions(self):
        # Instantiate Regions
        for region_name in region_table.keys():
            self.multiworld.regions.append(Region(region_name, self.player, self.multiworld))

        # Create locations.
        for location_data in location_table.values():
            # Ignore locations that cannot be created as the appropriate settings are not valid.
            if not location_data.can_create(self.multiworld, self.player):
                continue

            location_data.create_location(self.multiworld, self.player)

        # Connect regions and set access rules.
        for region_name, region_data in region_table.items():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_exits(region_data.exits, {
                exiting_region: lambda state: region_table[exiting_region].rules(state, self.player)
                for exiting_region in region_data.exits
            })

    # TODO: Replace calls to this function with #933's solution, once that PR is merged.
    def get_setting(self, name: str):
        return getattr(self.multiworld, name)[self.player]

    def get_filler_item_name(self) -> str:
        if self.get_setting("include_traps"):
            filler_names = filler_items["names"] + filler_items["trap_names"]
            filler_weights = filler_items["weights"] + filler_items["trap_weights"]
            return self.random.choices(filler_names, filler_weights, k=1)[0]

        return self.random.choices(filler_items["names"], filler_items["weights"], k=1)[0]

    # TODO: Only set required slot data.
    def fill_slot_data(self) -> dict:
        return {option_name: self.get_setting(option_name).value for option_name in rl_options}
