#Snagged from APQuest, not actually sure what these are.

from collections.abc import Mapping
from typing import Any

# Imports base Archipelago autoworld.
from worlds.AutoWorld import World

# Imports our files. We use capitals for the paths.
from . import Items, Locations, Options, Regions, Rules

class SDWorld(World):
    """
    This will describe Silver Daze eventually
    """
    game = "Silver Daze"

    #Webworld will be important eventually so we might as well add that now.
    #web = WebWorld.SilverDazeWebWorld()

    options_dataclass = Options.SilverDazeOptions
    options: Options.SilverDazeOptions

    #Sawyer: We used to define these here but we'll do it in Regions and Items instead.
    location_name_to_id = Locations.LOCATION_NAME_TO_ID
    #item_name_to_id = Items.ITEM_NAME_TO_ID
    item_name_to_id = Items.item_table

    #Sawyer: You start in Geo's Room, after all.
    origin_region_name = "Geo_Room"

    #Sawyer: These are important rules, check APQuest for an explanation.
    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    #Sawyer: Time to make items, of course!
    def create_item(self, name: str) -> Items.SDItem:
        return Items.create_item_with_correct_classification(self, name)

    #Sawyer: We should make sure we have filler items too.
    #Sawyer: ATM these will just be Heal Tokens but honestly most Tokens work, maybe even some weak cards.
    def get_filler_item_name(self) -> str:
        return Items.get_random_filler_item_name(self)

    #Sawyer: APQuest says to add this so we're adding it, not sure how it works yet.
    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict(
            #Sawyer: ATM we don't have any of these but that can change.
        )