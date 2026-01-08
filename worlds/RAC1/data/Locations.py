from dataclasses import dataclass
from typing import Callable, Optional

from ..Logic import *

POOL_START_PLANET: str = "StartPlanet"
POOL_START_ITEM: str = "StartItem"
POOL_WEAPON: str = "Weapons"
POOL_GOLDEN_WEAPON: str = "GoldenWeapons"
POOL_GADGET: str = "Gadgets"
POOL_PACK: str = "Packs"
POOL_HELMET: str = "Helmets"
POOL_BOOT: str = "Boots"
POOL_EXTRA_ITEM: str = "ExtraItems"
POOL_GOLD_BOLT: str = "GoldBolts"
POOL_INFOBOT: str = "Infobots"
POOL_SKILLPOINT: str = "Skillpoint"

DEFAULT_LIST = list([POOL_WEAPON, POOL_GADGET, POOL_PACK, POOL_HELMET, POOL_BOOT, POOL_EXTRA_ITEM, POOL_GOLD_BOLT,
                     POOL_INFOBOT])
ALL_POOLS = list([POOL_START_PLANET, POOL_START_ITEM, POOL_WEAPON, POOL_GOLDEN_WEAPON, POOL_GADGET, POOL_PACK,
                  POOL_HELMET, POOL_BOOT, POOL_EXTRA_ITEM, POOL_GOLD_BOLT, POOL_INFOBOT, POOL_SKILLPOINT])


# noinspection PyCompatibility
@dataclass
class LocationData:
    location_id: Optional[int]
    planet: str
    name: str
    vanilla_item: Optional[str]
    pools: set[str] = frozenset()
    """All of these must be enabled for this spot to be randomized"""
    access_rule: Optional[Callable[[CollectionState, int], bool]] = None


# Novalis
NOVALIS_PLUMBER = LocationData(1, "Novalis", "Novalis: Plumber", Items.ARIDIA_INFOBOT.name, {POOL_INFOBOT})
NOVALIS_MAYOR = LocationData(2, "Novalis", "Novalis: Chairman", Items.KERWAN_INFOBOT.name, {POOL_INFOBOT})
NOVALIS_VENDOR_PYROCITOR = LocationData(3, "Novalis", "Novalis: Vendor - 2,500", Items.PYROCITOR.name, {POOL_WEAPON})
NOVALIS_SEWER_GOLD_BOLT = LocationData(
    4, "Novalis", "Novalis: Gold Bolt: Waterworks", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT})
NOVALIS_CAVES_GOLD_BOLT = LocationData(
    5, "Novalis", "Novalis: Gold Bolt: Caves", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, has_explosive_weapon)
NOVALIS_UNDERWATER_CAVES_GOLD_BOLT = LocationData(6, "Novalis", "Novalis: Gold Bolt: Amoeboid Caves",
                                                  Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, novalis_underwater_caves_rule)
# Golden Weapon Locations
NOVALIS_GOLD_WEAPON_1 = LocationData(100, "Novalis", "Novalis: Golden Weapon 1 - 60,000",
                                     Items.GOLDEN_TESLA_CLAW.name, {POOL_GOLDEN_WEAPON}, novalis_gold_weapon_rule)
NOVALIS_GOLD_WEAPON_2 = LocationData(95, "Novalis", "Novalis: Golden Weapon 2 - 20,000",
                                     Items.GOLDEN_BOMB_GLOVE.name, {POOL_GOLDEN_WEAPON}, novalis_gold_weapon_rule)
NOVALIS_GOLD_WEAPON_3 = LocationData(101, "Novalis", "Novalis: Golden Weapon 3 - 60,000",
                                     Items.GOLDEN_DEVASTATOR.name, {POOL_GOLDEN_WEAPON}, novalis_gold_weapon_rule)
NOVALIS_GOLD_WEAPON_4 = LocationData(96, "Novalis", "Novalis: Golden Weapon 4 - 30,000",
                                     Items.GOLDEN_PYROCITOR.name, {POOL_GOLDEN_WEAPON}, novalis_gold_weapon_rule)
