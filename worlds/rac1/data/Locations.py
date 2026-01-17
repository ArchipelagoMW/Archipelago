from typing import Callable, NamedTuple, Optional

from ..Logic import *


class LocationData(NamedTuple):
    location_id: Optional[int]
    name: str
    access_rule: Optional[Callable[[CollectionState, int], bool]] = None


# Novalis
NOVALIS_PLUMBER = LocationData(1, "Novalis: Plumber - Infobot")
NOVALIS_MAYOR = LocationData(2, "Novalis: Mayor - Infobot")
NOVALIS_VENDOR_PYROCITOR = LocationData(3, "Novalis: Vendor - Pyrocitor")
NOVALIS_SEWER_GOLD_BOLT = LocationData(4, "Novalis: Sewer - Gold Bolt")
NOVALIS_CAVES_GOLD_BOLT = LocationData(5, "Novalis: Caves - Gold Bolt", has_explosive_weapon)
NOVALIS_UNDERWATER_CAVES_GOLD_BOLT = LocationData(6, "Novalis: Underwater Caves - Gold Bolt",
                                                  novalis_underwater_caves_rule)

# Aridia
ARIDIA_HOVERBOARD = LocationData(7, "Aridia: Save Skid Mc Marks")
ARIDIA_TRESPASSER = LocationData(8, "Aridia: Find the trespasser", can_swingshot)
ARIDIA_SONIC_SUMMONER = LocationData(9, "Aridia: Trade the platinum zoomerator for the sonic summoner", has_zoomerator)
ARIDIA_TRESPASSER_GOLD_BOLT = LocationData(10, "Aridia: Gold Bolt below trespasser", can_swingshot)
ARIDIA_ISLAND_GOLD_BOLT = LocationData(11, "Aridia: Gold bolt on island", can_improved_jump)
ARIDIA_MAGNEBOOTS_GOLD_BOLT = LocationData(12, "Aridia: Gold bolt near mortar turret", has_magneboots)
ARIDIA_SANDSHARK_GOLD_BOLT = LocationData(13, "Aridia: Gold bolt hidden in sandshark area", has_explosive_weapon)

# Kerwan
KERWAN_SWINGSHOT = LocationData(14, "Kerwan: Buy the swingshot from Helga")
KERWAN_HELIPACK = LocationData(15, "Kerwan: Buy the helipack from Al")
KERWAN_TRAIN_INFOBOT = LocationData(16, "Kerwan: Get the infobot after the train section", can_improved_jump)
KERWAN_VENDOR_BLASTER = LocationData(17, "Kerwan: Buy the blaster from the vendor")
KERWAN_BELOW_SHIP_GOLD_BOLT = LocationData(18, "Kerwan: Get the gold bolt below your ship", can_glide)
KERWAN_TRAIN_STATION_GOLD_BOLT = LocationData(19, "Kerwan: Get the gold bolt just before the flying train section",
                                              can_improved_jump)
KERWAN_LONE_TOWER_GOLD_BOLT = LocationData(20, "Kerwan: Get the gold bolt on the lone tower", can_glide)

# Eudora
EUDORA_HENCHMAN = LocationData(21, "Eudora: Get the infobot after the swingshot section", eudora_henchman_rule)
EUDORA_SUCK_CANNON = LocationData(22, "Eudora: get the suck cannon", eudora_suck_cannon_rule)
EUDORA_VENDOR_GLOVE_OF_DOOM = LocationData(23, "Eudora: Buy the glove of doom from the vendor", has_metal_detector)
EUDORA_GOLD_BOLT = LocationData(24, "Eudora: Get the gold bolt near your ship", can_heli_high_jump)

# Rilgar
RILGAR_QUARK_INFOBOT = LocationData(25, "Rilgar: Pay the bouncer to meet Captain Quark", rilgar_bouncer_rule)
RILGAR_PLATINUM_ZOOMERATOR = LocationData(26, "Rilgar: Win the hoverboard race", rilgar_hoverboard_rule)
RILGAR_MINE_GLOVE = LocationData(27, "Rilgar: buy the mine glove from the vendor", has_metal_detector)
RILGAR_RYNO = LocationData(28, "Rilgar: Buy the RYNO", rilgar_ryno_rule)
RILGAR_MAZE_GOLD_BOLT = LocationData(29, "Rilgar: Get the gold bolt in the maze", can_improved_jump)
RILGAR_WATERWORKS_GOLD_BOLT = LocationData(30, "Rilgar: Get the gold bolt in the flooded area",
                                           rilgar_underwater_bolt_rule)

