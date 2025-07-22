import json

from BaseClasses import ItemClassification, Tutorial, Item, Region, MultiWorld
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type, launch_subprocess
import random

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

    #Garib Logic
    garib_items = []
    match options.GaribLogic:
        #0: Level Garibs (No items to be sent)
        #Garib Groups
        case 1:
            garib_items = all_items_table.garib_table.copy()
        #Individual Garibs
        case 2:
            garib_dict = {}
            #Go over the list of garibs
            for each_garib_table in all_items_table.garib_table:
                #Keep the world info
                garib_name_list = each_garib_table[0].split()
                garib_item_name = garib_name_list[0] + " " + garib_name_list[2]
                #Apply the number of garibs to the group
                garib_count = int(garib_name_list[1]) * each_garib_table[1]
                if not garib_name_list in garib_dict:
                    garib_dict[garib_name_list] = garib_count
                else:
                    garib_dict[garib_name_list] += garib_count
            #Aplpy the items to the garib items list
            for garib_names, garib_counts in garib_dict.items():
                garib_items.append([garib_names, garib_counts])

    #Decoupling Garibs from Levels
    if options.GaribSorting > 0 & options.GaribLogic != 0:
        for each_garib_item in garib_items:
            each_garib_item[0] = each_garib_item[0][5:]
    
    #Checkpoint Logic
    checkpoint_items = []
    spawn_checkpoint = [
        2,3,3,
        4,5,4,
        3,3,4,
        3,4,4,
        3,3,5,
        2,1,4]
    if options.SpawningCheckpointRandomizer:
        for eachItem in spawn_checkpoint.count():
            spawn_checkpoint[eachItem] = random.randint(1, spawn_checkpoint[eachItem])
    else:
        for eachItem in spawn_checkpoint.count():
            spawn_checkpoint[eachItem] = 1

    #