from .Options import inscryption_options
from .Items import act1_items, act2_items, act3_items, filler_items, base_id, InscryptionItem, ItemDict
from .Locations import act1_locations, act2_locations, act3_locations, locations_to_progress_type, regions_to_locations
from .Regions import inscryption_regions_all, inscryption_regions_act_1
from typing import Dict, Any
from . import Rules
from BaseClasses import Region, Item, Tutorial
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
    all_locations = act1_locations + act2_locations + act3_locations
    location_name_to_id = {location: i + base_id for i, location in enumerate(all_locations)}

    def create_item(self, name: str) -> Item:
        item_id = self.item_name_to_id[name]
        item_data = self.all_items[item_id - base_id]
        return InscryptionItem(name, item_data['classification'], item_id, self.player)

    def create_items(self) -> None:
        nb_items_added = 0
        useful_items = (act1_items + act2_items + act3_items) if self.multiworld.goal[self.player] <= 1 else act1_items

        if self.multiworld.goal[self.player] <= 1:
            if self.multiworld.epitaph_pieces_randomization[self.player].value == 0:
                useful_items.remove(act2_items[3])
            elif self.multiworld.epitaph_pieces_randomization[self.player].value == 1:
                useful_items.remove(act2_items[2])
            else:
                useful_items.remove(act2_items[2])
                useful_items[len(act1_items) + 2]['count'] = 1

        for item in useful_items:
            for _ in range(item["count"]):
                new_item = self.create_item(item['name'])
                self.multiworld.itempool.append(new_item)
                nb_items_added += 1

        filler_count = len(self.all_locations if self.multiworld.goal[self.player] <= 1 else act1_locations)
        filler_count -= nb_items_added

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
                location: self.location_name_to_id[location] for location in regions_to_locations[region_name]
            })
            for name, progress_type in locations_to_progress_type.items():
                loc = next((x for x in region.locations if x.name == name), None)
                if loc is not None:
                    loc.progress_type = progress_type

    def set_rules(self) -> None:
        Rules.InscryptionRules(self).set_all_rules()

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "deathlink": self.multiworld.deathlink[self.player].value,
            "act1_deathlink_behaviour": self.multiworld.act1_deathlink_behaviour[self.player].value,
            "goal": self.multiworld.goal[self.player].value,
            "randomize_codes": self.multiworld.randomize_codes[self.player].value,
            "randomize_deck": self.multiworld.randomize_deck[self.player].value,
            "randomize_abilities": self.multiworld.randomize_abilities[self.player].value,
            "optional_death_card": self.multiworld.optional_death_card[self.player].value,
            "skip_tutorial": self.multiworld.skip_tutorial[self.player].value,
            "epitaph_pieces_randomization": self.multiworld.epitaph_pieces_randomization[self.player].value
        }
