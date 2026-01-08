from typing import TYPE_CHECKING

from BaseClasses import Location, Region
from worlds.rac3 import RAC3LOCATION
from worlds.rac3.constants.data.location import LOCATION_FROM_AP_CODE, RAC3_LOCATION_DATA_TABLE, RAC3LOCATIONDATA
from worlds.rac3.constants.items import RAC3ITEM
from worlds.rac3.constants.locations.nanotech import RAC3NANOTECH
from worlds.rac3.constants.locations.sewers import RAC3SEWER
from worlds.rac3.constants.locations.skillpoints import RAC3SKILLPOINT, SKILLPOINT_LOCATION_TO_NAME
from worlds.rac3.constants.locations.tags import RAC3TAG
from worlds.rac3.constants.locations.tbolts import RAC3TBOLT
from worlds.rac3.constants.locations.trophies import RAC3TROPHY
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.constants.player_type import RAC3PLAYERTYPE
from worlds.rac3.constants.region import RAC3REGION
from worlds.rac3.rac3options import RaC3Options

if TYPE_CHECKING:
    from worlds.rac3 import RaC3World


class GameLocation(Location):
    game = RAC3OPTION.GAME_TITLE_FULL


every_nanotech: list[str] = [
    RAC3NANOTECH.LEVEL_11,
    RAC3NANOTECH.LEVEL_12,
    RAC3NANOTECH.LEVEL_13,
    RAC3NANOTECH.LEVEL_14,
    RAC3NANOTECH.LEVEL_15,
    RAC3NANOTECH.LEVEL_16,
    RAC3NANOTECH.LEVEL_17,
    RAC3NANOTECH.LEVEL_18,
    RAC3NANOTECH.LEVEL_19,
    RAC3NANOTECH.LEVEL_20,
    RAC3NANOTECH.LEVEL_21,
    RAC3NANOTECH.LEVEL_22,
    RAC3NANOTECH.LEVEL_23,
    RAC3NANOTECH.LEVEL_24,
    RAC3NANOTECH.LEVEL_25,
    RAC3NANOTECH.LEVEL_26,
    RAC3NANOTECH.LEVEL_27,
    RAC3NANOTECH.LEVEL_28,
    RAC3NANOTECH.LEVEL_29,
    RAC3NANOTECH.LEVEL_30,
    RAC3NANOTECH.LEVEL_31,
    RAC3NANOTECH.LEVEL_32,
    RAC3NANOTECH.LEVEL_33,
    RAC3NANOTECH.LEVEL_34,
    RAC3NANOTECH.LEVEL_35,
    RAC3NANOTECH.LEVEL_36,
    RAC3NANOTECH.LEVEL_37,
    RAC3NANOTECH.LEVEL_38,
    RAC3NANOTECH.LEVEL_39,
    RAC3NANOTECH.LEVEL_40,
    RAC3NANOTECH.LEVEL_41,
    RAC3NANOTECH.LEVEL_42,
    RAC3NANOTECH.LEVEL_43,
    RAC3NANOTECH.LEVEL_44,
    RAC3NANOTECH.LEVEL_45,
    RAC3NANOTECH.LEVEL_46,
    RAC3NANOTECH.LEVEL_47,
    RAC3NANOTECH.LEVEL_48,
    RAC3NANOTECH.LEVEL_49,
    RAC3NANOTECH.LEVEL_50,
    RAC3NANOTECH.LEVEL_51,
    RAC3NANOTECH.LEVEL_52,
    RAC3NANOTECH.LEVEL_53,
    RAC3NANOTECH.LEVEL_54,
    RAC3NANOTECH.LEVEL_55,
    RAC3NANOTECH.LEVEL_56,
    RAC3NANOTECH.LEVEL_57,
    RAC3NANOTECH.LEVEL_58,
    RAC3NANOTECH.LEVEL_59,
    RAC3NANOTECH.LEVEL_60,
    RAC3NANOTECH.LEVEL_61,
    RAC3NANOTECH.LEVEL_62,
    RAC3NANOTECH.LEVEL_63,
    RAC3NANOTECH.LEVEL_64,
    RAC3NANOTECH.LEVEL_65,
    RAC3NANOTECH.LEVEL_66,
    RAC3NANOTECH.LEVEL_67,
    RAC3NANOTECH.LEVEL_68,
    RAC3NANOTECH.LEVEL_69,
    RAC3NANOTECH.LEVEL_70,
    RAC3NANOTECH.LEVEL_71,
    RAC3NANOTECH.LEVEL_72,
    RAC3NANOTECH.LEVEL_73,
    RAC3NANOTECH.LEVEL_74,
    RAC3NANOTECH.LEVEL_75,
    RAC3NANOTECH.LEVEL_76,
    RAC3NANOTECH.LEVEL_77,
    RAC3NANOTECH.LEVEL_78,
    RAC3NANOTECH.LEVEL_79,
    RAC3NANOTECH.LEVEL_80,
    RAC3NANOTECH.LEVEL_81,
    RAC3NANOTECH.LEVEL_82,
    RAC3NANOTECH.LEVEL_83,
    RAC3NANOTECH.LEVEL_84,
    RAC3NANOTECH.LEVEL_85,
    RAC3NANOTECH.LEVEL_86,
    RAC3NANOTECH.LEVEL_87,
    RAC3NANOTECH.LEVEL_88,
    RAC3NANOTECH.LEVEL_89,
    RAC3NANOTECH.LEVEL_90,
    RAC3NANOTECH.LEVEL_91,
    RAC3NANOTECH.LEVEL_92,
    RAC3NANOTECH.LEVEL_93,
    RAC3NANOTECH.LEVEL_94,
    RAC3NANOTECH.LEVEL_95,
    RAC3NANOTECH.LEVEL_96,
    RAC3NANOTECH.LEVEL_97,
    RAC3NANOTECH.LEVEL_98,
    RAC3NANOTECH.LEVEL_99,
    RAC3NANOTECH.LEVEL_100,
]
every_5_nanotech: list[str] = [
    RAC3NANOTECH.LEVEL_15,
    RAC3NANOTECH.LEVEL_20,
    RAC3NANOTECH.LEVEL_25,
    RAC3NANOTECH.LEVEL_30,
    RAC3NANOTECH.LEVEL_35,
    RAC3NANOTECH.LEVEL_40,
    RAC3NANOTECH.LEVEL_45,
    RAC3NANOTECH.LEVEL_50,
    RAC3NANOTECH.LEVEL_55,
    RAC3NANOTECH.LEVEL_60,
    RAC3NANOTECH.LEVEL_65,
    RAC3NANOTECH.LEVEL_70,
    RAC3NANOTECH.LEVEL_75,
    RAC3NANOTECH.LEVEL_80,
    RAC3NANOTECH.LEVEL_85,
    RAC3NANOTECH.LEVEL_90,
    RAC3NANOTECH.LEVEL_95,
    RAC3NANOTECH.LEVEL_100,
]
every_10_nanotech: list[str] = [
    RAC3NANOTECH.LEVEL_20,
    RAC3NANOTECH.LEVEL_30,
    RAC3NANOTECH.LEVEL_40,
    RAC3NANOTECH.LEVEL_50,
    RAC3NANOTECH.LEVEL_60,
    RAC3NANOTECH.LEVEL_70,
    RAC3NANOTECH.LEVEL_80,
    RAC3NANOTECH.LEVEL_90,
    RAC3NANOTECH.LEVEL_100,
]
every_20_nanotech: list[str] = [
    RAC3NANOTECH.LEVEL_20,
    RAC3NANOTECH.LEVEL_40,
    RAC3NANOTECH.LEVEL_60,
    RAC3NANOTECH.LEVEL_80,
    RAC3NANOTECH.LEVEL_100,
]

