from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

from . import items, locations, options, regions, rules, web_world

class CatQuestWorld(World):
    """
    Cat Quest is a small open world ARPG set in a cute world full of cats and cat puns. 
    Slash and dodge enemies while completing quests, dungeons and obtaining new gear.
    """

    game = "Cat Quest"
    web = web_world.CatQuestWebWorld()

    options_dataclass = options.CatQuestOptions
    options: options.CatQuestOptions

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Felingard"

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.CatQuestItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict(
            "goal", "include_temples", "skill_upgrade"
        )
    