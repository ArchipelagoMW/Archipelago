from dataclasses import dataclass
from enum import Enum
from typing import Optional

from BaseClasses import ItemClassification

CHECK_TYPE = {
    "bit": 0,
    "int": 1,
    "uint": 2,
    "byte": 3,
    "short": 4,
    "falseBit": 5,
    "long": 6,
    "nibble": 7,
}


class CHECKTYPE(Enum):
    """
    What memory size are we checking when reading memory:
    - BIT: a single bit, either 0 or 1
    - BYTE: 8 bits, 0x00 to 0xFF
    - SHORT: 16 bits, 2 bytes, 0x0000 to 0xFFFF
    - INT: 32 bits, 4 bytes, 0x00000000 to 0xFFFFFFFF
    What comparison is being done:
    - set or unset for individual bits
    - Equal, Not Equal, Greater Than, Less Than, Greater or Equal, Less than or Equal
    """
    BIT_SET = 0
    BIT_UNSET = 1
    BYTE_EQ = 2
    BYTE_NE = 3
    BYTE_GT = 4
    BYTE_LT = 5
    BYTE_GE = 6
    BYTE_LE = 7
    SHORT_EQ = 8
    SHORT_NE = 9
    SHORT_GT = 10
    SHORT_LT = 11
    SHORT_GE = 12
    SHORT_LE = 13
    INT_EQ = 14
    INT_NE = 15
    INT_GT = 16
    INT_LT = 17
    INT_GE = 18
    INT_LE = 19


COMPARE_TYPE = {
    "Match": 0,
    "GreaterThan": 1,
    "LessThan": 2,
}


# "Missions": {
#     "First Ranger gives weapon": 0x001426E0,
#     "Second Ranger gives weapon": 0x001426E1,
#     "Zeldrin starport: Find Nefarious": 0x001426E2,
#     "Save Veldin": 0x001426E3,
#     "Veldin: Eliminate the Enemy Forces": 0x001426E4,
#     "Florana: Find the mysterious man": 0x001426E5,
#     "Florana: Walk the path of death!": 0x001426E6,
#     "Defeat Qwark": 0x001426E7,
#     "Take Qwark to Cage": 0x001426E8,
#     "Meet Sasha bridge": 0x001426E9,
#     "Meet Al on Marcadia": 0x001426EA,
#     "Play VidComic1": 0x001426EB,
#     "Marcadia: Get to the Palace": 0x001426EF,
#     "Marcadia: Repair the LDS": 0x001426F1,
#     "Marcadia: Secure the Area": 0x001426F2,
#     "Annihilation Nation: Return": 0x001426F3,
#     "Phoenix Rescue": 0x001426F4,
#     "Annihilation Nation: Grand Prize Bout": 0x001426F5,
#     "Return to Phoenix after Annihilation Nation 2": 0x001426F6,
#     "Aquatos: Infiltrate the Base": 0x001426F7,
#     "Tyhrranosis: Destroy the Plasma Cannon Turrets": 0x001426F9,
#     "Obani Gemini: ???": 0x00142701,
#     "Save Blackwater City": 0x00142704,
#     "Blackwater: Destroy the Base": 0x00142705,
#     "Metropolis: Defeat Klunk": 0x00142708,
#     "Obani Draco: Defeat Courtney Gears": 0x0014270D,
#     "Defeat Dr Nefarious": 0x0014270F,
#     "Destroy the Biobliterator": 0x00142710,  # Doesn't get written to
#     "Holostar: Film Episode": 0x00142712,
#     "Holostar: Return to your ship": 0x00142713,
#     "Metropolis: Complete Ranger Missions": 0x00142714,
#     "Aquatos: Gather Sewer Crystals": 0x00142715,
#     "Tyhrranosis: Destroy the Encampment": 0x00142717,
#     "Tyhrranosis: Destroy the Momma Tyhrranoid": 0x0014271D,
#
# "Enemies":
#     "First of two noids - Mylon Landing Point": 0x001C169E,
#     "Second of two noids - Mylon Landing Point": 0x001C16F4


class RAC3OPTION:
    OPTIONS = "options"
    GAME_TITLE = "Rac3"
    GAME_TITLE_FULL = "Ratchet & Clank 3"
    START_INVENTORY_FROM_POOL = "start_inventory_from_pool"
    STARTING_WEAPONS = "starting_weapons"
    BOLT_AND_XP_MULTIPLIER = "bolt_and_xp_multiplier"
    ENABLE_PROGRESSIVE_WEAPONS = "enable_progressive_weapons"
    EXTRA_ARMOR_UPGRADE = "extra_armor_upgrade"
    SKILL_POINTS = "skill_points"
    TROPHIES = "trophies"
    TITANIUM_BOLTS = "titanium_bolts"
    NANOTECH_MILESTONES = "nanotech_milestones"
    EXCLUDE = "RaC3 Exclude Locations"
    TOTAL_LOCATIONS = "TotalLocations"
    SHIP_NOSE = "Ship Nose"
    SHIP_WINGS = "Ship Wings"
    SHIP_SKIN = "Ship Skin"
    SKIN = "Skin"


class RAC3ITEM:
    AGENTS_OF_DOOM = "Agents of Doom"
    AGENTS_OF_DOOM_V2 = "Agents of Doom V2"
    AGENTS_OF_DOOM_V3 = "Agents of Doom V3"
    AGENTS_OF_DOOM_V4 = "Agents of Doom V4"
    AGENTS_OF_DREAD = "Agents of Dread"
    AGENTS_OF_DREAD_V6 = "Agents of Dread V6"
    AGENTS_OF_DREAD_V7 = "Agents of Dread V7"
    AGENTS_OF_DREAD_V8 = "Agents of Dread V8"
    ANNIHILATOR = "Annihilator"
    ANNIHILATOR_V2 = "Annihilator V2"
    ANNIHILATOR_V3 = "Annihilator V3"
    ANNIHILATOR_V4 = "Annihilator V4"
    DECIMATOR = "Decimator"
    DECIMATOR_V6 = "Decimator V6"
    DECIMATOR_V7 = "Decimator V7"
    DECIMATOR_V8 = "Decimator V8"
    BOLT_GRABBER = "Bolt Grabber V2"
    BOMB_GLOVE = "Bomb Glove"
    BOUNCER = "Bouncer"
    BOUNCER_V2 = "Bouncer V2"
    BOUNCER_V3 = "Bouncer V3"
    BOUNCER_V4 = "Bouncer V4"
    HEAVY_BOUNCER = "Heavy Bouncer"
    HEAVY_BOUNCER_V6 = "Heavy Bouncer V6"
    HEAVY_BOUNCER_V7 = "Heavy Bouncer V7"
    HEAVY_BOUNCER_V8 = "Heavy Bouncer V8"
    BOX_BREAKER = "Box Breaker"
    CHARGE_BOOTS = "Charge Boots"
    COMMANDO_SUIT = "Commando Suit"
    DISC_BLADE = "Disc Blade Gun"
    DISC_BLADE_V2 = "Disc Blade Gun V2"
    DISC_BLADE_V3 = "Disc Blade Gun V3"
    DISC_BLADE_V4 = "Disc Blade Gun V4"
    MULTI_DISC = "Multi-Disc Gun"
    MULTI_DISC_V6 = "Multi-Disc Gun V6"
    MULTI_DISC_V7 = "Multi-Disc Gun V7"
    MULTI_DISC_V8 = "Multi-Disc Gun V8"
    FIRST_PERSON = "First Person"
    FLUX_RIFLE = "Flux Rifle"
    FLUX_RIFLE_V2 = "Flux Rifle V2"
    FLUX_RIFLE_V3 = "Flux Rifle V3"
    FLUX_RIFLE_V4 = "Flux Rifle V4"
    SPLITTER_RIFLE = "Splitter Rifle"
    SPLITTER_RIFLE_V6 = "Splitter Rifle V6"
    SPLITTER_RIFLE_V7 = "Splitter Rifle V7"
    SPLITTER_RIFLE_V8 = "Splitter Rifle V8"
    GLIDER = "Glider"
    GRAV_BOOTS = "Gravity Boots"
    GRIND_BOOTS = "Grind Boots"
    HACKER = "The Hacker"
    HASH = "Hash"
    HELI_PACK = "Heli-Pack"
    HELMET = "Helmet"
    HOLO_SHIELD = "Holo Shield Glove"
    HOLO_SHIELD_V2 = "Holo Shield Glove V2"
    HOLO_SHIELD_V3 = "Holo Shield Glove V3"
    HOLO_SHIELD_V4 = "Holo Shield Glove V4"
    ULTRA_SHIELD = "Ultrashield Launcher"
    ULTRA_SHIELD_V6 = "Ultrashield Launcher V6"
    ULTRA_SHIELD_V7 = "Ultrashield Launcher V7"
    ULTRA_SHIELD_V8 = "Ultrashield Launcher V8"
    HYDRO_PACK = "Hydro Pack"
    HYPERSHOT = "Hypershot"
    INFECTOR = "Infector"
    INFECTOR_V2 = "Infector V2"
    INFECTOR_V3 = "Infector V3"
    INFECTOR_V4 = "Infector V4"
    INFECTO_BOMB = "Infecto-Bomb"
    INFECTO_BOMB_V6 = "Infecto-Bomb V6"
    INFECTO_BOMB_V7 = "Infecto-Bomb V7"
    INFECTO_BOMB_V8 = "Infecto-Bomb V8"
    LAVA_GUN = "Lava Gun"
    LAVA_GUN_V2 = "Lava Gun V2"
    LAVA_GUN_V3 = "Lava Gun V3"
    LAVA_GUN_V4 = "Lava Gun V4"
    LIQUID_NITROGEN = "Liquid Nitrogen Gun"
    LIQUID_NITROGEN_V6 = "Liquid Nitrogen Gun V6"
    LIQUID_NITROGEN_V7 = "Liquid Nitrogen Gun V7"
    LIQUID_NITROGEN_V8 = "Liquid Nitrogen Gun V8"
    LEVITATOR = "Levitator"
    LOCK_STRAFE = "Lock Strafe"
    MAP_O_MATIC = "Map-O-Matic"
    MASTER_PLAN = "Master Plan"
    MINI_TURRET = "Miniturret Glove"
    MINI_TURRET_V2 = "Miniturret Glove V2"
    MINI_TURRET_V3 = "Miniturret Glove V3"
    MINI_TURRET_V4 = "Miniturret Glove V4"
    MEGA_TURRET = "Megaturret Glove"
    MEGA_TURRET_V6 = "Megaturret Glove V6"
    MEGA_TURRET_V7 = "Megaturret Glove V7"
    MEGA_TURRET_V8 = "Megaturret Glove V8"
    MORPH_O_RAY = "Morph-O-Ray"
    N60_STORM = "N60 Storm"
    N60_STORM_V2 = "N60 Storm V2"
    N60_STORM_V3 = "N60 Storm V3"
    N60_STORM_V4 = "N60 Storm V4"
    N90_HURRICANE = "N90 Hurricane"
    N90_HURRICANE_V6 = "N90 Hurricane V6"
    N90_HURRICANE_V7 = "N90 Hurricane V7"
    N90_HURRICANE_V8 = "N90 Hurricane V8"
    NANO_PAK = "Nano-pak"
    NITRO_LAUNCHER = "Nitro Launcher"
    NITRO_LAUNCHER_V2 = "Nitro Launcher V2"
    NITRO_LAUNCHER_V3 = "Nitro Launcher V3"
    NITRO_LAUNCHER_V4 = "Nitro Launcher V4"
    NITRO_ERUPTOR = "Nitro Eruptor"
    NITRO_ERUPTOR_V6 = "Nitro Eruptor V6"
    NITRO_ERUPTOR_V7 = "Nitro Eruptor V7"
    NITRO_ERUPTOR_V8 = "Nitro Eruptor V8"
    PDA = "PDA"
    PLASMA_COIL = "Plasma Coil"
    PLASMA_COIL_V2 = "Plasma Coil V2"
    PLASMA_COIL_V3 = "Plasma Coil V3"
    PLASMA_COIL_V4 = "Plasma Coil V4"
    PLASMA_STORM = "Plasma Storm"
    PLASMA_STORM_V6 = "Plasma Storm V6"
    PLASMA_STORM_V7 = "Plasma Storm V7"
    PLASMA_STORM_V8 = "Plasma Storm V8"
    PLASMA_WHIP = "Plasma Whip"
    PLASMA_WHIP_V2 = "Plasma Whip V2"
    PLASMA_WHIP_V3 = "Plasma Whip V3"
    PLASMA_WHIP_V4 = "Plasma Whip V4"
    QUANTUM_WHIP = "Quantum Whip"
    QUANTUM_WHIP_V6 = "Quantum Whip V6"
    QUANTUM_WHIP_V7 = "Quantum Whip V7"
    QUANTUM_WHIP_V8 = "Quantum Whip V8"
    QWACK_O_RAY = "Qwack-O-Ray"
    QWACK_O_RAY_V2 = "Qwack-O-Ray V2"
    QWACK_O_RAY_V3 = "Qwack-O-Ray V3"
    QWACK_O_RAY_V4 = "Qwack-O-Ray V4"
    QWACK_O_BLITZER = "Qwack-O-Blitzer"
    QWACK_O_BLITZER_V6 = "Qwack-O-Blitzer V6"
    QWACK_O_BLITZER_V7 = "Qwack-O-Blitzer V7"
    QWACK_O_BLITZER_V8 = "Qwack-O-Blitzer V8"
    REFRACTOR = "Refractor"
    RIFT_INDUCER = "Rift Inducer"
    RIFT_INDUCER_V2 = "Rift Inducer V2"
    RIFT_INDUCER_V3 = "Rift Inducer v3"
    RIFT_INDUCER_V4 = "Rift Inducer v4"
    RIFT_RIPPER = "Rift Ripper"
    RIFT_RIPPER_V6 = "Rift Ripper V6"
    RIFT_RIPPER_V7 = "Rift Ripper V7"
    RIFT_RIPPER_V8 = "Rift Ripper V8"
    RY3N0 = "RY3N0"
    RY3NO_V2 = "RY3NO V2"
    RY3NO_V3 = "RY3NO V3"
    RY3NO_V4 = "RY3NO V4"
    RYNOCIRATOR = "RYNOCIRATOR"
    SHIELD_CHARGER = "Shield Charger"
    SHIELD_CHARGER_V2 = "Shield Charger V2"
    SHIELD_CHARGER_V3 = "Shield Charger V3"
    SHIELD_CHARGER_V4 = "Shield Charger V4"
    TESLA_BARRIER = "Tesla Barrier"
    TESLA_BARRIER_V6 = "Tesla Barrier V6"
    TESLA_BARRIER_V7 = "Tesla Barrier V7"
    TESLA_BARRIER_V8 = "Tesla Barrier V8"
    SHOCK_BLASTER = "Shock Blaster"
    SHOCK_BLASTER_V2 = "Shock Blaster V2"
    SHOCK_BLASTER_V3 = "Shock Blaster V3"
    SHOCK_BLASTER_V4 = "Shock Blaster V4"
    SHOCK_CANNON = "Shock Cannon"
    SHOCK_CANNON_V6 = "Shock Cannon V6"
    SHOCK_CANNON_V7 = "Shock Cannon V7"
    SHOCK_CANNON_V8 = "Shock Cannon V8"
    SPITTING_HYDRA = "Spitting Hydra"
    SPITTING_HYDRA_V2 = "Spitting Hydra V2"
    SPITTING_HYDRA_V3 = "Spitting Hydra V3"
    SPITTING_HYDRA_V4 = "Spitting Hydra V4"
    TEMPEST = "Tempest"
    TEMPEST_V6 = "Tempest V6"
    TEMPEST_V7 = "Tempest V7"
    TEMPEST_V8 = "Tempest V8"
    STAR_MAP = "Star Map"
    SUCK_CANNON = "Suck Cannon"
    SUCK_CANNON_V2 = "Suck Cannon V2"
    SUCK_CANNON_V3 = "Suck Cannon V3"
    SUCK_CANNON_V4 = "Suck Cannon V4"
    VORTEX_CANNON = "Vortex Cannon"
    VORTEX_CANNON_V6 = "Vortex Cannon V6"
    VORTEX_CANNON_V7 = "Vortex Cannon V7"
    VORTEX_CANNON_V8 = "Vortex Cannon V8"
    THIRD_PERSON = "Third Person"
    THRUSTER_PACK = "Thruster-Pack"
    TYHRRA_GUISE = "Tyhrra-Guise"
    VIDCOMIC1 = "Qwark VidComic 1"
    VIDCOMIC2 = "Qwark VidComic 2"
    VIDCOMIC3 = "Qwark VidComic 3"
    VIDCOMIC4 = "Qwark VidComic 4"
    VIDCOMIC5 = "Qwark VidComic 5"
    WARP_PAD = "Warp Pad"
    WRENCH = "OmniWrench"
    WRENCH_V2 = "OmniWrench V2"
    WRENCH_V3 = "OmniWrench V3"
    WRENCH_V4 = "OmniWrench V4"
    WRENCH_V5 = "OmniWrench V5"
    WRENCH_V6 = "OmniWrench V6"
    WRENCH_V7 = "OmniWrench V7"
    WRENCH_V8 = "OmniWrench V8"
    GRIND_BOOTS_2 = "Grind Boots 2"
    MAGNAPLATE = "Magnaplate armor"
    ADAMANTINE = "Adamantine armor"
    AEGIS = "Aegis Mark V armor"
    INFERNOX = "Infernox armor"

    PROGRESSIVE_SHOCK_BLASTER = "Progressive Shock Blaster"
    PROGRESSIVE_NITRO_LAUNCHER = "Progressive Nitro Launcher"
    PROGRESSIVE_N60_STORM = "Progressive N60 Storm"
    PROGRESSIVE_PLASMA_WHIP = "Progressive Plasma Whip"
    PROGRESSIVE_INFECTOR = "Progressive Infector"
    PROGRESSIVE_SUCK_CANNON = "Progressive Suck Cannon"
    PROGRESSIVE_SPITTING_HYDRA = "Progressive Spitting Hydra"
    PROGRESSIVE_AGENTS_OF_DOOM = "Progressive Agents of Doom"
    PROGRESSIVE_FLUX_RIFLE = "Progressive Flux Rifle"
    PROGRESSIVE_ANNIHILATOR = "Progressive Annihilator"
    PROGRESSIVE_HOLO_SHIELD = "Progressive Holo Shield Glove"
    PROGRESSIVE_DISC_BLADE = "Progressive Disc Blade Gun"
    PROGRESSIVE_RIFT_INDUCER = "Progressive Rift Inducer"
    PROGRESSIVE_QWACK_O_RAY = "Progressive Qwack-O-Ray"
    PROGRESSIVE_RY3N0 = "Progressive RY3N0"
    PROGRESSIVE_MINI_TURRET = "Progressive Miniturret Glove"
    PROGRESSIVE_LAVA_GUN = "Progressive Lava Gun"
    PROGRESSIVE_SHIELD_CHARGER = "Progressive Shield Charger"
    PROGRESSIVE_BOUNCER = "Progressive Bouncer"
    PROGRESSIVE_PLASMA_COIL = "Progressive Plasma Coil"
    PROGRESSIVE_VIDCOMIC = "Progressive VidComic"
    PROGRESSIVE_ARMOR = "Progressive Armor"

    VELDIN = "Infobot: Veldin"
    FLORANA = "Infobot: Florana"
    STARSHIP_PHOENIX = "Infobot: Starship Phoenix"
    MARCADIA = "Infobot: Marcadia"
    ANNIHILATION_NATION = "Infobot: Annihilation Nation"
    AQUATOS = "Infobot: Aquatos"
    TYHRRANOSIS = "Infobot: Tyhrranosis"
    DAXX = "Infobot: Daxx"
    OBANI_GEMINI = "Infobot: Obani Gemini"
    BLACKWATER_CITY = "Infobot: Blackwater City"
    HOLOSTAR_STUDIOS = "Infobot: Holostar Studios"
    OBANI_DRACO = "Infobot: Obani Draco"
    ZELDRIN_STARPORT = "Infobot: Zeldrin Starport"
    METROPOLIS = "Infobot: Metropolis"
    CRASH_SITE = "Infobot: Crash Site"
    ARIDIA = "Infobot: Aridia"
    QWARKS_HIDEOUT = "Infobot: Qwarks Hideout"
    KOROS = "Infobot: Koros"
    COMMAND_CENTER = "Infobot: Command Center"
    MUSEUM = "Infobot: Museum"

    TITANIUM_BOLT = "Titanium Bolt"
    WEAPON_XP = "Weapon Level-Up"
    PLAYER_XP = "Player EXP"
    BOLTS = "Bolts"
    INFERNO_MODE = "Inferno Mode"
    JACKPOT = "Jackpot"

    MIRROR_TRAP = "Mirror Trap"
    OHKO_TRAP = "Instadeath Trap"
    LOCK_TRAP = "Item Lock Trap"
    WRENCH_TRAP = "Wrench Trap"
    PANCAKE_TRAP = "Pancake Trap"
    LAVA_TRAP = "Lava Trap"

    QUICK_SELECT_0 = "Quick Select 0"
    QUICK_SELECT_1 = "Quick Select 1"
    QUICK_SELECT_2 = "Quick Select 2"
    QUICK_SELECT_3 = "Quick Select 3"
    QUICK_SELECT_4 = "Quick Select 4"
    QUICK_SELECT_5 = "Quick Select 5"
    QUICK_SELECT_6 = "Quick Select 6"
    QUICK_SELECT_7 = "Quick Select 7"
    QUICK_SELECT_8 = "Quick Select 8"
    QUICK_SELECT_9 = "Quick Select 9"
    QUICK_SELECT_A = "Quick Select A"
    QUICK_SELECT_B = "Quick Select B"
    QUICK_SELECT_C = "Quick Select C"
    QUICK_SELECT_D = "Quick Select D"
    QUICK_SELECT_E = "Quick Select E"
    QUICK_SELECT_F = "Quick Select F"

    VICTORY = "Biobliterator Defeated!"