every_sewer_crystals: list[str] = [
    RAC3SEWER.TRADE_1,
    RAC3SEWER.TRADE_2,
    RAC3SEWER.TRADE_3,
    RAC3SEWER.TRADE_4,
    RAC3SEWER.TRADE_5,
    RAC3SEWER.TRADE_6,
    RAC3SEWER.TRADE_7,
    RAC3SEWER.TRADE_8,
    RAC3SEWER.TRADE_9,
    RAC3SEWER.TRADE_10,
    RAC3SEWER.TRADE_11,
    RAC3SEWER.TRADE_12,
    RAC3SEWER.TRADE_13,
    RAC3SEWER.TRADE_14,
    RAC3SEWER.TRADE_15,
    RAC3SEWER.TRADE_16,
    RAC3SEWER.TRADE_17,
    RAC3SEWER.TRADE_18,
    RAC3SEWER.TRADE_19,
    RAC3SEWER.TRADE_20,
    RAC3SEWER.TRADE_21,
    RAC3SEWER.TRADE_22,
    RAC3SEWER.TRADE_23,
    RAC3SEWER.TRADE_24,
    RAC3SEWER.TRADE_25,
    RAC3SEWER.TRADE_26,
    RAC3SEWER.TRADE_27,
    RAC3SEWER.TRADE_28,
    RAC3SEWER.TRADE_29,
    RAC3SEWER.TRADE_30,
    RAC3SEWER.TRADE_31,
    RAC3SEWER.TRADE_32,
    RAC3SEWER.TRADE_33,
    RAC3SEWER.TRADE_34,
    RAC3SEWER.TRADE_35,
    RAC3SEWER.TRADE_36,
    RAC3SEWER.TRADE_37,
    RAC3SEWER.TRADE_38,
    RAC3SEWER.TRADE_39,
    RAC3SEWER.TRADE_40,
    RAC3SEWER.TRADE_41,
    RAC3SEWER.TRADE_42,
    RAC3SEWER.TRADE_43,
    RAC3SEWER.TRADE_44,
    RAC3SEWER.TRADE_45,
    RAC3SEWER.TRADE_46,
    RAC3SEWER.TRADE_47,
    RAC3SEWER.TRADE_48,
    RAC3SEWER.TRADE_49,
    RAC3SEWER.TRADE_50,
    RAC3SEWER.TRADE_51,
    RAC3SEWER.TRADE_52,
    RAC3SEWER.TRADE_53,
    RAC3SEWER.TRADE_54,
    RAC3SEWER.TRADE_55,
    RAC3SEWER.TRADE_56,
    RAC3SEWER.TRADE_57,
    RAC3SEWER.TRADE_58,
    RAC3SEWER.TRADE_59,
    RAC3SEWER.TRADE_60,
    RAC3SEWER.TRADE_61,
    RAC3SEWER.TRADE_62,
    RAC3SEWER.TRADE_63,
    RAC3SEWER.TRADE_64,
    RAC3SEWER.TRADE_65,
    RAC3SEWER.TRADE_66,
    RAC3SEWER.TRADE_67,
    RAC3SEWER.TRADE_68,
    RAC3SEWER.TRADE_69,
    RAC3SEWER.TRADE_70,
    RAC3SEWER.TRADE_71,
    RAC3SEWER.TRADE_72,
    RAC3SEWER.TRADE_73,
    RAC3SEWER.TRADE_74,
    RAC3SEWER.TRADE_75,
    RAC3SEWER.TRADE_76,
    RAC3SEWER.TRADE_77,
    RAC3SEWER.TRADE_78,
    RAC3SEWER.TRADE_79,
    RAC3SEWER.TRADE_80,
    RAC3SEWER.TRADE_81,
    RAC3SEWER.TRADE_82,
    RAC3SEWER.TRADE_83,
    RAC3SEWER.TRADE_84,
    RAC3SEWER.TRADE_85,
    RAC3SEWER.TRADE_86,
    RAC3SEWER.TRADE_87,
    RAC3SEWER.TRADE_88,
    RAC3SEWER.TRADE_89,
    RAC3SEWER.TRADE_90,
    RAC3SEWER.TRADE_91,
    RAC3SEWER.TRADE_92,
    RAC3SEWER.TRADE_93,
    RAC3SEWER.TRADE_94,
    RAC3SEWER.TRADE_95,
    RAC3SEWER.TRADE_96,
    RAC3SEWER.TRADE_97,
    RAC3SEWER.TRADE_98,
    RAC3SEWER.TRADE_99,
    RAC3SKILLPOINT.SEWER_MOTHERLOAD,
]
every_5_sewer_crystals: list[str] = [
    RAC3SEWER.TRADE_5,
    RAC3SEWER.TRADE_10,
    RAC3SEWER.TRADE_15,
    RAC3SEWER.TRADE_20,
    RAC3SEWER.TRADE_25,
    RAC3SEWER.TRADE_30,
    RAC3SEWER.TRADE_35,
    RAC3SEWER.TRADE_40,
    RAC3SEWER.TRADE_45,
    RAC3SEWER.TRADE_50,
    RAC3SEWER.TRADE_55,
    RAC3SEWER.TRADE_60,
    RAC3SEWER.TRADE_65,
    RAC3SEWER.TRADE_70,
    RAC3SEWER.TRADE_75,
    RAC3SEWER.TRADE_80,
    RAC3SEWER.TRADE_85,
    RAC3SEWER.TRADE_90,
    RAC3SEWER.TRADE_95,
    RAC3SEWER.TRADE_99,
    RAC3SKILLPOINT.SEWER_MOTHERLOAD,
]
every_10_sewer_crystals: list[str] = [
    RAC3SEWER.TRADE_10,
    RAC3SEWER.TRADE_20,
    RAC3SEWER.TRADE_30,
    RAC3SEWER.TRADE_40,
    RAC3SEWER.TRADE_50,
    RAC3SEWER.TRADE_60,
    RAC3SEWER.TRADE_70,
    RAC3SEWER.TRADE_80,
    RAC3SEWER.TRADE_90,
    RAC3SEWER.TRADE_99,
    RAC3SKILLPOINT.SEWER_MOTHERLOAD,
]
every_20_sewer_crystals: list[str] = [
    RAC3SEWER.TRADE_20,
    RAC3SEWER.TRADE_40,
    RAC3SEWER.TRADE_60,
    RAC3SEWER.TRADE_80,
    RAC3SEWER.TRADE_99,
    RAC3SKILLPOINT.SEWER_MOTHERLOAD,
]

