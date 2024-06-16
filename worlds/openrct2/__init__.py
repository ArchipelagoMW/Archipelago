import math
from typing import TextIO
from Utils import local_path

import worlds.LauncherComponents as LauncherComponents
from BaseClasses import ItemClassification, Region, Item, Location, Tutorial
from worlds.generic.Rules import add_rule

from .Constants import base_id, item_info, location_info, scenario_info
from .Items import OpenRCT2Item, set_openRCT2_items
from .Options import openRCT2Options, Scenario, openrct2_option_groups
from worlds.AutoWorld import World, WebWorld

import requests
import pathlib
from PIL import Image
from io import BytesIO

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

# URL of the PNG image
url = 'https://github.com/OpenRCT2/OpenRCT2/blob/7ba17812d84d036164bc0657ba720346ff20859b/resources/logo/icon_x96.png?raw=true'

# Fetch the image
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Open the image using Pillow
    openrct2icon = Image.open(BytesIO(response.content))

    # Save the image locally
    openrct2icon.save(pathlib.Path('data/openrct2icon.png'))
    print("Image successfully downloaded and saved as 'openrct2icon.png'")
else:
    print(f"Failed to retrieve OpenRCT2 Icon. HTTP Status code: {response.status_code}")

LauncherComponents.icon_paths['openrct2icon'] = local_path('data', 'openrct2icon.png')

