import math
from typing import TextIO
from Utils import local_path

import worlds.LauncherComponents as LauncherComponents
from BaseClasses import ItemClassification, Region, Location, Tutorial
from worlds.generic.Rules import add_rule

from .Constants import base_id, apworld_version
from .data.scenario_info import scenario_info
from .data.item_info import item_info
from .data.location_info import location_info
from .Items import OpenRCT2Item, set_openRCT2_items
from .Options import openRCT2Options, Scenario, openrct2_option_groups
from worlds.AutoWorld import World, WebWorld


class OpenRCT2WebWorld(WebWorld):
    theme = "partyTime"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the OpenRCT2 randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Crazycolbster"]
    )

    tutorials = [setup_en]
    option_groups = openrct2_option_groups


class OpenRCT2Location(Location):
    game = "OpenRCT2"


def launch_client() -> None:  # Shoutout to Serpent.ai for the launcher code!
    from .Client import main
    LauncherComponents.launch_subprocess(main, name="OpenRCT2Client")


LauncherComponents.components.append(
    LauncherComponents.Component(
        "OpenRCT2 Client",
        func=launch_client,
        component_type=LauncherComponents.Type.CLIENT,
        # OpenRCT2 icon credit to the OpenRCT2 team: 
        # https://github.com/OpenRCT2/OpenRCT2/blob/develop/resources/logo/icon_x96.png
        icon='openrct2icon' 
    )
)


LauncherComponents.icon_paths['openrct2icon'] = f"ap:{__name__}/icons/openrct2icon.png"

def get_previous_region_from_OpenRCT2_location(location_number: int):
    if location_number <= 2:
        return "OpenRCT2_Level_0"
    if location_number == 3 or location_number == 4 or location_number == 5 or location_number == 6:
        return "OpenRCT2_Level_1"
    divider = location_number - 6
    region = math.ceil(divider / 8) + 1
    return f"OpenRCT2_Level_{region}"

