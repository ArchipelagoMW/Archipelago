import collections
import logging
import re
from dataclasses import dataclass, field
from typing import List, TextIO

from Options import OptionError
from worlds.AutoWorld import World
from .CharacterUtils import get_playable_characters, are_character_upgrades_randomized, is_level_playable, \
    is_character_playable
from .Enums import Character, Area, SubLevel, pascal_to_space, level_areas, LevelMission
from .Locations import level_location_table, upgrade_location_table, sub_level_location_table, \
    field_emblem_location_table, boss_location_table, capsule_location_table, mission_location_table
from .Logic import area_connections, chao_egg_location_table, enemy_location_table, fish_location_table
from .Options import SonicAdventureDXOptions


@dataclass
class CharacterArea:
    character: Character
    area: Area = None


@dataclass
class StarterSetup:
    character: Character = None
    area: Area = None
    charactersWithArea: List[CharacterArea] = field(default_factory=list)
    level_mapping: dict[Area, Area] = field(default_factory=dict)

    def get_starting_area(self, character: Character) -> Area:
        for char_area in self.charactersWithArea:
            if char_area.character == character:
                return char_area.area
        return self.area


def generate_early_sadx(world: World, options: SonicAdventureDXOptions) -> StarterSetup:
    validate_settings(options)

    starter_setup = StarterSetup()
    possible_characters = get_playable_characters(options)

    world.random.shuffle(possible_characters)

    if options.starting_character.value != 0:
        possible_characters.remove(Character(options.starting_character.value))
        possible_characters.insert(0, Character(options.starting_character.value))

    if options.entrance_randomizer:
        fixed_areas = {Area[re.sub(r' ', '', area)]: Area[re.sub(r' ', '', dest)]
                       for area, dest in options.level_entrance_plando.items()}
        remaining_areas = [area for area in level_areas if area not in fixed_areas.values()]
        randomized_remaining_areas = world.random.sample(remaining_areas, len(remaining_areas))
        starter_setup.level_mapping = {**fixed_areas, **dict(
            zip([area for area in level_areas if area not in fixed_areas], randomized_remaining_areas))}

    for character in possible_characters:
        possible_starter_areas = get_possible_starting_areas(world, character, starter_setup.level_mapping)

        if any(count >= options.guaranteed_starting_checks for count in possible_starter_areas.values()):
            possible_starter_areas = {area: count for area, count in possible_starter_areas.items() if
                                      count >= options.guaranteed_starting_checks}
        else:
            max_count = max(possible_starter_areas.values())
            possible_starter_areas = {area: count for area, count in possible_starter_areas.items() if
                                      count == max_count}

        if possible_starter_areas.keys():
            if options.starting_location.value > 0 and Area(options.starting_location.value - 1) in list(
                    possible_starter_areas.keys()):
                starter_setup.area = Area(options.starting_location.value - 1)
            else:
                starter_setup.area = world.random.choice(list(possible_starter_areas.keys()))
            starter_setup.character = character
            break

    if not starter_setup.area:
        raise OptionError(
            "SADX Error: Couldn't define a valid starting location (Probably a problem of low settings, guaranteed level and/or fixed starting location).")

    if options.random_starting_location_per_character:
        used_areas = {starter_setup.area}
        starter_setup.charactersWithArea.append(CharacterArea(starter_setup.character, starter_setup.area))
        possible_areas_dict = {char: get_possible_starting_areas(world, char, starter_setup.level_mapping) for
                               char in
                               possible_characters}
        filtered_areas_dict = {char: list(areas_dict.keys()) for char, areas_dict in possible_areas_dict.items()}
        characters_sorted_by_areas = sorted(possible_characters, key=lambda char: len(filtered_areas_dict[char]))

        for character in characters_sorted_by_areas:
            if character == starter_setup.character:
                continue
            unused_areas = [area for area in filtered_areas_dict[character] if area not in used_areas]
            area = world.random.choice(unused_areas if unused_areas else filtered_areas_dict[character])
            used_areas.add(area)
            starter_setup.charactersWithArea.append(CharacterArea(character, area))

    return starter_setup


