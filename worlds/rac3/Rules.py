from logging import DEBUG, getLogger
from typing import Callable, TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule
from worlds.rac3 import location_groups
from worlds.rac3.constants.data.Rac3ItemData import planet_data
from worlds.rac3.constants.locations.Rac3General import RAC3LOCATION
from worlds.rac3.constants.locations.Rac3Skillpoints import RAC3SKILLPOINT
from worlds.rac3.constants.locations.Rac3Tags import RAC3TAG
from worlds.rac3.constants.locations.Rac3TBolts import RAC3TBOLT
from worlds.rac3.constants.locations.Rac3Trophies import RAC3TROPHY
from worlds.rac3.constants.locations.Rac3Vendors import RAC3VENDOR
from worlds.rac3.constants.Rac3Items import RAC3ITEM
from worlds.rac3.constants.Rac3Options import RAC3OPTION
from worlds.rac3.constants.Rac3Region import RAC3REGION
from worlds.rac3.Regions import every_10_nanotech, every_20_nanotech, every_5_nanotech

if TYPE_CHECKING:
    from worlds.rac3 import RaC3World

rac3_logger = getLogger(RAC3OPTION.GAME_TITLE_FULL)
rac3_logger.setLevel(DEBUG)


def all_locations(state: CollectionState, world: "RaC3World", tag):
    check = True
    for loc in location_groups[tag]:
        check &= state.can_reach_location(loc, world.player)
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
        RAC3TROPHY.PHOENIX_TITANIUM_COLLECTOR: lambda state: all_locations(state, world, RAC3TAG.T_BOLT),
        RAC3TROPHY.PHOENIX_FRIEND_OF_THE_RANGERS: lambda state: all_locations(state, world, RAC3TAG.RANGERS),
        RAC3TROPHY.PHOENIX_ANNIHILATION_NATION_CHAMPION:
            lambda state: all_locations(state, world, RAC3REGION.ANNIHILATION_NATION),
        RAC3TROPHY.PHOENIX_SKILL_MASTER: lambda state: all_locations(state, world, RAC3TAG.SKILLPOINT),

        # RAC3VENDOR.MARCADIA_HYDRA
        # RAC3TBOLT.MARCADIA_POOL
        # RAC3LOCATION.MARCADIA_RANGERS_1
        # RAC3LOCATION.MARCADIA_RANGERS_2
        # RAC3LOCATION.MARCADIA_RANGERS_3
        # RAC3LOCATION.MARCADIA_RANGERS_4
        # RAC3LOCATION.MARCADIA_RANGERS_5
        # RAC3LOCATION.MARCADIA_REFRACTOR
        RAC3SKILLPOINT.MARCADIA_REFLECT: lambda state: state.has(RAC3ITEM.REFRACTOR, world.player),
        RAC3TBOLT.MARCADIA_LAST_REFRACTOR:
            lambda state: state.has_all([RAC3ITEM.REFRACTOR, RAC3ITEM.GRAV_BOOTS], world.player),
        RAC3TBOLT.MARCADIA_BEFORE_AL:
            lambda state: state.has_all([RAC3ITEM.REFRACTOR, RAC3ITEM.GRAV_BOOTS], world.player),
        RAC3LOCATION.MARCADIA_MEET_AL: lambda state: state.has(RAC3ITEM.REFRACTOR, world.player),

        # RAC3VENDOR.NATION_AGENTS
        # RAC3TBOLT.NATION_CLIFF
        # RAC3SKILLPOINT.NATION_CAMERA
        # RAC3SKILLPOINT.NATION_FLEE
        # RAC3LOCATION.NATION_TYHRRA_GUISE
        # RAC3LOCATION.NATION_GRAND_PRIZE_BOUT
        # RAC3LOCATION.NATION_THE_TERRIBLE_TWO
        # RAC3LOCATION.NATION_ROBOT_RAMPAGE
        # RAC3LOCATION.NATION_TWO_MINUTE_WARNING
        # RAC3LOCATION.NATION_90_SECONDS
        # RAC3LOCATION.NATION_ONSLAUGHT
        RAC3LOCATION.NATION_WHIP_IT_GOOD:
            lambda state: state.has_any([RAC3ITEM.PLASMA_WHIP, RAC3ITEM.PROGRESSIVE_PLASMA_WHIP], world.player),
        RAC3LOCATION.NATION_HYDRA_N_SEEK:
            lambda state: state.has_any([RAC3ITEM.SPITTING_HYDRA, RAC3ITEM.PROGRESSIVE_SPITTING_HYDRA], world.player)
                          and state.can_reach_location(RAC3LOCATION.NATION_WHIP_IT_GOOD, world.player),
        # RAC3LOCATION.NATION_CHAMPIONSHIP_BOUT
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
            lambda state: state.has_any([RAC3ITEM.SUCK_CANNON, RAC3ITEM.PROGRESSIVE_SUCK_CANNON], world.player),
        RAC3LOCATION.NATION_NAPTIME:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, player=world.player),
        RAC3LOCATION.NATION_MORE_CYCLING_WEAPONS:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, player=world.player),
        RAC3LOCATION.NATION_DODGE_THE_TWINS:
            lambda state: state.can_reach_location(RAC3LOCATION.DAXX_GUNSHIP, player=world.player),
        RAC3LOCATION.NATION_CHOP_CHOP:
            lambda state: state.has_any([RAC3ITEM.DISC_BLADE, RAC3ITEM.PROGRESSIVE_DISC_BLADE], world.player),
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
        # RAC3LOCATION.NATION_CRISPY_CRITTER
        # RAC3LOCATION.NATION_PYRO_PLAYGROUND
        # RAC3LOCATION.NATION_SUICIDE_RUN
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
        # RAC3SEWER.TRADE_1
        # RAC3SEWER.TRADE_2
        # RAC3SEWER.TRADE_3
        # RAC3SEWER.TRADE_4
        # RAC3SEWER.TRADE_5
        # RAC3SEWER.TRADE_6
        # RAC3SEWER.TRADE_7
        # RAC3SEWER.TRADE_8
        # RAC3SEWER.TRADE_9
        # RAC3SEWER.TRADE_10
        # RAC3SEWER.TRADE_11
        # RAC3SEWER.TRADE_12
        # RAC3SEWER.TRADE_13
        # RAC3SEWER.TRADE_14
        # RAC3SEWER.TRADE_15
        # RAC3SEWER.TRADE_16
        # RAC3SEWER.TRADE_17
        # RAC3SEWER.TRADE_18
        # RAC3SEWER.TRADE_19
        # RAC3SEWER.TRADE_20
        # RAC3SEWER.TRADE_21
        # RAC3SEWER.TRADE_22
        # RAC3SEWER.TRADE_23
        # RAC3SEWER.TRADE_24
        # RAC3SEWER.TRADE_25
        # RAC3SEWER.TRADE_26
        # RAC3SEWER.TRADE_27
        # RAC3SEWER.TRADE_28
        # RAC3SEWER.TRADE_29
        # RAC3SEWER.TRADE_30
        # RAC3SEWER.TRADE_31
        # RAC3SEWER.TRADE_32
        # RAC3SEWER.TRADE_33
        # RAC3SEWER.TRADE_34
        # RAC3SEWER.TRADE_35
        # RAC3SEWER.TRADE_36
        # RAC3SEWER.TRADE_37
        # RAC3SEWER.TRADE_38
        # RAC3SEWER.TRADE_39
        # RAC3SEWER.TRADE_40
        # RAC3SEWER.TRADE_41
        # RAC3SEWER.TRADE_42
        # RAC3SEWER.TRADE_43
        # RAC3SEWER.TRADE_44
        # RAC3SEWER.TRADE_45
        # RAC3SEWER.TRADE_46
        # RAC3SEWER.TRADE_47
        # RAC3SEWER.TRADE_48
        # RAC3SEWER.TRADE_49
        # RAC3SEWER.TRADE_50
        # RAC3SEWER.TRADE_51
        # RAC3SEWER.TRADE_52
        # RAC3SEWER.TRADE_53
        # RAC3SEWER.TRADE_54
        # RAC3SEWER.TRADE_55
        # RAC3SEWER.TRADE_56
        # RAC3SEWER.TRADE_57
        # RAC3SEWER.TRADE_58
        # RAC3SEWER.TRADE_59
        # RAC3SEWER.TRADE_60
        # RAC3SEWER.TRADE_61
        # RAC3SEWER.TRADE_62
        # RAC3SEWER.TRADE_63
        # RAC3SEWER.TRADE_64
        # RAC3SEWER.TRADE_65
        # RAC3SEWER.TRADE_66
        # RAC3SEWER.TRADE_67
        # RAC3SEWER.TRADE_68
        # RAC3SEWER.TRADE_69
        # RAC3SEWER.TRADE_70
        # RAC3SEWER.TRADE_71
        # RAC3SEWER.TRADE_72
        # RAC3SEWER.TRADE_73
        # RAC3SEWER.TRADE_74
        # RAC3SEWER.TRADE_75
        # RAC3SEWER.TRADE_76
        # RAC3SEWER.TRADE_77
        # RAC3SEWER.TRADE_78
        # RAC3SEWER.TRADE_79
        # RAC3SEWER.TRADE_80
        # RAC3SEWER.TRADE_81
        # RAC3SEWER.TRADE_82
        # RAC3SEWER.TRADE_83
        # RAC3SEWER.TRADE_84
        # RAC3SEWER.TRADE_85
        # RAC3SEWER.TRADE_86
        # RAC3SEWER.TRADE_87
        # RAC3SEWER.TRADE_88
        # RAC3SEWER.TRADE_89
        # RAC3SEWER.TRADE_90
        # RAC3SEWER.TRADE_91
        # RAC3SEWER.TRADE_92
        # RAC3SEWER.TRADE_93
        # RAC3SEWER.TRADE_94
        # RAC3SEWER.TRADE_95
        # RAC3SEWER.TRADE_96
        # RAC3SEWER.TRADE_97
        # RAC3SEWER.TRADE_98
        # RAC3SEWER.TRADE_99
        RAC3SKILLPOINT.SEWER_MOTHERLOAD: lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),

        # RAC3VENDOR.TYHRRANOSIS_ANNIHILATOR
        # RAC3VENDOR.TYHRRANOSIS_SHIELD_GLOVE
        RAC3SKILLPOINT.TYHRRANOSIS_SHARPSHOOTER:
            lambda state: state.has_any([RAC3ITEM.FLUX_RIFLE, RAC3ITEM.PROGRESSIVE_FLUX_RIFLE], world.player),
        # RAC3TBOLT.TYHRRANOSIS_CANNON
        # RAC3TROPHY.TYHRRANOSIS_AL
        RAC3TBOLT.TYHRRANOSIS_CAVE: lambda state: state.has(RAC3ITEM.HYPERSHOT, world.player),
        # RAC3LOCATION.TYHRRANOSIS_BOSS
        # RAC3LOCATION.TYHRRANOSIS_RANGERS_1
        # RAC3LOCATION.TYHRRANOSIS_RANGERS_2
        # RAC3LOCATION.TYHRRANOSIS_RANGERS_3
        # RAC3LOCATION.TYHRRANOSIS_RANGERS_4

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
        # RAC3LOCATION.BLACKWATER_CITY_RANGERS_2
        # RAC3LOCATION.BLACKWATER_CITY_RANGERS_3
        # RAC3LOCATION.BLACKWATER_CITY_COMPLETE

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
            lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player) and state.has(RAC3ITEM.REFRACTOR, world.player),
        RAC3TBOLT.METROPOLIS_RANGERS:
            lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player) and state.has(RAC3ITEM.REFRACTOR, world.player),
        RAC3LOCATION.METROPOLIS_RANGERS_1:
            lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player) and state.has(RAC3ITEM.REFRACTOR, world.player),
        RAC3LOCATION.METROPOLIS_RANGERS_2:
            lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player) and state.has(RAC3ITEM.REFRACTOR, world.player),
        RAC3LOCATION.METROPOLIS_RANGERS_3:
            lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player) and state.has(RAC3ITEM.REFRACTOR, world.player),
        RAC3LOCATION.METROPOLIS_RANGERS_4:
            lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player) and state.has(RAC3ITEM.REFRACTOR, world.player),
        RAC3LOCATION.METROPOLIS_RANGERS_5:
            lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player) and state.has(RAC3ITEM.REFRACTOR, world.player),
        RAC3LOCATION.METROPOLIS_MAP_O_MATIC:
            lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player) and state.has(RAC3ITEM.REFRACTOR, world.player),

        # RAC3TBOLT.CRASH_SITE
        # RAC3TROPHY.CRASH_NEFARIOUS
        RAC3SKILLPOINT.CRASH_SITE_SUCK:
            lambda state: state.has_any([RAC3ITEM.SUCK_CANNON, RAC3ITEM.PROGRESSIVE_SUCK_CANNON], world.player),
        RAC3SKILLPOINT.CRASH_SITE_AIM_HIGH:
            lambda state: state.has_any([RAC3ITEM.FLUX_RIFLE, RAC3ITEM.PROGRESSIVE_FLUX_RIFLE], world.player),
        RAC3LOCATION.CRASH_SITE_NANO_PAK:
            lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.HYPERSHOT], world.player),
        # RAC3LOCATION.CRASH_SITE_ESCAPE_POD
        RAC3LOCATION.CRASH_SITE_INFOBOT_ARIDIA: lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),

        # RAC3VENDOR.ARIDIA_QWACK_O_RAY
        RAC3SKILLPOINT.ARIDIA_ZAP: lambda state: state.has(RAC3ITEM.REFRACTOR, world.player),
        # RAC3LOCATION.ARIDIA_RANGERS_1
        RAC3TBOLT.ARIDIA_BRIDGE: lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),
        # RAC3SKILLPOINT.ARIDIA_HANG_TIME
        # RAC3LOCATION.ARIDIA_RANGERS_2
        # RAC3LOCATION.ARIDIA_RANGERS_3
        # RAC3LOCATION.ARIDIA_RANGERS_4
        RAC3TBOLT.ARIDIA_BASE: lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),
        # RAC3LOCATION.ARIDIA_RANGERS_5
        # RAC3LOCATION.ARIDIA_WARP_PAD

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
    }
    # ----- Nanotech -----#

    match world.options.nanotech_milestones.value:
        case 1:  # 5 nanotech level is a check
            for level, name in enumerate(every_5_nanotech):
                add_rule(world.get_location(name),
                         lambda state: state.has_from_list(planet_data.keys(), world.player, level))
        case 2:  # 10 nanotech level is a check
            for level, name in enumerate(every_10_nanotech):
                add_rule(world.get_location(name),
                         lambda state: state.has_from_list(planet_data.keys(), world.player, level))
        case 3:  # 20 nanotech level is a check
            for level, name in enumerate(every_20_nanotech):
                add_rule(world.get_location(name),
                         lambda state: state.has_from_list(planet_data.keys(), world.player, level))

        case 4:  # Every nanotech level is a check
            for level, name in enumerate(location_groups[RAC3TAG.NANOTECH]):
                add_rule(world.get_location(name),
                         lambda state: state.has_from_list(planet_data.keys(), world.player, level))

    for region in region_rules_dict.keys():
        add_rule(world.multiworld.get_entrance(region, world.player), region_rules_dict[region])
    for location in world.get_locations():
        add_rule(location, rules_dict.get(location.name, lambda _: True))

    # world.multiworld.completion_condition[world.player] = lambda state: state.has(RAC3ITEM.VICTORY, world.player)
    world.multiworld.completion_condition[world.player] = lambda state: state.has(RAC3ITEM.VICTORY, world.player)
