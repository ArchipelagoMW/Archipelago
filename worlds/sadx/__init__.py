import typing
from typing import Dict, Any

from BaseClasses import Tutorial, Region
from worlds.AutoWorld import WebWorld, World
from .CharacterUtils import get_playable_characters
from .Enums import Character, SADX_BASE_ID, Area, remove_character_suffix, pascal_to_space, level_areas, AreaConnection, \
    EnemySanityCategory, CapsuleSanityCategory
from .ItemPool import create_sadx_items, get_item_names, ItemDistribution
from .Items import SonicAdventureDXItem, group_item_table, item_name_to_info, filler_item_table
from .Locations import all_location_table, group_location_table
from .Logic import mission_location_table
from .Names import ItemName, LocationName
from .Options import sadx_option_groups, SonicAdventureDXOptions
from .Regions import create_sadx_regions, get_location_ids_for_area
from .Rules import create_sadx_rules, LocationDistribution
from .StartingSetup import StarterSetup, generate_early_sadx, write_sadx_spoiler, CharacterArea

sadx_version = 120


class SonicAdventureDXWeb(WebWorld):
    theme = "partyTime"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Sonic Adventure DX randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["ClassicSpeed"]
    )]
    option_groups = sadx_option_groups


class SonicAdventureDXWorld(World):
    game = "Sonic Adventure DX"
    web = SonicAdventureDXWeb()
    starter_setup: StarterSetup = StarterSetup()
    area_map = None
    explicit_indirect_conditions = False
    created_regions: Dict[typing.Tuple[Character, Area], Region] = {}
    item_distribution: ItemDistribution = ItemDistribution()
    location_distribution: LocationDistribution = LocationDistribution()
    item_name_to_id = {item.name: item.itemId + SADX_BASE_ID for item in item_name_to_info.values()}
    location_name_to_id = {loc["name"]: loc["id"] + SADX_BASE_ID for loc in all_location_table}

    item_name_groups = group_item_table
    location_name_groups = group_location_table

    options_dataclass = SonicAdventureDXOptions
    options: SonicAdventureDXOptions

    tracker_world = {"map_page_folder": "tracker", "map_page_maps": "maps/maps.json",
                     "map_page_locations": "locations/locations.json"}
    ut_can_gen_without_yaml = True

    def generate_early(self):
        self.starter_setup = generate_early_sadx(self, self.options)
        # Universal tracker stuff, shouldn't do anything in standard gen
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "Sonic Adventure DX" in self.multiworld.re_gen_passthrough:
                passthrough = self.multiworld.re_gen_passthrough["Sonic Adventure DX"]

                self.starter_setup.character = Character(passthrough["StartingCharacter"])
                self.starter_setup.area = Area(passthrough["StartingArea"])
                self.starter_setup.charactersWithArea = [
                    CharacterArea(Character.Sonic, Area(passthrough["SonicStartingArea"])),
                    CharacterArea(Character.Tails, Area(passthrough["TailsStartingArea"])),
                    CharacterArea(Character.Knuckles, Area(passthrough["KnucklesStartingArea"])),
                    CharacterArea(Character.Amy, Area(passthrough["AmyStartingArea"])),
                    CharacterArea(Character.Gamma, Area(passthrough["GammaStartingArea"])),
                    CharacterArea(Character.Big, Area(passthrough["BigStartingArea"]))

                ]
                self.starter_setup.level_mapping = {
                    AreaConnection.from_index(original): AreaConnection.from_index(randomized)
                    for original, randomized in passthrough["LevelEntranceMap"].items()}

                self.area_map = {AreaConnection.from_index(int(entranceIndex)): int(value)
                                 for entranceIndex, value in passthrough["EntranceEmblemValueMap"].items()}

                # Options synchronization, needed for weighted values
                self.options.goal_requires_levels.value = passthrough["GoalRequiresLevels"]
                self.options.levels_percentage.value = passthrough["LevelsPercentage"]
                self.options.goal_requires_chaos_emeralds.value = passthrough["GoalRequiresChaosEmeralds"]
                self.options.goal_requires_emblems.value = passthrough["GoalRequiresEmblems"]
                self.options.emblems_percentage.value = passthrough["EmblemsPercentage"]
                self.options.max_emblem_cap.value = passthrough["MaximumEmblemCap"]
                self.options.goal_requires_missions.value = passthrough["GoalRequiresMissions"]
                self.options.mission_percentage.value = passthrough["MissionsPercentage"]
                self.options.goal_requires_bosses.value = passthrough["GoalRequiresBosses"]
                self.options.boss_percentage.value = passthrough["BossPercentage"]
                self.options.goal_requires_chao_races.value = passthrough["GoalRequiresChaoRaces"]
                self.options.logic_level.value = passthrough["LogicLevel"]
                self.options.entrance_randomizer.value = passthrough["EntranceRandomizer"]
                self.options.gating_mode.value = passthrough["GatingMode"]

                self.options.playable_sonic.value = passthrough["PlayableSonic"]
                self.options.playable_tails.value = passthrough["PlayableTails"]
                self.options.playable_knuckles.value = passthrough["PlayableKnuckles"]
                self.options.playable_amy.value = passthrough["PlayableAmy"]
                self.options.playable_big.value = passthrough["PlayableBig"]
                self.options.playable_gamma.value = passthrough["PlayableGamma"]

                self.options.sonic_action_stage_missions.value = passthrough["SonicActionStageMissions"]
                self.options.tails_action_stage_missions.value = passthrough["TailsActionStageMissions"]
                self.options.knuckles_action_stage_missions.value = passthrough["KnucklesActionStageMissions"]
                self.options.amy_action_stage_missions.value = passthrough["AmyActionStageMissions"]
                self.options.gamma_action_stage_missions.value = passthrough["GammaActionStageMissions"]
                self.options.big_action_stage_missions.value = passthrough["BigActionStageMissions"]

                self.options.randomized_upgrades.value = passthrough["RandomizedUpgrades"]

                self.options.boss_checks.value = passthrough["BossChecks"]
                self.options.unify_chaos4.value = passthrough["UnifyChaos4"]
                self.options.unify_chaos6.value = passthrough["UnifyChaos6"]
                self.options.unify_egg_hornet.value = passthrough["UnifyEggHornet"]

                self.options.field_emblems_checks.value = passthrough["FieldEmblemChecks"]
                self.options.starting_character.value = passthrough["StartingCharacterOption"]
                self.options.starting_location.value = passthrough["StartingLocationOption"]

                self.options.chao_egg_checks.value = passthrough["SecretChaoEggs"]
                self.options.chao_races_checks.value = passthrough["ChaoRacesChecks"]
                self.options.chao_races_levels_to_access_percentage.value = passthrough[
                    "ChaoRacesLevelsToAccessPercentage"]
                self.options.mission_mode_checks.value = passthrough["MissionModeChecks"]
                self.options.auto_start_missions.value = passthrough["AutoStartMissions"]
                self.options.mission_blacklist.value = list(passthrough["MissionBlackList"].keys())

                self.options.twinkle_circuit_checks.value = passthrough["TwinkleCircuitChecks"]
                self.options.sand_hill_checks.value = passthrough["SandHillChecks"]
                self.options.sky_chase_checks.value = passthrough["SkyChaseChecks"]

                self.options.enemy_sanity.value = passthrough["EnemySanity"]
                self.options.enemy_sanity_list = EnemySanityCategory.to_object_list(passthrough["EnemySanityList"])
                self.options.enemy_sanity_list.value = passthrough["EnemySanityList"]
                self.options.missable_enemies.value = passthrough["MissableEnemies"]

                self.options.capsule_sanity.value = passthrough["CapsuleSanity"]
                self.options.capsule_sanity_list = CapsuleSanityCategory.to_object_list(
                    passthrough["CapsuleSanityList"])
                self.options.capsule_sanity_list.value = passthrough["CapsuleSanityList"]
                self.options.missable_capsules.value = passthrough["MissableCapsules"]
                self.options.pinball_capsules.value = passthrough["PinballCapsules"]

                self.options.fish_sanity.value = passthrough["FishSanity"]
                self.options.lazy_fishing.value = passthrough["LazyFishing"]

    # For the universal tracker, doesn't get called in standard gen
    # Returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:

        if slot_data["ModVersion"] != sadx_version:
            current_version = f"v{sadx_version // 100}.{(sadx_version // 10) % 10}.{sadx_version % 10}"
            slot_version = f"v{slot_data['ModVersion'] // 100}.{(slot_data['ModVersion'] // 10) % 10}.{slot_data['ModVersion'] % 10}"

            raise Exception(
                f"SADX version error: The version of apworld used to generate this world ({slot_version}) does not match the version of your installed apworld ({current_version}).")
        return slot_data

    def create_item(self, name: str) -> SonicAdventureDXItem:
        return SonicAdventureDXItem(name, self.player)

    def create_regions(self) -> None:
        self.created_regions = create_sadx_regions(self, self.starter_setup, self.options)

    def create_items(self):
        self.item_distribution = create_sadx_items(self, self.starter_setup, self.options)

    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_item_table).name

    def set_rules(self):
        self.location_distribution = create_sadx_rules(self, self.item_distribution.emblem_count_progressive,
                                                       self.area_map)

    def write_spoiler(self, spoiler_handle: typing.TextIO):
        write_sadx_spoiler(self, spoiler_handle, self.starter_setup, self.options)

    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        if self.options.entrance_randomizer.value == 0:
            return

        sadx_hint_data = {}
        level_area_strings = [pascal_to_space(area.name) + " (" for area in level_areas]
        # Add level entrance hints if entrance randomizer is on
        for location in self.multiworld.get_locations(self.player):
            if any(location.parent_region.name.startswith(area_string) for area_string in level_area_strings):
                if location.parent_region.entrances:
                    sadx_hint_data[location.address] = remove_character_suffix(location.parent_region.entrances[0].name)

        hint_data[self.player] = sadx_hint_data

    def generate_progression_data(self) -> typing.Dict[int, int]:
        progression_data = {}
        for ap_location in self.multiworld.get_locations(self.player):
            if ap_location.item.advancement:
                progression_data[ap_location.address] = ap_location.address
        return progression_data

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "ModVersion": sadx_version,
            "GoalRequiresLevels": self.options.goal_requires_levels.value,
            "LevelsPercentage": self.options.levels_percentage.value,
            "GoalRequiresChaosEmeralds": self.options.goal_requires_chaos_emeralds.value,
            "GoalRequiresEmblems": self.options.goal_requires_emblems.value,
            "EmblemsPercentage": self.options.emblems_percentage.value,
            "MaximumEmblemCap": self.options.max_emblem_cap.value,
            "GoalRequiresMissions": self.options.goal_requires_missions.value,
            "MissionsPercentage": self.options.mission_percentage.value,
            "GoalRequiresBosses": self.options.goal_requires_bosses.value,
            "BossPercentage": self.options.boss_percentage.value,
            "GoalRequiresChaoRaces": self.options.goal_requires_chao_races.value,
            "LogicLevel": self.options.logic_level.value,
            "GatingMode": self.options.gating_mode.value,
            "EmblemsForPerfectChaos": self.item_distribution.emblem_count_progressive,
            "LevelForPerfectChaos": self.location_distribution.levels_for_perfect_chaos,
            "MissionForPerfectChaos": self.location_distribution.missions_for_perfect_chaos,
            "BossesForPerfectChaos": self.location_distribution.bosses_for_perfect_chaos,
            "EntranceEmblemValueMap": self.location_distribution.entrance_emblem_value_map,
            "StartingCharacter": self.starter_setup.character.value,
            "StartingArea": self.starter_setup.area.value,
            "SonicStartingArea": self.starter_setup.get_starting_area(Character.Sonic).value,
            "TailsStartingArea": self.starter_setup.get_starting_area(Character.Tails).value,
            "KnucklesStartingArea": self.starter_setup.get_starting_area(Character.Knuckles).value,
            "AmyStartingArea": self.starter_setup.get_starting_area(Character.Amy).value,
            "GammaStartingArea": self.starter_setup.get_starting_area(Character.Gamma).value,
            "BigStartingArea": self.starter_setup.get_starting_area(Character.Big).value,
            "EntranceRandomizer": self.options.entrance_randomizer.value,
            "LevelEntranceMap": {original.get_index(): randomized.get_index() for original, randomized in
                                 self.starter_setup.level_mapping.items()},

            "StartingCharacterOption": self.options.starting_character.value,
            "StartingLocationOption": self.options.starting_location.value,
            "FieldEmblemChecks": self.options.field_emblems_checks.value,
            "SecretChaoEggs": self.options.chao_egg_checks.value,
            "ChaoRacesChecks": self.options.chao_races_checks.value,
            "ChaoRacesLevelsToAccessPercentage": self.options.chao_races_levels_to_access_percentage.value,
            "MissionModeChecks": self.options.mission_mode_checks.value,
            "AutoStartMissions": self.options.auto_start_missions.value,

            "MissionBlackList": {
                mission.missionNumber: mission.missionNumber
                for mission in mission_location_table
                if str(mission.missionNumber) in self.options.mission_blacklist.value
                   or str(mission.character.name) in self.options.mission_blacklist.value
            },

            "EnemySanity": self.options.enemy_sanity.value,
            "EnemySanityList": {enum_member.value: enum_member.value for enum_member in
                                EnemySanityCategory.from_object_list(self.options.enemy_sanity_list)},
            "MissableEnemies": self.options.missable_enemies.value,

            "CapsuleSanity": self.options.capsule_sanity.value,
            "CapsuleSanityList": {enum_member.value: enum_member.value for enum_member in
                                  CapsuleSanityCategory.from_object_list(self.options.capsule_sanity_list)},
            "MissableCapsules": self.options.missable_capsules.value,
            "PinballCapsules": self.options.pinball_capsules.value,

            "FishSanity": self.options.fish_sanity.value,
            "LazyFishing": self.options.lazy_fishing.value,

            "ProgressionItems": self.generate_progression_data(),

            "DeathLink": self.options.death_link.value,
            "SendDeathLinkChance": self.options.send_death_link_chance.value,
            "ReceiveDeathLinkChance": self.options.receive_death_link_chance.value,
            "RingLink": self.options.ring_link.value,
            "RingLoss": self.options.ring_loss.value,
            "TrapLink": self.options.trap_link.value,
            "TwinkleCircuitChecks": self.options.twinkle_circuit_checks.value,
            "SandHillChecks": self.options.sand_hill_checks.value,
            "SkyChaseChecks": self.options.sky_chase_checks.value,

            "MusicSource": self.options.music_source.value,
            "MusicShuffle": self.options.music_shuffle.value,
            "MusicShuffleConsistency": self.options.music_shuffle_consistency.value,
            "LifeCapsulesChangeSongs": self.options.life_capsules_change_songs.value,
            "MusicShuffleSeed": self.multiworld.seed % (2 ** 31),

            "BossChecks": self.options.boss_checks.value,
            "UnifyChaos4": self.options.unify_chaos4.value,
            "UnifyChaos6": self.options.unify_chaos6.value,
            "UnifyEggHornet": self.options.unify_egg_hornet.value,

            "RandomizedUpgrades": self.options.randomized_upgrades.value,

            "PlayableSonic": self.options.playable_sonic.value,
            "PlayableTails": self.options.playable_tails.value,
            "PlayableKnuckles": self.options.playable_knuckles.value,
            "PlayableAmy": self.options.playable_amy.value,
            "PlayableBig": self.options.playable_big.value,
            "PlayableGamma": self.options.playable_gamma.value,

            "SonicActionStageMissions": self.options.sonic_action_stage_missions.value,
            "TailsActionStageMissions": self.options.tails_action_stage_missions.value,
            "KnucklesActionStageMissions": self.options.knuckles_action_stage_missions.value,
            "AmyActionStageMissions": self.options.amy_action_stage_missions.value,
            "GammaActionStageMissions": self.options.gamma_action_stage_missions.value,
            "BigActionStageMissions": self.options.big_action_stage_missions.value,

            "JunkFillPercentage": self.options.junk_fill_percentage.value,

            "IceTrapWeight": self.options.ice_trap_weight.value,
            "SpringTrapWeight": self.options.spring_trap_weight.value,
            "PoliceTrapWeight": self.options.police_trap_weight.value,
            "BuyonTrapWeight": self.options.buyon_trap_weight.value,
            "ReverseTrapWeight": self.options.reverse_trap_weight.value,
            "GravityTrapWeight": self.options.gravity_trap_weight.value,

            "ReverseControlTrapDuration": self.options.reverse_trap_duration.value,
            "TrapsOnAdventureFields": self.options.traps_and_filler_on_adventure_fields.value,
            "TrapsOnBossFights": self.options.traps_and_filler_on_boss_fights.value,
            "TrapsOnPerfectChaosFight": self.options.traps_and_filler_on_perfect_chaos_fight.value

        }
