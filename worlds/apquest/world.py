# Imports of base Archipelago modules must be absolute.
from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import WebWorld, World

# Imports of your world's files must be relative.
from . import items, locations, regions, rules
from .options import APQuestOptions, option_groups, option_presets


class APQuestWebWorld(WebWorld):
    game = "APQuest"

    option_groups = option_groups
    options_presets = option_presets

# The world class is the heart and soul of an apworld implementation.
# It holds all the data and functions required to build the world and submit it to the multiworld generator.
# You could have all your world code in just this one class, but for readability and better structure,
# this implementation choses to split up the world functionality over a few different files, each covering one topic.
# These files are: regions.py, rules.py, items.py, options.py.
# regions.py covers re
# It is recommended that you read these in that specific order, then come back to the world class.
class APQuestWorld(World):
    game = "APQuest"

    # This is how we associate the options defined in our options.py with our world.
    options: APQuestOptions
    options_dataclass = APQuestOptions

    # Our world class must have a static location_name_to_id and item_name_to_id defined.
    # We define these in regions.py and items.py respectively, so we just set them here.
    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    # There is always one region that the generator starts from & assumes you can always go back to.
    # This defaults to "Menu", but you can change it by overriding origin_region_name.
    origin_region_name = "Overworld"

    # Our world class must have certain functions ("steps") that get called during generation.
    # The main ones are: create_regions, set_rules, create_items.
    # For better structure and readability, we put each of these in their own file.
    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    # Our world class must also have a create_item function that can create any one of our items by name at any time.
    # We also put this in a different file, the same one that create_items is in.
    def create_item(self, name: str) -> items.APQuestItem:
        return items.create_item_with_correct_classification(self, name)

    # For features such as item links and panic-method start inventory, AP may ask your world to create extra filler.
    # The way it does this is by calling get_filler_item_name.
    # You must override this function and have it return the name of an infinitely repeatable filler item.
    # If you have multiple repeatable filler items, you can randomly choose one using e.g. self.random.choice(...).
    def get_filler_item_name(self) -> str:
        return "Confetti Canon"

    # There may be data that the game client will need to modify the behavior of the game.
    # This is what slot_data exists for. Upon every client connection, the slot's slot_data is sent to the client.
    # slot_data is just a dictionary using basic types, that will be converted to json when sent to the client.
    def fill_slot_data(self) -> Mapping[str, Any]:
        # If you need access to the player's chosen options on the client side, there is a helper for that.
        return self.options.as_dict("hard_mode", "confetti_explosiveness", "player_sprite")
