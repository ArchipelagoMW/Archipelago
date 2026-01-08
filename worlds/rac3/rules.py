from logging import DEBUG, getLogger
from typing import Callable, TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule
from worlds.rac3 import location_groups
from worlds.rac3.constants.data.item import infobot_data
from worlds.rac3.constants.items import RAC3ITEM
from worlds.rac3.constants.locations.general import RAC3LOCATION
from worlds.rac3.constants.locations.nanotech import RAC3NANOTECH
from worlds.rac3.constants.locations.sewers import RAC3SEWER
from worlds.rac3.constants.locations.skillpoints import RAC3SKILLPOINT
from worlds.rac3.constants.locations.tags import RAC3TAG
from worlds.rac3.constants.locations.tbolts import RAC3TBOLT
from worlds.rac3.constants.locations.trophies import RAC3TROPHY
from worlds.rac3.constants.locations.vendors import RAC3VENDOR
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.constants.region import RAC3REGION

if TYPE_CHECKING:
    from worlds.rac3 import RaC3World

rac3_logger = getLogger(RAC3OPTION.GAME_TITLE_FULL)
rac3_logger.setLevel(DEBUG)


def all_locations(state: CollectionState, world: "RaC3World", tag: str, skip: str):
    check: bool = True
    for loc in world.get_locations():
        if loc.name in location_groups[tag] and loc.name != skip:
            check &= state.can_reach_location(loc.name, world.player)
    return check


