import logging
from typing import TYPE_CHECKING

from worlds.generic.Rules import add_rule

if TYPE_CHECKING:
    from . import RaC3World

rac3_logger = logging.getLogger("Ratchet & Clank 3")
rac3_logger.setLevel(logging.DEBUG)


def set_rules_planets(world):
    # Getting to Marcadia
    add_rule(world.multiworld.get_entrance("Starship Phoenix -> Marcadia", world.player),
             lambda state: state.has("Infobot: Marcadia", world.player))

    # Getting to Annihilation Nation:
    add_rule(world.multiworld.get_entrance("Starship Phoenix -> Annihilation Nation", world.player),
             lambda state: state.has("Infobot: Annihilation Nation", world.player))

    # Getting to Aquatos
    add_rule(world.multiworld.get_entrance("Starship Phoenix -> Aquatos", world.player),
             lambda state: state.has("Infobot: Aquatos", world.player))

    # Getting to Tyhrranosis
    add_rule(world.multiworld.get_entrance("Starship Phoenix -> Tyhrranosis", world.player),
             lambda state: state.has("Infobot: Tyhrranosis", world.player))

    # Getting to Daxx
    add_rule(world.multiworld.get_entrance("Starship Phoenix -> Daxx", world.player),
             lambda state: state.has("Infobot: Daxx", world.player))

    # Getting to Obani Gemini
    add_rule(world.multiworld.get_entrance("Starship Phoenix -> Obani Gemini", world.player),
             lambda state: state.has_all(["Infobot: Obani Gemini", "Refractor"], world.player))

    # Getting to Blackwater City
    add_rule(world.multiworld.get_entrance("Starship Phoenix -> Blackwater City", world.player),
             lambda state: state.has("Infobot: Blackwater City", world.player))

    # Getting to Holostar Studios
    add_rule(world.multiworld.get_entrance("Starship Phoenix -> Holostar Studios", world.player),  # Softlock Prevention
             lambda state: state.has_all(["Infobot: Holostar Studios", "Hacker", "Hypershot"], world.player))

    # Getting to Obani Draco (lol)
    add_rule(world.multiworld.get_entrance("Starship Phoenix -> Obani Draco", world.player),
             lambda state: state.has_all(["Infobot: Obani Draco", "Gravity-Boots"], world.player))

    # Getting to Zeldrin Starport
    add_rule(world.multiworld.get_entrance("Starship Phoenix -> Zeldrin Starport", world.player),
             lambda state: state.has("Infobot: Zeldrin Starport", world.player))

    # Getting to Metropolis
    add_rule(world.multiworld.get_entrance("Starship Phoenix -> Metropolis", world.player),
             lambda state: state.has("Infobot: Metropolis", world.player))

    # Getting to Crash Site
    add_rule(world.multiworld.get_entrance("Starship Phoenix -> Crash Site", world.player),
             lambda state: state.has("Infobot: Crash Site", world.player))

    # Getting to Aridia
    add_rule(world.multiworld.get_entrance("Starship Phoenix -> Aridia", world.player),
             lambda state: state.has("Infobot: Aridia", world.player))

    # Getting to Qwark's Hideout
    add_rule(world.multiworld.get_entrance("Starship Phoenix -> Qwarks Hideout", world.player),
             lambda state: state.has_all(["Infobot: Qwarks Hideout", "Refractor"], world.player))  # Softlock Prevention

    # Getting to Koros
    add_rule(world.multiworld.get_entrance("Starship Phoenix -> Koros", world.player),
             lambda state: state.has("Infobot: Koros", world.player))

    # Getting to Command Center
    add_rule(world.multiworld.get_entrance("Starship Phoenix -> Command Center", world.player),
             lambda state: state.has("Infobot: Command Center", world.player))


