from .Options import inscryption_options
from .Items import item_table, base_id, InscryptionItem, ItemDict
from .Locations import location_table, LocDict
from .Regions import inscryption_regions
from .Rules import inscryption_rules
from worlds.generic.Rules import add_rule, set_rule, forbid_item
from worlds.AutoWorld import World
from Utils import get_options, output_path
from typing import Dict, ClassVar, Set, List, Tuple
from collections import Counter
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
        ["Glowbuzz"]
    )]

    guide_fr = [Tutorial(
        "Multiworld Setup Guide",
        "Un guide pour configurer Inscryption Archipelago Multiworld",
        "English",
        "setup_fr.md",
        "setup/fr",
        ["Glowbuzz"]
    )]

    tutorials = [guide_en, guide_en]


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
        for item in item_table:
            new_item = self.create_item(item['name'])
            self.multiworld.itempool.append(new_item)

    def create_regions(self) -> None:
        local_regions = []
        for name in inscryption_regions:
            r = Region(name, self.player, self.multiworld)
            for dest in inscryption_regions[name]:
                if not(any(ent.name == dest for ent in self.multiworld.get_entrances())):
                    r.exits.append(Entrance(self.player, dest, r))
                else:
                    r.exits.append(self.multiworld.get_entrance(dest, self.player))
            for loc in filter(lambda location: location['region'] == name, location_table):
                r.locations.append(Location(self.player, loc['name'], None, r))
            self.multiworld.regions.append(r)
            local_regions.append(r)
        for region in local_regions:
            for entrance in region.exits:
                entrance.connect(self.multiworld.get_region(entrance.name, self.player))

    def set_rules(self) -> None:
        set_rule(self.multiworld.get_entrance("Act 2", self.player),
                 lambda state: state.has("Film Roll", self.player))
        for item in inscryption_rules:
            for location in inscryption_rules[item]:
                add_rule(self.multiworld.get_location(location, self.player),
                         lambda state: state.has(item, self.player))