NOVALIS_GOLD_WEAPON_5 = LocationData(102, "Novalis", "Novalis: Golden Weapon 5 - 10,000",
                                     Items.GOLDEN_MINE_GLOVE.name, {POOL_GOLDEN_WEAPON}, novalis_gold_weapon_rule)
NOVALIS_GOLD_WEAPON_6 = LocationData(97, "Novalis", "Novalis: Golden Weapon 6 - 20,000",
                                     Items.GOLDEN_BLASTER.name, {POOL_GOLDEN_WEAPON}, novalis_gold_weapon_rule)
NOVALIS_GOLD_WEAPON_7 = LocationData(103, "Novalis", "Novalis: Golden Weapon 7 - 20,000",
                                     Items.GOLDEN_MORPH_O_RAY.name, {POOL_GOLDEN_WEAPON}, novalis_gold_weapon_rule)
NOVALIS_GOLD_WEAPON_8 = LocationData(98, "Novalis", "Novalis: Golden Weapon 8 - 10,000",
                                     Items.GOLDEN_GLOVE_OF_DOOM.name, {POOL_GOLDEN_WEAPON}, novalis_gold_weapon_rule)
NOVALIS_GOLD_WEAPON_9 = LocationData(104, "Novalis", "Novalis: Golden Weapon 9 - 10,000",
                                     Items.GOLDEN_DECOY_GLOVE.name, {POOL_GOLDEN_WEAPON}, novalis_gold_weapon_rule)
NOVALIS_GOLD_WEAPON_10 = LocationData(99, "Novalis", "Novalis: Golden Weapon 10 - 10,000",
                                      Items.GOLDEN_SUCK_CANNON.name, {POOL_GOLDEN_WEAPON}, novalis_gold_weapon_rule)
# TODO: Skillpoint Locations
# Skill Point Locations
NOVALIS_SKILLPOINT = LocationData(
    105, "Novalis", "Novalis: Skillpoint: Take Aim", Items.TAKE_AIM.name, {POOL_SKILLPOINT}, novalis_skillpoint_rule)

# Aridia
ARIDIA_HOVERBOARD = LocationData(7, "Aridia", "Aridia: Kill the Sand Sharks", Items.HOVERBOARD.name, {POOL_EXTRA_ITEM})
ARIDIA_TRESPASSER = LocationData(
    8, "Aridia", "Aridia: Construction Zone", Items.TRESPASSER.name, {POOL_GADGET}, can_swingshot)
ARIDIA_SONIC_SUMMONER = LocationData(9, "Aridia", "Aridia: Bring Zoomerator to Agent",
                                     Items.SONIC_SUMMONER.name, {POOL_HELMET}, has_zoomerator)
ARIDIA_TRESPASSER_GOLD_BOLT = LocationData(
    10, "Aridia", "Aridia: Gold Bolt: Construction Zone", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, can_swingshot)
ARIDIA_ISLAND_GOLD_BOLT = LocationData(
    11, "Aridia", "Aridia: Gold bolt: Island", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT})
ARIDIA_MAGNEBOOTS_GOLD_BOLT = LocationData(
    12, "Aridia", "Aridia: Gold Bolt: Laser", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, has_magneboots)
ARIDIA_SANDSHARK_GOLD_BOLT = LocationData(13, "Aridia", "Aridia: Gold bolt: Sandshark Cave",
                                          Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, has_explosive_weapon)

# Kerwan
KERWAN_SWINGSHOT = LocationData(
    14, "Kerwan", "Kerwan: Fitness Course", Items.SWINGSHOT.name, {POOL_GADGET})
KERWAN_HELIPACK = LocationData(15, "Kerwan", "Kerwan: Al's Roboshack", Items.HELI_PACK.name, {POOL_PACK})
KERWAN_TRAIN_INFOBOT = LocationData(16, "Kerwan", "Kerwan: Ride the Robot Train",
                                    Items.EUDORA_INFOBOT.name, {POOL_INFOBOT}, can_improved_jump)
KERWAN_VENDOR_BLASTER = LocationData(
    17, "Kerwan", "Kerwan: Vendor - 2,500", Items.BLASTER.name, {POOL_WEAPON})