def validate_settings(options):
    if not get_playable_characters(options):
        logging.warning(" -- SADX warning: Zero playable characters in settings. enabling Sonic as a failsafe.")
        options.playable_sonic.value = True

    if options.starting_character.value > 0:
        if Character(options.starting_character.value) not in get_playable_characters(options):
            logging.warning(
                " -- SADX warning: Starting character is not playable. Randomizing starting character.")
            options.starting_character.value = 0

    if (not options.goal_requires_levels and not options.goal_requires_missions and not options.goal_requires_emblems
            and not options.goal_requires_chaos_emeralds and not options.goal_requires_bosses and not options.goal_requires_chao_races):
        logging.warning(" -- SADX warning: No goal requirement set. Enabling action stages requirement as a failsafe.")
        options.goal_requires_levels.value = True

    if options.goal_requires_levels.value or options.chao_races_checks:
        levels_available = False
        for level in level_location_table:
            if is_level_playable(level, options) and level.levelMission == LevelMission.C:
                levels_available = True
        if not levels_available:
            options.sonic_action_stage_missions.value = 1
            options.tails_action_stage_missions.value = 1
            options.knuckles_action_stage_missions.value = 1
            options.amy_action_stage_missions.value = 1
            options.big_action_stage_missions.value = 1
            options.gamma_action_stage_missions.value = 1
            if options.goal_requires_levels.value and not options.chao_races_checks:
                logging.warning(
                    " -- SADX warning: No action stages enabled with levels as goal. Enabling all characters levels as a failsafe")
            elif not options.goal_requires_levels.value and options.chao_races_checks:
                logging.warning(
                    " -- SADX warning: No action stages enabled with chao races as checks. Enabling all characters levels as a failsafe")
            else:
                logging.warning(
                    " -- SADX warning: No action stages enabled with chao races and levels as goal. Enabling all characters levels as a failsafe")

    if options.goal_requires_missions.value:
        if not options.mission_mode_checks.value:
            logging.warning(
                " -- SADX warning: Missions as goal requirement are enabled but mission mode checks are disabled. Enabling mission mode checks.")
            options.mission_mode_checks.value = True
    if options.goal_requires_bosses.value:
        if not options.boss_checks.value:
            logging.warning(
                " -- SADX warning: Bosses as goal requirement are enabled but mission mode checks are disabled. Enabling bosses checks.")
            options.boss_checks.value = True
    if options.goal_requires_chao_races.value:
        if not options.chao_races_checks.value:
            logging.warning(
                " -- SADX warning: Chao Races as goal requirements are enabled but chao races checks are disabled. Enabling chao races checks.")
            options.chao_races_checks.value = True

        mission_quantity = 0
        for mission in mission_location_table:
            if str(mission.missionNumber) in options.mission_blacklist.value:
                continue
            if str(mission.character.name) in options.mission_blacklist.value:
                continue
            if is_character_playable(mission.character, options):
                mission_quantity += 1
        if mission_quantity == 0:
            raise OptionError(
                " -- SADX Error: You need to add more missions in the settings to use mission as goal. Either add more characters or remove missions from the blacklist.")

    if options.capsule_sanity.value:
        if not options.life_capsule_sanity.value and not options.shield_capsule_sanity.value and not options.powerup_capsule_sanity and not options.ring_capsule_sanity:
            logging.warning(
                " -- SADX warning: Capsule-sanity is enabled but all capsule types are disabled. Enabling life capsules.")
            options.life_capsule_sanity.value = True

    if options.logic_level.value == 0 and (
            options.sonic_action_stage_missions.value == 4 or options.tails_action_stage_missions.value == 4
            or options.knuckles_action_stage_missions.value == 4 or options.amy_action_stage_missions.value == 4
            or options.big_action_stage_missions.value == 4 or options.gamma_action_stage_missions.value == 4):
        raise OptionError(
            " -- SADX error: S-Rank missions are not available for normal logic, please select a harder logic level.")


def get_possible_starting_areas(world, character: Character, level_mapping: dict[Area, Area]) -> \
        dict[Area, int]:
    possible_starting_areas = {}
    areas = [Area.StationSquareMain, Area.Station, Area.Hotel, Area.Casino, Area.TwinkleParkLobby,
             Area.MysticRuinsMain, Area.AngelIsland, Area.Jungle, Area.EggCarrierOutside, Area.EggCarrierInside]
    for area in areas:
        possible_list_for_area = get_possible_starting_area_information(character, area, world.options, level_mapping)
        if possible_list_for_area:
            possible_starting_areas.update(possible_list_for_area)

    return possible_starting_areas