# Blarg
BLARG_HYDRODISPLACER = LocationData(31, "Blarg: Get the hydrodisplacer as Clank", has_trespasser)
BLARG_EXPLOSION_INFOBOT = LocationData(32, "Blarg: Get the Infobot from the exploding ship")
BLARG_GRINDBOOTS = LocationData(33, "Blarg: Buy the grind boots from the scientist", can_swingshot)
BLARG_VENDOR_TAUNTER = LocationData(34, "Blarg: Buy the taunter from the vendor")
BLARG_OUTSIDE_GOLD_BOLT = LocationData(35, "Blarg: Get the gold bolt outside as Ratchet", blarg_outside_gold_bolt_rule)
BLARG_SWARMER_GOLD_BOLT = LocationData(36, "Blarg: Get the gold bolt from the swarmer nest", can_swingshot)

# Umbris
UMBRIS_SNAGGLEBEAST_INFOBOT = LocationData(37, "Umbris: Defeat the Snagglebeast and claim the infobot",
                                           umbris_snagglebeast_rule)
UMBRIS_PRESSURE_PUZZLE_GOLD_BOLT = LocationData(38, "Umbris: Get the gold bolt from solving the pressure plate puzzle",
                                                umbris_pressure_bolt_rule)
UMBRIS_JUMP_DOWN_GOLD_BOLT = LocationData(39, "Umbris: Get the gold bolt from jumping down onto it",
                                          umbris_jump_bolt_rule)

# Batalia
BATALIA_VENDOR_DEVASTATOR = LocationData(40, "Batalia: Buy the devastator from the vendor", has_metal_detector)
BATALIA_GRINDRAIL_INFOBOT = LocationData(41, "Batalia: Buy the infobot at the end of the grindrail", can_grind)
BATALIA_COMMANDER_INFOBOT = LocationData(42, "Batalia: Get the infobot from the commander")
BATALIA_METAL_DETECTOR = LocationData(43, "Batalia: Get the metal detector from the plumber", has_magneboots)
BATALIA_CLIFFSIDE_GOLD_BOLT = LocationData(44, "Batalia: Get the gold bolt at the cliffside", can_improved_jump)
BATALIA_TRESPASSER_GOLD_BOLT = LocationData(45, "Batalia: Get the gold bolt above the trespasser lock")

# Gaspar
GASPAR_VENDOR_WALLOPER = LocationData(46, "Gaspar: Buy the walloper from the vendor", has_metal_detector)
GASPAR_PILOT_HELMET = LocationData(47, "Gaspar: Get the pilot helmet")
GASPAR_SWINGSHOT_GOLD_BOLT = LocationData(48, "Gaspar: Get the gold bolt from the swingshot sidepath", can_swingshot)
GASPAR_VOLCANO_GOLD_BOLT = LocationData(49, "Gaspar: Get the gold bolt after a path through the volcano",
                                        can_improved_jump)

# Orxon
ORXON_VENDOR_VISIBOMB = LocationData(50, "Orxon: Buy the visibomb gun from the vendor", orxon_visibomb_rule)
ORXON_CLANK_INFOBOT = LocationData(51, "Orxon: Get the infobot in the clank section")
ORXON_RATCHET_INFOBOT = LocationData(52, "Orxon: Get the infobot as ratchet", orxon_ratchet_infobot_rule)
ORXON_CLANK_MAGNEBOOTS = LocationData(53, "Orxon: Get the magneboots in the clank section")
ORXON_PREMIUM_NANOTECH = LocationData(54, "Orxon: Buy the premium nanotech", orxon_nanotech_rule)
ORXON_ULTRA_NANOTECH = LocationData(55, "Orxon: Buy the ultra nanotech", orxon_ultra_nanotech_rule)
ORXON_CLANK_GOLD_BOLT = LocationData(56, "Orxon: Get the gold bolt in the clank section as ratchet", has_o2_mask)
ORXON_VISIBOMB_GOLD_BOLT = LocationData(57, "Orxon: Get the gold bolt requiring the visibomb", orxon_visibomb_bolt_rule)

# Pokitaru
POKITARU_VENDOR_DECOY_GLOVE = LocationData(58, "Pokitaru: Buy the decoy glove from the vendor", has_metal_detector)
POKITARU_O2_MASK = LocationData(59, "Pokitaru: Destroy all ships using the pilot's helmet", pokitaru_ship_rule)
POKITARU_SEWER_PERSUADER = LocationData(60, "Pokitaru: Trade raritanium for the persuader", pokitaru_persuader_rule)
POKITARU_THRUSTER_PACK = LocationData(61, "Pokitaru: Buy the thruster pack")
POKITARU_GOLD_BOLT = LocationData(62, "Pokitaru: Get the gold bolt on the waterfalls", pokitaru_gold_bolt_rule)

