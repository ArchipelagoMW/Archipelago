from collections.abc import Mapping
import os
import random
from typing import Any, Dict
import logging

# Imports of base Archipelago modules must be absolute.
from worlds.AutoWorld import World

from .patchfile import EVNContainer

# Imports of your world's files must be relative.
from . import items, locations, regions, rules, web_world

from . import options as evn_options  # rename due to a name conflict with World.options
from .logics import story_routes, possible_regions, EVNStoryRoute, MISSION_BLOCKING_BIT

# Game specific data imports
from .rezdata import misns, ships, outfits, desc, chars, crons
from .apdata.offsets import offsets_table
from .apdata.customoutf import cust_outf_table
from .apdata.customdesc import cust_desc_table

logger = logging.getLogger("Starcraft 2")

GAME_NAME = "EV Nova"

# --- How this works ---
# As a preface, the client uses bits to determine what has been completed and what is available.
# Ex: completing mission 128 can set bit 350 to 1. mission 129 checks for 350 and becomes available.
# By extension, additional ships and outfits can be made available this way as well.
# So, first we must assign each mission, ship and outfit a unique (UNUSED) bit that we care about,
# but that the game originally does not. This works because the game has a LOT of bits that it preps
# but isn't used by the original scenario's data.
# For missions (aka locations), this is "Address"
# For ships (aka items), this is "code".
# These values are used as both the bit id in the patch file, and as the ids for the server.
# They also don't change much with each generation. They are mainly affected by the options settings.
# Then, I believe the server manages a generated location -> item mapping
# When the client detects a mission (or other location) is checked, it will attempt to send all *changed* bits
# (Some missions set the same bit, those will be ignored if already checked previously).
# However, to reduce spam to the server, we provide an additional "aplocids.txt" file for the client
# to check against, thus it'll only send IDs in the list which are the ones the server cares about.
# The server then returns to the client an item "item received" function call with an item id.
# As this item ID in items.py was made the same as the bit id we care about, the client treats this
# as a bit and flips the associated bit. That ship or outfit that looks at that bit then becomes unlocked.
# Ergo, not much ID shuffling actually happens in the code defined here.

# --- Possible Improvements ---
# This game is *very* wide, with the exception of the story string that are deep.
# When we play this, we go through 1 story string. So the game is very wide except for this one pillar.
# The result is that balancing, or rather pushing into, new spheres has been very difficult.
# There's generally about 2 spheres now, which can cause early lock ups in other games while the player
# of this game tries to find that thing.
# This is further obfuscated by a lot of the generic missions being duplicates, or rather they accomplish
# the same thing and have the same name (in game), but are different missions with different associated checks.
# The game does this so you can have multiple copies of the same mission available, except with different destinations...
# I'm not being super clear about this, but basically "Deliver 10 tons to Thror" might or might not be the same
# location check as "Deliver 10 tons to Mars"... (Because their destination is rolled, but two copies are neaded
# to have two of those options show up in Mission BBS at the same time.)
# 1. Find a way to push logic into more spheres, namely for side missions and for story string.
# 2. Find a way to present hints better to player. "Deliver 10 tons to <dst> - 331" is actually this mission
# in this gov's area, while "Deliver 10 tons to <dst> - 333" is actually over here in this gov area.

