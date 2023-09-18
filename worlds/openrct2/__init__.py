from typing import NamedTuple, Union
from enum import IntEnum
import logging
import json
import random
from .Options import *
from .Constants import *
from .Items import *
from .Locations import *

from BaseClasses import Item, Tutorial, ItemClassification, Region, Entrance
from worlds.generic.Rules import add_rule, set_rule, forbid_item

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
    starting_ride = None
    item_table = {}
    item_frequency = {}
    location_prices = {}
    item_name_groups = {
        "roller_coasters": item_info["roller_coasters"],
        "transport_rides": item_info["transport_rides"],
        "gentle_rides": item_info["gentle_rides"],
        "thrill_rides": item_info["thrill_rides"],
        "water_rides": item_info["water_rides"]
    }
    


    #Okay future Colby, listen up. Here's the plan. We're going to take the item_table and shuffle it in the next section. We'll generate the 
    #unlock shop with the item locations and apply our logic to it. Prereqs can only be items one level lower on the tree. We then will set 
    #rules in create_regions that reflect our table.

    def generate_early(self) -> None:
        #Grabs options for item generation
        monopoly_mode = self.multiworld.monopoly_mode[self.player].value
        furry_convention_traps = self.multiworld.furry_convention_traps[self.player].value
        spam_traps = self.multiworld.spam_traps[self.player].value
        bathroom_traps = self.multiworld.bathroom_traps[self.player].value
        rules = self.multiworld.include_park_rules[self.player].value
        filler = self.multiworld.filler[self.player].value
        items = set_openRCT2_items(monopoly_mode,furry_convention_traps,spam_traps,bathroom_traps,rules,filler)

        self.item_table = items[0]
        self.item_frequency = items[1]
        print("Here's the generated item table and frequency table... again")
        print(self.item_table)
        print("\n\n")
        print(self.item_frequency)

        logic_table = []
        for item in self.item_table:
            count = 0
            while count != self.item_frequency[item]:
                logic_table.append(item)
                count += 1

        found_starter = False
        while found_starter == False:
            canidate = random.choice(logic_table)
            if canidate in item_info["rides"]:
                if canidate not in item_info["non_starters"]:
                    self.starting_ride = canidate
                    self.item_frequency[canidate] -= 1
                    found_starter = True

        print("Here's the starting ride!")
        print(self.starting_ride)

         

    def create_regions(self) -> None:
        logic_table = []
        for item in self.item_table:
            count = 0
            while count != self.item_frequency[item]:
                logic_table.append(item)
                count += 1
        logic_length = (len(logic_table))
        # print("Here's the logic table:")
        # random.shuffle(logic_table)
        # print(logic_table)



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
        while (item + 7) < logic_length: 
            level = Region("OpenRCT2_Level_" + str(current_level), self.player, self.multiworld)
            level.locations = locations_to_region(item, item + 7,level)
            self.multiworld.regions.append(level)
            item += 8
            current_level += 1
        if ((logic_length) % 8)  != 0:
            level = Region("OpenRCT2_Level_" + str(current_level), self.player, self.multiworld)
            level.locations = locations_to_region(item, (logic_length - 1),level)
            self.multiworld.regions.append(level)
        else:
            current_level -= 1

        victory = Region("Victory", self.player, self.multiworld)
        victory.locations = [OpenRCT2Location(self.player,"Victory",None,victory)]
        self.multiworld.regions.append(victory)

        r.connect(s)
        s.connect(self.multiworld.get_region("OpenRCT2_Level_0",self.player))
        count = 0
        while count < current_level:
            region = self.multiworld.get_region("OpenRCT2_Level_" + str(count), self.player)
            region.connect(self.multiworld.get_region("OpenRCT2_Level_" + str(count + 1) ,self.player))
            count += 1
        final_region = self.multiworld.get_region("OpenRCT2_Level_" + str(current_level), self.player)
        final_region.connect(victory)


    def create_items(self) -> None:
        print("The item tabel is this long:")
        print(len(self.item_table))
        print(self.item_frequency)
        for item in self.item_table:
            count = 0
            while count != self.item_frequency[item]:
                self.multiworld.itempool.append(self.create_item(item))
                count += 1

        #Adds the starting ride to precollected items
        # self.multiworld.precollected_items[self.player].append(self.create_item(self.starting_ride))

        self.multiworld.push_precollected(self.create_item(self.starting_ride))

        print("Here's the multiworld item pool:")
        print(len(self.multiworld.itempool))
        print(self.multiworld.itempool)

    def generate_basic(self) -> None:
        # place "Victory" at the end of the unlock tree and set collection as win condition
        self.multiworld.get_location("Victory", self.player).place_locked_item(OpenRCT2Item("Victory", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)


    def set_rules(self) -> None:
        print("Here's the precollected Items")
        print(self.multiworld.precollected_items[self.player])
        logic_table = []
        for item in self.item_table:
            count = 0
            while count != self.item_frequency[item]:
                logic_table.append(item)
                count += 1
        print("Here's the logic table:")
        random.shuffle(logic_table)
        print(logic_table)

        difficulty = self.multiworld.difficulty[self.player].value
        length = self.multiworld.scenario_length[self.player].value
        length_modifier = 0
        difficulty_modifier = 0
        difficulty_minimum = 0
        difficulty_maximum = 0

        if difficulty == 0: #very_easy
            difficulty_modifier = 0
        if difficulty == 1: #easy
            difficulty_modifier = .3
            difficulty_maximum = 5
        if difficulty == 2: #medium
            difficulty_modifier = .5
            difficulty_maximum = 6
        if difficulty == 3: #hard
            difficulty_modifier = .75
            difficulty_minimum = 5
            difficulty_maximum = 7
        if difficulty == 4: #extreme
            difficulty_modifier = .9
            difficulty_minimum = 6
            difficulty_maximum = 9

        if length == 0: #speedrun
            length_modifier = .2
        if length == 1: #normal
            length_modifier = .4
        if length == 2: #lengthy
            length_modifier = .6
        if length == 3: #marathon
            length_modifier = .9
            

        possible_prereqs = [self.starting_ride]
        queued_prereqs = [] #Once we're finished with the given region, we'll add the queued prereqs to the possibles list
        prereq_counter = 0
        for number, item in enumerate(logic_table):
            if number != 0: #We'll never have a prereq on the first item
                if random.random() < length_modifier: #Determines if we have a prereq
                    if random.random() < difficulty_modifier: #Determines if the prereq is a specific ride
                        chosen_prereq = random.choice(possible_prereqs)
                        add_rule(self.multiworld.get_location("OpenRCT2_" + str(number), self.player).parent_region.entrances[0],
                         lambda state: state.has(chosen_prereq, self.player))
                    else: #Prereq is not a specific ride
                        category = "ride"
                        category_selected = False
                        while category_selected == False:
                            category = random.choice(item_info["ride_types"])
                            for ride in possible_prereqs:
                                if ride in item_info[category]:
                                    category_selected = True
                        add_rule(self.multiworld.get_location("OpenRCT2_" + str(number), self.player).parent_region.entrances[0],
                         lambda state: state.has_group(category, self.player))

            if item in item_info["rides"]:
                queued_prereqs.append(item)
            if prereq_counter == 0 or prereq_counter == 2 or prereq_counter % 8 == 6:
                for prereq in queued_prereqs:
                    possible_prereqs.append(prereq)
                queued_prereqs.clear()
            prereq_counter += 1

            # add_rule(self.multiworld.get_location("OpenRCT2_" + str(number), self.player),
            #  lambda state: state.has(self.starting_ride, self.player))


    
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


    def create_item(self, item:str) -> OpenRCT2Item:
        classification = ItemClassification.useful
        if item in item_info["rides"] or item in item_info["progression_rules"]:
            classification = ItemClassification.progression
        if item in item_info["filler_items"]:
            classification = ItemClassification.filler
        return OpenRCT2Item(item, classification, self.item_name_to_id[item], self.player)
