from __future__ import annotations

from BaseClasses import CollectionState
from .constants import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from worlds.sonic_heroes import SonicHeroesWorld

from worlds.sonic_heroes.options import UnlockType

def can_homing_hover(world: SonicHeroesWorld, team: str, level: str, state: CollectionState) -> bool:
    return False

def can_tornado_hover(world: SonicHeroesWorld, team: str, level: str, state: CollectionState) -> bool:
    return False

def can_rocket_accel_jump(world: SonicHeroesWorld, team: str, level: str, state: CollectionState) -> bool:
    return False


def can_team_blast(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):

    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    #return False
    region: str = get_region_name_from_level(world, level)
    item_requirements = []
    for char_name in team_char_names[team]:
        item_requirements += get_all_ability_item_names_for_character_and_region(world, team, char_name, region)

    if not state.has_from_list_unique(item_requirements, world.player, len(item_requirements)):
        return False

    return has_char(world, team, level, state, speed=True, flying=True, power=True)

def has_char(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, speed: bool = False, flying: bool = False, power: bool = False, orcondition: bool = False) -> bool:
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    conditions = []
    if speed:
        conditions.append(get_playable_char_item_name(get_char_name_from_team(team, speed=True)))
    if flying:
        conditions.append(get_playable_char_item_name(get_char_name_from_team(team, flying=True)))
    if power:
        conditions.append(get_playable_char_item_name(get_char_name_from_team(team, power=True)))


    if orcondition:
        return state.has_any(conditions, world.player)

    else:
        return state.has_all(conditions, world.player)


def has_char_levelup(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, levelup: int, speed: bool = False, flying: bool = False, power: bool = False):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    region: str = get_region_name_from_level(world, level)
    if levelup < 1 or levelup > 3:
        print(f"Has Char LevelUp Called with bad LevelUp {levelup}")
        return False
    if sum([speed, flying, power]) != 1:
        print(f"Has Char LevelUp Called with bad number of chars. team {team} level {level} levelup {levelup} speed {speed} flying {flying} power {power}")
        return False
    #no abilities lvl 0
    #<= 49% lvl 1
    #<= 99% lvl 2
    #all abilities lvl 3
    if speed:
        char_name = team_char_names[team][0]
    elif power:
        char_name = team_char_names[team][1]
    else:       # flying
        char_name = team_char_names[team][2]


    abilities = get_all_ability_item_names_for_character_and_region(world, team, char_name, region)
    item_requirements: dict[int, float] = \
    {
        #0: 0,
        1: 1,
        2: len(abilities)/2,
        3: len(abilities),
    }

    return state.count_from_list_unique(abilities, world.player) >= item_requirements[levelup]


def can_homing_attack(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    #name, amount = get_item_req_for_ability(world, get_char_name_from_team(team, speed=True), get_region_name_from_level(world, level), HOMINGATTACK)
    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), HOMINGATTACK)
    return has_char(world, team, level, state, speed=True) and state.has(name, world.player)

def can_tornado(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), TORNADO)
    return has_char(world, team, level, state, speed=True) and state.has(name, world.player)

def can_rocket_accel(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), ROCKETACCEL)
    return has_char(world, team, level, state, speed=True) and state.has(name, world.player) and has_char(world, team, level, state, flying=True, power=True, orcondition=True)

def can_light_dash(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), LIGHTDASH)
    return has_char(world, team, level, state, speed=True) and state.has(name, world.player)

def can_triangle_jump(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), TRIANGLEJUMP)
    name2 = get_ability_item_name(world, team, get_region_name_from_level(world, level), HOMINGATTACK)
    return has_char(world, team, level, state, speed=True) and state.has(name, world.player) and state.has(name2, world.player)

def can_light_attack(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), LIGHTATTACK)
    return has_char(world, team, level, state, speed=True) and state.has(name, world.player)

