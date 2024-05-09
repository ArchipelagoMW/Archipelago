import random

from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type, launch_subprocess
from .Options import DSTOptions, Goal
from . import Regions, Rules, ItemPool
from .Locations import location_name_to_id, location_data_table
from .Items import item_data_table, item_name_to_id, DSTItem

from BaseClasses import Region, Entrance, Item, Tutorial, ItemClassification, Location

def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="DontStarveTogetherClient")


components.append(Component("Don't Starve Together Client", "DontStarveTogetherClient", func=launch_client, 
                            component_type=Type.CLIENT))

class DSTWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up the Archipelago Don't Starve Together game.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Dragon Wolf Leo"]
    )]

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
    web = DSTWeb()

    item_name_groups = {"all": set(item_data_table.keys())}

    dst_itempool: ItemPool.DSTItemPool

    def generate_early(self):
        self.dst_itempool = ItemPool.DSTItemPool()
        if self.options.goal.value == Goal.option_bosses_any or self.options.goal.value == Goal.option_bosses_all:
            if not len(self.options.required_bosses.value):
                # You didn't choose a boss... Selecting one at random!
                self.options.required_bosses.value.add(random.choice(self.options.required_bosses.valid_keys))
        self.dst_itempool.decide_itempools(self)

    def create_item(self, name: str) -> Item:
        return DSTItem(
            name, 
            item_data_table[name].type if name in item_name_to_id else ItemClassification.progression, 
            item_data_table[name].code if name in item_name_to_id else None, 
            self.player
        )
    
    def create_items(self) -> None:
        self.dst_itempool.create_items(self)
    
    def get_filler_item_name(self) -> str:
        return self.dst_itempool.get_filler_item_name(self)

    def create_regions(self):
        Regions.create_regions(self.multiworld, self.player, self.options, self.dst_itempool)

    set_rules = Rules.set_rules

    def fill_slot_data(self):
        slot_data = {
            "death_link": bool(self.options.death_link.value),
            "goal": self.options.goal.current_key,
            # "craft_with_locked_items": self.options.craft_with_locked_items.value,
            "locked_items_local_id": list(self.dst_itempool.locked_items_local_id),
        }
        if slot_data["goal"] == "survival":
            slot_data["days_to_survive"] = self.options.days_to_survive.value
        else:
            slot_data["goal_locations"] = [location_name_to_id[loc_name] for loc_name in self.options.required_bosses.value]
        return slot_data