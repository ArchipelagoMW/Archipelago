import math
from typing import TextIO

from BaseClasses import ItemClassification, Region, Location, Tutorial
from worlds.generic.Rules import add_rule

from .helpers.Statistics import Statistics
from .Constants import base_id, apworld_version
from .data.item_info import item_info
from .data.location_info import location_info

from .Items import ParkitectItem, set_parkitect_items
from .Options import ParkitectOptions, parkitect_option_groups
from worlds.AutoWorld import World, WebWorld

class ParkitectLocation(Location):
    game = "Parkitect"

class ParkitectWebWorld(WebWorld):
    theme = "partyTime"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Parkitect randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Crusher"]
    )

    tutorials = [setup_en]
    option_groups = parkitect_option_groups

def get_previous_region_from_parkitect_location(location_number: int):
    if location_number <= 2:
        return "Parkitect_Challenge_Level_0"

    if location_number <= 5:
        return "Parkitect_Challenge_Level_1"

    # level 3 -> 5 items / 3 rows
    id = math.ceil((location_number - 5) / 3) + 1
    return f"Parkitect_Challenge_Level_{id}"

class ParkitectWorld(World):
    """
    Parkitect is a modern take on classic theme park tycoon games where you build and manage the theme parks of your dreams!
    Construct your own coasters, design efficiently operating parks that fully immerse your guests in their theming and play through the campaign.
    """

    game = "Parkitect"
    web = ParkitectWebWorld()
    options_dataclass = ParkitectOptions
    options = ParkitectOptions
    item_name_to_id = {name: id for id, name in enumerate(item_info["all_items"], base_id)}
    item_name_groups = {
        "Calm Rides": item_info["Calm Rides"],
        "Thrill Rides": item_info["Thrill Rides"],
        "Coaster Rides": item_info["Coaster Rides"],
        "Water Rides": item_info["Water Rides"],
        "Transport Rides": item_info["Transport Rides"],
        "Rides": item_info["Rides"],
        "Shops": item_info["Shops"]
    }
    location_name_to_id = {name: id for id, name in enumerate(location_info["all_locations"], base_id)}

    def __init__(self, multiworld, player: int):
        super().__init__(multiworld, player)
        self.starter = None
        self.item_table = []
        self.challenges = [] # Parkitect Challenge Window

    def get_trap_item_name(self):
        trap_item = self.random.choice(item_info["trap_items"])
        return trap_item

    def generate_early(self) -> None:
        self.item_table, self.starter = set_parkitect_items(self)

    def create_regions(self) -> None:
        logic_length = (len(self.item_table))

        def locations_to_region(location, ending_location, chosen_region):
            locations = []

            while location <= ending_location:
                if location < 3:
                    locationName = f"Challenge_{location}_0"
                    locations.append(ParkitectLocation(
                        self.player,
                        locationName,
                        self.location_name_to_id[locationName], chosen_region
                    ))

                else:
                    challenge_map = {
                        0: "Challenge_1",
                        1: "Challenge_2",
                        2: "Challenge_3",
                    }
                    challenge = challenge_map[location % 3]
                    id = math.floor(location / 3)
                    locationName = f"{challenge}_{id}"

                    locations.append(ParkitectLocation(
                        self.player,
                        locationName,
                        self.location_name_to_id[locationName],
                        chosen_region
                    ))

                location += 1
            return locations
            
        m = Region("Menu", self.player, self.multiworld)
        m.locations= []
        self.multiworld.regions.append(m)

        c = Region("Challenges", self.player, self.multiworld)
        c.locations = []
        self.multiworld.regions.append(c)

        # first Challenges we can submit easily
        # Also just a show how the flow should look alike
        level_0 = Region("Parkitect_Challenge_Level_0", self.player, self.multiworld)  # Levels of the unlock tree
        level_0.locations = [
            ParkitectLocation(self.player, "Challenge_1_0", self.location_name_to_id["Challenge_1_0"], level_0),
            ParkitectLocation(self.player, "Challenge_2_0", self.location_name_to_id["Challenge_2_0"], level_0),
            ParkitectLocation(self.player, "Challenge_3_0", self.location_name_to_id["Challenge_3_0"], level_0),
        ]
        self.multiworld.regions.append(level_0)

        current_level = 1
        item = 3

        while (item + 2) < logic_length:
            level = Region("Parkitect_Challenge_Level_" + str(current_level), self.player, self.multiworld)
            level.locations = locations_to_region(item, item + 2, level)
            self.multiworld.regions.append(level)
            item += 3
            current_level += 1

        # fill rest of items, if there are any
        end_level = Region("Parkitect_Challenge_Level_" + str(current_level), self.player, self.multiworld)
        end_level.locations = locations_to_region(item, (logic_length - 1), end_level)
        self.multiworld.regions.append(end_level)

        victory = Region("Victory", self.player, self.multiworld)
        victory.locations = [ParkitectLocation(self.player, "Victory", None, victory)]
        self.multiworld.regions.append(victory)

        m.connect(c)
        c.connect(self.multiworld.get_region("Parkitect_Challenge_Level_0", self.player))
        count = 0

        while count < current_level:
            region = self.multiworld.get_region(f"Parkitect_Challenge_Level_{count}", self.player)
            region_entrance = region.connect(self.multiworld.get_region(f"Parkitect_Challenge_Level_{count + 1}", self.player))
            num_rides = 0
            num_shops = 0

            if count == 0:
                pass

            elif count == 1:  # 5 total items, we want 1 ride and 1 shop
                num_rides = 1
                num_shops = 1

            elif count == 2:  # 8 total items, we want 3 rides and 2 shops
                num_rides = 3
                num_shops = 2

            elif count == 4:  # 14 total items, we want 3 rides and 3 shops
                num_shops = 3

            elif count == 6:  # 20 total items, we want 5 rides and 4 shops
                num_rides = 5
                num_shops = 4

            elif count == 7:  # 23 total items, we want 6 rides and 5 shops
                num_rides = 6
                num_shops = 5

            add_rule(region_entrance, lambda state, num=num_rides: state.has_group("Rides", self.player, num))
            add_rule(region_entrance, lambda state, num=num_shops: state.has_group("Shops", self.player, num))
            count += 1

        final_region = self.multiworld.get_region("Parkitect_Challenge_Level_" + str(current_level), self.player)
        final_region.connect(victory)
    
    def create_items(self) -> None:
        for item in self.item_table:
            self.multiworld.itempool.append(self.create_item(item))

        # Adds the starting ride to precollected items
        self.multiworld.push_precollected(self.create_item(self.starter))

    def set_rules(self) -> None:
        self.random.shuffle(self.item_table)

        def set_parkitect_rule(rule_type, selected_item, number):
            entrance = self.multiworld.get_region(get_previous_region_from_parkitect_location(number), self.player).entrances[0]

            if rule_type == "ride" or rule_type == "shop":
                add_rule(entrance, lambda state, selected_prereq=selected_item: state.has(selected_prereq, self.player))
            else:
                add_rule(entrance, lambda state, selected_prereq=selected_item: state.has_group(selected_prereq, self.player))

        difficulty_modifier = 0

        if self.options.difficulty == "easy":
            difficulty_modifier = .25

        elif self.options.difficulty == "medium":
            difficulty_modifier = .45

        elif self.options.difficulty == "hard":
            difficulty_modifier = .65

        elif self.options.difficulty == "extreme":
            difficulty_modifier = .85

        possible_prereqs = [self.starter]
        prereq_counter = 0
        queued_prereqs = []
        item_table_length = len(self.item_table)

        #print(self.starter)
        #print("--------------------------------")
        #print("--------------------------------")
        #print("--------------------------------")
        for number, item in enumerate(self.item_table):
            thing = ""
            unlock = {"location_id": number, "item": []}

            progress = number / item_table_length

            # Chosen prerequisite
            if self.random.random() < difficulty_modifier:
                chosen_prereq = self.random.choice(possible_prereqs)
                thing = chosen_prereq
                #print("Prereq:")

                if chosen_prereq in item_info["Rides"]:
                    set_parkitect_rule("ride", chosen_prereq, number)

                elif chosen_prereq in item_info["Shops"]:
                    set_parkitect_rule("shop", chosen_prereq, number)

            # Is category
            else:
                #print("Category:")
                all_categories = item_info["ride_types"] + item_info["shop_types"]  
                category = "ride"
                category_selected = False

                while not category_selected:
                    category = self.random.choice(all_categories)

                    for ride in possible_prereqs:
                        if ride in item_info[category]: 
                            category_selected = True
                            set_parkitect_rule("category", category, number)
                            thing = category

            # Trap -> 1
            if item in item_info["trap_items"]:
                unlock["item"] = Statistics(thing, 1).to_dict()

            # --- Tier 1: -> first 6 items ---
            elif number <= 6:
                # max: 2
                max = 2

                unlock["item"] = Statistics(
                    thing,
                   self.random.randint(1, max),
                ).to_dict()

            # --- Tier 2: -> 10% ---
            elif progress <= 0.10: 
                customers = 0
                
                # Shop -> max: 3
                # Shop Typers -> max: 6
                if thing in item_info["Shops"] or thing in item_info["shop_types"]:
                    max = 3
                    shop_revenue = 0

                    if thing in item_info["shop_types"]:
                        max = 6

                    if thing not in item_info['non_profitables'] and self.random.random() < .5:
                        shop_revenue = round(self.random.uniform(
                            0, 
                            self.options.challenge_maximum_shop_revenue.value
                        ))

                    if self.random.random() < .5:
                        customers = round(self.random.uniform(
                            0, 
                            self.options.challenge_customers.value
                        ))

                    # Both given? i only want 1
                    if shop_revenue > 0 and customers > 0:
                        # Coin flip to decide which one to keep
                        if self.random.random() < 0.5:
                            customers = 0

                        else:
                            shop_revenue = 0

                    if thing in item_info['stat_exempt_shops'] and shop_revenue > 500:
                        shop_revenue = round(self.random.uniform(200, 500))

                    unlock["item"] = Statistics(
                        thing,
                        self.random.randint(1, 3),
                        revenue=shop_revenue,
                        customers=customers
                    ).to_dict()

                # Ride -> max: 3
                elif thing in item_info["Rides"] or thing in item_info["ride_types"]:
                    ride_revenue = 0

                    if self.random.random() < .5:
                        ride_revenue = round(self.random.uniform(
                            0, 
                            self.options.challenge_maximum_shop_revenue.value
                        ))

                    if self.random.random() < .5:
                        customers = round(self.random.uniform(
                            0, 
                            self.options.challenge_customers.value
                        ))

                    # Both given? i only want 1
                    if ride_revenue > 0 and customers > 0:
                        # Coin flip to decide which one to keep
                        if self.random.random() < 0.5:
                            customers = 0

                        else:
                            ride_revenue = 0

                    unlock["item"] = Statistics(
                        thing,
                        self.random.randint(1, 3),
                        revenue=ride_revenue,
                        customers=customers
                    ).to_dict()

            # --- Tier 3: -> 35% ---
            elif progress <= 0.35:
                # Shop -> max: 4
                # Shop Typers -> max: 8
                if thing in item_info["Shops"] or thing in item_info["shop_types"]:
                    max = 4

                    if thing in item_info["shop_types"]:
                        max = 8

                    unlock["item"] = Statistics.random_roll(
                        thing,
                        self.random.randint(1, max),
                        self,
                        possible_prereqs
                    ).to_dict()

                # Ride -> max: 4
                elif thing in item_info["Rides"] or thing in item_info["ride_types"]:
                    max = 4

                    unlock["item"] = Statistics.random_roll(
                        thing,
                        self.random.randint(1, max),
                        self,
                        possible_prereqs
                    ).to_dict()

            # --- Tier 4: -> 60% ---
            elif progress <= 0.60:
                # Shop -> max: 6
                # Shop Typers -> max: 18
                if thing in item_info["Shops"] or thing in item_info["shop_types"]:
                    max = 6
                
                    if thing in item_info["shop_types"]:
                        max = 18

                    unlock["item"] = Statistics.random_roll(
                        thing,
                        self.random.randint(1, max),
                        self,
                        possible_prereqs
                    ).to_dict()

                # Ride -> max: 5
                # Coaster -> max: 3
                elif thing in item_info["Rides"] or thing in item_info["ride_types"]:
                    max = 3 if thing in item_info["Coaster Rides"] else 5

                    unlock["item"] = Statistics.random_roll(
                        thing,
                        self.random.randint(1, max),
                        self,
                        possible_prereqs
                    ).to_dict()

            # --- Tier 5: +60% ---
            else:
                # Shops -> max: 6
                # Shop Types -> max: 24
                if thing in item_info["Shops"] or thing in item_info["shop_types"]:
                    max = 6

                    if thing in item_info["shop_types"]:
                        max = 24

                    unlock["item"] = Statistics.random_roll(
                        thing,
                        self.random.randint(1, max),
                        self,
                        possible_prereqs
                    ).to_dict()

                # Coaster Ride -> max: 4
                elif thing in item_info["Coaster Rides"]:
                    max = 4

                    unlock["item"] = Statistics.random_roll(
                        thing,
                        self.random.randint(1, max),
                        self,
                        possible_prereqs
                    ).to_dict()
            
                # Ride -> max: 5
                elif thing in item_info["Rides"] or thing in item_info["ride_types"]:
                    max = 5

                    unlock["item"] = Statistics.random_roll(
                        thing,
                        self.random.randint(1, 7),
                        self,
                        possible_prereqs
                    ).to_dict()

            #print("_______________________________")
            #print(item)
            #print(thing)
            #print(unlock)
            #print("_______________________________")
            if not unlock["item"]:
                print(f"[WARN] Skipping challenge at index {number} — no valid item generated.")
                continue
            self.challenges.append(unlock)

            # Handle unlocked rides
            if item in item_info["Rides"] or item in item_info["Shops"]:
                queued_prereqs.append(item)

            # Every fourth
            if prereq_counter == 0 or prereq_counter == 2 or prereq_counter % 4 == 0:
                for prereq in queued_prereqs:
                    possible_prereqs.append(prereq)
                queued_prereqs.clear()

            prereq_counter += 1

    def generate_basic(self) -> None:
        # place "Victory" at the end of the unlock tree and set collection as win condition
        self.multiworld.get_location("Victory", self.player).place_locked_item(
            ParkitectItem("Victory", ItemClassification.progression, None, self.player)
        )
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def fill_slot_data(self):
        goal_guests = self.options.goal_guests.value
        goal_money = self.options.goal_money.value
        goal_coasters = self.options.goal_coasters.value
        goal_coaster_excitement = self.options.goal_coaster_excitement.value
        goal_coaster_intensity = self.options.goal_coaster_intensity.value
        goal_ride_profit = self.options.goal_ride_profit.value
        goal_park_tickets = self.options.goal_park_tickets.value
        goal_shops = self.options.goal_shops.value
        goal_shop_profit = self.options.goal_shop_profit.value

        goals = {
            "park_tickets": {
                "enabled": goal_park_tickets > 0,
                "value": goal_park_tickets,
            },
            "guests": {
                "enabled": goal_guests > 0,
                "value": goal_guests,
            },
            "money": {
                "enabled": goal_money > 0,
                "value": goal_money,
            },
            "coaster_rides": {
                "enabled": goal_coasters > 0,
                "value": goal_coasters,
                "values": {
                    "excitement": goal_coaster_excitement,
                    "intensity": goal_coaster_intensity,
                },
            },
            "ride_profit": {
                "enabled": goal_ride_profit > 0,
                "value": goal_ride_profit,
            },
            "shop_profit": {
                "enabled": goal_shop_profit > 0,
                "value": goal_shop_profit,
            },
            "shops": {
                "enabled": goal_shops > 0,
                "value": goal_shops,
            },
            #"shops2": {
            #    "enabled": len(goal_shops) > 0,
            #    "value": goal_shops,
            #},
        }

        seed = self.multiworld.player_name[self.player] + str(self.options.scenario) + str(self.multiworld.seed_name)
        slot_data = self.options.as_dict(
            "scenario",
        )
        slot_data["goals"] = goals
        slot_data["rules"] = self.options.as_dict(
            "difficulty",
            "guests_money_flux",
        )
        
        slot_data["seed"] = seed
        slot_data["version"] = apworld_version
        slot_data["challenges"] = self.challenges

        return slot_data

    def create_item(self, item: str) -> ParkitectItem:
        classification = ItemClassification.useful

        if item in item_info["Rides"] or item in item_info["Shops"]:
            classification = ItemClassification.progression

        if item in item_info["trap_items"]:
            classification = ItemClassification.trap

        return ParkitectItem(item, classification, self.item_name_to_id[item], self.player)
