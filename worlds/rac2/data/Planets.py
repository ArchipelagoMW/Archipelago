from typing import Set

from .Locations import *


class PlanetData(NamedTuple):
    name: str
    number: int
    locations: Sequence[LocationData] = []


ARANOS_TUTORIAL = PlanetData("Aranos Tutorial", 0)
OOZLA = PlanetData("Oozla", 1, [
    OOZLA_OUTSIDE_MEGACORP_STORE,
    OOZLA_END_STORE_CUTSCENE,
    OOZLA_MEGACORP_SCIENTIST,
    OOZLA_TRACTOR_PUZZLE_PB,
    OOZLA_SWAMP_RUINS_PB,
    OOZLA_SWAMP_MONSTER_II,
    OOZLA_VENDOR_WEAPON_1,
    OOZLA_VENDOR_WEAPON_2,
])
MAKTAR_NEBULA = PlanetData("Maktar Nebula", 2, [
    MAKTAR_ARENA_CHALLENGE,
    MAKTAR_PHOTO_BOOTH,
    MAKTAR_DEACTIVATE_JAMMING_ARRAY,
    MAKTAR_JAMMING_ARRAY_PB,
    MAKTAR_CRANE_PB,
])
ENDAKO = PlanetData("Endako", 3, [
    ENDAKO_CLANK_APARTMENT_SS,
    ENDAKO_CLANK_APARTMENT_GB,
    ENDAKO_RESCUE_CLANK_HELI,
    ENDAKO_RESCUE_CLANK_THRUSTER,
    ENDAKO_LEDGE_PB,
    ENDAKO_CRANE_PB,
    ENDAKO_CRANE_NT,
    ENDAKO_VENDOR_WEAPON_1,
    ENDAKO_VENDOR_WEAPON_2,
])
BARLOW = PlanetData("Barlow", 4, [
    BARLOW_INVENTOR,
    BARLOW_HOVERBIKE_RACE_TRANSMISSION,
    BARLOW_HOVERBIKE_RACE_PB,
    BARLOW_HOUND_CAVE_PB,
    BARLOW_VENDOR_WEAPON,
    BARLOW_GADGETRON_1,
    BARLOW_GADGETRON_2,
    BARLOW_GADGETRON_3,
    BARLOW_GADGETRON_4,
    BARLOW_GADGETRON_5,
    BARLOW_GADGETRON_6,
])
FELTZIN_SYSTEM = PlanetData("Feltzin System", 5, [
    FELTZIN_DEFEAT_THUG_SHIPS,
    FELTZIN_RACE_PB,
    FELTZIN_CARGO_BAY_NT,
    FELTZIN_DESTROY_SPACE_WASPS,
    FELTZIN_FIGHT_ACE_THUGS,
    FELTZIN_RACE,
])
NOTAK = PlanetData("Notak", 6, [
    NOTAK_TOP_PIER_TELESCREEN,
    NOTAK_WORKER_BOTS,
    NOTAK_BEHIND_BUILDING_PB,
    NOTAK_PROMENADE_SIGN_PB,
    NOTAK_TIMED_DYNAMO_PB,
    NOTAK_PROMENADE_END_NT,
    NOTAK_VENDOR_WEAPON,
])
SIBERIUS = PlanetData("Siberius", 7, [
    SIBERIUS_DEFEAT_THIEF,
    SIBERIUS_FLAMEBOT_LEDGE_PB,
    SIBERIUS_FENCED_AREA_PB,
])
TABORA = PlanetData("Tabora", 8, [
    TABORA_MEET_ANGELA,
    TABORA_UNDERGROUND_MINES_END,
    TABORA_UNDERGROUND_MINES_PB,
    TABORA_CANYON_GLIDE_PB,
    TABORA_NORTHEAST_DESERT_PB,
    TABORA_CANYON_GLIDE_PILLAR_NT,
    TABORA_OMNIWRENCH_10000,
    TABORA_VENDOR_WEAPON_1,
    TABORA_VENDOR_WEAPON_2,
])
DOBBO = PlanetData("Dobbo", 9, [
    DOBBO_DEFEAT_THUG_LEADER,
    DOBBO_FACILITY_TERMINAL,
    DOBBO_SPIDERBOT_ROOM_PB,
    DOBBO_FACILITY_GLIDE_PB,
    DOBBO_FACILITY_GLIDE_NT,
    DOBBO_VENDOR_WEAPON,
])
HRUGIS_CLOUD = PlanetData("Hrugis Cloud", 10, [
    HRUGIS_DESTROY_DEFENSES,
    HRUGIS_RACE_PB,
    HRUGIS_SABOTEURS,
    HRUGIS_BERSERK_DRONES,
    HRUGIS_RACE,
])
JOBA = PlanetData("Joba", 11, [
    JOBA_FIRST_HOVERBIKE_RACE,
    JOBA_SHADY_SALESMAN,
    JOBA_ARENA_BATTLE,
    JOBA_ARENA_CAGE_MATCH,
    JOBA_HIDDEN_CLIFF_PB,
    JOBA_LEVITATOR_TOWER_PB,
    JOBA_HOVERBIKE_RACE_SHORTCUT_NT,
    JOBA_TIMED_DYNAMO_NT,
    JOBA_VENDOR_WEAPON_1,
    JOBA_VENDOR_WEAPON_2,
])
TODANO = PlanetData("Todano", 12, [
    TODANO_SEARCH_ROCKET_SILO,
    TODANO_STUART_ZURGO_TRADE,
    TODANO_FACILITY_INTERIOR,
    TODANO_NEAR_STUART_ZURGO_PB,
    TODANO_END_TOUR_PB,
    TODANO_SPIDERBOT_CONVEYOR_PB,
    TODANO_ROCKET_SILO_NT,
    TODANO_VENDOR_WEAPON,
])
BOLDAN = PlanetData("Boldan", 13, [
    BOLDAN_FIND_FIZZWIDGET,
    BOLDAN_SPIDERBOT_ALLEY_PB,
    BOLDAN_FLOATING_PLATFORM_PB,
    BOLDAN_UPPER_DOME_PB,
    BOLDAN_FOUNTAIN_NT,
])
ARANOS_PRISON = PlanetData("Aranos Prison", 14, [
    ARANOS_CONTROL_ROOM,
    ARANOS_PLUMBER,
    ARANOS_UNDER_SHIP_PB,
    ARANOS_OMNIWRENCH_12000,
    ARANOS_VENDOR_WEAPON_1,
    ARANOS_VENDOR_WEAPON_2,
])
GORN = PlanetData("Gorn", 15, [
    GORN_DEFEAT_THUG_FLEET,
    GORN_RACE_PB,
    GORN_FIGHT_BANDITS,
    GORN_GHOST_SHIP,
    GORN_RACE,
])
SNIVELAK = PlanetData("Snivelak", 16, [
    SNIVELAK_RESCUE_ANGELA,
    SNIVELAK_DYNAMO_PLATFORMS_PB,
    SNIVELAK_SWINGSHOT_TOWER_NT,
])
SMOLG = PlanetData("Smolg", 17, [
    SMOLG_BALLOON_TRANSMISSION,
    SMOLG_DISTRIBUTION_FACILITY_END,
    SMOLG_MUTANT_CRAB,
    SMOLG_FLOATING_PLATFORM_PB,
    SMOLG_WAREHOUSE_PB,
])
DAMOSEL = PlanetData("Damosel", 18, [
    DAMOSEL_HYPNOTIST,
    DAMOSEL_TRAIN_RAILS,
    DAMOSEL_DEFEAT_MOTHERSHIP,
    DAMOSEL_FROZEN_FOUNTAIN_PB,
    DAMOSEL_PYRAMID_PB,
])
GRELBIN = PlanetData("Grelbin", 19, [
    GRELBIN_FIND_ANGELA,
    GRELBIN_MYSTIC_MORE_MOONSTONES,
    GRELBIN_ICE_PLAINS_PB,
    GRELBIN_UNDERWATER_TUNNEL_PB,
    GRELBIN_YETI_CAVE_PB,
])
YEEDIL = PlanetData("Yeedil", 20, [
    YEEDIL_DEFEAT_MUTATED_PROTOPET,
    YEEDIL_BRIDGE_GRINDRAIL_PB,
    YEEDIL_TRACTOR_PILLAR_PB,
])
DOBBO_ORBIT = PlanetData("Dobbo Orbit", 22)
DAMOSEL_ORBIT = PlanetData("Damosel Orbit", 23)
SHIP_SHACK = PlanetData("Ship Shack", 24)
WUPASH_NEBULA = PlanetData("Wupash Nebula", 25)
JAMMING_ARRAY = PlanetData("Jamming Array", 26)
INSOMNIAC_MUSEUM = PlanetData("Insomniac Museum", 30)

