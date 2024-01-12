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
    data_version = 4
    required_client_version = (0, 3, 5)
    web = KH1Web()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}

    def create_items(self):
        item_pool: List[KH1Item] = []
        possible_level_up_item_pool = []
        level_up_item_pool = []
        
        #Fill pool with mandatory items
        for i in range(self.options.item_slot_increase):
            level_up_item_pool.append("Item Slot Increase")
        for i in range(self.options.accessory_slot_increase):
            level_up_item_pool.append("Accessory Slot Increase")
        
        #Create other pool
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
        
        #Fill remaining pool with items from other pool
        while len(level_up_item_pool) < 100 and len(possible_level_up_item_pool) > 0:
            level_up_item_pool.append(possible_level_up_item_pool.pop(random.randrange(len(possible_level_up_item_pool))))
        
        level_up_locations = list(get_locations_by_category("Levels").keys())
        random.shuffle(level_up_item_pool)
        i = 0
        while i < len(level_up_item_pool):
            self.multiworld.get_location(level_up_locations[i], self.player).place_locked_item(self.create_item(level_up_item_pool[i]))
            i = i + 1
        match self.options.goal:
            case "sephiroth":
                self.multiworld.get_location("Ansem's Secret Report 12", self.player).place_locked_item(self.create_item("Victory"))
            case "deep_jungle":
                self.multiworld.get_location("Chronicles Deep Jungle", self.player).place_locked_item(self.create_item("Victory"))
            case "agrabah":
                self.multiworld.get_location("Chronicles Agrabah", self.player).place_locked_item(self.create_item("Victory"))
            case "agrabah":
                self.multiworld.get_location("Chronicles Monstro", self.player).place_locked_item(self.create_item("Victory"))
            case "atlantica":
                self.multiworld.get_location("Ansem's Secret Report 3", self.player).place_locked_item(self.create_item("Victory"))
            case "halloween_town":
                self.multiworld.get_location("Chronicles Halloween Town", self.player).place_locked_item(self.create_item("Victory"))
            case "neverland":
                self.multiworld.get_location("Ansem's Secret Report 9", self.player).place_locked_item(self.create_item("Victory"))
            case "unknown":
                self.multiworld.get_location("Ansem's Secret Report 13", self.player).place_locked_item(self.create_item("Victory"))
            case "final_rest":
                self.multiworld.get_location("End of the World Final Rest Chest", self.player).place_locked_item(self.create_item("Victory"))
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        non_filler_item_categories = ["Key", "Magic", "Worlds", "Trinities", "Cups", "Summons", "Abilities", "Shared Abilities", "Keyblades"]
        if self.options.atlantica or self.options.goal == "atlantica":
            non_filler_item_categories.append("Atlantica")
        for name, data in item_table.items():
            quantity = data.max_quantity
            
            # Ignore filler, it will be added in a later stage.
            if data.category not in non_filler_item_categories:
                continue
            item_pool += [self.create_item(name) for _ in range(0, quantity)]

        # Fill any empty locations with filler items.
        item_names = []
        attempts = 0 #If we ever try to add items 200 times, and all the items are used up, lets clear the item_names array, we probably don't have enough items
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

    def get_filler_item_name(self) -> str:
        fillers = {}
        disclude = []
        fillers.update(get_items_by_category("Item", disclude))
        fillers.update(get_items_by_category("Accessory", disclude))
        fillers.update(get_items_by_category("Weapons", disclude))
        fillers.update(get_items_by_category("Camping", disclude))
        fillers.update(get_items_by_category("Stat Ups", disclude))
        weights = [data.weight for data in fillers.values()]
        return self.multiworld.random.choices([filler for filler in fillers.keys()], weights, k=1)[0]
        
    def create_item(self, name: str) -> KH1Item:
        data = item_table[name]
        return KH1Item(name, data.classification, data.code, self.player)

    def create_event(self, name: str) -> KH1Item:
        data = event_item_table[name]
        return KH1Item(name, data.classification, data.code, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.player, self.options.goal, self.options.atlantica)

    def create_regions(self):
        create_regions(self.multiworld, self.player, self.options.goal, self.options.atlantica\
            , min((self.options.strength_increase + self.options.defense_increase + self.options.hp_increase + self.options.mp_increase\
            + self.options.ap_increase + self.options.accessory_slot_increase + self.options.item_slot_increase), 100))