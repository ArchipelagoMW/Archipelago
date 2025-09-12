# This is where your imports go. That means any functions or variables that you want to use here but exist in another file
# What I have here is just some of the basic Archipelago classes that are widely used
# If you want more things from the import, add a comma like the worlds.AutoWorld import below
import logging

from BaseClasses import MultiWorld, Item, Tutorial
from worlds.AutoWorld import World, WebWorld
from .Locations import get_location_names, get_total_locations
from .Items import create_item, create_itempool, item_table, HEXCELLS_LEVEL_ITEMS 
from .Options import HexcellsInfiniteOptions
from .Regions import create_regions
from .Rules import set_rules

# This is where you setup the page on the site!
# Typically is the name of your game with "WebWorld"
# Whatever you named the folder you are holding all of this in
class HexcellsInfiniteWebWorld(WebWorld):
    # Theres a few different themes so have fun with it
    theme = "partyTime"
    
    # You shouldnt have to change much here except the name at the bottom!
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Hexcells Infinite for Archipelago. "
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "setup_en.md",
        "setup/en",
        ["ExpandedReality"]
    )]

# This class is the real meat and potatoes
# Same as the first class, it's normally named whatever you named your folder with "World" at the end
class HexcellsInfiniteWorld(World):
    """
    Hexcells Infinite is a deterministic minesweeper puzzle game. \nIf you like Minesweeper, but hate guessing, this is the game for you.
    """
    
    # You want to put the full name of the game here. If you shortened the name for the folder and class names, dont do that here
    game = "Hexcells Infinite"
    # The item_table will be setup in your Items.py. This line gets all the items you put into item_table and puts it in a way that AP can understand it
    item_name_to_id = {name: data.ap_code for name, data in item_table.items()}
    # get_location_names() will come from your Locations.py
    location_name_to_id = get_location_names()
    # And these 2 are the name of your Options.py class. 
    options_dataclass = HexcellsInfiniteOptions
    options: HexcellsInfiniteOptions
    # The name of the class above
    web = HexcellsInfiniteWebWorld()

    # This is where you'd do things just before the generation
    # Super important for doing things like adjusting the item pool based on options and the like
    # Can technically be skipped if you don't need to do anything, or if you handle it elsewhere like A Short Hike
    # I highly recommend looking at other apworlds init files to see some examples
    def generate_early(self):
        # Push precollected is how you give your player items they need to start with
        # This can be dependent based on your Options, like I do below 
        # Don't worry about the starting inventory option, that's in all yamls. AP handles that one

        if self.options.LevelUnlockType == Options.LevelUnlockType.option_individual :
            level_start = self.random.choice(HEXCELLS_LEVEL_ITEMS)
            self.multiworld.push_precollected(create_item(self, level_start))
            
    # Regions are the different locations in your world. So like Undead Burg in Dark Souls or Pacifilog Town in Pokemon
    # They don't have to match the name in-game, they can be whatever you need them to be for organization
    def create_regions(self):
        # This function comes from your Regions.py, don't worry that it matches the function that it's in
        create_regions(self)
        
        # You can also use this space to do other location creation activities
        # Like if an option is enabled, this is where you'd add extra locations
        # Or the opposite, whatever it is. Just be careful that you aren't duplicating locations

    def set_rules(self):
        set_rules(self)

    # The create_itempool(self) function is coming from Items.py in this instance
    # The important part is that the items get into the self.multiworld.itempool as a list of Items
    # Look at the Items.py file for more explanation
    def create_items(self):
        self.multiworld.itempool += create_itempool(self)

    # This is just a helper function for turning names into Items. You could do some other stuff here as well
    # A Hat In Time does similar if you want another look, and Bomb Rush Cyberfunk does it in a slightly different way by turning it into a specific item for that game
    def create_item(self, name: str) -> Item:
        return create_item(self, name)
    
    # The slot data is what you're sending to the AP server. You dont have to add all your options, but if it's needed to be used for your game implementation, then it should be added.
    # Seed, Slot, and TotalLocations are all super important for AP though, you need those
    def fill_slot_data(self) -> dict[str, object]:
        slot_data: dict[str, object] = {
            "options": {
                  "RequirePerfectClears":     self.options.RequirePerfectClears.value,
                  "PuzzleOptions":            self.options.PuzzleOptions.value,
                  "EnableShields":            self.options.EnableShields.value,
                  "LevelUnlockType":          self.options.LevelUnlockType.value,
                  "HardGeneration":           self.options.HardGeneration.value
            },
            "Seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "Slot": self.player_name,  # to connect to server
            "TotalLocations": get_total_locations(self) # get_total_locations(self) comes from Locations.py
        }

        return slot_data
