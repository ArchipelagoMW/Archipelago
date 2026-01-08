from typing import Optional, NamedTuple, Dict, Callable, TYPE_CHECKING, Any, Sequence
from ..Logic import *

if TYPE_CHECKING:
    from .RamAddresses import Addresses


class LocationData(NamedTuple):
    location_id: Optional[int]
    name: str
    access_rule: Optional[Callable[[CollectionState, int], bool]] = None
    checked_flag_address: Optional[Callable[["Addresses"], int]] = None
    enable_if: Optional[Callable[[Dict[str, Any]], bool]] = None
    is_vendor: bool = False


""" Oozla """
OOZLA_OUTSIDE_MEGACORP_STORE = LocationData(10, "Oozla: Outside Megacorp Store - Dynamo")
OOZLA_END_STORE_CUTSCENE = LocationData(11, "Oozla: End of Store Cutscene", oozla_end_store_cutscene_rule)
OOZLA_MEGACORP_SCIENTIST = LocationData(12, "Oozla: Megacorp Scientist - Tractor Beam")
OOZLA_TRACTOR_PUZZLE_PB = LocationData(13, "Oozla: Tractor Puzzle - Platinum Bolt", oozla_tractor_puzzle_pb_rule)
OOZLA_SWAMP_RUINS_PB = LocationData(14, "Oozla: Swamp Ruins - Platinum Bolt", oozla_swamp_ruins_pb_rule)
OOZLA_SWAMP_MONSTER_II = LocationData(15, "Oozla: Swamp Monster II - Box Breaker",oozla_swamp_monster_ii_rule)

""" Maktar """
MAKTAR_ARENA_CHALLENGE = LocationData(20, "Maktar: Arena Challenge - Electrolyzer")
MAKTAR_PHOTO_BOOTH = LocationData(21, "Maktar: Photo Booth", maktar_photo_booth_rule)
MAKTAR_DEACTIVATE_JAMMING_ARRAY = LocationData(22, "Maktar: Deactivate Jamming Array", maktar_deactivate_jamming_array_rule)
MAKTAR_JAMMING_ARRAY_PB = LocationData(23, "Maktar: Jamming Array - Platinum Bolt", maktar_jamming_array_pb_rule)
MAKTAR_CRANE_PB = LocationData(24, "Maktar: Crane - Platinum Bolt")

""" Endako """
ENDAKO_CLANK_APARTMENT_SS = LocationData(30, "Endako: Clank's Apartment - Swingshot")
ENDAKO_CLANK_APARTMENT_GB = LocationData(31, "Endako: Clank's Apartment - Grindboots")
ENDAKO_RESCUE_CLANK_HELI = LocationData(32, "Endako: Rescue Clank Heli-Pack", endako_rescue_clank_rule)
ENDAKO_RESCUE_CLANK_THRUSTER = LocationData(33, "Endako: Rescue Clank Thruster-Pack", endako_rescue_clank_rule)
ENDAKO_LEDGE_PB = LocationData(34, "Endako: Ledge - Platinum Bolt")
ENDAKO_CRANE_PB = LocationData(35, "Endako: Crane - Platinum Bolt", endako_crane_pb_rule)
ENDAKO_CRANE_NT = LocationData(36, "Endako: Crane - Nanotech Boost", endako_crane_nt_rule)

""" Barlow """
BARLOW_INVENTOR = LocationData(40, "Barlow: Inventor - Thermanator", barlow_inventor_rule)
BARLOW_HOVERBIKE_RACE_TRANSMISSION = LocationData(41, "Barlow: Hoverbike Race Transmission", barlow_overbike_race_rule)
BARLOW_HOVERBIKE_RACE_PB = LocationData(42, "Barlow: Hoverbike Race - Platinum Bolt", barlow_overbike_race_rule)
BARLOW_HOUND_CAVE_PB = LocationData(43, "Barlow: Hound Cave - Platinum Bolt", barlow_hound_cave_pb_rule)

