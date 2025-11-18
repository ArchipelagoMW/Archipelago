from typing import TYPE_CHECKING

from BaseClasses import Location, Region
from constants.locations.Rac3Skillpoints import SIMPLE_SKILL_POINTS
from constants.Rac3Items import RAC3ITEM
from constants.Rac3Options import RAC3OPTION
from constants.Rac3Region import RAC3REGION
from Locations import location_table

if TYPE_CHECKING:
    from worlds.rac3 import RaC3World


class GameLocation(Location):
    game = RAC3OPTION.GAME_TITLE_FULL


# Making an array with every 5 nanotech
every_5_nanotech = [f"Nanotech Milestone: {x}" for x in range(15, 101, 5)]

# Making an array with every 10 nanotech
every_10_nanotech = [f"Nanotech Milestone: {x}" for x in range(20, 101, 10)]

# Making an array with every 20 nanotech
every_20_nanotech = [f"Nanotech Milestone: {x}" for x in range(20, 101, 20)]


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
    starship_phoenix.connect(obani_draco, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.HOLOSTAR_STUDIOS}")
    starship_phoenix.connect(holostar_studios, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.OBANI_DRACO}")
    starship_phoenix.connect(zeldrin_starport, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.ZELDRIN_STARPORT}")
    starship_phoenix.connect(metropolis_first_half, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.METROPOLIS}")
    starship_phoenix.connect(crash_site, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.CRASH_SITE}")
    starship_phoenix.connect(aridia, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.ARIDIA}")
    starship_phoenix.connect(qwarks_hideout, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.QWARKS_HIDEOUT}")
    starship_phoenix.connect(koros, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.KOROS}")
    starship_phoenix.connect(command_center, f"{RAC3REGION.STARSHIP_PHOENIX} -> {RAC3REGION.COMMAND_CENTER}")

    # ----- Split planet connections for gadget reasons -----#

    # Annihilation mission is shown after Daxx Region2
    annihilation_nation_second_half = create_region(world, RAC3REGION.ANNIHILATION_NATION_2)
    annihilation_nation.connect(annihilation_nation_second_half,
                                rule=lambda state: state.can_reach_location("Daxx: Gunship", player=world.player)),

    aquatos_sewers = create_region(world, RAC3REGION.AQUATOS_SEWERS)
    aquatos.connect(aquatos_sewers, rule=lambda state: state.can_reach(RAC3REGION.AQUATOS, player=world.player)),

    tyhrranosis_second_half = create_region(world, RAC3REGION.TYHRRANOSIS_RANGERS)
    tyhrranosis.connect(tyhrranosis_second_half,
                        rule=lambda state: state.can_reach(RAC3REGION.TYHRRANOSIS, player=world.player)),

    # This cutscene requires beating Holostar and Blackwater in any order:
    skidd_cutscene = create_region(world, RAC3REGION.SKIDD_CUTSCENE)
    holostar_studios.connect(skidd_cutscene,
                             rule=lambda state: state.can_reach(RAC3REGION.BLACKWATER_CITY, player=world.player))
    blackwater_city.connect(skidd_cutscene,
                            rule=lambda state: state.can_reach(RAC3REGION.HOLOSTAR_STUDIOS, player=world.player))

    # You can get Metal-Noids in metropolis with no other requirements
    metropolis_second_half = create_region(world, RAC3REGION.METROPOLIS_RANGERS)
    metropolis_first_half.connect(metropolis_second_half,
                                  rule=lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player)
                                                     and state.has(RAC3ITEM.REFRACTOR, world.player)),

    # ----- Dummy regions for weapon upgrade organization -----#

    nanotech_levels = create_region(world, "Nanotech Levels")
    menu.connect(nanotech_levels)

    shock_blaster_upgrades = create_region(world, f"{RAC3ITEM.SHOCK_BLASTER} Upgrades")
    menu.connect(shock_blaster_upgrades, rule=lambda state: state.has(RAC3ITEM.SHOCK_BLASTER, world.player)),

    nitro_launcher_upgrades = create_region(world, f"{RAC3ITEM.NITRO_LAUNCHER} Upgrades")
    menu.connect(nitro_launcher_upgrades, rule=lambda state: state.has(RAC3ITEM.NITRO_LAUNCHER, world.player)),

    n60_storm_upgrades = create_region(world, f"{RAC3ITEM.N60_STORM} Upgrades")
    menu.connect(n60_storm_upgrades, rule=lambda state: state.has(RAC3ITEM.N60_STORM, world.player)),

    plasma_whip_upgrades = create_region(world, f"{RAC3ITEM.PLASMA_WHIP} Upgrades")
    menu.connect(plasma_whip_upgrades, rule=lambda state: state.has(RAC3ITEM.PLASMA_WHIP, world.player)),

    infector_upgrades = create_region(world, f"{RAC3ITEM.INFECTOR} Upgrades")
    menu.connect(infector_upgrades, rule=lambda state: state.has(RAC3ITEM.INFECTOR, world.player)),

    suck_cannon_upgrades = create_region(world, f"{RAC3ITEM.SUCK_CANNON} Upgrades")
    menu.connect(suck_cannon_upgrades, rule=lambda state: state.has(RAC3ITEM.SUCK_CANNON, world.player)),

    spitting_hydra_upgrades = create_region(world, f"{RAC3ITEM.SPITTING_HYDRA} Upgrades")
    menu.connect(spitting_hydra_upgrades, rule=lambda state: state.has(RAC3ITEM.SPITTING_HYDRA, world.player)),

    agents_of_doom_upgrades = create_region(world, f"{RAC3ITEM.AGENTS_OF_DOOM} Upgrades")
    menu.connect(agents_of_doom_upgrades, rule=lambda state: state.has(RAC3ITEM.AGENTS_OF_DOOM, world.player)),

    flux_rifle_upgrades = create_region(world, f"{RAC3ITEM.FLUX_RIFLE} Upgrades")
    menu.connect(flux_rifle_upgrades, rule=lambda state: state.has(RAC3ITEM.FLUX_RIFLE, world.player)),

    annihilator_upgrades = create_region(world, f"{RAC3ITEM.ANNIHILATOR} Upgrades")
    menu.connect(annihilator_upgrades, rule=lambda state: state.has(RAC3ITEM.ANNIHILATOR, world.player)),

    holo_shield_glove_upgrades = create_region(world, f"{RAC3ITEM.HOLO_SHIELD} Upgrades")
    menu.connect(holo_shield_glove_upgrades, rule=lambda state: state.has(RAC3ITEM.HOLO_SHIELD, world.player)),

    disc_blade_gun_upgrades = create_region(world, f"{RAC3ITEM.DISC_BLADE} Upgrades")
    menu.connect(disc_blade_gun_upgrades, rule=lambda state: state.has(RAC3ITEM.DISC_BLADE, world.player)),

    rift_inducer_upgrades = create_region(world, f"{RAC3ITEM.RIFT_INDUCER} Upgrades")
    menu.connect(rift_inducer_upgrades, rule=lambda state: state.has(RAC3ITEM.RIFT_INDUCER, world.player)),

    qwack_o_ray_upgrades = create_region(world, f"{RAC3ITEM.QWACK_O_RAY} Upgrades")
    menu.connect(qwack_o_ray_upgrades, rule=lambda state: state.has(RAC3ITEM.QWACK_O_RAY, world.player)),

    ry3no_upgrades = create_region(world, f"{RAC3ITEM.RY3N0} Upgrades")
    menu.connect(ry3no_upgrades, rule=lambda state: state.has(RAC3ITEM.RY3N0, world.player)),

    mega_turret_glove_upgrades = create_region(world, f"{RAC3ITEM.MINI_TURRET} Upgrades")
    menu.connect(mega_turret_glove_upgrades, rule=lambda state: state.has(RAC3ITEM.MINI_TURRET, world.player)),

    lava_gun_upgrades = create_region(world, f"{RAC3ITEM.LAVA_GUN} Upgrades")
    menu.connect(lava_gun_upgrades, rule=lambda state: state.has(RAC3ITEM.LAVA_GUN, world.player)),

    tesla_barrier_upgrades = create_region(world, f"{RAC3ITEM.SHIELD_CHARGER} Upgrades")
    menu.connect(tesla_barrier_upgrades, rule=lambda state: state.has(RAC3ITEM.SHIELD_CHARGER, world.player)),

    bouncer_upgrades = create_region(world, f"{RAC3ITEM.BOUNCER} Upgrades")
    menu.connect(bouncer_upgrades, rule=lambda state: state.has(RAC3ITEM.BOUNCER, world.player)),

    plasma_coil_upgrades = create_region(world, f"{RAC3ITEM.PLASMA_COIL} Upgrades")
    menu.connect(plasma_coil_upgrades, rule=lambda state: state.has(RAC3ITEM.PLASMA_COIL, world.player))

    # ----- Long Term Trophy Dummy Regions ----- #
    if world.options.trophies.value == 2:
        long_term_trophy = create_region(world, RAC3REGION.LONG_TROPHIES)
        menu.connect(long_term_trophy,
                     rule=lambda state: state.can_reach(RAC3REGION.STARSHIP_PHOENIX, player=world.player))


