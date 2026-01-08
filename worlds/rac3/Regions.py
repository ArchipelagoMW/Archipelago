from BaseClasses import Region
from typing import TYPE_CHECKING
from .Types import GameLocation
from .Locations import location_table

if TYPE_CHECKING:
    from . import RaC3World

# TODO: move to constants file once Myth is done with that
SIMPLE_SKILL_POINTS = [
    "Stay squeaky clean",
    "Beat Helga's Best VR Time",
    "Reflect on how to score",
    "Flee Flawlessly",
    "Lights, camera action!",
    "Search for sunken treasure",
    "Be a sharpshooter",
    "Bugs to Birdie",
    "Get to the belt",
    "Feeling Lucky?",
    "2002 was a good year in the city",
    "Aim High",
    "Go for hang time",
    "You break it, you win it",
    "Break the Dan"
]

#Making an array with every 5 nanotech
every_5_nanotech = [f"Nanotech Milestone: {x}" for x in range(15,101,5)]

#Making an array with every 10 nanotech
every_10_nanotech = [f"Nanotech Milestone: {x}" for x in range(20,101,10)]

#Making an array with every 20 nanotech
every_20_nanotech = [f"Nanotech Milestone: {x}" for x in range(20,101,20)]

def create_regions(world: "RaC3World"):
    # ----- Introduction Sequence -----#
    menu = create_region(world, "Menu")
    veldin = create_region_and_connect(world, "Veldin", "Menu -> Veldin", menu)
    florana = create_region(world, "Florana")
    veldin.connect(florana, "Veldin -> Florana", rule=lambda state: state.has("Infobot: Florana", world.player))
    starship_phoenix = create_region(world, "Starship Phoenix")
    florana.connect(starship_phoenix, "Florana -> Starship Phoenix",
                    rule=lambda state: state.has("Infobot: Starship Phoenix", world.player))
    starship_phoenix.connect(florana, "Starship Phoenix -> Florana")

    # ----- Regions within the game -----#
    marcadia = create_region(world, "Marcadia")
    annihilation_nation = create_region(world, "Annihilation Nation")
    aquatos = create_region(world, "Aquatos")
    tyhrranosis = create_region(world, "Tyhrranosis")
    daxx = create_region(world, "Daxx")
    obani_gemini = create_region(world, "Obani Gemini")
    blackwater_city = create_region(world, "Blackwater City")
    holostar_studios = create_region(world, "Holostar Studios")
    obani_draco = create_region(world, "Obani Draco")
    zeldrin_starport = create_region(world, "Zeldrin Starport")
    metropolis_first_half = create_region(world, "Metropolis Region 1")
    crash_site = create_region(world, "Crash Site")
    aridia = create_region(world, "Aridia")
    qwarks_hideout = create_region(world, "Qwarks Hideout")
    koros = create_region(world, "Koros")
    command_center = create_region(world, "Command Center")  # Victory Location

    # ----- Connecting everything to Starship Phoenix -----#
    starship_phoenix.connect(marcadia, "Starship Phoenix -> Marcadia")
    starship_phoenix.connect(annihilation_nation, "Starship Phoenix -> Annihilation Nation")
    starship_phoenix.connect(aquatos, "Starship Phoenix -> Aquatos")
    starship_phoenix.connect(tyhrranosis, "Starship Phoenix -> Tyhrranosis")
    starship_phoenix.connect(daxx, "Starship Phoenix -> Daxx")
    starship_phoenix.connect(obani_gemini, "Starship Phoenix -> Obani Gemini")
    starship_phoenix.connect(blackwater_city, "Starship Phoenix -> Blackwater City")
    starship_phoenix.connect(obani_draco, "Starship Phoenix -> Obani Draco")
    starship_phoenix.connect(holostar_studios, "Starship Phoenix -> Holostar Studios")
    starship_phoenix.connect(zeldrin_starport, "Starship Phoenix -> Zeldrin Starport")
    starship_phoenix.connect(metropolis_first_half, "Starship Phoenix -> Metropolis")
    starship_phoenix.connect(crash_site, "Starship Phoenix -> Crash Site")
    starship_phoenix.connect(aridia, "Starship Phoenix -> Aridia")
    starship_phoenix.connect(qwarks_hideout, "Starship Phoenix -> Qwarks Hideout")
    starship_phoenix.connect(koros, "Starship Phoenix -> Koros")
    starship_phoenix.connect(command_center, "Starship Phoenix -> Command Center")

    # ----- Split planet connections for gadget reasons -----#

    # Annihilation mission is shown after Daxx Region2
    annihilation_nation_second_half = create_region(world, "Annihilation Nation 2")
    annihilation_nation.connect(annihilation_nation_second_half,
                                rule=lambda state: state.can_reach_location("Daxx: Gunship", player=world.player)),

    tyhrranosis_second_half = create_region(world, "Tyhrranosis Region 2")
    tyhrranosis.connect(tyhrranosis_second_half,
                        rule=lambda state: state.can_reach("Tyhrranosis", player=world.player)),

    # This cutscene requires beating Holostar and Blackwater in any order:
    skidd_cutscene = create_region(world, "Skidd Cutscene")
    holostar_studios.connect(skidd_cutscene, rule=lambda state: state.can_reach("Blackwater City", player=world.player))
    blackwater_city.connect(skidd_cutscene, rule=lambda state: state.can_reach("Holostar Studios", player=world.player))

    # You can get Metal-Noids in metropolis with no other requirements
    metropolis_second_half = create_region(world, "Metropolis Region 2")
    metropolis_first_half.connect(metropolis_second_half,
                                  rule=lambda state: state.has("Gravity-Boots", world.player)
                                                     and state.has("Refractor", world.player)),

    # ----- Dummy regions for weapon upgrade organization -----#

    nanotech_levels = create_region(world, "Nanotech Levels")
    menu.connect(nanotech_levels)

    shock_blaster_upgrades = create_region(world, "Shock Blaster Upgrades")
    menu.connect(shock_blaster_upgrades, rule=lambda state: state.has("Shock Blaster", world.player)),

    nitro_launcher_upgrades = create_region(world, "Nitro Launcher Upgrades")
    menu.connect(nitro_launcher_upgrades, rule=lambda state: state.has("Nitro Launcher", world.player)),

    n60_storm_upgrades = create_region(world, "N60 Storm Upgrades")
    menu.connect(n60_storm_upgrades, rule=lambda state: state.has("N60 Storm", world.player)),

    plasma_whip_upgrades = create_region(world, "Plasma Whip Upgrades")
    menu.connect(plasma_whip_upgrades, rule=lambda state: state.has("Plasma Whip", world.player)),

    infector_upgrades = create_region(world, "Infector Upgrades")
    menu.connect(infector_upgrades, rule=lambda state: state.has("Infector", world.player)),

    suck_cannon_upgrades = create_region(world, "Suck Cannon Upgrades")
    menu.connect(suck_cannon_upgrades, rule=lambda state: state.has("Suck Cannon", world.player)),

    spitting_hydra_upgrades = create_region(world, "Spitting Hydra Upgrades")
    menu.connect(spitting_hydra_upgrades, rule=lambda state: state.has("Spitting Hydra", world.player)),

    agents_of_doom_upgrades = create_region(world, "Agents of Doom Upgrades")
    menu.connect(agents_of_doom_upgrades, rule=lambda state: state.has("Agents of Doom", world.player)),

    flux_rifle_upgrades = create_region(world, "Flux Rifle Upgrades")
    menu.connect(flux_rifle_upgrades, rule=lambda state: state.has("Flux Rifle", world.player)),

    annihilator_upgrades = create_region(world, "Annihilator Upgrades")
    menu.connect(annihilator_upgrades, rule=lambda state: state.has("Annihilator", world.player)),

    holo_shield_glove_upgrades = create_region(world, "Holo-Shield Glove Upgrades")
    menu.connect(holo_shield_glove_upgrades, rule=lambda state: state.has("Holo-Shield Glove", world.player)),

    disk_blade_gun_upgrades = create_region(world, "Disk-Blade Gun Upgrades")
    menu.connect(disk_blade_gun_upgrades, rule=lambda state: state.has("Disk-Blade Gun", world.player)),

    rift_inducer_upgrades = create_region(world, "Rift Inducer Upgrades")
    menu.connect(rift_inducer_upgrades, rule=lambda state: state.has("Rift Inducer", world.player)),

    qwack_o_ray_upgrades = create_region(world, "Qwack-O-Ray Upgrades")
    menu.connect(qwack_o_ray_upgrades, rule=lambda state: state.has("Qwack-O-Ray", world.player)),

    ry3no_upgrades = create_region(world, "RY3N0 Upgrades")
    menu.connect(ry3no_upgrades, rule=lambda state: state.has("RY3N0", world.player)),

    mega_turret_glove_upgrades = create_region(world, "Mini-Turret Glove Upgrades")
    menu.connect(mega_turret_glove_upgrades, rule=lambda state: state.has("Mini-Turret Glove", world.player)),

    lava_gun_upgrades = create_region(world, "Lava Gun Upgrades")
    menu.connect(lava_gun_upgrades, rule=lambda state: state.has("Lava Gun", world.player)),

    tesla_barrier_upgrades = create_region(world, "Shield Charger Upgrades")
    menu.connect(tesla_barrier_upgrades, rule=lambda state: state.has("Shield Charger", world.player)),

    bouncer_upgrades = create_region(world, "Bouncer Upgrades")
    menu.connect(bouncer_upgrades, rule=lambda state: state.has("Bouncer", world.player)),

    plasma_coil_upgrades = create_region(world, "Plasma Coil Upgrades")
    menu.connect(plasma_coil_upgrades, rule=lambda state: state.has("Plasma Coil", world.player))

    # ----- Long Term Trophy Dummy Regions ----- #
    if world.options.trophies.value == 2:
        long_term_trophy = create_region(world, "Long Term Trophy")
        menu.connect(long_term_trophy, rule=lambda state: state.can_reach("Starship Phoenix", player=world.player))


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
    
        #Skips nanotech milestones that are not in every 5
    if "Nanotech Milestone" in key and options.nanotech_milestones.value == 1:
        for every_5 in every_5_nanotech:
            if every_5.lower() in key.lower():
                return False
        return True
    
        #Skips nanotech milestones that are not in every 10
    if "Nanotech Milestone" in key and options.nanotech_milestones.value == 2:
        for every_10 in every_10_nanotech:
            if every_10.lower() in key.lower():
                return False
        return True
    
        #Skips nanotech milestones that are not in every 20
    if "Nanotech Milestone" in key and options.nanotech_milestones.value == 3:
        for every_20 in every_20_nanotech:
            if every_20.lower() in key.lower():
                return False
        return True


    # Add more conditions here if needed in the future

    return False
