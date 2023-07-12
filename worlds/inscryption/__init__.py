from .Options import inscryption_options
from .Items import item_table, base_id, InscryptionItem, ItemDict
from .Locations import location_table, LocDict
from .Regions import inscryption_regions
from worlds.generic.Rules import add_rule, set_rule, forbid_item
from worlds.AutoWorld import World
from Utils import get_options, output_path
from typing import Dict, ClassVar, Set, List, Tuple
from collections import Counter
from . import Rules
from BaseClasses import Region, Entrance, Location, Item, Tutorial, ItemClassification
from ..AutoWorld import World, WebWorld


class InscrypWeb(WebWorld):
    theme = "dirt"

    guide_en = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Inscryption Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["DrBibop"]
    )]

    guide_fr = [Tutorial(
        "Multiworld Setup Guide",
        "Un guide pour configurer Inscryption Archipelago Multiworld",
        "Français",
        "setup_fr.md",
        "setup/fr",
        ["Glowbuzz"]
    )]

    tutorials = [guide_en, guide_fr]


class InscryptionWorld(World):
    """
    Inscryption is an inky black card-based odyssey that blends the deckbuilding roguelike,
    escape-room style puzzles, and psychological horror into a blood-laced smoothie.
    Darker still are the secrets inscrybed upon the cards...
    """
    game = "Inscryption"
    web = InscrypWeb()
    option_definitions = inscryption_options
    item_name_to_id = {item['name']: i + base_id for i, item in enumerate(item_table)}
    location_name_to_id = {location['name']: i + base_id for i, location in enumerate(location_table)}

    def create_item(self, name: str) -> Item:
        item_id = self.item_name_to_id[name]
        item_data = item_table[item_id - base_id]
        return InscryptionItem(name, item_data['classification'], item_id, self.player)

    def create_items(self) -> None:
        unique_items = [item for item in item_table if item['classification'] != ItemClassification.filler]
        for item in unique_items:
            new_item = self.create_item(item['name'])
            self.multiworld.itempool.append(new_item)

        filler_count = len(location_table) - len(unique_items)
        filler_items = [item for item in item_table if item not in unique_items]
        for i in range(filler_count):
            index = i % len(filler_items)
            filler_item = filler_items[index]
            new_item = self.create_item(filler_item['name'])
            self.multiworld.itempool.append(new_item)

    def create_regions(self) -> None:
        for region_name in inscryption_regions.keys():
            self.multiworld.regions.append(Region(region_name, self.player, self.multiworld))

        for region_name, region_connections in inscryption_regions.items():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_exits(region_connections)
            region.add_locations({
                location['name']: self.location_name_to_id[location['name']] for location in location_table
                if location['region'] == region_name
            })

    def set_rules(self) -> None:
        Rules.InscryptionRules(self).set_all_rules()
