from collections.abc import Mapping
import os
from typing import Any
from venv import logger

# Imports of base Archipelago modules must be absolute.
from worlds.AutoWorld import World
from worlds.evn.patchfile import EVNContainer

# Imports of your world's files must be relative.
from . import items, locations, regions, rules, web_world
# from . import web_world
from . import options as evn_options  # rename due to a name conflict with World.options

from .rezdata import misns, ships

GAME_NAME = "EV Nova"

class EVNWorld(World):
    """
    EVN, also known as Escape Velocity Nova, is a space trading and combat simulation game.
    The third installment in the Escape Velocity series, EVN offers players an expansive universe to explore,
    filled with diverse factions, intricate storylines, and a vast array of ships and equipment.
    """

    # The docstring should contain a description of the game, to be displayed on the WebHost.

    # You must override the "game" field to say the name of the game.
    #game = "EV Nova"
    game = GAME_NAME

    # The WebWorld is a definition class that governs how this world will be displayed on the website.
    web = web_world.EVNWebWorld()

    # This is how we associate the options defined in our options.py with our world.
    # (Note: options.py has been imported as "evn_options" at the top of this file to avoid a name conflict)
    options_dataclass = evn_options.EVNOptions
    # options: evn_options.EVNOptions  # Common mistake: This has to be a colon (:), not an equals sign (=).

    # Our world class must have a static location_name_to_id and item_name_to_id defined.
    # We define these in regions.py and items.py respectively, so we just set them here.
    #location_name_to_id = locations.LOCATION_NAME_TO_ID
    location_name_to_id = locations.loc_name_to_id
    #item_name_to_id = items.ITEM_NAME_TO_ID

    #TODO: consider this design style
    # are we sure this isn't empty at the time of world class definition? If so, we can just set item_name_to_id = items.item_name_to_id and avoid the redundant lookup in items.py.
    #item_name_to_id = {data["name"]: item_id for item_id, data in items.ev_item_bank.items()}
    item_name_to_id = items.item_name_to_id
    # item_name_groups = Items.item_name_groups

    # location_name_to_id = {data["name"]: loc_id for loc_id, data in Locations.location_table.items()}
    # location_name_groups = Locations.location_name_groups

    # There is always one region that the generator starts from & assumes you can always go back to.
    # This defaults to "Menu", but you can change it by overriding origin_region_name.
    origin_region_name = "Universe"

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
    def create_item(self, name: str) -> items.EVNItem:
        return items.create_item_with_correct_classification(self, name)

    # For features such as item links and panic-method start inventory, AP may ask your world to create extra filler.
    # The way it does this is by calling get_filler_item_name.
    # For this purpose, your world *must* have at least one infinitely repeatable item (usually filler).
    # You must override this function and return this infinitely repeatable item's name.
    # In our case, we defined a function called get_random_filler_item_name for this purpose in our items.py.
    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    # There may be data that the game client will need to modify the behavior of the game.
    # This is what slot_data exists for. Upon every client connection, the slot's slot_data is sent to the client.
    # slot_data is just a dictionary using basic types, that will be converted to json when sent to the client.
    # NOTE: not currently making use of this in any way really on the client.
    def fill_slot_data(self) -> Mapping[str, Any]:
        # If you need access to the player's chosen options on the client side, there is a helper for that.
        return self.options.as_dict(
            "shuffle_systems" 
        ) # otherwise, I'll need to finish adding the options / details.
    
    # This function is called to generate the output mod file for the player.
    # Will present as a download link for the player on the website once generation is complete.
    def generate_output(self, output_directory: str):
        mod_name = self.multiworld.get_out_file_name_base(self.player).replace("_", "-")
        logger.info(f"Generating output mod for player {self.player} with mod name {mod_name} in directory {output_directory}")
        mod_dir = os.path.join(output_directory, mod_name)
        mod_files = {
            #f"test.txt": "Hello World!",    # Placeholder file content. TODO: Replace with actual mod files. Can utilize helper functions to export the items into useful data strings.
            "zzzapdata.txt": f"{self.prep_plugins_output()}", # The "zzz_" prefix is to ensure this file is last in the load order, so that all our data is loaded after any potential mod changes to the missions table.
            "aplocids.txt": f"{self.prep_emittable_loc_ids()}", # this is just a qol filter to keep EVN client from sending bit IDs the server doesn't care about.
        }
        mod = EVNContainer(
            mod_files,
            mod_dir,
            output_directory,
            self.player,
            self.multiworld.get_file_safe_player_name(self.player),
        )
        mod.write()

    def prep_emittable_loc_ids(self) -> str:
        ret_str = ""
        for loc_id in locations.ev_location_bank.keys():
            ret_str += f"{loc_id}\r\n"
        return ret_str

    def prep_plugins_output(self) -> str:
        """
        This exports our modified data into a text file format that can be converted into a game plugin. That's how the game's data will be initially altered to reflect the generated item placements.
        """
        output_file_string = ""

        # Missions

        # We've added the option for story string choice, so let's enforce that in the plugin by making the other strings not startable.
        block_missions = {
            evn_options.ChosenString.option_vellos: 128, #"Delivery to Earth; Vellos1"
            evn_options.ChosenString.option_fed: 428, #"Federation Resupply;Fed1"
            #evn_options.ChosenString.option_rebel: 3, #rebels can ONLY come from other lines, so don't I guess
            evn_options.ChosenString.option_pirate: 693, #"Pick Up Cargo From Sol;Pirate 001"
            evn_options.ChosenString.option_auroran: 653, #Take Supplies to Dominance
            evn_options.ChosenString.option_polaris: 150, #Transport Mu'Randa
        }

        block_missions[self.options.chosen_string.value] = 0 #so we won't block the one that was chosen.

        # first, the column headers
        for column in misns.misn_columns.keys():
            output_file_string += f'"{misns.misn_columns[column]}"\t'
        output_file_string += "\r\n"
        # then, the mission data
        for mission in misns.misn_table.keys():
            temp_mission = misns.misn_table[mission]
            for column in misns.misn_columns.keys():
                current_val = temp_mission[column]
                default_val = current_val + "\t"
                #if type(current_val) == str: #everything is a string because of how the data is filled.
                #logger.info(f"current_val type: {type(current_val)}, value: {current_val} and misns.MisnDict[column] type: {misns.MisnDict.__annotations__[column]} for column {column}")
                col_anno = misns.MisnDict.__annotations__[column]
                #logger.info(f"misns.MisnDict annotations: {misns.MisnDict.__annotations__[column]} - equal to str? {col_anno == str} or class str? {col_anno == '<class \'str\'>'} ")
                #if col_anno == '<class \'str\'>':
                if col_anno == str:
                    default_val = f'"{current_val}"\t'
                # We need to inject our special bit, as that's how the client will be able to properly inform the server which mission was completed.
                if column == "on_success":
                    # WARNING: if we ever change this format for location names, we need to change it in both the location creation code in locations.py and this export code here, to ensure the lookups work properly. We could consider making this more robust by storing the location name directly in the mission table, but that would require a lot of changes to the mission table and mission creation code, so for now we will just be careful to maintain this format.
                    # So, consider fetching this somehow instead of reconstructing it from the mission name and ID. That would be more robust and less error prone, but would require a lot of changes to the mission table and mission creation code, so for now we will just be careful to maintain this format.
                    #target_name = temp_mission["name"].strip() + "-" + temp_mission["id"] # this is the format we used for location names. We want to export the location name corresponding to the mission's on_success location, so we can use it for item placement in the plugin.
                    #target_name = self.location_name_to_id[mission]
                    target_id = locations.loc_type_offset["misn"] + mission
                    #logger.info(f"self.location_id_to_name keys: {self.location_id_to_name.keys()}")
                    #if target_id in self.location_id_to_name: # blank for some reason... maybe that's a bad sign?
                        #target_name = self.location_id_to_name[target_id]
                    if target_id in locations.ev_location_bank:
                        #associated_location = self.multiworld.get_location(target_name, self.player)
                        #associated_location = self.get_location(target_name)
                        associated_location = locations.ev_location_bank[target_id]
                        #new_id = self.location_id_to_name[target_id].address if target_id in self.location_id_to_name else None
                        new_id = associated_location["address"]
                        if (new_id is not None):
                            if (current_val is not None) and (current_val != ""):
                                output_file_string += f'"b{new_id} {current_val}"\t'  # No logic needed for this one
                            else:
                                output_file_string += f'"b{new_id}"\t' # We inject the "b" bit to indicate this is a location ID, so the client can properly parse it and know to look for an item at that location.
                        else:
                            logger.info(f"Warning: on_success location {target_id} for mission {temp_mission['name']} for player {self.player} does not have a valid address. This likely means the location was not created properly, and any item placements depending on this location will fail. Check the mission table and location creation code to debug this issue.")
                            output_file_string += default_val
                    else:
                        #logger.info(f"Warning: on_success location {target_name} for mission {temp_mission['name']} not found in location_name_to_id. This likely means the location was not created properly, and any item placements depending on this location will fail. Check the mission table and location creation code to debug this issue.")
                        logger.info(f"Warning: on_success location id {target_id} for mission {temp_mission['name']} not found in location_id_to_name. This likely means the location was not created properly, and any item placements depending on this location will fail. Check the mission table and location creation code to debug this issue.")
                        output_file_string += default_val
                elif column == "available_bits" and mission in block_missions.values():
                    output_file_string += f'"b{locations.loc_type_offset['misn-block']} & ({current_val})"\t'   #we know it is a bit string, and we know these ones have bits, so don't need to protect as much
                else:
                    output_file_string += default_val
            output_file_string += "\r\n"

        # Handle other data tables in a similar way...
        # prelude with two new lines to separate from the missions table. There should be a blank line between each type table.

        # Ships
        output_file_string += "\r\n"
        for column in ships.ship_columns.keys():
            output_file_string += f'"{ships.ship_columns[column]}"\t'
        output_file_string += "\r\n"
        # then, the ship data
        for ship in ships.ship_table.keys():
            temp_ship = ships.ship_table[ship]
            for column in ships.ship_columns.keys():
                current_val = temp_ship[column]
                default_val = current_val + "\t"
                col_anno = ships.ShipDict.__annotations__[column]
                if col_anno == str:
                    default_val = f'"{current_val}"\t'

                if column == "availability":
                    # We need to inject our special bit here as well, so the client can know when to unlock the ship.
                    target_id = items.type_offset["ship"] + ship
                    if target_id in items.ev_item_bank:
                        #associated_item = items.ev_item_bank[target_id]
                        new_id = items.ev_item_bank[target_id]["code"] if "code" in items.ev_item_bank[target_id] else None
                        if (new_id is not None):
                            if (current_val is not None) and (current_val != ""):
                                output_file_string += f'"b{new_id} & ({current_val})"\t'  # !Logic needed for this one!
                            else:
                                output_file_string += f'"b{new_id}"\t'
                        else:
                            logger.info(f"Warning: availability location {target_id} for ship {temp_ship['name']} for player {self.player} does not have a valid address. This likely means the location was not created properly, and any item placements depending on this location will fail. Check the ship table and location creation code to debug this issue.")
                            output_file_string += default_val
                    else:
                        logger.info(f"Warning: availability location {target_id} for ship {temp_ship['name']} not found in ev_item_bank. This likely means the location was not created properly, and any item placements depending on this location will fail. Check the ship table and location creation code to debug this issue.")
                        output_file_string += default_val
                else:
                    output_file_string += default_val
            output_file_string += "\r\n"

        logger.info(f"output file string prepared: {output_file_string[:1000]}...") # Log the first 1000 characters of the output for debugging purposes. Be careful with this if the output can be very large, as it may cause performance issues or clutter the logs.

        return output_file_string