KERWAN_BELOW_SHIP_GOLD_BOLT = LocationData(
    18, "Kerwan", "Kerwan: Gold Bolt: Underpass", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT})
KERWAN_TRAIN_STATION_GOLD_BOLT = LocationData(19, "Kerwan", "Kerwan: Gold Bolt: Train Station",
                                              Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, can_improved_jump)
KERWAN_LONE_TOWER_GOLD_BOLT = LocationData(
    20, "Kerwan", "Kerwan: Gold Bolt: Fitness Course Tower", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, can_glide)

# Eudora
EUDORA_HENCHMAN = LocationData(
    21, "Eudora", "Eudora: Robot Lieutenant", Items.BLARG_INFOBOT.name, {POOL_INFOBOT}, eudora_henchman_rule)
EUDORA_SUCK_CANNON = LocationData(
    22, "Eudora", "Eudora: Explore the Mills", Items.SUCK_CANNON.name, {POOL_WEAPON}, eudora_suck_cannon_rule)
EUDORA_VENDOR_GLOVE_OF_DOOM = LocationData(
    23, "Eudora", "Eudora: Vendor - 7,500", Items.GLOVE_OF_DOOM.name, {POOL_WEAPON}, has_metal_detector)
EUDORA_GOLD_BOLT = LocationData(
    24, "Eudora", "Eudora: Gold Bolt", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, can_heli_high_jump)

# Rilgar
RILGAR_QUARK_INFOBOT = LocationData(
    25, "Rilgar", "Rilgar: Locate Captain Quark", Items.UMBRIS_INFOBOT.name, {POOL_INFOBOT}, rilgar_bouncer_rule)
RILGAR_PLATINUM_ZOOMERATOR = LocationData(
    26, "Rilgar", "Rilgar: Win the hoverboard race", Items.ZOOMERATOR.name, {POOL_EXTRA_ITEM}, rilgar_hoverboard_rule)
RILGAR_MINE_GLOVE = LocationData(
    27, "Rilgar", "Rilgar: Vendor - 7,500", Items.MINE_GLOVE.name, {POOL_WEAPON}, has_metal_detector)
RILGAR_RYNO = LocationData(
    28, "Rilgar", "Rilgar: Shady Salesman - 150,000", Items.RYNO.name, {POOL_WEAPON}, rilgar_ryno_rule)
RILGAR_MAZE_GOLD_BOLT = LocationData(
    29, "Rilgar", "Rilgar: Gold Bolt: Maze", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, can_improved_jump)
RILGAR_WATERWORKS_GOLD_BOLT = LocationData(
    30, "Rilgar", "Rilgar: Gold Bolt: Sewer Cave", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, rilgar_underwater_bolt_rule)

# Blarg
BLARG_HYDRODISPLACER = LocationData(
    31, "Blarg", "Blarg: Outside as Clank", Items.HYDRODISPLACER.name, {POOL_GADGET}, has_trespasser)
BLARG_EXPLOSION_INFOBOT = LocationData(
    32, "Blarg", "Blarg: Destroy the Warship", Items.RILGAR_INFOBOT.name, {POOL_INFOBOT})
BLARG_GRINDBOOTS = LocationData(
    33, "Blarg", "Blarg: Explore the Space Station", Items.GRINDBOOTS.name, {POOL_BOOT}, can_swingshot)
BLARG_VENDOR_TAUNTER = LocationData(34, "Blarg", "Blarg: Vendor - 2,500", Items.TAUNTER.name, {POOL_WEAPON})
BLARG_OUTSIDE_GOLD_BOLT = LocationData(
    35, "Blarg", "Blarg: Gold Bolt: Outside", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, blarg_outside_gold_bolt_rule)
BLARG_SWARMER_GOLD_BOLT = LocationData(
    36, "Blarg", "Blarg: Gold Bolt: Cages", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, can_swingshot)

# Umbris
UMBRIS_SNAGGLEBEAST_INFOBOT = LocationData(
    37, "Umbris", "Umbris: Defeat the Snagglebeast", Items.BATALIA_INFOBOT.name, {POOL_INFOBOT},
    umbris_snagglebeast_rule)