def get_possible_starting_area_information(character: Character, area: Area, options: SonicAdventureDXOptions,
                                           level_mapping: dict[Area, Area]) -> \
        dict[Area, int]:
    possible_locations = collections.defaultdict(int)

    for level in level_location_table:
        if is_level_playable(level, options):
            actual_area_to = level.area
            if options.entrance_randomizer:
                for level_entrance, actual_level in level_mapping.items():
                    if actual_level == level.area:
                        actual_area_to = level_entrance
            key = (character, area, actual_area_to)
            if key in area_connections and not area_connections[key][options.logic_level.value]:
                if level.character == character and not level.get_logic_items(options):
                    possible_locations[area] += 1

    if are_character_upgrades_randomized(character, options):
        for upgrade in upgrade_location_table:
            if upgrade.character == character and upgrade.area == area and not upgrade.get_logic_items(options):
                possible_locations[area] += 1
    if options.sand_hill_check:
        for sub_level in sub_level_location_table:
            if sub_level.subLevel == SubLevel.SandHill:
                if character in sub_level.get_logic_characters(options) and sub_level.area == area:
                    possible_locations[area] += 1
    if options.twinkle_circuit_check:
        for sub_level in sub_level_location_table:
            if sub_level.subLevel == SubLevel.TwinkleCircuit and sub_level.subLevelMission == LevelMission.B:
                if character in sub_level.get_logic_characters(options) and sub_level.area == area:
                    possible_locations[area] += 1
    if options.sky_chase_checks:
        for sub_level in sub_level_location_table:
            if sub_level.subLevel == SubLevel.SkyChaseAct1 or sub_level.subLevel == SubLevel.SkyChaseAct2:
                if character in sub_level.get_logic_characters(options) and sub_level.area == area:
                    possible_locations[area] += 1
    if options.field_emblems_checks:
        for field_emblem in field_emblem_location_table:
            if character in field_emblem.get_logic_characters_upgrades(options) and field_emblem.area == area:
                possible_locations[area] += 1
    if options.boss_checks:
        for boss_fight in boss_location_table:
            if character in boss_fight.characters and boss_fight.area == area:
                possible_locations[area] += 1
    if options.capsule_sanity:
        for life_capsule in capsule_location_table:
            actual_area_to = life_capsule.area
            if options.entrance_randomizer:
                for level_entrance, actual_level in level_mapping.items():
                    if actual_level == life_capsule.area:
                        actual_area_to = level_entrance
            key = (character, area, actual_area_to)
            if key in area_connections and not area_connections[key][options.logic_level.value]:
                if life_capsule.character == character and not life_capsule.get_logic_items(options):
                    possible_locations[area] += 1
    if options.mission_mode_checks:
        for mission in mission_location_table:
            if str(mission.missionNumber) in options.mission_blacklist.value:
                continue
            if str(mission.character.name) in options.mission_blacklist.value:
                continue
            if (mission.character == character and mission.cardArea == area
                    and mission.objectiveArea == area and not mission.get_logic_items(options)):
                possible_locations[area] += 1
    if options.chao_egg_checks:
        for egg in chao_egg_location_table:
            if character in egg.characters and egg.area == area and not egg.requirements:
                possible_locations[area] += 1
    if options.enemy_sanity:
        for enemy in enemy_location_table:
            actual_area_to = enemy.area
            if options.entrance_randomizer:
                for level_entrance, actual_level in level_mapping.items():
                    if actual_level == enemy.area:
                        actual_area_to = level_entrance
            key = (character, area, actual_area_to)
            if key in area_connections and not area_connections[key][options.logic_level.value]:
                if enemy.character == character and not enemy.get_logic_items(options):
                    possible_locations[area] += 1
    if options.fish_sanity:
        for fish in fish_location_table:
            actual_area_to = fish.area
            if options.entrance_randomizer:
                for level_entrance, actual_level in level_mapping.items():
                    if actual_level == fish.area:
                        actual_area_to = level_entrance
            key = (character, area, actual_area_to)
            if key in area_connections and not area_connections[key][options.logic_level.value]:
                if Character.Big == character and not fish.get_logic_items(options):
                    possible_locations[area] += 1

    return possible_locations


def write_sadx_spoiler(world: World, spoiler_handle: TextIO, starter_setup: StarterSetup,
                       options: SonicAdventureDXOptions):
    spoiler_handle.write("\n")
    header_text = f"Sonic Adventure starting setup for {world.multiworld.player_name[world.player]}:\n"
    spoiler_handle.write(header_text)

    starting_area_name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', starter_setup.area.name)

    text = "- Will start as {0} in the {1} area.\n"
    text = text.format(starter_setup.character.name, starting_area_name)

    for characterArea in starter_setup.charactersWithArea:
        if characterArea.character == starter_setup.character:
            continue
        starting_area_name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', characterArea.area.name)
        text += "- {0} will spawn in the {1} area.\n".format(characterArea.character.name, starting_area_name)

    if options.entrance_randomizer:
        text += f"\nLevel entrances:\n"
        for original, randomized in starter_setup.level_mapping.items():
            text += f"- {pascal_to_space(original.name)} -> {pascal_to_space(randomized.name)}\n"
    spoiler_handle.writelines(text)
