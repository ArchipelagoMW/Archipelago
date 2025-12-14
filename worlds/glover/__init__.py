import gc
import math
from typing import Any, Dict

from BaseClasses import ItemClassification, Location, MultiWorld, Tutorial, Item, Region
from Options import OptionError, OptionGroup
from .MrTipText import generate_tip_table
from .TrapText import create_trap_name_table, select_trap_item_name
import settings
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, icon_paths, Type, launch_subprocess
from worlds.generic.Rules import add_rule, set_rule

from .Options import GaribLogic, GloverOptions, GaribSorting, StartingBall
from .JsonReader import build_data, generate_location_name_to_id
from .ItemPool import construct_blank_world_garibs, generate_item_name_to_id, generate_item_name_groups, find_item_data, world_garib_table, decoupled_garib_table, garibsanity_world_table, checkpoint_table, level_event_table, ability_table
from Utils import local_path, visualize_regions
from .Hints import create_hints

def run_client():
    from .GloverClient import main  # lazy import
    launch_subprocess(main)

components.append(Component("Glover Client", func=run_client, component_type=Type.CLIENT,
                            icon='Glover Icon',
                            description="Glover's N64 AP. Shazam!"))

icon_paths['Glover Icon'] = "ap:worlds.glover/assets/icon.png"

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
    #Fake names for traps
    fake_name : str | None = None
    @property
    def hint_text(self) -> str:
        name_for_use = self.name
        if self.fake_name != None:
            name_for_use = self.fake_name
        return getattr(self, "_hint_text", name_for_use.replace("_", " ").replace("-", " "))
    @property
    def pedestal_hint_text(self) -> str:
        name_for_use = self.name
        if self.fake_name != None:
            name_for_use = self.fake_name
        return getattr(self, "_pedestal_hint_text", name_for_use.replace("_", " ").replace("-", " "))

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
    option_groups = [
        OptionGroup("Victory Conditions", [
            Options.VictoryCondition,
            Options.RequiredCrystals,
            Options.GoldenGaribCount,
            Options.GoldenGaribRequirement
        ]),
        OptionGroup("Difficulty", [
            Options.DifficultyLogic,
            Options.EnableBonuses,
            Options.EasyBallWalk
        ]),
        OptionGroup("Links", [
            Options.TagLink,
            Options.TrapLink
        ]),
        OptionGroup("Game Setup", [
            Options.StartingBall,
            Options.RandomizeJump,
            Options.IncludePowerBall
        ]),
        OptionGroup("Garibs", [
            Options.GaribLogic,
            Options.GaribSorting,
            Options.GaribOrderOverrides
        ]),
        OptionGroup("Entrance Randomization", [
            Options.EntranceRandomizer,
            Options.EntranceOverrides#,
            #Options.Portalsanity
        ]),
        OptionGroup("Checkpoints", [
            Options.SpawningCheckpointRandomizer,
            Options.CheckpointOverrides
        ]),
        OptionGroup("Locations", [
            Options.CheckpointsChecks,
            Options.SwitchesChecks,
            Options.MrTipChecks,
            Options.Enemysanity,
            Options.Insectity
        ]),
        OptionGroup("Hints", [
            Options.MrHints,
            Options.MrTipTextDisplay,
            Options.MrTipScouts,
            Options.ChickenHints
        ]),
        OptionGroup("Filler", [
            Options.ExtraGaribsValue,
            Options.FillerExtraGaribsWeight,
            Options.FillerChickenSoundWeight,
            Options.FillerLifeWeight,
            Options.FillerBoomerangBallWeight,
            Options.FillerBeachballWeight,
            Options.FillerHerculesPotionWeight,
            Options.FillerHelicopterPotionWeight,
            Options.FillerSpeedPotionWeight,
            Options.FillerFrogPotionWeight,
            Options.FillerDeathPotionWeight,
            Options.FillerStickyPotionWeight
        ]),
        OptionGroup("Traps", [
            Options.TrapPercentage,
            Options.TrapFrogWeight,
            Options.TrapCursedBallWeight,
            Options.TrapBecomesCrystalWeight,
            Options.TrapCameraRotateWeight#,
            #Options.TrapTipWeight
        ])
    ]

