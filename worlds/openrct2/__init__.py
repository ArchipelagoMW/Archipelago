from typing import NamedTuple, Union
from enum import IntEnum
import logging
import json
import random
import math
import worlds.LauncherComponents as LauncherComponents

from .Options import *
from .Constants import *
from .Items import *
from .Locations import *

from BaseClasses import Item, Tutorial, ItemClassification, Region, Entrance
from worlds.generic.Rules import add_rule, set_rule, forbid_item

from ..AutoWorld import World, WebWorld
from NetUtils import SlotType


def launch_client() -> None: #Shoutout to Serpent.ai for the launcher code!
    from .Client import main
    LauncherComponents.launch_subprocess(main, name="OpenRCT2Client")


LauncherComponents.components.append(
    LauncherComponents.Component(
        "OpenRCT2 Client",
        func=launch_client,
        component_type=LauncherComponents.Type.CLIENT
    )
)

class OpenRCT2WebWorld(WebWorld):
    tutorials = []


class OpenRCT2Location(Location):
    game = "OpenRCT2"


class OpenRCT2World(World):
    """
    OpenRCT2 is a fan-made, open-source reimplementation of the classic simulation game. It faithfully preserves 
    the original game while introducing modern improvements and expanded features. Players can construct intricate 
    roller coasters, manage finances, and build the park of their dreams!
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
        "water_rides": item_info["water_rides"],
        "rides": item_info["rides"]
    }

    def __init__(self, multiworld, player: int):
        super().__init__(multiworld, player)
        # self.multiworld = multiworld
        # self.player = player
        self.starting_ride = None
        self.item_table = {}
        self.item_frequency = {}
        self.location_prices = []  # This list is passed to OpenRCT2 to create the unlock shop
        self.rules = []
        self.unique_rides = []

    # Okay future Colby, listen up. Here's the plan. We're going to take the item_table and shuffle it in the next
    # section. We'll generate the unlock shop with the item locations and apply our logic to it. Prereqs can only be
    # items one level lower on the tree. We then will set rules in create_regions that reflect our table.

    def generate_early(self) -> None:
        self.rules = [self.multiworld.difficult_guest_generation[self.player].value,
                      self.multiworld.difficult_park_rating[self.player].value,
                      self.multiworld.forbid_high_construction[self.player].value,
                      self.multiworld.forbid_landscape_changes[self.player].value,
                      self.multiworld.forbid_marketing_campaigns[self.player].value,
                      self.multiworld.forbid_tree_removal[self.player].value]
        # Grabs options for item generation
        scenario = self.multiworld.scenario[self.player].value
        # If the scenario is random, pick which random scenario it will be
        if scenario == 143:  # RCT1
            new_scenario = random.randint(0, 21)
            scenario = new_scenario
            self.multiworld.scenario[self.player].value = new_scenario
        elif scenario == 144:  # Corkscrew Follies
            new_scenario = random.randint(22, 51)
            scenario = new_scenario
            self.multiworld.scenario[self.player].value = new_scenario
        elif scenario == 145:  # Loopy Landscapes
            new_scenario = random.randint(52, 81)
            scenario = new_scenario
            self.multiworld.scenario[self.player].value = new_scenario
        elif scenario == 146:  # RCT2
            new_scenario = random.randint(82, 107)
            if new_scenario > 96:  # Throw extras in to capture the real parks later in the list
                new_scenario += 35
                if new_scenario == 136:  # Except ignore Fort Anachronism
                    new_scenario = 142
            scenario = new_scenario
            self.multiworld.scenario[self.player].value = new_scenario
        elif scenario == 147:  # Wacky Worlds
            new_scenario = random.randint(97, 113)
            scenario = new_scenario
            self.multiworld.scenario[self.player].value = new_scenario
        elif scenario == 148:  # Time Twister
            new_scenario = random.randint(114, 127)
            scenario = new_scenario
            self.multiworld.scenario[self.player].value = new_scenario
        elif scenario == 149:  # Random RCT1 + Expansions
            new_scenario = random.randint(0, 84)
            if new_scenario == 82:  # Include the out of place numbers in the IntEnum
                new_scenario = 128
            elif new_scenario == 83:
                new_scenario = 129
            elif new_scenario == 84:
                new_scenario = 130
            elif new_scenario == 85:
                new_scenario = 136
            scenario = new_scenario
            self.multiworld.scenario[self.player].value = new_scenario
        elif scenario == 150:  # Random RCT2 + Expansions
            new_scenario = random.randint(82, 142)
            while new_scenario == 128 or new_scenario == 129 or \
                    new_scenario == 130 or new_scenario == 136:  # Should have restructured the list, too late now! :D
                new_scenario = random.randint(82, 142)
            scenario = new_scenario
            self.multiworld.scenario[self.player].value = new_scenario

        monopoly_mode = self.multiworld.monopoly_mode[self.player].value
        include_gamespeed_items = self.multiworld.include_gamespeed_items[self.player].value
        furry_convention_traps = self.multiworld.furry_convention_traps[self.player].value
        spam_traps = self.multiworld.spam_traps[self.player].value
        bathroom_traps = self.multiworld.bathroom_traps[self.player].value
        filler = self.multiworld.filler[self.player].value
        rules = [self.multiworld.difficult_guest_generation[self.player].value,
                 self.multiworld.difficult_park_rating[self.player].value,
                 self.multiworld.forbid_high_construction[self.player].value,
                 self.multiworld.forbid_landscape_changes[self.player].value,
                 self.multiworld.forbid_marketing_campaigns[self.player].value,
                 self.multiworld.forbid_tree_removal[self.player].value]
        items = set_openRCT2_items(scenario, rules, monopoly_mode, include_gamespeed_items, furry_convention_traps, 
                                   spam_traps, bathroom_traps, filler)

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
        while not found_starter:
            candidate = random.choice(logic_table)
            if candidate in item_info["rides"]:
                if candidate not in item_info["non_starters"]:
                    self.starting_ride = candidate
                    self.item_frequency[candidate] -= 1
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
                locations.append(OpenRCT2Location(self.player, "OpenRCT2_" + str(location),
                                                  self.location_name_to_id["OpenRCT2_" + str(location)], region))
                location += 1
            return locations

        r = Region("Menu", self.player, self.multiworld)
        r.locations = []
        self.multiworld.regions.append(r)

        s = Region("Unlock Shop", self.player, self.multiworld)
        s.locations = []
        self.multiworld.regions.append(s)

        level0 = Region("OpenRCT2_Level_0", self.player, self.multiworld)  # Levels of the unlock tree
        level0.locations = [OpenRCT2Location(self.player, "OpenRCT2_0", self.location_name_to_id["OpenRCT2_0"], level0)]
        self.multiworld.regions.append(level0)

        level1 = Region("OpenRCT2_Level_1", self.player, self.multiworld)  # Levels of the unlock tree
        level1.locations = locations_to_region(1, 2, level1)
        self.multiworld.regions.append(level1)

        level2 = Region("OpenRCT2_Level_2", self.player, self.multiworld)  # Levels of the unlock tree
        level2.locations = locations_to_region(3, 6, level2)
        self.multiworld.regions.append(level2)

        level3 = Region("OpenRCT2_Level_3", self.player, self.multiworld)  # Levels of the unlock tree
        level3.locations = locations_to_region(7, 14, level3)
        self.multiworld.regions.append(level3)

        item = 15
        current_level = 4
        while (item + 7) < logic_length:
            level = Region("OpenRCT2_Level_" + str(current_level), self.player, self.multiworld)
            level.locations = locations_to_region(item, item + 7, level)
            self.multiworld.regions.append(level)
            item += 8
            current_level += 1

        level = Region("OpenRCT2_Level_" + str(current_level), self.player, self.multiworld)
        level.locations = locations_to_region(item, (logic_length - 1), level)
        self.multiworld.regions.append(level)

        victory = Region("Victory", self.player, self.multiworld)
        victory.locations = [OpenRCT2Location(self.player, "Victory", None, victory)]
        self.multiworld.regions.append(victory)

        r.connect(s)
        s.connect(self.multiworld.get_region("OpenRCT2_Level_0", self.player))
        count = 0
        while count < current_level:
            region = self.multiworld.get_region("OpenRCT2_Level_" + str(count), self.player)
            region.connect(self.multiworld.get_region("OpenRCT2_Level_" + str(count + 1), self.player))
            num_rides = 0
            if count == 0:
                pass
            elif count == 1:  # 3 total items, we want 2 to be rides
                num_rides = 2
            elif count == 2:  # 7 total items, we want 4 rides and a food stall
                num_rides = 4
                add_rule(region.exits[0], lambda state: state.has("Food Stall", self.player))
            elif count == 3:  # 15 total items, we want 10 rides and now a drink stall
                num_rides = 10
                add_rule(region.exits[0], lambda state: state.has("Drink Stall", self.player, 1))
            elif count == 4:  # 23 total items, we want 15 rides and now toilets
                num_rides = 15
                add_rule(region.exits[0], lambda state: state.has("Toilets", self.player, 1))
            elif count == 5:  # 31 total items, we want 20 rides and some rules if applicable
                num_rides = 20
                if self.rules[2] == 1:  # If high construction can be disabled
                    add_rule(region.exits[0], lambda state: state.has("Allow High Construction", self.player, 1))
                if self.rules[3] == 1:  # landscape
                    add_rule(region.exits[0], lambda state: state.has("Allow Landscape Changes", self.player, 1))
                if self.rules[5] == 1:  # tree removal
                    add_rule(region.exits[0], lambda state: state.has("Allow Tree Removal", self.player, 1))
                # add_rule(region.exits[0], lambda state: state.has("Cash Machine", self.player, 1))
                # add_rule(region.exits[0], lambda state: state.has("First Aid", self.player, 1))
            add_rule(region.exits[0], lambda state: state.has_group("rides", self.player, num_rides))
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

        # Adds the starting ride to precollected items
        # self.multiworld.precollected_items[self.player].append(self.create_item(self.starting_ride))

        self.multiworld.push_precollected(self.create_item(self.starting_ride))
        if not self.multiworld.include_gamespeed_items[self.player].value:# If the user doesn't want to unlock speed, give it to em for free
            count = 0
            while count < 4:
                self.multiworld.push_precollected(self.create_item("Progressive Speed"))
                count += 1

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

        def set_openRCT2_rule(rule_type, item, location_number):
            if rule_type == "ride":
                add_rule(self.multiworld.get_region(self.get_previous_region_from_OpenRCT2_location(number),
                                                    self.player).entrances[0],
                         lambda state, prereq=item: state.has(prereq, self.player))
                # Only add rules if there's an item to be unlocked in the first place
                if (item in item_info["requires_height"]) and (
                        self.multiworld.forbid_high_construction[self.player].value == 1):
                    add_rule(self.multiworld.get_region(self.get_previous_region_from_OpenRCT2_location(number),
                                                        self.player).entrances[0],
                             lambda state, prereq="Allow High Construction": state.has(prereq, self.player))
                    print(
                        "Added rule: \nHave: Allow High Construction\nLocation: " + self.get_previous_region_from_OpenRCT2_location(
                            location_number))
                if (item in item_info["requires_landscaping"]) and self.multiworld.forbid_landscape_changes[
                    self.player].value == 1:
                    add_rule(self.multiworld.get_region(self.get_previous_region_from_OpenRCT2_location(number),
                                                        self.player).entrances[0],
                             lambda state, prereq="Allow Landscape Changes": state.has(prereq, self.player))
                    print(
                        "Added rule: \nHave: Allow Landscape Changes\nLocation: " + self.get_previous_region_from_OpenRCT2_location(
                            location_number))
                print(self.multiworld.get_region(self.get_previous_region_from_OpenRCT2_location(number),
                                                 self.player).entrances)
                print("Added rule: \nHave: " + str(
                    chosen_prereq) + "\nLocation: " + self.get_previous_region_from_OpenRCT2_location(location_number))
            else:
                add_rule(self.multiworld.get_region(self.get_previous_region_from_OpenRCT2_location(number),
                                                    self.player).entrances[0],
                         # self.multiworld.get_location("OpenRCT2_" + str(number), self.player).parent_region.entrances[0],
                         lambda state, prereq=item: state.has_group(prereq, self.player))
                # TODO: Check if every item in the category has a rule requirement, and if so, force the rule to appear before the location
                # if item_info[item].issubset(item_info["requires_height"]):
                #     add_rule(self.multiworld.get_region(self.get_previous_region_from_OpenRCT2_location(number), self.player).entrances[0],
                #      lambda state, prereq="Allow High Construction": state.has(prereq, self.player))
                #     print("Added rule: \nHave: Allow High Construction\nLocation: " + self.get_previous_region_from_OpenRCT2_location(location_number))
                print(self.multiworld.get_region(self.get_previous_region_from_OpenRCT2_location(number),
                                                 self.player).entrances)
                print("Added rule: \nHave: " + str(
                    category) + "\nLocation: " + self.get_previous_region_from_OpenRCT2_location(location_number))

        difficulty = self.multiworld.difficulty[self.player].value
        length = self.multiworld.scenario_length[self.player].value
        length_modifier = 0
        difficulty_modifier = 0
        difficulty_minimum = 0
        difficulty_maximum = 2
        base_price = 500
        final_price = 500

        if difficulty == 0:  # very_easy
            difficulty_modifier = 0
        if difficulty == 1:  # easy
            difficulty_modifier = .3
            difficulty_maximum = 5
        if difficulty == 2:  # medium
            difficulty_modifier = .5
            difficulty_maximum = 6
        if difficulty == 3:  # hard
            difficulty_modifier = .75
            difficulty_minimum = 5
            difficulty_maximum = 7
        if difficulty == 4:  # extreme
            difficulty_modifier = .9
            difficulty_minimum = 6
            difficulty_maximum = 9

        if length == 0:  # speedrun
            length_modifier = .2
            final_price = 100000
        if length == 1:  # normal
            length_modifier = .4
            final_price = 250000
        if length == 2:  # lengthy
            length_modifier = .6
            final_price = 500000
        if length == 3:  # marathon
            length_modifier = .9
            final_price = 1000000

        print("This is the final price: " + str(final_price))
        possible_prereqs = [self.starting_ride]
        # Once we're finished with the given region, we'll add the queued prereqs to the possibles list
        queued_prereqs = []
        prereq_counter = 0
        total_price = base_price * len(logic_table)
        average_price = final_price / len(logic_table)
        if final_price < total_price:  # If everything being $500 is too expensive,
            base_price = final_price / len(logic_table)  # Make everything cheaper
        print("This is the base price: " + str(base_price))
        total_base = base_price * len(logic_table)
        remaining_amount = final_price - total_base
        increment = remaining_amount / (len(logic_table) * (len(logic_table) + 1) / 2)
        print("This is the increment: " + str(increment))
        print("with this many items: " + str(len(logic_table)))
        current_price = base_price
        for number, item in enumerate(logic_table):
            unlock = {"LocationID": number, "Price": 0, "Lives": 0, "RidePrereq": []}

            # Handles the price of each location
            if random.random() < 0.9 or number == 0:  # 90 percent of locations will have a cash price
                current_price = base_price + increment * number
                unlock["Price"] = int(current_price)
                # print(unlock["Price"])
            else:  # Everything else will cost lives. The Elder Gods will be pleased
                if number < 7:
                    unlock["Lives"] = random.randint(25, 150)
                elif number < 22:
                    unlock["Lives"] = random.randint(50, 300)
                else:
                    unlock["Lives"] = random.randint(50, 1000)

            # Handles the selection of a prerequisite and associated stats
            if number > 15 and unlock["Lives"] == 0:  # We'll never have a prereq on the first 15 items or on blood prices
                if (random.random() < length_modifier) or (len(logic_table) * .85 < number):  # Determines if we have a prereq
                    if random.random() < difficulty_modifier:  # Determines if the prereq is a specific ride
                        chosen_prereq = random.choice(possible_prereqs)
                        set_openRCT2_rule("ride", chosen_prereq, number)
                        if chosen_prereq in item_info["roller_coasters"] and chosen_prereq not in item_info[
                                "stat_exempt_roller_coasters"]:
                            excitement = 0
                            intensity = 0
                            nausea = 0
                            # 3 coin flips to determine what, if any, stat prereqs will be used
                            if random.random() < .5:
                                excitement = round(random.uniform(difficulty_minimum, difficulty_maximum), 1)
                            if random.random() < .5:
                                intensity = round(random.uniform(difficulty_minimum, difficulty_maximum), 1)
                            if random.random() < .5:
                                nausea = round(random.uniform(difficulty_minimum, difficulty_maximum - 2), 1)
                            unlock["RidePrereq"] = \
                                [random.randint(1, 3), chosen_prereq, excitement, intensity, nausea,0]
                        elif chosen_prereq in item_info["transport_rides"]:
                            unlock["RidePrereq"] = [random.randint(1, 3), chosen_prereq, 0, 0, 0, 0]
                        elif chosen_prereq in item_info["water_rides"]:
                            unlock["RidePrereq"] = [random.randint(1, 3), chosen_prereq, 0, 0, 0, 0]
                        else:
                            unlock["RidePrereq"] = [random.randint(1, 7), chosen_prereq, 0, 0, 0, 0]
                    else:  # Prereq is not a specific ride
                        category = "ride"
                        category_selected = False
                        while not category_selected:
                            category = random.choice(item_info["ride_types"])
                            for ride in possible_prereqs:
                                if ride in item_info[category]:
                                    category_selected = True
                        set_openRCT2_rule("category", category, number)
                        if category == "roller_coasters":
                            excitement = 0
                            intensity = 0
                            nausea = 0
                            # 3 coin flips to determine what, if any, stat prereqs will be used
                            if random.random() < .5: excitement = round(
                                random.uniform(difficulty_minimum, difficulty_maximum), 1)
                            if random.random() < .5: intensity = round(
                                random.uniform(difficulty_minimum, difficulty_maximum), 1)
                            if random.random() < .5: nausea = round(
                                random.uniform(difficulty_minimum, difficulty_maximum - 2), 1)
                            unlock["RidePrereq"] = \
                                [random.randint(1, 4), category, excitement, intensity, nausea, 0]
                        elif category == "transport_rides":
                            unlock["RidePrereq"] = [random.randint(1, 3), category, 0, 0, 0, 0]
                        elif category == "water_rides":
                            unlock["RidePrereq"] = [random.randint(1, 3), category, 0, 0, 0, 0]
                        else:
                            unlock["RidePrereq"] = [random.randint(1, 10), category, 0, 0, 0, 0]
            # Add the shop item to the shop prices
            self.location_prices.append(unlock)
            # Handle unlocked rides
            if item in item_info["rides"]:  # Don't put items in that require an impossible rule
                if not (self.multiworld.forbid_high_construction[self.player].value == 2 and item in item_info[
                        "requires_height"]):
                    if not (self.multiworld.forbid_landscape_changes[self.player].value == 2 and item in item_info[
                            "requires_landscaping"]):
                        queued_prereqs.append(item)
            if prereq_counter == 0 or prereq_counter == 2 or prereq_counter % 8 == 6:
                for prereq in queued_prereqs:
                    possible_prereqs.append(prereq)
                queued_prereqs.clear()
            prereq_counter += 1
        print("OpenRCT2 will make the shop will the following:")
        print(self.location_prices)

        # Okay, here's where we're going to take the last eligible rides in the logic table
        # and make them required for completion, if that's required.
        elligible_rides = [item for index, item in enumerate(logic_table) if
                           item in item_info["rides"] and item not in item_info["non_starters"]]
        elligible_rides = list(dict.fromkeys(elligible_rides))
        random.shuffle(elligible_rides)
        if self.multiworld.required_unique_rides[self.player].value:
            count = 0
            while count < self.multiworld.required_unique_rides[self.player].value:
                self.unique_rides.append(elligible_rides[count])
                count += 1
            # self.unique_rides = [elligible_rides[i] for i in
            #                     elligible_rides[-self.multiworld.required_unique_rides[self.player].value:]]
        print("Here's the eligible rides:")
        print(elligible_rides)
        print("Here's what was chosen:")
        print(self.unique_rides)
        for ride in self.unique_rides:
            add_rule(self.multiworld.get_region("Victory", self.player).entrances[0],
                     lambda state, prereq=ride: state.has(prereq, self.player))

    def generate_basic(self) -> None:
        # place "Victory" at the end of the unlock tree and set collection as win condition
        self.multiworld.get_location("Victory", self.player).place_locked_item(
            OpenRCT2Item("Victory", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def fill_slot_data(self):
        # archipelago_objectives = {Guests: [300, false], ParkValue: [0, false], RollerCoasters: [5,2,2,2,0,false],
        # RideIncome: [0, false], ShopIncome: [8000, false], ParkRating: [700, false], LoanPaidOff: [true, false],
        # Monopoly: [true, false]};
        guests = self.multiworld.guest_objective[self.player].value
        park_value = self.multiworld.park_value_objective[self.player].value
        roller_coasters = self.multiworld.roller_coaster_objective[self.player].value
        excitement = self.multiworld.roller_coaster_excitement[self.player].value
        intensity = self.multiworld.roller_coaster_intensity[self.player].value
        nausea = self.multiworld.roller_coaster_nausea[self.player].value
        park_rating = self.multiworld.park_rating_objective[self.player].value
        pay_off_loan = self.multiworld.pay_off_loan[self.player].value
        monopoly = self.multiworld.monopoly_mode[self.player].value
        unique_rides = self.unique_rides
        objectives = {"Guests": [guests, False], "ParkValue": [park_value, False],
                      "RollerCoasters": [roller_coasters, excitement, intensity, nausea, 0, False],
                      "RideIncome": [0, False], "ShopIncome": [0, False], "ParkRating": [park_rating, False],
                      "LoanPaidOff": [pay_off_loan, False], "Monopoly": [monopoly, False],
                      "UniqueRides": [unique_rides, False]}
        print(objectives)
        print(self.item_id_to_name)

        # Fixes Location Prices for OpenRCT2
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
        # from Utils import visualize_regions
        # visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")
        print("Here's the final unlock shop:")
        print(self.location_prices)
        return {
            "difficulty": self.multiworld.difficulty[self.player].value,
            "scenario_length": self.multiworld.scenario_length[self.player].value,
            "scenario": self.multiworld.scenario[self.player].value,
            "death_link": self.multiworld.deathlink[self.player].value,
            "randomization_range": self.multiworld.randomization_range[self.player].value,
            "stat_rerolls": self.multiworld.stat_rerolls[self.player].value,
            "randomize_park_values": self.multiworld.randomize_park_values[self.player].value,
            "visibility": self.multiworld.visibility[self.player].value,
            "rules": self.rules,
            "preferred_intensity": self.multiworld.preferred_intensity[self.player].value,
            "objectives": objectives,
            "location_prices": self.location_prices
        }

    def create_item(self, item: str) -> OpenRCT2Item:
        classification = ItemClassification.useful
        if item in item_info["rides"] or item in item_info["progression_rules"] or item in item_info["stalls"]:
            classification = ItemClassification.progression
        if item in item_info["filler_items"]:
            classification = ItemClassification.filler
        if item in item_info["trap_items"]:
            classification = ItemClassification.trap
        return OpenRCT2Item(item, classification, self.item_name_to_id[item], self.player)

    def get_previous_region_from_OpenRCT2_location(self, location_number: int):
        # print("Getting previous region from location: " + str(location_number))
        if location_number == 0:
            # print("OpenRCT2_Level_0")
            return "OpenRCT2_Level_0"
        elif location_number == 1 or location_number == 2:
            # print("OpenRCT2_Level_0")
            return "OpenRCT2_Level_0"
        elif location_number == 3 or location_number == 4 or location_number == 5 or location_number == 6:
            # print("OpenRCT2_Level_1")
            return "OpenRCT2_Level_1"
        else:
            divider = location_number - 6
            region = math.ceil(divider / 8) + 1
            # print("OpenRCT2_Level_" + str(region))
            return "OpenRCT2_Level_" + str(region)