annihilation_nation_1: list[str] = [
    RAC3TBOLT.NATION_CLIFF,
    RAC3SKILLPOINT.NATION_CAMERA,
    RAC3SKILLPOINT.NATION_FLEE,
    RAC3LOCATION.NATION_TYHRRA_GUISE,
    RAC3LOCATION.NATION_GRAND_PRIZE_BOUT,
    RAC3LOCATION.NATION_THE_TERRIBLE_TWO,
    RAC3LOCATION.NATION_ROBOT_RAMPAGE,
    RAC3LOCATION.NATION_TWO_MINUTE_WARNING,
    RAC3LOCATION.NATION_90_SECONDS,
    RAC3LOCATION.NATION_ONSLAUGHT,
    RAC3LOCATION.NATION_WHIP_IT_GOOD,
    RAC3LOCATION.NATION_HYDRA_N_SEEK,
    RAC3LOCATION.NATION_CHAMPIONSHIP_BOUT,
    RAC3LOCATION.NATION_HEAT_STREET,
    RAC3LOCATION.NATION_CRISPY_CRITTER,
    RAC3LOCATION.NATION_PYRO_PLAYGROUND,
    RAC3LOCATION.NATION_SUICIDE_RUN,
]
annihilation_nation_2: list[str] = [
    RAC3TBOLT.NATION_CLIFF,
    RAC3SKILLPOINT.NATION_CAMERA,
    RAC3SKILLPOINT.NATION_FLEE,
    # These 3 are doable on the second part of the challenges as well
    RAC3SKILLPOINT.NATION_BASH,
    RAC3LOCATION.NATION_MEET_COURTNEY,
    RAC3LOCATION.NATION_INFOBOT_HOLOSTAR,
    RAC3LOCATION.NATION_NINJA_CHALLENGE,
    RAC3LOCATION.NATION_COUNTING_DUCKS,
    RAC3LOCATION.NATION_CYCLING_WEAPONS,
    RAC3LOCATION.NATION_ONE_HIT_WONDER,
    RAC3LOCATION.NATION_TIME_TO_SUCK,
    RAC3LOCATION.NATION_NAPTIME,
    RAC3LOCATION.NATION_MORE_CYCLING_WEAPONS,
    RAC3LOCATION.NATION_DODGE_THE_TWINS,
    RAC3LOCATION.NATION_CHOP_CHOP,
    RAC3LOCATION.NATION_SLEEP_INDUCER,
    RAC3LOCATION.NATION_THE_OTHER_WHITE_MEAT,
    RAC3LOCATION.NATION_CHAMPIONSHIP_BOUT_II,
    RAC3LOCATION.NATION_QWARKTASTIC_BATTLE,
    RAC3LOCATION.NATION_BBQ_BOULEVARD,
    RAC3LOCATION.NATION_MAZE_OF_BLAZE,
    RAC3TBOLT.NATION_PLATFORM,
    RAC3LOCATION.NATION_CREMATION_STATION,
    RAC3LOCATION.NATION_THE_ANNIHILATOR,
]

