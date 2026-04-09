from collections.abc import Mapping
from typing import Any, Dict

# Imports of base Archipelago modules must be absolute.
from worlds.AutoWorld import World

# Imports of your world's files must be relative.
from . import items, locations, regions, rules
from .levels import LEVEL_DATA
from . import options as babaisyou_options  # rename due to a name conflict with World.options

import logging
logger = logging.getLogger("Baba Is You")

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
class BabaIsYouWorld(World):
    """
    (Steam description for now)
    Baba Is You is a puzzle game where the rules you have to follow are present as blocks you can interact with.
    By manipulating them, you can change how the game works, repurpose things you find in the levels and cause surprising interactions!
    """

    # The docstring should contain a description of the game, to be displayed on the WebHost.

    # You must override the "game" field to say the name of the game.
    game = "Baba Is You"

    # This is how we associate the options defined in our options.py with our world.
    # (Note: options.py has been imported as "babaisyou_options" at the top of this file to avoid a name conflict)
    options_dataclass = babaisyou_options.BabaIsYouOptions
    options: babaisyou_options.BabaIsYouOptions  # Common mistake: This has to be a colon (:), not an equals sign (=).

    # Our world class must have a static location_name_to_id and item_name_to_id defined.
    # We define these in regions.py and items.py respectively, so we just set them here.
    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    # We can define location and item name groups here as well.
    item_name_groups = items.item_name_groups
    # location_name_groups = location_name_groups

    # There is always one region that the generator starts from & assumes you can always go back to.
    # This defaults to "Menu", but you can change it by overriding origin_region_name.
    origin_region_name = "Map"

    # Mapping for level shuffle
    active_level_dict: dict[str,str]
    
    def generate_early(self) -> None:
        # Validate options
        maxBlossoms = self.options.blossoms + (self.options.blossom_petals // 8)
        if self.options.first_gate_blossoms > maxBlossoms:
            logger.warning(f"Baba Is You ({self.player_name}): First gate requires {self.options.first_gate_blossoms} blossoms, but only {maxBlossoms} are in the pool."
                           f"Reducing first gate amount...")
            self.options.first_gate_blossoms.value = maxBlossoms
        if self.options.second_gate_blossoms > maxBlossoms:
            logger.warning(f"Baba Is You ({self.player_name}): Second gate requires {self.options.second_gate_blossoms} blossoms, but only {maxBlossoms} are in the pool."
                           f"Reducing second gate amount...")
            self.options.second_gate_blossoms.value = maxBlossoms
        if self.options.area_access != 0 and self.options.third_gate_blossoms > maxBlossoms:
            logger.warning(f"Baba Is You ({self.player_name}): Third gate requires {self.options.third_gate_blossoms} blossoms, but only {maxBlossoms} are in the pool."
                           f"Reducing third gate amount...")
            self.options.third_gate_blossoms.value = maxBlossoms
        if self.options.goal == 6 and self.options.goal_blossoms > maxBlossoms:
            logger.warning(f"Baba Is You ({self.player_name}): Goal requires {self.options.goal_blossoms} blossoms, but only {maxBlossoms} are in the pool."
                           f"Reducing goal amount...")
            self.options.goal_blossoms.value = maxBlossoms

        # Set area access based on goal
        if self.options.goal == 1: # Reach ???
            self.options.area_access.value = 1 # Map access
        if self.options.goal == 2: # Reach Depths
            self.options.area_access.value = 2 # ??? access
        if self.options.goal == 3: # Reach Meta
            self.options.area_access.value = 3 # Depths access
        if self.options.goal == 4: # Done
            self.options.area_access.value = 5 # Full access
        
        # Set exclusions based on area access
        if self.options.area_access == 0: # Early access
            self.options.exclude_whoa.value = True
            self.options.exclude_gallery.value = True
            self.options.exclude_write.value = True
            # When transformsanity is added, it will also be disabled here
        elif self.options.area_access == 1: # Map access
            self.options.exclude_whoa.value = True
            self.options.exclude_gallery.value = True
            self.options.exclude_write.value = True
        elif self.options.area_access == 2 or self.options.area_access == 3: # ??? or Depths access
            self.options.exclude_whoa.value = True
            self.options.exclude_gallery.value = True
        elif self.options.area_access == 4: # Meta access
            self.options.exclude_gallery.value = True
    
    # Mark words as early items to make generation fail less often
    def pre_fill(self):
        # DEBUG!!!
        #for region in self.level_shuffle_dict:
            #region2 = self.level_shuffle_dict[region]
            #print(region + " -> " + region2)

        # Mark common words as early items
        self.multiworld.early_items[self.player]["Baba"] = 1
        self.multiworld.early_items[self.player]["Is"] = 1
        self.multiworld.early_items[self.player]["You"] = 1
        self.multiworld.early_items[self.player]["Flag"] = 1
        self.multiworld.early_items[self.player]["Win"] = 1
        self.multiworld.early_items[self.player]["Push"] = 1
        self.multiworld.early_items[self.player]["And"] = 1

        # Decide on one area to be the "Early Area"
        early_area = "Lake"
        if self.options.open_map:
            early_areas = ["Lake", "Island", "Fall", "Ruins", "Forest", "Space", "Garden", "Chasm"]
            self.random.shuffle(early_areas)
            early_area = early_areas.pop()
        
        # If world keys are on, make the early area's key early
        if self.options.world_keys:
            #print(early_area)
            self.multiworld.early_items[self.player][f"{early_area} Key"] = 1

        # Get first level of that area, and make all words required early items
        firstLevel = f"{early_area}-1"
        if early_area == "Chasm": # Chasm doesn't have a level 1, use extra 1 instead
            firstLevel = "Chasm-Extra 1"
        if self.options.level_shuffle != 0 and self.level_shuffle_dict.get(firstLevel) != None:
            firstLevel = self.level_shuffle_dict.get(firstLevel)
        data = LEVEL_DATA[firstLevel]
        #print(firstLevel)
        if data.get("winLogic") != None:
            for word in data["winLogic"]:
               #print(word)
               self.multiworld.early_items[self.player][word] = 1

        # Unused: give even more early words
        """if self.options.level_shuffle == 0:
            # Include words needed early in some starting worlds
            if self.options.open_map:
                self.multiworld.early_items[self.player]["Sink"] = 1 # Blocks Lake
                self.multiworld.early_items[self.player]["Weak"] = 1 # Blocks Ruins
                self.multiworld.early_items[self.player]["Float"] = 1 # Blocks Island
                self.multiworld.early_items[self.player]["Tele"] = 1 # Blocks Fall
                self.multiworld.early_items[self.player]["Belt"] = 1 # Blocks Forest
                self.multiworld.early_items[self.player]["Shift"] = 1 # Also blocks Forest
                self.multiworld.early_items[self.player]["Empty"] = 1 # Blocks Space
                self.multiworld.early_items[self.player]["More"] = 1 # Blocks Chasm
            else:
                # Important words in Lake
                self.multiworld.early_items[self.player]["Sink"] = 1
                self.multiworld.early_items[self.player]["Crab"] = 1
                self.multiworld.early_items[self.player]["Keke"] = 1
                self.multiworld.early_items[self.player]["Move"] = 1
                self.multiworld.early_items[self.player]["Star"] = 1
                self.multiworld.early_items[self.player]["Pillar"] = 1
                self.multiworld.early_items[self.player]["Love"] = 1
        else:
            # Include more general common words early
            self.multiworld.early_items[self.player]["Rock"] = 1
            self.multiworld.early_items[self.player]["Wall"] = 1
            self.multiworld.early_items[self.player]["Keke"] = 1
            self.multiworld.early_items[self.player]["Move"] = 1
            self.multiworld.early_items[self.player]["Open"] = 1
            self.multiworld.early_items[self.player]["Defeat"] = 1"""
        
    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]) -> None:
        level_hint_data = {}
        for name in LEVEL_DATA:
            data = LEVEL_DATA[name]
            if data.get("map") == True or data.get("parent") == None:
                continue
            
            # TODO: Need to also do this for bonus, etc.
            locationName = data.get("name") + ": Win"
            # Get parent based where the level is placed
            mapName = name
            if self.options.level_shuffle != 0:
                for oldName in self.level_shuffle_dict:
                    name2 = self.level_shuffle_dict[oldName]
                    if name == name2: # This level got shuffled into the other one, get the old parent
                        mapName = oldName
                        break
                    
            location = self.multiworld.get_location(locationName, self.player)
            level_hint_data[location.address] = mapName
                            
            hint_data[self.player] = level_hint_data

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
    def create_item(self, name: str) -> items.BabaIsYouItem:
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
    def fill_slot_data(self) -> Mapping[str, Any]:
        # If you need access to the player's chosen options on the client side, there is a helper for that.
        slot_data = self.options.as_dict(
            "goal",
            "goal_levels",
            "goal_blossoms",
            "start_with_default_words",
            "open_map",
            "world_keys",
            "area_access",
            "exclude_whoa",
            "exclude_gallery",
            "exclude_write",
            "blossom_petals",
            "blossoms",
            "first_gate_blossoms",
            "second_gate_blossoms",
            "third_gate_blossoms",
            "complete_checks",
            "transformsanity",
            "level_shuffle",
        )
        slot_data["level_shuffle_dict"] = self.level_shuffle_dict
        return slot_data
