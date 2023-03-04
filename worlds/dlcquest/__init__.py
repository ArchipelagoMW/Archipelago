import typing
from BaseClasses import Tutorial
from worlds.AutoWorld import World, WebWorld
from .Items import DLCquestItem, item_table, create_items
from .Locations import location_table, DLCquestLocation
from .Options import DLCquest_options
from .Rules import set_rules

client_version = 0

class DLCqwebworld(WebWorld):
    tutorials = [Tutorial(
        "magic it is "
    )]

class DLCqworld(World):
    """
    DLCquest is a metroid ish game where everything is an in-game dlc.
    """
    game: str = "DLCquest"
    topology_present = False
    web = DLCqwebworld

    item_name_to_id = item_table
    location_name_to_id = location_table

    data_version = 0

    option_definitions = DLCquest_options

    def create_regions(self):
        create_regions(self.multiworld, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.player, self.option)

    def create_event(self, event: str):
        return DLCquestItem(event, True, None, self.player)

    def create_items(self):
        locations_count = len([location
                               for location in self.multiworld.get_locations(self.player)
                               if not location.event])

        items_to_exclude = [excluded_items
                            for excluded_items in self.multiworld.precollected_items[self.player]]

        created_items = create_items(self.create_item, locations_count + len(items_to_exclude), self.options,
                                     self.multiworld.random)
        created_items += create_items(self.create_item,)
        self.multiworld.itempool += created_items



    def create_item(self, item: Union[str, ItemData]) -> DLCquestItem:
        if isinstance(item, str):
            item = item_table[item]

        return DLCquestItem(item.name, item.classification, item.code, self.player)



    def fill_slot_data(self):
        return {
            "DeathLink": self.multiworld.death_link[self.player].value
        }