""" Feltzin System """
FELTZIN_DEFEAT_THUG_SHIPS = LocationData(50, "Feltzin: Defeat Thug Ships")
FELTZIN_RACE_PB = LocationData(51, "Feltzin: Race Through the Asteroids - Platinum Bolt")
FELTZIN_CARGO_BAY_NT = LocationData(52, "Feltzin: Cargo Bay - Nanotech Boost")
FELTZIN_DESTROY_SPACE_WASPS = LocationData(
    53, "Feltzin: Destroy Space Wasps",
    checked_flag_address=lambda ram: ram.feltzin_challenge_wins + 0x1,
    enable_if=lambda options_dict: options_dict["extra_spaceship_challenge_locations"]
)
FELTZIN_FIGHT_ACE_THUGS = LocationData(
    54, "Feltzin: Fight Ace Thug Ships",
    checked_flag_address=lambda ram: ram.feltzin_challenge_wins + 0x2,
    enable_if=lambda options_dict: options_dict["extra_spaceship_challenge_locations"]
)
FELTZIN_RACE = LocationData(
    55, "Feltzin: Race Through the Asteroids",
    checked_flag_address=lambda ram: ram.feltzin_challenge_wins + 0x3,
    enable_if=lambda options_dict: options_dict["extra_spaceship_challenge_locations"]
)

""" Notak """
NOTAK_TOP_PIER_TELESCREEN = LocationData(60, "Notak: Top of Pier Telescreen", notak_top_pier_telescreen_rule)
NOTAK_WORKER_BOTS = LocationData(61, "Notak: Worker Bots", notak_worker_bots_rule)
NOTAK_BEHIND_BUILDING_PB = LocationData(62, "Notak: Behind Building - Platinum Bolt")
NOTAK_PROMENADE_SIGN_PB = LocationData(63, "Notak: Promenade Sign - Platinum Bolt")
NOTAK_TIMED_DYNAMO_PB = LocationData(64, "Notak: Timed Dynamo - Platinum Bolt", notak_timed_dynamo_rule)
NOTAK_PROMENADE_END_NT = LocationData(65, "Notak: Promenade End - Nanotech Boost")

""" Siberius """
SIBERIUS_DEFEAT_THIEF = LocationData(70, "Siberius: Defeat Thief", siberius_defeat_thief_rule)
SIBERIUS_FLAMEBOT_LEDGE_PB = LocationData(71, "Siberius: Flamebot Ledge - Platinum Bolt", siberius_flamebot_ledge_pb_rule)
SIBERIUS_FENCED_AREA_PB = LocationData(72, "Siberius: Fenced Area - Platinum Bolt", siberius_fenced_area_pb_rule)

""" Tabora """
TABORA_MEET_ANGELA = LocationData(80, "Tabora: Meet Angela", tabora_meet_angelar_rule)
TABORA_UNDERGROUND_MINES_END = LocationData(81, "Tabora: Underground Mines - Glider", tabora_underground_mines_end_rule)
TABORA_UNDERGROUND_MINES_PB = LocationData(82, "Tabora: Underground Mines - Platinum Bolt", tabora_underground_mines_end_rule)
TABORA_CANYON_GLIDE_PB = LocationData(83, "Tabora: Canyon Glide - Platinum Bolt", tabora_canyon_glide_pb_rule)
TABORA_NORTHEAST_DESERT_PB = LocationData(84, "Tabora: Northeast Desert - Platinum Bolt", tabora_northeast_desert_pb_rule)
TABORA_CANYON_GLIDE_PILLAR_NT = LocationData(85, "Tabora: Canyon Glide Pillar - Nanotech Boost", tabora_canyon_glide_pillar_nt_rule)
TABORA_OMNIWRENCH_10000 = LocationData(
    86, "Tabora: OmniWrench 10000",
    checked_flag_address=lambda ram: ram.tabora_wrench_cutscene_flag
)

""" Dobbo """
DOBBO_DEFEAT_THUG_LEADER = LocationData(90, "Dobbo: Defeat Thug Leader", dobbo_defeat_thug_leader_rule)
DOBBO_FACILITY_TERMINAL = LocationData(91, "Dobbo: Facility Terminal", dobbo_facility_terminal_rule)
DOBBO_SPIDERBOT_ROOM_PB = LocationData(92, "Dobbo: Spiderbot Room - Platinum Bolt", dobbo_spiderbot_room_pb_rule)
DOBBO_FACILITY_GLIDE_PB = LocationData(93, "Dobbo: Facility Glide End - Platinum Bolt", dobbo_facility_glide_pb_rule)
DOBBO_FACILITY_GLIDE_NT = LocationData(94, "Dobbo: Facility Glide Beginning - Nanotech Boost", dobbo_facility_glide_nt_rule)

