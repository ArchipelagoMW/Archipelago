from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

from . import items, locations, regions, rules, web_world
from . import options as Nothing_options

class NothingWorld(World):
    """
    Nothing is a minimilistic game about doing nothing for progressive longer times
    good games need at least 86400 check (*not really)
    """

    game = "nothing_archipelago"

    web = web_world.NothingWebWorld()

    options_dataclass = Nothing_options.NothingOptions
    options: Nothing_options.NothingOptions

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "start"

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name) -> items.Nothing_Archipelago_Item:
        return items.create_item_with_correct_classification(self, name)
    
    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)
    
    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict(
            "goal","shop_upgrades","shop_colors","shop_music","shop_sounds","gift_coins",
            "milestone_interval","timecap_interval","Starting_coin_count","Death_link",
            "Death_link_mercy","Time_dilation")