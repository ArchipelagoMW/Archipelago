"""This module contains the logic implementation for RAC3"""
from collections.abc import Callable
from logging import DEBUG, getLogger
import math
from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule
from worlds.rac3.constants.data.item import infobot_data, non_prog_weapon_data, prog_weapon_data
from worlds.rac3.constants.items import RAC3ITEM
from worlds.rac3.constants.locations.general import RAC3LOCATION
from worlds.rac3.constants.locations.nanotech import RAC3NANOTECH
from worlds.rac3.constants.locations.sewers import RAC3SEWER
from worlds.rac3.constants.locations.skillpoints import RAC3SKILLPOINT
from worlds.rac3.constants.locations.tags import RAC3TAG
from worlds.rac3.constants.locations.tbolts import RAC3TBOLT
from worlds.rac3.constants.locations.trophies import RAC3TROPHY
from worlds.rac3.constants.locations.vendors import RAC3VENDORLOCATION
from worlds.rac3.constants.locations.weapon_levels import RAC3WEAPONLEVEL
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.constants.region import RAC3REGION
from worlds.rac3.constants.shortcuts import RAC3SHORTCUTS
from worlds.rac3.locations import location_groups

if TYPE_CHECKING:
    from worlds.rac3.world import RaC3World

rac3_logger = getLogger(RAC3OPTION.GAME_TITLE_FULL)
rac3_logger.setLevel(DEBUG)
MULTIPLIERS = {0: 1, 1: 2, 2: 4, 3: 8, 4: 16}
NGPLUS_SCALE = {1: 1.0, 2: 10/7, 4: 10/5, 8: 10/4, 16: 10/2}
GOOD_EXP_PLANETS = [RAC3ITEM.KOROS, RAC3ITEM.CRASH_SITE, RAC3ITEM.METROPOLIS]

def all_locations(state: CollectionState, world: "RaC3World", tag: str, skip: str):
    """check if all locations with this tag can be reached"""
    check: bool = True
    for loc in world.get_locations():
        if loc.name in location_groups[tag] and loc.name != skip:
            check &= state.can_reach_location(loc.name, world.player)
    return check

def calc_nanotech_requirement(world: "RaC3World", default_infobot_count: int, ngplus_levels: bool = False) -> int:
    """Calculate the amount of infobots required for a given nanotech level based on the world options"""
    ngplus_enabled = world.options.ngplus_start.value
    if ngplus_enabled and not ngplus_levels:
        return 1

    multiplier_option = world.options.bolt_and_xp_multiplier.value
    multiplier_value = MULTIPLIERS.get(multiplier_option, 1)

    intro_skip_enabled = world.options.shortcuts.value.get(RAC3SHORTCUTS.VELDIN_SKIP, False)
    intro_skip_offset = 1 if intro_skip_enabled and multiplier_value >= 4 else 0

    if ngplus_levels:
        requirement = math.ceil(default_infobot_count / NGPLUS_SCALE[multiplier_value])
    else:
        requirement = (default_infobot_count + multiplier_value - 1) // multiplier_value

    return max(1, requirement + intro_skip_offset)

def can_earn_good_exp(state: CollectionState, world: "RaC3World") -> bool:
    """Determine if the player can earn good experience based on the planets they can access"""
    if state.has_any(GOOD_EXP_PLANETS, world.player):
        return True
    if (state.can_reach_region(RAC3REGION.COMMAND_CENTER, world.player)
        and state.has_all([RAC3ITEM.HYPERSHOT, RAC3ITEM.GRAV_BOOTS, RAC3ITEM.TYHRRA_GUISE], world.player)
        and state.has_any([RAC3ITEM.HELI_PACK, RAC3ITEM.THRUSTER_PACK, RAC3ITEM.CLANK, RAC3ITEM.PROGRESSIVE_PACK],
                              world.player)):
        return True
    if (state.can_reach_region(RAC3REGION.QWARKS_HIDEOUT, world.player)
        and state.has_all([RAC3ITEM.WARP_PAD, RAC3ITEM.HYPERSHOT], world.player)
        and state.has_any([RAC3ITEM.HELI_PACK, RAC3ITEM.CLANK, RAC3ITEM.PROGRESSIVE_PACK, RAC3ITEM.CHARGE_BOOTS],
                              world.player)):
        return True
    if world.options.ngplus_start.value:
        return True
    return False

