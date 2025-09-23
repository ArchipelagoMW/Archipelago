import logging
import re
from typing import List
from math import ceil

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import KH1Item, KH1ItemData, event_item_table, get_items_by_category, item_table, item_name_groups
from .Locations import KH1Location, location_table, get_locations_by_type, location_name_groups
from .Options import KH1Options, kh1_option_groups
from .Regions import connect_entrances, create_regions
from .Rules import set_rules
from .Presets import kh1_option_presets
from worlds.LauncherComponents import Component, components, Type, launch as launch_component, icon_paths
from .GenerateJSON import generate_json
from .Data import VANILLA_KEYBLADE_STATS, VANILLA_PUPPY_LOCATIONS, CHAR_TO_KH, VANILLA_ABILITY_AP_COSTS, WORLD_KEY_ITEMS
from worlds.LauncherComponents import Component, components, Type, launch_subprocess

def launch_client():
    from .Client import launch
    launch_component(launch, name="KH1 Client")


components.append(Component("KH1 Client", func=launch_client, component_type=Type.CLIENT, icon="kh1_heart"))

icon_paths["kh1_heart"] = f"ap:{__name__}/icons/kh1_heart.png"


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
    slot_2_levels: list[int]
    keyblade_stats: list[dict[str, int]]
    starting_accessory_locations: list[str]
    starting_accessories: list[str]
    ap_costs: list[dict[str, str | int | bool]]

    def __init__(self, multiworld, player):
        super(KH1World, self).__init__(multiworld, player)
        self.slot_2_levels = None
        self.keyblade_stats = None
        self.starting_accessory_locations = None
        self.starting_accessories = None
        self.ap_costs = None

    def create_items(self):
        self.place_predetermined_items()
        # Handle starting worlds
        starting_worlds = []
        if self.options.starting_worlds > 0:
            possible_starting_worlds = ["Wonderland", "Olympus Coliseum", "Deep Jungle", "Agrabah", "Monstro", "Halloween Town", "Neverland", "Hollow Bastion"]
            if self.options.atlantica:
                possible_starting_worlds.append("Atlantica")
            if self.options.destiny_islands:
                possible_starting_worlds.append("Destiny Islands")
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
        
        # Handle starting party member accessories
        starting_party_member_accessories = []
        starting_party_member_locations = []
        starting_party_member_locations = self.get_starting_accessory_locations()
        starting_party_member_accessories = self.get_starting_accessories()
        for i in range(len(starting_party_member_locations)):
            self.get_location(self.starting_accessory_locations[i]).place_locked_item(self.create_item(self.starting_accessories[i]))
        
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
        
        level_up_locations = list(get_locations_by_type("Level Slot 1").keys())
        self.random.shuffle(level_up_item_pool)
        current_level_index_for_placing_stats = self.options.force_stats_on_levels.value - 2 # Level 2 is index 0, Level 3 is index 1, etc
        if self.options.remote_items.current_key == "off" and self.options.force_stats_on_levels.value != 2:
            logging.info(f"{self.player_name}'s value {self.options.force_stats_on_levels.value} for force_stats_on_levels was changed\n"
                         f"Set to 2 as remote_items if \"off\"")
            self.options.force_stats_on_levels.value = 2
            current_level_index_for_placing_stats = 0
        while len(level_up_item_pool) > 0 and current_level_index_for_placing_stats < self.options.level_checks: # With all levels in location pool, 99 level ups so need to go index 0-98
            self.get_location(level_up_locations[current_level_index_for_placing_stats]).place_locked_item(self.create_item(level_up_item_pool.pop()))
            current_level_index_for_placing_stats += 1
        
        
        
        # Calculate prefilled locations and items
        exclude_items = ["Final Door Key", "Lucky Emblem"]
        if not self.options.randomize_emblem_pieces:
            exclude_items = exclude_items + ["Emblem Piece (Flame)", "Emblem Piece (Chest)", "Emblem Piece (Fountain)", "Emblem Piece (Statue)"]
        
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        
        non_filler_item_categories = ["Key", "Magic", "Worlds", "Trinities", "Cups", "Summons", "Abilities", "Shared Abilities", "Keyblades", "Accessory", "Weapons", "Puppies"]
        if self.options.hundred_acre_wood:
            non_filler_item_categories.append("Torn Pages")
        for name, data in item_table.items():
            quantity = data.max_quantity
            if data.category not in non_filler_item_categories:
                continue
            if name in starting_worlds or name in starting_tools or name in starting_party_member_accessories:
                continue
            if self.options.stacking_world_items and name in WORLD_KEY_ITEMS.keys() and name not in ("Crystal Trident", "Jack-In-The-Box"): # Handling these special cases separately
                item_pool += [self.create_item(WORLD_KEY_ITEMS[name]) for _ in range(0, 1)]
            elif self.options.halloween_town_key_item_bundle and name == "Jack-In-The-Box":
                continue
            elif name == "Puppy":
                if self.options.randomize_puppies:
                    item_pool += [self.create_item(name) for _ in range(ceil(99/self.options.puppy_value.value))]
            elif name == "Atlantica":
                if self.options.atlantica:
                    item_pool += [self.create_item(name) for _ in range(0, quantity)]
            elif name == "Mermaid Kick":
                if self.options.atlantica and self.options.extra_shared_abilities:
                    item_pool += [self.create_item(name) for _ in range(0, 2)]
                else:
                    item_pool += [self.create_item(name) for _ in range(0, quantity)]
            elif name == "Crystal Trident":
                if self.options.atlantica:
                    if self.options.stacking_world_items:
                        item_pool += [self.create_item(WORLD_KEY_ITEMS[name]) for _ in range(0, 1)]
                    else:
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
            elif name == "Orichalcum":
                item_pool += [self.create_item(name) for _ in range(0, self.options.orichalcum_in_pool.value)]
            elif name == "Mythril":
                item_pool += [self.create_item(name) for _ in range(0, self.options.mythril_in_pool.value)]
            elif name == "Destiny Islands":
                if self.options.destiny_islands:
                    item_pool += [self.create_item(name) for _ in range(0, quantity)]
            elif name == "Raft Materials":
                if self.options.destiny_islands:
                    item_pool += [self.create_item(name) for _ in range(0, self.options.materials_in_pool.value)]
            elif name not in exclude_items:
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
        if self.options.final_rest_door_key.current_key not in ["puppies", "postcards", "lucky_emblems"]:
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
        if self.options.final_rest_door_key.current_key != "lucky_emblems":
            self.get_location(goal_location_name).place_locked_item(self.create_item("Final Door Key"))
        self.get_location("Final Ansem").place_locked_item(self.create_event("Victory"))
                
        if not self.options.randomize_emblem_pieces:
            self.get_location("Hollow Bastion Entrance Hall Emblem Piece (Flame)").place_locked_item(self.create_item("Emblem Piece (Flame)"))
            self.get_location("Hollow Bastion Entrance Hall Emblem Piece (Statue)").place_locked_item(self.create_item("Emblem Piece (Statue)"))
            self.get_location("Hollow Bastion Entrance Hall Emblem Piece (Fountain)").place_locked_item(self.create_item("Emblem Piece (Fountain)"))
            self.get_location("Hollow Bastion Entrance Hall Emblem Piece (Chest)").place_locked_item(self.create_item("Emblem Piece (Chest)"))
        if self.options.randomize_postcards != "all":
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
        if not self.options.randomize_puppies:
            if self.options.puppy_value.value != 3:
                self.options.puppy_value.value = 3
                logging.info(f"{self.player_name}'s value of {self.options.puppy_value.value} for puppy value was changed to 3 as Randomize Puppies is OFF")
            for i, location in enumerate(VANILLA_PUPPY_LOCATIONS):
                self.get_location(location).place_locked_item(self.create_item("Puppy"))

    def get_filler_item_name(self) -> str:
        weights = [data.weight for data in self.fillers.values()]
        return self.random.choices([filler for filler in self.fillers.keys()], weights)[0]

    def fill_slot_data(self) -> dict:
        slot_data = {
                    "atlantica": bool(self.options.atlantica),
                    "auto_attack": bool(self.options.auto_attack),
                    "auto_save": bool(self.options.auto_save),
                    "bad_starting_weapons": bool(self.options.bad_starting_weapons),
                    "beep_hack": bool(self.options.beep_hack),
                    "consistent_finishers": bool(self.options.consistent_finishers),
                    "cups": str(self.options.cups.current_key),
                    "day_2_materials": int(self.options.day_2_materials.value),
                    "death_link": str(self.options.death_link.current_key),
                    "destiny_islands": bool(self.options.destiny_islands),
                    "donald_death_link": bool(self.options.donald_death_link),
                    "early_skip": bool(self.options.early_skip),
                    "end_of_the_world_unlock": str(self.options.end_of_the_world_unlock.current_key),
                    "exp_multiplier": int(self.options.exp_multiplier.value)/16,
                    "exp_zero_in_pool": bool(self.options.exp_zero_in_pool),
                    "extra_shared_abilities": bool(self.options.extra_shared_abilities),
                    "fast_camera": bool(self.options.fast_camera),
                    "faster_animations": bool(self.options.faster_animations),
                    "final_rest_door_key": str(self.options.final_rest_door_key.current_key),
                    "force_stats_on_levels": int(self.options.force_stats_on_levels.value),
                    "four_by_three": bool(self.options.four_by_three),
                    "goofy_death_link": bool(self.options.goofy_death_link),
                    "halloween_town_key_item_bundle": bool(self.options.halloween_town_key_item_bundle),
                    "homecoming_materials": int(self.options.homecoming_materials.value),
                    "hundred_acre_wood": bool(self.options.hundred_acre_wood),
                    "interact_in_battle": bool(self.options.interact_in_battle),
                    "jungle_slider": bool(self.options.jungle_slider),
                    "keyblades_unlock_chests": bool(self.options.keyblades_unlock_chests),
                    "level_checks": int(self.options.level_checks.value),
                    "logic_difficulty": str(self.options.logic_difficulty.current_key),
                    "materials_in_pool": int(self.options.materials_in_pool.value),
                    "max_ap_cost": int(self.options.max_ap_cost.value),
                    "min_ap_cost": int(self.options.min_ap_cost.value),
                    "mythril_in_pool": int(self.options.mythril_in_pool.value),
                    "mythril_price": int(self.options.mythril_price.value),
                    "one_hp": bool(self.options.one_hp),
                    "orichalcum_in_pool": int(self.options.orichalcum_in_pool.value),
                    "orichalcum_price": int(self.options.orichalcum_price.value),
                    "puppy_value": int(self.options.puppy_value.value),
                    "randomize_ap_costs": str(self.options.randomize_ap_costs.current_key),
                    "randomize_emblem_pieces": bool(self.options.exp_zero_in_pool),
                    "randomize_party_member_starting_accessories": bool(self.options.randomize_party_member_starting_accessories),
                    "randomize_postcards": str(self.options.randomize_postcards.current_key),
                    "randomize_puppies": str(self.options.randomize_puppies.current_key),
                    "remote_items": str(self.options.remote_items.current_key),
                    "remote_location_ids": self.get_remote_location_ids(),
                    "required_lucky_emblems_door": self.determine_lucky_emblems_required_to_open_final_rest_door(),
                    "required_lucky_emblems_eotw": self.determine_lucky_emblems_required_to_open_end_of_the_world(),
                    "required_postcards": int(self.options.required_postcards.value),
                    "required_puppies": int(self.options.required_puppies.value),
                    "seed": self.multiworld.seed_name,
                    "shorten_go_mode": bool(self.options.shorten_go_mode),
                    "slot_2_level_checks": int(self.options.slot_2_level_checks.value),
                    "stacking_world_items": bool(self.options.stacking_world_items),
                    "starting_items": [item.code for item in self.multiworld.precollected_items[self.player]],
                    "starting_tools": bool(self.options.starting_tools),
                    "super_bosses": bool(self.options.super_bosses),
                    "synthesis_item_name_byte_arrays": self.get_synthesis_item_name_byte_arrays(),
                    "unlock_0_volume": bool(self.options.unlock_0_volume),
                    "unskippable": bool(self.options.unskippable),
                    "warp_anywhere": bool(self.options.warp_anywhere)
                    }
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
    
    def connect_entrances(self):
        connect_entrances(self)
    
    def generate_output(self, output_directory: str):
        """
        Generates the json file for use with mod generator.
        """
        generate_json(self, output_directory)
    
    def generate_early(self):
        self.determine_level_checks()
        
        value_names = ["Lucky Emblems to Open End of the World", "Lucky Emblems to Open Final Rest Door", "Lucky Emblems in Pool"]
        initial_lucky_emblem_settings = [self.options.required_lucky_emblems_eotw.value, self.options.required_lucky_emblems_door.value, self.options.lucky_emblems_in_pool.value]
        self.change_numbers_of_lucky_emblems_to_consider()
        new_lucky_emblem_settings = [self.options.required_lucky_emblems_eotw.value, self.options.required_lucky_emblems_door.value, self.options.lucky_emblems_in_pool.value]
        for i in range(3):
            if initial_lucky_emblem_settings[i] != new_lucky_emblem_settings[i]:
                logging.info(f"{self.player_name}'s value {initial_lucky_emblem_settings[i]} for \"{value_names[i]}\" was invalid\n"
                             f"Setting \"{value_names[i]}\" value to {new_lucky_emblem_settings[i]}")
        
        value_names = ["Day 2 Materials", "Homecoming Materials", "Materials in Pool"]
        initial_materials_settings = [self.options.day_2_materials.value, self.options.homecoming_materials.value, self.options.materials_in_pool.value]
        self.change_numbers_of_materials_to_consider()
        new_materials_settings = [self.options.day_2_materials.value, self.options.homecoming_materials.value, self.options.materials_in_pool.value]
        for i in range(3):
            if initial_materials_settings[i] != new_materials_settings[i]:
                logging.info(f"{self.player_name}'s value {initial_materials_settings[i]} for \"{value_names[i]}\" was invalid\n"
                             f"Setting \"{value_names[i]}\" value to {new_materials_settings[i]}")
        
        if self.options.stacking_world_items.value and not self.options.halloween_town_key_item_bundle.value:
            logging.info(f"{self.player_name}'s value {self.options.halloween_town_key_item_bundle.value} for Halloween Town Key Item Bundle must be TRUE when Stacking World Items is on.  Setting to TRUE")
            self.options.halloween_town_key_item_bundle.value = True
    
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
        return -1
    
    def determine_lucky_emblems_required_to_open_final_rest_door(self) -> int:
        if self.options.final_rest_door_key == "lucky_emblems":
            return self.options.required_lucky_emblems_door.value
        return -1
    
    def change_numbers_of_materials_to_consider(self) -> None:
        if self.options.destiny_islands:
            self.options.day_2_materials.value, self.options.homecoming_materials.value, self.options.materials_in_pool.value = sorted(
                [self.options.day_2_materials.value, self.options.homecoming_materials.value, self.options.materials_in_pool.value])
    
    def get_remote_location_ids(self):
        remote_location_ids = []
        for location in self.multiworld.get_filled_locations(self.player):
            if location.name != "Final Ansem":
                location_data = location_table[location.name]
                if self.options.remote_items.current_key == "full":
                    if location_data.type != "Starting Accessory":
                        remote_location_ids.append(location_data.code)
                elif self.player == location.item.player and location.item.name != "Victory":
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
                        if item_data.category not in ["Level Up", "Limited Level Up"]:
                            remote_location_ids.append(location_data.code)
                    if location_data.type == "Level Slot 2":
                        if item_data.category not in ["Level Up", "Limited Level Up", "Abilities"]:
                            remote_location_ids.append(location_data.code)
                    if location_data.type == "Synth":
                        if item_data.type not in ["Item"]:
                            remote_location_ids.append(location_data.code)
                    if location_data.type == "Prize":
                        if item_data.type not in ["Item"]:
                            remote_location_ids.append(location_data.code)
        return remote_location_ids
    
    def get_slot_2_levels(self):
        if self.slot_2_levels is None:
            self.slot_2_levels = []
            if self.options.max_level_for_slot_2_level_checks - 1 > self.options.level_checks.value:
                logging.info(f"{self.player_name}'s value of {self.options.max_level_for_slot_2_level_checks.value} for max level for slot 2 level checks is invalid as it exceeds their value of {self.options.level_checks.value} for Level Checks\n"
                            f"Setting max level for slot 2 level checks's value to {self.options.level_checks.value + 1}")
                self.options.max_level_for_slot_2_level_checks.value = self.options.level_checks.value + 1
            if self.options.slot_2_level_checks.value > self.options.level_checks.value:
                logging.info(f"{self.player_name}'s value of {self.options.slot_2_level_checks.value} for slot 2 level checks is invalid as it exceeds their value of {self.options.level_checks.value} for Level Checks\n"
                            f"Setting slot 2 level check's value to {self.options.level_checks.value}")
                self.options.slot_2_level_checks.value = self.options.level_checks.value
            if self.options.slot_2_level_checks > self.options.max_level_for_slot_2_level_checks - 1:
                logging.info(f"{self.player_name}'s value of {self.options.slot_2_level_checks.value} for slot 2 level checks is invalid as it exceeds their value of {self.options.max_level_for_slot_2_level_checks.value} for Max Level for Slot 2 Level Checks\n"
                            f"Setting slot 2 level check's value to {self.options.max_level_for_slot_2_level_checks.value - 1}")
                self.options.slot_2_level_checks.value = self.options.max_level_for_slot_2_level_checks.value - 1
            # Range is exclusive of the top, so if max_level_for_slot_2_level_checks is 2 then the top end of the range needs to be 3 as the only level it can choose is 2.
            self.slot_2_levels = self.random.sample(range(2,self.options.max_level_for_slot_2_level_checks.value + 1), self.options.slot_2_level_checks.value) 
        return self.slot_2_levels
    
    def get_keyblade_stats(self):
        # Create keyblade stat array from vanilla
        keyblade_stats = [x.copy() for x in VANILLA_KEYBLADE_STATS]
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
                if self.options.bad_starting_weapons:
                    starting_weapons = keyblade_stats[:4]
                    other_weapons = keyblade_stats[4:]
                else:
                    starting_weapons = []
                    other_weapons = keyblade_stats
                for keyblade in other_weapons:
                        keyblade["STR"] = self.random.randint(min_str_bonus, max_str_bonus)
                        keyblade["CRR"] = self.random.randint(min_crit_rate, max_crit_rate)
                        keyblade["CRB"] = self.random.randint(min_crit_str, max_crit_str)
                        keyblade["REC"] = self.random.randint(min_recoil, max_recoil)
                        keyblade["MP"]  = self.random.randint(min_mp_bonus, max_mp_bonus)
                keyblade_stats = starting_weapons + other_weapons
            elif self.options.keyblade_stats == "shuffle":
                if self.options.bad_starting_weapons:
                    starting_weapons = keyblade_stats[:4]
                    other_weapons = keyblade_stats[4:]
                    self.random.shuffle(other_weapons)
                    keyblade_stats = starting_weapons + other_weapons
                else:
                    self.random.shuffle(keyblade_stats)
        return keyblade_stats
    
    def determine_level_checks(self):
        # Handle if remote_items is off and level_checks > number of stats items
        total_level_up_items = min(99,
            self.options.strength_increase.value +\
            self.options.defense_increase.value +\
            self.options.hp_increase.value +\
            self.options.mp_increase.value +\
            self.options.ap_increase.value +\
            self.options.accessory_slot_increase.value +\
            self.options.item_slot_increase.value)
        if self.options.level_checks.value > total_level_up_items and self.options.remote_items.current_key == "off":
            logging.info(f"{self.player_name}'s value {self.options.level_checks.value} for level_checks was changed.\n"
                         f"This value cannot be more than the number of stat items in the pool when \"remote_items\" is \"off\".\n"
                         f"Set to be equal to number of stat items in pool, {total_level_up_items}.")
            self.options.level_checks.value = total_level_up_items
    
    def get_synthesis_item_name_byte_arrays(self):
        # Get synth item names to show in synthesis menu
        synthesis_byte_arrays = []
        for location in self.multiworld.get_filled_locations(self.player):
            if location.name != "Final Ansem":
                location_data = location_table[location.name]
                if location_data.type == "Synth":
                    item_name = re.sub('[^A-Za-z0-9 ]+', '',str(location.item.name.replace("Progressive", "Prog")))[:14]
                    byte_array = []
                    for character in item_name:
                        byte_array.append(CHAR_TO_KH[character])
                    synthesis_byte_arrays.append(byte_array)
        return synthesis_byte_arrays
    
    def get_starting_accessory_locations(self):
        if self.starting_accessory_locations is None:
            if self.options.randomize_party_member_starting_accessories:
                self.starting_accessory_locations = list(get_locations_by_type("Starting Accessory").keys())
                if not self.options.atlantica:
                    self.starting_accessory_locations.remove("Ariel Starting Accessory 1")
                    self.starting_accessory_locations.remove("Ariel Starting Accessory 2")
                    self.starting_accessory_locations.remove("Ariel Starting Accessory 3")
                self.starting_accessory_locations = self.random.sample(self.starting_accessory_locations, 10)
            else:
                self.starting_accessory_locations = []
        return self.starting_accessory_locations
    
    def get_starting_accessories(self):
        if self.starting_accessories is None:
            if self.options.randomize_party_member_starting_accessories:
                self.starting_accessories = list(get_items_by_category("Accessory").keys())
                self.starting_accessories = self.random.sample(self.starting_accessories, 10)
            else:
                self.starting_accessories = []
        return self.starting_accessories
    
    def get_ap_costs(self):
        if self.ap_costs is None:
            ap_costs = VANILLA_ABILITY_AP_COSTS.copy()
            if self.options.randomize_ap_costs.current_key == "shuffle":
                possible_costs = []
                for ap_cost in VANILLA_ABILITY_AP_COSTS:
                    if ap_cost["Randomize"]:
                        possible_costs.append(ap_cost["AP Cost"])
                self.random.shuffle(possible_costs)
                for ap_cost in ap_costs:
                    if ap_cost["Randomize"]:
                        ap_cost["AP Cost"] = possible_costs.pop(0)
            elif self.options.randomize_ap_costs.current_key == "randomize":
                for ap_cost in ap_costs:
                    if ap_cost["Randomize"]:
                        ap_cost["AP Cost"] = self.random.randint(self.options.min_ap_cost.value, self.options.max_ap_cost.value)
            elif self.options.randomize_ap_costs.current_key == "distribute":
                total_ap_value = 0
                for ap_cost in VANILLA_ABILITY_AP_COSTS:
                    if ap_cost["Randomize"]:
                        total_ap_value = total_ap_value + ap_cost["AP Cost"]
                for ap_cost in ap_costs:
                    if ap_cost["Randomize"]:
                        total_ap_value = total_ap_value - self.options.min_ap_cost.value
                        ap_cost["AP Cost"] = self.options.min_ap_cost.value
                while total_ap_value > 0:
                    ap_cost = self.random.choice(ap_costs)
                    if ap_cost["Randomize"]:
                        if ap_cost["AP Cost"] < self.options.max_ap_cost.value:
                            amount_to_add = self.random.randint(1, min(self.options.max_ap_cost.value - ap_cost["AP Cost"], total_ap_value))
                            ap_cost["AP Cost"] = ap_cost["AP Cost"] + amount_to_add
                            total_ap_value = total_ap_value - amount_to_add
            self.ap_costs = ap_costs
        return self.ap_costs
