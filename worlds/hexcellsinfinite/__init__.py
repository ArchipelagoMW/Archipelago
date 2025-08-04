# This is where your imports go. That means any functions or variables that you want to use here but exist in another file
# What I have here is just some of the basic Archipelago classes that are widely used

# A more indepth explanation of the types of imports
# THE LINES FROM 7-12 ARE EXAMPLE IMPORTS AND NOT NECESSARILY REQUIRED

# import random
# With that import you are importing every single function, class, variable, whatever else that is allowed to be imported from random. Super useful and simple but somewhat bulky

# from random import randrange
# Here you are only grabbing the randrange function from random. This is less bulky but you need to put exactly what you want from that file/library
# If you want more things from the import add a comma like the worlds.AutoWorld import below
import logging

from BaseClasses import MultiWorld, Item, Tutorial
from worlds.AutoWorld import World, CollectionState, WebWorld
from typing import Dict

from .Locations import get_location_names, get_total_locations
from .Items import create_item, create_itempool, item_table
from .Options import APSkeletonOptions
from .Regions import create_regions
from .Types import ChapterType, chapter_type_to_name

# This is where you setup the page on the site!
# Typically is the name of your game with web
# Whatever you named the folder you are holding all of this in
class APSkeletonWeb(WebWorld):
    # Theres a few different themes so have fun with it
    theme = "Party"
    
    # You shouldnt have to change much here except the name at the bottom!
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up (the game you are randomizing) for Archipelago. "
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Nep (but you would put your name!)"]
    )]

# This class is the real meat and potatoes
# Same as the first class its normally named whatever you named your folder with World at the end
class APSkeletonWorld(World):
    """
    This is where you describe your game. Pretend you are marketing the game and that people have no clue what it is.
    Or make it silly. Whatever you wish I have no control over you.
    """

    # You want to put the full name of the game here. If you shortened the name for the folder and class names, dont do that here
    game = "APSkeleton"
    # The item_table will be setup in  your Items.py. This line gets all the items you put into item_table and puts it in a way that AP can understand it
    item_name_to_id = {name: data.ap_code for name, data in item_table.items()}
    # get_location_names() will come from your Locations.py
    location_name_to_id = get_location_names()
    # And these 2 are the name of your Options.py class. 
    options_dataclass = APSkeletonOptions
    options = APSkeletonOptions
    # The name of the class above
    web = APSkeletonWeb()
    # print("🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀")

    # There are other built in variables for AP. You can look at other worlds to see your options
    # Like PLEASE look at the various worlds. Its so helpful. Find one you like and you can duplicate a bunch of it

    # This is where you put stuff that need to be done RIGHT away. Typically you can just leave it alone but it can be useful to pop some things here as needed
    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

    # Generate early you do things just before the generation
    # Super important for doing things like adjusting the item pool based on options and the like
    # Can technically be skipped if you dont need to do anything or if you handle it elsewhere like a short hike
    def generate_early(self):
        # I highly recommend looking at other apworlds init files to see some examples
        # sly1 (hey i did that), ahit, and bomb rush cyberfunk are some good ones
        starting_chapter = chapter_type_to_name[ChapterType(self.options.StartingChapter)]

        # Push precollected is how you give your player items they need to start with
        # This is for options though. Dont worry about the starting inventory option thats in all yamls
        # AP handles that one
        self.multiworld.push_precollected(self.create_item(starting_chapter))

    # Regions are the different locations in your world. So like Undead Burgh in dark souls or Pacifilog Town in pokemon
    # They dont have to match your game, they can be whatever you need them to be for organization
    def create_regions(self):
        # This function comes from your Regions.py and dont worry that it matches the function that its in
        create_regions(self)

        # You can also use this space to do other location creation activities
        # Like if an option is enabled to add extra locations
        # Or the opposite, whatever it is. Just be careful that you arent duplicating locations

    # These are some examples of creating items. The create_itempool(self) function is coming from Items.py in this instance
    # The important part is that the items get into the self.multiworld.itempool as a list of Items
    # Ill try to explain better in the Items.py file 
    def create_items(self):
        self.multiworld.itempool += create_itempool(self)

    # This is just a helper function for turning names into Items. You could do some other stuff here as well
    # ahit does similar if you want another look and bomb rush cyberfunk does it in a slightly different way by turning it into a specific item for that game
    # Again hopefully I do a better job of explaining the Items.py file
    def create_item(self, name: str) -> Item:
        return create_item(self, name)
    
    # The slot data is what youre sending to the AP server kinda. You dont have to add all your options. Really you want the ones you think a pop tracker would use
    # Seed, Slot, and TotalLocations are all super important for AP though, you need those
    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {
            "options": {
                "StartingPlace":            self.options.StartingChapter.value,
                "ExtraLocations":           self.options.ExtraLocations.value,
                "TrapChance":               self.options.TrapChance.value,
                "ForcefemTrapWeight":       self.options.ForcefemTrapWeight.value,
                "SpeedChangeTrapWeight":    self.options.SpeedChangeTrapWeight.value
            },
            "Seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "Slot": self.multiworld.player_name[self.player],  # to connect to server
            "TotalLocations": get_total_locations(self) # get_total_locations(self) comes from Locations.py
        }

        return slot_data
    
    # These are used by AP to add and remove items from the player. You can probably just leave them alone
    def collect(self, state: "CollectionState", item: "Item") -> bool:
        return super().collect(state, item)
    
    def remove(self, state: "CollectionState", item: "Item") -> bool:
        return super().remove(state, item)