# Hoven
HOVEN_VENDOR_DRONE_DEVICE = LocationData(63, "Hoven: Buy the drone device from the vendor", has_metal_detector)
HOVEN_TURRET_INFOBOT = LocationData(64, "Hoven: Destroy the ship and get the infobot", hoven_infobot_rule)
HOVEN_HYDRO_PACK = LocationData(65, "Hoven: Buy the hydropack", has_hydrodisplacer)
HOVEN_RARITANIUM = LocationData(66, "Hoven: Get the raritanium", hoven_raritanium_rule)
HOVEN_WATER_GOLD_BOLT = LocationData(67, "Hoven: Get the gold bolt in the hydrodisplacer section", has_hydrodisplacer)
HOVEN_WALLJUMP_GOLD_BOLT = LocationData(68, "Hoven: Get the gold bolt at the top of the moving wall jump")

# Gemlik
GEMLIK_QUARK_FIGHT = LocationData(69, "Gemlik: Defeat Captain Quark", gemlik_quark_rule)
GEMLIK_GOLD_BOLT = LocationData(70, "Gemlik: Get the gold bolt after shooting its tower with the visibomb",
                                gemlik_bolt_rule)

# Oltanis
OLTANIS_VENDOR_TESLA_CLAW = LocationData(71, "Oltanis: Buy the tesla claw from the vendor", has_metal_detector)
OLTANIS_INFOBOT = LocationData(72, "Oltanis: Buy the infobot after traversing the grindrail", can_grind)
OLTANIS_PDA = LocationData(73, "Oltanis: Buy the PDA from Steve", has_magneboots)
OLTANIS_MORPH_O_RAY = LocationData(74, "Oltanis: Get the Morph-o-Ray", can_swingshot)
OLTANIS_MAIN_GOLD_BOLT = LocationData(75, "Oltanis: Get the gold bolt from swingshotting along the main path",
                                      oltanis_main_bolt_rule)
OLTANIS_MAGNET_GOLD_BOLT_1 = LocationData(76,
                                          "Oltanis: Get the gold bolt by dropping down the ice on the magneboot path",
                                          has_magneboots)
OLTANIS_MAGNET_GOLD_BOLT_2 = LocationData(77, "Oltanis: Get the gold bolt by ledge hanging on the magneboot path",
                                          has_magneboots)
OLTANIS_FINAL_GOLD_BOLT = LocationData(78, "Oltanis: Get the gold bolt after completing all objectives",
                                       oltanis_final_bolt_rule)

# Quartu
QUARTU_GIANT_CLANK_INFOBOT = LocationData(79, "Quartu: Get the infobot after the giant clank fight", can_swingshot)
QUARTU_BOLT_GRABBER = LocationData(80, "Quartu: Get the bolt grabber after the underwater section",
                                   quartu_bolt_grabber_rule)
QUARTU_INFILTRATE_INFOBOT = LocationData(81, "Quartu: Get the infobot from clank's mother", quartu_infiltrate_rule)
QUARTU_MOM_GOLD_BOLT = LocationData(82, "Quartu: Get the gold bolt behind clank's mother", quartu_infiltrate_rule)
QUARTU_CODEBOT_GOLD_BOLT = LocationData(83, "Quartu: Get the gold bolt behind the codebot door", quartu_codebot_rule)

# Kalebo III
KALEBO_HOLOGUISE = LocationData(84, "Kalebo III: Win the hoverboard race", kalebo_hologuise_rule)
KALEBO_MAP_O_MATIC = LocationData(85, "Kalebo III: Buy the map-o-matic after the grindrail", can_grind)
KALEBO_GRIND_GOLD_BOLT = LocationData(86, "Kalebo III: Get the gold bolt on the grindrail", can_grind)
KALEBO_BREAK_ROOM_GOLD_BOLT = LocationData(87, "Kalebo III: Get the gold bolt in the employee break room", can_grind)

# Drek's Fleet
FLEET_INFOBOT = LocationData(88, "Drek's Fleet: Get the infobot from the main ship", fleet_infobot_rule)
FLEET_CODEBOT = LocationData(89, "Drek's Fleet: Get the codebot after the water section", fleet_water_rule)
FLEET_WATER_GOLD_BOLT = LocationData(90, "Drek's Fleet: Get the gold bolt hidden in the water section",
                                     fleet_water_rule)
FLEET_ROBOT_GOLD_BOLT = LocationData(91, "Drek's Fleet: Get the gold bolt along the sidepath with robot guards",
                                     fleet_second_bolt_rule)

# Veldin
VELDIN_TAUNTER_GOLD_BOLT = LocationData(92, "Veldin: Get the gold bolt using the taunter to lure the horny toad",
                                        veldin_taunter_bolt_rule)
VELDIN_HALFWAY_GOLD_BOLT = LocationData(93, "Veldin: Get the gold bolt on the platforms", veldin_halfway_bolt_rule)
VELDIN_GRIND_GOLD_BOLT = LocationData(94, "Veldin: Get the gold bolt after a short grindrail", veldin_grind_bolt_rule)
VELDIN_DREK = LocationData(None, "Veldin: Defeat Chairman Drek", veldin_defeat_drek_rule)
