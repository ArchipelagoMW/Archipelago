import enum
from typing import List, Tuple, Optional, Callable, NamedTuple, Set, Any, TYPE_CHECKING
from . import item_names
from .options import (get_option_value, RequiredTactics,
    LocationInclusion, KerriganPresence,
)
from .rules import SC2Logic
from .mission_tables import SC2Mission

from BaseClasses import Location
from worlds.AutoWorld import World

if TYPE_CHECKING:
    from BaseClasses import CollectionState
    from . import SC2World

SC2WOL_LOC_ID_OFFSET = 1000
SC2HOTS_LOC_ID_OFFSET = 20000000  # Avoid clashes with The Legend of Zelda
SC2LOTV_LOC_ID_OFFSET = SC2HOTS_LOC_ID_OFFSET + 2000
SC2NCO_LOC_ID_OFFSET = SC2LOTV_LOC_ID_OFFSET + 2500
SC2_RACESWAP_LOC_ID_OFFSET = SC2NCO_LOC_ID_OFFSET + 900


class SC2Location(Location):
    game: str = "Starcraft2"


class LocationType(enum.IntEnum):
    VICTORY = 0  # Winning a mission
    VANILLA = 1  # Objectives that provided metaprogression in the original campaign, along with a few other locations for a balanced experience
    EXTRA = 2  # Additional locations based on mission progression, collecting in-mission rewards, etc. that do not significantly increase the challenge.
    CHALLENGE = 3  # Challenging objectives, often harder than just completing a mission, and often associated with Achievements
    MASTERY = 4  # Extremely challenging objectives often associated with Masteries and Feats of Strength in the original campaign
    SPEEDRUN = 5  # Objectives based around beating objectives within a time-limit


class LocationFlag(enum.IntFlag):
    NONE = 0
    SPEEDRUN = enum.auto()
    """Locations that are about doing something fast"""
    PREVENTATIVE = enum.auto()
    """Locations that are about preventing something from happening"""


class LocationData(NamedTuple):
    region: str
    name: str
    code: int
    type: LocationType
    rule: Callable[['CollectionState'], bool] = Location.access_rule
    tags: LocationFlag = LocationFlag.NONE


def make_location_data(
    region: str,
    name: str,
    code: int,
    type: LocationType,
    rule: Callable[['CollectionState'], bool] = Location.access_rule,
    flags: LocationFlag = LocationFlag.NONE,
) -> LocationData:
    return LocationData(region, f'{region}: {name}', code, type, rule, flags)


def get_location_types(world: 'SC2World', inclusion_type: int) -> Set[LocationType]:
    """
    :param world: The starcraft 2 world object
    :param inclusion_type: Level of inclusion to check for
    :return: A list of location types that match the inclusion type
    """
    exclusion_options = [
        ("vanilla_locations", LocationType.VANILLA),
        ("extra_locations", LocationType.EXTRA),
        ("challenge_locations", LocationType.CHALLENGE),
        ("mastery_locations", LocationType.MASTERY),
        ("speedrun_locations", LocationType.SPEEDRUN),
    ]
    excluded_location_types = set()
    for option_name, location_type in exclusion_options:
        if get_option_value(world, option_name) is inclusion_type:
            excluded_location_types.add(location_type)
    return excluded_location_types


def get_plando_locations(world: World) -> List[str]:
    """

    :param multiworld:
    :param player:
    :return: A list of locations affected by a plando in a world
    """
    if world is None:
        return []
    plando_locations = []
    for plando_setting in world.multiworld.plando_items[world.player]:
        plando_locations += plando_setting.get("locations", [])
        plando_setting_location = plando_setting.get("location", None)
        if plando_setting_location is not None:
            plando_locations.append(plando_setting_location)

    return plando_locations