class EVNWorld(World):
    """
    EVN, also known as Escape Velocity Nova, is a space trading and combat simulation game.
    The third installment in the Escape Velocity series, EVN offers players an expansive universe to explore,
    filled with diverse factions, intricate storylines, and a vast array of ships and equipment.
    """

    # The docstring should contain a description of the game, to be displayed on the WebHost.

    # You must override the "game" field to say the name of the game.
    game = GAME_NAME

    # The WebWorld is a definition class that governs how this world will be displayed on the website.
    web = web_world.EVNWebWorld()

    # This is how we associate the options defined in our options.py with our world.
    # (Note: options.py has been imported as "evn_options" at the top of this file to avoid a name conflict)
    options_dataclass = evn_options.EVNOptions
    # options: evn_options.EVNOptions  # Common mistake: This has to be a colon (:), not an equals sign (=).

    # Our world class must have a static location_name_to_id and item_name_to_id defined.
    # We define these in regions.py and items.py respectively, so we just set them here.
    location_name_to_id = locations.loc_name_to_id
    location_id_to_name = locations.loc_id_to_name # dunno if this exists or we are declaring, but I need it.

    #TODO: consider this design style
    # are we sure this isn't empty at the time of world class definition? If so, we can just set item_name_to_id = items.item_name_to_id and avoid the redundant lookup in items.py.
    item_name_to_id = items.item_name_to_id

    # There is always one region that the generator starts from & assumes you can always go back to.
    # This defaults to "Menu", but you can change it by overriding origin_region_name.
    origin_region_name = "Universe" # Our default is the ingame universe where the player starts, with no story line association

    # We need to know the story string chosen in options, or rolled if random was chosen
    # As that dictates some of the things we will do, as well as the logic chunk we will refer to in logics.py
    _chosen_string = -1

    # NOTE: the options class may have a built in random feature - let's look at that first!
    # Internal, locally defined function
    def get_chosen_string_id(self) -> int: 
        """
        Determine the story string ID either chosen or rolled by the player.
        Tied to logics' story route IDs.
        """
        if self._chosen_string > 0:
            return self._chosen_string
        
        cur_string = self.options.chosen_string.value
        #logger.info(f"player's choice for story string was {cur_string}")

        if cur_string > 0:
            self._chosen_string = cur_string
            return self._chosen_string
        
        # Other cases failed, so most likely this is the first call and options = 0 ("Surprise Me")
        self._chosen_string = random.randint(1,len(story_routes)) 
        #logger.info(f"rolled string {self._chosen_string}")
        return self._chosen_string
    
    def get_chosen_string(self) -> EVNStoryRoute:
        """
        Get the story string's data from logics.
        """
        return story_routes[self.get_chosen_string_id()]
        
    # Overwrite this function to provide player with a few early items
    def generate_early(self):
        # Try to get some Vell-os player ships into pool in sphere 1 because altogether ~75 checks locked behind 'em
        self.multiworld.early_items[self.player]["Vell-os Dart381"] = 1
        self.multiworld.early_items[self.player]["Vell-os Arrow382"] = 1
        self.multiworld.early_items[self.player]["Vell-os Javelin383"] = 1

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
    
    # This function is called to generate the output mod file (plugin) for the player.
    # Will present as a download link for the player on the website once generation is complete.
    def generate_output(self, output_directory: str):
        mod_name = self.multiworld.get_out_file_name_base(self.player).replace("_", "-")
        #logger.info(f"Generating output mod for player {self.player} with mod name {mod_name} in directory {output_directory}")
        mod_dir = os.path.join(output_directory, mod_name)
        mod_files = {
            # Can utilize helper functions to export the items into useful data strings.
            # The "zzz_" prefix is to ensure this file is last in the load order on the client, so that all our data is loaded after any potential mod changes to the missions table.
            "zzzapdata.txt": f"{self.prep_plugins_output()}", 
            # this is just a qol filter to keep EVN client from sending bit IDs the server doesn't care about.
            "aplocids.txt": f"{self.prep_emittable_loc_ids()}", 
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
        # block_missions = {
        #     evn_options.ChosenString.option_vellos: 128, #"Delivery to Earth; Vellos1"
        #     evn_options.ChosenString.option_fed: 428, #"Federation Resupply;Fed1"
        #     #evn_options.ChosenString.option_rebel: 3, #rebels can ONLY come from other lines, so don't I guess
        #     evn_options.ChosenString.option_pirate: 693, #"Pick Up Cargo From Sol;Pirate 001"
        #     evn_options.ChosenString.option_auroran: 653, #Take Supplies to Dominance
        #     evn_options.ChosenString.option_polaris: 150, #Transport Mu'Randa
        # }

        # block_missions[self.options.chosen_string.value] = 0 #so we won't block the one that was chosen.

        #chosen_route = story_routes[self.options.chosen_string.value]
        chosen_route = self.get_chosen_string()
        #use_extended = chosen_route["use_extended_checks"] # handled in locations.py

        # first, the column headers
        for column in misns.misn_columns.keys():
            output_file_string += f'"{misns.misn_columns[column]}"\t'
        output_file_string += "\r\n"
        # then, the mission data
        for mission in misns.misn_table.keys():
            # check for mission edits
            misn_edits = {} # dict[str,str]
            for regionid in chosen_route["regions"]:
                sregion = possible_regions[regionid]
                if mission in sregion["misn_edits"]:
                    misn_edits.update(sregion["misn_edits"][mission]) # will append all items to the var's set, overwriting existing
                    break   # NOTE: We assume that a mission can only show up in one region of a story string

            # Continue with replacement process
            temp_mission = misns.misn_table[mission]

            # By default, we usually want to alter a missions on_success trigger to unlock the item we want.
            # In some cases, the actual desired outcome of a mission can be something else, such as "on_refuse".
            # This is because the way story line choices are represented does not equate necessarily to the code representations.
            # I.E. on_success may be choice 1, and on_refuse is choice 2. Depending on the branch of story line
            # we're running through, we may want choice 2 instead.
            check_target = "on_success"

            for column in misns.misn_columns.keys():
                current_val = temp_mission[column]
                
                # Overwrite with our edit / replacement logic, but then continue the normal process
                if column in misn_edits:
                    # Sometimes, the "successful" option is a refuse (because it is a branching player choice), so we need to redirect where we put the check bit
                    if misn_edits[column] == "CHECK_TARGET":
                        check_target = column
                    else:
                        current_val = misn_edits[column]

                # Prep our output with the original value.
                # We may alter it later (usually be adding to it.)
                default_val = current_val + "\t"
                #logger.info(f"current_val type: {type(current_val)}, value: {current_val} and misns.MisnDict[column] type: {misns.MisnDict.__annotations__[column]} for column {column}")
                col_anno = misns.MisnDict.__annotations__[column]
                #logger.info(f"misns.MisnDict annotations: {misns.MisnDict.__annotations__[column]} - equal to str? {col_anno == str} or class str? {col_anno == '<class \'str\'>'} ")
                if col_anno == str:
                    default_val = f'"{current_val}"\t'

                # We need to inject our special bit, as that's how the client will be able to properly inform the server which mission was completed.
                if column == check_target:
                    # WARNING: if we ever change this format for location names, we need to change it in both the location creation code in locations.py and this export code here, to ensure the lookups work properly.
                    # We could consider making this more robust by storing the location name directly in the mission table, but that would require a lot of changes to the mission table and mission creation code, so for now we will just be careful to maintain this format.
                    # So, consider fetching this somehow instead of reconstructing it from the mission name and ID. That would be more robust and less error prone, but would require a lot of changes to the mission table and mission creation code.
                    # For now we will just be careful to maintain this format.
                    target_id = offsets_table["misn"] + mission
                    if target_id in locations.ev_location_bank:
                        associated_location = locations.ev_location_bank[target_id]
                        new_id = associated_location["address"]
                        if (new_id is not None):
                            if (current_val is not None) and (current_val != ""):
                                output_file_string += f'"b{new_id} {current_val}"\t'  # No logic needed for this one
                            else:
                                output_file_string += f'"b{new_id}"\t' # We inject the "b" bit to indicate this is a location ID, so the client can properly parse it and know to look for an item at that location.
                        else:
                            #logger.info(f"Warning: on_success location {target_id} for mission {temp_mission['name']} for player {self.player} does not have a valid address. This likely means the location was not created properly, and any item placements depending on this location will fail. Check the mission table and location creation code to debug this issue.")
                            output_file_string += default_val
                    else:
                        #logger.info(f"Warning: on_success location id {target_id} for mission {temp_mission['name']} not found in location_id_to_name. This likely means the location was not created properly, and any item placements depending on this location will fail. Check the mission table and location creation code to debug this issue.")
                        output_file_string += default_val
                # elif column == "available_bits" and mission in block_missions.values():
                #     output_file_string += f'"b{offsets_table['misn-block']} & ({current_val})"\t'   #we know it is a bit string, and we know these ones have bits, so don't need to protect as much
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
            # if ship in items.specific_exclusions:
            #     continue
            temp_ship = ships.ship_table[ship]
            for column in ships.ship_columns.keys():
                current_val = temp_ship[column]
                default_val = current_val + "\t"
                col_anno = ships.ShipDict.__annotations__[column]
                if col_anno == str:
                    default_val = f'"{current_val}"\t'

                if column == "availability":
                    # We need to inject our special bit here as well, so the client can know when to unlock the ship.
                    target_id = offsets_table["ship"] + ship
                    if target_id in items.ev_item_bank:
                        #associated_item = items.ev_item_bank[target_id]
                        new_id = items.ev_item_bank[target_id]["code"] if "code" in items.ev_item_bank[target_id] else None
                        if (new_id is not None):
                            output_file_string += f'"b{new_id}"\t'
                        else:
                            #logger.info(f"Warning: availability location {target_id} for ship {temp_ship['name']} for player {self.player} does not have a valid address. This likely means the location was not created properly, and any item placements depending on this location will fail. Check the ship table and location creation code to debug this issue.")
                            output_file_string += default_val
                    else:
                        #logger.info(f"Warning: availability location {target_id} for ship {temp_ship['name']} not found in ev_item_bank. This likely means the location was not created properly, and any item placements depending on this location will fail. Check the ship table and location creation code to debug this issue.")
                        #output_file_string += default_val
                        #logger.info(f"Ship blocked (must have been ignored): {target_id} for ship {temp_ship['name']}")
                        output_file_string += f'"b{MISSION_BLOCKING_BIT}"'
                elif (column == "buy_random" and self.options.always_avail_shops):
                    output_file_string += f'100\t' # considering altering hire chance too
                elif (column == "tech_level" and self.options.ignore_tech):
                    output_file_string += f'1\t'
                elif (column == "require_bits"): # and self.options.ignore_tech): 
                    # ignore license requirements regardless of options. removing licenses from pool.
                    output_file_string += f"0x0000000000000000\t"
                elif (column == "flags_3" and (self.options.always_avail_shops or self.options.ignore_tech)):
                    flag1 = 0x0100
                    flag2 = 0x0200
                    current_flag = int(current_val,16)
                    if (not current_flag & flag1):
                        current_flag += flag1 # int(flag1,16)
                    if (not current_flag & flag2):
                        current_flag += flag2 # int(flag2,16)
                    output_file_string += f'0x{current_flag:04x}\t'
                else:
                    output_file_string += default_val
            output_file_string += "\r\n"

        # Outfits
        # Now, due to the outf checks, we will always have outf data, so do the columns
        # column titles
        output_file_string += "\r\n"
        for column in outfits.outf_columns.keys():
            output_file_string += f'"{outfits.outf_columns[column]}"\t'
        output_file_string += "\r\n"

        if (self.options.include_outfits):
            # then, the outf data
            for outf in outfits.outf_table.keys():
                temp_outf = outfits.outf_table[outf]
                for column in outfits.outf_columns.keys():
                    current_val = temp_outf[column]
                    default_val = current_val + "\t"
                    col_anno = outfits.OutfDict.__annotations__[column]
                    if col_anno == str:
                        default_val = f'"{current_val}"\t'

                    if column == "availability":
                        # We need to inject our special bit here as well, so the client can know when to unlock the outf.
                        target_id = offsets_table["outf"] + outf
                        if target_id in items.ev_item_bank:
                            #associated_item = items.ev_item_bank[target_id]
                            new_id = items.ev_item_bank[target_id]["code"] if "code" in items.ev_item_bank[target_id] else None
                            if (new_id is not None):
                                #TESTING:
                                #new_id = 9999
                                output_file_string += f'"b{new_id}"\t'
                            else:
                                #logger.info(f"Warning: availability location {target_id} for outf {temp_outf['name']} for player {self.player} does not have a valid address. This likely means the location was not created properly, and any item placements depending on this location will fail. Check the outf table and location creation code to debug this issue.")
                                output_file_string += default_val
                        else:
                            #logger.info(f"Warning: availability location {target_id} for outf {temp_outf['name']} not found in ev_item_bank. This likely means the location was not created properly, and any item placements depending on this location will fail. Check the outf table and location creation code to debug this issue.")
                            #output_file_string += default_val
                            #logger.info(f"Outf blocked (must have been ignored): {target_id} for outf {temp_outf['name']}")
                            output_file_string += f'"b{MISSION_BLOCKING_BIT}"'
                    elif (column == "buy_random" and self.options.always_avail_shops):
                        output_file_string += f'100\t'
                    elif (column == "tech_level" and self.options.ignore_tech):
                        output_file_string += f'1\t'
                    elif (column == "require_bits"): # and self.options.ignore_tech): 
                        # ignore license requirements regardless of options. removing licenses from pool.
                        output_file_string += f"0x0000000000000001\t"
                    elif (column == "flags" and (self.options.always_avail_shops or self.options.ignore_tech)):
                        flag1 = 0x0100  # show only if req bits met (or has 1)
                        flag2 = 0x4000  # show only if availability is met (or has 1)
                        current_flag = int(current_val,16)
                        if (not current_flag & flag1):
                            current_flag += flag1 # int(flag1,16)
                        if (not current_flag & flag2):
                            current_flag += flag2 # int(flag2,16)
                        output_file_string += f'0x{current_flag:04x}\t'
                    else:
                        output_file_string += default_val
                output_file_string += "\r\n"

        # then, custom outfit checks
        # these are used as LOCATIONS not ITEMS, even though they are in game items.
        # meaning, use locations.ev_location_bank not items.ev_item_bank.
        # I kinda hate having to check this, but haven't figured out a better way yet
        our_multiworld_locations = [l.name for l in self.multiworld.get_locations(self.player)]
        # NOTE: This is because we may NOT have created the extended custom location checks!

        # If we were to dynamically create custom outfit locations, we would need to do it here, but for now we will just assume they are already created in locations.py and we will just export the data for them.
        # While target_id in locaitons.ev_location_bank:
        #   [create outfit data]
        #   target_id += 1

        for coutf in cust_outf_table.keys():
            temp_coutf = cust_outf_table[coutf]
            for column in outfits.outf_columns.keys():
                current_val = temp_coutf[column]
                default_val = current_val + "\t"
                col_anno = outfits.OutfDict.__annotations__[column]
                if col_anno == str:
                    default_val = f'"{current_val}"\t'

                target_id = offsets_table["outf_cks"] + coutf

                # TODO: make the locations.ev_location_bank check once here and reuse below, instead of checking for each column. But for now, this works.

                if column == "on_purchase":
                    # We need to inject our special bit here as well, so the client can know when to unlock the outf.
                    if target_id in locations.ev_location_bank:
                        associated_location = locations.ev_location_bank[target_id]
                        new_id = associated_location["address"]
                        if (new_id is not None):
                            output_file_string += f'"b{new_id}"\t'
                        else:
                            #logger.info(f"Warning: availability location {target_id} for outf {temp_coutf['name']} for player {self.player} does not have a valid address. This likely means the location was not created properly, and any item placements depending on this location will fail. Check the outf table and location creation code to debug this issue.")
                            output_file_string += default_val
                    else:
                        #logger.info(f"Outf blocked (must have been ignored): {target_id} for outf {temp_coutf['name']}")
                        #output_file_string += f'"b{MISSION_BLOCKING_BIT}"' # Don't set that! will make bad misns available!
                        output_file_string += f'""' # honestly, could just drop the else block
                elif (column == "buy_random"):
                    if target_id in locations.ev_location_bank and locations.ev_location_bank[target_id]["name"] in our_multiworld_locations:
                        output_file_string += default_val
                    else:
                        output_file_string += f'0\t' # don't show the item
                elif (column == "short_name"):
                    if target_id in locations.ev_location_bank and locations.ev_location_bank[target_id]["name"] in our_multiworld_locations:
                        mwloc = self.multiworld.get_location(locations.ev_location_bank[target_id]["name"], self.player) # should be the populated items for my seed now (post shuffle and fill)
                        output_file_string += f'"{temp_coutf["name"]}\\\\n- {mwloc.player} -"\t'
                    else:
                        output_file_string += default_val
                else:
                    output_file_string += default_val
            output_file_string += "\r\n"

        # Descriptions
        # column titles
        output_file_string += "\r\n"
        for column in desc.desc_columns.keys():
            output_file_string += f'"{desc.desc_columns[column]}"\t'
        output_file_string += "\r\n"

        # finally, custom desc data
        for cdesc in cust_desc_table.keys():
            temp_desc = cust_desc_table[cdesc]
            for column in desc.desc_columns.keys():
                current_val = temp_desc[column]
                default_val = current_val + "\t"
                col_anno = desc.DescDict.__annotations__[column]
                if col_anno == str:
                    default_val = f'"{current_val}"\t'

                target_id = cdesc - offsets_table["desc_alt"] + offsets_table["outf_cks"] # get custom outf id
                if column == "text":
                    #logger.info(f'trying to find desc for {target_id}, and I am player {self.player}')
                    # We need to inject our special bit here as well, so the client can know when to unlock the outf.
                    if target_id in locations.ev_location_bank and locations.ev_location_bank[target_id]["name"] in our_multiworld_locations:
                        mwloc = self.multiworld.get_location(locations.ev_location_bank[target_id]["name"], self.player) # should be the populated items for my seed now (post shuffle and fill)
                        output_file_string += f'"{temp_desc["name"]} will unlock {mwloc.item.name}"\t' # I don't know how to get the player name yet. mwloc.player is just my player id, becuase it it is my check.
                    else:
                        #logger.info(f"Outf blocked (must have been ignored): {target_id} for outf {temp_desc['name']}")
                        output_file_string += default_val
                else:
                    output_file_string += default_val
            output_file_string += "\r\n"

        # Chars

        # Actually, let's also throw in some pilot data options
        output_file_string += "\r\n"
        for column in chars.char_columns.keys():
            output_file_string += f'"{chars.char_columns[column]}"\t'
        output_file_string += "\r\n"
        # then, the data
        for pilot in chars.char_table.keys():
            temp_char = chars.char_table[pilot]
            for column in chars.char_columns.keys():
                current_val = temp_char[column]
                default_val = current_val + "\t"
                col_anno = chars.CharDict.__annotations__[column]
                if col_anno == str:
                    default_val = f'"{current_val}"\t'

                output_file_string += default_val
            output_file_string += "\r\n"

        # Crons
        output_file_string += "\r\n"
        for column in crons.cron_columns.keys():
            output_file_string += f'"{crons.cron_columns[column]}"\t'
        output_file_string += "\r\n"
        # then, the data
        for item in crons.cron_table.keys():
            temp_char = crons.cron_table[item]
            for column in crons.cron_columns.keys():
                current_val = temp_char[column]
                default_val = current_val + "\t"
                col_anno = crons.CronDict.__annotations__[column]
                if col_anno == str:
                    default_val = f'"{current_val}"\t'

                output_file_string += default_val
            output_file_string += "\r\n"


        #logger.info(f"output file string prepared: {output_file_string[:1000]}...") # Log the first 1000 characters of the output for debugging purposes. Be careful with this if the output can be very large, as it may cause performance issues or clutter the logs.

        return output_file_string