UMBRIS_PRESSURE_PUZZLE_GOLD_BOLT = LocationData(38, "Umbris", "Umbris: Gold Bolt: Lighthouse puzzle",
                                                Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, umbris_pressure_bolt_rule)
UMBRIS_JUMP_DOWN_GOLD_BOLT = LocationData(
    39, "Umbris", "Umbris: Gold bolt: Jumping Down", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, umbris_jump_bolt_rule)

# Batalia
BATALIA_VENDOR_DEVASTATOR = LocationData(
    40, "Batalia", "Batalia: Vendor - 10,000", Items.DEVASTATOR.name, {POOL_WEAPON}, has_metal_detector)
BATALIA_GRINDRAIL_INFOBOT = LocationData(
    41, "Batalia", "Batalia: Ride the grindrail", Items.GASPAR_INFOBOT.name, {POOL_INFOBOT}, can_grind)
BATALIA_COMMANDER_INFOBOT = LocationData(42, "Batalia", "Batalia: Commando", Items.ORXON_INFOBOT.name, {POOL_INFOBOT})
BATALIA_METAL_DETECTOR = LocationData(
    43, "Batalia", "Batalia: Shoot down the Bombers", Items.METAL_DETECTOR.name, {POOL_GADGET}, has_magneboots)
BATALIA_CLIFFSIDE_GOLD_BOLT = LocationData(
    44, "Batalia", "Batalia: Gold Bolt: Cliffside", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, can_improved_jump)
BATALIA_TRESPASSER_GOLD_BOLT = LocationData(
    45, "Batalia", "Batalia: Gold Bolt: House Roof", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT})

# Gaspar
GASPAR_VENDOR_WALLOPER = LocationData(
    46, "Gaspar", "Gaspar: Vendor - 7,500", Items.WALLOPER.name, {POOL_WEAPON}, has_metal_detector)
GASPAR_PILOT_HELMET = LocationData(
    47, "Gaspar", "Gaspar: Get the pilot helmet", Items.PILOTS_HELMET.name, {POOL_HELMET})
GASPAR_SWINGSHOT_GOLD_BOLT = (LocationData(
    48, "Gaspar", "Gaspar: Gold Bolt: Destroy the Bombers", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, can_swingshot))
GASPAR_VOLCANO_GOLD_BOLT = LocationData(
    49, "Gaspar", "Gaspar: Gold Bolt: Volcano", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, can_improved_jump)

# Orxon
ORXON_VENDOR_VISIBOMB = LocationData(
    50, "Orxon", "Orxon: Vendor - 15,000", Items.VISIBOMB.name, {POOL_WEAPON}, orxon_visibomb_rule)
ORXON_CLANK_INFOBOT = LocationData(
    51, "Orxon", "Orxon: Clank: Traverse the Wilderness", Items.POKITARU_INFOBOT.name, {POOL_INFOBOT})
ORXON_RATCHET_INFOBOT = LocationData(
    52, "Orxon", "Orxon: Chase the Infobot", Items.HOVEN_INFOBOT.name, {POOL_INFOBOT}, orxon_ratchet_infobot_rule)
ORXON_CLANK_MAGNEBOOTS = LocationData(53, "Orxon", "Orxon: Clank: Search the Labs", Items.MAGNEBOOTS.name, {POOL_BOOT})
ORXON_PREMIUM_NANOTECH = LocationData(
    54, "Orxon", "Orxon: Buy the premium nanotech", Items.PREMIUM_NANOTECH.name, {POOL_EXTRA_ITEM}, orxon_nanotech_rule)
ORXON_ULTRA_NANOTECH = LocationData(55, "Orxon", "Orxon: Buy the ultra nanotech",
                                    Items.ULTRA_NANOTECH.name, {POOL_EXTRA_ITEM}, orxon_ultra_nanotech_rule)
ORXON_CLANK_GOLD_BOLT = LocationData(
    56, "Orxon", "Orxon: Gold Bolt: Return to the Clank section", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, has_o2_mask)
ORXON_VISIBOMB_GOLD_BOLT = LocationData(
    57, "Orxon", "Orxon: Gold Bolt: Long Tunnel", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, orxon_visibomb_bolt_rule)