LOGIC_PLANETS: Sequence[PlanetData] = [
    OOZLA,
    MAKTAR_NEBULA,
    ENDAKO,
    BARLOW,
    FELTZIN_SYSTEM,
    NOTAK,
    SIBERIUS,
    TABORA,
    DOBBO,
    HRUGIS_CLOUD,
    JOBA,
    TODANO,
    BOLDAN,
    ARANOS_PRISON,
    GORN,
    SNIVELAK,
    SMOLG,
    DAMOSEL,
    GRELBIN,
    YEEDIL,
]

ALL_LOCATIONS: Sequence[LocationData] = [
    location
    for locations in [planet.locations for planet in LOGIC_PLANETS]
    for location in locations
]


def get_location_groups() -> Dict[str, Set[str]]:
    groups: Dict[str, Set[str]] = {}
    for planet in LOGIC_PLANETS:
        groups[planet.name] = {loc.name for loc in planet.locations}
    groups.update({
        "Spaceship": {
            *groups[FELTZIN_SYSTEM.name],
            *groups[HRUGIS_CLOUD.name],
            *groups[GORN.name]
        },
        "Hoverbike": {
            BARLOW_HOVERBIKE_RACE_TRANSMISSION.name,
            BARLOW_HOVERBIKE_RACE_PB.name,
            JOBA_FIRST_HOVERBIKE_RACE.name,
            JOBA_HOVERBIKE_RACE_SHORTCUT_NT.name,
        },
        "Giant Clank": {
            DOBBO_DEFEAT_THUG_LEADER.name,
            DAMOSEL_DEFEAT_MOTHERSHIP.name,
        },
        "Arena": {
            MAKTAR_ARENA_CHALLENGE.name,
            JOBA_ARENA_BATTLE.name,
            JOBA_ARENA_CAGE_MATCH.name,
        },
        "Tanky Bosses": {
            SNIVELAK_RESCUE_ANGELA.name,
            OOZLA_SWAMP_MONSTER_II.name,
            DOBBO_DEFEAT_THUG_LEADER.name,
            DAMOSEL_DEFEAT_MOTHERSHIP.name,
        },
    })

    return groups