def set_rules_hard_location(world):
    # ----- Planet Veldin -----# # Nothing
    # ----- Planet Florana -----# # Nothing

    # ----- Starship Phoenix -----#
    # "Phoenix: Received Suck Cannon": LocData(, "Starship Phoenix"),
    # "Phoenix: Received Infector": LocData(, "Starship Phoenix"),
    #  add_rule(world.get_location("Phoenix: T-Bolt: VR Nerves of Titanium"), None)

    add_rule(world.get_location("Phoenix: Received Adamantine Armor"),
             lambda state: state.can_reach("Aquatos", player=world.player))
    add_rule(world.get_location("Phoenix: Received Aegis Mark V Armor"),
             lambda state: state.can_reach("Zeldrin Starport", player=world.player))
    add_rule(world.get_location("Phoenix: Received Infernox Armor"),
             lambda state: state.can_reach("Koros", player=world.player))
    add_rule(world.get_location("Phoenix: Received Hacker"),
             lambda state: state.can_reach("Tyhrranosis", player=world.player)
                           and state.has_all(["Hacker", "Hypershot"], player=world.player))
    add_rule(world.get_location("Phoenix: Received Hypershot"),
             lambda state: state.can_reach("Tyhrranosis", player=world.player)
                           and state.has_all(["Hacker", "Hypershot"], player=world.player))
    # "Phoenix: Meet Sasha on the Bridge": LocData(, "Starship Phoenix"),
    add_rule(world.get_location("Phoenix: Return after winning Grand Prize Bout"),
             lambda state: state.can_reach("Annihilation Nation", player=world.player))
    add_rule(world.get_location("Phoenix: Return after Aquatos Base"),
             lambda state: state.can_reach("Aquatos", player=world.player))
    add_rule(world.get_location("Phoenix: VR Training after Noid Queen"),
             lambda state: state.can_reach("Tyhrranosis", player=world.player)
                           and state.has_all(["Hacker", "Hypershot"], player=world.player))
    add_rule(world.get_location("Phoenix: Post Hideout Assault"),
             lambda state: state.can_reach("Qwarks Hideout", player=world.player)
                           and state.has_all(["Warp Pad", "Hypershot"], world.player))
    add_rule(world.get_location("Phoenix: Give Al the Master Plan"),
             lambda state: state.has("Master Plan", player=world.player))
    # VidComic clear locations
    add_rule(world.get_location("Phoenix: Play VidComic 1"),
             lambda state: state.has("Progressive VidComic", world.player, 1))
    add_rule(world.get_location("Phoenix: Qwark VidComic 1 Clear"),
             lambda state: state.has("Progressive VidComic", world.player, 1))
    add_rule(world.get_location("Phoenix: Qwark VidComic 2 Clear"),
             lambda state: state.has("Progressive VidComic", world.player, 2))
    add_rule(world.get_location("Phoenix: Qwark VidComic 3 Clear"),
             lambda state: state.has("Progressive VidComic", world.player, 3))
    add_rule(world.get_location("Phoenix: Play VidComic 4"),
             lambda state: state.has("Progressive VidComic", world.player, 4))
    add_rule(world.get_location("Phoenix: Qwark VidComic 4 Clear"),
             lambda state: state.has("Progressive VidComic", world.player, 4))
    add_rule(world.get_location("Phoenix: Play VidComic 5"),
             lambda state: state.has("Progressive VidComic", world.player, 5))
    add_rule(world.get_location("Phoenix: Qwark VidComic 5 Clear"),
             lambda state: state.has("Progressive VidComic", world.player, 5))

    # VR
    add_rule(world.get_location("Phoenix: VR: VR Gadget Training"),
             lambda state: state.can_reach("Tyhrranosis", player=world.player)
                           and state.has_all(["Hacker", "Hypershot"], player=world.player))

    # ----- Planet Marcadia -----#
    # "Marcadia: Received Spitting Hydra": LocData(50001030, "Marcadia"),
    # "Marcadia: Received Refractor": LocData(50001031, "Marcadia"),
    # "Marcadia: T-Bolt: After Pool of Water": LocData(50001032, "Marcadia"),

    add_rule(world.get_location("Marcadia: Meet Al"),
             lambda state: state.has("Refractor", world.player))

    if world.options.skill_points.value > 0:  # Simple or Every Skill Point
        add_rule(world.get_location("Marcadia: Skill Point: Reflect on how to score"),
                 lambda state: state.has("Refractor", world.player))

    # ----- Annihilation Nation -----#
    # First visit (when getting Tyhrra-Guise)
    add_rule(world.get_location("Annihilation: Whip it Good"),
             lambda state: state.has_any(["Plasma Whip", "Progressive Plasma Whip"], world.player))
    add_rule(world.get_location("Annihilation: Hydra'n Seek"),
             lambda state: state.has_any(["Spitting Hydra", "Progressive Spitting Hydra"], world.player)
                           and state.can_reach_location("Annihilation: Whip it Good", world.player))

    # Second visit: Post-Dax(Meeting Courtney)
    add_rule(world.get_location("Annihilation: Time to Suck"),
             lambda state: state.has_any(["Suck Cannon", "Progressive Suck Cannon"], world.player))
    add_rule(world.get_location("Annihilation: Chop Chop"),
             lambda state: state.has_any(["Disk-Blade Gun", "Progressive Disk-Blade Gun"], world.player))
    add_rule(world.get_location("Annihilation: Sleep Inducer"),
             lambda state: state.has_any(["Rift Inducer", "Progressive Rift Inducer"], world.player)
                           and state.can_reach_location("Annihilation: Chop Chop", world.player))
    add_rule(world.get_location("Annihilation: The Other White Meat"),
             lambda state: state.has_any(["Qwack-O-Ray", "Progressive Qwack-O-Ray"], world.player)
                           and state.can_reach_location("Annihilation: Sleep Inducer", world.player))

    # Maybe difficult and long(100 rounds ...), so it restrict after getting items for clear the game.
    add_rule(world.get_location("Annihilation: Qwarktastic Battle"),
             lambda state: state.has_all(["Hacker", "Tyhrra-Guise", "Hypershot", "Gravity-Boots"], world.player)
                           and state.has("Progressive VidComic", world.player, 5)),

    # ----- Planet Aquatos -----#
    # "Aquatos: Received Flux Rifle": LocData(50001090, "Aquatos"),
    # "Aquatos: T-Bolt: Under the Bridge": LocData(50001091, "Aquatos"),
    # "Aquatos: T-Bolt: Underwater Bolt": LocData(50001092, "Aquatos"),
    # "Aquatos: Received Mini-Turret Glove"
    # "Aquatos: Received Lava Gun"
    add_rule(world.get_location("Aquatos: Received Shield Charger"),
             lambda state: state.can_reach("Command Center", player=world.player))
    add_rule(world.get_location("Aquatos: Received Bouncer"),
             lambda state: state.can_reach("Qwarks Hideout", player=world.player))
    add_rule(world.get_location("Aquatos: Received Plasma Coil"),
             lambda state: state.can_reach("Koros", player=world.player))

    # Sewers

    # "Aquatos: 1 Sewer Crystal Traded": LocData(50001096, "Aquatos"),
    # "Aquatos: 5 Sewer Crystals Traded": LocData(50001097, "Aquatos"),
    # "Aquatos: 10 Sewer Crystals Traded": LocData(50001098, "Aquatos"),
    # "Aquatos: 20 Sewer Crystals Traded": LocData(50001099, "Aquatos"),

    # ----- Planet Tyhrranosis -----#
    # "Tyhrranosis: Received Annihilator": LocData(50001300, "Tyhrranosis"),
    # "Tyhrranosis: Received Holo-Shield Glove": LocData(50001301, "Tyhrranosis"),
    # "Tyhrranosis: T-Bolt: South East Cannon": LocData(50001302, "Tyhrranosis"),

    # ----- Planet Daxx -----#
    add_rule(world.get_location("Daxx: Infiltrate Weapons Facility"),
             lambda state: state.has_all(["Hypershot", "Hacker"], world.player))
    # "Daxx: Received Charge Boots": LocData(50001322, "Daxx Region 1"),

    add_rule(world.get_location("Daxx: Gunship"),
             lambda state: state.has("Hypershot", world.player))

    # ----- Obani Gemini -----# # Nothing

    # ----- Planet Blackwater City -----# # Nothing

    # ----- Holostar Studios -----# # Nothing
    # "Holostar: T-Bolt: Lot 42's Gravity Ramp"
    # "Holostar: T-Bolt: Kamikaze Noids"

    # ----- Obani Draco (lol) -----# # Nothing

    # ----- Zeldrin Starport -----# # Nothing
    add_rule(world.get_location("Zeldrin Starport: Received Bolt Grabber V2"),
             lambda state: state.has("Hypershot", world.player))
    # "Zeldrin Starport: T-Bolt: Inside the Second Ship"

    # ----- Planet Metropolis -----#

    # Skrunch Trophy
    # "Metropolis: Metal-Noids"
    # "Metropolis: T-Bolt: Before Grav-Wall"
    # Klunk Fight

    # ----- Planet Crash Site -----#
    # add_rule(world.get_location("Crash Site: T-Bolt: Turn Around"), None)
    add_rule(world.get_location("Crash Site: Received Nano-Pak"),
             lambda state: state.has_all(["Gravity-Boots", "Hypershot"], world.player))
    # Escape Pod: None
    add_rule(world.get_location("Crash Site: Infobot: Aridia"), lambda state: state.has("Gravity-Boots", world.player))

    # ----- Planet Aridia -----#

    # ----- Qwark's Hideout -----#
    add_rule(world.get_location("Qwarks Hideout: Received Gadgetron PDA"),
             lambda state: state.has("Gravity-Boots", world.player))

    # ----- Planet Koros -----#
    # Courtney Gears Trophy
    # "Koros: T-Bolt: Behind the Metal Fence"
    # "Koros: T-Bolt: Pair of Towers"

    # ----- Planet Command Center -----#
    add_rule(world.get_location("Command Center: Dr. Nefarious Defeated!"),
             lambda state: state.has_all(["Hypershot", "Gravity-Boots", "Tyhrra-Guise",
                                          "Hacker", "Refractor"], world.player))
    add_rule(world.get_location("Command Center: Biobliterator Defeated!"),
             lambda state: state.has_all(["Hypershot", "Gravity-Boots", "Tyhrra-Guise",
                                          "Hacker", "Refractor"], world.player))

    # ----- Titanium Bolts -----#

    if world.options.titanium_bolts.value == 1:
        # Phoenix
        add_rule(world.get_location("Phoenix: T-Bolt: VR Gadget Training"),
                 lambda state: state.can_reach("Tyhrranosis", player=world.player)
                               and state.has_all(["Hacker", "Hypershot"], player=world.player))
        add_rule(world.get_location("Phoenix: T-Bolt: VidComic 1 100%"),
                 lambda state: state.has("Progressive VidComic", world.player, 1))
        add_rule(world.get_location("Phoenix: T-Bolt: VidComic 2 100%"),
                 lambda state: state.has("Progressive VidComic", world.player, 2))
        add_rule(world.get_location("Phoenix: T-Bolt: VidComic 3 100%"),
                 lambda state: state.has("Progressive VidComic", world.player, 3))
        add_rule(world.get_location("Phoenix: T-Bolt: VidComic 4 100%"),
                 lambda state: state.has("Progressive VidComic", world.player, 4))
        add_rule(world.get_location("Phoenix: T-Bolt: VidComic 5 100%"),
                 lambda state: state.has("Progressive VidComic", world.player, 5))
        # Marcadia
        add_rule(world.get_location("Marcadia: T-Bolt: Last Refractor Room"),
                 lambda state: state.has_all(["Refractor", "Gravity-Boots"], world.player))
        add_rule(world.get_location("Marcadia: T-Bolt: Ceiling just before Al"),
                 lambda state: state.has_all(["Refractor", "Gravity-Boots"], world.player))
        # Aquatos
        add_rule(world.get_location("Aquatos: T-Bolt: Behind the Locked Gate"),
                 lambda state: state.has("Hacker", world.player))
        add_rule(world.get_location("Aquatos: T-Bolt: Top Left Bolt"),
                 lambda state: state.has("Gravity-Boots", world.player))
        add_rule(world.get_location("Aquatos: T-Bolt: Swinging Bolt"),
                 lambda state: state.has_all(["Hypershot", "Gravity-Boots"], world.player))

        # Tyhrranosis
        add_rule(world.get_location("Tyhrranosis: T-Bolt: Underground Cave Bolt"),
                 lambda state: state.has("Hypershot", world.player))

        # Daxx
        add_rule(world.get_location("Daxx: T-Bolt: Right of the Taxi"),
                 lambda state: state.has("Hypershot", world.player))
        add_rule(world.get_location("Daxx: T-Bolt: Time Sensitive Door"),
                 lambda state: state.has_all(["Hypershot", "Charge-Boots", "Hacker"], world.player))
        # Holostar Studios
        add_rule(world.get_location("Holostar: T-Bolt: Lot 42's Gravity Ramp"),
                 lambda state: state.has("Gravity-Boots", world.player))
        add_rule(world.get_location("Holostar: T-Bolt: Kamikaze Noids"),
                 lambda state: state.has("Gravity-Boots", world.player))

        # Obani Gemini
        add_rule(world.get_location("Obani Gemini: T-Bolt: Follow the Lava"),
                 lambda state: state.has("Hypershot", world.player))

        # Zeldrin Starport
        add_rule(world.get_location("Zeldrin Starport: T-Bolt: Atop the Twin Shooters"),
                 lambda state: state.has("Hypershot", world.player))

        # Metropolis
        add_rule(world.get_location("Metropolis: T-Bolt: Across the Gap"),
                 lambda state: state.has("Hypershot", world.player))

        # Aridia
        add_rule(world.get_location("Aridia: T-Bolt: Under the Bridge (Assassination)"),
                 lambda state: state.has("Gravity-Boots", world.player))
        add_rule(world.get_location("Aridia: T-Bolt: Behind the Base (X12 Endgame)"),
                 lambda state: state.has("Gravity-Boots", world.player))

        # Qwark's Hideout
        add_rule(world.get_location("Qwarks Hideout: T-Bolt: Glide from the Ramp"),
                 lambda state: state.has("Gravity-Boots", world.player))

        # Command Center
        add_rule(world.get_location("Command Center: T-Bolt: Behind the Forcefield"),
                 lambda state: state.has_all(["Hypershot", "Gravity-Boots", "Tyhrra-Guise"], world.player))

    # ----- Simple Skill Points -----#
    if world.options.skill_points.value > 0:
        # Phoenix
        add_rule(world.get_location("Phoenix: Skill Point: Beat Helga's Best VR Time"),
                 lambda state: state.can_reach("Tyhrranosis", player=world.player)
                               and state.has_all(["Hacker", "Hypershot"], player=world.player))

        # Marcadia
        add_rule(world.get_location("Marcadia: Skill Point: Reflect on how to score"),
                 lambda state: state.has("Refractor", world.player))

        # Tyhrranosis
        add_rule(world.get_location("Tyhrranosis: Skill Point: Be a Sharpshooter"),
                 lambda state: state.has_any(["Flux Rifle", "Progressive Flux Rifle"], world.player))

        # Daxx
        add_rule(world.get_location("Daxx: Skill Point: Bugs to Birdie"),
                 lambda state: state.has_any(["Qwack-O-Ray", "Progressive Qwack-O-Ray"], world.player))

        # Metropolis
        add_rule(world.get_location("Metropolis: Skill Point: 2002 was a good year in the city"),
                 lambda state: state.has_any(["Flux Rifle", "Progressive Flux Rifle", "Annihilator",
                                              "Progressive Annihilator", "RY3N0", "Progressive RY3N0", "Suck Cannon",
                                              "Progressive Suck Cannon", "Disk-Blade Gun", "Progressive Disk-Blade Gun"
                                              ], world.player))

        # Crash Site
        add_rule(world.get_location("Crash Site: Skill Point: Aim High"),
                 lambda state: state.has_any(["Flux Rifle", "Progressive Flux Rifle"], world.player))

        # Qwark's Hideout
        add_rule(world.get_location("Qwarks Hideout: Skill Point: Break the Dan"),
                 lambda state: state.has_all(["Warp Pad", "Hypershot"], world.player))

        # Koros
        add_rule(world.get_location("Koros: Skill Point: You break it, you win it"),
                 lambda state: state.has("Box Breaker", world.player))

    # ----- Every Skill Point -----#
    if world.options.skill_points.value > 1:
        add_rule(world.get_location("Phoenix: Skill Point: Monkeying Around"),
                 lambda state: state.has("Tyhrra-Guise", world.player))
        add_rule(world.get_location("Phoenix: Skill Point: Turn Up The Heat!"),
                 lambda state: state.can_reach("Koros", player=world.player))
        add_rule(world.get_location("Phoenix: Skill Point: Strive for Arcade Perfection"),
                 lambda state: state.has("Progressive VidComic", world.player, 5))
        add_rule(world.get_location("Phoenix: Skill Point: Pirate booty - set a new record for qwark"),
                 lambda state: state.has("Progressive VidComic", world.player, 1))
        add_rule(world.get_location("Phoenix: Skill Point: Arriba Amoeba! - set a new record for qwark"),
                 lambda state: state.has("Progressive VidComic", world.player, 2)),
        add_rule(world.get_location("Phoenix: Skill Point: Shadow of the robot - set a new record for qwark"),
                 lambda state: state.has("Progressive VidComic", world.player, 3)),
        add_rule(world.get_location("Phoenix: Skill Point: Deja Q All over Again - set a new record for qwark"),
                 lambda state: state.has("Progressive VidComic", world.player, 4)),
        add_rule(world.get_location("Phoenix: Skill Point: The Shaming of the Q - set a new record for qwark"),
                 lambda state: state.has("Progressive VidComic", world.player, 5)),

        # Aquatos
        add_rule(world.get_location("Aquatos: Skill Point: Hit the motherload"),
                 lambda state: state.has("Gravity-Boots", world.player))

        # Crash Site
        add_rule(world.get_location("Crash Site: Skill Point: Suck it up!"),
                 lambda state: state.has_any(["Suck Cannon", "Progressive Suck Cannon"], world.player))

        # Aridia
        add_rule(world.get_location("Aridia: Skill Point: Zap back at ya'"),
                 lambda state: state.has("Refractor", world.player))

        # Command Center
        add_rule(world.get_location("Command Center: Skill Point: Spread Your Germs"),
                 lambda state: state.has_any(["Infector", "Progressive Infector"], world.player)
                               and state.has_all(["Hypershot", "Gravity-Boots", "Tyhrra-Guise"], world.player))

    # ----- Collectible Trophies -----#
    if world.options.trophies.value > 0:
        # Qwark's Hideout
        add_rule(world.get_location("Qwarks Hideout: Trophy: Outside Qwarks Room"),
                 lambda state: state.has_all(["Warp Pad", "Hypershot"], world.player))
        # Command Center
        add_rule(world.get_location("Command Center: Trophy: Up a Ladder"),
                lambda state: state.has_all(["Hypershot", "Gravity-Boots", "Tyhrra-Guise"], world.player))

    # ----- Long Term Trophies -----#
    if world.options.trophies.value > 1:
        add_rule(world.get_location("Phoenix: Long Term Trophy: Titanium Collector"),
                 lambda state: state.has("Progressive VidComic", world.player, 5)
                               and state.has_all(["Refractor", "Gravity-Boots", "Hacker", "Hypershot",
                                                  "Tyhrra-Guise", "Warp Pad"], world.player)
                               and state.can_reach("Florana", player=world.player)
                               and state.can_reach("Starship Phoenix", player=world.player)
                               and state.can_reach("Marcadia", player=world.player)
                               and state.can_reach("Annihilation Nation 2", player=world.player)
                               and state.can_reach("Aquatos", player=world.player)
                               and state.can_reach("Tyhrranosis", player=world.player)
                               and state.can_reach("Daxx", player=world.player)
                               and state.can_reach("Obani Gemini", player=world.player)
                               and state.can_reach("Holostar Studios", player=world.player)
                               and state.can_reach("Zeldrin Starport", player=world.player)
                               and state.can_reach("Metropolis Region 2", player=world.player)
                               and state.can_reach("Crash Site", player=world.player)
                               and state.can_reach("Aridia", player=world.player)
                               and state.can_reach("Qwarks Hideout", player=world.player)
                               and state.can_reach("Koros", player=world.player)
                               and state.can_reach("Command Center", player=world.player))

        add_rule(world.get_location("Phoenix: Long Term Trophy: Friend of the Rangers"),
                 lambda state: state.can_reach("Marcadia", player=world.player)
                               and state.can_reach("Tyhrranosis Region 2", player=world.player)
                               and state.can_reach("Metropolis Region 2", player=world.player)
                               and state.can_reach("Aridia", player=world.player)
                               and state.can_reach("Blackwater City", player=world.player))

        # Same rule as Qwarktastic Battle as you usually get it after that
        add_rule(world.get_location("Phoenix: Long Term Trophy: Annihilation Nation Champion"),
                 lambda state: state.has("Progressive VidComic", world.player, 5)
                               and state.has_all(["Hacker", "Tyhrra-Guise", "Hypershot", "Gravity-Boots"],
                                                 world.player))

        add_rule(world.get_location("Phoenix: Long Term Trophy: Skill Master"),
                 lambda state: state.has("Progressive VidComic", world.player, 5)
                               # Gadgets
                               and state.has_all(["Gravity-Boots", "Hacker", "Hypershot", "Refractor",
                                                  "Tyhrra-Guise", "Warp Pad"], world.player)
                               # Planets
                               and state.can_reach("Florana", player=world.player)
                               and state.can_reach("Starship Phoenix", player=world.player)
                               and state.can_reach("Marcadia", player=world.player)
                               and state.can_reach("Annihilation Nation 2", player=world.player)
                               and state.can_reach("Aquatos", player=world.player)
                               and state.can_reach("Tyhrranosis", player=world.player)
                               and state.can_reach("Daxx", player=world.player)
                               and state.can_reach("Obani Gemini", player=world.player)
                               and state.can_reach("Blackwater City", player=world.player)
                               and state.can_reach("Holostar Studios", player=world.player)
                               and state.can_reach("Metropolis Region 1", player=world.player)
                               and state.can_reach("Crash Site", player=world.player)
                               and state.can_reach("Aridia", player=world.player)
                               and state.can_reach("Qwarks Hideout", player=world.player)
                               and state.can_reach("Koros", player=world.player)
                               and state.can_reach("Command Center", player=world.player)
                               # Weapons
                               and state.has_all(["Plasma Whip", "Spitting Hydra", "Suck Cannon", "Disk-Blade Gun",
                                                  "Flux Rifle", "Qwack-O-Ray", "Annihilator", "Infector"],
                                                 world.player))

    # ----- Nanotech -----#
    planet_list: list[str] = [
        "Infobot: Florana",
        "Infobot: Starship Phoenix",
        "Infobot: Marcadia",
        "Infobot: Annihilation Nation",
        "Infobot: Aquatos",
        "Infobot: Tyhrranosis",
        "Infobot: Daxx",
        "Infobot: Obani Gemini",
        "Infobot: Blackwater City",
        "Infobot: Holostar Studios",
        "Infobot: Obani Draco",
        "Infobot: Zeldrin Starport",
        "Infobot: Metropolis",
        "Infobot: Crash Site",
        "Infobot: Aridia",
        "Infobot: Qwarks Hideout",
        "Infobot: Koros",
        "Infobot: Command Center"
    ]
    match world.options.nanotech_milestones.value:
        case 1:  # 5 nanotech level is a check
            for level in range(15, 101, 5):
                check = (level - 10) // 5
                add_rule(world.get_location(f"Nanotech Milestone: {level}"),
                         lambda state: state.has_from_list(planet_list, world.player, check))
        case 2:  # 10 nanotech level is a check
            for level in range(20, 101, 10):
                check = (level - 10) // 5
                add_rule(world.get_location(f"Nanotech Milestone: {level}"),
                         lambda state: state.has_from_list(planet_list, world.player, check))
        case 3:  # 20 nanotech level is a check
            for level in range(20, 101, 20):
                check = (level - 10) // 5
                add_rule(world.get_location(f"Nanotech Milestone: {level}"),
                         lambda state: state.has_from_list(planet_list, world.player, check))
        case 4:  # Every nanotech level is a check
            for level in range(11, 101):
                check = (level - 10) // 5
                add_rule(world.get_location(f"Nanotech Milestone: {level}"),
                         lambda state: state.has_from_list(planet_list, world.player, check))


def set_rules(world: "RaC3World"):
    # Rules for planets connection
    set_rules_planets(world)

    # Rules for hard to get Location
    set_rules_hard_location(world)

    # world.multiworld.completion_condition[world.player] = lambda state: state.has("Dr. Nefarious Defeated!",
    # world.player)
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Biobliterator Defeated!",
                                                                                  world.player)