def create_region(world: "RaC3World", name: str) -> Region:
    reg = Region(name, world.player, world.multiworld)
    options = world.options
    for (key, data) in location_table.items():
        if should_skip_location(key, options):  # Skip locations based on options
            continue

        if data.region == name:
            location = GameLocation(world.player, key, data.ap_code, reg)
            reg.locations.append(location)

    world.multiworld.regions.append(reg)
    return reg


def create_region_and_connect(world: "RaC3World",
                              name: str, entrance_name: str, connected_region: Region) -> Region:
    reg: Region = create_region(world, name)
    connected_region.connect(reg, entrance_name)
    return reg


def should_skip_location(key: str, options) -> bool:
    """Return False if the location should be skipped based on options."""

    # Skip trophy locations if trophies are disabled
    if "Trophy" in key and options.trophies.value == 0:
        return True

        # Skip long term trophies if not set to every trophy
    if "Long Term" in key and options.trophies.value < 2:
        return True

        # Skip skill point locations if not set to every skill point
    if "Skill Point" in key and options.skill_points.value == 0:
        return True

        # Skip skill points not in the simple list
    if "Skill Point" in key and options.skill_points.value == 1:
        for simple_skill in SIMPLE_SKILL_POINTS:
            if simple_skill.lower() in key.lower():
                return False
        return True

        # Skip titanium bolt locations if titanium bolt option is disabled
    if "T-Bolt" in key and options.titanium_bolts.value == 0:
        return True

        # Skip nanotech milestone locations if nanotech milestones option is disabled
    if "Nanotech Milestone" in key and options.nanotech_milestones.value == 0:
        return True

        # Skips nanotech milestones that are not in every 5
    if "Nanotech Milestone" in key and options.nanotech_milestones.value == 1:
        for every_5 in every_5_nanotech:
            if every_5.lower() in key.lower():
                return False
        return True

        # Skips nanotech milestones that are not in every 10
    if "Nanotech Milestone" in key and options.nanotech_milestones.value == 2:
        for every_10 in every_10_nanotech:
            if every_10.lower() in key.lower():
                return False
        return True

        # Skips nanotech milestones that are not in every 20
    if "Nanotech Milestone" in key and options.nanotech_milestones.value == 3:
        for every_20 in every_20_nanotech:
            if every_20.lower() in key.lower():
                return False
        return True

    # Add more conditions here if needed in the future

    return False
