import gc
import math
from typing import Any, Dict

from BaseClasses import ItemClassification, Location, MultiWorld, Tutorial, Item, Region
import settings
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type, launch_subprocess
from worlds.generic.Rules import add_rule, set_rule

from .Options import GaribLogic, GloverOptions, GaribSorting, StartingBall
from .JsonReader import build_data, generate_location_name_to_id
from .ItemPool import generate_item_name_to_id, generate_item_name_groups, find_item_data, world_garib_table, decoupled_garib_table, garibsanity_world_table, checkpoint_table, level_event_table, ability_table, filler_table, trap_table
from Utils import visualize_regions
from .Hints import create_hints

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
    #DELETE THIS ONCE IT'S FINISHED
    existing_levels = ["Atl1", "Atl2", "Atl3", "Atl!", "Atl?", "Crn!", "Prt!", "Pht!", "FoF!", "Otw!", "Training"]
    group_lists : list[str] = ["Not Crystal",
	"Not Bowling",
	"Not Bowling or Crystal",
	"Sinks",
	"Floats",
	"Ball Up"]

    item_name_to_id = generate_item_name_to_id()
    item_name_groups = generate_item_name_groups()
    location_name_to_id = generate_location_name_to_id(world_prefixes, level_prefixes)

    def collect(self, state, item):
        output = super().collect(state, item)
        name : str = item.name
        #Item group lists
        for each_group in self.group_lists:
            if name in self.item_name_groups[each_group] and state.count_group(each_group, self.player) == 1:
                state.add_item(each_group, self.player)
        #Garib counting
        if name.endswith("Garib"):
            state.add_item("Total Garibs", self.player)
        elif name == "Extra Garibs":
            state.add_item("Total Garibs", self.player, self.options.extra_garibs_value.value)
        elif name == "Locate Garibs":
            return output
        elif name.endswith("Garibs"):
            split_name : list[str] = name.split(" ")
            garibs_number : int = int(split_name[len(split_name) - 2])
            state.add_item("Total Garibs", self.player, garibs_number)
        return output

    def remove(self, state, item):
        output = super().remove(state, item)
        name : str = item.name
        #Item group lists
        for each_group in self.group_lists:
            if name in self.item_name_groups[each_group] and state.count_group(each_group, self.player) == 0:
                state.remove_item(each_group, self.player)
        #Garib counting
        if name.endswith("Garib"):
            state.remove_item("Total Garibs", self.player)
        elif name == "Extra Garibs":
            state.remove_item("Total Garibs", self.player, self.options.extra_garibs_value.value)
        elif name == "Locate Garibs":
            return output
        elif name.endswith("Garibs"):
            split_name : list[str] = name.split(" ")
            garibs_number : int = int(split_name[len(split_name) - 2])
            state.remove_item("Total Garibs", self.player, garibs_number)
        return output

    def __init__(self, world, player):
        self.version = "V0.1"
        self.spawn_checkpoint = [
            2,3,3,
            4,5,4,
            3,3,4,
            3,4,4,
            3,3,5,
            2,1,4]
        
        #Level Portal Randomization
        self.wayroom_entrances : list[str] = []
        self.overworld_entrances : list[str] = []
        for each_world_prefix in self.world_prefixes:
            for each_level_prefix in self.level_prefixes:
                each_entrance : str = each_world_prefix + each_level_prefix
                if each_level_prefix == "H":
                    self.overworld_entrances.append(each_entrance)
                else:
                    self.wayroom_entrances.append(each_entrance)
        self.wayroom_entrances.append("Training")
        self.overworld_entrances.append("Well")
        #Garib level order table
        self.garib_level_order = [
            ["Atl1", 50],
            ["Atl2", 60],
            ["Atl3", 80],
            ["Atl?", 25]#,
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
        #Grab Mr. Tips for hints
        self.tip_locations : list[str] = []
        #Speaking of hints
        self.mr_hints : dict[str, Location] = {}
        self.chicken_hints : dict[str, Location] = {}
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
        if self.options.garib_sorting == GaribSorting.option_random_order:
            self.random.shuffle(self.garib_level_order)
            #Bonus levels all go at the end if they're disabled
            if not self.options.bonus_levels:
                self.garib_level_order.append(self.garib_level_order.pop(["Atl?", 25]))
                #self.garib_level_order.append(self.garib_level_order.pop(["Crn?", 20]))
                #self.garib_level_order.append(self.garib_level_order.pop(["Prt?", 50]))
                #self.garib_level_order.append(self.garib_level_order.pop(["Pht?", 60]))
                #self.garib_level_order.append(self.garib_level_order.pop(["FoF?", 56]))
                #self.garib_level_order.append(self.garib_level_order.pop(["Otw?", 50]))
        #Setup the spawning checkpoints
        if self.options.spawning_checkpoint_randomizer:
            #If randomized, pick a number from it's assigned value to the current value
            for each_index, each_item in enumerate(self.spawn_checkpoint):
                self.spawn_checkpoint[each_index] = self.random.randint(1, each_item)
        else:
            #By default, they're all Checkpoint 1
            for each_item in range(len(self.spawn_checkpoint)):
                self.spawn_checkpoint[each_item] = 1
        #Level entry randomization
        if self.options.entrance_randomizer:
            #When all levels exist, you can just shuffle this
            #self.random.shuffle(self.wayroom_entrances)

            #TEMP: While only certain levels exist, randomize only those.
            randomizable_existing_levels = self.existing_levels.copy()
            randomizable_existing_levels.remove("Crn!")
            randomizable_existing_levels.remove("Prt!")
            randomizable_existing_levels.remove("Pht!")
            randomizable_existing_levels.remove("FoF!")
            randomizable_existing_levels.remove("Otw!")
            shuffled_existing_levels = randomizable_existing_levels.copy()
            self.random.shuffle(shuffled_existing_levels)
            for level_index, level_name in enumerate(randomizable_existing_levels):
                replaced_index = self.wayroom_entrances.index(level_name)
                self.wayroom_entrances[replaced_index] = shuffled_existing_levels[level_index]

            #self.random.shuffle(self.overworld_entrances)
            if not self.options.bonus_levels:
                self.wayroom_entrances.remove("Atl?")
                self.wayroom_entrances.remove("Crn?")
                self.wayroom_entrances.remove("Prt?")
                self.wayroom_entrances.remove("Pht?")
                self.wayroom_entrances.remove("FoF?")
                self.wayroom_entrances.remove("Otw?")
                self.wayroom_entrances.insert(4, "Atl?")
                self.wayroom_entrances.insert(9, "Crn?")
                self.wayroom_entrances.insert(14, "Prt?")
                self.wayroom_entrances.insert(19, "Pht?")
                self.wayroom_entrances.insert(24, "FoF?")
                self.wayroom_entrances.insert(29, "Otw?")
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
	            "Crystal"]
                self.starting_ball = self.random.choice(ball_options)
            case StartingBall.option_random_any:
                ball_options = ["Rubber Ball",
	            "Bowling Ball",
	            "Ball Bearing",
	            "Crystal",
	            "Power Ball"]
                self.starting_ball = self.random.choice(ball_options)
        self.multiworld.push_precollected(self.create_item(self.starting_ball))
        if not self.options.randomize_jump:
            self.multiworld.push_precollected(self.create_item("Jump"))

    def create_regions(self):
        multiworld = self.multiworld
        player = self.player
        #Build all the game locations, and the locations contained under them
        build_data(self)
        multiworld.regions.append(Region("Menu", player, multiworld))
        
        #Randomize the entrances for those remaining regions
        self.entrance_randomizer()

        #Create the rules for garibs now, so filler generation works correct
        self.garib_item_rules()

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
                item_classification = ItemClassification.progression_deprioritized
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
            return self.random.choice(best_names)
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
                    if not self.options.bonus_levels:
                        garib_items = list(filter(lambda a: a[3:4] != "?", garib_items))
                else:
                    garib_items = list(decoupled_garib_table.keys())
            #Individual Garibs
            case GaribLogic.option_garibsanity:
                if self.options.garib_sorting == GaribSorting.option_by_level:
                    garib_items = list(garibsanity_world_table.keys())
                    if not self.options.bonus_levels:
                        garib_items = list(filter(lambda a: a[3:4] != "?", garib_items))
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
        core_item_count = 0
        #Core Items
        for each_item in all_core_items:
            for _ in range(find_item_data(self, each_item).qty):
                self.multiworld.itempool.append(self.create_item(each_item))
                core_item_count += 1
        #Event Items
        #for each_item in event_items:
        #    self.multiworld.itempool.append(self.create_event(each_item))

        #Calculate the amount of trap filler and the amount of regular filler
        total_locations : int = len(self.multiworld.get_unfilled_locations(self.player))
        total_core_items : int = core_item_count + len(self.get_pre_fill_items())
        total_filler_items : int = int(total_locations - total_core_items)
        total_trap_items : int = int(self.percent_of(self.options.trap_percentage.value) * total_filler_items)
        total_filler_items -= total_trap_items
        filler_percentages : dict = {
            "Extra Garibs" : 							self.percent_of(self.options.filler_extra_garibs_weight.value),
            "Chicken Sound" : 							self.percent_of(self.options.filler_chicken_sound_weight.value),
	        "Life" : 									self.percent_of(self.options.filler_life_weight.value),
            "Boomerang Spell" : 								self.percent_of(self.options.filler_boomerang_weight.value),
            "Beachball Spell" : 								self.percent_of(self.options.filler_beachball_weight.value),
            "Hercules Spell" : 								self.percent_of(self.options.filler_hercules_weight.value),
            "Helicopter Spell" : 								self.percent_of(self.options.filler_helicopter_weight.value),
            "Speed Spell" : 									self.percent_of(self.options.filler_speed_weight.value),
            "Frog Spell" : 									self.percent_of(self.options.filler_frog_weight.value),
            "Death Spell" : 									self.percent_of(self.options.filler_death_weight.value),
            "Sticky Spell" : 									self.percent_of(self.options.filler_sticky_weight.value),
	    }
        trap_percentages : dict = {
            "Frog Trap" : 								self.percent_of(self.options.frog_trap_weight.value),
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

    def garib_item_rules(self):
        #Garib items now combine with the garib sorting type and garib rules to create rules
        player : int = self.player

        #Unless you've set it to level garibs, in which case it's so straight forward it's done in JsonReader
        if self.options.garib_logic == GaribLogic.option_level_garibs:
            return
        #Otherwise, start by the sorting method, since it has the most major effect on how garib rules act
        if self.options.garib_sorting == GaribSorting.option_by_level:
            #Garibs are sent to specific levels
            garib_level_suffixes = ["1", "2", "3", "?"]
            if not self.options.bonus_levels:
                garib_level_suffixes.remove("?")
            
            #The table for use
            table_for_use : dict
            match self.options.garib_logic:
                case GaribLogic.option_garib_groups:
                    table_for_use = world_garib_table
                case GaribLogic.option_garibsanity:
                    table_for_use = garibsanity_world_table
           
            #Go over all relevant levels
            for world_prefix in self.world_prefixes:
                for garib_level_suffix in garib_level_suffixes:
                    world_name = world_prefix + garib_level_suffix
                    #Get the "All Garibs" location to set rules for
                    level_all_garibs : Location = self.multiworld.get_location(world_name + ": All Garibs", player)
                    #Get all garibs groups that belong to the given world
                    garib_item_names : list[str] = []
                    garib_item_count : int = 0
                    for each_key, each_item in table_for_use.items():
                        if each_key.startswith(world_name):
                            garib_item_names.append(each_key)
                            garib_item_count += each_item.qty
                    #With world garibs, Extra Garibs counts as 1 group from each world
                    #garib_item_names.append("Extra Garibs")
                    #With the total number of garib items you need
                    if len(garib_item_names) > 0:
                        set_rule(level_all_garibs, lambda state, required_groups = garib_item_names, required_group_count = garib_item_count: state.has_from_list(required_groups, player, required_group_count))
        else:
            #If they're decoupled from levels, count directly
            total_required_garibs : int = 0
            #Garibs are collected in the given order
            for each_level in self.garib_level_order:
                #Ignore bonus levels if it's disabled
                if each_level[0].endswith("?") and not self.options.bonus_levels:
                    continue
                #At the next level
                level_all_garibs : Location = self.multiworld.get_location(each_level[0] + ": All Garibs", player)
                #Require the cumulative garib count of all garib completions before this one
                total_required_garibs += each_level[1]
                set_rule(level_all_garibs, lambda state, cumulative_garib_requirement = total_required_garibs: state.has("Total Garibs", player, cumulative_garib_requirement))

    def entrance_randomizer(self):
        entry_name : list[str] = ["1", "2", "3", "Boss", "Bonus"]
        multiworld : MultiWorld = self.multiworld
        player : int = self.player

        #TEMP ENDING
        final_location_name : str = "Atl3: Goal"
        end_region : Region = multiworld.get_location(final_location_name, player).parent_region
        final_location : Location = Location(player, "Ending", None, end_region)
        end_region.locations.append(final_location)
        add_rule(final_location, lambda state: state.can_reach_location(final_location_name, player))
        final_location.place_locked_item(self.create_event("Victory"))
        multiworld.completion_condition[player] = lambda state: state.has("Victory", player)

        #Menu loads into the hubworld
        hubworld : Region = multiworld.get_region("Hubworld", player)
        multiworld.get_region("Menu", player).connect(hubworld)
        hubworld.connect(multiworld.get_region("Hubworld: Main W/Ball", player))
        castle_cave : Region = multiworld.get_region("Castle Cave", player)
        hubworld.connect(castle_cave)
        castle_cave.connect(multiworld.get_region("Castle Cave: Main W/Ball", player))

        #Apply wayroom entrances
        for world_index, each_world_prefix in enumerate(self.world_prefixes):
            world_offset : int  = world_index * 5
            wayroom_name : str = each_world_prefix + "H"
            hubroom : Region = multiworld.get_region(wayroom_name, player)
            hubroom.connect(multiworld.get_region(wayroom_name + ": Main W/Ball", player))
            #Entries
            for entry_index, each_entry_suffix in enumerate(entry_name):
                #Connect hubs to the right location
                offset : int = world_offset + entry_index
                location_name : str = wayroom_name + ": Entry " + each_entry_suffix
                connecting_level_name : str = self.wayroom_entrances[offset]
                if connecting_level_name.endswith('?') and not self.options.bonus_levels:
                    continue
                connecting_level : Region = multiworld.get_region(connecting_level_name, player)
                entry_region : Region = multiworld.get_location(location_name, player).parent_region
                entry_region.connect(connecting_level, location_name, lambda state, each_location = location_name: state.can_reach_location(each_location, player))
                
                #Default portal and star positions
                if not self.options.portalsanity:
                    self.populate_goals_and_marks(connecting_level_name, wayroom_name, entry_index)
            
            #Getting a star on all 4 other levels
            if self.options.bonus_levels:
                bonus_unlock_address : int | None = None
                if self.options.portalsanity:
                    bonus_unlock_address = 3100 + (world_index * 100)
                bonus_unlock : Location = Location(player, wayroom_name + ": Bonus Unlock", bonus_unlock_address, hubroom)
                hubroom.locations.append(bonus_unlock)
                #Unlocks the bonus level
                if not self.options.portalsanity:
                   bonus_unlock.place_locked_item(self.create_event(wayroom_name + " Bonus Gate"))
                main_star_marks : list[str] = [wayroom_name + " 1 Star", wayroom_name + " 2 Star", wayroom_name + " 3 Star"]
                set_rule(bonus_unlock, lambda state, required_star_marks = main_star_marks: state.has_all(required_star_marks, player))

        #Entry Names
        hub_entry_names : list[str] = [
            "Atlantis Hub Entry",
            "Carnival Hub Entry",
            "Pirates Hub Entry",
            "Prehistoric Hub Entry",
            "Fear Hub Entry",
            "OotW Hub Entry",
            "Well Entry"
        ]

        #Apply hubworld entrances
        for entrance_index, entrance_name in enumerate(self.overworld_entrances):
            loading_zone : str = hub_entry_names[entrance_index]
            connecting_name : str  = entrance_name
            if entrance_name == "Well":
                connecting_name = self.wayroom_entrances[len(self.wayroom_entrances) - 1]
                #Plug the well's completions up so they do nothing
                if not self.options.portalsanity:
                    self.populate_goals_and_marks(connecting_name, "Well", -1)
            connecting_level : Region = multiworld.get_region(connecting_name, player)
            reaching_location : str = "Hubworld: " + loading_zone
            reaching_region : Region = multiworld.get_location(reaching_location, player).parent_region
            reaching_region.connect(connecting_level, loading_zone, lambda state, each_location = reaching_location: state.can_reach_location(each_location, player))

    #Lacking Portalsanity Gates and Marks
    def populate_goals_and_marks(self, connecting_level_name : str, wayroom_name : str, entry_index : int):
        player = self.player
        
        #Disable bonus levels
        if connecting_level_name.endswith('?') and not self.options.bonus_levels:
            return
        
        #Map Generation
        goal_item : Item
        all_garibs_item : Item
        #What fixed item is there?
        match entry_index:
            case -1:
                goal_item = self.create_event(wayroom_name + " Finished")
                all_garibs_item  = self.create_event(wayroom_name + " Completed")
            case 0:
                goal_item = self.create_event(wayroom_name + " 2 Gate")
                all_garibs_item  = self.create_event(wayroom_name + " 1 Star")
            case 1:
                goal_item = self.create_event(wayroom_name + " 3 Gate")
                all_garibs_item  = self.create_event(wayroom_name + " 2 Star")
            case 2:
                goal_item = self.create_event(wayroom_name + " Boss Gate")
                all_garibs_item  = self.create_event(wayroom_name + " 3 Star")
            case 3:
                goal_item = self.create_event(wayroom_name + " Ball")
                all_garibs_item  = self.create_event(wayroom_name + " Boss Star")
            case 4:
                goal_item = self.create_event(wayroom_name + " Bonus Complete")
                all_garibs_item  = self.create_event(wayroom_name + " Bonus Star")
        #What kind of level is this?
        
        #TEMP: REMOVE IF SATEMENTS ONCE GAME'S CONSTRUCTED
        if connecting_level_name in self.existing_levels:
            goal_or_boss : str = ": Goal"
            if connecting_level_name.endswith('!'):
                goal_or_boss = ": Boss"
            goal_location : Location = self.multiworld.get_location(connecting_level_name + goal_or_boss, player)
            goal_location.place_locked_item(goal_item)
        
        garibs_location : Location
        #Levels with garibs
        if connecting_level_name.endswith(('1','2','3','?')):
            garibs_location = self.multiworld.get_location(connecting_level_name + ": All Garibs", player)
        #Levels without garibs
        else:
            garibs_location = self.multiworld.get_location(connecting_level_name + ": Completion", player)
        #Place them
        garibs_location.place_locked_item(all_garibs_item)

    def connect_entrances(self):
        visualize_regions(self.multiworld.get_region("Menu", self.player), "Glover.puml", regions_to_highlight=self.multiworld.get_all_state().reachable_regions[self.player])
        return super().connect_entrances()

    def build_options(self):
        options = {}
        options["difficulty_logic"] = self.options.difficulty_logic.value
        options["death_link"] = self.options.death_link.value
        options["tag_link"] = self.options.tag_link.value
        options["starting_ball"] = self.options.starting_ball.value
        options["garib_logic"] = self.options.garib_logic.value
        options["garib_sorting"] = self.options.garib_sorting.value
        options["entrance_randomizer"] = self.options.entrance_randomizer.value
        options["portalsanity"] = self.options.portalsanity.value
        options["spawning_checkpoint_randomizer"] = self.options.spawning_checkpoint_randomizer.value
        options["bonus_levels"] = self.options.bonus_levels.value
        #options["atlantis_bonus"] = self.options.atlantis_bonus.value
        options["randomize_jump"] = self.options.randomize_jump.value
        options["include_power_ball"] = self.options.include_power_ball.value
        options["checkpoint_checks"] = self.options.checkpoint_checks.value
        options["switches_checks"] = self.options.switches_checks.value
        options["mr_tip_checks"] = self.options.mr_tip_checks.value
        options["enemysanity"] = self.options.enemysanity.value
        options["insectity"] = self.options.insectity.value
        options["mr_hints"] = self.options.mr_hints.value
        options["chicken_hints"] = self.options.chicken_hints.value
        options["extra_garibs_value"] = self.options.extra_garibs_value.value

        options["player_name"] = self.multiworld.player_name[self.player]
        options["seed"] = self.random.randint(-6500000, 6500000)
        options["version"] = self.version
        return options

    def generate_hints(self):
        hint_groups = create_hints(self)
        #Mr. Tip Hints
        self.mr_hints = hint_groups[0]
        #Chicken Hints
        self.chicken_hints = hint_groups[1]

    def lua_world_name(self, original_name):
        lua_prefixes = ["AP_ATLANTIS", "AP_CARNIVAL", "AP_PIRATES", "AP_PREHISTORIC", "AP_FORTRESS", "AP_SPACE", "AP_TRAINING"]
        lua_suffixes = ["_L1", "_L2", "_L3", "_BOSS", "_BONUS", "_WORLD"]
        world_index : int = self.world_from_string(original_name)
        level_index : int = self.level_from_string(original_name) - 1
        if world_index >= 6:
            level_index = 5
        lua_prefix = lua_prefixes[world_index]
        lua_suffix = lua_suffixes[level_index]
        return lua_prefix + lua_suffix

    def lua_decoupled_garib_order(self) -> dict[str, str]:
        output = {}
        for level_index, each_level in enumerate(self.garib_level_order):
            lua_name = self.lua_world_name(each_level[0])
            output[str(level_index)] = lua_name + "_GARIBS"
        return output

    def lua_world_entry_lookup_table(self) -> dict[str, str]:
        output = {}
        for each_wayroom_index, each_wayroom_entrance in enumerate(self.wayroom_entrances):
            #Wayroom info
            wayroom_orign = int(each_wayroom_index / 5) + 1
            wayroom_door = (each_wayroom_index % 5) + 1
            #Hub
            if wayroom_orign >= 7:
                wayroom_door = 0
            #Table entry with original world as a key, and the data entries as
            output[self.lua_world_name(each_wayroom_entrance)] = (wayroom_orign * 10) + wayroom_door
        return output

    def fill_slot_data(self) -> Dict[str, Any]:
        self.generate_hints()
        options = self.build_options()
        options["world_lookup"] = self.lua_world_entry_lookup_table()
        options["garib_order"] = self.lua_decoupled_garib_order()
        return options