# Pokitaru
POKITARU_VENDOR_DECOY_GLOVE = LocationData(
    58, "Pokitaru", "Pokitaru: Vendor - 7,500", Items.DECOY_GLOVE.name, {POOL_WEAPON}, has_metal_detector)
POKITARU_O2_MASK = LocationData(
    59, "Pokitaru", "Pokitaru: Pilot the Ship", Items.O2_MASK.name, {POOL_HELMET}, pokitaru_ship_rule)
POKITARU_SEWER_PERSUADER = LocationData(
    60, "Pokitaru", "Pokitaru: Trade Raritanium", Items.PERSUADER.name, {POOL_EXTRA_ITEM}, pokitaru_persuader_rule)
POKITARU_THRUSTER_PACK = LocationData(61, "Pokitaru", "Pokitaru: Bob's Shop", Items.THRUSTER_PACK.name, {POOL_PACK})
POKITARU_GOLD_BOLT = LocationData(
    62, "Pokitaru", "Pokitaru: Gold Bolt: Waterfalls", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, pokitaru_gold_bolt_rule)

# Hoven
HOVEN_VENDOR_DRONE_DEVICE = LocationData(
    63, "Hoven", "Hoven: Vendor - 7,500", Items.DRONE_DEVICE.name, {POOL_WEAPON}, has_metal_detector)
HOVEN_TURRET_INFOBOT = LocationData(
    64, "Hoven", "Hoven: Destroy the Planetbuster", Items.GEMLIK_INFOBOT.name, {POOL_INFOBOT}, hoven_infobot_rule)
HOVEN_HYDRO_PACK = LocationData(
    65, "Hoven", "Hoven: Edwina's Shop", Items.HYDRO_PACK.name, {POOL_PACK}, has_hydrodisplacer)
HOVEN_RARITANIUM = LocationData(
    66, "Hoven", "Hoven: Talk to the Miner", Items.RARITANIUM.name, {POOL_EXTRA_ITEM}, hoven_raritanium_rule)
HOVEN_WATER_GOLD_BOLT = LocationData(
    67, "Hoven", "Hoven: Gold Bolt: in the Water Cave", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, has_hydrodisplacer)
HOVEN_WALLJUMP_GOLD_BOLT = LocationData(
    68, "Hoven", "Hoven: Gold Bolt: Moving wall jump", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT})

# Gemlik
GEMLIK_QUARK_FIGHT = LocationData(
    69, "Gemlik", "Gemlik: Defeat Captain Quark", Items.OLTANIS_INFOBOT.name, {POOL_INFOBOT}, gemlik_quark_rule)
GEMLIK_GOLD_BOLT = LocationData(
    70, "Gemlik", "Gemlik: Gold Bolt: Visibomb Hidden Tower", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, gemlik_bolt_rule)

# Oltanis
OLTANIS_VENDOR_TESLA_CLAW = LocationData(
    71, "Oltanis", "Oltanis: Vendor - 40,000", Items.TESLA_CLAW.name, {POOL_WEAPON}, has_metal_detector)
OLTANIS_INFOBOT = LocationData(
    72, "Oltanis", "Oltanis: Grindrail path: Scrap Merchant", Items.QUARTU_INFOBOT.name, {POOL_INFOBOT}, can_grind)
OLTANIS_PDA = LocationData(
    73, "Oltanis", "Oltanis: Magneboot path: Buy the PDA from Steve", Items.PDA.name, {POOL_GADGET}, has_magneboots)
OLTANIS_MORPH_O_RAY = LocationData(
    74, "Oltanis", "Oltanis: Swingshot path: Search the city", Items.MORPH_O_RAY.name, {POOL_WEAPON}, can_swingshot)
OLTANIS_MAIN_GOLD_BOLT = LocationData(75, "Oltanis", "Oltanis: Gold Bolt: Grindrail path: Swingshot Upper Ledge",
                                      Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, oltanis_main_bolt_rule)
OLTANIS_MAGNET_GOLD_BOLT_1 = LocationData(76, "Oltanis", "Oltanis: Gold Bolt: Magneboot path: Ledge near Bomber",
                                          Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, has_magneboots)