def can_speed_abilities(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, homing: bool = False, tornado: bool = False, rocket: bool = False,lightdash: bool = False, triangle: bool = False, lightattack: bool = False, orcondition: bool = False):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    if not homing and not tornado and not rocket and not lightdash and not triangle and not lightattack:
        return False
    result = not orcondition
    if homing:
        if orcondition:
            result = result or can_homing_attack(world, team, level, state)
        else:
            result = result and can_homing_attack(world, team, level, state)
    if tornado:
        if orcondition:
            result = result or can_tornado(world, team, level, state)
        else:
            result = result and can_tornado(world, team, level, state)
    if rocket:
        if orcondition:
            result = result or can_rocket_accel(world, team, level, state)
        else:
            result = result and can_rocket_accel(world, team, level, state)
    if lightdash:
        if orcondition:
            result = result or can_light_dash(world, team, level, state)
        else:
            result = result and can_light_dash(world, team, level, state)
    if triangle:
        if orcondition:
            result = result or can_triangle_jump(world, team, level, state)
        else:
            result = result and can_triangle_jump(world, team, level, state)
    if lightattack:
        if orcondition:
            result = result or can_light_attack(world, team, level, state)
        else:
            result = result and can_light_attack(world, team, level, state)
    return result

def can_thundershoot_ground(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    #name, amount = get_item_req_for_ability(world, get_char_name_from_team(team, flying=True), get_region_name_from_level(world, level), THUNDERSHOOT)
    #return has_char(world, team, level, state, flying=True) and has_char(world, team, level, state, speed=True, power=True, orcondition=True) and state.has(name, world.player, amount)

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), THUNDERSHOOT)
    return has_char(world, team, level, state, flying=True) and has_char(world, team, level, state, speed=True, power=True, orcondition=True) and state.has(name, world.player)

def can_thundershoot_air(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), THUNDERSHOOT)
    return has_char(world, team, level, state, flying=True) and has_char(world, team, level, state, speed=True,power=True, orcondition=True) and state.has(name, world.player)

def can_thundershoot_both(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    return can_thundershoot_ground(world, team, level, state) and can_thundershoot_air(world, team, level, state)


def can_fly(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, speedreq: bool = False, powerreq: bool = False, orcondition: bool = False):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), FLIGHT)
    name2 = get_ability_item_name(world, team, get_region_name_from_level(world, level), THUNDERSHOOT)
    result = True
    if speedreq or powerreq:
        result = result and has_char(world, team, level, state, speed=speedreq, power=powerreq, orcondition=orcondition)
    return has_char(world, team, level, state, flying=True) and state.has(name, world.player) and result and state.has(name2, world.player)

def can_flower_sting(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), FLOWERSTING)
    return has_char(world, team, level, state, flying=True) and state.has(name, world.player) and team == CHAOTIX


def can_fake_ring_toss(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), DUMMYRINGS)
    return (team == SONIC or team == DARK or team == SUPERHARDMODE) and (has_char(world, team, level, state, flying=True) and not has_char(world, team, level, state, speed=True, power=True, orcondition=True)) and state.has(name, world.player)


"""
def can_cheese_cannon(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True
    
    return team == ROSE and (has_char(world, team, level, state, flying=True) and not has_char(world, team, level, state, speed=True, power=True, orcondition=True))

def can_flower_sting_attack(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True
    
    return can_flower_sting(world, team, level, state) and not has_char(world, team, level, state, speed=True, power=True, orcondition=True)
"""

def can_flying_abilities(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, thundershootair: bool = False, thundershootground: bool = False, thundershootboth: bool = False, flyany: bool = False, flyonechar: bool = False, flyspeed: bool = False, flypower: bool = False, flyfull: bool = False, flowersting: bool = False, orcondition: bool = False):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    if not thundershootair and not thundershootground and not thundershootboth and not flyany and not flyonechar and not flyspeed and not flypower and not flyfull and not flowersting:
        return False
    result = not orcondition
    if thundershootair:
        if orcondition:
            result = result or can_thundershoot_air(world, team, level, state)
        else:
            result = result and can_thundershoot_air(world, team, level, state)
    if thundershootground:
        if orcondition:
            result = result or can_thundershoot_ground(world, team, level, state)
        else:
            result = result and can_thundershoot_ground(world, team, level, state)
    if thundershootboth:
        if orcondition:
            result = result or can_thundershoot_both(world, team, level, state)
        else:
            result = result and can_thundershoot_both(world, team, level, state)
    if flyany:
        if orcondition:
            result = result or can_fly(world, team, level, state)
        else:
            result = result and can_fly(world, team, level, state)
    if flyonechar:
        if orcondition:
            result = result or can_fly(world, team, level, state, speedreq=True, powerreq=True, orcondition=True)
        else:
            result = result and can_fly(world, team, level, state, speedreq=True, powerreq=True, orcondition=True)
    if flyspeed:
        if orcondition:
            result = result or can_fly(world, team, level, state, speedreq=True)
        else:
            result = result and can_fly(world, team, level, state, speedreq=True)
    if flypower:
        if orcondition:
            result = result or can_fly(world, team, level, state, powerreq=True)
        else:
            result = result and can_fly(world, team, level, state, powerreq=True)
    if flyfull:
        if orcondition:
            result = result or can_fly(world, team, level, state, speedreq=True, powerreq=True)
        else:
            result = result and can_fly(world, team, level, state, speedreq=True, powerreq=True)
    if flowersting:
        if orcondition:
            result = result or can_flower_sting(world, team, level, state)
        else:
            result = result and can_flower_sting(world, team, level, state)
    return result

