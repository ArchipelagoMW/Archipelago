from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

from . import items, locations, regions, rules, names, web_world
from . import options as gens_options

class SonicGensWorld(World):
    """
    Sonic Generations (2011)
    """

    game = names.GameName
    web = web_world.SonicGensWebWorld()
    options_dataclass = gens_options.SonicGensOptions
    options: gens_options.SonicGensOptions

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.get_item_names_to_id()

    origin_region_name = names.Regions.WSClassic

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)
    
    def create_items(self) -> None:
        items.create_all_items(self)
    
    def create_item(self, name: str) -> items.SonicGensItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)
