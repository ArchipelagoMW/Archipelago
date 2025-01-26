import logging
from typing import List

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import KH1Item, KH1ItemData, event_item_table, get_items_by_category, item_table, item_name_groups
from .Locations import KH1Location, location_table, get_locations_by_category, location_name_groups
from .Options import KH1Options, kh1_option_groups
from .Regions import create_regions
from .Rules import set_rules
from .Presets import kh1_option_presets
from .GenerateJSON import generate_json
from worlds.LauncherComponents import Component, components, Type, launch_subprocess

VANILLA_KEYBLADE_STATS = [
    {"STR":  3, "CRR":  20, "CRB":  0, "REC": 30, "MP":  0}, # Kingdom Key
    {"STR":  1, "CRR":  20, "CRB":  0, "REC": 30, "MP":  0}, # Dream Sword
    {"STR":  1, "CRR":   0, "CRB":  0, "REC": 60, "MP":  0}, # Dream Shield
    {"STR":  1, "CRR":  10, "CRB":  0, "REC": 30, "MP":  0}, # Dream Rod
    {"STR":  0, "CRR":  20, "CRB":  0, "REC": 30, "MP":  0}, # Wooden Sword
    {"STR":  5, "CRR":  10, "CRB":  0, "REC":  1, "MP":  0}, # Jungle King
    {"STR":  6, "CRR":  20, "CRB":  0, "REC": 60, "MP":  0}, # Three Wishes
    {"STR":  8, "CRR":  10, "CRB":  2, "REC": 30, "MP":  1}, # Fairy Harp
    {"STR":  7, "CRR":  40, "CRB":  0, "REC":  1, "MP":  0}, # Pumpkinhead
    {"STR":  6, "CRR":  20, "CRB":  0, "REC": 30, "MP":  1}, # Crabclaw
    {"STR": 13, "CRR":  40, "CRB":  0, "REC": 60, "MP":  0}, # Divine Rose
    {"STR":  4, "CRR":  20, "CRB":  0, "REC": 30, "MP":  2}, # Spellbinder
    {"STR": 10, "CRR":  20, "CRB":  2, "REC": 90, "MP":  0}, # Olympia
    {"STR": 10, "CRR":  20, "CRB":  0, "REC": 30, "MP":  1}, # Lionheart
    {"STR":  9, "CRR":   2, "CRB":  0, "REC": 90, "MP": -1}, # Metal Chocobo
    {"STR":  9, "CRR":  40, "CRB":  0, "REC":  1, "MP":  1}, # Oathkeeper
    {"STR": 11, "CRR":  20, "CRB":  2, "REC": 30, "MP": -1}, # Oblivion
    {"STR":  7, "CRR":  20, "CRB":  0, "REC":  1, "MP":  2}, # Lady Luck
    {"STR":  5, "CRR": 200, "CRB":  2, "REC":  1, "MP":  0}, # Wishing Star
    {"STR": 14, "CRR":  40, "CRB":  2, "REC": 90, "MP":  2}, # Ultima Weapon
    {"STR":  3, "CRR":  20, "CRB":  0, "REC":  1, "MP":  3}, # Diamond Dust
    {"STR":  8, "CRR":  10, "CRB": 16, "REC": 90, "MP": -2}, # One-Winged Angel
    ]
