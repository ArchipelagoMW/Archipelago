from typing import ClassVar, Dict

from BaseClasses import Tutorial, ItemClassification
from Utils import visualize_regions
from worlds.AutoWorld import WebWorld, World
from worlds.potion_craft.Items import PotionCraftItem, create_potion_craft_items, full_item_dict, Direction, \
    get_ingredients_by_direction
from worlds.potion_craft.Locations import create_potion_craft_locations, get_all_potion_craft_locations
from worlds.potion_craft.Options import potion_craft_option_groups, PotionCraftOptions
from worlds.potion_craft.Regions import create_potion_craft_regions, connect_potion_craft_regions
from worlds.potion_craft.Rules import set_rules


class PotionCraftWeb(WebWorld):
    theme = "grass"

    setup_en = Tutorial(
        tutorial_name="Multiworld Setup Guide",
        description="A guide to setting up the Potion Craft randomizer connected to an Archipelago Multiworld.",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=["Pink,FyreDay"]
    )

    tutorials = [setup_en]

class PotionCraftWorld(World):
    """
    Potion Craft is a game that...
    """
    game = "Potion Craft"
    web = PotionCraftWeb()
    options_dataclass = PotionCraftOptions
    options: PotionCraftOptions
    option_groups = potion_craft_option_groups
    item_name_to_id: ClassVar[Dict[str, int]] = {item_name: item_data.code for item_name, item_data in full_item_dict.items()} #needs list of all possible items
    location_name_to_id: ClassVar[Dict[str, int]] = {loc_name: loc_data.code for loc_name, loc_data in get_all_potion_craft_locations().items()} #needs list of all possible locations

    item_name_groups = {
        "north": set(get_ingredients_by_direction(Direction.NORTH)),
        "south": set(get_ingredients_by_direction(Direction.SOUTH)),
        "east": set(get_ingredients_by_direction(Direction.EAST)),
        "west": set(get_ingredients_by_direction(Direction.WEST)),
    }

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.itempool = []
        self.locations = {}

    def generate_early(self) -> None:
        self.locations = create_potion_craft_locations(self)

    def create_regions(self):
        create_potion_craft_regions(self, self.locations)
        connect_potion_craft_regions(self)

    def create_item(self, item: str) -> PotionCraftItem:
        return PotionCraftItem(item, ItemClassification.useful, self.item_name_to_id[item], self.player)

    def create_items(self):
        create_potion_craft_items(self)

    def set_rules(self):
        set_rules(self)

    def fill_slot_data(self) -> id:
        return {
            "ModVersion": "0.0.1" #update mods version when you commit, on rider as well
        }

    def generate_output(self, output_directory: str):
        visualize_regions(self.multiworld.get_region("Menu", self.player), f"Player{self.player}.puml",
                          show_entrance_names=True,
                          regions_to_highlight=self.multiworld.get_all_state(self.player).reachable_regions[
                              self.player])