# Todo: Rule Builder
def set_rules(world: "RaC3World"):
    """Apply logic rules to each location"""
    progressive_requirement = 1
    ngplus_enabled = world.options.ngplus_start.value
    if ngplus_enabled:
        progressive_requirement += 5 if world.options.ngplus_items.value else 4

    region_rules_dict: dict[str, Callable] = {

        # Intro Florana
        f"{RAC3REGION.VELDIN} -> {RAC3REGION.FLORANA}":
            lambda state: state.has(RAC3ITEM.FLORANA, world.player),

        # Intro Phoenix
        f"{RAC3REGION.FLORANA} -> {RAC3REGION.STARSHIP_PHOENIX}":
            lambda state: state.has(RAC3ITEM.STARSHIP_PHOENIX, world.player),

        # Intro Skip Florana
        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.FLORANA}":
            lambda state: state.has(RAC3ITEM.FLORANA, world.player),

        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.MARCADIA}":
            lambda state: state.has(RAC3ITEM.MARCADIA, world.player),

        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.ANNIHILATION_NATION}":
            lambda state: state.has(RAC3ITEM.ANNIHILATION_NATION, world.player),

        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.AQUATOS}":
            lambda state: state.has(RAC3ITEM.AQUATOS, world.player),

        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.TYHRRANOSIS}":
            lambda state: state.has(RAC3ITEM.TYHRRANOSIS, world.player),

        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.DAXX}":
            lambda state: state.has(RAC3ITEM.DAXX, world.player),

        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.OBANI_GEMINI}":
            lambda state: state.has(RAC3ITEM.OBANI_GEMINI, world.player),

        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.BLACKWATER_CITY}":
            lambda state: state.has(RAC3ITEM.BLACKWATER_CITY, world.player),

        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.HOLOSTAR_STUDIOS}":
            lambda state: state.has(RAC3ITEM.HOLOSTAR_STUDIOS, world.player),

        f"{RAC3REGION.BLACKWATER_CITY} -> {RAC3REGION.SKIDD_CUTSCENE}":
            lambda state: state.has_all([RAC3ITEM.HOLOSTAR_STUDIOS, RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT], world.player),

        f"{RAC3REGION.HOLOSTAR_STUDIOS} -> {RAC3REGION.SKIDD_CUTSCENE}":
            lambda state: state.has_all([RAC3ITEM.BLACKWATER_CITY, RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT], world.player),

        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.OBANI_DRACO}":
            lambda state: state.has_all([RAC3ITEM.OBANI_DRACO, RAC3ITEM.GRAV_BOOTS], world.player),

        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.ZELDRIN_STARPORT}":
            lambda state: state.has(RAC3ITEM.ZELDRIN_STARPORT, world.player),

        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.METROPOLIS}":
            lambda state: state.has(RAC3ITEM.METROPOLIS, world.player),

        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.CRASH_SITE}":
            lambda state: state.has(RAC3ITEM.CRASH_SITE, world.player),

        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.ARIDIA}":
            lambda state: state.has(RAC3ITEM.ARIDIA, world.player),

        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.QWARKS_HIDEOUT}":
            lambda state: state.has(RAC3ITEM.QWARKS_HIDEOUT, world.player),

        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.KOROS}":
            lambda state: state.has(RAC3ITEM.KOROS, world.player),

        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.COMMAND_CENTER}":
            lambda state: state.has(RAC3ITEM.COMMAND_CENTER, world.player),
    }

    rules_dict: dict[str, Callable] = {
        # RAC3LOCATION.VELDIN_FIRST_RANGER
        # RAC3LOCATION.VELDIN_SECOND_RANGER
        # RAC3LOCATION.VELDIN_SAVE_VELDIN

        # RAC3VENDOR.FLORANA_WHIP
        # RAC3VENDOR.FLORANA_N60
        # RAC3TBOLT.FLORANA_BELOW_VENDOR
        RAC3TROPHY.FLORANA_RATCHET:
            lambda state: state.has_any([RAC3ITEM.HELI_PACK, RAC3ITEM.CLANK,
                                         RAC3ITEM.PROGRESSIVE_PACK, RAC3ITEM.CHARGE_BOOTS], world.player),
        RAC3TBOLT.FLORANA_PATH_OF_DEATH:
            lambda state: state.has_any([RAC3ITEM.HELI_PACK, RAC3ITEM.CLANK, RAC3ITEM.PROGRESSIVE_PACK], world.player)
                          or state.has_all([RAC3ITEM.CHARGE_BOOTS, RAC3ITEM.THRUSTER_PACK], world.player),
        RAC3SKILLPOINT.FLORANA_PATH:
            lambda state: state.has_any([RAC3ITEM.HELI_PACK, RAC3ITEM.CLANK,
                                         RAC3ITEM.PROGRESSIVE_PACK, RAC3ITEM.CHARGE_BOOTS], world.player),
        RAC3LOCATION.FLORANA_DEFEAT_QWARK:
            lambda state: state.has_any([RAC3ITEM.HELI_PACK, RAC3ITEM.CLANK,
                                         RAC3ITEM.PROGRESSIVE_PACK, RAC3ITEM.CHARGE_BOOTS], world.player),

        # RAC3VENDOR.PHOENIX_SUCK
        # RAC3VENDOR.PHOENIX_INFECTOR
        # RAC3VENDORLOCATION.PHOENIX_MAGNA_ARMOR
        RAC3VENDORLOCATION.PHOENIX_ADAMANTINE: lambda state: state.can_reach_region(RAC3REGION.AQUATOS, world.player),
        RAC3VENDORLOCATION.PHOENIX_AEGIS_ARMOR:
            lambda state: state.can_reach_region(RAC3REGION.ZELDRIN_STARPORT, world.player),
        RAC3VENDORLOCATION.PHOENIX_INFERNOX: lambda state: state.can_reach_region(RAC3REGION.KOROS, world.player),
        RAC3VENDORLOCATION.PHOENIX_WINGS_1: lambda state: state.has_from_list(infobot_data.keys(), world.player, 1),
        RAC3VENDORLOCATION.PHOENIX_WINGS_2: lambda state: state.has_from_list(infobot_data.keys(), world.player, 1),
        RAC3VENDORLOCATION.PHOENIX_WINGS_3: lambda state: state.has_from_list(infobot_data.keys(), world.player, 2),
        RAC3VENDORLOCATION.PHOENIX_NOSE_1: lambda state: state.has_from_list(infobot_data.keys(), world.player, 2),
        RAC3VENDORLOCATION.PHOENIX_NOSE_2: lambda state: state.has_from_list(infobot_data.keys(), world.player, 3),
        RAC3VENDORLOCATION.PHOENIX_NOSE_3: lambda state: state.has_from_list(infobot_data.keys(), world.player, 3),
        RAC3VENDORLOCATION.PHOENIX_SKIN_1: lambda state: state.has_from_list(infobot_data.keys(), world.player, 4),
        RAC3VENDORLOCATION.PHOENIX_SKIN_2: lambda state: state.has_from_list(infobot_data.keys(), world.player, 4),
        RAC3VENDORLOCATION.PHOENIX_SKIN_3: lambda state: state.has_from_list(infobot_data.keys(), world.player, 5),
        RAC3VENDORLOCATION.PHOENIX_SKIN_4: lambda state: state.has_from_list(infobot_data.keys(), world.player, 5),
        RAC3VENDORLOCATION.PHOENIX_SKIN_5: lambda state: state.has_from_list(infobot_data.keys(), world.player, 6),
        RAC3VENDORLOCATION.PHOENIX_SKIN_6: lambda state: state.has_from_list(infobot_data.keys(), world.player, 6),
        RAC3VENDORLOCATION.PHOENIX_SKIN_7: lambda state: state.has_from_list(infobot_data.keys(), world.player, 7),
        RAC3VENDORLOCATION.PHOENIX_SKIN_8: lambda state: state.has_from_list(infobot_data.keys(), world.player, 7),
        RAC3VENDORLOCATION.PHOENIX_SKIN_9: lambda state: state.has_from_list(infobot_data.keys(), world.player, 8),
        RAC3VENDORLOCATION.PHOENIX_SKIN_10: lambda state: state.has_from_list(infobot_data.keys(), world.player, 8),
        RAC3VENDORLOCATION.PHOENIX_SKIN_11: lambda state: state.has_from_list(infobot_data.keys(), world.player, 9),
        RAC3VENDORLOCATION.PHOENIX_SKIN_12: lambda state: state.has_from_list(infobot_data.keys(), world.player, 9),
        RAC3VENDORLOCATION.PHOENIX_SKIN_13: lambda state: state.has_from_list(infobot_data.keys(), world.player, 10),
        RAC3VENDORLOCATION.PHOENIX_SKIN_14: lambda state: state.has_from_list(infobot_data.keys(), world.player, 10),
        RAC3VENDORLOCATION.PHOENIX_SKIN_15: lambda state: state.has_from_list(infobot_data.keys(), world.player, 11),
        RAC3VENDORLOCATION.PHOENIX_SKIN_16: lambda state: state.has_from_list(infobot_data.keys(), world.player, 11),
        RAC3VENDORLOCATION.PHOENIX_SKIN_17: lambda state: state.has_from_list(infobot_data.keys(), world.player, 12),
        RAC3VENDORLOCATION.PHOENIX_SKIN_18: lambda state: state.has_from_list(infobot_data.keys(), world.player, 12),
        RAC3VENDORLOCATION.PHOENIX_SKIN_19: lambda state: state.has_from_list(infobot_data.keys(), world.player, 13),
        RAC3VENDORLOCATION.PHOENIX_SKIN_20: lambda state: state.has_from_list(infobot_data.keys(), world.player, 13),
        RAC3VENDORLOCATION.PHOENIX_SKIN_21: lambda state: state.has_from_list(infobot_data.keys(), world.player, 14),
        RAC3VENDORLOCATION.PHOENIX_SKIN_22: lambda state: state.has_from_list(infobot_data.keys(), world.player, 14),
        RAC3VENDORLOCATION.PHOENIX_SKIN_23: lambda state: state.has_from_list(infobot_data.keys(), world.player, 15),
        RAC3VENDORLOCATION.PHOENIX_SKIN_24: lambda state: state.has_from_list(infobot_data.keys(), world.player, 15),
        RAC3VENDORLOCATION.PHOENIX_SKIN_25: lambda state: state.has_from_list(infobot_data.keys(), world.player, 16),
        RAC3VENDORLOCATION.PHOENIX_SKIN_26: lambda state: state.has_from_list(infobot_data.keys(), world.player, 16),
        RAC3VENDORLOCATION.PHOENIX_SKIN_27: lambda state: state.has_from_list(infobot_data.keys(), world.player, 17),
        RAC3VENDORLOCATION.PHOENIX_SKIN_28: lambda state: state.has_from_list(infobot_data.keys(), world.player, 17),
        RAC3VENDORLOCATION.PHOENIX_SKIN_29: lambda state: state.has_from_list(infobot_data.keys(), world.player, 18),
        RAC3VENDORLOCATION.PHOENIX_SKIN_30: lambda state: state.has_from_list(infobot_data.keys(), world.player, 18),
        RAC3VENDORLOCATION.PHOENIX_SKIN_31: lambda state: state.has_from_list(infobot_data.keys(), world.player, 19),
        RAC3VENDORLOCATION.PHOENIX_SKIN_32: lambda state: state.has_from_list(infobot_data.keys(), world.player, 19),
        RAC3SKILLPOINT.PHOENIX_ARMOR: lambda state: state.can_reach_region(RAC3REGION.KOROS, world.player),
        # RAC3LOCATION.PHOENIX_MEET_SASHA
        RAC3SKILLPOINT.PHOENIX_MONKEY: lambda state: state.has(RAC3ITEM.TYHRRA_GUISE, world.player),
        RAC3LOCATION.PHOENIX_ASSAULT:
            lambda state: state.can_reach_region(RAC3REGION.QWARKS_HIDEOUT, world.player)
                          and state.has_all([RAC3ITEM.WARP_PAD, RAC3ITEM.HYPERSHOT, RAC3ITEM.REFRACTOR], world.player),
        RAC3LOCATION.PHOENIX_GRAND_PRIZE:
            lambda state: state.can_reach_region(RAC3REGION.ANNIHILATION_NATION, world.player),
        RAC3LOCATION.PHOENIX_STAR_MAP: lambda state: state.has(RAC3ITEM.STAR_MAP, world.player),
        RAC3LOCATION.PHOENIX_MASTER_PLAN: lambda state: state.has(RAC3ITEM.MASTER_PLAN, world.player),
        # RAC3LOCATION.PHOENIX_VR_WARM_UP
        RAC3LOCATION.PHOENIX_VR_D_L_D:
            lambda state: state.can_reach_location(RAC3LOCATION.PHOENIX_VR_WARM_UP, world.player),
        RAC3LOCATION.PHOENIX_VR_SPEED_ROUND:
            lambda state: state.can_reach_location(RAC3LOCATION.PHOENIX_VR_D_L_D, world.player),
        RAC3LOCATION.PHOENIX_VR_HOT_STEPPER:
            lambda state: state.can_reach_location(RAC3LOCATION.PHOENIX_VR_SPEED_ROUND, world.player),
        RAC3LOCATION.PHOENIX_VR_90_SECOND:
            lambda state: state.can_reach_location(RAC3LOCATION.PHOENIX_VR_SPEED_ROUND, world.player),
        RAC3LOCATION.PHOENIX_VR_SHOCKER:
            lambda state: (state.has(RAC3ITEM.SHOCK_BLASTER, world.player)
                           or state.has(RAC3ITEM.PROGRESSIVE_SHOCK_BLASTER, world.player, progressive_requirement))
                          and state.can_reach_location(RAC3LOCATION.PHOENIX_VR_D_L_D, world.player),
        RAC3LOCATION.PHOENIX_VR_WRENCH:
            lambda state: state.can_reach_location(RAC3LOCATION.PHOENIX_VR_SHOCKER, world.player),
        RAC3TBOLT.PHOENIX_VR_NERVES:
            lambda state: state.can_reach_location(RAC3LOCATION.PHOENIX_VR_WRENCH, world.player)
                          and state.can_reach_location(RAC3LOCATION.PHOENIX_VR_90_SECOND, world.player),
        RAC3LOCATION.PHOENIX_VR_NERVES:
            lambda state: state.can_reach_location(RAC3LOCATION.PHOENIX_VR_WRENCH, world.player)
                          and state.can_reach_location(RAC3LOCATION.PHOENIX_VR_90_SECOND, world.player),
        RAC3TBOLT.PHOENIX_VR_TRAINING:
            lambda state: state.can_reach_location(RAC3LOCATION.TYHRRANOSIS_BOSS, world.player)
                          and state.has_all([RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT], world.player),
        RAC3LOCATION.PHOENIX_HACKER:
            lambda state: state.can_reach_location(RAC3LOCATION.TYHRRANOSIS_BOSS, world.player)
                          and state.has_all([RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT], world.player),
        RAC3LOCATION.PHOENIX_HYPERSHOT:
            lambda state: state.can_reach_location(RAC3LOCATION.TYHRRANOSIS_BOSS, world.player)
                          and state.has_all([RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT], world.player),
        RAC3LOCATION.PHOENIX_VR_TRAINING:
            lambda state: state.can_reach_location(RAC3LOCATION.TYHRRANOSIS_BOSS, world.player)
                          and state.has_all([RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT], world.player),
        RAC3SKILLPOINT.PHOENIX_VR_TRAINING:
            lambda state: state.can_reach_location(RAC3LOCATION.TYHRRANOSIS_BOSS, world.player)
                          and state.has_all([RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT], world.player),
        RAC3TBOLT.PHOENIX_VID_COMIC_1: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 1),
        RAC3LOCATION.PHOENIX_VID_COMIC_1_CLEAR: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 1),
        RAC3SKILLPOINT.PHOENIX_COMIC_1: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 1),
        RAC3TBOLT.PHOENIX_VID_COMIC_2: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 2),
        RAC3LOCATION.PHOENIX_VID_COMIC_2_CLEAR: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 2),
        RAC3SKILLPOINT.PHOENIX_COMIC_2: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 2),
        RAC3TBOLT.PHOENIX_VID_COMIC_3: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 3),
        RAC3LOCATION.PHOENIX_VID_COMIC_3_CLEAR: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 3),
        RAC3SKILLPOINT.PHOENIX_COMIC_3: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 3),
        RAC3TBOLT.PHOENIX_VID_COMIC_4: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 4),
        RAC3LOCATION.PHOENIX_VID_COMIC_4_CLEAR: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 4),
        RAC3SKILLPOINT.PHOENIX_COMIC_4: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 4),
        RAC3TBOLT.PHOENIX_VID_COMIC_5: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 5),
        RAC3LOCATION.PHOENIX_VID_COMIC_5_CLEAR: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 5),
        RAC3SKILLPOINT.PHOENIX_COMIC_5: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 5),
        RAC3SKILLPOINT.PHOENIX_ARCADE: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 5),
        RAC3TROPHY.PHOENIX_TITANIUM_COLLECTOR:
            lambda state: all_locations(state, world, RAC3TAG.T_BOLT, RAC3TROPHY.PHOENIX_TITANIUM_COLLECTOR),
        RAC3TROPHY.PHOENIX_FRIEND_OF_THE_RANGERS:
            lambda state: all_locations(state, world, RAC3TAG.RANGERS, RAC3TROPHY.PHOENIX_FRIEND_OF_THE_RANGERS),
        RAC3TROPHY.PHOENIX_ANNIHILATION_NATION_CHAMPION:
            lambda state: all_locations(state, world, RAC3TAG.ARENA, RAC3TROPHY.PHOENIX_ANNIHILATION_NATION_CHAMPION),
        RAC3TROPHY.PHOENIX_SKILL_MASTER:
            lambda state: all_locations(state, world, RAC3TAG.SKILLPOINT, RAC3TROPHY.PHOENIX_SKILL_MASTER),
        RAC3TROPHY.PHOENIX_NANO_FINDER:
            lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 10, True)),
        RAC3TROPHY.PHOENIX_OMEGA_ARSENAL:
            lambda state: state.has_all(non_prog_weapon_data.keys(), world.player) 
                       or state.has_all_counts({weapon : 5 if weapon == RAC3ITEM.PROGRESSIVE_RY3N0 else 8 for weapon in prog_weapon_data.keys()}, world.player),

        # RAC3VENDOR.MARCADIA_HYDRA
        # RAC3TBOLT.MARCADIA_POOL
        # RAC3LOCATION.MARCADIA_RANGERS_1
        RAC3LOCATION.MARCADIA_RANGERS_2:
            lambda state: state.can_reach_location(RAC3LOCATION.MARCADIA_RANGERS_1, world.player),
        RAC3LOCATION.MARCADIA_RANGERS_3:
            lambda state: state.can_reach_location(RAC3LOCATION.MARCADIA_RANGERS_2, world.player),
        RAC3LOCATION.MARCADIA_RANGERS_4:
            lambda state: state.can_reach_location(RAC3LOCATION.MARCADIA_RANGERS_3, world.player),
        RAC3LOCATION.MARCADIA_RANGERS_5:
            lambda state: state.can_reach_location(RAC3LOCATION.MARCADIA_RANGERS_4, world.player),
        RAC3LOCATION.MARCADIA_REFRACTOR:
            lambda state: state.can_reach_location(RAC3LOCATION.MARCADIA_RANGERS_5, world.player),
        RAC3SKILLPOINT.MARCADIA_REFLECT:
            lambda state: state.has(RAC3ITEM.REFRACTOR, world.player)
                          and state.can_reach_location(RAC3LOCATION.MARCADIA_REFRACTOR, world.player),
        RAC3TBOLT.MARCADIA_LAST_REFRACTOR:
            lambda state: state.has_all([RAC3ITEM.REFRACTOR, RAC3ITEM.GRAV_BOOTS], world.player)
                          and state.can_reach_location(RAC3LOCATION.MARCADIA_REFRACTOR, world.player),
        RAC3TBOLT.MARCADIA_BEFORE_AL:
            lambda state: state.has_all([RAC3ITEM.REFRACTOR, RAC3ITEM.GRAV_BOOTS], world.player)
                          and state.can_reach_location(RAC3LOCATION.MARCADIA_REFRACTOR, world.player),
        RAC3LOCATION.MARCADIA_MEET_AL:
            lambda state: state.has(RAC3ITEM.REFRACTOR, world.player)
                          and state.can_reach_location(RAC3LOCATION.MARCADIA_REFRACTOR, world.player),

        # RAC3VENDOR.NATION_AGENTS
        # RAC3TBOLT.NATION_CLIFF
        # RAC3SKILLPOINT.NATION_CAMERA
        # RAC3SKILLPOINT.NATION_FLEE
        # RAC3LOCATION.NATION_TYHRRA_GUISE
        RAC3LOCATION.NATION_GRAND_PRIZE_BOUT:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_HEAT_STREET, world.player),
        RAC3LOCATION.NATION_THE_TERRIBLE_TWO:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_GRAND_PRIZE_BOUT, world.player),
        RAC3LOCATION.NATION_ROBOT_RAMPAGE:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_GRAND_PRIZE_BOUT, world.player),
        RAC3LOCATION.NATION_TWO_MINUTE_WARNING:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_THE_TERRIBLE_TWO, world.player),
        RAC3LOCATION.NATION_90_SECONDS:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_ROBOT_RAMPAGE, world.player),
        RAC3LOCATION.NATION_ONSLAUGHT:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_90_SECONDS, world.player),
        RAC3LOCATION.NATION_CHAMPIONSHIP_BOUT:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_ONSLAUGHT, world.player),
        RAC3LOCATION.NATION_WHIP_IT_GOOD:
            lambda state: (state.has(RAC3ITEM.PLASMA_WHIP, world.player)
                           or state.has(RAC3ITEM.PROGRESSIVE_PLASMA_WHIP, world.player, progressive_requirement))
                          and state.can_reach_location(RAC3LOCATION.NATION_ROBOT_RAMPAGE, world.player),
        RAC3LOCATION.NATION_HYDRA_N_SEEK:
            lambda state: (state.has(RAC3ITEM.SPITTING_HYDRA, world.player)
                           or state.has(RAC3ITEM.PROGRESSIVE_SPITTING_HYDRA, world.player, progressive_requirement))
                          and state.can_reach_location(RAC3LOCATION.NATION_WHIP_IT_GOOD, world.player),

        RAC3SKILLPOINT.NATION_BASH:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_BBQ_BOULEVARD, world.player),
        RAC3LOCATION.NATION_MEET_COURTNEY:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_BBQ_BOULEVARD, world.player),
        RAC3LOCATION.NATION_INFOBOT_HOLOSTAR:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_BBQ_BOULEVARD, world.player),
        RAC3LOCATION.NATION_NINJA_CHALLENGE:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_BBQ_BOULEVARD, world.player),
        RAC3LOCATION.NATION_COUNTING_DUCKS:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_BBQ_BOULEVARD, world.player),
        RAC3LOCATION.NATION_CYCLING_WEAPONS:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_BBQ_BOULEVARD, world.player),
        RAC3LOCATION.NATION_ONE_HIT_WONDER:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_BBQ_BOULEVARD, world.player),
        RAC3LOCATION.NATION_TIME_TO_SUCK:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_BBQ_BOULEVARD, world.player)
                          and (state.has(RAC3ITEM.SUCK_CANNON, world.player)
                               or state.has(RAC3ITEM.PROGRESSIVE_SUCK_CANNON, world.player, progressive_requirement)),
        RAC3LOCATION.NATION_NAPTIME:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_BBQ_BOULEVARD, world.player),
        RAC3LOCATION.NATION_MORE_CYCLING_WEAPONS:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_BBQ_BOULEVARD, world.player),
        RAC3LOCATION.NATION_DODGE_THE_TWINS:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_BBQ_BOULEVARD, world.player),
        RAC3LOCATION.NATION_CHOP_CHOP:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_TIME_TO_SUCK, world.player)
                         and (state.has(RAC3ITEM.DISC_BLADE, world.player)
                             or state.has(RAC3ITEM.PROGRESSIVE_DISC_BLADE, world.player, progressive_requirement)),
        RAC3LOCATION.NATION_SLEEP_INDUCER:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_CHOP_CHOP, world.player)
                         and (state.has(RAC3ITEM.RIFT_INDUCER, world.player)
                             or state.has(RAC3ITEM.PROGRESSIVE_RIFT_INDUCER, world.player, progressive_requirement)),
        RAC3LOCATION.NATION_THE_OTHER_WHITE_MEAT:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_SLEEP_INDUCER, world.player)
                         and (state.has(RAC3ITEM.QWACK_O_RAY, world.player)
                             or state.has(RAC3ITEM.PROGRESSIVE_QWACK_O_RAY, world.player, progressive_requirement)),
        RAC3LOCATION.NATION_CHAMPIONSHIP_BOUT_II:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_BBQ_BOULEVARD, world.player),
        RAC3LOCATION.NATION_QWARKTASTIC_BATTLE: lambda state: state.has(RAC3ITEM.VICTORY, world.player),
        # RAC3LOCATION.NATION_HEAT_STREET
        RAC3LOCATION.NATION_CRISPY_CRITTER:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_HEAT_STREET, world.player),
        RAC3LOCATION.NATION_PYRO_PLAYGROUND:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_CRISPY_CRITTER, world.player),
        RAC3LOCATION.NATION_SUICIDE_RUN:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_PYRO_PLAYGROUND, world.player),
        RAC3LOCATION.NATION_BBQ_BOULEVARD:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, world.player)
                          and state.has_any([RAC3ITEM.HELI_PACK, RAC3ITEM.THRUSTER_PACK, RAC3ITEM.CLANK,
                                             RAC3ITEM.PROGRESSIVE_PACK, RAC3ITEM.CHARGE_BOOTS], world.player),
        RAC3LOCATION.NATION_MAZE_OF_BLAZE:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_BBQ_BOULEVARD, world.player),
        RAC3TBOLT.NATION_PLATFORM:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_MAZE_OF_BLAZE, world.player)
                          and state.has_any([RAC3ITEM.HELI_PACK, RAC3ITEM.THRUSTER_PACK, RAC3ITEM.CLANK,
                                             RAC3ITEM.PROGRESSIVE_PACK], world.player),
        RAC3LOCATION.NATION_CREMATION_STATION:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_MAZE_OF_BLAZE, world.player),
        RAC3LOCATION.NATION_THE_ANNIHILATOR:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_CREMATION_STATION, world.player),
        RAC3SKILLPOINT.NATION_EIGHT:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_THE_ANNIHILATOR, world.player)
                          and state.can_reach_location(RAC3LOCATION.NATION_SUICIDE_RUN, world.player),

        # RAC3VENDOR.AQUATOS_FLUX_RIFLE
        # RAC3TBOLT.AQUATOS_BRIDGE
        # RAC3TBOLT.AQUATOS_UNDERWATER
        # RAC3SKILLPOINT.AQUATOS_SUNKEN
        RAC3TBOLT.AQUATOS_GATE: lambda state: state.has(RAC3ITEM.HACKER, world.player),
        # RAC3VENDOR.AQUATOS_MINI_TURRET
        # RAC3VENDOR.AQUATOS_LAVA_GUN
        RAC3VENDORLOCATION.AQUATOS_SHIELD_CHARGER:
            lambda state: state.can_reach_region(RAC3REGION.COMMAND_CENTER, world.player),
        RAC3VENDORLOCATION.AQUATOS_BOUNCER:
            lambda state: state.can_reach_region(RAC3REGION.QWARKS_HIDEOUT, world.player),
        RAC3VENDORLOCATION.AQUATOS_PLASMA_COIL: lambda state: state.can_reach_region(RAC3REGION.KOROS, world.player),
        # RAC3LOCATION.AQUATOS_BASE
        RAC3TBOLT.SEWER_PIPE: lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),
        RAC3TBOLT.SEWER_SWING: lambda state: state.has_all([RAC3ITEM.HYPERSHOT, RAC3ITEM.GRAV_BOOTS], world.player),
        # RAC3SEWER.TRADE_1: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        # RAC3SEWER.TRADE_2: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        # RAC3SEWER.TRADE_3: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        # RAC3SEWER.TRADE_4: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        # RAC3SEWER.TRADE_5: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        # RAC3SEWER.TRADE_6: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        # RAC3SEWER.TRADE_7: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        # RAC3SEWER.TRADE_8: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        # RAC3SEWER.TRADE_9: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        # RAC3SEWER.TRADE_10: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        # RAC3SEWER.TRADE_11: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        # RAC3SEWER.TRADE_12: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        # RAC3SEWER.TRADE_13: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        # RAC3SEWER.TRADE_14: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        # RAC3SEWER.TRADE_15: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        # RAC3SEWER.TRADE_16: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        # RAC3SEWER.TRADE_17: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        # RAC3SEWER.TRADE_18: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        # RAC3SEWER.TRADE_19: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        # RAC3SEWER.TRADE_20: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_21: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_22: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_23: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_24: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_25: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_26: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_27: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_28: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_29: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_30: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_31: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_32: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_33: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_34: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_35: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_36: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_37: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_38: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_39: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_40: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_41: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_42: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_43: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_44: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_45: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_46: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_47: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_48: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_49: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_50: lambda state: state.has(RAC3ITEM.MAP_O_MATIC, world.player),
        RAC3SEWER.TRADE_51: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_52: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_53: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_54: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_55: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_56: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_57: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_58: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_59: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_60: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_61: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_62: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_63: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_64: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_65: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_66: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_67: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_68: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_69: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_70: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_71: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_72: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_73: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_74: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_75: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_76: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_77: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_78: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_79: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_80: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_81: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_82: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_83: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_84: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_85: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_86: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_87: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_88: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_89: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_90: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_91: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_92: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_93: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_94: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_95: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_96: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_97: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_98: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_99: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_100: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SEWER.TRADE_101: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),
        RAC3SKILLPOINT.SEWER_MOTHERLOAD:
            lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC], world.player),

        # RAC3VENDOR.TYHRRANOSIS_ANNIHILATOR
        RAC3VENDORLOCATION.TYHRRANOSIS_SHIELD_GLOVE:
            lambda state: state.can_reach_location(RAC3LOCATION.TYHRRANOSIS_BOSS, world.player),
        RAC3SKILLPOINT.TYHRRANOSIS_SHARPSHOOTER:
            lambda state: state.has_any([RAC3ITEM.FLUX_RIFLE, RAC3ITEM.PROGRESSIVE_FLUX_RIFLE], world.player),
        # RAC3TBOLT.TYHRRANOSIS_CANNON
        RAC3TROPHY.TYHRRANOSIS_AL:
            lambda state: state.has_any([RAC3ITEM.HELI_PACK, RAC3ITEM.CLANK, RAC3ITEM.PROGRESSIVE_PACK], world.player),
        RAC3TBOLT.TYHRRANOSIS_CAVE: lambda state: state.has(RAC3ITEM.HYPERSHOT, world.player),
        # RAC3LOCATION.TYHRRANOSIS_BOSS
        RAC3LOCATION.TYHRRANOSIS_RANGERS_1:
            lambda state: state.can_reach_location(RAC3LOCATION.TYHRRANOSIS_BOSS, world.player),
        RAC3LOCATION.TYHRRANOSIS_RANGERS_2:
            lambda state: state.can_reach_location(RAC3LOCATION.TYHRRANOSIS_RANGERS_1, world.player),
        RAC3LOCATION.TYHRRANOSIS_RANGERS_3:
            lambda state: state.can_reach_location(RAC3LOCATION.TYHRRANOSIS_RANGERS_2, world.player),
        RAC3LOCATION.TYHRRANOSIS_RANGERS_4:
            lambda state: state.can_reach_location(RAC3LOCATION.TYHRRANOSIS_RANGERS_3, world.player),

        RAC3SKILLPOINT.DAXX_BUGS:
            lambda state: state.has_any([RAC3ITEM.QWACK_O_RAY, RAC3ITEM.PROGRESSIVE_QWACK_O_RAY], world.player),

        # RAC3LOCATION.DAXX_CHARGE_BOOTS
        # RAC3TROPHY.DAXX_PLUMBER
        RAC3LOCATION.DAXX_GUNSHIP: lambda state: state.has(RAC3ITEM.HYPERSHOT, world.player),
        RAC3TBOLT.DAXX_TAXI:
            lambda state: state.has(RAC3ITEM.HYPERSHOT, world.player) and
                          state.has_any([RAC3ITEM.HELI_PACK, RAC3ITEM.CLANK, RAC3ITEM.PROGRESSIVE_PACK], world.player),
        RAC3TBOLT.DAXX_DOOR:
            lambda state: state.has_all([RAC3ITEM.HYPERSHOT, RAC3ITEM.HACKER, RAC3ITEM.CHARGE_BOOTS], world.player),
        RAC3LOCATION.DAXX_FACILITY: lambda state: state.has_all([RAC3ITEM.HYPERSHOT, RAC3ITEM.HACKER], world.player),

        # RAC3VENDOR.OBANI_GEMINI_DISC
        RAC3TBOLT.OBANI_GEMINI_1: lambda state: state.has_all([RAC3ITEM.REFRACTOR, RAC3ITEM.HYPERSHOT], world.player),
        RAC3SKILLPOINT.GEMINI_BELT: lambda state: state.has(RAC3ITEM.REFRACTOR, world.player),
        RAC3TBOLT.OBANI_GEMINI_2: lambda state: state.has(RAC3ITEM.REFRACTOR, world.player),
        RAC3LOCATION.OBANI_GEMINI_SKIDD: lambda state: state.has(RAC3ITEM.REFRACTOR, world.player),

        # RAC3SKILLPOINT.BLACKWATER_BASH
        # RAC3LOCATION.BLACKWATER_CITY_RANGERS_1
        RAC3LOCATION.BLACKWATER_CITY_RANGERS_2:
            lambda state: state.can_reach_location(RAC3LOCATION.BLACKWATER_CITY_RANGERS_1, world.player),
        RAC3LOCATION.BLACKWATER_CITY_RANGERS_3:
            lambda state: state.can_reach_location(RAC3LOCATION.BLACKWATER_CITY_RANGERS_2, world.player),
        RAC3LOCATION.BLACKWATER_CITY_COMPLETE:
            lambda state: state.can_reach_location(RAC3LOCATION.BLACKWATER_CITY_RANGERS_3, world.player),

        # RAC3VENDOR.HOLOSTAR_RIFT_INDUCER
        RAC3LOCATION.HOLOSTAR_RETURN_TO_SHIP: lambda state: state.has_all([RAC3ITEM.HYPERSHOT, RAC3ITEM.HACKER],
                                                                          world.player),
        RAC3TROPHY.HOLOSTAR_CLANK: lambda state: state.has(RAC3ITEM.HACKER, world.player),
        RAC3TBOLT.HOLOSTAR_CHAIRS: lambda state: state.has(RAC3ITEM.HACKER, world.player),
        RAC3SKILLPOINT.HOLOSTAR_LUCKY: lambda state: state.has(RAC3ITEM.HACKER, world.player),
        RAC3TBOLT.HOLOSTAR_GRAV_RAMP:
            lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT], world.player),
        RAC3TBOLT.HOLOSTAR_KAMIKAZE_NOIDS:
            lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT], world.player),

        # RAC3LOCATION.SKIDD_CAPTURED

        RAC3LOCATION.DRACO_COURTNEY: lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),

        # RAC3TBOLT.ZELDRIN_STARPORT_1
        RAC3TBOLT.ZELDRIN_STARPORT_2:
            lambda state: state.has(RAC3ITEM.HYPERSHOT, world.player)
                          and state.has_any([RAC3ITEM.HELI_PACK, RAC3ITEM.THRUSTER_PACK,
                                             RAC3ITEM.CLANK, RAC3ITEM.PROGRESSIVE_PACK], world.player),
        RAC3LOCATION.ZELDRIN_STARPORT_BOLT_GRABBER:
            lambda state: state.has(RAC3ITEM.HYPERSHOT, world.player)
                          and state.has_any([RAC3ITEM.HELI_PACK, RAC3ITEM.THRUSTER_PACK, RAC3ITEM.CLANK,
                                             RAC3ITEM.PROGRESSIVE_PACK, RAC3ITEM.CHARGE_BOOTS], world.player),
        RAC3LOCATION.ZELDRIN_STARPORT_BOX_BREAKER:
            lambda state: state.has(RAC3ITEM.HYPERSHOT, world.player)
                          and state.has_any([RAC3ITEM.HELI_PACK, RAC3ITEM.THRUSTER_PACK, RAC3ITEM.CLANK,
                                             RAC3ITEM.PROGRESSIVE_PACK, RAC3ITEM.CHARGE_BOOTS], world.player),
        RAC3LOCATION.ZELDRIN_STARPORT_SHIP:
            lambda state: state.has_any([RAC3ITEM.HELI_PACK, RAC3ITEM.THRUSTER_PACK, RAC3ITEM.CLANK,
                                         RAC3ITEM.PROGRESSIVE_PACK, RAC3ITEM.CHARGE_BOOTS], world.player),

        RAC3SKILLPOINT.METROPOLIS_GOOD_YEAR:
            lambda state: state.has_any([RAC3ITEM.FLUX_RIFLE, RAC3ITEM.PROGRESSIVE_FLUX_RIFLE,
                                         RAC3ITEM.ANNIHILATOR, RAC3ITEM.PROGRESSIVE_ANNIHILATOR,
                                         RAC3ITEM.RY3N0, RAC3ITEM.PROGRESSIVE_RY3N0,
                                         RAC3ITEM.SUCK_CANNON, RAC3ITEM.PROGRESSIVE_SUCK_CANNON,
                                         RAC3ITEM.DISC_BLADE, RAC3ITEM.PROGRESSIVE_DISC_BLADE], world.player),
        RAC3TBOLT.METROPOLIS_SWING: lambda state: state.has(RAC3ITEM.HYPERSHOT, world.player),
        # RAC3TROPHY.METROPOLIS_SKRUNCH
        # RAC3LOCATION.METROPOLIS_METAL_NOIDS
        # RAC3TBOLT.METROPOLIS_BEHIND
        RAC3LOCATION.METROPOLIS_DEFEAT_KLUNK:
            lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.REFRACTOR], world.player),
        RAC3TBOLT.METROPOLIS_RANGERS:
            lambda state: state.can_reach_location(RAC3LOCATION.METROPOLIS_DEFEAT_KLUNK, world.player),
        RAC3LOCATION.METROPOLIS_RANGERS_1:
            lambda state: state.can_reach_location(RAC3LOCATION.METROPOLIS_DEFEAT_KLUNK, world.player),
        RAC3LOCATION.METROPOLIS_RANGERS_2:
            lambda state: state.can_reach_location(RAC3LOCATION.METROPOLIS_RANGERS_1, world.player),
        RAC3LOCATION.METROPOLIS_RANGERS_3:
            lambda state: state.can_reach_location(RAC3LOCATION.METROPOLIS_RANGERS_2, world.player),
        RAC3LOCATION.METROPOLIS_RANGERS_4:
            lambda state: state.can_reach_location(RAC3LOCATION.METROPOLIS_RANGERS_3, world.player),
        RAC3LOCATION.METROPOLIS_RANGERS_5:
            lambda state: state.can_reach_location(RAC3LOCATION.METROPOLIS_RANGERS_4, world.player),
        RAC3LOCATION.METROPOLIS_MAP_O_MATIC:
            lambda state: state.can_reach_location(RAC3LOCATION.METROPOLIS_RANGERS_5, world.player),

        # RAC3TBOLT.CRASH_SITE
        # RAC3TROPHY.CRASH_NEFARIOUS
        RAC3SKILLPOINT.CRASH_SITE_SUCK:
            lambda state: state.has(RAC3ITEM.SUCK_CANNON, world.player)
                          or state.has(RAC3ITEM.PROGRESSIVE_SUCK_CANNON, world.player, progressive_requirement if ngplus_enabled else 3),
        RAC3SKILLPOINT.CRASH_SITE_AIM_HIGH:
            lambda state: state.has_any([RAC3ITEM.FLUX_RIFLE, RAC3ITEM.PROGRESSIVE_FLUX_RIFLE], world.player),
        RAC3LOCATION.CRASH_SITE_NANO_PAK:
            lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.HYPERSHOT], world.player),
        # RAC3LOCATION.CRASH_SITE_ESCAPE_POD
        RAC3LOCATION.CRASH_SITE_INFOBOT_ARIDIA:
            lambda state: state.has_any([RAC3ITEM.HELI_PACK, RAC3ITEM.THRUSTER_PACK, RAC3ITEM.CLANK,
                                         RAC3ITEM.PROGRESSIVE_PACK, RAC3ITEM.HYPERSHOT], world.player)
                          and state.has(RAC3ITEM.GRAV_BOOTS, world.player),

        # RAC3VENDOR.ARIDIA_QWACK_O_RAY
        RAC3SKILLPOINT.ARIDIA_ZAP: lambda state: state.has(RAC3ITEM.REFRACTOR, world.player),
        # RAC3LOCATION.ARIDIA_RANGERS_1
        RAC3LOCATION.ARIDIA_RANGERS_2:
            lambda state: state.can_reach_location(RAC3LOCATION.ARIDIA_RANGERS_1, world.player),
        RAC3TBOLT.ARIDIA_BRIDGE:
            lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player)
                          and state.can_reach_location(RAC3LOCATION.ARIDIA_RANGERS_2, world.player),
        RAC3SKILLPOINT.ARIDIA_HANG_TIME:
            lambda state: state.can_reach_location(RAC3LOCATION.ARIDIA_RANGERS_2, world.player),
        RAC3LOCATION.ARIDIA_RANGERS_3:
            lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player)
                          and state.can_reach_location(RAC3LOCATION.ARIDIA_RANGERS_2, world.player),
        RAC3LOCATION.ARIDIA_RANGERS_4:
            lambda state: state.can_reach_location(RAC3LOCATION.ARIDIA_RANGERS_3, world.player),
        RAC3TBOLT.ARIDIA_BASE:
            lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player)
                          and state.can_reach_location(RAC3LOCATION.ARIDIA_RANGERS_4, world.player),
        RAC3LOCATION.ARIDIA_RANGERS_5:
            lambda state: state.can_reach_location(RAC3LOCATION.ARIDIA_RANGERS_4, world.player),
        RAC3LOCATION.ARIDIA_WARP_PAD:
            lambda state: state.can_reach_location(RAC3LOCATION.ARIDIA_RANGERS_5, world.player),

        RAC3TBOLT.HIDEOUT: lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),
        RAC3LOCATION.HIDEOUT_PDA: lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),
        RAC3SKILLPOINT.HIDEOUT_DAN: lambda state: state.has_all([RAC3ITEM.WARP_PAD, RAC3ITEM.HYPERSHOT], world.player),
        RAC3TROPHY.HIDEOUT_QWARK:
            lambda state: state.has_all([RAC3ITEM.WARP_PAD, RAC3ITEM.HYPERSHOT], world.player) and
                          state.has_any([RAC3ITEM.HELI_PACK, RAC3ITEM.CLANK,
                                         RAC3ITEM.PROGRESSIVE_PACK, RAC3ITEM.CHARGE_BOOTS], world.player),
        RAC3LOCATION.HIDEOUT_FIND_QWARK:
            lambda state: state.has_all([RAC3ITEM.WARP_PAD, RAC3ITEM.HYPERSHOT], world.player) and
                          state.has_any([RAC3ITEM.HELI_PACK, RAC3ITEM.CLANK,
                                         RAC3ITEM.PROGRESSIVE_PACK, RAC3ITEM.CHARGE_BOOTS], world.player),

        # RAC3TROPHY.KOROS_COURTNEY
        # RAC3TBOLT.KOROS_FENCE
        # RAC3TBOLT.KOROS_GLASS
        RAC3SKILLPOINT.KOROS_BREAK: lambda state: state.has(RAC3ITEM.BOX_BREAKER, world.player),
        # RAC3LOCATION.KOROS_BASE

        RAC3TBOLT.COMMAND_CENTER:
            lambda state: state.has_all([RAC3ITEM.HYPERSHOT, RAC3ITEM.GRAV_BOOTS, RAC3ITEM.TYHRRA_GUISE], world.player),
        RAC3TROPHY.COMMAND_LAWRENCE:
            lambda state: state.has_all([RAC3ITEM.HYPERSHOT, RAC3ITEM.GRAV_BOOTS, RAC3ITEM.TYHRRA_GUISE], world.player)
                          and state.has_any([RAC3ITEM.HELI_PACK, RAC3ITEM.THRUSTER_PACK,
                                             RAC3ITEM.CLANK, RAC3ITEM.PROGRESSIVE_PACK], world.player),
        RAC3SKILLPOINT.COMMAND_CENTER_GERMS:
            lambda state: state.has_any([RAC3ITEM.INFECTOR, RAC3ITEM.PROGRESSIVE_INFECTOR], world.player) and
                          state.has_all([RAC3ITEM.HYPERSHOT, RAC3ITEM.GRAV_BOOTS, RAC3ITEM.TYHRRA_GUISE], world.player),
        RAC3LOCATION.COMMAND_CENTER_NEFARIOUS:
            lambda state: state.has_all([RAC3ITEM.HYPERSHOT, RAC3ITEM.GRAV_BOOTS, RAC3ITEM.TYHRRA_GUISE,
                                         RAC3ITEM.HACKER, RAC3ITEM.REFRACTOR], world.player)
                          and state.has_any([RAC3ITEM.HELI_PACK, RAC3ITEM.THRUSTER_PACK,
                                             RAC3ITEM.CLANK, RAC3ITEM.PROGRESSIVE_PACK], world.player),
        RAC3LOCATION.COMMAND_CENTER_BIOBLITERATOR:
            lambda state: state.has_all([RAC3ITEM.HYPERSHOT, RAC3ITEM.GRAV_BOOTS, RAC3ITEM.TYHRRA_GUISE,
                                         RAC3ITEM.HACKER, RAC3ITEM.REFRACTOR], world.player)
                          and state.has_any([RAC3ITEM.HELI_PACK, RAC3ITEM.THRUSTER_PACK,
                                             RAC3ITEM.CLANK, RAC3ITEM.PROGRESSIVE_PACK], world.player),

        RAC3VENDORLOCATION.NGPLUS_RY3N0: lambda state: state.has_from_list(infobot_data.keys(), world.player, 10),

        RAC3NANOTECH.LEVEL_11: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 1)),
        RAC3NANOTECH.LEVEL_12: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 1)),
        RAC3NANOTECH.LEVEL_13: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 1)),
        RAC3NANOTECH.LEVEL_14: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 1)),
        RAC3NANOTECH.LEVEL_15: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 1)),
        RAC3NANOTECH.LEVEL_16: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 2)),
        RAC3NANOTECH.LEVEL_17: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 2)),
        RAC3NANOTECH.LEVEL_18: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 2)),
        RAC3NANOTECH.LEVEL_19: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 2)),
        RAC3NANOTECH.LEVEL_20: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 2)),
        RAC3NANOTECH.LEVEL_21: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 3)),
        RAC3NANOTECH.LEVEL_22: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 3)),
        RAC3NANOTECH.LEVEL_23: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 3)),
        RAC3NANOTECH.LEVEL_24: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 3)),
        RAC3NANOTECH.LEVEL_25: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 3)),
        RAC3NANOTECH.LEVEL_26: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 4)),
        RAC3NANOTECH.LEVEL_27: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 4)),
        RAC3NANOTECH.LEVEL_28: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 4)),
        RAC3NANOTECH.LEVEL_29: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 4)),
        RAC3NANOTECH.LEVEL_30: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 4)),
        RAC3NANOTECH.LEVEL_31: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 5)),
        RAC3NANOTECH.LEVEL_32: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 5)),
        RAC3NANOTECH.LEVEL_33: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 5)),
        RAC3NANOTECH.LEVEL_34: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 5)),
        RAC3NANOTECH.LEVEL_35: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 5)),
        RAC3NANOTECH.LEVEL_36: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 6)),
        RAC3NANOTECH.LEVEL_37: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 6)),
        RAC3NANOTECH.LEVEL_38: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 6)),
        RAC3NANOTECH.LEVEL_39: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 6)),
        RAC3NANOTECH.LEVEL_40: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 6)),
        RAC3NANOTECH.LEVEL_41: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 7)),
        RAC3NANOTECH.LEVEL_42: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 7)),
        RAC3NANOTECH.LEVEL_43: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 7)),
        RAC3NANOTECH.LEVEL_44: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 7)),
        RAC3NANOTECH.LEVEL_45: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 7)),
        RAC3NANOTECH.LEVEL_46: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 8)),
        RAC3NANOTECH.LEVEL_47: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 8)),
        RAC3NANOTECH.LEVEL_48: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 8)),
        RAC3NANOTECH.LEVEL_49: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 8)),
        RAC3NANOTECH.LEVEL_50: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 8)),
        RAC3NANOTECH.LEVEL_51: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 9)),
        RAC3NANOTECH.LEVEL_52: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 9)),
        RAC3NANOTECH.LEVEL_53: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 9)),
        RAC3NANOTECH.LEVEL_54: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 9)),
        RAC3NANOTECH.LEVEL_55: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 9)),
        RAC3NANOTECH.LEVEL_56: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 10)),
        RAC3NANOTECH.LEVEL_57: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 10)),
        RAC3NANOTECH.LEVEL_58: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 10)),
        RAC3NANOTECH.LEVEL_59: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 10)),
        RAC3NANOTECH.LEVEL_60: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 10)),
        RAC3NANOTECH.LEVEL_61: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 11)),
        RAC3NANOTECH.LEVEL_62: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 11)),
        RAC3NANOTECH.LEVEL_63: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 11)),
        RAC3NANOTECH.LEVEL_64: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 11)),
        RAC3NANOTECH.LEVEL_65: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 11)),
        RAC3NANOTECH.LEVEL_66: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 12)),
        RAC3NANOTECH.LEVEL_67: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 12)),
        RAC3NANOTECH.LEVEL_68: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 12)),
        RAC3NANOTECH.LEVEL_69: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 12)),
        RAC3NANOTECH.LEVEL_70: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 12)),
        RAC3NANOTECH.LEVEL_71: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 13)),
        RAC3NANOTECH.LEVEL_72: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 13)),
        RAC3NANOTECH.LEVEL_73: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 13)),
        RAC3NANOTECH.LEVEL_74: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 13)),
        RAC3NANOTECH.LEVEL_75: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 13)),
        RAC3NANOTECH.LEVEL_76: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 14)),
        RAC3NANOTECH.LEVEL_77: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 14)),
        RAC3NANOTECH.LEVEL_78: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 14)),
        RAC3NANOTECH.LEVEL_79: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 14)),
        RAC3NANOTECH.LEVEL_80: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 14)),
        RAC3NANOTECH.LEVEL_81: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 15)),
        RAC3NANOTECH.LEVEL_82: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 15)),
        RAC3NANOTECH.LEVEL_83: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 15)),
        RAC3NANOTECH.LEVEL_84: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 15)),
        RAC3NANOTECH.LEVEL_85: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 15)),
        RAC3NANOTECH.LEVEL_86: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 16)),
        RAC3NANOTECH.LEVEL_87: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 16)),
        RAC3NANOTECH.LEVEL_88: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 16)),
        RAC3NANOTECH.LEVEL_89: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 16)),
        RAC3NANOTECH.LEVEL_90: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 16)),
        RAC3NANOTECH.LEVEL_91: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 17)),
        RAC3NANOTECH.LEVEL_92: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 17)),
        RAC3NANOTECH.LEVEL_93: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 17)),
        RAC3NANOTECH.LEVEL_94: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 17)),
        RAC3NANOTECH.LEVEL_95: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 17)),
        RAC3NANOTECH.LEVEL_96: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 18)),
        RAC3NANOTECH.LEVEL_97: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 18)),
        RAC3NANOTECH.LEVEL_98: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 18)),
        RAC3NANOTECH.LEVEL_99: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 18)),
        RAC3NANOTECH.LEVEL_100: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 18)),
        RAC3NANOTECH.LEVEL_101: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 1, True)),
        RAC3NANOTECH.LEVEL_102: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 1, True)),
        RAC3NANOTECH.LEVEL_103: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 1, True)),
        RAC3NANOTECH.LEVEL_104: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 1, True)),
        RAC3NANOTECH.LEVEL_105: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 1, True)),
        RAC3NANOTECH.LEVEL_106: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 1, True)),
        RAC3NANOTECH.LEVEL_107: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 1, True)),
        RAC3NANOTECH.LEVEL_108: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 1, True)),
        RAC3NANOTECH.LEVEL_109: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 1, True)),
        RAC3NANOTECH.LEVEL_110: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 1, True)),
        RAC3NANOTECH.LEVEL_111: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 2, True)),
        RAC3NANOTECH.LEVEL_112: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 2, True)),
        RAC3NANOTECH.LEVEL_113: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 2, True)),
        RAC3NANOTECH.LEVEL_114: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 2, True)),
        RAC3NANOTECH.LEVEL_115: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 2, True)),
        RAC3NANOTECH.LEVEL_116: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 2, True)),
        RAC3NANOTECH.LEVEL_117: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 2, True)),
        RAC3NANOTECH.LEVEL_118: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 2, True)),
        RAC3NANOTECH.LEVEL_119: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 2, True)),
        RAC3NANOTECH.LEVEL_120: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 2, True)),
        RAC3NANOTECH.LEVEL_121: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 3, True)),
        RAC3NANOTECH.LEVEL_122: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 3, True)),
        RAC3NANOTECH.LEVEL_123: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 3, True)),
        RAC3NANOTECH.LEVEL_124: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 3, True)),
        RAC3NANOTECH.LEVEL_125: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 3, True)),
        RAC3NANOTECH.LEVEL_126: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 3, True)),
        RAC3NANOTECH.LEVEL_127: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 3, True)),
        RAC3NANOTECH.LEVEL_128: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 3, True)),
        RAC3NANOTECH.LEVEL_129: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 3, True)),
        RAC3NANOTECH.LEVEL_130: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 3, True)),
        RAC3NANOTECH.LEVEL_131: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 4, True)),
        RAC3NANOTECH.LEVEL_132: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 4, True)),
        RAC3NANOTECH.LEVEL_133: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 4, True)),
        RAC3NANOTECH.LEVEL_134: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 4, True)),
        RAC3NANOTECH.LEVEL_135: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 4, True)),
        RAC3NANOTECH.LEVEL_136: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 4, True)),
        RAC3NANOTECH.LEVEL_137: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 4, True)),
        RAC3NANOTECH.LEVEL_138: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 4, True)),
        RAC3NANOTECH.LEVEL_139: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 4, True)),
        RAC3NANOTECH.LEVEL_140: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 4, True)),
        RAC3NANOTECH.LEVEL_141: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 5, True)),
        RAC3NANOTECH.LEVEL_142: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 5, True)),
        RAC3NANOTECH.LEVEL_143: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 5, True)),
        RAC3NANOTECH.LEVEL_144: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 5, True)),
        RAC3NANOTECH.LEVEL_145: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 5, True)),
        RAC3NANOTECH.LEVEL_146: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 5, True)),
        RAC3NANOTECH.LEVEL_147: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 5, True)),
        RAC3NANOTECH.LEVEL_148: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 5, True)),
        RAC3NANOTECH.LEVEL_149: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 5, True)),
        RAC3NANOTECH.LEVEL_150: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 5, True)),
        RAC3NANOTECH.LEVEL_151: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 6, True)),
        RAC3NANOTECH.LEVEL_152: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 6, True)),
        RAC3NANOTECH.LEVEL_153: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 6, True)),
        RAC3NANOTECH.LEVEL_154: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 6, True)),
        RAC3NANOTECH.LEVEL_155: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 6, True)),
        RAC3NANOTECH.LEVEL_156: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 6, True)),
        RAC3NANOTECH.LEVEL_157: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 6, True)),
        RAC3NANOTECH.LEVEL_158: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 6, True)),
        RAC3NANOTECH.LEVEL_159: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 6, True)),
        RAC3NANOTECH.LEVEL_160: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 6, True)),
        RAC3NANOTECH.LEVEL_161: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 7, True)),
        RAC3NANOTECH.LEVEL_162: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 7, True)),
        RAC3NANOTECH.LEVEL_163: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 7, True)),
        RAC3NANOTECH.LEVEL_164: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 7, True)),
        RAC3NANOTECH.LEVEL_165: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 7, True)),
        RAC3NANOTECH.LEVEL_166: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 7, True)),
        RAC3NANOTECH.LEVEL_167: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 7, True)),
        RAC3NANOTECH.LEVEL_168: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 7, True)),
        RAC3NANOTECH.LEVEL_169: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 7, True)),
        RAC3NANOTECH.LEVEL_170: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 7, True)),
        RAC3NANOTECH.LEVEL_171: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 8, True)),
        RAC3NANOTECH.LEVEL_172: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 8, True)),
        RAC3NANOTECH.LEVEL_173: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 8, True)),
        RAC3NANOTECH.LEVEL_174: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 8, True)),
        RAC3NANOTECH.LEVEL_175: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 8, True)),
        RAC3NANOTECH.LEVEL_176: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 8, True)),
        RAC3NANOTECH.LEVEL_177: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 8, True)),
        RAC3NANOTECH.LEVEL_178: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 8, True)),
        RAC3NANOTECH.LEVEL_179: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 8, True)),
        RAC3NANOTECH.LEVEL_180: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 8, True)),
        RAC3NANOTECH.LEVEL_181: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 9, True)),
        RAC3NANOTECH.LEVEL_182: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 9, True)),
        RAC3NANOTECH.LEVEL_183: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 9, True)),
        RAC3NANOTECH.LEVEL_184: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 9, True)),
        RAC3NANOTECH.LEVEL_185: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 9, True)),
        RAC3NANOTECH.LEVEL_186: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 9, True)),
        RAC3NANOTECH.LEVEL_187: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 9, True)),
        RAC3NANOTECH.LEVEL_188: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 9, True)),
        RAC3NANOTECH.LEVEL_189: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 9, True)),
        RAC3NANOTECH.LEVEL_190: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 9, True)),
        RAC3NANOTECH.LEVEL_191: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 10, True)),
        RAC3NANOTECH.LEVEL_192: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 10, True)),
        RAC3NANOTECH.LEVEL_193: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 10, True)),
        RAC3NANOTECH.LEVEL_194: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 10, True)),
        RAC3NANOTECH.LEVEL_195: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 10, True)),
        RAC3NANOTECH.LEVEL_196: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 10, True)),
        RAC3NANOTECH.LEVEL_197: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 10, True)),
        RAC3NANOTECH.LEVEL_198: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 10, True)),
        RAC3NANOTECH.LEVEL_199: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 10, True)),
        RAC3NANOTECH.LEVEL_200: lambda state: state.has_from_list(infobot_data.keys(), world.player, calc_nanotech_requirement(world, 10, True)),

        RAC3WEAPONLEVEL.SHOCK_BLASTER_V2: lambda state: state.has(RAC3ITEM.SHOCK_BLASTER, world.player),
        RAC3WEAPONLEVEL.SHOCK_BLASTER_V3: lambda state: state.has(RAC3ITEM.SHOCK_BLASTER, world.player),
        RAC3WEAPONLEVEL.SHOCK_BLASTER_V4: lambda state: state.has(RAC3ITEM.SHOCK_BLASTER, world.player),
        RAC3WEAPONLEVEL.SHOCK_BLASTER_V5: lambda state: state.has(RAC3ITEM.SHOCK_BLASTER, world.player),
        RAC3WEAPONLEVEL.SHOCK_BLASTER_V6: lambda state: state.has(RAC3ITEM.SHOCK_BLASTER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.SHOCK_BLASTER_V7: lambda state: state.has(RAC3ITEM.SHOCK_BLASTER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.SHOCK_BLASTER_V8: lambda state: state.has(RAC3ITEM.SHOCK_BLASTER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.NITRO_LAUNCHER_V2: lambda state: state.has(RAC3ITEM.NITRO_LAUNCHER, world.player),
        RAC3WEAPONLEVEL.NITRO_LAUNCHER_V3: lambda state: state.has(RAC3ITEM.NITRO_LAUNCHER, world.player),
        RAC3WEAPONLEVEL.NITRO_LAUNCHER_V4: lambda state: state.has(RAC3ITEM.NITRO_LAUNCHER, world.player),
        RAC3WEAPONLEVEL.NITRO_LAUNCHER_V5: lambda state: state.has(RAC3ITEM.NITRO_LAUNCHER, world.player),
        RAC3WEAPONLEVEL.NITRO_LAUNCHER_V6: lambda state: state.has(RAC3ITEM.NITRO_LAUNCHER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.NITRO_LAUNCHER_V7: lambda state: state.has(RAC3ITEM.NITRO_LAUNCHER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.NITRO_LAUNCHER_V8: lambda state: state.has(RAC3ITEM.NITRO_LAUNCHER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.PLASMA_WHIP_V2: lambda state: state.has(RAC3ITEM.PLASMA_WHIP, world.player),
        RAC3WEAPONLEVEL.PLASMA_WHIP_V3: lambda state: state.has(RAC3ITEM.PLASMA_WHIP, world.player),
        RAC3WEAPONLEVEL.PLASMA_WHIP_V4: lambda state: state.has(RAC3ITEM.PLASMA_WHIP, world.player),
        RAC3WEAPONLEVEL.PLASMA_WHIP_V5: lambda state: state.has(RAC3ITEM.PLASMA_WHIP, world.player),
        RAC3WEAPONLEVEL.PLASMA_WHIP_V6: lambda state: state.has(RAC3ITEM.PLASMA_WHIP, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.PLASMA_WHIP_V7: lambda state: state.has(RAC3ITEM.PLASMA_WHIP, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.PLASMA_WHIP_V8: lambda state: state.has(RAC3ITEM.PLASMA_WHIP, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.N60_STORM_V2: lambda state: state.has(RAC3ITEM.N60_STORM, world.player),
        RAC3WEAPONLEVEL.N60_STORM_V3: lambda state: state.has(RAC3ITEM.N60_STORM, world.player),
        RAC3WEAPONLEVEL.N60_STORM_V4: lambda state: state.has(RAC3ITEM.N60_STORM, world.player),
        RAC3WEAPONLEVEL.N60_STORM_V5: lambda state: state.has(RAC3ITEM.N60_STORM, world.player),
        RAC3WEAPONLEVEL.N60_STORM_V6: lambda state: state.has(RAC3ITEM.N60_STORM, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.N60_STORM_V7: lambda state: state.has(RAC3ITEM.N60_STORM, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.N60_STORM_V8: lambda state: state.has(RAC3ITEM.N60_STORM, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.INFECTOR_V2: lambda state: state.has(RAC3ITEM.INFECTOR, world.player),
        RAC3WEAPONLEVEL.INFECTOR_V3: lambda state: state.has(RAC3ITEM.INFECTOR, world.player),
        RAC3WEAPONLEVEL.INFECTOR_V4: lambda state: state.has(RAC3ITEM.INFECTOR, world.player),
        RAC3WEAPONLEVEL.INFECTOR_V5: lambda state: state.has(RAC3ITEM.INFECTOR, world.player),
        RAC3WEAPONLEVEL.INFECTOR_V6: lambda state: state.has(RAC3ITEM.INFECTOR, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.INFECTOR_V7: lambda state: state.has(RAC3ITEM.INFECTOR, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.INFECTOR_V8: lambda state: state.has(RAC3ITEM.INFECTOR, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.SUCK_CANNON_V2: lambda state: state.has(RAC3ITEM.SUCK_CANNON, world.player),
        RAC3WEAPONLEVEL.SUCK_CANNON_V3: lambda state: state.has(RAC3ITEM.SUCK_CANNON, world.player),
        RAC3WEAPONLEVEL.SUCK_CANNON_V4: lambda state: state.has(RAC3ITEM.SUCK_CANNON, world.player),
        RAC3WEAPONLEVEL.SUCK_CANNON_V5: lambda state: state.has(RAC3ITEM.SUCK_CANNON, world.player),
        RAC3WEAPONLEVEL.SUCK_CANNON_V6: lambda state: state.has(RAC3ITEM.SUCK_CANNON, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.SUCK_CANNON_V7: lambda state: state.has(RAC3ITEM.SUCK_CANNON, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.SUCK_CANNON_V8: lambda state: state.has(RAC3ITEM.SUCK_CANNON, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.SPITTING_HYDRA_V2: lambda state: state.has(RAC3ITEM.SPITTING_HYDRA, world.player),
        RAC3WEAPONLEVEL.SPITTING_HYDRA_V3: lambda state: state.has(RAC3ITEM.SPITTING_HYDRA, world.player),
        RAC3WEAPONLEVEL.SPITTING_HYDRA_V4: lambda state: state.has(RAC3ITEM.SPITTING_HYDRA, world.player),
        RAC3WEAPONLEVEL.SPITTING_HYDRA_V5: lambda state: state.has(RAC3ITEM.SPITTING_HYDRA, world.player),
        RAC3WEAPONLEVEL.SPITTING_HYDRA_V6: lambda state: state.has(RAC3ITEM.SPITTING_HYDRA, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.SPITTING_HYDRA_V7: lambda state: state.has(RAC3ITEM.SPITTING_HYDRA, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.SPITTING_HYDRA_V8: lambda state: state.has(RAC3ITEM.SPITTING_HYDRA, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.AGENTS_OF_DOOM_V2: lambda state: state.has(RAC3ITEM.AGENTS_OF_DOOM, world.player),
        RAC3WEAPONLEVEL.AGENTS_OF_DOOM_V3: lambda state: state.has(RAC3ITEM.AGENTS_OF_DOOM, world.player),
        RAC3WEAPONLEVEL.AGENTS_OF_DOOM_V4: lambda state: state.has(RAC3ITEM.AGENTS_OF_DOOM, world.player),
        RAC3WEAPONLEVEL.AGENTS_OF_DOOM_V5: lambda state: state.has(RAC3ITEM.AGENTS_OF_DOOM, world.player),
        RAC3WEAPONLEVEL.AGENTS_OF_DOOM_V6: lambda state: state.has(RAC3ITEM.AGENTS_OF_DOOM, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.AGENTS_OF_DOOM_V7: lambda state: state.has(RAC3ITEM.AGENTS_OF_DOOM, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.AGENTS_OF_DOOM_V8: lambda state: state.has(RAC3ITEM.AGENTS_OF_DOOM, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.FLUX_RIFLE_V2: lambda state: state.has(RAC3ITEM.FLUX_RIFLE, world.player),
        RAC3WEAPONLEVEL.FLUX_RIFLE_V3: lambda state: state.has(RAC3ITEM.FLUX_RIFLE, world.player),
        RAC3WEAPONLEVEL.FLUX_RIFLE_V4: lambda state: state.has(RAC3ITEM.FLUX_RIFLE, world.player),
        RAC3WEAPONLEVEL.FLUX_RIFLE_V5: lambda state: state.has(RAC3ITEM.FLUX_RIFLE, world.player),
        RAC3WEAPONLEVEL.FLUX_RIFLE_V6: lambda state: state.has(RAC3ITEM.FLUX_RIFLE, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.FLUX_RIFLE_V7: lambda state: state.has(RAC3ITEM.FLUX_RIFLE, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.FLUX_RIFLE_V8: lambda state: state.has(RAC3ITEM.FLUX_RIFLE, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.LAVA_GUN_V2: lambda state: state.has(RAC3ITEM.LAVA_GUN, world.player),
        RAC3WEAPONLEVEL.LAVA_GUN_V3: lambda state: state.has(RAC3ITEM.LAVA_GUN, world.player),
        RAC3WEAPONLEVEL.LAVA_GUN_V4: lambda state: state.has(RAC3ITEM.LAVA_GUN, world.player),
        RAC3WEAPONLEVEL.LAVA_GUN_V5: lambda state: state.has(RAC3ITEM.LAVA_GUN, world.player),
        RAC3WEAPONLEVEL.LAVA_GUN_V6: lambda state: state.has(RAC3ITEM.LAVA_GUN, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.LAVA_GUN_V7: lambda state: state.has(RAC3ITEM.LAVA_GUN, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.LAVA_GUN_V8: lambda state: state.has(RAC3ITEM.LAVA_GUN, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.MINI_TURRET_V2: lambda state: state.has(RAC3ITEM.MINI_TURRET, world.player),
        RAC3WEAPONLEVEL.MINI_TURRET_V3: lambda state: state.has(RAC3ITEM.MINI_TURRET, world.player),
        RAC3WEAPONLEVEL.MINI_TURRET_V4: lambda state: state.has(RAC3ITEM.MINI_TURRET, world.player),
        RAC3WEAPONLEVEL.MINI_TURRET_V5: lambda state: state.has(RAC3ITEM.MINI_TURRET, world.player),
        RAC3WEAPONLEVEL.MINI_TURRET_V6: lambda state: state.has(RAC3ITEM.MINI_TURRET, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.MINI_TURRET_V7: lambda state: state.has(RAC3ITEM.MINI_TURRET, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.MINI_TURRET_V8: lambda state: state.has(RAC3ITEM.MINI_TURRET, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.ANNIHILATOR_V2: lambda state: state.has(RAC3ITEM.ANNIHILATOR, world.player),
        RAC3WEAPONLEVEL.ANNIHILATOR_V3: lambda state: state.has(RAC3ITEM.ANNIHILATOR, world.player),
        RAC3WEAPONLEVEL.ANNIHILATOR_V4: lambda state: state.has(RAC3ITEM.ANNIHILATOR, world.player),
        RAC3WEAPONLEVEL.ANNIHILATOR_V5: lambda state: state.has(RAC3ITEM.ANNIHILATOR, world.player),
        RAC3WEAPONLEVEL.ANNIHILATOR_V6: lambda state: state.has(RAC3ITEM.ANNIHILATOR, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.ANNIHILATOR_V7: lambda state: state.has(RAC3ITEM.ANNIHILATOR, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.ANNIHILATOR_V8: lambda state: state.has(RAC3ITEM.ANNIHILATOR, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.HOLO_SHIELD_V2: lambda state: state.has(RAC3ITEM.HOLO_SHIELD, world.player),
        RAC3WEAPONLEVEL.HOLO_SHIELD_V3: lambda state: state.has(RAC3ITEM.HOLO_SHIELD, world.player),
        RAC3WEAPONLEVEL.HOLO_SHIELD_V4: lambda state: state.has(RAC3ITEM.HOLO_SHIELD, world.player),
        RAC3WEAPONLEVEL.HOLO_SHIELD_V5: lambda state: state.has(RAC3ITEM.HOLO_SHIELD, world.player),
        RAC3WEAPONLEVEL.HOLO_SHIELD_V6: lambda state: state.has(RAC3ITEM.HOLO_SHIELD, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.HOLO_SHIELD_V7: lambda state: state.has(RAC3ITEM.HOLO_SHIELD, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.HOLO_SHIELD_V8: lambda state: state.has(RAC3ITEM.HOLO_SHIELD, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.DISC_BLADE_V2: lambda state: state.has(RAC3ITEM.DISC_BLADE, world.player),
        RAC3WEAPONLEVEL.DISC_BLADE_V3: lambda state: state.has(RAC3ITEM.DISC_BLADE, world.player),
        RAC3WEAPONLEVEL.DISC_BLADE_V4: lambda state: state.has(RAC3ITEM.DISC_BLADE, world.player),
        RAC3WEAPONLEVEL.DISC_BLADE_V5: lambda state: state.has(RAC3ITEM.DISC_BLADE, world.player),
        RAC3WEAPONLEVEL.DISC_BLADE_V6: lambda state: state.has(RAC3ITEM.DISC_BLADE, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.DISC_BLADE_V7: lambda state: state.has(RAC3ITEM.DISC_BLADE, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.DISC_BLADE_V8: lambda state: state.has(RAC3ITEM.DISC_BLADE, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.RIFT_INDUCER_V2: lambda state: state.has(RAC3ITEM.RIFT_INDUCER, world.player),
        RAC3WEAPONLEVEL.RIFT_INDUCER_V3: lambda state: state.has(RAC3ITEM.RIFT_INDUCER, world.player),
        RAC3WEAPONLEVEL.RIFT_INDUCER_V4: lambda state: state.has(RAC3ITEM.RIFT_INDUCER, world.player),
        RAC3WEAPONLEVEL.RIFT_INDUCER_V5: lambda state: state.has(RAC3ITEM.RIFT_INDUCER, world.player),
        RAC3WEAPONLEVEL.RIFT_INDUCER_V6: lambda state: state.has(RAC3ITEM.RIFT_INDUCER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.RIFT_INDUCER_V7: lambda state: state.has(RAC3ITEM.RIFT_INDUCER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.RIFT_INDUCER_V8: lambda state: state.has(RAC3ITEM.RIFT_INDUCER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.QWACK_O_RAY_V2: lambda state: state.has(RAC3ITEM.QWACK_O_RAY, world.player),
        RAC3WEAPONLEVEL.QWACK_O_RAY_V3: lambda state: state.has(RAC3ITEM.QWACK_O_RAY, world.player),
        RAC3WEAPONLEVEL.QWACK_O_RAY_V4: lambda state: state.has(RAC3ITEM.QWACK_O_RAY, world.player),
        RAC3WEAPONLEVEL.QWACK_O_RAY_V5: lambda state: state.has(RAC3ITEM.QWACK_O_RAY, world.player),
        RAC3WEAPONLEVEL.QWACK_O_RAY_V6: lambda state: state.has(RAC3ITEM.QWACK_O_RAY, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.QWACK_O_RAY_V7: lambda state: state.has(RAC3ITEM.QWACK_O_RAY, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.QWACK_O_RAY_V8: lambda state: state.has(RAC3ITEM.QWACK_O_RAY, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.BOUNCER_V2: lambda state: state.has(RAC3ITEM.BOUNCER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.BOUNCER_V3: lambda state: state.has(RAC3ITEM.BOUNCER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.BOUNCER_V4: lambda state: state.has(RAC3ITEM.BOUNCER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.BOUNCER_V5: lambda state: state.has(RAC3ITEM.BOUNCER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.BOUNCER_V6: lambda state: state.has(RAC3ITEM.BOUNCER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.BOUNCER_V7: lambda state: state.has(RAC3ITEM.BOUNCER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.BOUNCER_V8: lambda state: state.has(RAC3ITEM.BOUNCER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.PLASMA_COIL_V2: lambda state: state.has(RAC3ITEM.PLASMA_COIL, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.PLASMA_COIL_V3: lambda state: state.has(RAC3ITEM.PLASMA_COIL, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.PLASMA_COIL_V4: lambda state: state.has(RAC3ITEM.PLASMA_COIL, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.PLASMA_COIL_V5: lambda state: state.has(RAC3ITEM.PLASMA_COIL, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.PLASMA_COIL_V6: lambda state: state.has(RAC3ITEM.PLASMA_COIL, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.PLASMA_COIL_V7: lambda state: state.has(RAC3ITEM.PLASMA_COIL, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.PLASMA_COIL_V8: lambda state: state.has(RAC3ITEM.PLASMA_COIL, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.SHIELD_CHARGER_V2: lambda state: state.has(RAC3ITEM.SHIELD_CHARGER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.SHIELD_CHARGER_V3: lambda state: state.has(RAC3ITEM.SHIELD_CHARGER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.SHIELD_CHARGER_V4: lambda state: state.has(RAC3ITEM.SHIELD_CHARGER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.SHIELD_CHARGER_V5: lambda state: state.has(RAC3ITEM.SHIELD_CHARGER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.SHIELD_CHARGER_V6: lambda state: state.has(RAC3ITEM.SHIELD_CHARGER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.SHIELD_CHARGER_V7: lambda state: state.has(RAC3ITEM.SHIELD_CHARGER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.SHIELD_CHARGER_V8: lambda state: state.has(RAC3ITEM.SHIELD_CHARGER, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.RY3N0_V2: lambda state: state.has(RAC3ITEM.RY3N0, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.RY3N0_V3: lambda state: state.has(RAC3ITEM.RY3N0, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.RY3N0_V4: lambda state: state.has(RAC3ITEM.RY3N0, world.player) and can_earn_good_exp(state, world),
        RAC3WEAPONLEVEL.RY3N0_V5: lambda state: state.has(RAC3ITEM.RY3N0, world.player) and can_earn_good_exp(state, world),
    }
    for region in world.multiworld.get_regions(world.player):
        for entrance in region.entrances:
            add_rule(entrance, region_rules_dict.get(entrance.name, lambda _: True))
    for location in world.get_locations():
        add_rule(location, rules_dict.get(location.name, lambda _: True))

    # world.multiworld.completion_condition[world.player] = lambda state: state.has(RAC3ITEM.VICTORY, world.player)
    world.multiworld.completion_condition[world.player] = lambda state: state.has(RAC3ITEM.VICTORY, world.player)
