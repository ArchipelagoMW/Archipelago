from typing import List
import random

from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type, launch_subprocess
# from worlds.generic import Rules
from worlds.generic.Rules import add_rule, set_rule, forbid_item, add_item_rule
from .Options import DSTOptions, Goal
from . import Constants, Regions, Rules
from .Locations import location_name_to_id, location_data_table
from .Items import item_data_table, item_name_to_id, DSTItem

from BaseClasses import Region, Entrance, Item, Tutorial, ItemClassification, Location

def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="DontStarveTogetherClient")


components.append(Component("Don't Starve Together Client", "DontStarveTogetherClient", func=launch_client, 
                            component_type=Type.CLIENT))

class DSTWorld(World):
    """
    Don't Starve Together is a game where you are thrown into a strange and unexplored world full of odd creatures, 
    hidden dangers, and ancient secrets known as "The Constant". You must gather resources to craft items and build 
    strucutres and farms to help you protect yourself, survive, and most importantly, not starve.
    """
    game = "Don't Starve Together"

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    options_dataclass = DSTOptions  # assign the options dataclass to the world
    options: DSTOptions  # typing for option results
    topology_present = False
    # web = DSTWeb()

    item_name_groups = {"all": set(item_data_table.keys())}

    def generate_early(self):
        if self.options.goal.value == Goal.option_bosses_any or self.options.goal.value == Goal.option_bosses_all:
            if not len(self.options.required_bosses.value):
                # You didn't choose a boss... Selecting one at random!
                self.options.required_bosses.value.add(random.choice(self.options.required_bosses.valid_keys))

    filler_pool: List[str] = []
    trap_pool: List[str] = []
    seasontrap_pool: List[str] = []

    def create_item(self, name: str) -> Item:
        return DSTItem(
            name, 
            item_data_table[name].type if name in item_name_to_id else ItemClassification.progression, 
            item_data_table[name].code if name in item_name_to_id else None, 
            self.player
        )
    
    def create_items(self) -> None:
        item_pool: List[DSTItem] = []

        for name, item in item_data_table.items():
            if item.code:
                if "junk" in item.tags:
                    self.filler_pool.append(name)
                elif "trap" in item.tags:
                    (self.seasontrap_pool if "seasontrap" in item.tags else self.trap_pool).append(name)
                else:
                    item_pool.append(self.create_item(name))
        
        # Fill up with filler items
        while len(item_pool) < len(self.multiworld.get_unfilled_locations(self.player)):
            item_pool.append(self.create_item(self.get_filler_item_name()))

        self.multiworld.itempool += item_pool
    
    def get_filler_item_name(self) -> str:
        WEIGHTS = {
            "none": 0.0,
            "low": 0.2,
            "medium": 0.5,
            "high": 0.8,
        }
        # Decide if we get a trap, and choose the one with the highest number
        regulartrap_roll = WEIGHTS[self.options.trap_items.current_key] - random.random()
        seasontrap_roll = WEIGHTS[self.options.season_trap_items.current_key] - random.random()
        target_pool = self.filler_pool if max(regulartrap_roll, seasontrap_roll) < 0.0 else self.trap_pool if regulartrap_roll > seasontrap_roll else self.seasontrap_pool
        if len(target_pool) > 0:
            return random.choice(target_pool)
        return "20 Health"

    def create_regions(self):
        Regions.create_regions(self.multiworld, self.player, self.options)


    set_rules = Rules.set_rules

    def fill_slot_data(self):
        slot_data = {
            "death_link": bool(self.multiworld.death_link[self.player].value),
            "goal": self.multiworld.goal[self.player].current_key,
            "days_to_survive": self.multiworld.days_to_survive[self.player].value,
            "required_bosses": self.multiworld.required_bosses[self.player].value,
        }
        return slot_data