VANILLA_PUPPY_LOCATIONS = [
    "Traverse Town Mystical House Glide Chest",
    "Traverse Town Alleyway Behind Crates Chest",
    "Traverse Town Item Workshop Left Chest",
    "Traverse Town Secret Waterway Near Stairs Chest",
    "Wonderland Queen's Castle Hedge Right Blue Chest",
    "Wonderland Lotus Forest Nut Chest",
    "Wonderland Tea Party Garden Above Lotus Forest Entrance 1st Chest",
    "Olympus Coliseum Coliseum Gates Right Blue Trinity Chest",
    "Deep Jungle Hippo's Lagoon Center Chest",
    "Deep Jungle Vines 2 Chest",
    "Deep Jungle Waterfall Cavern Middle Chest",
    "Deep Jungle Camp Blue Trinity Chest",
    "Agrabah Cave of Wonders Treasure Room Across Platforms Chest",
    "Halloween Town Oogie's Manor Hollow Chest",
    "Neverland Pirate Ship Deck White Trinity Chest",
    "Agrabah Cave of Wonders Hidden Room Left Chest",
    "Agrabah Cave of Wonders Entrance Tall Tower Chest",
    "Agrabah Palace Gates High Opposite Palace Chest",
    "Monstro Chamber 3 Platform Above Chamber 2 Entrance Chest",
    "Wonderland Lotus Forest Through the Painting Thunder Plant Chest",
    "Hollow Bastion Grand Hall Left of Gate Chest",
    "Halloween Town Cemetery By Cat Shape Chest",
    "Halloween Town Moonlight Hill White Trinity Chest",
    "Halloween Town Guillotine Square Pumpkin Structure Right Chest",
    "Monstro Mouth High Platform Across from Boat Chest",
    "Monstro Chamber 6 Low Chest",
    "Monstro Chamber 5 Atop Barrel Chest",
    "Neverland Hold Flight 1st Chest",
    "Neverland Hold Yellow Trinity Green Chest",
    "Neverland Captain's Cabin Chest",
    "Hollow Bastion Rising Falls Floating Platform Near Save Chest",
    "Hollow Bastion Castle Gates Gravity Chest",
    "Hollow Bastion Lift Stop Outside Library Gravity Chest"
    ]

def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="KH1 Client")


components.append(Component("KH1 Client", "KH1Client", func=launch_client, component_type=Type.CLIENT))


class KH1Web(WebWorld):
    theme = "ocean"
    tutorials = [Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Kingdom Hearts Randomizer software on your computer."
            "This guide covers single-player, multiworld, and related software.",
            "English",
            "kh1_en.md",
            "kh1/en",
            ["Gicu"]
    )]
    option_groups = kh1_option_groups
    options_presets = kh1_option_presets


