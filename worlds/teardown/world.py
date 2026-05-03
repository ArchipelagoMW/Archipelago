from worlds.AutoWorld import World

from . import items, locations, regions, rules, web_world
from . import options as teardown_options
from.items import item_name_groups


class TeardownWorld(World):
    """
    Teardown is a demolition and heist planning game where you work for clients doing jobs to get each other.
    You're the one working for both sides, doing missions for one after destroying their stuff.
    """

    game = "Teardown"

    web = web_world.TeardownWebWorld()

    options_dataclass = teardown_options.TeardownOptions
    options: teardown_options.TeardownOptions

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Main Menu"

    item_name_groups = item_name_groups

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.TeardownItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    #def fill_slot_data(self) -> Mapping[str, Any]:
    #    # If you need access to the player's chosen options on the client side, there is a helper for that.
    #    return self.options.as_dict(
    #        "Bonus_level", "trap_chance"
    #    )
