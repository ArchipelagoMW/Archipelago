from typing import Set

from worlds.AutoWorld import World
from .Items import item_table, default_pool
from .Locations import lookup_name_to_id
from .Rules import set_rules, location_rules
from .Regions import locations_by_region, connectors
from .Options import options
from BaseClasses import Region, Item, Location, Entrance, ItemClassification


class OriBlindForest(World):
    game: str = "Ori and the Blind Forest"

    topology_present = True
    data_version = 1

    item_name_to_id = item_table
    location_name_to_id = lookup_name_to_id

    option_definitions = options

    hidden = True

    def generate_early(self):
        logic_sets = {"casual-core"}
        for logic_set in location_rules:
            if logic_set != "casual-core" and getattr(self.multiworld, logic_set.replace("-", "_")):
                logic_sets.add(logic_set)
        self.logic_sets = logic_sets

    set_rules = set_rules

    def create_region(self, name: str):
        return Region(name, self.player, self.multiworld)

    def create_regions(self):
        world = self.multiworld
        menu = self.create_region("Menu")
        world.regions.append(menu)
        start = Entrance(self.player, "Start Game", menu)
        menu.exits.append(start)

        # workaround for now, remove duplicate locations
        already_placed_locations = set()

        for region_name, locations in locations_by_region.items():
            locations -= already_placed_locations
            already_placed_locations |= locations
            region = self.create_region(region_name)
            if region_name == "SunkenGladesRunaway":  # starting point
                start.connect(region)
            region.locations = {Location(self.player, location, lookup_name_to_id[location], region)
                                for location in locations}
            world.regions.append(region)

        for region_name, exits in connectors.items():
            parent = world.get_region(region_name, self.player)
            for exit in exits:
                connection = Entrance(self.player, exit, parent)
                connection.connect(world.get_region(exit, self.player))
                parent.exits.append(connection)

    def generate_basic(self):
        for item_name, count in default_pool.items():
            self.multiworld.itempool.extend([self.create_item(item_name) for _ in range(count)])

    def create_item(self, name: str) -> Item:
        return Item(name,
                    ItemClassification.progression if not name.startswith("EX") else ItemClassification.filler,
                    item_table[name], self.player)
