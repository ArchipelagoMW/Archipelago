from collections.abc import Mapping
from typing import Any

# Imports of base Archipelago modules must be absolute.
from worlds.AutoWorld import World

# Imports of your world's files must be relative.
from . import items, locations, options, regions, rules, web_world, json_data

# APQuest will go through all the parts of the world api one step at a time,
# with many examples and comments across multiple files.
# If you'd rather read one continuous document, or just like reading multiple sources,
# we also have this document specifying the entire world api:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md


# The world class is the heart and soul of an apworld implementation.
# It holds all the data and functions required to build the world and submit it to the multiworld generator.
# You could have all your world code in just this one class, but for readability and better structure,
# it is common to split up world functionality into multiple files.
# This implementation in particular has the following additional files, each covering one topic:
# regions.py, locations.py, rules.py, items.py, options.py and web_world.py.
# It is recommended that you read these in that specific order, then come back to the world class.
class Schedule1World(World):
    """
    Scheudle 1 is a game about manufacturing. Produce a range of drugs. Purchase properties and equipment.
    Distribute your products through a network of dealers. Avoid the law and rival manufacturers.
    Expand your empire and become the ultimate drug lord!
    """

    # The docstring should contain a description of the game, to be displayed on the WebHost.

    # You must override the "game" field to say the name of the game.
    game = "Schedule1"

    # The WebWorld is a definition class that governs how this world will be displayed on the website.
    web = web_world.APSchedule1()

    # This is how we associate the options defined in our options.py with our world.
    options_dataclass = options.Schedule1Options
    options: options.Schedule1Options  # Common mistake: This has to be a colon (:), not an equals sign (=).

    # Our world class must have a static location_name_to_id and item_name_to_id defined.
    # We define these in regions.py and items.py respectively, so we just set them here.
    # Load items from json into needed dicts.
    items.load_items_data(json_data.schedule1_item_data)
    locations.load_locations_data(json_data.schedule1_location_data)
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
        locations.create_all_locations(self, json_data.schedule1_location_data, json_data.schedule1_event_data)

    def set_rules(self) -> None:
        rules.set_all_rules(self, json_data.schedule1_location_data, json_data.schedule1_event_data)

    def create_items(self) -> None:
        items.create_all_items(self, json_data.schedule1_item_data)

    # Our world class must also have a create_item function that can create any one of our items by name at any time.
    # We also put this in a different file, the same one that create_items is in.
    def create_item(self, name: str) -> items.Schedule1Item:
        return items.create_item_with_correct_classification(self, name)

    # For features such as item links and panic-method start inventory, AP may ask your world to create extra filler.
    # The way it does this is by calling get_filler_item_name.
    # For this purpose, your world *must* have at least one infinitely repeatable item (usually filler).
    # You must override this function and return this infinitely repeatable item's name.
    # In our case, we defined a function called get_random_filler_item_name for this purpose in our items.py.
    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self, json_data.schedule1_item_data)

    # There may be data that the game client will need to modify the behavior of the game.
    # This is what slot_data exists for. Upon every client connection, the slot's slot_data is sent to the client.
    # slot_data is just a dictionary using basic types, that will be converted to json when sent to the client.
    def fill_slot_data(self) -> Mapping[str, Any]:
        # If you need access to the player's chosen options on the client side, there is a helper for that.
        return self.options.as_dict(
            "goal",
            "number_of_xp_bundles",
            "amount_of_xp_per_bundle_min",
            "amount_of_xp_per_bundle_max",
            "number_of_cash_bundles",
            "amount_of_cash_per_bundle_min",
            "amount_of_cash_per_bundle_max",
            "networth_amount_required",
            "filler_item_pool_type",
            "randomize_cartel_influence",
            "randomize_drug_making_properties",
            "randomize_business_properties",
            "randomize_dealers",
            "randomize_customers",
            "cartel_influence_checks_per_region",
            "recipe_checks",
            "cash_for_trash",
            "randomize_level_unlocks"
        )
