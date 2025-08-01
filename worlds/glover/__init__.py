from typing import Any, Dict

from BaseClasses import ItemClassification, Location, Tutorial, Item, Region, MultiWorld
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type, launch_subprocess
import random

from .Options import GloverOptions
from worlds.glover import ItemPool, JsonReader

class GloverItem(Item):
	#Start at 650000
	game: str = "Glover"

class GloverLocation(Location):
    game : str = "Glover"

class GloverWeb(WebWorld):
    englishTut = Tutorial("",
                     """A guide for setting up Archipelago Glover on your computer.""",
                     "English",
                     "setup_en.md",
                     "setup/en",
                     ["Smg065"])
    tutorials = [englishTut]

class GloverWorld(World):
    """
    Glover is an N64 physics puzzle platformeing game.
    """
    game : str = "Glover"
    version : str = "V0.1"
    web = GloverWeb()
    topology_present = True
    options : GloverOptions
    all_items_table : ItemPool
    json_info : JsonReader.JsonInfo
    options_dataclass = Options.GloverOptions
    item_name_to_id = ItemPool.generate_item_name_to_id()
    item_name_groups = ItemPool.generate_item_name_groups()
    location_name_to_id = JsonReader.generate_location_name_to_id()

    spawn_checkpoint = [
        2,3,3,
        4,5,4,
        3,3,4,
        3,4,4,
        3,3,5,
        2,1,4]
    
    #Check/Item Prefixes
    world_prefixes = ["Atl", "Crn", "Prt", "Pht", "FoF", "Otw"]
    level_prefixes = ["H", "1", "2", "3", "!", "?"]

    def __init__(self, world, player):
        self.version = "V0.1"
        
        #Garib level order table
        garib_level_order = [
            ["Atl1", 50]#,
            #["Atl2", 60],
            #["Atl3", 80],
            #["Atl?", 25],
            #["Crn1", 65],
            #["Crn2", 80],
            #["Crn3", 80],
            #["Crn?", 20],
            #["Prt1", 70],
            #["Prt2", 60],
            #["Prt3", 80],
            #["Prt?", 50],
            #["Pht1", 80],
            #["Pht2", 80],
            #["Pht3", 80],
            #["Pht?", 60],
            #["FoF1", 60],
            #["FoF2", 60],
            #["FoF3", 70],
            #["FoF?", 56],
            #["Otw1", 50],
            #["Otw2", 50],
            #["Otw3", 80],
            #["Otw?", 50]
        ]

        if self.options.garib_sorting == 2:
            random.shuffle(garib_level_order)
        
        super(GloverWorld, self).__init__(world, player)

    def level_from_string(self, name : str) -> int:
        if name[3:4] in self.level_prefixes:
            return self.level_prefixes.index(name[3:4])
        if name.startswith("Hubworld"):
            return 0
        if name.startswith("Castle Cave"):
            return 1
        if name.startswith("Training"):
            return 2
        return -1

    def world_from_string(self, name : str) -> int:
        if name[:3] in self.world_prefixes:
            return self.level_prefixes.index(name[:3])
        if name.startswith("Hubworld") or name.startswith("Castle Cave") or name.startswith("Training"):
            return 6
        return -1

    def generate_early(self):
        #Setup the spawning checkpoints
        if self.options.spawning_checkpoint_randomizer:
            #If randomized, pick a number from it's assigned value to the current value
            for each_item in self.spawn_checkpoint.count():
                self.spawn_checkpoint[each_item] = random.randint(1, self.spawn_checkpoint[each_item])
        else:
            #By default, they're all Checkpoint 1
            for each_item in self.spawn_checkpoint.count():
                self.spawn_checkpoint[each_item] = 1
        self.json_info = JsonReader.build_data(self)

    def create_regions(self):
        main_menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(main_menu)
        for each_level in self.json_info.all_levels:
            for each_region_pair in each_level.map_regions:
                each_region_pair.ball_region_methods

    def create_item(self, name) -> Item:
        item_classification = None
        item_id = -1
        knownLevelAndWorld = [self.level_from_string(self, name), self.world_from_string(self, name)]
        item_data = ItemPool.find_item_data(name)
        item_id = item_data.glid
        match item_data.type:
            case "Progression":
                item_classification = ItemClassification.progression
            case "Useful":
                item_classification = ItemClassification.useful
            case "Filler":
                item_classification = ItemClassification.filler
            case "Trap":
                item_classification = ItemClassification.trap
            case "Garib":
                if self.options.bonus_levels or self.options.difficulty_logic > 0:
                    item_classification = ItemClassification.progression_deprioritized
                else:
                    item_classification = ItemClassification.filler
        name_for_use = name
        if name == "Garibsanity":
            name_for_use = "Garib"
        item_output = ItemPool.GloverItem(name_for_use, item_classification, item_id, self.player)
        return item_output

    def create_items(self) -> None:
        #Garib Logic
        garib_items = []
        match self.options.garib_logic:
            #0: Level Garibs (No items to be sent)
            #Garib Groups
            case 1:
                if self.options.garib_sorting == 0:
                    garib_items = list(self.all_items_table.world_garib_table.keys())
                else:
                    garib_items = list(self.all_items_table.decoupled_garib_table.keys())
            #Individual Garibs
            case 2:
                if self.options.garib_logic == 0:
                    garib_items = list(self.all_items_table.garibsanity_world_table.keys())
                else:
                    garib_items = ["Garibsanity"]
        
        #Checkpoint Logic
        checkpoint_items = []
        if self.options.checkpoint_checks:
            for each_checkpoint in self.all_items_table.checkpoint_table:
                level_offset = self.level_from_string(each_checkpoint)
                world_offset = self.world_from_string(each_checkpoint)
                if self.spawn_checkpoint[level_offset + (world_offset * 3)] != int(each_checkpoint[-1]):
                    checkpoint_items.append[each_checkpoint]

        #Level Event Logic
        event_items = []
        if self.options.switches_checks:
            event_items = list(self.all_items_table.level_event_table.keys())

        #Abilities
        ability_items = list(self.all_items_table.ability_table.keys())
        if not self.options.include_power_ball:
            ability_items.remove("Power Ball")
        
        #Apply all core items
        all_core_items = []
        all_core_items.extend(garib_items)
        all_core_items.extend(checkpoint_items)
        all_core_items.extend(event_items)
        all_core_items.extend(ability_items)
        for each_item in garib_items:
            self.create_item(each_item)
        for each_item in checkpoint_items:
            self.create_item(each_item)
        for each_item in event_items:
            self.create_item(each_item)
        for each_item in ability_items:
            self.create_item(each_item)

    def set_rules(self):
        #MethodData to actual method logic
        return super().set_rules()

    def connect_entrances(self):
        #Level portal randomization
        return super().connect_entrances()

    def fill_slot_data(self) -> Dict[str, Any]:
        options = self.options.as_dict(
            "death_link",
            "tag_link",
            "difficuilty_logic",
            "starting_ball",
            "garib_logic",
            "garib_sorting",
            "entrance_randomizer",
            "spawning_checkingpoint_randomizer",
            "bonus_levels",
            "atlantis_bonus",
            "death_link",
            "tag_link",
            "randomize_jump",
            "include_power_ball",
            "checkpoint_checks",
            "switches_checks",
            "mr_tip_checks",
            "mr_hints",
            "chicken_hints"
            )
        options["player_name"] = self.multiworld.player_name[self.player]
        options["seed"] = self.random.randint()
        options["version"] = self.version
        return options