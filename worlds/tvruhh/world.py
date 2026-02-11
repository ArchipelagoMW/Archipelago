from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

from . import items, locations, regions, rules, web_world
from . import options as tvruhh_options


class TVRUHHWorld(World):
    """
    The Void Rains Upon Her Heart is a game where you help a few alien girls on their journey to accept themselves.
    Love Monsters, remember their gifts and show The Void what love is capable of, in this roguelike bullet-hell game!
    """

    game = "TVRUHH"

    web_world = web_world.TVRUHHWebWorld()

    options_dataclass = tvruhh_options.TVRUHHOptions
    options: tvruhh_options.TVRUHHOptions

    location_name_to_id = locations.requestbbl()
    item_name_to_id = items.requestbbl()

    origin_region_name = "Start"

    bonus_gift_locations = 0

    def create_regions(self) -> None: #also creates all items
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)
    
    def set_rules(self) -> None:
        rules.set_all_rules(self)
    
    def create_items(self) -> None:
        items.create_all_items(self)
        locations.create_extra_locations(self, self.bonus_gift_locations+self.options.bonus_gift_amount.value)
    
    def create_item(self, name: str, chosenList = items.filler_item_list) -> items.TVRUHHItem:
        return items.create_item_with_default_classification(self, name, chosenList)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    # below function causes error, allows seeing all the print debugs (because those are not saved in the log files for some reason)
    # def generate_output(self):
    #     items.error()

    def fill_slot_data(self) -> Mapping[str, Any]:
        return_dict = {}
        return_dict.update(self.options.as_dict(
            "bonus_gift_chance"
        ))
        bonus_count = 0
        for x in self.location_name_to_id:
            if x.__contains__("Bonus Gift "):
                bonus_count += 1
        return_dict.update({"Bonus Gift Count": bonus_count})
        return return_dict
