from typing import NamedTuple, Union
import logging
import json
import random
from .Options import *
from .Constants import *
from .Items import *
from .Locations import *

from BaseClasses import Item, Tutorial, ItemClassification, Region, Entrance

from ..AutoWorld import World, WebWorld
from NetUtils import SlotType


class OpenRCT2WebWorld(WebWorld):
    tutorials = []

class OpenRCT2Location(Location):
    game = "OpenRCT2"

class OpenRCT2World(World):
    """
    OpenRCT2 is an awesome game! Blow up roller coasters!
    """

    game = "OpenRCT2"
    
    option_definitions = openRCT2_options  # options the player can set
    topology_present = True  # show path to required location checks in spoiler
    item_name_to_id = {name: id for id, name in enumerate(item_info["all_items"], base_id)}
    location_name_to_id = {name: id for id, name in enumerate(location_info["all_locations"], base_id)}
    item_table = {}
    item_frequency = {}
    
    # print("Here's the item_name_to_id dictionary:")
    # print(item_name_to_id)

    # print("Here's the location_name_to_id dictionary:")
    # print(location_name_to_id)

    # print("Monopoly Mode is enabled?")
    # print(self.multiworld.monopoly_mode[self.player])
    # if self.multiworld.monopoly_mode[self.player]:
    #     item_frequency["Land Discount"] = 20
    #     item_frequency["Construction Rights Discount"] = 20


    #Okay future Colby, listen up. Here's the plan. We're going to take the item_table and shuffle it in the next section. We'll generate the 
    #unlock shop with the item locations and apply our logic to it. Prereqs can only be items one level lower on the tree. We then will set 
    #rules in create_regions that reflect our table.

    def generate_early(self) -> None:
        #Grabs options for item generation
        monopoly_mode = self.multiworld.monopoly_mode[self.player].value
        furry_convention_traps = self.multiworld.furry_convention_traps[self.player].value
        spam_traps = self.multiworld.spam_traps[self.player].value
        bathroom_traps = self.multiworld.bathroom_traps[self.player].value
        items = set_openRCT2_items(monopoly_mode,furry_convention_traps,spam_traps,bathroom_traps)

        self.item_table = items[0]
        self.item_frequency = items[1]
        print("Here's the generated item table and frequency table... again")
        print(self.item_table)
        print("\n\n")
        print(self.item_frequency)

         

    def create_regions(self) -> None:
        logic_table = []
        for item in self.item_table:
            count = 0
            while count != self.item_frequency[item]:
                logic_table.append(item)
                count += 1
        print("Here's the logic table:")
        random.shuffle(logic_table)
        print(logic_table)

        def locations_to_region(location, ending_location, region):
            locations = []
            while location < ending_location + 1:
                locations.append(OpenRCT2Location(self.player,"OpenRCT2_" + str(location),self.location_name_to_id["OpenRCT2_" + str(location)],region))
                location += 1
            return locations

        r = Region("Menu", self.player, self.multiworld)
        r.locations = []
        self.multiworld.regions.append(r)
        
        s = Region("Unlock Shop", self.player, self.multiworld)
        s.locations = []
        self.multiworld.regions.append(s)

        level0 = Region("OpenRCT2_Level_0", self.player, self.multiworld) #Levels of the unlock tree
        level0.locations = [OpenRCT2Location(self.player,"OpenRCT2_0",self.location_name_to_id["OpenRCT2_0"],level0)]
        self.multiworld.regions.append(level0)

        level1 = Region("OpenRCT2_Level_1", self.player, self.multiworld) #Levels of the unlock tree
        level1.locations = locations_to_region(1,2,level1)
        self.multiworld.regions.append(level1)

        level2 = Region("OpenRCT2_Level_2", self.player, self.multiworld) #Levels of the unlock tree
        level2.locations = locations_to_region(3,6,level2)
        self.multiworld.regions.append(level2)

        level3 = Region("OpenRCT2_Level_3", self.player, self.multiworld) #Levels of the unlock tree
        level3.locations = locations_to_region(7,14,level3)
        self.multiworld.regions.append(level3)

        item = 15
        current_level = 4
        while (item + 7) < len(logic_table): 
            level = Region("OpenRCT2_Level_" + str(current_level), self.player, self.multiworld)
            level.locations = locations_to_region(item, item + 7,level)
            self.multiworld.regions.append(level)
            item += 8
            current_level += 1
        print(len(logic_table))
        if ((len(logic_table)) % 8)  != 0:
            level = Region("OpenRCT2_Level_" + str(current_level), self.player, self.multiworld)
            level.locations = locations_to_region(item, (len(logic_table) - 1),level)
            self.multiworld.regions.append(level)
        else:
            current_level -= 1

        # for region_number, item in enumerate(logic_table):
        #     region = Region("OpenRCT2_Region_" + str(region_number), self.player, self.multiworld)
        #     region.locations = [OpenRCT2Location(self.player,"OpenRCT2_" + str(region_number),self.location_name_to_id["OpenRCT2_" + str(region_number)],region)]
        #     self.multiworld.regions.append(region)

        r.connect(s)
        s.connect(self.multiworld.get_region("OpenRCT2_Level_0",self.player))
        count = 0
        while count < current_level:
            region = self.multiworld.get_region("OpenRCT2_Level_" + str(count), self.player)
            region.connect(self.multiworld.get_region("OpenRCT2_Level_" + str(count + 1) ,self.player))
            count += 1

        

        
                
    
    def create_items(self) -> None:
        print("The item tabel is this long:")
        print(len(self.item_table))
        print(self.item_frequency)
        for item in self.item_table:
            count = 0
            while count != self.item_frequency[item]:
                self.multiworld.itempool.append(self.create_item(item))
                count += 1

        print("Here's the multiworld item pool:")
        print(len(self.multiworld.itempool))
        print(self.multiworld.itempool)


    
        ##All this is on the chopping block
        # t = Region("No Prereqs", self.player, self.multiworld)
        # # Add unlocks that are just prices traced back to location 0. Anything with a ride requirement or after an item with a ride requirement won't appear here
        # NoPrereqs = []
        # for index, item in enumerate(openRCT2_items):
        # #if self.Options["difficulty"] == 0:
        #     NoPrereqs.append(OpenRCT2Location(self.player,"OpenRCT2_" + str(index),self.location_name_to_id["OpenRCT2_" + str(index)],t))
        
        # print("Region.locations: " + str(region))
        # print(region.locations[0].address)

        # t.locations = NoPrereqs
        # self.multiworld.regions.append(t)

        # If entrances are not randomized, they should be connected here, otherwise
        # they can also be connected at a later stage.
        # self.multiworld.get_entrance("New Game", self.player).connect(self.multiworld.get_region("Unlock Shop", self.player))
        # self.multiworld.get_entrance("No Prereqs", self.player).connect(self.multiworld.get_region("No Prereqs", self.player))
        #self.multiworld.get_entrance("Category ", self.player).connect(self.multiworld.get_region("No Prereqs", self.player))

        # for region_number, item in enumerate(logic_table):
        #     region = self.multiworld.get_region("OpenRCT2_Region_" + str(region_number), self.player)
        #     if region_number == 0:
        #         region.connect(self.multiworld.get_region("OpenRCT2_Region_1", self.player))
        #         region.connect(self.multiworld.get_region("OpenRCT2_Region_2", self.player))
        #     elif region_number == 1:
        #         region.connect(self.multiworld.get_region("OpenRCT2_Region_3", self.player))
        #         region.connect(self.multiworld.get_region("OpenRCT2_Region_4", self.player))
        #     elif region_number == 2:
        #         region.connect(self.multiworld.get_region("OpenRCT2_Region_5", self.player))
        #         region.connect(self.multiworld.get_region("OpenRCT2_Region_6", self.player))
        #     elif region_number == 3:
        #         region.connect(self.multiworld.get_region("OpenRCT2_Region_7", self.player))
        #         region.connect(self.multiworld.get_region("OpenRCT2_Region_8", self.player))
        #     elif region_number == 4:
        #         region.connect(self.multiworld.get_region("OpenRCT2_Region_9", self.player))
        #         region.connect(self.multiworld.get_region("OpenRCT2_Region_10", self.player))
        #     elif region_number == 5:
        #         region.connect(self.multiworld.get_region("OpenRCT2_Region_11", self.player))
        #         region.connect(self.multiworld.get_region("OpenRCT2_Region_12", self.player))
        #     elif region_number == 6:
        #         region.connect(self.multiworld.get_region("OpenRCT2_Region_13", self.player))
        #         region.connect(self.multiworld.get_region("OpenRCT2_Region_14", self.player))
        #     elif region_number < len(logic_table) - 8:
        #         region.connect(self.multiworld.get_region("OpenRCT2_Region_" + str(region_number + 8), self.player))


    def create_item(self, name:str) -> OpenRCT2Item:
        return OpenRCT2Item(name, ItemClassification.progression, self.item_name_to_id[name], self.player)
