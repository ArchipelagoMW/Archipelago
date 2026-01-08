from dataclasses import dataclass
from typing import Dict, Tuple

from BaseClasses import Region
from .CharacterUtils import is_character_playable
from .CharacterUtils import is_level_playable, \
    get_playable_characters, get_playable_character_item, is_any_character_playable, character_has_enemy_sanity, \
    character_has_capsule_sanity
from .Enums import Area, Character, SubLevelMission, SubLevel, pascal_to_space, Capsule
from .Locations import SonicAdventureDXLocation, \
    upgrade_location_table, level_location_table, mission_location_table, boss_location_table, sub_level_location_table, \
    field_emblem_location_table
from .Logic import area_connections, chao_egg_location_table, chao_race_location_table, enemy_location_table, \
    capsule_location_table, fish_location_table
from .Names import LocationName
from .Options import SonicAdventureDXOptions
from .StartingSetup import StarterSetup
from ..AutoWorld import World


@dataclass
class AreaConnection:
    areaFrom: Area
    areaTo: Area
    character: Character
    item: str


def get_region_name(character: Character, area: Area) -> str:
    return "{} ({})".format(pascal_to_space(area.name), character.name)


def get_entrance_name(character: Character, area: Area) -> str:
    return "{} Entrance ({})".format(pascal_to_space(area.name), character.name)


def create_sadx_regions(world: World, starter_setup: StarterSetup, options: SonicAdventureDXOptions):
    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)

    # Create regions for each character in each area
    created_regions: Dict[Tuple[Character, Area], Region] = {}
    for area in Area:
        for character in get_playable_characters(options):
            region = Region(get_region_name(character, area), world.player, world.multiworld)
            world.multiworld.regions.append(region)
            add_locations_to_region(region, area, character, world.player, options)
            created_regions[(character, area)] = region
            if area == starter_setup.get_starting_area(character):
                menu_region.connect(region, None,
                                    lambda state, item=get_playable_character_item(character): state.has(item,
                                                                                                         world.player))

    # Connect regions based on area connections rules
    for (character, area_from, area_to), (normal_logic_items, hard_logic_items, expert_dc_logic_items,
                                          expert_dx_logic_items, expert_plus_dx_logic_items) in area_connections.items():

        if options.entrance_randomizer:
            actual_area = starter_setup.level_mapping.get(area_to, area_to)
        else:
            actual_area = area_to

        region_from = created_regions.get((character, area_from))
        region_to = created_regions.get((character, actual_area))

        if options.logic_level.value == 4:
            key_items = expert_plus_dx_logic_items
        elif options.logic_level.value == 3:
            key_items = expert_dx_logic_items
        elif options.logic_level.value == 2:
            key_items = expert_dc_logic_items
        elif options.logic_level.value == 1:
            key_items = hard_logic_items
        else:
            key_items = normal_logic_items

        if Area.EmeraldCoast.value <= area_to.value <= Area.HotShelter.value:
            entrance_name = get_entrance_name(character, area_to)
        else:
            entrance_name = None

        if region_from and region_to:
            if key_items:
                if all(isinstance(item, str) for item in key_items):
                    region_from.connect(region_to, entrance_name,
                                        lambda state, items=key_items: all(
                                            state.has(item, world.player) for item in items))
                else:
                    region_from.connect(region_to, entrance_name,
                                        lambda state, items=key_items: any(
                                            all(state.has(item, world.player) for item in requirement_group) for
                                            requirement_group in items))
            else:
                region_from.connect(region_to, entrance_name)

    common_region = Region("Common region", world.player, world.multiworld)
    world.multiworld.regions.append(common_region)
    add_locations_to_common_region(common_region, world.player, options)
    menu_region.connect(common_region)

    perfect_chaos_area = Region("Perfect Chaos Fight", world.player, world.multiworld)
    perfect_chaos_fight = SonicAdventureDXLocation(world.player, 9, menu_region)
    perfect_chaos_fight.locked = True
    perfect_chaos_area.locations.append(perfect_chaos_fight)
    menu_region.connect(perfect_chaos_area)
    created_regions.clear()


def add_locations_to_region(region: Region, area: Area, character: Character, player: int,
                            options: SonicAdventureDXOptions):
    location_ids = get_location_ids_for_area(area, character, options)
    for location_id in location_ids:
        location = SonicAdventureDXLocation(player, location_id, region)
        region.locations.append(location)


