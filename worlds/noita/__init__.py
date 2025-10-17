from BaseClasses import Item, Tutorial
from worlds.AutoWorld import WebWorld, World
from typing import Dict, Any
from . import events, items, locations, regions, rules
from .options import NoitaOptions


class NoitaWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Noita integration for Archipelago multiworld games.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Heinermann", "ScipioWright", "DaftBrit"]
    )]
    theme = "partyTime"
    bug_report_page = "https://github.com/DaftBrit/NoitaArchipelago/issues"


# Keeping World slim so that it's easier to comprehend
class NoitaWorld(World):
    """
    Noita is a magical action roguelite set in a world where every pixel is physically simulated. Fight, explore, melt,
    burn, freeze, and evaporate your way through the procedurally generated world using wands you've created yourself.
    """

    game = "Noita"
    options: NoitaOptions
    options_dataclass = NoitaOptions

    item_name_to_id = items.item_name_to_id
    location_name_to_id = locations.location_name_to_id

    item_name_groups = items.item_name_groups
    location_name_groups = locations.location_name_groups

    web = NoitaWeb()

    def generate_early(self) -> None:
        if not self.player_name.isascii():
            raise Exception("Noita yaml's slot name has invalid character(s).")

    # Returned items will be sent over to the client
    def fill_slot_data(self) -> Dict[str, Any]:
        return self.options.as_dict("death_link", "victory_condition", "path_option", "hidden_chests",
                                    "pedestal_checks", "orbs_as_checks", "bosses_as_checks", "extra_orbs", "shop_price")

    def create_regions(self) -> None:
        regions.create_all_regions_and_connections(self)

    def create_item(self, name: str) -> Item:
        return items.create_item(self.player, name)

    def create_items(self) -> None:
        items.create_all_items(self)

    def set_rules(self) -> None:
        rules.create_all_rules(self)

    def get_filler_item_name(self) -> str:
        return self.random.choice(items.filler_items)