def can_break_things(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), POWERATTACK)
    return has_char(world, team, level, state, power=True)# and state.has(name, world.player)

def can_break_key_cage(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True
    return True

def can_break_in_ground_wood_container(world, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True
    return not can_wood_container(world, team, level, state) or (can_fire_dunk(world, team, level, state) or can_combo_finsh(world, team, level, state))

def can_break_in_ground_iron_container(world, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True
    return not can_iron_container(world, team, level, state) or (can_fire_dunk(world, team, level, state) or can_combo_finsh(world, team, level, state))

def can_break_in_ground_unbreakable_container(world, team: str, level: str, state: CollectionState):
    return False

def can_fire_dunk(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), FIREDUNK)
    return has_char(world, team, level, state, power=True) and has_char(world, team, level, state, speed=True, flying=True, orcondition=True) and state.has(name, world.player)

def can_glide(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), GLIDE)
    return has_char(world, team, level, state, power=True) and state.has(name, world.player)


def can_combo_finsh(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, lvl: int = 1):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    name = get_ability_item_name(world, team, get_region_name_from_level(world, level), COMBOFINISHER)
    return has_char(world, team, level, state, power=True) and state.has(name, world.player) and has_char_levelup(world, team, level, state, lvl, power=True)

def can_power_abilities(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, breaknotcage=False, breakcage=False, firedunk=False, glide=False, combofinsh=False, orcondition=False):
    if world.options.unlock_type != UnlockType.option_ability_character_unlocks:
        return True

    if not breaknotcage and not breakcage and not firedunk and not glide and not combofinsh:
        return False
    result = not orcondition
    if breaknotcage:
        if orcondition:
            result = result or can_break_things(world, team, level, state)
        else:
            result = result and can_break_things(world, team, level, state)
    if breakcage:
        if orcondition:
            result = result or can_break_key_cage(world, team, level, state)
        else:
            result = result and can_break_key_cage(world, team, level, state)
    if firedunk:
        if orcondition:
            result = result or can_fire_dunk(world, team, level, state)
        else:
            result = result and can_fire_dunk(world, team, level, state)
    if glide:
        if orcondition:
            result = result or can_glide(world, team, level, state)
        else:
            result = result and can_glide(world, team, level, state)
    if combofinsh:
        if orcondition:
            result = result or can_combo_finsh(world, team, level, state)
        else:
            result = result and can_combo_finsh(world, team, level, state)
    return result


def can_remove_ground_enemy_shield(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return (can_homing_attack(world, team, level, state) and has_char_levelup(world, team, level, state, 3, speed=True)) or ((can_tornado(world, team, level, state) or can_rocket_accel(world, team, level, state)) and has_char_levelup(world, team, level, state, 1, speed=True)) or can_team_blast(world, team, level, state)

def can_kill_ground_enemy_nothing(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_kill_ground_enemy_spear(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return (can_homing_attack(world, team, level, state) and has_char_levelup(world, team, level, state, 1, speed=True)) or can_break_things(world, team, level, state) or (can_thundershoot_both(world, team, level, state) and has_char_levelup(world, team, level, state, 1, flying=True)) or can_team_blast(world, team, level, state)

def can_kill_ground_enemy_plain_shield(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return (can_kill_ground_enemy_nothing(world, team, level, state) and can_remove_ground_enemy_shield(world, team, level, state)) or (can_break_things(world, team, level, state) and has_char_levelup(world, team, level, state, 1, power=True)) or can_team_blast(world, team, level, state)

def can_kill_ground_enemy_concrete_shield(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return (can_kill_ground_enemy_nothing(world, team, level, state) and can_remove_ground_enemy_shield(world, team, level, state)) or (can_combo_finsh(world, team, level, state) and has_char_levelup(world, team, level, state, 2, power=True)) or can_team_blast(world, team, level, state)

def can_kill_ground_enemy_spike_shield(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return can_kill_ground_enemy_concrete_shield(world, team, level, state)

def can_kill_ground_enemy_klagen(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return can_kill_ground_enemy_nothing(world, team, level, state)

def can_kill_ground_enemy_cameron(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return can_remove_ground_enemy_shield(world, team, level, state) or can_break_things(world, team, level, state) or can_team_blast(world, team, level, state)

def can_kill_ground_enemy_goldcameron(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return can_remove_ground_enemy_shield(world, team, level, state) or can_team_blast(world, team, level, state)

def can_kill_ground_enemy_rhinoliner(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return (can_thundershoot_both(world, team, level, state) and has_char_levelup(world, team, level, state, 2, flying=True)) or can_team_blast(world, team, level, state)

def can_kill_ground_enemy_eggbishop(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return (can_homing_attack(world, team, level, state) and has_char_levelup(world, team, level, state, 2, speed=True)) or (can_fire_dunk(world, team, level, state) and has_char_levelup(world, team, level, state, 2, power=True)) or (can_thundershoot_both(world, team, level, state) and has_char_levelup(world, team, level, state, 3, flying=True)) or can_team_blast(world, team, level, state)

def can_kill_ground_enemy_e2000(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return can_combo_finsh(world, team, level, state, 3) or (can_thundershoot_both(world, team, level, state) and has_char_levelup(world, team, level, state, 3, flying=True)) or can_team_blast(world, team, level, state)


def can_kill_ground_enemy_e2000r(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return (can_kill_ground_enemy_e2000(world, team, level, state)
            and (can_remove_ground_enemy_shield(world, team, level, state) or can_team_blast(world, team, level, state)))

def can_kill_ground_enemy_egghammer(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return (can_combo_finsh(world, team, level, state) and has_char_levelup(world, team, level, state, 3, power=True)) or can_team_blast(world, team, level, state)

def can_kill_ground_enemy_heavyegghammer(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return ((can_homing_attack(world, team, level, state) and has_char_levelup(world, team, level, state, 3, speed=True)) or (can_thundershoot_both(world, team, level, state) and has_char_levelup(world, team, level, state, 3, flying=True))) and can_fire_dunk(world, team, level, state) and (can_combo_finsh(world, team, level, state) and has_char_levelup(world, team, level, state, 3, power=True) and can_team_blast(world, team, level, state))

def can_kill_ground_enemy_cannon(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True #and can_cannon_obj(world, team, level, state)


def can_kill_ground_enemy(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, nothing: bool = False, spear: bool = False, plainshield: bool = False, concreteshield: bool = False, spikeshield: bool = False, klagen: bool = False, cameron: bool = False, goldcameron: bool = False, rhinoliner: bool = False, eggbishop: bool = False, e2000: bool = False, e2000r: bool = False, egghammer: bool = False, heavyegghammer: bool = False, cannon: bool = False, orcondition: bool = False):
    if not nothing and not spear and not plainshield and not spikeshield and not klagen and not cameron and not goldcameron and not rhinoliner and not eggbishop and not e2000 and not e2000r and not egghammer and not heavyegghammer and not cannon:
        return can_kill_ground_enemy_nothing(world, team, level, state)
    result = not orcondition
    if nothing:
        if orcondition:
            result = result or can_kill_ground_enemy_nothing(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_nothing(world, team, level, state)
    if spear:
        if orcondition:
            result = result or can_kill_ground_enemy_spear(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_spear(world, team, level, state)
    if plainshield:
        if orcondition:
            result = result or can_kill_ground_enemy_plain_shield(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_plain_shield(world, team, level, state)
    if concreteshield:
        if orcondition:
            result = result or can_kill_ground_enemy_concrete_shield(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_concrete_shield(world, team, level, state)
    if spikeshield:
        if orcondition:
            result = result or can_kill_ground_enemy_spike_shield(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_spike_shield(world, team, level, state)
    if klagen:
        if orcondition:
            result = result or can_kill_ground_enemy_klagen(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_klagen(world, team, level, state)
    if cameron:
        if orcondition:
            result = result or can_kill_ground_enemy_cameron(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_cameron(world, team, level, state)
    if goldcameron:
        if orcondition:
            result = result or can_kill_ground_enemy_goldcameron(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_goldcameron(world, team, level, state)
    if rhinoliner:
        if orcondition:
            result = result or can_kill_ground_enemy_rhinoliner(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_rhinoliner(world, team, level, state)
    if eggbishop:
        if orcondition:
            result = result or can_kill_ground_enemy_eggbishop(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_eggbishop(world, team, level, state)
    if e2000:
        if orcondition:
            result = result or can_kill_ground_enemy_e2000(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_e2000(world, team, level, state)
    if e2000r:
        if orcondition:
            result = result or can_kill_ground_enemy_e2000r(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_e2000r(world, team, level, state)
    if egghammer:
        if orcondition:
            result = result or can_kill_ground_enemy_egghammer(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_egghammer(world, team, level, state)
    if heavyegghammer:
        if orcondition:
            result = result or can_kill_ground_enemy_heavyegghammer(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_heavyegghammer(world, team, level, state)
    if cannon:
        if orcondition:
            result = result or can_kill_ground_enemy_cannon(world, team, level, state)
        else:
            result = result and can_kill_ground_enemy_cannon(world, team, level, state)
    return result


def can_kill_flying_enemy_red_flapper(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, nothing: bool = False, homing: bool = False, firedunk: bool = False):
    if nothing:
        return True
    return can_kill_flying_enemy_green_lightning(world, team, level, state, homing, firedunk)

def can_kill_flying_enemy_green_shot(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, nothing: bool = False, homing: bool = False, firedunk: bool = False):
    if nothing:
        return True
    return can_kill_flying_enemy_green_lightning(world, team, level, state, homing, firedunk)

def can_kill_flying_enemy_green_lightning(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, homing: bool = False, firedunk: bool = False):
    condition = False
    if homing:
        condition = condition or (can_homing_attack(world, team, level, state) and has_char_levelup(world, team, level, state, 1, speed=True))
    if firedunk:
        condition = condition or can_fire_dunk(world, team, level, state)
    return (can_thundershoot_both(world, team, level, state) and has_char_levelup(world, team, level, state, 1, flying=True)) or condition or can_team_blast(world, team, level, state)
    # homing 1 or thundershoot 1 or SFA

def can_kill_flying_enemy_yellow_light(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, homing: bool = False, firedunk: bool = False):
    return can_kill_flying_enemy_green_lightning(world, team, level, state, homing, firedunk)

def can_kill_flying_enemy_blue_mgun(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, homing: bool = False, firedunk: bool = False):
    condition = False
    if homing:
        condition = condition or (can_homing_attack(world, team, level, state) and has_char_levelup(world, team, level, state, 2, speed=True))
    if firedunk:
        condition = condition or can_fire_dunk(world, team, level, state)
    return (can_thundershoot_both(world, team, level, state) and has_char_levelup(world, team, level, state, 2, flying=True)) or condition or can_team_blast(world, team, level, state)
    # homing 2 or thundershoot 2 or SFA

def can_kill_flying_enemy_black_spikey(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, homing: bool = False, firedunk: bool = False):
    return can_kill_flying_enemy_blue_mgun(world, team, level, state, homing, firedunk)

def can_kill_flying_enemy_purple_bombs(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, homing: bool = False, firedunk: bool = False):
    return can_kill_flying_enemy_blue_mgun(world, team, level, state, homing, firedunk)

def can_kill_flying_enemy_silver_armor(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, firedunk=False):
    condition = False
    if firedunk:
        condition = condition or can_fire_dunk(world, team, level, state)
    return ((can_thundershoot_both(world, team, level, state) and has_char_levelup(world, team, level, state, 2, flying=True)) and can_break_things(world, team, level, state)) or condition or can_team_blast(world, team, level, state)
    #thundershoot 2 and break or SFA

def can_kill_flying_enemy_falco(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return (can_thundershoot_both(world, team, level, state) and has_char_levelup(world, team, level, state, 3, flying=True)) or can_team_blast(world, team, level, state)
    #thundershoot 3 or SFA


def can_kill_flying_enemy(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, red_flapper=False, green_shot=False, green_lightning=False, yellow_light=False, blue_mgun=False, black_spikey=False, silver_armor=False, purple_bombs=False, falco=False, nothing=False, homing=False, firedunk=False, orcondition=False):
    if not red_flapper and not green_shot and not green_lightning and not yellow_light and not blue_mgun and not black_spikey and not silver_armor and not purple_bombs and not falco:
        return False
    result = not orcondition
    if red_flapper:
        if orcondition:
            result = result or can_kill_flying_enemy_red_flapper(world, team, level, state, nothing=nothing, homing=homing, firedunk=firedunk)
        else:
            result = result and can_kill_flying_enemy_red_flapper(world, team, level, state, nothing=nothing, homing=homing, firedunk=firedunk)
    if green_shot:
        if orcondition:
            result = result or can_kill_flying_enemy_green_shot(world, team, level, state, nothing=nothing, homing=homing, firedunk=firedunk)
        else:
            result = result and can_kill_flying_enemy_green_shot(world, team, level, state, nothing=nothing, homing=homing, firedunk=firedunk)
    if green_lightning:
        if orcondition:
            result = result or can_kill_flying_enemy_green_lightning(world, team, level, state, homing=homing, firedunk=firedunk)
        else:
            result = result and can_kill_flying_enemy_green_lightning(world, team, level, state, homing=homing, firedunk=firedunk)
    if yellow_light:
        if orcondition:
            result = result or can_kill_flying_enemy_yellow_light(world, team, level, state, homing=homing, firedunk=firedunk)
        else:
            result = result and can_kill_flying_enemy_yellow_light(world, team, level, state, homing=homing, firedunk=firedunk)
    if blue_mgun:
        if orcondition:
            result = result or can_kill_flying_enemy_blue_mgun(world, team, level, state, homing=homing, firedunk=firedunk)
        else:
            result = result and can_kill_flying_enemy_blue_mgun(world, team, level, state, homing=homing, firedunk=firedunk)
    if black_spikey:
        if orcondition:
            result = result or can_kill_flying_enemy_black_spikey(world, team, level, state, homing=homing, firedunk=firedunk)
        else:
            result = result and can_kill_flying_enemy_black_spikey(world, team, level, state, homing=homing, firedunk=firedunk)
    if silver_armor:
        if orcondition:
            result = result or can_kill_flying_enemy_silver_armor(world, team, level, state, firedunk=firedunk)
        else:
            result = result and can_kill_flying_enemy_silver_armor(world, team, level, state, firedunk=firedunk)
    if purple_bombs:
        if orcondition:
            result = result or can_kill_flying_enemy_purple_bombs(world, team, level, state, homing=homing, firedunk=firedunk)
        else:
            result = result and can_kill_flying_enemy_purple_bombs(world, team, level, state, homing=homing, firedunk=firedunk)
    if falco:
        if orcondition:
            result = result or can_kill_flying_enemy_falco(world, team, level, state)
        else:
            result = result and can_kill_flying_enemy_falco(world, team, level, state)
    return result


#Objs Here
#in case I remove tp triggers here
def can_tp_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True


def can_spring(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, single = False, triple = False, orcondition = False):
    if not single and not triple:
        return False

    result = not orcondition
    if single:
        if orcondition:
            result = result or can_single_spring(world, team, level, state)
        else:
            result = result and can_single_spring(world, team, level, state)
    if triple:
        if orcondition:
            result = result or can_triple_spring(world, team, level, state)
        else:
            result = result and can_triple_spring(world, team, level, state)
    return result



def can_single_spring(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True


def can_triple_spring(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True


def can_ring_group(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_hint_ring(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_switch(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, regular = False, push_pull = False, target = False, orcondition = False):
    if not regular and not push_pull and not target:
        return False

    result = not orcondition
    if regular:
        if orcondition:
            result = result or can_regular_switch(world, team, level, state)
        else:
            result = result and can_regular_switch(world, team, level, state)

    if push_pull:
        if orcondition:
            result = result or can_push_pull_switch(world, team, level, state)
        else:
            result = result and can_push_pull_switch(world, team, level, state)

    if target:
        if orcondition:
            result = result or can_target_switch(world, team, level, state)
        else:
            result = result and can_target_switch(world, team, level, state)

    return result

def can_regular_switch(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_push_pull_switch(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_target_switch(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_dash_panel(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True


def can_dash_ring(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True


def can_rainbow_hoops(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_checkpoint_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_dash_ramp(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_cannon_obj(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_cannon(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, speed: bool = False, flying: bool = False, power: bool = False, orcondition=False):
    if not speed and not flying and not power:
        return False

    result = not orcondition
    if speed:
        if orcondition:
            result = result or can_cannon_speed(world, team, level, state)
        else:
            result = result and can_cannon_speed(world, team, level, state)

    if flying:
        if orcondition:
            result = result or can_cannon_flying(world, team, level, state)
        else:
            result = result and can_cannon_flying(world, team, level, state)

    if power:
        if orcondition:
            result = result or can_cannon_power(world, team, level, state)
        else:
            result = result and can_cannon_power(world, team, level, state)

    return result


def can_cannon_speed(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return can_cannon_obj(world, team, level, state) and has_char(world, team, level, state, speed=True)


def can_cannon_flying(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return can_cannon_obj(world, team, level, state) and has_char(world, team, level, state, flying=True)


def can_cannon_power(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return can_cannon_obj(world, team, level, state) and has_char(world, team, level, state, power=True)

def can_weight(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, regular = False, breakable = False, orcondition = False):
    if not regular and not breakable:
        return False
    result = not orcondition
    if regular:
        if orcondition:
            result = result or can_regular_weight(world, team, level, state)
        else:
            result = result and can_regular_weight(world, team, level, state)

    if breakable:
        if orcondition:
            result = result or can_breakable_weight(world, team, level, state)
        else:
            result = result and can_breakable_weight(world, team, level, state)
    return True

def can_regular_weight(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_breakable_weight(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_item_box(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_item_balloon(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_goal_ring(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_pulley(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_wood_container(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_iron_container(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_unbreakable_container(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_chao(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_propeller(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True and (can_tornado(world, team, level, state) or can_rocket_accel(world, team, level, state)) or (can_homing_attack(world, team, level, state) and has_char_levelup(world, team, level, state, 3, speed=True))

def can_pole(world: SonicHeroesWorld, team: str, level: str, state: CollectionState, air: bool = False):
    return True and (can_tornado(world, team, level, state) or (can_rocket_accel(world, team, level, state) and not air)) or (can_homing_attack(world, team, level, state) and has_char_levelup(world, team, level, state, 3, speed=True))

def can_gong(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_fan(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True and can_glide(world, team, level, state)

def can_warp_flower(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True and can_flower_sting(world, team, level, state)

def can_bonus_key(world, team: str, level: str, state: CollectionState):
    return True

def can_trigger_teleport(world, team: str, level: str, state: CollectionState):
    return True

def can_cement_sliding_block(world, team: str, level: str, state: CollectionState):
    return True

def can_cement_block(world, team: str, level: str, state: CollectionState):
    return True

def can_ruins(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_hermit_crab(world, team: str, level: str, state: CollectionState):
    return True

def can_small_stone_platform(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_crumbling_stone_pillar(world, team: str, level: str, state: CollectionState):
    return True

def can_falling_stone_structure(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    #this obj can not be disabled without editing collision mask (will always be true)
    return True

def can_accel_road(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def energy_road_section(world, team: str, level: str, state: CollectionState):
    return True

def can_falling_drawbridge(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_tilting_bridge(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_blimp_platform(world, team: str, level: str, state: CollectionState):
    return True

def can_energy_road_speed_effect(world, team: str, level: str, state: CollectionState):
    return True

def can_energy_road_upward_section(world, team: str, level: str, state: CollectionState):
    return True

def can_energy_column(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_elevator(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_lava_platform(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_liquid_lava(world, team: str, level: str, state: CollectionState):
    return True

def can_energy_road_upward_effect(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_shutter(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_pinball(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_small_bumper(world, team: str, level: str, state: CollectionState):
    return True

def can_green_floating_bumper(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_pinball_flipper(world, team: str, level: str, state: CollectionState):
    return True

def can_small_triangle_bumper(world, team: str, level: str, state: CollectionState):
    return True

def can_star_glass_panel(world, team: str, level: str, state: CollectionState):
    return True

def can_star_glass_air_panel(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_large_triangle_bumper(world, team: str, level: str, state: CollectionState):
    return True

def can_breakable_glass_floor(world, team: str, level: str, state: CollectionState):
    return True

def can_break_glass_floor(world, team: str, level: str, state: CollectionState):
    return not can_breakable_glass_floor(world, team, level, state) or (can_fire_dunk(world, team, level, state) or can_combo_finsh(world, team, level, state))

def can_floating_dice(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_triple_slots(world, team: str, level: str, state: CollectionState):
    return True

def can_single_slots(world, team: str, level: str, state: CollectionState):
    return True

def can_bingo_chart(world, team: str, level: str, state: CollectionState):
    return True

def can_bingo_chip(world, team: str, level: str, state: CollectionState):
    return True

def can_dash_arrow(world, team: str, level: str, state: CollectionState):
    return True

def can_potato_chip(world, team: str, level: str, state: CollectionState):
    return True

def can_rail(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_switchable_rail(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_rail_switch(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_switchable_arrow(world, team: str, level: str, state: CollectionState):
    return True

def can_rail_booster(world, team: str, level: str, state: CollectionState):
    return True

def can_rail_crossing_roadblock(world, team: str, level: str, state: CollectionState):
    return True

def can_capsule(world, team: str, level: str, state: CollectionState):
    return True

def can_rail_platform(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_train_train(world, team: str, level: str, state: CollectionState):
    return True

def can_rc_door(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    """
    This is the Door in Rail Canyon (prob not needed imo)
    """
    return True

def can_engine_core(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_big_gun_interior(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True


def can_barrel(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    """
    This refers to the barrel deco obj in rail canyon / bullet station
    """
    return True

def can_canyon_bridge(world, team: str, level: str, state: CollectionState):
    return True

def can_train_top(world, team: str, level: str, state: CollectionState):
    return True

def can_green_frog(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_small_green_rain_platform(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_small_bouncy_mushroom(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_tall_vertical_vine(world, team: str, level: str, state: CollectionState):
    return True

def can_tall_tree_platforms(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_grindable_growing_ivy(world, team: str, level: str, state: CollectionState):
    return True

def can_large_yellow_platform(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_bouncy_fruit(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_large_bouncy_mushroom(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_swinging_vine(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_black_frog(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_bouncy_falling_fruit(world, team: str, level: str, state: CollectionState):
    return True

def can_tp_switch(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_castle_floating_platform(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_flame_torch(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_pumpkin_ghost(world, team: str, level: str, state: CollectionState):
    return True

def can_mansion_floating_platform(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_castle_key(world, team: str, level: str, state: CollectionState):
    return True

def can_rectangle_floating_platform(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_square_floating_platform(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_falling_platform(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True

def can_self_destruct_tp_switch(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True and has_char(world, team, level, state, speed=True)

def can_eggman_cell_key(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True


def can_egg_flapper(world, team: str, level: str, state: CollectionState):
    return True

def can_egg_pawn(world, team: str, level: str, state: CollectionState):
    return True

def can_klagen(world, team: str, level: str, state: CollectionState):
    return True

def can_falco(world, team: str, level: str, state: CollectionState):
    return True

def can_egg_hammer(world, team: str, level: str, state: CollectionState):
    return True

def can_cameron(world, team: str, level: str, state: CollectionState):
    return True

def can_rhino_liner(world, team: str, level: str, state: CollectionState):
    return True

def can_egg_bishop(world, team: str, level: str, state: CollectionState):
    return True

def can_e2000(world, team: str, level: str, state: CollectionState):
    return True

def can_special_stage_orbs(world, team: str, level: str, state: CollectionState):
    return True

def can_appear_chaos_emerald(world, team: str, level: str, state: CollectionState):
    return True

def can_special_stage_spring(world, team: str, level: str, state: CollectionState):
    return True

def can_special_stage_dash_panel(world, team: str, level: str, state: CollectionState):
    return True

def can_special_stage_dash_ring(world, team: str, level: str, state: CollectionState):
    return True

def can_bobsled(world: SonicHeroesWorld, team: str, level: str, state: CollectionState):
    return True
