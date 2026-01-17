import os
from collections.abc import Mapping
from typing import Any

# Imports of base Archipelago modules must be absolute.
from worlds.AutoWorld import World

# Imports of your world's files must be relative.
from . import items, locations, regions, rules, web_world
from . import options as pso_options  # rename due to a name conflict with World.options
from .helpers import CLIENT_VERSION
from .options import PSOOptions
from .patcher.pso_settings import PSOSettings
from .patcher.rom_patch import PSOPlayerContainer
from .strings.region_names import Region

from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess
from ..saving_princess import CLIENT_NAME


# APQuest will go through all the parts of the world api one step at a time,
# with many examples and comments across multiple files.
# If you'd rather read one continuous document, or just like reading multiple sources,
# we also have this document specifying the entire world api:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md

def run_client(*args):
    from .client.pso_client import sync_main  # lazy import
    launch_subprocess(sync_main, name="PSO Client", args=args)


# Adds the launcher for our component and our client logo.
components.append(
    Component("PSO Client", func=run_client, component_type=Type.CLIENT,
              file_identifier=SuffixIdentifier(".appso")))

# The world class is the heart and soul of an apworld implementation.
# It holds all the data and functions required to build the world and submit it to the multiworld generator.
# You could have all your world code in just this one class, but for readability and better structure,
# it is common to split up world functionality into multiple files.
# This implementation in particular has the following additional files, each covering one topic:
# regions.py, locations.py, rules.py, items.py, options.py and web_world.py.
# It is recommended that you read these in that specific order, then come back to the world class.
class PSOWorld(World):
    """
    Phantasy Star Online Episodes I & II Plus is a hack-and-slash RPG produced by SEGA and Sonic Team for the
    Nintendo GameCube and Microsoft Xbox. Players make their way through Ragol in search of what happened to Red
    Ring Rico and the cause of a mysterious explosion that destroyed much of the earlier colony ship, Pioneer I.
    """

    # The docstring should contain a description of the game, to be displayed on the WebHost.

    # You must override the "game" field to say the name of the game.
    game = "Phantasy Star Online Episode I & II Plus"

    # The WebWorld is a definition class that governs how this world will be displayed on the website.
    web = web_world.PSOWebWorld()

    # This is how we associate the options defined in our options.py with our world.
    # (Note: options.py has been imported as "pso_options" at the top of this file to avoid a name conflict)
    options_dataclass = PSOOptions
    options: PSOOptions  # Common mistake: This has to be a colon (:), not an equals sign (=).

    settings: PSOSettings #This is the line that ties the get_base_rom_path together.

    # Our world class must have a static location_name_to_id and item_name_to_id defined.
    # We define these in regions.py and items.py respectively, so we just set them here.
    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    # There is always one region that the generator starts from & assumes you can always go back to.
    # This defaults to "Menu", but you can change it by overriding origin_region_name.
    origin_region_name = Region.PIONEER_2

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
    def create_item(self, name: str) -> items.PSOItem:
        return items.create_item_with_correct_classification(self, name)

    # For features such as item links and panic-method start inventory, AP may ask your world to create extra filler.
    # The way it does this is by calling get_filler_item_name.
    # For this purpose, your world *must* have at least one infinitely repeatable item (usually filler).
    # You must override this function and return this infinitely repeatable item's name.
    # In our case, we defined a function called get_random_filler_item_name for this purpose in our items.py.
    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def generate_output(self, output_directory: str, **kwargs):
        # Outputs the plando details to our expected output file
        # Create the output path based on the current player + expected patch file ending.
        patch_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}"
                                                    f"{PSOPlayerContainer.patch_file_ending}")
        # Create a zip (container) that will contain all the necessary output files for us to use during patching.
        dict_output_data: dict = {
            "Seed": self.multiworld.seed,
            "Slot": self.player,
            "Name": self.player_name,
            "Locations": {},
            "APWorldVersion": CLIENT_VERSION,
            "Options": {
                "start_with_lavis_blade": self.options.start_with_lavis_blade.value,
                "goal": self.options.goal.value,
                "quests_required": self.options.quests_required.value,
                "trap_chance": self.options.trap_chance.value
            }
        }

        # Creates the zip that will hold all necessary output files.
        pso_container = PSOPlayerContainer(dict_output_data, patch_path, self.multiworld.player_name[self.player],
                                               self.player)
        # Write the expected output zip container to the Generated Seed folder.
        pso_container.write()

    # There may be data that the game client will need to modify the behavior of the game.
    # This is what slot_data exists for. Upon every client connection, the slot's slot_data is sent to the client.
    # slot_data is just a dictionary using basic types, that will be converted to json when sent to the client.
    def fill_slot_data(self) -> Mapping[str, Any]:
        # If you need access to the player's chosen options on the client side, there is a helper for that.
        return self.options.as_dict(
            "goal", "quests_required", "start_with_lavis_blade"
        )
