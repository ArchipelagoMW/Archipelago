from .Options import InscryptionOptions, Goal, EpitaphPiecesRandomization, PaintingChecksBalancing
from .Items import act1_items, act2_items, act3_items, filler_items, base_id, InscryptionItem, ItemDict
from .Locations import act1_locations, act2_locations, act3_locations, regions_to_locations
from .Regions import inscryption_regions_all, inscryption_regions_act_1
from typing import Dict, Any
from . import Rules
from BaseClasses import Region, Item, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld


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

    bug_report_page = "https://github.com/DrBibop/Archipelago_Inscryption/issues"


class InscryptionWorld(World):
    """
    Inscryption is an inky black card-based odyssey that blends the deckbuilding roguelike,
    escape-room style puzzles, and psychological horror into a blood-laced smoothie.
    Darker still are the secrets inscrybed upon the cards...
    """
    game = "Inscryption"
    web = InscrypWeb()
    options_dataclass = InscryptionOptions
    options: InscryptionOptions
    all_items = act1_items + act2_items + act3_items + filler_items
    item_name_to_id = {item["name"]: i + base_id for i, item in enumerate(all_items)}
    all_locations = act1_locations + act2_locations + act3_locations
    location_name_to_id = {location: i + base_id for i, location in enumerate(all_locations)}
    required_epitaph_pieces_count = 9
    required_epitaph_pieces_name = "Epitaph Piece"

    def generate_early(self) -> None:
        self.all_items = [item.copy() for item in self.all_items]

        if self.options.epitaph_pieces_randomization == EpitaphPiecesRandomization.option_all_pieces:
            self.required_epitaph_pieces_name = "Epitaph Piece"
            self.required_epitaph_pieces_count = 9
        elif self.options.epitaph_pieces_randomization == EpitaphPiecesRandomization.option_in_groups:
            self.required_epitaph_pieces_name = "Epitaph Pieces"
            self.required_epitaph_pieces_count = 3
        else:
            self.required_epitaph_pieces_name = "Epitaph Pieces"
            self.required_epitaph_pieces_count = 1

        if self.options.painting_checks_balancing == PaintingChecksBalancing.option_balanced:
            self.all_items[6]["classification"] = ItemClassification.progression
            self.all_items[11]["classification"] = ItemClassification.progression

        if self.options.painting_checks_balancing == PaintingChecksBalancing.option_force_filler \
                and self.options.goal == Goal.option_first_act:
            self.all_items[3]["classification"] = ItemClassification.filler

        if self.options.epitaph_pieces_randomization != EpitaphPiecesRandomization.option_all_pieces:
            self.all_items[len(act1_items) + 3]["count"] = self.required_epitaph_pieces_count

    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_items)["name"]

    def create_item(self, name: str) -> Item:
        item_id = self.item_name_to_id[name]
        item_data = self.all_items[item_id - base_id]
        return InscryptionItem(name, item_data["classification"], item_id, self.player)

    def create_items(self) -> None:
        nb_items_added = 0
        useful_items = self.all_items.copy()

        if self.options.goal != Goal.option_first_act:
            useful_items = [item for item in useful_items
                            if not any(filler_item["name"] == item["name"] for filler_item in filler_items)]
            if self.options.epitaph_pieces_randomization == EpitaphPiecesRandomization.option_all_pieces:
                useful_items.pop(len(act1_items) + 3)
            else:
                useful_items.pop(len(act1_items) + 2)
        else:
            useful_items = [item for item in useful_items
                            if any(act1_item["name"] == item["name"] for act1_item in act1_items)]

        for item in useful_items:
            for _ in range(item["count"]):
                new_item = self.create_item(item["name"])
                self.multiworld.itempool.append(new_item)
                nb_items_added += 1

        filler_count = len(self.all_locations if self.options.goal != Goal.option_first_act else act1_locations)
        filler_count -= nb_items_added

        for i in range(filler_count):
            index = i % len(filler_items)
            filler_item = filler_items[index]
            new_item = self.create_item(filler_item["name"])
            self.multiworld.itempool.append(new_item)

    def create_regions(self) -> None:
        used_regions = inscryption_regions_all if self.options.goal != Goal.option_first_act \
            else inscryption_regions_act_1
        for region_name in used_regions.keys():
            self.multiworld.regions.append(Region(region_name, self.player, self.multiworld))

        for region_name, region_connections in used_regions.items():
            region = self.get_region(region_name)
            region.add_exits(region_connections)
            region.add_locations({
                location: self.location_name_to_id[location] for location in regions_to_locations[region_name]
            })

    def set_rules(self) -> None:
        Rules.InscryptionRules(self).set_all_rules()

    def fill_slot_data(self) -> Dict[str, Any]:
        return self.options.as_dict(
            "death_link",
            "act1_death_link_behaviour",
            "goal",
            "randomize_codes",
            "randomize_deck",
            "randomize_sigils",
            "optional_death_card",
            "skip_tutorial",
            "skip_epilogue",
            "epitaph_pieces_randomization"
        )
