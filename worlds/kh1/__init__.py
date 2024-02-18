from typing import List

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import KH1Item, KH1ItemData, event_item_table, get_items_by_category, item_table
from .Locations import KH1Location, location_table, get_locations_by_category
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
        i = 0
        while i < len(level_up_item_pool):
            self.multiworld.get_location(level_up_locations[i], self.player).place_locked_item(self.create_item(level_up_item_pool[i]))
            i = i + 1

        total_locations = len(self.multiworld.get_unfilled_locations(self.player)) - 1  # for victory placement
        non_filler_item_categories = ["Key", "Magic", "Worlds", "Trinities", "Cups", "Summons", "Abilities", "Shared Abilities", "Keyblades", "Accessory", "Weapons"]
        if self.options.atlantica or self.options.goal == "atlantica":
            non_filler_item_categories.append("Atlantica")
        for name, data in item_table.items():
            quantity = data.max_quantity

            # Ignore filler, it will be added in a later stage.
            if data.category not in non_filler_item_categories:
                continue
            item_pool += [self.create_item(name) for _ in range(0, quantity)]
        
        for i in range(max(self.options.required_reports, self.options.reports_in_pool)):
            item_pool += [self.create_item("Ansem's Report " + str(i+1))]

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
            "sephiroth":      "Ansem's Report 12",
            "wonderland":     "Wonderland Ifrit's Horn Event",
            "deep_jungle":    "Deep Jungle Jungle King Event",
            "agrabah":        "Agrabah Genie Event",
            "monstro":        "Monstro Stop Event",
            "atlantica":      "Atlantica Crabclaw Event",
            "halloween_town": "Halloween Town Pumpkinhead Event",
            "neverland":      "Neverland Fairy Harp Event",
            "unknown":        "Ansem's Report 13",
            "final_rest":     "End of the World Final Rest Chest",
            "postcards":      "Traverse Town Mail Postcard 10 Event",
            "final_ansem":    "Final Ansem"
        }
        self.multiworld.get_location(goal_dict[self.options.goal.current_key], self.player).place_locked_item(self.create_item("Victory"))

    def get_filler_item_name(self) -> str:
        fillers = {}
        disclude = []
        fillers.update(get_items_by_category("Item", disclude))
        fillers.update(get_items_by_category("Camping", disclude))
        fillers.update(get_items_by_category("Stat Ups", disclude))
        weights = [data.weight for data in fillers.values()]
        return self.multiworld.random.choices([filler for filler in fillers.keys()], weights, k=1)[0]

    def fill_slot_data(self) -> dict:
        slot_data = {"EXP Multiplier": int(self.options.exp_multiplier)/16
                    ,"Required Reports": min(int(self.options.required_reports), int(self.options.reports_in_pool))}
        if self.options.randomize_keyblade_stats:
            min_str_bonus = min(self.options.keyblade_min_str, self.options.keyblade_max_str)
            max_str_bonus = max(self.options.keyblade_min_str, self.options.keyblade_max_str)
            min_mp_bonus = min(self.options.keyblade_min_mp, self.options.keyblade_max_mp)
            max_mp_bonus = max(self.options.keyblade_min_mp, self.options.keyblade_max_mp)
            slot_data["Keyblade Stats"] = ""
            for i in range(22):
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
        set_rules(self.multiworld, self.player, self.options.goal, self.options.atlantica, min(self.options.required_reports, self.options.reports_in_pool))

    def create_regions(self):
        create_regions(self.multiworld, self.player, self.options.goal, self.options.atlantica \
                , min((self.options.strength_increase + self.options.defense_increase + self.options.hp_increase + self.options.mp_increase \
                       + self.options.ap_increase + self.options.accessory_slot_increase + self.options.item_slot_increase), 100))