import math

from worlds.generic.Rules import add_rule
from .CharacterUtils import get_playable_characters, is_level_playable, is_character_playable
from .Enums import LevelMission, Character
from .Locations import get_location_by_name, level_location_table, upgrade_location_table, sub_level_location_table, \
    LocationInfo, capsule_location_table, boss_location_table, mission_location_table, field_emblem_location_table
from .Logic import LevelLocation, UpgradeLocation, SubLevelLocation, EmblemLocation, CharacterUpgrade, \
    CapsuleLocation, BossFightLocation, MissionLocation, chao_egg_location_table, ChaoEggLocation, \
    chao_race_location_table, enemy_location_table, EnemyLocation, fish_location_table, FishLocation
from .Names import ItemName
from .Regions import get_region_name


class LocationDistribution:
    def __init__(self, levels_for_perfect_chaos=0, missions_for_perfect_chaos=0, bosses_for_perfect_chaos=0):
        self.levels_for_perfect_chaos = levels_for_perfect_chaos
        self.missions_for_perfect_chaos = missions_for_perfect_chaos
        self.bosses_for_perfect_chaos = bosses_for_perfect_chaos


def add_level_rules(self, location_name: str, level: LevelLocation):
    location = self.multiworld.get_location(location_name, self.player)
    for need in level.get_logic_items(self.options):
        add_rule(location, lambda state, item=need: state.has(item, self.player))
    if self.options.lazy_fishing.value == 3 and level.character == Character.Big and (
            level.levelMission == LevelMission.B or level.levelMission == LevelMission.A or level.levelMission == LevelMission.S):
        add_rule(location, lambda state: state.has(ItemName.Big.PowerRod, self.player))


def add_upgrade_rules(self, location_name: str, upgrade: UpgradeLocation):
    location = self.multiworld.get_location(location_name, self.player)
    logic_items = upgrade.get_logic_items(self.options)
    if all(isinstance(item, str) for item in logic_items):
        for need in logic_items:
            add_rule(location, lambda state, item=need: state.has(item, self.player))
    else:
        add_rule(location, lambda state, egg_requirements=logic_items: any(
            all(state.has(item, self.player) for item in requirement_group) for requirement_group in egg_requirements))


def add_sub_level_rules(self, location_name: str, sub_level: SubLevelLocation):
    location = self.multiworld.get_location(location_name, self.player)
    add_rule(location, lambda state: any(
        state.can_reach_region(get_region_name(character, sub_level.area), self.player) for character in
        sub_level.get_logic_characters(self.options) if character in get_playable_characters(self.options)))


def add_field_emblem_rules(self, location_name: str, field_emblem: EmblemLocation):
    location = self.multiworld.get_location(location_name, self.player)
    # We check if the player has any of the character / character+upgraded needed
    add_rule(location, lambda state: any(
        (state.can_reach_region(
            get_region_name(character.character if isinstance(character, CharacterUpgrade) else character,
                            field_emblem.area), self.player) and
         (state.has(character.upgrade, self.player) if isinstance(character, CharacterUpgrade) else True))
        for character in field_emblem.get_logic_characters_upgrades(self.options) if
        character in get_playable_characters(self.options) or
        (isinstance(character, CharacterUpgrade) and character.character in get_playable_characters(self.options))))


def add_capsule_rules(self, location_name: str, life_capsule: CapsuleLocation):
    location = self.multiworld.get_location(location_name, self.player)
    for need in life_capsule.get_logic_items(self.options):
        add_rule(location, lambda state, item=need: state.has(item, self.player))


def add_boss_fight_rules(self, location_name: str, boss_fight: BossFightLocation):
    location = self.multiworld.get_location(location_name, self.player)
    if not boss_fight.unified:
        return
    add_rule(location, lambda state: any(
        state.can_reach_region(get_region_name(character, boss_fight.area), self.player) for character in
        boss_fight.characters if character in get_playable_characters(self.options)))