def get_location_ids_for_area(area: Area, character: Character, options: SonicAdventureDXOptions):
    location_ids = []
    if area == Area.TwinkleParkLobby and options.twinkle_circuit_check and options.twinkle_circuit_multiple_check:
        for sub_level in sub_level_location_table:
            if sub_level.subLevel == SubLevel.TwinkleCircuit:
                if is_any_character_playable(sub_level.get_logic_characters(options), options):
                    if character in sub_level.get_logic_characters(options):
                        if sub_level.subLevelMission != SubLevelMission.B:
                            location_ids.append(sub_level.locationId)

    for level in level_location_table:
        if level.area == area and level.character == character:
            if is_level_playable(level, options):
                location_ids.append(level.locationId)
    for upgrade in upgrade_location_table:
        if upgrade.area == area and upgrade.character == character:
            if is_character_playable(upgrade.character, options):
                location_ids.append(upgrade.locationId)

    if options.capsule_sanity:
        for capsule in capsule_location_table:
            if capsule.area == area and capsule.character == character and is_character_playable(capsule.character,
                                                                                                 options):
                if character_has_capsule_sanity(capsule.character, options):
                    if 12548 <= capsule.locationId <= 12552 and not options.pinball_capsules.value:
                        continue
                    if capsule.type == Capsule.ExtraLife and options.life_capsule_sanity:
                        location_ids.append(capsule.locationId)
                    elif capsule.type in [Capsule.Shield, Capsule.MagneticShield] and options.shield_capsule_sanity:
                        location_ids.append(capsule.locationId)
                    elif (capsule.type in [Capsule.SpeedUp, Capsule.Invincibility, Capsule.Bomb]
                          and options.powerup_capsule_sanity):
                        location_ids.append(capsule.locationId)
                    elif (capsule.type in [Capsule.FiveRings, Capsule.TenRings, Capsule.RandomRings]
                          and options.ring_capsule_sanity):
                        location_ids.append(capsule.locationId)

    if options.enemy_sanity:
        for enemy in enemy_location_table:
            if enemy.area == area and enemy.character == character:
                if is_character_playable(enemy.character, options):
                    if character_has_enemy_sanity(enemy.character, options):
                        location_ids.append(enemy.locationId)

    if options.fish_sanity:
        for fish in fish_location_table:
            if fish.area == area and Character.Big == character:
                if is_character_playable(Character.Big, options):
                    location_ids.append(fish.locationId)

    if options.boss_checks:
        for boss_fight in boss_location_table:
            if boss_fight.area == area and len(boss_fight.characters) == 1 and boss_fight.characters[0] == character:
                if options.unify_chaos4 and boss_fight.boss == LocationName.Boss.Chaos4 and not boss_fight.unified:
                    continue
                if options.unify_chaos6 and boss_fight.boss == LocationName.Boss.Chaos6 and not boss_fight.unified:
                    continue
                if options.unify_egg_hornet and boss_fight.boss == LocationName.Boss.EggHornet and not boss_fight.unified:
                    continue
                if is_any_character_playable(boss_fight.characters, options):
                    location_ids.append(boss_fight.locationId)

    if options.mission_mode_checks:
        for mission in mission_location_table:
            if str(mission.missionNumber) in options.mission_blacklist.value:
                continue
            if str(mission.character.name) in options.mission_blacklist.value:
                continue
            if mission.objectiveArea == area and mission.character == character:
                if is_character_playable(mission.character, options):
                    location_ids.append(mission.locationId)

    return location_ids


def add_locations_to_common_region(region: Region, player: int, options: SonicAdventureDXOptions):
    location_ids = get_location_ids_for_common_region(options)
    for location_id in location_ids:
        location = SonicAdventureDXLocation(player, location_id, region)
        region.locations.append(location)


def get_location_ids_for_common_region(options):
    location_ids = []
    if options.sand_hill_check:
        for sub_level in sub_level_location_table:
            if sub_level.subLevel == SubLevel.SandHill:
                if is_any_character_playable(sub_level.get_logic_characters(options), options):
                    if ((options.sand_hill_check_hard and sub_level.subLevelMission == SubLevelMission.A)
                            or sub_level.subLevelMission == SubLevelMission.B):
                        location_ids.append(sub_level.locationId)

    if options.twinkle_circuit_check and not options.twinkle_circuit_multiple_check:
        for sub_level in sub_level_location_table:
            if sub_level.subLevel == SubLevel.TwinkleCircuit:
                if is_any_character_playable(sub_level.get_logic_characters(options), options):
                    if sub_level.subLevelMission == SubLevelMission.B:
                        location_ids.append(sub_level.locationId)
    if options.sky_chase_checks:
        for sub_level in sub_level_location_table:
            if sub_level.subLevel == SubLevel.SkyChaseAct1 or sub_level.subLevel == SubLevel.SkyChaseAct2:
                if is_any_character_playable(sub_level.get_logic_characters(options), options):
                    if ((options.sky_chase_checks_hard and sub_level.subLevelMission == SubLevelMission.A)
                            or sub_level.subLevelMission == SubLevelMission.B):
                        location_ids.append(sub_level.locationId)

    if options.field_emblems_checks:
        for field_emblem in field_emblem_location_table:
            if is_any_character_playable(field_emblem.get_logic_characters(options), options):
                location_ids.append(field_emblem.locationId)

    if options.boss_checks:
        for boss_fight in boss_location_table:
            if not boss_fight.unified:
                continue
            if not options.unify_chaos4 and boss_fight.boss == LocationName.Boss.Chaos4 and boss_fight.unified:
                continue
            if not options.unify_chaos6 and boss_fight.boss == LocationName.Boss.Chaos6 and boss_fight.unified:
                continue
            if not options.unify_egg_hornet and boss_fight.boss == LocationName.Boss.EggHornet and boss_fight.unified:
                continue
            if is_any_character_playable(boss_fight.characters, options):
                location_ids.append(boss_fight.locationId)

    if options.chao_egg_checks:
        for egg in chao_egg_location_table:
            if is_any_character_playable(egg.characters, options):
                location_ids.append(egg.locationId)

    if options.chao_races_checks:
        for race in chao_race_location_table:
            location_ids.append(race.locationId)

    return location_ids
