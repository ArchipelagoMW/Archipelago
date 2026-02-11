from typing import TextIO, Callable, Any

from BaseClasses import *
from worlds.AutoWorld import World, WebWorld
from . import csvdata
from .constants import *
from .csvdata import *  # type: ignore
from .items import *  # type: ignore
from .logic_mapping_sonic import *
from .options import *  # type: ignore
from .regions import *


class SonicHeroesWeb(WebWorld):
    theme = PARTYTIMETHEME
    setup_en = (Tutorial(
        tutorial_name=TUTORIALNAME,
        description=TUTORIALDESC,
        language=TUTORIALLANGUAGE,
        file_name=TUTORIALFILENAME,
        link=TUTORIALLINK,
        authors=TUTORIALAUTHORS
    ))

    tutorials = [setup_en]
    #option_groups = sonic_heroes_option_groups
    game_info_languages = ["en"]
    #option_groups = sonic_heroes_option_groups

class SonicHeroesWorld(World):
    """
    Sega's legendary mascot makes his historical multi-platform debut, and this time the adventure comes with several all-new gameplay twists. Control 3 playable characters simultaneously, using Sonic's speed, Knuckles' power, and tails' ability to fly as you explore massive worlds. Team-based gameplay lets you as one of 4 teams for a total of 12 playable characrters, each with their own unique signature moves. Each team boasts multiple special stages with unique missions, as well as their own story using each character's special powers. Sonic and his friends combine forces to battle the ultimate evil.
    """
    game: ClassVar[str] = SONICHEROES
    web: ClassVar[WebWorld] = SonicHeroesWeb()
    options_dataclass = SonicHeroesOptions
    options: SonicHeroesOptions
    item_name_to_id: ClassVar[dict[str, int]] = \
    {item.name: item.code for item in itemList}
    location_name_to_id: ClassVar[dict[str, int]] = {loc.name: loc.code for loc in get_full_location_list()}
    #{k: v for k, v in full_location_dict.items()}

    item_name_groups: ClassVar[dict[str, set[str]]] = item_groups
    location_name_groups: ClassVar[dict[str, set[str]]] = location_groups
    topology_present: bool = True

    #UT Stuff Here
    ut_can_gen_without_yaml: bool = True

    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return slot_data


    def __init__(self, multiworld: MultiWorld, player: int):
        #PUT STUFF HERE
        #self.loc_id_to_loc = {}

        self.secret = False

        self.level_goal_event_locations: list[str] = []
        self.team_level_goal_event_locations: dict[str, list[str]] = {}
        self.bonus_key_event_items_per_team: dict[str, dict[str, list[str]]] = {}
        self.region_to_location: dict[str, list[LocationCSVData]] = {}
        self.region_list: list[RegionCSVData] = []
        self.connection_list: list[ConnectionCSVData] = []
        #self.logic_mapping_dict: dict[str, dict[str, dict[str, CollectionState]]] = {}

        self.full_logic_mapping_dict: RejectDictionaryReturnToMonke[str, CollectionState] = RejectDictionaryReturnToMonke()  # type: ignore

        self.spoiler_string: str = ""
        self.extra_items: int = 0

        self.regular_regions: list[str] = \
        [
            OCEANREGION,
            HOTPLANTREGION,
            CASINOREGION,
            TRAINREGION,
            BIGPLANTREGION,
            GHOSTREGION,
            SKYREGION,
        ]

        self.enabled_teams: list[str] = \
        [
            #SONIC,
            #DARK,
            #ROSE,
            #CHAOTIX,
            #SUPERHARD,
        ]

        self.regular_levels: list[str] = \
        [
            SEASIDEHILL,
            OCEANPALACE,
            GRANDMETROPOLIS,
            POWERPLANT,
            CASINOPARK,
            BINGOHIGHWAY,
            RAILCANYON,
            BULLETSTATION,
            FROGFOREST,
            LOSTJUNGLE,
            HANGCASTLE,
            MYSTICMANSION,
            EGGFLEET,
            FINALFORTRESS,
        ]

        self.emerald_locations_added: list[str] = []
        self.boss_locations_added: list[str] = []#\
        #self.gate_num_to_boss_region:

        self.regular_boss_levels = \
        [
            EGGHAWK,
            TEAMFIGHT1,
            ROBOTCARNIVAL,
            EGGALBATROSS,
            TEAMFIGHT2,
            ROBOTSTORM,
            EGGEMPEROR,
        ]


        #self.allowed_levels: list[str] = []

        self.allowed_levels_per_team: dict[str, list[str]] = {}

        #self.should_make_puml: bool = True
        self.should_make_puml_earlier: bool = False
        self.highlight_unreachable_regions: bool = True

        self.is_ut_gen: bool = False

        self.legacy_gates_mode: bool = False

        self.bonus_keys_needed_for_bonus_stage: int = 1
        self.apworldversion: str = "2.1.0"
        #self.goal_unlock_conditions: set[str] = set()

        self.emblems_to_create: int = 0
        self.required_emblems_ratio: float = 0.8
        self.level_block_emblem_count: int = 14

        self.gate_emblem_costs: list[int] = []
        self.shuffled_levels: list[str] = []
        self.shuffled_bosses: list[str] = []
        self.gate_level_counts: list[int] = []

        super().__init__(multiworld, player)


    def create_item(self, name: str) -> "Item":
        tempitems = [x for x in itemList if x.name == name]
        if len(tempitems) == 0:
            return SonicHeroesItem(name, ItemClassification.progression, self.item_name_to_id[name], self.player)
        return SonicHeroesItem(name, tempitems[0].classification, self.item_name_to_id[name], self.player)


    def generate_early(self) -> None:


        #UT Stuff Here
        self.handle_ut_yamlless(None)

        # Check invalid options here
        check_invalid_options(self)

        #change stuff based on options
        self.handle_option_checking()


        if self.options.unlock_type == UnlockType.option_legacy_level_gates:
            self.handle_level_gates_start()


        """
        #UT Stuff Here
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if SONICHEROES not in self.multiworld.re_gen_passthrough:
                return
            passthrough = self.multiworld.re_gen_passthrough[SONICHEROES]
            self.options.goal_unlock_condition = passthrough["goal_unlock_condition"]
        """

        create_special_region_csv_data(self)

        if SONIC in self.enabled_teams:
            self.init_logic_mapping_sonic()

        #dont need other teams as only rules are empty string


        for team in self.enabled_teams:
            #import csv data
            self.import_csv_data(team)

            # level completion event locs
            self.team_level_goal_event_locations[team] = []
            self.bonus_key_event_items_per_team[team] = {}

            for level in self.allowed_levels_per_team[team]:
                self.bonus_key_event_items_per_team[team][level] = []

            #map regions
            #map_sonic_regions(self)
            #map locations
            #map_sonic_locations(self)
            #map connections
            #map_sonic_connections(self)

        pass


    def create_regions(self) -> None:
        create_regions(self)

        victory_item = SonicHeroesItem(VICTORYITEM, ItemClassification.progression,
                                       None, self.player)
        self.get_location(VICTORYLOCATION).place_locked_item(victory_item)

        #print(self.level_goal_event_locations)

        index = 1 if self.secret else 0

        for team in self.allowed_levels_per_team.keys():
            for loc_name in self.team_level_goal_event_locations[team]:
                #global level completion
                goal_unlock_item = SonicHeroesItem(f"{LEVEL} {COMPLETIONEVENT}", ItemClassification.progression, None, self.player)
                self.get_location(f"{loc_name} {team} Goal Event Location").place_locked_item(goal_unlock_item)

                #level completion for team
                goal_unlock_item = SonicHeroesItem(f"{team} {loc_name} {COMPLETIONEVENT}", ItemClassification.progression, None, self.player)
                self.get_location(f"{loc_name} {team} Goal Event Location For Team").place_locked_item(goal_unlock_item)

            for level in self.allowed_levels_per_team[team]:
                for key in range(bonus_key_amounts[team][level][index]):
                    self.bonus_key_event_items_per_team[team][level].append(f"{team} {level} Bonus Key #{key + 1} Event")
                    key_event_item = SonicHeroesItem(f"{team} {level} Bonus Key #{key + 1} Event", ItemClassification.progression, None, self.player)
                    self.get_location(f"{level} {team} Bonus Key {key + 1} Event").place_locked_item(key_event_item)


        #boss events
        if self.options.unlock_type == UnlockType.option_legacy_level_gates:
            for gate_num, boss in enumerate(self.boss_locations_added):
                boss_event_item = SonicHeroesItem(f"Gate {gate_num} Boss: {boss}", ItemClassification.progression, None, self.player)
                #print(f"Looking for Event Location: {boss} Event Location")
                self.get_location(f"{boss} Event Location").place_locked_item(boss_event_item)
        pass


    def create_items(self) -> None:
        create_items(self)

        if self.options.unlock_type == UnlockType.option_ability_character_unlocks:
            if self.options.sonic_story_starting_character == SonicStoryStartingCharacter.option_sonic:
                self.multiworld.push_precollected(self.create_item(PLAYABLESONIC))
            elif self.options.sonic_story_starting_character == SonicStoryStartingCharacter.option_tails:
                self.multiworld.push_precollected(self.create_item(PLAYABLETAILS))
            elif self.options.sonic_story_starting_character == SonicStoryStartingCharacter.option_knuckles:
                self.multiworld.push_precollected(self.create_item(PLAYABLEKNUCKLES))
            else:
                print("Cannot Determine Starting Character. Please Help")
        pass


    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has(VICTORYITEM, self.player)
        pass


    def connect_entrances(self) -> None:
        connect_entrances(self)
        pass


    def generate_basic(self) -> None:
        pass


    def pre_fill(self) -> None:
        #self.make_puml()
        pass


    def post_fill(self) -> None:
        if self.should_make_puml_earlier:
            self.make_puml()
        pass


    def generate_output(self, output_directory: str) -> None:
        pass


    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]) -> None:
        #Location: "Hint"
        pass


    def fill_slot_data(self) -> Mapping[str, Any]:
        if self.options.make_puml:
            self.make_puml()


        if self.options.unlock_type == UnlockType.option_ability_character_unlocks:
            self.gate_emblem_costs = [0]
            self.shuffled_levels = [f"S{x}" for x in range(2, 16)]
            self.shuffled_bosses = ["B23"]
            self.gate_level_counts = [14]

        return \
        {
            "APWorldVersion": self.apworldversion,

            "IncludedLevelsAndSanities": self.options.included_levels_and_sanities.value,
            "UnlockType": self.options.unlock_type.value,
            "AbilityUnlocks": self.options.ability_unlocks.value,
            "LegacyNumberOfLevelGates": self.options.legacy_number_of_level_gates.value,
            "LegacyLevelGatesAllowedBosses": self.options.legacy_level_gates_allowed_bosses.value,
            "RequiredRank": self.options.required_rank.value,

            "FinalBoss": self.options.final_boss.value,
            "GoalUnlockConditions": self.options.goal_unlock_conditions.value,
            "GoalLevelCompletions": self.options.goal_level_completions.value,
            "GoalLevelCompletionsPerStory": self.options.goal_level_completions_per_story.value,


            #"SonicStory": self.options.sonic_story.value,
            "SonicStoryStartingCharacter": self.options.sonic_story_starting_character.value,
            #"SonicKeySanity": self.options.sonic_key_sanity.value,
            #"SonicCheckpointSanity": self.options.sonic_checkpoint_sanity.value,


            #"DarkStory": self.options.dark_story.value,
            "DarkSanity": self.options.dark_sanity.value,
            "DarkStoryStartingCharacter": self.options.dark_story_starting_character.value,
            #"DarkKeySanity": self.options.dark_key_sanity.value,
            #"DarkCheckpointSanity": self.options.dark_checkpoint_sanity.value,

            #"RoseStory": self.options.rose_story.value,
            "RoseSanity": self.options.rose_sanity.value,
            "RoseStoryStartingCharacter": self.options.rose_story_starting_character.value,
            #"RoseKeySanity": self.options.rose_key_sanity.value,
            #"RoseCheckpointSanity": self.options.rose_checkpoint_sanity.value,

            #"ChaotixStory": self.options.chaotix_story.value,
            "ChaotixSanity": self.options.chaotix_sanity.value,
            "ChaotixStoryStartingCharacter": self.options.chaotix_story_starting_character.value,
            #"ChaotixKeySanity": self.options.chaotix_key_sanity.value,
            #"ChaotixCheckpointSanity": self.options.chaotix_checkpoint_sanity.value,

            #"SuperHardMode": self.options.super_hard_mode.value,
            "SuperHardModeStartingCharacter": self.options.super_hard_mode_starting_character.value,
            #"SuperHardModeCheckpointSanity": self.options.super_hard_mode_checkpoint_sanity.value,

            #"RingLink": self.options.ring_link.value,
            #"RingLinkOverlord": self.options.ring_link_metal_overlord.value,
            #"DeathLink": 0,

            #"ModernRingLoss": self.options.modern_ring_loss.value,
            "RemoveCasinoParkVIPTableLaserGate": self.options.remove_casino_park_vip_table_laser_gate.value,

            "GateEmblemCosts": self.gate_emblem_costs,
            "ShuffledLevels": self.shuffled_levels,
            "ShuffledBosses": self.shuffled_bosses,
            "GateLevelCounts": self.gate_level_counts,
        }


    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(self.spoiler_string)
        #print(self.item_name_groups)
        #print(self.location_name_groups)
        pass


    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        pass


    def write_spoiler_end(self, spoiler_handle: TextIO) -> None:
        pass


    def make_puml(self):
        if self.player_name[0:1].isdigit():
            return
        from Utils import visualize_regions
        state = self.multiworld.get_all_state()
        state.update_reachable_regions(self.player)

        reachable_regions = state.reachable_regions[self.player]
        unreachable_regions: set[Region] = set()  # type: ignore
        for region in self.multiworld.regions:
            if region not in reachable_regions:
                unreachable_regions.add(region)

        if self.highlight_unreachable_regions:
            visualize_regions(self.get_region("Menu"), f"{self.player_name}_world.puml", show_entrance_names=True,
                              regions_to_highlight=unreachable_regions)

        else:
            visualize_regions(self.get_region("Menu"), f"{self.player_name}_world.puml", show_entrance_names=True,
                              regions_to_highlight=reachable_regions)
        # !pragma layout smetana
        # put this at top to display PUML (after start UML)


    def import_csv_data(self, team: str):
        #Regions First
        import_region_csv(self, team)
        #Locations Next
        import_location_csv(self, team)
        #Connections Third
        import_connection_csv(self, team)


    def init_logic_mapping_sonic(self) -> None:

        self.full_logic_mapping_dict.update(create_logic_mapping_dict_seaside_hill_sonic(self))
        self.full_logic_mapping_dict.update(create_logic_mapping_dict_ocean_palace_sonic(self))
        self.full_logic_mapping_dict.update(create_logic_mapping_dict_grand_metropolis_sonic(self))
        self.full_logic_mapping_dict.update(create_logic_mapping_dict_power_plant_sonic(self))
        self.full_logic_mapping_dict.update(create_logic_mapping_dict_casino_park_sonic(self))
        self.full_logic_mapping_dict.update(create_logic_mapping_dict_bingo_highway_sonic(self))
        self.full_logic_mapping_dict.update(create_logic_mapping_dict_rail_canyon_sonic(self))
        self.full_logic_mapping_dict.update(create_logic_mapping_dict_bullet_station_sonic(self))
        self.full_logic_mapping_dict.update(create_logic_mapping_dict_frog_forest_sonic(self))
        self.full_logic_mapping_dict.update(create_logic_mapping_dict_lost_jungle_sonic(self))
        self.full_logic_mapping_dict.update(create_logic_mapping_dict_hang_castle_sonic(self))
        self.full_logic_mapping_dict.update(create_logic_mapping_dict_mystic_mansion_sonic(self))
        self.full_logic_mapping_dict.update(create_logic_mapping_dict_egg_fleet_sonic(self))
        self.full_logic_mapping_dict.update(create_logic_mapping_dict_final_fortress_sonic(self))

        """
        return \
            {
                SEASIDEHILL: create_logic_mapping_dict_seaside_hill_sonic(self),
                OCEANPALACE: create_logic_mapping_dict_ocean_palace_sonic(self),
                GRANDMETROPOLIS: create_logic_mapping_dict_grand_metropolis_sonic(self),
                POWERPLANT: create_logic_mapping_dict_power_plant_sonic(self),
                CASINOPARK: create_logic_mapping_dict_casino_park_sonic(self),
                BINGOHIGHWAY: create_logic_mapping_dict_bingo_highway_sonic(self),
                RAILCANYON: create_logic_mapping_dict_rail_canyon_sonic(self),
                BULLETSTATION: create_logic_mapping_dict_bullet_station_sonic(self),
                FROGFOREST: create_logic_mapping_dict_frog_forest_sonic(self),
                LOSTJUNGLE: create_logic_mapping_dict_lost_jungle_sonic(self),
                HANGCASTLE: create_logic_mapping_dict_hang_castle_sonic(self),
                MYSTICMANSION: create_logic_mapping_dict_mystic_mansion_sonic(self),
                EGGFLEET: create_logic_mapping_dict_egg_fleet_sonic(self),
                FINALFORTRESS: create_logic_mapping_dict_final_fortress_sonic(self),
            }
        """


    def init_logic_mapping_any_team(self) -> dict[str, dict[str, CollectionState]]:

        # noinspection PyTypeChecker
        rule_dict: dict[str, dict[str, CollectionState]] = \
        {
            METALMADNESS:
                {
                    "": lambda state: True,  # type: ignore
                },
        }
        rule_dict.update({name: {"": lambda state: True} for name in bonus_and_emerald_stages})  # type: ignore
        return rule_dict

    # noinspection PyTypeChecker
    def init_full_logic_mapping_defaults(self) -> None:
        rule_dict: dict[str, CollectionState] = \
        {
            "": lambda state: True,   # type: ignore
            "NOTPOSSIBLE": lambda state: False,  # type: ignore
        }
        self.full_logic_mapping_dict.update(rule_dict)


    def handle_ut_yamlless(self, slot_data: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:

        if not slot_data \
                and hasattr(self.multiworld, "re_gen_passthrough") \
                and isinstance(self.multiworld.re_gen_passthrough, dict) \
                and self.game in self.multiworld.re_gen_passthrough:
            slot_data = self.multiworld.re_gen_passthrough[self.game]

        if not slot_data:
            return None

        self.is_ut_gen = True


        self.options.included_levels_and_sanities.value = slot_data["IncludedLevelsAndSanities"]
        self.options.unlock_type.value = slot_data["UnlockType"]
        self.options.ability_unlocks.value = slot_data["AbilityUnlocks"]
        self.options.legacy_number_of_level_gates.value = slot_data["LegacyNumberOfLevelGates"]
        self.options.legacy_level_gates_allowed_bosses.value = slot_data["LegacyLevelGatesAllowedBosses"]
        self.options.required_rank.value = slot_data["RequiredRank"]

        self.options.final_boss.value = slot_data["FinalBoss"]
        self.options.goal_unlock_conditions.value = slot_data["GoalUnlockConditions"]
        self.options.goal_level_completions.value = slot_data["GoalLevelCompletions"]
        self.options.goal_level_completions_per_story.value = slot_data["GoalLevelCompletionsPerStory"]

        #self.options.sonic_story.value = slot_data["SonicStory"]
        self.options.sonic_story_starting_character.value = slot_data["SonicStoryStartingCharacter"]
        #self.options.sonic_key_sanity.value = slot_data["SonicKeySanity"]
        #self.options.sonic_checkpoint_sanity.value = slot_data["SonicCheckpointSanity"]

        #self.options.dark_story.value = slot_data["DarkStory"]
        self.options.dark_sanity.value = slot_data["DarkSanity"]
        self.options.dark_story_starting_character.value = slot_data["DarkStoryStartingCharacter"]
        #self.options.dark_key_sanity.value = slot_data["DarkKeySanity"]
        #self.options.dark_checkpoint_sanity.value = slot_data["DarkCheckpointSanity"]

        #self.options.rose_story.value = slot_data["RoseStory"]
        self.options.rose_sanity.value = slot_data["RoseSanity"]
        self.options.rose_story_starting_character.value = slot_data["RoseStoryStartingCharacter"]
        #self.options.rose_key_sanity.value = slot_data["RoseKeySanity"]
        #self.options.rose_checkpoint_sanity.value = slot_data["RoseCheckpointSanity"]

        #self.options.chaotix_story.value = slot_data["ChaotixStory"]
        self.options.chaotix_sanity.value = slot_data["ChaotixSanity"]
        self.options.chaotix_story_starting_character.value = slot_data["ChaotixStoryStartingCharacter"]
        #self.options.chaotix_key_sanity.value = slot_data["ChaotixKeySanity"]
        #self.options.chaotix_checkpoint_sanity.value = slot_data["ChaotixCheckpointSanity"]

        #self.options.super_hard_mode.value = slot_data["SuperHardMode"]
        self.options.super_hard_mode_starting_character.value = slot_data["SuperHardModeStartingCharacter"]
        #self.options.super_hard_mode_checkpoint_sanity.value = slot_data["SuperHardModeCheckpointSanity"]

        #self.options.ring_link.value = slot_data["RingLink"]
        #self.options.ring_link_metal_overlord.value = slot_data["RingLinkMetalOverlord"]
        #self.options.death_link.value = slot_data["DeathLink"]

        #self.options.modern_ring_loss.value = slot_data["ModernRingLoss"]
        self.options.remove_casino_park_vip_table_laser_gate.value = slot_data["RemoveCasinoParkVIPTableLaserGate"]


        self.gate_emblem_costs = slot_data["GateEmblemCosts"]
        self.shuffled_levels = slot_data["ShuffledLevels"]
        self.shuffled_bosses = slot_data["ShuffledBosses"]
        self.gate_level_counts = slot_data["GateLevelCounts"]

        return slot_data

    
    def handle_option_checking(self) -> None:
        if not LEVELCOMPLETIONSALLTEAMS in self.options.goal_unlock_conditions:
            self.options.goal_level_completions.value = 0
    
        if not LEVELCOMPLETIONSPERSTORY in self.options.goal_unlock_conditions:
            self.options.goal_level_completions_per_story.value = 0
    
    
        if self.is_this_team_enabled(SONIC):
            self.enabled_teams.append(SONIC)
            self.allowed_levels_per_team[SONIC] = self.regular_levels
    
            self.emblems_to_create += self.level_block_emblem_count
    
            if self.is_this_team_enabled(SONIC, both_acts_required=True):
                self.emblems_to_create += self.level_block_emblem_count
    
    
        if self.is_this_team_enabled(DARK):
            self.enabled_teams.append(DARK)
            self.allowed_levels_per_team[DARK] = self.regular_levels
    
            self.emblems_to_create += self.level_block_emblem_count
    
            if self.is_this_team_enabled(DARK, both_acts_required=True):
                self.emblems_to_create += self.level_block_emblem_count
    
    
        if self.is_this_team_enabled(ROSE):
            self.enabled_teams.append(ROSE)
            self.allowed_levels_per_team[ROSE] = self.regular_levels
    
            self.emblems_to_create += self.level_block_emblem_count
    
            if self.is_this_team_enabled(ROSE, both_acts_required=True):
                self.emblems_to_create += self.level_block_emblem_count
    
    
        if self.is_this_team_enabled(CHAOTIX):
            self.enabled_teams.append(CHAOTIX)
            self.allowed_levels_per_team[CHAOTIX] = self.regular_levels
    
            self.emblems_to_create += self.level_block_emblem_count
    
            if self.is_this_team_enabled(CHAOTIX, both_acts_required=True):
                self.emblems_to_create += self.level_block_emblem_count
    
        if self.is_this_team_enabled(SUPERHARDMODE):
            self.enabled_teams.append(SUPERHARDMODE)
            self.allowed_levels_per_team[SUPERHARDMODE] = self.regular_levels
            self.emblems_to_create += self.level_block_emblem_count

        if self.options.unlock_type == UnlockType.option_legacy_level_gates:
            if self.is_this_sanity_enabled(ROSE, OBJSANITY) or self.is_this_sanity_enabled(CHAOTIX, OBJSANITY):
                change_filler_weights_for_legacy_level_gates(self)
    
    
    def handle_level_gates_start(self) -> None:
        if not self.is_ut_gen:
            self.generate_level_gates()

        for gate_num in range(self.options.legacy_number_of_level_gates.value):
            self.boss_locations_added.append(sonic_heroes_extra_names[int(self.shuffled_bosses[gate_num][1:]) - 16])
            self.region_to_location[sonic_heroes_extra_names[int(self.shuffled_bosses[gate_num][1:]) - 16]] = []
    
    
    def generate_level_gates(self) -> None:
    
        shuffleable_levels: list[str] = []
    
        team_letter: str = 'S'
        """S D R C based on team (superhard is part of sonic)"""
    
        act_letter: str = 'A'
        """A B or C based on acts enabled"""
    
        if self.is_this_team_enabled(SONIC) or self.is_this_team_enabled(SUPERHARDMODE):
            team_letter = 'S'
    
            if SONICACTA in self.options.included_levels_and_sanities and not self.is_this_team_enabled(SONIC, both_acts_required=True) and not self.is_this_team_enabled(SUPERHARDMODE):
                act_letter = 'A'
    
            elif (SONICACTB in self.options.included_levels_and_sanities or self.is_this_team_enabled(SUPERHARDMODE)) and not SONICACTA in self.options.included_levels_and_sanities:
                act_letter = 'B'
    
            elif (SONICACTB in self.options.included_levels_and_sanities or self.is_this_team_enabled(SUPERHARDMODE)) and SONICACTA in self.options.included_levels_and_sanities:
                act_letter = 'C'

            if self.is_this_team_enabled(SONIC):
                for level in self.allowed_levels_per_team[SONIC]:
                    shuffleable_levels.append(f"{team_letter}{sonic_heroes_regular_levels_index[level]}")

            elif self.is_this_team_enabled(SUPERHARDMODE):
                for level in self.allowed_levels_per_team[SUPERHARDMODE]:
                    shuffleable_levels.append(f"{team_letter}{sonic_heroes_regular_levels_index[level]}")
    
    
        if self.is_this_team_enabled(DARK):
            team_letter = 'D'
    
            if DARKACTA in self.options.included_levels_and_sanities and not self.is_this_team_enabled(DARK, both_acts_required=True):
                act_letter = 'A'
    
            elif DARKACTB in self.options.included_levels_and_sanities and not self.is_this_team_enabled(DARK, both_acts_required=True):
                act_letter = 'B'
    
            elif self.is_this_team_enabled(DARK, both_acts_required=True):
                act_letter = 'C'
    
            for level in self.allowed_levels_per_team[DARK]:
                shuffleable_levels.append(f"{team_letter}{sonic_heroes_regular_levels_index[level]}")
    
    
        if self.is_this_team_enabled(ROSE):
            team_letter = 'R'
    
            if ROSEACTA in self.options.included_levels_and_sanities and not self.is_this_team_enabled(ROSE, both_acts_required=True):
                act_letter = 'A'
    
            elif ROSEACTB in self.options.included_levels_and_sanities and not self.is_this_team_enabled(ROSE, both_acts_required=True):
                act_letter = 'B'
    
            elif self.is_this_team_enabled(ROSE, both_acts_required=True):
                act_letter = 'C'
    
            for level in self.allowed_levels_per_team[ROSE]:
                shuffleable_levels.append(f"{team_letter}{sonic_heroes_regular_levels_index[level]}")
    
    
        if self.is_this_team_enabled(CHAOTIX):
            team_letter = 'C'
    
            if CHAOTIXACTA in self.options.included_levels_and_sanities and not self.is_this_team_enabled(CHAOTIX, both_acts_required=True):
                act_letter = 'A'
    
            elif CHAOTIXACTB in self.options.included_levels_and_sanities and not self.is_this_team_enabled(CHAOTIX, both_acts_required=True):
                act_letter = 'B'
    
            elif self.is_this_team_enabled(CHAOTIX, both_acts_required=True):
                act_letter = 'C'
    
            for level in self.allowed_levels_per_team[CHAOTIX]:
                shuffleable_levels.append(f"{team_letter}{sonic_heroes_regular_levels_index[level]}")
    
    
        #0-13 Sonic
        #14-27 Dark
        #28-41 Rose
        #42-55 Chaotix
    
        #Now Do Bosses
        shuffleable_bosses: list[str] = list(self.options.legacy_level_gates_allowed_bosses.value.copy())
    
        self.random.shuffle(shuffleable_levels)
        self.random.shuffle(shuffleable_bosses)
    
        for _ in range(len(shuffleable_bosses) - self.options.legacy_number_of_level_gates.value):
            shuffleable_bosses.pop()
    
    
        number_level_groups = self.options.legacy_number_of_level_gates.value + 1
        minimum_levels_per_group = len(shuffleable_levels) // number_level_groups
        remainder_levels = len(shuffleable_levels) % number_level_groups
    
        final_boss_emblem_cost = int(self.emblems_to_create * self.required_emblems_ratio)
        first_gate_cost = final_boss_emblem_cost // number_level_groups
    
        for level_group_number in range(number_level_groups):
            go_to_next_group: bool = False
            has_used_remainder_level: bool = False
            num_locations_in_group: int = 0
            num_levels_in_group: int = 0
    
            while not go_to_next_group:
                current_level_entry: str = shuffleable_levels.pop(0)
                current_team: str = team_code_to_team[current_level_entry[0]]
                current_level: str = sonic_heroes_level_names[int(current_level_entry[1:]) + 1]
    
                #num_locations_at_current_level: int = try_to_guess_how_many_locations_are_here(self, current_team, current_level)
                num_locations_in_group += self.try_to_guess_how_many_locations_are_here(current_team, current_level)
                if current_team == SONIC:
                    #num_locations_at_current_level += try_to_guess_how_many_locations_are_here(self, SUPERHARDMODE, current_level)
                    num_locations_in_group += self.try_to_guess_how_many_locations_are_here(SUPERHARDMODE, current_level)
    
                #add level here
                self.shuffled_levels.append(f"{current_level_entry[0]}{int(current_level_entry[1:]) + 2}")
                num_levels_in_group += 1
    
                if len(shuffleable_levels) == 0 or (num_locations_in_group >= first_gate_cost and num_levels_in_group >= minimum_levels_per_group):
                    go_to_next_group = True
                    if not has_used_remainder_level and remainder_levels > 0:
                        has_used_remainder_level = False
                        remainder_levels -= 1
                        go_to_next_group = False


            self.gate_level_counts.append(num_levels_in_group)
            if level_group_number < number_level_groups - 1:
                self.gate_emblem_costs.append(first_gate_cost * (level_group_number + 1))
                self.shuffled_bosses.append(f"B{boss_name_to_slot_data_id[shuffleable_bosses.pop(0)]}")
            else:
                self.gate_emblem_costs.append(final_boss_emblem_cost)
                self.shuffled_bosses.append(f"B{boss_name_to_slot_data_id[METALMADNESS]}")
    
    
    def try_to_guess_how_many_locations_are_here(self, team: str, level: str) -> int:
        """
        This is really stupid, why do I need to do this again?
        Future me says it to prevent fill errors, apparently.
        """
        num_locations = 0
        secret_index = 1 if self.secret else 0
    
    
        if self.is_this_team_enabled(team):
            num_locations += 1
            if self.is_this_sanity_enabled(team, KEYSANITY):
                num_locations += bonus_keys_per_team_level[team][level][secret_index]
            if self.is_this_sanity_enabled(team, CHECKPOINTSANITY):
                num_locations += checkpoints_per_team_level[team][level][secret_index]
    
            if self.is_this_sanity_enabled(team, OBJSANITY):
                num_locations += self.get_number_of_obj_sanity_checks(team, level)
    
            if self.is_this_team_enabled(team, both_acts_required=True):
                num_locations += 1
                if self.is_this_sanity_enabled(team, KEYSANITY, both_acts_required=True):
                    num_locations += bonus_keys_per_team_level[team][level][secret_index]
                if self.is_this_sanity_enabled(team, CHECKPOINTSANITY, both_acts_required=True):
                    num_locations += checkpoints_per_team_level[team][level][secret_index]
    
        return num_locations
    
    
    def get_number_of_obj_sanity_checks(self, team: str, level: str) -> int:
        num_locations: int = 0
    
        if team == DARK:
            num_locations += int(100 / self.options.dark_sanity.value) if DARKACTB in self.options.included_levels_and_sanities else 0
    
        elif team == ROSE:
            num_locations += int(200 / self.options.rose_sanity.value) if ROSEACTB in self.options.included_levels_and_sanities else 0
    
        elif team == CHAOTIX:
            if self.is_this_team_enabled(CHAOTIX, both_acts_required=True):
                if level == CASINOPARK:
                    num_locations += int(700 / self.options.chaotix_sanity.value)
                else:
                    num_locations += chaotix_obj_sanity_checks_per_level_act[level][0] + chaotix_obj_sanity_checks_per_level_act[level][1]
    
            elif CHAOTIXACTB in self.options.included_levels_and_sanities:
                if level == CASINOPARK:
                    num_locations += int(500 / self.options.chaotix_sanity.value)
                else:
                    num_locations += chaotix_obj_sanity_checks_per_level_act[level][1]
    
            elif CHAOTIXACTA in self.options.included_levels_and_sanities:
                if level == CASINOPARK:
                    num_locations += int(200 / self.options.chaotix_sanity.value)
                else:
                    num_locations += chaotix_obj_sanity_checks_per_level_act[level][0]
    
        return num_locations
    
    
    def is_this_team_enabled(self, team: str, both_acts_required: bool = False) -> bool:
        """
        Returns True if either Act of the team is enabled.
        both_acts_required requires both acts to be enabled to return True (Super Hard Mode ignores this).
        """
        if team == SONIC:
            if both_acts_required:
                return SONICACTA in self.options.included_levels_and_sanities and SONICACTB in self.options.included_levels_and_sanities
            return SONICACTA in self.options.included_levels_and_sanities or SONICACTB in self.options.included_levels_and_sanities
    
        if team == DARK:
            if both_acts_required:
                return DARKACTA in self.options.included_levels_and_sanities and DARKACTB in self.options.included_levels_and_sanities
            return DARKACTA in self.options.included_levels_and_sanities or DARKACTB in self.options.included_levels_and_sanities
    
        if team == ROSE:
            if both_acts_required:
                return ROSEACTA in self.options.included_levels_and_sanities and ROSEACTB in self.options.included_levels_and_sanities
            return ROSEACTA in self.options.included_levels_and_sanities or ROSEACTB in self.options.included_levels_and_sanities
    
        if team == CHAOTIX:
            if both_acts_required:
                return CHAOTIXACTA in self.options.included_levels_and_sanities and CHAOTIXACTB in self.options.included_levels_and_sanities
    
            return CHAOTIXACTA in self.options.included_levels_and_sanities or CHAOTIXACTB in self.options.included_levels_and_sanities
    
        if team == SUPERHARDMODE:
            #if both_acts_required:
                #print(f"Both Acts asked for in is_this_team_enabled for team Super Hard Mode.")
            return SUPERHARDMODE in self.options.included_levels_and_sanities
    
        if team == ANYTEAM:
            return False
    
        print(f"Wrong team {team} in is_this_team_enabled")
        return False
    
    
    def is_this_sanity_enabled(self, team: str, sanity: str, both_acts_required: bool = False) -> bool:
    
        if team == SONIC:
            if sanity == KEYSANITY:
                if both_acts_required:
                    return SONICKEYSANITYBOTHACTS in self.options.included_levels_and_sanities
                return SONICKEYSANITY1SET in self.options.included_levels_and_sanities or SONICKEYSANITYBOTHACTS in self.options.included_levels_and_sanities
    
            if sanity == CHECKPOINTSANITY:
                if both_acts_required:
                    return SONICCHECKPOINTSANITYBOTHACTS in self.options.included_levels_and_sanities
                return SONICCHECKPOINTSANITY1SET in self.options.included_levels_and_sanities or SONICCHECKPOINTSANITYBOTHACTS in self.options.included_levels_and_sanities
            
            if sanity == OBJSANITY:
                return False
    
            print(f"Team {team} does not have sanity {sanity} in is_this_sanity_enabled")
            return False

        if team == DARK:
            if sanity == KEYSANITY:
                if both_acts_required:
                    return DARKKEYSANITYBOTHACTS in self.options.included_levels_and_sanities
                return DARKKEYSANITY1SET in self.options.included_levels_and_sanities or DARKKEYSANITYBOTHACTS in self.options.included_levels_and_sanities
    
            if sanity == CHECKPOINTSANITY:
                if both_acts_required:
                    return DARKCHECKPOINTSANITYBOTHACTS in self.options.included_levels_and_sanities
                return DARKCHECKPOINTSANITY1SET in self.options.included_levels_and_sanities or DARKCHECKPOINTSANITYBOTHACTS in self.options.included_levels_and_sanities
            
            if sanity == OBJSANITY:
                return DARKOBJSANITY in self.options.included_levels_and_sanities
                #return self.options.dark_sanity.value > 0
                
    
            print(f"Team {team} does not have sanity {sanity} in is_this_sanity_enabled")
            return False

        if team == ROSE:
            if sanity == KEYSANITY:
                if both_acts_required:
                    return ROSEKEYSANITYBOTHACTS in self.options.included_levels_and_sanities
                return ROSEKEYSANITY1SET in self.options.included_levels_and_sanities or ROSEKEYSANITYBOTHACTS in self.options.included_levels_and_sanities
    
            if sanity == CHECKPOINTSANITY:
                if both_acts_required:
                    return ROSECHECKPOINTSANITYBOTHACTS in self.options.included_levels_and_sanities
                return ROSECHECKPOINTSANITY1SET in self.options.included_levels_and_sanities or ROSECHECKPOINTSANITYBOTHACTS in self.options.included_levels_and_sanities
    
            if sanity == OBJSANITY:
                return ROSEOBJSANITY in self.options.included_levels_and_sanities
    
            print(f"Team {team} does not have sanity {sanity} in is_this_sanity_enabled")
            return False
    
        if team == CHAOTIX:
            if sanity == KEYSANITY:
                if both_acts_required:
                    return CHAOTIXKEYSANITYBOTHACTS in self.options.included_levels_and_sanities
                return CHAOTIXKEYSANITY1SET in self.options.included_levels_and_sanities or CHAOTIXKEYSANITYBOTHACTS in self.options.included_levels_and_sanities
    
            if sanity == CHECKPOINTSANITY:
                if both_acts_required:
                    return CHAOTIXCHECKPOINTSANITYBOTHACTS in self.options.included_levels_and_sanities
                return CHAOTIXCHECKPOINTSANITY1SET in self.options.included_levels_and_sanities or CHAOTIXCHECKPOINTSANITYBOTHACTS in self.options.included_levels_and_sanities
    
            if sanity == OBJSANITY:
                return CHAOTIXOBJSANITY in self.options.included_levels_and_sanities
    
            print(f"Team {team} does not have sanity {sanity} in is_this_sanity_enabled")
            return False
    
        if team == SUPERHARDMODE:
            if sanity == KEYSANITY:
                return False
    
            if sanity == CHECKPOINTSANITY:
                if both_acts_required:
                    #print(f"Both Acts asked for in is_this_sanity_enabled for team Super Hard Mode.")
                    return False
                return SUPERHARDCHECKPOINTSANITY in self.options.included_levels_and_sanities
    
            if sanity == OBJSANITY:
                return False
    
            print(f"Team {team} does not have sanity {sanity} in is_this_sanity_enabled")
            return False
    
        if team == ANYTEAM:
            return False
    
        print(f"How did we get here? Team {team} in is_this_sanity_enabled")
        return False
