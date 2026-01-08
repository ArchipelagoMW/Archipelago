from typing import List
from .Items import item_table, pickup_item_table, trap_item_table, GungeonItem
from .Locations import location_table, GungeonLocation
from .Options import GungeonOptions, gungeon_option_groups, gungeon_options_presets
from .Rules import set_rules
from .Regions import create_regions
from BaseClasses import Item, ItemClassification, MultiWorld, Tutorial
from ..AutoWorld import World, WebWorld

client_version = 1

class GungeonWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Enter The Gungeon for Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["KinTheInfinite"]
    )]

    option_groups = gungeon_option_groups
    options_presets = gungeon_options_presets


class GungeonWorld(World):
     
    """ Enter the Gungeon is a bullet hell dungeon crawler following a band of misfits seeking to 
     shoot, loot, dodge roll and table-flip their way to personal absolution by reaching the 
     legendary Gungeon’s ultimate treasure: the gun that can kill the past.
    """ #Lifted from Store Page

    game: str = "Enter The Gungeon"
    topology_present = False
    web = GungeonWeb()

    item_name_to_id = item_table
    location_name_to_id = location_table

    options_dataclass = GungeonOptions
    options: GungeonOptions

    def create_regions(self):
        create_regions(self.multiworld, self.options, self.player)
        self.place_events()

    def fill_slot_data(self):
        return {
            "Goal": self.options.goal.value,
            "Blobulord Goal": int(self.options.additional_goals.__contains__("Blobulord")),
            "Old King Goal": int(self.options.additional_goals.__contains__("Old King")),
            "Resourceful Rat Goal": int(self.options.additional_goals.__contains__("Resourceful Rat")),
            "Agunim Goal": int(self.options.additional_goals.__contains__("Agunim")),
            "Advanced Dragun Goal": int(self.options.additional_goals.__contains__("Advanced Dragun")),
            "DeathLink": self.options.death_link.value,
        }

    def set_rules(self):
        self.area_connections = {}
        self.area_cost_map = {}
        set_rules(self.multiworld, self.options, self.player, self.area_connections, self.area_cost_map)

    def create_item(self, name: str) -> Item:
        return GungeonItem(name, ItemClassification.filler, item_table[name], self.player)
    
    def create_item_progression(self, name: str) -> Item:
        return GungeonItem(name, ItemClassification.progression, item_table[name], self.player)
    
    def create_event(self, name: str) -> GungeonItem:
        return GungeonItem(name, ItemClassification.progression, None, self.player)

    def create_items(self):
        item_pool: List[GungeonItem] = []
        for name, data in item_table.items():
            quantity = 0
            match name:
                case "Random D Tier Gun":
                    quantity = self.options.random_gun_tier_d.value
                case "Random C Tier Gun":
                    quantity = self.options.random_gun_tier_c.value
                case "Random B Tier Gun":
                    quantity = self.options.random_gun_tier_b.value
                case "Random A Tier Gun":
                    quantity = self.options.random_gun_tier_a.value
                case "Random S Tier Gun":
                    quantity = self.options.random_gun_tier_s.value
                case "Random D Tier Item":
                    quantity = self.options.random_item_tier_d.value
                case "Random C Tier Item":
                    quantity = self.options.random_item_tier_c.value
                case "Random B Tier Item":
                    quantity = self.options.random_item_tier_b.value
                case "Random A Tier Item":
                    quantity = self.options.random_item_tier_a.value
                case "Random S Tier Item":
                    quantity = self.options.random_item_tier_s.value
                case "Gnawed Key":
                    item_pool.append(self.create_item_progression(name))
                case "Old Crest":
                    item_pool.append(self.create_item_progression(name))
                case "Weird Egg":
                    item_pool.append(self.create_item_progression(name))

            if quantity == 0:
                continue

            item_pool += [self.create_item(name) for i in range(0, quantity)]

        for i in range(0, self.options.pickup_amount.value):
            item_pool.append(self.create_item(list(pickup_item_table)[i % len(pickup_item_table)]))

        for i in range(0, self.options.trap_amount.value):
            item_pool.append(self.create_item(list(trap_item_table)[i % len(trap_item_table)]))

        self.multiworld.itempool += item_pool

    def place_events(self):
        self.multiworld.get_location("Blobulord", self.player).place_locked_item(
            self.create_event("Defeat Blobulord"))

        self.multiworld.get_location("The Old King", self.player).place_locked_item(
            self.create_event("Defeat The Old King"))
        
        self.multiworld.get_location("The Resourceful Rat", self.player).place_locked_item(
            self.create_event("Defeat The Resourceful Rat"))
        
        self.multiworld.get_location("Agunim", self.player).place_locked_item(
            self.create_event("Defeat Agunim"))
        
        self.multiworld.get_location("The Advanced Dragun", self.player).place_locked_item(
            self.create_event("Defeat The Advanced Dragun"))
        
        self.multiworld.get_location("The High Dragun", self.player).place_locked_item(
            self.create_event("Defeat The High Dragun"))
        
        self.multiworld.get_location("The Lich", self.player).place_locked_item(
            self.create_event("Defeat The Lich"))
