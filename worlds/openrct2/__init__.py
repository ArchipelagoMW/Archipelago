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
    item_name_groups = {
            "roller_coasters": item_info["roller_coasters"],
            "transport_rides": item_info["transport_rides"],
            "gentle_rides": item_info["gentle_rides"],
            "thrill_rides": item_info["thrill_rides"],
            "water_rides": item_info["water_rides"]
        }
    
    def __init__(self, multiworld, player: int):
        super().__init__(multiworld, player)
        # self.multiworld = multiworld
        # self.player = player
        self.starting_ride = None
        self.item_table = {}
        self.item_frequency = {}
        self.location_prices = []#This list is passed to OpenRCT2 to create the unlock shop

    #Okay future Colby, listen up. Here's the plan. We're going to take the item_table and shuffle it in the next section. We'll generate the 
    #unlock shop with the item locations and apply our logic to it. Prereqs can only be items one level lower on the tree. We then will set 
    #rules in create_regions that reflect our table.

    def generate_early(self) -> None:
        #Grabs options for item generation
        scenario = self.multiworld.scenario[self.player].value
        monopoly_mode = self.multiworld.monopoly_mode[self.player].value
        furry_convention_traps = self.multiworld.furry_convention_traps[self.player].value
        spam_traps = self.multiworld.spam_traps[self.player].value
        bathroom_traps = self.multiworld.bathroom_traps[self.player].value
        rules = self.multiworld.include_park_rules[self.player].value
        filler = self.multiworld.filler[self.player].value
        items = set_openRCT2_items(scenario,monopoly_mode,furry_convention_traps,spam_traps,bathroom_traps,rules,filler)

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
        minimum_price = 500
        maximum_price = 500


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
            maximum_price = 25000
        if length == 1: #normal
            length_modifier = .4
            maximum_price = 50000
        if length == 2: #lengthy
            length_modifier = .6
            maximum_price = 75000
        if length == 3: #marathon
            length_modifier = .9
            maximum_price = 100000
            

        possible_prereqs = [self.starting_ride]
        queued_prereqs = [] #Once we're finished with the given region, we'll add the queued prereqs to the possibles list
        prereq_counter = 0
        for number, item in enumerate(logic_table):
            unlock = {"LocationID": number, "Price": 0, "Lives": 0, "RidePrereq": []}
            if random.random() < 0.95 or number == 0: #95 perecnt of locations will have a cash price
                unlock["Price"] = int(((maximum_price - minimum_price) * (number / len(logic_table))) + minimum_price)
                # print(unlock["Price"])
            else:# Everything else will cost lives. The Elder Gods will be pleased
                unlock["Lives"] = random.randint(50,1000)
            if number != 0 and unlock["Lives"] == 0: #We'll never have a prereq on the first item or on blood prices
                if random.random() < length_modifier: #Determines if we have a prereq
                    if random.random() < difficulty_modifier: #Determines if the prereq is a specific ride
                        chosen_prereq = random.choice(possible_prereqs)
                        add_rule(self.multiworld.get_location("OpenRCT2_" + str(number), self.player).parent_region.entrances[0],
                         lambda state: state.has(chosen_prereq, self.player))
                        if chosen_prereq in item_info["roller_coasters"]:
                            excitement = 0
                            intensity = 0
                            nausea = 0
                            #3 coin flips to determine what, if any, stat prereqs will be used
                            if random.random() < .5: excitement = round(random.uniform(difficulty_minimum, difficulty_maximum), 1)
                            if random.random() < .5: intensity = round(random.uniform(difficulty_minimum, difficulty_maximum), 1)
                            if random.random() < .5: nausea = round(random.uniform(difficulty_minimum, difficulty_maximum), 1)
                            unlock["RidePrereq"] = [random.randint(1,5),chosen_prereq,excitement,intensity,nausea,0]
                        else:
                            unlock["RidePrereq"] = [random.randint(1,7),chosen_prereq,0,0,0,0]
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
                        if category == "roller_coasters":
                            excitement = 0
                            intensity = 0
                            nausea = 0
                            #3 coin flips to determine what, if any, stat prereqs will be used
                            if random.random() < .5: excitement = round(random.uniform(difficulty_minimum, difficulty_maximum), 1)
                            if random.random() < .5: intensity = round(random.uniform(difficulty_minimum, difficulty_maximum), 1)
                            if random.random() < .5: nausea = round(random.uniform(difficulty_minimum, difficulty_maximum), 1)
                            unlock["RidePrereq"] = [random.randint(1,7),category,excitement,intensity,nausea,0]
                        else:
                            unlock["RidePrereq"] = [random.randint(1,10),category,0,0,0,0]
            #Add the shop item to the shop prices
            self.location_prices.append(unlock)
            #Handle unlocked rides
            if item in item_info["rides"]:
                queued_prereqs.append(item)
            if prereq_counter == 0 or prereq_counter == 2 or prereq_counter % 8 == 6:
                for prereq in queued_prereqs:
                    possible_prereqs.append(prereq)
                queued_prereqs.clear()
            prereq_counter += 1
        print("OpenRCT2 will make the shop will the following:")
        print(self.location_prices)

    def generate_basic(self) -> None:
        # place "Victory" at the end of the unlock tree and set collection as win condition
        self.multiworld.get_location("Victory", self.player).place_locked_item(OpenRCT2Item("Victory", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def fill_slot_data(self):
        #archipelago_objectives = {Guests: [300, false], ParkValue: [0, false], RollerCoasters: [5,2,2,2,0,false], RideIncome: [0, false], ShopIncome: [8000, false], ParkRating: [700, false], LoanPaidOff: [true, false], Monopoly: [true, false]};
        guests = self.multiworld.guest_objective[self.player].value
        park_value = self.multiworld.park_value_objective[self.player].value
        roller_coasters = self.multiworld.roller_coaster_objective[self.player].value
        excitement = self.multiworld.roller_coaster_excitement[self.player].value
        intensity = self.multiworld.roller_coaster_intensity[self.player].value
        nausea = self.multiworld.roller_coaster_nausea[self.player].value
        park_rating = self.multiworld.park_rating_objective[self.player].value
        pay_off_loan = self.multiworld.pay_off_loan[self.player].value
        monopoly = self.multiworld.monopoly_mode[self.player].value
        objectives = {"Guests": [guests, False], "ParkValue":[park_value, False], "RollerCoasters": [roller_coasters,excitement,intensity,nausea,0,False], "RideIncome": [0,False], "ShopIncome": [0,False], "ParkRating": [park_rating, False], "LoanPaidOff": [pay_off_loan, False], "Monopoly": [monopoly, False]}
        print(objectives)
        print(self.item_id_to_name)

        #Fixes Location Prices for OpenRCT2
        for index, location in enumerate(self.location_prices):
            # print("Here's the category! Maybe.")
            if self.location_prices[index]["RidePrereq"]:
                category = self.location_prices[index]["RidePrereq"][1]
                # print(self.location_prices[index]["RidePrereq"][1])
            else: 
                category = None
            if category in item_info["ride_types"]:
                if category == "roller_coasters":
                    self.location_prices[index]["RidePrereq"][1] = "rollercoaster"
                elif category == "transport_rides":
                    self.location_prices[index]["RidePrereq"][1] = "transport"
                elif category == "gentle_rides":
                    self.location_prices[index]["RidePrereq"][1] = "gentle"
                elif category == "thrill_rides":
                    self.location_prices[index]["RidePrereq"][1] = "thrill"
                else:
                    self.location_prices[index]["RidePrereq"][1] = "water"

        return {
            "difficulty": self.multiworld.difficulty[self.player].value,
            "scenario_length": self.multiworld.scenario_length[self.player].value,
            "scenario": self.multiworld.scenario[self.player].value,
            "death_link": self.multiworld.deathlink[self.player].value,
            "randomization_range": self.multiworld.randomization_range[self.player].value,
            "stat_rerolls": self.multiworld.stat_rerolls[self.player].value,
            "randomize_park_values": self.multiworld.randomize_park_values[self.player].value,
            "visibility": self.multiworld.visibility[self.player].value,
            "rules": self.multiworld.include_park_rules[self.player].value,
            "objectives": objectives,
            "location_prices": self.location_prices
        }

    def create_item(self, item:str) -> OpenRCT2Item:
        classification = ItemClassification.useful
        if item in item_info["rides"] or item in item_info["progression_rules"]:
            classification = ItemClassification.progression
        if item in item_info["filler_items"]:
            classification = ItemClassification.filler
        return OpenRCT2Item(item, classification, self.item_name_to_id[item], self.player)
