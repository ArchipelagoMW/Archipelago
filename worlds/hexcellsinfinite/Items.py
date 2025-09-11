# So the goal here is to have a catalog of all the items in your game
# To correctly generate a games items, they need to be bundled in a list
# A list in programming terms is anything in square brackets [] to put it simply

# A list is described as a separated order of x where x is the type of variable within it
# IE: ["apple", "pear", "grape"] is a list of strings (anything inside "" OR '' are considered strings)

# Logging = output. How you'll figure out whats going wrong
import logging


# Built in AP imports
from BaseClasses import Item, ItemClassification

# These come from the other files in this example. If you want to see the source ctrl + click the name
# You can also do that ctrl + click for any functions to see what they do
from .Types import ItemData, HexcellsInfiniteItem
from .Locations import get_total_locations
from . import Options
from typing import List, Dict, TYPE_CHECKING

# This is just making sure nothing gets confused about what its doing exactly
if TYPE_CHECKING:
    from . import HexcellsInfiniteWorld

# If you're curious about the -> List[Item] that is a syntax to make sure you return the correct variable type
# In this instance we're saying we only want to return a list of items
# You'll see a bunch of other examples of this in other functions
# It's main purpose is to protect yourself from yourself
def create_itempool(world: "HexcellsInfiniteWorld") -> List[Item]:
    # This is the empty list of items. You'll add all the items in the game to this list
    itempool: List[Item] = []

    # In this function is where you would remove any starting items that you add in options such as starting chapter
    # This is also the place you would add dynamic amounts of items from options
    # This is also a good place to grab anything you need from options

    if world.options.LevelUnlockType == Options.LevelUnlockType.option_vanilla:
        itempool.extend(create_multiple_items(world, "Gem", 36))
    elif world.options.LevelUnlockType == Options.LevelUnlockType.option_individual:
        for item in hexcells_infinite_items.keys():
            if item != "Gem":
                itempool.append(create_item(world, item))

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

hexcells_infinite_items = {}

HEXCELLS_LEVEL_ITEMS = []

# Progression items
for world in range(1, 7):
    for level in range(1, 7):
        name = f"Hexcells {world}-{level}"
        hexcells_infinite_items[name] = ItemData(len(hexcells_infinite_items)+1, ItemClassification.progression)
        HEXCELLS_LEVEL_ITEMS.append(name)
hexcells_infinite_items["Gem"] = ItemData(len(hexcells_infinite_items)+1, ItemClassification.progression)

# This makes a really convenient list of all the other dictionaries
# (fun fact: {} is a dictionary)
item_table = {
    **hexcells_infinite_items
}
