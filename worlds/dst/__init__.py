from typing import Dict, Set

from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type, launch_subprocess
from BaseClasses import ItemClassification
from .Options import DSTOptions
from . import Regions, Rules, ItemPool, Constants
from .Locations import location_data_table, location_name_to_id
from .Items import item_data_table, item_name_to_id, DSTItem

from BaseClasses import Item, Tutorial

def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="DontStarveTogetherClient")


components.append(Component("Don't Starve Together Client", func=launch_client, 
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
        _IS_BOSS_GOAL = self.options.goal.value == self.options.goal.option_bosses_any or self.options.goal.value == self.options.goal.option_bosses_all

        # Warn shuffling starting recipes with creature locations disabled and nothing in start inventory
        if self.options.shuffle_starting_recipes.value and not self.options.creature_locations.value and not len(self.options.start_inventory):
            print(f"{self.multiworld.get_player_name(self.player)} (Don't Starve Together): Warning! Shuffle Starting Recipes without Creature Locations. "\
                "Player will potentially have no reachable checks in Sphere 1!"
            )
        
        # Get regions bosses are in
        _regions = set()
        if _IS_BOSS_GOAL:
            for bossname in self.options.required_bosses.value:
                _regions.add(Constants.BOSS_REGIONS.get(bossname,""))

        # Set auto regions
        if self.options.cave_regions.value == self.options.cave_regions.option_auto:
            self.options.cave_regions.value = self.options.cave_regions.option_none
            if _IS_BOSS_GOAL:
                if "ruins" in _regions:
                    self.options.cave_regions.value = self.options.cave_regions.option_full
                elif "cave" in _regions:
                    self.options.cave_regions.value = self.options.cave_regions.option_light
        
        if self.options.ocean_regions.value == self.options.ocean_regions.option_auto:
            self.options.ocean_regions.value = self.options.ocean_regions.option_none
            if _IS_BOSS_GOAL:
                if "moonstorm" in _regions:
                    self.options.ocean_regions.value = self.options.ocean_regions.option_full
                elif "ocean" in _regions:
                    self.options.ocean_regions.value = self.options.ocean_regions.option_light

        # Auto set logic options
        ADVANCED_PLAYER_BIAS = self.options.skill_level.current_key != "easy"
        EXPERT_PLAYER_BIAS = self.options.skill_level.current_key == "expert"
        if self.options.lighting_logic.current_key == "auto":
            self.options.lighting_logic.value = 0 if EXPERT_PLAYER_BIAS else 2
        if self.options.weapon_logic.current_key == "auto":
            self.options.weapon_logic.value = 0 if EXPERT_PLAYER_BIAS else 2
        if self.options.season_gear_logic.current_key == "auto":
            self.options.season_gear_logic.value = 0 if ADVANCED_PLAYER_BIAS else 2
        if self.options.base_making_logic.current_key == "auto":
            self.options.base_making_logic.value = 0 if EXPERT_PLAYER_BIAS else 2
        if self.options.backpack_logic.current_key == "auto":
            self.options.backpack_logic.value = 0 if EXPERT_PLAYER_BIAS else 2
        if self.options.healing_logic.current_key == "auto":
            self.options.healing_logic.value = 0 if ADVANCED_PLAYER_BIAS else 2

        # Create itempools
        self.dst_itempool.decide_itempools(self)

    def create_item(self, name: str) -> Item:
        itemtype = (
            ItemClassification.progression if self.dst_itempool and name in self.dst_itempool.progression_items
            else item_data_table[name].type if name in item_name_to_id 
            else ItemClassification.progression
        )
        return DSTItem(
            name, 
            itemtype, 
            item_data_table[name].code if name in item_name_to_id else None, 
            self.player
        )
    
    def create_items(self) -> None:
        self.dst_itempool.create_items(self)
    
    def get_filler_item_name(self) -> str:
        return self.dst_itempool.get_filler_item_name(self)

    def create_regions(self):
        Regions.create_regions(self.multiworld, self.player, self.options, self.dst_itempool)
        Rules.set_rules(self, self.dst_itempool) # create_items needs rules set first

    def set_rules(self) -> None:
        pass

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        # Add crafting stations to hint information
        def get_station_from_tags(tags: Set[str]) -> str:
            return (
                "Science Machine" if "science" in tags and "tier_1" in tags
                else "Alchemy Engine" if "science" in tags and "tier_2" in tags
                else "Prestihatitor" if "magic" in tags and "tier_1" in tags
                else "Shadow Manipulator" if "magic" in tags and "tier_2" in tags
                else "Think Tank" if "seafaring" in tags
                else "Celestial Orb" if "celestial" in tags and "tier_1" in tags
                else "Celestial Altar" if "celestial" in tags and "tier_2" in tags
                else "Broken Pseudoscience Station" if "ancient" in tags and "tier_1" in tags
                else "Ancient Pseudoscience Station" if "ancient" in tags and "tier_2" in tags
                else "Crabby Hermit" if "hermitcrab" in tags
                else "Vanilla"
            )
        hint_information:Dict[int, str] = {}
        for data in location_data_table.values():
            if "research" in data.tags:
                hint_information[data.address] = get_station_from_tags(data.tags)
            elif "cooking" in data.tags:
                hint_information[data.address] = "Portable Crock Pot" if "warly" in data.tags else "Crock Pot"
        hint_data[self.player] = hint_information

    def fill_slot_data(self):
        slot_data = {
            "generator_version": Constants.VERSION,
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