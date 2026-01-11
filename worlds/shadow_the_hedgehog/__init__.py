import copy
import math
import typing
from typing import ClassVar, Tuple, Any

from BaseClasses import Tutorial, CollectionState, Item, ItemClassification
from Options import OptionError
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess
#from .Items import ShadowTheHedgehogItem

#from .Levels import GetLevelCompletionNames
#from .Locations import *

from . import Options, Rules, Regions, Utils as ShadowUtils, Story, Names, Items, Locations, Levels
from .Options import shadow_option_groups, PercentOverrides, AutoClearMissions


def run_client():
    print("Running ShTHClient")
    from .ShTHClient import main

    launch_subprocess(main, name="ShThClient")


components.append(
    Component(
        "Shadow The Hedgehog Client",
        func=run_client,
        component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".shth"),
    )
)


class ShtHWebWorld(WebWorld):
    theme = "dirt"

    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Archipelago Shadow The Hedgehog software on your computer.",
            "English",
            "setup_en.md",
            "setup/en",
            ["choatix"],
        )
    ]

    option_groups = shadow_option_groups

class ShtHWorld(World):
    """
        Shadow The Hedgehog (also known as Shadow 05) allows the player to play through 23 stages
        with the ultimate lifeform, tracking down the answers to his past.
        But this time, it seems the past makes even less sense as nothing appears to be what it seems!
        Help Shadow find the truth and put a stop the his cursed past from coming back to haunt him!
    """
    #options_dataclass = ShThOptions
    #options: ShThOptions

    game: ClassVar[str] = "Shadow The Hedgehog"
    topology_present: bool = True

    item_name_to_id: ClassVar[typing.Dict[str, int]] = Items.GetItemDict()
    location_name_to_id: ClassVar[typing.Dict[str, int]] = Locations.GetLocationDict()

    required_client_version: Tuple[int, int, int] = (0, 5, 1)
    web = ShtHWebWorld()

    options_dataclass = Options.ShadowTheHedgehogOptions
    options: Options.ShadowTheHedgehogOptions

    item_name_groups = Items.get_item_groups()

    location_name_groups = Locations.getLocationGroups()



    def reinitialise(self):
        self.first_regions = []
        self.available_characters = []
        self.available_weapons = []
        self.go_mode_weapons_only = []
        self.available_levels = []
        self.available_story_levels = []
        self.available_select_stages = []
        self.token_locations = []
        self.required_tokens = {}
        self.excess_item_count = 0
        self.shuffled_story_mode = None
        self.random_value = None
        self.starting_items = []
        self.gates = {}

        for token in Items.TOKENS:
            self.required_tokens[token] = 0

    def __init__(self, *args, **kwargs):
        self.reinitialise()

        super(ShtHWorld, self).__init__(*args, **kwargs)

    def set_rules(self):
        Rules.set_rules(self.multiworld, self, self.player)

        sphere_one_useful = []
        if not hasattr(self.multiworld, "re_gen_passthrough"):
            while len(sphere_one_useful) == 0:
                sphere_one_locs = self.multiworld.get_reachable_locations(CollectionState(self.multiworld), self.player)
                sphere_one_useful = [s for s in sphere_one_locs if not s.locked]

                if len(sphere_one_useful) > 0:
                    break

                locked_items = [ c for c in sphere_one_locs if c.locked and c not in self.starting_items]
                for item in locked_items:
                    print("Locked item given:", item.item.name)
                    self.starting_items.append(item)
                    item = Item(item.item.name,ItemClassification.progression, None, self.player)
                    self.multiworld.push_precollected(item)

                if len(locked_items) != 0:
                    continue

                push_items = Regions.FindStartingItems(self, required=True)
                for item in push_items:
                    print("Push emergency item:", item)
                    self.starting_items.append(item)
                    self.multiworld.push_precollected(self.create_item(item))

        # Test here

        locs = self.get_locations()
        l_count = len([ l for l in locs if not l.locked ])
        l_x = Locations.count_locations(self)

        if l_count != l_x:
            print("Invalid location counting")

        player_items = [ a for a in self.multiworld.itempool if a.player == self.player ]
        if len(player_items) not in [l_count, l_x]:
            print("Invalid item pool vs locations")


    def check_invalid_configurations(self):

        not_excluded_stages = [x for x in Levels.ALL_STAGES if
                                   x not in Levels.BOSS_STAGES and x not in Levels.LAST_STORY_STAGES and
                                   Names.LEVEL_ID_TO_LEVEL[x] not in self.options.excluded_stages]
        if len(not_excluded_stages) == 0:
            raise OptionError("You cannot exclude all stages")


        #if self.options.story_shuffle == Options.StoryShuffle.option_chaos:
        #    self.options.story_shuffle = Options.StoryShuffle(Options.StoryShuffle.option_off)

        if self.options.auto_clear_missions and not self.options.objective_sanity or \
            (self.options.objective_sanity and not self.options.enemy_objective_sanity):
            self.options.auto_clear_missions = AutoClearMissions(False)

        if (self.options.weapon_sanity_hold == Options.WeaponsanityHold.option_unlocked
                and not self.options.weapon_sanity_unlock):
            self.options.weapon_sanity_hold = Options.WeaponsanityHold(Options.WeaponsanityHold.option_on)

        if self.options.level_progression == Options.LevelProgression.option_select and \
            self.options.starting_stages == 0:
            self.options.starting_stages = Options.StartingStages(1)

        if self.options.shadow_mod.value != Options.ShadowMod.option_vanilla and\
            self.options.character_sanity:
            raise OptionError("Unable to play charactersanity outside of vanilla")

        if self.options.shadow_mod.value == Options.ShadowMod.option_reloaded and \
            self.options.key_sanity:
            raise OptionError("Key/RSR sanity not supported in Reloaded at this time.")

        if self.options.story_shuffle == Options.StoryShuffle.option_off and \
            self.options.include_last_way_shuffle:

            # If story is off, last way cannot be shuffled
            self.options.include_last_way_shuffle = Options.IncludeLastStoryShuffle(False)

        if self.options.level_progression == Options.LevelProgression.option_select and \
            self.options.include_last_way_shuffle:

            # If story is off, last way cannot be shuffled
            self.options.include_last_way_shuffle = Options.IncludeLastStoryShuffle(False)

        if self.options.level_progression == Options.LevelProgression.option_select and \
            self.options.story_shuffle:

            # If story is off, last way cannot be shuffled
            self.options.story_shuffle = Options.StoryShuffle(False)

        if (not self.options.objective_sanity or
            not self.options.enemy_objective_sanity) and self.options.story_progression_balancing_passes > 0:
            self.options.story_progression_balancing_passes = Options.StoryProgressionBalancingPasses(0)

        if (self.options.story_progression_balancing_passes > 0  and
                self.options.level_progression == Options.LevelProgression.option_select):
            self.options.story_progression_balancing_passes = Options.StoryProgressionBalancingPasses(0)

        if self.options.level_progression != Options.LevelProgression.option_both and \
            self.options.select_percentage != 100:
            self.options.select_percentage = Options.SelectPercentage(100)

        if self.options.level_progression != Options.LevelProgression.option_select and not self.options.story_shuffle\
            and "Westopolis" in self.options.excluded_stages:
            raise OptionError("Westopolis stage cannot be excluded on story without shuffle enabled.")

        if self.options.level_progression == Options.LevelProgression.option_select or \
            not self.options.include_last_way_shuffle:
            if "The Last Way" in self.options.excluded_stages.value:
                self.options.excluded_stages.value.remove("The Last Way")

        if self.options.chaos_control_logic_level != Options.ChaosControlLogicLevel.option_off and \
            self.options.logic_level != Options.LogicLevel.option_hard:
                # TODO Handle expert? here in future:
            self.options.chaos_control_logic_level = Options.ChaosControlLogicLevel(Options.ChaosControlLogicLevel.option_off)

        if not self.options.enemy_objective_sanity and self.options.enemy_sanity:
            self.options.enemy_sanity = Options.Enemysanity(False)

        if self.options.enable_traps:
            if not self.options.poison_trap_enabled and not self.options.ammo_trap_enabled and not self.options.checkpoint_trap_enabled:
                self.options.enable_traps = Options.EnableTraps(False)

        if self.options.level_progression == Options.LevelProgression.option_story:
            self.options.select_gates = Options.SelectGates(Options.SelectGates.option_off)

    def calculate_non_objective_sanity_maximums(self):
        relevant_mission_clears =  [m for m in Locations.MissionClearLocations if
                                    (m.stageId, m.alignmentId) in [ (n[0], n[1]) for n in Locations.MINIMUM_STAGE_REQUIREMENTS ]
                                    and m.stageId in self.available_levels]
        for clear in relevant_mission_clears:
            min_requirement_item = [ n for n in Locations.MINIMUM_STAGE_REQUIREMENTS if
                                     n[0] == clear.stageId and \
                                     n[1] == clear.alignmentId][0]

            base_objective_data = ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_COMPLETION,
                                                          clear.mission_object_name, self.options,
                                                                            clear.stageId, clear.alignmentId,
                                                                            self.options.percent_overrides)

            type_value = base_objective_data[0]

            max_required = ShadowUtils.getMaxRequired(
                base_objective_data,
                clear.requirement_count, clear.stageId, clear.alignmentId,
                self.options.percent_overrides)

            if max_required <= min_requirement_item[2]:
                # print("YX", clear, min_requirement_item[2], max_required)
                # Change the value in override settings to increase manually

                key = ""
                if type_value == ShadowUtils.TYPE_ID_COMPLETION:
                    if clear.alignmentId == Levels.MISSION_ALIGNMENT_DARK:
                        key = "CD."+Levels.LEVEL_ID_TO_LEVEL[clear.stageId]
                    elif clear.alignmentId == Levels.MISSION_ALIGNMENT_HERO:
                        key = "CH."+Levels.LEVEL_ID_TO_LEVEL[clear.stageId]

                if type_value == ShadowUtils.TYPE_ID_OBJECTIVE_ENEMY_COMPLETION:
                    if clear.alignmentId == Levels.MISSION_ALIGNMENT_DARK:
                        key = "OECD."+Levels.LEVEL_ID_TO_LEVEL[clear.stageId]
                    elif clear.alignmentId == Levels.MISSION_ALIGNMENT_HERO:
                        key = "OECH."+Levels.LEVEL_ID_TO_LEVEL[clear.stageId]

                expected_base_value = math.ceil((min_requirement_item[2] + 1) * 100 / clear.requirement_count)

                while max_required <= min_requirement_item[2]:
                    if key not in self.options.percent_overrides or \
                        self.options.percent_overrides[key] < expected_base_value:
                        self.options.percent_overrides.value[key]  = expected_base_value
                    else:
                        self.options.percent_overrides.value[key] += 1
                    if self.options.percent_overrides.value[key] > 100:
                        raise OptionError("Unable to handle to avoid minimum requirements.")

                    max_required = ShadowUtils.getMaxRequired(
                        base_objective_data,
                        clear.requirement_count, clear.stageId, clear.alignmentId,
                        self.options.percent_overrides)


    def calculate_object_discrepancies(self):

        if type(self.options.percent_overrides) == PercentOverrides:
            override_settings = self.options.percent_overrides.value
        else:
            override_settings = self.options.percent_overrides

        for stage in Locations.ALL_STAGES:

            related_clears = [ c for c in Locations.MissionClearLocations if c.stageId == stage]
            related_es = [ e for e in Locations.GetEnemySanityLocations() if e.stageId == stage ]

            for clear in related_clears:
                clear_class = None
                alignment_id = None
                key_prefix = None

                if clear.mission_object_name == "Alien":
                    clear_class = Locations.ENEMY_CLASS_ALIEN
                    alignment_id = Locations.MISSION_ALIGNMENT_HERO
                    key_prefix = "EA"
                elif clear.mission_object_name == "Soldier":
                    clear_class = Locations.ENEMY_CLASS_GUN
                    alignment_id = Locations.MISSION_ALIGNMENT_DARK
                    key_prefix = "EG"

                if clear_class is not None:
                    aliens = [ r for r in related_es if r.enemyClass == clear_class ]
                    if len(aliens) == 0:
                        continue

                    aliens = aliens[0]

                    max_required_complete = ShadowUtils.getMaxRequired(
                        ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_COMPLETION, clear.mission_object_name, self.options,
                                                                  clear.stageId, clear.alignmentId, self.options.percent_overrides),
                                   clear.requirement_count, clear.stageId, clear.alignmentId,
                                       override_settings)


                    #override_total_complete = ShadowUtils.getOverwriteRequiredCount(override_settings, stage,
                     #                                                      alignment_id, ShadowUtils.TYPE_ID_COMPLETION)
                    #max_required_complete = ShadowUtils.getRequiredCount(clear.requirement_count, objective_percentage,
                    #                                            override=override_total_complete, round_method=floor)

                    d_count = aliens.total_count - max_required_complete

                    if d_count > 0:

                        max_required = ShadowUtils.getMaxRequired(
                            ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY,
                                                                      clear.mission_object_name, self.options,
                                                                      stage, alignment_id, self.options.percent_overrides),
                            aliens.total_count, stage, alignment_id,
                            override_settings)

                        if max_required > max_required_complete:
                            key = key_prefix + "." + Levels.LEVEL_ID_TO_LEVEL[stage]
                            override_settings[key] = (max_required_complete * 100) / aliens.total_count
                            #print("Had to adjust key for {key}".format(key=key))

    def generate_early(self):
        random_bytes = self.generate_random_bytes()
        self.random_value = int.from_bytes(random_bytes, byteorder='big')
        self.check_invalid_configurations()

        if self.options.single_egg_dealer:
            Regions.handle_single_boss(self, "Egg Dealer")
        if self.options.single_black_doom:
            Regions.handle_single_boss(self, "Black Doom")
        if self.options.single_diablon:
            Regions.handle_single_boss(self, "Diablon")

        if self.options.level_progression != Options.LevelProgression.option_select:
            self.shuffled_story_mode = Story.GetStoryMode(self)
        else:
            self.shuffled_story_mode = Story.DefaultStoryMode

        #Story.PrintStoryMode(self, None)

        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "Shadow The Hedgehog" in self.multiworld.re_gen_passthrough:
                self.reinitialise()
                passthrough = self.multiworld.re_gen_passthrough["Shadow The Hedgehog"]

                if "objective_sanity" in passthrough:
                    self.options.objective_sanity = passthrough["objective_sanity"]

                if "objective_percentage" in passthrough:
                    self.options.objective_percentage = passthrough["objective_percentage"]

                if "objective_enemy_percentage" in passthrough:
                    self.options.objective_enemy_percentage = passthrough["objective_enemy_percentage"]

                if "objective_completion_percentage" in passthrough:
                    self.options.objective_completion_percentage = passthrough["objective_completion_percentage"]

                if "objective_percentage" in passthrough:
                    self.options.objective_percentage = passthrough["objective_percentage"]

                if "objective_enemy_percentage" in passthrough:
                    self.options.objective_enemy_percentage = passthrough["objective_enemy_percentage"]

                if "objective_completion_enemy_percentage" in passthrough:
                    self.options.objective_completion_enemy_percentage = passthrough["objective_completion_enemy_percentage"]

                if "objective_item_percentage_available" in passthrough:
                    self.options.objective_item_percentage_available = passthrough["objective_item_percentage_available"]

                if "objective_item_enemy_percentage_available" in passthrough:
                    self.options.objective_item_enemy_percentage_available = passthrough["objective_item_enemy_percentage_available"]

                if "enemy_sanity_percentage" in passthrough:
                    self.options.enemy_sanity_percentage = passthrough["enemy_sanity_percentage"]

                if "checkpoint_sanity" in passthrough:
                    self.options.checkpoint_sanity = passthrough["checkpoint_sanity"]

                if "character_sanity" in passthrough:
                    self.options.character_sanity = passthrough["character_sanity"]

                if "required_mission_tokens" in passthrough:
                    self.options.required_mission_tokens = passthrough["required_mission_tokens"]

                if "required_hero_tokens" in passthrough:
                    self.options.required_hero_tokens = passthrough["required_hero_tokens"]

                if "required_dark_tokens" in passthrough:
                    self.options.required_dark_tokens = passthrough["required_dark_tokens"]

                if "required_final_tokens" in passthrough:
                    self.options.required_final_tokens = passthrough["required_final_tokens"]

                if "required_boss_tokens" in passthrough:
                    self.options.required_boss_tokens = passthrough["required_boss_tokens"]

                if "required_final_boss_tokens" in passthrough:
                    self.options.required_final_boss_tokens = passthrough["required_final_boss_tokens"]

                if "objective_completion_percentage" in passthrough:
                    self.options.objective_completion_percentage = passthrough["objective_completion_percentage"]

                if "requires_emeralds" in passthrough:
                    self.options.requires_emeralds = passthrough["requires_emeralds"]

                if "key_sanity" in passthrough:
                    self.options.key_sanity = passthrough["key_sanity"]

                if "key_collection_method" in passthrough:
                    self.options.key_collection_method = passthrough["key_collection_method"]

                if "keys_required_for_doors" in passthrough:
                    self.options.keys_required_for_doors = passthrough["keys_required_for_doors"]

                if "select_gates" in passthrough:
                    self.options.select_gates = passthrough["select_gates"]

                if "select_gates_count" in passthrough:
                    self.options.select_gates_count = passthrough["select_gates_count"]

                if "gate_unlock_requirement" in passthrough:
                    self.options.gate_unlock_requirement = passthrough["gate_unlock_requirement"]

                if "enemy_sanity" in passthrough:
                    self.options.enemy_sanity = passthrough["enemy_sanity"]

                if "weapon_sanity_unlock" in passthrough:
                    self.options.weapon_sanity_unlock = passthrough["weapon_sanity_unlock"]

                if "weapon_sanity_hold" in passthrough:
                    self.options.weapon_sanity_hold = passthrough["weapon_sanity_hold"]

                if "vehicle_logic" in passthrough:
                    self.options.vehicle_logic = passthrough["vehicle_logic"]

                if "override_settings" in passthrough:
                    print("override=", passthrough["override_settings"])
                    self.options.percent_overrides = passthrough["override_settings"]

                if "level_progression" in passthrough:
                    self.options.level_progression = passthrough["level_progression"]

                if "excluded_stages" in passthrough:
                    self.options.excluded_stages = passthrough["excluded_stages"]

                if "logic_level" in passthrough:
                    self.options.logic_level = passthrough["logic_level"]

                if "include_last_way_shuffle" in passthrough:
                    self.options.include_last_way_shuffle = passthrough["include_last_way_shuffle"]

                if "story_boss_count" in passthrough:
                    self.options.story_boss_count = passthrough["story_boss_count"]

                if "story_shuffle" in passthrough:
                    self.options.story_shuffle = passthrough["story_shuffle"]

                if "select_bosses" in passthrough:
                    self.options.select_bosses = passthrough["select_bosses"]

                if "minimum_rank" in passthrough:
                    self.options.minimum_rank = passthrough["minimum_rank"]

                if "enemy_frequency" in passthrough:
                    self.options.enemy_frequency = passthrough["enemy_frequency"]

                if "objective_frequency" in passthrough:
                    self.options.objective_frequency = passthrough["objective_frequency"]

                if "enemy_objective_frequency" in passthrough:
                    self.options.enemy_objective_frequency = passthrough["enemy_objective_frequency"]

                if "secret_story_progression" in passthrough:
                    self.options.secret_story_progression = passthrough["secret_story_progression"]

                if "goal_missions" in passthrough:
                    self.options.goal_missions = passthrough["goal_missions"]

                if "goal_final_missions" in passthrough:
                    self.options.goal_final_missions = passthrough["goal_final_missions"]

                if "goal_hero_missions" in passthrough:
                    self.options.goal_hero_missions = passthrough["goal_hero_missions"]

                if "goal_dark_missions" in passthrough:
                    self.options.goal_dark_missions = passthrough["goal_dark_missions"]

                if "goal_objective_missions" in passthrough:
                    self.options.goal_objective_missions = passthrough["goal_objective_missions"]

                if "goal_bosses" in passthrough:
                    self.options.goal_bosses = passthrough["goal_bosses"]

                if "goal_final_bosses" in passthrough:
                    self.options.goal_final_bosses = passthrough["goal_final_bosses"]

                if "shuffled_story_mode" in passthrough:
                    self.shuffled_story_mode = Story.StringToStory(passthrough["shuffled_story_mode"])

                if "gates" in passthrough:
                    self.gates = passthrough["gates"]

                if "gate_requirements" in passthrough:
                    self.gate_requirements = passthrough["gate_requirements"]

                if "shadow_mod" in passthrough:
                    self.options.shadow_mod = passthrough["shadow_mod"]

                if "weapon_groups" in passthrough:
                    self.options.weapon_groups = passthrough["weapon_groups"]

                if "single_egg_dealer" in passthrough:
                    self.options.single_egg_dealer = passthrough["single_egg_dealer"]

                if "single_black_doom" in passthrough:
                    self.options.single_black_doom = passthrough["single_black_doom"]

                if "single_diablon" in passthrough:
                    self.options.single_diablon = passthrough["single_diablon"]

                if "boss_logic_level" in passthrough:
                    self.options.boss_logic_level = passthrough["boss_logic_level"]

                if "craft_logic_level" in passthrough:
                    self.options.craft_logic_level = passthrough["craft_logic_level"]

                if "starting_level_method" in passthrough:
                    self.options.starting_level_method = passthrough["starting_level_method"]

                if "object_unlocks" in passthrough:
                    self.options.object_unlocks = passthrough["object_unlocks"]

                if "object_pulleys" in passthrough:
                    self.options.object_pulleys = passthrough["object_pulleys"]

                if "object_ziplines" in passthrough:
                    self.options.object_zipline = passthrough["object_ziplines"]

                if "object_rockets" in passthrough:
                    self.options.object_rockets = passthrough["object_rockets"]

                if "object_light_dashes" in passthrough:
                    self.options.object_light_dashes = passthrough["object_light_dashes"]

                if "object_warp_holes" in passthrough:
                    self.options.object_warp_holes = passthrough["object_warp_holes"]

                if "shadow_boxes" in passthrough:
                    self.options.shadow_boxes = passthrough["shadow_boxes"]

                if "energy_cores" in passthrough:
                    self.options.energy_cores = passthrough["energy_cores"]

                if "door_sanity" in passthrough:
                    self.options.door_sanity = passthrough["door_sanity"]

                if "gold_beetle_sanity" in passthrough:
                    self.options.gold_beetle_sanity = passthrough["gold_beetle_sanity"]

                if "plando_starting_stages" in passthrough:
                    self.options.plando_starting_stages = passthrough["plando_starting_stages"]

                if "story_and_select_start_together" in passthrough:
                    self.options.story_and_select_start_together = passthrough["story_and_select_start_together"]

                if "objective_sanity_system" in passthrough:
                    self.options.objective_sanity_system = passthrough["objective_sanity_system"]

                if "objective_sanity_behaviour" in passthrough:
                    self.options.objective_sanity_behaviour = passthrough["objective_sanity_behaviour"]

                if "chaos_control_logic_level" in passthrough:
                    self.options.chaos_control_logic_level = passthrough["chaos_control_logic_level"]

                if "difficult_enemy_sanity" in passthrough:
                    self.options.difficult_enemy_sanity = passthrough["difficult_enemy_sanity"]

                if "exclude_go_mode_items" in passthrough:
                    self.options.exclude_go_mode_items = passthrough["exclude_go_mode_items"]

                if "first_levels" in passthrough:
                    self.first_regions = passthrough["first_levels"]

                if "boss_enemy_sanity" in passthrough:
                    self.options.boss_enemy_sanity = passthrough["boss_enemy_sanity"]

                if "item_sanity" in passthrough:
                    self.options.item_sanity = passthrough["item_sanity"]

        # Set maximum of levels required
        # Exclude missions listed in exclude_locations
        maximum_force_missions = self.options.force_objective_sanity_max.value
        maximum_force_mission_counter = self.options.force_objective_sanity_max_counter.value

        mission_counter = 0
        mission_total = 0

        Regions.early_region_checks(self)

        if not hasattr(self.multiworld, "re_gen_passthrough"):
            Regions.DetermineFirstStages(self)
            self.gates = Regions.DetermineGates(self)
            self.gate_requirements = {}

        if not hasattr(self.multiworld, "re_gen_passthrough") and self.options.starting_level_method == Options.StartingLevelMethod.option_stage_and_item:
            extra_items = Regions.FindStartingItems(self, required=False)
            for item in extra_items:
                self.starting_items.append(item)
                self.multiworld.push_precollected(self.create_item(item))

        if self.options.level_progression != Options.LevelProgression.option_select and \
            self.options.story_progression_balancing_passes > 0 and not hasattr(self.multiworld, "re_gen_passthrough"):

            balancing_overrides = {}
            for i in range(0, self.options.story_progression_balancing_passes):
                story_spheres = Story.DecideStoryPath(self, self.shuffled_story_mode)
                new_overrides, new_available_overrides = Story.AlterOverridesForStoryPath(story_spheres,self.options)

                for override in new_overrides.items():
                    if override[0] in balancing_overrides and balancing_overrides[override[0]] <= override[1]:
                        continue
                    balancing_overrides[override[0]] = override[1]

                for override in new_available_overrides.items():
                    if override[0] in balancing_overrides and balancing_overrides[override[0]] >= override[1]:
                        continue

                    balancing_overrides[override[0]] = override[1]

            for override in balancing_overrides.items():
                self.options.percent_overrides.value[override[0]] = override[1]

        if not self.options.objective_sanity:
            self.calculate_non_objective_sanity_maximums()

        item_count = Items.CountItems(self)
        location_count = Locations.count_locations(self)

        if self.options.exceeding_items_filler != Options.ExceedingItemsFiller.option_off:
            if item_count > location_count:
                #print("item_count=", item_count, "location_count=", location_count)
                potential_downgrades, removals = Items.GetPotentialDowngradeItems(self)
                if len(potential_downgrades) < item_count - location_count - len(removals):
                    c = item_count - location_count - len(potential_downgrades)
                    print("Issue with counts", item_count, location_count, len(potential_downgrades),
                          len(removals), c)

                    # Throw random items into start inventory, if disabled, throw an error
                    if not self.options.start_inventory_excess_items:
                        raise OptionError("Not enough locations to fill even with downgrades::"+str(c))

                self.excess_item_count = item_count - location_count

        elif self.options.exceeding_items_filler == Options.ExceedingItemsFiller.option_off and \
            location_count < item_count and not self.options.start_inventory_excess_items:
            raise OptionError("Invalid count of items present:"+str(location_count)+" vs "+str(item_count))

        for missionClear in Locations.MissionClearLocations:

            if missionClear.requirement_count is None:
                continue

            max_required_objective = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE,
                                                          missionClear.mission_object_name, self.options,
                                                          missionClear.stageId, missionClear.alignmentId, self.options.percent_overrides),
                missionClear.requirement_count, missionClear.stageId, missionClear.alignmentId,
                self.options.percent_overrides)

            if max_required_objective > missionClear.requirement_count and not self.options.allow_dangerous_settings:
                raise OptionError("Dangerous objective value set!")

        for enemy in Locations.GetEnemySanityLocations():
            max_required_enemy = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY,
                                                          enemy.mission_object_name, self.options,
                                                          enemy.stageId, enemy.enemyClass, self.options.percent_overrides),
                enemy.total_count, enemy.stageId, enemy.enemyClass, self.options.percent_overrides)

            if max_required_enemy > enemy.total_count and not self.options.allow_dangerous_settings:
                raise OptionError("Dangerous enemy value set!")

        if not self.options.objective_sanity and self.options.enemy_sanity:
            self.calculate_object_discrepancies()

        if self.options.objective_sanity and self.options.force_objective_sanity_chance > 0\
                and self.options.force_objective_sanity_max > 0:

            MissionLocations = copy.deepcopy(Locations.MissionClearLocations)
            self.random.shuffle(MissionLocations)

            for locationData in MissionLocations:
                if locationData.requirement_count is None:
                    continue
                if locationData.requirement_count == 1:
                    continue
                if mission_counter >= maximum_force_missions:
                    continue
                if locationData.requirement_count + mission_total > maximum_force_mission_counter:
                    continue

                location_id, completion_location_name = Levels.GetLevelCompletionNames(locationData.stageId, locationData.alignmentId)

                if completion_location_name in self.options.exclude_locations:
                    continue

                chance = self.options.force_objective_sanity_chance

                hero_ratio_base = self.options.goal_hero_missions + 1
                dark_ratio_base = self.options.goal_dark_missions + 1

                if locationData.alignmentId == Levels.MISSION_ALIGNMENT_DARK:
                    higher_value = (1 - pow((1 - (chance / 100)), math.sqrt(dark_ratio_base / hero_ratio_base))) * 100
                    ratio_of_change = chance / higher_value
                    if dark_ratio_base >= hero_ratio_base:
                        chance = math.ceil(higher_value)
                    else:
                        chance = math.floor(chance / ratio_of_change)
                elif locationData.alignmentId == Levels.MISSION_ALIGNMENT_HERO:
                    higher_value = (1 - pow((1 - (chance / 100)), math.sqrt(hero_ratio_base / dark_ratio_base))) * 100
                    ratio_of_change = chance / higher_value
                    if hero_ratio_base >= dark_ratio_base:
                        chance = math.ceil(higher_value)
                    else:
                        chance = math.floor(chance / ratio_of_change)

                r = self.multiworld.random.randrange(0, 100)
                if r > 100 - chance:
                    self.options.priority_locations.value.add(completion_location_name)
                    mission_counter += 1
                    mission_total += locationData.requirement_count


    def create_regions(self):
        regions = Regions.create_regions(self)
        Locations.create_locations(self, regions)
        self.multiworld.regions.extend(regions.values())

        if self.options.level_progression != Options.LevelProgression.option_story:
            for first_region in self.first_regions:
                stage_item = Items.GetStageUnlockItem(first_region)
                self.multiworld.push_precollected(self.create_item(stage_item))



    @staticmethod
    def interpret_slot_data(slot_data: typing.Dict[str, Any]) -> typing.Dict[str, Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        # we are using re_gen_passthrough over modifying the world here due to complexities with ER

        if "shuffled_story_mode" in slot_data:
            pass
            #self.shuffled_story_mode = Story.StringToStory(slot_data["shuffled_story_mode"])

        return slot_data

    def create_item(self, name: str) -> "Items.ShadowTheHedgehogItem":
        info = Items.GetItemByName(name)
        return Items.ShadowTheHedgehogItem(info, self.player)

    def create_items(self):
        Items.PopulateItemPool(self)

    def get_filler_item_name(self) -> str:
        # Use the same weights for filler items that are used in the base randomizer.
        #random, junk, traps, options, junk_count, available_weapons
        item_info = Items.ChooseJunkItems(self.random, Items.GetJunkItemInfo(), Items.GetTraps(), self.options, 1,
                                          self.available_weapons)[0]
        return item_info.name


    def get_pre_fill_items(self):
        res = []

        return res

    def generate_random_bytes(self):
        return self.multiworld.random.randbytes(8)


    def fill_slot_data(self):
        slot_data = {
            "check_level": None if len(self.first_regions) == 0 else self.first_regions[0],
            "first_levels": self.first_regions,

            "objective_sanity": self.options.objective_sanity.value,
            "objective_percentage": self.options.objective_percentage.value,
            "objective_enemy_percentage": self.options.objective_enemy_percentage.value,
            "objective_completion_percentage": self.options.objective_completion_percentage.value,
            "objective_completion_enemy_percentage": self.options.objective_completion_enemy_percentage.value,
            "objective_item_percentage_available": self.options.objective_item_percentage_available.value,
            "objective_item_enemy_percentage_available": self.options.objective_item_enemy_percentage_available.value,
            "enemy_sanity_percentage": self.options.enemy_sanity_percentage.value,

            "checkpoint_sanity": self.options.checkpoint_sanity.value,
            "character_sanity": self.options.character_sanity.value,

            "required_mission_tokens": self.required_tokens[Items.Progression.StandardMissionToken],
            "required_hero_tokens": self.required_tokens[Items.Progression.StandardHeroToken],
            "required_dark_tokens": self.required_tokens[Items.Progression.StandardDarkToken],
            "required_final_tokens": self.required_tokens[Items.Progression.FinalToken],
            "required_objective_tokens": self.required_tokens[Items.Progression.ObjectiveToken],
            "required_boss_tokens": self.required_tokens[Items.Progression.BossToken],
            "required_final_boss_tokens": self.required_tokens[Items.Progression.FinalBossToken],
            "requires_emeralds": self.options.goal_chaos_emeralds.value,
            "key_sanity": self.options.key_sanity.value,
            "key_collection_method": self.options.key_collection_method.value,
            "keys_required_for_doors": self.options.keys_required_for_doors.value,
            "gates": self.gates,
            "gate_requirements": self.gate_requirements,
            "select_gates": self.options.select_gates.value,
            "select_gates_count": self.options.select_gates_count.value,
            "gate_unlock_requirement": self.options.gate_unlock_requirement.value,

            "enemy_sanity": self.options.enemy_sanity.value,
            "enemy_objective_sanity": self.options.enemy_objective_sanity.value,
            "weapon_sanity_unlock": self.options.weapon_sanity_unlock.value,
            "weapon_sanity_hold": self.options.weapon_sanity_hold.value,
            "vehicle_logic": self.options.vehicle_logic.value,
            "ring_link": self.options.ring_link.value,
            "auto_clear_missions": self.options.auto_clear_missions.value,
            "story_mode_available": self.options.level_progression != Options.LevelProgression.option_select,
            "select_mode_available": self.options.level_progression != Options.LevelProgression.option_story,
            "required_client_version": ShadowUtils.GetVersionString(),
            "override_settings": self.options.percent_overrides.value,
            "shuffled_story_mode": Story.StoryToString(self.shuffled_story_mode),
            "level_progression": self.options.level_progression.value,
            "excluded_stages": self.options.excluded_stages.value,
            "logic_level": self.options.logic_level.value,
            "enable_gauge_items": self.options.enable_gauge_items.value,
            "exceeding_items_filler": self.options.exceeding_items_filler.value,
            "include_last_way_shuffle": self.options.include_last_way_shuffle.value,
            "story_shuffle": self.options.story_shuffle.value,
            "story_boss_count": self.options.story_boss_count.value,
            "secret_story_progression": self.options.secret_story_progression.value,
            "select_bosses": self.options.select_bosses.value,
            "minimum_rank": self.options.minimum_rank.value,
            "enemy_frequency": self.options.enemy_frequency.value,
            "objective_frequency": self.options.objective_frequency.value,
            "enemy_objective_frequency": self.options.enemy_objective_frequency.value,
            "goal_missions": self.options.goal_missions.value,
            "goal_final_missions": self.options.goal_final_missions.value,
            "goal_hero_missions": self.options.goal_hero_missions.value,
            "goal_dark_missions": self.options.goal_dark_missions.value,
            "goal_objective_missions": self.options.goal_objective_missions.value,
            "goal_bosses": self.options.goal_bosses.value,
            "goal_final_bosses": self.options.goal_final_bosses.value,
            "shadow_mod": self.options.shadow_mod.value,
            "weapon_groups": self.options.weapon_groups.value,
            "single_egg_dealer": self.options.single_egg_dealer.value,
            "single_black_doom": self.options.single_black_doom.value,
            "single_diablon": self.options.single_diablon.value,
            "boss_logic_level": self.options.boss_logic_level.value,
            "craft_logic_level": self.options.craft_logic_level.value,
            "starting_level_method": self.options.starting_level_method.value,
            "save_value": self.random_value,

            "object_unlocks": self.options.object_unlocks.value,
            "object_pulleys": self.options.object_pulleys.value,
            "object_ziplines": self.options.object_ziplines.value,
            "object_units": self.options.object_units.value,
            "object_rockets": self.options.object_rockets.value,
            "object_light_dashes": self.options.object_light_dashes.value,
            "object_warp_holes": self.options.object_warp_holes.value,
            "shadow_boxes": self.options.shadow_boxes.value,
            "energy_cores": self.options.energy_cores.value,
            "door_sanity": self.options.door_sanity.value,
            "gold_beetle_sanity": self.options.gold_beetle_sanity.value,
            "plando_starting_stages": self.options.plando_starting_stages.value,
            "story_and_select_start_together": self.options.story_and_select_start_together.value,
            "objective_sanity_system": self.options.objective_sanity_system.value,
            "objective_sanity_behaviour": self.options.objective_sanity_behaviour.value,
            "chaos_control_logic_level": self.options.chaos_control_logic_level.value,
            "difficult_enemy_sanity": self.options.difficult_enemy_sanity.value,
            "exclude_go_mode_items": self.options.exclude_go_mode_items.value,
            "boss_enemy_sanity": self.options.boss_enemy_sanity.value,
            "item_sanity": self.options.item_sanity.value
        }

        return slot_data

    def PrintGates(self, spoiler_handle, gates, gate_requirements):
        if spoiler_handle is not None:
            spoiler_handle.write(f"{self.multiworld.get_player_name(self.player)}'s Gate Unlocks\n")
            for gate_number, gate_stages in gates.items():
                spoiler_handle.write(f"Gate {gate_number} = {gate_stages}\n")

            spoiler_handle.write("\n")

            spoiler_handle.write(f"{self.multiworld.get_player_name(self.player)}'s Gate Requirements\n")
            for gate_number, requirements in gate_requirements.items():
                spoiler_handle.write(f"Gate {gate_number} = {requirements}\n")

            spoiler_handle.write("\n")



    def write_spoiler(self, spoiler_handle: typing.TextIO):
        if self.options.story_shuffle != Options.StoryShuffle.option_off:
            Story.PrintStoryMode(self, spoiler_handle)

        if self.options.select_gates != Options.SelectGates.option_off:
            self.PrintGates(spoiler_handle, self.gates, self.gate_requirements)