extra_ranger: list[str] = [
    RAC3LOCATION.TYHRRANOSIS_RANGERS_1,
    RAC3LOCATION.TYHRRANOSIS_RANGERS_2,
    RAC3LOCATION.TYHRRANOSIS_RANGERS_3,
    RAC3LOCATION.TYHRRANOSIS_RANGERS_4,
    RAC3TBOLT.METROPOLIS_RANGERS,
    RAC3LOCATION.METROPOLIS_RANGERS_1,
    RAC3LOCATION.METROPOLIS_RANGERS_2,
    RAC3LOCATION.METROPOLIS_RANGERS_3,
    RAC3LOCATION.METROPOLIS_RANGERS_4,
    RAC3LOCATION.METROPOLIS_RANGERS_5,
    RAC3LOCATION.METROPOLIS_MAP_O_MATIC,
]

veldin_weapons: list[str] = [
    RAC3LOCATION.VELDIN_FIRST_RANGER,
    RAC3LOCATION.VELDIN_SECOND_RANGER,
]


def create_regions(world: "RaC3World"):
    # ----- Introduction Sequence -----#
    menu = create_region(world, RAC3REGION.MENU)
    veldin = create_region_and_connect(world, RAC3REGION.VELDIN, f"{RAC3REGION.MENU} -> {RAC3REGION.VELDIN}", menu)
    florana = create_region(world, RAC3REGION.FLORANA)
    veldin.connect(florana, f"{RAC3REGION.VELDIN} -> {RAC3REGION.FLORANA}",
                   rule=lambda state: state.has(RAC3ITEM.FLORANA, world.player))
    starship_phoenix = create_region(world, RAC3REGION.STARSHIP_PHOENIX)
    florana.connect(starship_phoenix, f"{RAC3REGION.FLORANA} -> {RAC3REGION.STARSHIP_PHOENIX}",
                    rule=lambda state: state.has(RAC3ITEM.STARSHIP_PHOENIX, world.player))
    starship_phoenix.connect(florana, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.FLORANA}", )

    # ----- Regions within the game -----#
    marcadia = create_region(world, RAC3REGION.MARCADIA)
    annihilation_nation = create_region(world, RAC3REGION.ANNIHILATION_NATION)
    aquatos = create_region(world, RAC3REGION.AQUATOS)
    tyhrranosis = create_region(world, RAC3REGION.TYHRRANOSIS)
    daxx = create_region(world, RAC3REGION.DAXX)
    obani_gemini = create_region(world, RAC3REGION.OBANI_GEMINI)
    blackwater_city = create_region(world, RAC3REGION.BLACKWATER_CITY)
    holostar_studios = create_region(world, RAC3REGION.HOLOSTAR_STUDIOS)
    obani_draco = create_region(world, RAC3REGION.OBANI_DRACO)
    zeldrin_starport = create_region(world, RAC3REGION.ZELDRIN_STARPORT)
    metropolis_first_half = create_region(world, RAC3REGION.METROPOLIS)
    crash_site = create_region(world, RAC3REGION.CRASH_SITE)
    aridia = create_region(world, RAC3REGION.ARIDIA)
    qwarks_hideout = create_region(world, RAC3REGION.QWARKS_HIDEOUT)
    koros = create_region(world, RAC3REGION.KOROS)
    command_center = create_region(world, RAC3REGION.COMMAND_CENTER)  # Victory Location

    # ----- Connecting everything to Starship Phoenix -----#
    starship_phoenix.connect(marcadia, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.MARCADIA}")
    starship_phoenix.connect(annihilation_nation, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.ANNIHILATION_NATION}")
    starship_phoenix.connect(aquatos, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.AQUATOS}")
    starship_phoenix.connect(tyhrranosis, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.TYHRRANOSIS}")
    starship_phoenix.connect(daxx, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.DAXX}")
    starship_phoenix.connect(obani_gemini, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.OBANI_GEMINI}")
    starship_phoenix.connect(blackwater_city, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.BLACKWATER_CITY}")
    starship_phoenix.connect(holostar_studios, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.HOLOSTAR_STUDIOS}")
    starship_phoenix.connect(obani_draco, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.OBANI_DRACO}")
    starship_phoenix.connect(zeldrin_starport, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.ZELDRIN_STARPORT}")
    starship_phoenix.connect(metropolis_first_half, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.METROPOLIS}")
    starship_phoenix.connect(crash_site, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.CRASH_SITE}")
    starship_phoenix.connect(aridia, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.ARIDIA}")
    starship_phoenix.connect(qwarks_hideout, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.QWARKS_HIDEOUT}")
    starship_phoenix.connect(koros, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.KOROS}")
    starship_phoenix.connect(command_center, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.COMMAND_CENTER}")

    # ----- Split planet connections for gadget reasons -----#

    # This cutscene requires beating Holostar and Blackwater in any order:
    skidd_cutscene = create_region(world, RAC3REGION.SKIDD_CUTSCENE)
    holostar_studios.connect(skidd_cutscene,
                             rule=lambda state: state.can_reach(RAC3REGION.BLACKWATER_CITY, player=world.player))
    blackwater_city.connect(skidd_cutscene,
                            rule=lambda state: state.can_reach(RAC3REGION.HOLOSTAR_STUDIOS, player=world.player))

    # ----- Dummy regions for weapon upgrade organization -----#

    nanotech_levels = create_region(world, RAC3REGION.NANOTECH)
    menu.connect(nanotech_levels)

    # shock_blaster_upgrades = create_region(world, f"{RAC3ITEM.SHOCK_BLASTER} Upgrades")
    # menu.connect(shock_blaster_upgrades, rule=lambda state: state.has(RAC3ITEM.SHOCK_BLASTER, world.player)),
    #
    # nitro_launcher_upgrades = create_region(world, f"{RAC3ITEM.NITRO_LAUNCHER} Upgrades")
    # menu.connect(nitro_launcher_upgrades, rule=lambda state: state.has(RAC3ITEM.NITRO_LAUNCHER, world.player)),
    #
    # n60_storm_upgrades = create_region(world, f"{RAC3ITEM.N60_STORM} Upgrades")
    # menu.connect(n60_storm_upgrades, rule=lambda state: state.has(RAC3ITEM.N60_STORM, world.player)),
    #
    # plasma_whip_upgrades = create_region(world, f"{RAC3ITEM.PLASMA_WHIP} Upgrades")
    # menu.connect(plasma_whip_upgrades, rule=lambda state: state.has(RAC3ITEM.PLASMA_WHIP, world.player)),
    #
    # infector_upgrades = create_region(world, f"{RAC3ITEM.INFECTOR} Upgrades")
    # menu.connect(infector_upgrades, rule=lambda state: state.has(RAC3ITEM.INFECTOR, world.player)),
    #
    # suck_cannon_upgrades = create_region(world, f"{RAC3ITEM.SUCK_CANNON} Upgrades")
    # menu.connect(suck_cannon_upgrades, rule=lambda state: state.has(RAC3ITEM.SUCK_CANNON, world.player)),
    #
    # spitting_hydra_upgrades = create_region(world, f"{RAC3ITEM.SPITTING_HYDRA} Upgrades")
    # menu.connect(spitting_hydra_upgrades, rule=lambda state: state.has(RAC3ITEM.SPITTING_HYDRA, world.player)),
    #
    # agents_of_doom_upgrades = create_region(world, f"{RAC3ITEM.AGENTS_OF_DOOM} Upgrades")
    # menu.connect(agents_of_doom_upgrades, rule=lambda state: state.has(RAC3ITEM.AGENTS_OF_DOOM, world.player)),
    #
    # flux_rifle_upgrades = create_region(world, f"{RAC3ITEM.FLUX_RIFLE} Upgrades")
    # menu.connect(flux_rifle_upgrades, rule=lambda state: state.has(RAC3ITEM.FLUX_RIFLE, world.player)),
    #
    # annihilator_upgrades = create_region(world, f"{RAC3ITEM.ANNIHILATOR} Upgrades")
    # menu.connect(annihilator_upgrades, rule=lambda state: state.has(RAC3ITEM.ANNIHILATOR, world.player)),
    #
    # holo_shield_glove_upgrades = create_region(world, f"{RAC3ITEM.HOLO_SHIELD} Upgrades")
    # menu.connect(holo_shield_glove_upgrades, rule=lambda state: state.has(RAC3ITEM.HOLO_SHIELD, world.player)),
    #
    # disc_blade_gun_upgrades = create_region(world, f"{RAC3ITEM.DISC_BLADE} Upgrades")
    # menu.connect(disc_blade_gun_upgrades, rule=lambda state: state.has(RAC3ITEM.DISC_BLADE, world.player)),
    #
    # rift_inducer_upgrades = create_region(world, f"{RAC3ITEM.RIFT_INDUCER} Upgrades")
    # menu.connect(rift_inducer_upgrades, rule=lambda state: state.has(RAC3ITEM.RIFT_INDUCER, world.player)),
    #
    # qwack_o_ray_upgrades = create_region(world, f"{RAC3ITEM.QWACK_O_RAY} Upgrades")
    # menu.connect(qwack_o_ray_upgrades, rule=lambda state: state.has(RAC3ITEM.QWACK_O_RAY, world.player)),
    #
    # ry3no_upgrades = create_region(world, f"{RAC3ITEM.RY3N0} Upgrades")
    # menu.connect(ry3no_upgrades, rule=lambda state: state.has(RAC3ITEM.RY3N0, world.player)),
    #
    # mega_turret_glove_upgrades = create_region(world, f"{RAC3ITEM.MINI_TURRET} Upgrades")
    # menu.connect(mega_turret_glove_upgrades, rule=lambda state: state.has(RAC3ITEM.MINI_TURRET, world.player)),
    #
    # lava_gun_upgrades = create_region(world, f"{RAC3ITEM.LAVA_GUN} Upgrades")
    # menu.connect(lava_gun_upgrades, rule=lambda state: state.has(RAC3ITEM.LAVA_GUN, world.player)),
    #
    # tesla_barrier_upgrades = create_region(world, f"{RAC3ITEM.SHIELD_CHARGER} Upgrades")
    # menu.connect(tesla_barrier_upgrades, rule=lambda state: state.has(RAC3ITEM.SHIELD_CHARGER, world.player)),
    #
    # bouncer_upgrades = create_region(world, f"{RAC3ITEM.BOUNCER} Upgrades")
    # menu.connect(bouncer_upgrades, rule=lambda state: state.has(RAC3ITEM.BOUNCER, world.player)),
    #
    # plasma_coil_upgrades = create_region(world, f"{RAC3ITEM.PLASMA_COIL} Upgrades")
    # menu.connect(plasma_coil_upgrades, rule=lambda state: state.has(RAC3ITEM.PLASMA_COIL, world.player))


