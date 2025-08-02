import gc
from typing import Any, Dict

from BaseClasses import ItemClassification, Location, Tutorial, Item, Region, MultiWorld
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type, launch_subprocess

from .Options import GaribLogic, GloverOptions, SpawningCheckpointRandomizer
from .JsonReader import JsonInfo, build_data, generate_location_name_to_id
from .ItemPool import generate_item_name_to_id, generate_item_name_groups, find_item_data, world_garib_table, decoupled_garib_table, garibsanity_world_table, checkpoint_table, level_event_table, ability_table

spawn_checkpoint = [
    2,3,3,
    4,5,4,
    3,3,4,
    3,4,4,
    3,3,5,
    2,1,4]

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
    Glover is an N64 physics puzzle platforming game.
    """
    game : str = "Glover"
    version : str = "V0.1"
    web = GloverWeb()
    topology_present = True
    
    options_dataclass = GloverOptions
    options : GloverOptions

    #Check/Item Prefixes
    world_prefixes = ["Atl", "Crn", "Prt", "Pht", "FoF", "Otw"]
    level_prefixes = ["H", "1", "2", "3", "!", "?"]

    item_name_to_id = generate_item_name_to_id()
    item_name_groups = generate_item_name_groups()
    location_name_to_id = generate_location_name_to_id(world_prefixes, level_prefixes)

    def __init__(self, world, player):
        self.version = "V0.1"
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
            return self.world_prefixes.index(name[:3])
        if name.startswith("Hubworld") or name.startswith("Castle Cave") or name.startswith("Training"):
            return 6
        return -1

    def generate_early(self):
        #Garib Sorting Order
        if self.options.garib_sorting == GaribLogic.option_garibsanity:
            self.random.shuffle(garib_level_order)
        #Setup the spawning checkpoints
        if self.options.spawning_checkpoint_randomizer:
            #If randomized, pick a number from it's assigned value to the current value
            for each_inxex, each_item in enumerate(spawn_checkpoint):
                spawn_checkpoint[each_item] = self.random.randint(1, each_inxex)
        else:
            #By default, they're all Checkpoint 1
            for each_item in range(len(spawn_checkpoint)):
                spawn_checkpoint[each_item] = 1

    def create_regions(self):
        multiworld = self.multiworld
        player = self.player
        build_data(self, spawn_checkpoint)
        multiworld.regions.append(Region("Menu", player, multiworld))
        #Replace with a connection to the hubworld rather than Atlantis
        multiworld.get_region("Menu", player).connect(multiworld.get_region("Atl1", player))

    def create_item(self, name) -> Item:
        item_classification = None
        item_id = -1
        #knownLevelAndWorld = [self.level_from_string(self, name), self.world_from_string(self, name)]
        item_data = find_item_data(name)
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
                if self.options.bonus_levels == 1 or self.options.difficulty_logic.value > 0:
                    item_classification = ItemClassification.progression_deprioritized
                else:
                    item_classification = ItemClassification.filler
        name_for_use = name
        if name == "Garibsanity":
            name_for_use = "Garib"
        item_output = GloverItem(name_for_use, item_classification, item_id, self.player)
        return item_output

    def create_items(self) -> None:
        #Garib Logic
        garib_items = []
        match self.options.garib_logic.value:
            #0: Level Garibs (No items to be sent)
            #Garib Groups
            case 1:
                if self.options.garib_sorting.value == 0:
                    garib_items = list(world_garib_table.keys())
                else:
                    garib_items = list(decoupled_garib_table.keys())
            #Individual Garibs
            case 2:
                if self.options.garib_logic.value == 0:
                    garib_items = list(garibsanity_world_table.keys())
                else:
                    garib_items = ["Garibsanity"]
        
        #Checkpoint Logic
        checkpoint_items = []
        if self.options.checkpoint_checks.value == 1:
            for each_checkpoint in checkpoint_table:
                level_offset = self.level_from_string(each_checkpoint)
                world_offset = self.world_from_string(each_checkpoint)
                if spawn_checkpoint[level_offset + (world_offset * 3)] != int(each_checkpoint[-1]):
                    checkpoint_items.append[each_checkpoint]

        #Level Event Logic
        event_items = []
        if self.options.switches_checks.value == 1:
            event_items = list(level_event_table.keys())

        #Abilities
        ability_items = list(ability_table.keys())
        if not self.options.include_power_ball.value == 1:
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

    def connect_entrances(self):
        #Level portal randomization
        return super().connect_entrances()

    def fill_slot_data(self) -> Dict[str, Any]:
        options = {}
        options["difficulty_logic"] = self.options.difficulty_logic.value
        options["death_link"] = self.options.death_link.value
        options["tag_link"] = self.options.tag_link.value
        options["starting_ball"] = self.options.starting_ball.value
        options["garib_logic"] = self.options.garib_logic.value
        options["garib_sorting"] = self.options.garib_sorting.value
        options["entrance_randomizer"] = self.options.entrance_randomizer.value
        options["spawning_checkpoint_randomizer"] = self.options.spawning_checkpoint_randomizer.value
        options["bonus_levels"] = self.options.bonus_levels.value
        #options["atlantis_bonus"] = self.options.atlantis_bonus.value
        options["death_link"] = self.options.death_link.value
        options["tag_link"] = self.options.tag_link.value
        options["randomize_jump"] = self.options.randomize_jump.value
        options["include_power_ball"] = self.options.include_power_ball.value
        options["checkpoint_checks"] = self.options.checkpoint_checks.value
        options["switches_checks"] = self.options.switches_checks.value
        options["mr_tip_checks"] = self.options.mr_tip_checks.value
        options["mr_hints"] = self.options.mr_hints.value
        options["chicken_hints"] = self.options.chicken_hints.value

        options["player_name"] = self.multiworld.player_name[self.player]
        options["seed"] = self.random.randint(-6500000, 6500000)
        options["version"] = self.version
        reffers = gc.get_referrers(self.multiworld)
        print(reffers)
        
        return options