def add_mission_rules(self, location_name: str, mission: MissionLocation):
    location = self.multiworld.get_location(location_name, self.player)
    card_area_name = get_region_name(mission.character, mission.cardArea)
    if not self.options.auto_start_missions:
        add_rule(location, lambda state, card_area=card_area_name: state.can_reach_region(card_area, self.player))

    logic_items = mission.get_logic_items(self.options)
    if all(isinstance(item, str) for item in logic_items):
        for need in logic_items:
            add_rule(location, lambda state, item=need: state.has(item, self.player))
    else:
        add_rule(location, lambda state, requirements=logic_items: any(
            all(state.has(item, self.player) for item in requirement_group) for requirement_group in requirements))
    # If lazy fishing is enabled, we need the Big Power Rod for certain missions
    if self.options.lazy_fishing.value == 3 and mission.missionNumber in [14, 29, 35, 44]:
        add_rule(location, lambda state: state.has(ItemName.Big.PowerRod, self.player))


def add_egg_rules(self, location_name: str, egg: ChaoEggLocation):
    location = self.multiworld.get_location(location_name, self.player)
    add_rule(location, lambda state: any(
        state.can_reach_region(get_region_name(character, egg.area), self.player) for character in
        egg.characters if character in get_playable_characters(self.options)))
    if egg.requirements:
        add_rule(location, lambda state, egg_requirements=egg.requirements: any(
            all(state.has(item, self.player) for item in requirement_group) for requirement_group in egg_requirements))


def add_race_rules(self, location_name: str):
    location = self.multiworld.get_location(location_name, self.player)

    level_location_list = []
    for level in level_location_table:
        if is_level_playable(level, self.options) and level.levelMission == LevelMission.C:
            level_location_list.append(self.multiworld.get_location(level.get_level_name(), self.player))

    self.random.shuffle(level_location_list)
    num_locations = max(1, math.ceil(
        len(level_location_list) * self.options.chao_races_levels_to_access_percentage.value / 100))
    for level_location in level_location_list[:num_locations]:
        add_rule(location, lambda state, loc=level_location: loc.can_reach(state))


def add_enemy_rules(self, location_name: str, enemy: EnemyLocation):
    location = self.multiworld.get_location(location_name, self.player)
    for need in enemy.get_logic_items(self.options):
        add_rule(location, lambda state, item=need: state.has(item, self.player))


def add_fish_rules(self, location_name: str, fish: FishLocation):
    location = self.multiworld.get_location(location_name, self.player)
    for need in fish.get_logic_items(self.options):
        add_rule(location, lambda state, item=need: state.has(item, self.player))
    if self.options.lazy_fishing.value >= 2:
        add_rule(location, lambda state: state.has(ItemName.Big.PowerRod, self.player))


def calculate_rules(self, location: LocationInfo):
    if location is None:
        return
    for level in level_location_table:
        if location["id"] == level.locationId:
            add_level_rules(self, location["name"], level)
    for upgrade in upgrade_location_table:
        if location["id"] == upgrade.locationId:
            add_upgrade_rules(self, location["name"], upgrade)
    for sub_level in sub_level_location_table:
        if location["id"] == sub_level.locationId:
            add_sub_level_rules(self, location["name"], sub_level)
    for life_capsule in capsule_location_table:
        if location["id"] == life_capsule.locationId:
            add_capsule_rules(self, location["name"], life_capsule)
    for field_emblem in field_emblem_location_table:
        if location["id"] == field_emblem.locationId:
            add_field_emblem_rules(self, location["name"], field_emblem)
    for boss_fight in boss_location_table:
        if location["id"] == boss_fight.locationId:
            add_boss_fight_rules(self, location["name"], boss_fight)
    for mission in mission_location_table:
        if location["id"] == mission.locationId:
            add_mission_rules(self, location["name"], mission)
    for egg in chao_egg_location_table:
        if location["id"] == egg.locationId:
            add_egg_rules(self, location["name"], egg)
    for race in chao_race_location_table:
        if location["id"] == race.locationId:
            add_race_rules(self, location["name"])
    for enemy in enemy_location_table:
        if location["id"] == enemy.locationId:
            add_enemy_rules(self, location["name"], enemy)
    for fish in fish_location_table:
        if location["id"] == fish.locationId:
            add_fish_rules(self, location["name"], fish)