class KH1World(World):
    """
    Kingdom Hearts is an action RPG following Sora on his journey 
    through many worlds to find Riku and Kairi.
    """
    game = "Kingdom Hearts"
    options_dataclass = KH1Options
    options: KH1Options
    topology_present = True
    web = KH1Web()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups
    fillers = {}
    fillers.update(get_items_by_category("Item"))
    fillers.update(get_items_by_category("Camping"))
    fillers.update(get_items_by_category("Stat Ups"))
    slot_2_levels = None
    keyblade_stats = None

    def create_items(self):
        self.place_predetermined_items()
        # Handle starting worlds
        starting_worlds = []
        if self.options.starting_worlds > 0:
            possible_starting_worlds = ["Wonderland", "Olympus Coliseum", "Deep Jungle", "Agrabah", "Monstro", "Halloween Town", "Neverland", "Hollow Bastion"]
            if self.options.atlantica:
                possible_starting_worlds.append("Atlantica")
            if self.options.end_of_the_world_unlock == "item":
                possible_starting_worlds.append("End of the World")
            starting_worlds = self.random.sample(possible_starting_worlds, min(self.options.starting_worlds.value, len(possible_starting_worlds)))
            for starting_world in starting_worlds:
                self.multiworld.push_precollected(self.create_item(starting_world))
        
        # Handle starting tools
        starting_tools = []
        if self.options.starting_tools:
            starting_tools = ["Scan", "Dodge Roll"]
            self.multiworld.push_precollected(self.create_item("Scan"))
            self.multiworld.push_precollected(self.create_item("Dodge Roll"))
        
        item_pool: List[KH1Item] = []
        possible_level_up_item_pool = []
        level_up_item_pool = []
        
        # Calculate Level Up Items
        # Fill pool with mandatory items
        for _ in range(self.options.item_slot_increase):
            level_up_item_pool.append("Item Slot Increase")
        for _ in range(self.options.accessory_slot_increase):
            level_up_item_pool.append("Accessory Slot Increase")

        # Create other pool
        for _ in range(self.options.strength_increase):
            possible_level_up_item_pool.append("Strength Increase")
        for _ in range(self.options.defense_increase):
            possible_level_up_item_pool.append("Defense Increase")
        for _ in range(self.options.hp_increase):
            possible_level_up_item_pool.append("Max HP Increase")
        for _ in range(self.options.mp_increase):
            possible_level_up_item_pool.append("Max MP Increase")
        for _ in range(self.options.ap_increase):
            possible_level_up_item_pool.append("Max AP Increase")

        # Fill remaining pool with items from other pool
        self.random.shuffle(possible_level_up_item_pool)
        level_up_item_pool = level_up_item_pool + possible_level_up_item_pool[:(99 - len(level_up_item_pool))]

        level_up_locations = list(get_locations_by_category("Levels").keys())
        self.random.shuffle(level_up_item_pool)
        current_level_for_placing_stats = self.options.force_stats_on_levels.value
        while len(level_up_item_pool) > 0 and current_level_for_placing_stats <= self.options.level_checks:
            self.get_location(level_up_locations[current_level_for_placing_stats - 1]).place_locked_item(self.create_item(level_up_item_pool.pop()))
            current_level_for_placing_stats += 1
        
        # Calculate prefilled locations and items
        prefilled_items = ["Final Door Key"]
        if not self.options.randomize_emblem_pieces:
            prefilled_items = prefilled_items + ["Emblem Piece (Flame)", "Emblem Piece (Chest)", "Emblem Piece (Fountain)", "Emblem Piece (Statue)"]
        
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        
        non_filler_item_categories = ["Key", "Magic", "Worlds", "Trinities", "Cups", "Summons", "Abilities", "Shared Abilities", "Keyblades", "Accessory", "Weapons", "Puppies"]
        if self.options.hundred_acre_wood:
            non_filler_item_categories.append("Torn Pages")
        for name, data in item_table.items():
            quantity = data.max_quantity
            if data.category not in non_filler_item_categories:
                continue
            if name in starting_worlds or name in starting_tools:
                continue
            if name == "Puppy":
                if self.options.puppies.current_key != "vanilla":
                    if self.options.puppies == "triplets":
                        item_pool += [self.create_item(name) for _ in range(33)]
                    if self.options.puppies == "individual":
                        item_pool += [self.create_item(name) for _ in range(99)]
                    if self.options.puppies == "full":
                        item_pool += [self.create_item(name) for _ in range(1)]
            elif name == "Atlantica":
                if self.options.atlantica:
                    item_pool += [self.create_item(name) for _ in range(0, quantity)]
            elif name == "Mermaid Kick":
                if self.options.atlantica:
                    if self.options.extra_shared_abilities:
                        item_pool += [self.create_item(name) for _ in range(0, 2)]
                    else:
                        item_pool += [self.create_item(name) for _ in range(0, quantity)]
            elif name == "Crystal Trident":
                if self.options.atlantica:
                    item_pool += [self.create_item(name) for _ in range(0, quantity)]
            elif name == "High Jump":
                if self.options.extra_shared_abilities:
                    item_pool += [self.create_item(name) for _ in range(0, 3)]
                else:
                    item_pool += [self.create_item(name) for _ in range(0, quantity)]
            elif name == "Progressive Glide":
                if self.options.extra_shared_abilities:
                    item_pool += [self.create_item(name) for _ in range(0, 4)]
                else:
                    item_pool += [self.create_item(name) for _ in range(0, quantity)]
            elif name == "End of the World":
                if self.options.end_of_the_world_unlock.current_key == "item":
                    item_pool += [self.create_item(name) for _ in range(0, quantity)]
            elif name == "EXP Zero":
                if self.options.exp_zero_in_pool:
                    item_pool += [self.create_item(name) for _ in range(0, quantity)]
            elif name == "Postcard":
                if self.options.randomize_postcards.current_key == "chests":
                    item_pool += [self.create_item(name) for _ in range(0, 3)]
                if self.options.randomize_postcards.current_key == "all":
                    item_pool += [self.create_item(name) for _ in range(0, quantity)]
            elif name not in prefilled_items:
                item_pool += [self.create_item(name) for _ in range(0, quantity)]
        
        for i in range(self.determine_lucky_emblems_in_pool()):
            item_pool += [self.create_item("Lucky Emblem")]
        
        while len(item_pool) < total_locations and len(level_up_item_pool) > 0:
            item_pool += [self.create_item(level_up_item_pool.pop())]
        
        # Fill any empty locations with filler items.
        while len(item_pool) < total_locations:
            item_pool.append(self.create_item(self.get_filler_item_name()))
        
        self.multiworld.itempool += item_pool

    def place_predetermined_items(self) -> None:
        if self.options.final_rest_door_key.current_key not in ["puppies", "postcards", "lucky emblems"]:
            goal_dict = {
                "sephiroth":       "Olympus Coliseum Defeat Sephiroth Ansem's Report 12",
                "unknown":         "Hollow Bastion Defeat Unknown Ansem's Report 13",
                "final_rest":      "End of the World Final Rest Chest"
            }
            goal_location_name = goal_dict[self.options.final_rest_door_key.current_key]
        elif self.options.final_rest_door_key.current_key == "postcards":
            lpad_number = str(self.options.required_postcards).rjust(2, "0")
            goal_location_name = "Traverse Town Mail Postcard " + lpad_number + " Event"
        elif self.options.final_rest_door_key.current_key == "puppies":
            required_puppies = self.options.required_puppies.value
            goal_location_name = "Traverse Town Piano Room Return " + str(required_puppies) + " Puppies"
            if required_puppies == 50 or required_puppies == 99:
                goal_location_name = goal_location_name + " Reward 2"
        self.get_location(goal_location_name).place_locked_item(self.create_item("Final Door Key"))
        self.get_location("Final Ansem").place_locked_item(self.create_event("Victory"))
                
        if not self.options.randomize_emblem_pieces:
            self.get_location("Hollow Bastion Entrance Hall Emblem Piece (Flame)").place_locked_item(self.create_item("Emblem Piece (Flame)"))
            self.get_location("Hollow Bastion Entrance Hall Emblem Piece (Statue)").place_locked_item(self.create_item("Emblem Piece (Statue)"))
            self.get_location("Hollow Bastion Entrance Hall Emblem Piece (Fountain)").place_locked_item(self.create_item("Emblem Piece (Fountain)"))
            self.get_location("Hollow Bastion Entrance Hall Emblem Piece (Chest)").place_locked_item(self.create_item("Emblem Piece (Chest)"))
        if self.options.randomize_postcards.current_key not in ["all"]:
            self.get_location("Traverse Town Item Shop Postcard").place_locked_item(self.create_item("Postcard"))
            self.get_location("Traverse Town 1st District Safe Postcard").place_locked_item(self.create_item("Postcard"))
            self.get_location("Traverse Town Gizmo Shop Postcard 1").place_locked_item(self.create_item("Postcard"))
            self.get_location("Traverse Town Gizmo Shop Postcard 2").place_locked_item(self.create_item("Postcard"))
            self.get_location("Traverse Town Item Workshop Postcard").place_locked_item(self.create_item("Postcard"))
            self.get_location("Traverse Town 3rd District Balcony Postcard").place_locked_item(self.create_item("Postcard"))
            self.get_location("Traverse Town Geppetto's House Postcard").place_locked_item(self.create_item("Postcard"))
        if self.options.randomize_postcards.current_key == "vanilla":
            self.get_location("Traverse Town 1st District Accessory Shop Roof Chest").place_locked_item(self.create_item("Postcard"))
            self.get_location("Traverse Town 2nd District Boots and Shoes Awning Chest").place_locked_item(self.create_item("Postcard"))
            self.get_location("Traverse Town 1st District Blue Trinity Balcony Chest").place_locked_item(self.create_item("Postcard"))
        if self.options.puppies.current_key == "vanilla":
            for i, location in enumerate(VANILLA_PUPPY_LOCATIONS):
                self.get_location(location).place_locked_item(self.create_item("Puppy"))

    def get_filler_item_name(self) -> str:
        weights = [data.weight for data in self.fillers.values()]
        return self.random.choices([filler for filler in self.fillers.keys()], weights)[0]

    def fill_slot_data(self) -> dict:
        slot_data = {"xpmult": int(self.options.exp_multiplier)/16,
                    "required_lucky_emblems_eotw": self.determine_lucky_emblems_required_to_open_end_of_the_world(),
                    "required_lucky_emblems_door": self.determine_lucky_emblems_required_to_open_final_rest_door(),
                    "seed": self.multiworld.seed_name,
                    "advanced_logic": bool(self.options.advanced_logic),
                    "hundred_acre_wood": bool(self.options.hundred_acre_wood),
                    "atlantica": bool(self.options.atlantica),
                    "final_rest_door_key": str(self.options.final_rest_door_key.current_key),
                    "remote_location_ids": self.get_remote_location_ids()}
        if self.options.donald_death_link:
            slot_data["donalddl"] = ""
        if self.options.goofy_death_link:
            slot_data["goofydl"] = ""
        if self.options.keyblades_unlock_chests:
            slot_data["chestslocked"] = ""
        else:
            slot_data["chestsunlocked"] = ""
        if self.options.interact_in_battle:
            slot_data["interactinbattle"] = ""
        slot_data["required_postcards"] = self.options.required_postcards.value
        slot_data["required_puppies"] = self.options.required_puppies.value
        return slot_data
    
    def create_item(self, name: str) -> KH1Item:
        data = item_table[name]
        return KH1Item(name, data.classification, data.code, self.player)

    def create_event(self, name: str) -> KH1Item:
        data = event_item_table[name]
        return KH1Item(name, data.classification, data.code, self.player)

    def set_rules(self):
        set_rules(self)

    def create_regions(self):
        create_regions(self)
    
    def generate_output(self, output_directory: str):
        """
        Generates the json file for use with mod generator.
        """
        generate_json(self, output_directory)
    
    def generate_early(self):
        value_names = ["Lucky Emblems to Open End of the World", "Lucky Emblems to Open Final Rest Door", "Lucky Emblems in Pool"]
        initial_lucky_emblem_settings = [self.options.required_lucky_emblems_eotw.value, self.options.required_lucky_emblems_door.value, self.options.lucky_emblems_in_pool.value]
        self.change_numbers_of_lucky_emblems_to_consider()
        new_lucky_emblem_settings = [self.options.required_lucky_emblems_eotw.value, self.options.required_lucky_emblems_door.value, self.options.lucky_emblems_in_pool.value]
        for i in range(3):
            if initial_lucky_emblem_settings[i] != new_lucky_emblem_settings[i]:
                logging.info(f"{self.player_name}'s value {initial_lucky_emblem_settings[i]} for \"{value_names[i]}\" was invalid\n"
                             f"Setting \"{value_names[i]}\" value to {new_lucky_emblem_settings[i]}")
    
    def change_numbers_of_lucky_emblems_to_consider(self) -> None:
        if self.options.end_of_the_world_unlock == "lucky_emblems" and self.options.final_rest_door_key == "lucky_emblems":
            self.options.required_lucky_emblems_eotw.value, self.options.required_lucky_emblems_door.value, self.options.lucky_emblems_in_pool.value = sorted(
                [self.options.required_lucky_emblems_eotw.value, self.options.required_lucky_emblems_door.value, self.options.lucky_emblems_in_pool.value])

        elif self.options.end_of_the_world_unlock == "lucky_emblems":
            self.options.required_lucky_emblems_eotw.value, self.options.lucky_emblems_in_pool.value = sorted(
                [self.options.required_lucky_emblems_eotw.value, self.options.lucky_emblems_in_pool.value])

        elif self.options.final_rest_door_key == "lucky_emblems":
            self.options.required_lucky_emblems_door.value, self.options.lucky_emblems_in_pool.value = sorted(
                [self.options.required_lucky_emblems_door.value, self.options.lucky_emblems_in_pool.value])

    def determine_lucky_emblems_in_pool(self) -> int:
        if self.options.end_of_the_world_unlock == "lucky_emblems" or self.options.final_rest_door_key == "lucky_emblems":
            return self.options.lucky_emblems_in_pool.value
        return 0
    
    def determine_lucky_emblems_required_to_open_end_of_the_world(self) -> int:
        if self.options.end_of_the_world_unlock == "lucky_emblems":
            return self.options.required_lucky_emblems_eotw.value
        return 14
    
    def determine_lucky_emblems_required_to_open_final_rest_door(self) -> int:
        if self.options.final_rest_door_key == "lucky_emblems":
            return self.options.required_lucky_emblems_door.value
        return 14
    
    def get_remote_location_ids(self):
        remote_location_ids = []
        for location in self.multiworld.get_filled_locations(self.player):
            if location.name != "Final Ansem":
                location_data = location_table[location.name]
                if self.player == location.item.player and location.item.name != "Victory":
                    item_data = item_table[location.item.name]
                    if location_data.type == "Chest":
                        if item_data.type in ["Stats"]:
                            remote_location_ids.append(location_data.code)
                    if location_data.type == "Reward":
                        if item_data.type in ["Stats"]:
                            remote_location_ids.append(location_data.code)
                    if location_data.type == "Static":
                        if item_data.type not in ["Item"]:
                            remote_location_ids.append(location_data.code)
                    if location_data.type == "Level Slot 1":
                        if item_data.type not in ["Stats"]:
                            remote_location_ids.append(location_data.code)
                    if location_data.type == "Level Slot 2":
                        if item_data.type not in ["Stats", "Ability"]:
                            remote_location_ids.append(location_data.code)
        return remote_location_ids
    
    def get_slot_2_levels(self):
        if self.slot_2_levels is None:
            self.slot_2_levels = []
            if self.options.slot_2_level_checks.value > self.options.level_checks.value:
                logging.info(f"{self.player_name}'s value of {self.options.slot_2_level_checks.value} for slot 2 level checks is invalid as it exceeds their value of {self.options.level_checks.value} for Level Checks\n"
                            f"Setting slot 2 level check's value to {self.options.level_checks.value}")
                self.options.slot_2_level_checks.value = self.options.level_checks.value
            self.slot_2_levels = self.random.sample(range(2,self.options.level_checks.value + 1), self.options.slot_2_level_checks.value)
        return self.slot_2_levels
    
    def get_keyblade_stats(self):
        # Create keyblade stat array from vanilla
        keyblade_stats = VANILLA_KEYBLADE_STATS.copy()
        # Handle shuffling keyblade stats
        if self.options.keyblade_stats != "vanilla":
            if self.options.keyblade_stats == "randomize":
                # Fix any minimum and max values from settings
                min_str_bonus = min(self.options.keyblade_min_str.value, self.options.keyblade_max_str.value)
                max_str_bonus = max(self.options.keyblade_min_str.value, self.options.keyblade_max_str.value)
                self.options.keyblade_min_str.value = min_str_bonus
                self.options.keyblade_max_str.value = max_str_bonus
                min_crit_rate = min(self.options.keyblade_min_crit_rate.value, self.options.keyblade_max_crit_rate.value)
                max_crit_rate = max(self.options.keyblade_min_crit_rate.value, self.options.keyblade_max_crit_rate.value)
                self.options.keyblade_min_crit_rate.value = min_crit_rate
                self.options.keyblade_max_crit_rate.value = max_crit_rate
                min_crit_str = min(self.options.keyblade_min_crit_str.value, self.options.keyblade_max_crit_str.value)
                max_crit_str = max(self.options.keyblade_min_crit_str.value, self.options.keyblade_max_crit_str.value)
                self.options.keyblade_min_crit_str.value = min_crit_str
                self.options.keyblade_max_crit_str.value = max_crit_str
                min_recoil = min(self.options.keyblade_min_recoil.value, self.options.keyblade_max_recoil.value)
                max_recoil = max(self.options.keyblade_min_recoil.value, self.options.keyblade_max_recoil.value)
                self.options.keyblade_min_recoil.value = min_recoil
                self.options.keyblade_max_recoil.value = max_recoil
                min_mp_bonus = min(self.options.keyblade_min_mp.value, self.options.keyblade_max_mp.value)
                max_mp_bonus = max(self.options.keyblade_min_mp.value, self.options.keyblade_max_mp.value)
                self.options.keyblade_min_mp.value = min_mp_bonus
                self.options.keyblade_max_mp.value = max_mp_bonus
                for keyblade in keyblade_stats:
                        keyblade["STR"] = int(self.random.randint(min_str_bonus, max_str_bonus))
                        keyblade["CRR"] = int(self.random.randint(min_crit_rate, max_crit_rate))
                        keyblade["CRB"] = int(self.random.randint(min_crit_str, max_crit_str))
                        keyblade["REC"] = int(self.random.randint(min_recoil, max_recoil))
                        keyblade["MP"]  = int(self.random.randint(min_mp_bonus, max_mp_bonus))
            elif self.options.keyblade_stats == "shuffle":
                if self.options.bad_starting_weapons:
                    starting_weapons = keyblade_stats[:4]
                    other_weapons = keyblade_stats[4:]
                    self.random.shuffle(other_weapons)
                    keyblade_stats = starting_weapons + other_weapons
                else:
                    self.random.shuffle(keyblade_stats)
        return keyblade_stats
