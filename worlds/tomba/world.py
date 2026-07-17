from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

from . import constants
from . import locations, regions, rules, web_world
from . import (
    options as tomba_options,
)
from .constants import Regions
from .locations import LocationHandler
from .items import ItemHandler, TombaItem


class TombaWorld(World):
    """
    Tomba! is a platform/adventure/puzzle game for the PSX
    """

    game = constants.GAME
    web = web_world.APQuestWebWorld()

    options_dataclass = tomba_options.TombaOptions
    options: tomba_options.TombaOptions

    location_name_to_id = LocationHandler.name_to_id
    item_name_to_id = ItemHandler.name_to_id

    origin_region_name = Regions.VILLAGE_OF_ALL_BEGINNINGS

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        ItemHandler.create_all_items(self)

    def create_item(self, name: str) -> TombaItem:
        return ItemHandler.create_item(self, name)

    def get_filler_item_name(self) -> str:
        return ItemHandler.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data = {"world_version": self.world_version.as_simple_string()}

        return slot_data
