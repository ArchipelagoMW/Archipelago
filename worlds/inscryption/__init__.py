from .Options import inscryption_options
from .Items import act1_items, act2_items, act3_items, filler_items, base_id, InscryptionItem, ItemDict
from .Locations import location_table, LocDict
from .Regions import inscryption_regions_all, inscryption_regions_act_1
from typing import Dict, Any
from . import Rules
from BaseClasses import Region, Item, Tutorial, ItemClassification
from ..AutoWorld import World, WebWorld


class InscrypWeb(WebWorld):
    theme = "dirt"

    guide_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Inscryption Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["DrBibop"]
    )

    guide_fr = Tutorial(
        "Multiworld Setup Guide",
        "Un guide pour configurer Inscryption Archipelago Multiworld",
        "Français",
        "setup_fr.md",
        "setup/fr",
        ["Glowbuzz"]
    )

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
    all_items = act1_items + act2_items + act3_items + filler_items
    item_name_to_id = {item['name']: i + base_id for i, item in enumerate(all_items)}
    location_name_to_id = {location['name']: i + base_id for i, location in enumerate(location_table)}

    def create_item(self, name: str) -> Item:
        item_id = self.item_name_to_id[name]
        item_data = self.all_items[item_id - base_id]
        return InscryptionItem(name, item_data['classification'], item_id, self.player)

    def create_items(self) -> None:
        nb_items_added = 0
        useful_items = (act1_items + act2_items + act3_items) if self.multiworld.goal[self.player] <= 1 else act1_items
        for item in useful_items:
            for _ in range(item["count"]):
                new_item = self.create_item(item['name'])
                self.multiworld.itempool.append(new_item)
                nb_items_added += 1

        filler_count = len(location_table) - nb_items_added
        for i in range(filler_count):
            index = i % len(filler_items)
            filler_item = filler_items[index]
            new_item = self.create_item(filler_item['name'])
            self.multiworld.itempool.append(new_item)

    def create_regions(self) -> None:
        used_regions = inscryption_regions_all if self.multiworld.goal[self.player] <= 1 else inscryption_regions_act_1
        for region_name in used_regions.keys():
            self.multiworld.regions.append(Region(region_name, self.player, self.multiworld))

        for region_name, region_connections in used_regions.items():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_exits(region_connections)
            region.add_locations({
                location['name']: self.location_name_to_id[location['name']] for location in location_table
                if location['region'] == region_name
            })

    def set_rules(self) -> None:
        Rules.InscryptionRules(self).set_all_rules()

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "deathlink": self.multiworld.deathlink[self.player].value,
            "goal": self.multiworld.goal[self.player].value,
            "randomize_codes": self.multiworld.randomize_codes[self.player].value,
            "randomize_deck": self.multiworld.randomize_deck[self.player].value,
            "randomize_abilities": self.multiworld.randomize_abilities[self.player].value,
            "optional_death_card": self.multiworld.optional_death_card[self.player].value,
        }
