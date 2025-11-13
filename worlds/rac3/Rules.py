from logging import DEBUG, getLogger
from typing import Callable, TYPE_CHECKING

from constants.data.Rac3ItemData import planet_data
from constants.Rac3Items import RAC3ITEM
from constants.Rac3Options import RAC3OPTION
from constants.Rac3Region import RAC3REGION
from worlds.generic.Rules import add_rule

if TYPE_CHECKING:
    from worlds.rac3 import RaC3World

rac3_logger = getLogger(RAC3OPTION.GAME_TITLE_FULL)
rac3_logger.setLevel(DEBUG)


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
    # ----- Planet Veldin -----# # Nothing
    # ----- Planet Florana -----# # Nothing

    # ----- Starship Phoenix -----#
    # "Phoenix: Received Suck Cannon": LocData(, "Starship Phoenix"),
    # "Phoenix: Received Infector": LocData(, "Starship Phoenix"),
    #  add_rule(world.get_location("Phoenix: T-Bolt: VR Nerves of Titanium"), None)

    rules_dict: dict[str, Callable] = {

        "Phoenix: Received Adamantine Armor":
            lambda state: state.can_reach(RAC3REGION.AQUATOS, player=world.player),
        "Phoenix: Received Aegis Mark V Armor":
            lambda state: state.can_reach("Zeldrin Starport", player=world.player),
        "Phoenix: Received Infernox Armor":
            lambda state: state.can_reach("Koros", player=world.player),
        "Phoenix: Received Hacker":
            lambda state: state.can_reach("Tyhrranosis", player=world.player)
                          and state.has_all([RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT], player=world.player),
        "Phoenix: Received Hypershot":
            lambda state: state.can_reach("Tyhrranosis", player=world.player)
                          and state.has_all([RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT], player=world.player),
        # "Phoenix: Meet Sasha on the Bridge": LocData(, "Starship Phoenix":
        "Phoenix: Return after winning Grand Prize Bout":
            lambda state: state.can_reach("Annihilation Nation", player=world.player),
        "Phoenix: Deliver the Star Map to Qwark":
            lambda state: state.has(RAC3ITEM.STAR_MAP, player=world.player),
        "Phoenix: VR Training after Noid Queen":
            lambda state: state.can_reach("Tyhrranosis", player=world.player)
                          and state.has_all([RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT], player=world.player),
        "Phoenix: Post Hideout Assault":
            lambda state: state.can_reach("Qwarks Hideout", player=world.player)
                          and state.has_all([RAC3ITEM.WARP_PAD, RAC3ITEM.HYPERSHOT], world.player),
        "Phoenix: Give Al the Master Plan":
            lambda state: state.has(RAC3ITEM.MASTER_PLAN, player=world.player),
        # VidComic clear locations
        "Phoenix: Play VidComic 1":
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 1),
        "Phoenix: Qwark VidComic 1 Clear":
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 1),
        "Phoenix: Qwark VidComic 2 Clear":
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 2),
        "Phoenix: Qwark VidComic 3 Clear":
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 3),
        "Phoenix: Play VidComic 4":
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 4),
        "Phoenix: Qwark VidComic 4 Clear":
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 4),
        "Phoenix: Play VidComic 5":
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 5),
        "Phoenix: Qwark VidComic 5 Clear":
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 5),

        # VR
        "Phoenix: VR: VR Gadget Training":
            lambda state: state.can_reach("Tyhrranosis", player=world.player)
                          and state.has_all([RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT], player=world.player),

        # ----- Planet Marcadia -----#
        # "Marcadia: Received Spitting Hydra": LocData(50001030, "Marcadia":
        # "Marcadia: Received Refractor": LocData(50001031, "Marcadia":
        # "Marcadia: T-Bolt: After Pool of Water": LocData(50001032, "Marcadia":

        "Marcadia: Meet Al":
            lambda state: state.has(RAC3ITEM.REFRACTOR, world.player),

        # ----- Annihilation Nation -----#
        # First visit (when getting Tyhrra-Guise)
        "Annihilation: Whip it Good":
            lambda state: state.has_any([RAC3ITEM.PLASMA_WHIP, RAC3ITEM.PROGRESSIVE_PLASMA_WHIP], world.player),
        "Annihilation: Hydra'n Seek":
            lambda state: state.has_any([RAC3ITEM.SPITTING_HYDRA, RAC3ITEM.PROGRESSIVE_SPITTING_HYDRA], world.player)
                          and state.can_reach_location("Annihilation: Whip it Good", world.player),

        # Second visit: Post-Dax(Meeting Courtney)
        "Annihilation: Time to Suck":
            lambda state: state.has_any([RAC3ITEM.SUCK_CANNON, RAC3ITEM.PROGRESSIVE_SUCK_CANNON], world.player),
        "Annihilation: Chop Chop":
            lambda state: state.has_any([RAC3ITEM.DISC_BLADE, RAC3ITEM.PROGRESSIVE_DISC_BLADE], world.player),
        "Annihilation: Sleep Inducer":
            lambda state: state.has_any([RAC3ITEM.RIFT_INDUCER, RAC3ITEM.PROGRESSIVE_RIFT_INDUCER], world.player)
                          and state.can_reach_location("Annihilation: Chop Chop", world.player),
        "Annihilation: The Other White Meat":
            lambda state: state.has_any([RAC3ITEM.QWACK_O_RAY, RAC3ITEM.PROGRESSIVE_QWACK_O_RAY], world.player)
                          and state.can_reach_location("Annihilation: Sleep Inducer", world.player),

        # Maybe difficult and long(100 rounds ...), so it restrict after getting items for clear the game.
        "Annihilation: Qwarktastic Battle":
            lambda state: state.has_all(
                [RAC3ITEM.HACKER, RAC3ITEM.TYHRRA_GUISE, RAC3ITEM.HYPERSHOT, RAC3ITEM.GRAV_BOOTS], world.player)
                          and state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 5),

        # ----- Planet Aquatos -----#
        # "Aquatos: Received Flux Rifle": LocData(50001090, RAC3REGION.AQUATOS),
        # "Aquatos: T-Bolt: Under the Bridge": LocData(50001091, RAC3REGION.AQUATOS),
        # "Aquatos: T-Bolt: Underwater Bolt": LocData(50001092, RAC3REGION.AQUATOS),
        # "Aquatos: Received Mini-Turret Glove"
        # "Aquatos: Received Lava Gun"
        "Aquatos: Received Shield Charger":
            lambda state: state.can_reach("Command Center", player=world.player),
        "Aquatos: Received Bouncer":
            lambda state: state.can_reach("Qwarks Hideout", player=world.player),
        "Aquatos: Received Plasma Coil":
            lambda state: state.can_reach("Koros", player=world.player),

        # Sewers

        # "Aquatos: 1 Sewer Crystal Traded": LocData(50001096, RAC3REGION.AQUATOS),
        # "Aquatos: 5 Sewer Crystals Traded": LocData(50001097, RAC3REGION.AQUATOS),
        # "Aquatos: 10 Sewer Crystals Traded": LocData(50001098, RAC3REGION.AQUATOS),
        # "Aquatos: 20 Sewer Crystals Traded": LocData(50001099, RAC3REGION.AQUATOS),

        # ----- Planet Tyhrranosis -----#
        # "Tyhrranosis: Received Annihilator": LocData(50001300, "Tyhrranosis":
        # "Tyhrranosis: Received Holo-Shield Glove": LocData(50001301, "Tyhrranosis":
        # "Tyhrranosis: T-Bolt: South East Cannon": LocData(50001302, "Tyhrranosis":

        # ----- Planet Daxx -----#
        "Daxx: Infiltrate Weapons Facility":
            lambda state: state.has_all([RAC3ITEM.HYPERSHOT, RAC3ITEM.HACKER], world.player),
        # "Daxx: Received Charge Boots": LocData(50001322, "Daxx Region 1":

        "Daxx: Gunship":
            lambda state: state.has(RAC3ITEM.HYPERSHOT, world.player),

        # ----- Obani Gemini -----# # Nothing

        # ----- Planet Blackwater City -----# # Nothing

        # ----- Holostar Studios -----# # Nothing
        # "Holostar: T-Bolt: Lot 42's Gravity Ramp"
        # "Holostar: T-Bolt: Kamikaze Noids"

        # ----- Obani Draco (lol) -----# # Nothing

        # ----- Zeldrin Starport -----# # Nothing
        "Zeldrin Starport: Received Bolt Grabber V2":
            lambda state: state.has(RAC3ITEM.HYPERSHOT, world.player),
        # "Zeldrin Starport: T-Bolt: Inside the Second Ship"

        # ----- Planet Metropolis -----#

        # Skrunch Trophy
        # "Metropolis: Metal-Noids"
        # "Metropolis: T-Bolt: Before Grav-Wall"
        # Klunk Fight

        # ----- Planet Crash Site -----#
        # "Crash Site: T-Bolt: Turn Around": None
        "Crash Site: Received Nano-Pak":
            lambda state: state.has_all([RAC3ITEM.GRAV_BOOTS, RAC3ITEM.HYPERSHOT], world.player),
        # Escape Pod: None
        "Crash Site: Infobot: Aridia":
            lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),

        # ----- Planet Aridia -----#

        # ----- Qwark's Hideout -----#
        "Qwarks Hideout: Received Gadgetron PDA":
            lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),

        # ----- Planet Koros -----#
        # Courtney Gears Trophy
        # "Koros: T-Bolt: Behind the Metal Fence"
        # "Koros: T-Bolt: Pair of Towers"

        # ----- Planet Command Center -----#
        "Command Center: Trophy: Up a Ladder":
            lambda state: state.has_all([RAC3ITEM.HYPERSHOT, RAC3ITEM.GRAV_BOOTS, RAC3ITEM.TYHRRA_GUISE],
                                        world.player),
        "Command Center: Dr. Nefarious Defeated!":
            lambda state: state.has_all([RAC3ITEM.HYPERSHOT, RAC3ITEM.GRAV_BOOTS, RAC3ITEM.TYHRRA_GUISE,
                                         RAC3ITEM.HACKER, RAC3ITEM.REFRACTOR], world.player),
        "Command Center: Biobliterator Defeated!":
            lambda state: state.has_all([RAC3ITEM.HYPERSHOT, RAC3ITEM.GRAV_BOOTS, RAC3ITEM.TYHRRA_GUISE,
                                         RAC3ITEM.HACKER, RAC3ITEM.REFRACTOR], world.player),

        # ----- Titanium Bolts -----#

        # if world.options.titanium_bolts.value == 1:
        # Phoenix
        "Phoenix: T-Bolt: VR Gadget Training":
            lambda state: state.can_reach("Tyhrranosis", player=world.player)
                          and state.has_all([RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT], player=world.player),
        "Phoenix: T-Bolt: VidComic 1 100%":
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 1),
        "Phoenix: T-Bolt: VidComic 2 100%":
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 2),
        "Phoenix: T-Bolt: VidComic 3 100%":
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 3),
        "Phoenix: T-Bolt: VidComic 4 100%":
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 4),
        "Phoenix: T-Bolt: VidComic 5 100%":
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 5),
        # Marcadia
        "Marcadia: T-Bolt: Last Refractor Room":
            lambda state: state.has_all([RAC3ITEM.REFRACTOR, RAC3ITEM.GRAV_BOOTS], world.player),
        "Marcadia: T-Bolt: Ceiling just before Al":
            lambda state: state.has_all([RAC3ITEM.REFRACTOR, RAC3ITEM.GRAV_BOOTS], world.player),
        # Aquatos
        "Aquatos: T-Bolt: Behind the Locked Gate":
            lambda state: state.has(RAC3ITEM.HACKER, world.player),
        "Aquatos: T-Bolt: Top Left Bolt":
            lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),
        "Aquatos: T-Bolt: Swinging Bolt":
            lambda state: state.has_all([RAC3ITEM.HYPERSHOT, RAC3ITEM.GRAV_BOOTS], world.player),

        # Tyhrranosis
        "Tyhrranosis: T-Bolt: Underground Cave Bolt":
            lambda state: state.has(RAC3ITEM.HYPERSHOT, world.player),

        # Daxx
        "Daxx: T-Bolt: Right of the Taxi":
            lambda state: state.has(RAC3ITEM.HYPERSHOT, world.player),
        "Daxx: T-Bolt: Time Sensitive Door":
            lambda state: state.has_all([RAC3ITEM.HYPERSHOT, RAC3ITEM.CHARGE_BOOTS, RAC3ITEM.HACKER],
                                        world.player),
        # Holostar Studios
        "Holostar: T-Bolt: Lot 42's Gravity Ramp":
            lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),
        "Holostar: T-Bolt: Kamikaze Noids":
            lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),

        # Obani Gemini
        "Obani Gemini: T-Bolt: Follow the Lava":
            lambda state: state.has(RAC3ITEM.HYPERSHOT, world.player),

        # Zeldrin Starport
        "Zeldrin Starport: T-Bolt: Atop the Twin Shooters":
            lambda state: state.has(RAC3ITEM.HYPERSHOT, world.player),

        # Metropolis
        "Metropolis: T-Bolt: Across the Gap":
            lambda state: state.has(RAC3ITEM.HYPERSHOT, world.player),

        # Aridia
        "Aridia: T-Bolt: Under the Bridge (Assassination)":
            lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),
        "Aridia: T-Bolt: Behind the Base (X12 Endgame)":
            lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),

        # Qwark's Hideout
        "Qwarks Hideout: T-Bolt: Glide from the Ramp":
            lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),

        # Command Center
        "Command Center: T-Bolt: Behind the Forcefield":
            lambda state: state.has_all([RAC3ITEM.HYPERSHOT, RAC3ITEM.GRAV_BOOTS, RAC3ITEM.TYHRRA_GUISE],
                                        world.player),

        # ----- Simple Skill Points -----#
        # if world.options.skill_points.value > 0:
        # Phoenix
        "Phoenix: Skill Point: Beat Helga's Best VR Time":
            lambda state: state.can_reach("Tyhrranosis", player=world.player)
                          and state.has_all([RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT], player=world.player),

        # Marcadia
        "Marcadia: Skill Point: Reflect on how to score":
            lambda state: state.has(RAC3ITEM.REFRACTOR, world.player),

        # Tyhrranosis
        "Tyhrranosis: Skill Point: Be a Sharpshooter":
            lambda state: state.has_any([RAC3ITEM.FLUX_RIFLE, RAC3ITEM.PROGRESSIVE_FLUX_RIFLE], world.player),

        # Daxx
        "Daxx: Skill Point: Bugs to Birdie":
            lambda state: state.has_any([RAC3ITEM.QWACK_O_RAY, RAC3ITEM.PROGRESSIVE_QWACK_O_RAY], world.player),

        # Metropolis
        "Metropolis: Skill Point: 2002 was a good year in the city":
            lambda state: state.has_any(
                [RAC3ITEM.FLUX_RIFLE, RAC3ITEM.PROGRESSIVE_FLUX_RIFLE, RAC3ITEM.ANNIHILATOR,
                 RAC3ITEM.PROGRESSIVE_ANNIHILATOR, RAC3ITEM.RY3N0, RAC3ITEM.PROGRESSIVE_RY3N0,
                 RAC3ITEM.SUCK_CANNON,
                 RAC3ITEM.PROGRESSIVE_SUCK_CANNON, RAC3ITEM.DISC_BLADE, RAC3ITEM.PROGRESSIVE_DISC_BLADE
                 ], world.player),

        # Crash Site
        "Crash Site: Skill Point: Aim High":
            lambda state: state.has_any([RAC3ITEM.FLUX_RIFLE, RAC3ITEM.PROGRESSIVE_FLUX_RIFLE], world.player),

        # Qwark's Hideout
        "Qwarks Hideout: Skill Point: Break the Dan":
            lambda state: state.has_all([RAC3ITEM.WARP_PAD, RAC3ITEM.HYPERSHOT], world.player),

        # Koros
        "Koros: Skill Point: You break it, you win it":
            lambda state: state.has(RAC3ITEM.BOX_BREAKER, world.player),

        # ----- Every Skill Point -----#
        # if world.options.skill_points.value > 1:
        "Phoenix: Skill Point: Monkeying Around":
            lambda state: state.has(RAC3ITEM.TYHRRA_GUISE, world.player),
        "Phoenix: Skill Point: Turn Up The Heat!":
            lambda state: state.can_reach("Koros", player=world.player),
        "Phoenix: Skill Point: Strive for Arcade Perfection":
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 5),
        "Phoenix: Skill Point: Pirate booty - set a new record for qwark":
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 1),
        "Phoenix: Skill Point: Arriba Amoeba! - set a new record for qwark":
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 2),
        "Phoenix: Skill Point: Shadow of the robot - set a new record for qwark":
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 3),
        "Phoenix: Skill Point: Deja Q All over Again - set a new record for qwark":
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 4),
        "Phoenix: Skill Point: The Shaming of the Q - set a new record for qwark":
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 5),

        # Aquatos
        "Aquatos: Skill Point: Hit the motherload":
            lambda state: state.has(RAC3ITEM.GRAV_BOOTS, world.player),

        # Crash Site
        "Crash Site: Skill Point: Suck it up!":
            lambda state: state.has_any([RAC3ITEM.SUCK_CANNON, RAC3ITEM.PROGRESSIVE_SUCK_CANNON], world.player),

        # Aridia
        "Aridia: Skill Point: Zap back at ya'":
            lambda state: state.has(RAC3ITEM.REFRACTOR, world.player),

        # Command Center
        "Command Center: Skill Point: Spread Your Germs":
            lambda state: state.has_any([RAC3ITEM.INFECTOR, RAC3ITEM.PROGRESSIVE_INFECTOR], world.player)
                          and state.has_all([RAC3ITEM.HYPERSHOT, RAC3ITEM.GRAV_BOOTS, RAC3ITEM.TYHRRA_GUISE],
                                            world.player),

        # ----- Collectible Trophies -----#
        # if world.options.trophies.value > 0:
        # Qwark's Hideout
        "Qwarks Hideout: Trophy: Outside Qwarks Room":
            lambda state: state.has_all([RAC3ITEM.WARP_PAD, RAC3ITEM.HYPERSHOT], world.player),

        # ----- Long Term Trophies -----#
        # if world.options.trophies.value > 1:
        "Phoenix: Long Term Trophy: Titanium Collector":
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 5)
                          and state.has_all(
                [RAC3ITEM.REFRACTOR, RAC3ITEM.GRAV_BOOTS, RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT,
                 RAC3ITEM.TYHRRA_GUISE, RAC3ITEM.WARP_PAD], world.player)
                          and state.can_reach(RAC3REGION.FLORANA, player=world.player)
                          and state.can_reach(RAC3REGION.STARSHIP_PHOENIX, player=world.player)
                          and state.can_reach(RAC3REGION.MARCADIA, player=world.player)
                          and state.can_reach(RAC3REGION.ANNIHILATION_NATION_2, player=world.player)
                          and state.can_reach(RAC3REGION.AQUATOS_SEWERS, player=world.player)
                          and state.can_reach(RAC3REGION.TYHRRANOSIS_MISSION, player=world.player)
                          and state.can_reach(RAC3REGION.DAXX, player=world.player)
                          and state.can_reach(RAC3REGION.OBANI_GEMINI, player=world.player)
                          and state.can_reach(RAC3REGION.HOLOSTAR_STUDIOS, player=world.player)
                          and state.can_reach(RAC3REGION.ZELDRIN_STARPORT, player=world.player)
                          and state.can_reach(RAC3REGION.METROPOLIS_MISSION, player=world.player)
                          and state.can_reach(RAC3REGION.CRASH_SITE, player=world.player)
                          and state.can_reach(RAC3REGION.ARIDIA, player=world.player)
                          and state.can_reach(RAC3REGION.QWARKS_HIDEOUT, player=world.player)
                          and state.can_reach(RAC3REGION.KOROS, player=world.player)
                          and state.can_reach(RAC3REGION.COMMAND_CENTER, player=world.player),

        "Phoenix: Long Term Trophy: Friend of the Rangers":
            lambda state: state.can_reach(RAC3REGION.MARCADIA, player=world.player)
                          and state.can_reach(RAC3REGION.TYHRRANOSIS_MISSION, player=world.player)
                          and state.can_reach(RAC3REGION.METROPOLIS_MISSION, player=world.player)
                          and state.can_reach(RAC3REGION.ARIDIA, player=world.player)
                          and state.can_reach(RAC3REGION.BLACKWATER_CITY, player=world.player),

        # Same rule as Qwarktastic Battle as you usually get it after that
        "Phoenix: Long Term Trophy: Annihilation Nation Champion":
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 5)
                          and state.has_all(
                [RAC3ITEM.HACKER, RAC3ITEM.TYHRRA_GUISE, RAC3ITEM.HYPERSHOT, RAC3ITEM.GRAV_BOOTS],
                world.player),

        "Phoenix: Long Term Trophy: Skill Master":
            lambda state: state.has(RAC3ITEM.PROGRESSIVE_VIDCOMIC, world.player, 5)
                          # Gadgets
                          and state.has_all(
                [RAC3ITEM.GRAV_BOOTS, RAC3ITEM.HACKER, RAC3ITEM.HYPERSHOT, RAC3ITEM.REFRACTOR,
                 RAC3ITEM.TYHRRA_GUISE, RAC3ITEM.WARP_PAD], world.player)
                          # Planets
                          and state.can_reach(RAC3REGION.FLORANA, player=world.player)
                          and state.can_reach(RAC3REGION.STARSHIP_PHOENIX, player=world.player)
                          and state.can_reach(RAC3REGION.MARCADIA, player=world.player)
                          and state.can_reach(RAC3REGION.ANNIHILATION_NATION_2, player=world.player)
                          and state.can_reach(RAC3REGION.AQUATOS_SEWERS, player=world.player)
                          and state.can_reach(RAC3REGION.TYHRRANOSIS, player=world.player)
                          and state.can_reach(RAC3REGION.DAXX, player=world.player)
                          and state.can_reach(RAC3REGION.OBANI_GEMINI, player=world.player)
                          and state.can_reach(RAC3REGION.BLACKWATER_CITY, player=world.player)
                          and state.can_reach(RAC3REGION.HOLOSTAR_STUDIOS, player=world.player)
                          and state.can_reach(RAC3REGION.METROPOLIS, player=world.player)
                          and state.can_reach(RAC3REGION.CRASH_SITE, player=world.player)
                          and state.can_reach(RAC3REGION.ARIDIA, player=world.player)
                          and state.can_reach(RAC3REGION.QWARKS_HIDEOUT, player=world.player)
                          and state.can_reach(RAC3REGION.KOROS, player=world.player)
                          and state.can_reach(RAC3REGION.COMMAND_CENTER, player=world.player)
                          # Weapons
                          and state.has_all(
                [RAC3ITEM.PLASMA_WHIP, RAC3ITEM.SPITTING_HYDRA, RAC3ITEM.SUCK_CANNON, RAC3ITEM.DISC_BLADE,
                 RAC3ITEM.FLUX_RIFLE, RAC3ITEM.QWACK_O_RAY, RAC3ITEM.ANNIHILATOR, RAC3ITEM.INFECTOR],
                world.player),
    }
    # ----- Nanotech -----#

    match world.options.nanotech_milestones.value:
        case 1:  # 5 nanotech level is a check
            for level in range(15, 101, 5):
                check = (level - 10) // 5
                add_rule(world.get_location(f"Nanotech Milestone: {level}"),
                         lambda state: state.has_from_list(planet_data.keys(), world.player, check))
        case 2:  # 10 nanotech level is a check
            for level in range(20, 101, 10):
                check = (level - 10) // 5
                add_rule(world.get_location(f"Nanotech Milestone: {level}"),
                         lambda state: state.has_from_list(planet_data.keys(), world.player, check))
        case 3:  # 20 nanotech level is a check
            for level in range(20, 101, 20):
                check = (level - 10) // 5
                add_rule(world.get_location(f"Nanotech Milestone: {level}"),
                         lambda state: state.has_from_list(planet_data.keys(), world.player, check))

        case 4:  # Every nanotech level is a check
            for level in range(11, 101):
                check = (level - 10) // 5
                add_rule(world.get_location(f"Nanotech Milestone: {level}"),
                         lambda state: state.has_from_list(planet_data.keys(), world.player, check))

    for region in region_rules_dict.keys():
        add_rule(world.multiworld.get_entrance(region, world.player), region_rules_dict[region])
    for location in world.get_locations():
        add_rule(location, rules_dict.get(location.name, lambda _: True))

    # world.multiworld.completion_condition[world.player] = lambda state: state.has(RAC3ITEM.VICTORY, world.player)
    world.multiworld.completion_condition[world.player] = lambda state: state.has(RAC3ITEM.VICTORY, world.player)