class RAC3REGION:
    MENU = "Menu"
    GALAXY = "Galaxy"
    VELDIN = "Veldin"
    FLORANA = "Florana"
    STARSHIP_PHOENIX = "Starship Phoenix"
    MARCADIA = "Marcadia"
    DAXX = "Daxx"
    PHOENIX_ASSAULT = "Phoenix Assault"
    ANNIHILATION_NATION = "Annihilation Nation"
    ANNIHILATION_NATION_2 = "Annihilation Nation 2"
    AQUATOS = "Aquatos"
    TYHRRANOSIS = "Tyhrranosis"
    ZELDRIN_STARPORT = "Zeldrin Starport"
    OBANI_GEMINI = "Obani Gemini"
    BLACKWATER_CITY = "Blackwater City"
    HOLOSTAR_STUDIOS = "Holostar Studios"
    SKIDD_CUTSCENE = "Skidd Cutscene"
    KOROS = "Koros"
    UNUSED = "Unused"
    METROPOLIS = "Metropolis"
    CRASH_SITE = "Crash Site"
    ARIDIA = "Aridia"
    QWARKS_HIDEOUT = "Qwarks Hideout"
    COMMAND_CENTER_2 = "Command Center 2"
    OBANI_DRACO = "Obani Draco"
    COMMAND_CENTER = "Command Center"
    HOLOSTAR_STUDIOS_CLANK = "Holostar Studios Clank"
    MUSEUM = "Museum"
    UNUSED_2 = "Unused2"
    METROPOLIS_MISSION = "Metropolis: Mission"
    AQUATOS_BASE = "Aquatos Base"
    AQUATOS_SEWERS = "Aquatos Sewers"
    TYHRRANOSIS_MISSION = "Tyhrranosis: Mission"
    QWARK_VID_COMIC_UNUSED_1 = "Qwark VidComic Unused 1"
    QWARK_VID_COMIC_1 = "Qwark VidComic 1"
    QWARK_VID_COMIC_4 = "Qwark VidComic 4"
    QWARK_VID_COMIC_2 = "Qwark VidComic 2"
    QWARK_VID_COMIC_3 = "Qwark VidComic 3"
    QWARK_VID_COMIC_5 = "Qwark VidComic 5"
    QWARK_VID_COMIC_UNUSED_2 = "Qwark VidComic Unused 2"
    NANOTECH = "Nanotech"
    UPGRADES = "Upgrades"
    LONG_TROPHIES = "Long Term Trophy"
    SLOT_0 = "Planet Slot 0x00"
    SLOT_1 = "Planet Slot 0x01"
    SLOT_2 = "Planet Slot 0x02"
    SLOT_3 = "Planet Slot 0x03"
    SLOT_4 = "Planet Slot 0x04"
    SLOT_5 = "Planet Slot 0x05"
    SLOT_6 = "Planet Slot 0x06"
    SLOT_7 = "Planet Slot 0x07"
    SLOT_8 = "Planet Slot 0x08"
    SLOT_9 = "Planet Slot 0x09"
    SLOT_A = "Planet Slot 0x0A"
    SLOT_B = "Planet Slot 0x0B"
    SLOT_C = "Planet Slot 0x0C"
    SLOT_D = "Planet Slot 0x0D"
    SLOT_E = "Planet Slot 0x0E"
    SLOT_F = "Planet Slot 0x0F"
    SLOT_10 = "Planet Slot 0x10"
    SLOT_11 = "Planet Slot 0x11"
    SLOT_12 = "Planet Slot 0x12"
    SLOT_13 = "Planet Slot 0x13"


class RAC3TAG:
    SKILLPOINT = "SkillPoint"
    T_BOLT = "T-Bolt"
    SEWER = "Sewer"
    VIDCOMIC = "VidComic"
    TROPHY = "Trophy"
    LONG_TROPHY = "Long Term Trophy"
    RANGERS = "Rangers"
    ARENA = "Arena"
    NANOTECH = "Nanotech"
    UNSTABLE = "Unstable"
    WEAPONS = "Weapons"
    GADGETS = "Gadgets"
    INFOBOT = "Infobot"


# Todo: Missions, Skill Points, and anything that will trigger an item collection
class RAC3LOCATION:
    pass


class RAC3SKILLPOINT:
    GO_FOR_HANG_TIME = "Go for hang time"  # 0x001D54B0,
    STAY_SQUEAKY_CLEAN = "Stay Squeaky Clean"  # 0x001D54B1,
    ARCADE_PERFECTION = "Strive for arcade perfection"  # 0x001D54B2,
    BEAT_HELGAS_BEST_TIME = "Beat Helga's best time"  # 0x001D54B3,
    TURN_UP_THE_HEAT = "Turn Up The Heat"  # 0x001D54B4,
    MONKEYING_AROUND = "Monkeying around"  # 0x001D54B5,
    REFLECT_TO_SCORE = "Reflect on how to score"  # 0x001D54B6,
    BUGS_TO_BIRDIE = "Bugs to Birdie"  # 0x001D54B7,
    BASH_THE_BUG = "Bash the bug"  # 0x001D54B8,
    EIGHT_TIME_CHAMP = "Be an eight time champ"  # 0x001D54B9,
    FLEE_FLAWLESSLY = "Flee Flawlessly"  # 0x001D54BA,
    LIGHTS_CAMERA_ACTION = "Lights, camera action!"  # 0x001D54BB,
    SUNKEN_TREASURE = "Search for sunken treasure"  # 0x001D54BC,
    BE_A_SHARPSHOOTER = "Be a Sharpshooter"  # 0x001D54BD,
    GET_TO_THE_BELT = "Get to the belt"  # 0x001D54BE,
    BASH_THE_PARTY = "Bash the party"  # 0x001D54BF,
    FEELING_LUCKY = "Feeling Lucky"  # 0x001D54C0,
    YOU_BREAK_IT = "You break it, you win it"  # 0x001D54C1,
    GOOD_YEAR = "2002 was a good year in the city"  # 0x001D54C2,
    SUCK_IT_UP = "Suck it up!"  # 0x001D54C3,
    AIM_HIGH = "Aim High"  # 0x001D54C4,
    ZAP_BACK_AT_YA = "Zap back at ya'"  # 0x001D54C5,
    BREAK_THE_DAN = "Break the Dan"  # 0x001D54C6,
    SPREAD_YOUR_GERMS = "Spread your germs"  # 0x001D54C7,
    HIT_THE_MOTHERLOAD = "Hit the motherload"  # 0x001D54C8,
    PIRATE_BOOTY = "Pirate booty - set a new record for qwark"  # 0x001D54C9,
    DEJA_Q_ALL_OVER_AGAIN = "Deja Q All over Again - set a new record for qwark"  # 0x001D54CA,
    ARRIBA_AMOEBA = "Arriba Amoeba! - set a new record for qwark"  # 0x001D54CB,
    SHADOW_OF_THE_ROBOT = "Shadow of the robot - set a new record for qwark"  # 0x001D54CC,
    THE_SHAMING_OF_THE_Q = "The Shaming of the Q - set a new record for qwark"  # 0x001D54CD,


class RAC3DEATH:
    EATEN = "was Eaten"
    DROWNED = "Drowned"
    FELL = "Fell"
    LAVA = "Drowned"
    FROZEN = "became an Ice cube"


class RAC3STATUS:
    GAME_ID = "SCUS-97353"
    ACTION = 0x001A71A4
    LEVEL_TABLE = 0x001425C0
    BOLTS = 0x00142660
    MAX_HEALTH = 0x00142668
    LAST_USED_0 = 0x00142670
    LAST_USED_1 = 0x00142674
    LAST_USED_2 = 0x00142678
    WRENCH_EQUIPPED = 0x00142690
    CHALLENGE_MODE = 0x00142692
    NANOTECH_EXP = 0x00142694
    ARMOR = 0x001426A0
    HELMET = 0x001426D8
    CRYSTALS = 0x001426A2
    MULTIPLIER = 0x001426BA
    ROBONOIDS = 0x0014275C
    ITEM_AMMO_ADDRESS = 0x001427F0
    ITEM_UNLOCK_ADDRESS = 0x00142CA0
    ITEM_UNLOCK_ADDRESS_2_OFFSET = 0xA0
    ITEM_XP_ADDRESS = 0x00142DE0
    PLANET_SLOT_ADDRESS = 0x00143050
    MAIN_MENU = 0x0016C598
    MAP_CHECK = 0x0016C5A0
    JACKPOT_TIMER = 0x001A4E10
    INFERNO_TIMER = 0x001A4E14
    HOLDING_WEAPON = 0x001A5E08
    HEALTH = 0x001A7430
    JACKPOT = 0x001A74A8
    WEAPON_LOCK = 0x001A74A9
    PAUSE = 0x001CD021
    EQUIPPED = 0x001D4C40
    QUICK_SELECT = 0x001D4C60
    PLANET = 0x001D545C
    SHIP_CONFIG = 0x001D54D0
    SHIP_SKIN = 0x001D54D2
    PLAYER_SKIN = 0x001427AB
    PLAYER_SKIN_2 = 0x001C5D67
    ALLOW_SHIP = 0x001D5533


WEAPON_LIST: list[str] = [
    RAC3ITEM.SHOCK_BLASTER,
    RAC3ITEM.NITRO_LAUNCHER,
    RAC3ITEM.N60_STORM,
    RAC3ITEM.PLASMA_WHIP,
    RAC3ITEM.INFECTOR,
    RAC3ITEM.SUCK_CANNON,
    RAC3ITEM.SPITTING_HYDRA,
    RAC3ITEM.AGENTS_OF_DOOM,
    RAC3ITEM.FLUX_RIFLE,
    RAC3ITEM.ANNIHILATOR,
    RAC3ITEM.HOLO_SHIELD,
    RAC3ITEM.DISC_BLADE,
    RAC3ITEM.RIFT_INDUCER,
    RAC3ITEM.QWACK_O_RAY,
    RAC3ITEM.RY3N0,
    RAC3ITEM.MINI_TURRET,
    RAC3ITEM.LAVA_GUN,
    RAC3ITEM.SHIELD_CHARGER,
    RAC3ITEM.BOUNCER,
    RAC3ITEM.PLASMA_COIL,
]
UPGRADE_DICT: dict[str, list[int]] = {
    RAC3ITEM.SHOCK_BLASTER: [0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E],
    RAC3ITEM.NITRO_LAUNCHER: [0x77, 0x78, 0x79, 0x7A, 0x7B, 0x7C, 0x7D, 0x7E],
    RAC3ITEM.N60_STORM: [0x2F, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36],
    RAC3ITEM.PLASMA_WHIP: [0x7F, 0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86],
    RAC3ITEM.INFECTOR: [0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E],
    RAC3ITEM.SUCK_CANNON: [0x87, 0x88, 0x89, 0x8A, 0x8B, 0x8C, 0x8D, 0x8E],
    RAC3ITEM.SPITTING_HYDRA: [0x47, 0x48, 0x49, 0x4A, 0x4B, 0x4C, 0x4D, 0x4E],
    RAC3ITEM.AGENTS_OF_DOOM: [0x57, 0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E],
    RAC3ITEM.FLUX_RIFLE: [0x6F, 0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76],
    RAC3ITEM.ANNIHILATOR: [0x3F, 0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46],
    RAC3ITEM.HOLO_SHIELD: [0x67, 0x68, 0x69, 0x6A, 0x6B, 0x6C, 0x6D, 0x6E],
    RAC3ITEM.DISC_BLADE: [0x4F, 0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56],
    RAC3ITEM.RIFT_INDUCER: [0x5F, 0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66],
    RAC3ITEM.QWACK_O_RAY: [0x8F, 0x90, 0x91, 0x92, 0x93, 0x94, 0x95, 0x96],
    RAC3ITEM.RY3N0: [0x97, 0x98, 0x99, 0x9A, 0x9B],
    RAC3ITEM.MINI_TURRET: [0x15, 0xA2, 0xA8, 0xA9, 0xAA, 0xAB, 0xAC, 0xAD],
    RAC3ITEM.LAVA_GUN: [0x11, 0xA1, 0xAE, 0xAF, 0xB0, 0xB1, 0xB2, 0xB3],
    RAC3ITEM.SHIELD_CHARGER: [0x16, 0xA7, 0xC0, 0xC1, 0xC2, 0xC3, 0xC4, 0xC5],
    RAC3ITEM.BOUNCER: [0x13, 0xA6, 0xB4, 0xB5, 0xB6, 0xB7, 0xB8, 0xB9],
    RAC3ITEM.PLASMA_COIL: [0x10, 0xA0, 0xBA, 0xBB, 0xBC, 0xBD, 0xBE, 0xBF],
    RAC3ITEM.WRENCH: [0x09, 0xA4, 0xA5, 0xC6, 0xC7, 0xC8, 0xC9, 0xCA]
}
GADGET_LIST: list[str] = [
    RAC3ITEM.HELI_PACK,
    RAC3ITEM.THRUSTER_PACK,
    RAC3ITEM.HACKER,
    RAC3ITEM.HYPERSHOT,
    RAC3ITEM.REFRACTOR,
    RAC3ITEM.TYHRRA_GUISE,
    RAC3ITEM.GRAV_BOOTS,
    RAC3ITEM.BOLT_GRABBER,
    RAC3ITEM.BOX_BREAKER,
    RAC3ITEM.MAP_O_MATIC,
    RAC3ITEM.NANO_PAK,
    RAC3ITEM.WARP_PAD,
    RAC3ITEM.PDA,
    RAC3ITEM.CHARGE_BOOTS,
    RAC3ITEM.STAR_MAP,
    RAC3ITEM.MASTER_PLAN
]
VIDCOMIC_LIST: list[str] = [
    RAC3ITEM.VIDCOMIC1,
    RAC3ITEM.VIDCOMIC2,
    RAC3ITEM.VIDCOMIC3,
    RAC3ITEM.VIDCOMIC4,
    RAC3ITEM.VIDCOMIC5
]
ARMOR_LIST: list[str] = [
    RAC3ITEM.MAGNAPLATE,
    RAC3ITEM.ADAMANTINE,
    RAC3ITEM.AEGIS,
    RAC3ITEM.INFERNOX,
]
PROGRESSIVE_DICT: dict[str, str] = {
    RAC3ITEM.PROGRESSIVE_SHOCK_BLASTER: RAC3ITEM.SHOCK_BLASTER,
    RAC3ITEM.PROGRESSIVE_NITRO_LAUNCHER: RAC3ITEM.NITRO_LAUNCHER,
    RAC3ITEM.PROGRESSIVE_N60_STORM: RAC3ITEM.N60_STORM,
    RAC3ITEM.PROGRESSIVE_PLASMA_WHIP: RAC3ITEM.PLASMA_WHIP,
    RAC3ITEM.PROGRESSIVE_INFECTOR: RAC3ITEM.INFECTOR,
    RAC3ITEM.PROGRESSIVE_SUCK_CANNON: RAC3ITEM.SUCK_CANNON,
    RAC3ITEM.PROGRESSIVE_SPITTING_HYDRA: RAC3ITEM.SPITTING_HYDRA,
    RAC3ITEM.PROGRESSIVE_AGENTS_OF_DOOM: RAC3ITEM.AGENTS_OF_DOOM,
    RAC3ITEM.PROGRESSIVE_FLUX_RIFLE: RAC3ITEM.FLUX_RIFLE,
    RAC3ITEM.PROGRESSIVE_ANNIHILATOR: RAC3ITEM.ANNIHILATOR,
    RAC3ITEM.PROGRESSIVE_HOLO_SHIELD: RAC3ITEM.HOLO_SHIELD,
    RAC3ITEM.PROGRESSIVE_DISC_BLADE: RAC3ITEM.DISC_BLADE,
    RAC3ITEM.PROGRESSIVE_RIFT_INDUCER: RAC3ITEM.RIFT_INDUCER,
    RAC3ITEM.PROGRESSIVE_QWACK_O_RAY: RAC3ITEM.QWACK_O_RAY,
    RAC3ITEM.PROGRESSIVE_RY3N0: RAC3ITEM.RY3N0,
    RAC3ITEM.PROGRESSIVE_MINI_TURRET: RAC3ITEM.MINI_TURRET,
    RAC3ITEM.PROGRESSIVE_LAVA_GUN: RAC3ITEM.LAVA_GUN,
    RAC3ITEM.PROGRESSIVE_SHIELD_CHARGER: RAC3ITEM.SHIELD_CHARGER,
    RAC3ITEM.PROGRESSIVE_BOUNCER: RAC3ITEM.BOUNCER,
    RAC3ITEM.PROGRESSIVE_PLASMA_COIL: RAC3ITEM.PLASMA_COIL,
    RAC3ITEM.PROGRESSIVE_VIDCOMIC: RAC3ITEM.PROGRESSIVE_VIDCOMIC,
    RAC3ITEM.PROGRESSIVE_ARMOR: RAC3ITEM.PROGRESSIVE_ARMOR,
}
EQUIP_LIST: list[str] = [
    *WEAPON_LIST,
    *PROGRESSIVE_DICT.keys(),
    RAC3ITEM.HYPERSHOT,
    RAC3ITEM.REFRACTOR,
    RAC3ITEM.TYHRRA_GUISE,
    RAC3ITEM.WARP_PAD,
    RAC3ITEM.PDA,
]
INFOBOT_LIST: list[str] = [
    RAC3ITEM.VELDIN,
    RAC3ITEM.FLORANA,
    RAC3ITEM.STARSHIP_PHOENIX,
    RAC3ITEM.MARCADIA,
    RAC3ITEM.ANNIHILATION_NATION,
    RAC3ITEM.AQUATOS,
    RAC3ITEM.TYHRRANOSIS,
    RAC3ITEM.DAXX,
    RAC3ITEM.OBANI_GEMINI,
    RAC3ITEM.BLACKWATER_CITY,
    RAC3ITEM.HOLOSTAR_STUDIOS,
    RAC3ITEM.OBANI_DRACO,
    RAC3ITEM.ZELDRIN_STARPORT,
    RAC3ITEM.METROPOLIS,
    RAC3ITEM.CRASH_SITE,
    RAC3ITEM.ARIDIA,
    RAC3ITEM.QWARKS_HIDEOUT,
    RAC3ITEM.KOROS,
    RAC3ITEM.COMMAND_CENTER,
    # RAC3ITEM.MUSEUM,
]
PLANET_FROM_INFOBOT: dict[str, str] = {
    RAC3ITEM.VELDIN: RAC3REGION.VELDIN,
    RAC3ITEM.FLORANA: RAC3REGION.FLORANA,
    RAC3ITEM.STARSHIP_PHOENIX: RAC3REGION.STARSHIP_PHOENIX,
    RAC3ITEM.MARCADIA: RAC3REGION.MARCADIA,
    RAC3ITEM.ANNIHILATION_NATION: RAC3REGION.ANNIHILATION_NATION,
    RAC3ITEM.AQUATOS: RAC3REGION.AQUATOS,
    RAC3ITEM.TYHRRANOSIS: RAC3REGION.TYHRRANOSIS,
    RAC3ITEM.DAXX: RAC3REGION.DAXX,
    RAC3ITEM.OBANI_GEMINI: RAC3REGION.OBANI_GEMINI,
    RAC3ITEM.BLACKWATER_CITY: RAC3REGION.BLACKWATER_CITY,
    RAC3ITEM.HOLOSTAR_STUDIOS: RAC3REGION.HOLOSTAR_STUDIOS,
    RAC3ITEM.OBANI_DRACO: RAC3REGION.OBANI_DRACO,
    RAC3ITEM.ZELDRIN_STARPORT: RAC3REGION.ZELDRIN_STARPORT,
    RAC3ITEM.METROPOLIS: RAC3REGION.METROPOLIS,
    RAC3ITEM.CRASH_SITE: RAC3REGION.CRASH_SITE,
    RAC3ITEM.ARIDIA: RAC3REGION.ARIDIA,
    RAC3ITEM.QWARKS_HIDEOUT: RAC3REGION.QWARKS_HIDEOUT,
    RAC3ITEM.KOROS: RAC3REGION.KOROS,
    RAC3ITEM.COMMAND_CENTER: RAC3REGION.COMMAND_CENTER,
    # RAC3ITEM.MUSEUM = # RAC3REGION.MUSEUM,
}
QUICK_SELECT_LIST: list[str] = [
    RAC3ITEM.QUICK_SELECT_0,
    RAC3ITEM.QUICK_SELECT_1,
    RAC3ITEM.QUICK_SELECT_2,
    RAC3ITEM.QUICK_SELECT_3,
    RAC3ITEM.QUICK_SELECT_4,
    RAC3ITEM.QUICK_SELECT_5,
    RAC3ITEM.QUICK_SELECT_6,
    RAC3ITEM.QUICK_SELECT_7,
    RAC3ITEM.QUICK_SELECT_8,
    RAC3ITEM.QUICK_SELECT_9,
    RAC3ITEM.QUICK_SELECT_A,
    RAC3ITEM.QUICK_SELECT_B,
    RAC3ITEM.QUICK_SELECT_C,
    RAC3ITEM.QUICK_SELECT_D,
    RAC3ITEM.QUICK_SELECT_E,
    RAC3ITEM.QUICK_SELECT_F,
]
SHIP_SLOTS: list[str] = [
    RAC3REGION.SLOT_0,
    RAC3REGION.SLOT_1,
    RAC3REGION.SLOT_2,
    RAC3REGION.SLOT_3,
    RAC3REGION.SLOT_4,
    RAC3REGION.SLOT_5,
    RAC3REGION.SLOT_6,
    RAC3REGION.SLOT_7,
    RAC3REGION.SLOT_8,
    RAC3REGION.SLOT_9,
    RAC3REGION.SLOT_A,
    RAC3REGION.SLOT_B,
    RAC3REGION.SLOT_C,
    RAC3REGION.SLOT_D,
    RAC3REGION.SLOT_E,
    RAC3REGION.SLOT_F,
    RAC3REGION.SLOT_10,
    RAC3REGION.SLOT_11,
    RAC3REGION.SLOT_12,
    RAC3REGION.SLOT_13
]
PLANET_NAME_FROM_ID: dict[int, str] = {
    0x01: RAC3REGION.VELDIN,
    0x02: RAC3REGION.FLORANA,
    0x03: RAC3REGION.STARSHIP_PHOENIX,
    0x04: RAC3REGION.MARCADIA,
    0x05: RAC3REGION.DAXX,
    0x07: RAC3REGION.ANNIHILATION_NATION,
    0x08: RAC3REGION.AQUATOS,
    0x09: RAC3REGION.TYHRRANOSIS,
    0x0A: RAC3REGION.ZELDRIN_STARPORT,
    0x0B: RAC3REGION.OBANI_GEMINI,
    0x0C: RAC3REGION.BLACKWATER_CITY,
    0x0D: RAC3REGION.HOLOSTAR_STUDIOS,
    0x0E: RAC3REGION.KOROS,
    0x10: RAC3REGION.METROPOLIS,
    0x11: RAC3REGION.CRASH_SITE,
    0x12: RAC3REGION.ARIDIA,
    0x13: RAC3REGION.QWARKS_HIDEOUT,
    0x15: RAC3REGION.OBANI_DRACO,
    0x16: RAC3REGION.COMMAND_CENTER,
    0x18: RAC3REGION.MUSEUM,
    0x00: RAC3REGION.GALAXY,
    0x06: RAC3REGION.PHOENIX_ASSAULT,
    0x0F: RAC3REGION.UNUSED,
    0x14: RAC3REGION.COMMAND_CENTER_2,
    0x17: RAC3REGION.HOLOSTAR_STUDIOS_CLANK,
    0x19: RAC3REGION.UNUSED_2,
    0x1A: RAC3REGION.METROPOLIS_MISSION,
    0x1B: RAC3REGION.AQUATOS_BASE,
    0x1C: RAC3REGION.AQUATOS_SEWERS,
    0x1D: RAC3REGION.TYHRRANOSIS_MISSION,
    0x1E: RAC3REGION.QWARK_VID_COMIC_UNUSED_1,
    0x1F: RAC3REGION.QWARK_VID_COMIC_1,
    0x20: RAC3REGION.QWARK_VID_COMIC_4,
    0x21: RAC3REGION.QWARK_VID_COMIC_2,
    0x22: RAC3REGION.QWARK_VID_COMIC_3,
    0x23: RAC3REGION.QWARK_VID_COMIC_5,
    0x24: RAC3REGION.QWARK_VID_COMIC_UNUSED_2,
}
FILLER_LIST: list[str] = [
    RAC3ITEM.TITANIUM_BOLT,
    RAC3ITEM.WEAPON_XP,
    RAC3ITEM.PLAYER_XP,
    RAC3ITEM.BOLTS,
    RAC3ITEM.INFERNO_MODE,
    RAC3ITEM.JACKPOT,
]
SIMPLE_SKILL_POINTS = [
    RAC3SKILLPOINT.REFLECT_TO_SCORE,
    RAC3SKILLPOINT.LIGHTS_CAMERA_ACTION,
    RAC3SKILLPOINT.SUNKEN_TREASURE,
    RAC3SKILLPOINT.BE_A_SHARPSHOOTER,
    RAC3SKILLPOINT.BUGS_TO_BIRDIE,
    RAC3SKILLPOINT.GET_TO_THE_BELT,
    RAC3SKILLPOINT.BASH_THE_PARTY,
    RAC3SKILLPOINT.GOOD_YEAR,
    RAC3SKILLPOINT.AIM_HIGH,
    RAC3SKILLPOINT.SUCK_IT_UP,
    RAC3SKILLPOINT.GO_FOR_HANG_TIME,
    RAC3SKILLPOINT.ZAP_BACK_AT_YA,
    RAC3SKILLPOINT.BREAK_THE_DAN,
    RAC3SKILLPOINT.YOU_BREAK_IT,
    RAC3SKILLPOINT.SPREAD_YOUR_GERMS,
    # RAC3SKILLPOINT.STAY_SQUEAKY_CLEAN,
    # RAC3SKILLPOINT.MONKEYING_AROUND,
    # RAC3SKILLPOINT.BEAT_HELGAS_BEST_TIME,
    # RAC3SKILLPOINT.TURN_UP_THE_HEAT,
    # RAC3SKILLPOINT.FLEE_FLAWLESSLY,
    # RAC3SKILLPOINT.BASH_THE_BUG,
    # RAC3SKILLPOINT.FEELING_LUCKY,
    # RAC3SKILLPOINT.EIGHT_TIME_CHAMP,
    # RAC3SKILLPOINT.HIT_THE_MOTHERLOAD,
    # RAC3SKILLPOINT.PIRATE_BOOTY,
    # RAC3SKILLPOINT.DEJA_Q_ALL_OVER_AGAIN,
    # RAC3SKILLPOINT.ARRIBA_AMOEBA,
    # RAC3SKILLPOINT.SHADOW_OF_THE_ROBOT,
    # RAC3SKILLPOINT.THE_SHAMING_OF_THE_Q,
    # RAC3SKILLPOINT.ARCADE_PERFECTION,
]
DEATH_FROM_ACTION: dict[int, str] = {
    0x31: RAC3DEATH.EATEN,
    0x6C: RAC3DEATH.DROWNED,
    0x79: RAC3DEATH.FELL,
    0x7E: RAC3DEATH.LAVA,
    0x81: RAC3DEATH.FROZEN
}


