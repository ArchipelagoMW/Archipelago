from typing import ClassVar, Dict

from BaseClasses import Tutorial, ItemClassification
from Utils import visualize_regions
from worlds.AutoWorld import WebWorld, World
from .constants import POTION_CRAFT
from .data import Direction
from .data.items import all_items, get_ingredients_by_direction
from .data.locations import all_locations
from .items import PotionCraftItem, create_events, create_items
from .locations import create_regions, create_locations, create_entrances
from .options import potion_craft_option_groups, PotionCraftOptions
from .world_base import PotionCraftBase


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

class PotionCraftWorld(PotionCraftBase):
    """
    Potion Craft is a game that...
    """
    game = POTION_CRAFT
    web = PotionCraftWeb()
    option_groups = potion_craft_option_groups
    item_name_to_id: ClassVar[Dict[str, int]] = {item.value: item.item_id for item in all_items} #needs list of all possible items
    location_name_to_id: ClassVar[Dict[str, int]] = {loc.value: loc.location_id for loc in all_locations} #needs list of all possible locations

    item_lookup = {item.value: item for item in all_items}

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
        print("Handle option validation")

    def create_regions(self):
        create_regions(self)
        create_locations(self)
        create_entrances(self)

    def create_item(self, item: str) -> PotionCraftItem:
        item_enum = self.item_lookup[item]

        return PotionCraftItem(
            item,
            item_enum.classification,
            item_enum.item_id,
            self.player,
        )

    def create_items(self):
        create_events(self)
        create_items(self)

    def set_rules(self):

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory",
                                                                                      self.player)  # need victory to beat world

    def fill_slot_data(self) -> id:
        return {
            "ModVersion": "0.0.1", #update mods version when you commit, on rider as well
            "Deathlink": self.options.death_link.value
        }

    def generate_output(self, output_directory: str):
        visualize_regions(self.multiworld.get_region("Menu", self.player), f"Player{self.player}.puml",
                          show_entrance_names=True,
                          regions_to_highlight=self.multiworld.get_all_state(self.player).reachable_regions[
                              self.player])