""" Hrugis """
HRUGIS_DESTROY_DEFENSES = LocationData(100, "Hrugis Cloud: Destroy Defenses")
HRUGIS_RACE_PB = LocationData(101, "Hrugis Cloud: Race Through the Disposal Facility - Platinum Bolt")
HRUGIS_SABOTEURS = LocationData(
    102, "Hrugis Cloud: Take Out the Saboteurs",
    checked_flag_address=lambda ram: ram.hrugis_challenge_wins + 0x1,
    enable_if=lambda options_dict: options_dict["extra_spaceship_challenge_locations"],
)
HRUGIS_BERSERK_DRONES = LocationData(
    103, "Hrugis Cloud: Destroy the Berserk Repair Drones",
    checked_flag_address=lambda ram: ram.hrugis_challenge_wins + 0x2,
    enable_if=lambda options_dict: options_dict["extra_spaceship_challenge_locations"]
)
HRUGIS_RACE = LocationData(
    104, "Hrugis Cloud: Race Through the Disposal Facility",
    checked_flag_address=lambda ram: ram.hrugis_challenge_wins + 0x3,
    enable_if=lambda options_dict: options_dict["extra_spaceship_challenge_locations"]
)

""" Joba """
JOBA_FIRST_HOVERBIKE_RACE = LocationData(110, "Joba: First Hoverbike Race - Charge Boots", joba_hoverbike_race_rule)
JOBA_SHADY_SALESMAN = LocationData(111, "Joba: Shady Salesman - Levitator", joba_shady_salesman_rule)
JOBA_ARENA_BATTLE = LocationData(112, "Joba: Arena Battle - Gravity Boots", joba_arena_battle_rule)
JOBA_ARENA_CAGE_MATCH = LocationData(113, "Joba: Arena Cage Match - Infiltrator", joba_arena_cage_match_rule)
JOBA_HIDDEN_CLIFF_PB = LocationData(114, "Joba: Hidden Cliff - Platinum Bolt", joba_hidden_cliff_pb_rule)
JOBA_LEVITATOR_TOWER_PB = LocationData(115, "Joba: Levitator Tower - Platinum Bolt", joba_levitator_tower_pb_rule)
JOBA_HOVERBIKE_RACE_SHORTCUT_NT = LocationData(116, "Joba: Hoverbike Race Shortcut - Nanotech Boost", joba_hoverbike_race_rule)
JOBA_TIMED_DYNAMO_NT = LocationData(117, "Joba: Timed Dynamo Course - Nanotech Boost", joba_timed_dynamo_nt_rule)

""" Todano """
TODANO_SEARCH_ROCKET_SILO = LocationData(120, "Todano: Search Rocket Silo", todano_search_rocket_silo_rule)
TODANO_STUART_ZURGO_TRADE = LocationData(121, "Todano: Stuart Zurgo Trade - Armor Magnetizer", todano_stuart_zurgo_trade_rule)
TODANO_FACILITY_INTERIOR = LocationData(122, "Todano: Facility Interior - Sheepinator", todano_facility_interior_rule)
TODANO_NEAR_STUART_ZURGO_PB = LocationData(123, "Todano: Near Stuart Zurgo - Platinum Bolt", todano_near_stuart_zurgo_pb_rule)
TODANO_END_TOUR_PB = LocationData(124, "Todano: End of Tour - Platinum Bolt")
TODANO_SPIDERBOT_CONVEYOR_PB = LocationData(125, "Todano: Spiderbot Conveyor - Platinum Bolt", todano_spiderbot_conveyor_pb_rule)
TODANO_ROCKET_SILO_NT = LocationData(126, "Todano: Rocket Silo - Nanotech Boost", todano_rocket_silo_nt_rule)