def get_locations(world: Optional['SC2World']) -> Tuple[LocationData, ...]:
    # Note: rules which are ended with or True are rules identified as needed later when restricted units is an option
    if world is None:
        logic_level = int(RequiredTactics.default)
        kerriganless = False
    else:
        logic_level = world.options.required_tactics.value
        kerriganless = (
            world.options.kerrigan_presence.value != KerriganPresence.option_vanilla
            or not world.options.enable_hots_missions.value
        )
    adv_tactics = logic_level != RequiredTactics.option_standard
    logic = SC2Logic(world)
    player = 1 if world is None else world.player
    location_table: List[LocationData] = [
        # WoL
        make_location_data(SC2Mission.LIBERATION_DAY.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 100, LocationType.VICTORY),
        make_location_data(SC2Mission.LIBERATION_DAY.mission_name, "First Statue", SC2WOL_LOC_ID_OFFSET + 101, LocationType.VANILLA),
        make_location_data(SC2Mission.LIBERATION_DAY.mission_name, "Second Statue", SC2WOL_LOC_ID_OFFSET + 102, LocationType.VANILLA),
        make_location_data(SC2Mission.LIBERATION_DAY.mission_name, "Third Statue", SC2WOL_LOC_ID_OFFSET + 103, LocationType.VANILLA),
        make_location_data(SC2Mission.LIBERATION_DAY.mission_name, "Fourth Statue", SC2WOL_LOC_ID_OFFSET + 104, LocationType.VANILLA),
        make_location_data(SC2Mission.LIBERATION_DAY.mission_name, "Fifth Statue", SC2WOL_LOC_ID_OFFSET + 105, LocationType.VANILLA),
        make_location_data(SC2Mission.LIBERATION_DAY.mission_name, "Sixth Statue", SC2WOL_LOC_ID_OFFSET + 106, LocationType.VANILLA),
        make_location_data(SC2Mission.LIBERATION_DAY.mission_name, "Special Delivery", SC2WOL_LOC_ID_OFFSET + 107, LocationType.EXTRA),
        make_location_data(SC2Mission.LIBERATION_DAY.mission_name, "Transport", SC2WOL_LOC_ID_OFFSET + 108, LocationType.EXTRA),
        make_location_data(SC2Mission.THE_OUTLAWS.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 200, LocationType.VICTORY,
            logic.terran_early_tech
        ),
        make_location_data(SC2Mission.THE_OUTLAWS.mission_name, "Rebel Base", SC2WOL_LOC_ID_OFFSET + 201, LocationType.VANILLA,
            logic.terran_early_tech
        ),
        make_location_data(SC2Mission.THE_OUTLAWS.mission_name, "North Resource Pickups", SC2WOL_LOC_ID_OFFSET + 202, LocationType.EXTRA,
            logic.terran_early_tech
        ),
        make_location_data(SC2Mission.THE_OUTLAWS.mission_name, "Bunker", SC2WOL_LOC_ID_OFFSET + 203, LocationType.VANILLA,
            logic.terran_early_tech
        ),
        make_location_data(SC2Mission.THE_OUTLAWS.mission_name, "Close Resource Pickups", SC2WOL_LOC_ID_OFFSET + 204, LocationType.EXTRA),
        make_location_data(SC2Mission.ZERO_HOUR.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 300, LocationType.VICTORY,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_defense_rating(state, True) >= 2
                and (adv_tactics or logic.terran_basic_anti_air(state)))
        ),
        make_location_data(SC2Mission.ZERO_HOUR.mission_name, "First Group Rescued", SC2WOL_LOC_ID_OFFSET + 301, LocationType.VANILLA),
        make_location_data(SC2Mission.ZERO_HOUR.mission_name, "Second Group Rescued", SC2WOL_LOC_ID_OFFSET + 302, LocationType.VANILLA,
            logic.terran_common_unit
        ),
        make_location_data(SC2Mission.ZERO_HOUR.mission_name, "Third Group Rescued", SC2WOL_LOC_ID_OFFSET + 303, LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_defense_rating(state, True) >= 2)
        ),
        make_location_data(SC2Mission.ZERO_HOUR.mission_name, "First Hatchery", SC2WOL_LOC_ID_OFFSET + 304, LocationType.CHALLENGE,
            logic.terran_competent_comp
        ),
        make_location_data(SC2Mission.ZERO_HOUR.mission_name, "Second Hatchery", SC2WOL_LOC_ID_OFFSET + 305, LocationType.CHALLENGE,
            logic.terran_competent_comp
        ),
        make_location_data(SC2Mission.ZERO_HOUR.mission_name, "Third Hatchery", SC2WOL_LOC_ID_OFFSET + 306, LocationType.CHALLENGE,
            logic.terran_competent_comp
        ),
        make_location_data(SC2Mission.ZERO_HOUR.mission_name, "Fourth Hatchery", SC2WOL_LOC_ID_OFFSET + 307, LocationType.CHALLENGE,
            logic.terran_competent_comp
        ),
        make_location_data(SC2Mission.ZERO_HOUR.mission_name, "Ride's on its Way", SC2WOL_LOC_ID_OFFSET + 308, LocationType.EXTRA,
            logic.terran_common_unit
        ),
        make_location_data(SC2Mission.ZERO_HOUR.mission_name, "Hold Just a Little Longer", SC2WOL_LOC_ID_OFFSET + 309, LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_defense_rating(state, True) >= 2)
        ),
        make_location_data(SC2Mission.ZERO_HOUR.mission_name, "Cavalry's on the Way", SC2WOL_LOC_ID_OFFSET + 310, LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_defense_rating(state, True) >= 2)
        ),
        make_location_data(SC2Mission.EVACUATION.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 400, LocationType.VICTORY,
            lambda state: (
                logic.terran_early_tech(state)
                and (adv_tactics
                    and logic.terran_basic_anti_air(state)
                    or logic.terran_competent_anti_air(state)
                ))
        ),
        make_location_data(SC2Mission.EVACUATION.mission_name, "North Chrysalis", SC2WOL_LOC_ID_OFFSET + 401, LocationType.VANILLA),
        make_location_data(SC2Mission.EVACUATION.mission_name, "West Chrysalis", SC2WOL_LOC_ID_OFFSET + 402, LocationType.VANILLA,
            logic.terran_early_tech
        ),
        make_location_data(SC2Mission.EVACUATION.mission_name, "East Chrysalis", SC2WOL_LOC_ID_OFFSET + 403, LocationType.VANILLA,
            logic.terran_early_tech
        ),
        make_location_data(SC2Mission.EVACUATION.mission_name, "Reach Hanson", SC2WOL_LOC_ID_OFFSET + 404, LocationType.EXTRA),
        make_location_data(SC2Mission.EVACUATION.mission_name, "Secret Resource Stash", SC2WOL_LOC_ID_OFFSET + 405, LocationType.EXTRA),
        make_location_data(SC2Mission.EVACUATION.mission_name, "Flawless", SC2WOL_LOC_ID_OFFSET + 406, LocationType.CHALLENGE,
            lambda state: (
                logic.terran_early_tech(state)
                and logic.terran_defense_rating(state, True, False) >= 2
                and (adv_tactics
                    and logic.terran_basic_anti_air(state)
                    and logic.terran_basic_anti_air(state)
                    or logic.terran_competent_anti_air(state))),
            flags=LocationFlag.PREVENTATIVE
        ),
        make_location_data(SC2Mission.OUTBREAK.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 500, LocationType.VICTORY,
            logic.terran_outbreak_requirement
        ),
        make_location_data(SC2Mission.OUTBREAK.mission_name, "Left Infestor", SC2WOL_LOC_ID_OFFSET + 501, LocationType.VANILLA,
            logic.terran_outbreak_requirement
        ),
        make_location_data(SC2Mission.OUTBREAK.mission_name, "Right Infestor", SC2WOL_LOC_ID_OFFSET + 502, LocationType.VANILLA,
            logic.terran_outbreak_requirement
        ),
        make_location_data(SC2Mission.OUTBREAK.mission_name, "North Infested Command Center", SC2WOL_LOC_ID_OFFSET + 503, LocationType.EXTRA,
            logic.terran_outbreak_requirement
        ),
        make_location_data(SC2Mission.OUTBREAK.mission_name, "South Infested Command Center", SC2WOL_LOC_ID_OFFSET + 504, LocationType.EXTRA,
            logic.terran_outbreak_requirement
        ),
        make_location_data(SC2Mission.OUTBREAK.mission_name, "Northwest Bar", SC2WOL_LOC_ID_OFFSET + 505, LocationType.EXTRA,
            logic.terran_outbreak_requirement
        ),
        make_location_data(SC2Mission.OUTBREAK.mission_name, "North Bar", SC2WOL_LOC_ID_OFFSET + 506, LocationType.EXTRA,
            logic.terran_outbreak_requirement
        ),
        make_location_data(SC2Mission.OUTBREAK.mission_name, "South Bar", SC2WOL_LOC_ID_OFFSET + 507, LocationType.EXTRA,
            logic.terran_outbreak_requirement
        ),
        make_location_data(SC2Mission.SAFE_HAVEN.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 600, LocationType.VICTORY,
            logic.terran_safe_haven_requirement
        ),
        make_location_data(SC2Mission.SAFE_HAVEN.mission_name, "North Nexus", SC2WOL_LOC_ID_OFFSET + 601, LocationType.EXTRA,
            logic.terran_safe_haven_requirement
        ),
        make_location_data(SC2Mission.SAFE_HAVEN.mission_name, "East Nexus", SC2WOL_LOC_ID_OFFSET + 602, LocationType.EXTRA,
            logic.terran_safe_haven_requirement
        ),
        make_location_data(SC2Mission.SAFE_HAVEN.mission_name, "South Nexus", SC2WOL_LOC_ID_OFFSET + 603, LocationType.EXTRA,
            logic.terran_safe_haven_requirement
        ),
        make_location_data(SC2Mission.SAFE_HAVEN.mission_name, "First Terror Fleet", SC2WOL_LOC_ID_OFFSET + 604, LocationType.VANILLA,
            logic.terran_safe_haven_requirement
        ),
        make_location_data(SC2Mission.SAFE_HAVEN.mission_name, "Second Terror Fleet", SC2WOL_LOC_ID_OFFSET + 605, LocationType.VANILLA,
            logic.terran_safe_haven_requirement
        ),
        make_location_data(SC2Mission.SAFE_HAVEN.mission_name, "Third Terror Fleet", SC2WOL_LOC_ID_OFFSET + 606, LocationType.VANILLA,
            logic.terran_safe_haven_requirement
        ),
        make_location_data(SC2Mission.HAVENS_FALL.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 700, LocationType.VICTORY,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_competent_anti_air(state)
                and logic.terran_defense_rating(state, True) >= 3)
        ),
        make_location_data(SC2Mission.HAVENS_FALL.mission_name, "North Hive", SC2WOL_LOC_ID_OFFSET + 701, LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_competent_anti_air(state)
                and logic.terran_defense_rating(state, True) >= 3)
        ),
        make_location_data(SC2Mission.HAVENS_FALL.mission_name, "East Hive", SC2WOL_LOC_ID_OFFSET + 702, LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_competent_anti_air(state)
                and logic.terran_defense_rating(state, True) >= 3)
        ),
        make_location_data(SC2Mission.HAVENS_FALL.mission_name, "South Hive", SC2WOL_LOC_ID_OFFSET + 703, LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_competent_anti_air(state)
                and logic.terran_defense_rating(state, True) >= 3)
        ),
        make_location_data(SC2Mission.HAVENS_FALL.mission_name, "Northeast Colony Base", SC2WOL_LOC_ID_OFFSET + 704, LocationType.CHALLENGE,
            logic.terran_respond_to_colony_infestations
        ),
        make_location_data(SC2Mission.HAVENS_FALL.mission_name, "East Colony Base", SC2WOL_LOC_ID_OFFSET + 705, LocationType.CHALLENGE,
            logic.terran_respond_to_colony_infestations
        ),
        make_location_data(SC2Mission.HAVENS_FALL.mission_name, "Middle Colony Base", SC2WOL_LOC_ID_OFFSET + 706, LocationType.CHALLENGE,
            logic.terran_respond_to_colony_infestations
        ),
        make_location_data(SC2Mission.HAVENS_FALL.mission_name, "Southeast Colony Base", SC2WOL_LOC_ID_OFFSET + 707, LocationType.CHALLENGE,
            logic.terran_respond_to_colony_infestations
        ),
        make_location_data(SC2Mission.HAVENS_FALL.mission_name, "Southwest Colony Base", SC2WOL_LOC_ID_OFFSET + 708, LocationType.CHALLENGE,
            logic.terran_respond_to_colony_infestations
        ),
        make_location_data(SC2Mission.HAVENS_FALL.mission_name, "Southwest Gas Pickups", SC2WOL_LOC_ID_OFFSET + 709, LocationType.EXTRA),
        make_location_data(SC2Mission.HAVENS_FALL.mission_name, "East Gas Pickups", SC2WOL_LOC_ID_OFFSET + 710, LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_competent_anti_air(state)
                and logic.terran_defense_rating(state, True) >= 3)
        ),
        make_location_data(SC2Mission.HAVENS_FALL.mission_name, "Southeast Gas Pickups", SC2WOL_LOC_ID_OFFSET + 711, LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_competent_anti_air(state)
                and logic.terran_defense_rating(state, True) >= 3)
        ),
        make_location_data(SC2Mission.SMASH_AND_GRAB.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 800, LocationType.VICTORY,
            lambda state: (
                logic.terran_common_unit(state)
                and (adv_tactics
                    and logic.terran_basic_anti_air(state)
                    or logic.terran_competent_anti_air(state)))
        ),
        make_location_data(SC2Mission.SMASH_AND_GRAB.mission_name, "First Relic", SC2WOL_LOC_ID_OFFSET + 801, LocationType.VANILLA),
        make_location_data(SC2Mission.SMASH_AND_GRAB.mission_name, "Second Relic", SC2WOL_LOC_ID_OFFSET + 802, LocationType.VANILLA),
        make_location_data(SC2Mission.SMASH_AND_GRAB.mission_name, "Third Relic", SC2WOL_LOC_ID_OFFSET + 803, LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and (adv_tactics
                    and logic.terran_basic_anti_air(state)
                    or logic.terran_competent_anti_air(state)))
        ),
        make_location_data(SC2Mission.SMASH_AND_GRAB.mission_name, "Fourth Relic", SC2WOL_LOC_ID_OFFSET + 804, LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and (adv_tactics
                    and logic.terran_basic_anti_air(state)
                    or logic.terran_competent_anti_air(state)))
        ),
        make_location_data(SC2Mission.SMASH_AND_GRAB.mission_name, "First Forcefield Area Busted", SC2WOL_LOC_ID_OFFSET + 805, LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and (adv_tactics
                    and logic.terran_basic_anti_air(state)
                    or logic.terran_competent_anti_air(state)))
        ),
        make_location_data(SC2Mission.SMASH_AND_GRAB.mission_name, "Second Forcefield Area Busted", SC2WOL_LOC_ID_OFFSET + 806, LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and (adv_tactics
                    and logic.terran_basic_anti_air(state)
                    or logic.terran_competent_anti_air(state)))
        ),
        make_location_data(SC2Mission.THE_DIG.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 900, LocationType.VICTORY,
            lambda state: (
                logic.terran_basic_anti_air(state)
                and logic.terran_defense_rating(state, False, True) >= 8
                and logic.terran_defense_rating(state, False, False) >= 6
                and logic.terran_common_unit(state)
                and (logic.marine_medic_upgrade(state) or adv_tactics))
        ),
        make_location_data(SC2Mission.THE_DIG.mission_name, "Left Relic", SC2WOL_LOC_ID_OFFSET + 901, LocationType.VANILLA,
            lambda state: (
                logic.terran_defense_rating(state, False, False) >= 6
                and logic.terran_common_unit(state)
                and (logic.marine_medic_upgrade(state) or adv_tactics))
        ),
        make_location_data(SC2Mission.THE_DIG.mission_name, "Right Ground Relic", SC2WOL_LOC_ID_OFFSET + 902, LocationType.VANILLA,
            lambda state: (
                logic.terran_defense_rating(state, False, False) >= 6
                and logic.terran_common_unit(state)
                and (logic.marine_medic_upgrade(state) or adv_tactics))
        ),
        make_location_data(SC2Mission.THE_DIG.mission_name, "Right Cliff Relic", SC2WOL_LOC_ID_OFFSET + 903, LocationType.VANILLA,
            lambda state: (
                logic.terran_defense_rating(state, False, False) >= 6
                and logic.terran_common_unit(state)
                and (logic.marine_medic_upgrade(state) or adv_tactics))
        ),
        make_location_data(SC2Mission.THE_DIG.mission_name, "Moebius Base", SC2WOL_LOC_ID_OFFSET + 904, LocationType.EXTRA,
            lambda state: logic.marine_medic_upgrade(state) or adv_tactics
        ),
        make_location_data(SC2Mission.THE_DIG.mission_name, "Door Outer Layer", SC2WOL_LOC_ID_OFFSET + 905, LocationType.EXTRA,
            lambda state: (
                logic.terran_defense_rating(state, False, False) >= 6
                and logic.terran_common_unit(state)
                and (logic.marine_medic_upgrade(state) or adv_tactics))
        ),
        make_location_data(SC2Mission.THE_DIG.mission_name, "Door Thermal Barrier", SC2WOL_LOC_ID_OFFSET + 906, LocationType.EXTRA,
            lambda state: (
                logic.terran_basic_anti_air(state)
                and logic.terran_defense_rating(state, False, True) >= 8
                and logic.terran_defense_rating(state, False, False) >= 6
                and logic.terran_common_unit(state)
                and (logic.marine_medic_upgrade(state) or adv_tactics))
        ),
        make_location_data(SC2Mission.THE_DIG.mission_name, "Cutting Through the Core", SC2WOL_LOC_ID_OFFSET + 907, LocationType.EXTRA,
            lambda state: (
                logic.terran_basic_anti_air(state)
                and logic.terran_defense_rating(state, False, True) >= 8
                and logic.terran_defense_rating(state, False, False) >= 6
                and logic.terran_common_unit(state)
                and (logic.marine_medic_upgrade(state) or adv_tactics))
        ),
        make_location_data(SC2Mission.THE_DIG.mission_name, "Structure Access Imminent", SC2WOL_LOC_ID_OFFSET + 908, LocationType.EXTRA,
            lambda state: (
                logic.terran_basic_anti_air(state)
                and logic.terran_defense_rating(state, False, True) >= 8
                and logic.terran_defense_rating(state, False, False) >= 6
                and logic.terran_common_unit(state)
                and (logic.marine_medic_upgrade(state) or adv_tactics))
        ),
        make_location_data(SC2Mission.THE_MOEBIUS_FACTOR.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 1000, LocationType.VICTORY,
            lambda state: (
                logic.terran_basic_anti_air(state)
                and (logic.terran_air(state)
                    or state.has_any({item_names.MEDIVAC, item_names.HERCULES}, player)
                    and logic.terran_common_unit(state)))
        ),
        make_location_data(SC2Mission.THE_MOEBIUS_FACTOR.mission_name, "1st Data Core", SC2WOL_LOC_ID_OFFSET + 1001, LocationType.VANILLA),
        make_location_data(SC2Mission.THE_MOEBIUS_FACTOR.mission_name, "2nd Data Core", SC2WOL_LOC_ID_OFFSET + 1002, LocationType.VANILLA,
            lambda state: (
                logic.terran_air(state)
                or (state.has_any({item_names.MEDIVAC, item_names.HERCULES}, player)
                    and logic.terran_common_unit(state)))
        ),
        make_location_data(SC2Mission.THE_MOEBIUS_FACTOR.mission_name, "South Rescue", SC2WOL_LOC_ID_OFFSET + 1003, LocationType.EXTRA,
            logic.terran_can_rescue
        ),
        make_location_data(SC2Mission.THE_MOEBIUS_FACTOR.mission_name, "Wall Rescue", SC2WOL_LOC_ID_OFFSET + 1004, LocationType.EXTRA,
            logic.terran_can_rescue
        ),
        make_location_data(SC2Mission.THE_MOEBIUS_FACTOR.mission_name, "Mid Rescue", SC2WOL_LOC_ID_OFFSET + 1005, LocationType.EXTRA,
            logic.terran_can_rescue
        ),
        make_location_data(SC2Mission.THE_MOEBIUS_FACTOR.mission_name, "Nydus Roof Rescue", SC2WOL_LOC_ID_OFFSET + 1006, LocationType.EXTRA,
            logic.terran_can_rescue
        ),
        make_location_data(SC2Mission.THE_MOEBIUS_FACTOR.mission_name, "Alive Inside Rescue", SC2WOL_LOC_ID_OFFSET + 1007, LocationType.EXTRA,
            logic.terran_can_rescue
        ),
        make_location_data(SC2Mission.THE_MOEBIUS_FACTOR.mission_name, "Brutalisk", SC2WOL_LOC_ID_OFFSET + 1008, LocationType.VANILLA,
            lambda state: (
                logic.terran_basic_anti_air(state)
                and (logic.terran_air(state)
                    or state.has_any({item_names.MEDIVAC, item_names.HERCULES}, player)
                    and logic.terran_common_unit(state)))
        ),
        make_location_data(SC2Mission.THE_MOEBIUS_FACTOR.mission_name, "3rd Data Core", SC2WOL_LOC_ID_OFFSET + 1009, LocationType.VANILLA,
            lambda state: (
                logic.terran_basic_anti_air(state)
                and (logic.terran_air(state)
                    or state.has_any({item_names.MEDIVAC, item_names.HERCULES}, player)
                    and logic.terran_common_unit(state)))
        ),
        make_location_data(SC2Mission.SUPERNOVA.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 1100, LocationType.VICTORY,
            logic.terran_beats_protoss_deathball
        ),
        make_location_data(SC2Mission.SUPERNOVA.mission_name, "West Relic", SC2WOL_LOC_ID_OFFSET + 1101, LocationType.VANILLA),
        make_location_data(SC2Mission.SUPERNOVA.mission_name, "North Relic", SC2WOL_LOC_ID_OFFSET + 1102, LocationType.VANILLA),
        make_location_data(SC2Mission.SUPERNOVA.mission_name, "South Relic", SC2WOL_LOC_ID_OFFSET + 1103, LocationType.VANILLA,
            logic.terran_beats_protoss_deathball
        ),
        make_location_data(SC2Mission.SUPERNOVA.mission_name, "East Relic", SC2WOL_LOC_ID_OFFSET + 1104, LocationType.VANILLA,
            logic.terran_beats_protoss_deathball
        ),
        make_location_data(SC2Mission.SUPERNOVA.mission_name, "Landing Zone Cleared", SC2WOL_LOC_ID_OFFSET + 1105, LocationType.EXTRA),
        make_location_data(SC2Mission.SUPERNOVA.mission_name, "Middle Base", SC2WOL_LOC_ID_OFFSET + 1106, LocationType.EXTRA,
            logic.terran_beats_protoss_deathball
        ),
        make_location_data(SC2Mission.SUPERNOVA.mission_name, "Southeast Base", SC2WOL_LOC_ID_OFFSET + 1107, LocationType.EXTRA,
            logic.terran_beats_protoss_deathball
        ),
        make_location_data(SC2Mission.MAW_OF_THE_VOID.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 1200, LocationType.VICTORY,
            logic.terran_survives_rip_field
        ),
        make_location_data(SC2Mission.MAW_OF_THE_VOID.mission_name, "Landing Zone Cleared", SC2WOL_LOC_ID_OFFSET + 1201, LocationType.EXTRA),
        make_location_data(SC2Mission.MAW_OF_THE_VOID.mission_name, "Expansion Prisoners", SC2WOL_LOC_ID_OFFSET + 1202, LocationType.VANILLA,
            lambda state: adv_tactics or logic.terran_survives_rip_field(state)
        ),
        make_location_data(SC2Mission.MAW_OF_THE_VOID.mission_name, "South Close Prisoners", SC2WOL_LOC_ID_OFFSET + 1203, LocationType.VANILLA,
            lambda state: adv_tactics or logic.terran_survives_rip_field(state)
        ),
        make_location_data(SC2Mission.MAW_OF_THE_VOID.mission_name, "South Far Prisoners", SC2WOL_LOC_ID_OFFSET + 1204, LocationType.VANILLA,
            logic.terran_survives_rip_field
        ),
        make_location_data(SC2Mission.MAW_OF_THE_VOID.mission_name, "North Prisoners", SC2WOL_LOC_ID_OFFSET + 1205, LocationType.VANILLA,
            logic.terran_survives_rip_field
        ),
        make_location_data(SC2Mission.MAW_OF_THE_VOID.mission_name, "Mothership", SC2WOL_LOC_ID_OFFSET + 1206, LocationType.EXTRA,
            logic.terran_survives_rip_field
        ),
        make_location_data(SC2Mission.MAW_OF_THE_VOID.mission_name, "Expansion Rip Field Generator", SC2WOL_LOC_ID_OFFSET + 1207, LocationType.EXTRA,
            lambda state: adv_tactics or logic.terran_survives_rip_field(state)
        ),
        make_location_data(SC2Mission.MAW_OF_THE_VOID.mission_name, "Middle Rip Field Generator", SC2WOL_LOC_ID_OFFSET + 1208, LocationType.EXTRA,
            logic.terran_survives_rip_field
        ),
        make_location_data(SC2Mission.MAW_OF_THE_VOID.mission_name, "Southeast Rip Field Generator", SC2WOL_LOC_ID_OFFSET + 1209, LocationType.EXTRA,
            logic.terran_survives_rip_field
        ),
        make_location_data(SC2Mission.MAW_OF_THE_VOID.mission_name, "Stargate Rip Field Generator", SC2WOL_LOC_ID_OFFSET + 1210, LocationType.EXTRA,
            logic.terran_survives_rip_field
        ),
        make_location_data(SC2Mission.MAW_OF_THE_VOID.mission_name, "Northwest Rip Field Generator", SC2WOL_LOC_ID_OFFSET + 1211, LocationType.CHALLENGE,
            logic.terran_survives_rip_field
        ),
        make_location_data(SC2Mission.MAW_OF_THE_VOID.mission_name, "West Rip Field Generator", SC2WOL_LOC_ID_OFFSET + 1212, LocationType.CHALLENGE,
            logic.terran_survives_rip_field
        ),
        make_location_data(SC2Mission.MAW_OF_THE_VOID.mission_name, "Southwest Rip Field Generator", SC2WOL_LOC_ID_OFFSET + 1213, LocationType.CHALLENGE,
            logic.terran_survives_rip_field
        ),
        make_location_data(SC2Mission.DEVILS_PLAYGROUND.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 1300, LocationType.VICTORY,
            lambda state: (
                adv_tactics
                or logic.terran_basic_anti_air(state)
                    and (logic.terran_common_unit(state) or state.has(item_names.REAPER, player)))
        ),
        make_location_data(SC2Mission.DEVILS_PLAYGROUND.mission_name, "Tosh's Miners", SC2WOL_LOC_ID_OFFSET + 1301, LocationType.VANILLA),
        make_location_data(SC2Mission.DEVILS_PLAYGROUND.mission_name, "Brutalisk", SC2WOL_LOC_ID_OFFSET + 1302, LocationType.VANILLA,
            lambda state: adv_tactics or logic.terran_common_unit(state) or state.has(item_names.REAPER, player)
        ),
        make_location_data(SC2Mission.DEVILS_PLAYGROUND.mission_name, "North Reapers", SC2WOL_LOC_ID_OFFSET + 1303, LocationType.EXTRA),
        make_location_data(SC2Mission.DEVILS_PLAYGROUND.mission_name, "Middle Reapers", SC2WOL_LOC_ID_OFFSET + 1304, LocationType.EXTRA,
            lambda state: adv_tactics or logic.terran_common_unit(state) or state.has(item_names.REAPER, player)
        ),
        make_location_data(SC2Mission.DEVILS_PLAYGROUND.mission_name, "Southwest Reapers", SC2WOL_LOC_ID_OFFSET + 1305, LocationType.EXTRA,
            lambda state: adv_tactics or logic.terran_common_unit(state) or state.has(item_names.REAPER, player)
        ),
        make_location_data(SC2Mission.DEVILS_PLAYGROUND.mission_name, "Southeast Reapers", SC2WOL_LOC_ID_OFFSET + 1306, LocationType.EXTRA,
            lambda state: (
                adv_tactics
                or logic.terran_basic_anti_air(state)
                    and (logic.terran_common_unit(state) or state.has(item_names.REAPER, player)))
        ),
        make_location_data(SC2Mission.DEVILS_PLAYGROUND.mission_name, "East Reapers", SC2WOL_LOC_ID_OFFSET + 1307, LocationType.CHALLENGE,
            lambda state: (
                logic.terran_basic_anti_air(state)
                and (adv_tactics
                    or logic.terran_common_unit(state)
                    or state.has(item_names.REAPER, player)))
        ),
        make_location_data(SC2Mission.DEVILS_PLAYGROUND.mission_name, "Zerg Cleared", SC2WOL_LOC_ID_OFFSET + 1308, LocationType.CHALLENGE,
            lambda state: (
                logic.terran_competent_anti_air(state)
                and (logic.terran_common_unit(state)
                    or state.has(item_names.REAPER, player)))
        ),
        make_location_data(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 1400, LocationType.VICTORY,
            logic.welcome_to_the_jungle_requirement
        ),
        make_location_data(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "Close Relic", SC2WOL_LOC_ID_OFFSET + 1401, LocationType.VANILLA),
        make_location_data(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "West Relic", SC2WOL_LOC_ID_OFFSET + 1402, LocationType.VANILLA,
            logic.welcome_to_the_jungle_requirement
        ),
        make_location_data(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "North-East Relic", SC2WOL_LOC_ID_OFFSET + 1403, LocationType.VANILLA,
            logic.welcome_to_the_jungle_requirement
        ),
        make_location_data(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "Middle Base", SC2WOL_LOC_ID_OFFSET + 1404, LocationType.EXTRA,
            logic.welcome_to_the_jungle_requirement
        ),
        make_location_data(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "Main Base", SC2WOL_LOC_ID_OFFSET + 1405, LocationType.MASTERY,
            lambda state: (
                logic.welcome_to_the_jungle_requirement(state)
                and logic.terran_beats_protoss_deathball(state)
                and logic.terran_base_trasher(state))
        ),
        make_location_data(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "No Terrazine Nodes Sealed", SC2WOL_LOC_ID_OFFSET + 1406, LocationType.CHALLENGE,
            lambda state: (
                logic.welcome_to_the_jungle_requirement(state)
                and logic.terran_competent_ground_to_air(state)
                and logic.terran_beats_protoss_deathball(state)),
            flags=LocationFlag.PREVENTATIVE
        ),
        make_location_data(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "Up to 1 Terrazine Node Sealed", SC2WOL_LOC_ID_OFFSET + 1407, LocationType.CHALLENGE,
            lambda state: (
                logic.welcome_to_the_jungle_requirement(state)
                and logic.terran_competent_ground_to_air(state)
                and logic.terran_beats_protoss_deathball(state)),
            flags=LocationFlag.PREVENTATIVE
        ),
        make_location_data(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "Up to 2 Terrazine Nodes Sealed", SC2WOL_LOC_ID_OFFSET + 1408, LocationType.CHALLENGE,
            lambda state: (
                logic.welcome_to_the_jungle_requirement(state)
                and logic.terran_beats_protoss_deathball(state)),
            flags=LocationFlag.PREVENTATIVE
        ),
        make_location_data(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "Up to 3 Terrazine Nodes Sealed", SC2WOL_LOC_ID_OFFSET + 1409, LocationType.CHALLENGE,
            lambda state: (
                logic.welcome_to_the_jungle_requirement(state)
                and logic.terran_competent_comp(state)),
            flags=LocationFlag.PREVENTATIVE
        ),
        make_location_data(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "Up to 4 Terrazine Nodes Sealed", SC2WOL_LOC_ID_OFFSET + 1410, LocationType.EXTRA,
            logic.welcome_to_the_jungle_requirement,
            flags=LocationFlag.PREVENTATIVE
        ),
        make_location_data(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "Up to 5 Terrazine Nodes Sealed", SC2WOL_LOC_ID_OFFSET + 1411, LocationType.EXTRA,
            logic.welcome_to_the_jungle_requirement,
            flags=LocationFlag.PREVENTATIVE
        ),
        make_location_data(SC2Mission.BREAKOUT.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 1500, LocationType.VICTORY),
        make_location_data(SC2Mission.BREAKOUT.mission_name, "Diamondback Prison", SC2WOL_LOC_ID_OFFSET + 1501, LocationType.VANILLA),
        make_location_data(SC2Mission.BREAKOUT.mission_name, "Siege Tank Prison", SC2WOL_LOC_ID_OFFSET + 1502, LocationType.VANILLA),
        make_location_data(SC2Mission.BREAKOUT.mission_name, "First Checkpoint", SC2WOL_LOC_ID_OFFSET + 1503, LocationType.EXTRA),
        make_location_data(SC2Mission.BREAKOUT.mission_name, "Second Checkpoint", SC2WOL_LOC_ID_OFFSET + 1504, LocationType.EXTRA),
        make_location_data(SC2Mission.GHOST_OF_A_CHANCE.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 1600, LocationType.VICTORY),
        make_location_data(SC2Mission.GHOST_OF_A_CHANCE.mission_name, "Terrazine Tank", SC2WOL_LOC_ID_OFFSET + 1601, LocationType.EXTRA),
        make_location_data(SC2Mission.GHOST_OF_A_CHANCE.mission_name, "Jorium Stockpile", SC2WOL_LOC_ID_OFFSET + 1602, LocationType.EXTRA),
        make_location_data(SC2Mission.GHOST_OF_A_CHANCE.mission_name, "First Island Spectres", SC2WOL_LOC_ID_OFFSET + 1603, LocationType.VANILLA),
        make_location_data(SC2Mission.GHOST_OF_A_CHANCE.mission_name, "Second Island Spectres", SC2WOL_LOC_ID_OFFSET + 1604, LocationType.VANILLA),
        make_location_data(SC2Mission.GHOST_OF_A_CHANCE.mission_name, "Third Island Spectres", SC2WOL_LOC_ID_OFFSET + 1605, LocationType.VANILLA),
        make_location_data(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 1700, LocationType.VICTORY,
            lambda state: (
                logic.great_train_robbery_train_stopper(state)
                and logic.terran_basic_anti_air(state))
        ),
        make_location_data(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "North Defiler", SC2WOL_LOC_ID_OFFSET + 1701, LocationType.VANILLA),
        make_location_data(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "Mid Defiler", SC2WOL_LOC_ID_OFFSET + 1702, LocationType.VANILLA),
        make_location_data(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "South Defiler", SC2WOL_LOC_ID_OFFSET + 1703, LocationType.VANILLA),
        make_location_data(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "Close Diamondback", SC2WOL_LOC_ID_OFFSET + 1704, LocationType.EXTRA),
        make_location_data(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "Northwest Diamondback", SC2WOL_LOC_ID_OFFSET + 1705, LocationType.EXTRA),
        make_location_data(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "North Diamondback", SC2WOL_LOC_ID_OFFSET + 1706, LocationType.EXTRA),
        make_location_data(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "Northeast Diamondback", SC2WOL_LOC_ID_OFFSET + 1707, LocationType.EXTRA),
        make_location_data(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "Southwest Diamondback", SC2WOL_LOC_ID_OFFSET + 1708, LocationType.EXTRA),
        make_location_data(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "Southeast Diamondback", SC2WOL_LOC_ID_OFFSET + 1709, LocationType.EXTRA),
        make_location_data(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "Kill Team", SC2WOL_LOC_ID_OFFSET + 1710, LocationType.CHALLENGE,
            lambda state: (
                (adv_tactics or logic.terran_common_unit(state))
                and logic.great_train_robbery_train_stopper(state)
                and logic.terran_basic_anti_air(state))
        ),
        make_location_data(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "Flawless", SC2WOL_LOC_ID_OFFSET + 1711, LocationType.CHALLENGE,
            lambda state:(
                logic.great_train_robbery_train_stopper(state)
                and logic.terran_basic_anti_air(state)),
            flags=LocationFlag.PREVENTATIVE
        ),
        make_location_data(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "2 Trains Destroyed", SC2WOL_LOC_ID_OFFSET + 1712, LocationType.EXTRA,
            logic.great_train_robbery_train_stopper
        ),
        make_location_data(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "4 Trains Destroyed", SC2WOL_LOC_ID_OFFSET + 1713, LocationType.EXTRA,
            lambda state: (
                logic.great_train_robbery_train_stopper(state)
                and logic.terran_basic_anti_air(state))
        ),
        make_location_data(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "6 Trains Destroyed", SC2WOL_LOC_ID_OFFSET + 1714, LocationType.EXTRA,
            lambda state: (
                logic.great_train_robbery_train_stopper(state)
                and logic.terran_basic_anti_air(state))
        ),
        make_location_data(SC2Mission.CUTTHROAT.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 1800, LocationType.VICTORY,
            lambda state: (
                logic.terran_common_unit(state)
                and (adv_tactics or logic.terran_basic_anti_air(state)))
        ),
        make_location_data(SC2Mission.CUTTHROAT.mission_name, "Mira Han", SC2WOL_LOC_ID_OFFSET + 1801, LocationType.EXTRA,
            logic.terran_common_unit
        ),
        make_location_data(SC2Mission.CUTTHROAT.mission_name, "North Relic", SC2WOL_LOC_ID_OFFSET + 1802, LocationType.VANILLA,
            logic.terran_common_unit
        ),
        make_location_data(SC2Mission.CUTTHROAT.mission_name, "Mid Relic", SC2WOL_LOC_ID_OFFSET + 1803, LocationType.VANILLA),
        make_location_data(SC2Mission.CUTTHROAT.mission_name, "Southwest Relic", SC2WOL_LOC_ID_OFFSET + 1804, LocationType.VANILLA,
            logic.terran_common_unit
        ),
        make_location_data(SC2Mission.CUTTHROAT.mission_name, "North Command Center", SC2WOL_LOC_ID_OFFSET + 1805, LocationType.EXTRA,
            logic.terran_common_unit
        ),
        make_location_data(SC2Mission.CUTTHROAT.mission_name, "South Command Center", SC2WOL_LOC_ID_OFFSET + 1806, LocationType.EXTRA,
            logic.terran_common_unit
        ),
        make_location_data(SC2Mission.CUTTHROAT.mission_name, "West Command Center", SC2WOL_LOC_ID_OFFSET + 1807, LocationType.EXTRA,
            logic.terran_common_unit
        ),
        make_location_data(SC2Mission.ENGINE_OF_DESTRUCTION.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 1900, LocationType.VICTORY,
            logic.engine_of_destruction_requirement
        ),
        make_location_data(SC2Mission.ENGINE_OF_DESTRUCTION.mission_name, "Odin", SC2WOL_LOC_ID_OFFSET + 1901, LocationType.EXTRA,
            logic.marine_medic_upgrade
        ),
        make_location_data(SC2Mission.ENGINE_OF_DESTRUCTION.mission_name, "Loki", SC2WOL_LOC_ID_OFFSET + 1902, LocationType.CHALLENGE,
            logic.engine_of_destruction_requirement
        ),
        make_location_data(SC2Mission.ENGINE_OF_DESTRUCTION.mission_name, "Lab Devourer", SC2WOL_LOC_ID_OFFSET + 1903, LocationType.VANILLA,
            logic.marine_medic_upgrade
        ),
        make_location_data(SC2Mission.ENGINE_OF_DESTRUCTION.mission_name, "North Devourer", SC2WOL_LOC_ID_OFFSET + 1904, LocationType.VANILLA,
            logic.engine_of_destruction_requirement
        ),
        make_location_data(SC2Mission.ENGINE_OF_DESTRUCTION.mission_name, "Southeast Devourer", SC2WOL_LOC_ID_OFFSET + 1905, LocationType.VANILLA,
            logic.engine_of_destruction_requirement
        ),
        make_location_data(SC2Mission.ENGINE_OF_DESTRUCTION.mission_name, "West Base", SC2WOL_LOC_ID_OFFSET + 1906, LocationType.EXTRA,
            logic.engine_of_destruction_requirement
        ),
        make_location_data(SC2Mission.ENGINE_OF_DESTRUCTION.mission_name, "Northwest Base", SC2WOL_LOC_ID_OFFSET + 1907, LocationType.EXTRA,
            logic.engine_of_destruction_requirement
        ),
        make_location_data(SC2Mission.ENGINE_OF_DESTRUCTION.mission_name, "Northeast Base", SC2WOL_LOC_ID_OFFSET + 1908, LocationType.EXTRA,
            logic.engine_of_destruction_requirement
        ),
        make_location_data(SC2Mission.ENGINE_OF_DESTRUCTION.mission_name, "Southeast Base", SC2WOL_LOC_ID_OFFSET + 1909, LocationType.EXTRA,
            logic.engine_of_destruction_requirement
        ),
        make_location_data(SC2Mission.MEDIA_BLITZ.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 2000, LocationType.VICTORY,
            logic.terran_competent_comp
        ),
        make_location_data(SC2Mission.MEDIA_BLITZ.mission_name, "Tower 1", SC2WOL_LOC_ID_OFFSET + 2001, LocationType.VANILLA,
            logic.terran_competent_comp
        ),
        make_location_data(SC2Mission.MEDIA_BLITZ.mission_name, "Tower 2", SC2WOL_LOC_ID_OFFSET + 2002, LocationType.VANILLA,
            logic.terran_competent_comp
        ),
        make_location_data(SC2Mission.MEDIA_BLITZ.mission_name, "Tower 3", SC2WOL_LOC_ID_OFFSET + 2003, LocationType.VANILLA,
            logic.terran_competent_comp
        ),
        make_location_data(SC2Mission.MEDIA_BLITZ.mission_name, "Science Facility", SC2WOL_LOC_ID_OFFSET + 2004, LocationType.VANILLA),
        make_location_data(SC2Mission.MEDIA_BLITZ.mission_name, "All Barracks", SC2WOL_LOC_ID_OFFSET + 2005, LocationType.EXTRA,
            logic.terran_competent_comp
        ),
        make_location_data(SC2Mission.MEDIA_BLITZ.mission_name, "All Factories", SC2WOL_LOC_ID_OFFSET + 2006, LocationType.EXTRA,
            logic.terran_competent_comp
        ),
        make_location_data(SC2Mission.MEDIA_BLITZ.mission_name, "All Starports", SC2WOL_LOC_ID_OFFSET + 2007, LocationType.EXTRA,
            lambda state: adv_tactics or logic.terran_competent_comp(state)
        ),
        make_location_data(SC2Mission.MEDIA_BLITZ.mission_name, "Odin Not Trashed", SC2WOL_LOC_ID_OFFSET + 2008, LocationType.CHALLENGE,
            logic.terran_competent_comp
        ),
        make_location_data(SC2Mission.MEDIA_BLITZ.mission_name, "Surprise Attack Ends", SC2WOL_LOC_ID_OFFSET + 2009, LocationType.EXTRA),
        make_location_data(SC2Mission.PIERCING_OF_THE_SHROUD.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 2100, LocationType.VICTORY,
            logic.marine_medic_upgrade
        ),
        make_location_data(SC2Mission.PIERCING_OF_THE_SHROUD.mission_name, "Holding Cell Relic", SC2WOL_LOC_ID_OFFSET + 2101, LocationType.VANILLA),
        make_location_data(SC2Mission.PIERCING_OF_THE_SHROUD.mission_name, "Brutalisk Relic", SC2WOL_LOC_ID_OFFSET + 2102, LocationType.VANILLA,
            logic.marine_medic_upgrade
        ),
        make_location_data(SC2Mission.PIERCING_OF_THE_SHROUD.mission_name, "First Escape Relic", SC2WOL_LOC_ID_OFFSET + 2103, LocationType.VANILLA,
            logic.marine_medic_upgrade
        ),
        make_location_data(SC2Mission.PIERCING_OF_THE_SHROUD.mission_name, "Second Escape Relic", SC2WOL_LOC_ID_OFFSET + 2104, LocationType.VANILLA,
            logic.marine_medic_upgrade
        ),
        make_location_data(SC2Mission.PIERCING_OF_THE_SHROUD.mission_name, "Brutalisk", SC2WOL_LOC_ID_OFFSET + 2105, LocationType.VANILLA,
            logic.marine_medic_upgrade
        ),
        make_location_data(SC2Mission.PIERCING_OF_THE_SHROUD.mission_name, "Fusion Reactor", SC2WOL_LOC_ID_OFFSET + 2106, LocationType.EXTRA,
            logic.marine_medic_upgrade
        ),
        make_location_data(SC2Mission.PIERCING_OF_THE_SHROUD.mission_name, "Entrance Holding Pen", SC2WOL_LOC_ID_OFFSET + 2107, LocationType.EXTRA),
        make_location_data(SC2Mission.PIERCING_OF_THE_SHROUD.mission_name, "Cargo Bay Warbot", SC2WOL_LOC_ID_OFFSET + 2108, LocationType.EXTRA),
        make_location_data(SC2Mission.PIERCING_OF_THE_SHROUD.mission_name, "Escape Warbot", SC2WOL_LOC_ID_OFFSET + 2109, LocationType.EXTRA,
            logic.marine_medic_upgrade
        ),
        make_location_data(SC2Mission.WHISPERS_OF_DOOM.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 2200, LocationType.VICTORY),
        make_location_data(SC2Mission.WHISPERS_OF_DOOM.mission_name, "First Hatchery", SC2WOL_LOC_ID_OFFSET + 2201, LocationType.VANILLA),
        make_location_data(SC2Mission.WHISPERS_OF_DOOM.mission_name, "Second Hatchery", SC2WOL_LOC_ID_OFFSET + 2202, LocationType.VANILLA),
        make_location_data(SC2Mission.WHISPERS_OF_DOOM.mission_name, "Third Hatchery", SC2WOL_LOC_ID_OFFSET + 2203, LocationType.VANILLA),
        make_location_data(SC2Mission.WHISPERS_OF_DOOM.mission_name, "First Prophecy Fragment", SC2WOL_LOC_ID_OFFSET + 2204, LocationType.EXTRA),
        make_location_data(SC2Mission.WHISPERS_OF_DOOM.mission_name, "Second Prophecy Fragment", SC2WOL_LOC_ID_OFFSET + 2205, LocationType.EXTRA),
        make_location_data(SC2Mission.WHISPERS_OF_DOOM.mission_name, "Third Prophecy Fragment", SC2WOL_LOC_ID_OFFSET + 2206, LocationType.EXTRA),
        make_location_data(SC2Mission.A_SINISTER_TURN.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 2300, LocationType.VICTORY,
            lambda state: logic.protoss_common_unit(state) and logic.protoss_competent_anti_air(state)
        ),
        make_location_data(SC2Mission.A_SINISTER_TURN.mission_name, "Robotics Facility", SC2WOL_LOC_ID_OFFSET + 2301, LocationType.VANILLA,
            lambda state: adv_tactics or logic.protoss_common_unit(state)
        ),
        make_location_data(SC2Mission.A_SINISTER_TURN.mission_name, "Dark Shrine", SC2WOL_LOC_ID_OFFSET + 2302, LocationType.VANILLA,
            lambda state: adv_tactics or logic.protoss_common_unit(state)
        ),
        make_location_data(SC2Mission.A_SINISTER_TURN.mission_name, "Templar Archives", SC2WOL_LOC_ID_OFFSET + 2303, LocationType.VANILLA,
            lambda state: logic.protoss_common_unit(state) and logic.protoss_competent_anti_air(state)
        ),
        make_location_data(SC2Mission.A_SINISTER_TURN.mission_name, "Northeast Base", SC2WOL_LOC_ID_OFFSET + 2304, LocationType.EXTRA,
            lambda state: logic.protoss_common_unit(state) and logic.protoss_competent_anti_air(state)
        ),
        make_location_data(SC2Mission.A_SINISTER_TURN.mission_name, "Southwest Base", SC2WOL_LOC_ID_OFFSET + 2305, LocationType.CHALLENGE,
            lambda state: logic.protoss_common_unit(state) and logic.protoss_competent_anti_air(state)
        ),
        make_location_data(SC2Mission.A_SINISTER_TURN.mission_name, "Maar", SC2WOL_LOC_ID_OFFSET + 2306, LocationType.EXTRA,
            logic.protoss_common_unit
        ),
        make_location_data(SC2Mission.A_SINISTER_TURN.mission_name, "Northwest Preserver", SC2WOL_LOC_ID_OFFSET + 2307, LocationType.EXTRA,
            lambda state: logic.protoss_common_unit(state) and logic.protoss_competent_anti_air(state)
        ),
        make_location_data(SC2Mission.A_SINISTER_TURN.mission_name, "Southwest Preserver", SC2WOL_LOC_ID_OFFSET + 2308, LocationType.EXTRA,
            lambda state: logic.protoss_common_unit(state) and logic.protoss_competent_anti_air(state)
        ),
        make_location_data(SC2Mission.A_SINISTER_TURN.mission_name, "East Preserver", SC2WOL_LOC_ID_OFFSET + 2309, LocationType.EXTRA,
            lambda state: logic.protoss_common_unit(state) and logic.protoss_competent_anti_air(state)
        ),
        make_location_data(SC2Mission.ECHOES_OF_THE_FUTURE.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 2400, LocationType.VICTORY,
            lambda state: (
                (
                    adv_tactics
                    and logic.protoss_static_defense(state)
                ) or (
                    logic.protoss_common_unit(state)
                    and logic.protoss_competent_anti_air(state)
                )
            )
        ),
        make_location_data(SC2Mission.ECHOES_OF_THE_FUTURE.mission_name, "Close Obelisk", SC2WOL_LOC_ID_OFFSET + 2401, LocationType.VANILLA),
        make_location_data(SC2Mission.ECHOES_OF_THE_FUTURE.mission_name, "West Obelisk", SC2WOL_LOC_ID_OFFSET + 2402, LocationType.VANILLA,
            lambda state: adv_tactics and logic.protoss_static_defense(state) or logic.protoss_common_unit(state)
        ),
        make_location_data(SC2Mission.ECHOES_OF_THE_FUTURE.mission_name, "Base", SC2WOL_LOC_ID_OFFSET + 2403, LocationType.EXTRA),
        make_location_data(SC2Mission.ECHOES_OF_THE_FUTURE.mission_name, "Southwest Tendril", SC2WOL_LOC_ID_OFFSET + 2404, LocationType.EXTRA),
        make_location_data(SC2Mission.ECHOES_OF_THE_FUTURE.mission_name, "Southeast Tendril", SC2WOL_LOC_ID_OFFSET + 2405, LocationType.EXTRA,
            lambda state: adv_tactics and logic.protoss_static_defense(state) or logic.protoss_common_unit(state)
        ),
        make_location_data(SC2Mission.ECHOES_OF_THE_FUTURE.mission_name, "Northeast Tendril", SC2WOL_LOC_ID_OFFSET + 2406, LocationType.EXTRA,
            lambda state: adv_tactics and logic.protoss_static_defense(state) or logic.protoss_common_unit(state)
        ),
        make_location_data(SC2Mission.ECHOES_OF_THE_FUTURE.mission_name, "Northwest Tendril", SC2WOL_LOC_ID_OFFSET + 2407, LocationType.EXTRA,
            lambda state: adv_tactics and logic.protoss_static_defense(state) or logic.protoss_common_unit(state)
        ),
        make_location_data(SC2Mission.IN_UTTER_DARKNESS.mission_name, "Defeat", SC2WOL_LOC_ID_OFFSET + 2500, LocationType.VICTORY),
        make_location_data(SC2Mission.IN_UTTER_DARKNESS.mission_name, "Protoss Archive", SC2WOL_LOC_ID_OFFSET + 2501, LocationType.VANILLA,
            logic.last_stand_requirement
        ),
        make_location_data(SC2Mission.IN_UTTER_DARKNESS.mission_name, "Kills", SC2WOL_LOC_ID_OFFSET + 2502, LocationType.VANILLA,
            logic.last_stand_requirement
        ),
        make_location_data(SC2Mission.IN_UTTER_DARKNESS.mission_name, "Urun", SC2WOL_LOC_ID_OFFSET + 2503, LocationType.EXTRA),
        make_location_data(SC2Mission.IN_UTTER_DARKNESS.mission_name, "Mohandar", SC2WOL_LOC_ID_OFFSET + 2504, LocationType.EXTRA,
            logic.last_stand_requirement
        ),
        make_location_data(SC2Mission.IN_UTTER_DARKNESS.mission_name, "Selendis", SC2WOL_LOC_ID_OFFSET + 2505, LocationType.EXTRA,
            logic.last_stand_requirement
        ),
        make_location_data(SC2Mission.IN_UTTER_DARKNESS.mission_name, "Artanis", SC2WOL_LOC_ID_OFFSET + 2506, LocationType.EXTRA,
            logic.last_stand_requirement
        ),
        make_location_data(SC2Mission.GATES_OF_HELL.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 2600, LocationType.VICTORY,
            logic.terran_gates_of_hell_requirement
        ),
        make_location_data(SC2Mission.GATES_OF_HELL.mission_name, "Large Army", SC2WOL_LOC_ID_OFFSET + 2601, LocationType.VANILLA,
            logic.terran_gates_of_hell_requirement
        ),
        make_location_data(SC2Mission.GATES_OF_HELL.mission_name, "2 Drop Pods", SC2WOL_LOC_ID_OFFSET + 2602, LocationType.VANILLA,
            logic.terran_gates_of_hell_requirement
        ),
        make_location_data(SC2Mission.GATES_OF_HELL.mission_name, "4 Drop Pods", SC2WOL_LOC_ID_OFFSET + 2603, LocationType.VANILLA,
            logic.terran_gates_of_hell_requirement
        ),
        make_location_data(SC2Mission.GATES_OF_HELL.mission_name, "6 Drop Pods", SC2WOL_LOC_ID_OFFSET + 2604, LocationType.EXTRA,
            logic.terran_gates_of_hell_requirement
        ),
        make_location_data(SC2Mission.GATES_OF_HELL.mission_name, "8 Drop Pods", SC2WOL_LOC_ID_OFFSET + 2605, LocationType.CHALLENGE,
            logic.terran_gates_of_hell_requirement
        ),
        make_location_data(SC2Mission.GATES_OF_HELL.mission_name, "Southwest Spore Cannon", SC2WOL_LOC_ID_OFFSET + 2606, LocationType.EXTRA,
            logic.terran_gates_of_hell_requirement
        ),
        make_location_data(SC2Mission.GATES_OF_HELL.mission_name, "Northwest Spore Cannon", SC2WOL_LOC_ID_OFFSET + 2607, LocationType.EXTRA,
            logic.terran_gates_of_hell_requirement
        ),
        make_location_data(SC2Mission.GATES_OF_HELL.mission_name, "Northeast Spore Cannon", SC2WOL_LOC_ID_OFFSET + 2608, LocationType.EXTRA,
            logic.terran_gates_of_hell_requirement
        ),
        make_location_data(SC2Mission.GATES_OF_HELL.mission_name, "East Spore Cannon", SC2WOL_LOC_ID_OFFSET + 2609, LocationType.EXTRA,
            logic.terran_gates_of_hell_requirement
        ),
        make_location_data(SC2Mission.GATES_OF_HELL.mission_name, "Southeast Spore Cannon", SC2WOL_LOC_ID_OFFSET + 2610, LocationType.EXTRA,
            logic.terran_gates_of_hell_requirement
        ),
        make_location_data(SC2Mission.GATES_OF_HELL.mission_name, "Expansion Spore Cannon", SC2WOL_LOC_ID_OFFSET + 2611, LocationType.EXTRA,
            logic.terran_gates_of_hell_requirement
        ),
        make_location_data(SC2Mission.BELLY_OF_THE_BEAST.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 2700, LocationType.VICTORY),
        make_location_data(SC2Mission.BELLY_OF_THE_BEAST.mission_name, "First Charge", SC2WOL_LOC_ID_OFFSET + 2701, LocationType.EXTRA),
        make_location_data(SC2Mission.BELLY_OF_THE_BEAST.mission_name, "Second Charge", SC2WOL_LOC_ID_OFFSET + 2702, LocationType.EXTRA),
        make_location_data(SC2Mission.BELLY_OF_THE_BEAST.mission_name, "Third Charge", SC2WOL_LOC_ID_OFFSET + 2703, LocationType.EXTRA),
        make_location_data(SC2Mission.BELLY_OF_THE_BEAST.mission_name, "First Group Rescued", SC2WOL_LOC_ID_OFFSET + 2704, LocationType.VANILLA),
        make_location_data(SC2Mission.BELLY_OF_THE_BEAST.mission_name, "Second Group Rescued", SC2WOL_LOC_ID_OFFSET + 2705, LocationType.VANILLA),
        make_location_data(SC2Mission.BELLY_OF_THE_BEAST.mission_name, "Third Group Rescued", SC2WOL_LOC_ID_OFFSET + 2706, LocationType.VANILLA),
        make_location_data(SC2Mission.SHATTER_THE_SKY.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 2800, LocationType.VICTORY,
            logic.terran_competent_comp
        ),
        make_location_data(SC2Mission.SHATTER_THE_SKY.mission_name, "Close Coolant Tower", SC2WOL_LOC_ID_OFFSET + 2801, LocationType.VANILLA,
            logic.terran_competent_comp
        ),
        make_location_data(SC2Mission.SHATTER_THE_SKY.mission_name, "Northwest Coolant Tower", SC2WOL_LOC_ID_OFFSET + 2802, LocationType.VANILLA,
            logic.terran_competent_comp
        ),
        make_location_data(SC2Mission.SHATTER_THE_SKY.mission_name, "Southeast Coolant Tower", SC2WOL_LOC_ID_OFFSET + 2803, LocationType.VANILLA,
            logic.terran_competent_comp
        ),
        make_location_data(SC2Mission.SHATTER_THE_SKY.mission_name, "Southwest Coolant Tower", SC2WOL_LOC_ID_OFFSET + 2804, LocationType.VANILLA,
            logic.terran_competent_comp
        ),
        make_location_data(SC2Mission.SHATTER_THE_SKY.mission_name, "Leviathan", SC2WOL_LOC_ID_OFFSET + 2805, LocationType.VANILLA,
            logic.terran_competent_comp
        ),
        make_location_data(SC2Mission.SHATTER_THE_SKY.mission_name, "East Hatchery", SC2WOL_LOC_ID_OFFSET + 2806, LocationType.EXTRA,
            logic.terran_competent_comp
        ),
        make_location_data(SC2Mission.SHATTER_THE_SKY.mission_name, "North Hatchery", SC2WOL_LOC_ID_OFFSET + 2807, LocationType.EXTRA,
            logic.terran_competent_comp
        ),
        make_location_data(SC2Mission.SHATTER_THE_SKY.mission_name, "Mid Hatchery", SC2WOL_LOC_ID_OFFSET + 2808, LocationType.EXTRA,
            logic.terran_competent_comp
        ),
        make_location_data(SC2Mission.ALL_IN.mission_name, "Victory", SC2WOL_LOC_ID_OFFSET + 2900, LocationType.VICTORY,
            logic.all_in_requirement
        ),
        make_location_data(SC2Mission.ALL_IN.mission_name, "First Kerrigan Attack", SC2WOL_LOC_ID_OFFSET + 2901, LocationType.EXTRA,
            logic.all_in_requirement
        ),
        make_location_data(SC2Mission.ALL_IN.mission_name, "Second Kerrigan Attack", SC2WOL_LOC_ID_OFFSET + 2902, LocationType.EXTRA,
            logic.all_in_requirement
        ),
        make_location_data(SC2Mission.ALL_IN.mission_name, "Third Kerrigan Attack", SC2WOL_LOC_ID_OFFSET + 2903, LocationType.EXTRA,
            logic.all_in_requirement
        ),
        make_location_data(SC2Mission.ALL_IN.mission_name, "Fourth Kerrigan Attack", SC2WOL_LOC_ID_OFFSET + 2904, LocationType.EXTRA,
            logic.all_in_requirement
        ),
        make_location_data(SC2Mission.ALL_IN.mission_name, "Fifth Kerrigan Attack", SC2WOL_LOC_ID_OFFSET + 2905, LocationType.EXTRA,
            logic.all_in_requirement
        ),

        # HotS
        make_location_data(SC2Mission.LAB_RAT.mission_name, "Victory", SC2HOTS_LOC_ID_OFFSET + 100, LocationType.VICTORY,
            logic.zerg_common_unit
        ),
        make_location_data(SC2Mission.LAB_RAT.mission_name, "Gather Minerals", SC2HOTS_LOC_ID_OFFSET + 101, LocationType.VANILLA),
        make_location_data(SC2Mission.LAB_RAT.mission_name, "South Zergling Group", SC2HOTS_LOC_ID_OFFSET + 102, LocationType.VANILLA,
            lambda state: adv_tactics or logic.zerg_common_unit(state)
        ),
        make_location_data(SC2Mission.LAB_RAT.mission_name, "East Zergling Group", SC2HOTS_LOC_ID_OFFSET + 103, LocationType.VANILLA,
            lambda state: adv_tactics or logic.zerg_common_unit(state)
        ),
        make_location_data(SC2Mission.LAB_RAT.mission_name, "West Zergling Group", SC2HOTS_LOC_ID_OFFSET + 104, LocationType.VANILLA,
            lambda state: adv_tactics or logic.zerg_common_unit(state)
        ),
        make_location_data(SC2Mission.LAB_RAT.mission_name, "Hatchery", SC2HOTS_LOC_ID_OFFSET + 105, LocationType.EXTRA),
        make_location_data(SC2Mission.LAB_RAT.mission_name, "Overlord", SC2HOTS_LOC_ID_OFFSET + 106, LocationType.EXTRA),
        make_location_data(SC2Mission.LAB_RAT.mission_name, "Gas Turrets", SC2HOTS_LOC_ID_OFFSET + 107, LocationType.EXTRA,
            lambda state: adv_tactics or logic.zerg_common_unit(state)
        ),
        make_location_data(SC2Mission.LAB_RAT.mission_name, "Win In Under 10 Minutes", SC2HOTS_LOC_ID_OFFSET + 108, LocationType.SPEEDRUN,
            lambda state: adv_tactics or logic.zerg_common_unit(state)
        ),
        make_location_data(SC2Mission.BACK_IN_THE_SADDLE.mission_name, "Victory", SC2HOTS_LOC_ID_OFFSET + 200, LocationType.VICTORY,
            lambda state: logic.basic_kerrigan(state) or kerriganless or logic.story_tech_granted
        ),
        make_location_data(SC2Mission.BACK_IN_THE_SADDLE.mission_name, "Defend the Tram", SC2HOTS_LOC_ID_OFFSET + 201, LocationType.EXTRA,
            lambda state: logic.basic_kerrigan(state) or kerriganless or logic.story_tech_granted
        ),
        make_location_data(SC2Mission.BACK_IN_THE_SADDLE.mission_name, "Kinetic Blast", SC2HOTS_LOC_ID_OFFSET + 202, LocationType.VANILLA),
        make_location_data(SC2Mission.BACK_IN_THE_SADDLE.mission_name, "Crushing Grip", SC2HOTS_LOC_ID_OFFSET + 203, LocationType.VANILLA),
        make_location_data(SC2Mission.BACK_IN_THE_SADDLE.mission_name, "Reach the Sublevel", SC2HOTS_LOC_ID_OFFSET + 204, LocationType.EXTRA),
        make_location_data(SC2Mission.BACK_IN_THE_SADDLE.mission_name, "Door Section Cleared", SC2HOTS_LOC_ID_OFFSET + 205, LocationType.EXTRA,
            lambda state: logic.basic_kerrigan(state) or kerriganless or logic.story_tech_granted
        ),
        make_location_data(SC2Mission.RENDEZVOUS.mission_name, "Victory", SC2HOTS_LOC_ID_OFFSET + 300, LocationType.VICTORY,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state))
        ),
        make_location_data(SC2Mission.RENDEZVOUS.mission_name, "Right Queen", SC2HOTS_LOC_ID_OFFSET + 301, LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state))
        ),
        make_location_data(SC2Mission.RENDEZVOUS.mission_name, "Center Queen", SC2HOTS_LOC_ID_OFFSET + 302, LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state))
        ),
        make_location_data(SC2Mission.RENDEZVOUS.mission_name, "Left Queen", SC2HOTS_LOC_ID_OFFSET + 303, LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state))
        ),
        make_location_data(SC2Mission.RENDEZVOUS.mission_name, "Hold Out Finished", SC2HOTS_LOC_ID_OFFSET + 304, LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state))
        ),
        make_location_data(SC2Mission.RENDEZVOUS.mission_name, "Kill All Before Reinforcements", SC2HOTS_LOC_ID_OFFSET + 305, LocationType.SPEEDRUN,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_competent_anti_air(state)
                and (logic.basic_kerrigan(state) or kerriganless))
        ),
        make_location_data(SC2Mission.HARVEST_OF_SCREAMS.mission_name, "Victory", SC2HOTS_LOC_ID_OFFSET + 400, LocationType.VICTORY,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state))
        ),
        make_location_data(SC2Mission.HARVEST_OF_SCREAMS.mission_name, "First Ursadon Matriarch", SC2HOTS_LOC_ID_OFFSET + 401, LocationType.VANILLA),
        make_location_data(SC2Mission.HARVEST_OF_SCREAMS.mission_name, "North Ursadon Matriarch", SC2HOTS_LOC_ID_OFFSET + 402, LocationType.VANILLA,
            logic.zerg_common_unit
        ),
        make_location_data(SC2Mission.HARVEST_OF_SCREAMS.mission_name, "West Ursadon Matriarch", SC2HOTS_LOC_ID_OFFSET + 403, LocationType.VANILLA,
            logic.zerg_common_unit
        ),
        make_location_data(SC2Mission.HARVEST_OF_SCREAMS.mission_name, "Lost Brood", SC2HOTS_LOC_ID_OFFSET + 404, LocationType.EXTRA),
        make_location_data(SC2Mission.HARVEST_OF_SCREAMS.mission_name, "Northeast Psi-link Spire", SC2HOTS_LOC_ID_OFFSET + 405, LocationType.EXTRA,
            logic.zerg_common_unit
        ),
        make_location_data(SC2Mission.HARVEST_OF_SCREAMS.mission_name, "Northwest Psi-link Spire", SC2HOTS_LOC_ID_OFFSET + 406, LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state))
        ),
        make_location_data(SC2Mission.HARVEST_OF_SCREAMS.mission_name, "Southwest Psi-link Spire", SC2HOTS_LOC_ID_OFFSET + 407, LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state))
        ),
        make_location_data(SC2Mission.HARVEST_OF_SCREAMS.mission_name, "Nafash", SC2HOTS_LOC_ID_OFFSET + 408, LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state))
        ),
        make_location_data(SC2Mission.HARVEST_OF_SCREAMS.mission_name, "20 Unfrozen Structures", SC2HOTS_LOC_ID_OFFSET + 409, LocationType.CHALLENGE,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state))
        ),
        make_location_data(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "Victory", SC2HOTS_LOC_ID_OFFSET + 500, LocationType.VICTORY,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state))
        ),
        make_location_data(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "East Stasis Chamber", SC2HOTS_LOC_ID_OFFSET + 501, LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state))
        ),
        make_location_data(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "Center Stasis Chamber", SC2HOTS_LOC_ID_OFFSET + 502, LocationType.VANILLA,
            lambda state: logic.zerg_common_unit(state) or adv_tactics
        ),
        make_location_data(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "West Stasis Chamber", SC2HOTS_LOC_ID_OFFSET + 503, LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state))
        ),
        make_location_data(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "Destroy 4 Shuttles", SC2HOTS_LOC_ID_OFFSET + 504, LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state))
        ),
        make_location_data(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "Frozen Expansion", SC2HOTS_LOC_ID_OFFSET + 505, LocationType.EXTRA,
            logic.zerg_common_unit
        ),
        make_location_data(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "Southwest Frozen Zerg", SC2HOTS_LOC_ID_OFFSET + 506, LocationType.EXTRA),
        make_location_data(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "Southeast Frozen Zerg", SC2HOTS_LOC_ID_OFFSET + 507, LocationType.EXTRA,
            lambda state: logic.zerg_common_unit(state) or adv_tactics
        ),
        make_location_data(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "West Frozen Zerg", SC2HOTS_LOC_ID_OFFSET + 508, LocationType.EXTRA,
            logic.zerg_common_unit_basic_aa
        ),
        make_location_data(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "East Frozen Zerg", SC2HOTS_LOC_ID_OFFSET + 509, LocationType.EXTRA,
            logic.zerg_common_unit_competent_aa
        ),
        make_location_data(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "West Launch Bay", SC2HOTS_LOC_ID_OFFSET + 510, LocationType.CHALLENGE,
            logic.zerg_competent_comp_competent_aa
        ),
        make_location_data(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "Center Launch Bay", SC2HOTS_LOC_ID_OFFSET + 511, LocationType.CHALLENGE,
            logic.zerg_competent_comp_competent_aa
        ),
        make_location_data(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "East Launch Bay", SC2HOTS_LOC_ID_OFFSET + 512, LocationType.CHALLENGE,
            logic.zerg_competent_comp_competent_aa
        ),
        make_location_data(SC2Mission.ENEMY_WITHIN.mission_name, "Victory", SC2HOTS_LOC_ID_OFFSET + 600, LocationType.VICTORY,
            lambda state: (
                logic.zerg_pass_vents(state)
                and (logic.story_tech_granted
                    or state.has_any({
                        item_names.ZERGLING_RAPTOR_STRAIN,
                        item_names.ROACH,
                        item_names.HYDRALISK,
                        item_names.INFESTOR
                    }, player)))
        ),
        make_location_data(SC2Mission.ENEMY_WITHIN.mission_name, "Infest Giant Ursadon", SC2HOTS_LOC_ID_OFFSET + 601, LocationType.VANILLA,
            logic.zerg_pass_vents
        ),
        make_location_data(SC2Mission.ENEMY_WITHIN.mission_name, "First Niadra Evolution", SC2HOTS_LOC_ID_OFFSET + 602, LocationType.VANILLA,
            logic.zerg_pass_vents
        ),
        make_location_data(SC2Mission.ENEMY_WITHIN.mission_name, "Second Niadra Evolution", SC2HOTS_LOC_ID_OFFSET + 603, LocationType.VANILLA,
            logic.zerg_pass_vents
        ),
        make_location_data(SC2Mission.ENEMY_WITHIN.mission_name, "Third Niadra Evolution", SC2HOTS_LOC_ID_OFFSET + 604, LocationType.VANILLA,
            logic.zerg_pass_vents
        ),
        make_location_data(SC2Mission.ENEMY_WITHIN.mission_name, "Warp Drive", SC2HOTS_LOC_ID_OFFSET + 605, LocationType.EXTRA,
            logic.zerg_pass_vents
        ),
        make_location_data(SC2Mission.ENEMY_WITHIN.mission_name, "Stasis Quadrant", SC2HOTS_LOC_ID_OFFSET + 606, LocationType.EXTRA,
            logic.zerg_pass_vents
        ),
        make_location_data(SC2Mission.DOMINATION.mission_name, "Victory", SC2HOTS_LOC_ID_OFFSET + 700, LocationType.VICTORY,
            logic.zerg_common_unit_basic_aa
        ),
        make_location_data(SC2Mission.DOMINATION.mission_name, "Center Infested Command Center", SC2HOTS_LOC_ID_OFFSET + 701, LocationType.VANILLA,
            logic.zerg_common_unit
        ),
        make_location_data(SC2Mission.DOMINATION.mission_name, "North Infested Command Center", SC2HOTS_LOC_ID_OFFSET + 702, LocationType.VANILLA,
            logic.zerg_common_unit
        ),
        make_location_data(SC2Mission.DOMINATION.mission_name, "Repel Zagara", SC2HOTS_LOC_ID_OFFSET + 703, LocationType.EXTRA),
        make_location_data(SC2Mission.DOMINATION.mission_name, "Close Baneling Nest", SC2HOTS_LOC_ID_OFFSET + 704, LocationType.EXTRA),
        make_location_data(SC2Mission.DOMINATION.mission_name, "South Baneling Nest", SC2HOTS_LOC_ID_OFFSET + 705, LocationType.EXTRA,
            lambda state: adv_tactics or logic.zerg_common_unit(state)
        ),
        make_location_data(SC2Mission.DOMINATION.mission_name, "Southwest Baneling Nest", SC2HOTS_LOC_ID_OFFSET + 706, LocationType.EXTRA,
            logic.zerg_common_unit
        ),
        make_location_data(SC2Mission.DOMINATION.mission_name, "Southeast Baneling Nest", SC2HOTS_LOC_ID_OFFSET + 707, LocationType.EXTRA,
            logic.zerg_common_unit_basic_aa
        ),
        make_location_data(SC2Mission.DOMINATION.mission_name, "North Baneling Nest", SC2HOTS_LOC_ID_OFFSET + 708, LocationType.EXTRA,
            logic.zerg_common_unit
        ),
        make_location_data(SC2Mission.DOMINATION.mission_name, "Northeast Baneling Nest", SC2HOTS_LOC_ID_OFFSET + 709, LocationType.EXTRA,
            logic.zerg_common_unit
        ),
        make_location_data(SC2Mission.DOMINATION.mission_name, "Win Without 100 Eggs", SC2HOTS_LOC_ID_OFFSET + 710, LocationType.CHALLENGE,
            logic.zerg_competent_comp_competent_aa
        ),
        make_location_data(SC2Mission.FIRE_IN_THE_SKY.mission_name, "Victory", SC2HOTS_LOC_ID_OFFSET + 800, LocationType.VICTORY,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_basic_anti_air(state)
                and logic.spread_creep(state))
        ),
        make_location_data(SC2Mission.FIRE_IN_THE_SKY.mission_name, "West Biomass", SC2HOTS_LOC_ID_OFFSET + 801, LocationType.VANILLA),
        make_location_data(SC2Mission.FIRE_IN_THE_SKY.mission_name, "North Biomass", SC2HOTS_LOC_ID_OFFSET + 802, LocationType.VANILLA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_basic_anti_air(state)
                and logic.spread_creep(state))
        ),
        make_location_data(SC2Mission.FIRE_IN_THE_SKY.mission_name, "South Biomass", SC2HOTS_LOC_ID_OFFSET + 803, LocationType.VANILLA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_basic_anti_air(state)
                and logic.spread_creep(state))
        ),
        make_location_data(SC2Mission.FIRE_IN_THE_SKY.mission_name, "Destroy 3 Gorgons", SC2HOTS_LOC_ID_OFFSET + 804, LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_basic_anti_air(state)
                and logic.spread_creep(state))
        ),
        make_location_data(SC2Mission.FIRE_IN_THE_SKY.mission_name, "Close Zerg Rescue", SC2HOTS_LOC_ID_OFFSET + 805, LocationType.EXTRA),
        make_location_data(SC2Mission.FIRE_IN_THE_SKY.mission_name, "South Zerg Rescue", SC2HOTS_LOC_ID_OFFSET + 806, LocationType.EXTRA,
            logic.zerg_common_unit
        ),
        make_location_data(SC2Mission.FIRE_IN_THE_SKY.mission_name, "North Zerg Rescue", SC2HOTS_LOC_ID_OFFSET + 807, LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_basic_anti_air(state)
                and logic.spread_creep(state))
        ),
        make_location_data(SC2Mission.FIRE_IN_THE_SKY.mission_name, "West Queen Rescue", SC2HOTS_LOC_ID_OFFSET + 808, LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_basic_anti_air(state)
                and logic.spread_creep(state))
        ),
        make_location_data(SC2Mission.FIRE_IN_THE_SKY.mission_name, "East Queen Rescue", SC2HOTS_LOC_ID_OFFSET + 809, LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_basic_anti_air(state)
                and logic.spread_creep(state))
        ),
        make_location_data(SC2Mission.FIRE_IN_THE_SKY.mission_name, "South Orbital Command Center", SC2HOTS_LOC_ID_OFFSET + 810, LocationType.CHALLENGE,
            logic.zerg_competent_comp
        ),
        make_location_data(SC2Mission.FIRE_IN_THE_SKY.mission_name, "Northwest Orbital Command Center", SC2HOTS_LOC_ID_OFFSET + 811, LocationType.CHALLENGE,
            logic.zerg_competent_comp
        ),
        make_location_data(SC2Mission.FIRE_IN_THE_SKY.mission_name, "Southeast Orbital Command Center", SC2HOTS_LOC_ID_OFFSET + 812, LocationType.CHALLENGE,
            logic.zerg_competent_comp
        ),
        make_location_data(SC2Mission.OLD_SOLDIERS.mission_name, "Victory", SC2HOTS_LOC_ID_OFFSET + 900, LocationType.VICTORY,
            logic.zerg_competent_comp_basic_aa
        ),
        make_location_data(SC2Mission.OLD_SOLDIERS.mission_name, "East Science Lab", SC2HOTS_LOC_ID_OFFSET + 901, LocationType.VANILLA,
            logic.zerg_competent_comp_basic_aa
        ),
        make_location_data(SC2Mission.OLD_SOLDIERS.mission_name, "North Science Lab", SC2HOTS_LOC_ID_OFFSET + 902, LocationType.VANILLA,
            logic.zerg_competent_comp_basic_aa
        ),
        make_location_data(SC2Mission.OLD_SOLDIERS.mission_name, "Get Nuked", SC2HOTS_LOC_ID_OFFSET + 903, LocationType.EXTRA),
        make_location_data(SC2Mission.OLD_SOLDIERS.mission_name, "Entrance Gate", SC2HOTS_LOC_ID_OFFSET + 904, LocationType.EXTRA),
        make_location_data(SC2Mission.OLD_SOLDIERS.mission_name, "Citadel Gate", SC2HOTS_LOC_ID_OFFSET + 905, LocationType.EXTRA,
            logic.zerg_competent_comp_basic_aa
        ),
        make_location_data(SC2Mission.OLD_SOLDIERS.mission_name, "South Expansion", SC2HOTS_LOC_ID_OFFSET + 906, LocationType.EXTRA),
        make_location_data(SC2Mission.OLD_SOLDIERS.mission_name, "Rich Mineral Expansion", SC2HOTS_LOC_ID_OFFSET + 907, LocationType.EXTRA,
            logic.zerg_competent_comp_basic_aa
        ),
        make_location_data(SC2Mission.WAKING_THE_ANCIENT.mission_name, "Victory", SC2HOTS_LOC_ID_OFFSET + 1000, LocationType.VICTORY,
            logic.zerg_competent_comp_basic_aa
        ),
        make_location_data(SC2Mission.WAKING_THE_ANCIENT.mission_name, "Center Essence Pool", SC2HOTS_LOC_ID_OFFSET + 1001, LocationType.VANILLA),
        make_location_data(SC2Mission.WAKING_THE_ANCIENT.mission_name, "East Essence Pool", SC2HOTS_LOC_ID_OFFSET + 1002, LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and (adv_tactics
                    and logic.zerg_basic_anti_air(state)
                    or logic.zerg_competent_anti_air(state)))
        ),
        make_location_data(SC2Mission.WAKING_THE_ANCIENT.mission_name, "South Essence Pool", SC2HOTS_LOC_ID_OFFSET + 1003, LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and (adv_tactics
                    and logic.zerg_basic_anti_air(state)
                    or logic.zerg_competent_anti_air(state)))
        ),
        make_location_data(SC2Mission.WAKING_THE_ANCIENT.mission_name, "Finish Feeding", SC2HOTS_LOC_ID_OFFSET + 1004, LocationType.EXTRA,
            logic.zerg_common_unit_competent_aa
        ),
        make_location_data(SC2Mission.WAKING_THE_ANCIENT.mission_name, "South Proxy Primal Hive", SC2HOTS_LOC_ID_OFFSET + 1005, LocationType.CHALLENGE,
            logic.zerg_common_unit_competent_aa
        ),
        make_location_data(SC2Mission.WAKING_THE_ANCIENT.mission_name, "East Proxy Primal Hive", SC2HOTS_LOC_ID_OFFSET + 1006, LocationType.CHALLENGE,
            logic.zerg_common_unit_competent_aa
        ),
        make_location_data(SC2Mission.WAKING_THE_ANCIENT.mission_name, "South Main Primal Hive", SC2HOTS_LOC_ID_OFFSET + 1007, LocationType.CHALLENGE,
            logic.zerg_common_unit_competent_aa
        ),
        make_location_data(SC2Mission.WAKING_THE_ANCIENT.mission_name, "East Main Primal Hive", SC2HOTS_LOC_ID_OFFSET + 1008, LocationType.CHALLENGE,
            logic.zerg_common_unit_competent_aa
        ),
        make_location_data(SC2Mission.WAKING_THE_ANCIENT.mission_name, "Flawless", SC2HOTS_LOC_ID_OFFSET + 1009, LocationType.CHALLENGE,
            logic.zerg_common_unit_competent_aa,
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(SC2Mission.THE_CRUCIBLE.mission_name, "Victory", SC2HOTS_LOC_ID_OFFSET + 1100, LocationType.VICTORY,
            lambda state: (
                logic.zerg_competent_defense(state)
                and logic.zerg_competent_anti_air(state))
        ),
        make_location_data(SC2Mission.THE_CRUCIBLE.mission_name, "Tyrannozor", SC2HOTS_LOC_ID_OFFSET + 1101, LocationType.VANILLA,
            lambda state: (
                logic.zerg_competent_defense(state)
                and logic.zerg_competent_anti_air(state))
        ),
        make_location_data(SC2Mission.THE_CRUCIBLE.mission_name, "Reach the Pool", SC2HOTS_LOC_ID_OFFSET + 1102, LocationType.VANILLA),
        make_location_data(SC2Mission.THE_CRUCIBLE.mission_name, "15 Minutes Remaining", SC2HOTS_LOC_ID_OFFSET + 1103, LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_defense(state)
                and logic.zerg_competent_anti_air(state))
        ),
        make_location_data(SC2Mission.THE_CRUCIBLE.mission_name, "5 Minutes Remaining", SC2HOTS_LOC_ID_OFFSET + 1104, LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_defense(state)
                and logic.zerg_competent_anti_air(state))
        ),
        make_location_data(SC2Mission.THE_CRUCIBLE.mission_name, "Pincer Attack", SC2HOTS_LOC_ID_OFFSET + 1105, LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_defense(state)
                and logic.zerg_competent_anti_air(state))
        ),
        make_location_data(SC2Mission.THE_CRUCIBLE.mission_name, "Yagdra Claims Brakk's Pack", SC2HOTS_LOC_ID_OFFSET + 1106, LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_defense(state)
                and logic.zerg_competent_anti_air(state))
        ),
        make_location_data(SC2Mission.SUPREME.mission_name, "Victory", SC2HOTS_LOC_ID_OFFSET + 1200, LocationType.VICTORY,
            logic.supreme_requirement
        ),
        make_location_data(SC2Mission.SUPREME.mission_name, "First Relic", SC2HOTS_LOC_ID_OFFSET + 1201, LocationType.VANILLA,
            logic.supreme_requirement
        ),
        make_location_data(SC2Mission.SUPREME.mission_name, "Second Relic", SC2HOTS_LOC_ID_OFFSET + 1202, LocationType.VANILLA,
            logic.supreme_requirement
        ),
        make_location_data(SC2Mission.SUPREME.mission_name, "Third Relic", SC2HOTS_LOC_ID_OFFSET + 1203, LocationType.VANILLA,
            logic.supreme_requirement
        ),
        make_location_data(SC2Mission.SUPREME.mission_name, "Fourth Relic", SC2HOTS_LOC_ID_OFFSET + 1204, LocationType.VANILLA,
            logic.supreme_requirement
        ),
        make_location_data(SC2Mission.SUPREME.mission_name, "Yagdra", SC2HOTS_LOC_ID_OFFSET + 1205, LocationType.EXTRA,
            logic.supreme_requirement
        ),
        make_location_data(SC2Mission.SUPREME.mission_name, "Kraith", SC2HOTS_LOC_ID_OFFSET + 1206, LocationType.EXTRA,
            logic.supreme_requirement
        ),
        make_location_data(SC2Mission.SUPREME.mission_name, "Slivan", SC2HOTS_LOC_ID_OFFSET + 1207, LocationType.EXTRA,
            logic.supreme_requirement
        ),
        make_location_data(SC2Mission.INFESTED.mission_name, "Victory", SC2HOTS_LOC_ID_OFFSET + 1300, LocationType.VICTORY,
            lambda state: (
                logic.zerg_common_unit(state)
                and (
                    (logic.zerg_competent_anti_air(state) and state.has(item_names.INFESTOR, player))
                    or (adv_tactics and logic.zerg_basic_anti_air(state))
                ))
        ),
        make_location_data(SC2Mission.INFESTED.mission_name, "East Science Facility", SC2HOTS_LOC_ID_OFFSET + 1301, LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state)
                and logic.spread_creep(state))
        ),
        make_location_data(SC2Mission.INFESTED.mission_name, "Center Science Facility", SC2HOTS_LOC_ID_OFFSET + 1302, LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state)
                and logic.spread_creep(state))
        ),
        make_location_data(SC2Mission.INFESTED.mission_name, "West Science Facility", SC2HOTS_LOC_ID_OFFSET + 1303, LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state)
                and logic.spread_creep(state))
        ),
        make_location_data(SC2Mission.INFESTED.mission_name, "First Intro Garrison", SC2HOTS_LOC_ID_OFFSET + 1304, LocationType.EXTRA),
        make_location_data(SC2Mission.INFESTED.mission_name, "Second Intro Garrison", SC2HOTS_LOC_ID_OFFSET + 1305, LocationType.EXTRA),
        make_location_data(SC2Mission.INFESTED.mission_name, "Base Garrison", SC2HOTS_LOC_ID_OFFSET + 1306, LocationType.EXTRA),
        make_location_data(SC2Mission.INFESTED.mission_name, "East Garrison", SC2HOTS_LOC_ID_OFFSET + 1307, LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state)
                and (adv_tactics or state.has(item_names.INFESTOR, player)))
        ),
        make_location_data(SC2Mission.INFESTED.mission_name, "Mid Garrison", SC2HOTS_LOC_ID_OFFSET + 1308, LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state)
                and (adv_tactics or state.has(item_names.INFESTOR, player)))
        ),
        make_location_data(SC2Mission.INFESTED.mission_name, "North Garrison", SC2HOTS_LOC_ID_OFFSET + 1309, LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state)
                and (adv_tactics or state.has(item_names.INFESTOR, player)))
        ),
        make_location_data(SC2Mission.INFESTED.mission_name, "Close Southwest Garrison", SC2HOTS_LOC_ID_OFFSET + 1310, LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state)
                and (adv_tactics or state.has(item_names.INFESTOR, player)))
        ),
        make_location_data(SC2Mission.INFESTED.mission_name, "Far Southwest Garrison", SC2HOTS_LOC_ID_OFFSET + 1311, LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state)
                and (adv_tactics or state.has(item_names.INFESTOR, player)))
        ),
        make_location_data(SC2Mission.HAND_OF_DARKNESS.mission_name, "Victory", SC2HOTS_LOC_ID_OFFSET + 1400, LocationType.VICTORY,
            logic.zerg_competent_comp_basic_aa
        ),
        make_location_data(SC2Mission.HAND_OF_DARKNESS.mission_name, "North Brutalisk", SC2HOTS_LOC_ID_OFFSET + 1401, LocationType.VANILLA,
            logic.zerg_competent_comp_basic_aa
        ),
        make_location_data(SC2Mission.HAND_OF_DARKNESS.mission_name, "South Brutalisk", SC2HOTS_LOC_ID_OFFSET + 1402, LocationType.VANILLA,
            logic.zerg_competent_comp_basic_aa
        ),
        make_location_data(SC2Mission.HAND_OF_DARKNESS.mission_name, "Kill 1 Hybrid", SC2HOTS_LOC_ID_OFFSET + 1403, LocationType.EXTRA,
            logic.zerg_competent_comp_basic_aa
        ),
        make_location_data(SC2Mission.HAND_OF_DARKNESS.mission_name, "Kill 2 Hybrid", SC2HOTS_LOC_ID_OFFSET + 1404, LocationType.EXTRA,
            logic.zerg_competent_comp_basic_aa
        ),
        make_location_data(SC2Mission.HAND_OF_DARKNESS.mission_name, "Kill 3 Hybrid", SC2HOTS_LOC_ID_OFFSET + 1405, LocationType.EXTRA,
            logic.zerg_competent_comp_basic_aa
        ),
        make_location_data(SC2Mission.HAND_OF_DARKNESS.mission_name, "Kill 4 Hybrid", SC2HOTS_LOC_ID_OFFSET + 1406, LocationType.EXTRA,
            logic.zerg_competent_comp_basic_aa
        ),
        make_location_data(SC2Mission.HAND_OF_DARKNESS.mission_name, "Kill 5 Hybrid", SC2HOTS_LOC_ID_OFFSET + 1407, LocationType.EXTRA,
            logic.zerg_competent_comp_basic_aa
        ),
        make_location_data(SC2Mission.HAND_OF_DARKNESS.mission_name, "Kill 6 Hybrid", SC2HOTS_LOC_ID_OFFSET + 1408, LocationType.EXTRA,
            logic.zerg_competent_comp_basic_aa
        ),
        make_location_data(SC2Mission.HAND_OF_DARKNESS.mission_name, "Kill 7 Hybrid", SC2HOTS_LOC_ID_OFFSET + 1409, LocationType.EXTRA,
            logic.zerg_competent_comp_basic_aa
        ),
        make_location_data(SC2Mission.PHANTOMS_OF_THE_VOID.mission_name, "Victory", SC2HOTS_LOC_ID_OFFSET + 1500, LocationType.VICTORY,
            lambda state: (
                logic.zerg_competent_comp(state)
                and (logic.zerg_competent_anti_air(state) or adv_tactics))
        ),
        make_location_data(SC2Mission.PHANTOMS_OF_THE_VOID.mission_name, "Northwest Crystal", SC2HOTS_LOC_ID_OFFSET + 1501, LocationType.VANILLA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and (logic.zerg_competent_anti_air(state) or adv_tactics))
        ),
        make_location_data(SC2Mission.PHANTOMS_OF_THE_VOID.mission_name, "Northeast Crystal", SC2HOTS_LOC_ID_OFFSET + 1502, LocationType.VANILLA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and (logic.zerg_competent_anti_air(state) or adv_tactics))
        ),
        make_location_data(SC2Mission.PHANTOMS_OF_THE_VOID.mission_name, "South Crystal", SC2HOTS_LOC_ID_OFFSET + 1503, LocationType.VANILLA),
        make_location_data(SC2Mission.PHANTOMS_OF_THE_VOID.mission_name, "Base Established", SC2HOTS_LOC_ID_OFFSET + 1504, LocationType.EXTRA),
        make_location_data(SC2Mission.PHANTOMS_OF_THE_VOID.mission_name, "Close Temple", SC2HOTS_LOC_ID_OFFSET + 1505, LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and (logic.zerg_competent_anti_air(state) or adv_tactics))
        ),
        make_location_data(SC2Mission.PHANTOMS_OF_THE_VOID.mission_name, "Mid Temple", SC2HOTS_LOC_ID_OFFSET + 1506, LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and (logic.zerg_competent_anti_air(state) or adv_tactics))
        ),
        make_location_data(SC2Mission.PHANTOMS_OF_THE_VOID.mission_name, "Southeast Temple", SC2HOTS_LOC_ID_OFFSET + 1507, LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and (logic.zerg_competent_anti_air(state) or adv_tactics))
        ),
        make_location_data(SC2Mission.PHANTOMS_OF_THE_VOID.mission_name, "Northeast Temple", SC2HOTS_LOC_ID_OFFSET + 1508, LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and (logic.zerg_competent_anti_air(state) or adv_tactics))
        ),
        make_location_data(SC2Mission.PHANTOMS_OF_THE_VOID.mission_name, "Northwest Temple", SC2HOTS_LOC_ID_OFFSET + 1509, LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and (logic.zerg_competent_anti_air(state) or adv_tactics))
        ),
        make_location_data(SC2Mission.WITH_FRIENDS_LIKE_THESE.mission_name, "Victory", SC2HOTS_LOC_ID_OFFSET + 1600, LocationType.VICTORY),
        make_location_data(SC2Mission.WITH_FRIENDS_LIKE_THESE.mission_name, "Pirate Capital Ship", SC2HOTS_LOC_ID_OFFSET + 1601, LocationType.VANILLA),
        make_location_data(SC2Mission.WITH_FRIENDS_LIKE_THESE.mission_name, "First Mineral Patch", SC2HOTS_LOC_ID_OFFSET + 1602, LocationType.VANILLA),
        make_location_data(SC2Mission.WITH_FRIENDS_LIKE_THESE.mission_name, "Second Mineral Patch", SC2HOTS_LOC_ID_OFFSET + 1603, LocationType.VANILLA),
        make_location_data(SC2Mission.WITH_FRIENDS_LIKE_THESE.mission_name, "Third Mineral Patch", SC2HOTS_LOC_ID_OFFSET + 1604, LocationType.VANILLA),
        make_location_data(SC2Mission.CONVICTION.mission_name, "Victory", SC2HOTS_LOC_ID_OFFSET + 1700, LocationType.VICTORY,
            lambda state: (
                kerriganless
                or (
                    logic.two_kerrigan_actives(state)
                    and (logic.basic_kerrigan(state) or logic.story_tech_granted)
                ))
        ),
        make_location_data(SC2Mission.CONVICTION.mission_name, "First Secret Documents", SC2HOTS_LOC_ID_OFFSET + 1701, LocationType.VANILLA,
            lambda state: logic.two_kerrigan_actives(state) or kerriganless
        ),
        make_location_data(SC2Mission.CONVICTION.mission_name, "Second Secret Documents", SC2HOTS_LOC_ID_OFFSET + 1702, LocationType.VANILLA,
            lambda state: (
                kerriganless
                or (
                    logic.two_kerrigan_actives(state)
                    and (logic.basic_kerrigan(state) or logic.story_tech_granted)
                ))
        ),
        make_location_data(SC2Mission.CONVICTION.mission_name, "Power Coupling", SC2HOTS_LOC_ID_OFFSET + 1703, LocationType.EXTRA,
            lambda state: logic.two_kerrigan_actives(state) or kerriganless
        ),
        make_location_data(SC2Mission.CONVICTION.mission_name, "Door Blasted", SC2HOTS_LOC_ID_OFFSET + 1704, LocationType.EXTRA,
            lambda state: logic.two_kerrigan_actives(state) or kerriganless
        ),
        make_location_data(SC2Mission.PLANETFALL.mission_name, "Victory", SC2HOTS_LOC_ID_OFFSET + 1800, LocationType.VICTORY,
            logic.zerg_competent_comp_competent_aa
        ),
        make_location_data(SC2Mission.PLANETFALL.mission_name, "East Gate", SC2HOTS_LOC_ID_OFFSET + 1801, LocationType.VANILLA,
            logic.zerg_competent_comp_competent_aa
        ),
        make_location_data(SC2Mission.PLANETFALL.mission_name, "Northwest Gate", SC2HOTS_LOC_ID_OFFSET + 1802, LocationType.VANILLA,
            logic.zerg_competent_comp_competent_aa
        ),
        make_location_data(SC2Mission.PLANETFALL.mission_name, "North Gate", SC2HOTS_LOC_ID_OFFSET + 1803, LocationType.VANILLA,
            logic.zerg_competent_comp_competent_aa
        ),
        make_location_data(SC2Mission.PLANETFALL.mission_name, "1 Bile Launcher Deployed", SC2HOTS_LOC_ID_OFFSET + 1804, LocationType.EXTRA,
            logic.zerg_competent_comp_competent_aa
        ),
        make_location_data(SC2Mission.PLANETFALL.mission_name, "2 Bile Launchers Deployed", SC2HOTS_LOC_ID_OFFSET + 1805, LocationType.EXTRA,
            logic.zerg_competent_comp_competent_aa
        ),
        make_location_data(SC2Mission.PLANETFALL.mission_name, "3 Bile Launchers Deployed", SC2HOTS_LOC_ID_OFFSET + 1806, LocationType.EXTRA,
            logic.zerg_competent_comp_competent_aa
        ),
        make_location_data(SC2Mission.PLANETFALL.mission_name, "4 Bile Launchers Deployed", SC2HOTS_LOC_ID_OFFSET + 1807, LocationType.EXTRA,
            logic.zerg_competent_comp_competent_aa
        ),
        make_location_data(SC2Mission.PLANETFALL.mission_name, "5 Bile Launchers Deployed", SC2HOTS_LOC_ID_OFFSET + 1808, LocationType.EXTRA,
            logic.zerg_competent_comp_competent_aa
        ),
        make_location_data(SC2Mission.PLANETFALL.mission_name, "Sons of Korhal", SC2HOTS_LOC_ID_OFFSET + 1809, LocationType.EXTRA,
            logic.zerg_competent_comp_competent_aa
        ),
        make_location_data(SC2Mission.PLANETFALL.mission_name, "Night Wolves", SC2HOTS_LOC_ID_OFFSET + 1810, LocationType.EXTRA,
            logic.zerg_competent_comp_competent_aa
        ),
        make_location_data(SC2Mission.PLANETFALL.mission_name, "West Expansion", SC2HOTS_LOC_ID_OFFSET + 1811, LocationType.EXTRA,
            logic.zerg_competent_comp_competent_aa
        ),
        make_location_data(SC2Mission.PLANETFALL.mission_name, "Mid Expansion", SC2HOTS_LOC_ID_OFFSET + 1812, LocationType.EXTRA,
            logic.zerg_competent_comp_competent_aa
        ),
        make_location_data(SC2Mission.DEATH_FROM_ABOVE.mission_name, "Victory", SC2HOTS_LOC_ID_OFFSET + 1900, LocationType.VICTORY,
            logic.zerg_competent_comp_competent_aa
        ),
        make_location_data(SC2Mission.DEATH_FROM_ABOVE.mission_name, "First Power Link", SC2HOTS_LOC_ID_OFFSET + 1901, LocationType.VANILLA),
        make_location_data(SC2Mission.DEATH_FROM_ABOVE.mission_name, "Second Power Link", SC2HOTS_LOC_ID_OFFSET + 1902, LocationType.VANILLA,
            logic.zerg_competent_comp_competent_aa
        ),
        make_location_data(SC2Mission.DEATH_FROM_ABOVE.mission_name, "Third Power Link", SC2HOTS_LOC_ID_OFFSET + 1903, LocationType.VANILLA,
            logic.zerg_competent_comp_competent_aa
        ),
        make_location_data(SC2Mission.DEATH_FROM_ABOVE.mission_name, "Expansion Command Center", SC2HOTS_LOC_ID_OFFSET + 1904, LocationType.EXTRA,
            logic.zerg_competent_comp_competent_aa
        ),
        make_location_data(SC2Mission.DEATH_FROM_ABOVE.mission_name, "Main Path Command Center", SC2HOTS_LOC_ID_OFFSET + 1905, LocationType.EXTRA,
            logic.zerg_competent_comp_competent_aa
        ),
        make_location_data(SC2Mission.THE_RECKONING.mission_name, "Victory", SC2HOTS_LOC_ID_OFFSET + 2000, LocationType.VICTORY,
            logic.the_reckoning_requirement
        ),
        make_location_data(SC2Mission.THE_RECKONING.mission_name, "South Lane", SC2HOTS_LOC_ID_OFFSET + 2001, LocationType.VANILLA,
            logic.the_reckoning_requirement
        ),
        make_location_data(SC2Mission.THE_RECKONING.mission_name, "North Lane", SC2HOTS_LOC_ID_OFFSET + 2002, LocationType.VANILLA,
            logic.the_reckoning_requirement
        ),
        make_location_data(SC2Mission.THE_RECKONING.mission_name, "East Lane", SC2HOTS_LOC_ID_OFFSET + 2003, LocationType.VANILLA,
            logic.the_reckoning_requirement
        ),
        make_location_data(SC2Mission.THE_RECKONING.mission_name, "Odin", SC2HOTS_LOC_ID_OFFSET + 2004, LocationType.EXTRA,
            logic.the_reckoning_requirement
        ),
        make_location_data(SC2Mission.THE_RECKONING.mission_name, "Trash the Odin Early", SC2HOTS_LOC_ID_OFFSET + 2005,
            LocationType.SPEEDRUN,
            lambda state: (
                logic.the_reckoning_requirement(state)
                and state.has_any({item_names.INFESTOR, item_names.DEFILER}, player)
                and (not logic.take_over_ai_allies or logic.terran_base_trasher(state)))
        ),

        # LotV Prologue
        make_location_data(SC2Mission.DARK_WHISPERS.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 100, LocationType.VICTORY,
            logic.protoss_common_unit_basic_aa
        ),
        make_location_data(SC2Mission.DARK_WHISPERS.mission_name, "First Prisoner Group", SC2LOTV_LOC_ID_OFFSET + 101, LocationType.VANILLA,
            logic.protoss_common_unit_basic_aa
        ),
        make_location_data(SC2Mission.DARK_WHISPERS.mission_name, "Second Prisoner Group", SC2LOTV_LOC_ID_OFFSET + 102, LocationType.VANILLA,
            logic.protoss_common_unit_basic_aa
        ),
        make_location_data(SC2Mission.DARK_WHISPERS.mission_name, "First Pylon", SC2LOTV_LOC_ID_OFFSET + 103, LocationType.VANILLA,
            logic.protoss_common_unit_basic_aa
        ),
        make_location_data(SC2Mission.DARK_WHISPERS.mission_name, "Second Pylon", SC2LOTV_LOC_ID_OFFSET + 104, LocationType.VANILLA,
            logic.protoss_common_unit_basic_aa
        ),
        make_location_data(SC2Mission.GHOSTS_IN_THE_FOG.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 200, LocationType.VICTORY,
            logic.protoss_common_unit_anti_armor_air
        ),
        make_location_data(SC2Mission.GHOSTS_IN_THE_FOG.mission_name, "South Rock Formation", SC2LOTV_LOC_ID_OFFSET + 201, LocationType.VANILLA,
            logic.protoss_common_unit_anti_armor_air
        ),
        make_location_data(SC2Mission.GHOSTS_IN_THE_FOG.mission_name, "West Rock Formation", SC2LOTV_LOC_ID_OFFSET + 202, LocationType.VANILLA,
            logic.protoss_common_unit_anti_armor_air
        ),
        make_location_data(SC2Mission.GHOSTS_IN_THE_FOG.mission_name, "East Rock Formation", SC2LOTV_LOC_ID_OFFSET + 203, LocationType.VANILLA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_anti_armor_anti_air(state)
                and logic.protoss_can_attack_behind_chasm(state))
        ),
        make_location_data(SC2Mission.EVIL_AWOKEN.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 300, LocationType.VICTORY),
        make_location_data(SC2Mission.EVIL_AWOKEN.mission_name, "Temple Investigated", SC2LOTV_LOC_ID_OFFSET + 301, LocationType.EXTRA),
        make_location_data(SC2Mission.EVIL_AWOKEN.mission_name, "Void Catalyst", SC2LOTV_LOC_ID_OFFSET + 302, LocationType.EXTRA),
        make_location_data(SC2Mission.EVIL_AWOKEN.mission_name, "First Particle Cannon", SC2LOTV_LOC_ID_OFFSET + 303, LocationType.VANILLA),
        make_location_data(SC2Mission.EVIL_AWOKEN.mission_name, "Second Particle Cannon", SC2LOTV_LOC_ID_OFFSET + 304, LocationType.VANILLA),
        make_location_data(SC2Mission.EVIL_AWOKEN.mission_name, "Third Particle Cannon", SC2LOTV_LOC_ID_OFFSET + 305, LocationType.VANILLA),


        # LotV
        make_location_data(SC2Mission.FOR_AIUR.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 400, LocationType.VICTORY),
        make_location_data(SC2Mission.FOR_AIUR.mission_name, "Southwest Hive", SC2LOTV_LOC_ID_OFFSET + 401, LocationType.VANILLA),
        make_location_data(SC2Mission.FOR_AIUR.mission_name, "Northwest Hive", SC2LOTV_LOC_ID_OFFSET + 402, LocationType.VANILLA),
        make_location_data(SC2Mission.FOR_AIUR.mission_name, "Northeast Hive", SC2LOTV_LOC_ID_OFFSET + 403, LocationType.VANILLA),
        make_location_data(SC2Mission.FOR_AIUR.mission_name, "East Hive", SC2LOTV_LOC_ID_OFFSET + 404, LocationType.VANILLA),
        make_location_data(SC2Mission.FOR_AIUR.mission_name, "West Conduit", SC2LOTV_LOC_ID_OFFSET + 405, LocationType.EXTRA),
        make_location_data(SC2Mission.FOR_AIUR.mission_name, "Middle Conduit", SC2LOTV_LOC_ID_OFFSET + 406, LocationType.EXTRA),
        make_location_data(SC2Mission.FOR_AIUR.mission_name, "Northeast Conduit", SC2LOTV_LOC_ID_OFFSET + 407, LocationType.EXTRA),
        make_location_data(SC2Mission.THE_GROWING_SHADOW.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 500, LocationType.VICTORY,
            logic.protoss_common_unit_basic_aa
        ),
        make_location_data(SC2Mission.THE_GROWING_SHADOW.mission_name, "Close Pylon", SC2LOTV_LOC_ID_OFFSET + 501, LocationType.VANILLA),
        make_location_data(SC2Mission.THE_GROWING_SHADOW.mission_name, "East Pylon", SC2LOTV_LOC_ID_OFFSET + 502, LocationType.VANILLA,
            logic.protoss_common_unit_basic_aa
        ),
        make_location_data(SC2Mission.THE_GROWING_SHADOW.mission_name, "West Pylon", SC2LOTV_LOC_ID_OFFSET + 503, LocationType.VANILLA,
            logic.protoss_common_unit_basic_aa
        ),
        make_location_data(SC2Mission.THE_GROWING_SHADOW.mission_name, "Nexus", SC2LOTV_LOC_ID_OFFSET + 504, LocationType.EXTRA),
        make_location_data(SC2Mission.THE_GROWING_SHADOW.mission_name, "Templar Base", SC2LOTV_LOC_ID_OFFSET + 505, LocationType.EXTRA,
            logic.protoss_common_unit_basic_aa
        ),
        make_location_data(SC2Mission.THE_SPEAR_OF_ADUN.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 600, LocationType.VICTORY,
            logic.protoss_common_unit_anti_light_air
        ),
        make_location_data(SC2Mission.THE_SPEAR_OF_ADUN.mission_name, "Close Warp Gate", SC2LOTV_LOC_ID_OFFSET + 601, LocationType.VANILLA),
        make_location_data(SC2Mission.THE_SPEAR_OF_ADUN.mission_name, "West Warp Gate", SC2LOTV_LOC_ID_OFFSET + 602, LocationType.VANILLA,
            logic.protoss_common_unit_anti_light_air
        ),
        make_location_data(SC2Mission.THE_SPEAR_OF_ADUN.mission_name, "North Warp Gate", SC2LOTV_LOC_ID_OFFSET + 603, LocationType.VANILLA,
            logic.protoss_common_unit_anti_light_air
        ),
        make_location_data(SC2Mission.THE_SPEAR_OF_ADUN.mission_name, "North Power Cell", SC2LOTV_LOC_ID_OFFSET + 604, LocationType.EXTRA,
            logic.protoss_common_unit_anti_light_air
        ),
        make_location_data(SC2Mission.THE_SPEAR_OF_ADUN.mission_name, "East Power Cell", SC2LOTV_LOC_ID_OFFSET + 605, LocationType.EXTRA,
            logic.protoss_common_unit_anti_light_air
        ),
        make_location_data(SC2Mission.THE_SPEAR_OF_ADUN.mission_name, "South Power Cell", SC2LOTV_LOC_ID_OFFSET + 606, LocationType.EXTRA,
            logic.protoss_common_unit_anti_light_air
        ),
        make_location_data(SC2Mission.THE_SPEAR_OF_ADUN.mission_name, "Southeast Power Cell", SC2LOTV_LOC_ID_OFFSET + 607, LocationType.EXTRA,
            logic.protoss_common_unit_anti_light_air
        ),
        make_location_data(SC2Mission.SKY_SHIELD.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 700, LocationType.VICTORY,
            logic.protoss_common_unit_basic_aa
        ),
        make_location_data(SC2Mission.SKY_SHIELD.mission_name, "Mid EMP Scrambler", SC2LOTV_LOC_ID_OFFSET + 701, LocationType.VANILLA,
            logic.protoss_common_unit_basic_aa
        ),
        make_location_data(SC2Mission.SKY_SHIELD.mission_name, "Southeast EMP Scrambler", SC2LOTV_LOC_ID_OFFSET + 702, LocationType.VANILLA,
            logic.protoss_common_unit_basic_aa
        ),
        make_location_data(SC2Mission.SKY_SHIELD.mission_name, "North EMP Scrambler", SC2LOTV_LOC_ID_OFFSET + 703, LocationType.VANILLA,
            logic.protoss_common_unit_basic_aa
        ),
        make_location_data(SC2Mission.SKY_SHIELD.mission_name, "Mid Stabilizer", SC2LOTV_LOC_ID_OFFSET + 704, LocationType.EXTRA),
        make_location_data(SC2Mission.SKY_SHIELD.mission_name, "Southwest Stabilizer", SC2LOTV_LOC_ID_OFFSET + 705, LocationType.EXTRA,
            logic.protoss_common_unit_basic_aa
        ),
        make_location_data(SC2Mission.SKY_SHIELD.mission_name, "Northwest Stabilizer", SC2LOTV_LOC_ID_OFFSET + 706, LocationType.EXTRA,
            logic.protoss_common_unit_basic_aa
        ),
        make_location_data(SC2Mission.SKY_SHIELD.mission_name, "Northeast Stabilizer", SC2LOTV_LOC_ID_OFFSET + 707, LocationType.EXTRA,
            logic.protoss_common_unit_basic_aa
        ),
        make_location_data(SC2Mission.SKY_SHIELD.mission_name, "Southeast Stabilizer", SC2LOTV_LOC_ID_OFFSET + 708, LocationType.EXTRA,
            logic.protoss_common_unit_basic_aa
        ),
        make_location_data(SC2Mission.SKY_SHIELD.mission_name, "West Raynor Base", SC2LOTV_LOC_ID_OFFSET + 709, LocationType.EXTRA,
            logic.protoss_common_unit_basic_aa
        ),
        make_location_data(SC2Mission.SKY_SHIELD.mission_name, "East Raynor Base", SC2LOTV_LOC_ID_OFFSET + 710, LocationType.EXTRA,
            logic.protoss_common_unit_basic_aa
        ),
        make_location_data(SC2Mission.BROTHERS_IN_ARMS.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 800, LocationType.VICTORY,
            logic.brothers_in_arms_requirement
        ),
        make_location_data(SC2Mission.BROTHERS_IN_ARMS.mission_name, "Mid Science Facility", SC2LOTV_LOC_ID_OFFSET + 801, LocationType.VANILLA,
            lambda state: logic.protoss_common_unit(state) or logic.take_over_ai_allies
        ),
        make_location_data(SC2Mission.BROTHERS_IN_ARMS.mission_name, "North Science Facility", SC2LOTV_LOC_ID_OFFSET + 802, LocationType.VANILLA,
            lambda state: (
                logic.brothers_in_arms_requirement(state)
                or (
                    logic.take_over_ai_allies
                    and logic.advanced_tactics
                    and (
                        logic.terran_common_unit(state)
                        or logic.protoss_common_unit(state)
                    )
                ))
        ),
        make_location_data(SC2Mission.BROTHERS_IN_ARMS.mission_name, "South Science Facility", SC2LOTV_LOC_ID_OFFSET + 803, LocationType.VANILLA,
            logic.brothers_in_arms_requirement
        ),
        make_location_data(SC2Mission.AMON_S_REACH.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 900, LocationType.VICTORY,
            logic.protoss_common_unit_anti_light_air
        ),
        make_location_data(SC2Mission.AMON_S_REACH.mission_name, "Close Solarite Reserve", SC2LOTV_LOC_ID_OFFSET + 901, LocationType.VANILLA),
        make_location_data(SC2Mission.AMON_S_REACH.mission_name, "North Solarite Reserve", SC2LOTV_LOC_ID_OFFSET + 902, LocationType.VANILLA,
            logic.protoss_common_unit_anti_light_air
        ),
        make_location_data(SC2Mission.AMON_S_REACH.mission_name, "East Solarite Reserve", SC2LOTV_LOC_ID_OFFSET + 903, LocationType.VANILLA,
            logic.protoss_common_unit_anti_light_air
        ),
        make_location_data(SC2Mission.AMON_S_REACH.mission_name, "West Launch Bay", SC2LOTV_LOC_ID_OFFSET + 904, LocationType.EXTRA,
            logic.protoss_common_unit_anti_light_air
        ),
        make_location_data(SC2Mission.AMON_S_REACH.mission_name, "South Launch Bay", SC2LOTV_LOC_ID_OFFSET + 905, LocationType.EXTRA,
            logic.protoss_common_unit_anti_light_air
        ),
        make_location_data(SC2Mission.AMON_S_REACH.mission_name, "Northwest Launch Bay", SC2LOTV_LOC_ID_OFFSET + 906, LocationType.EXTRA,
            logic.protoss_common_unit_anti_light_air
        ),
        make_location_data(SC2Mission.AMON_S_REACH.mission_name, "East Launch Bay", SC2LOTV_LOC_ID_OFFSET + 907, LocationType.EXTRA,
            logic.protoss_common_unit_anti_light_air
        ),
        make_location_data(SC2Mission.LAST_STAND.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 1000, LocationType.VICTORY,
            logic.last_stand_requirement
        ),
        make_location_data(SC2Mission.LAST_STAND.mission_name, "West Zenith Stone", SC2LOTV_LOC_ID_OFFSET + 1001, LocationType.VANILLA,
            logic.last_stand_requirement
        ),
        make_location_data(SC2Mission.LAST_STAND.mission_name, "North Zenith Stone", SC2LOTV_LOC_ID_OFFSET + 1002, LocationType.VANILLA,
            logic.last_stand_requirement
        ),
        make_location_data(SC2Mission.LAST_STAND.mission_name, "East Zenith Stone", SC2LOTV_LOC_ID_OFFSET + 1003, LocationType.VANILLA,
            logic.last_stand_requirement
        ),
        make_location_data(SC2Mission.LAST_STAND.mission_name, "1 Billion Zerg", SC2LOTV_LOC_ID_OFFSET + 1004, LocationType.EXTRA,
            logic.last_stand_requirement
        ),
        make_location_data(SC2Mission.LAST_STAND.mission_name, "1.5 Billion Zerg", SC2LOTV_LOC_ID_OFFSET + 1005, LocationType.VANILLA,
            lambda state: (
                logic.last_stand_requirement(state)
                and (state.has_all({item_names.KHAYDARIN_MONOLITH, item_names.PHOTON_CANNON, item_names.SHIELD_BATTERY}, player)
                    or state.has_any({item_names.SOA_SOLAR_LANCE, item_names.SOA_DEPLOY_FENIX}, player)
                ))
        ),
        make_location_data(SC2Mission.FORBIDDEN_WEAPON.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 1100, LocationType.VICTORY,
            logic.protoss_common_unit_anti_armor_air
        ),
        make_location_data(SC2Mission.FORBIDDEN_WEAPON.mission_name, "South Solarite", SC2LOTV_LOC_ID_OFFSET + 1101, LocationType.VANILLA,
            logic.protoss_common_unit_anti_armor_air
        ),
        make_location_data(SC2Mission.FORBIDDEN_WEAPON.mission_name, "North Solarite", SC2LOTV_LOC_ID_OFFSET + 1102, LocationType.VANILLA,
            logic.protoss_common_unit_anti_armor_air
        ),
        make_location_data(SC2Mission.FORBIDDEN_WEAPON.mission_name, "Northwest Solarite", SC2LOTV_LOC_ID_OFFSET + 1103, LocationType.VANILLA,
            logic.protoss_common_unit_anti_armor_air
        ),
        make_location_data(SC2Mission.TEMPLE_OF_UNIFICATION.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 1200, LocationType.VICTORY,
            logic.protoss_common_unit_anti_armor_air
        ),
        make_location_data(SC2Mission.TEMPLE_OF_UNIFICATION.mission_name, "Mid Celestial Lock", SC2LOTV_LOC_ID_OFFSET + 1201, LocationType.EXTRA,
            logic.protoss_common_unit_anti_armor_air
        ),
        make_location_data(SC2Mission.TEMPLE_OF_UNIFICATION.mission_name, "West Celestial Lock", SC2LOTV_LOC_ID_OFFSET + 1202, LocationType.EXTRA,
            logic.protoss_common_unit_anti_armor_air
        ),
        make_location_data(SC2Mission.TEMPLE_OF_UNIFICATION.mission_name, "South Celestial Lock", SC2LOTV_LOC_ID_OFFSET + 1203, LocationType.EXTRA,
            logic.protoss_common_unit_anti_armor_air
        ),
        make_location_data(SC2Mission.TEMPLE_OF_UNIFICATION.mission_name, "East Celestial Lock", SC2LOTV_LOC_ID_OFFSET + 1204, LocationType.EXTRA,
            logic.protoss_common_unit_anti_armor_air
        ),
        make_location_data(SC2Mission.TEMPLE_OF_UNIFICATION.mission_name, "North Celestial Lock", SC2LOTV_LOC_ID_OFFSET + 1205, LocationType.EXTRA,
            logic.protoss_common_unit_anti_armor_air
        ),
        make_location_data(SC2Mission.TEMPLE_OF_UNIFICATION.mission_name, "Titanic Warp Prism", SC2LOTV_LOC_ID_OFFSET + 1206, LocationType.VANILLA,
            logic.protoss_common_unit_anti_armor_air
        ),
        make_location_data(SC2Mission.THE_INFINITE_CYCLE.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 1300, LocationType.VICTORY,
            logic.the_infinite_cycle_requirement
        ),
        make_location_data(SC2Mission.THE_INFINITE_CYCLE.mission_name, "First Hall of Revelation", SC2LOTV_LOC_ID_OFFSET + 1301, LocationType.EXTRA,
            logic.the_infinite_cycle_requirement
        ),
        make_location_data(SC2Mission.THE_INFINITE_CYCLE.mission_name, "Second Hall of Revelation", SC2LOTV_LOC_ID_OFFSET + 1302, LocationType.EXTRA,
            logic.the_infinite_cycle_requirement
        ),
        make_location_data(SC2Mission.THE_INFINITE_CYCLE.mission_name, "First Xel'Naga Device", SC2LOTV_LOC_ID_OFFSET + 1303, LocationType.VANILLA,
            logic.the_infinite_cycle_requirement
        ),
        make_location_data(SC2Mission.THE_INFINITE_CYCLE.mission_name, "Second Xel'Naga Device", SC2LOTV_LOC_ID_OFFSET + 1304, LocationType.VANILLA,
            logic.the_infinite_cycle_requirement
        ),
        make_location_data(SC2Mission.THE_INFINITE_CYCLE.mission_name, "Third Xel'Naga Device", SC2LOTV_LOC_ID_OFFSET + 1305, LocationType.VANILLA,
            logic.the_infinite_cycle_requirement
        ),
        make_location_data(SC2Mission.HARBINGER_OF_OBLIVION.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 1400, LocationType.VICTORY,
            logic.harbinger_of_oblivion_requirement
        ),
        make_location_data(SC2Mission.HARBINGER_OF_OBLIVION.mission_name, "Artanis", SC2LOTV_LOC_ID_OFFSET + 1401, LocationType.EXTRA),
        make_location_data(SC2Mission.HARBINGER_OF_OBLIVION.mission_name, "Northwest Void Crystal", SC2LOTV_LOC_ID_OFFSET + 1402, LocationType.EXTRA,
            logic.harbinger_of_oblivion_requirement
        ),
        make_location_data(SC2Mission.HARBINGER_OF_OBLIVION.mission_name, "Northeast Void Crystal", SC2LOTV_LOC_ID_OFFSET + 1403, LocationType.EXTRA,
            logic.harbinger_of_oblivion_requirement
        ),
        make_location_data(SC2Mission.HARBINGER_OF_OBLIVION.mission_name, "Southwest Void Crystal", SC2LOTV_LOC_ID_OFFSET + 1404, LocationType.EXTRA,
            logic.harbinger_of_oblivion_requirement
        ),
        make_location_data(SC2Mission.HARBINGER_OF_OBLIVION.mission_name, "Southeast Void Crystal", SC2LOTV_LOC_ID_OFFSET + 1405, LocationType.EXTRA,
            logic.harbinger_of_oblivion_requirement
        ),
        make_location_data(SC2Mission.HARBINGER_OF_OBLIVION.mission_name, "South Xel'Naga Vessel", SC2LOTV_LOC_ID_OFFSET + 1406, LocationType.VANILLA),
        make_location_data(SC2Mission.HARBINGER_OF_OBLIVION.mission_name, "Mid Xel'Naga Vessel", SC2LOTV_LOC_ID_OFFSET + 1407, LocationType.VANILLA,
            logic.harbinger_of_oblivion_requirement
        ),
        make_location_data(SC2Mission.HARBINGER_OF_OBLIVION.mission_name, "North Xel'Naga Vessel", SC2LOTV_LOC_ID_OFFSET + 1408, LocationType.VANILLA,
            logic.harbinger_of_oblivion_requirement
        ),
        make_location_data(SC2Mission.UNSEALING_THE_PAST.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 1500, LocationType.VICTORY,
            lambda state: (
                logic.protoss_basic_splash(state)
                and logic.protoss_anti_light_anti_air(state))
        ),
        make_location_data(SC2Mission.UNSEALING_THE_PAST.mission_name, "Zerg Cleared", SC2LOTV_LOC_ID_OFFSET + 1501, LocationType.EXTRA),
        make_location_data(SC2Mission.UNSEALING_THE_PAST.mission_name, "First Stasis Lock", SC2LOTV_LOC_ID_OFFSET + 1502, LocationType.EXTRA,
            lambda state: (
                logic.advanced_tactics
                or (logic.protoss_basic_splash(state)
                    and logic.protoss_anti_light_anti_air(state)
                ))
        ),
        make_location_data(SC2Mission.UNSEALING_THE_PAST.mission_name, "Second Stasis Lock", SC2LOTV_LOC_ID_OFFSET + 1503, LocationType.EXTRA,
            lambda state: (
                logic.protoss_basic_splash(state)
                and logic.protoss_anti_light_anti_air(state))
        ),
        make_location_data(SC2Mission.UNSEALING_THE_PAST.mission_name, "Third Stasis Lock", SC2LOTV_LOC_ID_OFFSET + 1504, LocationType.EXTRA,
            lambda state: (
                logic.protoss_basic_splash(state)
                and logic.protoss_anti_light_anti_air(state))
        ),
        make_location_data(SC2Mission.UNSEALING_THE_PAST.mission_name, "Fourth Stasis Lock", SC2LOTV_LOC_ID_OFFSET + 1505, LocationType.EXTRA,
            lambda state: (
                logic.protoss_basic_splash(state)
                and logic.protoss_anti_light_anti_air(state))
        ),
        make_location_data(SC2Mission.UNSEALING_THE_PAST.mission_name, "South Power Core", SC2LOTV_LOC_ID_OFFSET + 1506, LocationType.VANILLA,
            lambda state: (
                logic.protoss_basic_splash(state)
                and logic.protoss_anti_light_anti_air(state))
        ),
        make_location_data(SC2Mission.UNSEALING_THE_PAST.mission_name, "East Power Core", SC2LOTV_LOC_ID_OFFSET + 1507, LocationType.VANILLA,
            lambda state: (
                logic.protoss_basic_splash(state)
                and logic.protoss_anti_light_anti_air(state))
        ),
        make_location_data(SC2Mission.PURIFICATION.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 1600, LocationType.VICTORY,
            logic.protoss_competent_comp
        ),
        make_location_data(SC2Mission.PURIFICATION.mission_name, "North Sector: West Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1601, LocationType.VANILLA,
            logic.protoss_competent_comp
        ),
        make_location_data(SC2Mission.PURIFICATION.mission_name, "North Sector: Northeast Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1602, LocationType.EXTRA,
            logic.protoss_competent_comp
        ),
        make_location_data(SC2Mission.PURIFICATION.mission_name, "North Sector: Southeast Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1603, LocationType.EXTRA,
            logic.protoss_competent_comp
        ),
        make_location_data(SC2Mission.PURIFICATION.mission_name, "South Sector: West Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1604, LocationType.VANILLA,
            logic.protoss_competent_comp
        ),
        make_location_data(SC2Mission.PURIFICATION.mission_name, "South Sector: North Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1605, LocationType.EXTRA,
            logic.protoss_competent_comp
        ),
        make_location_data(SC2Mission.PURIFICATION.mission_name, "South Sector: East Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1606, LocationType.EXTRA,
            logic.protoss_competent_comp
        ),
        make_location_data(SC2Mission.PURIFICATION.mission_name, "West Sector: West Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1607, LocationType.VANILLA,
            logic.protoss_competent_comp
        ),
        make_location_data(SC2Mission.PURIFICATION.mission_name, "West Sector: Mid Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1608, LocationType.EXTRA,
            logic.protoss_competent_comp
        ),
        make_location_data(SC2Mission.PURIFICATION.mission_name, "West Sector: East Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1609, LocationType.EXTRA,
            logic.protoss_competent_comp
        ),
        make_location_data(SC2Mission.PURIFICATION.mission_name, "East Sector: North Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1610, LocationType.VANILLA,
            logic.protoss_competent_comp
        ),
        make_location_data(SC2Mission.PURIFICATION.mission_name, "East Sector: West Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1611, LocationType.EXTRA,
            logic.protoss_competent_comp
        ),
        make_location_data(SC2Mission.PURIFICATION.mission_name, "East Sector: South Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1612, LocationType.EXTRA,
            logic.protoss_competent_comp
        ),
        make_location_data(SC2Mission.PURIFICATION.mission_name, "Purifier Warden", SC2LOTV_LOC_ID_OFFSET + 1613, LocationType.VANILLA,
            logic.protoss_competent_comp
        ),
        make_location_data(SC2Mission.STEPS_OF_THE_RITE.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 1700, LocationType.VICTORY,
            logic.steps_of_the_rite_requirement
        ),
        make_location_data(SC2Mission.STEPS_OF_THE_RITE.mission_name, "First Terrazine Fog", SC2LOTV_LOC_ID_OFFSET + 1701, LocationType.EXTRA,
            logic.steps_of_the_rite_requirement
        ),
        make_location_data(SC2Mission.STEPS_OF_THE_RITE.mission_name, "Southwest Guardian", SC2LOTV_LOC_ID_OFFSET + 1702, LocationType.EXTRA,
            logic.steps_of_the_rite_requirement
        ),
        make_location_data(SC2Mission.STEPS_OF_THE_RITE.mission_name, "West Guardian", SC2LOTV_LOC_ID_OFFSET + 1703, LocationType.EXTRA,
            logic.steps_of_the_rite_requirement
        ),
        make_location_data(SC2Mission.STEPS_OF_THE_RITE.mission_name, "Northwest Guardian", SC2LOTV_LOC_ID_OFFSET + 1704, LocationType.EXTRA,
            logic.steps_of_the_rite_requirement
        ),
        make_location_data(SC2Mission.STEPS_OF_THE_RITE.mission_name, "Northeast Guardian", SC2LOTV_LOC_ID_OFFSET + 1705, LocationType.EXTRA,
            logic.steps_of_the_rite_requirement
        ),
        make_location_data(SC2Mission.STEPS_OF_THE_RITE.mission_name, "North Mothership", SC2LOTV_LOC_ID_OFFSET + 1706, LocationType.VANILLA,
            logic.steps_of_the_rite_requirement
        ),
        make_location_data(SC2Mission.STEPS_OF_THE_RITE.mission_name, "South Mothership", SC2LOTV_LOC_ID_OFFSET + 1707, LocationType.VANILLA,
            logic.steps_of_the_rite_requirement
        ),
        make_location_data(SC2Mission.RAK_SHIR.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 1800, LocationType.VICTORY,
            logic.protoss_competent_comp
        ),
        make_location_data(SC2Mission.RAK_SHIR.mission_name, "North Slayn Elemental", SC2LOTV_LOC_ID_OFFSET + 1801, LocationType.VANILLA,
            logic.protoss_competent_comp
        ),
        make_location_data(SC2Mission.RAK_SHIR.mission_name, "Southwest Slayn Elemental", SC2LOTV_LOC_ID_OFFSET + 1802, LocationType.VANILLA,
            logic.protoss_competent_comp
        ),
        make_location_data(SC2Mission.RAK_SHIR.mission_name, "East Slayn Elemental", SC2LOTV_LOC_ID_OFFSET + 1803, LocationType.VANILLA,
            logic.protoss_competent_comp
        ),
        make_location_data(SC2Mission.TEMPLAR_S_CHARGE.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 1900, LocationType.VICTORY,
            logic.templars_charge_requirement
        ),
        make_location_data(SC2Mission.TEMPLAR_S_CHARGE.mission_name, "Northwest Power Core", SC2LOTV_LOC_ID_OFFSET + 1901, LocationType.EXTRA,
            logic.templars_charge_requirement
        ),
        make_location_data(SC2Mission.TEMPLAR_S_CHARGE.mission_name, "Northeast Power Core", SC2LOTV_LOC_ID_OFFSET + 1902, LocationType.EXTRA,
            logic.templars_charge_requirement
        ),
        make_location_data(SC2Mission.TEMPLAR_S_CHARGE.mission_name, "Southeast Power Core", SC2LOTV_LOC_ID_OFFSET + 1903, LocationType.EXTRA,
            logic.templars_charge_requirement
        ),
        make_location_data(SC2Mission.TEMPLAR_S_CHARGE.mission_name, "West Hybrid Stasis Chamber", SC2LOTV_LOC_ID_OFFSET + 1904, LocationType.VANILLA,
            logic.templars_charge_requirement
        ),
        make_location_data(SC2Mission.TEMPLAR_S_CHARGE.mission_name, "Southeast Hybrid Stasis Chamber", SC2LOTV_LOC_ID_OFFSET + 1905, LocationType.VANILLA,
            logic.protoss_fleet
        ),
        make_location_data(SC2Mission.TEMPLAR_S_RETURN.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 2000, LocationType.VICTORY,
            logic.templars_return_requirement
        ),
        make_location_data(SC2Mission.TEMPLAR_S_RETURN.mission_name, "Citadel: First Gate", SC2LOTV_LOC_ID_OFFSET + 2001, LocationType.EXTRA),
        make_location_data(SC2Mission.TEMPLAR_S_RETURN.mission_name, "Citadel: Second Gate", SC2LOTV_LOC_ID_OFFSET + 2002, LocationType.EXTRA),
        make_location_data(SC2Mission.TEMPLAR_S_RETURN.mission_name, "Citadel: Power Structure", SC2LOTV_LOC_ID_OFFSET + 2003, LocationType.VANILLA),
        make_location_data(SC2Mission.TEMPLAR_S_RETURN.mission_name, "Temple Grounds: Gather Army", SC2LOTV_LOC_ID_OFFSET + 2004, LocationType.VANILLA,
            logic.templars_return_requirement
        ),
        make_location_data(SC2Mission.TEMPLAR_S_RETURN.mission_name, "Temple Grounds: Power Structure", SC2LOTV_LOC_ID_OFFSET + 2005, LocationType.VANILLA,
            logic.templars_return_requirement
        ),
        make_location_data(SC2Mission.TEMPLAR_S_RETURN.mission_name, "Caverns: Purifier", SC2LOTV_LOC_ID_OFFSET + 2006, LocationType.EXTRA,
            logic.templars_return_requirement
        ),
        make_location_data(SC2Mission.TEMPLAR_S_RETURN.mission_name, "Caverns: Dark Templar", SC2LOTV_LOC_ID_OFFSET + 2007, LocationType.EXTRA,
            logic.templars_return_requirement
        ),
        make_location_data(SC2Mission.THE_HOST.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 2100, LocationType.VICTORY,
            logic.the_host_requirement
        ),
        make_location_data(SC2Mission.THE_HOST.mission_name, "Southeast Void Shard", SC2LOTV_LOC_ID_OFFSET + 2101, LocationType.VICTORY,
            logic.the_host_requirement
        ),
        make_location_data(SC2Mission.THE_HOST.mission_name, "South Void Shard", SC2LOTV_LOC_ID_OFFSET + 2102, LocationType.EXTRA,
            logic.the_host_requirement
        ),
        make_location_data(SC2Mission.THE_HOST.mission_name, "Southwest Void Shard", SC2LOTV_LOC_ID_OFFSET + 2103, LocationType.EXTRA,
            logic.the_host_requirement
        ),
        make_location_data(SC2Mission.THE_HOST.mission_name, "North Void Shard", SC2LOTV_LOC_ID_OFFSET + 2104, LocationType.EXTRA,
            logic.the_host_requirement
        ),
        make_location_data(SC2Mission.THE_HOST.mission_name, "Northwest Void Shard", SC2LOTV_LOC_ID_OFFSET + 2105, LocationType.EXTRA,
            logic.the_host_requirement
        ),
        make_location_data(SC2Mission.THE_HOST.mission_name, "Nerazim Warp in Zone", SC2LOTV_LOC_ID_OFFSET + 2106, LocationType.VANILLA,
            logic.the_host_requirement
        ),
        make_location_data(SC2Mission.THE_HOST.mission_name, "Tal'darim Warp in Zone", SC2LOTV_LOC_ID_OFFSET + 2107, LocationType.VANILLA,
            logic.the_host_requirement
        ),
        make_location_data(SC2Mission.THE_HOST.mission_name, "Purifier Warp in Zone", SC2LOTV_LOC_ID_OFFSET + 2108, LocationType.VANILLA,
            logic.the_host_requirement
        ),
        make_location_data(SC2Mission.SALVATION.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 2200, LocationType.VICTORY,
            logic.salvation_requirement
        ),
        make_location_data(SC2Mission.SALVATION.mission_name, "Fabrication Matrix", SC2LOTV_LOC_ID_OFFSET + 2201, LocationType.EXTRA,
            logic.salvation_requirement
        ),
        make_location_data(SC2Mission.SALVATION.mission_name, "Assault Cluster", SC2LOTV_LOC_ID_OFFSET + 2202, LocationType.EXTRA,
            logic.salvation_requirement
        ),
        make_location_data(SC2Mission.SALVATION.mission_name, "Hull Breach", SC2LOTV_LOC_ID_OFFSET + 2203, LocationType.EXTRA,
            logic.salvation_requirement
        ),
        make_location_data(SC2Mission.SALVATION.mission_name, "Core Critical", SC2LOTV_LOC_ID_OFFSET + 2204, LocationType.EXTRA,
            logic.salvation_requirement
        ),

        # Epilogue
        make_location_data(SC2Mission.INTO_THE_VOID.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 2300, LocationType.VICTORY,
            logic.into_the_void_requirement
        ),
        make_location_data(SC2Mission.INTO_THE_VOID.mission_name, "Corruption Source", SC2LOTV_LOC_ID_OFFSET + 2301, LocationType.EXTRA),
        make_location_data(SC2Mission.INTO_THE_VOID.mission_name, "Southwest Forward Position", SC2LOTV_LOC_ID_OFFSET + 2302, LocationType.VANILLA,
            logic.into_the_void_requirement
        ),
        make_location_data(SC2Mission.INTO_THE_VOID.mission_name, "Northwest Forward Position", SC2LOTV_LOC_ID_OFFSET + 2303, LocationType.VANILLA,
            logic.into_the_void_requirement
        ),
        make_location_data(SC2Mission.INTO_THE_VOID.mission_name, "Southeast Forward Position", SC2LOTV_LOC_ID_OFFSET + 2304, LocationType.VANILLA,
            logic.into_the_void_requirement
        ),
        make_location_data(SC2Mission.INTO_THE_VOID.mission_name, "Northeast Forward Position", SC2LOTV_LOC_ID_OFFSET + 2305, LocationType.VANILLA),
        make_location_data(SC2Mission.THE_ESSENCE_OF_ETERNITY.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 2400, LocationType.VICTORY,
            logic.essence_of_eternity_requirement
        ),
        make_location_data(SC2Mission.THE_ESSENCE_OF_ETERNITY.mission_name, "Void Trashers", SC2LOTV_LOC_ID_OFFSET + 2401, LocationType.EXTRA),
        make_location_data(SC2Mission.AMON_S_FALL.mission_name, "Victory", SC2LOTV_LOC_ID_OFFSET + 2500, LocationType.VICTORY,
            logic.amons_fall_requirement
        ),

        # Nova Covert Ops
        make_location_data(SC2Mission.THE_ESCAPE.mission_name, "Victory", SC2NCO_LOC_ID_OFFSET + 100, LocationType.VICTORY,
            logic.the_escape_requirement
        ),
        make_location_data(SC2Mission.THE_ESCAPE.mission_name, "Rifle", SC2NCO_LOC_ID_OFFSET + 101, LocationType.VANILLA,
            logic.the_escape_first_stage_requirement
        ),
        make_location_data(SC2Mission.THE_ESCAPE.mission_name, "Grenades", SC2NCO_LOC_ID_OFFSET + 102, LocationType.VANILLA,
            logic.the_escape_first_stage_requirement
        ),
        make_location_data(SC2Mission.THE_ESCAPE.mission_name, "Agent Delta", SC2NCO_LOC_ID_OFFSET + 103, LocationType.VANILLA,
            logic.the_escape_requirement
        ),
        make_location_data(SC2Mission.THE_ESCAPE.mission_name, "Agent Pierce", SC2NCO_LOC_ID_OFFSET + 104, LocationType.VANILLA,
            logic.the_escape_requirement
        ),
        make_location_data(SC2Mission.THE_ESCAPE.mission_name, "Agent Stone", SC2NCO_LOC_ID_OFFSET + 105, LocationType.VANILLA,
            logic.the_escape_requirement
        ),
        make_location_data(SC2Mission.SUDDEN_STRIKE.mission_name, "Victory", SC2NCO_LOC_ID_OFFSET + 200, LocationType.VICTORY,
            logic.sudden_strike_can_reach_objectives
        ),
        make_location_data(SC2Mission.SUDDEN_STRIKE.mission_name, "Research Center", SC2NCO_LOC_ID_OFFSET + 201, LocationType.VANILLA,
            logic.sudden_strike_can_reach_objectives
        ),
        make_location_data(SC2Mission.SUDDEN_STRIKE.mission_name, "Weaponry Labs", SC2NCO_LOC_ID_OFFSET + 202, LocationType.VANILLA,
            logic.sudden_strike_requirement
        ),
        make_location_data(SC2Mission.SUDDEN_STRIKE.mission_name, "Brutalisk", SC2NCO_LOC_ID_OFFSET + 203, LocationType.EXTRA,
            logic.sudden_strike_requirement
        ),
        make_location_data(SC2Mission.ENEMY_INTELLIGENCE.mission_name, "Victory", SC2NCO_LOC_ID_OFFSET + 300, LocationType.VICTORY,
            logic.enemy_intelligence_third_stage_requirement
        ),
        make_location_data(SC2Mission.ENEMY_INTELLIGENCE.mission_name, "West Garrison", SC2NCO_LOC_ID_OFFSET + 301, LocationType.EXTRA,
            logic.enemy_intelligence_first_stage_requirement
        ),
        make_location_data(SC2Mission.ENEMY_INTELLIGENCE.mission_name, "Close Garrison", SC2NCO_LOC_ID_OFFSET + 302, LocationType.EXTRA,
            logic.enemy_intelligence_first_stage_requirement
        ),
        make_location_data(SC2Mission.ENEMY_INTELLIGENCE.mission_name, "Northeast Garrison", SC2NCO_LOC_ID_OFFSET + 303, LocationType.EXTRA,
            logic.enemy_intelligence_first_stage_requirement
        ),
        make_location_data(SC2Mission.ENEMY_INTELLIGENCE.mission_name, "Southeast Garrison", SC2NCO_LOC_ID_OFFSET + 304, LocationType.EXTRA,
            lambda state: (
                logic.enemy_intelligence_first_stage_requirement(state)
                and logic.enemy_intelligence_cliff_garrison(state))
        ),
        make_location_data(SC2Mission.ENEMY_INTELLIGENCE.mission_name, "South Garrison", SC2NCO_LOC_ID_OFFSET + 305, LocationType.EXTRA,
            logic.enemy_intelligence_first_stage_requirement
        ),
        make_location_data(SC2Mission.ENEMY_INTELLIGENCE.mission_name, "All Garrisons", SC2NCO_LOC_ID_OFFSET + 306, LocationType.VANILLA,
            lambda state: (
                logic.enemy_intelligence_first_stage_requirement(state)
                and logic.enemy_intelligence_cliff_garrison(state))
        ),
        make_location_data(SC2Mission.ENEMY_INTELLIGENCE.mission_name, "Forces Rescued", SC2NCO_LOC_ID_OFFSET + 307, LocationType.VANILLA,
            logic.enemy_intelligence_first_stage_requirement
        ),
        make_location_data(SC2Mission.ENEMY_INTELLIGENCE.mission_name, "Communications Hub", SC2NCO_LOC_ID_OFFSET + 308, LocationType.VANILLA,
            logic.enemy_intelligence_second_stage_requirement
        ),
        make_location_data(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "Victory", SC2NCO_LOC_ID_OFFSET + 400, LocationType.VICTORY,
            logic.trouble_in_paradise_requirement
        ),
        make_location_data(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "North Base: West Hatchery", SC2NCO_LOC_ID_OFFSET + 401, LocationType.VANILLA,
            logic.trouble_in_paradise_requirement
        ),
        make_location_data(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "North Base: North Hatchery", SC2NCO_LOC_ID_OFFSET + 402, LocationType.VANILLA,
            logic.trouble_in_paradise_requirement
        ),
        make_location_data(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "North Base: East Hatchery", SC2NCO_LOC_ID_OFFSET + 403, LocationType.VANILLA),
        make_location_data(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "South Base: Northwest Hatchery", SC2NCO_LOC_ID_OFFSET + 404, LocationType.VANILLA,
            logic.trouble_in_paradise_requirement
        ),
        make_location_data(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "South Base: Southwest Hatchery", SC2NCO_LOC_ID_OFFSET + 405, LocationType.VANILLA,
            logic.trouble_in_paradise_requirement
        ),
        make_location_data(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "South Base: East Hatchery", SC2NCO_LOC_ID_OFFSET + 406, LocationType.VANILLA),
        make_location_data(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "North Shield Projector", SC2NCO_LOC_ID_OFFSET + 407, LocationType.EXTRA,
            logic.trouble_in_paradise_requirement
        ),
        make_location_data(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "East Shield Projector", SC2NCO_LOC_ID_OFFSET + 408, LocationType.EXTRA,
            logic.trouble_in_paradise_requirement
        ),
        make_location_data(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "South Shield Projector", SC2NCO_LOC_ID_OFFSET + 409, LocationType.EXTRA,
            logic.trouble_in_paradise_requirement
        ),
        make_location_data(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "West Shield Projector", SC2NCO_LOC_ID_OFFSET + 410, LocationType.EXTRA,
            logic.trouble_in_paradise_requirement
        ),
        make_location_data(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "Fleet Beacon", SC2NCO_LOC_ID_OFFSET + 411, LocationType.VANILLA,
            logic.trouble_in_paradise_requirement
        ),
        make_location_data(SC2Mission.NIGHT_TERRORS.mission_name, "Victory", SC2NCO_LOC_ID_OFFSET + 500, LocationType.VICTORY,
            logic.night_terrors_requirement
        ),
        make_location_data(SC2Mission.NIGHT_TERRORS.mission_name, "1 Terrazine Node Collected", SC2NCO_LOC_ID_OFFSET + 501, LocationType.EXTRA,
            logic.night_terrors_requirement
        ),
        make_location_data(SC2Mission.NIGHT_TERRORS.mission_name, "2 Terrazine Nodes Collected", SC2NCO_LOC_ID_OFFSET + 502, LocationType.EXTRA,
            logic.night_terrors_requirement
        ),
        make_location_data(SC2Mission.NIGHT_TERRORS.mission_name, "3 Terrazine Nodes Collected", SC2NCO_LOC_ID_OFFSET + 503, LocationType.EXTRA,
            logic.night_terrors_requirement
        ),
        make_location_data(SC2Mission.NIGHT_TERRORS.mission_name, "4 Terrazine Nodes Collected", SC2NCO_LOC_ID_OFFSET + 504, LocationType.EXTRA,
            logic.night_terrors_requirement
        ),
        make_location_data(SC2Mission.NIGHT_TERRORS.mission_name, "5 Terrazine Nodes Collected", SC2NCO_LOC_ID_OFFSET + 505, LocationType.EXTRA,
            logic.night_terrors_requirement
        ),
        make_location_data(SC2Mission.NIGHT_TERRORS.mission_name, "HERC Outpost", SC2NCO_LOC_ID_OFFSET + 506, LocationType.VANILLA,
            logic.night_terrors_requirement
        ),
        make_location_data(SC2Mission.NIGHT_TERRORS.mission_name, "Umojan Mine", SC2NCO_LOC_ID_OFFSET + 507, LocationType.EXTRA,
            logic.night_terrors_requirement
        ),
        make_location_data(SC2Mission.NIGHT_TERRORS.mission_name, "Blightbringer", SC2NCO_LOC_ID_OFFSET + 508, LocationType.VANILLA,
            lambda state: (
                logic.night_terrors_requirement(state)
                and logic.nova_ranged_weapon(state)
                and state.has_any({
                    item_names.NOVA_HELLFIRE_SHOTGUN, item_names.NOVA_PULSE_GRENADES, item_names.NOVA_STIM_INFUSION,
                    item_names.NOVA_HOLO_DECOY
                }, player))
        ),
        make_location_data(SC2Mission.NIGHT_TERRORS.mission_name, "Science Facility", SC2NCO_LOC_ID_OFFSET + 509, LocationType.EXTRA,
            logic.night_terrors_requirement
        ),
        make_location_data(SC2Mission.NIGHT_TERRORS.mission_name, "Eradicators", SC2NCO_LOC_ID_OFFSET + 510, LocationType.VANILLA,
            lambda state: (
                logic.night_terrors_requirement(state)
                and logic.nova_any_weapon(state))
        ),
        make_location_data(SC2Mission.FLASHPOINT.mission_name, "Victory", SC2NCO_LOC_ID_OFFSET + 600, LocationType.VICTORY,
            logic.flashpoint_far_requirement
        ),
        make_location_data(SC2Mission.FLASHPOINT.mission_name, "Close North Evidence Coordinates", SC2NCO_LOC_ID_OFFSET + 601, LocationType.EXTRA,
            lambda state: (
                state.has_any({item_names.LIBERATOR_RAID_ARTILLERY, item_names.RAVEN_HUNTER_SEEKER_WEAPON}, player)
                or logic.terran_common_unit(state))
        ),
        make_location_data(SC2Mission.FLASHPOINT.mission_name, "Close East Evidence Coordinates", SC2NCO_LOC_ID_OFFSET + 602, LocationType.EXTRA,
            lambda state: (
                state.has_any({item_names.LIBERATOR_RAID_ARTILLERY, item_names.RAVEN_HUNTER_SEEKER_WEAPON}, player)
                or logic.terran_common_unit(state))
        ),
        make_location_data(SC2Mission.FLASHPOINT.mission_name, "Far North Evidence Coordinates", SC2NCO_LOC_ID_OFFSET + 603, LocationType.EXTRA,
            logic.flashpoint_far_requirement
        ),
        make_location_data(SC2Mission.FLASHPOINT.mission_name, "Far East Evidence Coordinates", SC2NCO_LOC_ID_OFFSET + 604, LocationType.EXTRA,
            logic.flashpoint_far_requirement
        ),
        make_location_data(SC2Mission.FLASHPOINT.mission_name, "Experimental Weapon", SC2NCO_LOC_ID_OFFSET + 605, LocationType.VANILLA,
            logic.flashpoint_far_requirement
        ),
        make_location_data(SC2Mission.FLASHPOINT.mission_name, "Northwest Subway Entrance", SC2NCO_LOC_ID_OFFSET + 606, LocationType.VANILLA,
            lambda state: (
                state.has_any({item_names.LIBERATOR_RAID_ARTILLERY, item_names.RAVEN_HUNTER_SEEKER_WEAPON}, player)
                and logic.terran_common_unit(state)
                        or logic.flashpoint_far_requirement(state))
        ),
        make_location_data(SC2Mission.FLASHPOINT.mission_name, "Southeast Subway Entrance", SC2NCO_LOC_ID_OFFSET + 607, LocationType.VANILLA,
                     lambda state: state.has_any(
                         {item_names.LIBERATOR_RAID_ARTILLERY, item_names.RAVEN_HUNTER_SEEKER_WEAPON}, player)
                                   and logic.terran_common_unit(state)
                                   or logic.flashpoint_far_requirement(state)),
        make_location_data(SC2Mission.FLASHPOINT.mission_name, "Northeast Subway Entrance", SC2NCO_LOC_ID_OFFSET + 608, LocationType.VANILLA,
            logic.flashpoint_far_requirement
        ),
        make_location_data(SC2Mission.FLASHPOINT.mission_name, "Expansion Hatchery", SC2NCO_LOC_ID_OFFSET + 609, LocationType.EXTRA,
                     lambda state: state.has(item_names.LIBERATOR_RAID_ARTILLERY, player) and logic.terran_common_unit(state)
                                   or logic.flashpoint_far_requirement(state)),
        make_location_data(SC2Mission.FLASHPOINT.mission_name, "Baneling Spawns", SC2NCO_LOC_ID_OFFSET + 610, LocationType.EXTRA,
            logic.flashpoint_far_requirement
        ),
        make_location_data(SC2Mission.FLASHPOINT.mission_name, "Mutalisk Spawns", SC2NCO_LOC_ID_OFFSET + 611, LocationType.EXTRA,
            logic.flashpoint_far_requirement
        ),
        make_location_data(SC2Mission.FLASHPOINT.mission_name, "Nydus Worm Spawns", SC2NCO_LOC_ID_OFFSET + 612, LocationType.EXTRA,
            logic.flashpoint_far_requirement
        ),
        make_location_data(SC2Mission.FLASHPOINT.mission_name, "Lurker Spawns", SC2NCO_LOC_ID_OFFSET + 613, LocationType.EXTRA,
            logic.flashpoint_far_requirement
        ),
        make_location_data(SC2Mission.FLASHPOINT.mission_name, "Brood Lord Spawns", SC2NCO_LOC_ID_OFFSET + 614, LocationType.EXTRA,
            logic.flashpoint_far_requirement
        ),
        make_location_data(SC2Mission.FLASHPOINT.mission_name, "Ultralisk Spawns", SC2NCO_LOC_ID_OFFSET + 615, LocationType.EXTRA,
            logic.flashpoint_far_requirement
        ),
        make_location_data(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "Victory", SC2NCO_LOC_ID_OFFSET + 700, LocationType.VICTORY,
            logic.enemy_shadow_victory
        ),
        make_location_data(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "Sewers: Domination Visor", SC2NCO_LOC_ID_OFFSET + 701, LocationType.VANILLA,
            logic.enemy_shadow_domination
        ),
        make_location_data(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "Sewers: Resupply Crate", SC2NCO_LOC_ID_OFFSET + 702, LocationType.EXTRA,
            logic.enemy_shadow_first_stage
        ),
        make_location_data(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "Sewers: Facility Access", SC2NCO_LOC_ID_OFFSET + 703, LocationType.VANILLA,
            logic.enemy_shadow_first_stage
        ),
        make_location_data(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "Facility: Northwest Door Lock", SC2NCO_LOC_ID_OFFSET + 704, LocationType.VANILLA,
            logic.enemy_shadow_door_controls
        ),
        make_location_data(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "Facility: Southeast Door Lock", SC2NCO_LOC_ID_OFFSET + 705, LocationType.VANILLA,
            logic.enemy_shadow_door_controls
        ),
        make_location_data(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "Facility: Blazefire Gunblade", SC2NCO_LOC_ID_OFFSET + 706, LocationType.VANILLA,
            lambda state: (
                logic.enemy_shadow_second_stage(state)
                and (logic.story_tech_granted
                    or state.has(item_names.NOVA_BLINK, player)
                    or (adv_tactics
                        and state.has_all({item_names.NOVA_DOMINATION, item_names.NOVA_HOLO_DECOY, item_names.NOVA_JUMP_SUIT_MODULE}, player)
                    )
                ))
        ),
        make_location_data(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "Facility: Blink Suit", SC2NCO_LOC_ID_OFFSET + 707, LocationType.VANILLA,
            logic.enemy_shadow_second_stage
        ),
        make_location_data(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "Facility: Advanced Weaponry", SC2NCO_LOC_ID_OFFSET + 708, LocationType.VANILLA,
            logic.enemy_shadow_second_stage
        ),
        make_location_data(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "Facility: Entrance Resupply Crate", SC2NCO_LOC_ID_OFFSET + 709, LocationType.EXTRA,
            logic.enemy_shadow_first_stage
        ),
        make_location_data(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "Facility: West Resupply Crate", SC2NCO_LOC_ID_OFFSET + 710, LocationType.EXTRA,
            logic.enemy_shadow_second_stage
        ),
        make_location_data(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "Facility: North Resupply Crate", SC2NCO_LOC_ID_OFFSET + 711, LocationType.EXTRA,
            logic.enemy_shadow_second_stage
        ),
        make_location_data(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "Facility: East Resupply Crate", SC2NCO_LOC_ID_OFFSET + 712, LocationType.EXTRA,
            logic.enemy_shadow_second_stage
        ),
        make_location_data(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "Facility: South Resupply Crate", SC2NCO_LOC_ID_OFFSET + 713, LocationType.EXTRA,
            logic.enemy_shadow_second_stage
        ),
        make_location_data(SC2Mission.DARK_SKIES.mission_name, "Victory", SC2NCO_LOC_ID_OFFSET + 800, LocationType.VICTORY,
            logic.dark_skies_requirement
        ),
        make_location_data(SC2Mission.DARK_SKIES.mission_name, "First Squadron of Dominion Fleet", SC2NCO_LOC_ID_OFFSET + 801, LocationType.EXTRA,
            logic.dark_skies_requirement
        ),
        make_location_data(SC2Mission.DARK_SKIES.mission_name, "Remainder of Dominion Fleet", SC2NCO_LOC_ID_OFFSET + 802, LocationType.EXTRA,
            logic.dark_skies_requirement
        ),
        make_location_data(SC2Mission.DARK_SKIES.mission_name, "Ji'nara", SC2NCO_LOC_ID_OFFSET + 803, LocationType.EXTRA,
            logic.dark_skies_requirement
        ),
        make_location_data(SC2Mission.DARK_SKIES.mission_name, "Science Facility", SC2NCO_LOC_ID_OFFSET + 804, LocationType.VANILLA,
            logic.dark_skies_requirement
        ),
        make_location_data(SC2Mission.END_GAME.mission_name, "Victory", SC2NCO_LOC_ID_OFFSET + 900, LocationType.VICTORY,
            lambda state: logic.end_game_requirement(state) and logic.nova_any_weapon(state)
        ),
        make_location_data(SC2Mission.END_GAME.mission_name, "Xanthos", SC2NCO_LOC_ID_OFFSET + 901, LocationType.VANILLA,
            logic.end_game_requirement
        ),

        # Mission Variants
        # 10X/20X - Liberation Day
        make_location_data(SC2Mission.THE_OUTLAWS_Z.mission_name, "Victory", SC2_RACESWAP_LOC_ID_OFFSET + 300, LocationType.VICTORY,
            logic.zerg_common_unit
        ),
        make_location_data(SC2Mission.THE_OUTLAWS_Z.mission_name, "Rebel Base", SC2_RACESWAP_LOC_ID_OFFSET + 301, LocationType.VANILLA,
            logic.zerg_common_unit
        ),
        make_location_data(SC2Mission.THE_OUTLAWS_Z.mission_name, "North Resource Pickups", SC2_RACESWAP_LOC_ID_OFFSET + 302, LocationType.EXTRA,
            logic.zerg_common_unit
        ),
        make_location_data(SC2Mission.THE_OUTLAWS_Z.mission_name, "Bunker", SC2_RACESWAP_LOC_ID_OFFSET + 303, LocationType.VANILLA,
            logic.zerg_common_unit
        ),
        make_location_data(SC2Mission.THE_OUTLAWS_Z.mission_name, "Close Resource Pickups", SC2_RACESWAP_LOC_ID_OFFSET + 304, LocationType.EXTRA),
        make_location_data(SC2Mission.THE_OUTLAWS_P.mission_name, "Victory", SC2_RACESWAP_LOC_ID_OFFSET + 400, LocationType.VICTORY,
            logic.protoss_common_unit
        ),
        make_location_data(SC2Mission.THE_OUTLAWS_P.mission_name, "Rebel Base", SC2_RACESWAP_LOC_ID_OFFSET + 401, LocationType.VANILLA,
            logic.protoss_common_unit
        ),
        make_location_data(SC2Mission.THE_OUTLAWS_P.mission_name, "North Resource Pickups", SC2_RACESWAP_LOC_ID_OFFSET + 402, LocationType.EXTRA,
            logic.protoss_common_unit
        ),
        make_location_data(SC2Mission.THE_OUTLAWS_P.mission_name, "Bunker", SC2_RACESWAP_LOC_ID_OFFSET + 403, LocationType.VANILLA,
            logic.protoss_common_unit
        ),
        make_location_data(SC2Mission.THE_OUTLAWS_P.mission_name, "Close Resource Pickups", SC2_RACESWAP_LOC_ID_OFFSET + 404, LocationType.EXTRA),
        make_location_data(SC2Mission.ZERO_HOUR_Z.mission_name, "Victory", SC2_RACESWAP_LOC_ID_OFFSET + 500, LocationType.VICTORY,
            lambda state: (
                logic.zerg_competent_defense(state)
                and logic.zerg_basic_kerriganless_anti_air(state))
        ),
        make_location_data(SC2Mission.ZERO_HOUR_Z.mission_name, "First Group Rescued", SC2_RACESWAP_LOC_ID_OFFSET + 501, LocationType.VANILLA),
        make_location_data(SC2Mission.ZERO_HOUR_Z.mission_name, "Second Group Rescued", SC2_RACESWAP_LOC_ID_OFFSET + 502, LocationType.VANILLA,
            logic.zerg_common_unit
        ),
        make_location_data(SC2Mission.ZERO_HOUR_Z.mission_name, "Third Group Rescued", SC2_RACESWAP_LOC_ID_OFFSET + 503, LocationType.VANILLA,
            logic.zerg_competent_defense
        ),
        make_location_data(SC2Mission.ZERO_HOUR_Z.mission_name, "First Hatchery", SC2_RACESWAP_LOC_ID_OFFSET + 504, LocationType.CHALLENGE,
            logic.zerg_competent_comp
        ),
        make_location_data(SC2Mission.ZERO_HOUR_Z.mission_name, "Second Hatchery", SC2_RACESWAP_LOC_ID_OFFSET + 505, LocationType.CHALLENGE,
            logic.zerg_competent_comp
        ),
        make_location_data(SC2Mission.ZERO_HOUR_Z.mission_name, "Third Hatchery", SC2_RACESWAP_LOC_ID_OFFSET + 506, LocationType.CHALLENGE,
            logic.zerg_competent_comp
        ),
        make_location_data(SC2Mission.ZERO_HOUR_Z.mission_name, "Fourth Hatchery", SC2_RACESWAP_LOC_ID_OFFSET + 507, LocationType.CHALLENGE,
            logic.zerg_competent_comp
        ),
        make_location_data(SC2Mission.ZERO_HOUR_Z.mission_name, "Ride's on its Way", SC2_RACESWAP_LOC_ID_OFFSET + 508, LocationType.EXTRA,
            logic.zerg_common_unit
        ),
        make_location_data(SC2Mission.ZERO_HOUR_Z.mission_name, "Hold Just a Little Longer", SC2_RACESWAP_LOC_ID_OFFSET + 509,
                     LocationType.EXTRA,
            logic.zerg_competent_defense
        ),
        make_location_data(SC2Mission.ZERO_HOUR_Z.mission_name, "Cavalry's on the Way", SC2_RACESWAP_LOC_ID_OFFSET + 510, LocationType.EXTRA,
            logic.zerg_competent_defense
        ),
        make_location_data(SC2Mission.ZERO_HOUR_P.mission_name, "Victory", SC2_RACESWAP_LOC_ID_OFFSET + 600, LocationType.VICTORY,
            lambda state: (
                logic.protoss_common_unit(state)
                and (adv_tactics or logic.protoss_basic_anti_air(state)))
        ),
        make_location_data(SC2Mission.ZERO_HOUR_P.mission_name, "First Group Rescued", SC2_RACESWAP_LOC_ID_OFFSET + 601, LocationType.VANILLA),
        make_location_data(SC2Mission.ZERO_HOUR_P.mission_name, "Second Group Rescued", SC2_RACESWAP_LOC_ID_OFFSET + 602, LocationType.VANILLA,
            logic.protoss_common_unit
        ),
        make_location_data(SC2Mission.ZERO_HOUR_P.mission_name, "Third Group Rescued", SC2_RACESWAP_LOC_ID_OFFSET + 603, LocationType.VANILLA,
            logic.protoss_common_unit
        ),
        make_location_data(SC2Mission.ZERO_HOUR_P.mission_name, "First Hatchery", SC2_RACESWAP_LOC_ID_OFFSET + 604, LocationType.CHALLENGE,
            logic.protoss_competent_comp
        ),
        make_location_data(SC2Mission.ZERO_HOUR_P.mission_name, "Second Hatchery", SC2_RACESWAP_LOC_ID_OFFSET + 605, LocationType.CHALLENGE,
            logic.protoss_competent_comp
        ),
        make_location_data(SC2Mission.ZERO_HOUR_P.mission_name, "Third Hatchery", SC2_RACESWAP_LOC_ID_OFFSET + 606, LocationType.CHALLENGE,
            logic.protoss_competent_comp
        ),
        make_location_data(SC2Mission.ZERO_HOUR_P.mission_name, "Fourth Hatchery", SC2_RACESWAP_LOC_ID_OFFSET + 607, LocationType.CHALLENGE,
            logic.protoss_competent_comp
        ),
        make_location_data(SC2Mission.ZERO_HOUR_P.mission_name, "Ride's on its Way", SC2_RACESWAP_LOC_ID_OFFSET + 608, LocationType.EXTRA,
            logic.protoss_common_unit
        ),
        make_location_data(SC2Mission.ZERO_HOUR_P.mission_name, "Hold Just a Little Longer", SC2_RACESWAP_LOC_ID_OFFSET + 609,
                     LocationType.EXTRA,
            logic.protoss_common_unit
        ),
        make_location_data(SC2Mission.ZERO_HOUR_P.mission_name, "Cavalry's on the Way", SC2_RACESWAP_LOC_ID_OFFSET + 610, LocationType.EXTRA,
            logic.protoss_common_unit
        ),
        make_location_data(SC2Mission.EVACUATION_Z.mission_name, "Victory", SC2_RACESWAP_LOC_ID_OFFSET + 700, LocationType.VICTORY,
            lambda state: (
                logic.zerg_common_unit(state)
                and (logic.zerg_competent_anti_air(state)
                    or (adv_tactics
                        and logic.zerg_basic_kerriganless_anti_air(state)
                    )
                ))
        ),
        make_location_data(SC2Mission.EVACUATION_Z.mission_name, "North Chrysalis", SC2_RACESWAP_LOC_ID_OFFSET + 701, LocationType.VANILLA),
        make_location_data(SC2Mission.EVACUATION_Z.mission_name, "West Chrysalis", SC2_RACESWAP_LOC_ID_OFFSET + 702, LocationType.VANILLA,
            logic.zerg_common_unit
        ),
        make_location_data(SC2Mission.EVACUATION_Z.mission_name, "East Chrysalis", SC2_RACESWAP_LOC_ID_OFFSET + 703, LocationType.VANILLA,
            logic.zerg_common_unit
        ),
        make_location_data(SC2Mission.EVACUATION_Z.mission_name, "Reach Hanson", SC2_RACESWAP_LOC_ID_OFFSET + 704, LocationType.EXTRA),
        make_location_data(SC2Mission.EVACUATION_Z.mission_name, "Secret Resource Stash", SC2_RACESWAP_LOC_ID_OFFSET + 705, LocationType.EXTRA),
        make_location_data(SC2Mission.EVACUATION_Z.mission_name, "Flawless", SC2_RACESWAP_LOC_ID_OFFSET + 706, LocationType.CHALLENGE,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_competent_defense(state)
                and ((adv_tactics and logic.zerg_basic_kerriganless_anti_air(state))
                    or logic.zerg_competent_anti_air(state)
                )),
            flags=LocationFlag.PREVENTATIVE
        ),
        make_location_data(SC2Mission.EVACUATION_P.mission_name, "Victory", SC2_RACESWAP_LOC_ID_OFFSET + 800, LocationType.VICTORY,
            lambda state: (
                logic.protoss_common_unit(state)
                and ((adv_tactics and logic.protoss_basic_anti_air(state))
                    or logic.protoss_competent_anti_air(state)
                ))
        ),
        make_location_data(SC2Mission.EVACUATION_P.mission_name, "North Chrysalis", SC2_RACESWAP_LOC_ID_OFFSET + 801, LocationType.VANILLA),
        make_location_data(SC2Mission.EVACUATION_P.mission_name, "West Chrysalis", SC2_RACESWAP_LOC_ID_OFFSET + 802, LocationType.VANILLA,
            logic.protoss_common_unit
        ),
        make_location_data(SC2Mission.EVACUATION_P.mission_name, "East Chrysalis", SC2_RACESWAP_LOC_ID_OFFSET + 803, LocationType.VANILLA,
            logic.protoss_common_unit
        ),
        make_location_data(SC2Mission.EVACUATION_P.mission_name, "Reach Hanson", SC2_RACESWAP_LOC_ID_OFFSET + 804, LocationType.EXTRA),
        make_location_data(SC2Mission.EVACUATION_P.mission_name, "Secret Resource Stash", SC2_RACESWAP_LOC_ID_OFFSET + 805, LocationType.EXTRA),
        make_location_data(SC2Mission.EVACUATION_P.mission_name, "Flawless", SC2_RACESWAP_LOC_ID_OFFSET + 806, LocationType.CHALLENGE,
            lambda state: (
                logic.protoss_defense_rating(state, True) >= 2
                and logic.protoss_common_unit(state)
                and ((adv_tactics and logic.protoss_basic_anti_air(state))
                    or logic.protoss_competent_anti_air(state)
                )),
            flags=LocationFlag.PREVENTATIVE
        ),
        make_location_data(SC2Mission.OUTBREAK_Z.mission_name, "Victory", SC2_RACESWAP_LOC_ID_OFFSET + 900, LocationType.VICTORY,
            lambda state: (
                logic.zerg_defense_rating(state, True, False) >= 4
                and logic.zerg_common_unit(state))
        ),
        make_location_data(SC2Mission.OUTBREAK_Z.mission_name, "Left Infestor", SC2_RACESWAP_LOC_ID_OFFSET + 901, LocationType.VANILLA,
            lambda state: (
                logic.zerg_defense_rating(state, True, False) >= 2
                and logic.zerg_common_unit(state))
        ),
        make_location_data(SC2Mission.OUTBREAK_Z.mission_name, "Right Infestor", SC2_RACESWAP_LOC_ID_OFFSET + 902, LocationType.VANILLA,
            lambda state: (
                logic.zerg_defense_rating(state, True, False) >= 2
                and logic.zerg_common_unit(state))
        ),
        make_location_data(SC2Mission.OUTBREAK_Z.mission_name, "North Infested Command Center", SC2_RACESWAP_LOC_ID_OFFSET + 903, LocationType.EXTRA,
            lambda state: (
                logic.zerg_defense_rating(state, True, False) >= 2
                and logic.zerg_common_unit(state))
        ),
        make_location_data(SC2Mission.OUTBREAK_Z.mission_name, "South Infested Command Center", SC2_RACESWAP_LOC_ID_OFFSET + 904, LocationType.EXTRA,
            lambda state: (
                logic.zerg_defense_rating(state, True, False) >= 2
                and logic.zerg_common_unit(state))
        ),
        make_location_data(SC2Mission.OUTBREAK_Z.mission_name, "Northwest Bar", SC2_RACESWAP_LOC_ID_OFFSET + 905, LocationType.EXTRA,
            lambda state: (
                logic.zerg_defense_rating(state, True, False) >= 2
                and logic.zerg_common_unit(state))
        ),
        make_location_data(SC2Mission.OUTBREAK_Z.mission_name, "North Bar", SC2_RACESWAP_LOC_ID_OFFSET + 906, LocationType.EXTRA,
            lambda state: (
                logic.zerg_defense_rating(state, True, False) >= 2
                and logic.zerg_common_unit(state))
        ),
        make_location_data(SC2Mission.OUTBREAK_Z.mission_name, "South Bar", SC2_RACESWAP_LOC_ID_OFFSET + 907, LocationType.EXTRA,
            lambda state: (
                logic.zerg_defense_rating(state, True, False) >= 2
                and logic.zerg_common_unit(state))
        ),
        make_location_data(SC2Mission.OUTBREAK_P.mission_name, "Victory", SC2_RACESWAP_LOC_ID_OFFSET + 1000, LocationType.VICTORY,
            lambda state: (
                logic.protoss_defense_rating(state, True) >= 4
                and logic.protoss_common_unit(state))
        ),
        make_location_data(SC2Mission.OUTBREAK_P.mission_name, "Left Infestor", SC2_RACESWAP_LOC_ID_OFFSET + 1001, LocationType.VANILLA,
            lambda state: (
                logic.protoss_defense_rating(state, True) >= 2
                and logic.protoss_common_unit(state))
        ),
        make_location_data(SC2Mission.OUTBREAK_P.mission_name, "Right Infestor", SC2_RACESWAP_LOC_ID_OFFSET + 1002, LocationType.VANILLA,
            lambda state: (
                logic.protoss_defense_rating(state, True) >= 2
                and logic.protoss_common_unit(state))
        ),
        make_location_data(SC2Mission.OUTBREAK_P.mission_name, "North Infested Command Center", SC2_RACESWAP_LOC_ID_OFFSET + 1003, LocationType.EXTRA,
            lambda state: (
                logic.protoss_defense_rating(state, True) >= 2
                and logic.protoss_common_unit(state))
        ),
        make_location_data(SC2Mission.OUTBREAK_P.mission_name, "South Infested Command Center", SC2_RACESWAP_LOC_ID_OFFSET + 1004, LocationType.EXTRA,
            lambda state: (
                logic.protoss_defense_rating(state, True) >= 2
                and logic.protoss_common_unit(state))
        ),
        make_location_data(SC2Mission.OUTBREAK_P.mission_name, "Northwest Bar", SC2_RACESWAP_LOC_ID_OFFSET + 1005, LocationType.EXTRA,
            lambda state: (
                logic.protoss_defense_rating(state, True) >= 2
                and logic.protoss_common_unit(state))
        ),
        make_location_data(SC2Mission.OUTBREAK_P.mission_name, "North Bar", SC2_RACESWAP_LOC_ID_OFFSET + 1006, LocationType.EXTRA,
            lambda state: (
                logic.protoss_defense_rating(state, True) >= 2
                and logic.protoss_common_unit(state))
        ),
        make_location_data(SC2Mission.OUTBREAK_P.mission_name, "South Bar", SC2_RACESWAP_LOC_ID_OFFSET + 1007, LocationType.EXTRA,
            lambda state: (
                logic.protoss_defense_rating(state, True) >= 2
                and logic.protoss_common_unit(state))
        ),
        # 110X/120X - Safe Haven
        make_location_data(SC2Mission.HAVENS_FALL_Z.mission_name, "Victory", SC2_RACESWAP_LOC_ID_OFFSET + 1300, LocationType.VICTORY,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_competent_anti_air(state)
                and logic.zerg_defense_rating(state, True) >= 3)
        ),
        make_location_data(SC2Mission.HAVENS_FALL_Z.mission_name, "North Hive", SC2_RACESWAP_LOC_ID_OFFSET + 1301, LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_competent_anti_air(state)
                and logic.zerg_defense_rating(state, True) >= 3)
        ),
        make_location_data(SC2Mission.HAVENS_FALL_Z.mission_name, "East Hive", SC2_RACESWAP_LOC_ID_OFFSET + 1302, LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_competent_anti_air(state)
                and logic.zerg_defense_rating(state, True) >= 3)
        ),
        make_location_data(SC2Mission.HAVENS_FALL_Z.mission_name, "South Hive", SC2_RACESWAP_LOC_ID_OFFSET + 1303, LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_competent_anti_air(state)
                and logic.zerg_defense_rating(state, True) >= 3)
        ),
        make_location_data(SC2Mission.HAVENS_FALL_Z.mission_name, "Northeast Colony Base", SC2_RACESWAP_LOC_ID_OFFSET + 1304, LocationType.CHALLENGE,
            logic.zerg_respond_to_colony_infestations
        ),
        make_location_data(SC2Mission.HAVENS_FALL_Z.mission_name, "East Colony Base", SC2_RACESWAP_LOC_ID_OFFSET + 1305, LocationType.CHALLENGE,
            logic.zerg_respond_to_colony_infestations
        ),
        make_location_data(SC2Mission.HAVENS_FALL_Z.mission_name, "Middle Colony Base", SC2_RACESWAP_LOC_ID_OFFSET + 1306, LocationType.CHALLENGE,
            logic.zerg_respond_to_colony_infestations
        ),
        make_location_data(SC2Mission.HAVENS_FALL_Z.mission_name, "Southeast Colony Base", SC2_RACESWAP_LOC_ID_OFFSET + 1307, LocationType.CHALLENGE,
            logic.zerg_respond_to_colony_infestations
        ),
        make_location_data(SC2Mission.HAVENS_FALL_Z.mission_name, "Southwest Colony Base", SC2_RACESWAP_LOC_ID_OFFSET + 1308, LocationType.CHALLENGE,
            logic.zerg_respond_to_colony_infestations
        ),
        make_location_data(SC2Mission.HAVENS_FALL_Z.mission_name, "Southwest Gas Pickups", SC2_RACESWAP_LOC_ID_OFFSET + 1309, LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and state.has(item_names.OVERLORD_VENTRAL_SACS, player)
                and logic.zerg_competent_anti_air(state)
                and logic.zerg_defense_rating(state, True) >= 3)
        ),
        make_location_data(SC2Mission.HAVENS_FALL_Z.mission_name, "East Gas Pickups", SC2_RACESWAP_LOC_ID_OFFSET + 1310, LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and state.has(item_names.OVERLORD_VENTRAL_SACS, player)
                and logic.zerg_competent_anti_air(state)
                and logic.zerg_defense_rating(state, True) >= 3)
        ),
        make_location_data(SC2Mission.HAVENS_FALL_Z.mission_name, "Southeast Gas Pickups", SC2_RACESWAP_LOC_ID_OFFSET + 1311, LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and state.has(item_names.OVERLORD_VENTRAL_SACS, player)
                and logic.zerg_competent_anti_air(state)
                and logic.zerg_defense_rating(state, True) >= 3)
        ),
        make_location_data(SC2Mission.HAVENS_FALL_P.mission_name, "Victory", SC2_RACESWAP_LOC_ID_OFFSET + 1400, LocationType.VICTORY,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_competent_anti_air(state)
                and logic.protoss_defense_rating(state, True) >= 3)
        ),
        make_location_data(SC2Mission.HAVENS_FALL_P.mission_name, "North Hive", SC2_RACESWAP_LOC_ID_OFFSET + 1401, LocationType.VANILLA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_competent_anti_air(state)
                and logic.protoss_defense_rating(state, True) >= 3)
        ),
        make_location_data(SC2Mission.HAVENS_FALL_P.mission_name, "East Hive", SC2_RACESWAP_LOC_ID_OFFSET + 1402, LocationType.VANILLA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_competent_anti_air(state)
                and logic.protoss_defense_rating(state, True) >= 3)
        ),
        make_location_data(SC2Mission.HAVENS_FALL_P.mission_name, "South Hive", SC2_RACESWAP_LOC_ID_OFFSET + 1403, LocationType.VANILLA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_competent_anti_air(state)
                and logic.protoss_defense_rating(state, True) >= 3)
        ),
        make_location_data(SC2Mission.HAVENS_FALL_P.mission_name, "Northeast Colony Base", SC2_RACESWAP_LOC_ID_OFFSET + 1404, LocationType.CHALLENGE,
            logic.protoss_respond_to_colony_infestations
        ),
        make_location_data(SC2Mission.HAVENS_FALL_P.mission_name, "East Colony Base", SC2_RACESWAP_LOC_ID_OFFSET + 1405, LocationType.CHALLENGE,
            logic.protoss_respond_to_colony_infestations
        ),
        make_location_data(SC2Mission.HAVENS_FALL_P.mission_name, "Middle Colony Base", SC2_RACESWAP_LOC_ID_OFFSET + 1406, LocationType.CHALLENGE,
            logic.protoss_respond_to_colony_infestations
        ),
        make_location_data(SC2Mission.HAVENS_FALL_P.mission_name, "Southeast Colony Base", SC2_RACESWAP_LOC_ID_OFFSET + 1407, LocationType.CHALLENGE,
            logic.protoss_respond_to_colony_infestations
        ),
        make_location_data(SC2Mission.HAVENS_FALL_P.mission_name, "Southwest Colony Base", SC2_RACESWAP_LOC_ID_OFFSET + 1408, LocationType.CHALLENGE,
            logic.protoss_respond_to_colony_infestations
        ),
        make_location_data(SC2Mission.HAVENS_FALL_P.mission_name, "Southwest Gas Pickups", SC2_RACESWAP_LOC_ID_OFFSET + 1409, LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state)
                and state.has(item_names.WARP_PRISM, player)
                and logic.protoss_competent_anti_air(state)
                and logic.protoss_defense_rating(state, True) >= 3)
        ),
        make_location_data(SC2Mission.HAVENS_FALL_P.mission_name, "East Gas Pickups", SC2_RACESWAP_LOC_ID_OFFSET + 1410, LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state)
                and state.has(item_names.WARP_PRISM, player)
                and logic.protoss_competent_anti_air(state)
                and logic.protoss_defense_rating(state, True) >= 3)
        ),
        make_location_data(SC2Mission.HAVENS_FALL_P.mission_name, "Southeast Gas Pickups", SC2_RACESWAP_LOC_ID_OFFSET + 1411, LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state)
                and state.has(item_names.WARP_PRISM, player)
                and logic.protoss_competent_anti_air(state)
                and logic.protoss_defense_rating(state, True) >= 3)
        ),
        make_location_data(SC2Mission.SMASH_AND_GRAB_Z.mission_name, "Victory", SC2_RACESWAP_LOC_ID_OFFSET + 1500, LocationType.VICTORY,
            lambda state: (
                logic.zerg_common_unit(state)
                and ((adv_tactics and logic.zerg_basic_anti_air(state))
                    or logic.zerg_competent_anti_air(state)
                ))
        ),
        make_location_data(SC2Mission.SMASH_AND_GRAB_Z.mission_name, "First Relic", SC2_RACESWAP_LOC_ID_OFFSET + 1501, LocationType.VANILLA),
        make_location_data(SC2Mission.SMASH_AND_GRAB_Z.mission_name, "Second Relic", SC2_RACESWAP_LOC_ID_OFFSET + 1502, LocationType.VANILLA),
        make_location_data(SC2Mission.SMASH_AND_GRAB_Z.mission_name, "Third Relic", SC2_RACESWAP_LOC_ID_OFFSET + 1503, LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and  ((adv_tactics and logic.zerg_basic_kerriganless_anti_air(state))
                    or logic.zerg_competent_anti_air(state)
                ))
        ),
        make_location_data(SC2Mission.SMASH_AND_GRAB_Z.mission_name, "Fourth Relic", SC2_RACESWAP_LOC_ID_OFFSET + 1504, LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and ((adv_tactics and logic.zerg_basic_kerriganless_anti_air(state))
                    or logic.zerg_competent_anti_air(state)
                ))
        ),
        make_location_data(SC2Mission.SMASH_AND_GRAB_Z.mission_name, "First Forcefield Area Busted", SC2_RACESWAP_LOC_ID_OFFSET + 1505, LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and ((adv_tactics and logic.zerg_basic_kerriganless_anti_air(state))
                    or logic.zerg_competent_anti_air(state)
                ))
        ),
        make_location_data(SC2Mission.SMASH_AND_GRAB_Z.mission_name, "Second Forcefield Area Busted", SC2_RACESWAP_LOC_ID_OFFSET + 1506, LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and ((adv_tactics and logic.zerg_basic_kerriganless_anti_air(state))
                    or logic.zerg_competent_anti_air(state)
                ))
        ),
        make_location_data(SC2Mission.SMASH_AND_GRAB_P.mission_name, "Victory", SC2_RACESWAP_LOC_ID_OFFSET + 1600, LocationType.VICTORY,
            lambda state: (
                logic.zerg_common_unit(state)
                and ((adv_tactics and logic.zerg_basic_kerriganless_anti_air(state))
                    or logic.zerg_competent_anti_air(state)
                ))
        ),
        make_location_data(SC2Mission.SMASH_AND_GRAB_P.mission_name, "First Relic", SC2_RACESWAP_LOC_ID_OFFSET + 1601, LocationType.VANILLA),
        make_location_data(SC2Mission.SMASH_AND_GRAB_P.mission_name, "Second Relic", SC2_RACESWAP_LOC_ID_OFFSET + 1602, LocationType.VANILLA),
        make_location_data(SC2Mission.SMASH_AND_GRAB_P.mission_name, "Third Relic", SC2_RACESWAP_LOC_ID_OFFSET + 1603, LocationType.VANILLA,
            lambda state: (
                logic.protoss_common_unit(state)
                and ((adv_tactics and logic.protoss_basic_anti_air(state))
                    or logic.protoss_competent_anti_air(state)
                ))
        ),
        make_location_data(SC2Mission.SMASH_AND_GRAB_P.mission_name, "Fourth Relic", SC2_RACESWAP_LOC_ID_OFFSET + 1604, LocationType.VANILLA,
            lambda state: (
                logic.protoss_common_unit(state)
                and ((adv_tactics and logic.protoss_basic_anti_air(state))
                    or logic.protoss_competent_anti_air(state)
                ))
        ),
        make_location_data(SC2Mission.SMASH_AND_GRAB_P.mission_name, "First Forcefield Area Busted", SC2_RACESWAP_LOC_ID_OFFSET + 1605, LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state)
                and ((adv_tactics and logic.protoss_basic_anti_air(state))
                    or logic.protoss_competent_anti_air(state)
                ))
        ),
        make_location_data(SC2Mission.SMASH_AND_GRAB_P.mission_name, "Second Forcefield Area Busted", SC2_RACESWAP_LOC_ID_OFFSET + 1606, LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state)
                and ((adv_tactics and logic.protoss_basic_anti_air(state))
                    or logic.protoss_competent_anti_air(state)
                ))
        ),
    ]

    beat_events = []
    # Filtering out excluded locations
    if world is not None:
        excluded_location_types = get_location_types(world, LocationInclusion.option_disabled)
        plando_locations = get_plando_locations(world)
        exclude_locations = world.options.exclude_locations.value
        location_table = [location for location in location_table
                          if (location.type is LocationType.VICTORY or location.name not in exclude_locations)
                          and location.type not in excluded_location_types
                          or location.name in plando_locations]
    for i, location_data in enumerate(location_table):
        # Removing all item-based logic on No Logic
        if logic_level == RequiredTactics.option_no_logic:
            location_data = location_data._replace(rule=Location.access_rule)
            location_table[i] = location_data
        # Generating Beat event locations
        if location_data.name.endswith((": Victory", ": Defeat")):
            beat_events.append(
                location_data._replace(name="Beat " + location_data.name.rsplit(": ", 1)[0], code=None)
            )
    return tuple(location_table + beat_events)

lookup_location_id_to_type = {loc.code: loc.type for loc in get_locations(None) if loc.code is not None}