@dataclass
class RAC3STATUSDATA:
    SLOT_ADDRESS = None

    def __init__(self, slot: Optional[int] = None):
        self.SLOT_ADDRESS: int = 4 * slot + RAC3STATUS.QUICK_SELECT


@dataclass
class RAC3ITEMDATA:
    ID = None
    LEVEL = None
    LEVEL_ADDRESS = None
    UNLOCK_ADDRESS = None
    UNLOCK_ADDRESS_2 = None
    XP_ADDRESS = None
    XP_THRESHOLD = None
    POWER = None
    ARMOR = None
    AMMO_ADDRESS = None
    AMMO = None
    AP_CODE = None
    AP_CLASSIFICATION = None

    def __init__(self,
                 idx: int,
                 address: Optional[int] = None,
                 address_2: Optional[int] = None,
                 power: Optional[int] = None,
                 ammo: Optional[int] = None,
                 xp: Optional[int] = None,
                 level: Optional[int] = None,
                 level_address: Optional[int] = None,
                 armor: Optional[float] = None,
                 ap_classification: Optional[ItemClassification] = ItemClassification.filler):
        self.ID: int = idx
        self.AP_CODE: int = idx + 50000000
        self.AP_CLASSIFICATION: ItemClassification = ap_classification
        self.LEVEL: Optional[int] = level
        self.LEVEL_ADDRESS: Optional[int] = level_address
        self.UNLOCK_ADDRESS: Optional[int] = address
        self.UNLOCK_ADDRESS_2: Optional[int] = address_2
        self.XP_ADDRESS: int = 4 * idx + RAC3STATUS.ITEM_XP_ADDRESS
        self.XP_THRESHOLD: Optional[int] = xp
        self.POWER: Optional[int] = power
        self.ARMOR: Optional[float] = armor
        self.AMMO_ADDRESS: int = 4 * idx + RAC3STATUS.ITEM_AMMO_ADDRESS
        self.AMMO: Optional[int] = ammo

    @staticmethod
    def construct_unused(idx: int,
                         ammo: Optional[int] = None):
        return RAC3ITEMDATA(idx, ammo=ammo)

    @staticmethod
    def construct_gadget(idx: int,
                         ap_classification: ItemClassification):
        address: int = idx + RAC3STATUS.ITEM_UNLOCK_ADDRESS
        address_2: int = address + RAC3STATUS.ITEM_UNLOCK_ADDRESS_2_OFFSET
        return RAC3ITEMDATA(idx, address, address_2, ap_classification=ap_classification)

    @staticmethod
    def construct_weapon(idx: int,
                         power: int,
                         ammo: Optional[int] = None,
                         ap_classification: Optional[ItemClassification] = None):
        address: int = idx + RAC3STATUS.ITEM_UNLOCK_ADDRESS
        address_2: int = address + RAC3STATUS.ITEM_UNLOCK_ADDRESS_2_OFFSET
        return RAC3ITEMDATA(idx, address, address_2, power, ammo, level=1, level_address=idx + RAC3STATUS.LEVEL_TABLE,
                            ap_classification=ap_classification)

    @staticmethod
    def construct_weapon_level(idx: int,
                               power: int,
                               ammo: Optional[int] = None,
                               xp: Optional[int] = 0):
        base: int = [weapon[0] for weapon in UPGRADE_DICT.values() if idx in weapon][-1]
        amount: int = 32 * xp
        return RAC3ITEMDATA(idx, power=power, ammo=ammo, xp=amount, level=idx - base,
                            level_address=base + RAC3STATUS.LEVEL_TABLE)

    @staticmethod
    def construct_weapon_prog(idx: int,
                              ap_classification: ItemClassification):
        address: int = (idx - 0xCB) * 8 + 0x27 + RAC3STATUS.ITEM_UNLOCK_ADDRESS
        address_2: int = address + RAC3STATUS.ITEM_UNLOCK_ADDRESS_2_OFFSET
        return RAC3ITEMDATA(idx, address, address_2, ap_classification=ap_classification)

    @staticmethod
    def construct_rac2_prog(idx: int,
                            ap_classification: ItemClassification):
        address: int = idx - 0xCA + RAC3STATUS.ITEM_UNLOCK_ADDRESS
        address_2: int = address + RAC3STATUS.ITEM_UNLOCK_ADDRESS_2_OFFSET
        return RAC3ITEMDATA(idx, address, address_2, ap_classification=ap_classification)

    @staticmethod
    def construct_infobot(idx: int,
                          ap_classification: ItemClassification):
        return RAC3ITEMDATA(idx, ap_classification=ap_classification)

    @staticmethod
    def construct_armor(idx: int,
                        ap_classification: ItemClassification,
                        armor: int):
        address: int = RAC3STATUS.ARMOR
        reduction: float = armor / 30
        return RAC3ITEMDATA(idx, address, armor=reduction, ap_classification=ap_classification)

    @staticmethod
    def construct_vidcomic(idx: int):
        address = idx + 0x001D5454
        return RAC3ITEMDATA(idx, address, ap_classification=ItemClassification.progression)

    @staticmethod
    def construct_other(idx: int,
                        address: Optional[int] = None):
        return RAC3ITEMDATA(idx, address, ap_classification=ItemClassification.filler)

    @staticmethod
    def construct_goal(idx: int):
        return RAC3ITEMDATA(idx, ap_classification=ItemClassification.progression)


@dataclass
class RAC3REGIONDATA:
    ID: int = None
    SLOT_ADDRESS: Optional[int] = None

    def __init__(self,
                 idx: Optional[int] = None,
                 slot: Optional[int] = None):
        self.ID: Optional[int] = idx
        self.SLOT_ADDRESS: Optional[int] = slot

    @staticmethod
    def construct_slot(slot: int):
        idx: int = slot + 1
        addr: int = 4 * slot + RAC3STATUS.PLANET_SLOT_ADDRESS
        return RAC3REGIONDATA(idx, addr)