def get_previous_region_from_OpenRCT2_location(location_number: int):
    if location_number <= 2:
        return "OpenRCT2_Level_0"
    elif location_number == 3 or location_number == 4 or location_number == 5 or location_number == 6:
        return "OpenRCT2_Level_1"
    else:
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
        "roller_coasters": item_info["roller_coasters"],
        "transport_rides": item_info["transport_rides"],
        "gentle_rides": item_info["gentle_rides"],
        "thrill_rides": item_info["thrill_rides"],
        "water_rides": item_info["water_rides"],
        "rides": item_info["rides"]
    }

    def __init__(self, multiworld, player: int):
        super().__init__(multiworld, player)
        self.starting_ride = None
        self.item_table = {}
        self.location_prices = []  # This list is passed to OpenRCT2 to create the unlock shop
        self.rules = []
        self.unique_rides = []

    # Okay future Colby, listen up. Here's the plan. We're going to take the item_table and shuffle it in the next
    # section. We'll generate the unlock shop with the item locations and apply our logic to it. Prereqs can only be
    # items one level lower on the tree. We then will set rules in create_regions that reflect our table.

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
                locations.append(OpenRCT2Location(self.player, f"OpenRCT2_{location}",
                                                  self.location_name_to_id[f"OpenRCT2_{location}"], chosen_region))
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
            region = self.multiworld.get_region(f"OpenRCT2_Level_{count}", self.player)
            region_entrance = region.connect(self.multiworld.get_region(f"OpenRCT2_Level_{count + 1}", self.player))
            num_rides = 0
            if count == 0:
                pass
            elif count == 1:  # 3 total items, we want 2 to be rides
                num_rides = 2
            elif count == 2:  # 7 total items, we want 4 rides and a food stall
                num_rides = 4
                add_rule(region_entrance, lambda state: state.has("Food Stall", self.player))
            elif count == 3:  # 15 total items, we want 10 rides and now a drink stall
                num_rides = 10
                add_rule(region_entrance, lambda state: state.has("Drink Stall", self.player, 1))
            elif count == 4:  # 23 total items, we want 15 rides and now toilets
                num_rides = 15
                add_rule(region_entrance, lambda state: state.has("Toilets", self.player, 1))
            elif count == 5:  # 31 total items, we want 18 rides and some rules if applicable
                num_rides = 18
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
            add_rule(region_entrance, lambda state: state.has_group("rides", self.player, num_rides))
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
                        self.options.forbid_high_construction.value == 1):
                    add_rule(self.multiworld.get_region(get_previous_region_from_OpenRCT2_location(number),
                                                        self.player).entrances[0],
                             lambda state, selected_prereq="Allow High Construction": state.has(selected_prereq,
                                                                                                self.player))
                    # print(
                    #     "Added rule: \nHave: Allow High Construction\nLocation: " +
                    #     get_previous_region_from_OpenRCT2_location(location_number))
                if (selected_item in item_info["requires_landscaping"]) and self.options.forbid_landscape_changes.value == 1:
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
            else:
                add_rule(self.multiworld.get_region(get_previous_region_from_OpenRCT2_location(number),
                                                    self.player).entrances[0],
                         # self.multiworld.get_location("OpenRCT2_" +
                         # str(number), self.player).parent_region.entrances[0],
                         lambda state, selected_prereq=selected_item: state.has_group(selected_prereq, self.player))
                # TODO: Check if every item in the category has a rule requirement,
                #  and if so, force the rule to appear before the location
                # if item_info[item].issubset(item_info["requires_height"]):
                #     add_rule(self.multiworld.get_region(self.get_previous_region_from_OpenRCT2_location(number),
                #     self.player).entrances[0],
                #      lambda state, prereq="Allow High Construction": state.has(prereq, self.player))
                #     print("Added rule: \nHave: Allow High Construction\nLocation: " +
                #     self.get_previous_region_from_OpenRCT2_location(location_number))
                # print(self.multiworld.get_region(get_previous_region_from_OpenRCT2_location(number),
                #                                  self.player).entrances)
                # print("Added rule: \nHave: " + str(
                #     category) + "\nLocation: " + get_previous_region_from_OpenRCT2_location(location_number))

        length_modifier = 0
        difficulty_modifier = 0
        base_price = 500
        final_price = 500

        if self.options.difficulty == "very_easy":
            difficulty_modifier = 0
        if self.options.difficulty == "easy":
            difficulty_modifier = .3
        if self.options.difficulty == "medium":
            difficulty_modifier = .5
        if self.options.difficulty == "hard":
            difficulty_modifier = .75
        if self.options.difficulty == "extreme":
            difficulty_modifier = .9

        if self.options.scenario_length == "synchronous_short":
            length_modifier = .2
            final_price = 100000
        if self.options.scenario_length == "synchronous_long":
            length_modifier = .4
            final_price = 250000
        if self.options.scenario_length == "lengthy":
            length_modifier = .6
            final_price = 500000
        if self.options.scenario_length == "marathon": 
            length_modifier = .9
            final_price = 1000000

        # print("This is the final price: " + str(final_price))
        possible_prereqs = [self.starting_ride]
        # Once we're finished with the given region, we'll add the queued prereqs to the possibles list
        queued_prereqs = []
        prereq_counter = 0
        total_price = base_price * len(self.item_table)
        if final_price < total_price:  # If everything being $500 is too expensive,
            base_price = final_price / len(self.item_table)  # Make everything cheaper
        # print("This is the base price: " + str(base_price))
        total_base = base_price * len(self.item_table)
        remaining_amount = final_price - total_base
        increment = remaining_amount / (len(self.item_table) * (len(self.item_table) + 1) / 2)
        # print("This is the increment: " + str(increment))
        # print("with this many items: " + str(len(self.item_table)))
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
                if (self.random.random() < length_modifier) or (
                        len(self.item_table) * .85 < number):  # Determines if we have a prereq
                    if self.random.random() < difficulty_modifier:  # Determines if the prereq is a specific ride
                        chosen_prereq = self.random.choice(possible_prereqs)
                        set_openRCT2_rule("ride", chosen_prereq, number)
                        if chosen_prereq in item_info["roller_coasters"] and chosen_prereq not in item_info[
                                "stat_exempt_roller_coasters"]:
                            excitement = 0
                            intensity = 0
                            nausea = 0
                            # 3 coin flips to determine what, if any, stat prereqs will be used
                            if self.random.random() < .5:
                                excitement = round(self.random.uniform(self.options.shop_minimum_excitement, self.options.shop_maximum_excitement), 1)
                            if self.random.random() < .5:
                                intensity = round(self.random.uniform(self.options.shop_minimum_intensity, self.options.shop_maximum_intensity), 1)
                            if self.random.random() < .5:
                                nausea = round(self.random.uniform(self.options.shop_minimum_nausea, self.options.shop_maximum_nausea), 1)
                            unlock["RidePrereq"] = \
                                [self.random.randint(1, 3), chosen_prereq, excitement, intensity, nausea, 0]
                        elif (chosen_prereq in item_info["tracked_rides"]
                              and (self.options.scenario_length.value == 0 or self.options.scenario_length.value == 1)):
                            unlock["RidePrereq"] = [self.random.randint(1, 3), chosen_prereq, 0, 0, 0, 0]
                        else:
                            if number > 100:
                                unlock["RidePrereq"] = [self.random.randint(1, 7), chosen_prereq, 0, 0, 0, 0]
                            else: #Even in async games, don't require too many rides too early
                                unlock["RidePrereq"] = [self.random.randint(1, 3), chosen_prereq, 0, 0, 0, 0]
                    else:  # Prereq is not a specific ride
                        category = "ride"
                        category_selected = False
                        while not category_selected:
                            category = self.random.choice(item_info["ride_types"])
                            for ride in possible_prereqs:
                                if ride in item_info[category]:
                                    category_selected = True
                        set_openRCT2_rule("category", category, number)
                        if category == "roller_coasters" and any(item in possible_prereqs and item not in item_info["stat_exempt_roller_coasters"] for item in possible_prereqs):
                            excitement = 0
                            intensity = 0
                            nausea = 0
                            # 3 coin flips to determine what, if any, stat prereqs will be used
                            if self.random.random() < .5:
                                excitement = round(self.random.uniform(self.options.shop_minimum_excitement, self.options.shop_maximum_excitement), 1)
                            if self.random.random() < .5:
                                intensity = round(self.random.uniform(self.options.shop_minimum_intensity, self.options.shop_maximum_intensity), 1)
                            if self.random.random() < .5:
                                nausea = round(self.random.uniform(self.options.shop_minimum_nausea, self.options.shop_maximum_nausea), 1)
                            unlock["RidePrereq"] = \
                                [self.random.randint(1, 4), category, excitement, intensity, nausea, 0]
                        elif category == "transport_rides" or category == "water_rides" or category == "roller_coasters":
                            unlock["RidePrereq"] = [self.random.randint(1, 3), category, 0, 0, 0, 0]
                        else:
                            unlock["RidePrereq"] = [self.random.randint(1, 10), category, 0, 0, 0, 0]
            # Add the shop item to the shop prices
            self.location_prices.append(unlock)
            # Handle unlocked rides
            if item in item_info["rides"]:  # Don't put items in that require an impossible rule
                if not (self.options.forbid_high_construction.value == 2 and item in item_info[
                        "requires_height"]):
                    if not (self.options.forbid_landscape_changes.value == 2 and item in item_info[
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
                          item in item_info["rides"] and item not in item_info["non_starters"]]
        eligible_rides = list(dict.fromkeys(eligible_rides))
        self.random.shuffle(eligible_rides)
        if self.options.required_unique_rides.value:
            count = 0
            while count < self.options.required_unique_rides.value:
                self.unique_rides.append(eligible_rides[count])
                count += 1
            # self.unique_rides = [eligible_rides[i] for i in
            #                     eligible_rides[-self.multiworld.required_unique_rides[self.player].value:]]
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
        # print("Here's the final unlock shop:")
        slot_data = self.options.as_dict("difficulty", "scenario_length", "scenario", "death_link", "randomization_range",
        "stat_rerolls", "randomize_park_values", "ignore_ride_stat_changes", "visibility", "preferred_intensity")
        slot_data["objectives"] = objectives
        slot_data["rules"] = self.rules
        slot_data["location_prices"] = self.location_prices
        return slot_data

    def create_item(self, item: str) -> OpenRCT2Item:
        classification = ItemClassification.useful
        if item in item_info["rides"] or item in item_info["progression_rules"] or item in item_info["stalls"]:
            classification = ItemClassification.progression
        if item in item_info["filler_items"]:
            classification = ItemClassification.filler
        if item in item_info["trap_items"]:
            classification = ItemClassification.trap
        return OpenRCT2Item(item, classification, self.item_name_to_id[item], self.player)