def set_rules(world: "RaC3World"):
    region_rules_dict: dict[str, Callable] = {

        # Getting to Marcadia
        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.MARCADIA}":
            lambda state: state.has(RAC3ITEM.MARCADIA, world.player),

        # Getting to Annihilation Nation:
        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.ANNIHILATION_NATION}":
            lambda state: state.has(RAC3ITEM.ANNIHILATION_NATION, world.player),

        # Getting to Aquatos
        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.AQUATOS}":
            lambda state: state.has(RAC3ITEM.AQUATOS, world.player),

        # Getting to Tyhrranosis
        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.TYHRRANOSIS}":
            lambda state: state.has(RAC3ITEM.TYHRRANOSIS, world.player),

        # Getting to Daxx
        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.DAXX}":
            lambda state: state.has(RAC3ITEM.DAXX, world.player),

        # Getting to Obani Gemini
        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.OBANI_GEMINI}":
            lambda state: state.has_all([RAC3ITEM.OBANI_GEMINI, RAC3ITEM.REFRACTOR], world.player),

        # Getting to Blackwater City
        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.BLACKWATER_CITY}":
            lambda state: state.has(RAC3ITEM.BLACKWATER_CITY, world.player),

        # Getting to Holostar Studios
        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.HOLOSTAR_STUDIOS}":
        # Softlock
        # Prevention
            lambda state: state.has_all([RAC3ITEM.HOLOSTAR_STUDIOS, RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT], world.player),

        # Getting to Obani Draco (lol)
        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.OBANI_DRACO}":
            lambda state: state.has_all([RAC3ITEM.OBANI_DRACO, RAC3ITEM.GRAV_BOOTS], world.player),

        # Getting to Zeldrin Starport
        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.ZELDRIN_STARPORT}":
            lambda state: state.has(RAC3ITEM.ZELDRIN_STARPORT, world.player),

        # Getting to Metropolis
        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.METROPOLIS}":
            lambda state: state.has(RAC3ITEM.METROPOLIS, world.player),

        # Getting to Crash Site
        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.CRASH_SITE}":
            lambda state: state.has(RAC3ITEM.CRASH_SITE, world.player),

        # Getting to Aridia
        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.ARIDIA}":
            lambda state: state.has(RAC3ITEM.ARIDIA, world.player),

        # Getting to Qwark's Hideout
        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.QWARKS_HIDEOUT}":
            lambda state: state.has_all([RAC3ITEM.QWARKS_HIDEOUT, RAC3ITEM.REFRACTOR], world.player),
        # Softlock Prevention

        # Getting to Koros
        f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.KOROS}":
            lambda state: state.has(RAC3ITEM.KOROS, world.player),

        # Getting to Command Center
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
        # RAC3TROPHY.FLORANA_RATCHET
        # RAC3TBOLT.FLORANA_PATH_OF_DEATH
        # RAC3SKILLPOINT.FLORANA_PATH
        # RAC3LOCATION.FLORANA_DEFEAT_QWARK

        # RAC3VENDOR.PHOENIX_SUCK
        # RAC3VENDOR.PHOENIX_INFECTOR
        # RAC3VENDOR.PHOENIX_MAGNA_ARMOR
        RAC3VENDOR.PHOENIX_ADAMANTINE: lambda state: state.can_reach(RAC3REGION.AQUATOS, player=world.player),
        RAC3VENDOR.PHOENIX_AEGIS_ARMOR: lambda state: state.can_reach(RAC3REGION.ZELDRIN_STARPORT, player=world.player),
        RAC3VENDOR.PHOENIX_INFERNOX: lambda state: state.can_reach(RAC3REGION.KOROS, player=world.player),
        RAC3SKILLPOINT.PHOENIX_ARMOR: lambda state: state.can_reach(RAC3REGION.KOROS, player=world.player),
        # RAC3LOCATION.PHOENIX_MEET_SASHA
        RAC3SKILLPOINT.PHOENIX_MONKEY: lambda state: state.has(RAC3ITEM.TYHRRA_GUISE, world.player),
        RAC3LOCATION.PHOENIX_ASSAULT:
            lambda state: state.can_reach(RAC3REGION.QWARKS_HIDEOUT, player=world.player)
                          and state.has_all([RAC3ITEM.WARP_PAD, RAC3ITEM.HYPERSHOT], world.player),
        RAC3LOCATION.PHOENIX_GRAND_PRIZE:
            lambda state: state.can_reach(RAC3REGION.ANNIHILATION_NATION, player=world.player),
        RAC3LOCATION.PHOENIX_STAR_MAP: lambda state: state.has(RAC3ITEM.STAR_MAP, player=world.player),
        RAC3LOCATION.PHOENIX_MASTER_PLAN: lambda state: state.has(RAC3ITEM.MASTER_PLAN, player=world.player),
        # RAC3LOCATION.PHOENIX_VR_WARM_UP
        # RAC3LOCATION.PHOENIX_VR_D_L_D
        # RAC3LOCATION.PHOENIX_VR_SPEED_ROUND
        # RAC3LOCATION.PHOENIX_VR_HOT_STEPPER
        # RAC3LOCATION.PHOENIX_VR_90_SECOND
        # RAC3LOCATION.PHOENIX_VR_SHOCKER
        # RAC3LOCATION.PHOENIX_VR_WRENCH
        # RAC3TBOLT.PHOENIX_VR_NERVES
        # RAC3LOCATION.PHOENIX_VR_NERVES
        RAC3TBOLT.PHOENIX_VR_TRAINING:
            lambda state: state.can_reach(RAC3REGION.TYHRRANOSIS, player=world.player)
                          and state.has_all([RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT], player=world.player),
        RAC3LOCATION.PHOENIX_HACKER:
            lambda state: state.can_reach(RAC3REGION.TYHRRANOSIS, player=world.player)
                          and state.has_all([RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT], player=world.player),
        RAC3LOCATION.PHOENIX_HYPERSHOT:
            lambda state: state.can_reach(RAC3REGION.TYHRRANOSIS, player=world.player)
                          and state.has_all([RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT], player=world.player),
        RAC3LOCATION.PHOENIX_VR_TRAINING:
            lambda state: state.can_reach(RAC3REGION.TYHRRANOSIS, player=world.player)
                          and state.has_all([RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT], player=world.player),
        RAC3SKILLPOINT.PHOENIX_VR_TRAINING:
            lambda state: state.can_reach(RAC3REGION.TYHRRANOSIS, player=world.player)
                          and state.has_all([RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT], player=world.player),
        RAC3TBOLT.PHOENIX_VID_COMIC_1: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 1),
        RAC3LOCATION.PHOENIX_VID_COMIC_1_CLEAR:
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 1),
        RAC3SKILLPOINT.PHOENIX_COMIC_1: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 1),
        RAC3TBOLT.PHOENIX_VID_COMIC_2: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 2),
        RAC3LOCATION.PHOENIX_VID_COMIC_2_CLEAR:
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 2),
        RAC3SKILLPOINT.PHOENIX_COMIC_2: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 2),
        RAC3TBOLT.PHOENIX_VID_COMIC_3: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 3),
        RAC3LOCATION.PHOENIX_VID_COMIC_3_CLEAR:
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 3),
        RAC3SKILLPOINT.PHOENIX_COMIC_3: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 3),
        RAC3TBOLT.PHOENIX_VID_COMIC_4: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 4),
        RAC3LOCATION.PHOENIX_VID_COMIC_4_CLEAR:
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 4),
        RAC3SKILLPOINT.PHOENIX_COMIC_4: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 4),
        RAC3TBOLT.PHOENIX_VID_COMIC_5: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 5),
        RAC3LOCATION.PHOENIX_VID_COMIC_5_CLEAR:
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 5),
        RAC3SKILLPOINT.PHOENIX_COMIC_5: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 5),
        RAC3SKILLPOINT.PHOENIX_ARCADE: lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 5),
        RAC3TROPHY.PHOENIX_TITANIUM_COLLECTOR:
            lambda state: all_locations(state, world, RAC3TAG.T_BOLT, RAC3TROPHY.PHOENIX_TITANIUM_COLLECTOR),
        RAC3TROPHY.PHOENIX_FRIEND_OF_THE_RANGERS:
            lambda state: all_locations(state, world, RAC3TAG.RANGERS, RAC3TROPHY.PHOENIX_FRIEND_OF_THE_RANGERS),
        RAC3TROPHY.PHOENIX_ANNIHILATION_NATION_CHAMPION:
            lambda state: all_locations(state, world, RAC3REGION.ANNIHILATION_NATION,
                                        RAC3TROPHY.PHOENIX_ANNIHILATION_NATION_CHAMPION),
        RAC3TROPHY.PHOENIX_SKILL_MASTER:
            lambda state: all_locations(state, world, RAC3TAG.SKILLPOINT, RAC3TROPHY.PHOENIX_SKILL_MASTER),

        # RAC3VENDOR.MARCADIA_HYDRA
        # RAC3TBOLT.MARCADIA_POOL
        # RAC3LOCATION.MARCADIA_RANGERS_1
        RAC3LOCATION.MARCADIA_RANGERS_2:
            lambda state: state.can_reach_location(RAC3LOCATION.MARCADIA_RANGERS_1, player=world.player),
        RAC3LOCATION.MARCADIA_RANGERS_3:
            lambda state: state.can_reach_location(RAC3LOCATION.MARCADIA_RANGERS_2, player=world.player),
        RAC3LOCATION.MARCADIA_RANGERS_4:
            lambda state: state.can_reach_location(RAC3LOCATION.MARCADIA_RANGERS_3, player=world.player),
        RAC3LOCATION.MARCADIA_RANGERS_5:
            lambda state: state.can_reach_location(RAC3LOCATION.MARCADIA_RANGERS_4, player=world.player),
        RAC3LOCATION.MARCADIA_REFRACTOR:
            lambda state: state.can_reach_location(RAC3LOCATION.MARCADIA_RANGERS_5, player=world.player),
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
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_HEAT_STREET, player=world.player),
        RAC3LOCATION.NATION_THE_TERRIBLE_TWO:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_GRAND_PRIZE_BOUT, player=world.player),
        RAC3LOCATION.NATION_ROBOT_RAMPAGE:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_GRAND_PRIZE_BOUT, player=world.player),
        RAC3LOCATION.NATION_TWO_MINUTE_WARNING:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_THE_TERRIBLE_TWO, player=world.player),
        RAC3LOCATION.NATION_90_SECONDS:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_ROBOT_RAMPAGE, player=world.player),
        RAC3LOCATION.NATION_ONSLAUGHT:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_90_SECONDS, player=world.player),
        RAC3LOCATION.NATION_CHAMPIONSHIP_BOUT:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_ONSLAUGHT, player=world.player),
        RAC3LOCATION.NATION_WHIP_IT_GOOD:
            lambda state: state.has_any([RAC3ITEM.PLASMA_WHIP, RAC3ITEM.PROGRESSIVE_PLASMA_WHIP], world.player)
                          and state.can_reach_location(RAC3LOCATION.NATION_ROBOT_RAMPAGE, world.player),
        RAC3LOCATION.NATION_HYDRA_N_SEEK:
            lambda state: state.has_any([RAC3ITEM.SPITTING_HYDRA, RAC3ITEM.PROGRESSIVE_SPITTING_HYDRA], world.player)
                          and state.can_reach_location(RAC3LOCATION.NATION_WHIP_IT_GOOD, world.player),

        RAC3SKILLPOINT.NATION_BASH:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, player=world.player),
        RAC3LOCATION.NATION_MEET_COURTNEY:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, player=world.player),
        RAC3LOCATION.NATION_INFOBOT_HOLOSTAR:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, player=world.player),
        RAC3LOCATION.NATION_NINJA_CHALLENGE:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, player=world.player),
        RAC3LOCATION.NATION_COUNTING_DUCKS:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, player=world.player),
        RAC3LOCATION.NATION_CYCLING_WEAPONS:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, player=world.player),
        RAC3LOCATION.NATION_ONE_HIT_WONDER:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, player=world.player),
        RAC3LOCATION.NATION_TIME_TO_SUCK:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, player=world.player)
                          and state.has_any([RAC3ITEM.SUCK_CANNON, RAC3ITEM.PROGRESSIVE_SUCK_CANNON], world.player),
        RAC3LOCATION.NATION_NAPTIME:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, player=world.player),
        RAC3LOCATION.NATION_MORE_CYCLING_WEAPONS:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, player=world.player),
        RAC3LOCATION.NATION_DODGE_THE_TWINS:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, player=world.player),
        RAC3LOCATION.NATION_CHOP_CHOP:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, player=world.player)
                          and state.has_any([RAC3ITEM.DISC_BLADE, RAC3ITEM.PROGRESSIVE_DISC_BLADE], world.player),
        RAC3LOCATION.NATION_SLEEP_INDUCER:
            lambda state: state.has_any([RAC3ITEM.RIFT_INDUCER, RAC3ITEM.PROGRESSIVE_RIFT_INDUCER], world.player)
                          and state.can_reach_location(RAC3LOCATION.NATION_CHOP_CHOP, world.player),
        RAC3LOCATION.NATION_THE_OTHER_WHITE_MEAT:
            lambda state: state.has_any([RAC3ITEM.QWACK_O_RAY, RAC3ITEM.PROGRESSIVE_QWACK_O_RAY], world.player)
                          and state.can_reach_location(RAC3LOCATION.NATION_SLEEP_INDUCER, world.player),
        RAC3LOCATION.NATION_CHAMPIONSHIP_BOUT_II:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, player=world.player),
        RAC3LOCATION.NATION_QWARKTASTIC_BATTLE: lambda state: state.has(RAC3ITEM.VICTORY, world.player),
        # RAC3LOCATION.NATION_HEAT_STREET
        RAC3LOCATION.NATION_CRISPY_CRITTER:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_HEAT_STREET, player=world.player),
        RAC3LOCATION.NATION_PYRO_PLAYGROUND:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_CRISPY_CRITTER, player=world.player),
        RAC3LOCATION.NATION_SUICIDE_RUN:
            lambda state: state.can_reach_location(RAC3LOCATION.NATION_PYRO_PLAYGROUND, player=world.player),
        RAC3LOCATION.NATION_BBQ_BOULEVARD:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, player=world.player),
        RAC3LOCATION.NATION_MAZE_OF_BLAZE:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, player=world.player),
        RAC3TBOLT.NATION_PLATFORM:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, player=world.player),
        RAC3LOCATION.NATION_CREMATION_STATION:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, player=world.player),
        RAC3LOCATION.NATION_THE_ANNIHILATOR:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, player=world.player),
        RAC3SKILLPOINT.NATION_EIGHT:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, player=world.player),

        # RAC3VENDOR.AQUATOS_FLUX_RIFLE
        # RAC3TBOLT.AQUATOS_BRIDGE
        # RAC3TBOLT.AQUATOS_UNDERWATER
        # RAC3SKILLPOINT.AQUATOS_SUNKEN
        RAC3TBOLT.AQUATOS_GATE: lambda state: state.has(RAC3ITEM.HACKER, world.player),
        # RAC3VENDOR.AQUATOS_MINI_TURRET
        # RAC3VENDOR.AQUATOS_LAVA_GUN
        RAC3VENDOR.AQUATOS_SHIELD_CHARGER:
            lambda state: state.can_reach(RAC3REGION.COMMAND_CENTER, player=world.player),
        RAC3VENDOR.AQUATOS_BOUNCER: lambda state: state.can_reach(RAC3REGION.QWARKS_HIDEOUT, player=world.player),
        RAC3VENDOR.AQUATOS_PLASMA_COIL: lambda state: state.can_reach(RAC3REGION.KOROS, player=world.player),
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
        RAC3SKILLPOINT.SEWER_MOTHERLOAD: lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.MAP_O_MATIC],
                                                                     world.player),

        # RAC3VENDOR.TYHRRANOSIS_ANNIHILATOR
        # RAC3VENDOR.TYHRRANOSIS_SHIELD_GLOVE
        RAC3SKILLPOINT.TYHRRANOSIS_SHARPSHOOTER:
            lambda state: state.has_any([RAC3ITEM.FLUX_RIFLE, RAC3ITEM.PROGRESSIVE_FLUX_RIFLE], world.player),
        # RAC3TBOLT.TYHRRANOSIS_CANNON
        # RAC3TROPHY.TYHRRANOSIS_AL
        RAC3TBOLT.TYHRRANOSIS_CAVE: lambda state: state.has(RAC3ITEM.HYPERSHOT, world.player),
        # RAC3LOCATION.TYHRRANOSIS_BOSS
        RAC3LOCATION.TYHRRANOSIS_RANGERS_1:
            lambda state: state.can_reach_location(RAC3LOCATION.TYHRRANOSIS_BOSS, player=world.player),
        RAC3LOCATION.TYHRRANOSIS_RANGERS_2:
            lambda state: state.can_reach_location(RAC3LOCATION.TYHRRANOSIS_RANGERS_1, player=world.player),
        RAC3LOCATION.TYHRRANOSIS_RANGERS_3:
            lambda state: state.can_reach_location(RAC3LOCATION.TYHRRANOSIS_RANGERS_2, player=world.player),
        RAC3LOCATION.TYHRRANOSIS_RANGERS_4:
            lambda state: state.can_reach_location(RAC3LOCATION.TYHRRANOSIS_RANGERS_3, player=world.player),

        RAC3SKILLPOINT.DAXX_BUGS:
            lambda state: state.has_any([RAC3ITEM.QWACK_O_RAY, RAC3ITEM.PROGRESSIVE_QWACK_O_RAY], world.player),

        # RAC3LOCATION.DAXX_CHARGE_BOOTS
        # RAC3TROPHY.DAXX_PLUMBER
        RAC3LOCATION.DAXX_GUNSHIP: lambda state: state.has(RAC3ITEM.HYPERSHOT, world.player),
        RAC3TBOLT.DAXX_TAXI: lambda state: state.has(RAC3ITEM.HYPERSHOT, world.player),
        RAC3TBOLT.DAXX_DOOR:
            lambda state: state.has_all([RAC3ITEM.HYPERSHOT, RAC3ITEM.HACKER, RAC3ITEM.CHARGE_BOOTS], world.player),
        RAC3LOCATION.DAXX_FACILITY: lambda state: state.has_all([RAC3ITEM.HYPERSHOT, RAC3ITEM.HACKER], world.player),

        # RAC3VENDOR.OBANI_GEMINI_DISC
        RAC3TBOLT.OBANI_GEMINI_1: lambda state: state.has(RAC3ITEM.HYPERSHOT, world.player),
        # RAC3SKILLPOINT.GEMINI_BELT
        # RAC3TBOLT.OBANI_GEMINI_2
        # RAC3LOCATION.OBANI_GEMINI_SKIDD

        # RAC3SKILLPOINT.BLACKWATER_BASH
        # RAC3LOCATION.BLACKWATER_CITY_RANGERS_1
        RAC3LOCATION.BLACKWATER_CITY_RANGERS_2:
            lambda state: state.can_reach_location(RAC3LOCATION.BLACKWATER_CITY_RANGERS_1, player=world.player),
        RAC3LOCATION.BLACKWATER_CITY_RANGERS_3:
            lambda state: state.can_reach_location(RAC3LOCATION.BLACKWATER_CITY_RANGERS_2, player=world.player),
        RAC3LOCATION.BLACKWATER_CITY_COMPLETE:
            lambda state: state.can_reach_location(RAC3LOCATION.BLACKWATER_CITY_RANGERS_3, player=world.player),

        # RAC3VENDOR.HOLOSTAR_RIFT_INDUCER
        # RAC3TROPHY.HOLOSTAR_CLANK
        # RAC3TBOLT.HOLOSTAR_CHAIRS
        # RAC3SKILLPOINT.HOLOSTAR_LUCKY
        RAC3TBOLT.HOLOSTAR_GRAV_RAMP: lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),
        RAC3TBOLT.HOLOSTAR_KAMIKAZE_NOIDS: lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),

        # RAC3LOCATION.SKIDD_CAPTURED

        RAC3LOCATION.DRACO_COURTNEY: lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),

        # RAC3TBOLT.ZELDRIN_STARPORT_1
        RAC3TBOLT.ZELDRIN_STARPORT_2: lambda state: state.has(RAC3ITEM.HYPERSHOT, world.player),
        RAC3LOCATION.ZELDRIN_STARPORT_ITEM: lambda state: state.has(RAC3ITEM.HYPERSHOT, world.player),
        # RAC3LOCATION.ZELDRIN_STARPORT_SHIP

        RAC3SKILLPOINT.METROPOLIS_GOOD_YEAR: lambda state: state.has_any(
            [RAC3ITEM.FLUX_RIFLE, RAC3ITEM.PROGRESSIVE_FLUX_RIFLE, RAC3ITEM.ANNIHILATOR,
             RAC3ITEM.PROGRESSIVE_ANNIHILATOR, RAC3ITEM.RY3N0, RAC3ITEM.PROGRESSIVE_RY3N0, RAC3ITEM.SUCK_CANNON,
             RAC3ITEM.PROGRESSIVE_SUCK_CANNON, RAC3ITEM.DISC_BLADE, RAC3ITEM.PROGRESSIVE_DISC_BLADE], world.player),
        RAC3TBOLT.METROPOLIS_SWING: lambda state: state.has(RAC3ITEM.HYPERSHOT, world.player),
        # RAC3TROPHY.METROPOLIS_SKRUNCH
        # RAC3LOCATION.METROPOLIS_METAL_NOIDS
        # RAC3TBOLT.METROPOLIS_BEHIND
        RAC3LOCATION.METROPOLIS_DEFEAT_KLUNK:
            lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.REFRACTOR], player=world.player),
        RAC3LOCATION.METROPOLIS_RANGERS_1:
            lambda state: state.can_reach_location(RAC3LOCATION.METROPOLIS_DEFEAT_KLUNK, player=world.player),
        RAC3TBOLT.METROPOLIS_RANGERS:
            lambda state: state.can_reach_location(RAC3LOCATION.METROPOLIS_RANGERS_1, player=world.player),
        RAC3LOCATION.METROPOLIS_RANGERS_2:
            lambda state: state.can_reach_location(RAC3LOCATION.METROPOLIS_RANGERS_1, player=world.player),
        RAC3LOCATION.METROPOLIS_RANGERS_3:
            lambda state: state.can_reach_location(RAC3LOCATION.METROPOLIS_RANGERS_2, player=world.player),
        RAC3LOCATION.METROPOLIS_RANGERS_4:
            lambda state: state.can_reach_location(RAC3LOCATION.METROPOLIS_RANGERS_3, player=world.player),
        RAC3LOCATION.METROPOLIS_RANGERS_5:
            lambda state: state.can_reach_location(RAC3LOCATION.METROPOLIS_RANGERS_4, player=world.player),
        RAC3LOCATION.METROPOLIS_MAP_O_MATIC:
            lambda state: state.can_reach_location(RAC3LOCATION.METROPOLIS_RANGERS_5, player=world.player),

        # RAC3TBOLT.CRASH_SITE
        # RAC3TROPHY.CRASH_NEFARIOUS
        RAC3SKILLPOINT.CRASH_SITE_SUCK:
            lambda state: state.has(RAC3ITEM.SUCK_CANNON, world.player)
                          or state.has(RAC3ITEM.PROGRESSIVE_SUCK_CANNON, world.player, 3),
        RAC3SKILLPOINT.CRASH_SITE_AIM_HIGH:
            lambda state: state.has_any([RAC3ITEM.FLUX_RIFLE, RAC3ITEM.PROGRESSIVE_FLUX_RIFLE], world.player),
        RAC3LOCATION.CRASH_SITE_NANO_PAK:
            lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.HYPERSHOT], world.player),
        # RAC3LOCATION.CRASH_SITE_ESCAPE_POD
        RAC3LOCATION.CRASH_SITE_INFOBOT_ARIDIA: lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),

        # RAC3VENDOR.ARIDIA_QWACK_O_RAY
        RAC3SKILLPOINT.ARIDIA_ZAP: lambda state: state.has(RAC3ITEM.REFRACTOR, world.player),
        # RAC3LOCATION.ARIDIA_RANGERS_1
        RAC3LOCATION.ARIDIA_RANGERS_2:
            lambda state: state.can_reach_location(RAC3LOCATION.ARIDIA_RANGERS_1, world.player),
        RAC3TBOLT.ARIDIA_BRIDGE: lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player) and
                                               state.can_reach_location(RAC3LOCATION.ARIDIA_RANGERS_2, world.player),
        RAC3SKILLPOINT.ARIDIA_HANG_TIME:
            lambda state: state.can_reach_location(RAC3LOCATION.ARIDIA_RANGERS_2, world.player),
        RAC3LOCATION.ARIDIA_RANGERS_3: lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player) and
                                                     state.can_reach_location(RAC3LOCATION.ARIDIA_RANGERS_2,
                                                                              world.player),
        RAC3LOCATION.ARIDIA_RANGERS_4:
            lambda state: state.can_reach_location(RAC3LOCATION.ARIDIA_RANGERS_3, world.player),
        RAC3TBOLT.ARIDIA_BASE: lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player) and
                                             state.can_reach_location(RAC3LOCATION.ARIDIA_RANGERS_4, world.player),
        RAC3LOCATION.ARIDIA_RANGERS_5:
            lambda state: state.can_reach_location(RAC3LOCATION.ARIDIA_RANGERS_4, world.player),
        RAC3LOCATION.ARIDIA_WARP_PAD:
            lambda state: state.can_reach_location(RAC3LOCATION.ARIDIA_RANGERS_5, world.player),

        RAC3TBOLT.HIDEOUT: lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),
        RAC3LOCATION.HIDEOUT_PDA: lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),
        RAC3SKILLPOINT.HIDEOUT_DAN: lambda state: state.has_all([RAC3ITEM.WARP_PAD, RAC3ITEM.HYPERSHOT], world.player),
        RAC3TROPHY.HIDEOUT_QWARK: lambda state: state.has_all([RAC3ITEM.WARP_PAD, RAC3ITEM.HYPERSHOT], world.player),
        RAC3LOCATION.HIDEOUT_QWARK: lambda state: state.has_all([RAC3ITEM.WARP_PAD, RAC3ITEM.HYPERSHOT], world.player),

        # RAC3TROPHY.KOROS_COURTNEY
        # RAC3TBOLT.KOROS_FENCE
        # RAC3TBOLT.KOROS_GLASS
        RAC3SKILLPOINT.KOROS_BREAK: lambda state: state.has(RAC3ITEM.BOX_BREAKER, world.player),
        # RAC3LOCATION.KOROS_BASE

        RAC3TBOLT.COMMAND_CENTER:
            lambda state: state.has_all([RAC3ITEM.HYPERSHOT, RAC3ITEM.GRAV_BOOTS, RAC3ITEM.TYHRRA_GUISE], world.player),
        RAC3TROPHY.COMMAND_LAWRENCE: lambda state: state.has_all(
            [RAC3ITEM.HYPERSHOT, RAC3ITEM.GRAV_BOOTS, RAC3ITEM.TYHRRA_GUISE],
            world.player),
        RAC3SKILLPOINT.COMMAND_CENTER_GERMS: lambda state: state.has_any(
            [RAC3ITEM.INFECTOR, RAC3ITEM.PROGRESSIVE_INFECTOR], world.player) and state.has_all(
            [RAC3ITEM.HYPERSHOT, RAC3ITEM.GRAV_BOOTS, RAC3ITEM.TYHRRA_GUISE], world.player),
        RAC3LOCATION.COMMAND_CENTER_NEFARIOUS: lambda state: state.has_all(
            [RAC3ITEM.HYPERSHOT, RAC3ITEM.GRAV_BOOTS, RAC3ITEM.TYHRRA_GUISE, RAC3ITEM.HACKER, RAC3ITEM.REFRACTOR],
            world.player),
        RAC3LOCATION.COMMAND_CENTER_BIOBLITERATOR: lambda state: state.has_all(
            [RAC3ITEM.HYPERSHOT, RAC3ITEM.GRAV_BOOTS, RAC3ITEM.TYHRRA_GUISE, RAC3ITEM.HACKER, RAC3ITEM.REFRACTOR],
            world.player),

        RAC3NANOTECH.LEVEL_11: lambda state: state.has_from_list(infobot_data.keys(), world.player, 3),
        RAC3NANOTECH.LEVEL_12: lambda state: state.has_from_list(infobot_data.keys(), world.player, 3),
        RAC3NANOTECH.LEVEL_13: lambda state: state.has_from_list(infobot_data.keys(), world.player, 3),
        RAC3NANOTECH.LEVEL_14: lambda state: state.has_from_list(infobot_data.keys(), world.player, 3),
        RAC3NANOTECH.LEVEL_15: lambda state: state.has_from_list(infobot_data.keys(), world.player, 3),
        RAC3NANOTECH.LEVEL_16: lambda state: state.has_from_list(infobot_data.keys(), world.player, 4),
        RAC3NANOTECH.LEVEL_17: lambda state: state.has_from_list(infobot_data.keys(), world.player, 4),
        RAC3NANOTECH.LEVEL_18: lambda state: state.has_from_list(infobot_data.keys(), world.player, 4),
        RAC3NANOTECH.LEVEL_19: lambda state: state.has_from_list(infobot_data.keys(), world.player, 4),
        RAC3NANOTECH.LEVEL_20: lambda state: state.has_from_list(infobot_data.keys(), world.player, 4),
        RAC3NANOTECH.LEVEL_21: lambda state: state.has_from_list(infobot_data.keys(), world.player, 5),
        RAC3NANOTECH.LEVEL_22: lambda state: state.has_from_list(infobot_data.keys(), world.player, 5),
        RAC3NANOTECH.LEVEL_23: lambda state: state.has_from_list(infobot_data.keys(), world.player, 5),
        RAC3NANOTECH.LEVEL_24: lambda state: state.has_from_list(infobot_data.keys(), world.player, 5),
        RAC3NANOTECH.LEVEL_25: lambda state: state.has_from_list(infobot_data.keys(), world.player, 5),
        RAC3NANOTECH.LEVEL_26: lambda state: state.has_from_list(infobot_data.keys(), world.player, 6),
        RAC3NANOTECH.LEVEL_27: lambda state: state.has_from_list(infobot_data.keys(), world.player, 6),
        RAC3NANOTECH.LEVEL_28: lambda state: state.has_from_list(infobot_data.keys(), world.player, 6),
        RAC3NANOTECH.LEVEL_29: lambda state: state.has_from_list(infobot_data.keys(), world.player, 6),
        RAC3NANOTECH.LEVEL_30: lambda state: state.has_from_list(infobot_data.keys(), world.player, 6),
        RAC3NANOTECH.LEVEL_31: lambda state: state.has_from_list(infobot_data.keys(), world.player, 7),
        RAC3NANOTECH.LEVEL_32: lambda state: state.has_from_list(infobot_data.keys(), world.player, 7),
        RAC3NANOTECH.LEVEL_33: lambda state: state.has_from_list(infobot_data.keys(), world.player, 7),
        RAC3NANOTECH.LEVEL_34: lambda state: state.has_from_list(infobot_data.keys(), world.player, 7),
        RAC3NANOTECH.LEVEL_35: lambda state: state.has_from_list(infobot_data.keys(), world.player, 7),
        RAC3NANOTECH.LEVEL_36: lambda state: state.has_from_list(infobot_data.keys(), world.player, 8),
        RAC3NANOTECH.LEVEL_37: lambda state: state.has_from_list(infobot_data.keys(), world.player, 8),
        RAC3NANOTECH.LEVEL_38: lambda state: state.has_from_list(infobot_data.keys(), world.player, 8),
        RAC3NANOTECH.LEVEL_39: lambda state: state.has_from_list(infobot_data.keys(), world.player, 8),
        RAC3NANOTECH.LEVEL_40: lambda state: state.has_from_list(infobot_data.keys(), world.player, 8),
        RAC3NANOTECH.LEVEL_41: lambda state: state.has_from_list(infobot_data.keys(), world.player, 9),
        RAC3NANOTECH.LEVEL_42: lambda state: state.has_from_list(infobot_data.keys(), world.player, 9),
        RAC3NANOTECH.LEVEL_43: lambda state: state.has_from_list(infobot_data.keys(), world.player, 9),
        RAC3NANOTECH.LEVEL_44: lambda state: state.has_from_list(infobot_data.keys(), world.player, 9),
        RAC3NANOTECH.LEVEL_45: lambda state: state.has_from_list(infobot_data.keys(), world.player, 9),
        RAC3NANOTECH.LEVEL_46: lambda state: state.has_from_list(infobot_data.keys(), world.player, 10),
        RAC3NANOTECH.LEVEL_47: lambda state: state.has_from_list(infobot_data.keys(), world.player, 10),
        RAC3NANOTECH.LEVEL_48: lambda state: state.has_from_list(infobot_data.keys(), world.player, 10),
        RAC3NANOTECH.LEVEL_49: lambda state: state.has_from_list(infobot_data.keys(), world.player, 10),
        RAC3NANOTECH.LEVEL_50: lambda state: state.has_from_list(infobot_data.keys(), world.player, 10),
        RAC3NANOTECH.LEVEL_51: lambda state: state.has_from_list(infobot_data.keys(), world.player, 11),
        RAC3NANOTECH.LEVEL_52: lambda state: state.has_from_list(infobot_data.keys(), world.player, 11),
        RAC3NANOTECH.LEVEL_53: lambda state: state.has_from_list(infobot_data.keys(), world.player, 11),
        RAC3NANOTECH.LEVEL_54: lambda state: state.has_from_list(infobot_data.keys(), world.player, 11),
        RAC3NANOTECH.LEVEL_55: lambda state: state.has_from_list(infobot_data.keys(), world.player, 11),
        RAC3NANOTECH.LEVEL_56: lambda state: state.has_from_list(infobot_data.keys(), world.player, 12),
        RAC3NANOTECH.LEVEL_57: lambda state: state.has_from_list(infobot_data.keys(), world.player, 12),
        RAC3NANOTECH.LEVEL_58: lambda state: state.has_from_list(infobot_data.keys(), world.player, 12),
        RAC3NANOTECH.LEVEL_59: lambda state: state.has_from_list(infobot_data.keys(), world.player, 12),
        RAC3NANOTECH.LEVEL_60: lambda state: state.has_from_list(infobot_data.keys(), world.player, 12),
        RAC3NANOTECH.LEVEL_61: lambda state: state.has_from_list(infobot_data.keys(), world.player, 13),
        RAC3NANOTECH.LEVEL_62: lambda state: state.has_from_list(infobot_data.keys(), world.player, 13),
        RAC3NANOTECH.LEVEL_63: lambda state: state.has_from_list(infobot_data.keys(), world.player, 13),
        RAC3NANOTECH.LEVEL_64: lambda state: state.has_from_list(infobot_data.keys(), world.player, 13),
        RAC3NANOTECH.LEVEL_65: lambda state: state.has_from_list(infobot_data.keys(), world.player, 13),
        RAC3NANOTECH.LEVEL_66: lambda state: state.has_from_list(infobot_data.keys(), world.player, 14),
        RAC3NANOTECH.LEVEL_67: lambda state: state.has_from_list(infobot_data.keys(), world.player, 14),
        RAC3NANOTECH.LEVEL_68: lambda state: state.has_from_list(infobot_data.keys(), world.player, 14),
        RAC3NANOTECH.LEVEL_69: lambda state: state.has_from_list(infobot_data.keys(), world.player, 14),
        RAC3NANOTECH.LEVEL_70: lambda state: state.has_from_list(infobot_data.keys(), world.player, 14),
        RAC3NANOTECH.LEVEL_71: lambda state: state.has_from_list(infobot_data.keys(), world.player, 15),
        RAC3NANOTECH.LEVEL_72: lambda state: state.has_from_list(infobot_data.keys(), world.player, 15),
        RAC3NANOTECH.LEVEL_73: lambda state: state.has_from_list(infobot_data.keys(), world.player, 15),
        RAC3NANOTECH.LEVEL_74: lambda state: state.has_from_list(infobot_data.keys(), world.player, 15),
        RAC3NANOTECH.LEVEL_75: lambda state: state.has_from_list(infobot_data.keys(), world.player, 15),
        RAC3NANOTECH.LEVEL_76: lambda state: state.has_from_list(infobot_data.keys(), world.player, 16),
        RAC3NANOTECH.LEVEL_77: lambda state: state.has_from_list(infobot_data.keys(), world.player, 16),
        RAC3NANOTECH.LEVEL_78: lambda state: state.has_from_list(infobot_data.keys(), world.player, 16),
        RAC3NANOTECH.LEVEL_79: lambda state: state.has_from_list(infobot_data.keys(), world.player, 16),
        RAC3NANOTECH.LEVEL_80: lambda state: state.has_from_list(infobot_data.keys(), world.player, 16),
        RAC3NANOTECH.LEVEL_81: lambda state: state.has_from_list(infobot_data.keys(), world.player, 17),
        RAC3NANOTECH.LEVEL_82: lambda state: state.has_from_list(infobot_data.keys(), world.player, 17),
        RAC3NANOTECH.LEVEL_83: lambda state: state.has_from_list(infobot_data.keys(), world.player, 17),
        RAC3NANOTECH.LEVEL_84: lambda state: state.has_from_list(infobot_data.keys(), world.player, 17),
        RAC3NANOTECH.LEVEL_85: lambda state: state.has_from_list(infobot_data.keys(), world.player, 17),
        RAC3NANOTECH.LEVEL_86: lambda state: state.has_from_list(infobot_data.keys(), world.player, 18),
        RAC3NANOTECH.LEVEL_87: lambda state: state.has_from_list(infobot_data.keys(), world.player, 18),
        RAC3NANOTECH.LEVEL_88: lambda state: state.has_from_list(infobot_data.keys(), world.player, 18),
        RAC3NANOTECH.LEVEL_89: lambda state: state.has_from_list(infobot_data.keys(), world.player, 18),
        RAC3NANOTECH.LEVEL_90: lambda state: state.has_from_list(infobot_data.keys(), world.player, 18),
        RAC3NANOTECH.LEVEL_91: lambda state: state.has_from_list(infobot_data.keys(), world.player, 19),
        RAC3NANOTECH.LEVEL_92: lambda state: state.has_from_list(infobot_data.keys(), world.player, 19),
        RAC3NANOTECH.LEVEL_93: lambda state: state.has_from_list(infobot_data.keys(), world.player, 19),
        RAC3NANOTECH.LEVEL_94: lambda state: state.has_from_list(infobot_data.keys(), world.player, 19),
        RAC3NANOTECH.LEVEL_95: lambda state: state.has_from_list(infobot_data.keys(), world.player, 19),
        RAC3NANOTECH.LEVEL_96: lambda state: state.has_from_list(infobot_data.keys(), world.player, 20),
        RAC3NANOTECH.LEVEL_97: lambda state: state.has_from_list(infobot_data.keys(), world.player, 20),
        RAC3NANOTECH.LEVEL_98: lambda state: state.has_from_list(infobot_data.keys(), world.player, 20),
        RAC3NANOTECH.LEVEL_99: lambda state: state.has_from_list(infobot_data.keys(), world.player, 20),
        RAC3NANOTECH.LEVEL_100: lambda state: state.has_from_list(infobot_data.keys(), world.player, 20),
    }

    for region in region_rules_dict.keys():
        add_rule(world.multiworld.get_entrance(region, world.player), region_rules_dict[region])
    for location in world.get_locations():
        add_rule(location, rules_dict.get(location.name, lambda _: True))

    # world.multiworld.completion_condition[world.player] = lambda state: state.has(RAC3ITEM.VICTORY, world.player)
    world.multiworld.completion_condition[world.player] = lambda state: state.has(RAC3ITEM.VICTORY, world.player)