class GloverWorld(World):
    """
    Glover is an N64 physics puzzle platforming game.
    """
    game : str = "Glover"
    version : str = "V1.0"
    web = GloverWeb()
    topology_present = True
    settings: GloverSettings
    settings_key = "glover_options"
    options_dataclass = GloverOptions
    options : GloverOptions

    #Check/Item Prefixes
    world_prefixes = ["Atl", "Crn", "Prt", "Pht", "FoF", "Otw"]
    level_prefixes = ["H", "1", "2", "3", "!", "?"]
    existing_levels = ["Atl1", "Atl2", "Atl3", "Atl!", "Atl?", 
                       "Crn1", "Crn2", "Crn3", "Crn!", "Crn?", 
                       "Prt1", "Prt2", "Prt3", "Prt!", "Prt?", 
                       "Pht1", "Pht2", "Pht3", "Pht!", "Pht?", 
                       "FoF1", "FoF2", "FoF3", "FoF!", "FoF?", 
                       "Otw1", "Otw2", "Otw3", "Otw!", "Otw?", 
                       "Training"]
    group_lists : list[str] = ["Not Crystal",
	"Not Bowling",
	"Not Bowling or Crystal",
	"Sinks",
	"Floats",
	"Ball Up"]

    item_name_to_id = generate_item_name_to_id(world_prefixes, level_prefixes)
    item_name_groups = generate_item_name_groups()
    location_name_to_id = generate_location_name_to_id(world_prefixes, level_prefixes)

    def collect(self, state, item):
        output = super().collect(state, item)
        name : str = item.name
        #Item group lists
        for each_group in self.group_lists:
            if name in self.item_name_groups[each_group] and state.count_group(each_group, self.player) == 1:
                state.add_item(each_group, self.player)
        #You've gotten a ball by beating the level in the 4th gate
        if name.endswith("H Ball") and name.startswith(tuple(self.world_prefixes)) and item.code == None:
            state.add_item("Returned Balls", self.player)
        #Progressive Events
        if name in ["Crn1 Rocket", "Pht3 Lower Monolith", "FoF1 Progressive Doorway", "FoF2 Progressive Gate"]:
            progressive_count = state.count(name, self.player)
            state.add_item(name + " " + str(progressive_count), self.player)
        #Garib counting
        if self.options.difficulty_logic.value > 0 or self.options.bonus_levels:
            if name.endswith("Garib") or name.endswith("Garibs") and name != "Golden Garib":
                garibs_number : int = self.get_garib_group_size(name)
                if garibs_number >= 0:
                    state.add_item("Total Garibs", self.player, garibs_number)
        return output

    def remove(self, state, item):
        output = super().remove(state, item)
        name : str = item.name
        #Item group lists
        for each_group in self.group_lists:
            if name in self.item_name_groups[each_group] and state.count_group(each_group, self.player) == 0:
                state.remove_item(each_group, self.player)
        #You've gotten a ball by beating the level in the 4th gate
        if name.endswith("H Ball") and name.startswith(tuple(self.world_prefixes)) and item.code == None:
            state.remove_item("Returned Balls", self.player)
        #Progressive Events
        if name in ["Crn1 Rocket", "Pht3 Lower Monolith", "FoF1 Progressive Doorway", "FoF2 Progressive Gate"]:
            progressive_count = state.count(name, self.player)
            state.remove_item(name + " " + str(progressive_count), self.player)
        #Garib counting
        if self.options.difficulty_logic.value > 0 or self.options.bonus_levels:
            if name.endswith("Garib") or name.endswith("Garibs") and name != "Golden Garib":
                garibs_number : int = self.get_garib_group_size(name)
                if garibs_number >= 0:
                    state.remove_item("Total Garibs", self.player, garibs_number)
        return output

    def get_garib_group_size(self, garibName : str):
        if garibName == "Garib":
            return 1
        nameDigit : str = garibName.removesuffix(" Garib").removesuffix(" Garibs")[-2:].removeprefix(" ")
        if nameDigit.isdigit():
            return int(nameDigit)
        return -1

    def __init__(self, world, player):
        self.version = "V1.0"
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
            ["Atl?", 25],
            ["Crn1", 65],
            ["Crn2", 80],
            ["Crn3", 80],
            ["Crn?", 20],
            ["Prt1", 70],
            ["Prt2", 60],
            ["Prt3", 80],
            ["Prt?", 50],
            ["Pht1", 80],
            ["Pht2", 80],
            ["Pht3", 80],
            ["Pht?", 60],
            ["FoF1", 60],
            ["FoF2", 60],
            ["FoF3", 70],
            ["FoF?", 56],
            ["Otw1", 50],
            ["Otw2", 50],
            ["Otw3", 80],
            ["Otw?", 50]
        ]
        #Extra garib placements
        self.extra_garib_levels = [
            ["Atl1", 0],
            ["Atl2", 0],
            ["Atl3", 0],
            ["Atl?", 0],
            ["Crn1", 0],
            ["Crn2", 0],
            ["Crn3", 0],
            ["Crn?", 0],
            ["Prt1", 0],
            ["Prt2", 0],
            ["Prt3", 0],
            ["Prt?", 0],
            ["Pht1", 0],
            ["Pht2", 0],
            ["Pht3", 0],
            ["Pht?", 0],
            ["FoF1", 0],
            ["FoF2", 0],
            ["FoF3", 0],
            ["FoF?", 0],
            ["Otw1", 0],
            ["Otw2", 0],
            ["Otw3", 0],
            ["Otw?", 0]
        ]
        self.starting_ball : str = "Rubber Ball"
        #Grab Mr. Tips for hints
        self.tip_locations : list[str] = []
        #Speaking of hints
        self.mr_hints = {}
        self.chicken_hints = {}
        #Fake item names
        self.fake_item_names = []

        #Create null items for the table
        world_garib_table.update(construct_blank_world_garibs(self.world_prefixes, self.level_prefixes))

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

    def set_highest_valid_checkpoints(self):
        #Limit checkpoint options if everything must be accessable
        if self.options.accessibility.value == 0 and self.options.checkpoint_checks != 1:
            #Carnival 2 (Pre-Rollercoaster)
            self.spawn_checkpoint[4] = 1
            #Fear 3 (Post-Warp)
            self.spawn_checkpoint[14] = 1, 2, 3
            #Intended Locks
            if self.options.difficulty_logic.value == 0:
                #Prehistoric 1 (Icicles)
                self.spawn_checkpoint[9] = 1
                #Prehistoric 3 (Lava Platforms)
                self.spawn_checkpoint[11] = 1, 2, 3
            #Without Switch Items
            if not self.options.switches_checks:
                #Intended Locks
                if self.options.difficulty_logic.value == 0:
                    #Carnival 3 (Hands)
                    self.spawn_checkpoint[5] = 3
                    #Pirates 1 (Raise Ship)
                    self.spawn_checkpoint[6] = 3
                    #Prehistoric 2 (Lava Platforms)
                    self.spawn_checkpoint[10] = 2
                    #Fear 1 (Ball Gate)
                    self.spawn_checkpoint[12] = 2
                    #Space 3 (Glass Gate)
                    self.spawn_checkpoint[17] = 3
                #Easy/Intended Locks
                if self.options.difficulty_logic.value <= 1:
                    #Prehistoric 3 (Lava Platforms)
                    self.spawn_checkpoint[11] = 2
                    #Fear 2 (Lever Room)
                    self.spawn_checkpoint[13] = 2

    def validate_options(self):
        #Level Name input validation
        for each_level, each_door in self.options.entrance_overrides.items():
            if not self.valid_override_level_name(each_level):
                raise OptionError("\""+ each_level + "\" is not a valid level for Entrance Overrides!")
            if not self.valid_override_level_name(each_door):
                raise OptionError("\""+ each_door + "\" is not a valid door for Entrance Overrides!")
        for each_level in list(self.options.garib_order_overrides.keys()):
            if not self.valid_override_level_name(each_level, False):
                raise OptionError("\""+ each_level + "\" is not a valid level for Garib Order Overrides!")
        garib_override_positions = list(self.options.garib_order_overrides.values())
        entrance_override_doors = list(self.options.entrance_overrides.values())
        
        #No duplicate override choices for Garib Order or World Order
        if len(garib_override_positions) != len(set(garib_override_positions)):
            raise OptionError("Two garib overrides choose the same position! Make sure all values are unique.")
        if len(entrance_override_doors) != len(set(entrance_override_doors)):
            raise OptionError("Two entrance overrides choose the same door! Make sure all values are unique.")

        #Checkpoint Overrides In-Bounds
        for target_level, set_checkpoint in self.options.checkpoint_overrides.items():
            if not self.valid_override_level_name(target_level, False, False):
                raise OptionError("\""+ target_level + "\" is not a valid level for Checkpoint Overrides!")
            world_index = self.world_from_string(target_level)
            level_index = self.level_from_string(target_level) - 1
            max_checkpoint_value = self.spawn_checkpoint[(world_index * 3) + level_index]
            if max_checkpoint_value < set_checkpoint or set_checkpoint < 1:
                raise OptionError("Level " + target_level + " does not have a \"Checkpoint " + str(set_checkpoint) + "\"! Check your Checkpoint Overrides.")
        
        #Golden Garibs Possible
        total_golden_garibs = self.options.golden_garib_count.value
        total_golden_garibs += self.get_pre_fill_items().count("Golden Garib")
        if total_golden_garibs < self.options.required_golden_garibs.value:
            raise OptionError("Must have enough golden garibs to get the required golden garib count!")
    
    def valid_override_level_name(self, in_level : str, allow_bosses : bool = True, allow_bonuses : bool = True) -> bool:
        end_options = ["1", "2", "3"]
        if self.options.bonus_levels and allow_bonuses:
            end_options.append("?")
        if allow_bosses:
            end_options.append("!")
        return in_level.endswith(tuple(end_options)) and in_level.startswith(tuple(["Atl", "Crn", "Prt", "Pht", "FoF", "Otw"])) and len(in_level) == 4
   
    def percents_sum_100(self, percents_dict : dict) -> dict:
        sum : float = 0
        for all_percentages in percents_dict.values():
            sum += all_percentages
        if math.isclose(sum, 1):
            return percents_dict
        if math.isclose(sum, 0):
            raise OptionError("All weight entries are 0! Check your Filler or Trap weights!")
        for all_entries, all_percentages in percents_dict.items():
            percents_dict[all_entries] /= sum
        return percents_dict
    
    def setup_entrance_randomization(self):
        #While only certain levels exist, randomize only those.
        randomizable_existing_levels = self.existing_levels.copy()
        randomizable_existing_levels.remove("Training")
        shuffled_existing_levels = randomizable_existing_levels.copy()
        self.random.shuffle(shuffled_existing_levels)
        originalEntries = self.wayroom_entrances.copy()
        for level_index, level_name in enumerate(randomizable_existing_levels):
            replaced_index = originalEntries.index(level_name)
            self.wayroom_entrances[replaced_index] = shuffled_existing_levels[level_index]
        
        #Remove bonus levels by placing them in vanilla spots
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
        
        #Override randomized entrances here
        for each_entry, each_door in self.options.entrance_overrides.items():
            index = (self.world_from_string(each_door) * 5) + self.level_from_string(each_door) - 1
            original_world = self.wayroom_entrances[index]
            original_index = self.wayroom_entrances.index(each_entry)
            self.wayroom_entrances[index] = each_entry
            self.wayroom_entrances[original_index] = original_world

    def setup_garib_order(self):
        #Random Garib Sorting Order
        if self.options.garib_sorting == GaribSorting.option_random_order:
            self.random.shuffle(self.garib_level_order)
            #Override the garib order
            for each_level, each_placement in self.options.garib_order_overrides.items():
                level_in_slot = self.garib_level_order[each_placement]
                original_placement = -1
                original_level = []
                #Swap the randomized position with the overwriten one
                for original_index, each_original in enumerate(self.garib_level_order):
                    if each_original[0] == each_level:
                        original_placement = original_index
                        original_level = each_original
                self.garib_level_order[original_placement] = level_in_slot
                self.garib_level_order[each_placement] = original_level
        #Randomized Entrances, Garibs in Order
        elif self.options.garib_sorting == GaribSorting.option_in_order and self.options.entrance_randomizer:
            new_garib_order : list[list] = []
            for level_name in self.wayroom_entrances:
                #Find the level with the same name
                for each_entry in self.garib_level_order:
                    if each_entry[0] == level_name:
                        new_garib_order.append(each_entry)
            self.garib_level_order = new_garib_order

        #Bonus level garibs all go at the end if they're disabled
        if not self.options.bonus_levels:
            self.garib_level_order.remove(["Atl?", 25])
            self.garib_level_order.remove(["Crn?", 20])
            self.garib_level_order.remove(["Prt?", 50])
            self.garib_level_order.remove(["Pht?", 60])
            self.garib_level_order.remove(["FoF?", 56])
            self.garib_level_order.remove(["Otw?", 50])
            self.garib_level_order.append(["Atl?", 25])
            self.garib_level_order.append(["Crn?", 20])
            self.garib_level_order.append(["Prt?", 50])
            self.garib_level_order.append(["Pht?", 60])
            self.garib_level_order.append(["FoF?", 56])
            self.garib_level_order.append(["Otw?", 50])

    def give_starting_ball(self):
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

    def generate_early(self):
        #Set the valid spawning checkpoints
        self.set_highest_valid_checkpoints()
        #Validate options
        self.validate_options()
        #Setup the Filler Table logic
        self.setup_filler_table()
        #Shuffle Checkpoints
        self.checkpoint_randomization()
        #Level entry randomization
        if self.options.entrance_randomizer:
            self.setup_entrance_randomization()
        #Set the garib order if the settings allow it
        self.setup_garib_order()
        #Set the starting ball
        self.give_starting_ball()
        #Jump randomization is so easy it can just be done here
        if not self.options.randomize_jump:
            self.multiworld.push_precollected(self.create_item("Jump"))
        #Create fake items
        self.fake_item_names = create_trap_name_table(self)
        #Create the Mr. Tip Table
        self.mr_tip_table : list[str] = generate_tip_table(self)

    def checkpoint_randomization(self):
        #Setup the spawning checkpoints
        if self.options.spawning_checkpoint_randomizer:
            #Choose where you spawn from a list of options created
            spawning_options : list[list[int]] = []
            for each_index, each_item in enumerate(self.spawn_checkpoint):
                listEntry : list[int] = list(range(1, each_item + 1))
                spawning_options.append(listEntry)
            
            #Choose at random
            for each_index, each_item in enumerate(self.spawn_checkpoint):
                self.spawn_checkpoint[each_index] = self.random.choice(spawning_options[each_index])
            
            #Override Checkpoints
            for each_map, checkpoint_number in self.options.checkpoint_overrides.items():
                checkpoint_entry = (self.world_from_string(each_map) * 3) + self.level_from_string(each_map) - 1
                self.spawn_checkpoint[checkpoint_entry] = checkpoint_number
        else:
            #By default, they're all Checkpoint 1
            for each_item in range(len(self.spawn_checkpoint)):
                self.spawn_checkpoint[each_item] = 1

    def create_regions(self):
        multiworld = self.multiworld
        player = self.player
        #Build all the game locations, and the locations contained under them
        build_data(self)
        multiworld.regions.append(Region("Menu", player, multiworld))
        
        #Randomize the entrances for those remaining regions
        self.entrance_randomizer()

        #Create the victory conditon
        self.setup_victory()

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
            case "Proguseful":
                item_classification = ItemClassification.progression | ItemClassification.useful
            case "Progression":
                item_classification = ItemClassification.progression
            case "Useful":
                item_classification = ItemClassification.useful
            case "Filler":
                item_classification = ItemClassification.filler
            case "Trap":
                item_classification = ItemClassification.trap
            case "Garib":
                #If the garibs have no use, they're filler
                if self.options.difficulty_logic.value == 0 and not self.options.bonus_levels:
                    item_classification = ItemClassification.filler
                #If they're part of World Sorting logic, don't skip balancing for them
                elif self.options.garib_sorting.value == 0:
                    item_classification = ItemClassification.progression_deprioritized
                #Otherwise, skip balancing too
                else:
                    item_classification = ItemClassification.progression_deprioritized_skip_balancing
        name_for_use = name
        #Garibsanity is just Garib
        if name == "Garibsanity":
            name_for_use = "Garib"
        #Convert Extra Garibs into other types
        #if name == "Extra Garibs":
        #    name_for_use = convert_extra_garibs(self)
        item_output : GloverItem = GloverItem(name_for_use, item_classification, item_id, self.player)
        #Rename traps on pedestals
        if item_data.type == "Trap":
            fake_item_name = select_trap_item_name(self, name_for_use)
            item_output.fake_name = fake_item_name
        return item_output

    def percent_of(self, percent : int) -> float:
        return (float(percent) / 100.0)

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
        if not self.options.include_power_ball and self.starting_ball != "Power Ball":
            ability_items.remove("Power Ball")
        if not self.options.randomize_jump:
            ability_items.remove("Jump")

        #You don't need the item pool to contain your starting item
        ability_items.remove(self.starting_ball)
        
        #Golden Garibs
        if self.options.victory_condition.value == 2:
            ability_items.append("Golden Garib")

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

        #Calculate the total number of filler items needed to fill the missing locations
        total_locations : int = len(self.multiworld.get_unfilled_locations(self.player))
        total_core_items : int = core_item_count + len(self.get_pre_fill_items())
        total_filler_items : int = int(total_locations - total_core_items)
        
        #Create a filler item for each missing location
        for _ in range(total_filler_items):
            self.multiworld.itempool.append(self.create_filler())
    
    #Constructs the table for refrence using the get_filler_item_name function
    def setup_filler_table(self):
        filler_percentages : dict[str, float] = {
            "Extra Garibs" : 		    self.percent_of(self.options.filler_extra_garibs_weight.value),
            "Chicken Sound" : 		    self.percent_of(self.options.filler_chicken_sound_weight.value),
	        "Life" : 				    self.percent_of(self.options.filler_life_weight.value),
            "Boomerang Spell" : 	    self.percent_of(self.options.filler_boomerang_weight.value),
            "Beachball Spell" : 	    self.percent_of(self.options.filler_beachball_weight.value),
            "Hercules Spell" : 		    self.percent_of(self.options.filler_hercules_weight.value),
            "Helicopter Spell" :	    self.percent_of(self.options.filler_helicopter_weight.value),
            "Speed Spell" : 		    self.percent_of(self.options.filler_speed_weight.value),
            "Frog Spell" : 			    self.percent_of(self.options.filler_frog_weight.value),
            "Death Spell" : 		    self.percent_of(self.options.filler_death_weight.value),
            "Sticky Spell" : 		    self.percent_of(self.options.filler_sticky_weight.value),
	    }
        trap_percentages : dict[str, float] = {
            "Frog Trap" : 			    self.percent_of(self.options.frog_trap_weight.value),
            "Cursed Ball Trap" :	    self.percent_of(self.options.cursed_ball_trap_weight.value),
            "Instant Crystal Trap" :    self.percent_of(self.options.instant_crystal_trap_weight.value),
            "Camera Rotate Trap" :	    self.percent_of(self.options.camera_rotate_trap_weight.value),
            "Tip Trap" :			    self.percent_of(self.options.tip_trap_weight.value)
        }
        
        trap_percentage = self.percent_of(self.options.trap_percentage.value)
        filler_percentage = 1 - trap_percentage

        #Weighted off the sum assuming there are entries, multiplied by the percentage of each type
        if filler_percentage != 0:
            filler_percentages = self.percents_sum_100(filler_percentages)
            for each_filler in filler_percentages:
                filler_percentages[each_filler] *= filler_percentage
        if trap_percentage != 0:
            trap_percentages = self.percents_sum_100(trap_percentages)
            for each_trap in trap_percentages:
                trap_percentages[each_trap] *= trap_percentage
        
        #Create the percentage table for calculation
        self.filler_percent_table : dict[str, float] = {**filler_percentages, **trap_percentages}
        #Trim 0 entries
        self.filler_percent_table = {key:val for key, val in self.filler_percent_table.items() if val > 0}
        
        #Create the counter of filler items for comparision
        self.filler_item_counts : dict[str, int] = {}
        for each_entry in self.filler_percent_table:
            self.filler_item_counts[each_entry] = 0
        self.total_filler : float = 0.0


    def get_filler_item_name(self):
        output : str
        #Make sure there's 1 of every weighted item at minimum
        one_minimum = {key:val for key, val in self.filler_item_counts.items() if val == 0}
        if len(one_minimum) > 0:
            output = self.random.choice(list(one_minimum.keys()))
        else:
            #Create a table to see how far you are from the target percentage
            percentage_offsets : dict[str, float] = {}
            for each_item in self.filler_item_counts:
                #First, get the current actual item percentage
                each_percent = self.filler_item_counts[each_item] / self.total_filler
                #The offset is the target percentage minus the current percentage
                percentage_offsets[each_item] = self.filler_percent_table[each_item] - each_percent
            output = max(percentage_offsets, key=percentage_offsets.get)

        #Return the next expected item
        self.filler_item_counts[output] += 1
        self.total_filler += 1
        return output

    def next_garib_level(self) -> str:
        lowest_extra_garibs : int = 999
        levels_from_lowest_extras : list = []
        #Get the levels with the least extra garibs
        for each_garib_level in self.extra_garib_levels:
            #If it's the same number as the lowest extra garibs, append it
            if each_garib_level[1] == lowest_extra_garibs:
                levels_from_lowest_extras.append(each_garib_level)
            #If it's lower, it's the new standard
            elif each_garib_level[1] < lowest_extra_garibs:
                lowest_extra_garibs = each_garib_level[1]
                levels_from_lowest_extras = [each_garib_level]
        
        #Going with garibs of this name
        lowest_garib_count : int = 999
        levels_from_lowest_count : list = []
        for each_lowest_levels in levels_from_lowest_extras:
            for each_entry in self.garib_level_order:
                #Get the coresponding level order entry
                if each_entry[0] == each_lowest_levels[0]:
                    #Get the levels with the least garibs
                    if each_entry[1] < lowest_garib_count:
                        lowest_garib_count = each_entry[1]
                        levels_from_lowest_count = [each_lowest_levels]
                    elif each_entry[1] == lowest_garib_count:
                        levels_from_lowest_count.append(each_lowest_levels)
        
        #Now finally, from the levels with the least garibs and the least extra garib items, pick one at random
        chosen_level = self.random.choice(levels_from_lowest_count)
        #Get the index of it
        chosen_index : int = self.extra_garib_levels.index(chosen_level)

        #Note that you got a garib there, and return the name for use
        self.extra_garib_levels[chosen_index][1] += 1
        return self.extra_garib_levels[chosen_index][0]

    def garib_item_rules(self):
        #Garib items now combine with the garib sorting type and garib rules to create rules
        player : int = self.player

        #Unless you've set it to level garibs, in which case it's so straight forward it's done in JsonReader
        if self.options.garib_logic == GaribLogic.option_level_garibs:
            return
        #Filler Garibs
        if not self.options.bonus_levels and self.options.difficulty_logic == 0:
            for each_level in self.garib_level_order:
                #Ignore bonus levels if it's disabled
                if each_level[0].endswith("?"):
                    continue
                #At the next level
                level_all_garibs : Location = self.multiworld.get_location(each_level[0] + ": All Garibs", player)
                set_rule(level_all_garibs, lambda state: True)
        #Otherwise, start by the sorting method, since it has the most major effect on how garib rules act
        elif self.options.garib_sorting == GaribSorting.option_by_level:
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
                        if each_item.qty <= 0:
                            continue
                        if each_key.startswith(world_name):
                            garib_item_names.append(each_key)
                            garib_item_count += each_item.qty
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
            #Unlocking the bonus level doesn't ACTUALLY care about the star marks; it cares about all garibs in level
            all_garib_locations : list[Location] = []
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
                
                #Bonus unlocks require all levels with garibs
                if connecting_level_name.endswith(('1','2','3','?')) and entry_index < 4:
                    all_garib_locations.append(multiworld.get_location(connecting_level_name + ": All Garibs", player))
            
            #Getting all garibs from non-boss levels
            if self.options.bonus_levels:
                bonus_unlock_address : int | None = None
                if self.options.portalsanity:
                    bonus_unlock_address = 3100 + (world_index * 100)
                bonus_unlock : Location = Location(player, wayroom_name + ": Bonus Unlock", bonus_unlock_address, hubroom)
                hubroom.locations.append(bonus_unlock)
                #Makes bonus unlocks happen as vanilla
                if not self.options.portalsanity:
                   bonus_unlock.place_locked_item(self.create_event(wayroom_name + " Bonus Gate"))
                #Only require marks from levels that require garibs
                for each_all_garib_location in all_garib_locations:
                    add_rule(bonus_unlock, lambda state, required_garib_completion = each_all_garib_location.name: state.can_reach_location(required_garib_completion, player))

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

        hub_gates : list[str] = [
            "Hubworld Atlantis Gate",
            "Hubworld Carnival Gate",
            "Hubworld Pirate's Cove Gate",
            "Hubworld Prehistoric Gate",
            "Hubworld Fortress of Fear Gate",
            "Hubworld Out of This World Gate"
        ]

        if not self.options.portalsanity:
            final_location : Location = self.returning_crystal(castle_cave, 7)
            final_location.place_locked_item(self.create_event("Endscreen"))

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
            
            #Make the hubworld operate normally while portalsanity's off
            if not self.options.portalsanity:
                #The Thing
                crystal_location : Location | None = None
                match entrance_index:
                    case 0:
                        #Requires 1/7 Balls Returned
                        crystal_location = self.returning_crystal(castle_cave, 1)
                    case 1:
                        #Requires 2/7 Balls Returned
                        crystal_location = self.returning_crystal(castle_cave, 2, "A")
                    case 2:
                        #Requires 2/7 Balls Returned
                        crystal_location = self.returning_crystal(castle_cave, 2, "B")
                    case 3:
                        #Requires 4/7 Balls Returned
                        crystal_location = self.returning_crystal(castle_cave, 4, "A")
                    case 4:
                        #Requires 4/7 Balls Returned
                        crystal_location = self.returning_crystal(castle_cave, 4, "B")
                    case 5:
                        #Requires 6/7 Balls Returned
                        crystal_location = self.returning_crystal(castle_cave, 6)
                #Put the gate to it at the crystal location
                if crystal_location != None:
                    crystal_location.place_locked_item(self.create_event(hub_gates[entrance_index]))

    def extend_hint_information(self, hint_data : Dict[int, Dict[int, str]]):
        player = self.player
        if not self.options.entrance_randomizer:
            return
        hint_data[player] = {}
        #Go over the randomizable regions
        for vanilla_index, level_region_name in enumerate(self.existing_levels):
            #If it's in a vanilla position, don't flag the location as unique
            randomized_index = self.wayroom_entrances.index(level_region_name)
            if vanilla_index == randomized_index:
                continue
            entrance_name : str = self.existing_levels[randomized_index]
            #Get the current level region
            level_region : Region = self.get_region(level_region_name)
            for each_region in self.recursive_region_search([level_region]):
                for each_location in each_region.locations:
                    each_address = each_location.address
                    #Don't consider event locations, since they aren't hinted
                    if each_address == None:
                        continue
                    hint_data[player][each_address] = self.verbose_level_name(entrance_name)

    #Verbose
    def verbose_level_name(self, inLevel : str) -> str:
        level_suffix : str = inLevel[3:4]
        if level_suffix == "?":
            level_suffix = "Bonus"
        elif level_suffix == "!":
            level_suffix = "Boss"
        match self.world_from_string(inLevel):
            case 0:
                return "Atlantis " + level_suffix
            case 1:
                return "Carnival " + level_suffix
            case 2:
                return "Pirates Cove " + level_suffix
            case 3:
                return "Prehistoric " + level_suffix
            case 4:
                return "Fortress of Fear " + level_suffix
            case 5:
                return "Out of This World " + level_suffix
        return "Tutorial Well"
                

    #Get all regions contected to the exits of this region
    def recursive_region_search(self, known_regions : list[Region]) -> list[Region]:
        for each_region in known_regions:
            for each_exit in each_region.exits:
                #Stop Two-Way refrences from looping forever
                if not each_exit.connected_region in known_regions:
                    known_regions.append(each_exit.connected_region)
                    known_regions = self.recursive_region_search(known_regions)
        return known_regions

    #Puts the victory location
    def setup_victory(self):
        multiworld = self.multiworld
        player = self.player
        victory_condition = "ERROR"
        match self.options.victory_condition.value:
            case 1:
                castle_cave : Region = multiworld.get_region("Castle Cave", player)
                victory_condition = str(self.options.required_crystals.value) + " Balls Returned"
                victory_location : Location = self.returning_crystal(castle_cave, self.options.required_crystals.value, "G")
                victory_location.place_locked_item(self.create_event(victory_condition))
            case 2:
                menu : Region = multiworld.get_region("Menu", player)
                victory_location : Location = Location(player, "Golden Garibs Victory", None, menu)
                menu.locations.append(victory_location)
                rggs_to_win = self.options.required_golden_garibs.value
                victory_condition = str(rggs_to_win) + " Golden Garibs"
                victory_location.place_locked_item(self.create_event(victory_condition))
                set_rule(victory_location, lambda state, rgg = rggs_to_win: state.has("Golden Garib", player, rgg))
                print(victory_condition)
            case _:
                victory_condition = "Endscreen"
        multiworld.completion_condition[player] = lambda state: state.has(victory_condition, player)

    #Crystal return locations
    def returning_crystal(self, castle_cave : Region, required_balls : int, suffix : str = "") -> Location:
        player = self.player
        crystal_return_location : Location = Location(player, "Ball Turn-In " + str(required_balls) + suffix, None, castle_cave)
        castle_cave.locations.append(crystal_return_location)
        set_rule(crystal_return_location, lambda state, returned_balls_needed = required_balls - 1: state.has("Returned Balls", player, returned_balls_needed))
        return crystal_return_location

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
        if connecting_level_name in self.existing_levels:
            goal_or_boss : str = ": Goal"
            if connecting_level_name.endswith('!'):
                goal_or_boss = ": Boss"
            goal_location : Location = self.multiworld.get_location(connecting_level_name + goal_or_boss, player)
            psudo_goal_location : Location = Location(player, connecting_level_name + goal_or_boss + " Reached", None, goal_location.parent_region)
            goal_location.parent_region.locations.append(psudo_goal_location)
            set_rule(psudo_goal_location, lambda state, psudo_goal = goal_location.name: state.can_reach_location(psudo_goal, player))
            psudo_goal_location.place_locked_item(goal_item)
        
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
        if self.options.generate_puml:
            reachable_regions = self.multiworld.get_all_state().reachable_regions[self.player]
            unreachable_regions = []
            for each_region in self.multiworld.regions:
                if not each_region in reachable_regions:
                    unreachable_regions.append(each_region)
            visualize_regions(self.multiworld.get_region("Menu", self.player), "Glover.puml", regions_to_highlight=unreachable_regions)
        return super().connect_entrances()

    def build_options(self):
        options = {}
        options["victory_condition"] = self.options.victory_condition.value
        options["required_crystals"] = self.options.required_crystals.value
        options["required_golden_garibs"] = self.options.required_golden_garibs.value
        options["difficulty_logic"] = self.options.difficulty_logic.value
        options["death_link"] = self.options.death_link.value
        options["tag_link"] = self.options.tag_link.value
        options["trap_link"] = self.options.trap_link.value
        options["starting_ball"] = self.options.starting_ball.value
        options["garib_logic"] = self.options.garib_logic.value
        options["garib_sorting"] = self.options.garib_sorting.value
        options["entrance_randomizer"] = self.options.entrance_randomizer.value
        options["portalsanity"] = self.options.portalsanity.value
        options["randomized_spawns"] = self.options.spawning_checkpoint_randomizer.value
        options["bonus_levels"] = self.options.bonus_levels.value
        options["randomize_jump"] = self.options.randomize_jump.value
        options["include_power_ball"] = self.options.include_power_ball.value
        options["checkpoint_checks"] = self.options.checkpoint_checks.value
        options["switches_checks"] = self.options.switches_checks.value
        options["mr_tip_checks"] = self.options.mr_tip_checks.value
        options["enemysanity"] = self.options.enemysanity.value
        options["insectity"] = self.options.insectity.value
        options["easy_ball_walk"] = self.options.easy_ball_walk.value
        options["mr_hints"] = self.options.mr_hints.value
        options["mr_hints_scouts"] = self.options.mr_hints_scouts.value
        options["mr_tip_text_display"] = self.options.mr_tip_text_display.value
        options["chicken_hints"] = self.options.chicken_hints.value
        options["extra_garibs_value"] = self.options.extra_garibs_value.value

        options["player_name"] = self.multiworld.player_name[self.player]
        options["seed"] = self.random.randint(-6500000, 6500000)
        options["version"] = self.version
        return options

    def generate_hints(self):
        hint_groups = create_hints(self)
        self.mr_hints = hint_groups[0]
        self.chicken_hints = hint_groups[1]
        #Mr. Tip Hint Display Text
        if self.options.mr_tip_text_display.value == 1:
            self.mr_tip_text = hint_groups[2]
        if self.options.chicken_hints.value == 2:
            self.vague_chicken_text = hint_groups[3]
        else:
            self.vague_chicken_text = {}

    def generate_tip_text(self):
        #Mr. Tip Custom Text
        if self.options.mr_tip_text_display.value != 0:
            for each_tip in self.tip_locations:
                tip_address = str(self.multiworld.get_location(each_tip, self.player).address)
                if tip_address in self.mr_tip_text:
                    continue
                #Create unique tip text
                self.mr_tip_text[tip_address] = self.random.choice(self.mr_tip_table)

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
        options = self.build_options()
        self.generate_hints()
        self.generate_tip_text()
        options["mr_hints_locations"] = self.mr_hints
        options["mr_tips_text"] = self.mr_tip_text
        options["chicken_hints_locations"] = self.chicken_hints
        options["vague_chicken_text"] = self.vague_chicken_text
        options["world_lookup"] = self.lua_world_entry_lookup_table()
        options["garib_order"] = self.lua_decoupled_garib_order()
        options["spawning_checkpoints"] = self.spawn_checkpoint
        return options