def create_region(world: "RaC3World", name: str) -> Region:
    reg = Region(name, world.player, world.multiworld)
    options = world.options
    for key, data in RAC3_LOCATION_DATA_TABLE.items():
        if data.REGION == name and not should_skip_location(data, options):
            location = GameLocation(world.player, key, data.AP_CODE, reg)
            reg.locations.append(location)

    world.multiworld.regions.append(reg)
    return reg


def create_region_and_connect(world: "RaC3World", name: str, entrance_name: str, connected_region: Region) -> Region:
    reg: Region = create_region(world, name)
    connected_region.connect(reg, entrance_name)
    return reg


def should_skip_location(data: RAC3LOCATIONDATA, options: type[RaC3Options]) -> bool:
    """Return False if the location should be skipped based on options."""
    all_skill_points = all(options.skill_points.values())
    loc = LOCATION_FROM_AP_CODE[data.AP_CODE]
    for tag in data.TAGS:
        match tag:
            case RAC3TAG.UNSTABLE:  # Skip all unstable locations
                return True
            case RAC3TAG.TROPHY:
                if not options.trophies.value:  # Skip trophy locations if trophies are disabled
                    return True
            case RAC3TAG.LONG_TROPHY:
                if options.trophies.value < 2:  # Skip long term trophies if not set to every trophy
                    return True
                elif not all_skill_points and loc == RAC3TROPHY.PHOENIX_SKILL_MASTER:
                    return True
            case RAC3TAG.SKILLPOINT:
                if not options.skill_points[SKILLPOINT_LOCATION_TO_NAME[loc]]:
                    return True  # Skips the skill points which the player didn't choose
            case RAC3TAG.T_BOLT:
                if options.titanium_bolts.value == 0:
                    return True  # Skip titanium bolt locations if titanium bolt option is disabled
            case RAC3TAG.NANOTECH:
                if loc in every_nanotech[options.nanotech_limitation.value - 10::]:
                    return True  # Place nanotech milestone amount specified in nanotech_limitation
                if options.nanotech_milestones.value == 0:
                    return True  # Skip nanotech milestone locations if nanotech milestones option is disabled
                elif options.nanotech_milestones.value == 1 and loc not in every_20_nanotech:
                    return True  # Skips nanotech milestones that are not in every 20
                elif options.nanotech_milestones.value == 2 and loc not in every_10_nanotech:
                    return True  # Skips nanotech milestones that are not in every 10
                elif options.nanotech_milestones.value == 3 and loc not in every_5_nanotech:
                    return True  # Skips nanotech milestones that are not in every 5
            case RAC3TAG.RANGERS:
                if options.rangers.value == 0:
                    return True  # Skips ranger missions locations if rangers option is none
                elif options.rangers.value == 1 and loc in extra_ranger:
                    return True  # Skips optional ranger missions locations if set to story_missions
                elif options.rangers.value == 2 and loc not in extra_ranger:
                    return True  # Skips story ranger missions locations if set to optional_missions
            case RAC3TAG.ARENA:
                if options.arena.value == 0:
                    return True  # Skips arena challenges locations if arena option is none
                elif options.arena.value == 1 and loc not in annihilation_nation_1:
                    return True  # Skips AN2 challenge locations if arena option is set to first_only
                elif options.arena.value == 2 and loc not in annihilation_nation_2:
                    return True  # Skips AN1 challenge locations if arena option is set to second_only
            case RAC3TAG.VIDCOMIC:
                if options.vidcomics.value == 0:
                    return True  # Skips vidcomic locations if vidcomics option is disabled
            case RAC3TAG.VR:
                if options.vr_challenges.value == 0:
                    return True  # Skips vr challenges locations if vr_challenges option is disabled
            case RAC3TAG.SEWER:
                if loc in every_sewer_crystals[options.sewer_limitation.value::]:
                    return True  # Place sewer crystal amount specified in sewer_limitations
                elif options.sewer_crystals.value == 0:
                    return True  # Skip sewer crystal locations if sewer crystals option is disabled
                elif options.sewer_crystals.value == 1 and loc not in every_20_sewer_crystals:
                    return True  # Skip sewer crystal locations that are not in every 20
                elif options.sewer_crystals.value == 2 and loc not in every_10_sewer_crystals:
                    return True  # Skip sewer crystal locations that are not in every 10
                elif options.sewer_crystals.value == 3 and loc not in every_5_sewer_crystals:
                    return True  # Skip sewer crystal locations that are not in every 5
            case RAC3TAG.WEAPONS:
                if options.weapon_vendors.value == 0 and loc not in veldin_weapons:
                    return True  # Skips every weapon vendor checks except the Veldin ones
            # Add more conditions here if needed in the future
            case RAC3TAG.ONE_HP_UNSTABLE:
                if options.one_hp_challenge.value[RAC3PLAYERTYPE.RATCHET]:
                    return True  # Skip all unstable locations in One HP Challenge
    return False