class SpaceshipSystemTextInfo(NamedTuple):
    challenge_descriptions: Sequence[int]
    challenge_locations: Sequence[int]
    perfect_race_location: int
    challenge_1_completed_text: int


# This dictionary is used by the `process_spaceship_text` function in the game client in order to know how to properly
# set dynamic text in the spaceship challenge menus
SPACESHIP_SYSTEMS: Dict[int, SpaceshipSystemTextInfo] = {
    FELTZIN_SYSTEM.number: SpaceshipSystemTextInfo(
        challenge_descriptions=[0x2FDB, 0x2FDD, 0x2FDC, 0x2FDF],
        challenge_locations=[
            FELTZIN_DEFEAT_THUG_SHIPS.location_id,
            FELTZIN_DESTROY_SPACE_WASPS.location_id,
            FELTZIN_FIGHT_ACE_THUGS.location_id,
            FELTZIN_RACE.location_id
        ],
        perfect_race_location=FELTZIN_RACE_PB.location_id,
        challenge_1_completed_text=0x11F5,
    ),
    HRUGIS_CLOUD.number: SpaceshipSystemTextInfo(
        challenge_descriptions=[0x2FE7, 0x2FE8, 0x2FE9, 0x2FEB],
        challenge_locations=[
            HRUGIS_DESTROY_DEFENSES.location_id,
            HRUGIS_SABOTEURS.location_id,
            HRUGIS_BERSERK_DRONES.location_id,
            HRUGIS_RACE.location_id
        ],
        perfect_race_location=HRUGIS_RACE_PB.location_id,
        challenge_1_completed_text=0x11FB,
    ),
    GORN.number: SpaceshipSystemTextInfo(
        challenge_descriptions=[0x2FEF, 0x2FF0, 0x2FF1, 0x2FF2],
        challenge_locations=[
            GORN_DEFEAT_THUG_FLEET.location_id,
            GORN_FIGHT_BANDITS.location_id,
            GORN_GHOST_SHIP.location_id,
            GORN_RACE.location_id
        ],
        perfect_race_location=GORN_RACE_PB.location_id,
        challenge_1_completed_text=0x11FF,
    )
}


def get_all_active_locations(options_as_dict: Dict[str, Any]):
    return [loc for loc in ALL_LOCATIONS
            if (loc.enable_if is None or loc.enable_if(options_as_dict))
            and loc.location_id is not None]