""" Boldan """
BOLDAN_FIND_FIZZWIDGET = LocationData(130, "Boldan: Find Fizzwidget", boldan_find_fizzwidget_rule)
BOLDAN_SPIDERBOT_ALLEY_PB = LocationData(131, "Boldan: Spiderbot Alley - Platinum Bolt", boldan_spiderbot_alley_pb_rule)
BOLDAN_FLOATING_PLATFORM_PB = LocationData(132, "Boldan: Floating Platform - Platinum Bolt",boldan_floating_platform_rule)
BOLDAN_UPPER_DOME_PB = LocationData(133, "Boldan: Upper Dome - Platinum Bolt", boldan_find_fizzwidget_rule)
BOLDAN_FOUNTAIN_NT = LocationData(134, "Boldan: Fountain - Nanotech Boost", boldan_fountain_nt_rule)

""" Aranos Prison """
ARANOS_CONTROL_ROOM = LocationData(140, "Aranos: Control Room", aranos_control_room_rule)
ARANOS_PLUMBER = LocationData(141, "Aranos: Plumber - Qwark Statuette", aranos_plumber_rule)
ARANOS_UNDER_SHIP_PB = LocationData(142, "Aranos: Under Ship - Platinum Bolt", aranos_under_ship_pb_rule)
ARANOS_OMNIWRENCH_12000 = LocationData(143, "Aranos: OmniWrench 12000", aranos_omniwrench_12000_rule,
    checked_flag_address=lambda ram: ram.aranos_wrench_cutscene_flag
)

""" Gorn """
GORN_DEFEAT_THUG_FLEET = LocationData(150, "Gorn: Defeat Thug Fleet")
GORN_RACE_PB = LocationData(151, "Gorn: Race Through the Docking Bays - Platinum Bolt")
GORN_FIGHT_BANDITS = LocationData(
    152, "Gorn: Fight the Bandits",
    checked_flag_address=lambda ram: ram.gorn_challenge_wins + 0x1,
    enable_if=lambda options_dict: options_dict["extra_spaceship_challenge_locations"]
)
GORN_GHOST_SHIP = LocationData(
    153, "Gorn: Defeat the Ghost Ship",
    checked_flag_address=lambda ram: ram.gorn_challenge_wins + 0x2,
    enable_if=lambda options_dict: options_dict["extra_spaceship_challenge_locations"]
)
GORN_RACE = LocationData(
    154, "Gorn: Race Through the Docking Bays",
    checked_flag_address=lambda ram: ram.gorn_challenge_wins + 0x3,
    enable_if=lambda options_dict: options_dict["extra_spaceship_challenge_locations"]
)

""" Snivelak """
SNIVELAK_RESCUE_ANGELA = LocationData(160, "Snivelak: Rescue Angela", snivelak_rescue_angelak_rule)
SNIVELAK_DYNAMO_PLATFORMS_PB = LocationData(161, "Snivelak: Dynamo Platforms - Platinum Bolt", snivelak_dynamo_pb_rule)
SNIVELAK_SWINGSHOT_TOWER_NT = LocationData(162, "Snivelak: Swingshot Tower - Nanotech Boost", snivelak_swingshot_tower_nt_rule)

""" Smolg """
SMOLG_BALLOON_TRANSMISSION = LocationData(170, "Smolg: Balloon Transmission", smolg_balloon_transmission_rule)
SMOLG_DISTRIBUTION_FACILITY_END = LocationData(171, "Smolg: Distribution Facility End - Hypnomatic Part", smolg_distribution_facility_end_rule,
    checked_flag_address=lambda ram: ram.hypnomatic_part1
)
SMOLG_MUTANT_CRAB = LocationData(172, "Smolg: Mutant Crab", smolg_mutant_crab_rule)
SMOLG_FLOATING_PLATFORM_PB = LocationData(173, "Smolg: Floating Platform - Platinum Bolt", smolg_floating_platform_pb_rule)
SMOLG_WAREHOUSE_PB = LocationData(174, "Smolg: Warehouse - Platinum Bolt", smolg_warehouse_pb_rule)

""" Damosel """
DAMOSEL_HYPNOTIST = LocationData(180, "Damosel: Hypnotist", damosel_hypnotist_rule)
DAMOSEL_TRAIN_RAILS = LocationData(181, "Damosel: Train Rails - Hypnomatic Part", damosel_train_rails_rule,
    checked_flag_address=lambda ram: ram.hypnomatic_part2
)
DAMOSEL_DEFEAT_MOTHERSHIP = LocationData(182, "Damosel: Defeat Mothership - Mapper")
DAMOSEL_FROZEN_FOUNTAIN_PB = LocationData(183, "Damosel: Frozen Fountain - Platinum Bolt", damosel_frozen_mountain_pb_rule)
DAMOSEL_PYRAMID_PB = LocationData(184, "Damosel: Pyramid - Platinum Bolt", damosel_pyramid_pb_rule)

