import json

from BaseClasses import ItemClassification, Tutorial, Item, Region, MultiWorld
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type, launch_subprocess

from worlds.glover.Options import GloverOptions
from worlds.glover.ItemPool import ItemPoolLookup

class GloverWeb(WebWorld):
    englishTut = Tutorial("",
                     """A guide for setting up Archipelago Glover on your computer.""",
                     "English",
                     "setup_en.md",
                     "setup/en",
                     ["Smg065"])
    tutorials = [englishTut]

class GloverWorld(World):
    """
    Glover is an N64 physics puzzle platformeing game.
    """
    game : str = "Glover"
    web = GloverWeb()
    topology_present = True
    item_name_to_id = {}
    options : GloverOptions
    all_items_table : ItemPoolLookup

    #Build Logic
    logic_file = open('Logic.json')
    logic_data = json.load(logic_file)

    #Check/Item Prefixes
    world_prefixes = ["Atl", "Crn", "Prt", "Pht", "FoF", "Otw"]
    level_prefixes = ["H", "1", "2", "3", "!", "?"]

    #Go over the lookup table to get the info to use
    for each_level_event in all_items_table.level_event_table:
        each_level_event