RAC3_ITEM_DATA_TABLE: dict[str, RAC3ITEMDATA] = {
    # Items
    # 0x01
    RAC3ITEM.HELI_PACK: RAC3ITEMDATA.construct_gadget(0x02, ap_classification=ItemClassification.useful),
    RAC3ITEM.THRUSTER_PACK: RAC3ITEMDATA.construct_gadget(0x03, ap_classification=ItemClassification.useful),
    RAC3ITEM.HYDRO_PACK: RAC3ITEMDATA.construct_unused(0x04),  # Unused
    RAC3ITEM.MAP_O_MATIC: RAC3ITEMDATA.construct_gadget(0x05, ap_classification=ItemClassification.useful),
    RAC3ITEM.COMMANDO_SUIT: RAC3ITEMDATA.construct_unused(0x06),  # Unused
    RAC3ITEM.BOLT_GRABBER: RAC3ITEMDATA.construct_gadget(0x07, ap_classification=ItemClassification.useful),
    RAC3ITEM.LEVITATOR: RAC3ITEMDATA.construct_unused(0x08),  # Unused
    RAC3ITEM.WRENCH: RAC3ITEMDATA.construct_unused(0x09),
    RAC3ITEM.BOMB_GLOVE: RAC3ITEMDATA.construct_unused(0x0A, 40),  # Unused
    RAC3ITEM.HYPERSHOT: RAC3ITEMDATA.construct_gadget(0x0B, ap_classification=ItemClassification.progression),
    RAC3ITEM.MORPH_O_RAY: RAC3ITEMDATA.construct_unused(0x0C),  # Unused
    RAC3ITEM.GRAV_BOOTS: RAC3ITEMDATA.construct_gadget(0x0D, ap_classification=ItemClassification.progression),
    RAC3ITEM.GRIND_BOOTS: RAC3ITEMDATA.construct_unused(0x0E),  # Unused
    RAC3ITEM.GLIDER: RAC3ITEMDATA.construct_unused(0x0F),  # Unused
    RAC3ITEM.PLASMA_COIL:
        RAC3ITEMDATA.construct_weapon(0x10, 2400, 15, ap_classification=ItemClassification.useful),
    RAC3ITEM.LAVA_GUN: RAC3ITEMDATA.construct_weapon(0x11, 160, 150, ap_classification=ItemClassification.useful),
    RAC3ITEM.REFRACTOR: RAC3ITEMDATA.construct_gadget(0x12, ap_classification=ItemClassification.progression),
    RAC3ITEM.BOUNCER: RAC3ITEMDATA.construct_weapon(0x13, 1200, 10, ap_classification=ItemClassification.useful),
    RAC3ITEM.HACKER: RAC3ITEMDATA.construct_gadget(0x14, ap_classification=ItemClassification.progression),
    RAC3ITEM.MINI_TURRET:
        RAC3ITEMDATA.construct_weapon(0x15, 600, 10, ap_classification=ItemClassification.useful),
    RAC3ITEM.SHIELD_CHARGER:
        RAC3ITEMDATA.construct_weapon(0x16, 60, 3, ap_classification=ItemClassification.useful),
    # 0x17 Set on new file, Empty Hand
    RAC3ITEM.HELMET: RAC3ITEMDATA.construct_unused(0x18),  # Unused
    # 0x19 SEVERE CRASH RISK
    RAC3ITEM.BOX_BREAKER: RAC3ITEMDATA.construct_gadget(0x1A, ap_classification=ItemClassification.progression),
    RAC3ITEM.HASH: RAC3ITEMDATA.construct_unused(0x1B),  # Unused
    RAC3ITEM.GRIND_BOOTS_2: RAC3ITEMDATA.construct_unused(0x1C),  # Unused
    RAC3ITEM.CHARGE_BOOTS: RAC3ITEMDATA.construct_gadget(0x1D, ap_classification=ItemClassification.progression),
    RAC3ITEM.TYHRRA_GUISE: RAC3ITEMDATA.construct_gadget(0x1E, ap_classification=ItemClassification.progression),
    RAC3ITEM.WARP_PAD: RAC3ITEMDATA.construct_gadget(0x1F, ap_classification=ItemClassification.progression),
    RAC3ITEM.NANO_PAK: RAC3ITEMDATA.construct_gadget(0x20, ap_classification=ItemClassification.useful),
    RAC3ITEM.STAR_MAP: RAC3ITEMDATA.construct_gadget(0x21, ap_classification=ItemClassification.progression),
    RAC3ITEM.MASTER_PLAN: RAC3ITEMDATA.construct_gadget(0x22, ap_classification=ItemClassification.progression),
    RAC3ITEM.PDA: RAC3ITEMDATA.construct_gadget(0x23, ap_classification=ItemClassification.useful),
    RAC3ITEM.THIRD_PERSON: RAC3ITEMDATA.construct_unused(0x24),
    RAC3ITEM.FIRST_PERSON: RAC3ITEMDATA.construct_unused(0x25),
    RAC3ITEM.LOCK_STRAFE: RAC3ITEMDATA.construct_unused(0x26),
    RAC3ITEM.SHOCK_BLASTER: RAC3ITEMDATA.construct_weapon(0x27, 40, 30, ap_classification=ItemClassification.useful),
    RAC3ITEM.SHOCK_BLASTER_V2: RAC3ITEMDATA.construct_weapon_level(0x28, 50, 35, 150),
    RAC3ITEM.SHOCK_BLASTER_V3: RAC3ITEMDATA.construct_weapon_level(0x29, 60, 40, 400),
    RAC3ITEM.SHOCK_BLASTER_V4: RAC3ITEMDATA.construct_weapon_level(0x2A, 80, 40, 700),
    RAC3ITEM.SHOCK_CANNON: RAC3ITEMDATA.construct_weapon_level(0x2B, 100, 50, 1000),
    RAC3ITEM.SHOCK_CANNON_V6: RAC3ITEMDATA.construct_weapon_level(0x2C, 1100, 50),
    RAC3ITEM.SHOCK_CANNON_V7: RAC3ITEMDATA.construct_weapon_level(0x2D, 1400, 55, 10000),
    RAC3ITEM.SHOCK_CANNON_V8: RAC3ITEMDATA.construct_weapon_level(0x2E, 2100, 60, 25000),
    RAC3ITEM.N60_STORM: RAC3ITEMDATA.construct_weapon(0x2F, 150, 150, ap_classification=ItemClassification.useful),
    RAC3ITEM.N60_STORM_V2: RAC3ITEMDATA.construct_weapon_level(0x30, 175, 175, 200),
    RAC3ITEM.N60_STORM_V3: RAC3ITEMDATA.construct_weapon_level(0x31, 200, 200, 500),
    RAC3ITEM.N60_STORM_V4: RAC3ITEMDATA.construct_weapon_level(0x32, 250, 225, 1500),
    RAC3ITEM.N90_HURRICANE: RAC3ITEMDATA.construct_weapon_level(0x33, 350, 300, 3300),
    RAC3ITEM.N90_HURRICANE_V6: RAC3ITEMDATA.construct_weapon_level(0x34, 3500, 300),
    RAC3ITEM.N90_HURRICANE_V7: RAC3ITEMDATA.construct_weapon_level(0x35, 5000, 350, 15000),
    RAC3ITEM.N90_HURRICANE_V8: RAC3ITEMDATA.construct_weapon_level(0x36, 6000, 400, 37500),
    RAC3ITEM.INFECTOR: RAC3ITEMDATA.construct_weapon(0x37, 180, 15, ap_classification=ItemClassification.progression),
    RAC3ITEM.INFECTOR_V2: RAC3ITEMDATA.construct_weapon_level(0x38, 240, 15, 400),
    RAC3ITEM.INFECTOR_V3: RAC3ITEMDATA.construct_weapon_level(0x39, 320, 18, 800),
    RAC3ITEM.INFECTOR_V4: RAC3ITEMDATA.construct_weapon_level(0x3A, 400, 18, 2000),
    RAC3ITEM.INFECTO_BOMB: RAC3ITEMDATA.construct_weapon_level(0x3B, 600, 20, 3800),
    RAC3ITEM.INFECTO_BOMB_V6: RAC3ITEMDATA.construct_weapon_level(0x3C, 4000, 20),
    RAC3ITEM.INFECTO_BOMB_V7: RAC3ITEMDATA.construct_weapon_level(0x3D, 5000, 25, 10000),
    RAC3ITEM.INFECTO_BOMB_V8: RAC3ITEMDATA.construct_weapon_level(0x3E, 6000, 30, 15000),
    RAC3ITEM.ANNIHILATOR:
        RAC3ITEMDATA.construct_weapon(0x3F, 500, 20, ap_classification=ItemClassification.progression),
    RAC3ITEM.ANNIHILATOR_V2: RAC3ITEMDATA.construct_weapon_level(0x40, 600, 20, 800),
    RAC3ITEM.ANNIHILATOR_V3: RAC3ITEMDATA.construct_weapon_level(0x41, 800, 20, 2400),
    RAC3ITEM.ANNIHILATOR_V4: RAC3ITEMDATA.construct_weapon_level(0x42, 1100, 22, 6400),
    RAC3ITEM.DECIMATOR: RAC3ITEMDATA.construct_weapon_level(0x43, 1400, 25, 12400),
    RAC3ITEM.DECIMATOR_V6: RAC3ITEMDATA.construct_weapon_level(0x44, 3000, 25),
    RAC3ITEM.DECIMATOR_V7: RAC3ITEMDATA.construct_weapon_level(0x45, 4000, 28, 10000),
    RAC3ITEM.DECIMATOR_V8: RAC3ITEMDATA.construct_weapon_level(0x46, 5000, 30, 25000),
    RAC3ITEM.SPITTING_HYDRA:
        RAC3ITEMDATA.construct_weapon(0x47, 200, 15, ap_classification=ItemClassification.progression),
    RAC3ITEM.SPITTING_HYDRA_V2: RAC3ITEMDATA.construct_weapon_level(0x48, 240, 15, 300),
    RAC3ITEM.SPITTING_HYDRA_V3: RAC3ITEMDATA.construct_weapon_level(0x49, 280, 15, 900),
    RAC3ITEM.SPITTING_HYDRA_V4: RAC3ITEMDATA.construct_weapon_level(0x4A, 320, 15, 1800),
    RAC3ITEM.TEMPEST: RAC3ITEMDATA.construct_weapon_level(0x4B, 400, 15, 3000),
    RAC3ITEM.TEMPEST_V6: RAC3ITEMDATA.construct_weapon_level(0x4C, 3200, 15),
    RAC3ITEM.TEMPEST_V7: RAC3ITEMDATA.construct_weapon_level(0x4D, 5400, 18, 15000),
    RAC3ITEM.TEMPEST_V8: RAC3ITEMDATA.construct_weapon_level(0x4E, 6000, 20, 37500),
    RAC3ITEM.DISC_BLADE: RAC3ITEMDATA.construct_weapon(0x4F, 500, 25, ap_classification=ItemClassification.progression),
    RAC3ITEM.DISC_BLADE_V2: RAC3ITEMDATA.construct_weapon_level(0x50, 600, 25, 700),
    RAC3ITEM.DISC_BLADE_V3: RAC3ITEMDATA.construct_weapon_level(0x51, 1400, 25, 2100),
    RAC3ITEM.DISC_BLADE_V4: RAC3ITEMDATA.construct_weapon_level(0x52, 2400, 25, 6100),
    RAC3ITEM.MULTI_DISC: RAC3ITEMDATA.construct_weapon_level(0x53, 3600, 25, 12100),
    RAC3ITEM.MULTI_DISC_V6: RAC3ITEMDATA.construct_weapon_level(0x54, 4400, 25),
    RAC3ITEM.MULTI_DISC_V7: RAC3ITEMDATA.construct_weapon_level(0x55, 5600, 28, 10000),
    RAC3ITEM.MULTI_DISC_V8: RAC3ITEMDATA.construct_weapon_level(0x56, 8400, 30, 25000),
    RAC3ITEM.AGENTS_OF_DOOM: RAC3ITEMDATA.construct_weapon(0x57, 240, 6, ap_classification=ItemClassification.useful),
    RAC3ITEM.AGENTS_OF_DOOM_V2: RAC3ITEMDATA.construct_weapon_level(0x58, 400, 6, 400),
    RAC3ITEM.AGENTS_OF_DOOM_V3: RAC3ITEMDATA.construct_weapon_level(0x59, 660, 6, 1000),
    RAC3ITEM.AGENTS_OF_DOOM_V4: RAC3ITEMDATA.construct_weapon_level(0x5A, 2000, 8, 3000),
    RAC3ITEM.AGENTS_OF_DREAD: RAC3ITEMDATA.construct_weapon_level(0x5B, 6000, 8, 6000),
    RAC3ITEM.AGENTS_OF_DREAD_V6: RAC3ITEMDATA.construct_weapon_level(0x5C, 8000, 8),
    RAC3ITEM.AGENTS_OF_DREAD_V7: RAC3ITEMDATA.construct_weapon_level(0x5D, 10000, 10, 7500),
    RAC3ITEM.AGENTS_OF_DREAD_V8: RAC3ITEMDATA.construct_weapon_level(0x5E, 12000, 12, 20000),
    RAC3ITEM.RIFT_INDUCER:
        RAC3ITEMDATA.construct_weapon(0x5F, 1000, 8, ap_classification=ItemClassification.progression),
    RAC3ITEM.RIFT_INDUCER_V2: RAC3ITEMDATA.construct_weapon_level(0x60, 1300, 8, 800),
    RAC3ITEM.RIFT_INDUCER_V3: RAC3ITEMDATA.construct_weapon_level(0x61, 1500, 10, 2400),
    RAC3ITEM.RIFT_INDUCER_V4: RAC3ITEMDATA.construct_weapon_level(0x62, 1700, 10, 6400),
    RAC3ITEM.RIFT_RIPPER: RAC3ITEMDATA.construct_weapon_level(0x63, 2000, 12, 12400),
    RAC3ITEM.RIFT_RIPPER_V6: RAC3ITEMDATA.construct_weapon_level(0x64, 4000, 12),
    RAC3ITEM.RIFT_RIPPER_V7: RAC3ITEMDATA.construct_weapon_level(0x65, 5000, 14, 15000),
    RAC3ITEM.RIFT_RIPPER_V8: RAC3ITEMDATA.construct_weapon_level(0x66, 6000, 16, 37500),
    RAC3ITEM.HOLO_SHIELD: RAC3ITEMDATA.construct_weapon(0x67, 200, 8, ap_classification=ItemClassification.useful),
    RAC3ITEM.HOLO_SHIELD_V2: RAC3ITEMDATA.construct_weapon_level(0x68, 300, 8, 150),
    RAC3ITEM.HOLO_SHIELD_V3: RAC3ITEMDATA.construct_weapon_level(0x69, 400, 10, 450),
    RAC3ITEM.HOLO_SHIELD_V4: RAC3ITEMDATA.construct_weapon_level(0x6A, 500, 10, 1350),
    RAC3ITEM.ULTRA_SHIELD: RAC3ITEMDATA.construct_weapon_level(0x6B, 600, 12, 2700),
    RAC3ITEM.ULTRA_SHIELD_V6: RAC3ITEMDATA.construct_weapon_level(0x6C, 1000, 12),
    RAC3ITEM.ULTRA_SHIELD_V7: RAC3ITEMDATA.construct_weapon_level(0x6D, 1500, 12, 5000),
    RAC3ITEM.ULTRA_SHIELD_V8: RAC3ITEMDATA.construct_weapon_level(0x6E, 2000, 14, 12500),
    RAC3ITEM.FLUX_RIFLE: RAC3ITEMDATA.construct_weapon(0x6F, 300, 10, ap_classification=ItemClassification.progression),
    RAC3ITEM.FLUX_RIFLE_V2: RAC3ITEMDATA.construct_weapon_level(0x70, 400, 12, 200),
    RAC3ITEM.FLUX_RIFLE_V3: RAC3ITEMDATA.construct_weapon_level(0x71, 500, 12, 600),
    RAC3ITEM.FLUX_RIFLE_V4: RAC3ITEMDATA.construct_weapon_level(0x72, 1600, 12, 1500),
    RAC3ITEM.SPLITTER_RIFLE: RAC3ITEMDATA.construct_weapon_level(0x73, 2800, 15, 2900),
    RAC3ITEM.SPLITTER_RIFLE_V6: RAC3ITEMDATA.construct_weapon_level(0x74, 5200, 15),
    RAC3ITEM.SPLITTER_RIFLE_V7: RAC3ITEMDATA.construct_weapon_level(0x75, 7000, 18, 7500),
    RAC3ITEM.SPLITTER_RIFLE_V8: RAC3ITEMDATA.construct_weapon_level(0x76, 8400, 20, 20000),
    RAC3ITEM.NITRO_LAUNCHER: RAC3ITEMDATA.construct_weapon(0x77, 200, 8, ap_classification=ItemClassification.useful),
    RAC3ITEM.NITRO_LAUNCHER_V2: RAC3ITEMDATA.construct_weapon_level(0x78, 240, 8, 200),
    RAC3ITEM.NITRO_LAUNCHER_V3: RAC3ITEMDATA.construct_weapon_level(0x79, 300, 10, 500),
    RAC3ITEM.NITRO_LAUNCHER_V4: RAC3ITEMDATA.construct_weapon_level(0x7A, 400, 10, 1100),
    RAC3ITEM.NITRO_ERUPTOR: RAC3ITEMDATA.construct_weapon_level(0x7B, 800, 12, 2600),
    RAC3ITEM.NITRO_ERUPTOR_V6: RAC3ITEMDATA.construct_weapon_level(0x7C, 4200, 12),
    RAC3ITEM.NITRO_ERUPTOR_V7: RAC3ITEMDATA.construct_weapon_level(0x7D, 5000, 14, 7500),
    RAC3ITEM.NITRO_ERUPTOR_V8: RAC3ITEMDATA.construct_weapon_level(0x7E, 6000, 16, 20000),
    RAC3ITEM.PLASMA_WHIP: RAC3ITEMDATA.construct_weapon(0x7F, 40, 25, ap_classification=ItemClassification.progression),
    RAC3ITEM.PLASMA_WHIP_V2: RAC3ITEMDATA.construct_weapon_level(0x80, 50, 30, 200),
    RAC3ITEM.PLASMA_WHIP_V3: RAC3ITEMDATA.construct_weapon_level(0x81, 70, 35, 800),
    RAC3ITEM.PLASMA_WHIP_V4: RAC3ITEMDATA.construct_weapon_level(0x82, 100, 40, 1800),
    RAC3ITEM.QUANTUM_WHIP: RAC3ITEMDATA.construct_weapon_level(0x83, 140, 40, 3300),
    RAC3ITEM.QUANTUM_WHIP_V6: RAC3ITEMDATA.construct_weapon_level(0x84, 1400, 50),
    RAC3ITEM.QUANTUM_WHIP_V7: RAC3ITEMDATA.construct_weapon_level(0x85, 1800, 55, 10000),
    RAC3ITEM.QUANTUM_WHIP_V8: RAC3ITEMDATA.construct_weapon_level(0x86, 2400, 60, 25000),
    RAC3ITEM.SUCK_CANNON: RAC3ITEMDATA.construct_weapon(0x87, 200, ap_classification=ItemClassification.progression),
    RAC3ITEM.SUCK_CANNON_V2: RAC3ITEMDATA.construct_weapon_level(0x88, 260, xp=200),
    RAC3ITEM.SUCK_CANNON_V3: RAC3ITEMDATA.construct_weapon_level(0x89, 320, xp=600),
    RAC3ITEM.SUCK_CANNON_V4: RAC3ITEMDATA.construct_weapon_level(0x8A, 400, xp=1200),
    RAC3ITEM.VORTEX_CANNON: RAC3ITEMDATA.construct_weapon_level(0x8B, 600, xp=2000),
    RAC3ITEM.VORTEX_CANNON_V6: RAC3ITEMDATA.construct_weapon_level(0x8C, 4200),
    RAC3ITEM.VORTEX_CANNON_V7: RAC3ITEMDATA.construct_weapon_level(0x8D, 5000, xp=5000),
    RAC3ITEM.VORTEX_CANNON_V8: RAC3ITEMDATA.construct_weapon_level(0x8E, 6000, xp=12500),
    RAC3ITEM.QWACK_O_RAY: RAC3ITEMDATA.construct_weapon(0x8F, 1000, ap_classification=ItemClassification.progression),
    RAC3ITEM.QWACK_O_RAY_V2: RAC3ITEMDATA.construct_weapon_level(0x90, 1500, xp=1000),
    RAC3ITEM.QWACK_O_RAY_V3: RAC3ITEMDATA.construct_weapon_level(0x91, 2000, xp=3000),
    RAC3ITEM.QWACK_O_RAY_V4: RAC3ITEMDATA.construct_weapon_level(0x92, 2500, xp=8000),
    RAC3ITEM.QWACK_O_BLITZER: RAC3ITEMDATA.construct_weapon_level(0x93, 3000, xp=16000),
    RAC3ITEM.QWACK_O_BLITZER_V6: RAC3ITEMDATA.construct_weapon_level(0x94, 4000),
    RAC3ITEM.QWACK_O_BLITZER_V7: RAC3ITEMDATA.construct_weapon_level(0x95, 5000, xp=10000),
    RAC3ITEM.QWACK_O_BLITZER_V8: RAC3ITEMDATA.construct_weapon_level(0x96, 6000, xp=25000),
    RAC3ITEM.RY3N0: RAC3ITEMDATA.construct_weapon(0x97, 6000, 25, ap_classification=ItemClassification.progression),
    RAC3ITEM.RY3NO_V2: RAC3ITEMDATA.construct_weapon_level(0x98, 7000, 30, 20000),
    RAC3ITEM.RY3NO_V3: RAC3ITEMDATA.construct_weapon_level(0x99, 8000, 35, 50000),
    RAC3ITEM.RY3NO_V4: RAC3ITEMDATA.construct_weapon_level(0x9A, 9000, 40, 90000),
    RAC3ITEM.RYNOCIRATOR: RAC3ITEMDATA.construct_weapon_level(0x9B, 10000, 50, 140000),
    RAC3ITEM.PLASMA_COIL_V2: RAC3ITEMDATA.construct_weapon_level(0xA0, 3000, 15, 8000),
    RAC3ITEM.LAVA_GUN_V2: RAC3ITEMDATA.construct_weapon_level(0xA1, 240, 150, 600),
    RAC3ITEM.MINI_TURRET_V2: RAC3ITEMDATA.construct_weapon_level(0xA2, 800, 10, 400),
    RAC3ITEM.WRENCH_V2: RAC3ITEMDATA.construct_unused(0xA4),
    RAC3ITEM.WRENCH_V3: RAC3ITEMDATA.construct_unused(0xA5),
    RAC3ITEM.BOUNCER_V2: RAC3ITEMDATA.construct_weapon_level(0xA6, 1400, 10, 2500),
    RAC3ITEM.SHIELD_CHARGER_V2: RAC3ITEMDATA.construct_weapon_level(0xA7, 100, 3, 2200),
    RAC3ITEM.MINI_TURRET_V3: RAC3ITEMDATA.construct_weapon_level(0xA8, 1000, 12, 1000),
    RAC3ITEM.MINI_TURRET_V4: RAC3ITEMDATA.construct_weapon_level(0xA9, 1200, 12, 2000),
    RAC3ITEM.MEGA_TURRET: RAC3ITEMDATA.construct_weapon_level(0xAA, 2080, 12, 3500),
    RAC3ITEM.MEGA_TURRET_V6: RAC3ITEMDATA.construct_weapon_level(0xAB, 10400, 12),
    RAC3ITEM.MEGA_TURRET_V7: RAC3ITEMDATA.construct_weapon_level(0xAC, 13000, 14, 10000),
    RAC3ITEM.MEGA_TURRET_V8: RAC3ITEMDATA.construct_weapon_level(0xAD, 15600, 16, 25000),
    RAC3ITEM.LAVA_GUN_V3: RAC3ITEMDATA.construct_weapon_level(0xAE, 360, 175, 1500),
    RAC3ITEM.LAVA_GUN_V4: RAC3ITEMDATA.construct_weapon_level(0xAF, 500, 175, 2700),
    RAC3ITEM.LIQUID_NITROGEN: RAC3ITEMDATA.construct_weapon_level(0xB0, 700, 200, 4200),
    RAC3ITEM.LIQUID_NITROGEN_V6: RAC3ITEMDATA.construct_weapon_level(0xB1, 2600, 200),
    RAC3ITEM.LIQUID_NITROGEN_V7: RAC3ITEMDATA.construct_weapon_level(0xB2, 3000, 250, 10000),
    RAC3ITEM.LIQUID_NITROGEN_V8: RAC3ITEMDATA.construct_weapon_level(0xB3, 3600, 300, 25000),
    RAC3ITEM.BOUNCER_V3: RAC3ITEMDATA.construct_weapon_level(0xB4, 1400, 12, 8500),
    RAC3ITEM.BOUNCER_V4: RAC3ITEMDATA.construct_weapon_level(0xB5, 1800, 12, 18500),
    RAC3ITEM.HEAVY_BOUNCER: RAC3ITEMDATA.construct_weapon_level(0xB6, 2000, 12, 30500),
    RAC3ITEM.HEAVY_BOUNCER_V6: RAC3ITEMDATA.construct_weapon_level(0xB7, 3000, 12),
    RAC3ITEM.HEAVY_BOUNCER_V7: RAC3ITEMDATA.construct_weapon_level(0xB8, 3600, 14, 10000),
    RAC3ITEM.HEAVY_BOUNCER_V8: RAC3ITEMDATA.construct_weapon_level(0xB9, 4400, 16, 25000),
    RAC3ITEM.PLASMA_COIL_V3: RAC3ITEMDATA.construct_weapon_level(0xBA, 3600, 18, 18000),
    RAC3ITEM.PLASMA_COIL_V4: RAC3ITEMDATA.construct_weapon_level(0xBB, 4200, 18, 30000),
    RAC3ITEM.PLASMA_STORM: RAC3ITEMDATA.construct_weapon_level(0xBC, 6000, 20, 44000),
    RAC3ITEM.PLASMA_STORM_V6: RAC3ITEMDATA.construct_weapon_level(0xBD, 6800, 20),
    RAC3ITEM.PLASMA_STORM_V7: RAC3ITEMDATA.construct_weapon_level(0xBE, 7600, 22, 15000),
    RAC3ITEM.PLASMA_STORM_V8: RAC3ITEMDATA.construct_weapon_level(0xBF, 8400, 25, 37500),
    RAC3ITEM.SHIELD_CHARGER_V3: RAC3ITEMDATA.construct_weapon_level(0xC0, 140, 3, 5000),
    RAC3ITEM.SHIELD_CHARGER_V4: RAC3ITEMDATA.construct_weapon_level(0xC1, 180, 4, 9600),
    RAC3ITEM.TESLA_BARRIER: RAC3ITEMDATA.construct_weapon_level(0xC2, 240, 4, 16800),
    RAC3ITEM.TESLA_BARRIER_V6: RAC3ITEMDATA.construct_weapon_level(0xC3, 300, 4),
    RAC3ITEM.TESLA_BARRIER_V7: RAC3ITEMDATA.construct_weapon_level(0xC4, 400, 5, 12000),
    RAC3ITEM.TESLA_BARRIER_V8: RAC3ITEMDATA.construct_weapon_level(0xC5, 500, 5, 30000),
    RAC3ITEM.WRENCH_V4: RAC3ITEMDATA.construct_unused(0xC6),
    RAC3ITEM.WRENCH_V5: RAC3ITEMDATA.construct_unused(0xC7),
    RAC3ITEM.WRENCH_V6: RAC3ITEMDATA.construct_unused(0xC8),
    RAC3ITEM.WRENCH_V7: RAC3ITEMDATA.construct_unused(0xC9),
    RAC3ITEM.WRENCH_V8: RAC3ITEMDATA.construct_unused(0xCA),
    # Progressive
    RAC3ITEM.PROGRESSIVE_SHOCK_BLASTER:
        RAC3ITEMDATA.construct_weapon_prog(0xCB, ItemClassification.useful),
    RAC3ITEM.PROGRESSIVE_N60_STORM:
        RAC3ITEMDATA.construct_weapon_prog(0xCC, ItemClassification.useful),
    RAC3ITEM.PROGRESSIVE_INFECTOR:
        RAC3ITEMDATA.construct_weapon_prog(0xCD, ItemClassification.progression_skip_balancing),
    RAC3ITEM.PROGRESSIVE_ANNIHILATOR:
        RAC3ITEMDATA.construct_weapon_prog(0xCE, ItemClassification.progression_skip_balancing),
    RAC3ITEM.PROGRESSIVE_SPITTING_HYDRA:
        RAC3ITEMDATA.construct_weapon_prog(0xCF, ItemClassification.progression_skip_balancing),
    RAC3ITEM.PROGRESSIVE_DISC_BLADE:
        RAC3ITEMDATA.construct_weapon_prog(0xD0, ItemClassification.progression_skip_balancing),
    RAC3ITEM.PROGRESSIVE_AGENTS_OF_DOOM:
        RAC3ITEMDATA.construct_weapon_prog(0xD1, ItemClassification.useful),
    RAC3ITEM.PROGRESSIVE_RIFT_INDUCER:
        RAC3ITEMDATA.construct_weapon_prog(0xD2, ItemClassification.progression_skip_balancing),
    RAC3ITEM.PROGRESSIVE_HOLO_SHIELD:
        RAC3ITEMDATA.construct_weapon_prog(0xD3, ItemClassification.useful),
    RAC3ITEM.PROGRESSIVE_FLUX_RIFLE:
        RAC3ITEMDATA.construct_weapon_prog(0xD4, ItemClassification.progression_skip_balancing),
    RAC3ITEM.PROGRESSIVE_NITRO_LAUNCHER:
        RAC3ITEMDATA.construct_weapon_prog(0xD5, ItemClassification.useful),
    RAC3ITEM.PROGRESSIVE_PLASMA_WHIP:
        RAC3ITEMDATA.construct_weapon_prog(0xD6, ItemClassification.progression_skip_balancing),
    RAC3ITEM.PROGRESSIVE_SUCK_CANNON:
        RAC3ITEMDATA.construct_weapon_prog(0xD7, ItemClassification.progression_skip_balancing),
    RAC3ITEM.PROGRESSIVE_QWACK_O_RAY:
        RAC3ITEMDATA.construct_weapon_prog(0xD8, ItemClassification.progression_skip_balancing),
    RAC3ITEM.PROGRESSIVE_RY3N0:
        RAC3ITEMDATA.construct_weapon_prog(0xD9, ItemClassification.progression_skip_balancing),
    RAC3ITEM.PROGRESSIVE_PLASMA_COIL:
        RAC3ITEMDATA.construct_rac2_prog(0xDA, ItemClassification.useful),
    RAC3ITEM.PROGRESSIVE_LAVA_GUN:
        RAC3ITEMDATA.construct_rac2_prog(0xDB, ItemClassification.useful),
    RAC3ITEM.PROGRESSIVE_BOUNCER:
        RAC3ITEMDATA.construct_rac2_prog(0xDD, ItemClassification.useful),
    RAC3ITEM.PROGRESSIVE_MINI_TURRET:
        RAC3ITEMDATA.construct_rac2_prog(0xDF, ItemClassification.useful),
    RAC3ITEM.PROGRESSIVE_SHIELD_CHARGER:
        RAC3ITEMDATA.construct_rac2_prog(0xE0, ItemClassification.useful),
    # Infobots
    RAC3ITEM.VELDIN: RAC3ITEMDATA.construct_infobot(0xE1, ItemClassification.progression),
    RAC3ITEM.FLORANA: RAC3ITEMDATA.construct_infobot(0xE2, ItemClassification.progression),
    RAC3ITEM.STARSHIP_PHOENIX: RAC3ITEMDATA.construct_infobot(0xE3, ItemClassification.progression),
    RAC3ITEM.MARCADIA: RAC3ITEMDATA.construct_infobot(0xE4, ItemClassification.progression),
    RAC3ITEM.ANNIHILATION_NATION: RAC3ITEMDATA.construct_infobot(0xE5, ItemClassification.progression),
    RAC3ITEM.AQUATOS: RAC3ITEMDATA.construct_infobot(0xE6, ItemClassification.progression),
    RAC3ITEM.TYHRRANOSIS: RAC3ITEMDATA.construct_infobot(0xE7, ItemClassification.progression),
    RAC3ITEM.DAXX: RAC3ITEMDATA.construct_infobot(0xE8, ItemClassification.progression),
    RAC3ITEM.OBANI_GEMINI: RAC3ITEMDATA.construct_infobot(0xE9, ItemClassification.progression),
    RAC3ITEM.BLACKWATER_CITY: RAC3ITEMDATA.construct_infobot(0xEA, ItemClassification.progression),
    RAC3ITEM.HOLOSTAR_STUDIOS: RAC3ITEMDATA.construct_infobot(0xEB, ItemClassification.progression),
    RAC3ITEM.OBANI_DRACO: RAC3ITEMDATA.construct_infobot(0xEC, ItemClassification.progression),
    RAC3ITEM.ZELDRIN_STARPORT: RAC3ITEMDATA.construct_infobot(0xED, ItemClassification.progression),
    RAC3ITEM.METROPOLIS: RAC3ITEMDATA.construct_infobot(0xEE, ItemClassification.progression),
    RAC3ITEM.CRASH_SITE: RAC3ITEMDATA.construct_infobot(0xEF, ItemClassification.progression),
    RAC3ITEM.ARIDIA: RAC3ITEMDATA.construct_infobot(0xF0, ItemClassification.progression),
    RAC3ITEM.QWARKS_HIDEOUT: RAC3ITEMDATA.construct_infobot(0xF1, ItemClassification.progression),
    RAC3ITEM.KOROS: RAC3ITEMDATA.construct_infobot(0xF2, ItemClassification.progression),
    RAC3ITEM.COMMAND_CENTER: RAC3ITEMDATA.construct_infobot(0xF3, ItemClassification.progression),
    RAC3ITEM.MUSEUM: RAC3ITEMDATA.construct_infobot(0xF4, ItemClassification.progression),
    # Armor
    RAC3ITEM.PROGRESSIVE_ARMOR: RAC3ITEMDATA.construct_armor(0xF5, ItemClassification.progression, 0),
    RAC3ITEM.MAGNAPLATE: RAC3ITEMDATA.construct_armor(0xF6, ItemClassification.progression, 10),
    RAC3ITEM.ADAMANTINE: RAC3ITEMDATA.construct_armor(0xF7, ItemClassification.progression, 15),
    RAC3ITEM.AEGIS: RAC3ITEMDATA.construct_armor(0xF8, ItemClassification.progression, 20),
    RAC3ITEM.INFERNOX: RAC3ITEMDATA.construct_armor(0xF9, ItemClassification.progression, 24),
    # VidComics
    RAC3ITEM.PROGRESSIVE_VIDCOMIC: RAC3ITEMDATA.construct_vidcomic(0xFA),
    RAC3ITEM.VIDCOMIC1: RAC3ITEMDATA.construct_vidcomic(0xFB),
    RAC3ITEM.VIDCOMIC2: RAC3ITEMDATA.construct_vidcomic(0xFC),
    RAC3ITEM.VIDCOMIC3: RAC3ITEMDATA.construct_vidcomic(0xFD),
    RAC3ITEM.VIDCOMIC4: RAC3ITEMDATA.construct_vidcomic(0xFE),
    RAC3ITEM.VIDCOMIC5: RAC3ITEMDATA.construct_vidcomic(0xFF),

    # Filler
    RAC3ITEM.TITANIUM_BOLT: RAC3ITEMDATA.construct_other(0x100),
    RAC3ITEM.WEAPON_XP: RAC3ITEMDATA.construct_other(0x101),
    RAC3ITEM.PLAYER_XP: RAC3ITEMDATA.construct_other(0x102),
    RAC3ITEM.BOLTS: RAC3ITEMDATA.construct_other(0x103, RAC3STATUS.BOLTS),
    RAC3ITEM.INFERNO_MODE: RAC3ITEMDATA.construct_other(0x104),
    RAC3ITEM.JACKPOT: RAC3ITEMDATA.construct_other(0x105),

    # Goal
    RAC3ITEM.VICTORY: RAC3ITEMDATA.construct_goal(0x106),
}
RAC3_STATUS_DATA_TABLE: dict[str, RAC3STATUSDATA] = {
    # Quick Select
    RAC3ITEM.QUICK_SELECT_0: RAC3STATUSDATA(0x0),
    RAC3ITEM.QUICK_SELECT_1: RAC3STATUSDATA(0x1),
    RAC3ITEM.QUICK_SELECT_2: RAC3STATUSDATA(0x2),
    RAC3ITEM.QUICK_SELECT_3: RAC3STATUSDATA(0x3),
    RAC3ITEM.QUICK_SELECT_4: RAC3STATUSDATA(0x4),
    RAC3ITEM.QUICK_SELECT_5: RAC3STATUSDATA(0x5),
    RAC3ITEM.QUICK_SELECT_6: RAC3STATUSDATA(0x6),
    RAC3ITEM.QUICK_SELECT_7: RAC3STATUSDATA(0x7),
    RAC3ITEM.QUICK_SELECT_8: RAC3STATUSDATA(0x8),
    RAC3ITEM.QUICK_SELECT_9: RAC3STATUSDATA(0x9),
    RAC3ITEM.QUICK_SELECT_A: RAC3STATUSDATA(0xA),
    RAC3ITEM.QUICK_SELECT_B: RAC3STATUSDATA(0xB),
    RAC3ITEM.QUICK_SELECT_C: RAC3STATUSDATA(0xC),
    RAC3ITEM.QUICK_SELECT_D: RAC3STATUSDATA(0xD),
    RAC3ITEM.QUICK_SELECT_E: RAC3STATUSDATA(0xE),
    RAC3ITEM.QUICK_SELECT_F: RAC3STATUSDATA(0xF),
}
RAC3_REGION_DATA_TABLE: dict[str, RAC3REGIONDATA] = {
    # Regions
    RAC3REGION.VELDIN: RAC3REGIONDATA(0x01),
    RAC3REGION.FLORANA: RAC3REGIONDATA(0x02),
    RAC3REGION.STARSHIP_PHOENIX: RAC3REGIONDATA(0x03),
    RAC3REGION.MARCADIA: RAC3REGIONDATA(0x04),
    RAC3REGION.DAXX: RAC3REGIONDATA(0x05),
    RAC3REGION.ANNIHILATION_NATION: RAC3REGIONDATA(0x07),
    RAC3REGION.AQUATOS: RAC3REGIONDATA(0x08),
    RAC3REGION.TYHRRANOSIS: RAC3REGIONDATA(0x09),
    RAC3REGION.ZELDRIN_STARPORT: RAC3REGIONDATA(0x0A),
    RAC3REGION.OBANI_GEMINI: RAC3REGIONDATA(0x0B),
    RAC3REGION.BLACKWATER_CITY: RAC3REGIONDATA(0x0C),
    RAC3REGION.HOLOSTAR_STUDIOS: RAC3REGIONDATA(0x0D),
    RAC3REGION.KOROS: RAC3REGIONDATA(0x0E),
    RAC3REGION.METROPOLIS: RAC3REGIONDATA(0x10),
    RAC3REGION.CRASH_SITE: RAC3REGIONDATA(0x11),
    RAC3REGION.ARIDIA: RAC3REGIONDATA(0x12),
    RAC3REGION.QWARKS_HIDEOUT: RAC3REGIONDATA(0x13),
    RAC3REGION.OBANI_DRACO: RAC3REGIONDATA(0x15),
    RAC3REGION.COMMAND_CENTER: RAC3REGIONDATA(0x16),
    RAC3REGION.MUSEUM: RAC3REGIONDATA(0x18),
    RAC3REGION.GALAXY: RAC3REGIONDATA(0x00),
    RAC3REGION.PHOENIX_ASSAULT: RAC3REGIONDATA(0x06),
    RAC3REGION.UNUSED: RAC3REGIONDATA(0x0F),
    RAC3REGION.COMMAND_CENTER_2: RAC3REGIONDATA(0x14),
    RAC3REGION.HOLOSTAR_STUDIOS_CLANK: RAC3REGIONDATA(0x17),
    RAC3REGION.UNUSED_2: RAC3REGIONDATA(0x19),
    RAC3REGION.METROPOLIS_MISSION: RAC3REGIONDATA(0x1A),
    RAC3REGION.AQUATOS_BASE: RAC3REGIONDATA(0x1B),
    RAC3REGION.AQUATOS_SEWERS: RAC3REGIONDATA(0x1C),
    RAC3REGION.TYHRRANOSIS_MISSION: RAC3REGIONDATA(0x1D),
    RAC3REGION.QWARK_VID_COMIC_UNUSED_1: RAC3REGIONDATA(0x1E),
    RAC3REGION.QWARK_VID_COMIC_1: RAC3REGIONDATA(0x1F),
    RAC3REGION.QWARK_VID_COMIC_4: RAC3REGIONDATA(0x20),
    RAC3REGION.QWARK_VID_COMIC_2: RAC3REGIONDATA(0x21),
    RAC3REGION.QWARK_VID_COMIC_3: RAC3REGIONDATA(0x22),
    RAC3REGION.QWARK_VID_COMIC_5: RAC3REGIONDATA(0x23),
    RAC3REGION.QWARK_VID_COMIC_UNUSED_2: RAC3REGIONDATA(0x24),
    RAC3REGION.SLOT_0: RAC3REGIONDATA.construct_slot(slot=0x00),
    RAC3REGION.SLOT_1: RAC3REGIONDATA.construct_slot(slot=0x01),
    RAC3REGION.SLOT_2: RAC3REGIONDATA.construct_slot(slot=0x02),
    RAC3REGION.SLOT_3: RAC3REGIONDATA.construct_slot(slot=0x03),
    RAC3REGION.SLOT_4: RAC3REGIONDATA.construct_slot(slot=0x04),
    RAC3REGION.SLOT_5: RAC3REGIONDATA.construct_slot(slot=0x05),
    RAC3REGION.SLOT_6: RAC3REGIONDATA.construct_slot(slot=0x06),
    RAC3REGION.SLOT_7: RAC3REGIONDATA.construct_slot(slot=0x07),
    RAC3REGION.SLOT_8: RAC3REGIONDATA.construct_slot(slot=0x08),
    RAC3REGION.SLOT_9: RAC3REGIONDATA.construct_slot(slot=0x09),
    RAC3REGION.SLOT_A: RAC3REGIONDATA.construct_slot(slot=0x0A),
    RAC3REGION.SLOT_B: RAC3REGIONDATA.construct_slot(slot=0x0B),
    RAC3REGION.SLOT_C: RAC3REGIONDATA.construct_slot(slot=0x0C),
    RAC3REGION.SLOT_D: RAC3REGIONDATA.construct_slot(slot=0x0D),
    RAC3REGION.SLOT_E: RAC3REGIONDATA.construct_slot(slot=0x0E),
    RAC3REGION.SLOT_F: RAC3REGIONDATA.construct_slot(slot=0x0F),
    RAC3REGION.SLOT_10: RAC3REGIONDATA.construct_slot(slot=0x10),
    RAC3REGION.SLOT_11: RAC3REGIONDATA.construct_slot(slot=0x11),
    RAC3REGION.SLOT_12: RAC3REGIONDATA.construct_slot(slot=0x12),
    RAC3REGION.SLOT_13: RAC3REGIONDATA.construct_slot(slot=0x13),
}


