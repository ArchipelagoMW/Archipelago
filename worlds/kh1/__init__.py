from typing import List

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import KH1Item, KH1ItemData, event_item_table, get_items_by_category, item_table, item_name_groups
from .Locations import KH1Location, location_table, get_locations_by_category, location_name_groups
from .Options import KH1Options
from .Regions import create_regions
from .Rules import set_rules
from worlds.LauncherComponents import Component, components, Type, launch_subprocess
import random


def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="KH1 Client")


components.append(Component("KH1 Client", "KH1Client", func=launch_client, component_type=Type.CLIENT))


class KH1Web(WebWorld):
    theme = "ocean"
    tutorials = [Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Kingdom Hearts Randomizer software on your computer. This guide covers single-player, "
            "multiworld, and related software.",
            "English",
            "kh1_en.md",
            "kh1/en",
            ["Gicu"]
    )]


class KH1World(World):
    """
    Kingdom Hearts is an action RPG following Sora on his journey 
    through many worlds to find Riku and Kairi.
    """
    game = "Kingdom Hearts"
    options_dataclass = KH1Options
    options: KH1Options
    topology_present = True
    required_client_version = (0, 3, 5)
    web = KH1Web()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    def create_items(self):
        if self.options.reports_in_pool < self.options.required_reports:
            print("LESS REPORTS IN POOL THAN REQUIRED REPORTS, SWAPPING")
        
        item_pool: List[KH1Item] = []
        possible_level_up_item_pool = []
        level_up_item_pool = []

        # Fill pool with mandatory items
        for i in range(self.options.item_slot_increase):
            level_up_item_pool.append("Item Slot Increase")
        for i in range(self.options.accessory_slot_increase):
            level_up_item_pool.append("Accessory Slot Increase")

        # Create other pool
        for i in range(self.options.strength_increase):
            possible_level_up_item_pool.append("Strength Increase")
        for i in range(self.options.defense_increase):
            possible_level_up_item_pool.append("Defense Increase")
        for i in range(self.options.hp_increase):
            possible_level_up_item_pool.append("Max HP Increase")
        for i in range(self.options.mp_increase):
            possible_level_up_item_pool.append("Max MP Increase")
        for i in range(self.options.ap_increase):
            possible_level_up_item_pool.append("Max AP Increase")

        # Fill remaining pool with items from other pool
        while len(level_up_item_pool) < 100 and len(possible_level_up_item_pool) > 0:
            level_up_item_pool.append(possible_level_up_item_pool.pop(random.randrange(len(possible_level_up_item_pool))))

        level_up_locations = list(get_locations_by_category("Levels").keys())
        random.shuffle(level_up_item_pool)
        i = self.options.force_stats_on_levels - 1
        while len(level_up_item_pool) > 0 and i < self.options.level_checks:
            self.multiworld.get_location(level_up_locations[i], self.player).place_locked_item(self.create_item(level_up_item_pool.pop()))
            i = i + 1
        total_locations = len(self.multiworld.get_unfilled_locations(self.player)) - 1
        if self.options.goal.current_key == "super_boss_hunt":
            total_locations = total_locations - 5
        elif self.options.goal.current_key != "final_ansem" and self.options.require_final_ansem:
            total_locations = total_locations - 1
        non_filler_item_categories = ["Key", "Magic", "Worlds", "Trinities", "Cups", "Summons", "Abilities", "Shared Abilities", "Keyblades", "Accessory", "Weapons"]
        if self.options.puppies == "full":
            non_filler_item_categories.append("Puppies ALL")
        if self.options.puppies == "triplets":
            non_filler_item_categories.append("Puppies TRP")
        if self.options.puppies == "individual":
           non_filler_item_categories.append("Puppies IND")
        if self.options.atlantica:
            non_filler_item_categories.append("Atlantica")
        if self.options.hundred_acre_wood:
            non_filler_item_categories.append("HAW")
        for name, data in item_table.items():
            quantity = data.max_quantity

            # Ignore filler, it will be added in a later stage.
            if data.category not in non_filler_item_categories:
                continue
            item_pool += [self.create_item(name) for _ in range(0, quantity)]
        
        reports_in_pool = max(int(self.options.required_reports), int(self.options.reports_in_pool))
        if self.options.goal.current_key == "super_boss_hunt":
            i = 5
        elif self.options.require_final_ansem and self.options.goal.current_key != "final_ansem":
            i = 1
        else:
            i = 0
        while i < reports_in_pool:
            item_pool += [self.create_item("Ansem's Report " + str(i+1))]
            i = i + 1
        
        print("KH1: Item Pool = " + str(len(item_pool)))
        print("KH1: Locations = " + str(total_locations))
        print("KH1: Level Up Item Pool = " + str(len(level_up_item_pool)))
        print("KH1: Adding " + str(min(len(level_up_item_pool), total_locations - len(item_pool))) + " Stat Increases to the Item Pool")
        while len(item_pool) < total_locations and len(level_up_item_pool) > 0:
            item_pool += [self.create_item(level_up_item_pool.pop())]
        
        # Fill any empty locations with filler items.
        item_names = []
        attempts = 0  # If we ever try to add items 200 times, and all the items are used up, lets clear the item_names array, we probably don't have enough items
        while len(item_pool) < total_locations:
            item_name = self.get_filler_item_name()
            if item_name not in item_names:
                item_names.append(item_name)
                item_pool.append(self.create_item(item_name))
                attempts = 0
            elif attempts >= 200:
                item_names = []
                attempts = 0
            else:
                attempts = attempts + 1

        self.multiworld.itempool += item_pool

    def pre_fill(self) -> None:
        goal_dict = {
            "sephiroth":       ["Olympus Coliseum Defeat Sephiroth Ansem's Report 12"],
            "unknown":         ["Hollow Bastion Defeat Unknown Ansem's Report 13"],
            "postcards":       ["Traverse Town Mail Postcard 10 Event"],
            "final_ansem":     ["Final Ansem"],
            "puppies":         ["Traverse Town Piano Room Return 99 Puppies Reward 2"],
            "super_boss_hunt": ["Olympus Coliseum Defeat Sephiroth Ansem's Report 12"
                               , "Hollow Bastion Defeat Unknown Ansem's Report 13"
                               , "Agrabah Defeat Kurt Zisa Ansem's Report 11"
                               , "Neverland Defeat Phantom Stop Event"
                               , "Olympus Coliseum Defeat Ice Titan Diamond Dust Event"],
        }
        if (self.options.require_final_ansem or self.options.goal.current_key == "super_boss_hunt") and self.options.goal.current_key != "final_ansem":
            self.multiworld.get_location("Final Ansem", self.player).place_locked_item(self.create_item("Victory"))
            report_no = 1
            for location_name in goal_dict[self.options.goal.current_key]: 
                self.multiworld.get_location(location_name, self.player).place_locked_item(self.create_item("Ansem's Report " + str(report_no)))
                report_no = report_no + 1
        elif self.options.goal.current_key == "final_ansem":
            self.multiworld.get_location("Final Ansem", self.player).place_locked_item(self.create_item("Victory"))
        else:
            self.multiworld.get_location(goal_dict[self.options.goal.current_key][0], self.player).place_locked_item(self.create_item("Victory"))

    def get_filler_item_name(self) -> str:
        fillers = {}
        disclude = []
        fillers.update(get_items_by_category("Item", disclude))
        fillers.update(get_items_by_category("Camping", disclude))
        fillers.update(get_items_by_category("Stat Ups", disclude))
        weights = [data.weight for data in fillers.values()]
        return self.multiworld.random.choices([filler for filler in fillers.keys()], weights, k=1)[0]

    def fill_slot_data(self) -> dict:
        if self.options.goal.current_key == "super_boss_hunt":
            reports_in_pool = max(self.options.reports_in_pool, 5)
        else:
            reports_in_pool = self.options.reports_in_pool
        required_reports = min(int(self.options.required_reports), reports_in_pool)
        slot_data = {"EXP Multiplier": int(self.options.exp_multiplier)/16
                    ,"Required Reports": required_reports}
        if self.options.randomize_keyblade_stats:
            min_str_bonus = min(self.options.keyblade_min_str, self.options.keyblade_max_str)
            max_str_bonus = max(self.options.keyblade_min_str, self.options.keyblade_max_str)
            min_mp_bonus = min(self.options.keyblade_min_mp, self.options.keyblade_max_mp)
            max_mp_bonus = max(self.options.keyblade_min_mp, self.options.keyblade_max_mp)
            slot_data["Keyblade Stats"] = ""
            for i in range(22):
                if i < 4 and self.options.bad_starting_weapons:
                    slot_data["Keyblade Stats"] = slot_data["Keyblade Stats"] + "1,0,"
                else:
                    slot_data["Keyblade Stats"] = slot_data["Keyblade Stats"] + str(int(self.random.randrange(min_str_bonus,max_str_bonus))) + "," + str(int(self.random.randrange(min_mp_bonus,max_mp_bonus))) + ","
            slot_data["Keyblade Stats"] = slot_data["Keyblade Stats"][:-1]
        return slot_data
    
    def create_item(self, name: str) -> KH1Item:
        data = item_table[name]
        return KH1Item(name, data.classification, data.code, self.player)

    def create_event(self, name: str) -> KH1Item:
        data = event_item_table[name]
        return KH1Item(name, data.classification, data.code, self.player)

    def set_rules(self):
        if self.options.goal.current_key == "super_boss_hunt":
            reports_in_pool = max(self.options.reports_in_pool, 5)
        else:
            reports_in_pool = self.options.reports_in_pool
        set_rules(self.multiworld, self.player, self.options, min(self.options.required_reports, reports_in_pool))

    def create_regions(self):
        create_regions(self.multiworld, self.player, self.options)