OLTANIS_MAGNET_GOLD_BOLT_2 = LocationData(77, "Oltanis", "Oltanis: Gold Bolt: Magneboot path: Ledge hang",
                                          Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, has_magneboots)
OLTANIS_FINAL_GOLD_BOLT = LocationData(78, "Oltanis", "Oltanis: Gold Bolt: All Objectives",
                                       Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, oltanis_final_bolt_rule)

# Quartu
QUARTU_GIANT_CLANK_INFOBOT = LocationData(
    79, "Quartu", "Quartu: Giant Clank Fight", Items.KALEBO_INFOBOT.name, {POOL_INFOBOT}, can_swingshot)
QUARTU_BOLT_GRABBER = LocationData(
    80, "Quartu", "Quartu: Water Path", Items.BOLT_GRABBER.name, {POOL_EXTRA_ITEM}, quartu_bolt_grabber_rule)
QUARTU_INFILTRATE_INFOBOT = LocationData(
    81, "Quartu", "Quartu: Clank's mother", Items.FLEET_INFOBOT.name, {POOL_INFOBOT}, quartu_infiltrate_rule)
QUARTU_MOM_GOLD_BOLT = LocationData(82, "Quartu", "Quartu: Gold Bolt: Behind Clank's mother",
                                    Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, quartu_infiltrate_rule)
QUARTU_CODEBOT_GOLD_BOLT = LocationData(
    83, "Quartu", "Quartu: Gold Bolt: Codebot door", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, quartu_codebot_rule)

# Kalebo III
KALEBO_HOLOGUISE = LocationData(
    84, "Kalebo III", "Kalebo III: Win the hoverboard race", Items.HOLOGUISE.name, {POOL_GADGET}, kalebo_hologuise_rule)
KALEBO_MAP_O_MATIC = LocationData(
    85, "Kalebo III", "Kalebo III: Grindrail: Helpdesk", Items.MAP_O_MATIC.name, {POOL_EXTRA_ITEM}, can_grind)
KALEBO_GRIND_GOLD_BOLT = LocationData(
    86, "Kalebo III", "Kalebo III: Gold Bolt: On the Grindrail", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, can_grind)
KALEBO_BREAK_ROOM_GOLD_BOLT = LocationData(
    87, "Kalebo III", "Kalebo III: Gold Bolt: Employee break room", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, can_grind)

# Drek's Fleet
FLEET_INFOBOT = LocationData(
    88, "Drek's Fleet", "Drek's Fleet: Flagship", Items.VELDIN_INFOBOT.name, {POOL_INFOBOT}, fleet_infobot_rule)
FLEET_CODEBOT = LocationData(
    89, "Drek's Fleet", "Drek's Fleet: Water section", Items.CODEBOT.name, {POOL_EXTRA_ITEM}, fleet_water_rule)
FLEET_WATER_GOLD_BOLT = LocationData(90, "Drek's Fleet", "Drek's Fleet: Gold Bolt: Water section",
                                     Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, fleet_water_rule)
FLEET_ROBOT_GOLD_BOLT = (LocationData(91, "Drek's Fleet", "Drek's Fleet: Gold Bolt: Sidepath with robot guards",
                                      Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, fleet_second_bolt_rule))

# Veldin
VELDIN_TAUNTER_GOLD_BOLT = LocationData(92, "Veldin", "Veldin: Gold Bolt: Taunter the horny toad",
                                        Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, veldin_taunter_bolt_rule)
VELDIN_HALFWAY_GOLD_BOLT = LocationData(
    93, "Veldin", "Veldin: Gold Bolt: Platforms", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, veldin_halfway_bolt_rule)
VELDIN_GRIND_GOLD_BOLT = LocationData(
    94, "Veldin", "Veldin: Gold Bolt: Grindrail", Items.GOLD_BOLT.name, {POOL_GOLD_BOLT}, veldin_grind_bolt_rule)
VELDIN_DREK = LocationData(None, "Veldin", "Veldin: Defeat Chairman Drek", None, access_rule=veldin_defeat_drek_rule)