@dataclass
class RAC3LOCATIONDATA:
    ID: int = 0
    REGION: RAC3REGION = RAC3REGION.GALAXY
    CHECK_ADDRESS: set[tuple[int, CHECKTYPE, int]] = None
    AP_CODE: int = None
    TAGS: set[str] = None
    LOCAL_TRACKER: str = None
    GALAXY_TRACKER: str = None

    def __init__(self,
                 idx: int,
                 region: RAC3REGION = RAC3REGION.GALAXY,
                 check: set[tuple[int, CHECKTYPE, int]] = (),
                 tags: set[str] = None,
                 tracker: str = None):
        self.ID = idx
        self.REGION = region
        self.CHECK_ADDRESS = check
        self.AP_CODE = idx + 50000000
        self.TAGS = tags
        self.LOCAL_TRACKER = tracker


RAC3_LOCATION_DATA_TABLE: dict[str, RAC3LOCATIONDATA] = {

}

ITEM_FROM_AP_CODE: dict[int, str] = dict(
    (kv[1].AP_CODE, kv[0]) for kv in
    filter(lambda data_kv: data_kv[1].AP_CODE is not None, RAC3_ITEM_DATA_TABLE.items()))

ITEM_NAME_FROM_ID: dict[int, str] = dict(
    (kv[1].ID, kv[0]) for kv in filter(lambda data_kv: data_kv[1].ID is not None, RAC3_ITEM_DATA_TABLE.items()))

ITEM_NAME_FROM_ADDRESS: dict[int, str] = dict(
    (kv[1].UNLOCK_ADDRESS, kv[0]) for kv in
    filter(lambda data_kv: data_kv[1].UNLOCK_ADDRESS is not None, RAC3_ITEM_DATA_TABLE.items()))

ALL_ITEMS_LIST: list[str] = list(ITEM_FROM_AP_CODE.values())
ITEMS_WITH_ADDRESSES: list[str] = list(ITEM_NAME_FROM_ADDRESS.values())

