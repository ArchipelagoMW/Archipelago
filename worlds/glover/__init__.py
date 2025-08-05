import gc
import math
from typing import Any, Dict

from BaseClasses import ItemClassification, Location, Tutorial, Item, Region
import settings
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type, launch_subprocess

from .Options import GaribLogic, GloverOptions, GaribSorting, StartingBall
from .JsonReader import build_data, generate_location_name_to_id
from .ItemPool import generate_item_name_to_id, generate_item_name_groups, find_item_data, world_garib_table, decoupled_garib_table, garibsanity_world_table, checkpoint_table, level_event_table, ability_table, filler_table, trap_table
from Utils import visualize_regions

def run_client():
    from .GloverClient import main  # lazy import
    launch_subprocess(main)

components.append(Component("Glover Client", func=run_client, component_type=Type.CLIENT))

class GloverSettings(settings.Group):

  class RomPath(settings.OptionalUserFilePath):
    """File path of the Glover (USA) ROM."""

  class PatchPath(settings.OptionalUserFolderPath):
    """Folder path of where to save the patched ROM."""

  class ProgramPath(settings.OptionalUserFilePath):
    """
      File path of the program to automatically run.
      Leave blank to disable.
    """

  class ProgramArgs(str):
    """
      Arguments to pass to the automatically run program.
      Leave blank to disable.
      Set to "--lua=" to automatically use the correct path for the lua connector.
    """

  rom_path: RomPath | str = ""
  patch_path: PatchPath | str = ""
  program_path: ProgramPath | str = ""
  program_args: ProgramArgs | str = "--lua="

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
    settings: GloverSettings
    settings_key = "glover_options"
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
        self.spawn_checkpoint = [
            2,3,3,
            4,5,4,
            3,3,4,
            3,4,4,
            3,3,5,
            2,1,4]
        #Garib level order table
        self.garib_level_order = [
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
        self.starting_ball : str = "Rubber Ball"
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
            self.random.shuffle(self.garib_level_order)
        #Setup the spawning checkpoints
        if self.options.spawning_checkpoint_randomizer:
            #If randomized, pick a number from it's assigned value to the current value
            for each_index, each_item in enumerate(self.spawn_checkpoint):
                self.spawn_checkpoint[each_index] = self.random.randint(1, each_item)
        else:
            #By default, they're all Checkpoint 1
            for each_item in range(len(self.spawn_checkpoint)):
                self.spawn_checkpoint[each_item] = 1
        #Set the starting ball
        match self.options.starting_ball:
            case StartingBall.option_rubber_ball:
                self.starting_ball = "Rubber Ball"
            case StartingBall.option_bowling_ball:
                self.starting_ball = "Bowling Ball"
            case StartingBall.option_ball_bearing:
                self.starting_ball = "Ball Bearing"
            case StartingBall.option_crystal_ball:
                self.starting_ball = "Crystal"
            case StartingBall.option_power_ball:
                self.starting_ball = "Power Ball"
            case StartingBall.option_random_no_power_ball:
                ball_options = ["Rubber Ball",
	            "Bowling Ball",
	            "Ball Bearing",
	            "Crystal",
	            "Power Ball"]
                self.starting_ball = self.random.choice(ball_options)
            case StartingBall.option_random_any:
                ball_options = ["Rubber Ball",
	            "Bowling Ball",
	            "Ball Bearing",
	            "Crystal"]
                self.starting_ball = self.random.choice(ball_options)
        self.multiworld.push_precollected(self.create_item(self.starting_ball))
        if not self.options.randomize_jump:
            self.multiworld.push_precollected(self.create_item("Jump"))

    def create_regions(self):
        multiworld = self.multiworld
        player = self.player
        build_data(self)
        multiworld.regions.append(Region("Menu", player, multiworld))
        #Replace with a connection to the hubworld rather than Atlantis
        multiworld.get_region("Menu", player).connect(multiworld.get_region("Atl1", player))
        end_region : Region = multiworld.get_region("Atl1: End", player)
        goal_location : Location = Location(player, "Ending", None, end_region)
        end_region.locations.append(goal_location)
        goal_location.place_locked_item(self.create_event("Victory"))

    def create_event(self, event : str) -> GloverItem:
        return GloverItem(event, ItemClassification.progression, None, self.player)

    def create_item(self, name) -> GloverItem:
        item_classification = None
        item_id = -1
        #knownLevelAndWorld = [self.level_from_string(self, name), self.world_from_string(self, name)]
        item_data = find_item_data(self, name)
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

    def percent_of(self, percent : int) -> float:
        return (float(percent) / 100.0)

    def percents_sum_100(self, percents_dict : dict) -> bool:
        sum : float = 0
        for all_percentages in percents_dict.values():
            sum += all_percentages
        return math.isclose(sum, 1)

    def highest_dict_value(self, input_dict : dict) -> str:
        best_names : list[str]
        best_value : float = -99
        #Goes through all items
        for each_name, each_value in input_dict.items():
            if math.isclose(best_value, each_value):
                best_names.append(each_name)
            elif each_value > best_value:
                best_value = each_value
                best_names = [each_name]
        #If there's multiple valid options, pick one at random
        if len(best_names) > 1:
            return best_names[self.random.choice(best_names)]
        else:
            return best_names[0]

    def create_items(self) -> None:
        #Garib Logic
        garib_items = []
        match self.options.garib_logic:
            #0: Level Garibs (No items to be sent)
            #Garib Groups
            case GaribLogic.option_garib_groups:
                if self.options.garib_sorting == GaribSorting.option_by_level:
                    garib_items = list(world_garib_table.keys())
                else:
                    garib_items = list(decoupled_garib_table.keys())
            #Individual Garibs
            case GaribLogic.option_garibsanity:
                if self.options.garib_logic.value == GaribSorting.option_by_level:
                    garib_items = list(garibsanity_world_table.keys())
                else:
                    garib_items = ["Garibsanity"]
        
        #Checkpoint Logic
        checkpoint_items = []
        if self.options.checkpoint_checks.value:
            for each_checkpoint in checkpoint_table:
                level_offset = self.level_from_string(each_checkpoint)
                world_offset = self.world_from_string(each_checkpoint)
                if self.spawn_checkpoint[(level_offset - 1) + (world_offset * 3)] != int(each_checkpoint[-1]):
                    checkpoint_items.append(each_checkpoint)

        #Level Event Logic
        event_items = []
        if self.options.switches_checks.value == 1:
            event_items = list(level_event_table.keys())

        #Abilities
        ability_items = list(ability_table.keys())
        if not self.options.include_power_ball:
            ability_items.remove("Power Ball")
        if not self.options.randomize_jump:
            ability_items.remove("Jump")

        #You don't need the item pool to contain your starting item
        ability_items.remove(self.starting_ball)
        
        #self.multiworld
        #Apply all core items
        all_core_items = []
        all_core_items.extend(garib_items)
        all_core_items.extend(checkpoint_items)
        all_core_items.extend(ability_items)
        all_core_items.extend(event_items)
        #Core Items
        for each_item in all_core_items:
            for total_items in range(find_item_data(self, each_item).qty):
                self.multiworld.itempool.append(self.create_item(each_item))
        #Event Items
        #for each_item in event_items:
        #    self.multiworld.itempool.append(self.create_event(each_item))


        #Calculate the amount of trap filler and the amount of regular filler
        total_locations : int = len(self.multiworld.get_unfilled_locations(self.player))
        total_core_items : int = len(self.multiworld.itempool) + len(self.get_pre_fill_items())
        total_filler_items : int = int(total_locations - total_core_items)
        total_trap_items : int = int(self.percent_of(self.options.trap_percentage.value) * total_filler_items)
        total_filler_items -= total_trap_items
        filler_percentages : dict = {
            "Extra Garibs" : 							self.percent_of(self.options.filler_extra_garibs_weight.value),
            "Chicken Sound" : 							self.percent_of(self.options.filler_chicken_sound_weight.value),
	        "Life" : 									self.percent_of(self.options.filler_life_weight.value),
            "Boomerang" : 								self.percent_of(self.options.filler_boomerang_weight.value),
            "Beachball" : 								self.percent_of(self.options.filler_beachball_weight.value),
            "Hercules" : 								self.percent_of(self.options.filler_hercules_weight.value),
            "Helicopter" : 								self.percent_of(self.options.filler_helicopter_weight.value),
            "Speed" : 									self.percent_of(self.options.filler_speed_weight.value),
            "Frog" : 									self.percent_of(self.options.filler_frog_weight.value),
            "Death" : 									self.percent_of(self.options.filler_death_weight.value),
            "Sticky" : 									self.percent_of(self.options.filler_sticky_weight.value),
	    }
        trap_percentages : dict = {
            "Frog Spell" : 								self.percent_of(self.options.frog_trap_weight.value),
            "Cursed Ball" :								self.percent_of(self.options.cursed_ball_trap_weight.value),
            "Instant Crystal" :							self.percent_of(self.options.instant_crystal_trap_weight.value),
            "Camera Rotate" :							self.percent_of(self.options.camera_rotate_trap_weight.value),
            "Tip Trap" :								self.percent_of(self.options.tip_trap_weight.value)
        }
        
        #Apply the filler
        if not self.percents_sum_100(filler_percentages):
            print("The total of filler percentages isn't 100!")
        if not self.percents_sum_100(trap_percentages):
            print("The total of trap percentages isn't 100!")
        
        #Filler begins
        all_filler_items = []

        #Filler Item Count
        for each_item in range(int(total_filler_items)):
            item_key : str = self.highest_dict_value(filler_percentages)
            filler_percentages[item_key] -= total_filler_items / 100.0
            all_filler_items.append(item_key)
        
        #Trap Count
        for each_item in range(int(total_trap_items)):
            item_key : str = self.highest_dict_value(trap_percentages)
            trap_percentages[item_key] -= total_filler_items / 100.0
            all_filler_items.append(item_key)

        #Create the filler items
        for each_item in all_filler_items:
            self.multiworld.itempool.append(self.create_item(each_item))

    def connect_entrances(self):
        #Level portal randomization
        visualize_regions(self.multiworld.get_region("Menu", self.player), "Glover.puml")
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
        
        return options
