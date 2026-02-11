from collections.abc import Mapping
from typing import Any

from Options import OptionError
# Imports of base Archipelago modules must be absolute.
from worlds.AutoWorld import World

# Imports of your world's files must be relative.
from . import items, locations, options, regions, rules, web_world

import uuid

class GatoRobotoWorld(World):
    """
    Gato Roboto is a 2D Metroidvania Platformer where you play as a cat named Kiki attempting to save her owner after
    they crash-land on an alien planet. Collect weapon modules as you explore the various regions of the planet, but
    beware of irritable creatures and treacherous obstacles, and the dark secrets it holds...
    """
    game = "Gato Roboto B-Side"

    web = web_world.GatoRobotoWebWorld()

    options_dataclass = options.GatoRobotoOptions
    options: options.GatoRobotoOptions

    # Our world class must have a static location_name_to_id and item_name_to_id defined.
    # We define these in regions.py and items.py respectively, so we just set them here.
    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    # There is always one region that the generator starts from & assumes you can always go back to.
    # This defaults to "Menu", but you can change it by overriding origin_region_name.
    origin_region_name = "Landing Site"

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
    def create_item(self, name: str) -> items.GatoRobotoItem:
        return items.create_item_with_correct_classification(self, name)

    # For features such as item links and panic-method start inventory, AP may ask your world to create extra filler.
    # The way it does this is by calling get_filler_item_name.
    # For this purpose, your world *must* have at least one infinitely repeatable item (usually filler).
    # You must override this function and return this infinitely repeatable item's name.
    # In our case, we defined a function called get_random_filler_item_name for this purpose in our items.py.
    def get_filler_item_name(self) -> str:
        return "Cute Meow"

    def generate_early(self) -> None:
        if self.options.unlock_all_warps:
            self.options.unlock_all_warps.value = False
            #raise OptionError
        items.generate_early(self)

    # There may be data that the game client will need to modify the behavior of the game.
    # This is what slot_data exists for. Upon every client connection, the slot's slot_data is sent to the client.
    # slot_data is just a dictionary using basic types, that will be converted to json when sent to the client.
    def fill_slot_data(self) -> Mapping[str, Any]:
        # If you need access to the player's chosen options on the client side, there is a helper for that.
        slot_data = self.options.as_dict("nexus_start", "unlock_all_warps", "gato_tech")
        slot_data["game_id"] = str(uuid.uuid4())
        return slot_data

    def DISABLED_generate_output(self, output_directory: str) -> None:
        from Utils import visualize_regions
        state = self.multiworld.get_all_state(False)
        state.update_reachable_regions(self.player)
        visualize_regions(self.get_region("Nexus"), "my_world.puml", show_entrance_names=True, regions_to_highlight=state.reachable_regions[self.player])