LOCATIONS = [
    {
        "Name": "Recruitment/Received Shock Blaster",
        "Id": 50010000,
        "Address": "0x001426E0",
        # Use event flag rather than weapon unlock address to avoid issues with weapon randomizer
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Rangers/Received Nitro Launcher",
        "Id": 50010001,
        "Address": "0x001426E1",
        # Use event flag rather than weapon unlock address to avoid issues with weapon randomizer
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Save Veldin!/Infobot: Florana",
        "Id": 50010002,
        "Address": "0x001426E4",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Vendor/Received Plasma Whip",
        "Id": 50020000,
        "Address": "0x00142D1F",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Vendor/Received N60 Storm",
        "Id": 50020001,
        "Address": "0x00142CCF",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Below Vendor/Titanium Bolt",
        "Id": 50020002,
        "Address": "0x001BBB29",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Path of Death/Titanium Bolt",
        "Id": 50020003,
        "Address": "0x001BBB2A",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Walk the PATH OF DEATH!/Defeat Qwark",
        "Id": 50020004,
        "Address": "0x001426E7",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Vendor/Received Suck Cannon",
        "Id": 50030000,
        "Address": "0x00142D27",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Vendor/Received Infector",
        "Id": 50030001,
        "Address": "0x00142CD7",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "VR Training/Nerves of Titanium Bolt",
        "Id": 50030027,
        "Address": "0x001BBB30",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "VR Training/Gadget Training Titanium Bolt",
        "Id": 50030015,
        "Address": "0x001BBB31",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Armor Vendor/Received Magna Plate Armor",
        "Id": 50030002,
        "Address": "0x001426A0",
        "CheckValue": 1,
        "CheckType": 3
    },
    {
        "Name": "Armor Vendor/Received Adamantine Armor",
        "Id": 50030003,
        "Address": "0x001426A0",
        "CheckValue": 2,
        "CheckType": 3
    },
    {
        "Name": "Armor Vendor/Received Aegis Mark V Armor",
        "Id": 50030004,
        "Address": "0x001426A0",
        "CheckValue": 3,
        "CheckType": 3
    },
    {
        "Name": "Armor Vendor/Received Infernox Armor",
        "Id": 50030005,
        "Checks": [
            {
                "Address": "0x001D54B4",
                "CheckType": 0,
                "AddressBit": 0
            },
            {
                "Address": "0x001D545C",
                "CheckValue": 3,
                "CheckType": 0
            }
        ]
    },
    {
        "Name": "VR Training/Received Hacker",
        "Id": 50030016,
        # "Address": "0x00142CB4",
        "Address": "0x00142765",  # Same as VR Gadget Training mission completion
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "VR Training/Received Hypershot",
        "Id": 50030017,
        # "Address": "0x00142CAB",
        "Address": "0x00142765",  # Same as VR Gadget Training mission completion
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Bridge/Infobot: Marcadia",
        "Id": 50030006,
        "Checks": [
            {
                "Address": "0x001426E9",
                "CheckValue": 1,
                "CheckType": 0
            },
            {
                "Address": "0x001D545C",
                "CheckValue": 3,
                "CheckType": 0
            }
        ]
    },
    {
        "Name": "Get to the Bridge/Infobot: Koros",
        "Id": 50030007,
        "Address": "0x001D553E",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Qwark Vid Comics/Infobot: Annihilation Nation",
        "Id": 50030008,
        "Address": "0x001426EB",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix Infobots/Infobot: Aquatos",
        "Id": 50030009,
        # " Address": 0x001426F6, #  Correct Infobot address
        "Address": "0x0014276F",  # Same as Tyhrra-Guise Getting event. This event behinds Phoenix Ship event.
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix Infobots/Infobot: Tyhrranosis",
        "Id": 50030010,
        # "Address": "0x00142C1B",
        "Address": "0x0014275E",  # Same as 1 Sewer Crystal Traded
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "VR Training/Infobot: Daxx",
        "Id": 50030011,
        #  "Address": "0x00142765",
        "Address": "0x00142765",  # Same as T-Bolt: VR training
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Klunk Fight/Infobot: Crash Site",
        "Id": 50160004,
        #  "Address": "0x001D5541",
        "Address": "0x00142708",  # Same as defeat Giant Cronk
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Qwark Vid Comics/Infobot: Qwarks Hideout",
        "Id": 50030014,
        "Address": "0x00142734",
        "CheckType": 0,
        "AddressBit": 5  # 3E 00X0_0000
    },
    {
        "Name": "The Leviathan/Qwark Vidcomic 4",
        "Id": 50100003,
        "Address": "0x001426E2",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix Infobots/Qwark Vidcomic 5",
        "Id": 50030029,
        "Address": "0x001D5553",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Qwark Vid Comics/Infobot: Metropolis",
        "Id": 50030012,
        "Address": "0x001D5550",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Vendor/Received Spitting Hydra",
        "Id": 50040000,
        "Address": "0x00142CE7",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Laser Defense Facility/Received Refractor",
        "Id": 50040001,
        # "Address": "0x00142CB2", # item flag
        "Address": "0x00142C29",  # Marcadia Mission event Flag
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "After Pool of Water/Titanium Bolt",
        "Id": 50040002,
        "Address": "0x001BBB39",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Last Refractor Room/Titanium Bolt",
        "Id": 50040003,
        "Address": "0x001BBB3A",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Ceiling just before Al/Titanium Bolt",
        "Id": 50040004,
        "Address": "0x001BBB3B",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Repair the Laser Defense Shield/Qwark Vidcomic 1",
        "Id": 50040005,
        "Address": "0x001426ea",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Vendor/Received Agents of Doom",
        "Id": 50070000,
        "Address": "0x00142CF7",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Prizes/Received Tyhrra-Guise",
        "Id": 50070001,
        "Address": "0x0014276F",  # Same as Grand Prize Bout(Tyhrra-Guise Getting event)
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Heat Street Bolt/Titanium Bolt",
        "Id": 50070002,
        "Address": "0x001BBB51",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Maze of Blaze Bolt/Titanium Bolt",
        "Id": 50070003,
        "Address": "0x001BBB52",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Arena Challenges/Grand Prize Bout",
        "Id": 50070004,
        "Address": "0x0014276F",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Arena Challenges/The Terrible Two",
        "Id": 50070005,
        "Address": "0x00142772",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Arena Challenges/Robot Rampage",
        "Id": 50070006,
        "Address": "0x00142773",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Arena Challenges/Two Minute Warning",
        "Id": 50070007,
        "Address": "0x00142774",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Arena Challenges/90 Seconds of Carnage",
        "Id": 50070008,
        "Address": "0x00142775",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Arena Challenges/Onslaught",
        "Id": 50070009,
        "Address": "0x00142776",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Arena Challenges/Whip It Good",
        "Id": 50070010,
        "Address": "0x00142777",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Arena Challenges/Hydra'n Seek",
        "Id": 50070011,
        "Address": "0x00142778",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Arena Challenges/Championship Bout",
        "Id": 50070012,
        "Address": "0x00142779",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Arena Revisit Challenges/Ninja Challenge",
        "Id": 50070014,
        "Address": "0x0014277D",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Arena Revisit Challenges/Counting Ducks",
        "Id": 50070015,
        "Address": "0x0014277E",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Arena Revisit Challenges/Cycling Weapons",
        "Id": 50070016,
        "Address": "0x0014277F",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Arena Revisit Challenges/One Hit Wonder",
        "Id": 50070017,
        "Address": "0x00142780",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Arena Revisit Challenges/Time to Suck",
        "Id": 50070018,
        "Address": "0x00142781",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Arena Revisit Challenges/Naptime",
        "Id": 50070019,
        "Address": "0x00142782",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Arena Revisit Challenges/Meet Courtney - Arena",
        "Id": 50070013,
        "Address": "0x00142771",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Arena Revisit Challenges/More Cycling Weapons",
        "Id": 50070020,
        "Address": "0x00142783",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Arena Revisit Challenges/Dodge the Twins",
        "Id": 50070021,
        "Address": "0x00142784",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Arena Revisit Challenges/Chop Chop",
        "Id": 50070022,
        "Address": "0x00142785",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Arena Revisit Challenges/Sleep Inducer",
        "Id": 50070023,
        "Address": "0x00142786",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Arena Revisit Challenges/The Other White Meat",
        "Id": 50070024,
        "Address": "0x00142787",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Arena Revisit Challenges/Championship Bout II",
        "Id": 50070025,
        "Address": "0x00142788",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Qwarktastic Battle/It's Qwarktastic!",
        "Id": 50070026,
        "Address": "0x00142789",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Gauntlet Challenges/Heat Street",
        "Id": 50070027,
        "Address": "0x0014276E",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Gauntlet Challenges/Crispy Critter",
        "Id": 50070028,
        "Address": "0x0014277A",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Gauntlet Challenges/Pyro Playground",
        "Id": 50070029,
        "Address": "0x0014277B",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Gauntlet Challenges/Suicide Run",
        "Id": 50070030,
        "Address": "0x0014277C",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Gauntlet Revisit Challenges/BBQ Boulevard",  # (Meet Courtney - Gauntlet)
        "Id": 50070031,
        "Address": "0x00142770",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Gauntlet Revisit Challenges/Maze of Blaze",
        "Id": 50070032,
        "Address": "0x0014278A",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Gauntlet Revisit Challenges/Cremation Station",
        "Id": 50070033,
        "Address": "0x0014278B",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Gauntlet Revisit Challenges/The Annihilator",
        "Id": 50070034,
        "Address": "0x0014278C",
        "CheckType": 0,
        "AddressBit": 0
    },
    # {
    #     "Name": "Prizes/Qwark VidComic 2",
    #     "Id": 50070035,
    #     "Address": "0x001D5551",
    #     "CheckType": 0,
    #     "AddressBit": 0
    # },
    # {
    #     "Name": "Prizes/Qwark VidComic 3",
    #     "Id": 50070036,
    #     "Address": "0x001D5552",
    #     "CheckType": 0,
    #     "AddressBit": 0
    # },
    {
        "Name": "Vendor/Received Flux Rifle",
        "Id": 50080000,
        "Address": "0x00142D0F",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Under the Bridge/Titanium Bolt",
        "Id": 50080001,
        "Address": "0x001BBB5A",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Underwater Bolt/Titanium Bolt",
        "Id": 50080002,
        "Address": "0x001BBB5B",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Behind the Locked Gate/Titanium Bolt",
        "Id": 50080003,
        "Address": "0x001BBB59",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Top Left Bolt/Titanium Bolt",
        "Id": 50280000,
        "Address": "0x001BBBF9",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Swinging Bolt/Titanium Bolt",
        "Id": 50280001,
        "Address": "0x001BBBFA",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Gather Sewer Crystals/1 Sewer Crystal Traded",
        "Id": 50280002,
        "Address": "0x0014275E",  # JP: 1426DE,
        "CompareType": 1,  # Greater than
        "CheckType": 3,  # Byte type
        "CheckValue": 0
    },
    {
        "Name": "Gather Sewer Crystals/5 Sewer Crystals Traded",
        "Id": 50280003,
        "Address": "0x0014275E",  # JP: 1426DE,
        "CheckType": 3,  # Byte type
        "CompareType": 1,  # Greater than
        "CheckValue": 4
    },
    {
        "Name": "Gather Sewer Crystals/10 Sewer Crystals Traded",
        "Id": 50280004,
        "Address": "0x0014275E",  # JP: 1426DE,
        "CheckType": 3,  # Byte type
        "CompareType": 1,  # Greater than
        "CheckValue": 9  # 0x9
    },
    {
        "Name": "Gather Sewer Crystals/20 Sewer Crystals Traded",
        "Id": 50280005,
        "Address": "0x0014275E",  # JP: 1426DE,
        "CheckType": 3,  # Byte type
        "CompareType": 1,  # Greater than
        "CheckValue": 19  # 0x13
    },
    {
        "Name": "Vendor/Received Annihilator",
        "Id": 50090000,
        "Address": "0x00142CDF",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Vendor/Received Holo-Shield Glove",
        "Id": 50090001,
        "Address": "0x00142D07",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "South East Cannon/Titanium Bolt",
        "Id": 50090002,
        "Address": "0x001BBB62",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Underground Cave Bolt/Titanium Bolt",
        "Id": 50090003,
        "Address": "0x001BBB61",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Right of the Taxi/Titanium Bolt",
        "Id": 50050001,
        "Address": "0x001BBB41",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Time Sensitive Door/Titanium Bolt",
        "Id": 50050002,
        "Address": "0x001BBB42",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Around the Island/Received Charge Boots",
        "Id": 50050003,
        "Address": "0x00142CBD",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Infiltrate the Weapons Facility/Infobot: Obani Gemini",
        "Id": 50050000,
        "Address": "0x001D553B",
        # Infobot Address: "0x00142C29" bit 3
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Explore the Docks/Courtney's Music Vid",
        "Id": 50050004,
        # "Address": "0x00143B39", #  ??
        "Address": "0x0014275B",  # Daxx Courtney Room
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Vendor/Received Disc Blade Gun",
        "Id": 50110000,
        "Address": "0x00142CEF",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Follow the Lava/Titanium Bolt",
        "Id": 50110001,
        "Address": "0x001BBB72",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Between the Twin Towers/Titanium Bolt",
        "Id": 50110002,
        "Address": "0x001BBB71",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Explore the Second Moon/Infobot: Blackwater City",
        "Id": 50110003,
        "Address": "0x00142BB2",
        "CheckType": 0,
        "AddressBit": 3  # 08: 0000_X000
    },
    {
        "Name": "Save Blackwater City/Received Grav Boots",
        "Id": 50120000,
        #  "Address": "0x00142CAD",
        "Address": "0x00142C40",
        "CheckType": 0,
        "AddressBit": 3  # 0x08: 0000_X000
    },
    {
        "Name": "Save Blackwater City/Infobot: Holostar Studios",
        "Id": 50120001,
        "Address": "0x00142705",
        #  "Address": "0x00142771", #  WA: Same as Meet Courtney - Arena
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Vendor/Received Rift Inducer",
        "Id": 50130000,
        "Address": "0x00142CFF",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Atop the Chairs/Titanium Bolt",
        "Id": 50130001,
        "Address": "0x001BBB82",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Lot 42's Grav Ramp/Titanium Bolt",
        "Id": 50130002,
        "Address": "0x001BBB83",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Kamikaze Noids/Titanium Bolt",
        "Id": 50130003,
        "Address": "0x001BBB81",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Escape the Tyhrranoid Ambush/Infobot: Obani Draco",
        "Id": 50130004,
        "Address": "0x00142713",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Beat Courtney Gears/Infobot: Zeldrin Starport",
        "Id": 50210000,
        "Address": "0x0014270D",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Go to the Zeldrin Starport/Received Bolt Grabber V2",
        "Id": 50100000,
        "Address": "0x00142CA7",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Inside the Second Ship/Titanium Bolt",
        "Id": 50100001,
        "Address": "0x001BBB6A",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Atop the Twin Shooters/Titanium Bolt",
        "Id": 50100002,
        "Address": "0x001BBB69",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Operation: URBAN STORM/Received Map-O-Matic",
        "Id": 50260006,
        #  "Address": "0x00142CA5", #  item flag
        "Address": "0x00142C64",  # Metropolis Mission Clear
        "CheckType": 0,
        "AddressBit": 5  # 0x20 : 00X0_0000
    },
    {
        "Name": "Across the Gap/Titanium Bolt",
        "Id": 50160000,
        "Address": "0x001BBB99",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Right of the Balcony/Titanium Bolt",
        "Id": 50160003,
        "Address": "0x001BBB9A",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Tall Tower (Hovership) /Titanium Bolt",
        "Id": 50260000,
        "Address": "0x001BBBE9",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Metal-Noids/The AAAAGE OF ROBOTS!!!",
        "Id": 50160002,
        "Address": "0x0014275C",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Side Route/Received Nano-Pak",
        "Id": 50170001,
        "Address": "0x00142CC0",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Turn Around/Titanium Bolt",
        "Id": 50170000,
        "Address": "0x001BBBA1",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Post Explore Crash Site/Infobot: Aridia",
        "Id": 50170003,
        "Address": "0x00142C52",
        # "Address": "0x00142722",
        # Correct Address: 0x00142C52(4bit: 0x07->0x0f) (US), but Event is not happened in some case.
        "CheckType": 0,
        "AddressBit": 3  # / 0x02: 0000_00X0
    },
    {
        "Name": "Operation: DEATH VALLEY/Received Warp Pad",
        "Id": 50180000,
        # "Address": "0x00142CBF", #  Item flag
        "Address": "0x00142C56",  # Clear Aridia
        "CheckType": 0,
        "AddressBit": 4  # 0x10: 000X_0000
    },
    {
        "Name": "Vendor/Received Qwack-O-Ray",
        "Id": 50180001,
        "Address": "0x00142D2F",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Under the Bridge (Assassination)/Titanium Bolt",
        "Id": 50180002,
        "Address": "0x001BBBAA",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Behind the Base (X12 Endgame)/Titanium Bolt",
        "Id": 50180003,
        "Address": "0x001BBBA9",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Grav-Ramp Path/Received Gadgetron PDA",
        "Id": 50190000,
        "Address": "0x00142CC3",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Glide from the Ramp/Titanium Bolt",
        "Id": 50190001,
        "Address": "0x001BBBB1",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Behind the Metal Fence/Titanium Bolt",
        "Id": 50140000,
        "Address": "0x001BBB89",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Pair of Towers/Titanium Bolt",
        "Id": 50140001,
        "Address": "0x001BBB8A",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Access big gun control panel/Infobot: Command Center",
        "Id": 50140002,
        "Address": "0x00142C49",
        "CheckType": 0,
        "AddressBit": 3  # 04 -> 0C: 0000_X000
    },
    {
        "Name": "Behind the Forcefield/Titanium Bolt",
        "Id": 50220000,
        "Address": "0x001BBBC9",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Defeat Dr. Nefarious/Dr. Nefarious Defeated!",
        "Id": 50200000,
        "Address": "0x0014270F",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Defeat the Biobliterator/Biobliterator Defeated!",
        "Id": 50200001,
        "Address": "0x00142BB6",
        "CheckType": 0,
        "AddressBit": 6  # 40: 0X00_0000
    },
    {
        "Name": "Qwark Vid Comics/VC1 - All Tokens Titanium Bolt",
        "Id": 50310001,
        "Address": "0x001BBB32",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Qwark Vid Comics/VC2 - All Tokens Titanium Bolt",
        "Id": 50330001,
        "Address": "0x001BBB34",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Qwark Vid Comics/VC3 - All Tokens Titanium Bolt",
        "Id": 50340001,
        "Address": "0x001BBB35",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Qwark Vid Comics/VC4 - All Tokens Titanium Bolt",
        "Id": 50320001,
        "Address": "0x001BBB33",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Qwark Vid Comics/VC5 - All Tokens Titanium Bolt",
        "Id": 50350001,
        "Address": "0x001BBB36",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Shock Blaster: V2",
        "Id": 50150000,
        "Address": "0x00142E7C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 4800
    },
    {
        "Name": "Shock Blaster: V3",
        "Id": 50150001,
        "Address": "0x00142E7C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 12800
    },
    {
        "Name": "Shock Blaster: V4",
        "Id": 50150002,
        "Address": "0x00142E7C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 22400
    },
    {
        "Name": "Shock Blaster: V5",
        "Id": 50150003,
        "Address": "0x001425E7",
        "CompareType": 0,
        "CheckType": 1,
        "CheckValue": 43
    },
    {
        "Name": "Nitro Launcher: V2",
        "Id": 50150004,
        "Address": "0x00142FBC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 6400
    },
    {
        "Name": "Nitro Launcher: V3",
        "Id": 50150005,
        "Address": "0x00142FBC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 16000
    },
    {
        "Name": "Nitro Launcher: V4",
        "Id": 50150006,
        "Address": "0x00142FBC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 35200
    },
    {
        "Name": "Nitro Launcher: V5",
        "Id": 50150007,
        "Address": "0x00142FBC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 83200
    },
    {
        "Name": "N60 Storm: V2",
        "Id": 50150008,
        "Address": "0x00142E9C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 6400
    },
    {
        "Name": "N60 Storm: V3",
        "Id": 50150009,
        "Address": "0x00142E9C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 16000
    },
    {
        "Name": "N60 Storm: V4",
        "Id": 50150010,
        "Address": "0x00142E9C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 48000
    },
    {
        "Name": "N60 Storm: V5",
        "Id": 50150011,
        "Address": "0x00142E9C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 57600
    },
    {
        "Name": "Plasma Whip: V2",
        "Id": 50150012,
        "Address": "0x00142FDC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 6400
    },
    {
        "Name": "Plasma Whip: V3",
        "Id": 50150013,
        "Address": "0x00142FDC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 25600
    },
    {
        "Name": "Plasma Whip: V4",
        "Id": 50150014,
        "Address": "0x00142FDC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 57600
    },
    {
        "Name": "Plasma Whip: V5",
        "Id": 50150015,
        "Address": "0x00142FDC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 105600
    },
    {
        "Name": "Infector: V2",
        "Id": 50150016,
        "Address": "0x00142EBC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 12800
    },
    {
        "Name": "Infector: V3",
        "Id": 50150017,
        "Address": "0x00142EBC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 25600
    },
    {
        "Name": "Infector: V4",
        "Id": 50150018,
        "Address": "0x00142EBC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 64000
    },
    {
        "Name": "Infector: V5",
        "Id": 50150019,
        "Address": "0x00142EBC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 121600
    },
    {
        "Name": "Suck Cannon: V2",
        "Id": 50150020,
        "Address": "0x00142FFC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 6400
    },
    {
        "Name": "Suck Cannon: V3",
        "Id": 50150021,
        "Address": "0x00142FFC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 19200
    },
    {
        "Name": "Suck Cannon: V4",
        "Id": 50150022,
        "Address": "0x00142FFC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 38400
    },
    {
        "Name": "Suck Cannon: V5",
        "Id": 50150023,
        "Address": "0x00142FFC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 76800
    },
    {
        "Name": "Spitting Hydra: V2",
        "Id": 50150024,
        "Address": "0x00142EFC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 9600
    },
    {
        "Name": "Spitting Hydra: V3",
        "Id": 50150025,
        "Address": "0x00142EFC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 28800
    },
    {
        "Name": "Spitting Hydra: V4",
        "Id": 50150026,
        "Address": "0x00142EFC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 57600
    },
    {
        "Name": "Spitting Hydra: V5",
        "Id": 50150027,
        "Address": "0x00142EFC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 96000
    },
    {
        "Name": "Agents of Doom: V2",
        "Id": 50150028,
        "Address": "0x00142F3C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 12800
    },
    {
        "Name": "Agents of Doom: V3",
        "Id": 50150029,
        "Address": "0x00142F3C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 32000
    },
    {
        "Name": "Agents of Doom: V4",
        "Id": 50150030,
        "Address": "0x00142F3C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 96000
    },
    {
        "Name": "Agents of Doom: V5",
        "Id": 50150031,
        "Address": "0x00142F3C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 192000
    },
    {
        "Name": "Flux Rifle: V2",
        "Id": 50150032,
        "Address": "0x00142F9C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 6400
    },
    {
        "Name": "Flux Rifle: V3",
        "Id": 50150033,
        "Address": "0x00142F9C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 19200
    },
    {
        "Name": "Flux Rifle: V4",
        "Id": 50150034,
        "Address": "0x00142F9C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 48000
    },
    {
        "Name": "Flux Rifle: V5",
        "Id": 50150035,
        "Address": "0x00142F9C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 92800
    },
    {
        "Name": "Annihilator: V2",
        "Id": 50150036,
        "Address": "0x00142EDC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 25600
    },
    {
        "Name": "Annihilator: V3",
        "Id": 50150037,
        "Address": "0x00142EDC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 76800
    },
    {
        "Name": "Annihilator: V4",
        "Id": 50150038,
        "Address": "0x00142EDC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 204800
    },
    {
        "Name": "Annihilator: V5",
        "Id": 50150039,
        "Address": "0x00142EDC",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 396800
    },
    {
        "Name": "Holo-Shield Glove: V2",
        "Id": 50150040,
        "Address": "0x00142F7C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 4800
    },
    {
        "Name": "Holo-Shield Glove: V3",
        "Id": 50150041,
        "Address": "0x00142F7C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 14400
    },
    {
        "Name": "Holo-Shield Glove: V4",
        "Id": 50150042,
        "Address": "0x00142F7C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 43200
    },
    {
        "Name": "Holo-Shield Glove: V5",
        "Id": 50150043,
        "Address": "0x00142F7C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 86400
    },
    {
        "Name": "Disc-Blade Gun: V2",
        "Id": 50150044,
        "Address": "0x00142F1C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 22400
    },
    {
        "Name": "Disc-Blade Gun: V3",
        "Id": 50150045,
        "Address": "0x00142F1C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 67200
    },
    {
        "Name": "Disc-Blade Gun: V4",
        "Id": 50150046,
        "Address": "0x00142F1C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 195200
    },
    {
        "Name": "Disc-Blade Gun: V5",
        "Id": 50150047,
        "Address": "0x00142F1C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 387200
    },
    {
        "Name": "Rift Inducer: V2",
        "Id": 50150048,
        "Address": "0x00142F5C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 25600
    },
    {
        "Name": "Rift Inducer: V3",
        "Id": 50150049,
        "Address": "0x00142F5C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 76800
    },
    {
        "Name": "Rift Inducer: V4",
        "Id": 50150050,
        "Address": "0x00142F5C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 204800
    },
    {
        "Name": "Rift Inducer: V5",
        "Id": 50150051,
        "Address": "0x00142F5C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 396800
    },
    {
        "Name": "Qwack-O-Ray: V2",
        "Id": 50150052,
        "Address": "0x0014301C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 32000
    },
    {
        "Name": "Qwack-O-Ray: V3",
        "Id": 50150053,
        "Address": "0x0014301C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 96000
    },
    {
        "Name": "Qwack-O-Ray: V4",
        "Id": 50150054,
        "Address": "0x0014301C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 256000
    },
    {
        "Name": "Qwack-O-Ray: V5",
        "Id": 50150055,
        "Address": "0x0014301C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 512000
    },
    {
        "Name": "RY3N0: V2",
        "Id": 50150056,
        "Address": "0x0014303C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 640000
    },
    {
        "Name": "RY3N0: V3",
        "Id": 50150057,
        "Address": "0x0014303C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 1600000
    },
    {
        "Name": "RY3N0: V4",
        "Id": 50150058,
        "Address": "0x0014303C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 2880000
    },
    {
        "Name": "RY3N0: V5",
        "Id": 50150059,
        "Address": "0x0014303C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 4480000
    },
    {
        "Name": "Mini-Turret Glove: V2",
        "Id": 50150060,
        "Address": "0x00142E34",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 12800
    },
    {
        "Name": "Mini-Turret Glove: V3",
        "Id": 50150061,
        "Address": "0x00142E34",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 32000
    },
    {
        "Name": "Mini-Turret Glove: V4",
        "Id": 50150062,
        "Address": "0x00142E34",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 64000
    },
    {
        "Name": "Mini-Turret Glove: V5",
        "Id": 50150063,
        "Address": "0x00142E34",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 112000
    },
    {
        "Name": "Lava Gun: V2",
        "Id": 50150064,
        "Address": "0x00142E24",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 19200
    },
    {
        "Name": "Lava Gun: V3",
        "Id": 50150065,
        "Address": "0x00142E24",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 48000
    },
    {
        "Name": "Lava Gun: V4",
        "Id": 50150066,
        "Address": "0x00142E24",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 86400
    },
    {
        "Name": "Lava Gun: V5",
        "Id": 50150067,
        "Address": "0x00142E24",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 134400
    },
    {
        "Name": "Shield Charger: V2",
        "Id": 50150068,
        "Address": "0x00142E38",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 70400
    },
    {
        "Name": "Shield Charger: V3",
        "Id": 50150069,
        "Address": "0x00142E38",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 160000
    },
    {
        "Name": "Shield Charger: V4",
        "Id": 50150070,
        "Address": "0x00142E38",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 307200
    },
    {
        "Name": "Shield Charger: V5",
        "Id": 50150071,
        "Address": "0x00142E38",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 537600
    },
    {
        "Name": "Bouncer: V2",
        "Id": 50150072,
        "Address": "0x00142E2C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 80000
    },
    {
        "Name": "Bouncer: V3",
        "Id": 50150073,
        "Address": "0x00142E2C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 272000
    },
    {
        "Name": "Bouncer: V4",
        "Id": 50150074,
        "Address": "0x00142E2C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 592000
    },
    {
        "Name": "Bouncer: V5",
        "Id": 50150075,
        "Address": "0x00142E2C",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 976000
    },
    {
        "Name": "Plasma Coil: V2",
        "Id": 50150076,
        "Address": "0x00142E20",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 256000
    },
    {
        "Name": "Plasma Coil: V3",
        "Id": 50150077,
        "Address": "0x00142E20",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 576000
    },
    {
        "Name": "Plasma Coil: V4",
        "Id": 50150078,
        "Address": "0x00142E20",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 960000
    },
    {
        "Name": "Plasma Coil: V5",
        "Id": 50150079,
        "Address": "0x00142E20",
        "CompareType": 1,
        "CheckType": 1,
        "CheckValue": 1408000
    },
    {
        "Name": "Operation: IRON SHIELD/Secure the Area",
        "Id": 50040006,
        "Address": "0x00142738",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Operation: IRON SHIELD/Air Assault",
        "Id": 50040007,
        "Address": "0x00142739",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Operation: IRON SHIELD/Turret Command",
        "Id": 50040008,
        "Address": "0x0014273A",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Operation: IRON SHIELD/Under the Gun",
        "Id": 50040009,
        "Address": "0x0014273B",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Operation: IRON SHIELD/Hit n' Run",
        "Id": 50040010,
        "Address": "0x0014273C",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Operation: BLACK TIDE/The Battle of Blackwater City",
        "Id": 50120002,
        "Address": "0x0014273D",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Operation: BLACK TIDE/The Bridge",
        "Id": 50120003,
        "Address": "0x0014273E",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Operation: BLACK TIDE/Counterattack",
        "Id": 50120004,
        "Address": "0x00142C40",  # As same as Gravity-Boots event
        "CheckType": 0,
        "AddressBit": 3
    },
    {
        "Name": "Operation: URBAN STORM/Countdown",
        "Id": 50260001,
        "Address": "0x00142747",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Operation: URBAN STORM/Urban Combat",
        "Id": 50260002,
        "Address": "0x00142748",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Operation: URBAN STORM/Tower Attack",
        "Id": 50260003,
        "Address": "0x00142749",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Operation: URBAN STORM/Air Superiority",
        "Id": 50260004,
        "Address": "0x0014274A",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Operation: URBAN STORM/Turret Command",
        "Id": 50260005,
        "Address": "0x0014274B",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Operation: DEATH VALLEY/The Tunnels of Outpost X12",
        "Id": 50180004,
        "Address": "0x00142742",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Operation: DEATH VALLEY/Ambush in Red Rock Valley",
        "Id": 50180005,
        "Address": "0x00142743",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Operation: DEATH VALLEY/Assassination",
        "Id": 50180006,
        "Address": "0x00142744",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Operation: DEATH VALLEY/Reclaim the Valley",
        "Id": 50180007,
        "Address": "0x00142745",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Operation: DEATH VALLEY/X12 Endgame",
        "Id": 50180008,
        "Address": "0x00142746",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Qwark Vid Comics/Qwark VidComic 1 Clear",
        "Id": 50310000,
        "Address": "0x00142734",
        "CheckType": 0,
        "AddressBit": 1
    },
    {
        "Name": "Qwark Vid Comics/Qwark VidComic 2 Clear",
        "Id": 50330000,
        "Address": "0x00142734",
        "CheckType": 0,
        "AddressBit": 3
    },
    {
        "Name": "Qwark Vid Comics/Qwark VidComic 3 Clear",
        "Id": 50340000,
        "Address": "0x00142734",
        "CheckType": 0,
        "AddressBit": 4
    },
    {
        "Name": "Qwark Vid Comics/Qwark VidComic 4 Clear",
        "Id": 50320000,
        "Address": "0x00142734",
        "CheckType": 0,
        "AddressBit": 2
    },
    {
        "Name": "Qwark Vid Comics/Qwark VidComic 5 Clear",
        "Id": 50350000,
        "Address": "0x00142734",
        "CheckType": 0,
        "AddressBit": 5
    },
    {
        "Name": "Destroy the Momma Tyhrranoid/IRON. HARD. ABS.",
        "Id": 50090004,
        "Address": "0x0014271D",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Operation: ISLAND STRIKE/Assault on Kavu Island",
        "Id": 50290000,
        "Address": "0x0014274C",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Operation: ISLAND STRIKE/Dogfight over Kavu Island",
        "Id": 50290001,
        "Address": "0x0014274D",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Operation: ISLAND STRIKE/Operation Thunderbolt",
        "Id": 50290002,
        "Address": "0x0014274F",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Operation: ISLAND STRIKE/The Final Battle",
        "Id": 50290003,
        "Address": "0x00142750",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Stay Squeaky Clean (SP)/Complete the Path of Death without a hit",
        "Id": 50020005,
        "Address": "0x001D54B1",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Armor Vendor/Turn Up The Heat! (SP)",
        "Id": 50030030,
        "Address": "0x001D54B4",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Qwark Vid Comics/Strive for arcade perfection (SP)",
        "Id": 50030031,
        "Address": "0x001D54B2",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "VR Training/Beat Helga's Best Time (0:50) (SP)",
        "Id": 50030032,
        "Address": "0x001D54B3",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Bridge/Monkeying Around (SP)",
        "Id": 50030033,
        "Address": "0x001D54B5",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Reflect on how to score (SP)/Kill 25 enemies with the Refractor",
        "Id": 50040011,
        "Address": "0x001D54B6",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Bugs to Birds (SP)/Turn 15 Floranian Blood Flies into ducks.",
        "Id": 50050005,
        "Address": "0x001D54B7",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Bash the bug (SP)/Beat Scorpio using only the wrench",
        "Id": 50070037,
        "Address": "0x001D54B8",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Be an eight time champ (SP)/Beat all the Gauntlet challenges",
        "Id": 50070038,
        "Address": "0x001D54B9",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Flee Flawlessly (SP)/Complete a Gauntlet without taking a hit",
        "Id": 50070039,
        "Address": "0x001D54BA",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Lights, camera action! (SP)/Destroy 5 Floating Cameras in the gauntlet.",
        "Id": 50070040,
        "Address": "0x001D54BB",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Search for sunken treasure (SP)/Blow up 40 underwater crates",
        "Id": 50080004,
        "Address": "0x001D54BC",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Be a Sharpshooter (SP)/Snipe 10 Tyhrranoids in the towers",
        "Id": 50090005,
        "Address": "0x001D54BD",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Get to the belt (SP)/Get onto the floating asteroid ring",
        "Id": 50110004,
        "Address": "0x001D54BE",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Bash the party (SP)/Kill 20 enemies with the wrench",
        "Id": 50120005,
        "Address": "0x001D54BF",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Feeling Lucky (SP)/Win the jackpot",
        "Id": 50130005,
        "Address": "0x001D54C0",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "You break it, you win it (SP)/Smash up the Robot Base",
        "Id": 50140003,
        "Address": "0x001D54C1",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "2002 was a good year in the city (SP)/Destroy the blimp",
        "Id": 50160001,
        "Address": "0x001D54C2",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Suck it up! (SP)/Kill 40 enemies using the Suck Cannon",
        "Id": 50170004,
        "Address": "0x001D54C3",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Aim High (SP)/Kill 10 Skreeducks",
        "Id": 50170005,
        "Address": "0x001D54C4",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Go for hang time (SP)/Get 2 seconds of air with the Turbo Slider",
        "Id": 50180009,
        "Address": "0x001D54B0",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Zap back at ya' (SP)/Kill 10 enemies with the Refractor",
        "Id": 50180010,
        "Address": "0x001D54C5",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Break the Dan (SP)/Break the Dan o7",
        "Id": 50190002,
        "Address": "0x001D54C6",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Spread Your Germs (SP)/Infect 30 enemies.",
        "Id": 50220001,
        "Address": "0x001D54C7",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Gather Sewer Crystals/Hit the motherload (SP)",
        "Id": 50280006,
        "Address": "0x001D54C8",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Qwark Vid Comics/VC1 - Set a new record for Qwark (2:40) (SP)",
        "Id": 50310003,
        "Address": "0x001D54C9",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Qwark Vid Comics/VC2 - Set a new record for Qwark (2:10) (SP)",
        "Id": 50330003,
        "Address": "0x001D54CB",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Qwark Vid Comics/VC3 - Set a new record for Qwark (1:50) (SP)",
        "Id": 50340003,
        "Address": "0x001D54CC",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Qwark Vid Comics/VC4 - Set a new record for Qwark (4:45) (SP)",
        "Id": 50320003,
        "Address": "0x001D54CA",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Qwark Vid Comics/VC5 - Set a new record for Qwark (2:00) (SP)",
        "Id": 50350003,
        "Address": "0x001D54CD",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "VR Training/VR Gadget Training",
        "Id": 50030018,
        "Address": "0x00142765",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "VR Training/Warm Up",
        "Id": 50030019,
        "Address": "0x00142766",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "VR Training/Don't Look Down",
        "Id": 50030020,
        "Address": "0x00142767",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "VR Training/Speed Round",
        "Id": 50030021,
        "Address": "0x00142768",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "VR Training/Hot Stepper",
        "Id": 50030022,
        "Address": "0x00142769",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "VR Training/90 Second Slayer",
        "Id": 50030023,
        "Address": "0x0014276A",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "VR Training/The Shocker",
        "Id": 50030024,
        "Address": "0x0014276B",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "VR Training/Wrench Beatdown",
        "Id": 50030025,
        "Address": "0x0014276C",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "VR Training/Nerves of Titanium",
        "Id": 50030026,
        "Address": "0x0014276D",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Slim Cognito/Received Mini-Turret Glove",
        "Id": 50080005,
        "Address": "0x00142CB5",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Slim Cognito/Received Lava Gun",
        "Id": 50080006,
        "Address": "0x00142CB1",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Slim Cognito/Received Shield Charger",
        "Id": 50080007,
        "Address": "0x00142CB6",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Slim Cognito/Received Bouncer",
        "Id": 50080008,
        "Address": "0x00142CB3",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Slim Cognito/Received Plasma Coil",
        "Id": 50080009,
        "Address": "0x00142CB0",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Explore Crash Site/Master Plan",
        "Id": 50170002,
        "Address": "0x00142C52",  # weird address but it's correct
        "CheckType": 0,
        "AddressBit": 2
    },
    {
        "Name": "2nd Building Upper/Ratchet trophy",
        "Id": 50020006,
        "Address": "0x00142790",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Above the tall elevator/Clank trophy",
        "Id": 50130006,
        "Address": "0x00142791",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Before Qwark's room/Qwark trophy",
        "Id": 50190003,
        "Address": "0x00142792",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "First Corner/Dr Nefarious trophy",
        "Id": 50170006,
        "Address": "0x00142793",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "In the Window/Skrunch trophy",
        "Id": 50160005,
        "Address": "0x00142794",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Atop the ladder/Lawrence trophy",
        "Id": 50220002,
        "Address": "0x00142795",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Around the Island/Plumber trophy",
        "Id": 50050006,
        "Address": "0x00142796",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "In the Glass House/Courtney Gears trophy",
        "Id": 50140004,
        "Address": "0x00142797",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Atop the pillar/AL trophy",
        "Id": 50090006,
        "Address": "0x00142798",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Titanium Collector trophy",
        "Id": 50030034,
        "Address": "0x00142799",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Friend of the Rangers trophy",
        "Id": 50030035,
        "Address": "0x0014279D",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation Champion trophy",
        "Id": 50030036,
        "Address": "0x0014279C",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Skill Master trophy",
        "Id": 50030037,
        "Address": "0x0014279A",
        "CheckType": 0,
        "AddressBit": 0
    },
    # Todo: NG+ Long term trophies
    # Nano Finder trophy 0x0014279b
    # Omega Arsenal trophy 0x0014279e

    {
        "Name": "Nanotech Levels 11-15/Nanotech Milestone: 11",
        "Id": 50250011,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 10
        # "Checks": [
        #     {
        #         "Address": "0x001A4E18",
        #         "CheckType": 0,
        #         "AddressBit": 0
        #     },
        #     {
        #         "Address": "0x001A7430",
        #         "CompareType": 0,
        #         "CheckType": 1,
        #         "CheckValue": "11"
        #     }
        # ]
    },
    {
        "Name": "Nanotech Levels 11-15/Nanotech Milestone: 12",
        "Id": 50250012,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 11
    },
    {
        "Name": "Nanotech Levels 11-15/Nanotech Milestone: 13",
        "Id": 50250013,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 12
    },
    {
        "Name": "Nanotech Levels 11-15/Nanotech Milestone: 14",
        "Id": 50250014,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 13
    },
    {
        "Name": "Nanotech Levels 11-15/Nanotech Milestone: 15",
        "Id": 50250015,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 14
    },
    {
        "Name": "Nanotech Levels 16-20/Nanotech Milestone: 16",
        "Id": 50250016,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 15
    },
    {
        "Name": "Nanotech Levels 16-20/Nanotech Milestone: 17",
        "Id": 50250017,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 16
    },
    {
        "Name": "Nanotech Levels 16-20/Nanotech Milestone: 18",
        "Id": 50250018,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 17
    },
    {
        "Name": "Nanotech Levels 16-20/Nanotech Milestone: 19",
        "Id": 50250019,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 18
    },
    {
        "Name": "Nanotech Levels 16-20/Nanotech Milestone: 20",
        "Id": 50250020,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 19
    },
    {
        "Name": "Nanotech Levels 21-25/Nanotech Milestone: 21",
        "Id": 50250021,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 20
    },
    {
        "Name": "Nanotech Levels 21-25/Nanotech Milestone: 22",
        "Id": 50250022,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 21
    },
    {
        "Name": "Nanotech Levels 21-25/Nanotech Milestone: 23",
        "Id": 50250023,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 22
    },
    {
        "Name": "Nanotech Levels 21-25/Nanotech Milestone: 24",
        "Id": 50250024,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 23
    },
    {
        "Name": "Nanotech Levels 21-25/Nanotech Milestone: 25",
        "Id": 50250025,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 24
    },
    {
        "Name": "Nanotech Levels 26-30/Nanotech Milestone: 26",
        "Id": 50250026,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 25
    },
    {
        "Name": "Nanotech Levels 26-30/Nanotech Milestone: 27",
        "Id": 50250027,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 26
    },
    {
        "Name": "Nanotech Levels 26-30/Nanotech Milestone: 28",
        "Id": 50250028,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 27
    },
    {
        "Name": "Nanotech Levels 26-30/Nanotech Milestone: 29",
        "Id": 50250029,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 28
    },
    {
        "Name": "Nanotech Levels 26-30/Nanotech Milestone: 30",
        "Id": 50250030,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 29
    },
    {
        "Name": "Nanotech Levels 31-35/Nanotech Milestone: 31",
        "Id": 50250031,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 30
    },
    {
        "Name": "Nanotech Levels 31-35/Nanotech Milestone: 32",
        "Id": 50250032,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 31
    },
    {
        "Name": "Nanotech Levels 31-35/Nanotech Milestone: 33",
        "Id": 50250033,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 32
    },
    {
        "Name": "Nanotech Levels 31-35/Nanotech Milestone: 34",
        "Id": 50250034,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 33
    },
    {
        "Name": "Nanotech Levels 31-35/Nanotech Milestone: 35",
        "Id": 50250035,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 34
    },
    {
        "Name": "Nanotech Levels 36-40/Nanotech Milestone: 36",
        "Id": 50250036,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 35
    },
    {
        "Name": "Nanotech Levels 36-40/Nanotech Milestone: 37",
        "Id": 50250037,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 36
    },
    {
        "Name": "Nanotech Levels 36-40/Nanotech Milestone: 38",
        "Id": 50250038,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 37
    },
    {
        "Name": "Nanotech Levels 36-40/Nanotech Milestone: 39",
        "Id": 50250039,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 38
    },
    {
        "Name": "Nanotech Levels 36-40/Nanotech Milestone: 40",
        "Id": 50250040,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 39
    },
    {
        "Name": "Nanotech Levels 41-45/Nanotech Milestone: 41",
        "Id": 50250041,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 40
    },
    {
        "Name": "Nanotech Levels 41-45/Nanotech Milestone: 42",
        "Id": 50250042,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 41
    },
    {
        "Name": "Nanotech Levels 41-45/Nanotech Milestone: 43",
        "Id": 50250043,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 42
    },
    {
        "Name": "Nanotech Levels 41-45/Nanotech Milestone: 44",
        "Id": 50250044,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 43
    },
    {
        "Name": "Nanotech Levels 41-45/Nanotech Milestone: 45",
        "Id": 50250045,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 44
    },
    {
        "Name": "Nanotech Levels 46-50/Nanotech Milestone: 46",
        "Id": 50250046,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 45
    },
    {
        "Name": "Nanotech Levels 46-50/Nanotech Milestone: 47",
        "Id": 50250047,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 46
    },
    {
        "Name": "Nanotech Levels 46-50/Nanotech Milestone: 48",
        "Id": 50250048,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 47
    },
    {
        "Name": "Nanotech Levels 46-50/Nanotech Milestone: 49",
        "Id": 50250049,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 48
    },
    {
        "Name": "Nanotech Levels 46-50/Nanotech Milestone: 50",
        "Id": 50250050,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 49
    },
    {
        "Name": "Nanotech Levels 51-55/Nanotech Milestone: 51",
        "Id": 50250051,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 50
    },
    {
        "Name": "Nanotech Levels 51-55/Nanotech Milestone: 52",
        "Id": 50250052,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 51
    },
    {
        "Name": "Nanotech Levels 51-55/Nanotech Milestone: 53",
        "Id": 50250053,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 52
    },
    {
        "Name": "Nanotech Levels 51-55/Nanotech Milestone: 54",
        "Id": 50250054,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 53
    },
    {
        "Name": "Nanotech Levels 51-55/Nanotech Milestone: 55",
        "Id": 50250055,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 54
    },
    {
        "Name": "Nanotech Levels 56-60/Nanotech Milestone: 56",
        "Id": 50250056,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 55
    },
    {
        "Name": "Nanotech Levels 56-60/Nanotech Milestone: 57",
        "Id": 50250057,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 56
    },
    {
        "Name": "Nanotech Levels 56-60/Nanotech Milestone: 58",
        "Id": 50250058,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 57
    },
    {
        "Name": "Nanotech Levels 56-60/Nanotech Milestone: 59",
        "Id": 50250059,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 58
    },
    {
        "Name": "Nanotech Levels 56-60/Nanotech Milestone: 60",
        "Id": 50250060,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 59
    },
    {
        "Name": "Nanotech Levels 61-65/Nanotech Milestone: 61",
        "Id": 50250061,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 60
    },
    {
        "Name": "Nanotech Levels 61-65/Nanotech Milestone: 62",
        "Id": 50250062,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 61
    },
    {
        "Name": "Nanotech Levels 61-65/Nanotech Milestone: 63",
        "Id": 50250063,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 62
    },
    {
        "Name": "Nanotech Levels 61-65/Nanotech Milestone: 64",
        "Id": 50250064,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 63
    },
    {
        "Name": "Nanotech Levels 61-65/Nanotech Milestone: 65",
        "Id": 50250065,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 64
    },
    {
        "Name": "Nanotech Levels 66-70/Nanotech Milestone: 66",
        "Id": 50250066,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 65
    },
    {
        "Name": "Nanotech Levels 66-70/Nanotech Milestone: 67",
        "Id": 50250067,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 66
    },
    {
        "Name": "Nanotech Levels 66-70/Nanotech Milestone: 68",
        "Id": 50250068,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 67
    },
    {
        "Name": "Nanotech Levels 66-70/Nanotech Milestone: 69",
        "Id": 50250069,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 68
    },
    {
        "Name": "Nanotech Levels 66-70/Nanotech Milestone: 70",
        "Id": 50250070,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 69
    },
    {
        "Name": "Nanotech Levels 71-75/Nanotech Milestone: 71",
        "Id": 50250071,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 70
    },
    {
        "Name": "Nanotech Levels 71-75/Nanotech Milestone: 72",
        "Id": 50250072,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 71
    },
    {
        "Name": "Nanotech Levels 71-75/Nanotech Milestone: 73",
        "Id": 50250073,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 72
    },
    {
        "Name": "Nanotech Levels 71-75/Nanotech Milestone: 74",
        "Id": 50250074,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 73
    },
    {
        "Name": "Nanotech Levels 71-75/Nanotech Milestone: 75",
        "Id": 50250075,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 74
    },
    {
        "Name": "Nanotech Levels 76-80/Nanotech Milestone: 76",
        "Id": 50250076,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 75
    },
    {
        "Name": "Nanotech Levels 76-80/Nanotech Milestone: 77",
        "Id": 50250077,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 76
    },
    {
        "Name": "Nanotech Levels 76-80/Nanotech Milestone: 78",
        "Id": 50250078,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 77
    },
    {
        "Name": "Nanotech Levels 76-80/Nanotech Milestone: 79",
        "Id": 50250079,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 78
    },
    {
        "Name": "Nanotech Levels 76-80/Nanotech Milestone: 80",
        "Id": 50250080,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 79
    },
    {
        "Name": "Nanotech Levels 81-85/Nanotech Milestone: 81",
        "Id": 50250081,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 80
    },
    {
        "Name": "Nanotech Levels 81-85/Nanotech Milestone: 82",
        "Id": 50250082,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 81
    },
    {
        "Name": "Nanotech Levels 81-85/Nanotech Milestone: 83",
        "Id": 50250083,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 82
    },
    {
        "Name": "Nanotech Levels 81-85/Nanotech Milestone: 84",
        "Id": 50250084,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 83
    },
    {
        "Name": "Nanotech Levels 81-85/Nanotech Milestone: 85",
        "Id": 50250085,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 84
    },
    {
        "Name": "Nanotech Levels 86-90/Nanotech Milestone: 86",
        "Id": 50250086,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 85
    },
    {
        "Name": "Nanotech Levels 86-90/Nanotech Milestone: 87",
        "Id": 50250087,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 86
    },
    {
        "Name": "Nanotech Levels 86-90/Nanotech Milestone: 88",
        "Id": 50250088,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 87
    },
    {
        "Name": "Nanotech Levels 86-90/Nanotech Milestone: 89",
        "Id": 50250089,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 88
    },
    {
        "Name": "Nanotech Levels 86-90/Nanotech Milestone: 90",
        "Id": 50250090,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 89
    },
    {
        "Name": "Nanotech Levels 91-95/Nanotech Milestone: 91",
        "Id": 50250091,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 90
    },
    {
        "Name": "Nanotech Levels 91-95/Nanotech Milestone: 92",
        "Id": 50250092,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 91
    },
    {
        "Name": "Nanotech Levels 91-95/Nanotech Milestone: 93",
        "Id": 50250093,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 92
    },
    {
        "Name": "Nanotech Levels 91-95/Nanotech Milestone: 94",
        "Id": 50250094,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 93
    },
    {
        "Name": "Nanotech Levels 91-95/Nanotech Milestone: 95",
        "Id": 50250095,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 94
    },
    {
        "Name": "Nanotech Levels 96-100/Nanotech Milestone: 96",
        "Id": 50250096,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 95
    },
    {
        "Name": "Nanotech Levels 96-100/Nanotech Milestone: 97",
        "Id": 50250097,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 96
    },
    {
        "Name": "Nanotech Levels 96-100/Nanotech Milestone: 98",
        "Id": 50250098,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 97
    },
    {
        "Name": "Nanotech Levels 96-100/Nanotech Milestone: 99",
        "Id": 50250099,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 98
    },
    {
        "Name": "Nanotech Levels 96-100/Nanotech Milestone: 100",
        "Id": 50250100,
        "Address": "0x00142668",
        "CompareType": 1,  # Greater Than
        "CheckType": 1,
        "CheckValue": 99
    },
    # Map Tracker duplicates
    {
        "Name": "Veldin/Received Shock Blaster",
        "Id": 50010000,
        "Address": "0x001426E0",
        # Use event flag rather than weapon unlock address to avoid issues with weapon randomizer
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Veldin/Received Nitro Launcher",
        "Id": 50010001,
        "Address": "0x001426E1",
        # Use event flag rather than weapon unlock address to avoid issues with weapon randomizer
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Veldin/Infobot: Florana",
        "Id": 50010002,
        "Address": "0x001426E4",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Florana/Received Plasma Whip",
        "Id": 50020000,
        "Address": "0x00142D1F",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Florana/Received N60 Storm",
        "Id": 50020001,
        "Address": "0x00142CCF",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Florana/Titanium Bolt 1",
        "Id": 50020002,
        "Address": "0x001BBB29",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Florana/Titanium Bolt 2",
        "Id": 50020003,
        "Address": "0x001BBB2A",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Florana/Defeat Qwark",
        "Id": 50020004,
        "Address": "0x001426E7",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Received Suck Cannon",
        "Id": 50030000,
        "Address": "0x00142D27",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Received Infector",
        "Id": 50030001,
        "Address": "0x00142CD7",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Nerves of Titanium Bolt",
        "Id": 50030027,
        "Address": "0x001BBB30",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Gadget Training Titanium Bolt",
        "Id": 50030015,
        "Address": "0x001BBB31",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Received Magna Plate Armor",
        "Id": 50030002,
        "Address": "0x001426A0",
        "CheckValue": 1,
        "CheckType": 3
    },
    {
        "Name": "Phoenix/Received Adamantine Armor",
        "Id": 50030003,
        "Address": "0x001426A0",
        "CheckValue": 2,
        "CheckType": 3
    },
    {
        "Name": "Phoenix/Received Aegis Mark V Armor",
        "Id": 50030004,
        "Address": "0x001426A0",
        "CheckValue": 3,
        "CheckType": 3
    },
    {
        "Name": "Phoenix/Received Infernox Armor",
        "Id": 50030005,
        "Checks": [
            {
                "Address": "0x001D54B4",
                "CheckType": 0,
                "AddressBit": 0
            },
            {
                "Address": "0x001D545C",
                "CheckValue": 3,
                "CheckType": 0
            }
        ]
    },
    {
        "Name": "Phoenix/Received Hacker",
        "Id": 50030016,
        # "Address": "0x00142CB4",
        "Address": "0x00142765",  # Same as VR Gadget Training mission completion
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Received Hypershot",
        "Id": 50030017,
        # "Address": "0x00142CAB",
        "Address": "0x00142765",  # Same as VR Gadget Training mission completion
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Infobot: Marcadia",
        "Id": 50030006,
        "Checks": [
            {
                "Address": "0x001426E9",
                "CheckValue": 1,
                "CheckType": 0
            },
            {
                "Address": "0x001D545C",
                "CheckValue": 3,
                "CheckType": 0
            }
        ]
    },
    {
        "Name": "Phoenix/Infobot: Koros",
        "Id": 50030007,
        "Address": "0x001D553E",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Infobot: Annihilation Nation",
        "Id": 50030008,
        "Address": "0x001426EB",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Infobot: Aquatos",
        "Id": 50030009,
        # " Address": 0x001426F6, #  Correct Infobot address
        "Address": "0x0014276F",  # Same as Tyhrra-Guise Getting event. This event behinds Phoenix Ship event.
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Infobot: Tyhrranosis",
        "Id": 50030010,
        # "Address": "0x00142C1B",
        "Address": "0x0014275E",  # Same as 1 Sewer Crystal Traded
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Infobot: Daxx",
        "Id": 50030011,
        #  "Address": "0x00142765",
        "Address": "0x00142765",  # Same as T-Bolt: VR training
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Metropolis/Infobot: Crash Site",
        "Id": 50160004,
        #  "Address": "0x001D5541",
        "Address": "0x00142708",  # Same as defeat Giant Cronk
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Infobot: Qwarks Hideout",
        "Id": 50030014,
        "Address": "0x00142734",
        "CheckType": 0,
        "AddressBit": 5  # 3E 00X0_0000
    },
    {
        "Name": "Zeldrin Starport/Qwark Vidcomic 4",
        "Id": 50100003,
        "Address": "0x001426E2",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Qwark Vidcomic 5",
        "Id": 50030029,
        "Address": "0x001D5553",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Infobot: Metropolis",
        "Id": 50030012,
        "Address": "0x001D5550",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Marcadia/Received Spitting Hydra",
        "Id": 50040000,
        "Address": "0x00142CE7",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Marcadia/Received Refractor",
        "Id": 50040001,
        # "Address": "0x00142CB2", # item flag
        "Address": "0x00142C29",  # Marcadia Mission event Flag
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Marcadia/Titanium Bolt 1",
        "Id": 50040002,
        "Address": "0x001BBB39",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Marcadia/Titanium Bolt 2",
        "Id": 50040003,
        "Address": "0x001BBB3A",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Marcadia/Titanium Bolt 3",
        "Id": 50040004,
        "Address": "0x001BBB3B",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Marcadia/Qwark Vidcomic 1",
        "Id": 50040005,
        "Address": "0x001426ea",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Received Agents of Doom",
        "Id": 50070000,
        "Address": "0x00142CF7",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Received Tyhrra-Guise",
        "Id": 50070001,
        "Address": "0x0014276F",  # Same as Grand Prize Bout(Tyhrra-Guise Getting event)
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Titanium Bolt 1",
        "Id": 50070002,
        "Address": "0x001BBB51",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Titanium Bolt 2",
        "Id": 50070003,
        "Address": "0x001BBB52",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Grand Prize Bout",
        "Id": 50070004,
        "Address": "0x0014276F",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/The Terrible Two",
        "Id": 50070005,
        "Address": "0x00142772",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Robot Rampage",
        "Id": 50070006,
        "Address": "0x00142773",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Two Minute Warning",
        "Id": 50070007,
        "Address": "0x00142774",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/90 Seconds of Carnage",
        "Id": 50070008,
        "Address": "0x00142775",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Onslaught",
        "Id": 50070009,
        "Address": "0x00142776",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Whip It Good",
        "Id": 50070010,
        "Address": "0x00142777",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Hydra'n Seek",
        "Id": 50070011,
        "Address": "0x00142778",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Championship Bout",
        "Id": 50070012,
        "Address": "0x00142779",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Ninja Challenge",
        "Id": 50070014,
        "Address": "0x0014277D",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Counting Ducks",
        "Id": 50070015,
        "Address": "0x0014277E",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Cycling Weapons",
        "Id": 50070016,
        "Address": "0x0014277F",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/One Hit Wonder",
        "Id": 50070017,
        "Address": "0x00142780",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Time to Suck",
        "Id": 50070018,
        "Address": "0x00142781",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Naptime",
        "Id": 50070019,
        "Address": "0x00142782",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Meet Courtney - Arena",
        "Id": 50070013,
        "Address": "0x00142771",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/More Cycling Weapons",
        "Id": 50070020,
        "Address": "0x00142783",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Dodge the Twins",
        "Id": 50070021,
        "Address": "0x00142784",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Chop Chop",
        "Id": 50070022,
        "Address": "0x00142785",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Sleep Inducer",
        "Id": 50070023,
        "Address": "0x00142786",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/The Other White Meat",
        "Id": 50070024,
        "Address": "0x00142787",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Championship Bout II",
        "Id": 50070025,
        "Address": "0x00142788",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/It's Qwarktastic!",
        "Id": 50070026,
        "Address": "0x00142789",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Heat Street",
        "Id": 50070027,
        "Address": "0x0014276E",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Crispy Critter",
        "Id": 50070028,
        "Address": "0x0014277A",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Pyro Playground",
        "Id": 50070029,
        "Address": "0x0014277B",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Suicide Run",
        "Id": 50070030,
        "Address": "0x0014277C",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/BBQ Boulevard",  # (Meet Courtney - Gauntlet)
        "Id": 50070031,
        "Address": "0x00142770",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Maze of Blaze",
        "Id": 50070032,
        "Address": "0x0014278A",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Cremation Station",
        "Id": 50070033,
        "Address": "0x0014278B",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/The Annihilator",
        "Id": 50070034,
        "Address": "0x0014278C",
        "CheckType": 0,
        "AddressBit": 0
    },
    # {
    #     "Name": "Annihilation Nation/Qwark VidComic 2",
    #     "Id": 50070035,
    #     "Address": "0x001D5551",
    #     "CheckType": 0,
    #     "AddressBit": 0
    # },
    # {
    #     "Name": "Annihilation Nation/Qwark VidComic 3",
    #     "Id": 50070036,
    #     "Address": "0x001D5552",
    #     "CheckType": 0,
    #     "AddressBit": 0
    # },
    {
        "Name": "Aquatos/Received Flux Rifle",
        "Id": 50080000,
        "Address": "0x00142D0F",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Aquatos/Titanium Bolt 1",
        "Id": 50080001,
        "Address": "0x001BBB5A",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Aquatos/Titanium Bolt 2",
        "Id": 50080002,
        "Address": "0x001BBB5B",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Aquatos/Titanium Bolt 3",
        "Id": 50080003,
        "Address": "0x001BBB59",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Aquatos/Titanium Bolt 4",
        "Id": 50280000,
        "Address": "0x001BBBF9",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Aquatos/Titanium Bolt 5",
        "Id": 50280001,
        "Address": "0x001BBBFA",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Aquatos/1 Sewer Crystal Traded",
        "Id": 50280002,
        "Address": "0x0014275E",  # JP: 1426DE,
        "CompareType": 1,  # Greater than
        "CheckType": 3,  # Byte type
        "CheckValue": 0
    },
    {
        "Name": "Aquatos/5 Sewer Crystals Traded",
        "Id": 50280003,
        "Address": "0x0014275E",  # JP: 1426DE,
        "CheckType": 3,  # Byte type
        "CompareType": 1,  # Greater than
        "CheckValue": 4
    },
    {
        "Name": "Aquatos/10 Sewer Crystals Traded",
        "Id": 50280004,
        "Address": "0x0014275E",  # JP: 1426DE,
        "CheckType": 3,  # Byte type
        "CompareType": 1,  # Greater than
        "CheckValue": 9  # 0x9
    },
    {
        "Name": "Aquatos/20 Sewer Crystals Traded",
        "Id": 50280005,
        "Address": "0x0014275E",  # JP: 1426DE,
        "CheckType": 3,  # Byte type
        "CompareType": 1,  # Greater than
        "CheckValue": 19  # 0x13
    },
    {
        "Name": "Tyhrranosis/Received Annihilator",
        "Id": 50090000,
        "Address": "0x00142CDF",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Tyhrranosis/Received Holo-Shield Glove",
        "Id": 50090001,
        "Address": "0x00142D07",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Tyhrranosis/Titanium Bolt 1",
        "Id": 50090002,
        "Address": "0x001BBB62",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Tyhrranosis/Titanium Bolt 2",
        "Id": 50090003,
        "Address": "0x001BBB61",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Daxx/Titanium Bolt 1",
        "Id": 50050001,
        "Address": "0x001BBB41",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Daxx/Titanium Bolt 2",
        "Id": 50050002,
        "Address": "0x001BBB42",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Daxx/Received Charge Boots",
        "Id": 50050003,
        "Address": "0x00142CBD",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Daxx/Infobot: Obani Gemini",
        "Id": 50050000,
        "Address": "0x001D553B",
        # Infobot Address: "0x00142C29" bit 3
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Daxx/Courtney's Music Vid",
        "Id": 50050004,
        # "Address": "0x00143B39", #  ??
        "Address": "0x0014275B",  # Daxx Courtney Room
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Obani Gemini/Received Disc Blade Gun",
        "Id": 50110000,
        "Address": "0x00142CEF",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Obani Gemini/Titanium Bolt 1",
        "Id": 50110001,
        "Address": "0x001BBB72",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Obani Gemini/Titanium Bolt 2",
        "Id": 50110002,
        "Address": "0x001BBB71",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Obani Gemini/Infobot: Blackwater City",
        "Id": 50110003,
        "Address": "0x00142BB2",
        "CheckType": 0,
        "AddressBit": 3  # 08: 0000_X000
    },
    {
        "Name": "Blackwater/Received Grav Boots",
        "Id": 50120000,
        #  "Address": "0x00142CAD",
        "Address": "0x00142C40",
        "CheckType": 0,
        "AddressBit": 3  # 0x08: 0000_X000
    },
    {
        "Name": "Blackwater/Infobot: Holostar Studios",
        "Id": 50120001,
        "Address": "0x00142705",
        #  "Address": "0x00142771", #  WA: Same as Meet Courtney - Arena
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Holostar/Received Rift Inducer",
        "Id": 50130000,
        "Address": "0x00142CFF",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Holostar/Titanium Bolt 1",
        "Id": 50130001,
        "Address": "0x001BBB82",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Holostar/Titanium Bolt 2",
        "Id": 50130002,
        "Address": "0x001BBB83",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Holostar/Titanium Bolt 3",
        "Id": 50130003,
        "Address": "0x001BBB81",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Holostar/Infobot: Obani Draco",
        "Id": 50130004,
        "Address": "0x00142713",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Obani Draco/Infobot: Zeldrin Starport",
        "Id": 50210000,
        "Address": "0x0014270D",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Zeldrin Starport/Received Bolt Grabber V2",
        "Id": 50100000,
        "Address": "0x00142CA7",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Zeldrin Starport/Titanium Bolt 1",
        "Id": 50100001,
        "Address": "0x001BBB6A",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Zeldrin Starport/Titanium Bolt 2",
        "Id": 50100002,
        "Address": "0x001BBB69",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Metropolis/Received Map-O-Matic",
        "Id": 50260006,
        #  "Address": "0x00142CA5", #  item flag
        "Address": "0x00142C64",  # Metropolis Mission Clear
        "CheckType": 0,
        "AddressBit": 5  # 0x20 : 00X0_0000
    },
    {
        "Name": "Metropolis/Titanium Bolt 1",
        "Id": 50160000,
        "Address": "0x001BBB99",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Metropolis/Titanium Bolt 2",
        "Id": 50160003,
        "Address": "0x001BBB9A",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Metropolis/Titanium Bolt 3",
        "Id": 50260000,
        "Address": "0x001BBBE9",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Metropolis/The AAAAGE OF ROBOTS!!!",
        "Id": 50160002,
        "Address": "0x0014275C",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Crash Site/Received Nano-Pak",
        "Id": 50170001,
        "Address": "0x00142CC0",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Crash Site/Titanium Bolt",
        "Id": 50170000,
        "Address": "0x001BBBA1",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Crash Site/Infobot: Aridia",
        "Id": 50170003,
        "Address": "0x00142C52",
        # "Address": "0x00142722",
        # Correct Address: 0x00142C52(4bit: 0x07->0x0f) (US), but Event is not happened in some case.
        "CheckType": 0,
        "AddressBit": 3  # / 0x02: 0000_00X0
    },
    {
        "Name": "Aridia/Received Warp Pad",
        "Id": 50180000,
        # "Address": "0x00142CBF", #  Item flag
        "Address": "0x00142C56",  # Clear Aridia
        "CheckType": 0,
        "AddressBit": 4  # 0x10: 000X_0000
    },
    {
        "Name": "Aridia/Received Qwack-O-Ray",
        "Id": 50180001,
        "Address": "0x00142D2F",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Aridia/Titanium Bolt 1",
        "Id": 50180002,
        "Address": "0x001BBBAA",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Aridia/Titanium Bolt 2",
        "Id": 50180003,
        "Address": "0x001BBBA9",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Hideout/Received Gadgetron PDA",
        "Id": 50190000,
        "Address": "0x00142CC3",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Hideout/Titanium Bolt",
        "Id": 50190001,
        "Address": "0x001BBBB1",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Koros/Titanium Bolt 1",
        "Id": 50140000,
        "Address": "0x001BBB89",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Koros/Titanium Bolt 2",
        "Id": 50140001,
        "Address": "0x001BBB8A",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Koros/Infobot: Command Center",
        "Id": 50140002,
        "Address": "0x00142C49",
        "CheckType": 0,
        "AddressBit": 3  # 04 -> 0C: 0000_X000
    },
    {
        "Name": "Command Center/Titanium Bolt",
        "Id": 50220000,
        "Address": "0x001BBBC9",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Command Center/Dr. Nefarious Defeated!",
        "Id": 50200000,
        "Address": "0x0014270F",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Command Center/Biobliterator Defeated!",
        "Id": 50200001,
        "Address": "0x00142BB6",
        "CheckType": 0,
        "AddressBit": 6  # 40: 0X00_0000
    },
    {
        "Name": "Phoenix/VC1 - All Tokens Titanium Bolt",
        "Id": 50310001,
        "Address": "0x001BBB32",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/VC2 - All Tokens Titanium Bolt",
        "Id": 50330001,
        "Address": "0x001BBB34",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/VC3 - All Tokens Titanium Bolt",
        "Id": 50340001,
        "Address": "0x001BBB35",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/VC4 - All Tokens Titanium Bolt",
        "Id": 50320001,
        "Address": "0x001BBB33",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/VC5 - All Tokens Titanium Bolt",
        "Id": 50350001,
        "Address": "0x001BBB36",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Marcadia/Secure the Area",
        "Id": 50040006,
        "Address": "0x00142738",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Marcadia/Air Assault",
        "Id": 50040007,
        "Address": "0x00142739",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Marcadia/Turret Command",
        "Id": 50040008,
        "Address": "0x0014273A",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Marcadia/Under the Gun",
        "Id": 50040009,
        "Address": "0x0014273B",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Marcadia/Hit n' Run",
        "Id": 50040010,
        "Address": "0x0014273C",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Blackwater/The Battle of Blackwater City",
        "Id": 50120002,
        "Address": "0x0014273D",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Blackwater/The Bridge",
        "Id": 50120003,
        "Address": "0x0014273E",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Blackwater/Counterattack",
        "Id": 50120004,
        "Address": "0x00142C40",  # As same as Gravity-Boots event
        "CheckType": 0,
        "AddressBit": 3
    },
    {
        "Name": "Metropolis/Countdown",
        "Id": 50260001,
        "Address": "0x00142747",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Metropolis/Urban Combat",
        "Id": 50260002,
        "Address": "0x00142748",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Metropolis/Tower Attack",
        "Id": 50260003,
        "Address": "0x00142749",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Metropolis/Air Superiority",
        "Id": 50260004,
        "Address": "0x0014274A",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Metropolis/Turret Command",
        "Id": 50260005,
        "Address": "0x0014274B",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Aridia/The Tunnels of Outpost X12",
        "Id": 50180004,
        "Address": "0x00142742",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Aridia/Ambush in Red Rock Valley",
        "Id": 50180005,
        "Address": "0x00142743",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Aridia/Assassination",
        "Id": 50180006,
        "Address": "0x00142744",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Aridia/Reclaim the Valley",
        "Id": 50180007,
        "Address": "0x00142745",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Aridia/X12 Endgame",
        "Id": 50180008,
        "Address": "0x00142746",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Qwark VidComic 1 Clear",
        "Id": 50310000,
        "Address": "0x00142734",
        "CheckType": 0,
        "AddressBit": 1
    },
    {
        "Name": "Phoenix/Qwark VidComic 2 Clear",
        "Id": 50330000,
        "Address": "0x00142734",
        "CheckType": 0,
        "AddressBit": 3
    },
    {
        "Name": "Phoenix/Qwark VidComic 3 Clear",
        "Id": 50340000,
        "Address": "0x00142734",
        "CheckType": 0,
        "AddressBit": 4
    },
    {
        "Name": "Phoenix/Qwark VidComic 4 Clear",
        "Id": 50320000,
        "Address": "0x00142734",
        "CheckType": 0,
        "AddressBit": 2
    },
    {
        "Name": "Phoenix/Qwark VidComic 5 Clear",
        "Id": 50350000,
        "Address": "0x00142734",
        "CheckType": 0,
        "AddressBit": 5
    },
    {
        "Name": "Tyhrranosis/IRON. HARD. ABS.",
        "Id": 50090004,
        "Address": "0x0014271D",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Tyhrranosis/Assault on Kavu Island",
        "Id": 50290000,
        "Address": "0x0014274C",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Tyhrranosis/Dogfight over Kavu Island",
        "Id": 50290001,
        "Address": "0x0014274D",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Tyhrranosis/Operation Thunderbolt",
        "Id": 50290002,
        "Address": "0x0014274F",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Tyhrranosis/The Final Battle",
        "Id": 50290003,
        "Address": "0x00142750",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Florana/Complete the Path of Death without a hit",
        "Id": 50020005,
        "Address": "0x001D54B1",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Turn Up The Heat! (SP)",
        "Id": 50030030,
        "Address": "0x001D54B4",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Strive for arcade perfection (SP)",
        "Id": 50030031,
        "Address": "0x001D54B2",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Beat Helga's Best Time (0:50) (SP)",
        "Id": 50030032,
        "Address": "0x001D54B3",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Hit n' Run",
        "Id": 50030033,
        "Address": "0x001D54B5",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Marcadia/Kill 25 enemies with the Refractor",
        "Id": 50040011,
        "Address": "0x001D54B6",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Daxx/Turn 15 Floranian Blood Flies into ducks.",
        "Id": 50050005,
        "Address": "0x001D54B7",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Beat Scorpio using only the wrench",
        "Id": 50070037,
        "Address": "0x001D54B8",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Beat all the Gauntlet challenges",
        "Id": 50070038,
        "Address": "0x001D54B9",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Complete a Gauntlet without taking a hit",
        "Id": 50070039,
        "Address": "0x001D54BA",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Annihilation Nation/Destroy 5 Floating Cameras in the gauntlet.",
        "Id": 50070040,
        "Address": "0x001D54BB",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Aquatos/Blow up 40 underwater crates",
        "Id": 50080004,
        "Address": "0x001D54BC",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Tyhrranosis/Snipe 10 Tyhrranoids in the towers",
        "Id": 50090005,
        "Address": "0x001D54BD",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Obani Gemini/Get onto the floating asteroid ring",
        "Id": 50110004,
        "Address": "0x001D54BE",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Blackwater/Kill 20 enemies with the wrench",
        "Id": 50120005,
        "Address": "0x001D54BF",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Holostar/Win the jackpot",
        "Id": 50130005,
        "Address": "0x001D54C0",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Koros/Smash up the Robot Base",
        "Id": 50140003,
        "Address": "0x001D54C1",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Metropolis/Destroy the blimp",
        "Id": 50160001,
        "Address": "0x001D54C2",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Crash Site/Kill 40 enemies using the Suck Cannon",
        "Id": 50170004,
        "Address": "0x001D54C3",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Crash Site/Kill 10 Skreeducks",
        "Id": 50170005,
        "Address": "0x001D54C4",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Aridia/Get 2 seconds of air with the Turbo Slider",
        "Id": 50180009,
        "Address": "0x001D54B0",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Aridia/Kill 10 enemies with the Refractor",
        "Id": 50180010,
        "Address": "0x001D54C5",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Hideout/Break the Dan o7",
        "Id": 50190002,
        "Address": "0x001D54C6",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Command Center/Infect 30 enemies.",
        "Id": 50220001,
        "Address": "0x001D54C7",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Aquatos/Hit the motherload (SP)",
        "Id": 50280006,
        "Address": "0x001D54C8",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/VC1 - Set a new record for Qwark (2:40) (SP)",
        "Id": 50310003,
        "Address": "0x001D54C9",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/VC2 - Set a new record for Qwark (2:10) (SP)",
        "Id": 50330003,
        "Address": "0x001D54CB",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/VC3 - Set a new record for Qwark (1:50) (SP)",
        "Id": 50340003,
        "Address": "0x001D54CC",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/VC4 - Set a new record for Qwark (4:45) (SP)",
        "Id": 50320003,
        "Address": "0x001D54CA",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/VC5 - Set a new record for Qwark (2:00) (SP)",
        "Id": 50350003,
        "Address": "0x001D54CD",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/VR Gadget Training",
        "Id": 50030018,
        "Address": "0x00142765",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Warm Up",
        "Id": 50030019,
        "Address": "0x00142766",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Don't Look Down",
        "Id": 50030020,
        "Address": "0x00142767",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Speed Round",
        "Id": 50030021,
        "Address": "0x00142768",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Hot Stepper",
        "Id": 50030022,
        "Address": "0x00142769",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/90 Second Slayer",
        "Id": 50030023,
        "Address": "0x0014276A",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/The Shocker",
        "Id": 50030024,
        "Address": "0x0014276B",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Wrench Beatdown",
        "Id": 50030025,
        "Address": "0x0014276C",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Nerves of Titanium",
        "Id": 50030026,
        "Address": "0x0014276D",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Received Mini-Turret Glove",
        "Id": 50080005,
        "Address": "0x00142CB5",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Received Lava Gun",
        "Id": 50080006,
        "Address": "0x00142CB1",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Received Shield Charger",
        "Id": 50080007,
        "Address": "0x00142CB6",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Received Bouncer",
        "Id": 50080008,
        "Address": "0x00142CB3",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Phoenix/Received Plasma Coil",
        "Id": 50080009,
        "Address": "0x00142CB0",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Crash Site/Master Plan",
        "Id": 50170002,
        "Address": "0x00142C52",  # weird address but it's correct
        "CheckType": 0,
        "AddressBit": 2
    },
    {
        "Name": "Florana/Ratchet trophy",
        "Id": 50020006,
        "Address": "0x00142790",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Holostar/Clank trophy",
        "Id": 50130006,
        "Address": "0x00142791",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Hideout/Qwark trophy",
        "Id": 50190003,
        "Address": "0x00142792",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Crash Site/Dr Nefarious trophy",
        "Id": 50170006,
        "Address": "0x00142793",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Metropolis/Skrunch trophy",
        "Id": 50160005,
        "Address": "0x00142794",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Command Center/Lawrence trophy",
        "Id": 50220002,
        "Address": "0x00142795",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Daxx/Plumber trophy",
        "Id": 50050006,
        "Address": "0x00142796",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Koros/Courtney Gears trophy",
        "Id": 50140004,
        "Address": "0x00142797",
        "CheckType": 0,
        "AddressBit": 0
    },
    {
        "Name": "Tyhrranosis/AL trophy",
        "Id": 50090006,
        "Address": "0x00142798",
        "CheckType": 0,
        "AddressBit": 0
    }
    # {
    #     "Name": "Titanium Collector trophy",
    #     "Id": 50030034,
    #     "Address": "0x00142799",
    #     "CheckType": 0,
    #     "AddressBit": 0
    # },
    # {
    #     "Name": "Friend of the Rangers trophy",
    #     "Id": 50030035,
    #     "Address": "0x0014279D",
    #     "CheckType": 0,
    #     "AddressBit": 0
    # },
    # {
    #     "Name": "Annihilation Nation Champion trophy",
    #     "Id": 50030036,
    #     "Address": "0x0014279C",
    #     "CheckType": 0,
    #     "AddressBit": 0
    # },
    # {
    #     "Name": "Skill Master trophy",
    #     "Id": 50030037,
    #     "Address": "0x0014279A",
    #     "CheckType": 0,
    #     "AddressBit": 0
    # },
    # Todo: NG+ Long term trophies
    # Nano Finder trophy 0x0014279b
    # Omega Arsenal trophy 0x0014279e
]