""" Grelbin """
GRELBIN_FIND_ANGELA = LocationData(190, "Grelbin: Find Angela", grelbin_find_angela_rule)
GRELBIN_MYSTIC_MORE_MOONSTONES = LocationData(191, "Grelbin: Mystic More Moonstones - Hypnomatic Part", grelbin_mystic_more_moonstones_rule,
    checked_flag_address=lambda ram: ram.hypnomatic_part3
)
GRELBIN_ICE_PLAINS_PB = LocationData(192, "Grelbin: Ice Plains - Platinum Bolt", grelbin_ice_plains_pb_rule)
GRELBIN_UNDERWATER_TUNNEL_PB = LocationData(193, "Grelbin: Underwater Tunnel - Platinum Bolt", grelbin_underwater_tunnel_pb_rule)
GRELBIN_YETI_CAVE_PB = LocationData(194, "Grelbin: Yeti Cave - Platinum Bolt", grelbin_yeti_cave_pb_rule)

""" Yeedil """
YEEDIL_DEFEAT_MUTATED_PROTOPET = LocationData(None, "Yeedil: Defeat Mutated Protopet", yeedil_defeat_mutated_protopet_rule)
YEEDIL_BRIDGE_GRINDRAIL_PB = LocationData(200, "Yeedil: Bridge Grindrail - Platinum Bolt", yeedil_bridge_grindrail_pb_rule)
YEEDIL_TRACTOR_PILLAR_PB = LocationData(201, "Yeedil: Tractor Pillar - Platinum Bolt", yeedil_tractor_pillar_pb_rule)

""" Megacorp Vendor """
OOZLA_VENDOR_WEAPON_1 = LocationData(
    300, "Oozla: Megacorp Vendor - New Weapon 1",
    checked_flag_address=lambda ram: ram.secondary_inventory + Items.CHOPPER.offset,
    is_vendor=True
)
OOZLA_VENDOR_WEAPON_2 = LocationData(
    301, "Oozla: Megacorp Vendor - New Weapon 2",
    checked_flag_address=lambda ram: ram.secondary_inventory + Items.BLITZ_GUN.offset,
    is_vendor=True
)
ENDAKO_VENDOR_WEAPON_1 = LocationData(
    302, "Endako: Megacorp Vendor - New Weapon 1",
    checked_flag_address=lambda ram: ram.secondary_inventory + Items.PULSE_RIFLE.offset,
    is_vendor=True
)
ENDAKO_VENDOR_WEAPON_2 = LocationData(
    303, "Endako: Megacorp Vendor - New Weapon 2",
    checked_flag_address=lambda ram: ram.secondary_inventory + Items.MINITURRET_GLOVE.offset,
    is_vendor=True
)
BARLOW_VENDOR_WEAPON = LocationData(
    304, "Barlow: Megacorp Vendor - New Weapon",
    checked_flag_address=lambda ram: ram.secondary_inventory + Items.SEEKER_GUN.offset,
    is_vendor=True
)
NOTAK_VENDOR_WEAPON = LocationData(
    305, "Notak: Megacorp Vendor - New Weapon",
    checked_flag_address=lambda ram: ram.secondary_inventory + Items.SYNTHENOID.offset,
    is_vendor=True
)
TABORA_VENDOR_WEAPON_1 = LocationData(
    306, "Tabora: Megacorp Vendor - New Weapon 1",
    checked_flag_address=lambda ram: ram.secondary_inventory + Items.LAVA_GUN.offset,
    is_vendor=True
)
TABORA_VENDOR_WEAPON_2 = LocationData(
    307, "Tabora: Megacorp Vendor - New Weapon 2",
    checked_flag_address=lambda ram: ram.secondary_inventory + Items.BOUNCER.offset,
    is_vendor=True
)
DOBBO_VENDOR_WEAPON = LocationData(
    308, "Dobbo: Megacorp Vendor - New Weapon",
    checked_flag_address=lambda ram: ram.secondary_inventory + Items.MINIROCKET_TUBE.offset,
    is_vendor=True
)
JOBA_VENDOR_WEAPON_1 = LocationData(
    309, "Joba: Megacorp Vendor - New Weapon 1",
    checked_flag_address=lambda ram: ram.secondary_inventory + Items.SPIDERBOT_GLOVE.offset,
    is_vendor=True
)
JOBA_VENDOR_WEAPON_2 = LocationData(
    310, "Joba: Megacorp Vendor - New Weapon 2",
    checked_flag_address=lambda ram: ram.secondary_inventory + Items.PLASMA_COIL.offset,
    is_vendor=True
)
TODANO_VENDOR_WEAPON = LocationData(
    311, "Todano: Megacorp Vendor - New Weapon",
    checked_flag_address=lambda ram: ram.secondary_inventory + Items.HOVERBOMB_GUN.offset,
    is_vendor=True
)
ARANOS_VENDOR_WEAPON_1 = LocationData(
    312, "Aranos Prison: Megacorp Vendor - New Weapon 1",
    checked_flag_address=lambda ram: ram.secondary_inventory + Items.SHIELD_CHARGER.offset,
    is_vendor=True
)
ARANOS_VENDOR_WEAPON_2 = LocationData(
    313, "Aranos Prison: Megacorp Vendor - New Weapon 2",
    checked_flag_address=lambda ram: ram.secondary_inventory + Items.ZODIAC.offset,
    is_vendor=True
)

