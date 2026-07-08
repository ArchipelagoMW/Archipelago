from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

from . import constants
from . import items, locations, regions, rules, web_world
from . import options as tomba_options  # rename due to a name conflict with World.options


class TombaWorld(World):
    """
    Tomba! is a platform/adventure/puzzle game for the PSX
    """

    game = constants.GAME
    web = web_world.APQuestWebWorld()

    options_dataclass = tomba_options.TombaOptions
    options: tomba_options.TombaOptions

    location_name_to_id  = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = constants.VILLAGE_OF_ALL_BEGINNINGS

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.TombaItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {}
