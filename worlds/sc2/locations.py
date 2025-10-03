import enum
from typing import List, Tuple, Optional, Callable, NamedTuple, Set, TYPE_CHECKING
from .item import item_names
from .item.item_groups import kerrigan_logic_ultimates
from .options import (
    get_option_value,
    RequiredTactics,
    LocationInclusion,
    KerriganPresence,
    GrantStoryTech,
    get_enabled_campaigns,
)
from .mission_tables import SC2Mission, SC2Campaign

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
VICTORY_CACHE_OFFSET = 90


class SC2Location(Location):
    game: str = "Starcraft2"


class LocationType(enum.IntEnum):
    VICTORY = 0  # Winning a mission
    VANILLA = 1  # Objectives that provided metaprogression in the original campaign, along with a few other locations for a balanced experience
    EXTRA = 2  # Additional locations based on mission progression, collecting in-mission rewards, etc. that do not significantly increase the challenge.
    CHALLENGE = 3  # Challenging objectives, often harder than just completing a mission, and often associated with Achievements
    MASTERY = 4  # Extremely challenging objectives often associated with Masteries and Feats of Strength in the original campaign
    VICTORY_CACHE = 5  # Bonus locations for beating a mission


class LocationFlag(enum.IntFlag):
    NONE = 0
    BASEBUST = enum.auto()
    """Locations about killing challenging bases"""
    SPEEDRUN = enum.auto()
    """Locations that are about doing something fast"""
    PREVENTATIVE = enum.auto()
    """Locations that are about preventing something from happening"""

    def values(self):
        """Hacky iterator for backwards-compatibility with Python <= 3.10. Not necessary on Python 3.11+"""
        return tuple(
            val
            for val in (
                LocationFlag.SPEEDRUN,
                LocationFlag.PREVENTATIVE,
            )
            if val in self
        )


class LocationData(NamedTuple):
    region: str
    name: str
    code: int
    type: LocationType
    rule: Callable[["CollectionState"], bool] = Location.access_rule
    flags: LocationFlag = LocationFlag.NONE
    hard_rule: Optional[Callable[["CollectionState"], bool]] = None


def make_location_data(
    region: str,
    name: str,
    code: int,
    type: LocationType,
    rule: Callable[["CollectionState"], bool] = Location.access_rule,
    flags: LocationFlag = LocationFlag.NONE,
    hard_rule: Optional[Callable[["CollectionState"], bool]] = None,
) -> LocationData:
    return LocationData(region, f"{region}: {name}", code, type, rule, flags, hard_rule)


def get_location_types(world: "SC2World", inclusion_type: int) -> Set[LocationType]:
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
    ]
    excluded_location_types = set()
    for option_name, location_type in exclusion_options:
        if get_option_value(world, option_name) is inclusion_type:
            excluded_location_types.add(location_type)
    return excluded_location_types


def get_location_flags(world: "SC2World", inclusion_type: int) -> LocationFlag:
    """
    :param world: The starcraft 2 world object
    :param inclusion_type: Level of inclusion to check for
    :return: A list of location types that match the inclusion type
    """
    matching_location_flags = LocationFlag.NONE
    if world.options.basebust_locations.value == inclusion_type:
        matching_location_flags |= LocationFlag.BASEBUST
    if world.options.speedrun_locations.value == inclusion_type:
        matching_location_flags |= LocationFlag.SPEEDRUN
    if world.options.preventative_locations.value == inclusion_type:
        matching_location_flags |= LocationFlag.PREVENTATIVE
    return matching_location_flags


def get_plando_locations(world: World) -> List[str]:
    """
    :param multiworld:
    :param player:
    :return: A list of locations affected by a plando in a world
    """
    if world is None:
        return []
    plando_locations = []
    for plando_setting in world.options.plando_items:
        plando_locations += plando_setting.locations

    return plando_locations


def get_locations(world: Optional["SC2World"]) -> Tuple[LocationData, ...]:
    # Note: rules which are ended with or True are rules identified as needed later when restricted units is an option
    if world is None:
        logic_level = int(RequiredTactics.default)
        kerriganless = False
    else:
        logic_level = world.options.required_tactics.value
        kerriganless = (
            world.options.kerrigan_presence.value != KerriganPresence.option_vanilla
            or SC2Campaign.HOTS not in get_enabled_campaigns(world)
        )
    adv_tactics = logic_level != RequiredTactics.option_standard
    if world is not None and world.logic is not None:
        logic = world.logic
    else:
        from .rules import SC2Logic

        logic = SC2Logic(world)
    player = 1 if world is None else world.player
    location_table: List[LocationData] = [
        # WoL
        make_location_data(
            SC2Mission.LIBERATION_DAY.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 100,
            LocationType.VICTORY,
        ),
        make_location_data(
            SC2Mission.LIBERATION_DAY.mission_name,
            "First Statue",
            SC2WOL_LOC_ID_OFFSET + 101,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.LIBERATION_DAY.mission_name,
            "Second Statue",
            SC2WOL_LOC_ID_OFFSET + 102,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.LIBERATION_DAY.mission_name,
            "Third Statue",
            SC2WOL_LOC_ID_OFFSET + 103,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.LIBERATION_DAY.mission_name,
            "Fourth Statue",
            SC2WOL_LOC_ID_OFFSET + 104,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.LIBERATION_DAY.mission_name,
            "Fifth Statue",
            SC2WOL_LOC_ID_OFFSET + 105,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.LIBERATION_DAY.mission_name,
            "Sixth Statue",
            SC2WOL_LOC_ID_OFFSET + 106,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.LIBERATION_DAY.mission_name,
            "Special Delivery",
            SC2WOL_LOC_ID_OFFSET + 107,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.LIBERATION_DAY.mission_name,
            "Transport",
            SC2WOL_LOC_ID_OFFSET + 108,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_OUTLAWS.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 200,
            LocationType.VICTORY,
            logic.terran_early_tech,
        ),
        make_location_data(
            SC2Mission.THE_OUTLAWS.mission_name,
            "Rebel Base",
            SC2WOL_LOC_ID_OFFSET + 201,
            LocationType.VANILLA,
            logic.terran_early_tech,
        ),
        make_location_data(
            SC2Mission.THE_OUTLAWS.mission_name,
            "North Resource Pickups",
            SC2WOL_LOC_ID_OFFSET + 202,
            LocationType.EXTRA,
            logic.terran_early_tech,
        ),
        make_location_data(
            SC2Mission.THE_OUTLAWS.mission_name,
            "Bunker",
            SC2WOL_LOC_ID_OFFSET + 203,
            LocationType.VANILLA,
            logic.terran_early_tech,
        ),
        make_location_data(
            SC2Mission.THE_OUTLAWS.mission_name,
            "Close Resource Pickups",
            SC2WOL_LOC_ID_OFFSET + 204,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 300,
            LocationType.VICTORY,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_defense_rating(state, True) >= 2
                and (adv_tactics or logic.terran_basic_anti_air(state))
            ),
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR.mission_name,
            "First Group Rescued",
            SC2WOL_LOC_ID_OFFSET + 301,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR.mission_name,
            "Second Group Rescued",
            SC2WOL_LOC_ID_OFFSET + 302,
            LocationType.VANILLA,
            logic.terran_common_unit,
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR.mission_name,
            "Third Group Rescued",
            SC2WOL_LOC_ID_OFFSET + 303,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_defense_rating(state, True) >= 2
            ),
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR.mission_name,
            "First Hatchery",
            SC2WOL_LOC_ID_OFFSET + 304,
            LocationType.CHALLENGE,
            logic.terran_competent_comp,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR.mission_name,
            "Second Hatchery",
            SC2WOL_LOC_ID_OFFSET + 305,
            LocationType.CHALLENGE,
            logic.terran_competent_comp,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR.mission_name,
            "Third Hatchery",
            SC2WOL_LOC_ID_OFFSET + 306,
            LocationType.CHALLENGE,
            logic.terran_competent_comp,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR.mission_name,
            "Fourth Hatchery",
            SC2WOL_LOC_ID_OFFSET + 307,
            LocationType.CHALLENGE,
            logic.terran_competent_comp,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR.mission_name,
            "Ride's on its Way",
            SC2WOL_LOC_ID_OFFSET + 308,
            LocationType.EXTRA,
            logic.terran_common_unit,
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR.mission_name,
            "Hold Just a Little Longer",
            SC2WOL_LOC_ID_OFFSET + 309,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_defense_rating(state, True) >= 2
            ),
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR.mission_name,
            "Cavalry's on the Way",
            SC2WOL_LOC_ID_OFFSET + 310,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_defense_rating(state, True) >= 2
            ),
        ),
        make_location_data(
            SC2Mission.EVACUATION.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 400,
            LocationType.VICTORY,
            lambda state: (
                logic.terran_early_tech(state)
                and (
                    (adv_tactics and logic.terran_basic_anti_air(state))
                    or logic.terran_competent_anti_air(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.EVACUATION.mission_name,
            "North Chrysalis",
            SC2WOL_LOC_ID_OFFSET + 401,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.EVACUATION.mission_name,
            "West Chrysalis",
            SC2WOL_LOC_ID_OFFSET + 402,
            LocationType.VANILLA,
            logic.terran_early_tech,
        ),
        make_location_data(
            SC2Mission.EVACUATION.mission_name,
            "East Chrysalis",
            SC2WOL_LOC_ID_OFFSET + 403,
            LocationType.VANILLA,
            logic.terran_early_tech,
        ),
        make_location_data(
            SC2Mission.EVACUATION.mission_name,
            "Reach Hanson",
            SC2WOL_LOC_ID_OFFSET + 404,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.EVACUATION.mission_name,
            "Secret Resource Stash",
            SC2WOL_LOC_ID_OFFSET + 405,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.EVACUATION.mission_name,
            "Flawless",
            SC2WOL_LOC_ID_OFFSET + 406,
            LocationType.CHALLENGE,
            lambda state: (
                logic.terran_early_tech(state)
                and logic.terran_defense_rating(state, True, False) >= 2
                and (
                    (adv_tactics and logic.terran_basic_anti_air(state))
                    or logic.terran_competent_anti_air(state)
                )
            ),
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.EVACUATION.mission_name,
            "Western Zerg Base",
            SC2WOL_LOC_ID_OFFSET + 407,
            LocationType.MASTERY,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_base_trasher(state)
                and logic.terran_competent_anti_air(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.EVACUATION.mission_name,
            "Eastern Zerg Base",
            SC2WOL_LOC_ID_OFFSET + 408,
            LocationType.MASTERY,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_base_trasher(state)
                and logic.terran_competent_anti_air(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.OUTBREAK.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 500,
            LocationType.VICTORY,
            logic.terran_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.OUTBREAK.mission_name,
            "Left Infestor",
            SC2WOL_LOC_ID_OFFSET + 501,
            LocationType.VANILLA,
            logic.terran_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.OUTBREAK.mission_name,
            "Right Infestor",
            SC2WOL_LOC_ID_OFFSET + 502,
            LocationType.VANILLA,
            logic.terran_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.OUTBREAK.mission_name,
            "North Infested Command Center",
            SC2WOL_LOC_ID_OFFSET + 503,
            LocationType.EXTRA,
            logic.terran_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.OUTBREAK.mission_name,
            "South Infested Command Center",
            SC2WOL_LOC_ID_OFFSET + 504,
            LocationType.EXTRA,
            logic.terran_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.OUTBREAK.mission_name,
            "Northwest Bar",
            SC2WOL_LOC_ID_OFFSET + 505,
            LocationType.EXTRA,
            logic.terran_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.OUTBREAK.mission_name,
            "North Bar",
            SC2WOL_LOC_ID_OFFSET + 506,
            LocationType.EXTRA,
            logic.terran_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.OUTBREAK.mission_name,
            "South Bar",
            SC2WOL_LOC_ID_OFFSET + 507,
            LocationType.EXTRA,
            logic.terran_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.SAFE_HAVEN.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 600,
            LocationType.VICTORY,
            logic.terran_safe_haven_requirement,
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.SAFE_HAVEN.mission_name,
            "North Nexus",
            SC2WOL_LOC_ID_OFFSET + 601,
            LocationType.EXTRA,
            logic.terran_safe_haven_requirement,
        ),
        make_location_data(
            SC2Mission.SAFE_HAVEN.mission_name,
            "East Nexus",
            SC2WOL_LOC_ID_OFFSET + 602,
            LocationType.EXTRA,
            logic.terran_safe_haven_requirement,
        ),
        make_location_data(
            SC2Mission.SAFE_HAVEN.mission_name,
            "South Nexus",
            SC2WOL_LOC_ID_OFFSET + 603,
            LocationType.EXTRA,
            logic.terran_safe_haven_requirement,
        ),
        make_location_data(
            SC2Mission.SAFE_HAVEN.mission_name,
            "First Terror Fleet",
            SC2WOL_LOC_ID_OFFSET + 604,
            LocationType.VANILLA,
            logic.terran_safe_haven_requirement,
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.SAFE_HAVEN.mission_name,
            "Second Terror Fleet",
            SC2WOL_LOC_ID_OFFSET + 605,
            LocationType.VANILLA,
            logic.terran_safe_haven_requirement,
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.SAFE_HAVEN.mission_name,
            "Third Terror Fleet",
            SC2WOL_LOC_ID_OFFSET + 606,
            LocationType.VANILLA,
            logic.terran_safe_haven_requirement,
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 700,
            LocationType.VICTORY,
            logic.terran_havens_fall_requirement,
            hard_rule=logic.terran_any_anti_air_or_science_vessels,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL.mission_name,
            "North Hive",
            SC2WOL_LOC_ID_OFFSET + 701,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL.mission_name,
            "East Hive",
            SC2WOL_LOC_ID_OFFSET + 702,
            LocationType.VANILLA,
            logic.terran_havens_fall_requirement,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL.mission_name,
            "South Hive",
            SC2WOL_LOC_ID_OFFSET + 703,
            LocationType.VANILLA,
            logic.terran_havens_fall_requirement,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL.mission_name,
            "Northeast Colony Base",
            SC2WOL_LOC_ID_OFFSET + 704,
            LocationType.CHALLENGE,
            logic.terran_respond_to_colony_infestations,
            hard_rule=logic.terran_any_anti_air_or_science_vessels,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL.mission_name,
            "East Colony Base",
            SC2WOL_LOC_ID_OFFSET + 705,
            LocationType.CHALLENGE,
            logic.terran_respond_to_colony_infestations,
            hard_rule=logic.terran_any_anti_air_or_science_vessels,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL.mission_name,
            "Middle Colony Base",
            SC2WOL_LOC_ID_OFFSET + 706,
            LocationType.CHALLENGE,
            logic.terran_respond_to_colony_infestations,
            hard_rule=logic.terran_any_anti_air_or_science_vessels,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL.mission_name,
            "Southeast Colony Base",
            SC2WOL_LOC_ID_OFFSET + 707,
            LocationType.CHALLENGE,
            logic.terran_respond_to_colony_infestations,
            hard_rule=logic.terran_any_anti_air_or_science_vessels,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL.mission_name,
            "Southwest Colony Base",
            SC2WOL_LOC_ID_OFFSET + 708,
            LocationType.CHALLENGE,
            logic.terran_respond_to_colony_infestations,
            hard_rule=logic.terran_any_anti_air_or_science_vessels,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL.mission_name,
            "Southwest Gas Pickups",
            SC2WOL_LOC_ID_OFFSET + 709,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL.mission_name,
            "East Gas Pickups",
            SC2WOL_LOC_ID_OFFSET + 710,
            LocationType.EXTRA,
            logic.terran_havens_fall_requirement,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL.mission_name,
            "Southeast Gas Pickups",
            SC2WOL_LOC_ID_OFFSET + 711,
            LocationType.EXTRA,
            logic.terran_havens_fall_requirement,
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 800,
            LocationType.VICTORY,
            lambda state: (
                logic.terran_common_unit(state)
                and (
                    adv_tactics
                    and logic.terran_moderate_anti_air(state)
                    or logic.terran_competent_anti_air(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB.mission_name,
            "First Relic",
            SC2WOL_LOC_ID_OFFSET + 801,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB.mission_name,
            "Second Relic",
            SC2WOL_LOC_ID_OFFSET + 802,
            LocationType.VANILLA,
            lambda state: (adv_tactics or logic.terran_common_unit(state)),
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB.mission_name,
            "Third Relic",
            SC2WOL_LOC_ID_OFFSET + 803,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and (
                    adv_tactics
                    and logic.terran_moderate_anti_air(state)
                    or logic.terran_competent_anti_air(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB.mission_name,
            "Fourth Relic",
            SC2WOL_LOC_ID_OFFSET + 804,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and (
                    adv_tactics
                    and logic.terran_moderate_anti_air(state)
                    or logic.terran_competent_anti_air(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB.mission_name,
            "First Forcefield Area Busted",
            SC2WOL_LOC_ID_OFFSET + 805,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and (
                    adv_tactics
                    and logic.terran_moderate_anti_air(state)
                    or logic.terran_competent_anti_air(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB.mission_name,
            "Second Forcefield Area Busted",
            SC2WOL_LOC_ID_OFFSET + 806,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and (
                    adv_tactics
                    and logic.terran_moderate_anti_air(state)
                    or logic.terran_competent_anti_air(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB.mission_name,
            "Defeat Kerrigan",
            SC2WOL_LOC_ID_OFFSET + 807,
            LocationType.MASTERY,
            lambda state: (
                logic.terran_common_unit(state) and logic.terran_base_trasher(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.THE_DIG.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 900,
            LocationType.VICTORY,
            lambda state: (
                (
                    logic.terran_competent_anti_air(state)
                    or adv_tactics
                    and logic.terran_moderate_anti_air(state)
                )
                and logic.terran_defense_rating(state, False, True) >= 8
                and logic.terran_common_unit(state)
                and (logic.marine_medic_upgrade(state) or adv_tactics)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG.mission_name,
            "Left Relic",
            SC2WOL_LOC_ID_OFFSET + 901,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_defense_rating(state, False, False) >= 6
                and logic.terran_common_unit(state)
                and (logic.marine_medic_upgrade(state) or adv_tactics)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG.mission_name,
            "Right Ground Relic",
            SC2WOL_LOC_ID_OFFSET + 902,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_defense_rating(state, False, False) >= 6
                and logic.terran_common_unit(state)
                and (logic.marine_medic_upgrade(state) or adv_tactics)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG.mission_name,
            "Right Cliff Relic",
            SC2WOL_LOC_ID_OFFSET + 903,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_defense_rating(state, False, False) >= 6
                and logic.terran_common_unit(state)
                and (logic.marine_medic_upgrade(state) or adv_tactics)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG.mission_name,
            "Moebius Base",
            SC2WOL_LOC_ID_OFFSET + 904,
            LocationType.EXTRA,
            lambda state: logic.marine_medic_upgrade(state) or adv_tactics,
        ),
        make_location_data(
            SC2Mission.THE_DIG.mission_name,
            "Door Outer Layer",
            SC2WOL_LOC_ID_OFFSET + 905,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_defense_rating(state, False, False) >= 6
                and logic.terran_common_unit(state)
                and (logic.marine_medic_upgrade(state) or adv_tactics)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG.mission_name,
            "Door Thermal Barrier",
            SC2WOL_LOC_ID_OFFSET + 906,
            LocationType.EXTRA,
            lambda state: (
                (
                    logic.terran_competent_anti_air(state)
                    or adv_tactics
                    and logic.terran_moderate_anti_air(state)
                )
                and logic.terran_defense_rating(state, False, True) >= 8
                and logic.terran_common_unit(state)
                and (logic.marine_medic_upgrade(state) or adv_tactics)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG.mission_name,
            "Cutting Through the Core",
            SC2WOL_LOC_ID_OFFSET + 907,
            LocationType.EXTRA,
            lambda state: (
                (
                    logic.terran_competent_anti_air(state)
                    or adv_tactics
                    and logic.terran_moderate_anti_air(state)
                )
                and logic.terran_defense_rating(state, False, True) >= 8
                and logic.terran_common_unit(state)
                and (logic.marine_medic_upgrade(state) or adv_tactics)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG.mission_name,
            "Structure Access Imminent",
            SC2WOL_LOC_ID_OFFSET + 908,
            LocationType.EXTRA,
            lambda state: (
                (
                    logic.terran_competent_anti_air(state)
                    or adv_tactics
                    and logic.terran_moderate_anti_air(state)
                )
                and logic.terran_defense_rating(state, False, True) >= 8
                and logic.terran_common_unit(state)
                and (logic.marine_medic_upgrade(state) or adv_tactics)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG.mission_name,
            "Northwestern Protoss Base",
            SC2WOL_LOC_ID_OFFSET + 909,
            LocationType.MASTERY,
            lambda state: (
                logic.terran_beats_protoss_deathball(state)
                and logic.terran_defense_rating(state, False, True) >= 8
                and logic.terran_common_unit(state)
                and (logic.marine_medic_upgrade(state) or adv_tactics)
                and logic.terran_base_trasher(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.THE_DIG.mission_name,
            "Northeastern Protoss Base",
            SC2WOL_LOC_ID_OFFSET + 910,
            LocationType.MASTERY,
            lambda state: (
                logic.terran_beats_protoss_deathball(state)
                and logic.terran_defense_rating(state, False, True) >= 8
                and logic.terran_common_unit(state)
                and (logic.marine_medic_upgrade(state) or adv_tactics)
                and logic.terran_base_trasher(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.THE_DIG.mission_name,
            "Eastern Protoss Base",
            SC2WOL_LOC_ID_OFFSET + 911,
            LocationType.MASTERY,
            lambda state: (
                logic.terran_beats_protoss_deathball(state)
                and logic.terran_defense_rating(state, False, True) >= 8
                and logic.terran_common_unit(state)
                and logic.terran_base_trasher(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 1000,
            LocationType.VICTORY,
            lambda state: (
                (
                    logic.terran_moderate_anti_air(state)
                    and state.has_any({item_names.MEDIVAC, item_names.HERCULES}, player)
                    or logic.terran_air_anti_air(state)
                )
                and (
                    logic.terran_air(state)
                    or state.has_any({item_names.MEDIVAC, item_names.HERCULES}, player)
                    and logic.terran_common_unit(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR.mission_name,
            "1st Data Core",
            SC2WOL_LOC_ID_OFFSET + 1001,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR.mission_name,
            "2nd Data Core",
            SC2WOL_LOC_ID_OFFSET + 1002,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_air(state)
                or (
                    state.has_any({item_names.MEDIVAC, item_names.HERCULES}, player)
                    and logic.terran_common_unit(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR.mission_name,
            "South Rescue",
            SC2WOL_LOC_ID_OFFSET + 1003,
            LocationType.EXTRA,
            logic.terran_can_rescue,
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR.mission_name,
            "Wall Rescue",
            SC2WOL_LOC_ID_OFFSET + 1004,
            LocationType.EXTRA,
            logic.terran_can_rescue,
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR.mission_name,
            "Mid Rescue",
            SC2WOL_LOC_ID_OFFSET + 1005,
            LocationType.EXTRA,
            logic.terran_can_rescue,
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR.mission_name,
            "Nydus Roof Rescue",
            SC2WOL_LOC_ID_OFFSET + 1006,
            LocationType.EXTRA,
            logic.terran_can_rescue,
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR.mission_name,
            "Alive Inside Rescue",
            SC2WOL_LOC_ID_OFFSET + 1007,
            LocationType.EXTRA,
            logic.terran_can_rescue,
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR.mission_name,
            "Brutalisk",
            SC2WOL_LOC_ID_OFFSET + 1008,
            LocationType.VANILLA,
            lambda state: (
                (
                    logic.terran_moderate_anti_air(state)
                    and state.has_any({item_names.MEDIVAC, item_names.HERCULES}, player)
                    or logic.terran_air_anti_air(state)
                )
                and (
                    logic.terran_air(state)
                    or state.has_any({item_names.MEDIVAC, item_names.HERCULES}, player)
                    and logic.terran_common_unit(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR.mission_name,
            "3rd Data Core",
            SC2WOL_LOC_ID_OFFSET + 1009,
            LocationType.VANILLA,
            lambda state: (
                (
                    logic.terran_moderate_anti_air(state)
                    and state.has_any({item_names.MEDIVAC, item_names.HERCULES}, player)
                    or logic.terran_air_anti_air(state)
                )
                and (
                    logic.terran_air(state)
                    or state.has_any({item_names.MEDIVAC, item_names.HERCULES}, player)
                    and logic.terran_common_unit(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.SUPERNOVA.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 1100,
            LocationType.VICTORY,
            logic.terran_supernova_requirement,
        ),
        make_location_data(
            SC2Mission.SUPERNOVA.mission_name,
            "West Relic",
            SC2WOL_LOC_ID_OFFSET + 1101,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.SUPERNOVA.mission_name,
            "North Relic",
            SC2WOL_LOC_ID_OFFSET + 1102,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.SUPERNOVA.mission_name,
            "South Relic",
            SC2WOL_LOC_ID_OFFSET + 1103,
            LocationType.VANILLA,
            logic.terran_supernova_requirement,
        ),
        make_location_data(
            SC2Mission.SUPERNOVA.mission_name,
            "East Relic",
            SC2WOL_LOC_ID_OFFSET + 1104,
            LocationType.VANILLA,
            logic.terran_supernova_requirement,
        ),
        make_location_data(
            SC2Mission.SUPERNOVA.mission_name,
            "Landing Zone Cleared",
            SC2WOL_LOC_ID_OFFSET + 1105,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.SUPERNOVA.mission_name,
            "Middle Base",
            SC2WOL_LOC_ID_OFFSET + 1106,
            LocationType.EXTRA,
            logic.terran_supernova_requirement,
        ),
        make_location_data(
            SC2Mission.SUPERNOVA.mission_name,
            "Southeast Base",
            SC2WOL_LOC_ID_OFFSET + 1107,
            LocationType.EXTRA,
            logic.terran_supernova_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 1200,
            LocationType.VICTORY,
            logic.terran_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID.mission_name,
            "Landing Zone Cleared",
            SC2WOL_LOC_ID_OFFSET + 1201,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID.mission_name,
            "Expansion Prisoners",
            SC2WOL_LOC_ID_OFFSET + 1202,
            LocationType.VANILLA,
            lambda state: adv_tactics or logic.terran_maw_requirement(state),
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID.mission_name,
            "South Close Prisoners",
            SC2WOL_LOC_ID_OFFSET + 1203,
            LocationType.VANILLA,
            lambda state: adv_tactics or logic.terran_maw_requirement(state),
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID.mission_name,
            "South Far Prisoners",
            SC2WOL_LOC_ID_OFFSET + 1204,
            LocationType.VANILLA,
            logic.terran_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID.mission_name,
            "North Prisoners",
            SC2WOL_LOC_ID_OFFSET + 1205,
            LocationType.VANILLA,
            logic.terran_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID.mission_name,
            "Mothership",
            SC2WOL_LOC_ID_OFFSET + 1206,
            LocationType.EXTRA,
            logic.terran_maw_requirement,
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID.mission_name,
            "Expansion Rip Field Generator",
            SC2WOL_LOC_ID_OFFSET + 1207,
            LocationType.EXTRA,
            lambda state: adv_tactics or logic.terran_maw_requirement(state),
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID.mission_name,
            "Middle Rip Field Generator",
            SC2WOL_LOC_ID_OFFSET + 1208,
            LocationType.EXTRA,
            logic.terran_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID.mission_name,
            "Southeast Rip Field Generator",
            SC2WOL_LOC_ID_OFFSET + 1209,
            LocationType.EXTRA,
            logic.terran_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID.mission_name,
            "Stargate Rip Field Generator",
            SC2WOL_LOC_ID_OFFSET + 1210,
            LocationType.EXTRA,
            logic.terran_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID.mission_name,
            "Northwest Rip Field Generator",
            SC2WOL_LOC_ID_OFFSET + 1211,
            LocationType.CHALLENGE,
            logic.terran_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID.mission_name,
            "West Rip Field Generator",
            SC2WOL_LOC_ID_OFFSET + 1212,
            LocationType.CHALLENGE,
            logic.terran_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID.mission_name,
            "Southwest Rip Field Generator",
            SC2WOL_LOC_ID_OFFSET + 1213,
            LocationType.CHALLENGE,
            logic.terran_maw_requirement,
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 1300,
            LocationType.VICTORY,
            lambda state: (
                adv_tactics
                or logic.terran_moderate_anti_air(state)
                and (
                    logic.terran_common_unit(state)
                    or state.has(item_names.REAPER, player)
                )
            ),
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND.mission_name,
            "Tosh's Miners",
            SC2WOL_LOC_ID_OFFSET + 1301,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND.mission_name,
            "Brutalisk",
            SC2WOL_LOC_ID_OFFSET + 1302,
            LocationType.VANILLA,
            lambda state: adv_tactics
            or logic.terran_common_unit(state)
            or state.has(item_names.REAPER, player),
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND.mission_name,
            "North Reapers",
            SC2WOL_LOC_ID_OFFSET + 1303,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND.mission_name,
            "Middle Reapers",
            SC2WOL_LOC_ID_OFFSET + 1304,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND.mission_name,
            "Southwest Reapers",
            SC2WOL_LOC_ID_OFFSET + 1305,
            LocationType.EXTRA,
            lambda state: adv_tactics
            or logic.terran_common_unit(state)
            or state.has(item_names.REAPER, player),
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND.mission_name,
            "Southeast Reapers",
            SC2WOL_LOC_ID_OFFSET + 1306,
            LocationType.EXTRA,
            lambda state: (
                adv_tactics
                or logic.terran_moderate_anti_air(state)
                and (
                    logic.terran_common_unit(state)
                    or state.has(item_names.REAPER, player)
                )
            ),
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND.mission_name,
            "East Reapers",
            SC2WOL_LOC_ID_OFFSET + 1307,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_moderate_anti_air(state)
                and (
                    adv_tactics
                    or logic.terran_common_unit(state)
                    or state.has(item_names.REAPER, player)
                )
            ),
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND.mission_name,
            "Zerg Cleared",
            SC2WOL_LOC_ID_OFFSET + 1308,
            LocationType.CHALLENGE,
            lambda state: (
                logic.terran_competent_anti_air(state)
                and (
                    logic.terran_common_unit(state)
                    or state.has(item_names.REAPER, player)
                )
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 1400,
            LocationType.VICTORY,
            logic.terran_welcome_to_the_jungle_requirement,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name,
            "Close Relic",
            SC2WOL_LOC_ID_OFFSET + 1401,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name,
            "West Relic",
            SC2WOL_LOC_ID_OFFSET + 1402,
            LocationType.VANILLA,
            logic.terran_welcome_to_the_jungle_requirement,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name,
            "North-East Relic",
            SC2WOL_LOC_ID_OFFSET + 1403,
            LocationType.VANILLA,
            logic.terran_welcome_to_the_jungle_requirement,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name,
            "Middle Base",
            SC2WOL_LOC_ID_OFFSET + 1404,
            LocationType.EXTRA,
            logic.terran_welcome_to_the_jungle_requirement,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name,
            "Protoss Cleared",
            SC2WOL_LOC_ID_OFFSET + 1405,
            LocationType.MASTERY,
            lambda state: (
                logic.terran_welcome_to_the_jungle_requirement(state)
                and logic.terran_beats_protoss_deathball(state)
                and logic.terran_base_trasher(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name,
            "No Terrazine Nodes Sealed",
            SC2WOL_LOC_ID_OFFSET + 1406,
            LocationType.CHALLENGE,
            lambda state: (
                logic.terran_welcome_to_the_jungle_requirement(state)
                and logic.terran_competent_ground_to_air(state)
                and logic.terran_beats_protoss_deathball(state)
            ),
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name,
            "Up to 1 Terrazine Node Sealed",
            SC2WOL_LOC_ID_OFFSET + 1407,
            LocationType.CHALLENGE,
            lambda state: (
                logic.terran_welcome_to_the_jungle_requirement(state)
                and logic.terran_competent_ground_to_air(state)
                and logic.terran_beats_protoss_deathball(state)
            ),
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name,
            "Up to 2 Terrazine Nodes Sealed",
            SC2WOL_LOC_ID_OFFSET + 1408,
            LocationType.CHALLENGE,
            lambda state: (
                logic.terran_welcome_to_the_jungle_requirement(state)
                and logic.terran_beats_protoss_deathball(state)
            ),
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name,
            "Up to 3 Terrazine Nodes Sealed",
            SC2WOL_LOC_ID_OFFSET + 1409,
            LocationType.CHALLENGE,
            lambda state: (
                logic.terran_welcome_to_the_jungle_requirement(state)
                and logic.terran_competent_comp(state)
            ),
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name,
            "Up to 4 Terrazine Nodes Sealed",
            SC2WOL_LOC_ID_OFFSET + 1410,
            LocationType.EXTRA,
            logic.terran_welcome_to_the_jungle_requirement,
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name,
            "Up to 5 Terrazine Nodes Sealed",
            SC2WOL_LOC_ID_OFFSET + 1411,
            LocationType.EXTRA,
            logic.terran_welcome_to_the_jungle_requirement,
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.BREAKOUT.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 1500,
            LocationType.VICTORY,
        ),
        make_location_data(
            SC2Mission.BREAKOUT.mission_name,
            "Diamondback Prison",
            SC2WOL_LOC_ID_OFFSET + 1501,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.BREAKOUT.mission_name,
            "Siege Tank Prison",
            SC2WOL_LOC_ID_OFFSET + 1502,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.BREAKOUT.mission_name,
            "First Checkpoint",
            SC2WOL_LOC_ID_OFFSET + 1503,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.BREAKOUT.mission_name,
            "Second Checkpoint",
            SC2WOL_LOC_ID_OFFSET + 1504,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.GHOST_OF_A_CHANCE.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 1600,
            LocationType.VICTORY,
            logic.ghost_of_a_chance_requirement,
            hard_rule=logic.ghost_of_a_chance_requirement,
        ),
        make_location_data(
            SC2Mission.GHOST_OF_A_CHANCE.mission_name,
            "Terrazine Tank",
            SC2WOL_LOC_ID_OFFSET + 1601,
            LocationType.EXTRA,
            logic.ghost_of_a_chance_requirement,
            hard_rule=logic.ghost_of_a_chance_requirement,
        ),
        make_location_data(
            SC2Mission.GHOST_OF_A_CHANCE.mission_name,
            "Jorium Stockpile",
            SC2WOL_LOC_ID_OFFSET + 1602,
            LocationType.EXTRA,
            logic.ghost_of_a_chance_requirement,
            hard_rule=logic.ghost_of_a_chance_requirement,
        ),
        make_location_data(
            SC2Mission.GHOST_OF_A_CHANCE.mission_name,
            "First Island Spectres",
            SC2WOL_LOC_ID_OFFSET + 1603,
            LocationType.VANILLA,
            logic.ghost_of_a_chance_requirement,
            hard_rule=logic.ghost_of_a_chance_requirement,
        ),
        make_location_data(
            SC2Mission.GHOST_OF_A_CHANCE.mission_name,
            "Second Island Spectres",
            SC2WOL_LOC_ID_OFFSET + 1604,
            LocationType.VANILLA,
            logic.ghost_of_a_chance_requirement,
            hard_rule=logic.ghost_of_a_chance_requirement,
        ),
        make_location_data(
            SC2Mission.GHOST_OF_A_CHANCE.mission_name,
            "Third Island Spectres",
            SC2WOL_LOC_ID_OFFSET + 1605,
            LocationType.VANILLA,
            logic.ghost_of_a_chance_requirement,
            hard_rule=logic.ghost_of_a_chance_requirement,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 1700,
            LocationType.VICTORY,
            lambda state: (
                logic.terran_great_train_robbery_train_stopper(state)
                and logic.terran_basic_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name,
            "North Defiler",
            SC2WOL_LOC_ID_OFFSET + 1701,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name,
            "Mid Defiler",
            SC2WOL_LOC_ID_OFFSET + 1702,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name,
            "South Defiler",
            SC2WOL_LOC_ID_OFFSET + 1703,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name,
            "Close Diamondback",
            SC2WOL_LOC_ID_OFFSET + 1704,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name,
            "Northwest Diamondback",
            SC2WOL_LOC_ID_OFFSET + 1705,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name,
            "North Diamondback",
            SC2WOL_LOC_ID_OFFSET + 1706,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name,
            "Northeast Diamondback",
            SC2WOL_LOC_ID_OFFSET + 1707,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name,
            "Southwest Diamondback",
            SC2WOL_LOC_ID_OFFSET + 1708,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name,
            "Southeast Diamondback",
            SC2WOL_LOC_ID_OFFSET + 1709,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name,
            "Kill Team",
            SC2WOL_LOC_ID_OFFSET + 1710,
            LocationType.CHALLENGE,
            lambda state: (
                (adv_tactics or logic.terran_common_unit(state))
                and logic.terran_great_train_robbery_train_stopper(state)
                and logic.terran_basic_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name,
            "Flawless",
            SC2WOL_LOC_ID_OFFSET + 1711,
            LocationType.CHALLENGE,
            lambda state: (
                logic.terran_great_train_robbery_train_stopper(state)
                and logic.terran_basic_anti_air(state)
            ),
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name,
            "2 Trains Destroyed",
            SC2WOL_LOC_ID_OFFSET + 1712,
            LocationType.EXTRA,
            logic.terran_great_train_robbery_train_stopper,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name,
            "4 Trains Destroyed",
            SC2WOL_LOC_ID_OFFSET + 1713,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_great_train_robbery_train_stopper(state)
                and logic.terran_basic_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name,
            "6 Trains Destroyed",
            SC2WOL_LOC_ID_OFFSET + 1714,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_great_train_robbery_train_stopper(state)
                and logic.terran_basic_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.CUTTHROAT.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 1800,
            LocationType.VICTORY,
            lambda state: (
                logic.terran_common_unit(state)
                and (adv_tactics or logic.terran_moderate_anti_air(state))
            ),
        ),
        make_location_data(
            SC2Mission.CUTTHROAT.mission_name,
            "Mira Han",
            SC2WOL_LOC_ID_OFFSET + 1801,
            LocationType.EXTRA,
            logic.terran_common_unit,
        ),
        make_location_data(
            SC2Mission.CUTTHROAT.mission_name,
            "North Relic",
            SC2WOL_LOC_ID_OFFSET + 1802,
            LocationType.VANILLA,
            logic.terran_common_unit,
        ),
        make_location_data(
            SC2Mission.CUTTHROAT.mission_name,
            "Mid Relic",
            SC2WOL_LOC_ID_OFFSET + 1803,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.CUTTHROAT.mission_name,
            "Southwest Relic",
            SC2WOL_LOC_ID_OFFSET + 1804,
            LocationType.VANILLA,
            logic.terran_common_unit,
        ),
        make_location_data(
            SC2Mission.CUTTHROAT.mission_name,
            "North Command Center",
            SC2WOL_LOC_ID_OFFSET + 1805,
            LocationType.EXTRA,
            logic.terran_common_unit,
        ),
        make_location_data(
            SC2Mission.CUTTHROAT.mission_name,
            "South Command Center",
            SC2WOL_LOC_ID_OFFSET + 1806,
            LocationType.EXTRA,
            logic.terran_common_unit,
        ),
        make_location_data(
            SC2Mission.CUTTHROAT.mission_name,
            "West Command Center",
            SC2WOL_LOC_ID_OFFSET + 1807,
            LocationType.EXTRA,
            logic.terran_common_unit,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 1900,
            LocationType.VICTORY,
            logic.terran_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION.mission_name,
            "Odin",
            SC2WOL_LOC_ID_OFFSET + 1901,
            LocationType.EXTRA,
            logic.marine_medic_upgrade,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION.mission_name,
            "Loki",
            SC2WOL_LOC_ID_OFFSET + 1902,
            LocationType.CHALLENGE,
            logic.terran_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION.mission_name,
            "Lab Devourer",
            SC2WOL_LOC_ID_OFFSET + 1903,
            LocationType.VANILLA,
            logic.marine_medic_upgrade,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION.mission_name,
            "North Devourer",
            SC2WOL_LOC_ID_OFFSET + 1904,
            LocationType.VANILLA,
            logic.terran_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION.mission_name,
            "Southeast Devourer",
            SC2WOL_LOC_ID_OFFSET + 1905,
            LocationType.VANILLA,
            logic.terran_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION.mission_name,
            "West Base",
            SC2WOL_LOC_ID_OFFSET + 1906,
            LocationType.EXTRA,
            logic.terran_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION.mission_name,
            "Northwest Base",
            SC2WOL_LOC_ID_OFFSET + 1907,
            LocationType.EXTRA,
            logic.terran_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION.mission_name,
            "Northeast Base",
            SC2WOL_LOC_ID_OFFSET + 1908,
            LocationType.EXTRA,
            logic.terran_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION.mission_name,
            "Southeast Base",
            SC2WOL_LOC_ID_OFFSET + 1909,
            LocationType.EXTRA,
            logic.terran_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 2000,
            LocationType.VICTORY,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ.mission_name,
            "Tower 1",
            SC2WOL_LOC_ID_OFFSET + 2001,
            LocationType.VANILLA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ.mission_name,
            "Tower 2",
            SC2WOL_LOC_ID_OFFSET + 2002,
            LocationType.VANILLA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ.mission_name,
            "Tower 3",
            SC2WOL_LOC_ID_OFFSET + 2003,
            LocationType.VANILLA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ.mission_name,
            "Science Facility",
            SC2WOL_LOC_ID_OFFSET + 2004,
            LocationType.VANILLA,
            lambda state: adv_tactics or logic.terran_competent_comp(state),
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ.mission_name,
            "All Barracks",
            SC2WOL_LOC_ID_OFFSET + 2005,
            LocationType.EXTRA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ.mission_name,
            "All Factories",
            SC2WOL_LOC_ID_OFFSET + 2006,
            LocationType.EXTRA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ.mission_name,
            "All Starports",
            SC2WOL_LOC_ID_OFFSET + 2007,
            LocationType.EXTRA,
            lambda state: adv_tactics or logic.terran_competent_comp(state),
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ.mission_name,
            "Odin Not Trashed",
            SC2WOL_LOC_ID_OFFSET + 2008,
            LocationType.CHALLENGE,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ.mission_name,
            "Surprise Attack Ends",
            SC2WOL_LOC_ID_OFFSET + 2009,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.PIERCING_OF_THE_SHROUD.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 2100,
            LocationType.VICTORY,
            logic.marine_medic_upgrade,
        ),
        make_location_data(
            SC2Mission.PIERCING_OF_THE_SHROUD.mission_name,
            "Holding Cell Relic",
            SC2WOL_LOC_ID_OFFSET + 2101,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.PIERCING_OF_THE_SHROUD.mission_name,
            "Brutalisk Relic",
            SC2WOL_LOC_ID_OFFSET + 2102,
            LocationType.VANILLA,
            logic.marine_medic_upgrade,
        ),
        make_location_data(
            SC2Mission.PIERCING_OF_THE_SHROUD.mission_name,
            "First Escape Relic",
            SC2WOL_LOC_ID_OFFSET + 2103,
            LocationType.VANILLA,
            logic.marine_medic_upgrade,
        ),
        make_location_data(
            SC2Mission.PIERCING_OF_THE_SHROUD.mission_name,
            "Second Escape Relic",
            SC2WOL_LOC_ID_OFFSET + 2104,
            LocationType.VANILLA,
            logic.marine_medic_upgrade,
        ),
        make_location_data(
            SC2Mission.PIERCING_OF_THE_SHROUD.mission_name,
            "Brutalisk",
            SC2WOL_LOC_ID_OFFSET + 2105,
            LocationType.VANILLA,
            logic.marine_medic_upgrade,
        ),
        make_location_data(
            SC2Mission.PIERCING_OF_THE_SHROUD.mission_name,
            "Fusion Reactor",
            SC2WOL_LOC_ID_OFFSET + 2106,
            LocationType.EXTRA,
            logic.marine_medic_upgrade,
        ),
        make_location_data(
            SC2Mission.PIERCING_OF_THE_SHROUD.mission_name,
            "Entrance Holding Pen",
            SC2WOL_LOC_ID_OFFSET + 2107,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.PIERCING_OF_THE_SHROUD.mission_name,
            "Cargo Bay Warbot",
            SC2WOL_LOC_ID_OFFSET + 2108,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.PIERCING_OF_THE_SHROUD.mission_name,
            "Escape Warbot",
            SC2WOL_LOC_ID_OFFSET + 2109,
            LocationType.EXTRA,
            logic.marine_medic_upgrade,
        ),
        make_location_data(
            SC2Mission.WHISPERS_OF_DOOM.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 2200,
            LocationType.VICTORY,
        ),
        make_location_data(
            SC2Mission.WHISPERS_OF_DOOM.mission_name,
            "First Hatchery",
            SC2WOL_LOC_ID_OFFSET + 2201,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.WHISPERS_OF_DOOM.mission_name,
            "Second Hatchery",
            SC2WOL_LOC_ID_OFFSET + 2202,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.WHISPERS_OF_DOOM.mission_name,
            "Third Hatchery",
            SC2WOL_LOC_ID_OFFSET + 2203,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.WHISPERS_OF_DOOM.mission_name,
            "First Prophecy Fragment",
            SC2WOL_LOC_ID_OFFSET + 2204,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.WHISPERS_OF_DOOM.mission_name,
            "Second Prophecy Fragment",
            SC2WOL_LOC_ID_OFFSET + 2205,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.WHISPERS_OF_DOOM.mission_name,
            "Third Prophecy Fragment",
            SC2WOL_LOC_ID_OFFSET + 2206,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 2300,
            LocationType.VICTORY,
            lambda state: logic.protoss_common_unit(state)
            and logic.protoss_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN.mission_name,
            "Robotics Facility",
            SC2WOL_LOC_ID_OFFSET + 2301,
            LocationType.VANILLA,
            lambda state: adv_tactics or logic.protoss_common_unit(state),
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN.mission_name,
            "Dark Shrine",
            SC2WOL_LOC_ID_OFFSET + 2302,
            LocationType.VANILLA,
            lambda state: adv_tactics or logic.protoss_common_unit(state),
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN.mission_name,
            "Templar Archives",
            SC2WOL_LOC_ID_OFFSET + 2303,
            LocationType.VANILLA,
            lambda state: logic.protoss_common_unit(state)
            and logic.protoss_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN.mission_name,
            "Northeast Base",
            SC2WOL_LOC_ID_OFFSET + 2304,
            LocationType.EXTRA,
            lambda state: logic.protoss_common_unit(state)
            and logic.protoss_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN.mission_name,
            "Southwest Base",
            SC2WOL_LOC_ID_OFFSET + 2305,
            LocationType.CHALLENGE,
            lambda state: logic.protoss_common_unit(state)
            and logic.protoss_competent_anti_air(state),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN.mission_name,
            "Maar",
            SC2WOL_LOC_ID_OFFSET + 2306,
            LocationType.EXTRA,
            logic.protoss_common_unit,
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN.mission_name,
            "Northwest Preserver",
            SC2WOL_LOC_ID_OFFSET + 2307,
            LocationType.EXTRA,
            lambda state: logic.protoss_common_unit(state)
            and logic.protoss_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN.mission_name,
            "Southwest Preserver",
            SC2WOL_LOC_ID_OFFSET + 2308,
            LocationType.EXTRA,
            lambda state: logic.protoss_common_unit(state)
            and logic.protoss_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN.mission_name,
            "East Preserver",
            SC2WOL_LOC_ID_OFFSET + 2309,
            LocationType.EXTRA,
            lambda state: logic.protoss_common_unit(state)
            and logic.protoss_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 2400,
            LocationType.VICTORY,
            lambda state: (
                (adv_tactics and logic.protoss_static_defense(state))
                or (
                    logic.protoss_common_unit(state)
                    and logic.protoss_competent_anti_air(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE.mission_name,
            "Close Obelisk",
            SC2WOL_LOC_ID_OFFSET + 2401,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE.mission_name,
            "West Obelisk",
            SC2WOL_LOC_ID_OFFSET + 2402,
            LocationType.VANILLA,
            lambda state: adv_tactics or logic.protoss_common_unit(state),
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE.mission_name,
            "Base",
            SC2WOL_LOC_ID_OFFSET + 2403,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE.mission_name,
            "Southwest Tendril",
            SC2WOL_LOC_ID_OFFSET + 2404,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE.mission_name,
            "Southeast Tendril",
            SC2WOL_LOC_ID_OFFSET + 2405,
            LocationType.EXTRA,
            lambda state: adv_tactics
            and logic.protoss_static_defense(state)
            or logic.protoss_common_unit(state),
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE.mission_name,
            "Northeast Tendril",
            SC2WOL_LOC_ID_OFFSET + 2406,
            LocationType.EXTRA,
            lambda state: adv_tactics
            and logic.protoss_static_defense(state)
            or logic.protoss_common_unit(state),
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE.mission_name,
            "Northwest Tendril",
            SC2WOL_LOC_ID_OFFSET + 2407,
            LocationType.EXTRA,
            lambda state: adv_tactics
            and logic.protoss_static_defense(state)
            or logic.protoss_common_unit(state),
        ),
        make_location_data(
            SC2Mission.IN_UTTER_DARKNESS.mission_name,
            "Defeat",
            SC2WOL_LOC_ID_OFFSET + 2500,
            LocationType.VICTORY,
        ),
        make_location_data(
            SC2Mission.IN_UTTER_DARKNESS.mission_name,
            "Protoss Archive",
            SC2WOL_LOC_ID_OFFSET + 2501,
            LocationType.VANILLA,
            logic.protoss_in_utter_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.IN_UTTER_DARKNESS.mission_name,
            "Kills",
            SC2WOL_LOC_ID_OFFSET + 2502,
            LocationType.VANILLA,
            logic.protoss_in_utter_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.IN_UTTER_DARKNESS.mission_name,
            "Urun",
            SC2WOL_LOC_ID_OFFSET + 2503,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.IN_UTTER_DARKNESS.mission_name,
            "Mohandar",
            SC2WOL_LOC_ID_OFFSET + 2504,
            LocationType.EXTRA,
            logic.protoss_in_utter_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.IN_UTTER_DARKNESS.mission_name,
            "Selendis",
            SC2WOL_LOC_ID_OFFSET + 2505,
            LocationType.EXTRA,
            logic.protoss_in_utter_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.IN_UTTER_DARKNESS.mission_name,
            "Artanis",
            SC2WOL_LOC_ID_OFFSET + 2506,
            LocationType.EXTRA,
            logic.protoss_in_utter_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 2600,
            LocationType.VICTORY,
            logic.terran_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL.mission_name,
            "Large Army",
            SC2WOL_LOC_ID_OFFSET + 2601,
            LocationType.VANILLA,
            logic.terran_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL.mission_name,
            "2 Drop Pods",
            SC2WOL_LOC_ID_OFFSET + 2602,
            LocationType.VANILLA,
            logic.terran_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL.mission_name,
            "4 Drop Pods",
            SC2WOL_LOC_ID_OFFSET + 2603,
            LocationType.VANILLA,
            logic.terran_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL.mission_name,
            "6 Drop Pods",
            SC2WOL_LOC_ID_OFFSET + 2604,
            LocationType.EXTRA,
            logic.terran_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL.mission_name,
            "8 Drop Pods",
            SC2WOL_LOC_ID_OFFSET + 2605,
            LocationType.CHALLENGE,
            logic.terran_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL.mission_name,
            "Southwest Spore Cannon",
            SC2WOL_LOC_ID_OFFSET + 2606,
            LocationType.EXTRA,
            logic.terran_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL.mission_name,
            "Northwest Spore Cannon",
            SC2WOL_LOC_ID_OFFSET + 2607,
            LocationType.EXTRA,
            logic.terran_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL.mission_name,
            "Northeast Spore Cannon",
            SC2WOL_LOC_ID_OFFSET + 2608,
            LocationType.EXTRA,
            logic.terran_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL.mission_name,
            "East Spore Cannon",
            SC2WOL_LOC_ID_OFFSET + 2609,
            LocationType.EXTRA,
            logic.terran_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL.mission_name,
            "Southeast Spore Cannon",
            SC2WOL_LOC_ID_OFFSET + 2610,
            LocationType.EXTRA,
            logic.terran_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL.mission_name,
            "Expansion Spore Cannon",
            SC2WOL_LOC_ID_OFFSET + 2611,
            LocationType.EXTRA,
            logic.terran_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.BELLY_OF_THE_BEAST.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 2700,
            LocationType.VICTORY,
            lambda state: adv_tactics or logic.marine_medic_firebat_upgrade(state),
        ),
        make_location_data(
            SC2Mission.BELLY_OF_THE_BEAST.mission_name,
            "First Charge",
            SC2WOL_LOC_ID_OFFSET + 2701,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.BELLY_OF_THE_BEAST.mission_name,
            "Second Charge",
            SC2WOL_LOC_ID_OFFSET + 2702,
            LocationType.EXTRA,
            lambda state: adv_tactics or logic.marine_medic_firebat_upgrade(state),
        ),
        make_location_data(
            SC2Mission.BELLY_OF_THE_BEAST.mission_name,
            "Third Charge",
            SC2WOL_LOC_ID_OFFSET + 2703,
            LocationType.EXTRA,
            lambda state: adv_tactics or logic.marine_medic_firebat_upgrade(state),
        ),
        make_location_data(
            SC2Mission.BELLY_OF_THE_BEAST.mission_name,
            "First Group Rescued",
            SC2WOL_LOC_ID_OFFSET + 2704,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.BELLY_OF_THE_BEAST.mission_name,
            "Second Group Rescued",
            SC2WOL_LOC_ID_OFFSET + 2705,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.BELLY_OF_THE_BEAST.mission_name,
            "Third Group Rescued",
            SC2WOL_LOC_ID_OFFSET + 2706,
            LocationType.VANILLA,
            lambda state: adv_tactics or logic.marine_medic_firebat_upgrade(state),
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 2800,
            LocationType.VICTORY,
            lambda state: logic.terran_competent_comp(state, 2),
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY.mission_name,
            "Close Coolant Tower",
            SC2WOL_LOC_ID_OFFSET + 2801,
            LocationType.VANILLA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY.mission_name,
            "Northwest Coolant Tower",
            SC2WOL_LOC_ID_OFFSET + 2802,
            LocationType.VANILLA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY.mission_name,
            "Southeast Coolant Tower",
            SC2WOL_LOC_ID_OFFSET + 2803,
            LocationType.VANILLA,
            lambda state: logic.terran_competent_comp(state, 2),
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY.mission_name,
            "Southwest Coolant Tower",
            SC2WOL_LOC_ID_OFFSET + 2804,
            LocationType.VANILLA,
            lambda state: logic.terran_competent_comp(state, 2),
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY.mission_name,
            "Leviathan",
            SC2WOL_LOC_ID_OFFSET + 2805,
            LocationType.VANILLA,
            lambda state: logic.terran_competent_comp(state, 2),
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY.mission_name,
            "East Hatchery",
            SC2WOL_LOC_ID_OFFSET + 2806,
            LocationType.EXTRA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY.mission_name,
            "North Hatchery",
            SC2WOL_LOC_ID_OFFSET + 2807,
            LocationType.EXTRA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY.mission_name,
            "Mid Hatchery",
            SC2WOL_LOC_ID_OFFSET + 2808,
            LocationType.EXTRA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.ALL_IN.mission_name,
            "Victory",
            SC2WOL_LOC_ID_OFFSET + 2900,
            LocationType.VICTORY,
            logic.terran_all_in_requirement,
        ),
        make_location_data(
            SC2Mission.ALL_IN.mission_name,
            "First Kerrigan Attack",
            SC2WOL_LOC_ID_OFFSET + 2901,
            LocationType.EXTRA,
            logic.terran_all_in_requirement,
        ),
        make_location_data(
            SC2Mission.ALL_IN.mission_name,
            "Second Kerrigan Attack",
            SC2WOL_LOC_ID_OFFSET + 2902,
            LocationType.EXTRA,
            logic.terran_all_in_requirement,
        ),
        make_location_data(
            SC2Mission.ALL_IN.mission_name,
            "Third Kerrigan Attack",
            SC2WOL_LOC_ID_OFFSET + 2903,
            LocationType.EXTRA,
            logic.terran_all_in_requirement,
        ),
        make_location_data(
            SC2Mission.ALL_IN.mission_name,
            "Fourth Kerrigan Attack",
            SC2WOL_LOC_ID_OFFSET + 2904,
            LocationType.EXTRA,
            logic.terran_all_in_requirement,
        ),
        make_location_data(
            SC2Mission.ALL_IN.mission_name,
            "Fifth Kerrigan Attack",
            SC2WOL_LOC_ID_OFFSET + 2905,
            LocationType.EXTRA,
            logic.terran_all_in_requirement,
        ),
        # HotS
        make_location_data(
            SC2Mission.LAB_RAT.mission_name,
            "Victory",
            SC2HOTS_LOC_ID_OFFSET + 100,
            LocationType.VICTORY,
            lambda state: (
                logic.zerg_common_unit(state)
                or state.has_any((item_names.ZERGLING, item_names.PYGALISK), player)
            ),
        ),
        make_location_data(
            SC2Mission.LAB_RAT.mission_name,
            "Gather Minerals",
            SC2HOTS_LOC_ID_OFFSET + 101,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.LAB_RAT.mission_name,
            "South Zergling Group",
            SC2HOTS_LOC_ID_OFFSET + 102,
            LocationType.VANILLA,
            lambda state: adv_tactics
            or (
                logic.zerg_common_unit(state)
                or state.has_any((item_names.ZERGLING, item_names.PYGALISK), player)
            ),
        ),
        make_location_data(
            SC2Mission.LAB_RAT.mission_name,
            "East Zergling Group",
            SC2HOTS_LOC_ID_OFFSET + 103,
            LocationType.VANILLA,
            lambda state: adv_tactics
            or (
                logic.zerg_common_unit(state)
                or state.has_any((item_names.ZERGLING, item_names.PYGALISK), player)
            ),
        ),
        make_location_data(
            SC2Mission.LAB_RAT.mission_name,
            "West Zergling Group",
            SC2HOTS_LOC_ID_OFFSET + 104,
            LocationType.VANILLA,
            lambda state: adv_tactics
            or (
                logic.zerg_common_unit(state)
                or state.has_any((item_names.ZERGLING, item_names.PYGALISK), player)
            ),
        ),
        make_location_data(
            SC2Mission.LAB_RAT.mission_name,
            "Hatchery",
            SC2HOTS_LOC_ID_OFFSET + 105,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.LAB_RAT.mission_name,
            "Overlord",
            SC2HOTS_LOC_ID_OFFSET + 106,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.LAB_RAT.mission_name,
            "Gas Turrets",
            SC2HOTS_LOC_ID_OFFSET + 107,
            LocationType.EXTRA,
            lambda state: adv_tactics
            or (
                logic.zerg_common_unit(state)
                or state.has_any((item_names.ZERGLING, item_names.PYGALISK), player)
            ),
        ),
        make_location_data(
            SC2Mission.LAB_RAT.mission_name,
            "Win In Under 10 Minutes",
            SC2HOTS_LOC_ID_OFFSET + 108,
            LocationType.CHALLENGE,
            lambda state: (
                logic.zerg_common_unit(state)
                or state.has_any((item_names.ZERGLING, item_names.PYGALISK), player)
            ),
            flags=LocationFlag.SPEEDRUN,
        ),
        make_location_data(
            SC2Mission.BACK_IN_THE_SADDLE.mission_name,
            "Victory",
            SC2HOTS_LOC_ID_OFFSET + 200,
            LocationType.VICTORY,
            lambda state: logic.basic_kerrigan(state)
                or kerriganless,
            hard_rule=logic.zerg_any_units_back_in_the_saddle_requirement,
        ),
        make_location_data(
            SC2Mission.BACK_IN_THE_SADDLE.mission_name,
            "Defend the Tram",
            SC2HOTS_LOC_ID_OFFSET + 201,
            LocationType.EXTRA,
            lambda state: logic.basic_kerrigan(state)
                or kerriganless,
            hard_rule=logic.zerg_any_units_back_in_the_saddle_requirement,
        ),
        make_location_data(
            SC2Mission.BACK_IN_THE_SADDLE.mission_name,
            "Kinetic Blast",
            SC2HOTS_LOC_ID_OFFSET + 202,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.BACK_IN_THE_SADDLE.mission_name,
            "Crushing Grip",
            SC2HOTS_LOC_ID_OFFSET + 203,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.BACK_IN_THE_SADDLE.mission_name,
            "Reach the Sublevel",
            SC2HOTS_LOC_ID_OFFSET + 204,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.BACK_IN_THE_SADDLE.mission_name,
            "Door Section Cleared",
            SC2HOTS_LOC_ID_OFFSET + 205,
            LocationType.EXTRA,
            lambda state: logic.basic_kerrigan(state)
                or kerriganless,
            hard_rule=logic.zerg_any_units_back_in_the_saddle_requirement,
        ),
        make_location_data(
            SC2Mission.RENDEZVOUS.mission_name,
            "Victory",
            SC2HOTS_LOC_ID_OFFSET + 300,
            LocationType.VICTORY,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state)
                and logic.zerg_defense_rating(state, False, False) >= 3
            ),
        ),
        make_location_data(
            SC2Mission.RENDEZVOUS.mission_name,
            "Right Queen",
            SC2HOTS_LOC_ID_OFFSET + 301,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state)
                and logic.zerg_defense_rating(state, False, False) >= 3
            ),
        ),
        make_location_data(
            SC2Mission.RENDEZVOUS.mission_name,
            "Center Queen",
            SC2HOTS_LOC_ID_OFFSET + 302,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state)
                and logic.zerg_defense_rating(state, False, False) >= 3
            ),
        ),
        make_location_data(
            SC2Mission.RENDEZVOUS.mission_name,
            "Left Queen",
            SC2HOTS_LOC_ID_OFFSET + 303,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state)
                and logic.zerg_defense_rating(state, False, False) >= 3
            ),
        ),
        make_location_data(
            SC2Mission.RENDEZVOUS.mission_name,
            "Hold Out Finished",
            SC2HOTS_LOC_ID_OFFSET + 304,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_basic_anti_air(state)
                and logic.zerg_defense_rating(state, False, False) >= 3
            ),
        ),
        make_location_data(
            SC2Mission.RENDEZVOUS.mission_name,
            "Kill All Buildings Before Reinforcements",
            SC2HOTS_LOC_ID_OFFSET + 305,
            LocationType.MASTERY,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_competent_anti_air(state)
                and (logic.basic_kerrigan(state, False) or kerriganless)
                and logic.zerg_defense_rating(state, False, False) >= 3
                and logic.zerg_power_rating(state) >= 5
            ),
            flags=LocationFlag.SPEEDRUN,
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS.mission_name,
            "Victory",
            SC2HOTS_LOC_ID_OFFSET + 400,
            LocationType.VICTORY,
            lambda state: (
                logic.zerg_common_unit(state) and logic.zerg_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS.mission_name,
            "First Ursadon Matriarch",
            SC2HOTS_LOC_ID_OFFSET + 401,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS.mission_name,
            "North Ursadon Matriarch",
            SC2HOTS_LOC_ID_OFFSET + 402,
            LocationType.VANILLA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS.mission_name,
            "West Ursadon Matriarch",
            SC2HOTS_LOC_ID_OFFSET + 403,
            LocationType.VANILLA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS.mission_name,
            "Lost Brood",
            SC2HOTS_LOC_ID_OFFSET + 404,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS.mission_name,
            "Northeast Psi-link Spire",
            SC2HOTS_LOC_ID_OFFSET + 405,
            LocationType.EXTRA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS.mission_name,
            "Northwest Psi-link Spire",
            SC2HOTS_LOC_ID_OFFSET + 406,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state) and logic.zerg_moderate_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS.mission_name,
            "Southwest Psi-link Spire",
            SC2HOTS_LOC_ID_OFFSET + 407,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state) and logic.zerg_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS.mission_name,
            "Nafash",
            SC2HOTS_LOC_ID_OFFSET + 408,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state) and logic.zerg_moderate_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS.mission_name,
            "20 Unfrozen Structures",
            SC2HOTS_LOC_ID_OFFSET + 409,
            LocationType.CHALLENGE,
            lambda state: (
                logic.zerg_common_unit(state) and logic.zerg_moderate_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER.mission_name,
            "Victory",
            SC2HOTS_LOC_ID_OFFSET + 500,
            LocationType.VICTORY,
            lambda state: (
                logic.zerg_common_unit(state) and logic.zerg_competent_anti_air(state)
            ),
            hard_rule=logic.zerg_any_anti_air,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER.mission_name,
            "East Stasis Chamber",
            SC2HOTS_LOC_ID_OFFSET + 501,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state) and logic.zerg_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER.mission_name,
            "Center Stasis Chamber",
            SC2HOTS_LOC_ID_OFFSET + 502,
            LocationType.VANILLA,
            lambda state: logic.zerg_common_unit(state) or adv_tactics,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER.mission_name,
            "West Stasis Chamber",
            SC2HOTS_LOC_ID_OFFSET + 503,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state) and logic.zerg_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER.mission_name,
            "Destroy 4 Shuttles",
            SC2HOTS_LOC_ID_OFFSET + 504,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state) and logic.zerg_competent_anti_air(state)
            ),
            hard_rule=logic.zerg_any_anti_air,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER.mission_name,
            "Frozen Expansion",
            SC2HOTS_LOC_ID_OFFSET + 505,
            LocationType.EXTRA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER.mission_name,
            "Southwest Frozen Zerg",
            SC2HOTS_LOC_ID_OFFSET + 506,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER.mission_name,
            "Southeast Frozen Zerg",
            SC2HOTS_LOC_ID_OFFSET + 507,
            LocationType.EXTRA,
            lambda state: logic.zerg_common_unit(state) or adv_tactics,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER.mission_name,
            "West Frozen Zerg",
            SC2HOTS_LOC_ID_OFFSET + 508,
            LocationType.EXTRA,
            logic.zerg_common_unit_competent_aa,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER.mission_name,
            "East Frozen Zerg",
            SC2HOTS_LOC_ID_OFFSET + 509,
            LocationType.EXTRA,
            logic.zerg_common_unit_competent_aa,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER.mission_name,
            "West Launch Bay",
            SC2HOTS_LOC_ID_OFFSET + 510,
            LocationType.CHALLENGE,
            logic.zerg_competent_comp_competent_aa,
            hard_rule=logic.zerg_any_anti_air,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER.mission_name,
            "Center Launch Bay",
            SC2HOTS_LOC_ID_OFFSET + 511,
            LocationType.CHALLENGE,
            logic.zerg_competent_comp_competent_aa,
            hard_rule=logic.zerg_any_anti_air,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER.mission_name,
            "East Launch Bay",
            SC2HOTS_LOC_ID_OFFSET + 512,
            LocationType.CHALLENGE,
            logic.zerg_competent_comp_competent_aa,
            hard_rule=logic.zerg_any_anti_air,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.ENEMY_WITHIN.mission_name,
            "Victory",
            SC2HOTS_LOC_ID_OFFSET + 600,
            LocationType.VICTORY,
            lambda state: (
                logic.zerg_pass_vents(state)
                and (
                    logic.grant_story_tech == GrantStoryTech.option_grant
                    or state.has_any(
                        {
                            item_names.ZERGLING_RAPTOR_STRAIN,
                            item_names.ROACH,
                            item_names.HYDRALISK,
                            item_names.INFESTOR,
                        },
                        player,
                    )
                )
            ),
            hard_rule=logic.zerg_pass_vents,
        ),
        make_location_data(
            SC2Mission.ENEMY_WITHIN.mission_name,
            "Infest Giant Ursadon",
            SC2HOTS_LOC_ID_OFFSET + 601,
            LocationType.VANILLA,
            logic.zerg_pass_vents,
            hard_rule=logic.zerg_pass_vents,
        ),
        make_location_data(
            SC2Mission.ENEMY_WITHIN.mission_name,
            "First Niadra Evolution",
            SC2HOTS_LOC_ID_OFFSET + 602,
            LocationType.VANILLA,
            logic.zerg_pass_vents,
        ),
        make_location_data(
            SC2Mission.ENEMY_WITHIN.mission_name,
            "Second Niadra Evolution",
            SC2HOTS_LOC_ID_OFFSET + 603,
            LocationType.VANILLA,
            logic.zerg_pass_vents,
            hard_rule=logic.zerg_pass_vents,
        ),
        make_location_data(
            SC2Mission.ENEMY_WITHIN.mission_name,
            "Third Niadra Evolution",
            SC2HOTS_LOC_ID_OFFSET + 604,
            LocationType.VANILLA,
            logic.zerg_pass_vents,
            hard_rule=logic.zerg_pass_vents,
        ),
        make_location_data(
            SC2Mission.ENEMY_WITHIN.mission_name,
            "Warp Drive",
            SC2HOTS_LOC_ID_OFFSET + 605,
            LocationType.EXTRA,
            logic.zerg_pass_vents,
            hard_rule=logic.zerg_pass_vents,
        ),
        make_location_data(
            SC2Mission.ENEMY_WITHIN.mission_name,
            "Stasis Quadrant",
            SC2HOTS_LOC_ID_OFFSET + 606,
            LocationType.EXTRA,
            logic.zerg_pass_vents,
            hard_rule=logic.zerg_pass_vents,
        ),
        make_location_data(
            SC2Mission.DOMINATION.mission_name,
            "Victory",
            SC2HOTS_LOC_ID_OFFSET + 700,
            LocationType.VICTORY,
            logic.zerg_common_unit_basic_aa,
        ),
        make_location_data(
            SC2Mission.DOMINATION.mission_name,
            "Center Infested Command Center",
            SC2HOTS_LOC_ID_OFFSET + 701,
            LocationType.VANILLA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.DOMINATION.mission_name,
            "North Infested Command Center",
            SC2HOTS_LOC_ID_OFFSET + 702,
            LocationType.VANILLA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.DOMINATION.mission_name,
            "Repel Zagara",
            SC2HOTS_LOC_ID_OFFSET + 703,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.DOMINATION.mission_name,
            "Close Baneling Nest",
            SC2HOTS_LOC_ID_OFFSET + 704,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.DOMINATION.mission_name,
            "South Baneling Nest",
            SC2HOTS_LOC_ID_OFFSET + 705,
            LocationType.EXTRA,
            lambda state: adv_tactics or logic.zerg_common_unit(state),
        ),
        make_location_data(
            SC2Mission.DOMINATION.mission_name,
            "Southwest Baneling Nest",
            SC2HOTS_LOC_ID_OFFSET + 706,
            LocationType.EXTRA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.DOMINATION.mission_name,
            "Southeast Baneling Nest",
            SC2HOTS_LOC_ID_OFFSET + 707,
            LocationType.EXTRA,
            logic.zerg_common_unit_basic_aa,
        ),
        make_location_data(
            SC2Mission.DOMINATION.mission_name,
            "North Baneling Nest",
            SC2HOTS_LOC_ID_OFFSET + 708,
            LocationType.EXTRA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.DOMINATION.mission_name,
            "Northeast Baneling Nest",
            SC2HOTS_LOC_ID_OFFSET + 709,
            LocationType.EXTRA,
            logic.zerg_common_unit_basic_aa,
        ),
        make_location_data(
            SC2Mission.DOMINATION.mission_name,
            "Win Without 100 Eggs",
            SC2HOTS_LOC_ID_OFFSET + 710,
            LocationType.CHALLENGE,
            logic.zerg_competent_comp_competent_aa,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY.mission_name,
            "Victory",
            SC2HOTS_LOC_ID_OFFSET + 800,
            LocationType.VICTORY,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_moderate_anti_air(state)
                and logic.spread_creep(state)
            ),
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY.mission_name,
            "West Biomass",
            SC2HOTS_LOC_ID_OFFSET + 801,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY.mission_name,
            "North Biomass",
            SC2HOTS_LOC_ID_OFFSET + 802,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_moderate_anti_air(state)
                and logic.spread_creep(state)
            ),
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY.mission_name,
            "South Biomass",
            SC2HOTS_LOC_ID_OFFSET + 803,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_moderate_anti_air(state)
                and logic.spread_creep(state)
            ),
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY.mission_name,
            "Destroy 3 Gorgons",
            SC2HOTS_LOC_ID_OFFSET + 804,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_moderate_anti_air(state)
                and logic.spread_creep(state)
            ),
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY.mission_name,
            "Close Zerg Rescue",
            SC2HOTS_LOC_ID_OFFSET + 805,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY.mission_name,
            "South Zerg Rescue",
            SC2HOTS_LOC_ID_OFFSET + 806,
            LocationType.EXTRA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY.mission_name,
            "North Zerg Rescue",
            SC2HOTS_LOC_ID_OFFSET + 807,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_moderate_anti_air(state)
                and logic.spread_creep(state)
            ),
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY.mission_name,
            "West Queen Rescue",
            SC2HOTS_LOC_ID_OFFSET + 808,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_moderate_anti_air(state)
                and logic.spread_creep(state)
            ),
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY.mission_name,
            "East Queen Rescue",
            SC2HOTS_LOC_ID_OFFSET + 809,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_moderate_anti_air(state)
                and logic.spread_creep(state)
            ),
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY.mission_name,
            "South Orbital Command Center",
            SC2HOTS_LOC_ID_OFFSET + 810,
            LocationType.CHALLENGE,
            lambda state: (
                logic.zerg_competent_comp(state) and logic.zerg_moderate_anti_air(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY.mission_name,
            "Northwest Orbital Command Center",
            SC2HOTS_LOC_ID_OFFSET + 811,
            LocationType.CHALLENGE,
            lambda state: (
                logic.zerg_competent_comp(state) and logic.zerg_moderate_anti_air(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY.mission_name,
            "Southeast Orbital Command Center",
            SC2HOTS_LOC_ID_OFFSET + 812,
            LocationType.CHALLENGE,
            lambda state: (
                logic.zerg_competent_comp(state) and logic.zerg_moderate_anti_air(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS.mission_name,
            "Victory",
            SC2HOTS_LOC_ID_OFFSET + 900,
            LocationType.VICTORY,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS.mission_name,
            "East Science Lab",
            SC2HOTS_LOC_ID_OFFSET + 901,
            LocationType.VANILLA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS.mission_name,
            "North Science Lab",
            SC2HOTS_LOC_ID_OFFSET + 902,
            LocationType.VANILLA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS.mission_name,
            "Get Nuked",
            SC2HOTS_LOC_ID_OFFSET + 903,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS.mission_name,
            "Entrance Gate",
            SC2HOTS_LOC_ID_OFFSET + 904,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS.mission_name,
            "Citadel Gate",
            SC2HOTS_LOC_ID_OFFSET + 905,
            LocationType.EXTRA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS.mission_name,
            "South Expansion",
            SC2HOTS_LOC_ID_OFFSET + 906,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS.mission_name,
            "Rich Mineral Expansion",
            SC2HOTS_LOC_ID_OFFSET + 907,
            LocationType.EXTRA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT.mission_name,
            "Victory",
            SC2HOTS_LOC_ID_OFFSET + 1000,
            LocationType.VICTORY,
            logic.zerg_competent_comp_competent_aa,
            hard_rule=logic.zerg_kerrigan_or_any_anti_air,
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT.mission_name,
            "Center Essence Pool",
            SC2HOTS_LOC_ID_OFFSET + 1001,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT.mission_name,
            "East Essence Pool",
            SC2HOTS_LOC_ID_OFFSET + 1002,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and (
                    adv_tactics
                    and logic.zerg_basic_anti_air(state)
                    or logic.zerg_competent_anti_air(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT.mission_name,
            "South Essence Pool",
            SC2HOTS_LOC_ID_OFFSET + 1003,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and (
                    adv_tactics
                    and logic.zerg_basic_anti_air(state)
                    or logic.zerg_competent_anti_air(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT.mission_name,
            "Finish Feeding",
            SC2HOTS_LOC_ID_OFFSET + 1004,
            LocationType.EXTRA,
            logic.zerg_competent_comp_competent_aa,
            hard_rule=logic.zerg_kerrigan_or_any_anti_air,
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT.mission_name,
            "South Proxy Primal Hive",
            SC2HOTS_LOC_ID_OFFSET + 1005,
            LocationType.CHALLENGE,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT.mission_name,
            "East Proxy Primal Hive",
            SC2HOTS_LOC_ID_OFFSET + 1006,
            LocationType.CHALLENGE,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT.mission_name,
            "South Main Primal Hive",
            SC2HOTS_LOC_ID_OFFSET + 1007,
            LocationType.CHALLENGE,
            logic.zerg_competent_comp_competent_aa,
            flags=LocationFlag.BASEBUST,
            hard_rule=logic.zerg_kerrigan_or_any_anti_air,
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT.mission_name,
            "East Main Primal Hive",
            SC2HOTS_LOC_ID_OFFSET + 1008,
            LocationType.CHALLENGE,
            logic.zerg_competent_comp_competent_aa,
            flags=LocationFlag.BASEBUST,
            hard_rule=logic.zerg_kerrigan_or_any_anti_air,
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT.mission_name,
            "Flawless",
            SC2HOTS_LOC_ID_OFFSET + 1009,
            LocationType.CHALLENGE,
            logic.zerg_competent_comp_competent_aa,
            flags=LocationFlag.PREVENTATIVE,
            hard_rule=logic.zerg_kerrigan_or_any_anti_air,
        ),
        make_location_data(
            SC2Mission.THE_CRUCIBLE.mission_name,
            "Victory",
            SC2HOTS_LOC_ID_OFFSET + 1100,
            LocationType.VICTORY,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_defense_rating(state, True, True) >= 7
                and logic.zerg_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_CRUCIBLE.mission_name,
            "Tyrannozor",
            SC2HOTS_LOC_ID_OFFSET + 1101,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_defense_rating(state, True, True) >= 7
                and logic.zerg_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_CRUCIBLE.mission_name,
            "Reach the Pool",
            SC2HOTS_LOC_ID_OFFSET + 1102,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.THE_CRUCIBLE.mission_name,
            "15 Minutes Remaining",
            SC2HOTS_LOC_ID_OFFSET + 1103,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_defense_rating(state, True, True) >= 7
                and logic.zerg_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_CRUCIBLE.mission_name,
            "5 Minutes Remaining",
            SC2HOTS_LOC_ID_OFFSET + 1104,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_defense_rating(state, True, True) >= 7
                and logic.zerg_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_CRUCIBLE.mission_name,
            "Pincer Attack",
            SC2HOTS_LOC_ID_OFFSET + 1105,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_defense_rating(state, True, True) >= 7
                and logic.zerg_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_CRUCIBLE.mission_name,
            "Yagdra Claims Brakk's Pack",
            SC2HOTS_LOC_ID_OFFSET + 1106,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_defense_rating(state, True, True) >= 7
                and logic.zerg_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.SUPREME.mission_name,
            "Victory",
            SC2HOTS_LOC_ID_OFFSET + 1200,
            LocationType.VICTORY,
            logic.supreme_requirement,
            hard_rule=logic.supreme_requirement,
        ),
        make_location_data(
            SC2Mission.SUPREME.mission_name,
            "First Relic",
            SC2HOTS_LOC_ID_OFFSET + 1201,
            LocationType.VANILLA,
            logic.supreme_requirement,
            hard_rule=logic.supreme_requirement,
        ),
        make_location_data(
            SC2Mission.SUPREME.mission_name,
            "Second Relic",
            SC2HOTS_LOC_ID_OFFSET + 1202,
            LocationType.VANILLA,
            logic.supreme_requirement,
            hard_rule=logic.supreme_requirement,
        ),
        make_location_data(
            SC2Mission.SUPREME.mission_name,
            "Third Relic",
            SC2HOTS_LOC_ID_OFFSET + 1203,
            LocationType.VANILLA,
            logic.supreme_requirement,
            hard_rule=logic.supreme_requirement,
        ),
        make_location_data(
            SC2Mission.SUPREME.mission_name,
            "Fourth Relic",
            SC2HOTS_LOC_ID_OFFSET + 1204,
            LocationType.VANILLA,
            logic.supreme_requirement,
            hard_rule=logic.supreme_requirement,
        ),
        make_location_data(
            SC2Mission.SUPREME.mission_name,
            "Yagdra",
            SC2HOTS_LOC_ID_OFFSET + 1205,
            LocationType.EXTRA,
            logic.supreme_requirement,
            hard_rule=logic.supreme_requirement,
        ),
        make_location_data(
            SC2Mission.SUPREME.mission_name,
            "Kraith",
            SC2HOTS_LOC_ID_OFFSET + 1206,
            LocationType.EXTRA,
            logic.supreme_requirement,
            hard_rule=logic.supreme_requirement,
        ),
        make_location_data(
            SC2Mission.SUPREME.mission_name,
            "Slivan",
            SC2HOTS_LOC_ID_OFFSET + 1207,
            LocationType.EXTRA,
            logic.supreme_requirement,
            hard_rule=logic.supreme_requirement,
        ),
        make_location_data(
            SC2Mission.INFESTED.mission_name,
            "Victory",
            SC2HOTS_LOC_ID_OFFSET + 1300,
            LocationType.VICTORY,
            lambda state: (
                logic.zerg_common_unit(state)
                and (
                    (
                        logic.zerg_competent_anti_air(state)
                        and state.has(item_names.INFESTOR, player)
                    )
                    or (adv_tactics and logic.zerg_moderate_anti_air(state))
                )
            ),
            hard_rule=logic.zerg_kerrigan_or_any_anti_air,
        ),
        make_location_data(
            SC2Mission.INFESTED.mission_name,
            "East Science Facility",
            SC2HOTS_LOC_ID_OFFSET + 1301,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_moderate_anti_air(state)
                and logic.spread_creep(state)
            ),
        ),
        make_location_data(
            SC2Mission.INFESTED.mission_name,
            "Center Science Facility",
            SC2HOTS_LOC_ID_OFFSET + 1302,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_moderate_anti_air(state)
                and logic.spread_creep(state)
            ),
        ),
        make_location_data(
            SC2Mission.INFESTED.mission_name,
            "West Science Facility",
            SC2HOTS_LOC_ID_OFFSET + 1303,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_moderate_anti_air(state)
                and logic.spread_creep(state)
            ),
        ),
        make_location_data(
            SC2Mission.INFESTED.mission_name,
            "First Intro Garrison",
            SC2HOTS_LOC_ID_OFFSET + 1304,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.INFESTED.mission_name,
            "Second Intro Garrison",
            SC2HOTS_LOC_ID_OFFSET + 1305,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.INFESTED.mission_name,
            "Base Garrison",
            SC2HOTS_LOC_ID_OFFSET + 1306,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.INFESTED.mission_name,
            "East Garrison",
            SC2HOTS_LOC_ID_OFFSET + 1307,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_moderate_anti_air(state)
                and (adv_tactics or state.has(item_names.INFESTOR, player))
            ),
        ),
        make_location_data(
            SC2Mission.INFESTED.mission_name,
            "Mid Garrison",
            SC2HOTS_LOC_ID_OFFSET + 1308,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_moderate_anti_air(state)
                and (adv_tactics or state.has(item_names.INFESTOR, player))
            ),
        ),
        make_location_data(
            SC2Mission.INFESTED.mission_name,
            "North Garrison",
            SC2HOTS_LOC_ID_OFFSET + 1309,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_moderate_anti_air(state)
                and (adv_tactics or state.has(item_names.INFESTOR, player))
            ),
        ),
        make_location_data(
            SC2Mission.INFESTED.mission_name,
            "Close Southwest Garrison",
            SC2HOTS_LOC_ID_OFFSET + 1310,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_moderate_anti_air(state)
                and (adv_tactics or state.has(item_names.INFESTOR, player))
            ),
        ),
        make_location_data(
            SC2Mission.INFESTED.mission_name,
            "Far Southwest Garrison",
            SC2HOTS_LOC_ID_OFFSET + 1311,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_moderate_anti_air(state)
                and (adv_tactics or state.has(item_names.INFESTOR, player))
            ),
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS.mission_name,
            "Victory",
            SC2HOTS_LOC_ID_OFFSET + 1400,
            LocationType.VICTORY,
            logic.zerg_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS.mission_name,
            "North Brutalisk",
            SC2HOTS_LOC_ID_OFFSET + 1401,
            LocationType.VANILLA,
            logic.zerg_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS.mission_name,
            "South Brutalisk",
            SC2HOTS_LOC_ID_OFFSET + 1402,
            LocationType.VANILLA,
            logic.zerg_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS.mission_name,
            "Kill 1 Hybrid",
            SC2HOTS_LOC_ID_OFFSET + 1403,
            LocationType.EXTRA,
            logic.zerg_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS.mission_name,
            "Kill 2 Hybrid",
            SC2HOTS_LOC_ID_OFFSET + 1404,
            LocationType.EXTRA,
            logic.zerg_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS.mission_name,
            "Kill 3 Hybrid",
            SC2HOTS_LOC_ID_OFFSET + 1405,
            LocationType.EXTRA,
            logic.zerg_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS.mission_name,
            "Kill 4 Hybrid",
            SC2HOTS_LOC_ID_OFFSET + 1406,
            LocationType.EXTRA,
            logic.zerg_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS.mission_name,
            "Kill 5 Hybrid",
            SC2HOTS_LOC_ID_OFFSET + 1407,
            LocationType.EXTRA,
            logic.zerg_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS.mission_name,
            "Kill 6 Hybrid",
            SC2HOTS_LOC_ID_OFFSET + 1408,
            LocationType.EXTRA,
            logic.zerg_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS.mission_name,
            "Kill 7 Hybrid",
            SC2HOTS_LOC_ID_OFFSET + 1409,
            LocationType.EXTRA,
            logic.zerg_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID.mission_name,
            "Victory",
            SC2HOTS_LOC_ID_OFFSET + 1500,
            LocationType.VICTORY,
            lambda state: (
                logic.zerg_competent_comp(state)
                and (
                    logic.zerg_competent_anti_air(state)
                    or (adv_tactics and logic.zerg_moderate_anti_air(state))
                )
            ),
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID.mission_name,
            "Northwest Crystal",
            SC2HOTS_LOC_ID_OFFSET + 1501,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and (
                    logic.zerg_competent_anti_air(state)
                    or (adv_tactics and logic.zerg_moderate_anti_air(state))
                )
            ),
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID.mission_name,
            "Northeast Crystal",
            SC2HOTS_LOC_ID_OFFSET + 1502,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and (
                    logic.zerg_competent_anti_air(state)
                    or (adv_tactics and logic.zerg_moderate_anti_air(state))
                )
            ),
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID.mission_name,
            "South Crystal",
            SC2HOTS_LOC_ID_OFFSET + 1503,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID.mission_name,
            "Base Established",
            SC2HOTS_LOC_ID_OFFSET + 1504,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID.mission_name,
            "Close Temple",
            SC2HOTS_LOC_ID_OFFSET + 1505,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and (
                    logic.zerg_competent_anti_air(state)
                    or (adv_tactics and logic.zerg_moderate_anti_air(state))
                )
            ),
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID.mission_name,
            "Mid Temple",
            SC2HOTS_LOC_ID_OFFSET + 1506,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and (
                    logic.zerg_competent_anti_air(state)
                    or (adv_tactics and logic.zerg_moderate_anti_air(state))
                )
            ),
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID.mission_name,
            "Southeast Temple",
            SC2HOTS_LOC_ID_OFFSET + 1507,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and (
                    logic.zerg_competent_anti_air(state)
                    or (adv_tactics and logic.zerg_moderate_anti_air(state))
                )
            ),
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID.mission_name,
            "Northeast Temple",
            SC2HOTS_LOC_ID_OFFSET + 1508,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and (
                    logic.zerg_competent_anti_air(state)
                    or (adv_tactics and logic.zerg_moderate_anti_air(state))
                )
            ),
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID.mission_name,
            "Northwest Temple",
            SC2HOTS_LOC_ID_OFFSET + 1509,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and (
                    logic.zerg_competent_anti_air(state)
                    or (adv_tactics and logic.zerg_moderate_anti_air(state))
                )
            ),
        ),
        make_location_data(
            SC2Mission.WITH_FRIENDS_LIKE_THESE.mission_name,
            "Victory",
            SC2HOTS_LOC_ID_OFFSET + 1600,
            LocationType.VICTORY,
        ),
        make_location_data(
            SC2Mission.WITH_FRIENDS_LIKE_THESE.mission_name,
            "Pirate Capital Ship",
            SC2HOTS_LOC_ID_OFFSET + 1601,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.WITH_FRIENDS_LIKE_THESE.mission_name,
            "First Mineral Patch",
            SC2HOTS_LOC_ID_OFFSET + 1602,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.WITH_FRIENDS_LIKE_THESE.mission_name,
            "Second Mineral Patch",
            SC2HOTS_LOC_ID_OFFSET + 1603,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.WITH_FRIENDS_LIKE_THESE.mission_name,
            "Third Mineral Patch",
            SC2HOTS_LOC_ID_OFFSET + 1604,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.CONVICTION.mission_name,
            "Victory",
            SC2HOTS_LOC_ID_OFFSET + 1700,
            LocationType.VICTORY,
            lambda state: (
                kerriganless
                or (
                    logic.two_kerrigan_actives(state)
                    and logic.basic_kerrigan(state)
                    and logic.kerrigan_levels(state, 25)
                )
            ),
        ),
        make_location_data(
            SC2Mission.CONVICTION.mission_name,
            "First Secret Documents",
            SC2HOTS_LOC_ID_OFFSET + 1701,
            LocationType.VANILLA,
            lambda state: (
                logic.two_kerrigan_actives(state) and logic.kerrigan_levels(state, 25)
            )
            or kerriganless,
        ),
        make_location_data(
            SC2Mission.CONVICTION.mission_name,
            "Second Secret Documents",
            SC2HOTS_LOC_ID_OFFSET + 1702,
            LocationType.VANILLA,
            lambda state: (
                kerriganless
                or (
                    logic.two_kerrigan_actives(state)
                    and logic.basic_kerrigan(state)
                    and logic.kerrigan_levels(state, 25)
                )
            ),
        ),
        make_location_data(
            SC2Mission.CONVICTION.mission_name,
            "Power Coupling",
            SC2HOTS_LOC_ID_OFFSET + 1703,
            LocationType.EXTRA,
            lambda state: (
                logic.two_kerrigan_actives(state) and logic.kerrigan_levels(state, 25)
            )
            or kerriganless,
        ),
        make_location_data(
            SC2Mission.CONVICTION.mission_name,
            "Door Blasted",
            SC2HOTS_LOC_ID_OFFSET + 1704,
            LocationType.EXTRA,
            lambda state: (
                logic.two_kerrigan_actives(state) and logic.kerrigan_levels(state, 25)
            )
            or kerriganless,
        ),
        make_location_data(
            SC2Mission.PLANETFALL.mission_name,
            "Victory",
            SC2HOTS_LOC_ID_OFFSET + 1800,
            LocationType.VICTORY,
            logic.zerg_planetfall_requirement,
            hard_rule=logic.zerg_kerrigan_or_any_anti_air,
        ),
        make_location_data(
            SC2Mission.PLANETFALL.mission_name,
            "East Gate",
            SC2HOTS_LOC_ID_OFFSET + 1801,
            LocationType.VANILLA,
            logic.zerg_planetfall_requirement,
        ),
        make_location_data(
            SC2Mission.PLANETFALL.mission_name,
            "Northwest Gate",
            SC2HOTS_LOC_ID_OFFSET + 1802,
            LocationType.VANILLA,
            logic.zerg_planetfall_requirement,
        ),
        make_location_data(
            SC2Mission.PLANETFALL.mission_name,
            "North Gate",
            SC2HOTS_LOC_ID_OFFSET + 1803,
            LocationType.VANILLA,
            logic.zerg_planetfall_requirement,
        ),
        make_location_data(
            SC2Mission.PLANETFALL.mission_name,
            "1 Bile Launcher Deployed",
            SC2HOTS_LOC_ID_OFFSET + 1804,
            LocationType.EXTRA,
            logic.zerg_planetfall_requirement,
        ),
        make_location_data(
            SC2Mission.PLANETFALL.mission_name,
            "2 Bile Launchers Deployed",
            SC2HOTS_LOC_ID_OFFSET + 1805,
            LocationType.EXTRA,
            logic.zerg_planetfall_requirement,
        ),
        make_location_data(
            SC2Mission.PLANETFALL.mission_name,
            "3 Bile Launchers Deployed",
            SC2HOTS_LOC_ID_OFFSET + 1806,
            LocationType.EXTRA,
            logic.zerg_planetfall_requirement,
        ),
        make_location_data(
            SC2Mission.PLANETFALL.mission_name,
            "4 Bile Launchers Deployed",
            SC2HOTS_LOC_ID_OFFSET + 1807,
            LocationType.EXTRA,
            logic.zerg_planetfall_requirement,
            hard_rule=logic.zerg_kerrigan_or_any_anti_air,
        ),
        make_location_data(
            SC2Mission.PLANETFALL.mission_name,
            "5 Bile Launchers Deployed",
            SC2HOTS_LOC_ID_OFFSET + 1808,
            LocationType.EXTRA,
            logic.zerg_planetfall_requirement,
            hard_rule=logic.zerg_kerrigan_or_any_anti_air,
        ),
        make_location_data(
            SC2Mission.PLANETFALL.mission_name,
            "Sons of Korhal",
            SC2HOTS_LOC_ID_OFFSET + 1809,
            LocationType.EXTRA,
            logic.zerg_planetfall_requirement,
        ),
        make_location_data(
            SC2Mission.PLANETFALL.mission_name,
            "Night Wolves",
            SC2HOTS_LOC_ID_OFFSET + 1810,
            LocationType.EXTRA,
            logic.zerg_planetfall_requirement,
            hard_rule=logic.zerg_kerrigan_or_any_anti_air,
        ),
        make_location_data(
            SC2Mission.PLANETFALL.mission_name,
            "West Expansion",
            SC2HOTS_LOC_ID_OFFSET + 1811,
            LocationType.EXTRA,
            logic.zerg_planetfall_requirement,
            hard_rule=logic.zerg_kerrigan_or_any_anti_air,
        ),
        make_location_data(
            SC2Mission.PLANETFALL.mission_name,
            "Mid Expansion",
            SC2HOTS_LOC_ID_OFFSET + 1812,
            LocationType.EXTRA,
            logic.zerg_planetfall_requirement,
            hard_rule=logic.zerg_kerrigan_or_any_anti_air,
        ),
        make_location_data(
            SC2Mission.DEATH_FROM_ABOVE.mission_name,
            "Victory",
            SC2HOTS_LOC_ID_OFFSET + 1900,
            LocationType.VICTORY,
            lambda state: logic.zerg_competent_comp_competent_aa(state)
            and (adv_tactics or logic.zerg_base_buster(state)),
        ),
        make_location_data(
            SC2Mission.DEATH_FROM_ABOVE.mission_name,
            "First Power Link",
            SC2HOTS_LOC_ID_OFFSET + 1901,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.DEATH_FROM_ABOVE.mission_name,
            "Second Power Link",
            SC2HOTS_LOC_ID_OFFSET + 1902,
            LocationType.VANILLA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.DEATH_FROM_ABOVE.mission_name,
            "Third Power Link",
            SC2HOTS_LOC_ID_OFFSET + 1903,
            LocationType.VANILLA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.DEATH_FROM_ABOVE.mission_name,
            "Expansion Command Center",
            SC2HOTS_LOC_ID_OFFSET + 1904,
            LocationType.EXTRA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.DEATH_FROM_ABOVE.mission_name,
            "Main Path Command Center",
            SC2HOTS_LOC_ID_OFFSET + 1905,
            LocationType.EXTRA,
            lambda state: logic.zerg_competent_comp_competent_aa(state)
            and (adv_tactics or logic.zerg_base_buster(state)),
        ),
        make_location_data(
            SC2Mission.THE_RECKONING.mission_name,
            "Victory",
            SC2HOTS_LOC_ID_OFFSET + 2000,
            LocationType.VICTORY,
            logic.zerg_the_reckoning_requirement,
        ),
        make_location_data(
            SC2Mission.THE_RECKONING.mission_name,
            "South Lane",
            SC2HOTS_LOC_ID_OFFSET + 2001,
            LocationType.VANILLA,
            logic.zerg_the_reckoning_requirement,
        ),
        make_location_data(
            SC2Mission.THE_RECKONING.mission_name,
            "North Lane",
            SC2HOTS_LOC_ID_OFFSET + 2002,
            LocationType.VANILLA,
            logic.zerg_the_reckoning_requirement,
        ),
        make_location_data(
            SC2Mission.THE_RECKONING.mission_name,
            "East Lane",
            SC2HOTS_LOC_ID_OFFSET + 2003,
            LocationType.VANILLA,
            logic.zerg_the_reckoning_requirement,
        ),
        make_location_data(
            SC2Mission.THE_RECKONING.mission_name,
            "Odin",
            SC2HOTS_LOC_ID_OFFSET + 2004,
            LocationType.EXTRA,
            logic.zerg_the_reckoning_requirement,
        ),
        make_location_data(
            SC2Mission.THE_RECKONING.mission_name,
            "Trash the Odin Early",
            SC2HOTS_LOC_ID_OFFSET + 2005,
            LocationType.MASTERY,
            lambda state: (
                logic.zerg_the_reckoning_requirement(state)
                and (
                    kerriganless
                    or (
                        logic.kerrigan_levels(state, 50, False)
                        and state.has_any(kerrigan_logic_ultimates, player)
                    )
                )
                and logic.zerg_power_rating(state) >= 10
            ),
            flags=LocationFlag.SPEEDRUN,
        ),
        # LotV Prologue
        make_location_data(
            SC2Mission.DARK_WHISPERS.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 100,
            LocationType.VICTORY,
            logic.protoss_common_unit_basic_aa,
        ),
        make_location_data(
            SC2Mission.DARK_WHISPERS.mission_name,
            "First Prisoner Group",
            SC2LOTV_LOC_ID_OFFSET + 101,
            LocationType.VANILLA,
            logic.protoss_common_unit_basic_aa,
        ),
        make_location_data(
            SC2Mission.DARK_WHISPERS.mission_name,
            "Second Prisoner Group",
            SC2LOTV_LOC_ID_OFFSET + 102,
            LocationType.VANILLA,
            logic.protoss_common_unit_basic_aa,
        ),
        make_location_data(
            SC2Mission.DARK_WHISPERS.mission_name,
            "First Pylon",
            SC2LOTV_LOC_ID_OFFSET + 103,
            LocationType.VANILLA,
            logic.protoss_common_unit_basic_aa,
        ),
        make_location_data(
            SC2Mission.DARK_WHISPERS.mission_name,
            "Second Pylon",
            SC2LOTV_LOC_ID_OFFSET + 104,
            LocationType.VANILLA,
            logic.protoss_common_unit_basic_aa,
        ),
        make_location_data(
            SC2Mission.DARK_WHISPERS.mission_name,
            "Zerg Base",
            SC2LOTV_LOC_ID_OFFSET + 105,
            LocationType.MASTERY,
            lambda state: logic.protoss_deathball(state)
            and logic.protoss_power_rating(state) >= 6,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.GHOSTS_IN_THE_FOG.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 200,
            LocationType.VICTORY,
            lambda state: logic.protoss_competent_comp(state)
            and logic.protoss_mineral_dump(state),
        ),
        make_location_data(
            SC2Mission.GHOSTS_IN_THE_FOG.mission_name,
            "South Rock Formation",
            SC2LOTV_LOC_ID_OFFSET + 201,
            LocationType.VANILLA,
            lambda state: logic.protoss_competent_comp(state)
            and logic.protoss_mineral_dump(state),
        ),
        make_location_data(
            SC2Mission.GHOSTS_IN_THE_FOG.mission_name,
            "West Rock Formation",
            SC2LOTV_LOC_ID_OFFSET + 202,
            LocationType.VANILLA,
            lambda state: logic.protoss_competent_comp(state)
            and logic.protoss_mineral_dump(state),
        ),
        make_location_data(
            SC2Mission.GHOSTS_IN_THE_FOG.mission_name,
            "East Rock Formation",
            SC2LOTV_LOC_ID_OFFSET + 203,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_competent_comp(state)
                and logic.protoss_mineral_dump(state)
                and logic.protoss_can_attack_behind_chasm(state)
            ),
        ),
        make_location_data(
            SC2Mission.EVIL_AWOKEN.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 300,
            LocationType.VICTORY,
            lambda state: adv_tactics
            or state.has_any((
                item_names.STALKER_PHASE_REACTOR,
                item_names.STALKER_INSTIGATOR_SLAYER_DISINTEGRATING_PARTICLES,
                item_names.STALKER_INSTIGATOR_SLAYER_PARTICLE_REFLECTION,
            ), player),
        ),
        make_location_data(
            SC2Mission.EVIL_AWOKEN.mission_name,
            "Temple Investigated",
            SC2LOTV_LOC_ID_OFFSET + 301,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.EVIL_AWOKEN.mission_name,
            "Void Catalyst",
            SC2LOTV_LOC_ID_OFFSET + 302,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.EVIL_AWOKEN.mission_name,
            "First Particle Cannon",
            SC2LOTV_LOC_ID_OFFSET + 303,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.EVIL_AWOKEN.mission_name,
            "Second Particle Cannon",
            SC2LOTV_LOC_ID_OFFSET + 304,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.EVIL_AWOKEN.mission_name,
            "Third Particle Cannon",
            SC2LOTV_LOC_ID_OFFSET + 305,
            LocationType.VANILLA,
        ),
        # LotV
        make_location_data(
            SC2Mission.FOR_AIUR.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 400,
            LocationType.VICTORY,
        ),
        make_location_data(
            SC2Mission.FOR_AIUR.mission_name,
            "Southwest Hive",
            SC2LOTV_LOC_ID_OFFSET + 401,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.FOR_AIUR.mission_name,
            "Northwest Hive",
            SC2LOTV_LOC_ID_OFFSET + 402,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.FOR_AIUR.mission_name,
            "Northeast Hive",
            SC2LOTV_LOC_ID_OFFSET + 403,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.FOR_AIUR.mission_name,
            "East Hive",
            SC2LOTV_LOC_ID_OFFSET + 404,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.FOR_AIUR.mission_name,
            "West Conduit",
            SC2LOTV_LOC_ID_OFFSET + 405,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.FOR_AIUR.mission_name,
            "Middle Conduit",
            SC2LOTV_LOC_ID_OFFSET + 406,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.FOR_AIUR.mission_name,
            "Northeast Conduit",
            SC2LOTV_LOC_ID_OFFSET + 407,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_GROWING_SHADOW.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 500,
            LocationType.VICTORY,
            lambda state: logic.protoss_common_unit(state)
            and (adv_tactics or logic.protoss_moderate_anti_air(state)),
        ),
        make_location_data(
            SC2Mission.THE_GROWING_SHADOW.mission_name,
            "Close Pylon",
            SC2LOTV_LOC_ID_OFFSET + 501,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.THE_GROWING_SHADOW.mission_name,
            "East Pylon",
            SC2LOTV_LOC_ID_OFFSET + 502,
            LocationType.VANILLA,
            lambda state: logic.protoss_common_unit(state)
            and (adv_tactics or logic.protoss_moderate_anti_air(state)),
        ),
        make_location_data(
            SC2Mission.THE_GROWING_SHADOW.mission_name,
            "West Pylon",
            SC2LOTV_LOC_ID_OFFSET + 503,
            LocationType.VANILLA,
            lambda state: logic.protoss_common_unit(state)
            and (adv_tactics or logic.protoss_moderate_anti_air(state)),
        ),
        make_location_data(
            SC2Mission.THE_GROWING_SHADOW.mission_name,
            "Nexus",
            SC2LOTV_LOC_ID_OFFSET + 504,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_GROWING_SHADOW.mission_name,
            "Templar Base",
            SC2LOTV_LOC_ID_OFFSET + 505,
            LocationType.EXTRA,
            lambda state: logic.protoss_common_unit(state)
            and (adv_tactics or logic.protoss_moderate_anti_air(state)),
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 600,
            LocationType.VICTORY,
            logic.protoss_spear_of_adun_requirement,
            hard_rule=logic.protoss_any_anti_air_unit_or_soa,
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN.mission_name,
            "Close Warp Gate",
            SC2LOTV_LOC_ID_OFFSET + 601,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN.mission_name,
            "West Warp Gate",
            SC2LOTV_LOC_ID_OFFSET + 602,
            LocationType.VANILLA,
            logic.protoss_spear_of_adun_requirement,
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN.mission_name,
            "North Warp Gate",
            SC2LOTV_LOC_ID_OFFSET + 603,
            LocationType.VANILLA,
            logic.protoss_spear_of_adun_requirement,
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN.mission_name,
            "North Power Cell",
            SC2LOTV_LOC_ID_OFFSET + 604,
            LocationType.EXTRA,
            logic.protoss_spear_of_adun_requirement,
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN.mission_name,
            "East Power Cell",
            SC2LOTV_LOC_ID_OFFSET + 605,
            LocationType.EXTRA,
            logic.protoss_spear_of_adun_requirement,
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN.mission_name,
            "South Power Cell",
            SC2LOTV_LOC_ID_OFFSET + 606,
            LocationType.EXTRA,
            logic.protoss_spear_of_adun_requirement,
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN.mission_name,
            "Southeast Power Cell",
            SC2LOTV_LOC_ID_OFFSET + 607,
            LocationType.EXTRA,
            logic.protoss_spear_of_adun_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 700,
            LocationType.VICTORY,
            logic.protoss_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD.mission_name,
            "Mid EMP Scrambler",
            SC2LOTV_LOC_ID_OFFSET + 701,
            LocationType.VANILLA,
            logic.protoss_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD.mission_name,
            "Southeast EMP Scrambler",
            SC2LOTV_LOC_ID_OFFSET + 702,
            LocationType.VANILLA,
            logic.protoss_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD.mission_name,
            "North EMP Scrambler",
            SC2LOTV_LOC_ID_OFFSET + 703,
            LocationType.VANILLA,
            logic.protoss_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD.mission_name,
            "Mid Stabilizer",
            SC2LOTV_LOC_ID_OFFSET + 704,
            LocationType.EXTRA,
            logic.protoss_common_unit,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD.mission_name,
            "Southwest Stabilizer",
            SC2LOTV_LOC_ID_OFFSET + 705,
            LocationType.EXTRA,
            logic.protoss_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD.mission_name,
            "Northwest Stabilizer",
            SC2LOTV_LOC_ID_OFFSET + 706,
            LocationType.EXTRA,
            logic.protoss_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD.mission_name,
            "Northeast Stabilizer",
            SC2LOTV_LOC_ID_OFFSET + 707,
            LocationType.EXTRA,
            logic.protoss_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD.mission_name,
            "Southeast Stabilizer",
            SC2LOTV_LOC_ID_OFFSET + 708,
            LocationType.EXTRA,
            logic.protoss_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD.mission_name,
            "West Raynor Base",
            SC2LOTV_LOC_ID_OFFSET + 709,
            LocationType.EXTRA,
            logic.protoss_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD.mission_name,
            "East Raynor Base",
            SC2LOTV_LOC_ID_OFFSET + 710,
            LocationType.EXTRA,
            logic.protoss_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.BROTHERS_IN_ARMS.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 800,
            LocationType.VICTORY,
            logic.protoss_brothers_in_arms_requirement,
        ),
        make_location_data(
            SC2Mission.BROTHERS_IN_ARMS.mission_name,
            "Mid Science Facility",
            SC2LOTV_LOC_ID_OFFSET + 801,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.BROTHERS_IN_ARMS.mission_name,
            "North Science Facility",
            SC2LOTV_LOC_ID_OFFSET + 802,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_brothers_in_arms_requirement(state)
                or (
                    logic.take_over_ai_allies
                    and logic.advanced_tactics
                    and (
                        logic.terran_common_unit(state)
                        or logic.protoss_common_unit(state)
                    )
                )
            ),
        ),
        make_location_data(
            SC2Mission.BROTHERS_IN_ARMS.mission_name,
            "South Science Facility",
            SC2LOTV_LOC_ID_OFFSET + 803,
            LocationType.VANILLA,
            logic.protoss_brothers_in_arms_requirement,
        ),
        make_location_data(
            SC2Mission.BROTHERS_IN_ARMS.mission_name,
            "Raynor Forward Positions",
            SC2LOTV_LOC_ID_OFFSET + 804,
            LocationType.EXTRA,
            logic.protoss_brothers_in_arms_requirement,
        ),
        make_location_data(
            SC2Mission.BROTHERS_IN_ARMS.mission_name,
            "Valerian Forward Positions",
            SC2LOTV_LOC_ID_OFFSET + 805,
            LocationType.EXTRA,
            logic.protoss_brothers_in_arms_requirement,
        ),
        make_location_data(
            SC2Mission.BROTHERS_IN_ARMS.mission_name,
            "Win in under 15 minutes",
            SC2LOTV_LOC_ID_OFFSET + 806,
            LocationType.CHALLENGE,
            lambda state: (
                logic.protoss_brothers_in_arms_requirement(state)
                and logic.protoss_deathball(state)
                and logic.protoss_power_rating(state) >= 8
            ),
            flags=LocationFlag.SPEEDRUN,
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 900,
            LocationType.VICTORY,
            logic.protoss_common_unit_anti_light_air,
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH.mission_name,
            "Close Solarite Reserve",
            SC2LOTV_LOC_ID_OFFSET + 901,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH.mission_name,
            "North Solarite Reserve",
            SC2LOTV_LOC_ID_OFFSET + 902,
            LocationType.VANILLA,
            logic.protoss_common_unit_anti_light_air,
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH.mission_name,
            "East Solarite Reserve",
            SC2LOTV_LOC_ID_OFFSET + 903,
            LocationType.VANILLA,
            logic.protoss_common_unit_anti_light_air,
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH.mission_name,
            "West Launch Bay",
            SC2LOTV_LOC_ID_OFFSET + 904,
            LocationType.EXTRA,
            logic.protoss_common_unit_anti_light_air,
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH.mission_name,
            "South Launch Bay",
            SC2LOTV_LOC_ID_OFFSET + 905,
            LocationType.EXTRA,
            logic.protoss_common_unit_anti_light_air,
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH.mission_name,
            "Northwest Launch Bay",
            SC2LOTV_LOC_ID_OFFSET + 906,
            LocationType.EXTRA,
            logic.protoss_common_unit_anti_light_air,
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH.mission_name,
            "East Launch Bay",
            SC2LOTV_LOC_ID_OFFSET + 907,
            LocationType.EXTRA,
            logic.protoss_common_unit_anti_light_air,
        ),
        make_location_data(
            SC2Mission.LAST_STAND.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 1000,
            LocationType.VICTORY,
            logic.protoss_last_stand_requirement,
        ),
        make_location_data(
            SC2Mission.LAST_STAND.mission_name,
            "West Zenith Stone",
            SC2LOTV_LOC_ID_OFFSET + 1001,
            LocationType.VANILLA,
            logic.protoss_last_stand_requirement,
        ),
        make_location_data(
            SC2Mission.LAST_STAND.mission_name,
            "North Zenith Stone",
            SC2LOTV_LOC_ID_OFFSET + 1002,
            LocationType.VANILLA,
            logic.protoss_last_stand_requirement,
        ),
        make_location_data(
            SC2Mission.LAST_STAND.mission_name,
            "East Zenith Stone",
            SC2LOTV_LOC_ID_OFFSET + 1003,
            LocationType.VANILLA,
            logic.protoss_last_stand_requirement,
        ),
        make_location_data(
            SC2Mission.LAST_STAND.mission_name,
            "1 Billion Zerg",
            SC2LOTV_LOC_ID_OFFSET + 1004,
            LocationType.EXTRA,
            logic.protoss_last_stand_requirement,
        ),
        make_location_data(
            SC2Mission.LAST_STAND.mission_name,
            "1.5 Billion Zerg",
            SC2LOTV_LOC_ID_OFFSET + 1005,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_last_stand_requirement(state)
                and (
                    state.has_all(
                        {
                            item_names.KHAYDARIN_MONOLITH,
                            item_names.PHOTON_CANNON,
                            item_names.SHIELD_BATTERY,
                        },
                        player,
                    )
                    or state.has_any(
                        {item_names.SOA_SOLAR_LANCE, item_names.SOA_DEPLOY_FENIX},
                        player,
                    )
                )
                and logic.protoss_defense_rating(state, False) >= 13
            ),
        ),
        make_location_data(
            SC2Mission.FORBIDDEN_WEAPON.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 1100,
            LocationType.VICTORY,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.FORBIDDEN_WEAPON.mission_name,
            "South Solarite",
            SC2LOTV_LOC_ID_OFFSET + 1101,
            LocationType.VANILLA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.FORBIDDEN_WEAPON.mission_name,
            "North Solarite",
            SC2LOTV_LOC_ID_OFFSET + 1102,
            LocationType.VANILLA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.FORBIDDEN_WEAPON.mission_name,
            "Northwest Solarite",
            SC2LOTV_LOC_ID_OFFSET + 1103,
            LocationType.VANILLA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.FORBIDDEN_WEAPON.mission_name,
            "Rescue Sentries",
            SC2LOTV_LOC_ID_OFFSET + 1104,
            LocationType.EXTRA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.FORBIDDEN_WEAPON.mission_name,
            "Destroy Gateways",
            SC2LOTV_LOC_ID_OFFSET + 1105,
            LocationType.CHALLENGE,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 1200,
            LocationType.VICTORY,
            logic.protoss_temple_of_unification_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION.mission_name,
            "Mid Celestial Lock",
            SC2LOTV_LOC_ID_OFFSET + 1201,
            LocationType.EXTRA,
            logic.protoss_temple_of_unification_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION.mission_name,
            "West Celestial Lock",
            SC2LOTV_LOC_ID_OFFSET + 1202,
            LocationType.EXTRA,
            logic.protoss_temple_of_unification_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION.mission_name,
            "South Celestial Lock",
            SC2LOTV_LOC_ID_OFFSET + 1203,
            LocationType.EXTRA,
            logic.protoss_temple_of_unification_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION.mission_name,
            "East Celestial Lock",
            SC2LOTV_LOC_ID_OFFSET + 1204,
            LocationType.EXTRA,
            logic.protoss_temple_of_unification_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION.mission_name,
            "North Celestial Lock",
            SC2LOTV_LOC_ID_OFFSET + 1205,
            LocationType.EXTRA,
            logic.protoss_temple_of_unification_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION.mission_name,
            "Titanic Warp Prism",
            SC2LOTV_LOC_ID_OFFSET + 1206,
            LocationType.VANILLA,
            logic.protoss_temple_of_unification_requirement,
            hard_rule=logic.protoss_any_anti_air_unit_or_soa,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION.mission_name,
            "Terran Main Base",
            SC2LOTV_LOC_ID_OFFSET + 1207,
            LocationType.MASTERY,
            lambda state: logic.protoss_temple_of_unification_requirement(state)
            and logic.protoss_deathball(state),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION.mission_name,
            "Protoss Main Base",
            SC2LOTV_LOC_ID_OFFSET + 1208,
            LocationType.MASTERY,
            lambda state: logic.protoss_temple_of_unification_requirement(state)
            and logic.protoss_deathball(state),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.THE_INFINITE_CYCLE.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 1300,
            LocationType.VICTORY,
            logic.the_infinite_cycle_requirement,
        ),
        make_location_data(
            SC2Mission.THE_INFINITE_CYCLE.mission_name,
            "First Hall of Revelation",
            SC2LOTV_LOC_ID_OFFSET + 1301,
            LocationType.EXTRA,
            logic.the_infinite_cycle_requirement,
        ),
        make_location_data(
            SC2Mission.THE_INFINITE_CYCLE.mission_name,
            "Second Hall of Revelation",
            SC2LOTV_LOC_ID_OFFSET + 1302,
            LocationType.EXTRA,
            logic.the_infinite_cycle_requirement,
        ),
        make_location_data(
            SC2Mission.THE_INFINITE_CYCLE.mission_name,
            "First Xel'Naga Device",
            SC2LOTV_LOC_ID_OFFSET + 1303,
            LocationType.VANILLA,
            logic.the_infinite_cycle_requirement,
        ),
        make_location_data(
            SC2Mission.THE_INFINITE_CYCLE.mission_name,
            "Second Xel'Naga Device",
            SC2LOTV_LOC_ID_OFFSET + 1304,
            LocationType.VANILLA,
            logic.the_infinite_cycle_requirement,
        ),
        make_location_data(
            SC2Mission.THE_INFINITE_CYCLE.mission_name,
            "Third Xel'Naga Device",
            SC2LOTV_LOC_ID_OFFSET + 1305,
            LocationType.VANILLA,
            logic.the_infinite_cycle_requirement,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 1400,
            LocationType.VICTORY,
            logic.protoss_harbinger_of_oblivion_requirement,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION.mission_name,
            "Artanis",
            SC2LOTV_LOC_ID_OFFSET + 1401,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION.mission_name,
            "Northwest Void Crystal",
            SC2LOTV_LOC_ID_OFFSET + 1402,
            LocationType.EXTRA,
            logic.protoss_harbinger_of_oblivion_requirement,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION.mission_name,
            "Northeast Void Crystal",
            SC2LOTV_LOC_ID_OFFSET + 1403,
            LocationType.EXTRA,
            logic.protoss_harbinger_of_oblivion_requirement,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION.mission_name,
            "Southwest Void Crystal",
            SC2LOTV_LOC_ID_OFFSET + 1404,
            LocationType.EXTRA,
            logic.protoss_harbinger_of_oblivion_requirement,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION.mission_name,
            "Southeast Void Crystal",
            SC2LOTV_LOC_ID_OFFSET + 1405,
            LocationType.EXTRA,
            logic.protoss_harbinger_of_oblivion_requirement,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION.mission_name,
            "South Xel'Naga Vessel",
            SC2LOTV_LOC_ID_OFFSET + 1406,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION.mission_name,
            "Mid Xel'Naga Vessel",
            SC2LOTV_LOC_ID_OFFSET + 1407,
            LocationType.VANILLA,
            logic.protoss_harbinger_of_oblivion_requirement,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION.mission_name,
            "North Xel'Naga Vessel",
            SC2LOTV_LOC_ID_OFFSET + 1408,
            LocationType.VANILLA,
            logic.protoss_harbinger_of_oblivion_requirement,
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 1500,
            LocationType.VICTORY,
            lambda state: (
                logic.protoss_deathball(state)
                and logic.protoss_power_rating(state) >= 6
            ),
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST.mission_name,
            "Zerg Cleared",
            SC2LOTV_LOC_ID_OFFSET + 1501,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST.mission_name,
            "First Stasis Lock",
            SC2LOTV_LOC_ID_OFFSET + 1502,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_deathball(state)
                and logic.protoss_power_rating(state) >= 6
            ),
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST.mission_name,
            "Second Stasis Lock",
            SC2LOTV_LOC_ID_OFFSET + 1503,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_deathball(state)
                and logic.protoss_power_rating(state) >= 6
            ),
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST.mission_name,
            "Third Stasis Lock",
            SC2LOTV_LOC_ID_OFFSET + 1504,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_deathball(state)
                and logic.protoss_power_rating(state) >= 6
            ),
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST.mission_name,
            "Fourth Stasis Lock",
            SC2LOTV_LOC_ID_OFFSET + 1505,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_deathball(state)
                and logic.protoss_power_rating(state) >= 6
            ),
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST.mission_name,
            "South Power Core",
            SC2LOTV_LOC_ID_OFFSET + 1506,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_deathball(state)
                and logic.protoss_power_rating(state) >= 6
                and (adv_tactics or logic.protoss_unsealing_the_past_ledge_requirement(state))
            ),
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST.mission_name,
            "East Power Core",
            SC2LOTV_LOC_ID_OFFSET + 1507,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_deathball(state)
                and logic.protoss_power_rating(state) >= 6
                and (adv_tactics or logic.protoss_unsealing_the_past_ledge_requirement(state))
            ),
        ),
        make_location_data(
            SC2Mission.PURIFICATION.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 1600,
            LocationType.VICTORY,
            logic.protoss_deathball,
        ),
        make_location_data(
            SC2Mission.PURIFICATION.mission_name,
            "North Sector: West Null Circuit",
            SC2LOTV_LOC_ID_OFFSET + 1601,
            LocationType.VANILLA,
            logic.protoss_deathball,
        ),
        make_location_data(
            SC2Mission.PURIFICATION.mission_name,
            "North Sector: Northeast Null Circuit",
            SC2LOTV_LOC_ID_OFFSET + 1602,
            LocationType.EXTRA,
            logic.protoss_deathball,
        ),
        make_location_data(
            SC2Mission.PURIFICATION.mission_name,
            "North Sector: Southeast Null Circuit",
            SC2LOTV_LOC_ID_OFFSET + 1603,
            LocationType.EXTRA,
            logic.protoss_deathball,
        ),
        make_location_data(
            SC2Mission.PURIFICATION.mission_name,
            "South Sector: West Null Circuit",
            SC2LOTV_LOC_ID_OFFSET + 1604,
            LocationType.VANILLA,
            logic.protoss_deathball,
        ),
        make_location_data(
            SC2Mission.PURIFICATION.mission_name,
            "South Sector: North Null Circuit",
            SC2LOTV_LOC_ID_OFFSET + 1605,
            LocationType.EXTRA,
            logic.protoss_deathball,
        ),
        make_location_data(
            SC2Mission.PURIFICATION.mission_name,
            "South Sector: East Null Circuit",
            SC2LOTV_LOC_ID_OFFSET + 1606,
            LocationType.EXTRA,
            logic.protoss_deathball,
        ),
        make_location_data(
            SC2Mission.PURIFICATION.mission_name,
            "West Sector: West Null Circuit",
            SC2LOTV_LOC_ID_OFFSET + 1607,
            LocationType.VANILLA,
            logic.protoss_deathball,
        ),
        make_location_data(
            SC2Mission.PURIFICATION.mission_name,
            "West Sector: Mid Null Circuit",
            SC2LOTV_LOC_ID_OFFSET + 1608,
            LocationType.EXTRA,
            logic.protoss_deathball,
        ),
        make_location_data(
            SC2Mission.PURIFICATION.mission_name,
            "West Sector: East Null Circuit",
            SC2LOTV_LOC_ID_OFFSET + 1609,
            LocationType.EXTRA,
            logic.protoss_deathball,
        ),
        make_location_data(
            SC2Mission.PURIFICATION.mission_name,
            "East Sector: North Null Circuit",
            SC2LOTV_LOC_ID_OFFSET + 1610,
            LocationType.VANILLA,
            logic.protoss_deathball,
        ),
        make_location_data(
            SC2Mission.PURIFICATION.mission_name,
            "East Sector: West Null Circuit",
            SC2LOTV_LOC_ID_OFFSET + 1611,
            LocationType.EXTRA,
            logic.protoss_deathball,
        ),
        make_location_data(
            SC2Mission.PURIFICATION.mission_name,
            "East Sector: South Null Circuit",
            SC2LOTV_LOC_ID_OFFSET + 1612,
            LocationType.EXTRA,
            logic.protoss_deathball,
        ),
        make_location_data(
            SC2Mission.PURIFICATION.mission_name,
            "Purifier Warden",
            SC2LOTV_LOC_ID_OFFSET + 1613,
            LocationType.VANILLA,
            logic.protoss_deathball,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 1700,
            LocationType.VICTORY,
            logic.protoss_steps_of_the_rite_requirement,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE.mission_name,
            "First Terrazine Fog",
            SC2LOTV_LOC_ID_OFFSET + 1701,
            LocationType.EXTRA,
            logic.protoss_steps_of_the_rite_requirement,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE.mission_name,
            "Southwest Guardian",
            SC2LOTV_LOC_ID_OFFSET + 1702,
            LocationType.EXTRA,
            logic.protoss_steps_of_the_rite_requirement,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE.mission_name,
            "West Guardian",
            SC2LOTV_LOC_ID_OFFSET + 1703,
            LocationType.EXTRA,
            logic.protoss_steps_of_the_rite_requirement,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE.mission_name,
            "Northwest Guardian",
            SC2LOTV_LOC_ID_OFFSET + 1704,
            LocationType.EXTRA,
            logic.protoss_steps_of_the_rite_requirement,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE.mission_name,
            "Northeast Guardian",
            SC2LOTV_LOC_ID_OFFSET + 1705,
            LocationType.EXTRA,
            logic.protoss_steps_of_the_rite_requirement,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE.mission_name,
            "North Mothership",
            SC2LOTV_LOC_ID_OFFSET + 1706,
            LocationType.VANILLA,
            logic.protoss_steps_of_the_rite_requirement,
            hard_rule=logic.protoss_any_anti_air_unit_or_soa,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE.mission_name,
            "South Mothership",
            SC2LOTV_LOC_ID_OFFSET + 1707,
            LocationType.VANILLA,
            logic.protoss_steps_of_the_rite_requirement,
            hard_rule=logic.protoss_any_anti_air_unit_or_soa,
        ),
        make_location_data(
            SC2Mission.RAK_SHIR.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 1800,
            LocationType.VICTORY,
            logic.protoss_rak_shir_requirement,
        ),
        make_location_data(
            SC2Mission.RAK_SHIR.mission_name,
            "North Slayn Elemental",
            SC2LOTV_LOC_ID_OFFSET + 1801,
            LocationType.VANILLA,
            logic.protoss_rak_shir_requirement,
            hard_rule=logic.protoss_any_anti_air_unit_or_soa,
        ),
        make_location_data(
            SC2Mission.RAK_SHIR.mission_name,
            "Southwest Slayn Elemental",
            SC2LOTV_LOC_ID_OFFSET + 1802,
            LocationType.VANILLA,
            logic.protoss_rak_shir_requirement,
            hard_rule=logic.protoss_any_anti_air_unit_or_soa,
        ),
        make_location_data(
            SC2Mission.RAK_SHIR.mission_name,
            "East Slayn Elemental",
            SC2LOTV_LOC_ID_OFFSET + 1803,
            LocationType.VANILLA,
            logic.protoss_rak_shir_requirement,
            hard_rule=logic.protoss_any_anti_air_unit_or_soa,
        ),
        make_location_data(
            SC2Mission.RAK_SHIR.mission_name,
            "Resource Pickups",
            SC2LOTV_LOC_ID_OFFSET + 1804,
            LocationType.EXTRA,
            logic.protoss_rak_shir_requirement,
        ),
        make_location_data(
            SC2Mission.RAK_SHIR.mission_name,
            "Destroy Nexuses",
            SC2LOTV_LOC_ID_OFFSET + 1805,
            LocationType.CHALLENGE,
            logic.protoss_rak_shir_requirement,
        ),
        make_location_data(
            SC2Mission.RAK_SHIR.mission_name,
            "Win in under 15 minutes",
            SC2LOTV_LOC_ID_OFFSET + 1806,
            LocationType.MASTERY,
            logic.protoss_rak_shir_requirement,
            flags=LocationFlag.SPEEDRUN,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_CHARGE.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 1900,
            LocationType.VICTORY,
            logic.protoss_templars_charge_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_CHARGE.mission_name,
            "Northwest Power Core",
            SC2LOTV_LOC_ID_OFFSET + 1901,
            LocationType.EXTRA,
            logic.protoss_templars_charge_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_CHARGE.mission_name,
            "Northeast Power Core",
            SC2LOTV_LOC_ID_OFFSET + 1902,
            LocationType.EXTRA,
            logic.protoss_templars_charge_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_CHARGE.mission_name,
            "Southeast Power Core",
            SC2LOTV_LOC_ID_OFFSET + 1903,
            LocationType.EXTRA,
            logic.protoss_templars_charge_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_CHARGE.mission_name,
            "West Hybrid Stasis Chamber",
            SC2LOTV_LOC_ID_OFFSET + 1904,
            LocationType.VANILLA,
            logic.protoss_templars_charge_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_CHARGE.mission_name,
            "Southeast Hybrid Stasis Chamber",
            SC2LOTV_LOC_ID_OFFSET + 1905,
            LocationType.VANILLA,
            logic.protoss_fleet,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_RETURN.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 2000,
            LocationType.VICTORY,
            logic.templars_return_phase_3_reach_dts_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_RETURN.mission_name,
            "Citadel: First Gate",
            SC2LOTV_LOC_ID_OFFSET + 2001,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_RETURN.mission_name,
            "Citadel: Second Gate",
            SC2LOTV_LOC_ID_OFFSET + 2002,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_RETURN.mission_name,
            "Citadel: Power Structure",
            SC2LOTV_LOC_ID_OFFSET + 2003,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_RETURN.mission_name,
            "Temple Grounds: Gather Army",
            SC2LOTV_LOC_ID_OFFSET + 2004,
            LocationType.VANILLA,
            logic.templars_return_phase_2_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_RETURN.mission_name,
            "Temple Grounds: Power Structure",
            SC2LOTV_LOC_ID_OFFSET + 2005,
            LocationType.VANILLA,
            logic.templars_return_phase_2_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_RETURN.mission_name,
            "Caverns: Purifier",
            SC2LOTV_LOC_ID_OFFSET + 2006,
            LocationType.EXTRA,
            logic.templars_return_phase_3_reach_colossus_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_RETURN.mission_name,
            "Caverns: Dark Templar",
            SC2LOTV_LOC_ID_OFFSET + 2007,
            LocationType.EXTRA,
            logic.templars_return_phase_3_reach_dts_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 2100,
            LocationType.VICTORY,
            logic.protoss_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST.mission_name,
            "Southeast Void Shard",
            SC2LOTV_LOC_ID_OFFSET + 2101,
            LocationType.EXTRA,
            logic.protoss_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST.mission_name,
            "South Void Shard",
            SC2LOTV_LOC_ID_OFFSET + 2102,
            LocationType.EXTRA,
            logic.protoss_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST.mission_name,
            "Southwest Void Shard",
            SC2LOTV_LOC_ID_OFFSET + 2103,
            LocationType.EXTRA,
            logic.protoss_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST.mission_name,
            "North Void Shard",
            SC2LOTV_LOC_ID_OFFSET + 2104,
            LocationType.EXTRA,
            logic.protoss_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST.mission_name,
            "Northwest Void Shard",
            SC2LOTV_LOC_ID_OFFSET + 2105,
            LocationType.EXTRA,
            logic.protoss_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST.mission_name,
            "Nerazim Warp in Zone",
            SC2LOTV_LOC_ID_OFFSET + 2106,
            LocationType.VANILLA,
            logic.protoss_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST.mission_name,
            "Tal'darim Warp in Zone",
            SC2LOTV_LOC_ID_OFFSET + 2107,
            LocationType.VANILLA,
            logic.protoss_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST.mission_name,
            "Purifier Warp in Zone",
            SC2LOTV_LOC_ID_OFFSET + 2108,
            LocationType.VANILLA,
            logic.protoss_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.SALVATION.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 2200,
            LocationType.VICTORY,
            logic.protoss_salvation_requirement,
        ),
        make_location_data(
            SC2Mission.SALVATION.mission_name,
            "Fabrication Matrix",
            SC2LOTV_LOC_ID_OFFSET + 2201,
            LocationType.EXTRA,
            logic.protoss_salvation_requirement,
        ),
        make_location_data(
            SC2Mission.SALVATION.mission_name,
            "Assault Cluster",
            SC2LOTV_LOC_ID_OFFSET + 2202,
            LocationType.EXTRA,
            logic.protoss_salvation_requirement,
        ),
        make_location_data(
            SC2Mission.SALVATION.mission_name,
            "Hull Breach",
            SC2LOTV_LOC_ID_OFFSET + 2203,
            LocationType.EXTRA,
            logic.protoss_salvation_requirement,
        ),
        make_location_data(
            SC2Mission.SALVATION.mission_name,
            "Core Critical",
            SC2LOTV_LOC_ID_OFFSET + 2204,
            LocationType.EXTRA,
            logic.protoss_salvation_requirement,
        ),
        make_location_data(
            SC2Mission.SALVATION.mission_name,
            "Kill Brutalisk",
            SC2LOTV_LOC_ID_OFFSET + 2205,
            LocationType.MASTERY,
            logic.protoss_salvation_requirement,
        ),
        # Epilogue
        make_location_data(
            SC2Mission.INTO_THE_VOID.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 2300,
            LocationType.VICTORY,
            logic.into_the_void_requirement,
        ),
        make_location_data(
            SC2Mission.INTO_THE_VOID.mission_name,
            "Corruption Source",
            SC2LOTV_LOC_ID_OFFSET + 2301,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.INTO_THE_VOID.mission_name,
            "Southwest Forward Position",
            SC2LOTV_LOC_ID_OFFSET + 2302,
            LocationType.VANILLA,
            logic.into_the_void_requirement,
        ),
        make_location_data(
            SC2Mission.INTO_THE_VOID.mission_name,
            "Northwest Forward Position",
            SC2LOTV_LOC_ID_OFFSET + 2303,
            LocationType.VANILLA,
            logic.into_the_void_requirement,
        ),
        make_location_data(
            SC2Mission.INTO_THE_VOID.mission_name,
            "Southeast Forward Position",
            SC2LOTV_LOC_ID_OFFSET + 2304,
            LocationType.VANILLA,
            logic.into_the_void_requirement,
        ),
        make_location_data(
            SC2Mission.INTO_THE_VOID.mission_name,
            "Northeast Forward Position",
            SC2LOTV_LOC_ID_OFFSET + 2305,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.THE_ESSENCE_OF_ETERNITY.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 2400,
            LocationType.VICTORY,
            logic.essence_of_eternity_requirement,
        ),
        make_location_data(
            SC2Mission.THE_ESSENCE_OF_ETERNITY.mission_name,
            "Initial Void Thrashers",
            SC2LOTV_LOC_ID_OFFSET + 2401,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_ESSENCE_OF_ETERNITY.mission_name,
            "Void Thrasher Wave 1",
            SC2LOTV_LOC_ID_OFFSET + 2402,
            LocationType.EXTRA,
            logic.essence_of_eternity_requirement,
        ),
        make_location_data(
            SC2Mission.THE_ESSENCE_OF_ETERNITY.mission_name,
            "Void Thrasher Wave 2",
            SC2LOTV_LOC_ID_OFFSET + 2403,
            LocationType.EXTRA,
            logic.essence_of_eternity_requirement,
        ),
        make_location_data(
            SC2Mission.THE_ESSENCE_OF_ETERNITY.mission_name,
            "Void Thrasher Wave 3",
            SC2LOTV_LOC_ID_OFFSET + 2404,
            LocationType.EXTRA,
            logic.essence_of_eternity_requirement,
        ),
        make_location_data(
            SC2Mission.THE_ESSENCE_OF_ETERNITY.mission_name,
            "Void Thrasher Wave 4",
            SC2LOTV_LOC_ID_OFFSET + 2405,
            LocationType.EXTRA,
            logic.essence_of_eternity_requirement,
        ),
        make_location_data(
            SC2Mission.THE_ESSENCE_OF_ETERNITY.mission_name,
            "No more than 15 Kerrigan Kills",
            SC2LOTV_LOC_ID_OFFSET + 2406,
            LocationType.MASTERY,
            logic.essence_of_eternity_requirement,
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.AMON_S_FALL.mission_name,
            "Victory",
            SC2LOTV_LOC_ID_OFFSET + 2500,
            LocationType.VICTORY,
            logic.amons_fall_requirement,
        ),
        make_location_data(
            SC2Mission.AMON_S_FALL.mission_name,
            "Destroy 1 Crystal",
            SC2LOTV_LOC_ID_OFFSET + 2501,
            LocationType.EXTRA,
            logic.amons_fall_requirement,
        ),
        make_location_data(
            SC2Mission.AMON_S_FALL.mission_name,
            "Destroy 2 Crystals",
            SC2LOTV_LOC_ID_OFFSET + 2502,
            LocationType.EXTRA,
            logic.amons_fall_requirement,
        ),
        make_location_data(
            SC2Mission.AMON_S_FALL.mission_name,
            "Destroy 3 Crystals",
            SC2LOTV_LOC_ID_OFFSET + 2503,
            LocationType.EXTRA,
            logic.amons_fall_requirement,
        ),
        make_location_data(
            SC2Mission.AMON_S_FALL.mission_name,
            "Destroy 4 Crystals",
            SC2LOTV_LOC_ID_OFFSET + 2504,
            LocationType.EXTRA,
            logic.amons_fall_requirement,
        ),
        make_location_data(
            SC2Mission.AMON_S_FALL.mission_name,
            "Destroy 5 Crystals",
            SC2LOTV_LOC_ID_OFFSET + 2505,
            LocationType.EXTRA,
            logic.amons_fall_requirement,
        ),
        make_location_data(
            SC2Mission.AMON_S_FALL.mission_name,
            "Destroy 6 Crystals",
            SC2LOTV_LOC_ID_OFFSET + 2506,
            LocationType.EXTRA,
            logic.amons_fall_requirement,
        ),
        make_location_data(
            SC2Mission.AMON_S_FALL.mission_name,
            "Clear Void Chasms",
            SC2LOTV_LOC_ID_OFFSET + 2507,
            LocationType.MASTERY,
            lambda state: logic.amons_fall_requirement(state)
            and logic.spread_creep(state, False)
            and logic.zerg_big_monsters(state),
        ),
        # Nova Covert Ops
        make_location_data(
            SC2Mission.THE_ESCAPE.mission_name,
            "Victory",
            SC2NCO_LOC_ID_OFFSET + 100,
            LocationType.VICTORY,
            logic.the_escape_requirement,
            hard_rule=logic.nova_any_nobuild_damage,
        ),
        make_location_data(
            SC2Mission.THE_ESCAPE.mission_name,
            "Rifle",
            SC2NCO_LOC_ID_OFFSET + 101,
            LocationType.VANILLA,
            logic.the_escape_first_stage_requirement,
        ),
        make_location_data(
            SC2Mission.THE_ESCAPE.mission_name,
            "Grenades",
            SC2NCO_LOC_ID_OFFSET + 102,
            LocationType.VANILLA,
            logic.the_escape_first_stage_requirement,
            hard_rule=logic.nova_any_nobuild_damage,
        ),
        make_location_data(
            SC2Mission.THE_ESCAPE.mission_name,
            "Agent Delta",
            SC2NCO_LOC_ID_OFFSET + 103,
            LocationType.VANILLA,
            logic.the_escape_requirement,
            hard_rule=logic.nova_any_nobuild_damage,
        ),
        make_location_data(
            SC2Mission.THE_ESCAPE.mission_name,
            "Agent Pierce",
            SC2NCO_LOC_ID_OFFSET + 104,
            LocationType.VANILLA,
            logic.the_escape_requirement,
            hard_rule=logic.nova_any_nobuild_damage,
        ),
        make_location_data(
            SC2Mission.THE_ESCAPE.mission_name,
            "Agent Stone",
            SC2NCO_LOC_ID_OFFSET + 105,
            LocationType.VANILLA,
            logic.the_escape_requirement,
            hard_rule=logic.nova_any_nobuild_damage,
        ),
        make_location_data(
            SC2Mission.SUDDEN_STRIKE.mission_name,
            "Victory",
            SC2NCO_LOC_ID_OFFSET + 200,
            LocationType.VICTORY,
            logic.sudden_strike_requirement,
        ),
        make_location_data(
            SC2Mission.SUDDEN_STRIKE.mission_name,
            "Research Center",
            SC2NCO_LOC_ID_OFFSET + 201,
            LocationType.VANILLA,
            logic.sudden_strike_requirement,
        ),
        make_location_data(
            SC2Mission.SUDDEN_STRIKE.mission_name,
            "Weaponry Labs",
            SC2NCO_LOC_ID_OFFSET + 202,
            LocationType.VANILLA,
            logic.sudden_strike_requirement,
        ),
        make_location_data(
            SC2Mission.SUDDEN_STRIKE.mission_name,
            "Brutalisk",
            SC2NCO_LOC_ID_OFFSET + 203,
            LocationType.EXTRA,
            logic.sudden_strike_requirement,
        ),
        make_location_data(
            SC2Mission.SUDDEN_STRIKE.mission_name,
            "Gas Pickups",
            SC2NCO_LOC_ID_OFFSET + 204,
            LocationType.EXTRA,
            lambda state: (
                logic.advanced_tactics or logic.sudden_strike_requirement(state)
            ),
        ),
        make_location_data(
            SC2Mission.SUDDEN_STRIKE.mission_name,
            "Protect Buildings",
            SC2NCO_LOC_ID_OFFSET + 205,
            LocationType.CHALLENGE,
            logic.sudden_strike_requirement,
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.SUDDEN_STRIKE.mission_name,
            "Zerg Base",
            SC2NCO_LOC_ID_OFFSET + 206,
            LocationType.MASTERY,
            lambda state: (
                logic.sudden_strike_requirement(state)
                and logic.terran_competent_comp(state)
                and logic.terran_base_trasher(state)
                and logic.terran_power_rating(state) >= 8
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.ENEMY_INTELLIGENCE.mission_name,
            "Victory",
            SC2NCO_LOC_ID_OFFSET + 300,
            LocationType.VICTORY,
            logic.enemy_intelligence_third_stage_requirement,
            hard_rule=logic.enemy_intelligence_cliff_garrison_and_nova_mobility,
        ),
        make_location_data(
            SC2Mission.ENEMY_INTELLIGENCE.mission_name,
            "West Garrison",
            SC2NCO_LOC_ID_OFFSET + 301,
            LocationType.EXTRA,
            logic.enemy_intelligence_first_stage_requirement,
            hard_rule=logic.enemy_intelligence_garrisonable_unit,
        ),
        make_location_data(
            SC2Mission.ENEMY_INTELLIGENCE.mission_name,
            "Close Garrison",
            SC2NCO_LOC_ID_OFFSET + 302,
            LocationType.EXTRA,
            logic.enemy_intelligence_first_stage_requirement,
            hard_rule=logic.enemy_intelligence_garrisonable_unit,
        ),
        make_location_data(
            SC2Mission.ENEMY_INTELLIGENCE.mission_name,
            "Northeast Garrison",
            SC2NCO_LOC_ID_OFFSET + 303,
            LocationType.EXTRA,
            logic.enemy_intelligence_first_stage_requirement,
            hard_rule=logic.enemy_intelligence_garrisonable_unit,
        ),
        make_location_data(
            SC2Mission.ENEMY_INTELLIGENCE.mission_name,
            "Southeast Garrison",
            SC2NCO_LOC_ID_OFFSET + 304,
            LocationType.EXTRA,
            lambda state: (
                logic.enemy_intelligence_first_stage_requirement(state)
                and logic.enemy_intelligence_cliff_garrison(state)
            ),
            hard_rule=logic.enemy_intelligence_cliff_garrison,
        ),
        make_location_data(
            SC2Mission.ENEMY_INTELLIGENCE.mission_name,
            "South Garrison",
            SC2NCO_LOC_ID_OFFSET + 305,
            LocationType.EXTRA,
            logic.enemy_intelligence_first_stage_requirement,
            hard_rule=logic.enemy_intelligence_garrisonable_unit,
        ),
        make_location_data(
            SC2Mission.ENEMY_INTELLIGENCE.mission_name,
            "All Garrisons",
            SC2NCO_LOC_ID_OFFSET + 306,
            LocationType.VANILLA,
            lambda state: (
                logic.enemy_intelligence_first_stage_requirement(state)
                and logic.enemy_intelligence_cliff_garrison(state)
            ),
            hard_rule=logic.enemy_intelligence_cliff_garrison,
        ),
        make_location_data(
            SC2Mission.ENEMY_INTELLIGENCE.mission_name,
            "Forces Rescued",
            SC2NCO_LOC_ID_OFFSET + 307,
            LocationType.VANILLA,
            logic.enemy_intelligence_first_stage_requirement,
        ),
        make_location_data(
            SC2Mission.ENEMY_INTELLIGENCE.mission_name,
            "Communications Hub",
            SC2NCO_LOC_ID_OFFSET + 308,
            LocationType.VANILLA,
            logic.enemy_intelligence_second_stage_requirement,
            hard_rule=logic.enemy_intelligence_cliff_garrison_and_nova_mobility,
        ),
        make_location_data(
            SC2Mission.TROUBLE_IN_PARADISE.mission_name,
            "Victory",
            SC2NCO_LOC_ID_OFFSET + 400,
            LocationType.VICTORY,
            logic.trouble_in_paradise_requirement,
        ),
        make_location_data(
            SC2Mission.TROUBLE_IN_PARADISE.mission_name,
            "North Base: West Hatchery",
            SC2NCO_LOC_ID_OFFSET + 401,
            LocationType.VANILLA,
            logic.trouble_in_paradise_requirement,
        ),
        make_location_data(
            SC2Mission.TROUBLE_IN_PARADISE.mission_name,
            "North Base: North Hatchery",
            SC2NCO_LOC_ID_OFFSET + 402,
            LocationType.VANILLA,
            logic.trouble_in_paradise_requirement,
        ),
        make_location_data(
            SC2Mission.TROUBLE_IN_PARADISE.mission_name,
            "North Base: East Hatchery",
            SC2NCO_LOC_ID_OFFSET + 403,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.TROUBLE_IN_PARADISE.mission_name,
            "South Base: Northwest Hatchery",
            SC2NCO_LOC_ID_OFFSET + 404,
            LocationType.VANILLA,
            logic.trouble_in_paradise_requirement,
        ),
        make_location_data(
            SC2Mission.TROUBLE_IN_PARADISE.mission_name,
            "South Base: Southwest Hatchery",
            SC2NCO_LOC_ID_OFFSET + 405,
            LocationType.VANILLA,
            logic.trouble_in_paradise_requirement,
        ),
        make_location_data(
            SC2Mission.TROUBLE_IN_PARADISE.mission_name,
            "South Base: East Hatchery",
            SC2NCO_LOC_ID_OFFSET + 406,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.TROUBLE_IN_PARADISE.mission_name,
            "North Shield Projector",
            SC2NCO_LOC_ID_OFFSET + 407,
            LocationType.EXTRA,
            logic.trouble_in_paradise_requirement,
        ),
        make_location_data(
            SC2Mission.TROUBLE_IN_PARADISE.mission_name,
            "East Shield Projector",
            SC2NCO_LOC_ID_OFFSET + 408,
            LocationType.EXTRA,
            logic.trouble_in_paradise_requirement,
        ),
        make_location_data(
            SC2Mission.TROUBLE_IN_PARADISE.mission_name,
            "South Shield Projector",
            SC2NCO_LOC_ID_OFFSET + 409,
            LocationType.EXTRA,
            logic.trouble_in_paradise_requirement,
        ),
        make_location_data(
            SC2Mission.TROUBLE_IN_PARADISE.mission_name,
            "West Shield Projector",
            SC2NCO_LOC_ID_OFFSET + 410,
            LocationType.EXTRA,
            logic.trouble_in_paradise_requirement,
        ),
        make_location_data(
            SC2Mission.TROUBLE_IN_PARADISE.mission_name,
            "Fleet Beacon",
            SC2NCO_LOC_ID_OFFSET + 411,
            LocationType.VANILLA,
            logic.trouble_in_paradise_requirement,
        ),
        make_location_data(
            SC2Mission.NIGHT_TERRORS.mission_name,
            "Victory",
            SC2NCO_LOC_ID_OFFSET + 500,
            LocationType.VICTORY,
            logic.night_terrors_requirement,
        ),
        make_location_data(
            SC2Mission.NIGHT_TERRORS.mission_name,
            "1 Terrazine Node Collected",
            SC2NCO_LOC_ID_OFFSET + 501,
            LocationType.EXTRA,
            logic.night_terrors_requirement,
        ),
        make_location_data(
            SC2Mission.NIGHT_TERRORS.mission_name,
            "2 Terrazine Nodes Collected",
            SC2NCO_LOC_ID_OFFSET + 502,
            LocationType.EXTRA,
            logic.night_terrors_requirement,
        ),
        make_location_data(
            SC2Mission.NIGHT_TERRORS.mission_name,
            "3 Terrazine Nodes Collected",
            SC2NCO_LOC_ID_OFFSET + 503,
            LocationType.EXTRA,
            logic.night_terrors_requirement,
        ),
        make_location_data(
            SC2Mission.NIGHT_TERRORS.mission_name,
            "4 Terrazine Nodes Collected",
            SC2NCO_LOC_ID_OFFSET + 504,
            LocationType.EXTRA,
            logic.night_terrors_requirement,
        ),
        make_location_data(
            SC2Mission.NIGHT_TERRORS.mission_name,
            "5 Terrazine Nodes Collected",
            SC2NCO_LOC_ID_OFFSET + 505,
            LocationType.EXTRA,
            logic.night_terrors_requirement,
        ),
        make_location_data(
            SC2Mission.NIGHT_TERRORS.mission_name,
            "HERC Outpost",
            SC2NCO_LOC_ID_OFFSET + 506,
            LocationType.VANILLA,
            logic.night_terrors_requirement,
        ),
        make_location_data(
            SC2Mission.NIGHT_TERRORS.mission_name,
            "Umojan Mine",
            SC2NCO_LOC_ID_OFFSET + 507,
            LocationType.EXTRA,
            logic.night_terrors_requirement,
        ),
        make_location_data(
            SC2Mission.NIGHT_TERRORS.mission_name,
            "Blightbringer",
            SC2NCO_LOC_ID_OFFSET + 508,
            LocationType.VANILLA,
            lambda state: (
                logic.night_terrors_requirement(state)
                and logic.nova_ranged_weapon(state)
                and state.has_any(
                    {
                        item_names.NOVA_HELLFIRE_SHOTGUN,
                        item_names.NOVA_PULSE_GRENADES,
                        item_names.NOVA_STIM_INFUSION,
                        item_names.NOVA_HOLO_DECOY,
                    },
                    player,
                )
            ),
        ),
        make_location_data(
            SC2Mission.NIGHT_TERRORS.mission_name,
            "Science Facility",
            SC2NCO_LOC_ID_OFFSET + 509,
            LocationType.EXTRA,
            logic.night_terrors_requirement,
        ),
        make_location_data(
            SC2Mission.NIGHT_TERRORS.mission_name,
            "Eradicators",
            SC2NCO_LOC_ID_OFFSET + 510,
            LocationType.VANILLA,
            lambda state: (
                logic.night_terrors_requirement(state) and logic.nova_any_weapon(state)
            ),
        ),
        make_location_data(
            SC2Mission.FLASHPOINT.mission_name,
            "Victory",
            SC2NCO_LOC_ID_OFFSET + 600,
            LocationType.VICTORY,
            logic.flashpoint_far_requirement,
        ),
        make_location_data(
            SC2Mission.FLASHPOINT.mission_name,
            "Close North Evidence Coordinates",
            SC2NCO_LOC_ID_OFFSET + 601,
            LocationType.EXTRA,
            lambda state: (
                state.has_any(
                    {
                        item_names.LIBERATOR_RAID_ARTILLERY,
                        item_names.RAVEN_HUNTER_SEEKER_WEAPON,
                    },
                    player,
                )
                or logic.terran_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.FLASHPOINT.mission_name,
            "Close East Evidence Coordinates",
            SC2NCO_LOC_ID_OFFSET + 602,
            LocationType.EXTRA,
            lambda state: (
                state.has_any(
                    {
                        item_names.LIBERATOR_RAID_ARTILLERY,
                        item_names.RAVEN_HUNTER_SEEKER_WEAPON,
                    },
                    player,
                )
                or logic.terran_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.FLASHPOINT.mission_name,
            "Far North Evidence Coordinates",
            SC2NCO_LOC_ID_OFFSET + 603,
            LocationType.EXTRA,
            logic.flashpoint_far_requirement,
        ),
        make_location_data(
            SC2Mission.FLASHPOINT.mission_name,
            "Far East Evidence Coordinates",
            SC2NCO_LOC_ID_OFFSET + 604,
            LocationType.EXTRA,
            logic.flashpoint_far_requirement,
        ),
        make_location_data(
            SC2Mission.FLASHPOINT.mission_name,
            "Experimental Weapon",
            SC2NCO_LOC_ID_OFFSET + 605,
            LocationType.VANILLA,
            logic.flashpoint_far_requirement,
        ),
        make_location_data(
            SC2Mission.FLASHPOINT.mission_name,
            "Northwest Subway Entrance",
            SC2NCO_LOC_ID_OFFSET + 606,
            LocationType.VANILLA,
            lambda state: (
                state.has_any(
                    {
                        item_names.LIBERATOR_RAID_ARTILLERY,
                        item_names.RAVEN_HUNTER_SEEKER_WEAPON,
                    },
                    player,
                )
                and logic.terran_common_unit(state)
                or logic.flashpoint_far_requirement(state)
            ),
        ),
        make_location_data(
            SC2Mission.FLASHPOINT.mission_name,
            "Southeast Subway Entrance",
            SC2NCO_LOC_ID_OFFSET + 607,
            LocationType.VANILLA,
            lambda state: state.has_any(
                {
                    item_names.LIBERATOR_RAID_ARTILLERY,
                    item_names.RAVEN_HUNTER_SEEKER_WEAPON,
                },
                player,
            )
            and logic.terran_common_unit(state)
            or logic.flashpoint_far_requirement(state),
        ),
        make_location_data(
            SC2Mission.FLASHPOINT.mission_name,
            "Northeast Subway Entrance",
            SC2NCO_LOC_ID_OFFSET + 608,
            LocationType.VANILLA,
            logic.flashpoint_far_requirement,
        ),
        make_location_data(
            SC2Mission.FLASHPOINT.mission_name,
            "Expansion Hatchery",
            SC2NCO_LOC_ID_OFFSET + 609,
            LocationType.EXTRA,
            lambda state: state.has(item_names.LIBERATOR_RAID_ARTILLERY, player)
            and logic.terran_common_unit(state)
            or logic.flashpoint_far_requirement(state),
        ),
        make_location_data(
            SC2Mission.FLASHPOINT.mission_name,
            "Baneling Spawns",
            SC2NCO_LOC_ID_OFFSET + 610,
            LocationType.EXTRA,
            logic.flashpoint_far_requirement,
        ),
        make_location_data(
            SC2Mission.FLASHPOINT.mission_name,
            "Mutalisk Spawns",
            SC2NCO_LOC_ID_OFFSET + 611,
            LocationType.EXTRA,
            logic.flashpoint_far_requirement,
        ),
        make_location_data(
            SC2Mission.FLASHPOINT.mission_name,
            "Nydus Worm Spawns",
            SC2NCO_LOC_ID_OFFSET + 612,
            LocationType.EXTRA,
            logic.flashpoint_far_requirement,
        ),
        make_location_data(
            SC2Mission.FLASHPOINT.mission_name,
            "Lurker Spawns",
            SC2NCO_LOC_ID_OFFSET + 613,
            LocationType.EXTRA,
            logic.flashpoint_far_requirement,
        ),
        make_location_data(
            SC2Mission.FLASHPOINT.mission_name,
            "Brood Lord Spawns",
            SC2NCO_LOC_ID_OFFSET + 614,
            LocationType.EXTRA,
            logic.flashpoint_far_requirement,
        ),
        make_location_data(
            SC2Mission.FLASHPOINT.mission_name,
            "Ultralisk Spawns",
            SC2NCO_LOC_ID_OFFSET + 615,
            LocationType.EXTRA,
            logic.flashpoint_far_requirement,
        ),
        make_location_data(
            SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name,
            "Victory",
            SC2NCO_LOC_ID_OFFSET + 700,
            LocationType.VICTORY,
            logic.enemy_shadow_victory,
            hard_rule=lambda state: logic.nova_beat_stone(state)
                and logic.enemy_shadow_door_unlocks_tool(state),
        ),
        make_location_data(
            SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name,
            "Sewers: Domination Visor",
            SC2NCO_LOC_ID_OFFSET + 701,
            LocationType.VANILLA,
            logic.enemy_shadow_domination,
            hard_rule=logic.nova_any_nobuild_damage,
        ),
        make_location_data(
            SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name,
            "Sewers: Resupply Crate",
            SC2NCO_LOC_ID_OFFSET + 702,
            LocationType.EXTRA,
            logic.enemy_shadow_first_stage,
            hard_rule=logic.nova_any_nobuild_damage,
        ),
        make_location_data(
            SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name,
            "Sewers: Facility Access",
            SC2NCO_LOC_ID_OFFSET + 703,
            LocationType.VANILLA,
            logic.enemy_shadow_first_stage,
            hard_rule=logic.nova_any_nobuild_damage,
        ),
        make_location_data(
            SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name,
            "Facility: Northwest Door Lock",
            SC2NCO_LOC_ID_OFFSET + 704,
            LocationType.VANILLA,
            logic.enemy_shadow_door_controls,
            hard_rule=lambda state: logic.nova_any_nobuild_damage(state)
            and logic.enemy_shadow_door_unlocks_tool(state),
        ),
        make_location_data(
            SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name,
            "Facility: Southeast Door Lock",
            SC2NCO_LOC_ID_OFFSET + 705,
            LocationType.VANILLA,
            logic.enemy_shadow_door_controls,
            hard_rule=lambda state: logic.nova_any_nobuild_damage(state)
            and logic.enemy_shadow_door_unlocks_tool(state),
        ),
        make_location_data(
            SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name,
            "Facility: Blazefire Gunblade",
            SC2NCO_LOC_ID_OFFSET + 706,
            LocationType.VANILLA,
            lambda state: (
                logic.enemy_shadow_second_stage(state)
                and (
                    logic.grant_story_tech == GrantStoryTech.option_grant
                    or state.has(item_names.NOVA_BLINK, player)
                    or (
                        adv_tactics
                        and state.has_all(
                            {
                                item_names.NOVA_DOMINATION,
                                item_names.NOVA_HOLO_DECOY,
                                item_names.NOVA_JUMP_SUIT_MODULE,
                            },
                            player,
                        )
                    )
                )
            ),
            hard_rule=logic.enemy_shadow_nova_damage_and_blazefire_unlock,
        ),
        make_location_data(
            SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name,
            "Facility: Blink Suit",
            SC2NCO_LOC_ID_OFFSET + 707,
            LocationType.VANILLA,
            logic.enemy_shadow_second_stage,
            hard_rule=logic.nova_any_nobuild_damage,
        ),
        make_location_data(
            SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name,
            "Facility: Advanced Weaponry",
            SC2NCO_LOC_ID_OFFSET + 708,
            LocationType.VANILLA,
            logic.enemy_shadow_second_stage,
            hard_rule=logic.nova_any_nobuild_damage,
        ),
        make_location_data(
            SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name,
            "Facility: Entrance Resupply Crate",
            SC2NCO_LOC_ID_OFFSET + 709,
            LocationType.EXTRA,
            logic.enemy_shadow_first_stage,
            hard_rule=logic.nova_any_nobuild_damage,
        ),
        make_location_data(
            SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name,
            "Facility: West Resupply Crate",
            SC2NCO_LOC_ID_OFFSET + 710,
            LocationType.EXTRA,
            logic.enemy_shadow_second_stage,
            hard_rule=logic.nova_any_nobuild_damage,
        ),
        make_location_data(
            SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name,
            "Facility: North Resupply Crate",
            SC2NCO_LOC_ID_OFFSET + 711,
            LocationType.EXTRA,
            logic.enemy_shadow_second_stage,
            hard_rule=logic.nova_any_nobuild_damage,
        ),
        make_location_data(
            SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name,
            "Facility: East Resupply Crate",
            SC2NCO_LOC_ID_OFFSET + 712,
            LocationType.EXTRA,
            logic.enemy_shadow_second_stage,
            hard_rule=logic.nova_any_nobuild_damage,
        ),
        make_location_data(
            SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name,
            "Facility: South Resupply Crate",
            SC2NCO_LOC_ID_OFFSET + 713,
            LocationType.EXTRA,
            logic.enemy_shadow_second_stage,
            hard_rule=logic.nova_any_nobuild_damage,
        ),
        make_location_data(
            SC2Mission.DARK_SKIES.mission_name,
            "Victory",
            SC2NCO_LOC_ID_OFFSET + 800,
            LocationType.VICTORY,
            logic.dark_skies_requirement,
        ),
        make_location_data(
            SC2Mission.DARK_SKIES.mission_name,
            "First Squadron of Dominion Fleet",
            SC2NCO_LOC_ID_OFFSET + 801,
            LocationType.EXTRA,
            logic.dark_skies_requirement,
        ),
        make_location_data(
            SC2Mission.DARK_SKIES.mission_name,
            "Remainder of Dominion Fleet",
            SC2NCO_LOC_ID_OFFSET + 802,
            LocationType.EXTRA,
            logic.dark_skies_requirement,
        ),
        make_location_data(
            SC2Mission.DARK_SKIES.mission_name,
            "Ji'nara",
            SC2NCO_LOC_ID_OFFSET + 803,
            LocationType.EXTRA,
            logic.dark_skies_requirement,
        ),
        make_location_data(
            SC2Mission.DARK_SKIES.mission_name,
            "Science Facility",
            SC2NCO_LOC_ID_OFFSET + 804,
            LocationType.VANILLA,
            logic.dark_skies_requirement,
        ),
        make_location_data(
            SC2Mission.END_GAME.mission_name,
            "Victory",
            SC2NCO_LOC_ID_OFFSET + 900,
            LocationType.VICTORY,
            lambda state: logic.end_game_requirement(state)
            and logic.nova_any_weapon(state),
        ),
        make_location_data(
            SC2Mission.END_GAME.mission_name,
            "Destroy the Xanthos",
            SC2NCO_LOC_ID_OFFSET + 901,
            LocationType.VANILLA,
            logic.end_game_requirement,
        ),
        make_location_data(
            SC2Mission.END_GAME.mission_name,
            "Disable Xanthos Railgun",
            SC2NCO_LOC_ID_OFFSET + 902,
            LocationType.EXTRA,
            logic.end_game_requirement,
        ),
        make_location_data(
            SC2Mission.END_GAME.mission_name,
            "Disable Xanthos Flamethrower",
            SC2NCO_LOC_ID_OFFSET + 903,
            LocationType.EXTRA,
            logic.end_game_requirement,
        ),
        make_location_data(
            SC2Mission.END_GAME.mission_name,
            "Disable Xanthos Fighter Bay",
            SC2NCO_LOC_ID_OFFSET + 904,
            LocationType.EXTRA,
            logic.end_game_requirement,
        ),
        make_location_data(
            SC2Mission.END_GAME.mission_name,
            "Disable Xanthos Missile Pods",
            SC2NCO_LOC_ID_OFFSET + 905,
            LocationType.EXTRA,
            logic.end_game_requirement,
        ),
        make_location_data(
            SC2Mission.END_GAME.mission_name,
            "Protect Hyperion",
            SC2NCO_LOC_ID_OFFSET + 906,
            LocationType.CHALLENGE,
            logic.end_game_requirement,
        ),
        make_location_data(
            SC2Mission.END_GAME.mission_name,
            "Destroy Orbital Commands",
            SC2NCO_LOC_ID_OFFSET + 907,
            LocationType.CHALLENGE,
            logic.end_game_requirement,
            flags=LocationFlag.BASEBUST,
        ),
        # Mission Variants
        # 10X/20X - Liberation Day
        make_location_data(
            SC2Mission.THE_OUTLAWS_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 300,
            LocationType.VICTORY,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.THE_OUTLAWS_Z.mission_name,
            "Rebel Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 301,
            LocationType.VANILLA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.THE_OUTLAWS_Z.mission_name,
            "North Resource Pickups",
            SC2_RACESWAP_LOC_ID_OFFSET + 302,
            LocationType.EXTRA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.THE_OUTLAWS_Z.mission_name,
            "Bunker",
            SC2_RACESWAP_LOC_ID_OFFSET + 303,
            LocationType.VANILLA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.THE_OUTLAWS_Z.mission_name,
            "Close Resource Pickups",
            SC2_RACESWAP_LOC_ID_OFFSET + 304,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_OUTLAWS_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 400,
            LocationType.VICTORY,
            logic.protoss_common_unit,
        ),
        make_location_data(
            SC2Mission.THE_OUTLAWS_P.mission_name,
            "Rebel Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 401,
            LocationType.VANILLA,
            logic.protoss_common_unit,
        ),
        make_location_data(
            SC2Mission.THE_OUTLAWS_P.mission_name,
            "North Resource Pickups",
            SC2_RACESWAP_LOC_ID_OFFSET + 402,
            LocationType.EXTRA,
            logic.protoss_common_unit,
        ),
        make_location_data(
            SC2Mission.THE_OUTLAWS_P.mission_name,
            "Bunker",
            SC2_RACESWAP_LOC_ID_OFFSET + 403,
            LocationType.VANILLA,
            logic.protoss_common_unit,
        ),
        make_location_data(
            SC2Mission.THE_OUTLAWS_P.mission_name,
            "Close Resource Pickups",
            SC2_RACESWAP_LOC_ID_OFFSET + 404,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 500,
            LocationType.VICTORY,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_defense_rating(state, True, True) >= 5
                and logic.zerg_basic_kerriganless_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR_Z.mission_name,
            "First Group Rescued",
            SC2_RACESWAP_LOC_ID_OFFSET + 501,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR_Z.mission_name,
            "Second Group Rescued",
            SC2_RACESWAP_LOC_ID_OFFSET + 502,
            LocationType.VANILLA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR_Z.mission_name,
            "Third Group Rescued",
            SC2_RACESWAP_LOC_ID_OFFSET + 503,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_defense_rating(state, True, True) >= 5
                and logic.zerg_basic_kerriganless_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR_Z.mission_name,
            "First Hatchery",
            SC2_RACESWAP_LOC_ID_OFFSET + 504,
            LocationType.CHALLENGE,
            logic.zerg_competent_comp_competent_aa,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR_Z.mission_name,
            "Second Hatchery",
            SC2_RACESWAP_LOC_ID_OFFSET + 505,
            LocationType.CHALLENGE,
            logic.zerg_competent_comp_competent_aa,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR_Z.mission_name,
            "Third Hatchery",
            SC2_RACESWAP_LOC_ID_OFFSET + 506,
            LocationType.CHALLENGE,
            logic.zerg_competent_comp_competent_aa,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR_Z.mission_name,
            "Fourth Hatchery",
            SC2_RACESWAP_LOC_ID_OFFSET + 507,
            LocationType.CHALLENGE,
            logic.zerg_competent_comp_competent_aa,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR_Z.mission_name,
            "Ride's on its Way",
            SC2_RACESWAP_LOC_ID_OFFSET + 508,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_defense_rating(state, True, True) >= 5
                and logic.zerg_basic_kerriganless_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR_Z.mission_name,
            "Hold Just a Little Longer",
            SC2_RACESWAP_LOC_ID_OFFSET + 509,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_defense_rating(state, True, True) >= 5
                and logic.zerg_basic_kerriganless_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR_Z.mission_name,
            "Cavalry's on the Way",
            SC2_RACESWAP_LOC_ID_OFFSET + 510,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_defense_rating(state, True, True) >= 5
                and logic.zerg_basic_kerriganless_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 600,
            LocationType.VICTORY,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_anti_light_anti_air(state)
                and (
                    state.has(item_names.PHOTON_CANNON, player)
                    or logic.protoss_basic_splash(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR_P.mission_name,
            "First Group Rescued",
            SC2_RACESWAP_LOC_ID_OFFSET + 601,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR_P.mission_name,
            "Second Group Rescued",
            SC2_RACESWAP_LOC_ID_OFFSET + 602,
            LocationType.VANILLA,
            logic.protoss_common_unit,
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR_P.mission_name,
            "Third Group Rescued",
            SC2_RACESWAP_LOC_ID_OFFSET + 603,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_anti_light_anti_air(state)
                and (
                    state.has(item_names.PHOTON_CANNON, player)
                    or logic.protoss_basic_splash(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR_P.mission_name,
            "First Hatchery",
            SC2_RACESWAP_LOC_ID_OFFSET + 604,
            LocationType.CHALLENGE,
            logic.protoss_competent_comp,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR_P.mission_name,
            "Second Hatchery",
            SC2_RACESWAP_LOC_ID_OFFSET + 605,
            LocationType.CHALLENGE,
            logic.protoss_competent_comp,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR_P.mission_name,
            "Third Hatchery",
            SC2_RACESWAP_LOC_ID_OFFSET + 606,
            LocationType.CHALLENGE,
            logic.protoss_competent_comp,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR_P.mission_name,
            "Fourth Hatchery",
            SC2_RACESWAP_LOC_ID_OFFSET + 607,
            LocationType.CHALLENGE,
            logic.protoss_competent_comp,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR_P.mission_name,
            "Ride's on its Way",
            SC2_RACESWAP_LOC_ID_OFFSET + 608,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_anti_light_anti_air(state)
                and (
                    state.has(item_names.PHOTON_CANNON, player)
                    or logic.protoss_basic_splash(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR_P.mission_name,
            "Hold Just a Little Longer",
            SC2_RACESWAP_LOC_ID_OFFSET + 609,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_anti_light_anti_air(state)
                and (
                    state.has(item_names.PHOTON_CANNON, player)
                    or logic.protoss_basic_splash(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.ZERO_HOUR_P.mission_name,
            "Cavalry's on the Way",
            SC2_RACESWAP_LOC_ID_OFFSET + 610,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_anti_light_anti_air(state)
                and (
                    state.has(item_names.PHOTON_CANNON, player)
                    or logic.protoss_basic_splash(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.EVACUATION_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 700,
            LocationType.VICTORY,
            lambda state: (
                logic.zerg_common_unit(state)
                and (
                    logic.zerg_competent_anti_air(state)
                    or (adv_tactics and logic.zerg_basic_kerriganless_anti_air(state))
                )
            ),
        ),
        make_location_data(
            SC2Mission.EVACUATION_Z.mission_name,
            "North Chrysalis",
            SC2_RACESWAP_LOC_ID_OFFSET + 701,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.EVACUATION_Z.mission_name,
            "West Chrysalis",
            SC2_RACESWAP_LOC_ID_OFFSET + 702,
            LocationType.VANILLA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.EVACUATION_Z.mission_name,
            "East Chrysalis",
            SC2_RACESWAP_LOC_ID_OFFSET + 703,
            LocationType.VANILLA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.EVACUATION_Z.mission_name,
            "Reach Hanson",
            SC2_RACESWAP_LOC_ID_OFFSET + 704,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.EVACUATION_Z.mission_name,
            "Secret Resource Stash",
            SC2_RACESWAP_LOC_ID_OFFSET + 705,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.EVACUATION_Z.mission_name,
            "Flawless",
            SC2_RACESWAP_LOC_ID_OFFSET + 706,
            LocationType.CHALLENGE,
            lambda state: (
                logic.zerg_common_unit(state)
                and logic.zerg_defense_rating(state, True, False) >= 5
                and (
                    (adv_tactics and logic.zerg_basic_kerriganless_anti_air(state))
                    or logic.zerg_competent_anti_air(state)
                )
            ),
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.EVACUATION_Z.mission_name,
            "Western Zerg Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 707,
            LocationType.MASTERY,
            lambda state: (
                logic.zerg_common_unit_competent_aa(state)
                and logic.zerg_base_buster(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.EVACUATION_Z.mission_name,
            "Eastern Zerg Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 708,
            LocationType.MASTERY,
            lambda state: (
                logic.zerg_common_unit_competent_aa(state)
                and logic.zerg_base_buster(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.EVACUATION_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 800,
            LocationType.VICTORY,
            lambda state: (
                logic.protoss_common_unit(state)
                and (
                    (adv_tactics and logic.protoss_basic_anti_air(state))
                    or logic.protoss_anti_light_anti_air(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.EVACUATION_P.mission_name,
            "North Chrysalis",
            SC2_RACESWAP_LOC_ID_OFFSET + 801,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.EVACUATION_P.mission_name,
            "West Chrysalis",
            SC2_RACESWAP_LOC_ID_OFFSET + 802,
            LocationType.VANILLA,
            logic.protoss_common_unit,
        ),
        make_location_data(
            SC2Mission.EVACUATION_P.mission_name,
            "East Chrysalis",
            SC2_RACESWAP_LOC_ID_OFFSET + 803,
            LocationType.VANILLA,
            logic.protoss_common_unit,
        ),
        make_location_data(
            SC2Mission.EVACUATION_P.mission_name,
            "Reach Hanson",
            SC2_RACESWAP_LOC_ID_OFFSET + 804,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.EVACUATION_P.mission_name,
            "Secret Resource Stash",
            SC2_RACESWAP_LOC_ID_OFFSET + 805,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.EVACUATION_P.mission_name,
            "Flawless",
            SC2_RACESWAP_LOC_ID_OFFSET + 806,
            LocationType.CHALLENGE,
            lambda state: (
                logic.protoss_defense_rating(state, True) >= 2
                and logic.protoss_common_unit(state)
                and (
                    (adv_tactics and logic.protoss_basic_anti_air(state))
                    or logic.protoss_anti_light_anti_air(state)
                )
            ),
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.EVACUATION_P.mission_name,
            "Western Zerg Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 807,
            LocationType.MASTERY,
            logic.protoss_competent_comp,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.EVACUATION_P.mission_name,
            "Eastern Zerg Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 808,
            LocationType.MASTERY,
            logic.protoss_competent_comp,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.OUTBREAK_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 900,
            LocationType.VICTORY,
            logic.zerg_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.OUTBREAK_Z.mission_name,
            "Left Infestor",
            SC2_RACESWAP_LOC_ID_OFFSET + 901,
            LocationType.VANILLA,
            logic.zerg_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.OUTBREAK_Z.mission_name,
            "Right Infestor",
            SC2_RACESWAP_LOC_ID_OFFSET + 902,
            LocationType.VANILLA,
            logic.zerg_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.OUTBREAK_Z.mission_name,
            "North Infested Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 903,
            LocationType.EXTRA,
            logic.zerg_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.OUTBREAK_Z.mission_name,
            "South Infested Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 904,
            LocationType.EXTRA,
            logic.zerg_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.OUTBREAK_Z.mission_name,
            "Northwest Bar",
            SC2_RACESWAP_LOC_ID_OFFSET + 905,
            LocationType.EXTRA,
            logic.zerg_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.OUTBREAK_Z.mission_name,
            "North Bar",
            SC2_RACESWAP_LOC_ID_OFFSET + 906,
            LocationType.EXTRA,
            logic.zerg_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.OUTBREAK_Z.mission_name,
            "South Bar",
            SC2_RACESWAP_LOC_ID_OFFSET + 907,
            LocationType.EXTRA,
            logic.zerg_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.OUTBREAK_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 1000,
            LocationType.VICTORY,
            logic.protoss_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.OUTBREAK_P.mission_name,
            "Left Infestor",
            SC2_RACESWAP_LOC_ID_OFFSET + 1001,
            LocationType.VANILLA,
            logic.protoss_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.OUTBREAK_P.mission_name,
            "Right Infestor",
            SC2_RACESWAP_LOC_ID_OFFSET + 1002,
            LocationType.VANILLA,
            logic.protoss_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.OUTBREAK_P.mission_name,
            "North Infested Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 1003,
            LocationType.EXTRA,
            logic.protoss_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.OUTBREAK_P.mission_name,
            "South Infested Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 1004,
            LocationType.EXTRA,
            logic.protoss_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.OUTBREAK_P.mission_name,
            "Northwest Bar",
            SC2_RACESWAP_LOC_ID_OFFSET + 1005,
            LocationType.EXTRA,
            logic.protoss_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.OUTBREAK_P.mission_name,
            "North Bar",
            SC2_RACESWAP_LOC_ID_OFFSET + 1006,
            LocationType.EXTRA,
            logic.protoss_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.OUTBREAK_P.mission_name,
            "South Bar",
            SC2_RACESWAP_LOC_ID_OFFSET + 1007,
            LocationType.EXTRA,
            logic.protoss_outbreak_requirement,
        ),
        make_location_data(
            SC2Mission.SAFE_HAVEN_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 1100,
            LocationType.VICTORY,
            lambda state: logic.zerg_common_unit(state)
            and logic.zerg_competent_anti_air(state),
            hard_rule=logic.zerg_any_anti_air,
        ),
        make_location_data(
            SC2Mission.SAFE_HAVEN_Z.mission_name,
            "North Nexus",
            SC2_RACESWAP_LOC_ID_OFFSET + 1101,
            LocationType.EXTRA,
            lambda state: logic.zerg_common_unit(state)
            and logic.zerg_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.SAFE_HAVEN_Z.mission_name,
            "East Nexus",
            SC2_RACESWAP_LOC_ID_OFFSET + 1102,
            LocationType.EXTRA,
            lambda state: logic.zerg_common_unit(state)
            and logic.zerg_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.SAFE_HAVEN_Z.mission_name,
            "South Nexus",
            SC2_RACESWAP_LOC_ID_OFFSET + 1103,
            LocationType.EXTRA,
            lambda state: logic.zerg_common_unit(state)
            and logic.zerg_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.SAFE_HAVEN_Z.mission_name,
            "First Terror Fleet",
            SC2_RACESWAP_LOC_ID_OFFSET + 1104,
            LocationType.VANILLA,
            lambda state: logic.zerg_common_unit(state)
            and logic.zerg_competent_anti_air(state),
            hard_rule=logic.zerg_any_anti_air,
        ),
        make_location_data(
            SC2Mission.SAFE_HAVEN_Z.mission_name,
            "Second Terror Fleet",
            SC2_RACESWAP_LOC_ID_OFFSET + 1105,
            LocationType.VANILLA,
            lambda state: logic.zerg_common_unit(state)
            and logic.zerg_competent_anti_air(state),
            hard_rule=logic.zerg_any_anti_air,
        ),
        make_location_data(
            SC2Mission.SAFE_HAVEN_Z.mission_name,
            "Third Terror Fleet",
            SC2_RACESWAP_LOC_ID_OFFSET + 1106,
            LocationType.VANILLA,
            lambda state: logic.zerg_common_unit(state)
            and logic.zerg_competent_anti_air(state),
            hard_rule=logic.zerg_any_anti_air,
        ),
        make_location_data(
            SC2Mission.SAFE_HAVEN_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 1200,
            LocationType.VICTORY,
            lambda state: logic.protoss_common_unit(state)
            and logic.protoss_anti_armor_anti_air(state),
            hard_rule=logic.protoss_any_anti_air_unit_or_soa_any_protoss,
        ),
        make_location_data(
            SC2Mission.SAFE_HAVEN_P.mission_name,
            "North Nexus",
            SC2_RACESWAP_LOC_ID_OFFSET + 1201,
            LocationType.EXTRA,
            lambda state: logic.protoss_common_unit(state)
            and logic.protoss_anti_armor_anti_air(state),
        ),
        make_location_data(
            SC2Mission.SAFE_HAVEN_P.mission_name,
            "East Nexus",
            SC2_RACESWAP_LOC_ID_OFFSET + 1202,
            LocationType.EXTRA,
            lambda state: logic.protoss_common_unit(state)
            and logic.protoss_anti_armor_anti_air(state),
        ),
        make_location_data(
            SC2Mission.SAFE_HAVEN_P.mission_name,
            "South Nexus",
            SC2_RACESWAP_LOC_ID_OFFSET + 1203,
            LocationType.EXTRA,
            lambda state: logic.protoss_common_unit(state)
            and logic.protoss_anti_armor_anti_air(state),
        ),
        make_location_data(
            SC2Mission.SAFE_HAVEN_P.mission_name,
            "First Terror Fleet",
            SC2_RACESWAP_LOC_ID_OFFSET + 1204,
            LocationType.VANILLA,
            lambda state: logic.protoss_common_unit(state)
            and logic.protoss_anti_armor_anti_air(state),
            hard_rule=logic.protoss_any_anti_air_unit_or_soa_any_protoss,
        ),
        make_location_data(
            SC2Mission.SAFE_HAVEN_P.mission_name,
            "Second Terror Fleet",
            SC2_RACESWAP_LOC_ID_OFFSET + 1205,
            LocationType.VANILLA,
            lambda state: logic.protoss_common_unit(state)
            and logic.protoss_anti_armor_anti_air(state),
            hard_rule=logic.protoss_any_anti_air_unit_or_soa_any_protoss,
        ),
        make_location_data(
            SC2Mission.SAFE_HAVEN_P.mission_name,
            "Third Terror Fleet",
            SC2_RACESWAP_LOC_ID_OFFSET + 1206,
            LocationType.VANILLA,
            lambda state: logic.protoss_common_unit(state)
            and logic.protoss_anti_armor_anti_air(state),
            hard_rule=logic.protoss_any_anti_air_unit_or_soa_any_protoss,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 1300,
            LocationType.VICTORY,
            logic.zerg_havens_fall_requirement,
            hard_rule=logic.zerg_any_anti_air,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_Z.mission_name,
            "North Hive",
            SC2_RACESWAP_LOC_ID_OFFSET + 1301,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state) and logic.zerg_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_Z.mission_name,
            "East Hive",
            SC2_RACESWAP_LOC_ID_OFFSET + 1302,
            LocationType.VANILLA,
            logic.zerg_havens_fall_requirement,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_Z.mission_name,
            "South Hive",
            SC2_RACESWAP_LOC_ID_OFFSET + 1303,
            LocationType.VANILLA,
            logic.zerg_havens_fall_requirement,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_Z.mission_name,
            "Northeast Colony Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 1304,
            LocationType.CHALLENGE,
            logic.zerg_havens_fall_requirement,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_Z.mission_name,
            "East Colony Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 1305,
            LocationType.CHALLENGE,
            logic.zerg_respond_to_colony_infestations,
            hard_rule=logic.zerg_any_anti_air,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_Z.mission_name,
            "Middle Colony Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 1306,
            LocationType.CHALLENGE,
            logic.zerg_respond_to_colony_infestations,
            hard_rule=logic.zerg_any_anti_air,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_Z.mission_name,
            "Southeast Colony Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 1307,
            LocationType.CHALLENGE,
            logic.zerg_respond_to_colony_infestations,
            hard_rule=logic.zerg_any_anti_air,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_Z.mission_name,
            "Southwest Colony Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 1308,
            LocationType.CHALLENGE,
            logic.zerg_respond_to_colony_infestations,
            hard_rule=logic.zerg_any_anti_air,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_Z.mission_name,
            "Southwest Gas Pickups",
            SC2_RACESWAP_LOC_ID_OFFSET + 1309,
            LocationType.EXTRA,
            lambda state: state.has_any(
                (item_names.OVERLORD_VENTRAL_SACS, item_names.YGGDRASIL), player
            )
            or adv_tactics
            and state.has_all(
                (
                    item_names.INFESTED_BANSHEE,
                    item_names.INFESTED_BANSHEE_RAPID_HIBERNATION,
                ),
                player,
            ),
            hard_rule=logic.zerg_can_collect_pickup_across_gap,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_Z.mission_name,
            "East Gas Pickups",
            SC2_RACESWAP_LOC_ID_OFFSET + 1310,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_havens_fall_requirement(state)
                and (
                    state.has(item_names.OVERLORD_VENTRAL_SACS, player)
                    or adv_tactics
                    and (
                        state.has_all(
                            (
                                item_names.INFESTED_BANSHEE,
                                item_names.INFESTED_BANSHEE_RAPID_HIBERNATION,
                            ),
                            player,
                        )
                        or state.has(item_names.YGGDRASIL, player)
                        or logic.morph_viper(state)
                    )
                )
            ),
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_Z.mission_name,
            "Southeast Gas Pickups",
            SC2_RACESWAP_LOC_ID_OFFSET + 1311,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_havens_fall_requirement(state)
                and (
                    state.has(item_names.OVERLORD_VENTRAL_SACS, player)
                    or adv_tactics
                    and (
                        state.has_all(
                            (
                                item_names.INFESTED_BANSHEE,
                                item_names.INFESTED_BANSHEE_RAPID_HIBERNATION,
                            ),
                            player,
                        )
                        or state.has(item_names.YGGDRASIL, player)
                    )
                )
            ),
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 1400,
            LocationType.VICTORY,
            logic.protoss_havens_fall_requirement,
            hard_rule=logic.protoss_any_anti_air_unit_or_soa_any_protoss,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_P.mission_name,
            "North Hive",
            SC2_RACESWAP_LOC_ID_OFFSET + 1401,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_P.mission_name,
            "East Hive",
            SC2_RACESWAP_LOC_ID_OFFSET + 1402,
            LocationType.VANILLA,
            logic.protoss_havens_fall_requirement,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_P.mission_name,
            "South Hive",
            SC2_RACESWAP_LOC_ID_OFFSET + 1403,
            LocationType.VANILLA,
            logic.protoss_havens_fall_requirement,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_P.mission_name,
            "Northeast Colony Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 1404,
            LocationType.CHALLENGE,
            logic.protoss_respond_to_colony_infestations,
            hard_rule=logic.protoss_any_anti_air_unit_or_soa_any_protoss,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_P.mission_name,
            "East Colony Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 1405,
            LocationType.CHALLENGE,
            logic.protoss_respond_to_colony_infestations,
            hard_rule=logic.protoss_any_anti_air_unit_or_soa_any_protoss,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_P.mission_name,
            "Middle Colony Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 1406,
            LocationType.CHALLENGE,
            logic.protoss_respond_to_colony_infestations,
            hard_rule=logic.protoss_any_anti_air_unit_or_soa_any_protoss,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_P.mission_name,
            "Southeast Colony Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 1407,
            LocationType.CHALLENGE,
            logic.protoss_respond_to_colony_infestations,
            hard_rule=logic.protoss_any_anti_air_unit_or_soa_any_protoss,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_P.mission_name,
            "Southwest Colony Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 1408,
            LocationType.CHALLENGE,
            logic.protoss_respond_to_colony_infestations,
            hard_rule=logic.protoss_any_anti_air_unit_or_soa_any_protoss,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_P.mission_name,
            "Southwest Gas Pickups",
            SC2_RACESWAP_LOC_ID_OFFSET + 1409,
            LocationType.EXTRA,
            lambda state: (
                state.has(item_names.WARP_PRISM, player)
                or adv_tactics
                and (
                    state.has_all(
                        (item_names.MISTWING, item_names.MISTWING_PILOT), player
                    )
                    or state.has(item_names.ARBITER, player)
                )
            ),
            hard_rule=logic.protoss_any_gap_transport,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_P.mission_name,
            "East Gas Pickups",
            SC2_RACESWAP_LOC_ID_OFFSET + 1410,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_havens_fall_requirement(state)
                and (
                    state.has(item_names.WARP_PRISM, player)
                    or adv_tactics
                    and (
                        state.has_all(
                            (item_names.MISTWING, item_names.MISTWING_PILOT), player
                        )
                        or state.has(item_names.ARBITER, player)
                    )
                )
            ),
            hard_rule=logic.protoss_any_gap_transport,
        ),
        make_location_data(
            SC2Mission.HAVENS_FALL_P.mission_name,
            "Southeast Gas Pickups",
            SC2_RACESWAP_LOC_ID_OFFSET + 1411,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_havens_fall_requirement(state)
                and (
                    state.has(item_names.WARP_PRISM, player)
                    or adv_tactics
                    and (
                        state.has_all(
                            (item_names.MISTWING, item_names.MISTWING_PILOT), player
                        )
                        or state.has(item_names.ARBITER, player)
                    )
                )
            ),
            hard_rule=logic.protoss_any_gap_transport,
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 1500,
            LocationType.VICTORY,
            lambda state: (
                logic.zerg_common_unit(state)
                and (
                    (adv_tactics and logic.zerg_moderate_anti_air(state))
                    or logic.zerg_competent_anti_air(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB_Z.mission_name,
            "First Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 1501,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB_Z.mission_name,
            "Second Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 1502,
            LocationType.VANILLA,
            lambda state: logic.zerg_common_unit(state)
            or state.has(item_names.OVERLORD_VENTRAL_SACS, player),
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB_Z.mission_name,
            "Third Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 1503,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and (
                    (adv_tactics and logic.zerg_moderate_anti_air(state))
                    or logic.zerg_competent_anti_air(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB_Z.mission_name,
            "Fourth Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 1504,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state)
                and (
                    (adv_tactics and logic.zerg_moderate_anti_air(state))
                    or logic.zerg_competent_anti_air(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB_Z.mission_name,
            "First Forcefield Area Busted",
            SC2_RACESWAP_LOC_ID_OFFSET + 1505,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and (
                    (adv_tactics and logic.zerg_moderate_anti_air(state))
                    or logic.zerg_competent_anti_air(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB_Z.mission_name,
            "Second Forcefield Area Busted",
            SC2_RACESWAP_LOC_ID_OFFSET + 1506,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state)
                and (
                    (adv_tactics and logic.zerg_moderate_anti_air(state))
                    or logic.zerg_competent_anti_air(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB_Z.mission_name,
            "Defeat Kerrigan",
            SC2_RACESWAP_LOC_ID_OFFSET + 1507,
            LocationType.MASTERY,
            lambda state: (
                logic.zerg_common_unit_competent_aa(state)
                and logic.zerg_base_buster(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 1600,
            LocationType.VICTORY,
            lambda state: (
                logic.protoss_common_unit(state)
                and (
                    (adv_tactics and logic.protoss_basic_anti_air(state))
                    or logic.protoss_anti_light_anti_air(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB_P.mission_name,
            "First Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 1601,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB_P.mission_name,
            "Second Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 1602,
            LocationType.VANILLA,
            lambda state: adv_tactics or logic.protoss_common_unit(state),
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB_P.mission_name,
            "Third Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 1603,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_common_unit(state)
                and (
                    (adv_tactics and logic.protoss_basic_anti_air(state))
                    or logic.protoss_anti_light_anti_air(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB_P.mission_name,
            "Fourth Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 1604,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_common_unit(state)
                and (
                    (adv_tactics and logic.protoss_basic_anti_air(state))
                    or logic.protoss_anti_light_anti_air(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB_P.mission_name,
            "First Forcefield Area Busted",
            SC2_RACESWAP_LOC_ID_OFFSET + 1605,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state)
                and (
                    (adv_tactics and logic.protoss_basic_anti_air(state))
                    or logic.protoss_anti_light_anti_air(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB_P.mission_name,
            "Second Forcefield Area Busted",
            SC2_RACESWAP_LOC_ID_OFFSET + 1606,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state)
                and (
                    (adv_tactics and logic.protoss_basic_anti_air(state))
                    or logic.protoss_anti_light_anti_air(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.SMASH_AND_GRAB_P.mission_name,
            "Defeat Kerrigan",
            SC2_RACESWAP_LOC_ID_OFFSET + 1607,
            LocationType.MASTERY,
            logic.protoss_deathball,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.THE_DIG_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 1700,
            LocationType.VICTORY,
            lambda state: (
                (
                    logic.zerg_competent_anti_air(state)
                    or adv_tactics
                    and logic.zerg_moderate_anti_air(state)
                )
                and logic.zerg_defense_rating(state, False, True) >= 8
                and logic.zerg_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG_Z.mission_name,
            "Left Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 1701,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_defense_rating(state, False, False) >= 6
                and logic.zerg_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG_Z.mission_name,
            "Right Ground Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 1702,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_defense_rating(state, False, False) >= 6
                and logic.zerg_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG_Z.mission_name,
            "Right Cliff Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 1703,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_defense_rating(state, False, False) >= 6
                and logic.zerg_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG_Z.mission_name,
            "Moebius Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 1704,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_DIG_Z.mission_name,
            "Door Outer Layer",
            SC2_RACESWAP_LOC_ID_OFFSET + 1705,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_defense_rating(state, False, False) >= 6
                and logic.zerg_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG_Z.mission_name,
            "Door Thermal Barrier",
            SC2_RACESWAP_LOC_ID_OFFSET + 1706,
            LocationType.EXTRA,
            lambda state: (
                (
                    logic.zerg_competent_anti_air(state)
                    or adv_tactics
                    and logic.zerg_moderate_anti_air(state)
                )
                and logic.zerg_defense_rating(state, False, True) >= 8
                and logic.zerg_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG_Z.mission_name,
            "Cutting Through the Core",
            SC2_RACESWAP_LOC_ID_OFFSET + 1707,
            LocationType.EXTRA,
            lambda state: (
                (
                    logic.zerg_competent_anti_air(state)
                    or adv_tactics
                    and logic.zerg_moderate_anti_air(state)
                )
                and logic.zerg_defense_rating(state, False, True) >= 8
                and logic.zerg_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG_Z.mission_name,
            "Structure Access Imminent",
            SC2_RACESWAP_LOC_ID_OFFSET + 1708,
            LocationType.EXTRA,
            lambda state: (
                (
                    logic.zerg_competent_anti_air(state)
                    or adv_tactics
                    and logic.zerg_moderate_anti_air(state)
                )
                and logic.zerg_defense_rating(state, False, True) >= 8
                and logic.zerg_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG_Z.mission_name,
            "Northwestern Protoss Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 1709,
            LocationType.MASTERY,
            lambda state: (
                logic.zerg_competent_anti_air(state)
                and logic.zerg_defense_rating(state, False, True) >= 8
                and logic.zerg_common_unit(state)
                and logic.zerg_base_buster(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.THE_DIG_Z.mission_name,
            "Northeastern Protoss Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 1710,
            LocationType.MASTERY,
            lambda state: (
                logic.zerg_competent_anti_air(state)
                and logic.zerg_defense_rating(state, False, True) >= 8
                and logic.zerg_common_unit(state)
                and logic.zerg_base_buster(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.THE_DIG_Z.mission_name,
            "Eastern Protoss Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 1711,
            LocationType.MASTERY,
            lambda state: (
                logic.zerg_competent_anti_air(state)
                and logic.zerg_defense_rating(state, False, True) >= 8
                and logic.zerg_common_unit(state)
                and logic.zerg_base_buster(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.THE_DIG_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 1800,
            LocationType.VICTORY,
            lambda state: (
                (
                    logic.protoss_anti_armor_anti_air(state)
                    or adv_tactics
                    and logic.protoss_moderate_anti_air(state)
                )
                and logic.protoss_defense_rating(state, False) >= 6
                and logic.protoss_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG_P.mission_name,
            "Left Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 1801,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_defense_rating(state, False) >= 6
                and logic.protoss_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG_P.mission_name,
            "Right Ground Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 1802,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_defense_rating(state, False) >= 6
                and logic.protoss_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG_P.mission_name,
            "Right Cliff Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 1803,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_defense_rating(state, False) >= 6
                and logic.protoss_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG_P.mission_name,
            "Moebius Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 1804,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_DIG_P.mission_name,
            "Door Outer Layer",
            SC2_RACESWAP_LOC_ID_OFFSET + 1805,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_defense_rating(state, False) >= 6
                and logic.protoss_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG_P.mission_name,
            "Door Thermal Barrier",
            SC2_RACESWAP_LOC_ID_OFFSET + 1806,
            LocationType.EXTRA,
            lambda state: (
                (
                    logic.protoss_anti_armor_anti_air(state)
                    or adv_tactics
                    and logic.protoss_moderate_anti_air(state)
                )
                and logic.protoss_defense_rating(state, False) >= 6
                and logic.protoss_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG_P.mission_name,
            "Cutting Through the Core",
            SC2_RACESWAP_LOC_ID_OFFSET + 1807,
            LocationType.EXTRA,
            lambda state: (
                (
                    logic.protoss_anti_armor_anti_air(state)
                    or adv_tactics
                    and logic.protoss_moderate_anti_air(state)
                )
                and logic.protoss_defense_rating(state, False) >= 6
                and logic.protoss_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG_P.mission_name,
            "Structure Access Imminent",
            SC2_RACESWAP_LOC_ID_OFFSET + 1808,
            LocationType.EXTRA,
            lambda state: (
                (
                    logic.protoss_anti_armor_anti_air(state)
                    or adv_tactics
                    and logic.protoss_moderate_anti_air(state)
                )
                and logic.protoss_defense_rating(state, False) >= 6
                and logic.protoss_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_DIG_P.mission_name,
            "Northwestern Protoss Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 1809,
            LocationType.MASTERY,
            lambda state: (
                logic.protoss_anti_armor_anti_air(state)
                and logic.protoss_defense_rating(state, False) >= 6
                and logic.protoss_common_unit(state)
                and logic.protoss_deathball(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.THE_DIG_P.mission_name,
            "Northeastern Protoss Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 1810,
            LocationType.MASTERY,
            lambda state: (
                logic.protoss_anti_armor_anti_air(state)
                and logic.protoss_defense_rating(state, False) >= 6
                and logic.protoss_common_unit(state)
                and logic.protoss_deathball(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.THE_DIG_P.mission_name,
            "Eastern Protoss Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 1811,
            LocationType.MASTERY,
            lambda state: (
                logic.protoss_anti_armor_anti_air(state)
                and logic.protoss_defense_rating(state, False) >= 6
                and logic.protoss_common_unit(state)
                and logic.protoss_deathball(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 1900,
            LocationType.VICTORY,
            lambda state: (
                logic.zerg_moderate_anti_air(state)
                and (
                    logic.zerg_versatile_air(state)
                    or state.has_any(
                        {
                            item_names.YGGDRASIL,
                            item_names.OVERLORD_VENTRAL_SACS,
                            item_names.NYDUS_WORM,
                            item_names.BULLFROG,
                        },
                        player,
                    )
                    and logic.zerg_common_unit(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR_Z.mission_name,
            "1st Data Core",
            SC2_RACESWAP_LOC_ID_OFFSET + 1901,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR_Z.mission_name,
            "2nd Data Core",
            SC2_RACESWAP_LOC_ID_OFFSET + 1902,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_versatile_air(state)
                or state.has_any(
                    {
                        item_names.YGGDRASIL,
                        item_names.OVERLORD_VENTRAL_SACS,
                        item_names.NYDUS_WORM,
                        item_names.BULLFROG,
                    },
                    player,
                )
                and logic.zerg_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR_Z.mission_name,
            "South Rescue",
            SC2_RACESWAP_LOC_ID_OFFSET + 1903,
            LocationType.EXTRA,
            lambda state: state.has_any(
                {
                    item_names.YGGDRASIL,
                    item_names.OVERLORD_VENTRAL_SACS,
                    item_names.NYDUS_WORM,
                    item_names.BULLFROG,
                },
                player,
            ),
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR_Z.mission_name,
            "Wall Rescue",
            SC2_RACESWAP_LOC_ID_OFFSET + 1904,
            LocationType.EXTRA,
            lambda state: state.has_any(
                {
                    item_names.YGGDRASIL,
                    item_names.OVERLORD_VENTRAL_SACS,
                    item_names.NYDUS_WORM,
                    item_names.BULLFROG,
                },
                player,
            ),
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR_Z.mission_name,
            "Mid Rescue",
            SC2_RACESWAP_LOC_ID_OFFSET + 1905,
            LocationType.EXTRA,
            lambda state: state.has_any(
                {
                    item_names.YGGDRASIL,
                    item_names.OVERLORD_VENTRAL_SACS,
                    item_names.NYDUS_WORM,
                    item_names.BULLFROG,
                },
                player,
            ),
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR_Z.mission_name,
            "Nydus Roof Rescue",
            SC2_RACESWAP_LOC_ID_OFFSET + 1906,
            LocationType.EXTRA,
            lambda state: state.has_any(
                {
                    item_names.YGGDRASIL,
                    item_names.OVERLORD_VENTRAL_SACS,
                    item_names.NYDUS_WORM,
                    item_names.BULLFROG,
                },
                player,
            ),
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR_Z.mission_name,
            "Alive Inside Rescue",
            SC2_RACESWAP_LOC_ID_OFFSET + 1907,
            LocationType.EXTRA,
            lambda state: state.has_any(
                {
                    item_names.YGGDRASIL,
                    item_names.OVERLORD_VENTRAL_SACS,
                    item_names.NYDUS_WORM,
                    item_names.BULLFROG,
                },
                player,
            ),
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR_Z.mission_name,
            "Brutalisk",
            SC2_RACESWAP_LOC_ID_OFFSET + 1908,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_moderate_anti_air(state)
                and (
                    logic.zerg_versatile_air(state)
                    or state.has_any(
                        {
                            item_names.YGGDRASIL,
                            item_names.OVERLORD_VENTRAL_SACS,
                            item_names.NYDUS_WORM,
                            item_names.BULLFROG,
                        },
                        player,
                    )
                    and logic.zerg_common_unit(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR_Z.mission_name,
            "3rd Data Core",
            SC2_RACESWAP_LOC_ID_OFFSET + 1909,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_moderate_anti_air(state)
                and (
                    logic.zerg_versatile_air(state)
                    or state.has_any(
                        {
                            item_names.YGGDRASIL,
                            item_names.OVERLORD_VENTRAL_SACS,
                            item_names.NYDUS_WORM,
                            item_names.BULLFROG,
                        },
                        player,
                    )
                    and logic.zerg_common_unit(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 2000,
            LocationType.VICTORY,
            lambda state: (
                logic.protoss_moderate_anti_air(state)
                and (
                    logic.protoss_fleet(state)
                    or state.has(item_names.WARP_PRISM, player)
                    and logic.protoss_common_unit(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR_P.mission_name,
            "1st Data Core",
            SC2_RACESWAP_LOC_ID_OFFSET + 2001,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR_P.mission_name,
            "2nd Data Core",
            SC2_RACESWAP_LOC_ID_OFFSET + 2002,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_fleet(state)
                or (
                    state.has(item_names.WARP_PRISM, player)
                    and logic.protoss_common_unit(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR_P.mission_name,
            "South Rescue",
            SC2_RACESWAP_LOC_ID_OFFSET + 2003,
            LocationType.EXTRA,
            lambda state: adv_tactics or state.has(item_names.WARP_PRISM, player),
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR_P.mission_name,
            "Wall Rescue",
            SC2_RACESWAP_LOC_ID_OFFSET + 2004,
            LocationType.EXTRA,
            lambda state: adv_tactics or state.has(item_names.WARP_PRISM, player),
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR_P.mission_name,
            "Mid Rescue",
            SC2_RACESWAP_LOC_ID_OFFSET + 2005,
            LocationType.EXTRA,
            lambda state: adv_tactics or state.has(item_names.WARP_PRISM, player),
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR_P.mission_name,
            "Nydus Roof Rescue",
            SC2_RACESWAP_LOC_ID_OFFSET + 2006,
            LocationType.EXTRA,
            lambda state: adv_tactics or state.has(item_names.WARP_PRISM, player),
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR_P.mission_name,
            "Alive Inside Rescue",
            SC2_RACESWAP_LOC_ID_OFFSET + 2007,
            LocationType.EXTRA,
            lambda state: adv_tactics or state.has(item_names.WARP_PRISM, player),
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR_P.mission_name,
            "Brutalisk",
            SC2_RACESWAP_LOC_ID_OFFSET + 2008,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_moderate_anti_air(state)
                and (
                    logic.protoss_fleet(state)
                    or state.has(item_names.WARP_PRISM, player)
                    and logic.protoss_common_unit(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.THE_MOEBIUS_FACTOR_P.mission_name,
            "3rd Data Core",
            SC2_RACESWAP_LOC_ID_OFFSET + 2009,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_moderate_anti_air(state)
                and (
                    logic.protoss_fleet(state)
                    or state.has(item_names.WARP_PRISM, player)
                    and logic.protoss_common_unit(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.SUPERNOVA_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 2100,
            LocationType.VICTORY,
            logic.zerg_supernova_requirement,
        ),
        make_location_data(
            SC2Mission.SUPERNOVA_Z.mission_name,
            "West Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 2101,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.SUPERNOVA_Z.mission_name,
            "North Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 2102,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.SUPERNOVA_Z.mission_name,
            "South Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 2103,
            LocationType.VANILLA,
            logic.zerg_supernova_requirement,
        ),
        make_location_data(
            SC2Mission.SUPERNOVA_Z.mission_name,
            "East Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 2104,
            LocationType.VANILLA,
            logic.zerg_supernova_requirement,
        ),
        make_location_data(
            SC2Mission.SUPERNOVA_Z.mission_name,
            "Landing Zone Cleared",
            SC2_RACESWAP_LOC_ID_OFFSET + 2105,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.SUPERNOVA_Z.mission_name,
            "Middle Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 2106,
            LocationType.EXTRA,
            logic.zerg_supernova_requirement,
        ),
        make_location_data(
            SC2Mission.SUPERNOVA_Z.mission_name,
            "Southeast Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 2107,
            LocationType.EXTRA,
            logic.zerg_supernova_requirement,
        ),
        make_location_data(
            SC2Mission.SUPERNOVA_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 2200,
            LocationType.VICTORY,
            logic.protoss_supernova_requirement,
        ),
        make_location_data(
            SC2Mission.SUPERNOVA_P.mission_name,
            "West Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 2201,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.SUPERNOVA_P.mission_name,
            "North Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 2202,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.SUPERNOVA_P.mission_name,
            "South Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 2203,
            LocationType.VANILLA,
            logic.protoss_supernova_requirement,
        ),
        make_location_data(
            SC2Mission.SUPERNOVA_P.mission_name,
            "East Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 2204,
            LocationType.VANILLA,
            logic.protoss_supernova_requirement,
        ),
        make_location_data(
            SC2Mission.SUPERNOVA_P.mission_name,
            "Landing Zone Cleared",
            SC2_RACESWAP_LOC_ID_OFFSET + 2205,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.SUPERNOVA_P.mission_name,
            "Middle Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 2206,
            LocationType.EXTRA,
            logic.protoss_supernova_requirement,
        ),
        make_location_data(
            SC2Mission.SUPERNOVA_P.mission_name,
            "Southeast Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 2207,
            LocationType.EXTRA,
            logic.protoss_supernova_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 2300,
            LocationType.VICTORY,
            logic.zerg_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_Z.mission_name,
            "Landing Zone Cleared",
            SC2_RACESWAP_LOC_ID_OFFSET + 2301,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_Z.mission_name,
            "Expansion Prisoners",
            SC2_RACESWAP_LOC_ID_OFFSET + 2302,
            LocationType.VANILLA,
            logic.zerg_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_Z.mission_name,
            "South Close Prisoners",
            SC2_RACESWAP_LOC_ID_OFFSET + 2303,
            LocationType.VANILLA,
            logic.zerg_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_Z.mission_name,
            "South Far Prisoners",
            SC2_RACESWAP_LOC_ID_OFFSET + 2304,
            LocationType.VANILLA,
            logic.zerg_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_Z.mission_name,
            "North Prisoners",
            SC2_RACESWAP_LOC_ID_OFFSET + 2305,
            LocationType.VANILLA,
            logic.zerg_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_Z.mission_name,
            "Mothership",
            SC2_RACESWAP_LOC_ID_OFFSET + 2306,
            LocationType.EXTRA,
            logic.zerg_maw_requirement,
            hard_rule=logic.zerg_any_anti_air,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_Z.mission_name,
            "Expansion Rip Field Generator",
            SC2_RACESWAP_LOC_ID_OFFSET + 2307,
            LocationType.EXTRA,
            logic.zerg_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_Z.mission_name,
            "Middle Rip Field Generator",
            SC2_RACESWAP_LOC_ID_OFFSET + 2308,
            LocationType.EXTRA,
            logic.zerg_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_Z.mission_name,
            "Southeast Rip Field Generator",
            SC2_RACESWAP_LOC_ID_OFFSET + 2309,
            LocationType.EXTRA,
            logic.zerg_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_Z.mission_name,
            "Stargate Rip Field Generator",
            SC2_RACESWAP_LOC_ID_OFFSET + 2310,
            LocationType.EXTRA,
            logic.zerg_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_Z.mission_name,
            "Northwest Rip Field Generator",
            SC2_RACESWAP_LOC_ID_OFFSET + 2311,
            LocationType.CHALLENGE,
            logic.zerg_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_Z.mission_name,
            "West Rip Field Generator",
            SC2_RACESWAP_LOC_ID_OFFSET + 2312,
            LocationType.CHALLENGE,
            logic.zerg_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_Z.mission_name,
            "Southwest Rip Field Generator",
            SC2_RACESWAP_LOC_ID_OFFSET + 2313,
            LocationType.CHALLENGE,
            logic.zerg_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 2400,
            LocationType.VICTORY,
            logic.protoss_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_P.mission_name,
            "Landing Zone Cleared",
            SC2_RACESWAP_LOC_ID_OFFSET + 2401,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_P.mission_name,
            "Expansion Prisoners",
            SC2_RACESWAP_LOC_ID_OFFSET + 2402,
            LocationType.VANILLA,
            lambda state: adv_tactics or logic.protoss_maw_requirement(state),
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_P.mission_name,
            "South Close Prisoners",
            SC2_RACESWAP_LOC_ID_OFFSET + 2403,
            LocationType.VANILLA,
            lambda state: adv_tactics or logic.protoss_maw_requirement(state),
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_P.mission_name,
            "South Far Prisoners",
            SC2_RACESWAP_LOC_ID_OFFSET + 2404,
            LocationType.VANILLA,
            logic.protoss_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_P.mission_name,
            "North Prisoners",
            SC2_RACESWAP_LOC_ID_OFFSET + 2405,
            LocationType.VANILLA,
            logic.protoss_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_P.mission_name,
            "Mothership",
            SC2_RACESWAP_LOC_ID_OFFSET + 2406,
            LocationType.EXTRA,
            logic.protoss_maw_requirement,
            hard_rule=logic.protoss_any_anti_air_unit_or_soa_any_protoss,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_P.mission_name,
            "Expansion Rip Field Generator",
            SC2_RACESWAP_LOC_ID_OFFSET + 2407,
            LocationType.EXTRA,
            lambda state: adv_tactics or logic.protoss_maw_requirement(state),
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_P.mission_name,
            "Middle Rip Field Generator",
            SC2_RACESWAP_LOC_ID_OFFSET + 2408,
            LocationType.EXTRA,
            logic.protoss_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_P.mission_name,
            "Southeast Rip Field Generator",
            SC2_RACESWAP_LOC_ID_OFFSET + 2409,
            LocationType.EXTRA,
            logic.protoss_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_P.mission_name,
            "Stargate Rip Field Generator",
            SC2_RACESWAP_LOC_ID_OFFSET + 2410,
            LocationType.EXTRA,
            logic.protoss_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_P.mission_name,
            "Northwest Rip Field Generator",
            SC2_RACESWAP_LOC_ID_OFFSET + 2411,
            LocationType.CHALLENGE,
            logic.protoss_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_P.mission_name,
            "West Rip Field Generator",
            SC2_RACESWAP_LOC_ID_OFFSET + 2412,
            LocationType.CHALLENGE,
            logic.protoss_maw_requirement,
        ),
        make_location_data(
            SC2Mission.MAW_OF_THE_VOID_P.mission_name,
            "Southwest Rip Field Generator",
            SC2_RACESWAP_LOC_ID_OFFSET + 2413,
            LocationType.CHALLENGE,
            logic.protoss_maw_requirement,
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 2500,
            LocationType.VICTORY,
            lambda state: (
                logic.zerg_moderate_anti_air(state)
                and logic.zerg_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND_Z.mission_name,
            "Tosh's Miners",
            SC2_RACESWAP_LOC_ID_OFFSET + 2501,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND_Z.mission_name,
            "Brutalisk",
            SC2_RACESWAP_LOC_ID_OFFSET + 2502,
            LocationType.VANILLA,
            lambda state: logic.zerg_common_unit(state),
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND_Z.mission_name,
            "North Reinforcements",
            SC2_RACESWAP_LOC_ID_OFFSET + 2503,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND_Z.mission_name,
            "Middle Reinforcements",
            SC2_RACESWAP_LOC_ID_OFFSET + 2504,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND_Z.mission_name,
            "Southwest Reinforcements",
            SC2_RACESWAP_LOC_ID_OFFSET + 2505,
            LocationType.EXTRA,
            lambda state: logic.zerg_common_unit(state),
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND_Z.mission_name,
            "Southeast Reinforcements",
            SC2_RACESWAP_LOC_ID_OFFSET + 2506,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_moderate_anti_air(state)
                and logic.zerg_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND_Z.mission_name,
            "East Reinforcements",
            SC2_RACESWAP_LOC_ID_OFFSET + 2507,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_moderate_anti_air(state)
                and logic.zerg_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND_Z.mission_name,
            "Zerg Cleared",
            SC2_RACESWAP_LOC_ID_OFFSET + 2508,
            LocationType.CHALLENGE,
            lambda state: (
                logic.zerg_competent_anti_air(state)
                and logic.zerg_common_unit(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 2600,
            LocationType.VICTORY,
            lambda state: (
                adv_tactics
                or logic.protoss_basic_anti_air(state)
                and logic.protoss_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND_P.mission_name,
            "Tosh's Miners",
            SC2_RACESWAP_LOC_ID_OFFSET + 2601,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND_P.mission_name,
            "Brutalisk",
            SC2_RACESWAP_LOC_ID_OFFSET + 2602,
            LocationType.VANILLA,
            lambda state: adv_tactics or logic.protoss_common_unit(state),
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND_P.mission_name,
            "North Reinforcements",
            SC2_RACESWAP_LOC_ID_OFFSET + 2603,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND_P.mission_name,
            "Middle Reinforcements",
            SC2_RACESWAP_LOC_ID_OFFSET + 2604,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND_P.mission_name,
            "Southwest Reinforcements",
            SC2_RACESWAP_LOC_ID_OFFSET + 2605,
            LocationType.EXTRA,
            lambda state: adv_tactics or logic.protoss_common_unit(state),
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND_P.mission_name,
            "Southeast Reinforcements",
            SC2_RACESWAP_LOC_ID_OFFSET + 2606,
            LocationType.EXTRA,
            lambda state: (
                adv_tactics
                or logic.protoss_basic_anti_air(state)
                and logic.protoss_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND_P.mission_name,
            "East Reinforcements",
            SC2_RACESWAP_LOC_ID_OFFSET + 2607,
            LocationType.EXTRA,
            lambda state: (
                adv_tactics
                or logic.protoss_basic_anti_air(state)
                and logic.protoss_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.DEVILS_PLAYGROUND_P.mission_name,
            "Zerg Cleared",
            SC2_RACESWAP_LOC_ID_OFFSET + 2608,
            LocationType.CHALLENGE,
            lambda state: (
                logic.protoss_competent_anti_air(state)
                and (logic.protoss_common_unit(state))
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 2700,
            LocationType.VICTORY,
            logic.zerg_welcome_to_the_jungle_requirement,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_Z.mission_name,
            "Close Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 2701,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_Z.mission_name,
            "West Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 2702,
            LocationType.VANILLA,
            logic.zerg_welcome_to_the_jungle_requirement,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_Z.mission_name,
            "North-East Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 2703,
            LocationType.VANILLA,
            logic.zerg_welcome_to_the_jungle_requirement,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_Z.mission_name,
            "Middle Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 2704,
            LocationType.EXTRA,
            logic.zerg_welcome_to_the_jungle_requirement,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_Z.mission_name,
            "Protoss Cleared",
            SC2_RACESWAP_LOC_ID_OFFSET + 2705,
            LocationType.MASTERY,
            lambda state: (
                logic.zerg_welcome_to_the_jungle_requirement(state)
                and logic.zerg_competent_anti_air(state)
                and logic.zerg_base_buster(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_Z.mission_name,
            "No Terrazine Nodes Sealed",
            SC2_RACESWAP_LOC_ID_OFFSET + 2706,
            LocationType.CHALLENGE,
            lambda state: (
                logic.zerg_welcome_to_the_jungle_requirement(state)
                and logic.zerg_competent_anti_air(state)
                and logic.zerg_big_monsters(state)
            ),
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_Z.mission_name,
            "Up to 1 Terrazine Node Sealed",
            SC2_RACESWAP_LOC_ID_OFFSET + 2707,
            LocationType.CHALLENGE,
            lambda state: (
                logic.zerg_welcome_to_the_jungle_requirement(state)
                and logic.zerg_competent_anti_air(state)
            ),
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_Z.mission_name,
            "Up to 2 Terrazine Nodes Sealed",
            SC2_RACESWAP_LOC_ID_OFFSET + 2708,
            LocationType.CHALLENGE,
            lambda state: (
                logic.zerg_welcome_to_the_jungle_requirement(state)
                and logic.zerg_competent_anti_air(state)
            ),
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_Z.mission_name,
            "Up to 3 Terrazine Nodes Sealed",
            SC2_RACESWAP_LOC_ID_OFFSET + 2709,
            LocationType.CHALLENGE,
            lambda state: (
                logic.zerg_welcome_to_the_jungle_requirement(state)
                and logic.zerg_competent_anti_air(state)
            ),
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_Z.mission_name,
            "Up to 4 Terrazine Nodes Sealed",
            SC2_RACESWAP_LOC_ID_OFFSET + 2710,
            LocationType.EXTRA,
            logic.zerg_welcome_to_the_jungle_requirement,
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_Z.mission_name,
            "Up to 5 Terrazine Nodes Sealed",
            SC2_RACESWAP_LOC_ID_OFFSET + 2711,
            LocationType.EXTRA,
            logic.zerg_welcome_to_the_jungle_requirement,
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 2800,
            LocationType.VICTORY,
            logic.protoss_welcome_to_the_jungle_requirement,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_P.mission_name,
            "Close Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 2801,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_P.mission_name,
            "West Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 2802,
            LocationType.VANILLA,
            logic.protoss_welcome_to_the_jungle_requirement,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_P.mission_name,
            "North-East Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 2803,
            LocationType.VANILLA,
            logic.protoss_welcome_to_the_jungle_requirement,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_P.mission_name,
            "Middle Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 2804,
            LocationType.EXTRA,
            logic.protoss_welcome_to_the_jungle_requirement,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_P.mission_name,
            "Protoss Cleared",
            SC2_RACESWAP_LOC_ID_OFFSET + 2805,
            LocationType.MASTERY,
            lambda state: (
                logic.protoss_welcome_to_the_jungle_requirement(state)
                and logic.protoss_competent_comp(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_P.mission_name,
            "No Terrazine Nodes Sealed",
            SC2_RACESWAP_LOC_ID_OFFSET + 2806,
            LocationType.CHALLENGE,
            lambda state: (
                logic.protoss_welcome_to_the_jungle_requirement(state)
                and logic.protoss_competent_comp(state)
            ),
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_P.mission_name,
            "Up to 1 Terrazine Node Sealed",
            SC2_RACESWAP_LOC_ID_OFFSET + 2807,
            LocationType.CHALLENGE,
            lambda state: (
                logic.protoss_welcome_to_the_jungle_requirement(state)
                and logic.protoss_competent_comp(state)
            ),
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_P.mission_name,
            "Up to 2 Terrazine Nodes Sealed",
            SC2_RACESWAP_LOC_ID_OFFSET + 2808,
            LocationType.CHALLENGE,
            lambda state: (
                logic.protoss_welcome_to_the_jungle_requirement(state)
                and logic.protoss_basic_splash(state)
            ),
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_P.mission_name,
            "Up to 3 Terrazine Nodes Sealed",
            SC2_RACESWAP_LOC_ID_OFFSET + 2809,
            LocationType.CHALLENGE,
            lambda state: (
                logic.protoss_welcome_to_the_jungle_requirement(state)
                and logic.protoss_basic_splash(state)
            ),
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_P.mission_name,
            "Up to 4 Terrazine Nodes Sealed",
            SC2_RACESWAP_LOC_ID_OFFSET + 2810,
            LocationType.EXTRA,
            logic.protoss_welcome_to_the_jungle_requirement,
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.WELCOME_TO_THE_JUNGLE_P.mission_name,
            "Up to 5 Terrazine Nodes Sealed",
            SC2_RACESWAP_LOC_ID_OFFSET + 2811,
            LocationType.EXTRA,
            logic.protoss_welcome_to_the_jungle_requirement,
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 3300,
            LocationType.VICTORY,
            lambda state: (
                logic.zerg_great_train_robbery_train_stopper(state)
                and logic.zerg_basic_kerriganless_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_Z.mission_name,
            "North Defiler",
            SC2_RACESWAP_LOC_ID_OFFSET + 3301,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_Z.mission_name,
            "Mid Defiler",
            SC2_RACESWAP_LOC_ID_OFFSET + 3302,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_Z.mission_name,
            "South Defiler",
            SC2_RACESWAP_LOC_ID_OFFSET + 3303,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_Z.mission_name,
            "Close Infested Diamondback",
            SC2_RACESWAP_LOC_ID_OFFSET + 3304,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_Z.mission_name,
            "Northwest Infested Diamondback",
            SC2_RACESWAP_LOC_ID_OFFSET + 3305,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_Z.mission_name,
            "North Infested Diamondback",
            SC2_RACESWAP_LOC_ID_OFFSET + 3306,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_Z.mission_name,
            "Northeast Infested Diamondback",
            SC2_RACESWAP_LOC_ID_OFFSET + 3307,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_Z.mission_name,
            "Southwest Infested Diamondback",
            SC2_RACESWAP_LOC_ID_OFFSET + 3308,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_Z.mission_name,
            "Southeast Infested Diamondback",
            SC2_RACESWAP_LOC_ID_OFFSET + 3309,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_Z.mission_name,
            "Kill Team",
            SC2_RACESWAP_LOC_ID_OFFSET + 3310,
            LocationType.CHALLENGE,
            lambda state: (
                (adv_tactics or logic.zerg_common_unit(state))
                and logic.zerg_great_train_robbery_train_stopper(state)
                and logic.zerg_basic_kerriganless_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_Z.mission_name,
            "Flawless",
            SC2_RACESWAP_LOC_ID_OFFSET + 3311,
            LocationType.CHALLENGE,
            lambda state: (
                logic.zerg_great_train_robbery_train_stopper(state)
                and logic.zerg_basic_kerriganless_anti_air(state)
            ),
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_Z.mission_name,
            "2 Trains Destroyed",
            SC2_RACESWAP_LOC_ID_OFFSET + 3312,
            LocationType.EXTRA,
            logic.zerg_great_train_robbery_train_stopper,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_Z.mission_name,
            "4 Trains Destroyed",
            SC2_RACESWAP_LOC_ID_OFFSET + 3313,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_great_train_robbery_train_stopper(state)
                and logic.zerg_basic_kerriganless_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_Z.mission_name,
            "6 Trains Destroyed",
            SC2_RACESWAP_LOC_ID_OFFSET + 3314,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_great_train_robbery_train_stopper(state)
                and logic.zerg_basic_kerriganless_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 3400,
            LocationType.VICTORY,
            lambda state: (
                logic.protoss_great_train_robbery_train_stopper(state)
                and logic.protoss_basic_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_P.mission_name,
            "North Defiler",
            SC2_RACESWAP_LOC_ID_OFFSET + 3401,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_P.mission_name,
            "Mid Defiler",
            SC2_RACESWAP_LOC_ID_OFFSET + 3402,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_P.mission_name,
            "South Defiler",
            SC2_RACESWAP_LOC_ID_OFFSET + 3403,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_P.mission_name,
            "Close Immortal",
            SC2_RACESWAP_LOC_ID_OFFSET + 3404,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_P.mission_name,
            "Northwest Immortal",
            SC2_RACESWAP_LOC_ID_OFFSET + 3405,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_P.mission_name,
            "North Instigator",
            SC2_RACESWAP_LOC_ID_OFFSET + 3406,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_P.mission_name,
            "Northeast Instigator",
            SC2_RACESWAP_LOC_ID_OFFSET + 3407,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_P.mission_name,
            "Southwest Instigator",
            SC2_RACESWAP_LOC_ID_OFFSET + 3408,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_P.mission_name,
            "Southeast Immortal",
            SC2_RACESWAP_LOC_ID_OFFSET + 3409,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_P.mission_name,
            "Kill Team",
            SC2_RACESWAP_LOC_ID_OFFSET + 3410,
            LocationType.CHALLENGE,
            lambda state: (
                (adv_tactics or logic.protoss_common_unit(state))
                and logic.protoss_great_train_robbery_train_stopper(state)
                and logic.protoss_basic_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_P.mission_name,
            "Flawless",
            SC2_RACESWAP_LOC_ID_OFFSET + 3411,
            LocationType.CHALLENGE,
            lambda state: (
                logic.protoss_great_train_robbery_train_stopper(state)
                and logic.protoss_basic_anti_air(state)
            ),
            flags=LocationFlag.PREVENTATIVE,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_P.mission_name,
            "2 Trains Destroyed",
            SC2_RACESWAP_LOC_ID_OFFSET + 3412,
            LocationType.EXTRA,
            logic.protoss_great_train_robbery_train_stopper,
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_P.mission_name,
            "4 Trains Destroyed",
            SC2_RACESWAP_LOC_ID_OFFSET + 3413,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_great_train_robbery_train_stopper(state)
                and logic.protoss_basic_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_GREAT_TRAIN_ROBBERY_P.mission_name,
            "6 Trains Destroyed",
            SC2_RACESWAP_LOC_ID_OFFSET + 3414,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_great_train_robbery_train_stopper(state)
                and logic.protoss_basic_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.CUTTHROAT_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 3500,
            LocationType.VICTORY,
            lambda state: (
                logic.zerg_common_unit(state)
                and (adv_tactics or logic.zerg_moderate_anti_air(state))
            ),
        ),
        make_location_data(
            SC2Mission.CUTTHROAT_Z.mission_name,
            "Mira Han",
            SC2_RACESWAP_LOC_ID_OFFSET + 3501,
            LocationType.EXTRA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.CUTTHROAT_Z.mission_name,
            "North Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 3502,
            LocationType.VANILLA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.CUTTHROAT_Z.mission_name,
            "Mid Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 3503,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.CUTTHROAT_Z.mission_name,
            "Southwest Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 3504,
            LocationType.VANILLA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.CUTTHROAT_Z.mission_name,
            "North Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 3505,
            LocationType.EXTRA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.CUTTHROAT_Z.mission_name,
            "South Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 3506,
            LocationType.EXTRA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.CUTTHROAT_Z.mission_name,
            "West Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 3507,
            LocationType.EXTRA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.CUTTHROAT_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 3600,
            LocationType.VICTORY,
            lambda state: (
                logic.protoss_common_unit(state)
                and (adv_tactics or logic.protoss_basic_anti_air(state))
            ),
        ),
        make_location_data(
            SC2Mission.CUTTHROAT_P.mission_name,
            "Mira Han",
            SC2_RACESWAP_LOC_ID_OFFSET + 3601,
            LocationType.EXTRA,
            logic.protoss_common_unit,
        ),
        make_location_data(
            SC2Mission.CUTTHROAT_P.mission_name,
            "North Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 3602,
            LocationType.VANILLA,
            logic.protoss_common_unit,
        ),
        make_location_data(
            SC2Mission.CUTTHROAT_P.mission_name,
            "Mid Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 3603,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.CUTTHROAT_P.mission_name,
            "Southwest Relic",
            SC2_RACESWAP_LOC_ID_OFFSET + 3604,
            LocationType.VANILLA,
            logic.protoss_common_unit,
        ),
        make_location_data(
            SC2Mission.CUTTHROAT_P.mission_name,
            "North Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 3605,
            LocationType.EXTRA,
            logic.protoss_common_unit,
        ),
        make_location_data(
            SC2Mission.CUTTHROAT_P.mission_name,
            "South Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 3606,
            LocationType.EXTRA,
            logic.protoss_common_unit,
        ),
        make_location_data(
            SC2Mission.CUTTHROAT_P.mission_name,
            "West Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 3607,
            LocationType.EXTRA,
            logic.protoss_common_unit,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 3700,
            LocationType.VICTORY,
            logic.zerg_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION_Z.mission_name,
            "Odin",
            SC2_RACESWAP_LOC_ID_OFFSET + 3701,
            LocationType.EXTRA,
            logic.zergling_hydra_roach_start,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION_Z.mission_name,
            "Loki",
            SC2_RACESWAP_LOC_ID_OFFSET + 3702,
            LocationType.CHALLENGE,
            logic.zerg_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION_Z.mission_name,
            "Lab Devourer",
            SC2_RACESWAP_LOC_ID_OFFSET + 3703,
            LocationType.VANILLA,
            logic.zergling_hydra_roach_start,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION_Z.mission_name,
            "North Devourer",
            SC2_RACESWAP_LOC_ID_OFFSET + 3704,
            LocationType.VANILLA,
            logic.zerg_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION_Z.mission_name,
            "Southeast Devourer",
            SC2_RACESWAP_LOC_ID_OFFSET + 3705,
            LocationType.VANILLA,
            logic.zerg_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION_Z.mission_name,
            "West Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 3706,
            LocationType.EXTRA,
            logic.zerg_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION_Z.mission_name,
            "Northwest Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 3707,
            LocationType.EXTRA,
            logic.zerg_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION_Z.mission_name,
            "Northeast Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 3708,
            LocationType.EXTRA,
            logic.zerg_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION_Z.mission_name,
            "Southeast Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 3709,
            LocationType.EXTRA,
            logic.zerg_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 3800,
            LocationType.VICTORY,
            logic.protoss_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION_P.mission_name,
            "Odin",
            SC2_RACESWAP_LOC_ID_OFFSET + 3801,
            LocationType.EXTRA,
            logic.zealot_sentry_slayer_start,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION_P.mission_name,
            "Loki",
            SC2_RACESWAP_LOC_ID_OFFSET + 3802,
            LocationType.CHALLENGE,
            logic.protoss_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION_P.mission_name,
            "Lab Devourer",
            SC2_RACESWAP_LOC_ID_OFFSET + 3803,
            LocationType.VANILLA,
            logic.zealot_sentry_slayer_start,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION_P.mission_name,
            "North Devourer",
            SC2_RACESWAP_LOC_ID_OFFSET + 3804,
            LocationType.VANILLA,
            logic.protoss_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION_P.mission_name,
            "Southeast Devourer",
            SC2_RACESWAP_LOC_ID_OFFSET + 3805,
            LocationType.VANILLA,
            logic.protoss_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION_P.mission_name,
            "West Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 3806,
            LocationType.EXTRA,
            logic.protoss_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION_P.mission_name,
            "Northwest Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 3807,
            LocationType.EXTRA,
            logic.protoss_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION_P.mission_name,
            "Northeast Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 3808,
            LocationType.EXTRA,
            logic.protoss_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.ENGINE_OF_DESTRUCTION_P.mission_name,
            "Southeast Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 3809,
            LocationType.EXTRA,
            logic.protoss_engine_of_destruction_requirement,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 3900,
            LocationType.VICTORY,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ_Z.mission_name,
            "Tower 1",
            SC2_RACESWAP_LOC_ID_OFFSET + 3901,
            LocationType.VANILLA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ_Z.mission_name,
            "Tower 2",
            SC2_RACESWAP_LOC_ID_OFFSET + 3902,
            LocationType.VANILLA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ_Z.mission_name,
            "Tower 3",
            SC2_RACESWAP_LOC_ID_OFFSET + 3903,
            LocationType.VANILLA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ_Z.mission_name,
            "Science Facility",
            SC2_RACESWAP_LOC_ID_OFFSET + 3904,
            LocationType.VANILLA,
            lambda state: (
                logic.advanced_tactics or logic.zerg_competent_comp_competent_aa(state)
            ),
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ_Z.mission_name,
            "All Barracks",
            SC2_RACESWAP_LOC_ID_OFFSET + 3905,
            LocationType.EXTRA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ_Z.mission_name,
            "All Factories",
            SC2_RACESWAP_LOC_ID_OFFSET + 3906,
            LocationType.EXTRA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ_Z.mission_name,
            "All Starports",
            SC2_RACESWAP_LOC_ID_OFFSET + 3907,
            LocationType.EXTRA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ_Z.mission_name,
            "Odin Not Trashed",
            SC2_RACESWAP_LOC_ID_OFFSET + 3908,
            LocationType.CHALLENGE,
            lambda state: (
                logic.zerg_competent_comp_competent_aa(state)
                and logic.zerg_repair_odin(state)
            ),
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ_Z.mission_name,
            "Surprise Attack Ends",
            SC2_RACESWAP_LOC_ID_OFFSET + 3909,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 4000,
            LocationType.VICTORY,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ_P.mission_name,
            "Tower 1",
            SC2_RACESWAP_LOC_ID_OFFSET + 4001,
            LocationType.VANILLA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ_P.mission_name,
            "Tower 2",
            SC2_RACESWAP_LOC_ID_OFFSET + 4002,
            LocationType.VANILLA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ_P.mission_name,
            "Tower 3",
            SC2_RACESWAP_LOC_ID_OFFSET + 4003,
            LocationType.VANILLA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ_P.mission_name,
            "Science Facility",
            SC2_RACESWAP_LOC_ID_OFFSET + 4004,
            LocationType.VANILLA,
            lambda state: adv_tactics or logic.protoss_competent_comp(state),
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ_P.mission_name,
            "All Barracks",
            SC2_RACESWAP_LOC_ID_OFFSET + 4005,
            LocationType.EXTRA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ_P.mission_name,
            "All Factories",
            SC2_RACESWAP_LOC_ID_OFFSET + 4006,
            LocationType.EXTRA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ_P.mission_name,
            "All Starports",
            SC2_RACESWAP_LOC_ID_OFFSET + 4007,
            LocationType.EXTRA,
            lambda state: adv_tactics or logic.protoss_competent_comp(state),
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ_P.mission_name,
            "Odin Not Trashed",
            SC2_RACESWAP_LOC_ID_OFFSET + 4008,
            LocationType.CHALLENGE,
            lambda state: (
                logic.protoss_competent_comp(state) and logic.protoss_repair_odin(state)
            ),
        ),
        make_location_data(
            SC2Mission.MEDIA_BLITZ_P.mission_name,
            "Surprise Attack Ends",
            SC2_RACESWAP_LOC_ID_OFFSET + 4009,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 4500,
            LocationType.VICTORY,
            lambda state: (
                logic.terran_competent_comp(state)
                and logic.terran_common_unit(state)
                and logic.terran_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN_T.mission_name,
            "Factory",
            SC2_RACESWAP_LOC_ID_OFFSET + 4501,
            LocationType.VANILLA,
            lambda state: adv_tactics or logic.terran_common_unit(state),
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN_T.mission_name,
            "Armory",
            SC2_RACESWAP_LOC_ID_OFFSET + 4502,
            LocationType.VANILLA,
            lambda state: adv_tactics or logic.terran_common_unit(state),
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN_T.mission_name,
            "Shadow Ops",
            SC2_RACESWAP_LOC_ID_OFFSET + 4503,
            LocationType.VANILLA,
            lambda state: logic.terran_common_unit(state)
            and logic.terran_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN_T.mission_name,
            "Northeast Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 4504,
            LocationType.EXTRA,
            lambda state: logic.terran_common_unit(state)
            and logic.terran_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN_T.mission_name,
            "Southwest Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 4505,
            LocationType.CHALLENGE,
            lambda state: (
                logic.terran_competent_comp(state)
                and logic.terran_common_unit(state)
                and logic.terran_competent_anti_air(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN_T.mission_name,
            "Maar",
            SC2_RACESWAP_LOC_ID_OFFSET + 4506,
            LocationType.EXTRA,
            logic.terran_common_unit,
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN_T.mission_name,
            "Northwest Preserver",
            SC2_RACESWAP_LOC_ID_OFFSET + 4507,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_competent_comp(state)
                and logic.terran_common_unit(state)
                and logic.terran_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN_T.mission_name,
            "Southwest Preserver",
            SC2_RACESWAP_LOC_ID_OFFSET + 4508,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_competent_comp(state)
                and logic.terran_common_unit(state)
                and logic.terran_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN_T.mission_name,
            "East Preserver",
            SC2_RACESWAP_LOC_ID_OFFSET + 4509,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_competent_comp(state)
                and logic.terran_common_unit(state)
                and logic.terran_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 4600,
            LocationType.VICTORY,
            lambda state: logic.zerg_competent_comp(state)
            and logic.zerg_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN_Z.mission_name,
            "Ultralisk Cavern",
            SC2_RACESWAP_LOC_ID_OFFSET + 4601,
            LocationType.VANILLA,
            lambda state: (adv_tactics or logic.zerg_common_unit(state))
            and logic.spread_creep(state),
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN_Z.mission_name,
            "Hydralisk Den",
            SC2_RACESWAP_LOC_ID_OFFSET + 4602,
            LocationType.VANILLA,
            lambda state: (adv_tactics or logic.zerg_common_unit(state))
            and logic.spread_creep(state),
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN_Z.mission_name,
            "Infestation Pit",
            SC2_RACESWAP_LOC_ID_OFFSET + 4603,
            LocationType.VANILLA,
            lambda state: logic.zerg_common_unit(state)
            and logic.zerg_competent_anti_air(state)
            and logic.spread_creep(state),
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN_Z.mission_name,
            "Northeast Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 4604,
            LocationType.EXTRA,
            lambda state: logic.zerg_common_unit(state)
            and logic.zerg_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN_Z.mission_name,
            "Southwest Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 4605,
            LocationType.CHALLENGE,
            lambda state: logic.zerg_common_unit(state)
            and logic.zerg_competent_anti_air(state),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN_Z.mission_name,
            "Maar",
            SC2_RACESWAP_LOC_ID_OFFSET + 4606,
            LocationType.EXTRA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN_Z.mission_name,
            "Northwest Preserver",
            SC2_RACESWAP_LOC_ID_OFFSET + 4607,
            LocationType.EXTRA,
            lambda state: logic.zerg_competent_comp(state)
            and logic.zerg_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN_Z.mission_name,
            "Southwest Preserver",
            SC2_RACESWAP_LOC_ID_OFFSET + 4608,
            LocationType.EXTRA,
            lambda state: logic.zerg_competent_comp(state)
            and logic.zerg_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.A_SINISTER_TURN_Z.mission_name,
            "East Preserver",
            SC2_RACESWAP_LOC_ID_OFFSET + 4609,
            LocationType.EXTRA,
            lambda state: logic.zerg_competent_comp(state)
            and logic.zerg_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 4700,
            LocationType.VICTORY,
            lambda state: logic.terran_common_unit(state)
            and logic.terran_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE_T.mission_name,
            "Close Obelisk",
            SC2_RACESWAP_LOC_ID_OFFSET + 4701,
            LocationType.VANILLA,
            lambda state: adv_tactics or logic.terran_common_unit(state),
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE_T.mission_name,
            "West Obelisk",
            SC2_RACESWAP_LOC_ID_OFFSET + 4702,
            LocationType.VANILLA,
            lambda state: adv_tactics
            or (logic.terran_common_unit(state) and logic.terran_basic_anti_air(state)),
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE_T.mission_name,
            "Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 4703,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE_T.mission_name,
            "Southwest Tendril",
            SC2_RACESWAP_LOC_ID_OFFSET + 4704,
            LocationType.EXTRA,
            logic.terran_common_unit,
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE_T.mission_name,
            "Southeast Tendril",
            SC2_RACESWAP_LOC_ID_OFFSET + 4705,
            LocationType.EXTRA,
            logic.terran_common_unit,
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE_T.mission_name,
            "Northeast Tendril",
            SC2_RACESWAP_LOC_ID_OFFSET + 4706,
            LocationType.EXTRA,
            lambda state: logic.terran_common_unit(state)
            and logic.terran_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE_T.mission_name,
            "Northwest Tendril",
            SC2_RACESWAP_LOC_ID_OFFSET + 4707,
            LocationType.EXTRA,
            lambda state: logic.terran_common_unit(state)
            and logic.terran_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 4800,
            LocationType.VICTORY,
            lambda state: logic.zerg_common_unit(state)
            and logic.zerg_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE_Z.mission_name,
            "Close Obelisk",
            SC2_RACESWAP_LOC_ID_OFFSET + 4801,
            LocationType.VANILLA,
            lambda state: adv_tactics or logic.zerg_common_unit(state),
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE_Z.mission_name,
            "West Obelisk",
            SC2_RACESWAP_LOC_ID_OFFSET + 4802,
            LocationType.VANILLA,
            lambda state: (
                adv_tactics
                or (
                    logic.zerg_common_unit(state)
                    and logic.zerg_basic_kerriganless_anti_air(state)
                    and logic.spread_creep(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE_Z.mission_name,
            "Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 4803,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE_Z.mission_name,
            "Southwest Tendril",
            SC2_RACESWAP_LOC_ID_OFFSET + 4804,
            LocationType.EXTRA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE_Z.mission_name,
            "Southeast Tendril",
            SC2_RACESWAP_LOC_ID_OFFSET + 4805,
            LocationType.EXTRA,
            logic.zerg_common_unit,
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE_Z.mission_name,
            "Northeast Tendril",
            SC2_RACESWAP_LOC_ID_OFFSET + 4806,
            LocationType.EXTRA,
            lambda state: logic.zerg_common_unit(state)
            and logic.zerg_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.ECHOES_OF_THE_FUTURE_Z.mission_name,
            "Northwest Tendril",
            SC2_RACESWAP_LOC_ID_OFFSET + 4807,
            LocationType.EXTRA,
            lambda state: logic.zerg_common_unit(state)
            and logic.zerg_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.IN_UTTER_DARKNESS_T.mission_name,
            "Defeat",
            SC2_RACESWAP_LOC_ID_OFFSET + 4900,
            LocationType.VICTORY,
        ),
        make_location_data(
            SC2Mission.IN_UTTER_DARKNESS_T.mission_name,
            "Protoss Archive",
            SC2_RACESWAP_LOC_ID_OFFSET + 4901,
            LocationType.VANILLA,
            logic.terran_in_utter_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.IN_UTTER_DARKNESS_T.mission_name,
            "Kills",
            SC2_RACESWAP_LOC_ID_OFFSET + 4902,
            LocationType.VANILLA,
            logic.terran_in_utter_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.IN_UTTER_DARKNESS_T.mission_name,
            "Urun",
            SC2_RACESWAP_LOC_ID_OFFSET + 4903,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.IN_UTTER_DARKNESS_T.mission_name,
            "Mohandar",
            SC2_RACESWAP_LOC_ID_OFFSET + 4904,
            LocationType.EXTRA,
            logic.terran_in_utter_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.IN_UTTER_DARKNESS_T.mission_name,
            "Selendis",
            SC2_RACESWAP_LOC_ID_OFFSET + 4905,
            LocationType.EXTRA,
            logic.terran_in_utter_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.IN_UTTER_DARKNESS_T.mission_name,
            "Artanis",
            SC2_RACESWAP_LOC_ID_OFFSET + 4906,
            LocationType.EXTRA,
            logic.terran_in_utter_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.IN_UTTER_DARKNESS_Z.mission_name,
            "Defeat",
            SC2_RACESWAP_LOC_ID_OFFSET + 5000,
            LocationType.VICTORY,
        ),
        make_location_data(
            SC2Mission.IN_UTTER_DARKNESS_Z.mission_name,
            "Protoss Archive",
            SC2_RACESWAP_LOC_ID_OFFSET + 5001,
            LocationType.VANILLA,
            logic.zerg_in_utter_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.IN_UTTER_DARKNESS_Z.mission_name,
            "Kills",
            SC2_RACESWAP_LOC_ID_OFFSET + 5002,
            LocationType.VANILLA,
            logic.zerg_in_utter_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.IN_UTTER_DARKNESS_Z.mission_name,
            "Urun",
            SC2_RACESWAP_LOC_ID_OFFSET + 5003,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.IN_UTTER_DARKNESS_Z.mission_name,
            "Mohandar",
            SC2_RACESWAP_LOC_ID_OFFSET + 5004,
            LocationType.EXTRA,
            logic.zerg_in_utter_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.IN_UTTER_DARKNESS_Z.mission_name,
            "Selendis",
            SC2_RACESWAP_LOC_ID_OFFSET + 5005,
            LocationType.EXTRA,
            logic.zerg_in_utter_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.IN_UTTER_DARKNESS_Z.mission_name,
            "Artanis",
            SC2_RACESWAP_LOC_ID_OFFSET + 5006,
            LocationType.EXTRA,
            logic.zerg_in_utter_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 5100,
            LocationType.VICTORY,
            logic.zerg_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_Z.mission_name,
            "Large Army",
            SC2_RACESWAP_LOC_ID_OFFSET + 5101,
            LocationType.VANILLA,
            logic.zerg_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_Z.mission_name,
            "2 Drop Pods",
            SC2_RACESWAP_LOC_ID_OFFSET + 5102,
            LocationType.VANILLA,
            logic.zerg_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_Z.mission_name,
            "4 Drop Pods",
            SC2_RACESWAP_LOC_ID_OFFSET + 5103,
            LocationType.VANILLA,
            logic.zerg_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_Z.mission_name,
            "6 Drop Pods",
            SC2_RACESWAP_LOC_ID_OFFSET + 5104,
            LocationType.EXTRA,
            logic.zerg_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_Z.mission_name,
            "8 Drop Pods",
            SC2_RACESWAP_LOC_ID_OFFSET + 5105,
            LocationType.CHALLENGE,
            logic.zerg_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_Z.mission_name,
            "Southwest Spore Cannon",
            SC2_RACESWAP_LOC_ID_OFFSET + 5106,
            LocationType.EXTRA,
            logic.zerg_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_Z.mission_name,
            "Northwest Spore Cannon",
            SC2_RACESWAP_LOC_ID_OFFSET + 5107,
            LocationType.EXTRA,
            logic.zerg_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_Z.mission_name,
            "Northeast Spore Cannon",
            SC2_RACESWAP_LOC_ID_OFFSET + 5108,
            LocationType.EXTRA,
            logic.zerg_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_Z.mission_name,
            "East Spore Cannon",
            SC2_RACESWAP_LOC_ID_OFFSET + 5109,
            LocationType.EXTRA,
            logic.zerg_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_Z.mission_name,
            "Southeast Spore Cannon",
            SC2_RACESWAP_LOC_ID_OFFSET + 5110,
            LocationType.EXTRA,
            logic.zerg_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_Z.mission_name,
            "Expansion Spore Cannon",
            SC2_RACESWAP_LOC_ID_OFFSET + 5111,
            LocationType.EXTRA,
            logic.zerg_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 5200,
            LocationType.VICTORY,
            logic.protoss_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_P.mission_name,
            "Large Army",
            SC2_RACESWAP_LOC_ID_OFFSET + 5201,
            LocationType.VANILLA,
            logic.protoss_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_P.mission_name,
            "2 Drop Pods",
            SC2_RACESWAP_LOC_ID_OFFSET + 5202,
            LocationType.VANILLA,
            logic.protoss_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_P.mission_name,
            "4 Drop Pods",
            SC2_RACESWAP_LOC_ID_OFFSET + 5203,
            LocationType.VANILLA,
            logic.protoss_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_P.mission_name,
            "6 Drop Pods",
            SC2_RACESWAP_LOC_ID_OFFSET + 5204,
            LocationType.EXTRA,
            logic.protoss_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_P.mission_name,
            "8 Drop Pods",
            SC2_RACESWAP_LOC_ID_OFFSET + 5205,
            LocationType.CHALLENGE,
            logic.protoss_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_P.mission_name,
            "Southwest Spore Cannon",
            SC2_RACESWAP_LOC_ID_OFFSET + 5206,
            LocationType.EXTRA,
            logic.protoss_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_P.mission_name,
            "Northwest Spore Cannon",
            SC2_RACESWAP_LOC_ID_OFFSET + 5207,
            LocationType.EXTRA,
            logic.protoss_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_P.mission_name,
            "Northeast Spore Cannon",
            SC2_RACESWAP_LOC_ID_OFFSET + 5208,
            LocationType.EXTRA,
            logic.protoss_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_P.mission_name,
            "East Spore Cannon",
            SC2_RACESWAP_LOC_ID_OFFSET + 5209,
            LocationType.EXTRA,
            logic.protoss_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_P.mission_name,
            "Southeast Spore Cannon",
            SC2_RACESWAP_LOC_ID_OFFSET + 5210,
            LocationType.EXTRA,
            logic.protoss_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.GATES_OF_HELL_P.mission_name,
            "Expansion Spore Cannon",
            SC2_RACESWAP_LOC_ID_OFFSET + 5211,
            LocationType.EXTRA,
            logic.protoss_gates_of_hell_requirement,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 5500,
            LocationType.VICTORY,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY_Z.mission_name,
            "Close Coolant Tower",
            SC2_RACESWAP_LOC_ID_OFFSET + 5501,
            LocationType.VANILLA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY_Z.mission_name,
            "Northwest Coolant Tower",
            SC2_RACESWAP_LOC_ID_OFFSET + 5502,
            LocationType.VANILLA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY_Z.mission_name,
            "Southeast Coolant Tower",
            SC2_RACESWAP_LOC_ID_OFFSET + 5503,
            LocationType.VANILLA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY_Z.mission_name,
            "Southwest Coolant Tower",
            SC2_RACESWAP_LOC_ID_OFFSET + 5504,
            LocationType.VANILLA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY_Z.mission_name,
            "Leviathan",
            SC2_RACESWAP_LOC_ID_OFFSET + 5505,
            LocationType.VANILLA,
            logic.zerg_competent_comp_competent_aa,
            hard_rule=logic.zerg_any_anti_air,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY_Z.mission_name,
            "East Hatchery",
            SC2_RACESWAP_LOC_ID_OFFSET + 5506,
            LocationType.EXTRA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY_Z.mission_name,
            "North Hatchery",
            SC2_RACESWAP_LOC_ID_OFFSET + 5507,
            LocationType.EXTRA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY_Z.mission_name,
            "Mid Hatchery",
            SC2_RACESWAP_LOC_ID_OFFSET + 5508,
            LocationType.EXTRA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 5600,
            LocationType.VICTORY,
            lambda state: logic.protoss_competent_comp(state)
            and logic.protoss_army_weapon_armor_upgrade_min_level(state) >= 2,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY_P.mission_name,
            "Close Coolant Tower",
            SC2_RACESWAP_LOC_ID_OFFSET + 5601,
            LocationType.VANILLA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY_P.mission_name,
            "Northwest Coolant Tower",
            SC2_RACESWAP_LOC_ID_OFFSET + 5602,
            LocationType.VANILLA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY_P.mission_name,
            "Southeast Coolant Tower",
            SC2_RACESWAP_LOC_ID_OFFSET + 5603,
            LocationType.VANILLA,
            lambda state: logic.protoss_competent_comp(state)
            and logic.protoss_army_weapon_armor_upgrade_min_level(state) >= 2,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY_P.mission_name,
            "Southwest Coolant Tower",
            SC2_RACESWAP_LOC_ID_OFFSET + 5604,
            LocationType.VANILLA,
            lambda state: logic.protoss_competent_comp(state)
            and logic.protoss_army_weapon_armor_upgrade_min_level(state) >= 2,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY_P.mission_name,
            "Leviathan",
            SC2_RACESWAP_LOC_ID_OFFSET + 5605,
            LocationType.VANILLA,
            lambda state: logic.protoss_competent_comp(state)
            and logic.protoss_army_weapon_armor_upgrade_min_level(state) >= 2,
            hard_rule=logic.protoss_any_anti_air_unit_or_soa_any_protoss,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY_P.mission_name,
            "East Hatchery",
            SC2_RACESWAP_LOC_ID_OFFSET + 5606,
            LocationType.EXTRA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY_P.mission_name,
            "North Hatchery",
            SC2_RACESWAP_LOC_ID_OFFSET + 5607,
            LocationType.EXTRA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.SHATTER_THE_SKY_P.mission_name,
            "Mid Hatchery",
            SC2_RACESWAP_LOC_ID_OFFSET + 5608,
            LocationType.EXTRA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.ALL_IN_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 5700,
            LocationType.VICTORY,
            logic.zerg_all_in_requirement,
        ),
        make_location_data(
            SC2Mission.ALL_IN_Z.mission_name,
            "First Kerrigan Attack",
            SC2_RACESWAP_LOC_ID_OFFSET + 5701,
            LocationType.EXTRA,
            logic.zerg_all_in_requirement,
        ),
        make_location_data(
            SC2Mission.ALL_IN_Z.mission_name,
            "Second Kerrigan Attack",
            SC2_RACESWAP_LOC_ID_OFFSET + 5702,
            LocationType.EXTRA,
            logic.zerg_all_in_requirement,
        ),
        make_location_data(
            SC2Mission.ALL_IN_Z.mission_name,
            "Third Kerrigan Attack",
            SC2_RACESWAP_LOC_ID_OFFSET + 5703,
            LocationType.EXTRA,
            logic.zerg_all_in_requirement,
        ),
        make_location_data(
            SC2Mission.ALL_IN_Z.mission_name,
            "Fourth Kerrigan Attack",
            SC2_RACESWAP_LOC_ID_OFFSET + 5704,
            LocationType.EXTRA,
            logic.zerg_all_in_requirement,
        ),
        make_location_data(
            SC2Mission.ALL_IN_Z.mission_name,
            "Fifth Kerrigan Attack",
            SC2_RACESWAP_LOC_ID_OFFSET + 5705,
            LocationType.EXTRA,
            logic.zerg_all_in_requirement,
        ),
        make_location_data(
            SC2Mission.ALL_IN_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 5800,
            LocationType.VICTORY,
            logic.protoss_all_in_requirement,
        ),
        make_location_data(
            SC2Mission.ALL_IN_P.mission_name,
            "First Kerrigan Attack",
            SC2_RACESWAP_LOC_ID_OFFSET + 5801,
            LocationType.EXTRA,
            logic.protoss_all_in_requirement,
        ),
        make_location_data(
            SC2Mission.ALL_IN_P.mission_name,
            "Second Kerrigan Attack",
            SC2_RACESWAP_LOC_ID_OFFSET + 5802,
            LocationType.EXTRA,
            logic.protoss_all_in_requirement,
        ),
        make_location_data(
            SC2Mission.ALL_IN_P.mission_name,
            "Third Kerrigan Attack",
            SC2_RACESWAP_LOC_ID_OFFSET + 5803,
            LocationType.EXTRA,
            logic.protoss_all_in_requirement,
        ),
        make_location_data(
            SC2Mission.ALL_IN_P.mission_name,
            "Fourth Kerrigan Attack",
            SC2_RACESWAP_LOC_ID_OFFSET + 5804,
            LocationType.EXTRA,
            logic.protoss_all_in_requirement,
        ),
        make_location_data(
            SC2Mission.ALL_IN_P.mission_name,
            "Fifth Kerrigan Attack",
            SC2_RACESWAP_LOC_ID_OFFSET + 5805,
            LocationType.EXTRA,
            logic.protoss_all_in_requirement,
        ),
        make_location_data(
            SC2Mission.LAB_RAT_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 5900,
            LocationType.VICTORY,
            logic.terran_common_unit,
        ),
        make_location_data(
            SC2Mission.LAB_RAT_T.mission_name,
            "Gather Minerals",
            SC2_RACESWAP_LOC_ID_OFFSET + 5901,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.LAB_RAT_T.mission_name,
            "South Marine Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 5902,
            LocationType.VANILLA,
            lambda state: adv_tactics or logic.terran_common_unit(state),
        ),
        make_location_data(
            SC2Mission.LAB_RAT_T.mission_name,
            "East Marine Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 5903,
            LocationType.VANILLA,
            lambda state: adv_tactics or logic.terran_common_unit(state),
        ),
        make_location_data(
            SC2Mission.LAB_RAT_T.mission_name,
            "West Marine Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 5904,
            LocationType.VANILLA,
            lambda state: adv_tactics or logic.terran_common_unit(state),
        ),
        make_location_data(
            SC2Mission.LAB_RAT_T.mission_name,
            "Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 5905,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.LAB_RAT_T.mission_name,
            "Supply Depot",
            SC2_RACESWAP_LOC_ID_OFFSET + 5906,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.LAB_RAT_T.mission_name,
            "Gas Turrets",
            SC2_RACESWAP_LOC_ID_OFFSET + 5907,
            LocationType.EXTRA,
            lambda state: adv_tactics or logic.terran_common_unit(state),
        ),
        make_location_data(
            SC2Mission.LAB_RAT_T.mission_name,
            "Win In Under 10 Minutes",
            SC2_RACESWAP_LOC_ID_OFFSET + 5908,
            LocationType.CHALLENGE,
            lambda state: logic.terran_common_unit(state)
            and logic.terran_early_tech(state),
            flags=LocationFlag.SPEEDRUN,
        ),
        make_location_data(
            SC2Mission.LAB_RAT_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 6000,
            LocationType.VICTORY,
            logic.protoss_common_unit,
        ),
        make_location_data(
            SC2Mission.LAB_RAT_P.mission_name,
            "Gather Minerals",
            SC2_RACESWAP_LOC_ID_OFFSET + 6001,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.LAB_RAT_P.mission_name,
            "South Zealot Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 6002,
            LocationType.VANILLA,
            lambda state: adv_tactics or logic.protoss_common_unit(state),
        ),
        make_location_data(
            SC2Mission.LAB_RAT_P.mission_name,
            "East Zealot Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 6003,
            LocationType.VANILLA,
            lambda state: adv_tactics or logic.protoss_common_unit(state),
        ),
        make_location_data(
            SC2Mission.LAB_RAT_P.mission_name,
            "West Zealot Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 6004,
            LocationType.VANILLA,
            lambda state: adv_tactics or logic.protoss_common_unit(state),
        ),
        make_location_data(
            SC2Mission.LAB_RAT_P.mission_name,
            "Nexus",
            SC2_RACESWAP_LOC_ID_OFFSET + 6005,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.LAB_RAT_P.mission_name,
            "Pylon",
            SC2_RACESWAP_LOC_ID_OFFSET + 6006,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.LAB_RAT_P.mission_name,
            "Gas Turrets",
            SC2_RACESWAP_LOC_ID_OFFSET + 6007,
            LocationType.EXTRA,
            lambda state: adv_tactics or logic.protoss_common_unit(state),
        ),
        make_location_data(
            SC2Mission.LAB_RAT_P.mission_name,
            "Win In Under 10 Minutes",
            SC2_RACESWAP_LOC_ID_OFFSET + 6008,
            LocationType.CHALLENGE,
            logic.protoss_common_unit,
            flags=LocationFlag.SPEEDRUN,
        ),
        make_location_data(
            SC2Mission.RENDEZVOUS_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 6300,
            LocationType.VICTORY,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_basic_anti_air(state)
                and logic.terran_defense_rating(state, False, False) >= 3
            ),
        ),
        make_location_data(
            SC2Mission.RENDEZVOUS_T.mission_name,
            "Right Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 6301,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_basic_anti_air(state)
                and logic.terran_defense_rating(state, False, False) >= 3
            ),
        ),
        make_location_data(
            SC2Mission.RENDEZVOUS_T.mission_name,
            "Center Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 6302,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_basic_anti_air(state)
                and logic.terran_defense_rating(state, False, False) >= 3
            ),
        ),
        make_location_data(
            SC2Mission.RENDEZVOUS_T.mission_name,
            "Left Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 6303,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_basic_anti_air(state)
                and logic.terran_defense_rating(state, False, False) >= 3
            ),
        ),
        make_location_data(
            SC2Mission.RENDEZVOUS_T.mission_name,
            "Hold Out Finished",
            SC2_RACESWAP_LOC_ID_OFFSET + 6304,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_basic_anti_air(state)
                and logic.terran_defense_rating(state, False, False) >= 3
            ),
        ),
        make_location_data(
            SC2Mission.RENDEZVOUS_T.mission_name,
            "Kill All Buildings Before Reinforcements",
            SC2_RACESWAP_LOC_ID_OFFSET + 6305,
            LocationType.MASTERY,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_competent_comp(state)
                and logic.terran_defense_rating(state, False, False) >= 3
                and logic.terran_power_rating(state) >= 5
            ),
            flags=LocationFlag.SPEEDRUN,
        ),
        make_location_data(
            SC2Mission.RENDEZVOUS_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 6400,
            LocationType.VICTORY,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_basic_anti_air(state)
                and logic.protoss_defense_rating(state, False) >= 3
            ),
        ),
        make_location_data(
            SC2Mission.RENDEZVOUS_P.mission_name,
            "Right Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 6401,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_basic_anti_air(state)
                and logic.protoss_defense_rating(state, False) >= 3
            ),
        ),
        make_location_data(
            SC2Mission.RENDEZVOUS_P.mission_name,
            "Center Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 6402,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_basic_anti_air(state)
                and logic.protoss_defense_rating(state, False) >= 3
            ),
        ),
        make_location_data(
            SC2Mission.RENDEZVOUS_P.mission_name,
            "Left Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 6403,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_basic_anti_air(state)
                and logic.protoss_defense_rating(state, False) >= 3
            ),
        ),
        make_location_data(
            SC2Mission.RENDEZVOUS_P.mission_name,
            "Hold Out Finished",
            SC2_RACESWAP_LOC_ID_OFFSET + 6404,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_basic_anti_air(state)
                and logic.protoss_defense_rating(state, False) >= 3
            ),
        ),
        make_location_data(
            SC2Mission.RENDEZVOUS_P.mission_name,
            "Kill All Buildings Before Reinforcements",
            SC2_RACESWAP_LOC_ID_OFFSET + 6405,
            LocationType.MASTERY,
            lambda state: (
                logic.protoss_competent_comp(state)
                and logic.protoss_defense_rating(state, False) >= 3
                and logic.protoss_power_rating(state) >= 5
            ),
            flags=LocationFlag.SPEEDRUN,
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 6500,
            LocationType.VICTORY,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS_T.mission_name,
            "First Ursadon Matriarch",
            SC2_RACESWAP_LOC_ID_OFFSET + 6501,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS_T.mission_name,
            "North Ursadon Matriarch",
            SC2_RACESWAP_LOC_ID_OFFSET + 6502,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_moderate_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS_T.mission_name,
            "West Ursadon Matriarch",
            SC2_RACESWAP_LOC_ID_OFFSET + 6503,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_moderate_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS_T.mission_name,
            "Lost Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 6504,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS_T.mission_name,
            "Northeast Psi-link Spire",
            SC2_RACESWAP_LOC_ID_OFFSET + 6505,
            LocationType.EXTRA,
            lambda state: logic.terran_common_unit(state) or adv_tactics,
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS_T.mission_name,
            "Northwest Psi-link Spire",
            SC2_RACESWAP_LOC_ID_OFFSET + 6506,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_moderate_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS_T.mission_name,
            "Southwest Psi-link Spire",
            SC2_RACESWAP_LOC_ID_OFFSET + 6507,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS_T.mission_name,
            "Nafash",
            SC2_RACESWAP_LOC_ID_OFFSET + 6508,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_moderate_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS_T.mission_name,
            "20 Unfrozen Structures",
            SC2_RACESWAP_LOC_ID_OFFSET + 6509,
            LocationType.CHALLENGE,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 6600,
            LocationType.VICTORY,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_anti_armor_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS_P.mission_name,
            "First Ursadon Matriarch",
            SC2_RACESWAP_LOC_ID_OFFSET + 6601,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS_P.mission_name,
            "North Ursadon Matriarch",
            SC2_RACESWAP_LOC_ID_OFFSET + 6602,
            LocationType.VANILLA,
            logic.protoss_common_unit_basic_aa,
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS_P.mission_name,
            "West Ursadon Matriarch",
            SC2_RACESWAP_LOC_ID_OFFSET + 6603,
            LocationType.VANILLA,
            logic.protoss_common_unit_basic_aa,
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS_P.mission_name,
            "Lost Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 6604,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS_P.mission_name,
            "Northeast Psi-link Spire",
            SC2_RACESWAP_LOC_ID_OFFSET + 6605,
            LocationType.EXTRA,
            lambda state: logic.protoss_common_unit(state) or adv_tactics,
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS_P.mission_name,
            "Northwest Psi-link Spire",
            SC2_RACESWAP_LOC_ID_OFFSET + 6606,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state) and logic.protoss_basic_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS_P.mission_name,
            "Southwest Psi-link Spire",
            SC2_RACESWAP_LOC_ID_OFFSET + 6607,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_anti_armor_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS_P.mission_name,
            "Nafash",
            SC2_RACESWAP_LOC_ID_OFFSET + 6608,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state) and logic.protoss_basic_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.HARVEST_OF_SCREAMS_P.mission_name,
            "20 Unfrozen Structures",
            SC2_RACESWAP_LOC_ID_OFFSET + 6609,
            LocationType.CHALLENGE,
            lambda state: (
                logic.protoss_common_unit(state) and logic.protoss_basic_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 6700,
            LocationType.VICTORY,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_competent_anti_air(state)
            ),
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_T.mission_name,
            "East Stasis Chamber",
            SC2_RACESWAP_LOC_ID_OFFSET + 6701,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_T.mission_name,
            "Center Stasis Chamber",
            SC2_RACESWAP_LOC_ID_OFFSET + 6702,
            LocationType.VANILLA,
            lambda state: logic.terran_common_unit(state) or adv_tactics,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_T.mission_name,
            "West Stasis Chamber",
            SC2_RACESWAP_LOC_ID_OFFSET + 6703,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_T.mission_name,
            "Destroy 4 Shuttles",
            SC2_RACESWAP_LOC_ID_OFFSET + 6704,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_competent_anti_air(state)
            ),
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_T.mission_name,
            "Frozen Expansion",
            SC2_RACESWAP_LOC_ID_OFFSET + 6705,
            LocationType.EXTRA,
            logic.terran_common_unit,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_T.mission_name,
            "Southwest Frozen Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 6706,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_T.mission_name,
            "Southeast Frozen Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 6707,
            LocationType.EXTRA,
            lambda state: logic.terran_common_unit(state) or adv_tactics,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_T.mission_name,
            "West Frozen Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 6708,
            LocationType.EXTRA,
            lambda state: logic.terran_common_unit(state)
            and logic.terran_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_T.mission_name,
            "East Frozen Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 6709,
            LocationType.EXTRA,
            lambda state: logic.terran_common_unit(state)
            and logic.terran_competent_anti_air(state),
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_T.mission_name,
            "West Launch Bay",
            SC2_RACESWAP_LOC_ID_OFFSET + 6710,
            LocationType.CHALLENGE,
            lambda state: logic.terran_beats_protoss_deathball(state)
                and logic.terran_common_unit(state),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_T.mission_name,
            "Center Launch Bay",
            SC2_RACESWAP_LOC_ID_OFFSET + 6711,
            LocationType.CHALLENGE,
            lambda state: logic.terran_beats_protoss_deathball(state)
                and logic.terran_competent_ground_to_air(state)
                and logic.terran_common_unit(state),
            hard_rule=logic.terran_any_anti_air,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_T.mission_name,
            "East Launch Bay",
            SC2_RACESWAP_LOC_ID_OFFSET + 6712,
            LocationType.CHALLENGE,
            lambda state: logic.terran_beats_protoss_deathball(state)
                and logic.terran_competent_ground_to_air(state)
                and logic.terran_common_unit(state),
            hard_rule=logic.terran_any_anti_air,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 6800,
            LocationType.VICTORY,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_anti_armor_anti_air(state)
            ),
            hard_rule=logic.protoss_any_anti_air_unit,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_P.mission_name,
            "East Stasis Chamber",
            SC2_RACESWAP_LOC_ID_OFFSET + 6801,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_anti_armor_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_P.mission_name,
            "Center Stasis Chamber",
            SC2_RACESWAP_LOC_ID_OFFSET + 6802,
            LocationType.VANILLA,
            lambda state: logic.protoss_common_unit(state) or adv_tactics,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_P.mission_name,
            "West Stasis Chamber",
            SC2_RACESWAP_LOC_ID_OFFSET + 6803,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_anti_armor_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_P.mission_name,
            "Destroy 4 Shuttles",
            SC2_RACESWAP_LOC_ID_OFFSET + 6804,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_anti_armor_anti_air(state)
            ),
            hard_rule=logic.protoss_any_anti_air_unit,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_P.mission_name,
            "Frozen Expansion",
            SC2_RACESWAP_LOC_ID_OFFSET + 6805,
            LocationType.EXTRA,
            logic.protoss_common_unit,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_P.mission_name,
            "Southwest Frozen Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 6806,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_P.mission_name,
            "Southeast Frozen Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 6807,
            LocationType.EXTRA,
            lambda state: logic.protoss_common_unit(state) or adv_tactics,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_P.mission_name,
            "West Frozen Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 6808,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_anti_armor_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_P.mission_name,
            "East Frozen Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 6809,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_anti_armor_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_P.mission_name,
            "West Launch Bay",
            SC2_RACESWAP_LOC_ID_OFFSET + 6810,
            LocationType.CHALLENGE,
            logic.protoss_competent_comp,
            hard_rule=logic.protoss_any_anti_air_unit,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_P.mission_name,
            "Center Launch Bay",
            SC2_RACESWAP_LOC_ID_OFFSET + 6811,
            LocationType.CHALLENGE,
            logic.protoss_competent_comp,
            hard_rule=logic.protoss_any_anti_air_unit,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.SHOOT_THE_MESSENGER_P.mission_name,
            "East Launch Bay",
            SC2_RACESWAP_LOC_ID_OFFSET + 6812,
            LocationType.CHALLENGE,
            logic.protoss_competent_comp,
            hard_rule=logic.protoss_any_anti_air_unit,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.DOMINATION_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 7100,
            LocationType.VICTORY,
            lambda state: logic.terran_common_unit(state)
            and (logic.terran_basic_anti_air(state) or adv_tactics),
        ),
        make_location_data(
            SC2Mission.DOMINATION_T.mission_name,
            "Center Infested Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 7101,
            LocationType.VANILLA,
            logic.terran_common_unit,
        ),
        make_location_data(
            SC2Mission.DOMINATION_T.mission_name,
            "North Infested Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 7102,
            LocationType.VANILLA,
            logic.terran_common_unit,
        ),
        make_location_data(
            SC2Mission.DOMINATION_T.mission_name,
            "Repel Zagara",
            SC2_RACESWAP_LOC_ID_OFFSET + 7103,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.DOMINATION_T.mission_name,
            "Close Bunker",
            SC2_RACESWAP_LOC_ID_OFFSET + 7104,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.DOMINATION_T.mission_name,
            "South Bunker",
            SC2_RACESWAP_LOC_ID_OFFSET + 7105,
            LocationType.EXTRA,
            lambda state: adv_tactics or logic.terran_common_unit(state),
        ),
        make_location_data(
            SC2Mission.DOMINATION_T.mission_name,
            "Southwest Bunker",
            SC2_RACESWAP_LOC_ID_OFFSET + 7106,
            LocationType.EXTRA,
            logic.terran_common_unit,
        ),
        make_location_data(
            SC2Mission.DOMINATION_T.mission_name,
            "Southeast Bunker",
            SC2_RACESWAP_LOC_ID_OFFSET + 7107,
            LocationType.EXTRA,
            lambda state: logic.terran_common_unit(state)
            and (logic.terran_basic_anti_air(state) or adv_tactics),
        ),
        make_location_data(
            SC2Mission.DOMINATION_T.mission_name,
            "North Bunker",
            SC2_RACESWAP_LOC_ID_OFFSET + 7108,
            LocationType.EXTRA,
            logic.terran_common_unit,
        ),
        make_location_data(
            SC2Mission.DOMINATION_T.mission_name,
            "Northeast Bunker",
            SC2_RACESWAP_LOC_ID_OFFSET + 7109,
            LocationType.EXTRA,
            lambda state: logic.terran_common_unit(state)
            and (logic.terran_basic_anti_air(state) or adv_tactics),
        ),
        make_location_data(
            SC2Mission.DOMINATION_T.mission_name,
            "Win Without 100 Eggs",
            SC2_RACESWAP_LOC_ID_OFFSET + 7110,
            LocationType.CHALLENGE,
            logic.terran_competent_comp,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.DOMINATION_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 7200,
            LocationType.VICTORY,
            lambda state: logic.protoss_common_unit(state)
            and (adv_tactics or logic.protoss_basic_anti_air(state)),
        ),
        make_location_data(
            SC2Mission.DOMINATION_P.mission_name,
            "Center Infested Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 7201,
            LocationType.VANILLA,
            logic.protoss_common_unit,
        ),
        make_location_data(
            SC2Mission.DOMINATION_P.mission_name,
            "North Infested Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 7202,
            LocationType.VANILLA,
            logic.protoss_common_unit,
        ),
        make_location_data(
            SC2Mission.DOMINATION_P.mission_name,
            "Repel Zagara",
            SC2_RACESWAP_LOC_ID_OFFSET + 7203,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.DOMINATION_P.mission_name,
            "Close Templar",
            SC2_RACESWAP_LOC_ID_OFFSET + 7204,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.DOMINATION_P.mission_name,
            "South Templar",
            SC2_RACESWAP_LOC_ID_OFFSET + 7205,
            LocationType.EXTRA,
            lambda state: adv_tactics or logic.protoss_common_unit(state),
        ),
        make_location_data(
            SC2Mission.DOMINATION_P.mission_name,
            "Southwest Templar",
            SC2_RACESWAP_LOC_ID_OFFSET + 7206,
            LocationType.EXTRA,
            logic.protoss_common_unit,
        ),
        make_location_data(
            SC2Mission.DOMINATION_P.mission_name,
            "Southeast Templar",
            SC2_RACESWAP_LOC_ID_OFFSET + 7207,
            LocationType.EXTRA,
            lambda state: logic.protoss_common_unit(state)
            and (adv_tactics or logic.protoss_basic_anti_air(state)),
        ),
        make_location_data(
            SC2Mission.DOMINATION_P.mission_name,
            "North Templar",
            SC2_RACESWAP_LOC_ID_OFFSET + 7208,
            LocationType.EXTRA,
            logic.protoss_common_unit,
        ),
        make_location_data(
            SC2Mission.DOMINATION_P.mission_name,
            "Northeast Templar",
            SC2_RACESWAP_LOC_ID_OFFSET + 7209,
            LocationType.EXTRA,
            lambda state: logic.protoss_common_unit(state)
            and (adv_tactics or logic.protoss_basic_anti_air(state)),
        ),
        make_location_data(
            SC2Mission.DOMINATION_P.mission_name,
            "Win Without 100 Eggs",
            SC2_RACESWAP_LOC_ID_OFFSET + 7210,
            LocationType.CHALLENGE,
            logic.protoss_competent_comp,
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 7300,
            LocationType.VICTORY,
            lambda state: (
                logic.terran_common_unit(state) and logic.terran_competent_comp(state)
            ),
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_T.mission_name,
            "West Biomass",
            SC2_RACESWAP_LOC_ID_OFFSET + 7301,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_T.mission_name,
            "North Biomass",
            SC2_RACESWAP_LOC_ID_OFFSET + 7302,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state) and logic.terran_competent_comp(state)
            ),
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_T.mission_name,
            "South Biomass",
            SC2_RACESWAP_LOC_ID_OFFSET + 7303,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state) and logic.terran_competent_comp(state)
            ),
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_T.mission_name,
            "Destroy 3 Gorgons",
            SC2_RACESWAP_LOC_ID_OFFSET + 7304,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state) and logic.terran_competent_comp(state)
            ),
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_T.mission_name,
            "Close Rescue",
            SC2_RACESWAP_LOC_ID_OFFSET + 7305,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_T.mission_name,
            "South Rescue",
            SC2_RACESWAP_LOC_ID_OFFSET + 7306,
            LocationType.EXTRA,
            logic.terran_common_unit,
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_T.mission_name,
            "North Rescue",
            SC2_RACESWAP_LOC_ID_OFFSET + 7307,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state) and logic.terran_competent_comp(state)
            ),
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_T.mission_name,
            "West Medic Rescue",
            SC2_RACESWAP_LOC_ID_OFFSET + 7308,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state) and logic.terran_competent_comp(state)
            ),
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_T.mission_name,
            "East Medic Rescue",
            SC2_RACESWAP_LOC_ID_OFFSET + 7309,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state) and logic.terran_competent_comp(state)
            ),
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_T.mission_name,
            "South Orbital Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 7310,
            LocationType.CHALLENGE,
            lambda state: (
                logic.terran_common_unit(state) and logic.terran_competent_comp(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_T.mission_name,
            "Northwest Orbital Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 7311,
            LocationType.CHALLENGE,
            lambda state: (
                logic.terran_common_unit(state) and logic.terran_competent_comp(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_T.mission_name,
            "Southeast Orbital Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 7312,
            LocationType.CHALLENGE,
            lambda state: (
                logic.terran_common_unit(state) and logic.terran_competent_comp(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 7400,
            LocationType.VICTORY,
            lambda state: (
                logic.protoss_common_unit(state) and logic.protoss_competent_comp(state)
            ),
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_P.mission_name,
            "West Biomass",
            SC2_RACESWAP_LOC_ID_OFFSET + 7401,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_P.mission_name,
            "North Biomass",
            SC2_RACESWAP_LOC_ID_OFFSET + 7402,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_common_unit(state) and logic.protoss_competent_comp(state)
            ),
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_P.mission_name,
            "South Biomass",
            SC2_RACESWAP_LOC_ID_OFFSET + 7403,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_common_unit(state) and logic.protoss_competent_comp(state)
            ),
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_P.mission_name,
            "Destroy 3 Gorgons",
            SC2_RACESWAP_LOC_ID_OFFSET + 7404,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state) and logic.protoss_competent_comp(state)
            ),
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_P.mission_name,
            "Close Rescue",
            SC2_RACESWAP_LOC_ID_OFFSET + 7405,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_P.mission_name,
            "South Rescue",
            SC2_RACESWAP_LOC_ID_OFFSET + 7406,
            LocationType.EXTRA,
            logic.protoss_common_unit,
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_P.mission_name,
            "North Rescue",
            SC2_RACESWAP_LOC_ID_OFFSET + 7407,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state) and logic.protoss_competent_comp(state)
            ),
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_P.mission_name,
            "West Energizer Rescue",
            SC2_RACESWAP_LOC_ID_OFFSET + 7408,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state) and logic.protoss_competent_comp(state)
            ),
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_P.mission_name,
            "East Energizer Rescue",
            SC2_RACESWAP_LOC_ID_OFFSET + 7409,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state) and logic.protoss_competent_comp(state)
            ),
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_P.mission_name,
            "South Orbital Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 7410,
            LocationType.CHALLENGE,
            lambda state: (
                logic.protoss_common_unit(state) and logic.protoss_competent_comp(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_P.mission_name,
            "Northwest Orbital Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 7411,
            LocationType.CHALLENGE,
            lambda state: (
                logic.protoss_common_unit(state) and logic.protoss_competent_comp(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.FIRE_IN_THE_SKY_P.mission_name,
            "Southeast Orbital Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 7412,
            LocationType.CHALLENGE,
            lambda state: (
                logic.protoss_common_unit(state) and logic.protoss_competent_comp(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 7500,
            LocationType.VICTORY,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS_T.mission_name,
            "East Science Lab",
            SC2_RACESWAP_LOC_ID_OFFSET + 7501,
            LocationType.VANILLA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS_T.mission_name,
            "North Science Lab",
            SC2_RACESWAP_LOC_ID_OFFSET + 7502,
            LocationType.VANILLA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS_T.mission_name,
            "Get Nuked",
            SC2_RACESWAP_LOC_ID_OFFSET + 7503,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS_T.mission_name,
            "Entrance Gate",
            SC2_RACESWAP_LOC_ID_OFFSET + 7504,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS_T.mission_name,
            "Citadel Gate",
            SC2_RACESWAP_LOC_ID_OFFSET + 7505,
            LocationType.EXTRA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS_T.mission_name,
            "South Expansion",
            SC2_RACESWAP_LOC_ID_OFFSET + 7506,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS_T.mission_name,
            "Rich Mineral Expansion",
            SC2_RACESWAP_LOC_ID_OFFSET + 7507,
            LocationType.EXTRA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 7600,
            LocationType.VICTORY,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS_P.mission_name,
            "East Science Lab",
            SC2_RACESWAP_LOC_ID_OFFSET + 7601,
            LocationType.VANILLA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS_P.mission_name,
            "North Science Lab",
            SC2_RACESWAP_LOC_ID_OFFSET + 7602,
            LocationType.VANILLA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS_P.mission_name,
            "Get Nuked",
            SC2_RACESWAP_LOC_ID_OFFSET + 7603,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS_P.mission_name,
            "Entrance Gate",
            SC2_RACESWAP_LOC_ID_OFFSET + 7604,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS_P.mission_name,
            "Citadel Gate",
            SC2_RACESWAP_LOC_ID_OFFSET + 7605,
            LocationType.EXTRA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS_P.mission_name,
            "South Expansion",
            SC2_RACESWAP_LOC_ID_OFFSET + 7606,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.OLD_SOLDIERS_P.mission_name,
            "Rich Mineral Expansion",
            SC2_RACESWAP_LOC_ID_OFFSET + 7607,
            LocationType.EXTRA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 7700,
            LocationType.VICTORY,
            lambda state: (
                logic.terran_competent_comp(state) and logic.terran_common_unit(state)
            ),
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT_T.mission_name,
            "Center Essence Pool",
            SC2_RACESWAP_LOC_ID_OFFSET + 7701,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT_T.mission_name,
            "East Essence Pool",
            SC2_RACESWAP_LOC_ID_OFFSET + 7702,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and (
                    adv_tactics
                    and logic.terran_basic_anti_air(state)
                    or logic.terran_competent_anti_air(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT_T.mission_name,
            "South Essence Pool",
            SC2_RACESWAP_LOC_ID_OFFSET + 7703,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and (
                    adv_tactics
                    and logic.terran_basic_anti_air(state)
                    or logic.terran_competent_anti_air(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT_T.mission_name,
            "Finish Feeding",
            SC2_RACESWAP_LOC_ID_OFFSET + 7704,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_competent_comp(state) and logic.terran_common_unit(state)
            ),
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT_T.mission_name,
            "South Proxy Primal Hive",
            SC2_RACESWAP_LOC_ID_OFFSET + 7705,
            LocationType.CHALLENGE,
            lambda state: (
                logic.terran_competent_comp(state) and logic.terran_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT_T.mission_name,
            "East Proxy Primal Hive",
            SC2_RACESWAP_LOC_ID_OFFSET + 7706,
            LocationType.CHALLENGE,
            lambda state: (
                logic.terran_competent_comp(state) and logic.terran_common_unit(state)
            ),
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT_T.mission_name,
            "South Main Primal Hive",
            SC2_RACESWAP_LOC_ID_OFFSET + 7707,
            LocationType.CHALLENGE,
            lambda state: (
                logic.terran_competent_comp(state) and logic.terran_common_unit(state)
            ),
            flags=LocationFlag.BASEBUST,
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT_T.mission_name,
            "East Main Primal Hive",
            SC2_RACESWAP_LOC_ID_OFFSET + 7708,
            LocationType.CHALLENGE,
            lambda state: (
                logic.terran_competent_comp(state) and logic.terran_common_unit(state)
            ),
            flags=LocationFlag.BASEBUST,
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT_T.mission_name,
            "Flawless",
            SC2_RACESWAP_LOC_ID_OFFSET + 7709,
            LocationType.CHALLENGE,
            lambda state: (
                logic.terran_competent_comp(state)
                and logic.terran_common_unit(state)
                and (
                    # Fast unit
                    state.has_any(
                        (
                            item_names.BANSHEE,
                            item_names.VULTURE,
                            item_names.DIAMONDBACK,
                            item_names.WARHOUND,
                            item_names.CYCLONE,
                        ),
                        player,
                    )
                    or state.has_all(
                        (item_names.VALKYRIE, item_names.VALKYRIE_FLECHETTE_MISSILES),
                        player,
                    )
                    or state.has_all(
                        (
                            item_names.WRAITH,
                            item_names.WRAITH_ADVANCED_LASER_TECHNOLOGY,
                        ),
                        player,
                    )
                )
            ),
            flags=LocationFlag.PREVENTATIVE,
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 7800,
            LocationType.VICTORY,
            logic.protoss_competent_comp,
            hard_rule=logic.protoss_any_anti_air_unit,
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT_P.mission_name,
            "Center Essence Pool",
            SC2_RACESWAP_LOC_ID_OFFSET + 7801,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT_P.mission_name,
            "East Essence Pool",
            SC2_RACESWAP_LOC_ID_OFFSET + 7802,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_anti_light_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT_P.mission_name,
            "South Essence Pool",
            SC2_RACESWAP_LOC_ID_OFFSET + 7803,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_anti_light_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT_P.mission_name,
            "Finish Feeding",
            SC2_RACESWAP_LOC_ID_OFFSET + 7804,
            LocationType.EXTRA,
            logic.protoss_competent_comp,
            hard_rule=logic.protoss_any_anti_air_unit,
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT_P.mission_name,
            "South Proxy Primal Hive",
            SC2_RACESWAP_LOC_ID_OFFSET + 7805,
            LocationType.CHALLENGE,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT_P.mission_name,
            "East Proxy Primal Hive",
            SC2_RACESWAP_LOC_ID_OFFSET + 7806,
            LocationType.CHALLENGE,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT_P.mission_name,
            "South Main Primal Hive",
            SC2_RACESWAP_LOC_ID_OFFSET + 7807,
            LocationType.CHALLENGE,
            logic.protoss_competent_comp,
            flags=LocationFlag.BASEBUST,
            hard_rule=logic.protoss_any_anti_air_unit,
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT_P.mission_name,
            "East Main Primal Hive",
            SC2_RACESWAP_LOC_ID_OFFSET + 7808,
            LocationType.CHALLENGE,
            logic.protoss_competent_comp,
            flags=LocationFlag.BASEBUST,
            hard_rule=logic.protoss_any_anti_air_unit,
        ),
        make_location_data(
            SC2Mission.WAKING_THE_ANCIENT_P.mission_name,
            "Flawless",
            SC2_RACESWAP_LOC_ID_OFFSET + 7809,
            LocationType.CHALLENGE,
            logic.protoss_competent_comp,
            flags=LocationFlag.PREVENTATIVE,
            hard_rule=logic.protoss_any_anti_air_unit,
        ),
        make_location_data(
            SC2Mission.THE_CRUCIBLE_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 7900,
            LocationType.VICTORY,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_defense_rating(state, True, True) >= 7
                and logic.terran_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_CRUCIBLE_T.mission_name,
            "Tyrannozor",
            SC2_RACESWAP_LOC_ID_OFFSET + 7901,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_defense_rating(state, True, True) >= 7
                and logic.terran_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_CRUCIBLE_T.mission_name,
            "Reach the Pool",
            SC2_RACESWAP_LOC_ID_OFFSET + 7902,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.THE_CRUCIBLE_T.mission_name,
            "15 Minutes Remaining",
            SC2_RACESWAP_LOC_ID_OFFSET + 7903,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_defense_rating(state, True, True) >= 7
                and logic.terran_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_CRUCIBLE_T.mission_name,
            "5 Minutes Remaining",
            SC2_RACESWAP_LOC_ID_OFFSET + 7904,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_defense_rating(state, True, True) >= 7
                and logic.terran_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_CRUCIBLE_T.mission_name,
            "Pincer Attack",
            SC2_RACESWAP_LOC_ID_OFFSET + 7905,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_defense_rating(state, True, True) >= 7
                and logic.terran_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_CRUCIBLE_T.mission_name,
            "Yagdra Claims Brakk's Pack",
            SC2_RACESWAP_LOC_ID_OFFSET + 7906,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_defense_rating(state, True, True) >= 7
                and logic.terran_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_CRUCIBLE_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 8000,
            LocationType.VICTORY,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_defense_rating(state, True) >= 7
                and logic.protoss_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_CRUCIBLE_P.mission_name,
            "Tyrannozor",
            SC2_RACESWAP_LOC_ID_OFFSET + 8001,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_defense_rating(state, True) >= 7
                and logic.protoss_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_CRUCIBLE_P.mission_name,
            "Reach the Pool",
            SC2_RACESWAP_LOC_ID_OFFSET + 8002,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.THE_CRUCIBLE_P.mission_name,
            "15 Minutes Remaining",
            SC2_RACESWAP_LOC_ID_OFFSET + 8003,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_defense_rating(state, True) >= 7
                and logic.protoss_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_CRUCIBLE_P.mission_name,
            "5 Minutes Remaining",
            SC2_RACESWAP_LOC_ID_OFFSET + 8004,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_defense_rating(state, True) >= 7
                and logic.protoss_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_CRUCIBLE_P.mission_name,
            "Pincer Attack",
            SC2_RACESWAP_LOC_ID_OFFSET + 8005,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_defense_rating(state, True) >= 7
                and logic.protoss_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_CRUCIBLE_P.mission_name,
            "Yagdra Claims Brakk's Pack",
            SC2_RACESWAP_LOC_ID_OFFSET + 8006,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_defense_rating(state, True) >= 7
                and logic.protoss_competent_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.INFESTED_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 8300,
            LocationType.VICTORY,
            lambda state: (
                logic.terran_common_unit(state) and logic.terran_competent_comp(state)
            ),
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.INFESTED_T.mission_name,
            "East Science Facility",
            SC2_RACESWAP_LOC_ID_OFFSET + 8301,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_moderate_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.INFESTED_T.mission_name,
            "Center Science Facility",
            SC2_RACESWAP_LOC_ID_OFFSET + 8302,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state) and logic.terran_competent_comp(state)
            ),
        ),
        make_location_data(
            SC2Mission.INFESTED_T.mission_name,
            "West Science Facility",
            SC2_RACESWAP_LOC_ID_OFFSET + 8303,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state) and logic.terran_competent_comp(state)
            ),
        ),
        make_location_data(
            SC2Mission.INFESTED_T.mission_name,
            "First Intro Garrison",
            SC2_RACESWAP_LOC_ID_OFFSET + 8304,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.INFESTED_T.mission_name,
            "Second Intro Garrison",
            SC2_RACESWAP_LOC_ID_OFFSET + 8305,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.INFESTED_T.mission_name,
            "Base Garrison",
            SC2_RACESWAP_LOC_ID_OFFSET + 8306,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.INFESTED_T.mission_name,
            "East Garrison",
            SC2_RACESWAP_LOC_ID_OFFSET + 8307,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_moderate_anti_air(state)
                and (adv_tactics or logic.terran_infested_garrison_claimer(state))
            ),
        ),
        make_location_data(
            SC2Mission.INFESTED_T.mission_name,
            "Mid Garrison",
            SC2_RACESWAP_LOC_ID_OFFSET + 8308,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_moderate_anti_air(state)
                and (adv_tactics or logic.terran_infested_garrison_claimer(state))
            ),
        ),
        make_location_data(
            SC2Mission.INFESTED_T.mission_name,
            "North Garrison",
            SC2_RACESWAP_LOC_ID_OFFSET + 8309,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_competent_comp(state)
                and (adv_tactics or logic.terran_infested_garrison_claimer(state))
            ),
        ),
        make_location_data(
            SC2Mission.INFESTED_T.mission_name,
            "Close Southwest Garrison",
            SC2_RACESWAP_LOC_ID_OFFSET + 8310,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_competent_comp(state)
                and (adv_tactics or logic.terran_infested_garrison_claimer(state))
            ),
        ),
        make_location_data(
            SC2Mission.INFESTED_T.mission_name,
            "Far Southwest Garrison",
            SC2_RACESWAP_LOC_ID_OFFSET + 8311,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_competent_comp(state)
                and (adv_tactics or logic.terran_infested_garrison_claimer(state))
            ),
        ),
        make_location_data(
            SC2Mission.INFESTED_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 8400,
            LocationType.VICTORY,
            logic.protoss_competent_comp,
            hard_rule=logic.protoss_any_anti_air_unit_or_soa_any_protoss,
        ),
        make_location_data(
            SC2Mission.INFESTED_P.mission_name,
            "East Science Facility",
            SC2_RACESWAP_LOC_ID_OFFSET + 8401,
            LocationType.VANILLA,
            lambda state: (
                logic.protoss_common_unit(state) and logic.protoss_basic_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.INFESTED_P.mission_name,
            "Center Science Facility",
            SC2_RACESWAP_LOC_ID_OFFSET + 8402,
            LocationType.VANILLA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.INFESTED_P.mission_name,
            "West Science Facility",
            SC2_RACESWAP_LOC_ID_OFFSET + 8403,
            LocationType.VANILLA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.INFESTED_P.mission_name,
            "First Intro Garrison",
            SC2_RACESWAP_LOC_ID_OFFSET + 8404,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.INFESTED_P.mission_name,
            "Second Intro Garrison",
            SC2_RACESWAP_LOC_ID_OFFSET + 8405,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.INFESTED_P.mission_name,
            "Base Garrison",
            SC2_RACESWAP_LOC_ID_OFFSET + 8406,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.INFESTED_P.mission_name,
            "East Garrison",
            SC2_RACESWAP_LOC_ID_OFFSET + 8407,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_basic_anti_air(state)
                and (adv_tactics or logic.protoss_infested_garrison_claimer(state))
            ),
        ),
        make_location_data(
            SC2Mission.INFESTED_P.mission_name,
            "Mid Garrison",
            SC2_RACESWAP_LOC_ID_OFFSET + 8408,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_basic_anti_air(state)
                and (adv_tactics or logic.protoss_infested_garrison_claimer(state))
            ),
        ),
        make_location_data(
            SC2Mission.INFESTED_P.mission_name,
            "North Garrison",
            SC2_RACESWAP_LOC_ID_OFFSET + 8409,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_common_unit(state)
                and logic.protoss_competent_anti_air(state)
                and (adv_tactics or logic.protoss_infested_garrison_claimer(state))
            ),
        ),
        make_location_data(
            SC2Mission.INFESTED_P.mission_name,
            "Close Southwest Garrison",
            SC2_RACESWAP_LOC_ID_OFFSET + 8410,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_competent_comp(state)
                and (adv_tactics or logic.protoss_infested_garrison_claimer(state))
            ),
        ),
        make_location_data(
            SC2Mission.INFESTED_P.mission_name,
            "Far Southwest Garrison",
            SC2_RACESWAP_LOC_ID_OFFSET + 8411,
            LocationType.EXTRA,
            lambda state: (
                logic.protoss_competent_comp(state)
                and (adv_tactics or logic.protoss_infested_garrison_claimer(state))
            ),
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 8500,
            LocationType.VICTORY,
            logic.terran_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS_T.mission_name,
            "North War Bot",
            SC2_RACESWAP_LOC_ID_OFFSET + 8501,
            LocationType.VANILLA,
            logic.terran_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS_T.mission_name,
            "South War Bot",
            SC2_RACESWAP_LOC_ID_OFFSET + 8502,
            LocationType.VANILLA,
            logic.terran_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS_T.mission_name,
            "Kill 1 Hybrid",
            SC2_RACESWAP_LOC_ID_OFFSET + 8503,
            LocationType.EXTRA,
            logic.terran_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS_T.mission_name,
            "Kill 2 Hybrid",
            SC2_RACESWAP_LOC_ID_OFFSET + 8504,
            LocationType.EXTRA,
            logic.terran_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS_T.mission_name,
            "Kill 3 Hybrid",
            SC2_RACESWAP_LOC_ID_OFFSET + 8505,
            LocationType.EXTRA,
            logic.terran_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS_T.mission_name,
            "Kill 4 Hybrid",
            SC2_RACESWAP_LOC_ID_OFFSET + 8506,
            LocationType.EXTRA,
            logic.terran_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS_T.mission_name,
            "Kill 5 Hybrid",
            SC2_RACESWAP_LOC_ID_OFFSET + 8507,
            LocationType.EXTRA,
            logic.terran_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS_T.mission_name,
            "Kill 6 Hybrid",
            SC2_RACESWAP_LOC_ID_OFFSET + 8508,
            LocationType.EXTRA,
            logic.terran_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS_T.mission_name,
            "Kill 7 Hybrid",
            SC2_RACESWAP_LOC_ID_OFFSET + 8509,
            LocationType.EXTRA,
            logic.terran_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 8600,
            LocationType.VICTORY,
            logic.protoss_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS_P.mission_name,
            "North Stone Zealot",
            SC2_RACESWAP_LOC_ID_OFFSET + 8601,
            LocationType.VANILLA,
            logic.protoss_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS_P.mission_name,
            "South Stone Zealot",
            SC2_RACESWAP_LOC_ID_OFFSET + 8602,
            LocationType.VANILLA,
            logic.protoss_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS_P.mission_name,
            "Kill 1 Hybrid",
            SC2_RACESWAP_LOC_ID_OFFSET + 8603,
            LocationType.EXTRA,
            logic.protoss_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS_P.mission_name,
            "Kill 2 Hybrid",
            SC2_RACESWAP_LOC_ID_OFFSET + 8604,
            LocationType.EXTRA,
            logic.protoss_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS_P.mission_name,
            "Kill 3 Hybrid",
            SC2_RACESWAP_LOC_ID_OFFSET + 8605,
            LocationType.EXTRA,
            logic.protoss_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS_P.mission_name,
            "Kill 4 Hybrid",
            SC2_RACESWAP_LOC_ID_OFFSET + 8606,
            LocationType.EXTRA,
            logic.protoss_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS_P.mission_name,
            "Kill 5 Hybrid",
            SC2_RACESWAP_LOC_ID_OFFSET + 8607,
            LocationType.EXTRA,
            logic.protoss_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS_P.mission_name,
            "Kill 6 Hybrid",
            SC2_RACESWAP_LOC_ID_OFFSET + 8608,
            LocationType.EXTRA,
            logic.protoss_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.HAND_OF_DARKNESS_P.mission_name,
            "Kill 7 Hybrid",
            SC2_RACESWAP_LOC_ID_OFFSET + 8609,
            LocationType.EXTRA,
            logic.protoss_hand_of_darkness_requirement,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 8700,
            LocationType.VICTORY,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID_T.mission_name,
            "Northwest Crystal",
            SC2_RACESWAP_LOC_ID_OFFSET + 8701,
            LocationType.VANILLA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID_T.mission_name,
            "Northeast Crystal",
            SC2_RACESWAP_LOC_ID_OFFSET + 8702,
            LocationType.VANILLA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID_T.mission_name,
            "South Crystal",
            SC2_RACESWAP_LOC_ID_OFFSET + 8703,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID_T.mission_name,
            "Base Established",
            SC2_RACESWAP_LOC_ID_OFFSET + 8704,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID_T.mission_name,
            "Close Temple",
            SC2_RACESWAP_LOC_ID_OFFSET + 8705,
            LocationType.EXTRA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID_T.mission_name,
            "Mid Temple",
            SC2_RACESWAP_LOC_ID_OFFSET + 8706,
            LocationType.EXTRA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID_T.mission_name,
            "Southeast Temple",
            SC2_RACESWAP_LOC_ID_OFFSET + 8707,
            LocationType.EXTRA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID_T.mission_name,
            "Northeast Temple",
            SC2_RACESWAP_LOC_ID_OFFSET + 8708,
            LocationType.EXTRA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID_T.mission_name,
            "Northwest Temple",
            SC2_RACESWAP_LOC_ID_OFFSET + 8709,
            LocationType.EXTRA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 8800,
            LocationType.VICTORY,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID_P.mission_name,
            "Northwest Crystal",
            SC2_RACESWAP_LOC_ID_OFFSET + 8801,
            LocationType.VANILLA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID_P.mission_name,
            "Northeast Crystal",
            SC2_RACESWAP_LOC_ID_OFFSET + 8802,
            LocationType.VANILLA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID_P.mission_name,
            "South Crystal",
            SC2_RACESWAP_LOC_ID_OFFSET + 8803,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID_P.mission_name,
            "Base Established",
            SC2_RACESWAP_LOC_ID_OFFSET + 8804,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID_P.mission_name,
            "Close Temple",
            SC2_RACESWAP_LOC_ID_OFFSET + 8805,
            LocationType.EXTRA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID_P.mission_name,
            "Mid Temple",
            SC2_RACESWAP_LOC_ID_OFFSET + 8806,
            LocationType.EXTRA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID_P.mission_name,
            "Southeast Temple",
            SC2_RACESWAP_LOC_ID_OFFSET + 8807,
            LocationType.EXTRA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID_P.mission_name,
            "Northeast Temple",
            SC2_RACESWAP_LOC_ID_OFFSET + 8808,
            LocationType.EXTRA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.PHANTOMS_OF_THE_VOID_P.mission_name,
            "Northwest Temple",
            SC2_RACESWAP_LOC_ID_OFFSET + 8809,
            LocationType.EXTRA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 9300,
            LocationType.VICTORY,
            logic.terran_planetfall_requirement,
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_T.mission_name,
            "East Gate",
            SC2_RACESWAP_LOC_ID_OFFSET + 9301,
            LocationType.VANILLA,
            logic.terran_planetfall_requirement,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_T.mission_name,
            "Northwest Gate",
            SC2_RACESWAP_LOC_ID_OFFSET + 9302,
            LocationType.VANILLA,
            logic.terran_planetfall_requirement,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_T.mission_name,
            "North Gate",
            SC2_RACESWAP_LOC_ID_OFFSET + 9303,
            LocationType.VANILLA,
            logic.terran_planetfall_requirement,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_T.mission_name,
            "1 Laser Drill Deployed",
            SC2_RACESWAP_LOC_ID_OFFSET + 9304,
            LocationType.EXTRA,
            logic.terran_planetfall_requirement,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_T.mission_name,
            "2 Laser Drills Deployed",
            SC2_RACESWAP_LOC_ID_OFFSET + 9305,
            LocationType.EXTRA,
            logic.terran_planetfall_requirement,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_T.mission_name,
            "3 Laser Drills Deployed",
            SC2_RACESWAP_LOC_ID_OFFSET + 9306,
            LocationType.EXTRA,
            logic.terran_planetfall_requirement,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_T.mission_name,
            "4 Laser Drills Deployed",
            SC2_RACESWAP_LOC_ID_OFFSET + 9307,
            LocationType.EXTRA,
            logic.terran_planetfall_requirement,
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_T.mission_name,
            "5 Laser Drills Deployed",
            SC2_RACESWAP_LOC_ID_OFFSET + 9308,
            LocationType.EXTRA,
            logic.terran_planetfall_requirement,
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_T.mission_name,
            "Sons of Korhal",
            SC2_RACESWAP_LOC_ID_OFFSET + 9309,
            LocationType.EXTRA,
            logic.terran_planetfall_requirement,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_T.mission_name,
            "Night Wolves",
            SC2_RACESWAP_LOC_ID_OFFSET + 9310,
            LocationType.EXTRA,
            logic.terran_planetfall_requirement,
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_T.mission_name,
            "West Expansion",
            SC2_RACESWAP_LOC_ID_OFFSET + 9311,
            LocationType.EXTRA,
            logic.terran_planetfall_requirement,
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_T.mission_name,
            "Mid Expansion",
            SC2_RACESWAP_LOC_ID_OFFSET + 9312,
            LocationType.EXTRA,
            logic.terran_planetfall_requirement,
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 9400,
            LocationType.VICTORY,
            logic.protoss_planetfall_requirement,
            hard_rule=logic.protoss_any_anti_air_unit_or_soa_any_protoss,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_P.mission_name,
            "East Gate",
            SC2_RACESWAP_LOC_ID_OFFSET + 9401,
            LocationType.VANILLA,
            logic.protoss_planetfall_requirement,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_P.mission_name,
            "Northwest Gate",
            SC2_RACESWAP_LOC_ID_OFFSET + 9402,
            LocationType.VANILLA,
            logic.protoss_planetfall_requirement,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_P.mission_name,
            "North Gate",
            SC2_RACESWAP_LOC_ID_OFFSET + 9403,
            LocationType.VANILLA,
            logic.protoss_planetfall_requirement,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_P.mission_name,
            "1 Particle Cannon Deployed",
            SC2_RACESWAP_LOC_ID_OFFSET + 9404,
            LocationType.EXTRA,
            logic.protoss_planetfall_requirement,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_P.mission_name,
            "2 Particle Cannons Deployed",
            SC2_RACESWAP_LOC_ID_OFFSET + 9405,
            LocationType.EXTRA,
            logic.protoss_planetfall_requirement,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_P.mission_name,
            "3 Particle Cannons Deployed",
            SC2_RACESWAP_LOC_ID_OFFSET + 9406,
            LocationType.EXTRA,
            logic.protoss_planetfall_requirement,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_P.mission_name,
            "4 Particle Cannons Deployed",
            SC2_RACESWAP_LOC_ID_OFFSET + 9407,
            LocationType.EXTRA,
            logic.protoss_planetfall_requirement,
            hard_rule=logic.protoss_any_anti_air_unit_or_soa_any_protoss,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_P.mission_name,
            "5 Particle Cannons Deployed",
            SC2_RACESWAP_LOC_ID_OFFSET + 9408,
            LocationType.EXTRA,
            logic.protoss_planetfall_requirement,
            hard_rule=logic.protoss_any_anti_air_unit_or_soa_any_protoss,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_P.mission_name,
            "Sons of Korhal",
            SC2_RACESWAP_LOC_ID_OFFSET + 9409,
            LocationType.EXTRA,
            logic.protoss_planetfall_requirement,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_P.mission_name,
            "Night Wolves",
            SC2_RACESWAP_LOC_ID_OFFSET + 9410,
            LocationType.EXTRA,
            logic.protoss_planetfall_requirement,
            hard_rule=logic.protoss_any_anti_air_unit_or_soa_any_protoss,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_P.mission_name,
            "West Expansion",
            SC2_RACESWAP_LOC_ID_OFFSET + 9411,
            LocationType.EXTRA,
            logic.protoss_planetfall_requirement,
            hard_rule=logic.protoss_any_anti_air_unit_or_soa_any_protoss,
        ),
        make_location_data(
            SC2Mission.PLANETFALL_P.mission_name,
            "Mid Expansion",
            SC2_RACESWAP_LOC_ID_OFFSET + 9412,
            LocationType.EXTRA,
            logic.protoss_planetfall_requirement,
            hard_rule=logic.protoss_any_anti_air_unit_or_soa_any_protoss,
        ),
        make_location_data(
            SC2Mission.DEATH_FROM_ABOVE_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 9500,
            LocationType.VICTORY,
            logic.terran_base_trasher,
        ),
        make_location_data(
            SC2Mission.DEATH_FROM_ABOVE_T.mission_name,
            "First Power Link",
            SC2_RACESWAP_LOC_ID_OFFSET + 9501,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.DEATH_FROM_ABOVE_T.mission_name,
            "Second Power Link",
            SC2_RACESWAP_LOC_ID_OFFSET + 9502,
            LocationType.VANILLA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.DEATH_FROM_ABOVE_T.mission_name,
            "Third Power Link",
            SC2_RACESWAP_LOC_ID_OFFSET + 9503,
            LocationType.VANILLA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.DEATH_FROM_ABOVE_T.mission_name,
            "Expansion Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 9504,
            LocationType.EXTRA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.DEATH_FROM_ABOVE_T.mission_name,
            "Main Path Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 9505,
            LocationType.EXTRA,
            logic.terran_base_trasher,
        ),
        make_location_data(
            SC2Mission.DEATH_FROM_ABOVE_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 9600,
            LocationType.VICTORY,
            lambda state: logic.protoss_deathball(state)
            or (adv_tactics and logic.protoss_competent_comp(state)),
        ),
        make_location_data(
            SC2Mission.DEATH_FROM_ABOVE_P.mission_name,
            "First Power Link",
            SC2_RACESWAP_LOC_ID_OFFSET + 9601,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.DEATH_FROM_ABOVE_P.mission_name,
            "Second Power Link",
            SC2_RACESWAP_LOC_ID_OFFSET + 9602,
            LocationType.VANILLA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.DEATH_FROM_ABOVE_P.mission_name,
            "Third Power Link",
            SC2_RACESWAP_LOC_ID_OFFSET + 9603,
            LocationType.VANILLA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.DEATH_FROM_ABOVE_P.mission_name,
            "Expansion Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 9604,
            LocationType.EXTRA,
            logic.protoss_competent_comp,
        ),
        make_location_data(
            SC2Mission.DEATH_FROM_ABOVE_P.mission_name,
            "Main Path Command Center",
            SC2_RACESWAP_LOC_ID_OFFSET + 9605,
            LocationType.EXTRA,
            lambda state: logic.protoss_deathball(state)
            or (adv_tactics and logic.protoss_competent_comp(state)),
        ),
        make_location_data(
            SC2Mission.THE_RECKONING_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 9700,
            LocationType.VICTORY,
            logic.terran_the_reckoning_requirement,
        ),
        make_location_data(
            SC2Mission.THE_RECKONING_T.mission_name,
            "South Lane",
            SC2_RACESWAP_LOC_ID_OFFSET + 9701,
            LocationType.VANILLA,
            logic.terran_the_reckoning_requirement,
        ),
        make_location_data(
            SC2Mission.THE_RECKONING_T.mission_name,
            "North Lane",
            SC2_RACESWAP_LOC_ID_OFFSET + 9702,
            LocationType.VANILLA,
            logic.terran_the_reckoning_requirement,
        ),
        make_location_data(
            SC2Mission.THE_RECKONING_T.mission_name,
            "East Lane",
            SC2_RACESWAP_LOC_ID_OFFSET + 9703,
            LocationType.VANILLA,
            logic.terran_the_reckoning_requirement,
        ),
        make_location_data(
            SC2Mission.THE_RECKONING_T.mission_name,
            "Odin",
            SC2_RACESWAP_LOC_ID_OFFSET + 9704,
            LocationType.EXTRA,
            logic.terran_the_reckoning_requirement,
        ),
        make_location_data(
            SC2Mission.THE_RECKONING_T.mission_name,
            "Trash the Odin Early",
            SC2_RACESWAP_LOC_ID_OFFSET + 9705,
            LocationType.MASTERY,
            lambda state: (
                logic.terran_the_reckoning_requirement(state)
                and logic.terran_power_rating(state) >= 10
            ),
            flags=LocationFlag.SPEEDRUN,
        ),
        make_location_data(
            SC2Mission.THE_RECKONING_P.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 9800,
            LocationType.VICTORY,
            logic.protoss_the_reckoning_requirement,
        ),
        make_location_data(
            SC2Mission.THE_RECKONING_P.mission_name,
            "South Lane",
            SC2_RACESWAP_LOC_ID_OFFSET + 9801,
            LocationType.VANILLA,
            logic.protoss_the_reckoning_requirement,
        ),
        make_location_data(
            SC2Mission.THE_RECKONING_P.mission_name,
            "North Lane",
            SC2_RACESWAP_LOC_ID_OFFSET + 9802,
            LocationType.VANILLA,
            logic.protoss_the_reckoning_requirement,
        ),
        make_location_data(
            SC2Mission.THE_RECKONING_P.mission_name,
            "East Lane",
            SC2_RACESWAP_LOC_ID_OFFSET + 9803,
            LocationType.VANILLA,
            logic.protoss_the_reckoning_requirement,
        ),
        make_location_data(
            SC2Mission.THE_RECKONING_P.mission_name,
            "Odin",
            SC2_RACESWAP_LOC_ID_OFFSET + 9804,
            LocationType.EXTRA,
            logic.protoss_the_reckoning_requirement,
        ),
        make_location_data(
            SC2Mission.THE_RECKONING_P.mission_name,
            "Trash the Odin Early",
            SC2_RACESWAP_LOC_ID_OFFSET + 9805,
            LocationType.MASTERY,
            lambda state: (
                logic.protoss_the_reckoning_requirement(state)
                and (
                    logic.protoss_fleet(state)
                    or logic.protoss_power_rating(state) >= 10
                )
            ),
            flags=LocationFlag.SPEEDRUN,
        ),
        make_location_data(
            SC2Mission.DARK_WHISPERS_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 9900,
            LocationType.VICTORY,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.DARK_WHISPERS_T.mission_name,
            "First Prisoner Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 9901,
            LocationType.VANILLA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.DARK_WHISPERS_T.mission_name,
            "Second Prisoner Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 9902,
            LocationType.VANILLA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.DARK_WHISPERS_T.mission_name,
            "First Pylon",
            SC2_RACESWAP_LOC_ID_OFFSET + 9903,
            LocationType.VANILLA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.DARK_WHISPERS_T.mission_name,
            "Second Pylon",
            SC2_RACESWAP_LOC_ID_OFFSET + 9904,
            LocationType.VANILLA,
            logic.terran_competent_comp,
        ),
        make_location_data(
            SC2Mission.DARK_WHISPERS_T.mission_name,
            "Zerg Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 9905,
            LocationType.MASTERY,
            lambda state: (
                logic.terran_competent_comp(state)
                and logic.terran_base_trasher(state)
                and logic.terran_power_rating(state) >= 6
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.DARK_WHISPERS_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 10000,
            LocationType.VICTORY,
            lambda state: logic.zerg_competent_comp(state)
            and logic.zerg_moderate_anti_air(state),
        ),
        make_location_data(
            SC2Mission.DARK_WHISPERS_Z.mission_name,
            "First Prisoner Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 10001,
            LocationType.VANILLA,
            lambda state: logic.zerg_competent_comp(state)
            and logic.zerg_moderate_anti_air(state),
        ),
        make_location_data(
            SC2Mission.DARK_WHISPERS_Z.mission_name,
            "Second Prisoner Group",
            SC2_RACESWAP_LOC_ID_OFFSET + 10002,
            LocationType.VANILLA,
            lambda state: logic.zerg_competent_comp(state)
            and logic.zerg_moderate_anti_air(state),
        ),
        make_location_data(
            SC2Mission.DARK_WHISPERS_Z.mission_name,
            "First Pylon",
            SC2_RACESWAP_LOC_ID_OFFSET + 10003,
            LocationType.VANILLA,
            lambda state: logic.zerg_competent_comp(state)
            and logic.zerg_moderate_anti_air(state),
        ),
        make_location_data(
            SC2Mission.DARK_WHISPERS_Z.mission_name,
            "Second Pylon",
            SC2_RACESWAP_LOC_ID_OFFSET + 10004,
            LocationType.VANILLA,
            lambda state: logic.zerg_competent_comp(state)
            and logic.zerg_moderate_anti_air(state),
        ),
        make_location_data(
            SC2Mission.DARK_WHISPERS_Z.mission_name,
            "Zerg Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 10005,
            LocationType.MASTERY,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_moderate_anti_air(state)
                and logic.zerg_base_buster(state)
                and logic.zerg_power_rating(state) >= 6
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.GHOSTS_IN_THE_FOG_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 10100,
            LocationType.VICTORY,
            lambda state: (
                logic.terran_beats_protoss_deathball(state)
                and logic.terran_mineral_dump(state)
            ),
        ),
        make_location_data(
            SC2Mission.GHOSTS_IN_THE_FOG_T.mission_name,
            "South Rock Formation",
            SC2_RACESWAP_LOC_ID_OFFSET + 10101,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_beats_protoss_deathball(state)
                and logic.terran_mineral_dump(state)
            ),
        ),
        make_location_data(
            SC2Mission.GHOSTS_IN_THE_FOG_T.mission_name,
            "West Rock Formation",
            SC2_RACESWAP_LOC_ID_OFFSET + 10102,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_beats_protoss_deathball(state)
                and logic.terran_mineral_dump(state)
            ),
        ),
        make_location_data(
            SC2Mission.GHOSTS_IN_THE_FOG_T.mission_name,
            "East Rock Formation",
            SC2_RACESWAP_LOC_ID_OFFSET + 10103,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_beats_protoss_deathball(state)
                and logic.terran_mineral_dump(state)
                and logic.terran_can_grab_ghosts_in_the_fog_east_rock_formation(state)
            ),
        ),
        make_location_data(
            SC2Mission.GHOSTS_IN_THE_FOG_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 10200,
            LocationType.VICTORY,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_competent_anti_air(state)
                and logic.zerg_mineral_dump(state)
            ),
        ),
        make_location_data(
            SC2Mission.GHOSTS_IN_THE_FOG_Z.mission_name,
            "South Rock Formation",
            SC2_RACESWAP_LOC_ID_OFFSET + 10201,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_competent_anti_air(state)
                and logic.zerg_mineral_dump(state)
            ),
        ),
        make_location_data(
            SC2Mission.GHOSTS_IN_THE_FOG_Z.mission_name,
            "West Rock Formation",
            SC2_RACESWAP_LOC_ID_OFFSET + 10202,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_competent_anti_air(state)
                and logic.zerg_mineral_dump(state)
            ),
        ),
        make_location_data(
            SC2Mission.GHOSTS_IN_THE_FOG_Z.mission_name,
            "East Rock Formation",
            SC2_RACESWAP_LOC_ID_OFFSET + 10203,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_competent_anti_air(state)
                and logic.zerg_mineral_dump(state)
                and logic.zerg_can_grab_ghosts_in_the_fog_east_rock_formation(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_GROWING_SHADOW_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 10700,
            LocationType.VICTORY,
            lambda state: (
                logic.terran_common_unit(state)
                and (adv_tactics or logic.terran_moderate_anti_air(state))
            ),
        ),
        make_location_data(
            SC2Mission.THE_GROWING_SHADOW_T.mission_name,
            "Close Pylon",
            SC2_RACESWAP_LOC_ID_OFFSET + 10701,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.THE_GROWING_SHADOW_T.mission_name,
            "East Pylon",
            SC2_RACESWAP_LOC_ID_OFFSET + 10702,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and (
                    adv_tactics
                    or (
                        logic.terran_moderate_anti_air(state)
                        and logic.terran_any_air_unit(state)
                    )
                )
            ),
        ),
        make_location_data(
            SC2Mission.THE_GROWING_SHADOW_T.mission_name,
            "West Pylon",
            SC2_RACESWAP_LOC_ID_OFFSET + 10703,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and (adv_tactics or logic.terran_moderate_anti_air(state))
            ),
        ),
        make_location_data(
            SC2Mission.THE_GROWING_SHADOW_T.mission_name,
            "Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 10704,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_GROWING_SHADOW_T.mission_name,
            "Templar Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 10705,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state)
                and (adv_tactics or logic.terran_moderate_anti_air(state))
            ),
        ),
        make_location_data(
            SC2Mission.THE_GROWING_SHADOW_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 10800,
            LocationType.VICTORY,
            lambda state: (
                logic.zerg_common_unit(state) and logic.zerg_moderate_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_GROWING_SHADOW_Z.mission_name,
            "Close Pylon",
            SC2_RACESWAP_LOC_ID_OFFSET + 10801,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.THE_GROWING_SHADOW_Z.mission_name,
            "East Pylon",
            SC2_RACESWAP_LOC_ID_OFFSET + 10802,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state) and logic.zerg_moderate_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_GROWING_SHADOW_Z.mission_name,
            "West Pylon",
            SC2_RACESWAP_LOC_ID_OFFSET + 10803,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_common_unit(state) and logic.zerg_moderate_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_GROWING_SHADOW_Z.mission_name,
            "Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 10804,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.THE_GROWING_SHADOW_Z.mission_name,
            "Templar Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 10805,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_common_unit(state) and logic.zerg_moderate_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 10900,
            LocationType.VICTORY,
            logic.terran_spear_of_adun_requirement,
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN_T.mission_name,
            "Factory",
            SC2_RACESWAP_LOC_ID_OFFSET + 10901,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN_T.mission_name,
            "Armory",
            SC2_RACESWAP_LOC_ID_OFFSET + 10902,
            LocationType.VANILLA,
            logic.terran_spear_of_adun_requirement,
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN_T.mission_name,
            "Starport",
            SC2_RACESWAP_LOC_ID_OFFSET + 10903,
            LocationType.VANILLA,
            logic.terran_spear_of_adun_requirement,
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN_T.mission_name,
            "North Power Cell",
            SC2_RACESWAP_LOC_ID_OFFSET + 10904,
            LocationType.EXTRA,
            logic.terran_spear_of_adun_requirement,
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN_T.mission_name,
            "East Power Cell",
            SC2_RACESWAP_LOC_ID_OFFSET + 10905,
            LocationType.EXTRA,
            logic.terran_spear_of_adun_requirement,
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN_T.mission_name,
            "South Power Cell",
            SC2_RACESWAP_LOC_ID_OFFSET + 10906,
            LocationType.EXTRA,
            logic.terran_spear_of_adun_requirement,
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN_T.mission_name,
            "Southeast Power Cell",
            SC2_RACESWAP_LOC_ID_OFFSET + 10907,
            LocationType.EXTRA,
            logic.terran_spear_of_adun_requirement,
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 11000,
            LocationType.VICTORY,
            logic.zerg_competent_comp_competent_aa,
            hard_rule=logic.zerg_any_anti_air,
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN_Z.mission_name,
            "Baneling Nest",
            SC2_RACESWAP_LOC_ID_OFFSET + 11001,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN_Z.mission_name,
            "Roach Warren",
            SC2_RACESWAP_LOC_ID_OFFSET + 11002,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_spear_of_adun_requirement(state)
                and logic.spread_creep(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN_Z.mission_name,
            "Infestation Pit",
            SC2_RACESWAP_LOC_ID_OFFSET + 11003,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_spear_of_adun_requirement(state)
                and logic.spread_creep(state)
            ),
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN_Z.mission_name,
            "North Power Cell",
            SC2_RACESWAP_LOC_ID_OFFSET + 11004,
            LocationType.EXTRA,
            logic.zerg_spear_of_adun_requirement,
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN_Z.mission_name,
            "East Power Cell",
            SC2_RACESWAP_LOC_ID_OFFSET + 11005,
            LocationType.EXTRA,
            logic.zerg_spear_of_adun_requirement,
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN_Z.mission_name,
            "South Power Cell",
            SC2_RACESWAP_LOC_ID_OFFSET + 11006,
            LocationType.EXTRA,
            logic.zerg_spear_of_adun_requirement,
        ),
        make_location_data(
            SC2Mission.THE_SPEAR_OF_ADUN_Z.mission_name,
            "Southeast Power Cell",
            SC2_RACESWAP_LOC_ID_OFFSET + 11007,
            LocationType.EXTRA,
            logic.zerg_spear_of_adun_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 11100,
            LocationType.VICTORY,
            logic.terran_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD_T.mission_name,
            "Mid EMP Scrambler",
            SC2_RACESWAP_LOC_ID_OFFSET + 11101,
            LocationType.VANILLA,
            logic.terran_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD_T.mission_name,
            "Southeast EMP Scrambler",
            SC2_RACESWAP_LOC_ID_OFFSET + 11102,
            LocationType.VANILLA,
            logic.terran_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD_T.mission_name,
            "North EMP Scrambler",
            SC2_RACESWAP_LOC_ID_OFFSET + 11103,
            LocationType.VANILLA,
            logic.terran_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD_T.mission_name,
            "Mid Stabilizer",
            SC2_RACESWAP_LOC_ID_OFFSET + 11104,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD_T.mission_name,
            "Southwest Stabilizer",
            SC2_RACESWAP_LOC_ID_OFFSET + 11105,
            LocationType.EXTRA,
            logic.terran_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD_T.mission_name,
            "Northwest Stabilizer",
            SC2_RACESWAP_LOC_ID_OFFSET + 11106,
            LocationType.EXTRA,
            logic.terran_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD_T.mission_name,
            "Northeast Stabilizer",
            SC2_RACESWAP_LOC_ID_OFFSET + 11107,
            LocationType.EXTRA,
            logic.terran_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD_T.mission_name,
            "Southeast Stabilizer",
            SC2_RACESWAP_LOC_ID_OFFSET + 11108,
            LocationType.EXTRA,
            logic.terran_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD_T.mission_name,
            "West Raynor Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 11109,
            LocationType.EXTRA,
            logic.terran_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD_T.mission_name,
            "East Raynor Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 11110,
            LocationType.EXTRA,
            logic.terran_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 11200,
            LocationType.VICTORY,
            logic.zerg_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD_Z.mission_name,
            "Mid EMP Scrambler",
            SC2_RACESWAP_LOC_ID_OFFSET + 11201,
            LocationType.VANILLA,
            logic.zerg_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD_Z.mission_name,
            "Southeast EMP Scrambler",
            SC2_RACESWAP_LOC_ID_OFFSET + 11202,
            LocationType.VANILLA,
            logic.zerg_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD_Z.mission_name,
            "North EMP Scrambler",
            SC2_RACESWAP_LOC_ID_OFFSET + 11203,
            LocationType.VANILLA,
            logic.zerg_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD_Z.mission_name,
            "Mid Stabilizer",
            SC2_RACESWAP_LOC_ID_OFFSET + 11204,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD_Z.mission_name,
            "Southwest Stabilizer",
            SC2_RACESWAP_LOC_ID_OFFSET + 11205,
            LocationType.EXTRA,
            logic.zerg_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD_Z.mission_name,
            "Northwest Stabilizer",
            SC2_RACESWAP_LOC_ID_OFFSET + 11206,
            LocationType.EXTRA,
            logic.zerg_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD_Z.mission_name,
            "Northeast Stabilizer",
            SC2_RACESWAP_LOC_ID_OFFSET + 11207,
            LocationType.EXTRA,
            logic.zerg_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD_Z.mission_name,
            "Southeast Stabilizer",
            SC2_RACESWAP_LOC_ID_OFFSET + 11208,
            LocationType.EXTRA,
            logic.zerg_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD_Z.mission_name,
            "West Raynor Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 11209,
            LocationType.EXTRA,
            logic.zerg_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.SKY_SHIELD_Z.mission_name,
            "East Raynor Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 11210,
            LocationType.EXTRA,
            logic.zerg_sky_shield_requirement,
        ),
        make_location_data(
            SC2Mission.BROTHERS_IN_ARMS_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 11300,
            LocationType.VICTORY,
            lambda state: (
                logic.terran_common_unit(state) and logic.terran_competent_comp(state)
            ),
        ),
        make_location_data(
            SC2Mission.BROTHERS_IN_ARMS_T.mission_name,
            "Mid Science Facility",
            SC2_RACESWAP_LOC_ID_OFFSET + 11301,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.BROTHERS_IN_ARMS_T.mission_name,
            "North Science Facility",
            SC2_RACESWAP_LOC_ID_OFFSET + 11302,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_competent_comp(state)
                or (
                    logic.take_over_ai_allies
                    and logic.advanced_tactics
                    and logic.terran_common_unit(state)
                )
            ),
        ),
        make_location_data(
            SC2Mission.BROTHERS_IN_ARMS_T.mission_name,
            "South Science Facility",
            SC2_RACESWAP_LOC_ID_OFFSET + 11303,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_common_unit(state) and logic.terran_competent_comp(state)
            ),
        ),
        make_location_data(
            SC2Mission.BROTHERS_IN_ARMS_T.mission_name,
            "Raynor Forward Positions",
            SC2_RACESWAP_LOC_ID_OFFSET + 11304,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state) and logic.terran_competent_comp(state)
            ),
        ),
        make_location_data(
            SC2Mission.BROTHERS_IN_ARMS_T.mission_name,
            "Valerian Forward Positions",
            SC2_RACESWAP_LOC_ID_OFFSET + 11305,
            LocationType.EXTRA,
            lambda state: (
                logic.terran_common_unit(state) and logic.terran_competent_comp(state)
            ),
        ),
        make_location_data(
            SC2Mission.BROTHERS_IN_ARMS_T.mission_name,
            "Win in under 15 Minutes",
            SC2_RACESWAP_LOC_ID_OFFSET + 11306,
            LocationType.CHALLENGE,
            lambda state: (
                logic.terran_common_unit(state)
                and logic.terran_base_trasher(state)
                and logic.terran_power_rating(state) >= 8
            ),
            flags=LocationFlag.SPEEDRUN,
        ),
        make_location_data(
            SC2Mission.BROTHERS_IN_ARMS_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 11400,
            LocationType.VICTORY,
            logic.zerg_brothers_in_arms_requirement,
        ),
        make_location_data(
            SC2Mission.BROTHERS_IN_ARMS_Z.mission_name,
            "Mid Science Facility",
            SC2_RACESWAP_LOC_ID_OFFSET + 11401,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.BROTHERS_IN_ARMS_Z.mission_name,
            "North Science Facility",
            SC2_RACESWAP_LOC_ID_OFFSET + 11402,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_brothers_in_arms_requirement(state)
                or (
                    logic.take_over_ai_allies
                    and logic.advanced_tactics
                    and (
                        logic.zerg_common_unit(state) or logic.terran_common_unit(state)
                    )
                )
            ),
        ),
        make_location_data(
            SC2Mission.BROTHERS_IN_ARMS_Z.mission_name,
            "South Science Facility",
            SC2_RACESWAP_LOC_ID_OFFSET + 11403,
            LocationType.VANILLA,
            logic.zerg_brothers_in_arms_requirement,
        ),
        make_location_data(
            SC2Mission.BROTHERS_IN_ARMS_Z.mission_name,
            "Raynor Forward Positions",
            SC2_RACESWAP_LOC_ID_OFFSET + 11404,
            LocationType.EXTRA,
            logic.zerg_brothers_in_arms_requirement,
        ),
        make_location_data(
            SC2Mission.BROTHERS_IN_ARMS_Z.mission_name,
            "Valerian Forward Positions",
            SC2_RACESWAP_LOC_ID_OFFSET + 11405,
            LocationType.EXTRA,
            logic.zerg_brothers_in_arms_requirement,
        ),
        make_location_data(
            SC2Mission.BROTHERS_IN_ARMS_Z.mission_name,
            "Win in under 15 Minutes",
            SC2_RACESWAP_LOC_ID_OFFSET + 11406,
            LocationType.CHALLENGE,
            lambda state: (
                logic.zerg_brothers_in_arms_requirement(state)
                and logic.zerg_base_buster(state)
                and logic.zerg_power_rating(state) >= 8
            ),
            flags=LocationFlag.SPEEDRUN,
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 11500,
            LocationType.VICTORY,
            lambda state: (logic.terran_competent_comp(state)),
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH_T.mission_name,
            "Close Solarite Reserve",
            SC2_RACESWAP_LOC_ID_OFFSET + 11501,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH_T.mission_name,
            "North Solarite Reserve",
            SC2_RACESWAP_LOC_ID_OFFSET + 11502,
            LocationType.VANILLA,
            lambda state: (logic.terran_competent_comp(state)),
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH_T.mission_name,
            "East Solarite Reserve",
            SC2_RACESWAP_LOC_ID_OFFSET + 11503,
            LocationType.VANILLA,
            lambda state: (logic.terran_competent_comp(state)),
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH_T.mission_name,
            "West Launch Bay",
            SC2_RACESWAP_LOC_ID_OFFSET + 11504,
            LocationType.EXTRA,
            lambda state: (logic.terran_competent_comp(state)),
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH_T.mission_name,
            "South Launch Bay",
            SC2_RACESWAP_LOC_ID_OFFSET + 11505,
            LocationType.EXTRA,
            lambda state: (logic.terran_competent_comp(state)),
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH_T.mission_name,
            "Northwest Launch Bay",
            SC2_RACESWAP_LOC_ID_OFFSET + 11506,
            LocationType.EXTRA,
            lambda state: (logic.terran_competent_comp(state)),
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH_T.mission_name,
            "East Launch Bay",
            SC2_RACESWAP_LOC_ID_OFFSET + 11507,
            LocationType.EXTRA,
            lambda state: (logic.terran_competent_comp(state)),
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 11600,
            LocationType.VICTORY,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_basic_kerriganless_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH_Z.mission_name,
            "Close Solarite Reserve",
            SC2_RACESWAP_LOC_ID_OFFSET + 11601,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH_Z.mission_name,
            "North Solarite Reserve",
            SC2_RACESWAP_LOC_ID_OFFSET + 11602,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_basic_kerriganless_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH_Z.mission_name,
            "East Solarite Reserve",
            SC2_RACESWAP_LOC_ID_OFFSET + 11603,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_basic_kerriganless_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH_Z.mission_name,
            "West Launch Bay",
            SC2_RACESWAP_LOC_ID_OFFSET + 11604,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_basic_kerriganless_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH_Z.mission_name,
            "South Launch Bay",
            SC2_RACESWAP_LOC_ID_OFFSET + 11605,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_basic_kerriganless_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH_Z.mission_name,
            "Northwest Launch Bay",
            SC2_RACESWAP_LOC_ID_OFFSET + 11606,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_basic_kerriganless_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.AMON_S_REACH_Z.mission_name,
            "East Launch Bay",
            SC2_RACESWAP_LOC_ID_OFFSET + 11607,
            LocationType.EXTRA,
            lambda state: (
                logic.zerg_competent_comp(state)
                and logic.zerg_basic_kerriganless_anti_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.LAST_STAND_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 11700,
            LocationType.VICTORY,
            logic.terran_last_stand_requirement,
        ),
        make_location_data(
            SC2Mission.LAST_STAND_T.mission_name,
            "West Zenith Stone",
            SC2_RACESWAP_LOC_ID_OFFSET + 11701,
            LocationType.VANILLA,
            logic.terran_last_stand_requirement,
        ),
        make_location_data(
            SC2Mission.LAST_STAND_T.mission_name,
            "North Zenith Stone",
            SC2_RACESWAP_LOC_ID_OFFSET + 11702,
            LocationType.VANILLA,
            logic.terran_last_stand_requirement,
        ),
        make_location_data(
            SC2Mission.LAST_STAND_T.mission_name,
            "East Zenith Stone",
            SC2_RACESWAP_LOC_ID_OFFSET + 11703,
            LocationType.VANILLA,
            logic.terran_last_stand_requirement,
        ),
        make_location_data(
            SC2Mission.LAST_STAND_T.mission_name,
            "1 Billion Zerg",
            SC2_RACESWAP_LOC_ID_OFFSET + 11704,
            LocationType.EXTRA,
            logic.terran_last_stand_requirement,
        ),
        make_location_data(
            SC2Mission.LAST_STAND_T.mission_name,
            "1.5 Billion Zerg",
            SC2_RACESWAP_LOC_ID_OFFSET + 11705,
            LocationType.VANILLA,
            lambda state: logic.terran_last_stand_requirement(state)
            and logic.terran_defense_rating(state, True, True) >= 13,
        ),
        make_location_data(
            SC2Mission.LAST_STAND_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 11800,
            LocationType.VICTORY,
            logic.zerg_last_stand_requirement,
        ),
        make_location_data(
            SC2Mission.LAST_STAND_Z.mission_name,
            "West Zenith Stone",
            SC2_RACESWAP_LOC_ID_OFFSET + 11801,
            LocationType.VANILLA,
            logic.zerg_last_stand_requirement,
        ),
        make_location_data(
            SC2Mission.LAST_STAND_Z.mission_name,
            "North Zenith Stone",
            SC2_RACESWAP_LOC_ID_OFFSET + 11802,
            LocationType.VANILLA,
            logic.zerg_last_stand_requirement,
        ),
        make_location_data(
            SC2Mission.LAST_STAND_Z.mission_name,
            "East Zenith Stone",
            SC2_RACESWAP_LOC_ID_OFFSET + 11803,
            LocationType.VANILLA,
            logic.zerg_last_stand_requirement,
        ),
        make_location_data(
            SC2Mission.LAST_STAND_Z.mission_name,
            "1 Billion Zerg",
            SC2_RACESWAP_LOC_ID_OFFSET + 11804,
            LocationType.EXTRA,
            logic.zerg_last_stand_requirement,
        ),
        make_location_data(
            SC2Mission.LAST_STAND_Z.mission_name,
            "1.5 Billion Zerg",
            SC2_RACESWAP_LOC_ID_OFFSET + 11805,
            LocationType.VANILLA,
            logic.zerg_last_stand_requirement,
        ),
        make_location_data(
            SC2Mission.FORBIDDEN_WEAPON_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 11900,
            LocationType.VICTORY,
            logic.terran_beats_protoss_deathball,
        ),
        make_location_data(
            SC2Mission.FORBIDDEN_WEAPON_T.mission_name,
            "South Solarite",
            SC2_RACESWAP_LOC_ID_OFFSET + 11901,
            LocationType.VANILLA,
            logic.terran_beats_protoss_deathball,
        ),
        make_location_data(
            SC2Mission.FORBIDDEN_WEAPON_T.mission_name,
            "North Solarite",
            SC2_RACESWAP_LOC_ID_OFFSET + 11902,
            LocationType.VANILLA,
            logic.terran_beats_protoss_deathball,
        ),
        make_location_data(
            SC2Mission.FORBIDDEN_WEAPON_T.mission_name,
            "Northwest Solarite",
            SC2_RACESWAP_LOC_ID_OFFSET + 11903,
            LocationType.VANILLA,
            logic.terran_beats_protoss_deathball,
        ),
        make_location_data(
            SC2Mission.FORBIDDEN_WEAPON_T.mission_name,
            "Rescue Medics",
            SC2_RACESWAP_LOC_ID_OFFSET + 11904,
            LocationType.EXTRA,
            logic.terran_beats_protoss_deathball,
        ),
        make_location_data(
            SC2Mission.FORBIDDEN_WEAPON_T.mission_name,
            "Destroy Gateways",
            SC2_RACESWAP_LOC_ID_OFFSET + 11905,
            LocationType.CHALLENGE,
            logic.terran_beats_protoss_deathball,
        ),
        make_location_data(
            SC2Mission.FORBIDDEN_WEAPON_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 12000,
            LocationType.VICTORY,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.FORBIDDEN_WEAPON_Z.mission_name,
            "South Solarite",
            SC2_RACESWAP_LOC_ID_OFFSET + 12001,
            LocationType.VANILLA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.FORBIDDEN_WEAPON_Z.mission_name,
            "North Solarite",
            SC2_RACESWAP_LOC_ID_OFFSET + 12002,
            LocationType.VANILLA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.FORBIDDEN_WEAPON_Z.mission_name,
            "Northwest Solarite",
            SC2_RACESWAP_LOC_ID_OFFSET + 12003,
            LocationType.VANILLA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.FORBIDDEN_WEAPON_Z.mission_name,
            "Rescue Infested Medics",
            SC2_RACESWAP_LOC_ID_OFFSET + 12004,
            LocationType.EXTRA,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.FORBIDDEN_WEAPON_Z.mission_name,
            "Destroy Gateways",
            SC2_RACESWAP_LOC_ID_OFFSET + 12005,
            LocationType.CHALLENGE,
            logic.zerg_competent_comp_competent_aa,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 12100,
            LocationType.VICTORY,
            logic.terran_temple_of_unification_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION_T.mission_name,
            "Mid Celestial Lock",
            SC2_RACESWAP_LOC_ID_OFFSET + 12101,
            LocationType.EXTRA,
            logic.terran_temple_of_unification_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION_T.mission_name,
            "West Celestial Lock",
            SC2_RACESWAP_LOC_ID_OFFSET + 12102,
            LocationType.EXTRA,
            logic.terran_temple_of_unification_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION_T.mission_name,
            "South Celestial Lock",
            SC2_RACESWAP_LOC_ID_OFFSET + 12103,
            LocationType.EXTRA,
            logic.terran_temple_of_unification_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION_T.mission_name,
            "East Celestial Lock",
            SC2_RACESWAP_LOC_ID_OFFSET + 12104,
            LocationType.EXTRA,
            logic.terran_temple_of_unification_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION_T.mission_name,
            "North Celestial Lock",
            SC2_RACESWAP_LOC_ID_OFFSET + 12105,
            LocationType.EXTRA,
            logic.terran_temple_of_unification_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION_T.mission_name,
            "Titanic Warp Prism",
            SC2_RACESWAP_LOC_ID_OFFSET + 12106,
            LocationType.VANILLA,
            logic.terran_temple_of_unification_requirement,
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION_T.mission_name,
            "Terran Main Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 12107,
            LocationType.MASTERY,
            lambda state: (
                logic.terran_temple_of_unification_requirement(state)
                and logic.terran_base_trasher(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION_T.mission_name,
            "Protoss Main Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 12108,
            LocationType.MASTERY,
            lambda state: (
                logic.terran_temple_of_unification_requirement(state)
                and logic.terran_base_trasher(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 12200,
            LocationType.VICTORY,
            logic.zerg_temple_of_unification_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION_Z.mission_name,
            "Mid Celestial Lock",
            SC2_RACESWAP_LOC_ID_OFFSET + 12201,
            LocationType.EXTRA,
            logic.zerg_temple_of_unification_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION_Z.mission_name,
            "West Celestial Lock",
            SC2_RACESWAP_LOC_ID_OFFSET + 12202,
            LocationType.EXTRA,
            logic.zerg_temple_of_unification_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION_Z.mission_name,
            "South Celestial Lock",
            SC2_RACESWAP_LOC_ID_OFFSET + 12203,
            LocationType.EXTRA,
            logic.zerg_temple_of_unification_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION_Z.mission_name,
            "East Celestial Lock",
            SC2_RACESWAP_LOC_ID_OFFSET + 12204,
            LocationType.EXTRA,
            logic.zerg_temple_of_unification_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION_Z.mission_name,
            "North Celestial Lock",
            SC2_RACESWAP_LOC_ID_OFFSET + 12205,
            LocationType.EXTRA,
            logic.zerg_temple_of_unification_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION_Z.mission_name,
            "Titanic Warp Prism",
            SC2_RACESWAP_LOC_ID_OFFSET + 12206,
            LocationType.VANILLA,
            logic.zerg_temple_of_unification_requirement,
            hard_rule=logic.zerg_any_anti_air,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION_Z.mission_name,
            "Terran Main Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 12207,
            LocationType.MASTERY,
            lambda state: (
                logic.zerg_temple_of_unification_requirement(state)
                and logic.zerg_base_buster(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.TEMPLE_OF_UNIFICATION_Z.mission_name,
            "Protoss Main Base",
            SC2_RACESWAP_LOC_ID_OFFSET + 12208,
            LocationType.MASTERY,
            lambda state: (
                logic.zerg_temple_of_unification_requirement(state)
                and logic.zerg_base_buster(state)
            ),
            flags=LocationFlag.BASEBUST,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 12500,
            LocationType.VICTORY,
            logic.terran_harbinger_of_oblivion_requirement,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION_T.mission_name,
            "Artanis",
            SC2_RACESWAP_LOC_ID_OFFSET + 12501,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION_T.mission_name,
            "Northwest Void Crystal",
            SC2_RACESWAP_LOC_ID_OFFSET + 12502,
            LocationType.EXTRA,
            logic.terran_harbinger_of_oblivion_requirement,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION_T.mission_name,
            "Northeast Void Crystal",
            SC2_RACESWAP_LOC_ID_OFFSET + 12503,
            LocationType.EXTRA,
            logic.terran_harbinger_of_oblivion_requirement,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION_T.mission_name,
            "Southwest Void Crystal",
            SC2_RACESWAP_LOC_ID_OFFSET + 12504,
            LocationType.EXTRA,
            logic.terran_harbinger_of_oblivion_requirement,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION_T.mission_name,
            "Southeast Void Crystal",
            SC2_RACESWAP_LOC_ID_OFFSET + 12505,
            LocationType.EXTRA,
            logic.terran_harbinger_of_oblivion_requirement,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION_T.mission_name,
            "South Xel'Naga Vessel",
            SC2_RACESWAP_LOC_ID_OFFSET + 12506,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION_T.mission_name,
            "Mid Xel'Naga Vessel",
            SC2_RACESWAP_LOC_ID_OFFSET + 12507,
            LocationType.VANILLA,
            logic.terran_harbinger_of_oblivion_requirement,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION_T.mission_name,
            "North Xel'Naga Vessel",
            SC2_RACESWAP_LOC_ID_OFFSET + 12508,
            LocationType.VANILLA,
            logic.terran_harbinger_of_oblivion_requirement,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 12600,
            LocationType.VICTORY,
            logic.zerg_harbinger_of_oblivion_requirement,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION_Z.mission_name,
            "Artanis",
            SC2_RACESWAP_LOC_ID_OFFSET + 12601,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION_Z.mission_name,
            "Northwest Void Crystal",
            SC2_RACESWAP_LOC_ID_OFFSET + 12602,
            LocationType.EXTRA,
            logic.zerg_harbinger_of_oblivion_requirement,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION_Z.mission_name,
            "Northeast Void Crystal",
            SC2_RACESWAP_LOC_ID_OFFSET + 12603,
            LocationType.EXTRA,
            logic.zerg_harbinger_of_oblivion_requirement,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION_Z.mission_name,
            "Southwest Void Crystal",
            SC2_RACESWAP_LOC_ID_OFFSET + 12604,
            LocationType.EXTRA,
            logic.zerg_harbinger_of_oblivion_requirement,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION_Z.mission_name,
            "Southeast Void Crystal",
            SC2_RACESWAP_LOC_ID_OFFSET + 12605,
            LocationType.EXTRA,
            logic.zerg_harbinger_of_oblivion_requirement,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION_Z.mission_name,
            "South Xel'Naga Vessel",
            SC2_RACESWAP_LOC_ID_OFFSET + 12606,
            LocationType.VANILLA,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION_Z.mission_name,
            "Mid Xel'Naga Vessel",
            SC2_RACESWAP_LOC_ID_OFFSET + 12607,
            LocationType.VANILLA,
            logic.zerg_harbinger_of_oblivion_requirement,
        ),
        make_location_data(
            SC2Mission.HARBINGER_OF_OBLIVION_Z.mission_name,
            "North Xel'Naga Vessel",
            SC2_RACESWAP_LOC_ID_OFFSET + 12608,
            LocationType.VANILLA,
            logic.zerg_harbinger_of_oblivion_requirement,
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 12700,
            LocationType.VICTORY,
            logic.terran_unsealing_the_past_requirement,
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST_T.mission_name,
            "Zerg Cleared",
            SC2_RACESWAP_LOC_ID_OFFSET + 12701,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST_T.mission_name,
            "First Stasis Lock",
            SC2_RACESWAP_LOC_ID_OFFSET + 12702,
            LocationType.EXTRA,
            lambda state: (
                logic.advanced_tactics
                or logic.terran_unsealing_the_past_requirement(state)
            ),
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST_T.mission_name,
            "Second Stasis Lock",
            SC2_RACESWAP_LOC_ID_OFFSET + 12703,
            LocationType.EXTRA,
            logic.terran_unsealing_the_past_requirement,
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST_T.mission_name,
            "Third Stasis Lock",
            SC2_RACESWAP_LOC_ID_OFFSET + 12704,
            LocationType.EXTRA,
            logic.terran_unsealing_the_past_requirement,
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST_T.mission_name,
            "Fourth Stasis Lock",
            SC2_RACESWAP_LOC_ID_OFFSET + 12705,
            LocationType.EXTRA,
            logic.terran_unsealing_the_past_requirement,
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST_T.mission_name,
            "South Power Core",
            SC2_RACESWAP_LOC_ID_OFFSET + 12706,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_unsealing_the_past_requirement(state)
                and (
                    adv_tactics
                    or logic.terran_air(state)
                    or state.has_all(
                        {item_names.GOLIATH, item_names.GOLIATH_JUMP_JETS}, player
                    )
                )
            ),
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST_T.mission_name,
            "East Power Core",
            SC2_RACESWAP_LOC_ID_OFFSET + 12707,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_unsealing_the_past_requirement(state)
                and (
                    adv_tactics
                    or logic.terran_air(state)
                    or state.has_all(
                        {item_names.GOLIATH, item_names.GOLIATH_JUMP_JETS}, player
                    )
                )
            ),
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 12800,
            LocationType.VICTORY,
            logic.zerg_unsealing_the_past_requirement,
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST_Z.mission_name,
            "Zerg Cleared",
            SC2_RACESWAP_LOC_ID_OFFSET + 12801,
            LocationType.EXTRA,
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST_Z.mission_name,
            "First Stasis Lock",
            SC2_RACESWAP_LOC_ID_OFFSET + 12802,
            LocationType.EXTRA,
            lambda state: (
                logic.advanced_tactics
                or logic.zerg_unsealing_the_past_requirement(state)
            ),
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST_Z.mission_name,
            "Second Stasis Lock",
            SC2_RACESWAP_LOC_ID_OFFSET + 12803,
            LocationType.EXTRA,
            logic.zerg_unsealing_the_past_requirement,
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST_Z.mission_name,
            "Third Stasis Lock",
            SC2_RACESWAP_LOC_ID_OFFSET + 12804,
            LocationType.EXTRA,
            logic.zerg_unsealing_the_past_requirement,
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST_Z.mission_name,
            "Fourth Stasis Lock",
            SC2_RACESWAP_LOC_ID_OFFSET + 12805,
            LocationType.EXTRA,
            logic.zerg_unsealing_the_past_requirement,
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST_Z.mission_name,
            "South Power Core",
            SC2_RACESWAP_LOC_ID_OFFSET + 12806,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_unsealing_the_past_requirement(state)
                and (
                    adv_tactics
                    or (
                        state.has(item_names.MUTALISK, player)
                        or logic.morph_brood_lord(state)
                        or logic.morph_guardian(state)
                    )
                )
            ),
        ),
        make_location_data(
            SC2Mission.UNSEALING_THE_PAST_Z.mission_name,
            "East Power Core",
            SC2_RACESWAP_LOC_ID_OFFSET + 12807,
            LocationType.VANILLA,
            lambda state: (
                logic.zerg_unsealing_the_past_requirement(state)
                and (
                    adv_tactics
                    or (
                        state.has(item_names.MUTALISK, player)
                        or logic.morph_brood_lord(state)
                        or logic.morph_guardian(state)
                    )
                )
            ),
        ),
        make_location_data(
            SC2Mission.PURIFICATION_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 12900,
            LocationType.VICTORY,
            logic.terran_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_T.mission_name,
            "North Sector: West Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 12901,
            LocationType.VANILLA,
            logic.terran_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_T.mission_name,
            "North Sector: Northeast Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 12902,
            LocationType.EXTRA,
            logic.terran_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_T.mission_name,
            "North Sector: Southeast Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 12903,
            LocationType.EXTRA,
            logic.terran_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_T.mission_name,
            "South Sector: West Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 12904,
            LocationType.VANILLA,
            logic.terran_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_T.mission_name,
            "South Sector: North Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 12905,
            LocationType.EXTRA,
            logic.terran_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_T.mission_name,
            "South Sector: East Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 12906,
            LocationType.EXTRA,
            logic.terran_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_T.mission_name,
            "West Sector: West Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 12907,
            LocationType.VANILLA,
            logic.terran_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_T.mission_name,
            "West Sector: Mid Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 12908,
            LocationType.EXTRA,
            logic.terran_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_T.mission_name,
            "West Sector: East Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 12909,
            LocationType.EXTRA,
            logic.terran_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_T.mission_name,
            "East Sector: North Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 12910,
            LocationType.VANILLA,
            logic.terran_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_T.mission_name,
            "East Sector: West Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 12911,
            LocationType.EXTRA,
            logic.terran_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_T.mission_name,
            "East Sector: South Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 12912,
            LocationType.EXTRA,
            logic.terran_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_T.mission_name,
            "Purifier Warden",
            SC2_RACESWAP_LOC_ID_OFFSET + 12913,
            LocationType.VANILLA,
            logic.terran_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 13000,
            LocationType.VICTORY,
            logic.zerg_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_Z.mission_name,
            "North Sector: West Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 13001,
            LocationType.VANILLA,
            logic.zerg_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_Z.mission_name,
            "North Sector: Northeast Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 13002,
            LocationType.EXTRA,
            logic.zerg_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_Z.mission_name,
            "North Sector: Southeast Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 13003,
            LocationType.EXTRA,
            logic.zerg_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_Z.mission_name,
            "South Sector: West Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 13004,
            LocationType.VANILLA,
            logic.zerg_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_Z.mission_name,
            "South Sector: North Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 13005,
            LocationType.EXTRA,
            logic.zerg_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_Z.mission_name,
            "South Sector: East Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 13006,
            LocationType.EXTRA,
            logic.zerg_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_Z.mission_name,
            "West Sector: West Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 13007,
            LocationType.VANILLA,
            logic.zerg_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_Z.mission_name,
            "West Sector: Mid Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 13008,
            LocationType.EXTRA,
            logic.zerg_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_Z.mission_name,
            "West Sector: East Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 13009,
            LocationType.EXTRA,
            logic.zerg_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_Z.mission_name,
            "East Sector: North Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 13010,
            LocationType.VANILLA,
            logic.zerg_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_Z.mission_name,
            "East Sector: West Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 13011,
            LocationType.EXTRA,
            logic.zerg_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_Z.mission_name,
            "East Sector: South Null Circuit",
            SC2_RACESWAP_LOC_ID_OFFSET + 13012,
            LocationType.EXTRA,
            logic.zerg_purification_requirement,
        ),
        make_location_data(
            SC2Mission.PURIFICATION_Z.mission_name,
            "Purifier Warden",
            SC2_RACESWAP_LOC_ID_OFFSET + 13013,
            LocationType.VANILLA,
            logic.zerg_purification_requirement,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 13100,
            LocationType.VICTORY,
            logic.terran_steps_of_the_rite_requirement,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE_T.mission_name,
            "First Terrazine Fog",
            SC2_RACESWAP_LOC_ID_OFFSET + 13101,
            LocationType.EXTRA,
            logic.terran_steps_of_the_rite_requirement,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE_T.mission_name,
            "Southwest Guardian",
            SC2_RACESWAP_LOC_ID_OFFSET + 13102,
            LocationType.EXTRA,
            logic.terran_steps_of_the_rite_requirement,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE_T.mission_name,
            "West Guardian",
            SC2_RACESWAP_LOC_ID_OFFSET + 13103,
            LocationType.EXTRA,
            logic.terran_steps_of_the_rite_requirement,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE_T.mission_name,
            "Northwest Guardian",
            SC2_RACESWAP_LOC_ID_OFFSET + 13104,
            LocationType.EXTRA,
            logic.terran_steps_of_the_rite_requirement,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE_T.mission_name,
            "Northeast Guardian",
            SC2_RACESWAP_LOC_ID_OFFSET + 13105,
            LocationType.EXTRA,
            logic.terran_steps_of_the_rite_requirement,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE_T.mission_name,
            "North Mothership",
            SC2_RACESWAP_LOC_ID_OFFSET + 13106,
            LocationType.VANILLA,
            logic.terran_steps_of_the_rite_requirement,
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE_T.mission_name,
            "South Mothership",
            SC2_RACESWAP_LOC_ID_OFFSET + 13107,
            LocationType.VANILLA,
            logic.terran_steps_of_the_rite_requirement,
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 13200,
            LocationType.VICTORY,
            logic.zerg_steps_of_the_rite_requirement,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE_Z.mission_name,
            "First Terrazine Fog",
            SC2_RACESWAP_LOC_ID_OFFSET + 13201,
            LocationType.EXTRA,
            logic.zerg_steps_of_the_rite_requirement,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE_Z.mission_name,
            "Southwest Guardian",
            SC2_RACESWAP_LOC_ID_OFFSET + 13202,
            LocationType.EXTRA,
            logic.zerg_steps_of_the_rite_requirement,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE_Z.mission_name,
            "West Guardian",
            SC2_RACESWAP_LOC_ID_OFFSET + 13203,
            LocationType.EXTRA,
            logic.zerg_steps_of_the_rite_requirement,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE_Z.mission_name,
            "Northwest Guardian",
            SC2_RACESWAP_LOC_ID_OFFSET + 13204,
            LocationType.EXTRA,
            logic.zerg_steps_of_the_rite_requirement,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE_Z.mission_name,
            "Northeast Guardian",
            SC2_RACESWAP_LOC_ID_OFFSET + 13205,
            LocationType.EXTRA,
            logic.zerg_steps_of_the_rite_requirement,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE_Z.mission_name,
            "North Mothership",
            SC2_RACESWAP_LOC_ID_OFFSET + 13206,
            LocationType.VANILLA,
            logic.zerg_steps_of_the_rite_requirement,
            hard_rule=logic.zerg_any_anti_air,
        ),
        make_location_data(
            SC2Mission.STEPS_OF_THE_RITE_Z.mission_name,
            "South Mothership",
            SC2_RACESWAP_LOC_ID_OFFSET + 13207,
            LocationType.VANILLA,
            logic.zerg_steps_of_the_rite_requirement,
            hard_rule=logic.zerg_any_anti_air,
        ),
        make_location_data(
            SC2Mission.RAK_SHIR_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 13300,
            LocationType.VICTORY,
            logic.terran_rak_shir_requirement,
        ),
        make_location_data(
            SC2Mission.RAK_SHIR_T.mission_name,
            "North Slayn Elemental",
            SC2_RACESWAP_LOC_ID_OFFSET + 13301,
            LocationType.VANILLA,
            logic.terran_rak_shir_requirement,
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.RAK_SHIR_T.mission_name,
            "Southwest Slayn Elemental",
            SC2_RACESWAP_LOC_ID_OFFSET + 13302,
            LocationType.VANILLA,
            logic.terran_rak_shir_requirement,
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.RAK_SHIR_T.mission_name,
            "East Slayn Elemental",
            SC2_RACESWAP_LOC_ID_OFFSET + 13303,
            LocationType.VANILLA,
            logic.terran_rak_shir_requirement,
            hard_rule=logic.terran_any_anti_air,
        ),
        make_location_data(
            SC2Mission.RAK_SHIR_T.mission_name,
            "Resource Pickups",
            SC2_RACESWAP_LOC_ID_OFFSET + 13304,
            LocationType.EXTRA,
            logic.terran_rak_shir_requirement,
        ),
        make_location_data(
            SC2Mission.RAK_SHIR_T.mission_name,
            "Destroy Nexuses",
            SC2_RACESWAP_LOC_ID_OFFSET + 13305,
            LocationType.CHALLENGE,
            logic.terran_rak_shir_requirement,
        ),
        make_location_data(
            SC2Mission.RAK_SHIR_T.mission_name,
            "Win in under 15 minutes",
            SC2_RACESWAP_LOC_ID_OFFSET + 13306,
            LocationType.MASTERY,
            logic.terran_rak_shir_requirement,
            flags=LocationFlag.SPEEDRUN,
        ),
        make_location_data(
            SC2Mission.RAK_SHIR_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 13400,
            LocationType.VICTORY,
            logic.zerg_rak_shir_requirement,
        ),
        make_location_data(
            SC2Mission.RAK_SHIR_Z.mission_name,
            "North Slayn Elemental",
            SC2_RACESWAP_LOC_ID_OFFSET + 13401,
            LocationType.VANILLA,
            logic.zerg_rak_shir_requirement,
            hard_rule=logic.zerg_any_anti_air,
        ),
        make_location_data(
            SC2Mission.RAK_SHIR_Z.mission_name,
            "Southwest Slayn Elemental",
            SC2_RACESWAP_LOC_ID_OFFSET + 13402,
            LocationType.VANILLA,
            logic.zerg_rak_shir_requirement,
            hard_rule=logic.zerg_any_anti_air,
        ),
        make_location_data(
            SC2Mission.RAK_SHIR_Z.mission_name,
            "East Slayn Elemental",
            SC2_RACESWAP_LOC_ID_OFFSET + 13403,
            LocationType.VANILLA,
            logic.zerg_rak_shir_requirement,
            hard_rule=logic.zerg_any_anti_air,
        ),
        make_location_data(
            SC2Mission.RAK_SHIR_Z.mission_name,
            "Resource Pickups",
            SC2_RACESWAP_LOC_ID_OFFSET + 13404,
            LocationType.EXTRA,
            logic.zerg_rak_shir_requirement,
        ),
        make_location_data(
            SC2Mission.RAK_SHIR_Z.mission_name,
            "Destroy Nexuses",
            SC2_RACESWAP_LOC_ID_OFFSET + 13405,
            LocationType.CHALLENGE,
            logic.zerg_rak_shir_requirement,
        ),
        make_location_data(
            SC2Mission.RAK_SHIR_Z.mission_name,
            "Win in under 15 minutes",
            SC2_RACESWAP_LOC_ID_OFFSET + 13406,
            LocationType.MASTERY,
            logic.zerg_rak_shir_requirement,
            flags=LocationFlag.SPEEDRUN,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_CHARGE_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 13500,
            LocationType.VICTORY,
            logic.terran_templars_charge_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_CHARGE_T.mission_name,
            "Northwest Power Core",
            SC2_RACESWAP_LOC_ID_OFFSET + 13501,
            LocationType.EXTRA,
            logic.terran_templars_charge_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_CHARGE_T.mission_name,
            "Northeast Power Core",
            SC2_RACESWAP_LOC_ID_OFFSET + 13502,
            LocationType.EXTRA,
            logic.terran_templars_charge_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_CHARGE_T.mission_name,
            "Southeast Power Core",
            SC2_RACESWAP_LOC_ID_OFFSET + 13503,
            LocationType.EXTRA,
            logic.terran_templars_charge_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_CHARGE_T.mission_name,
            "West Hybrid Stasis Chamber",
            SC2_RACESWAP_LOC_ID_OFFSET + 13504,
            LocationType.VANILLA,
            logic.terran_templars_charge_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_CHARGE_T.mission_name,
            "Southeast Hybrid Stasis Chamber",
            SC2_RACESWAP_LOC_ID_OFFSET + 13505,
            LocationType.VANILLA,
            lambda state: (
                logic.terran_templars_charge_requirement(state)
                and logic.terran_air(state)
            ),
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_CHARGE_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 13600,
            LocationType.VICTORY,
            logic.zerg_templars_charge_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_CHARGE_Z.mission_name,
            "Northwest Power Core",
            SC2_RACESWAP_LOC_ID_OFFSET + 13601,
            LocationType.EXTRA,
            logic.zerg_templars_charge_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_CHARGE_Z.mission_name,
            "Northeast Power Core",
            SC2_RACESWAP_LOC_ID_OFFSET + 13602,
            LocationType.EXTRA,
            logic.zerg_templars_charge_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_CHARGE_Z.mission_name,
            "Southeast Power Core",
            SC2_RACESWAP_LOC_ID_OFFSET + 13603,
            LocationType.EXTRA,
            logic.zerg_templars_charge_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_CHARGE_Z.mission_name,
            "West Hybrid Stasis Chamber",
            SC2_RACESWAP_LOC_ID_OFFSET + 13604,
            LocationType.VANILLA,
            logic.zerg_templars_charge_requirement,
        ),
        make_location_data(
            SC2Mission.TEMPLAR_S_CHARGE_Z.mission_name,
            "Southeast Hybrid Stasis Chamber",
            SC2_RACESWAP_LOC_ID_OFFSET + 13605,
            LocationType.VANILLA,
            logic.zerg_templars_charge_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 13900,
            LocationType.VICTORY,
            logic.terran_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST_T.mission_name,
            "Southeast Void Shard",
            SC2_RACESWAP_LOC_ID_OFFSET + 13901,
            LocationType.EXTRA,
            logic.terran_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST_T.mission_name,
            "South Void Shard",
            SC2_RACESWAP_LOC_ID_OFFSET + 13902,
            LocationType.EXTRA,
            logic.terran_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST_T.mission_name,
            "Southwest Void Shard",
            SC2_RACESWAP_LOC_ID_OFFSET + 13903,
            LocationType.EXTRA,
            logic.terran_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST_T.mission_name,
            "North Void Shard",
            SC2_RACESWAP_LOC_ID_OFFSET + 13904,
            LocationType.EXTRA,
            logic.terran_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST_T.mission_name,
            "Northwest Void Shard",
            SC2_RACESWAP_LOC_ID_OFFSET + 13905,
            LocationType.EXTRA,
            logic.terran_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST_T.mission_name,
            "Nerazim Warp in Zone",
            SC2_RACESWAP_LOC_ID_OFFSET + 13906,
            LocationType.VANILLA,
            logic.terran_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST_T.mission_name,
            "Tal'darim Warp in Zone",
            SC2_RACESWAP_LOC_ID_OFFSET + 13907,
            LocationType.VANILLA,
            logic.terran_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST_T.mission_name,
            "Purifier Warp in Zone",
            SC2_RACESWAP_LOC_ID_OFFSET + 13908,
            LocationType.VANILLA,
            logic.terran_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 14000,
            LocationType.VICTORY,
            logic.zerg_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST_Z.mission_name,
            "Southeast Void Shard",
            SC2_RACESWAP_LOC_ID_OFFSET + 14001,
            LocationType.EXTRA,
            logic.zerg_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST_Z.mission_name,
            "South Void Shard",
            SC2_RACESWAP_LOC_ID_OFFSET + 14002,
            LocationType.EXTRA,
            logic.zerg_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST_Z.mission_name,
            "Southwest Void Shard",
            SC2_RACESWAP_LOC_ID_OFFSET + 14003,
            LocationType.EXTRA,
            logic.zerg_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST_Z.mission_name,
            "North Void Shard",
            SC2_RACESWAP_LOC_ID_OFFSET + 14004,
            LocationType.EXTRA,
            logic.zerg_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST_Z.mission_name,
            "Northwest Void Shard",
            SC2_RACESWAP_LOC_ID_OFFSET + 14005,
            LocationType.EXTRA,
            logic.zerg_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST_Z.mission_name,
            "Nerazim Warp in Zone",
            SC2_RACESWAP_LOC_ID_OFFSET + 14006,
            LocationType.VANILLA,
            logic.zerg_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST_Z.mission_name,
            "Tal'darim Warp in Zone",
            SC2_RACESWAP_LOC_ID_OFFSET + 14007,
            LocationType.VANILLA,
            logic.zerg_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.THE_HOST_Z.mission_name,
            "Purifier Warp in Zone",
            SC2_RACESWAP_LOC_ID_OFFSET + 14008,
            LocationType.VANILLA,
            logic.zerg_the_host_requirement,
        ),
        make_location_data(
            SC2Mission.SALVATION_T.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 14100,
            LocationType.VICTORY,
            logic.terran_salvation_requirement,
        ),
        make_location_data(
            SC2Mission.SALVATION_T.mission_name,
            "Fabrication Matrix",
            SC2_RACESWAP_LOC_ID_OFFSET + 14101,
            LocationType.EXTRA,
            logic.terran_salvation_requirement,
        ),
        make_location_data(
            SC2Mission.SALVATION_T.mission_name,
            "Assault Cluster",
            SC2_RACESWAP_LOC_ID_OFFSET + 14102,
            LocationType.EXTRA,
            logic.terran_salvation_requirement,
        ),
        make_location_data(
            SC2Mission.SALVATION_T.mission_name,
            "Hull Breach",
            SC2_RACESWAP_LOC_ID_OFFSET + 14103,
            LocationType.EXTRA,
            logic.terran_salvation_requirement,
        ),
        make_location_data(
            SC2Mission.SALVATION_T.mission_name,
            "Core Critical",
            SC2_RACESWAP_LOC_ID_OFFSET + 14104,
            LocationType.EXTRA,
            logic.terran_salvation_requirement,
        ),
        make_location_data(
            SC2Mission.SALVATION_T.mission_name,
            "Kill Brutalisk",
            SC2_RACESWAP_LOC_ID_OFFSET + 14105,
            LocationType.MASTERY,
            logic.terran_salvation_requirement,
        ),
        make_location_data(
            SC2Mission.SALVATION_Z.mission_name,
            "Victory",
            SC2_RACESWAP_LOC_ID_OFFSET + 14200,
            LocationType.VICTORY,
            logic.zerg_salvation_requirement,
        ),
        make_location_data(
            SC2Mission.SALVATION_Z.mission_name,
            "Fabrication Matrix",
            SC2_RACESWAP_LOC_ID_OFFSET + 14201,
            LocationType.EXTRA,
            logic.zerg_salvation_requirement,
        ),
        make_location_data(
            SC2Mission.SALVATION_Z.mission_name,
            "Assault Cluster",
            SC2_RACESWAP_LOC_ID_OFFSET + 14202,
            LocationType.EXTRA,
            logic.zerg_salvation_requirement,
        ),
        make_location_data(
            SC2Mission.SALVATION_Z.mission_name,
            "Hull Breach",
            SC2_RACESWAP_LOC_ID_OFFSET + 14203,
            LocationType.EXTRA,
            logic.zerg_salvation_requirement,
        ),
        make_location_data(
            SC2Mission.SALVATION_Z.mission_name,
            "Core Critical",
            SC2_RACESWAP_LOC_ID_OFFSET + 14204,
            LocationType.EXTRA,
            logic.zerg_salvation_requirement,
        ),
        make_location_data(
            SC2Mission.SALVATION_Z.mission_name,
            "Kill Brutalisk",
            SC2_RACESWAP_LOC_ID_OFFSET + 14205,
            LocationType.MASTERY,
            logic.zerg_salvation_requirement,
        ),
    ]

    # Filtering out excluded locations
    if world is not None:
        excluded_location_types = get_location_types(
            world, LocationInclusion.option_disabled
        )
        excluded_location_flags = get_location_flags(
            world, LocationInclusion.option_disabled
        )
        chance_location_types = get_location_types(
            world, LocationInclusion.option_half_chance
        )
        chance_location_flags = get_location_flags(
            world, LocationInclusion.option_half_chance
        )
        plando_locations = get_plando_locations(world)
        exclude_locations = world.options.exclude_locations.value

        def include_location(location: LocationData) -> bool:
            if location.type is LocationType.VICTORY:
                return True
            if location.name in plando_locations:
                return True
            if location.name in exclude_locations:
                return False
            if location.flags & excluded_location_flags:
                return False
            if location.type in excluded_location_types:
                return False
            if location.flags & chance_location_flags:
                if world.random.random() < 0.5:
                    return False
            if location.type in chance_location_types:
                if world.random.random() < 0.5:
                    return False
            return True

        location_table = [
            location for location in location_table if include_location(location)
        ]
    beat_events: List[LocationData] = []
    victory_caches: List[LocationData] = []
    VICTORY_CACHE_SIZE = 10
    for location_data in location_table:
        # Generating Beat event and Victory Cache locations
        if location_data.type == LocationType.VICTORY:
            beat_events.append(
                location_data._replace(name="Beat " + location_data.region, code=None)  # type: ignore
            )
            for v in range(VICTORY_CACHE_SIZE):
                victory_caches.append(
                    location_data._replace(
                        name=location_data.name + f" Cache ({v + 1})",
                        code=location_data.code + VICTORY_CACHE_OFFSET + v,
                        type=LocationType.VICTORY_CACHE,
                    )
                )

    return tuple(location_table + beat_events + victory_caches)


DEFAULT_LOCATION_LIST = get_locations(None)
"""A location table with `None` as the input world; does not contain logic rules"""

lookup_location_id_to_type = {
    loc.code: loc.type for loc in DEFAULT_LOCATION_LIST if loc.code is not None
}
lookup_location_id_to_flags = {
    loc.code: loc.flags for loc in DEFAULT_LOCATION_LIST if loc.code is not None
}