""" Gadgetron Vendor """
BARLOW_GADGETRON_1 = LocationData(
    314, "Barlow: Gadgetron Vendor - Weapon 1",
    checked_flag_address=lambda ram: ram.secondary_inventory + Items.BOMB_GLOVE.offset,
    is_vendor=True
)
BARLOW_GADGETRON_2 = LocationData(
    315, "Barlow: Gadgetron Vendor - Weapon 2",
    checked_flag_address=lambda ram: ram.secondary_inventory + Items.VISIBOMB_GUN.offset,
    is_vendor=True
)
BARLOW_GADGETRON_3 = LocationData(
    316, "Barlow: Gadgetron Vendor - Weapon 3",
    checked_flag_address=lambda ram: ram.secondary_inventory + Items.TESLA_CLAW.offset,
    is_vendor=True
)
BARLOW_GADGETRON_4 = LocationData(
    317, "Barlow: Gadgetron Vendor - Weapon 4",
    checked_flag_address=lambda ram: ram.secondary_inventory + Items.DECOY_GLOVE.offset,
    is_vendor=True
)
BARLOW_GADGETRON_5 = LocationData(
    318, "Barlow: Gadgetron Vendor - Weapon 5",
    checked_flag_address=lambda ram: ram.secondary_inventory + Items.RYNO_II.offset,
    is_vendor=True
)
BARLOW_GADGETRON_6 = LocationData(
    319, "Barlow: Gadgetron Vendor - Weapon 6",
    checked_flag_address=lambda ram: ram.secondary_inventory + Items.WALLOPER.offset,
    is_vendor=True
)

# Keep in correct order
MEGACORP_VENDOR_LOCATIONS: Sequence[LocationData] = [
    OOZLA_VENDOR_WEAPON_1,
    OOZLA_VENDOR_WEAPON_2,
    ENDAKO_VENDOR_WEAPON_1,
    ENDAKO_VENDOR_WEAPON_2,
    BARLOW_VENDOR_WEAPON,
    NOTAK_VENDOR_WEAPON,
    TABORA_VENDOR_WEAPON_1,
    TABORA_VENDOR_WEAPON_2,
    DOBBO_VENDOR_WEAPON,
    JOBA_VENDOR_WEAPON_1,
    JOBA_VENDOR_WEAPON_2,
    TODANO_VENDOR_WEAPON,
    ARANOS_VENDOR_WEAPON_1,
    ARANOS_VENDOR_WEAPON_2,
]

# Keep in correct order
GADGETRON_VENDOR_LOCATIONS: Sequence[LocationData] = [
    BARLOW_GADGETRON_1,
    BARLOW_GADGETRON_2,
    BARLOW_GADGETRON_3,
    BARLOW_GADGETRON_4,
    BARLOW_GADGETRON_5,
    BARLOW_GADGETRON_6,
]
