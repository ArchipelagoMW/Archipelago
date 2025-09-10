# So the goal here is to have a catalog of all the items in your game
# To correctly generate a games items they need to be bundled in a list
# A list in programming terms is anything in square brackets [] to put it simply

# When a list is described its described as a list of x where x is the type of variable within it
# IE: ["apple", "pear", "grape"] is a list of strings (anything inside "" OR '' are considered strings)

# Logging = output. How you'll figure out whats going wrong
import logging
import random

# Built in AP imports
from BaseClasses import Item, ItemClassification

# These come from the other files in this example. If you want to see the source ctrl + click the name
# You can also do that ctrl + click for any functions to see what they do
from .Types import ItemData, HexcellsInfiniteItem
from .Locations import get_total_locations
from . import Options
from typing import List, Dict, TYPE_CHECKING

# This is just making sure nothing gets confused dw about what its doing exactly
if TYPE_CHECKING:
    from . import HexcellsInfiniteWorld


level_start = ""

def get_level_start():
    global level_start
    return level_start

# If you're curious about the -> List[Item] that is a syntax to make sure you return the correct variable type
# In this instance we're saying we only want to return a list of items
# You'll see a bunch of other examples of this in other functions
# It's main purpose is to protect yourself from yourself
def create_itempool(world: "HexcellsInfiniteWorld") -> List[Item]:
    # This is the empty list of items. You'll add all the items in the game to this list
    itempool: List[Item] = []

    # In this function is where you would remove any starting items that you add in options such as starting chapter
    # This is also the place you would add dynamic amounts of items from options
    # I can point to Sly Cooper and the Thievious Raccoonus since I did that

    # This is a good place to grab anything you need from options
    # starting_chapter = chapter_type_to_name[ChapterType(world.options.StartingChapter)]

    global level_start
    level_start = random.choice(list(hexcells_infinite_items.keys()))
    print(level_start)
    if (world.options.LevelUnlockType == Options.LevelUnlockType.option_vanilla):
        print("Creating Gem Items")
        itempool.extend(create_multiple_items(world,hexcells_infinite_items["Gem"],36))
    elif (world.options.LevelUnlockType == Options.LevelUnlockType.option_individual):
        for item in hexcells_infinite_items.keys():
            if(item != level_start and item != "Gem"):
                itempool.append(create_item(world, hexcells_infinite_items[item]))

    return itempool

# This is a generic function to create a singular item
def create_item(world: "HexcellsInfiniteWorld", name: str) -> Item:
    data = item_table[name]
    return HexcellsInfiniteItem(name, data.classification, data.ap_code, world.player)

# Another generic function. For creating a bunch of items at once!
def create_multiple_items(world: "HexcellsInfiniteWorld", name: str, count: int,
                          item_type: ItemClassification = ItemClassification.progression) -> List[Item]:
    data = item_table[name]
    itemlist: List[Item] = []

    for i in range(count):
        itemlist += [HexcellsInfiniteItem(name, item_type, data.ap_code, world.player)]

    return itemlist

# Time for the fun part of listing all of the items
# Watch out for overlap with your item codes
# These are just random numbers dont trust them PLEASE
# I've seen some games that dynamically add item codes such as DOOM as well

hexcells_infinite_items = {
    # Progression items
    "Gem": ItemData(0, ItemClassification.progression),
            "1-1": ItemData(1, ItemClassification.progression),
            "1-2": ItemData(2, ItemClassification.progression),
            "1-3": ItemData(3, ItemClassification.progression),
            "1-4": ItemData(4, ItemClassification.progression),
            "1-5": ItemData(5, ItemClassification.progression),
            "1-6": ItemData(6, ItemClassification.progression),

            "2-1": ItemData(7, ItemClassification.progression),
            "2-2": ItemData(8, ItemClassification.progression),
            "2-3": ItemData(9, ItemClassification.progression),
            "2-4": ItemData(10, ItemClassification.progression),
            "2-5": ItemData(11, ItemClassification.progression),
            "2-6": ItemData(12, ItemClassification.progression),

            "3-1": ItemData(13, ItemClassification.progression),
            "3-2": ItemData(14, ItemClassification.progression),
            "3-3": ItemData(15, ItemClassification.progression), 
            "3-4": ItemData(16, ItemClassification.progression),
            "3-5": ItemData(17, ItemClassification.progression),
            "3-6": ItemData(18, ItemClassification.progression),

            "4-1": ItemData(19, ItemClassification.progression),
            "4-2": ItemData(20, ItemClassification.progression),
            "4-3": ItemData(21, ItemClassification.progression),
            "4-4": ItemData(22, ItemClassification.progression),
            "4-5": ItemData(23, ItemClassification.progression),
            "4-6": ItemData(24, ItemClassification.progression),

            "5-1": ItemData(25, ItemClassification.progression),
            "5-2": ItemData(26, ItemClassification.progression),
            "5-3": ItemData(27, ItemClassification.progression),
            "5-4": ItemData(28, ItemClassification.progression),
            "5-5": ItemData(29, ItemClassification.progression),
            "5-6": ItemData(30, ItemClassification.progression),

            "6-1": ItemData(31, ItemClassification.progression),
            "6-2": ItemData(32, ItemClassification.progression),
            "6-3": ItemData(33, ItemClassification.progression),
            "6-4": ItemData(34, ItemClassification.progression),
            "6-5": ItemData(35, ItemClassification.progression),
            "6-6": ItemData(36, ItemClassification.progression)
    }
    


# This makes a really convenient list of all the other dictionaries
# (fun fact: {} is a dictionary)
item_table = {
    **hexcells_infinite_items
}