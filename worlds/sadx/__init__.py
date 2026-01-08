import typing
from typing import Dict, Any

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .CharacterUtils import get_playable_characters
from .Enums import Character, SADX_BASE_ID, Area, remove_character_suffix, pascal_to_space
from .ItemPool import create_sadx_items, get_item_names, ItemDistribution
from .Items import SonicAdventureDXItem, group_item_table, item_name_to_info, filler_item_table
from .Locations import all_location_table, group_location_table
from .Logic import mission_location_table
from .Names import ItemName, LocationName
from .Options import sadx_option_groups, SonicAdventureDXOptions
from .Regions import create_sadx_regions, get_location_ids_for_area
from .Rules import create_sadx_rules, LocationDistribution
from .StartingSetup import StarterSetup, generate_early_sadx, write_sadx_spoiler, CharacterArea, level_areas

sadx_version = 113


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
                self.starter_setup.level_mapping = {Area(int(original)): Area(int(randomized))
                                                    for original, randomized in passthrough["LevelEntranceMap"].items()}

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

                self.options.randomized_sonic_upgrades.value = passthrough["RandomizedSonicUpgrades"]
                self.options.randomized_tails_upgrades.value = passthrough["RandomizedTailsUpgrades"]
                self.options.randomized_knuckles_upgrades.value = passthrough["RandomizedKnucklesUpgrades"]
                self.options.randomized_amy_upgrades.value = passthrough["RandomizedAmyUpgrades"]
                self.options.randomized_big_upgrades.value = passthrough["RandomizedGammaUpgrades"]
                self.options.randomized_gamma_upgrades.value = passthrough["RandomizedBigUpgrades"]

                self.options.boss_checks.value = passthrough["BossChecks"]
                self.options.unify_chaos4.value = passthrough["UnifyChaos4"]
                self.options.unify_chaos6.value = passthrough["UnifyChaos6"]
                self.options.unify_egg_hornet.value = passthrough["UnifyEggHornet"]

                self.options.field_emblems_checks.value = passthrough["FieldEmblemChecks"]
                self.options.starting_character.value = passthrough["StartingCharacterOption"]
                self.options.starting_location.value = passthrough["StartingLocationOption"]
                self.options.random_starting_location_per_character.value = passthrough[
                    "RandomStartingLocationPerCharacter"]
                self.options.guaranteed_starting_checks.value = passthrough["GuaranteedStartingChecks"]

                self.options.chao_egg_checks.value = passthrough["SecretChaoEggs"]
                self.options.chao_races_checks.value = passthrough["ChaoRacesChecks"]
                self.options.chao_races_levels_to_access_percentage.value = passthrough[
                    "ChaoRacesLevelsToAccessPercentage"]
                self.options.mission_mode_checks.value = passthrough["MissionModeChecks"]
                self.options.auto_start_missions.value = passthrough["AutoStartMissions"]
                self.options.mission_blacklist.value = list(passthrough["MissionBlackList"].keys())

                self.options.twinkle_circuit_check.value = passthrough["TwinkleCircuitCheck"]
                self.options.twinkle_circuit_multiple_check.value = passthrough["MultipleTwinkleCircuitChecks"]
                self.options.sand_hill_check.value = passthrough["SandHillCheck"]
                self.options.sand_hill_check_hard.value = passthrough["SandHillCheckHard"]
                self.options.sky_chase_checks.value = passthrough["SkyChaseChecks"]
                self.options.sky_chase_checks_hard.value = passthrough["SkyChaseChecksHard"]

                self.options.enemy_sanity.value = passthrough["EnemySanity"]

                self.options.sonic_enemy_sanity.value = passthrough["SonicEnemySanity"]
                self.options.tails_enemy_sanity.value = passthrough["TailsEnemySanity"]
                self.options.knuckles_enemy_sanity.value = passthrough["KnucklesEnemySanity"]
                self.options.amy_enemy_sanity.value = passthrough["AmyEnemySanity"]
                self.options.big_enemy_sanity.value = passthrough["BigEnemySanity"]
                self.options.gamma_enemy_sanity.value = passthrough["GammaEnemySanity"]

                self.options.capsule_sanity.value = passthrough["CapsuleSanity"]
                self.options.pinball_capsules.value = passthrough["PinballCapsules"]

                self.options.sonic_capsule_sanity.value = passthrough["SonicCapsuleSanity"]
                self.options.tails_capsule_sanity.value = passthrough["TailsCapsuleSanity"]
                self.options.knuckles_capsule_sanity.value = passthrough["KnucklesCapsuleSanity"]
                self.options.amy_capsule_sanity.value = passthrough["AmyCapsuleSanity"]
                self.options.big_capsule_sanity.value = passthrough["BigCapsuleSanity"]
                self.options.gamma_capsule_sanity.value = passthrough["GammaCapsuleSanity"]

                self.options.life_capsule_sanity.value = passthrough["LifeCapsuleSanity"]
                self.options.shield_capsule_sanity.value = passthrough["ShieldCapsuleSanity"]
                self.options.powerup_capsule_sanity.value = passthrough["PowerUpCapsuleSanity"]
                self.options.ring_capsule_sanity.value = passthrough["RingCapsuleSanity"]
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
        create_sadx_regions(self, self.starter_setup, self.options)

    def create_items(self):
        self.item_distribution = create_sadx_items(self, self.starter_setup, self.options)

    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_item_table).name

    def set_rules(self):
        self.location_distribution = create_sadx_rules(self, self.item_distribution.emblem_count_progressive)

    def write_spoiler(self, spoiler_handle: typing.TextIO):
        write_sadx_spoiler(self, spoiler_handle, self.starter_setup, self.options)

    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        if not self.options.entrance_randomizer:
            return

        sadx_hint_data = {}
        level_area_strings = [pascal_to_space(area.name) + " (" for area in level_areas]
        # Add level entrance hints if entrance randomizer is on
        for location in self.multiworld.get_locations(self.player):
            if any(location.parent_region.name.startswith(area_string) for area_string in level_area_strings):
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
            "EmblemsForPerfectChaos": self.item_distribution.emblem_count_progressive,
            "LevelForPerfectChaos": self.location_distribution.levels_for_perfect_chaos,
            "MissionForPerfectChaos": self.location_distribution.missions_for_perfect_chaos,
            "BossesForPerfectChaos": self.location_distribution.bosses_for_perfect_chaos,
            "StartingCharacter": self.starter_setup.character.value,
            "StartingArea": self.starter_setup.area.value,
            "SonicStartingArea": self.starter_setup.get_starting_area(Character.Sonic).value,
            "TailsStartingArea": self.starter_setup.get_starting_area(Character.Tails).value,
            "KnucklesStartingArea": self.starter_setup.get_starting_area(Character.Knuckles).value,
            "AmyStartingArea": self.starter_setup.get_starting_area(Character.Amy).value,
            "GammaStartingArea": self.starter_setup.get_starting_area(Character.Gamma).value,
            "BigStartingArea": self.starter_setup.get_starting_area(Character.Big).value,
            "EntranceRandomizer": self.options.entrance_randomizer.value,
            "LevelEntranceMap": {original.value: randomized.value for original, randomized in
                                 self.starter_setup.level_mapping.items()},

            "StartingCharacterOption": self.options.starting_character.value,
            "StartingLocationOption": self.options.starting_location.value,
            "RandomStartingLocationPerCharacter": self.options.random_starting_location_per_character.value,
            "GuaranteedStartingChecks": self.options.guaranteed_starting_checks.value,
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
            "SonicEnemySanity": self.options.sonic_enemy_sanity.value,
            "TailsEnemySanity": self.options.tails_enemy_sanity.value,
            "KnucklesEnemySanity": self.options.knuckles_enemy_sanity.value,
            "AmyEnemySanity": self.options.amy_enemy_sanity.value,
            "BigEnemySanity": self.options.big_enemy_sanity.value,
            "GammaEnemySanity": self.options.gamma_enemy_sanity.value,
            "CapsuleSanity": self.options.capsule_sanity.value,
            "PinballCapsules": self.options.pinball_capsules.value,
            "SonicCapsuleSanity": self.options.sonic_capsule_sanity.value,
            "TailsCapsuleSanity": self.options.tails_capsule_sanity.value,
            "KnucklesCapsuleSanity": self.options.knuckles_capsule_sanity.value,
            "AmyCapsuleSanity": self.options.amy_capsule_sanity.value,
            "BigCapsuleSanity": self.options.big_capsule_sanity.value,
            "GammaCapsuleSanity": self.options.gamma_capsule_sanity.value,
            "LifeCapsuleSanity": self.options.life_capsule_sanity.value,
            "ShieldCapsuleSanity": self.options.shield_capsule_sanity.value,
            "PowerUpCapsuleSanity": self.options.powerup_capsule_sanity.value,
            "RingCapsuleSanity": self.options.ring_capsule_sanity.value,
            "FishSanity": self.options.fish_sanity.value,
            "LazyFishing": self.options.lazy_fishing.value,

            "ProgressionItems": self.generate_progression_data(),

            "DeathLink": self.options.death_link.value,
            "SendDeathLinkChance": self.options.send_death_link_chance.value,
            "ReceiveDeathLinkChance": self.options.receive_death_link_chance.value,
            "RingLink": self.options.ring_link.value,
            "CasinopolisRingLink": self.options.casinopolis_ring_link.value,
            "HardRingLink": self.options.hard_ring_link.value,
            "RingLoss": self.options.ring_loss.value,
            "TrapLink": self.options.trap_link.value,
            "TwinkleCircuitCheck": self.options.twinkle_circuit_check.value,
            "MultipleTwinkleCircuitChecks": self.options.twinkle_circuit_multiple_check.value,
            "SandHillCheck": self.options.sand_hill_check.value,
            "SandHillCheckHard": self.options.sand_hill_check_hard.value,
            "SkyChaseChecks": self.options.sky_chase_checks.value,
            "SkyChaseChecksHard": self.options.sky_chase_checks_hard.value,

            "MusicSource": self.options.music_source.value,
            "MusicShuffle": self.options.music_shuffle.value,
            "MusicShuffleConsistency": self.options.music_shuffle_consistency.value,
            "LifeCapsulesChangeSongs": self.options.life_capsules_change_songs.value,
            "MusicShuffleSeed": self.multiworld.seed % (2 ** 31),

            "BossChecks": self.options.boss_checks.value,
            "UnifyChaos4": self.options.unify_chaos4.value,
            "UnifyChaos6": self.options.unify_chaos6.value,
            "UnifyEggHornet": self.options.unify_egg_hornet.value,

            "RandomizedSonicUpgrades": self.options.randomized_sonic_upgrades.value,
            "RandomizedTailsUpgrades": self.options.randomized_tails_upgrades.value,
            "RandomizedKnucklesUpgrades": self.options.randomized_knuckles_upgrades.value,
            "RandomizedAmyUpgrades": self.options.randomized_amy_upgrades.value,
            "RandomizedGammaUpgrades": self.options.randomized_big_upgrades.value,
            "RandomizedBigUpgrades": self.options.randomized_gamma_upgrades.value,

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