class OpenRCT2World(World):
    """
    OpenRCT2 is a fan-made, open-source reimplementation of the classic simulation game. It faithfully preserves 
    the original game while introducing modern improvements and expanded features. Players can construct intricate 
    roller coasters, manage finances, and build the park of their dreams!
    """

    game = "OpenRCT2"
    web = OpenRCT2WebWorld()

    options_dataclass = openRCT2Options
    options: openRCT2Options
    topology_present = False  # show path to required location checks in spoiler
    item_name_to_id = {name: id for id, name in enumerate(item_info["all_items"], base_id)}
    location_name_to_id = {name: id for id, name in enumerate(location_info["all_locations"], base_id)}
    item_name_groups = {
        "Roller Coasters": item_info["Roller Coasters"],
        "Transport Rides": item_info["Transport Rides"],
        "Gentle Rides": item_info["Gentle Rides"],
        "Thrill Rides": item_info["Thrill Rides"],
        "Water Rides": item_info["Water Rides"],
        "Rides": item_info["Rides"]
    }

    def __init__(self, multiworld, player: int):
        super().__init__(multiworld, player)
        self.starting_ride = None
        self.item_table = []
        self.location_prices = []  # This list is passed to OpenRCT2 to create the unlock shop
        self.rules = []
        self.unique_rides = []
        # print(item_info)

    # Okay future Colby, listen up. Here's the plan. We're going to take the item_table and shuffle it in the next
    # section. We'll generate the unlock shop with the item locations and apply our logic to it. Prereqs can only be
    # items one level lower on the tree. We then will set rules in create_regions that reflect our table.

    def get_filler_item_name(self):
        filler_item = self.random.choice(item_info["filler_items"])
        return filler_item

    def generate_early(self) -> None:
        self.rules = [self.options.difficult_guest_generation.value,
                      self.options.difficult_park_rating.value,
                      self.options.forbid_high_construction.value,
                      self.options.forbid_landscape_changes.value,
                      self.options.forbid_marketing_campaigns.value,
                      self.options.forbid_tree_removal.value]
        # Grabs options for item generation
        scenario = self.options.scenario.value
        eligible_scenarios = []
        # If the scenario is random, pick which random scenario it will be
        if scenario == 143:  # RCT1
            eligible_scenarios = [scenario for scenario in scenario_info["rct1"] if
                                  scenario not in scenario_info["unreasonable_scenarios"]]
        elif scenario == 144:  # Corkscrew Follies
            eligible_scenarios = [scenario for scenario in scenario_info["corkscrew_follies"] if
                                  scenario not in scenario_info["unreasonable_scenarios"]]
        elif scenario == 145:  # Loopy Landscapes
            eligible_scenarios = [scenario for scenario in scenario_info["loopy_landscapes"] if
                                  scenario not in scenario_info["unreasonable_scenarios"]]
        elif scenario == 146:  # RCT2
            eligible_scenarios = [scenario for scenario in scenario_info["rct2"] if
                                  scenario not in scenario_info["unreasonable_scenarios"]]
        elif scenario == 147:  # Wacky Worlds
            eligible_scenarios = [scenario for scenario in scenario_info["wacky_worlds"] if
                                  scenario not in scenario_info["unreasonable_scenarios"]]
        elif scenario == 148:  # Time Twister
            eligible_scenarios = [scenario for scenario in scenario_info["time_twister"] if
                                  scenario not in scenario_info["unreasonable_scenarios"]]
        elif scenario == 149:  # Random RCT1 + Expansions
            eligible_scenarios = [scenario for scenario in scenario_info["rct1_plus_expansions"] if
                                  scenario not in scenario_info["unreasonable_scenarios"]]
        elif scenario == 150:  # Random RCT2 + Expansions
            eligible_scenarios = [scenario for scenario in scenario_info["rct2_plus_expansions"] if
                                  scenario not in scenario_info["unreasonable_scenarios"]]
        # Finish assigning the scenario
        if eligible_scenarios:
            new_scenario = str(self.random.choice(eligible_scenarios))  # Pick the Scenario
            scenario = Scenario[new_scenario].value  # Reassign the scenario option to the randomly selected choice
            self.options.scenario.value = scenario

        self.item_table, self.starting_ride = set_openRCT2_items(self)


    def create_regions(self) -> None:
        logic_length = (len(self.item_table))

        def locations_to_region(location, ending_location, chosen_region):
            locations = []
            while location < ending_location + 1:
                if location < 8:
                    locations.append(OpenRCT2Location(self.player, f"White_{location}",
                        self.location_name_to_id[f"White_{location}"], chosen_region))
                else:
                    color_map = {
                        0: "Black",
                        1: "Green",
                        2: "Blue",
                        3: "Yellow",
                        4: "Gold",
                        5: "Silver",
                        6: "Celadon",
                        7: "Pink",
                    }
                    color = color_map[location % 8]
                    locations.append(OpenRCT2Location(self.player, f"{color}_{math.floor(location/8 - 1)}",
                        self.location_name_to_id[f"{color}_{math.floor(location/8 - 1)}"], chosen_region))
                location += 1
            return locations

        r = Region("Menu", self.player, self.multiworld)
        r.locations = []
        self.multiworld.regions.append(r)

        s = Region("Unlock Shop", self.player, self.multiworld)
        s.locations = []
        self.multiworld.regions.append(s)

        level0 = Region("OpenRCT2_Level_0", self.player, self.multiworld)  # Levels of the unlock tree
        level0.locations = [OpenRCT2Location(self.player, "White_0", self.location_name_to_id["White_0"], level0)]
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
            region = self.multiworld.get_region(f"OpenRCT2_Level_{count}", self.player)
            region_entrance = region.connect(self.multiworld.get_region(f"OpenRCT2_Level_{count + 1}", self.player))
            num_rides = 0
            if count == 0:
                pass
            elif count == 1:  # 3 total items, we want 2 to be rides
                num_rides = 2
            elif count == 2:  # 7 total items, we want 4 rides
                num_rides = 4
            elif count == 3:  # 15 total items, we want 10 rides
                num_rides = 10
            elif count == 4:  # 23 total items, we want 15 rides and now toilets
                num_rides = 15
            elif count == 5:  # 31 total items, we want 18 rides, food, drinks, toilets, and some rules if applicable
                num_rides = 18
                add_rule(region_entrance, lambda state: state.has("Toilets", self.player, 1))
                add_rule(region_entrance, lambda state: state.has("Drink Stall", self.player, 1))
                add_rule(region_entrance, lambda state: state.has("Food Stall", self.player))
                if self.rules[2] == 1:  # If high construction can be disabled
                    add_rule(region_entrance, lambda state: state.has("Allow High Construction", self.player, 1))
                if self.rules[3] == 1:  # landscape
                    add_rule(region_entrance, lambda state: state.has("Allow Landscape Changes", self.player, 1))
                if self.rules[5] == 1:  # tree removal
                    add_rule(region_entrance, lambda state: state.has("Allow Tree Removal", self.player, 1))
                if "Cash Machine" in self.item_table:
                    add_rule(region_entrance, lambda state: state.has("Cash Machine", self.player, 1))
                if "First Aid" in self.item_table:
                    add_rule(region_entrance, lambda state: state.has("First Aid", self.player, 1))
            add_rule(region_entrance, lambda state: state.has_group("Rides", self.player, num_rides))
            count += 1
        final_region = self.multiworld.get_region("OpenRCT2_Level_" + str(current_level), self.player)
        final_region.connect(victory)

    def create_items(self) -> None:
        for item in self.item_table:
            self.multiworld.itempool.append(self.create_item(item))

        # Adds the starting ride to precollected items
        self.multiworld.push_precollected(self.create_item(self.starting_ride))
        # If the user doesn't want to buy speed, give it to em for free
        if not self.options.include_gamespeed_items.value:
            count = 0
            while count < 4:
                self.multiworld.push_precollected(self.create_item("Progressive Speed"))
                count += 1

        # print("Here's the multiworld item pool:")
        # print(len(self.multiworld.itempool))
        # print(self.multiworld.itempool)

    def set_rules(self) -> None:
        # print("Here's the precollected Items")
        # print(self.multiworld.precollected_items[self.player])
        self.random.shuffle(self.item_table)
        # print(self.item_table)

        def set_openRCT2_rule(rule_type, selected_item, location_number):
            if rule_type == "ride":
                add_rule(self.multiworld.get_region(get_previous_region_from_OpenRCT2_location(number),
                                                    self.player).entrances[0],
                         lambda state, selected_prereq=selected_item: state.has(selected_prereq, self.player))
                # Only add rules if there's an item to be unlocked in the first place
                if (selected_item in item_info["requires_height"]) and (
                        self.options.forbid_high_construction.value == "unlockable"):
                    add_rule(self.multiworld.get_region(get_previous_region_from_OpenRCT2_location(number),
                                                        self.player).entrances[0],
                             lambda state, selected_prereq="Allow High Construction": state.has(selected_prereq,
                                                                                                self.player))
                    # print(
                    #     "Added rule: \nHave: Allow High Construction\nLocation: " +
                    #     get_previous_region_from_OpenRCT2_location(location_number))
                if (selected_item in item_info["requires_landscaping"]) and self.options.forbid_landscape_changes.value == "unlockable":
                    add_rule(self.multiworld.get_region(get_previous_region_from_OpenRCT2_location(number),
                                                        self.player).entrances[0],
                             lambda state, selected_prereq="Allow Landscape Changes":
                             state.has(selected_prereq, self.player))
                    # print(
                    #     "Added rule: \nHave: Allow Landscape Changes\nLocation: " +
                    #     get_previous_region_from_OpenRCT2_location(location_number))
                # print(self.multiworld.get_region(get_previous_region_from_OpenRCT2_location(number),
                #                                  self.player).entrances)
                # print("Added rule: \nHave: " + str(
                #     chosen_prereq) + "\nLocation: " + get_previous_region_from_OpenRCT2_location(location_number))

            else: # This is a category
                add_rule(self.multiworld.get_region(get_previous_region_from_OpenRCT2_location(number),
                                                    self.player).entrances[0],
                         lambda state, selected_prereq=selected_item: state.has_group(selected_prereq, self.player))
                # print(self.multiworld.get_region(get_previous_region_from_OpenRCT2_location(number),
                #                                  self.player).entrances)
                # print("Added rule: \nHave: " + str(
                #     category) + "\nLocation: " + get_previous_region_from_OpenRCT2_location(location_number))
            # print("Here's the rule!")
            # print("Rule Type: " + str(rule_type))
            # print("Selected Item: " + str(selected_item))
            # print("Location Number: " + str(location_number))

        length_modifier = 0
        difficulty_modifier = 0
        base_price = 500
        final_price = 500

        if self.options.difficulty == "very_easy":
            difficulty_modifier = 0
        elif self.options.difficulty == "easy":
            difficulty_modifier = .3
        elif self.options.difficulty == "medium":
            difficulty_modifier = .5
        elif self.options.difficulty == "hard":
            difficulty_modifier = .75
        elif self.options.difficulty == "extreme":
            difficulty_modifier = .9

        if self.options.scenario_length == "synchronous_short":
            length_modifier = .2
            final_price = 100000
        elif self.options.scenario_length == "synchronous_long":
            length_modifier = .4
            final_price = 250000
        elif self.options.scenario_length == "lengthy":
            length_modifier = .6
            final_price = 500000
        elif self.options.scenario_length == "marathon": 
            length_modifier = .9
            final_price = 1000000

        # print("This is the final price: " + str(final_price))
        possible_prereqs = [self.starting_ride]
        # Once we're finished with the given region, we'll add the queued prereqs to the possibles list
        queued_prereqs = []
        prereq_counter = 0
        item_table_length = len(self.item_table)
        total_price = base_price * item_table_length
        if final_price < total_price:  # If everything being $500 is too expensive,
            base_price = final_price // item_table_length  # Make everything cheaper
        # print("This is the base price: " + str(base_price))
        total_base = base_price * item_table_length
        remaining_amount = final_price - total_base
        increment = remaining_amount / (item_table_length * (item_table_length + 1) / 2)
        # print("This is the increment: " + str(increment))
        # print("with this many items: " + str(item_table_length))
        for number, item in enumerate(self.item_table):
            unlock = {"LocationID": number, "Price": 0, "Lives": 0, "RidePrereq": []}

            # Handles the price of each location
            if number == 0 or self.random.random() < 0.9:  # 90 percent of locations will have a cash price
                current_price = base_price + increment * number
                unlock["Price"] = int(current_price)
                # print(unlock["Price"])
            else:  # Everything else will cost lives. The Elder Gods will be pleased
                if number < 7:
                    unlock["Lives"] = self.random.randint(2, 150)
                elif number < 32:
                    unlock["Lives"] = self.random.randint(2, 300)
                else:
                    unlock["Lives"] = self.random.randint(2, 1000)

            # Handles the selection of a prerequisite and associated stats

            # We'll never have a prereq on the first 31 items or on blood prices
            if number > 31 and unlock["Lives"] == 0:
                if (self.random.random() < length_modifier) or (# Determines if we have a prereq
                        item_table_length * .85 < number):  # The last 15% will always have a prereq
                    total_customers = 0 # Handle total customers early, since it can apply on any prereq
                    if self.random.random() < .5: # Coin flip to determine if there's a customer requirement
                        total_customers = round(self.random.uniform(self.options.shop_minimum_total_customers.value, 
                        self.options.shop_maximum_total_customers.value))
                    if self.random.random() < difficulty_modifier:  # Determines if the prereq is a specific ride
                        chosen_prereq = self.random.choice(possible_prereqs)
                        set_openRCT2_rule("ride", chosen_prereq, number)
                        if chosen_prereq in item_info["Roller Coasters"] and chosen_prereq not in item_info[
                                "stat_exempt_roller_coasters"]:
                            excitement = 0
                            intensity = 0
                            nausea = 0
                            length = 0
                            # 4 coin flips to determine what, if any, stat prereqs will be used
                            if self.random.random() < .5:
                                excitement = round(self.random.uniform(self.options.shop_minimum_excitement.value, 
                                self.options.shop_maximum_excitement.value))
                            if self.random.random() < .5:
                                intensity = round(self.random.uniform(self.options.shop_minimum_intensity.value, 
                                self.options.shop_maximum_intensity.value))
                            if self.random.random() < .5:
                                nausea = round(self.random.uniform(self.options.shop_minimum_nausea.value, 
                                self.options.shop_maximum_nausea.value))
                            if self.random.random() < .5:
                                length = round(self.random.uniform(self.options.shop_minimum_length.value, 
                                self.options.shop_maximum_length.value))
                            unlock["RidePrereq"] = \
                                [self.random.randint(1, 3), chosen_prereq, excitement, intensity, nausea, length, total_customers]
                        elif (chosen_prereq in item_info["tracked_rides"]
                              and (self.options.scenario_length.value == 0 or #Sync Short
                              self.options.scenario_length.value == 1)):#Sync Long
                            unlock["RidePrereq"] = [self.random.randint(1, 3), chosen_prereq, 0, 0, 0, 0, total_customers]
                        else:
                            if number > 100:
                                unlock["RidePrereq"] = [self.random.randint(1, 7), chosen_prereq, 0, 0, 0, 0, total_customers]
                            else: #Even in async games, don't require too many rides too early
                                unlock["RidePrereq"] = [self.random.randint(1, 3), chosen_prereq, 0, 0, 0, 0, total_customers]
                    else:  # Prereq is not a specific ride
                        category = "ride"
                        category_selected = False
                        while not category_selected:
                            category = self.random.choice(item_info["ride_types"])
                            for ride in possible_prereqs:
                                # Too many parks are unpredictable with water access, especially if landscaping is disabled
                                if ride not in item_info["requires_landscaping"]: 
                                    #Ensures that a category won't be selected if there's no unlocked rides in it
                                    if ride in item_info[category]: 
                                        category_selected = True #e.g. thrill rides won't be required if none can be unlocked at that point
                        set_openRCT2_rule("category", category, number)
                        # print("Added requirement for: " + category)
                        if category == "Roller Coasters" and any(item in possible_prereqs and 
                        item not in item_info["stat_exempt_roller_coasters"] for item in possible_prereqs):
                            excitement = 0
                            intensity = 0
                            nausea = 0
                            length = 0
                            total_customers = 0
                            # 5 coin flips to determine what, if any, stat prereqs will be used
                            if self.random.random() < .5:
                                excitement = round(self.random.uniform(self.options.shop_minimum_excitement.value, 
                                self.options.shop_maximum_excitement.value))
                            if self.random.random() < .5:
                                intensity = round(self.random.uniform(self.options.shop_minimum_intensity.value, 
                                self.options.shop_maximum_intensity.value))
                            if self.random.random() < .5:
                                nausea = round(self.random.uniform(self.options.shop_minimum_nausea.value, 
                                self.options.shop_maximum_nausea.value))
                            if self.random.random() < .5:
                                length = round(self.random.uniform(self.options.shop_minimum_length.value, 
                                self.options.shop_maximum_length.value))
                            unlock["RidePrereq"] = \
                                [self.random.randint(1, 4), 
                                category, excitement, intensity, nausea, length, total_customers]
                        elif category == "Transport Rides" or category == "Water Rides" or category == "Roller Coasters":
                            unlock["RidePrereq"] = [self.random.randint(1, 3), category, 0, 0, 0, 0, total_customers]
                        else:
                            unlock["RidePrereq"] = [self.random.randint(1, 10), category, 0, 0, 0, 0, total_customers]
                    if self.options.balance_guest_counts.value & total_customers > 0: # Balances rides for throughput
                        min_customers = self.options.shop_minimum_total_customers.value
                        max_customers = self.options.shop_maximum_total_customers.value
                        scale = max_customers - min_customers
                        if unlock["RidePrereq"][1] in item_info["low_throughput"]:
                            bias_factor = 3 # The higher the factor, the stronger the bais towards small numbers
                            total_customers = round(min_customers + (scale * (self.random.random() ** bias_factor)))
                            # print("Customer Requirements for " + unlock["RidePrereq"][1] + ": " + str(total_customers))
                        elif unlock["RidePrereq"][1] in item_info["high_throughput"]:
                            bias_factor = .4 # The lower the factor, the stronger the bais towards large numbers
                            total_customers = round(min_customers + (scale * (self.random.random() ** bias_factor)))
                            # print("Customer Requirements for " + unlock["RidePrereq"][1] + ": " + str(total_customers))
                            #No need to check outside low or high, since we made a random selection at the top
                        unlock["RidePrereq"][6] = total_customers
                            
            # Add the shop item to the shop prices
            self.location_prices.append(unlock)
            # Handle unlocked rides
            if item in item_info["Rides"]:  # Don't put items in that require an impossible rule
                if not (self.options.forbid_high_construction.value == "on" and item in item_info[
                        "requires_height"]):
                    if not (self.options.forbid_landscape_changes.value == "on" and item in item_info[
                            "requires_landscaping"]):
                        queued_prereqs.append(item)
            if prereq_counter == 0 or prereq_counter == 2 or prereq_counter % 8 == 6:
                for prereq in queued_prereqs:
                    possible_prereqs.append(prereq)
                queued_prereqs.clear()
            prereq_counter += 1
        # print("OpenRCT2 will make the shop will the following:")
        # print(self.location_prices)

        # Okay, here's where we're going to take the last eligible rides in the logic table
        # and make them required for completion, if that's required.
        eligible_rides = [item for index, item in enumerate(self.item_table) if
                          item in item_info["Rides"] and item not in item_info["non_starters"]]
        eligible_rides = list(dict.fromkeys(eligible_rides))
        self.random.shuffle(eligible_rides)
        if self.options.required_unique_rides.value:
            count = 0
            while count < self.options.required_unique_rides.value:
                self.unique_rides.append(eligible_rides[count])
                count += 1
        # print("Here's the eligible rides:")
        # print(eligible_rides)
        # print("Here's what was chosen:")
        # print(self.unique_rides)
        for ride in self.unique_rides:
            add_rule(self.multiworld.get_region("Victory", self.player).entrances[0],
                     lambda state, selected_prereq=ride: state.has(selected_prereq, self.player))

    def generate_basic(self) -> None:
        # place "Victory" at the end of the unlock tree and set collection as win condition
        self.multiworld.get_location("Victory", self.player).place_locked_item(
            OpenRCT2Item("Victory", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(f'Starting Ride:       {self.starting_ride}\n')

    def fill_slot_data(self):
        guests = self.options.guest_objective.value
        park_value = self.options.park_value_objective.value
        roller_coasters = self.options.roller_coaster_objective.value
        excitement = self.options.roller_coaster_excitement.value
        intensity = self.options.roller_coaster_intensity.value
        nausea = self.options.roller_coaster_nausea.value
        park_rating = self.options.park_rating_objective.value
        pay_off_loan = self.options.pay_off_loan.value
        monopoly = self.options.monopoly_mode.value
        unique_rides = self.unique_rides
        objectives = {"Guests": [guests, False], "ParkValue": [park_value, False],
                      "RollerCoasters": [roller_coasters, excitement, intensity, nausea, 0, False],
                      "RideIncome": [0, False], "ShopIncome": [0, False], "ParkRating": [park_rating, False],
                      "LoanPaidOff": [pay_off_loan, False], "Monopoly": [monopoly, False],
                      "UniqueRides": [unique_rides, False]}
        seed = self.multiworld.player_name[self.player] + str(self.options.scenario) + str(self.multiworld.seed_name)
        # print("SEEED!")
        # print(seed)
        # print(objectives)
        # print(self.item_id_to_name)

        # Fixes Location Prices for OpenRCT2
        for index, location in enumerate(self.location_prices):
            # print("Here's the category! Maybe.")
            if self.location_prices[index]["RidePrereq"]:
                category = self.location_prices[index]["RidePrereq"][1]
                # print(self.location_prices[index]["RidePrereq"][1])
            else:
                category = None
            # If the item has a prereq that's a category instead of a specific ride, convert that to what
            # the in-game plugin will read
            if category in item_info["ride_types"]:
                if category == "Roller Coasters":
                    self.location_prices[index]["RidePrereq"][1] = "rollercoaster"
                elif category == "Transport Rides":
                    self.location_prices[index]["RidePrereq"][1] = "transport"
                elif category == "Gentle Rides":
                    self.location_prices[index]["RidePrereq"][1] = "gentle"
                elif category == "Thrill Rides":
                    self.location_prices[index]["RidePrereq"][1] = "thrill"
                else:
                    self.location_prices[index]["RidePrereq"][1] = "water"
        # from Utils import visualize_regions
        # visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")
        # print("Here's the final unlock shop:")
        # print(self.location_prices)
        slot_data = self.options.as_dict("difficulty", "scenario_length", "scenario", "death_link", "randomization_range",
        "stat_rerolls", "randomize_park_values", "ignore_ride_stat_changes", "visibility", "preferred_intensity", 
        "all_rides_and_scenery_base", "all_rides_and_scenery_expansion")
        slot_data["objectives"] = objectives
        slot_data["rules"] = self.rules
        slot_data["seed"] = seed
        slot_data["version"] = apworld_version
        # print("Here's the seed!" + str(seed))
        slot_data["location_prices"] = self.location_prices
        # print("Here's all the rules!")
        # print(self.multiworld.rules)
        return slot_data

    def create_item(self, item: str) -> OpenRCT2Item:
        classification = ItemClassification.useful
        if item in item_info["Rides"] or item in item_info["progression_rules"] or item in item_info["stalls"]:
            classification = ItemClassification.progression
        if item in item_info["filler_items"]:
            classification = ItemClassification.filler
        if item in item_info["trap_items"]:
            classification = ItemClassification.trap
        return OpenRCT2Item(item, classification, self.item_name_to_id[item], self.player)