def create_sadx_rules(self, needed_emblems: int) -> LocationDistribution:
    levels_for_perfect_chaos = 0
    missions_for_perfect_chaos = 0
    bosses_for_perfect_chaos = 0
    for ap_location in self.multiworld.get_locations(self.player):
        calculate_rules(self, get_location_by_name(ap_location.name))

    perfect_chaos_fight = self.multiworld.get_location("Perfect Chaos Fight", self.player)
    perfect_chaos_fight.place_locked_item(self.create_item(ItemName.Progression.ChaosPeace))

    if self.options.goal_requires_emblems.value:
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.Emblem, self.player, needed_emblems))

    if self.options.goal_requires_levels.value:
        level_location_list = []
        for level in level_location_table:
            if is_level_playable(level, self.options) and level.levelMission == LevelMission.C:
                level_location_list.append(self.multiworld.get_location(level.get_level_name(), self.player))

        self.random.shuffle(level_location_list)
        num_locations = max(1, math.ceil(len(level_location_list) * self.options.levels_percentage.value / 100))
        for location in level_location_list[:num_locations]:
            add_rule(perfect_chaos_fight, lambda state, loc=location: loc.can_reach(state))
            levels_for_perfect_chaos += 1

    if self.options.goal_requires_missions.value:
        mission_location_list = []
        for mission in mission_location_table:
            if str(mission.missionNumber) in self.options.mission_blacklist.value:
                continue
            if str(mission.character.name) in self.options.mission_blacklist.value:
                continue
            if is_character_playable(mission.character, self.options) and self.options.mission_mode_checks:
                mission_location_list.append(self.multiworld.get_location(mission.get_mission_name(), self.player))

        self.random.shuffle(mission_location_list)
        num_locations = max(1, math.ceil(len(mission_location_list) * self.options.mission_percentage.value / 100))
        for location in mission_location_list[:num_locations]:
            add_rule(perfect_chaos_fight, lambda state, loc=location: loc.can_reach(state))
            missions_for_perfect_chaos += 1

    if self.options.goal_requires_bosses.value:
        bosses_location_list = []
        for ap_location in self.multiworld.get_locations(self.player):
            location = get_location_by_name(ap_location.name)
            for boss_fight in boss_location_table:
                if location["id"] == boss_fight.locationId:
                    bosses_location_list.append(self.multiworld.get_location(boss_fight.get_boss_name(), self.player))

        self.random.shuffle(bosses_location_list)
        num_locations = max(1, math.ceil(len(bosses_location_list) * self.options.boss_percentage.value / 100))
        for location in bosses_location_list[:num_locations]:
            add_rule(perfect_chaos_fight, lambda state, loc=location: loc.can_reach(state))
            bosses_for_perfect_chaos += 1

    if self.options.goal_requires_chao_races.value:
        for chao_race in chao_race_location_table:
            chao_race_location = self.multiworld.get_location(chao_race.name, self.player)
            add_rule(perfect_chaos_fight, lambda state, loc=chao_race_location: loc.can_reach(state))

    if self.options.goal_requires_chaos_emeralds.value:
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.WhiteEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.RedEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.CyanEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.PurpleEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.GreenEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.YellowEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.BlueEmerald, self.player))

    self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.Progression.ChaosPeace,
                                                                                self.player)
    return LocationDistribution(
        levels_for_perfect_chaos=levels_for_perfect_chaos,
        missions_for_perfect_chaos=missions_for_perfect_chaos,
        bosses_for_perfect_chaos=bosses_for_perfect_chaos,
    )
