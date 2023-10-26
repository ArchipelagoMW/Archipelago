from BaseClasses import Item, Tutorial
from worlds.AutoWorld import WebWorld, World
from typing import Dict, Any
from . import Events, Items, Locations, Options, Regions, Rules
from .Options import NoitaOptions


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

    item_name_to_id = Items.item_name_to_id
    location_name_to_id = Locations.location_name_to_id

    item_name_groups = Items.item_name_groups
    location_name_groups = Locations.location_name_groups
    data_version = 2

    web = NoitaWeb()

    # Returned items will be sent over to the client
    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "start_inventory_from_pool": self.options.start_inventory_from_pool.value,
            "death_link": self.options.death_link.value,
            "bad_effects": self.options.bad_effects.value,
            "victory_condition": self.options.victory_condition.value,
            "path_option": self.options.path_option.value,
            "hidden_chests": self.options.hidden_chests.value,
            "pedestal_checks": self.options.pedestal_checks.value,
            "orbs_as_checks": self.options.orbs_as_checks.value,
            "bosses_as_checks": self.options.bosses_as_checks.value,
            "extra_orbs": self.options.extra_orbs.value,
            "shop_price": self.options.shop_price.value
        }

    def create_regions(self) -> None:
        Regions.create_all_regions_and_connections(self)

    def create_item(self, name: str) -> Item:
        return Items.create_item(self.player, name)

    def create_items(self) -> None:
        Items.create_all_items(self)

    def set_rules(self) -> None:
        Rules.create_all_rules(self)

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(Items.filler_items)
