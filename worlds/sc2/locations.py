from enum import IntEnum
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


class LocationType(IntEnum):
    VICTORY = 0  # Winning a mission
    VANILLA = 1  # Objectives that provided metaprogression in the original campaign, along with a few other locations for a balanced experience
    EXTRA = 2  # Additional locations based on mission progression, collecting in-mission rewards, etc. that do not significantly increase the challenge.
    CHALLENGE = 3  # Challenging objectives, often harder than just completing a mission, and often associated with Achievements
    MASTERY = 4  # Extremely challenging objectives often associated with Masteries and Feats of Strength in the original campaign


class LocationData(NamedTuple):
    region: str
    name: str
    code: int
    type: LocationType
    rule: Callable[['CollectionState'], bool] = Location.access_rule


def get_location_types(world: 'SC2World', inclusion_type: int) -> Set[LocationType]:
    """

    :param multiworld:
    :param player:
    :param inclusion_type: Level of inclusion to check for
    :return: A list of location types that match the inclusion type
    """
    exclusion_options = [
        ("vanilla_locations", LocationType.VANILLA),
        ("extra_locations", LocationType.EXTRA),
        ("challenge_locations", LocationType.CHALLENGE),
        ("mastery_locations", LocationType.MASTERY)
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
        LocationData(SC2Mission.LIBERATION_DAY.mission_name, "Liberation Day: Victory", SC2WOL_LOC_ID_OFFSET + 100, LocationType.VICTORY),
        LocationData(SC2Mission.LIBERATION_DAY.mission_name, "Liberation Day: First Statue", SC2WOL_LOC_ID_OFFSET + 101, LocationType.VANILLA),
        LocationData(SC2Mission.LIBERATION_DAY.mission_name, "Liberation Day: Second Statue", SC2WOL_LOC_ID_OFFSET + 102, LocationType.VANILLA),
        LocationData(SC2Mission.LIBERATION_DAY.mission_name, "Liberation Day: Third Statue", SC2WOL_LOC_ID_OFFSET + 103, LocationType.VANILLA),
        LocationData(SC2Mission.LIBERATION_DAY.mission_name, "Liberation Day: Fourth Statue", SC2WOL_LOC_ID_OFFSET + 104, LocationType.VANILLA),
        LocationData(SC2Mission.LIBERATION_DAY.mission_name, "Liberation Day: Fifth Statue", SC2WOL_LOC_ID_OFFSET + 105, LocationType.VANILLA),
        LocationData(SC2Mission.LIBERATION_DAY.mission_name, "Liberation Day: Sixth Statue", SC2WOL_LOC_ID_OFFSET + 106, LocationType.VANILLA),
        LocationData(SC2Mission.LIBERATION_DAY.mission_name, "Liberation Day: Special Delivery", SC2WOL_LOC_ID_OFFSET + 107, LocationType.EXTRA),
        LocationData(SC2Mission.LIBERATION_DAY.mission_name, "Liberation Day: Transport", SC2WOL_LOC_ID_OFFSET + 108, LocationType.EXTRA),
        LocationData(SC2Mission.THE_OUTLAWS.mission_name, "The Outlaws (Terran): Victory", SC2WOL_LOC_ID_OFFSET + 200, LocationType.VICTORY,
                     lambda state: logic.terran_early_tech(state)),
        LocationData(SC2Mission.THE_OUTLAWS.mission_name, "The Outlaws (Terran): Rebel Base", SC2WOL_LOC_ID_OFFSET + 201, LocationType.VANILLA,
                     lambda state: logic.terran_early_tech(state)),
        LocationData(SC2Mission.THE_OUTLAWS.mission_name, "The Outlaws (Terran): North Resource Pickups", SC2WOL_LOC_ID_OFFSET + 202, LocationType.EXTRA,
                     lambda state: logic.terran_early_tech(state)),
        LocationData(SC2Mission.THE_OUTLAWS.mission_name, "The Outlaws (Terran): Bunker", SC2WOL_LOC_ID_OFFSET + 203, LocationType.VANILLA,
                     lambda state: logic.terran_early_tech(state)),
        LocationData(SC2Mission.THE_OUTLAWS.mission_name, "The Outlaws (Terran): Close Resource Pickups", SC2WOL_LOC_ID_OFFSET + 204, LocationType.EXTRA),
        LocationData(SC2Mission.ZERO_HOUR.mission_name, "Zero Hour (Terran): Victory", SC2WOL_LOC_ID_OFFSET + 300, LocationType.VICTORY,
                     lambda state: logic.terran_common_unit(state) and
                                   logic.terran_defense_rating(state, True) >= 2 and
                                   (adv_tactics or logic.terran_basic_anti_air(state))),
        LocationData(SC2Mission.ZERO_HOUR.mission_name, "Zero Hour (Terran): First Group Rescued", SC2WOL_LOC_ID_OFFSET + 301, LocationType.VANILLA),
        LocationData(SC2Mission.ZERO_HOUR.mission_name, "Zero Hour (Terran): Second Group Rescued", SC2WOL_LOC_ID_OFFSET + 302, LocationType.VANILLA,
                     lambda state: logic.terran_common_unit(state)),
        LocationData(SC2Mission.ZERO_HOUR.mission_name, "Zero Hour (Terran): Third Group Rescued", SC2WOL_LOC_ID_OFFSET + 303, LocationType.VANILLA,
                     lambda state: logic.terran_common_unit(state) and
                                   logic.terran_defense_rating(state, True) >= 2),
        LocationData(SC2Mission.ZERO_HOUR.mission_name, "Zero Hour (Terran): First Hatchery", SC2WOL_LOC_ID_OFFSET + 304, LocationType.CHALLENGE,
                     lambda state: logic.terran_competent_comp(state)),
        LocationData(SC2Mission.ZERO_HOUR.mission_name, "Zero Hour (Terran): Second Hatchery", SC2WOL_LOC_ID_OFFSET + 305, LocationType.CHALLENGE,
                     lambda state: logic.terran_competent_comp(state)),
        LocationData(SC2Mission.ZERO_HOUR.mission_name, "Zero Hour (Terran): Third Hatchery", SC2WOL_LOC_ID_OFFSET + 306, LocationType.CHALLENGE,
                     lambda state: logic.terran_competent_comp(state)),
        LocationData(SC2Mission.ZERO_HOUR.mission_name, "Zero Hour (Terran): Fourth Hatchery", SC2WOL_LOC_ID_OFFSET + 307, LocationType.CHALLENGE,
                     lambda state: logic.terran_competent_comp(state)),
        LocationData(SC2Mission.ZERO_HOUR.mission_name, "Zero Hour (Terran): Ride's on its Way", SC2WOL_LOC_ID_OFFSET + 308, LocationType.EXTRA,
                     lambda state: logic.terran_common_unit(state)),
        LocationData(SC2Mission.ZERO_HOUR.mission_name, "Zero Hour (Terran): Hold Just a Little Longer", SC2WOL_LOC_ID_OFFSET + 309, LocationType.EXTRA,
                     lambda state: logic.terran_common_unit(state) and
                                   logic.terran_defense_rating(state, True) >= 2),
        LocationData(SC2Mission.ZERO_HOUR.mission_name, "Zero Hour (Terran): Cavalry's on the Way", SC2WOL_LOC_ID_OFFSET + 310, LocationType.EXTRA,
                     lambda state: logic.terran_common_unit(state) and
                                   logic.terran_defense_rating(state, True) >= 2),
        LocationData(SC2Mission.EVACUATION.mission_name, "Evacuation: Victory", SC2WOL_LOC_ID_OFFSET + 400, LocationType.VICTORY,
                     lambda state: logic.terran_early_tech(state) and
                                   (adv_tactics and logic.terran_basic_anti_air(state)
                                    or logic.terran_competent_anti_air(state))),
        LocationData(SC2Mission.EVACUATION.mission_name, "Evacuation: North Chrysalis", SC2WOL_LOC_ID_OFFSET + 401, LocationType.VANILLA),
        LocationData(SC2Mission.EVACUATION.mission_name, "Evacuation: West Chrysalis", SC2WOL_LOC_ID_OFFSET + 402, LocationType.VANILLA,
                     lambda state: logic.terran_early_tech(state)),
        LocationData(SC2Mission.EVACUATION.mission_name, "Evacuation: East Chrysalis", SC2WOL_LOC_ID_OFFSET + 403, LocationType.VANILLA,
                     lambda state: logic.terran_early_tech(state)),
        LocationData(SC2Mission.EVACUATION.mission_name, "Evacuation: Reach Hanson", SC2WOL_LOC_ID_OFFSET + 404, LocationType.EXTRA),
        LocationData(SC2Mission.EVACUATION.mission_name, "Evacuation: Secret Resource Stash", SC2WOL_LOC_ID_OFFSET + 405, LocationType.EXTRA),
        LocationData(SC2Mission.EVACUATION.mission_name, "Evacuation: Flawless", SC2WOL_LOC_ID_OFFSET + 406, LocationType.CHALLENGE,
                     lambda state: logic.terran_early_tech(state) and
                                   logic.terran_defense_rating(state, True, False) >= 2 and
                                   (adv_tactics and logic.terran_basic_anti_air(state)
                                    or logic.terran_competent_anti_air(state))),
        LocationData(SC2Mission.OUTBREAK.mission_name, "Outbreak: Victory", SC2WOL_LOC_ID_OFFSET + 500, LocationType.VICTORY,
                     lambda state: logic.terran_defense_rating(state, True, False) >= 4 and
                                   (logic.terran_common_unit(state) or state.has(item_names.REAPER, player))),
        LocationData(SC2Mission.OUTBREAK.mission_name, "Outbreak: Left Infestor", SC2WOL_LOC_ID_OFFSET + 501, LocationType.VANILLA,
                     lambda state: logic.terran_defense_rating(state, True, False) >= 2 and
                                   (logic.terran_common_unit(state) or state.has(item_names.REAPER, player))),
        LocationData(SC2Mission.OUTBREAK.mission_name, "Outbreak: Right Infestor", SC2WOL_LOC_ID_OFFSET + 502, LocationType.VANILLA,
                     lambda state: logic.terran_defense_rating(state, True, False) >= 2 and
                                   (logic.terran_common_unit(state) or state.has(item_names.REAPER, player))),
        LocationData(SC2Mission.OUTBREAK.mission_name, "Outbreak: North Infested Command Center", SC2WOL_LOC_ID_OFFSET + 503, LocationType.EXTRA,
                     lambda state: logic.terran_defense_rating(state, True, False) >= 2 and
                                   (logic.terran_common_unit(state) or state.has(item_names.REAPER, player))),
        LocationData(SC2Mission.OUTBREAK.mission_name, "Outbreak: South Infested Command Center", SC2WOL_LOC_ID_OFFSET + 504, LocationType.EXTRA,
                     lambda state: logic.terran_defense_rating(state, True, False) >= 2 and
                                   (logic.terran_common_unit(state) or state.has(item_names.REAPER, player))),
        LocationData(SC2Mission.OUTBREAK.mission_name, "Outbreak: Northwest Bar", SC2WOL_LOC_ID_OFFSET + 505, LocationType.EXTRA,
                     lambda state: logic.terran_defense_rating(state, True, False) >= 2 and
                                   (logic.terran_common_unit(state) or state.has(item_names.REAPER, player))),
        LocationData(SC2Mission.OUTBREAK.mission_name, "Outbreak: North Bar", SC2WOL_LOC_ID_OFFSET + 506, LocationType.EXTRA,
                     lambda state: logic.terran_defense_rating(state, True, False) >= 2 and
                                   (logic.terran_common_unit(state) or state.has(item_names.REAPER, player))),
        LocationData(SC2Mission.OUTBREAK.mission_name, "Outbreak: South Bar", SC2WOL_LOC_ID_OFFSET + 507, LocationType.EXTRA,
                     lambda state: logic.terran_defense_rating(state, True, False) >= 2 and
                                   (logic.terran_common_unit(state) or state.has(item_names.REAPER, player))),
        LocationData(SC2Mission.SAFE_HAVEN.mission_name, "Safe Haven: Victory", SC2WOL_LOC_ID_OFFSET + 600, LocationType.VICTORY,
                     lambda state: logic.terran_common_unit(state) and
                                   logic.terran_competent_anti_air(state)),
        LocationData(SC2Mission.SAFE_HAVEN.mission_name, "Safe Haven: North Nexus", SC2WOL_LOC_ID_OFFSET + 601, LocationType.EXTRA,
                     lambda state: logic.terran_common_unit(state) and
                                   logic.terran_competent_anti_air(state)),
        LocationData(SC2Mission.SAFE_HAVEN.mission_name, "Safe Haven: East Nexus", SC2WOL_LOC_ID_OFFSET + 602, LocationType.EXTRA,
                     lambda state: logic.terran_common_unit(state) and
                                   logic.terran_competent_anti_air(state)),
        LocationData(SC2Mission.SAFE_HAVEN.mission_name, "Safe Haven: South Nexus", SC2WOL_LOC_ID_OFFSET + 603, LocationType.EXTRA,
                     lambda state: logic.terran_common_unit(state) and
                                   logic.terran_competent_anti_air(state)),
        LocationData(SC2Mission.SAFE_HAVEN.mission_name, "Safe Haven: First Terror Fleet", SC2WOL_LOC_ID_OFFSET + 604, LocationType.VANILLA,
                     lambda state: logic.terran_common_unit(state) and
                                   logic.terran_competent_anti_air(state)),
        LocationData(SC2Mission.SAFE_HAVEN.mission_name, "Safe Haven: Second Terror Fleet", SC2WOL_LOC_ID_OFFSET + 605, LocationType.VANILLA,
                     lambda state: logic.terran_common_unit(state) and
                                   logic.terran_competent_anti_air(state)),
        LocationData(SC2Mission.SAFE_HAVEN.mission_name, "Safe Haven: Third Terror Fleet", SC2WOL_LOC_ID_OFFSET + 606, LocationType.VANILLA,
                     lambda state: logic.terran_common_unit(state) and
                                   logic.terran_competent_anti_air(state)),
        LocationData(SC2Mission.HAVENS_FALL.mission_name, "Haven's Fall: Victory", SC2WOL_LOC_ID_OFFSET + 700, LocationType.VICTORY,
                     lambda state: logic.terran_common_unit(state) and
                                   logic.terran_competent_anti_air(state) and
                                   logic.terran_defense_rating(state, True) >= 3),
        LocationData(SC2Mission.HAVENS_FALL.mission_name, "Haven's Fall: North Hive", SC2WOL_LOC_ID_OFFSET + 701, LocationType.VANILLA,
                     lambda state: logic.terran_common_unit(state) and
                                   logic.terran_competent_anti_air(state) and
                                   logic.terran_defense_rating(state, True) >= 3),
        LocationData(SC2Mission.HAVENS_FALL.mission_name, "Haven's Fall: East Hive", SC2WOL_LOC_ID_OFFSET + 702, LocationType.VANILLA,
                     lambda state: logic.terran_common_unit(state) and
                                   logic.terran_competent_anti_air(state) and
                                   logic.terran_defense_rating(state, True) >= 3),
        LocationData(SC2Mission.HAVENS_FALL.mission_name, "Haven's Fall: South Hive", SC2WOL_LOC_ID_OFFSET + 703, LocationType.VANILLA,
                     lambda state: logic.terran_common_unit(state) and
                                   logic.terran_competent_anti_air(state) and
                                   logic.terran_defense_rating(state, True) >= 3),
        LocationData(SC2Mission.HAVENS_FALL.mission_name, "Haven's Fall: Northeast Colony Base", SC2WOL_LOC_ID_OFFSET + 704, LocationType.CHALLENGE,
                     lambda state: logic.terran_respond_to_colony_infestations(state)),
        LocationData(SC2Mission.HAVENS_FALL.mission_name, "Haven's Fall: East Colony Base", SC2WOL_LOC_ID_OFFSET + 705, LocationType.CHALLENGE,
                     lambda state: logic.terran_respond_to_colony_infestations(state)),
        LocationData(SC2Mission.HAVENS_FALL.mission_name, "Haven's Fall: Middle Colony Base", SC2WOL_LOC_ID_OFFSET + 706, LocationType.CHALLENGE,
                     lambda state: logic.terran_respond_to_colony_infestations(state)),
        LocationData(SC2Mission.HAVENS_FALL.mission_name, "Haven's Fall: Southeast Colony Base", SC2WOL_LOC_ID_OFFSET + 707, LocationType.CHALLENGE,
                     lambda state: logic.terran_respond_to_colony_infestations(state)),
        LocationData(SC2Mission.HAVENS_FALL.mission_name, "Haven's Fall: Southwest Colony Base", SC2WOL_LOC_ID_OFFSET + 708, LocationType.CHALLENGE,
                     lambda state: logic.terran_respond_to_colony_infestations(state)),
        LocationData(SC2Mission.HAVENS_FALL.mission_name, "Haven's Fall: Southwest Gas Pickups", SC2WOL_LOC_ID_OFFSET + 709, LocationType.EXTRA,
                     lambda state: logic.terran_common_unit(state) and
                                   logic.terran_competent_anti_air(state) and
                                   logic.terran_defense_rating(state, True) >= 3),
        LocationData(SC2Mission.HAVENS_FALL.mission_name, "Haven's Fall: East Gas Pickups", SC2WOL_LOC_ID_OFFSET + 710, LocationType.EXTRA,
                     lambda state: logic.terran_common_unit(state) and
                                   logic.terran_competent_anti_air(state) and
                                   logic.terran_defense_rating(state, True) >= 3),
        LocationData(SC2Mission.HAVENS_FALL.mission_name, "Haven's Fall: Southeast Gas Pickups", SC2WOL_LOC_ID_OFFSET + 711, LocationType.EXTRA,
                     lambda state: logic.terran_common_unit(state) and
                                   logic.terran_competent_anti_air(state) and
                                   logic.terran_defense_rating(state, True) >= 3),
        LocationData(SC2Mission.SMASH_AND_GRAB.mission_name, "Smash and Grab (Terran): Victory", SC2WOL_LOC_ID_OFFSET + 800, LocationType.VICTORY,
                     lambda state: logic.terran_common_unit(state) and
                                   (adv_tactics and logic.terran_basic_anti_air(state)
                                    or logic.terran_competent_anti_air(state))),
        LocationData(SC2Mission.SMASH_AND_GRAB.mission_name, "Smash and Grab (Terran): First Relic", SC2WOL_LOC_ID_OFFSET + 801, LocationType.VANILLA),
        LocationData(SC2Mission.SMASH_AND_GRAB.mission_name, "Smash and Grab (Terran): Second Relic", SC2WOL_LOC_ID_OFFSET + 802, LocationType.VANILLA),
        LocationData(SC2Mission.SMASH_AND_GRAB.mission_name, "Smash and Grab (Terran): Third Relic", SC2WOL_LOC_ID_OFFSET + 803, LocationType.VANILLA,
                     lambda state: logic.terran_common_unit(state) and
                                   (adv_tactics and logic.terran_basic_anti_air(state)
                                    or logic.terran_competent_anti_air(state))),
        LocationData(SC2Mission.SMASH_AND_GRAB.mission_name, "Smash and Grab (Terran): Fourth Relic", SC2WOL_LOC_ID_OFFSET + 804, LocationType.VANILLA,
                     lambda state: logic.terran_common_unit(state) and
                                   (adv_tactics and logic.terran_basic_anti_air(state)
                                    or logic.terran_competent_anti_air(state))),
        LocationData(SC2Mission.SMASH_AND_GRAB.mission_name, "Smash and Grab (Terran): First Forcefield Area Busted", SC2WOL_LOC_ID_OFFSET + 805, LocationType.EXTRA,
                     lambda state: logic.terran_common_unit(state) and
                                   (adv_tactics and logic.terran_basic_anti_air(state)
                                    or logic.terran_competent_anti_air(state))),
        LocationData(SC2Mission.SMASH_AND_GRAB.mission_name, "Smash and Grab (Terran): Second Forcefield Area Busted", SC2WOL_LOC_ID_OFFSET + 806, LocationType.EXTRA,
                     lambda state: logic.terran_common_unit(state) and
                                   (adv_tactics and logic.terran_basic_anti_air(state)
                                    or logic.terran_competent_anti_air(state))),
        LocationData(SC2Mission.THE_DIG.mission_name, "The Dig: Victory", SC2WOL_LOC_ID_OFFSET + 900, LocationType.VICTORY,
                     lambda state: logic.terran_basic_anti_air(state)
                                   and logic.terran_defense_rating(state, False, True) >= 8
                                   and logic.terran_defense_rating(state, False, False) >= 6
                                   and logic.terran_common_unit(state)
                                   and (logic.marine_medic_upgrade(state) or adv_tactics)),
        LocationData(SC2Mission.THE_DIG.mission_name, "The Dig: Left Relic", SC2WOL_LOC_ID_OFFSET + 901, LocationType.VANILLA,
                     lambda state: logic.terran_defense_rating(state, False, False) >= 6
                                   and logic.terran_common_unit(state)
                                   and (logic.marine_medic_upgrade(state) or adv_tactics)),
        LocationData(SC2Mission.THE_DIG.mission_name, "The Dig: Right Ground Relic", SC2WOL_LOC_ID_OFFSET + 902, LocationType.VANILLA,
                     lambda state: logic.terran_defense_rating(state, False, False) >= 6
                                   and logic.terran_common_unit(state)
                                   and (logic.marine_medic_upgrade(state) or adv_tactics)),
        LocationData(SC2Mission.THE_DIG.mission_name, "The Dig: Right Cliff Relic", SC2WOL_LOC_ID_OFFSET + 903, LocationType.VANILLA,
                     lambda state: logic.terran_defense_rating(state, False, False) >= 6
                                   and logic.terran_common_unit(state)
                                   and (logic.marine_medic_upgrade(state) or adv_tactics)),
        LocationData(SC2Mission.THE_DIG.mission_name, "The Dig: Moebius Base", SC2WOL_LOC_ID_OFFSET + 904, LocationType.EXTRA,
                     lambda state: logic.marine_medic_upgrade(state) or adv_tactics),
        LocationData(SC2Mission.THE_DIG.mission_name, "The Dig: Door Outer Layer", SC2WOL_LOC_ID_OFFSET + 905, LocationType.EXTRA,
                     lambda state: logic.terran_defense_rating(state, False, False) >= 6
                                   and logic.terran_common_unit(state)
                                   and (logic.marine_medic_upgrade(state) or adv_tactics)),
        LocationData(SC2Mission.THE_DIG.mission_name, "The Dig: Door Thermal Barrier", SC2WOL_LOC_ID_OFFSET + 906, LocationType.EXTRA,
                     lambda state: logic.terran_basic_anti_air(state)
                                   and logic.terran_defense_rating(state, False, True) >= 8
                                   and logic.terran_defense_rating(state, False, False) >= 6
                                   and logic.terran_common_unit(state)
                                   and (logic.marine_medic_upgrade(state) or adv_tactics)),
        LocationData(SC2Mission.THE_DIG.mission_name, "The Dig: Cutting Through the Core", SC2WOL_LOC_ID_OFFSET + 907, LocationType.EXTRA,
                     lambda state: logic.terran_basic_anti_air(state)
                                   and logic.terran_defense_rating(state, False, True) >= 8
                                   and logic.terran_defense_rating(state, False, False) >= 6
                                   and logic.terran_common_unit(state)
                                   and (logic.marine_medic_upgrade(state) or adv_tactics)),
        LocationData(SC2Mission.THE_DIG.mission_name, "The Dig: Structure Access Imminent", SC2WOL_LOC_ID_OFFSET + 908, LocationType.EXTRA,
                     lambda state: logic.terran_basic_anti_air(state)
                                   and logic.terran_defense_rating(state, False, True) >= 8
                                   and logic.terran_defense_rating(state, False, False) >= 6
                                   and logic.terran_common_unit(state)
                                   and (logic.marine_medic_upgrade(state) or adv_tactics)),
        LocationData(SC2Mission.THE_MOEBIUS_FACTOR.mission_name, "The Moebius Factor: Victory", SC2WOL_LOC_ID_OFFSET + 1000, LocationType.VICTORY,
                     lambda state: logic.terran_basic_anti_air(state) and
                                   (logic.terran_air(state)
                                    or state.has_any({item_names.MEDIVAC, item_names.HERCULES}, player)
                                    and logic.terran_common_unit(state))),
        LocationData(SC2Mission.THE_MOEBIUS_FACTOR.mission_name, "The Moebius Factor: 1st Data Core", SC2WOL_LOC_ID_OFFSET + 1001, LocationType.VANILLA),
        LocationData(SC2Mission.THE_MOEBIUS_FACTOR.mission_name, "The Moebius Factor: 2nd Data Core", SC2WOL_LOC_ID_OFFSET + 1002, LocationType.VANILLA,
                     lambda state: (logic.terran_air(state)
                                    or state.has_any({item_names.MEDIVAC, item_names.HERCULES}, player)
                                    and logic.terran_common_unit(state))),
        LocationData(SC2Mission.THE_MOEBIUS_FACTOR.mission_name, "The Moebius Factor: South Rescue", SC2WOL_LOC_ID_OFFSET + 1003, LocationType.EXTRA,
                     lambda state: logic.terran_can_rescue(state)),
        LocationData(SC2Mission.THE_MOEBIUS_FACTOR.mission_name, "The Moebius Factor: Wall Rescue", SC2WOL_LOC_ID_OFFSET + 1004, LocationType.EXTRA,
                     lambda state: logic.terran_can_rescue(state)),
        LocationData(SC2Mission.THE_MOEBIUS_FACTOR.mission_name, "The Moebius Factor: Mid Rescue", SC2WOL_LOC_ID_OFFSET + 1005, LocationType.EXTRA,
                     lambda state: logic.terran_can_rescue(state)),
        LocationData(SC2Mission.THE_MOEBIUS_FACTOR.mission_name, "The Moebius Factor: Nydus Roof Rescue", SC2WOL_LOC_ID_OFFSET + 1006, LocationType.EXTRA,
                     lambda state: logic.terran_can_rescue(state)),
        LocationData(SC2Mission.THE_MOEBIUS_FACTOR.mission_name, "The Moebius Factor: Alive Inside Rescue", SC2WOL_LOC_ID_OFFSET + 1007, LocationType.EXTRA,
                     lambda state: logic.terran_can_rescue(state)),
        LocationData(SC2Mission.THE_MOEBIUS_FACTOR.mission_name, "The Moebius Factor: Brutalisk", SC2WOL_LOC_ID_OFFSET + 1008, LocationType.VANILLA,
                     lambda state: logic.terran_basic_anti_air(state) and
                                   (logic.terran_air(state)
                                    or state.has_any({item_names.MEDIVAC, item_names.HERCULES}, player)
                                    and logic.terran_common_unit(state))),
        LocationData(SC2Mission.THE_MOEBIUS_FACTOR.mission_name, "The Moebius Factor: 3rd Data Core", SC2WOL_LOC_ID_OFFSET + 1009, LocationType.VANILLA,
                     lambda state: logic.terran_basic_anti_air(state) and
                                   (logic.terran_air(state)
                                    or state.has_any({item_names.MEDIVAC, item_names.HERCULES}, player)
                                    and logic.terran_common_unit(state))),
        LocationData(SC2Mission.SUPERNOVA.mission_name, "Supernova: Victory", SC2WOL_LOC_ID_OFFSET + 1100, LocationType.VICTORY,
                     lambda state: logic.terran_beats_protoss_deathball(state)),
        LocationData(SC2Mission.SUPERNOVA.mission_name, "Supernova: West Relic", SC2WOL_LOC_ID_OFFSET + 1101, LocationType.VANILLA),
        LocationData(SC2Mission.SUPERNOVA.mission_name, "Supernova: North Relic", SC2WOL_LOC_ID_OFFSET + 1102, LocationType.VANILLA),
        LocationData(SC2Mission.SUPERNOVA.mission_name, "Supernova: South Relic", SC2WOL_LOC_ID_OFFSET + 1103, LocationType.VANILLA,
                     lambda state: logic.terran_beats_protoss_deathball(state)),
        LocationData(SC2Mission.SUPERNOVA.mission_name, "Supernova: East Relic", SC2WOL_LOC_ID_OFFSET + 1104, LocationType.VANILLA,
                     lambda state: logic.terran_beats_protoss_deathball(state)),
        LocationData(SC2Mission.SUPERNOVA.mission_name, "Supernova: Landing Zone Cleared", SC2WOL_LOC_ID_OFFSET + 1105, LocationType.EXTRA),
        LocationData(SC2Mission.SUPERNOVA.mission_name, "Supernova: Middle Base", SC2WOL_LOC_ID_OFFSET + 1106, LocationType.EXTRA,
                     lambda state: logic.terran_beats_protoss_deathball(state)),
        LocationData(SC2Mission.SUPERNOVA.mission_name, "Supernova: Southeast Base", SC2WOL_LOC_ID_OFFSET + 1107, LocationType.EXTRA,
                     lambda state: logic.terran_beats_protoss_deathball(state)),
        LocationData(SC2Mission.MAW_OF_THE_VOID.mission_name, "Maw of the Void: Victory", SC2WOL_LOC_ID_OFFSET + 1200, LocationType.VICTORY,
                     lambda state: logic.terran_survives_rip_field(state)),
        LocationData(SC2Mission.MAW_OF_THE_VOID.mission_name, "Maw of the Void: Landing Zone Cleared", SC2WOL_LOC_ID_OFFSET + 1201, LocationType.EXTRA),
        LocationData(SC2Mission.MAW_OF_THE_VOID.mission_name, "Maw of the Void: Expansion Prisoners", SC2WOL_LOC_ID_OFFSET + 1202, LocationType.VANILLA,
                     lambda state: adv_tactics or logic.terran_survives_rip_field(state)),
        LocationData(SC2Mission.MAW_OF_THE_VOID.mission_name, "Maw of the Void: South Close Prisoners", SC2WOL_LOC_ID_OFFSET + 1203, LocationType.VANILLA,
                     lambda state: adv_tactics or logic.terran_survives_rip_field(state)),
        LocationData(SC2Mission.MAW_OF_THE_VOID.mission_name, "Maw of the Void: South Far Prisoners", SC2WOL_LOC_ID_OFFSET + 1204, LocationType.VANILLA,
                     lambda state: logic.terran_survives_rip_field(state)),
        LocationData(SC2Mission.MAW_OF_THE_VOID.mission_name, "Maw of the Void: North Prisoners", SC2WOL_LOC_ID_OFFSET + 1205, LocationType.VANILLA,
                     lambda state: logic.terran_survives_rip_field(state)),
        LocationData(SC2Mission.MAW_OF_THE_VOID.mission_name, "Maw of the Void: Mothership", SC2WOL_LOC_ID_OFFSET + 1206, LocationType.EXTRA,
                     lambda state: logic.terran_survives_rip_field(state)),
        LocationData(SC2Mission.MAW_OF_THE_VOID.mission_name, "Maw of the Void: Expansion Rip Field Generator", SC2WOL_LOC_ID_OFFSET + 1207, LocationType.EXTRA,
                     lambda state: adv_tactics or logic.terran_survives_rip_field(state)),
        LocationData(SC2Mission.MAW_OF_THE_VOID.mission_name, "Maw of the Void: Middle Rip Field Generator", SC2WOL_LOC_ID_OFFSET + 1208, LocationType.EXTRA,
                     lambda state: logic.terran_survives_rip_field(state)),
        LocationData(SC2Mission.MAW_OF_THE_VOID.mission_name, "Maw of the Void: Southeast Rip Field Generator", SC2WOL_LOC_ID_OFFSET + 1209, LocationType.EXTRA,
                     lambda state: logic.terran_survives_rip_field(state)),
        LocationData(SC2Mission.MAW_OF_THE_VOID.mission_name, "Maw of the Void: Stargate Rip Field Generator", SC2WOL_LOC_ID_OFFSET + 1210, LocationType.EXTRA,
                     lambda state: logic.terran_survives_rip_field(state)),
        LocationData(SC2Mission.MAW_OF_THE_VOID.mission_name, "Maw of the Void: Northwest Rip Field Generator", SC2WOL_LOC_ID_OFFSET + 1211, LocationType.CHALLENGE,
                     lambda state: logic.terran_survives_rip_field(state)),
        LocationData(SC2Mission.MAW_OF_THE_VOID.mission_name, "Maw of the Void: West Rip Field Generator", SC2WOL_LOC_ID_OFFSET + 1212, LocationType.CHALLENGE,
                     lambda state: logic.terran_survives_rip_field(state)),
        LocationData(SC2Mission.MAW_OF_THE_VOID.mission_name, "Maw of the Void: Southwest Rip Field Generator", SC2WOL_LOC_ID_OFFSET + 1213, LocationType.CHALLENGE,
                     lambda state: logic.terran_survives_rip_field(state)),
        LocationData(SC2Mission.DEVILS_PLAYGROUND.mission_name, "Devil's Playground: Victory", SC2WOL_LOC_ID_OFFSET + 1300, LocationType.VICTORY,
                     lambda state: adv_tactics or
                                   logic.terran_basic_anti_air(state) and (
                                           logic.terran_common_unit(state) or state.has(item_names.REAPER, player))),
        LocationData(SC2Mission.DEVILS_PLAYGROUND.mission_name, "Devil's Playground: Tosh's Miners", SC2WOL_LOC_ID_OFFSET + 1301, LocationType.VANILLA),
        LocationData(SC2Mission.DEVILS_PLAYGROUND.mission_name, "Devil's Playground: Brutalisk", SC2WOL_LOC_ID_OFFSET + 1302, LocationType.VANILLA,
                     lambda state: adv_tactics or logic.terran_common_unit(state) or state.has(item_names.REAPER, player)),
        LocationData(SC2Mission.DEVILS_PLAYGROUND.mission_name, "Devil's Playground: North Reapers", SC2WOL_LOC_ID_OFFSET + 1303, LocationType.EXTRA),
        LocationData(SC2Mission.DEVILS_PLAYGROUND.mission_name, "Devil's Playground: Middle Reapers", SC2WOL_LOC_ID_OFFSET + 1304, LocationType.EXTRA,
                     lambda state: adv_tactics or logic.terran_common_unit(state) or state.has(item_names.REAPER, player)),
        LocationData(SC2Mission.DEVILS_PLAYGROUND.mission_name, "Devil's Playground: Southwest Reapers", SC2WOL_LOC_ID_OFFSET + 1305, LocationType.EXTRA,
                     lambda state: adv_tactics or logic.terran_common_unit(state) or state.has(item_names.REAPER, player)),
        LocationData(SC2Mission.DEVILS_PLAYGROUND.mission_name, "Devil's Playground: Southeast Reapers", SC2WOL_LOC_ID_OFFSET + 1306, LocationType.EXTRA,
                     lambda state: adv_tactics or
                                   logic.terran_basic_anti_air(state) and (
                                           logic.terran_common_unit(state) or state.has(item_names.REAPER, player))),
        LocationData(SC2Mission.DEVILS_PLAYGROUND.mission_name, "Devil's Playground: East Reapers", SC2WOL_LOC_ID_OFFSET + 1307, LocationType.CHALLENGE,
                     lambda state: logic.terran_basic_anti_air(state) and
                                    (adv_tactics or
                                           logic.terran_common_unit(state) or state.has(item_names.REAPER, player))),
        LocationData(SC2Mission.DEVILS_PLAYGROUND.mission_name, "Devil's Playground: Zerg Cleared", SC2WOL_LOC_ID_OFFSET + 1308, LocationType.CHALLENGE,
                     lambda state: logic.terran_competent_anti_air(state) and (
                                           logic.terran_common_unit(state) or state.has(item_names.REAPER, player))),
        LocationData(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "Welcome to the Jungle: Victory", SC2WOL_LOC_ID_OFFSET + 1400, LocationType.VICTORY,
                     lambda state: logic.welcome_to_the_jungle_requirement(state)),
        LocationData(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "Welcome to the Jungle: Close Relic", SC2WOL_LOC_ID_OFFSET + 1401, LocationType.VANILLA),
        LocationData(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "Welcome to the Jungle: West Relic", SC2WOL_LOC_ID_OFFSET + 1402, LocationType.VANILLA,
                     lambda state: logic.welcome_to_the_jungle_requirement(state)),
        LocationData(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "Welcome to the Jungle: North-East Relic", SC2WOL_LOC_ID_OFFSET + 1403, LocationType.VANILLA,
                     lambda state: logic.welcome_to_the_jungle_requirement(state)),
        LocationData(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "Welcome to the Jungle: Middle Base", SC2WOL_LOC_ID_OFFSET + 1404, LocationType.EXTRA,
                     lambda state: logic.welcome_to_the_jungle_requirement(state)),
        LocationData(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "Welcome to the Jungle: Main Base", SC2WOL_LOC_ID_OFFSET + 1405,
                     LocationType.MASTERY,
                     lambda state: logic.welcome_to_the_jungle_requirement(state)
                                   and logic.terran_beats_protoss_deathball(state)
                                   and logic.terran_base_trasher(state)),
        LocationData(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "Welcome to the Jungle: No Terrazine Nodes Sealed", SC2WOL_LOC_ID_OFFSET + 1406, LocationType.CHALLENGE,
                     lambda state: logic.welcome_to_the_jungle_requirement(state)
                                    and logic.terran_competent_ground_to_air(state)
                                   and logic.terran_beats_protoss_deathball(state)),
        LocationData(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "Welcome to the Jungle: Up to 1 Terrazine Node Sealed", SC2WOL_LOC_ID_OFFSET + 1407, LocationType.CHALLENGE,
                     lambda state: logic.welcome_to_the_jungle_requirement(state)
                                   and logic.terran_competent_ground_to_air(state)
                                   and logic.terran_beats_protoss_deathball(state)),
        LocationData(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "Welcome to the Jungle: Up to 2 Terrazine Nodes Sealed", SC2WOL_LOC_ID_OFFSET + 1408, LocationType.CHALLENGE,
                     lambda state: logic.welcome_to_the_jungle_requirement(state)
                                   and logic.terran_beats_protoss_deathball(state)),
        LocationData(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "Welcome to the Jungle: Up to 3 Terrazine Nodes Sealed", SC2WOL_LOC_ID_OFFSET + 1409, LocationType.CHALLENGE,
                     lambda state: logic.welcome_to_the_jungle_requirement(state)
                                   and logic.terran_competent_comp(state)),
        LocationData(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "Welcome to the Jungle: Up to 4 Terrazine Nodes Sealed", SC2WOL_LOC_ID_OFFSET + 1410, LocationType.EXTRA,
                     lambda state: logic.welcome_to_the_jungle_requirement(state)),
        LocationData(SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, "Welcome to the Jungle: Up to 5 Terrazine Nodes Sealed", SC2WOL_LOC_ID_OFFSET + 1411, LocationType.EXTRA,
                     lambda state: logic.welcome_to_the_jungle_requirement(state)),
        LocationData(SC2Mission.BREAKOUT.mission_name, "Breakout: Victory", SC2WOL_LOC_ID_OFFSET + 1500, LocationType.VICTORY),
        LocationData(SC2Mission.BREAKOUT.mission_name, "Breakout: Diamondback Prison", SC2WOL_LOC_ID_OFFSET + 1501, LocationType.VANILLA),
        LocationData(SC2Mission.BREAKOUT.mission_name, "Breakout: Siege Tank Prison", SC2WOL_LOC_ID_OFFSET + 1502, LocationType.VANILLA),
        LocationData(SC2Mission.BREAKOUT.mission_name, "Breakout: First Checkpoint", SC2WOL_LOC_ID_OFFSET + 1503, LocationType.EXTRA),
        LocationData(SC2Mission.BREAKOUT.mission_name, "Breakout: Second Checkpoint", SC2WOL_LOC_ID_OFFSET + 1504, LocationType.EXTRA),
        LocationData(SC2Mission.GHOST_OF_A_CHANCE.mission_name, "Ghost of a Chance: Victory", SC2WOL_LOC_ID_OFFSET + 1600, LocationType.VICTORY),
        LocationData(SC2Mission.GHOST_OF_A_CHANCE.mission_name, "Ghost of a Chance: Terrazine Tank", SC2WOL_LOC_ID_OFFSET + 1601, LocationType.EXTRA),
        LocationData(SC2Mission.GHOST_OF_A_CHANCE.mission_name, "Ghost of a Chance: Jorium Stockpile", SC2WOL_LOC_ID_OFFSET + 1602, LocationType.EXTRA),
        LocationData(SC2Mission.GHOST_OF_A_CHANCE.mission_name, "Ghost of a Chance: First Island Spectres", SC2WOL_LOC_ID_OFFSET + 1603, LocationType.VANILLA),
        LocationData(SC2Mission.GHOST_OF_A_CHANCE.mission_name, "Ghost of a Chance: Second Island Spectres", SC2WOL_LOC_ID_OFFSET + 1604, LocationType.VANILLA),
        LocationData(SC2Mission.GHOST_OF_A_CHANCE.mission_name, "Ghost of a Chance: Third Island Spectres", SC2WOL_LOC_ID_OFFSET + 1605, LocationType.VANILLA),
        LocationData(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "The Great Train Robbery: Victory", SC2WOL_LOC_ID_OFFSET + 1700, LocationType.VICTORY,
                     lambda state: logic.great_train_robbery_train_stopper(state) and
                                   logic.terran_basic_anti_air(state)),
        LocationData(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "The Great Train Robbery: North Defiler", SC2WOL_LOC_ID_OFFSET + 1701, LocationType.VANILLA),
        LocationData(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "The Great Train Robbery: Mid Defiler", SC2WOL_LOC_ID_OFFSET + 1702, LocationType.VANILLA),
        LocationData(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "The Great Train Robbery: South Defiler", SC2WOL_LOC_ID_OFFSET + 1703, LocationType.VANILLA),
        LocationData(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "The Great Train Robbery: Close Diamondback", SC2WOL_LOC_ID_OFFSET + 1704, LocationType.EXTRA),
        LocationData(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "The Great Train Robbery: Northwest Diamondback", SC2WOL_LOC_ID_OFFSET + 1705, LocationType.EXTRA),
        LocationData(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "The Great Train Robbery: North Diamondback", SC2WOL_LOC_ID_OFFSET + 1706, LocationType.EXTRA),
        LocationData(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "The Great Train Robbery: Northeast Diamondback", SC2WOL_LOC_ID_OFFSET + 1707, LocationType.EXTRA),
        LocationData(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "The Great Train Robbery: Southwest Diamondback", SC2WOL_LOC_ID_OFFSET + 1708, LocationType.EXTRA),
        LocationData(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "The Great Train Robbery: Southeast Diamondback", SC2WOL_LOC_ID_OFFSET + 1709, LocationType.EXTRA),
        LocationData(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "The Great Train Robbery: Kill Team", SC2WOL_LOC_ID_OFFSET + 1710, LocationType.CHALLENGE,
                     lambda state: (adv_tactics or logic.terran_common_unit(state)) and
                                   logic.great_train_robbery_train_stopper(state) and
                                   logic.terran_basic_anti_air(state)),
        LocationData(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "The Great Train Robbery: Flawless", SC2WOL_LOC_ID_OFFSET + 1711, LocationType.CHALLENGE,
                     lambda state: logic.great_train_robbery_train_stopper(state) and
                                   logic.terran_basic_anti_air(state)),
        LocationData(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "The Great Train Robbery: 2 Trains Destroyed", SC2WOL_LOC_ID_OFFSET + 1712, LocationType.EXTRA,
                     lambda state: logic.great_train_robbery_train_stopper(state)),
        LocationData(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "The Great Train Robbery: 4 Trains Destroyed", SC2WOL_LOC_ID_OFFSET + 1713, LocationType.EXTRA,
                     lambda state: logic.great_train_robbery_train_stopper(state) and
                                   logic.terran_basic_anti_air(state)),
        LocationData(SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, "The Great Train Robbery: 6 Trains Destroyed", SC2WOL_LOC_ID_OFFSET + 1714, LocationType.EXTRA,
                     lambda state: logic.great_train_robbery_train_stopper(state) and
                                   logic.terran_basic_anti_air(state)),
        LocationData(SC2Mission.CUTTHROAT.mission_name, "Cutthroat: Victory", SC2WOL_LOC_ID_OFFSET + 1800, LocationType.VICTORY,
                     lambda state: logic.terran_common_unit(state)
                                    and (adv_tactics or logic.terran_basic_anti_air(state))),
        LocationData(SC2Mission.CUTTHROAT.mission_name, "Cutthroat: Mira Han", SC2WOL_LOC_ID_OFFSET + 1801, LocationType.EXTRA,
                     lambda state: logic.terran_common_unit(state)),
        LocationData(SC2Mission.CUTTHROAT.mission_name, "Cutthroat: North Relic", SC2WOL_LOC_ID_OFFSET + 1802, LocationType.VANILLA,
                     lambda state: logic.terran_common_unit(state)),
        LocationData(SC2Mission.CUTTHROAT.mission_name, "Cutthroat: Mid Relic", SC2WOL_LOC_ID_OFFSET + 1803, LocationType.VANILLA),
        LocationData(SC2Mission.CUTTHROAT.mission_name, "Cutthroat: Southwest Relic", SC2WOL_LOC_ID_OFFSET + 1804, LocationType.VANILLA,
                     lambda state: logic.terran_common_unit(state)),
        LocationData(SC2Mission.CUTTHROAT.mission_name, "Cutthroat: North Command Center", SC2WOL_LOC_ID_OFFSET + 1805, LocationType.EXTRA,
                     lambda state: logic.terran_common_unit(state)),
        LocationData(SC2Mission.CUTTHROAT.mission_name, "Cutthroat: South Command Center", SC2WOL_LOC_ID_OFFSET + 1806, LocationType.EXTRA,
                     lambda state: logic.terran_common_unit(state)),
        LocationData(SC2Mission.CUTTHROAT.mission_name, "Cutthroat: West Command Center", SC2WOL_LOC_ID_OFFSET + 1807, LocationType.EXTRA,
                     lambda state: logic.terran_common_unit(state)),
        LocationData(SC2Mission.ENGINE_OF_DESTRUCTION.mission_name, "Engine of Destruction: Victory", SC2WOL_LOC_ID_OFFSET + 1900, LocationType.VICTORY,
                     lambda state: logic.engine_of_destruction_requirement(state)),
        LocationData(SC2Mission.ENGINE_OF_DESTRUCTION.mission_name, "Engine of Destruction: Odin", SC2WOL_LOC_ID_OFFSET + 1901, LocationType.EXTRA,
                     lambda state: logic.marine_medic_upgrade(state)),
        LocationData(SC2Mission.ENGINE_OF_DESTRUCTION.mission_name, "Engine of Destruction: Loki", SC2WOL_LOC_ID_OFFSET + 1902,
                     LocationType.CHALLENGE,
                     lambda state: logic.engine_of_destruction_requirement(state)),
        LocationData(SC2Mission.ENGINE_OF_DESTRUCTION.mission_name, "Engine of Destruction: Lab Devourer", SC2WOL_LOC_ID_OFFSET + 1903, LocationType.VANILLA,
                     lambda state: logic.marine_medic_upgrade(state)),
        LocationData(SC2Mission.ENGINE_OF_DESTRUCTION.mission_name, "Engine of Destruction: North Devourer", SC2WOL_LOC_ID_OFFSET + 1904, LocationType.VANILLA,
                     lambda state: logic.engine_of_destruction_requirement(state)),
        LocationData(SC2Mission.ENGINE_OF_DESTRUCTION.mission_name, "Engine of Destruction: Southeast Devourer", SC2WOL_LOC_ID_OFFSET + 1905, LocationType.VANILLA,
                     lambda state: logic.engine_of_destruction_requirement(state)),
        LocationData(SC2Mission.ENGINE_OF_DESTRUCTION.mission_name, "Engine of Destruction: West Base", SC2WOL_LOC_ID_OFFSET + 1906, LocationType.EXTRA,
                     lambda state: logic.engine_of_destruction_requirement(state)),
        LocationData(SC2Mission.ENGINE_OF_DESTRUCTION.mission_name, "Engine of Destruction: Northwest Base", SC2WOL_LOC_ID_OFFSET + 1907, LocationType.EXTRA,
                     lambda state: logic.engine_of_destruction_requirement(state)),
        LocationData(SC2Mission.ENGINE_OF_DESTRUCTION.mission_name, "Engine of Destruction: Northeast Base", SC2WOL_LOC_ID_OFFSET + 1908, LocationType.EXTRA,
                     lambda state: logic.engine_of_destruction_requirement(state)),
        LocationData(SC2Mission.ENGINE_OF_DESTRUCTION.mission_name, "Engine of Destruction: Southeast Base", SC2WOL_LOC_ID_OFFSET + 1909, LocationType.EXTRA,
                     lambda state: logic.engine_of_destruction_requirement(state)),
        LocationData(SC2Mission.MEDIA_BLITZ.mission_name, "Media Blitz: Victory", SC2WOL_LOC_ID_OFFSET + 2000, LocationType.VICTORY,
                     lambda state: logic.terran_competent_comp(state)),
        LocationData(SC2Mission.MEDIA_BLITZ.mission_name, "Media Blitz: Tower 1", SC2WOL_LOC_ID_OFFSET + 2001, LocationType.VANILLA,
                     lambda state: logic.terran_competent_comp(state)),
        LocationData(SC2Mission.MEDIA_BLITZ.mission_name, "Media Blitz: Tower 2", SC2WOL_LOC_ID_OFFSET + 2002, LocationType.VANILLA,
                     lambda state: logic.terran_competent_comp(state)),
        LocationData(SC2Mission.MEDIA_BLITZ.mission_name, "Media Blitz: Tower 3", SC2WOL_LOC_ID_OFFSET + 2003, LocationType.VANILLA,
                     lambda state: logic.terran_competent_comp(state)),
        LocationData(SC2Mission.MEDIA_BLITZ.mission_name, "Media Blitz: Science Facility", SC2WOL_LOC_ID_OFFSET + 2004, LocationType.VANILLA),
        LocationData(SC2Mission.MEDIA_BLITZ.mission_name, "Media Blitz: All Barracks", SC2WOL_LOC_ID_OFFSET + 2005, LocationType.EXTRA,
                     lambda state: logic.terran_competent_comp(state)),
        LocationData(SC2Mission.MEDIA_BLITZ.mission_name, "Media Blitz: All Factories", SC2WOL_LOC_ID_OFFSET + 2006, LocationType.EXTRA,
                     lambda state: logic.terran_competent_comp(state)),
        LocationData(SC2Mission.MEDIA_BLITZ.mission_name, "Media Blitz: All Starports", SC2WOL_LOC_ID_OFFSET + 2007, LocationType.EXTRA,
                     lambda state: adv_tactics or logic.terran_competent_comp(state)),
        LocationData(SC2Mission.MEDIA_BLITZ.mission_name, "Media Blitz: Odin Not Trashed", SC2WOL_LOC_ID_OFFSET + 2008, LocationType.CHALLENGE,
                     lambda state: logic.terran_competent_comp(state)),
        LocationData(SC2Mission.MEDIA_BLITZ.mission_name, "Media Blitz: Surprise Attack Ends", SC2WOL_LOC_ID_OFFSET + 2009, LocationType.EXTRA),
        LocationData(SC2Mission.PIERCING_OF_THE_SHROUD.mission_name, "Piercing the Shroud: Victory", SC2WOL_LOC_ID_OFFSET + 2100, LocationType.VICTORY,
                     lambda state: logic.marine_medic_upgrade(state)),
        LocationData(SC2Mission.PIERCING_OF_THE_SHROUD.mission_name, "Piercing the Shroud: Holding Cell Relic", SC2WOL_LOC_ID_OFFSET + 2101, LocationType.VANILLA),
        LocationData(SC2Mission.PIERCING_OF_THE_SHROUD.mission_name, "Piercing the Shroud: Brutalisk Relic", SC2WOL_LOC_ID_OFFSET + 2102, LocationType.VANILLA,
                     lambda state: logic.marine_medic_upgrade(state)),
        LocationData(SC2Mission.PIERCING_OF_THE_SHROUD.mission_name, "Piercing the Shroud: First Escape Relic", SC2WOL_LOC_ID_OFFSET + 2103, LocationType.VANILLA,
                     lambda state: logic.marine_medic_upgrade(state)),
        LocationData(SC2Mission.PIERCING_OF_THE_SHROUD.mission_name, "Piercing the Shroud: Second Escape Relic", SC2WOL_LOC_ID_OFFSET + 2104, LocationType.VANILLA,
                     lambda state: logic.marine_medic_upgrade(state)),
        LocationData(SC2Mission.PIERCING_OF_THE_SHROUD.mission_name, "Piercing the Shroud: Brutalisk", SC2WOL_LOC_ID_OFFSET + 2105, LocationType.VANILLA,
                     lambda state: logic.marine_medic_upgrade(state)),
        LocationData(SC2Mission.PIERCING_OF_THE_SHROUD.mission_name, "Piercing the Shroud: Fusion Reactor", SC2WOL_LOC_ID_OFFSET + 2106, LocationType.EXTRA,
                     lambda state: logic.marine_medic_upgrade(state)),
        LocationData(SC2Mission.PIERCING_OF_THE_SHROUD.mission_name, "Piercing the Shroud: Entrance Holding Pen", SC2WOL_LOC_ID_OFFSET + 2107, LocationType.EXTRA),
        LocationData(SC2Mission.PIERCING_OF_THE_SHROUD.mission_name, "Piercing the Shroud: Cargo Bay Warbot", SC2WOL_LOC_ID_OFFSET + 2108, LocationType.EXTRA),
        LocationData(SC2Mission.PIERCING_OF_THE_SHROUD.mission_name, "Piercing the Shroud: Escape Warbot", SC2WOL_LOC_ID_OFFSET + 2109, LocationType.EXTRA,
                     lambda state: logic.marine_medic_upgrade(state)),
        LocationData(SC2Mission.WHISPERS_OF_DOOM.mission_name, "Whispers of Doom: Victory", SC2WOL_LOC_ID_OFFSET + 2200, LocationType.VICTORY),
        LocationData(SC2Mission.WHISPERS_OF_DOOM.mission_name, "Whispers of Doom: First Hatchery", SC2WOL_LOC_ID_OFFSET + 2201, LocationType.VANILLA),
        LocationData(SC2Mission.WHISPERS_OF_DOOM.mission_name, "Whispers of Doom: Second Hatchery", SC2WOL_LOC_ID_OFFSET + 2202, LocationType.VANILLA),
        LocationData(SC2Mission.WHISPERS_OF_DOOM.mission_name, "Whispers of Doom: Third Hatchery", SC2WOL_LOC_ID_OFFSET + 2203, LocationType.VANILLA),
        LocationData(SC2Mission.WHISPERS_OF_DOOM.mission_name, "Whispers of Doom: First Prophecy Fragment", SC2WOL_LOC_ID_OFFSET + 2204, LocationType.EXTRA),
        LocationData(SC2Mission.WHISPERS_OF_DOOM.mission_name, "Whispers of Doom: Second Prophecy Fragment", SC2WOL_LOC_ID_OFFSET + 2205, LocationType.EXTRA),
        LocationData(SC2Mission.WHISPERS_OF_DOOM.mission_name, "Whispers of Doom: Third Prophecy Fragment", SC2WOL_LOC_ID_OFFSET + 2206, LocationType.EXTRA),
        LocationData(SC2Mission.A_SINISTER_TURN.mission_name, "A Sinister Turn: Victory", SC2WOL_LOC_ID_OFFSET + 2300, LocationType.VICTORY,
                     lambda state: logic.protoss_common_unit(state) and logic.protoss_competent_anti_air(state)),
        LocationData(SC2Mission.A_SINISTER_TURN.mission_name, "A Sinister Turn: Robotics Facility", SC2WOL_LOC_ID_OFFSET + 2301, LocationType.VANILLA,
                     lambda state: adv_tactics or logic.protoss_common_unit(state)),
        LocationData(SC2Mission.A_SINISTER_TURN.mission_name, "A Sinister Turn: Dark Shrine", SC2WOL_LOC_ID_OFFSET + 2302, LocationType.VANILLA,
                     lambda state: adv_tactics or logic.protoss_common_unit(state)),
        LocationData(SC2Mission.A_SINISTER_TURN.mission_name, "A Sinister Turn: Templar Archives", SC2WOL_LOC_ID_OFFSET + 2303, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state) and logic.protoss_competent_anti_air(state)),
        LocationData(SC2Mission.A_SINISTER_TURN.mission_name, "A Sinister Turn: Northeast Base", SC2WOL_LOC_ID_OFFSET + 2304, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state) and logic.protoss_competent_anti_air(state)),
        LocationData(SC2Mission.A_SINISTER_TURN.mission_name, "A Sinister Turn: Southwest Base", SC2WOL_LOC_ID_OFFSET + 2305, LocationType.CHALLENGE,
                     lambda state: logic.protoss_common_unit(state) and logic.protoss_competent_anti_air(state)),
        LocationData(SC2Mission.A_SINISTER_TURN.mission_name, "A Sinister Turn: Maar", SC2WOL_LOC_ID_OFFSET + 2306, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)),
        LocationData(SC2Mission.A_SINISTER_TURN.mission_name, "A Sinister Turn: Northwest Preserver", SC2WOL_LOC_ID_OFFSET + 2307, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state) and logic.protoss_competent_anti_air(state)),
        LocationData(SC2Mission.A_SINISTER_TURN.mission_name, "A Sinister Turn: Southwest Preserver", SC2WOL_LOC_ID_OFFSET + 2308, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state) and logic.protoss_competent_anti_air(state)),
        LocationData(SC2Mission.A_SINISTER_TURN.mission_name, "A Sinister Turn: East Preserver", SC2WOL_LOC_ID_OFFSET + 2309, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state) and logic.protoss_competent_anti_air(state)),
        LocationData(SC2Mission.ECHOES_OF_THE_FUTURE.mission_name, "Echoes of the Future: Victory", SC2WOL_LOC_ID_OFFSET + 2400, LocationType.VICTORY,
                     lambda state: adv_tactics and logic.protoss_static_defense(state) or logic.protoss_common_unit(state) and logic.protoss_competent_anti_air(state)),
        LocationData(SC2Mission.ECHOES_OF_THE_FUTURE.mission_name, "Echoes of the Future: Close Obelisk", SC2WOL_LOC_ID_OFFSET + 2401, LocationType.VANILLA),
        LocationData(SC2Mission.ECHOES_OF_THE_FUTURE.mission_name, "Echoes of the Future: West Obelisk", SC2WOL_LOC_ID_OFFSET + 2402, LocationType.VANILLA,
                     lambda state: adv_tactics and logic.protoss_static_defense(state) or logic.protoss_common_unit(state)),
        LocationData(SC2Mission.ECHOES_OF_THE_FUTURE.mission_name, "Echoes of the Future: Base", SC2WOL_LOC_ID_OFFSET + 2403, LocationType.EXTRA),
        LocationData(SC2Mission.ECHOES_OF_THE_FUTURE.mission_name, "Echoes of the Future: Southwest Tendril", SC2WOL_LOC_ID_OFFSET + 2404, LocationType.EXTRA),
        LocationData(SC2Mission.ECHOES_OF_THE_FUTURE.mission_name, "Echoes of the Future: Southeast Tendril", SC2WOL_LOC_ID_OFFSET + 2405, LocationType.EXTRA,
                     lambda state: adv_tactics and logic.protoss_static_defense(state) or logic.protoss_common_unit(state)),
        LocationData(SC2Mission.ECHOES_OF_THE_FUTURE.mission_name, "Echoes of the Future: Northeast Tendril", SC2WOL_LOC_ID_OFFSET + 2406, LocationType.EXTRA,
                     lambda state: adv_tactics and logic.protoss_static_defense(state) or logic.protoss_common_unit(state)),
        LocationData(SC2Mission.ECHOES_OF_THE_FUTURE.mission_name, "Echoes of the Future: Northwest Tendril", SC2WOL_LOC_ID_OFFSET + 2407, LocationType.EXTRA,
                     lambda state: adv_tactics and logic.protoss_static_defense(state) or logic.protoss_common_unit(state)),
        LocationData(SC2Mission.IN_UTTER_DARKNESS.mission_name, "In Utter Darkness: Defeat", SC2WOL_LOC_ID_OFFSET + 2500, LocationType.VICTORY),
        LocationData(SC2Mission.IN_UTTER_DARKNESS.mission_name, "In Utter Darkness: Protoss Archive", SC2WOL_LOC_ID_OFFSET + 2501, LocationType.VANILLA,
                     lambda state: logic.last_stand_requirement(state)),
        LocationData(SC2Mission.IN_UTTER_DARKNESS.mission_name, "In Utter Darkness: Kills", SC2WOL_LOC_ID_OFFSET + 2502, LocationType.VANILLA,
                     lambda state: logic.last_stand_requirement(state)),
        LocationData(SC2Mission.IN_UTTER_DARKNESS.mission_name, "In Utter Darkness: Urun", SC2WOL_LOC_ID_OFFSET + 2503, LocationType.EXTRA),
        LocationData(SC2Mission.IN_UTTER_DARKNESS.mission_name, "In Utter Darkness: Mohandar", SC2WOL_LOC_ID_OFFSET + 2504, LocationType.EXTRA,
                     lambda state: logic.last_stand_requirement(state)),
        LocationData(SC2Mission.IN_UTTER_DARKNESS.mission_name, "In Utter Darkness: Selendis", SC2WOL_LOC_ID_OFFSET + 2505, LocationType.EXTRA,
                     lambda state: logic.last_stand_requirement(state)),
        LocationData(SC2Mission.IN_UTTER_DARKNESS.mission_name, "In Utter Darkness: Artanis", SC2WOL_LOC_ID_OFFSET + 2506, LocationType.EXTRA,
                     lambda state: logic.last_stand_requirement(state)),
        LocationData(SC2Mission.GATES_OF_HELL.mission_name, "Gates of Hell: Victory", SC2WOL_LOC_ID_OFFSET + 2600, LocationType.VICTORY,
                     lambda state: logic.terran_competent_comp(state) and
                                   logic.terran_defense_rating(state, True) > 6),
        LocationData(SC2Mission.GATES_OF_HELL.mission_name, "Gates of Hell: Large Army", SC2WOL_LOC_ID_OFFSET + 2601, LocationType.VANILLA,
                     lambda state: logic.terran_competent_comp(state) and
                                   logic.terran_defense_rating(state, True) > 6),
        LocationData(SC2Mission.GATES_OF_HELL.mission_name, "Gates of Hell: 2 Drop Pods", SC2WOL_LOC_ID_OFFSET + 2602, LocationType.VANILLA,
                     lambda state: logic.terran_competent_comp(state) and
                                   logic.terran_defense_rating(state, True) > 6),
        LocationData(SC2Mission.GATES_OF_HELL.mission_name, "Gates of Hell: 4 Drop Pods", SC2WOL_LOC_ID_OFFSET + 2603, LocationType.VANILLA,
                     lambda state: logic.terran_competent_comp(state) and
                                   logic.terran_defense_rating(state, True) > 6),
        LocationData(SC2Mission.GATES_OF_HELL.mission_name, "Gates of Hell: 6 Drop Pods", SC2WOL_LOC_ID_OFFSET + 2604, LocationType.EXTRA,
                     lambda state: logic.terran_competent_comp(state) and
                                   logic.terran_defense_rating(state, True) > 6),
        LocationData(SC2Mission.GATES_OF_HELL.mission_name, "Gates of Hell: 8 Drop Pods", SC2WOL_LOC_ID_OFFSET + 2605, LocationType.CHALLENGE,
                     lambda state: logic.terran_competent_comp(state) and
                                   logic.terran_defense_rating(state, True) > 6),
        LocationData(SC2Mission.GATES_OF_HELL.mission_name, "Gates of Hell: Southwest Spore Cannon", SC2WOL_LOC_ID_OFFSET + 2606, LocationType.EXTRA,
                     lambda state: logic.terran_competent_comp(state) and
                                   logic.terran_defense_rating(state, True) > 6),
        LocationData(SC2Mission.GATES_OF_HELL.mission_name, "Gates of Hell: Northwest Spore Cannon", SC2WOL_LOC_ID_OFFSET + 2607, LocationType.EXTRA,
                     lambda state: logic.terran_competent_comp(state) and
                                   logic.terran_defense_rating(state, True) > 6),
        LocationData(SC2Mission.GATES_OF_HELL.mission_name, "Gates of Hell: Northeast Spore Cannon", SC2WOL_LOC_ID_OFFSET + 2608, LocationType.EXTRA,
                     lambda state: logic.terran_competent_comp(state) and
                                   logic.terran_defense_rating(state, True) > 6),
        LocationData(SC2Mission.GATES_OF_HELL.mission_name, "Gates of Hell: East Spore Cannon", SC2WOL_LOC_ID_OFFSET + 2609, LocationType.EXTRA,
                     lambda state: logic.terran_competent_comp(state) and
                                   logic.terran_defense_rating(state, True) > 6),
        LocationData(SC2Mission.GATES_OF_HELL.mission_name, "Gates of Hell: Southeast Spore Cannon", SC2WOL_LOC_ID_OFFSET + 2610, LocationType.EXTRA,
                     lambda state: logic.terran_competent_comp(state) and
                                   logic.terran_defense_rating(state, True) > 6),
        LocationData(SC2Mission.GATES_OF_HELL.mission_name, "Gates of Hell: Expansion Spore Cannon", SC2WOL_LOC_ID_OFFSET + 2611, LocationType.EXTRA,
                     lambda state: logic.terran_competent_comp(state) and
                                   logic.terran_defense_rating(state, True) > 6),
        LocationData(SC2Mission.BELLY_OF_THE_BEAST.mission_name, "Belly of the Beast: Victory", SC2WOL_LOC_ID_OFFSET + 2700, LocationType.VICTORY),
        LocationData(SC2Mission.BELLY_OF_THE_BEAST.mission_name, "Belly of the Beast: First Charge", SC2WOL_LOC_ID_OFFSET + 2701, LocationType.EXTRA),
        LocationData(SC2Mission.BELLY_OF_THE_BEAST.mission_name, "Belly of the Beast: Second Charge", SC2WOL_LOC_ID_OFFSET + 2702, LocationType.EXTRA),
        LocationData(SC2Mission.BELLY_OF_THE_BEAST.mission_name, "Belly of the Beast: Third Charge", SC2WOL_LOC_ID_OFFSET + 2703, LocationType.EXTRA),
        LocationData(SC2Mission.BELLY_OF_THE_BEAST.mission_name, "Belly of the Beast: First Group Rescued", SC2WOL_LOC_ID_OFFSET + 2704, LocationType.VANILLA),
        LocationData(SC2Mission.BELLY_OF_THE_BEAST.mission_name, "Belly of the Beast: Second Group Rescued", SC2WOL_LOC_ID_OFFSET + 2705, LocationType.VANILLA),
        LocationData(SC2Mission.BELLY_OF_THE_BEAST.mission_name, "Belly of the Beast: Third Group Rescued", SC2WOL_LOC_ID_OFFSET + 2706, LocationType.VANILLA),
        LocationData(SC2Mission.SHATTER_THE_SKY.mission_name, "Shatter the Sky: Victory", SC2WOL_LOC_ID_OFFSET + 2800, LocationType.VICTORY,
                     lambda state: logic.terran_competent_comp(state)),
        LocationData(SC2Mission.SHATTER_THE_SKY.mission_name, "Shatter the Sky: Close Coolant Tower", SC2WOL_LOC_ID_OFFSET + 2801, LocationType.VANILLA,
                     lambda state: logic.terran_competent_comp(state)),
        LocationData(SC2Mission.SHATTER_THE_SKY.mission_name, "Shatter the Sky: Northwest Coolant Tower", SC2WOL_LOC_ID_OFFSET + 2802, LocationType.VANILLA,
                     lambda state: logic.terran_competent_comp(state)),
        LocationData(SC2Mission.SHATTER_THE_SKY.mission_name, "Shatter the Sky: Southeast Coolant Tower", SC2WOL_LOC_ID_OFFSET + 2803, LocationType.VANILLA,
                     lambda state: logic.terran_competent_comp(state)),
        LocationData(SC2Mission.SHATTER_THE_SKY.mission_name, "Shatter the Sky: Southwest Coolant Tower", SC2WOL_LOC_ID_OFFSET + 2804, LocationType.VANILLA,
                     lambda state: logic.terran_competent_comp(state)),
        LocationData(SC2Mission.SHATTER_THE_SKY.mission_name, "Shatter the Sky: Leviathan", SC2WOL_LOC_ID_OFFSET + 2805, LocationType.VANILLA,
                     lambda state: logic.terran_competent_comp(state)),
        LocationData(SC2Mission.SHATTER_THE_SKY.mission_name, "Shatter the Sky: East Hatchery", SC2WOL_LOC_ID_OFFSET + 2806, LocationType.EXTRA,
                     lambda state: logic.terran_competent_comp(state)),
        LocationData(SC2Mission.SHATTER_THE_SKY.mission_name, "Shatter the Sky: North Hatchery", SC2WOL_LOC_ID_OFFSET + 2807, LocationType.EXTRA,
                     lambda state: logic.terran_competent_comp(state)),
        LocationData(SC2Mission.SHATTER_THE_SKY.mission_name, "Shatter the Sky: Mid Hatchery", SC2WOL_LOC_ID_OFFSET + 2808, LocationType.EXTRA,
                     lambda state: logic.terran_competent_comp(state)),
        LocationData(SC2Mission.ALL_IN.mission_name, "All-In: Victory", SC2WOL_LOC_ID_OFFSET + 2900, LocationType.VICTORY,
                     lambda state: logic.all_in_requirement(state)),
        LocationData(SC2Mission.ALL_IN.mission_name, "All-In: First Kerrigan Attack", SC2WOL_LOC_ID_OFFSET + 2901, LocationType.EXTRA,
                     lambda state: logic.all_in_requirement(state)),
        LocationData(SC2Mission.ALL_IN.mission_name, "All-In: Second Kerrigan Attack", SC2WOL_LOC_ID_OFFSET + 2902, LocationType.EXTRA,
                     lambda state: logic.all_in_requirement(state)),
        LocationData(SC2Mission.ALL_IN.mission_name, "All-In: Third Kerrigan Attack", SC2WOL_LOC_ID_OFFSET + 2903, LocationType.EXTRA,
                     lambda state: logic.all_in_requirement(state)),
        LocationData(SC2Mission.ALL_IN.mission_name, "All-In: Fourth Kerrigan Attack", SC2WOL_LOC_ID_OFFSET + 2904, LocationType.EXTRA,
                     lambda state: logic.all_in_requirement(state)),
        LocationData(SC2Mission.ALL_IN.mission_name, "All-In: Fifth Kerrigan Attack", SC2WOL_LOC_ID_OFFSET + 2905, LocationType.EXTRA,
                     lambda state: logic.all_in_requirement(state)),

        # HotS
        LocationData(SC2Mission.LAB_RAT.mission_name, "Lab Rat: Victory", SC2HOTS_LOC_ID_OFFSET + 100, LocationType.VICTORY,
                     lambda state: logic.zerg_common_unit(state)),
        LocationData(SC2Mission.LAB_RAT.mission_name, "Lab Rat: Gather Minerals", SC2HOTS_LOC_ID_OFFSET + 101, LocationType.VANILLA),
        LocationData(SC2Mission.LAB_RAT.mission_name, "Lab Rat: South Zergling Group", SC2HOTS_LOC_ID_OFFSET + 102, LocationType.VANILLA,
                     lambda state: adv_tactics or logic.zerg_common_unit(state)),
        LocationData(SC2Mission.LAB_RAT.mission_name, "Lab Rat: East Zergling Group", SC2HOTS_LOC_ID_OFFSET + 103, LocationType.VANILLA,
                     lambda state: adv_tactics or logic.zerg_common_unit(state)),
        LocationData(SC2Mission.LAB_RAT.mission_name, "Lab Rat: West Zergling Group", SC2HOTS_LOC_ID_OFFSET + 104, LocationType.VANILLA,
                     lambda state: adv_tactics or logic.zerg_common_unit(state)),
        LocationData(SC2Mission.LAB_RAT.mission_name, "Lab Rat: Hatchery", SC2HOTS_LOC_ID_OFFSET + 105, LocationType.EXTRA),
        LocationData(SC2Mission.LAB_RAT.mission_name, "Lab Rat: Overlord", SC2HOTS_LOC_ID_OFFSET + 106, LocationType.EXTRA),
        LocationData(SC2Mission.LAB_RAT.mission_name, "Lab Rat: Gas Turrets", SC2HOTS_LOC_ID_OFFSET + 107, LocationType.EXTRA,
                     lambda state: adv_tactics or logic.zerg_common_unit(state)),
        LocationData(SC2Mission.BACK_IN_THE_SADDLE.mission_name, "Back in the Saddle: Victory", SC2HOTS_LOC_ID_OFFSET + 200, LocationType.VICTORY,
                     lambda state: logic.basic_kerrigan(state) or kerriganless or logic.story_tech_granted),
        LocationData(SC2Mission.BACK_IN_THE_SADDLE.mission_name, "Back in the Saddle: Defend the Tram", SC2HOTS_LOC_ID_OFFSET + 201, LocationType.EXTRA,
                     lambda state: logic.basic_kerrigan(state) or kerriganless or logic.story_tech_granted),
        LocationData(SC2Mission.BACK_IN_THE_SADDLE.mission_name, "Back in the Saddle: Kinetic Blast", SC2HOTS_LOC_ID_OFFSET + 202, LocationType.VANILLA),
        LocationData(SC2Mission.BACK_IN_THE_SADDLE.mission_name, "Back in the Saddle: Crushing Grip", SC2HOTS_LOC_ID_OFFSET + 203, LocationType.VANILLA),
        LocationData(SC2Mission.BACK_IN_THE_SADDLE.mission_name, "Back in the Saddle: Reach the Sublevel", SC2HOTS_LOC_ID_OFFSET + 204, LocationType.EXTRA),
        LocationData(SC2Mission.BACK_IN_THE_SADDLE.mission_name, "Back in the Saddle: Door Section Cleared", SC2HOTS_LOC_ID_OFFSET + 205, LocationType.EXTRA,
                     lambda state: logic.basic_kerrigan(state) or kerriganless or logic.story_tech_granted),
        LocationData(SC2Mission.RENDEZVOUS.mission_name, "Rendezvous: Victory", SC2HOTS_LOC_ID_OFFSET + 300, LocationType.VICTORY,
                     lambda state: logic.zerg_common_unit(state) and
                                   logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.RENDEZVOUS.mission_name, "Rendezvous: Right Queen", SC2HOTS_LOC_ID_OFFSET + 301, LocationType.VANILLA,
                     lambda state: logic.zerg_common_unit(state) and
                                   logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.RENDEZVOUS.mission_name, "Rendezvous: Center Queen", SC2HOTS_LOC_ID_OFFSET + 302, LocationType.VANILLA,
                     lambda state: logic.zerg_common_unit(state) and
                                   logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.RENDEZVOUS.mission_name, "Rendezvous: Left Queen", SC2HOTS_LOC_ID_OFFSET + 303, LocationType.VANILLA,
                     lambda state: logic.zerg_common_unit(state) and
                                   logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.RENDEZVOUS.mission_name, "Rendezvous: Hold Out Finished", SC2HOTS_LOC_ID_OFFSET + 304, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state) and
                                   logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.HARVEST_OF_SCREAMS.mission_name, "Harvest of Screams: Victory", SC2HOTS_LOC_ID_OFFSET + 400, LocationType.VICTORY,
                     lambda state: logic.zerg_common_unit(state)
                                   and logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.HARVEST_OF_SCREAMS.mission_name, "Harvest of Screams: First Ursadon Matriarch", SC2HOTS_LOC_ID_OFFSET + 401, LocationType.VANILLA),
        LocationData(SC2Mission.HARVEST_OF_SCREAMS.mission_name, "Harvest of Screams: North Ursadon Matriarch", SC2HOTS_LOC_ID_OFFSET + 402, LocationType.VANILLA,
                     lambda state: logic.zerg_common_unit(state)),
        LocationData(SC2Mission.HARVEST_OF_SCREAMS.mission_name, "Harvest of Screams: West Ursadon Matriarch", SC2HOTS_LOC_ID_OFFSET + 403, LocationType.VANILLA,
                     lambda state: logic.zerg_common_unit(state)),
        LocationData(SC2Mission.HARVEST_OF_SCREAMS.mission_name, "Harvest of Screams: Lost Brood", SC2HOTS_LOC_ID_OFFSET + 404, LocationType.EXTRA),
        LocationData(SC2Mission.HARVEST_OF_SCREAMS.mission_name, "Harvest of Screams: Northeast Psi-link Spire", SC2HOTS_LOC_ID_OFFSET + 405, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state)),
        LocationData(SC2Mission.HARVEST_OF_SCREAMS.mission_name, "Harvest of Screams: Northwest Psi-link Spire", SC2HOTS_LOC_ID_OFFSET + 406, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state)
                                   and logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.HARVEST_OF_SCREAMS.mission_name, "Harvest of Screams: Southwest Psi-link Spire", SC2HOTS_LOC_ID_OFFSET + 407, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state)
                                   and logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.HARVEST_OF_SCREAMS.mission_name, "Harvest of Screams: Nafash", SC2HOTS_LOC_ID_OFFSET + 408, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state)
                                   and logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "Shoot the Messenger: Victory", SC2HOTS_LOC_ID_OFFSET + 500, LocationType.VICTORY,
                     lambda state: logic.zerg_common_unit(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "Shoot the Messenger: East Stasis Chamber", SC2HOTS_LOC_ID_OFFSET + 501, LocationType.VANILLA,
                     lambda state: logic.zerg_common_unit(state) and logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "Shoot the Messenger: Center Stasis Chamber", SC2HOTS_LOC_ID_OFFSET + 502, LocationType.VANILLA,
                     lambda state: logic.zerg_common_unit(state) or adv_tactics),
        LocationData(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "Shoot the Messenger: West Stasis Chamber", SC2HOTS_LOC_ID_OFFSET + 503, LocationType.VANILLA,
                     lambda state: logic.zerg_common_unit(state) and logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "Shoot the Messenger: Destroy 4 Shuttles", SC2HOTS_LOC_ID_OFFSET + 504, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state) and logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "Shoot the Messenger: Frozen Expansion", SC2HOTS_LOC_ID_OFFSET + 505, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state)),
        LocationData(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "Shoot the Messenger: Southwest Frozen Zerg", SC2HOTS_LOC_ID_OFFSET + 506, LocationType.EXTRA),
        LocationData(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "Shoot the Messenger: Southeast Frozen Zerg", SC2HOTS_LOC_ID_OFFSET + 507, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state) or adv_tactics),
        LocationData(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "Shoot the Messenger: West Frozen Zerg", SC2HOTS_LOC_ID_OFFSET + 508, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state) and logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.SHOOT_THE_MESSENGER.mission_name, "Shoot the Messenger: East Frozen Zerg", SC2HOTS_LOC_ID_OFFSET + 509, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state) and logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.ENEMY_WITHIN.mission_name, "Enemy Within: Victory", SC2HOTS_LOC_ID_OFFSET + 600, LocationType.VICTORY,
                     lambda state: logic.zerg_pass_vents(state)
                                   and (logic.story_tech_granted
                                        or state.has_any({item_names.ZERGLING_RAPTOR_STRAIN, item_names.ROACH,
                                                         item_names.HYDRALISK, item_names.INFESTOR}, player))
                     ),
        LocationData(SC2Mission.ENEMY_WITHIN.mission_name, "Enemy Within: Infest Giant Ursadon", SC2HOTS_LOC_ID_OFFSET + 601, LocationType.VANILLA,
                     lambda state: logic.zerg_pass_vents(state)),
        LocationData(SC2Mission.ENEMY_WITHIN.mission_name, "Enemy Within: First Niadra Evolution", SC2HOTS_LOC_ID_OFFSET + 602, LocationType.VANILLA,
                     lambda state: logic.zerg_pass_vents(state)),
        LocationData(SC2Mission.ENEMY_WITHIN.mission_name, "Enemy Within: Second Niadra Evolution", SC2HOTS_LOC_ID_OFFSET + 603, LocationType.VANILLA,
                     lambda state: logic.zerg_pass_vents(state)),
        LocationData(SC2Mission.ENEMY_WITHIN.mission_name, "Enemy Within: Third Niadra Evolution", SC2HOTS_LOC_ID_OFFSET + 604, LocationType.VANILLA,
                     lambda state: logic.zerg_pass_vents(state)),
        LocationData(SC2Mission.ENEMY_WITHIN.mission_name, "Enemy Within: Warp Drive", SC2HOTS_LOC_ID_OFFSET + 605, LocationType.EXTRA,
                     lambda state: logic.zerg_pass_vents(state)),
        LocationData(SC2Mission.ENEMY_WITHIN.mission_name, "Enemy Within: Stasis Quadrant", SC2HOTS_LOC_ID_OFFSET + 606, LocationType.EXTRA,
                     lambda state: logic.zerg_pass_vents(state)),
        LocationData(SC2Mission.DOMINATION.mission_name, "Domination: Victory", SC2HOTS_LOC_ID_OFFSET + 700, LocationType.VICTORY,
                     lambda state: logic.zerg_common_unit(state) and logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.DOMINATION.mission_name, "Domination: Center Infested Command Center", SC2HOTS_LOC_ID_OFFSET + 701, LocationType.VANILLA,
                     lambda state: logic.zerg_common_unit(state)),
        LocationData(SC2Mission.DOMINATION.mission_name, "Domination: North Infested Command Center", SC2HOTS_LOC_ID_OFFSET + 702, LocationType.VANILLA,
                     lambda state: logic.zerg_common_unit(state)),
        LocationData(SC2Mission.DOMINATION.mission_name, "Domination: Repel Zagara", SC2HOTS_LOC_ID_OFFSET + 703, LocationType.EXTRA),
        LocationData(SC2Mission.DOMINATION.mission_name, "Domination: Close Baneling Nest", SC2HOTS_LOC_ID_OFFSET + 704, LocationType.EXTRA),
        LocationData(SC2Mission.DOMINATION.mission_name, "Domination: South Baneling Nest", SC2HOTS_LOC_ID_OFFSET + 705, LocationType.EXTRA,
                     lambda state: adv_tactics or logic.zerg_common_unit(state)),
        LocationData(SC2Mission.DOMINATION.mission_name, "Domination: Southwest Baneling Nest", SC2HOTS_LOC_ID_OFFSET + 706, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state)),
        LocationData(SC2Mission.DOMINATION.mission_name, "Domination: Southeast Baneling Nest", SC2HOTS_LOC_ID_OFFSET + 707, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state) and logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.DOMINATION.mission_name, "Domination: North Baneling Nest", SC2HOTS_LOC_ID_OFFSET + 708, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state)),
        LocationData(SC2Mission.DOMINATION.mission_name, "Domination: Northeast Baneling Nest", SC2HOTS_LOC_ID_OFFSET + 709, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state)),
        LocationData(SC2Mission.FIRE_IN_THE_SKY.mission_name, "Fire in the Sky: Victory", SC2HOTS_LOC_ID_OFFSET + 800, LocationType.VICTORY,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_basic_anti_air(state) and
                                   logic.spread_creep(state)),
        LocationData(SC2Mission.FIRE_IN_THE_SKY.mission_name, "Fire in the Sky: West Biomass", SC2HOTS_LOC_ID_OFFSET + 801, LocationType.VANILLA),
        LocationData(SC2Mission.FIRE_IN_THE_SKY.mission_name, "Fire in the Sky: North Biomass", SC2HOTS_LOC_ID_OFFSET + 802, LocationType.VANILLA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_basic_anti_air(state) and
                                   logic.spread_creep(state)),
        LocationData(SC2Mission.FIRE_IN_THE_SKY.mission_name, "Fire in the Sky: South Biomass", SC2HOTS_LOC_ID_OFFSET + 803, LocationType.VANILLA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_basic_anti_air(state) and
                                   logic.spread_creep(state)),
        LocationData(SC2Mission.FIRE_IN_THE_SKY.mission_name, "Fire in the Sky: Destroy 3 Gorgons", SC2HOTS_LOC_ID_OFFSET + 804, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_basic_anti_air(state) and
                                   logic.spread_creep(state)),
        LocationData(SC2Mission.FIRE_IN_THE_SKY.mission_name, "Fire in the Sky: Close Zerg Rescue", SC2HOTS_LOC_ID_OFFSET + 805, LocationType.EXTRA),
        LocationData(SC2Mission.FIRE_IN_THE_SKY.mission_name, "Fire in the Sky: South Zerg Rescue", SC2HOTS_LOC_ID_OFFSET + 806, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state)),
        LocationData(SC2Mission.FIRE_IN_THE_SKY.mission_name, "Fire in the Sky: North Zerg Rescue", SC2HOTS_LOC_ID_OFFSET + 807, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_basic_anti_air(state) and
                                   logic.spread_creep(state)),
        LocationData(SC2Mission.FIRE_IN_THE_SKY.mission_name, "Fire in the Sky: West Queen Rescue", SC2HOTS_LOC_ID_OFFSET + 808, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_basic_anti_air(state) and
                                   logic.spread_creep(state)),
        LocationData(SC2Mission.FIRE_IN_THE_SKY.mission_name, "Fire in the Sky: East Queen Rescue", SC2HOTS_LOC_ID_OFFSET + 809, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_basic_anti_air(state) and
                                   logic.spread_creep(state)),
        LocationData(SC2Mission.OLD_SOLDIERS.mission_name, "Old Soldiers: Victory", SC2HOTS_LOC_ID_OFFSET + 900, LocationType.VICTORY,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.OLD_SOLDIERS.mission_name, "Old Soldiers: East Science Lab", SC2HOTS_LOC_ID_OFFSET + 901, LocationType.VANILLA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.OLD_SOLDIERS.mission_name, "Old Soldiers: North Science Lab", SC2HOTS_LOC_ID_OFFSET + 902, LocationType.VANILLA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.OLD_SOLDIERS.mission_name, "Old Soldiers: Get Nuked", SC2HOTS_LOC_ID_OFFSET + 903, LocationType.EXTRA),
        LocationData(SC2Mission.OLD_SOLDIERS.mission_name, "Old Soldiers: Entrance Gate", SC2HOTS_LOC_ID_OFFSET + 904, LocationType.EXTRA),
        LocationData(SC2Mission.OLD_SOLDIERS.mission_name, "Old Soldiers: Citadel Gate", SC2HOTS_LOC_ID_OFFSET + 905, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.OLD_SOLDIERS.mission_name, "Old Soldiers: South Expansion", SC2HOTS_LOC_ID_OFFSET + 906, LocationType.EXTRA),
        LocationData(SC2Mission.OLD_SOLDIERS.mission_name, "Old Soldiers: Rich Mineral Expansion", SC2HOTS_LOC_ID_OFFSET + 907, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.WAKING_THE_ANCIENT.mission_name, "Waking the Ancient: Victory", SC2HOTS_LOC_ID_OFFSET + 1000, LocationType.VICTORY,
                     lambda state: logic.zerg_common_unit(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.WAKING_THE_ANCIENT.mission_name, "Waking the Ancient: Center Essence Pool", SC2HOTS_LOC_ID_OFFSET + 1001, LocationType.VANILLA),
        LocationData(SC2Mission.WAKING_THE_ANCIENT.mission_name, "Waking the Ancient: East Essence Pool", SC2HOTS_LOC_ID_OFFSET + 1002, LocationType.VANILLA,
                     lambda state: logic.zerg_common_unit(state) and
                                   (adv_tactics and logic.zerg_basic_anti_air(state)
                                    or logic.zerg_competent_anti_air(state))),
        LocationData(SC2Mission.WAKING_THE_ANCIENT.mission_name, "Waking the Ancient: South Essence Pool", SC2HOTS_LOC_ID_OFFSET + 1003, LocationType.VANILLA,
                     lambda state: logic.zerg_common_unit(state) and
                                   (adv_tactics and logic.zerg_basic_anti_air(state)
                                    or logic.zerg_competent_anti_air(state))),
        LocationData(SC2Mission.WAKING_THE_ANCIENT.mission_name, "Waking the Ancient: Finish Feeding", SC2HOTS_LOC_ID_OFFSET + 1004, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.WAKING_THE_ANCIENT.mission_name, "Waking the Ancient: South Proxy Primal Hive", SC2HOTS_LOC_ID_OFFSET + 1005, LocationType.CHALLENGE,
                     lambda state: logic.zerg_common_unit(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.WAKING_THE_ANCIENT.mission_name, "Waking the Ancient: East Proxy Primal Hive", SC2HOTS_LOC_ID_OFFSET + 1006, LocationType.CHALLENGE,
                     lambda state: logic.zerg_common_unit(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.WAKING_THE_ANCIENT.mission_name, "Waking the Ancient: South Main Primal Hive", SC2HOTS_LOC_ID_OFFSET + 1007, LocationType.CHALLENGE,
                     lambda state: logic.zerg_common_unit(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.WAKING_THE_ANCIENT.mission_name, "Waking the Ancient: East Main Primal Hive", SC2HOTS_LOC_ID_OFFSET + 1008, LocationType.CHALLENGE,
                     lambda state: logic.zerg_common_unit(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.THE_CRUCIBLE.mission_name, "The Crucible: Victory", SC2HOTS_LOC_ID_OFFSET + 1100, LocationType.VICTORY,
                     lambda state: logic.zerg_competent_defense(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.THE_CRUCIBLE.mission_name, "The Crucible: Tyrannozor", SC2HOTS_LOC_ID_OFFSET + 1101, LocationType.VANILLA,
                     lambda state: logic.zerg_competent_defense(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.THE_CRUCIBLE.mission_name, "The Crucible: Reach the Pool", SC2HOTS_LOC_ID_OFFSET + 1102, LocationType.VANILLA),
        LocationData(SC2Mission.THE_CRUCIBLE.mission_name, "The Crucible: 15 Minutes Remaining", SC2HOTS_LOC_ID_OFFSET + 1103, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_defense(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.THE_CRUCIBLE.mission_name, "The Crucible: 5 Minutes Remaining", SC2HOTS_LOC_ID_OFFSET + 1104, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_defense(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.THE_CRUCIBLE.mission_name, "The Crucible: Pincer Attack", SC2HOTS_LOC_ID_OFFSET + 1105, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_defense(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.THE_CRUCIBLE.mission_name, "The Crucible: Yagdra Claims Brakk's Pack", SC2HOTS_LOC_ID_OFFSET + 1106, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_defense(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.SUPREME.mission_name, "Supreme: Victory", SC2HOTS_LOC_ID_OFFSET + 1200, LocationType.VICTORY,
                     lambda state: logic.supreme_requirement(state)),
        LocationData(SC2Mission.SUPREME.mission_name, "Supreme: First Relic", SC2HOTS_LOC_ID_OFFSET + 1201, LocationType.VANILLA,
                     lambda state: logic.supreme_requirement(state)),
        LocationData(SC2Mission.SUPREME.mission_name, "Supreme: Second Relic", SC2HOTS_LOC_ID_OFFSET + 1202, LocationType.VANILLA,
                     lambda state: logic.supreme_requirement(state)),
        LocationData(SC2Mission.SUPREME.mission_name, "Supreme: Third Relic", SC2HOTS_LOC_ID_OFFSET + 1203, LocationType.VANILLA,
                     lambda state: logic.supreme_requirement(state)),
        LocationData(SC2Mission.SUPREME.mission_name, "Supreme: Fourth Relic", SC2HOTS_LOC_ID_OFFSET + 1204, LocationType.VANILLA,
                     lambda state: logic.supreme_requirement(state)),
        LocationData(SC2Mission.SUPREME.mission_name, "Supreme: Yagdra", SC2HOTS_LOC_ID_OFFSET + 1205, LocationType.EXTRA,
                     lambda state: logic.supreme_requirement(state)),
        LocationData(SC2Mission.SUPREME.mission_name, "Supreme: Kraith", SC2HOTS_LOC_ID_OFFSET + 1206, LocationType.EXTRA,
                     lambda state: logic.supreme_requirement(state)),
        LocationData(SC2Mission.SUPREME.mission_name, "Supreme: Slivan", SC2HOTS_LOC_ID_OFFSET + 1207, LocationType.EXTRA,
                     lambda state: logic.supreme_requirement(state)),
        LocationData(SC2Mission.INFESTED.mission_name, "Infested: Victory", SC2HOTS_LOC_ID_OFFSET + 1300, LocationType.VICTORY,
                     lambda state: logic.zerg_common_unit(state) and
                                   ((logic.zerg_competent_anti_air(state) and state.has(item_names.INFESTOR, player)) or
                                   (adv_tactics and logic.zerg_basic_anti_air(state)))),
        LocationData(SC2Mission.INFESTED.mission_name, "Infested: East Science Facility", SC2HOTS_LOC_ID_OFFSET + 1301, LocationType.VANILLA,
                     lambda state: logic.zerg_common_unit(state) and
                                   logic.zerg_basic_anti_air(state) and
                                   logic.spread_creep(state)),
        LocationData(SC2Mission.INFESTED.mission_name, "Infested: Center Science Facility", SC2HOTS_LOC_ID_OFFSET + 1302, LocationType.VANILLA,
                     lambda state: logic.zerg_common_unit(state) and
                                   logic.zerg_basic_anti_air(state) and
                                   logic.spread_creep(state)),
        LocationData(SC2Mission.INFESTED.mission_name, "Infested: West Science Facility", SC2HOTS_LOC_ID_OFFSET + 1303, LocationType.VANILLA,
                     lambda state: logic.zerg_common_unit(state) and
                                   logic.zerg_basic_anti_air(state) and
                                   logic.spread_creep(state)),
        LocationData(SC2Mission.INFESTED.mission_name, "Infested: First Intro Garrison", SC2HOTS_LOC_ID_OFFSET + 1304, LocationType.EXTRA),
        LocationData(SC2Mission.INFESTED.mission_name, "Infested: Second Intro Garrison", SC2HOTS_LOC_ID_OFFSET + 1305, LocationType.EXTRA),
        LocationData(SC2Mission.INFESTED.mission_name, "Infested: Base Garrison", SC2HOTS_LOC_ID_OFFSET + 1306, LocationType.EXTRA),
        LocationData(SC2Mission.INFESTED.mission_name, "Infested: East Garrison", SC2HOTS_LOC_ID_OFFSET + 1307, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state)
                                   and logic.zerg_basic_anti_air(state)
                                   and (adv_tactics or state.has(item_names.INFESTOR, player))),
        LocationData(SC2Mission.INFESTED.mission_name, "Infested: Mid Garrison", SC2HOTS_LOC_ID_OFFSET + 1308, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state)
                                   and logic.zerg_basic_anti_air(state)
                                   and (adv_tactics or state.has(item_names.INFESTOR, player))),
        LocationData(SC2Mission.INFESTED.mission_name, "Infested: North Garrison", SC2HOTS_LOC_ID_OFFSET + 1309, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state)
                                   and logic.zerg_basic_anti_air(state)
                                   and (adv_tactics or state.has(item_names.INFESTOR, player))),
        LocationData(SC2Mission.INFESTED.mission_name, "Infested: Close Southwest Garrison", SC2HOTS_LOC_ID_OFFSET + 1310, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state)
                                   and logic.zerg_basic_anti_air(state)
                                   and (adv_tactics or state.has(item_names.INFESTOR, player))),
        LocationData(SC2Mission.INFESTED.mission_name, "Infested: Far Southwest Garrison", SC2HOTS_LOC_ID_OFFSET + 1311, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state)
                                   and logic.zerg_basic_anti_air(state)
                                   and (adv_tactics or state.has(item_names.INFESTOR, player))),
        LocationData(SC2Mission.HAND_OF_DARKNESS.mission_name, "Hand of Darkness: Victory", SC2HOTS_LOC_ID_OFFSET + 1400, LocationType.VICTORY,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.HAND_OF_DARKNESS.mission_name, "Hand of Darkness: North Brutalisk", SC2HOTS_LOC_ID_OFFSET + 1401, LocationType.VANILLA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.HAND_OF_DARKNESS.mission_name, "Hand of Darkness: South Brutalisk", SC2HOTS_LOC_ID_OFFSET + 1402, LocationType.VANILLA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.HAND_OF_DARKNESS.mission_name, "Hand of Darkness: Kill 1 Hybrid", SC2HOTS_LOC_ID_OFFSET + 1403, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.HAND_OF_DARKNESS.mission_name, "Hand of Darkness: Kill 2 Hybrid", SC2HOTS_LOC_ID_OFFSET + 1404, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.HAND_OF_DARKNESS.mission_name, "Hand of Darkness: Kill 3 Hybrid", SC2HOTS_LOC_ID_OFFSET + 1405, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.HAND_OF_DARKNESS.mission_name, "Hand of Darkness: Kill 4 Hybrid", SC2HOTS_LOC_ID_OFFSET + 1406, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.HAND_OF_DARKNESS.mission_name, "Hand of Darkness: Kill 5 Hybrid", SC2HOTS_LOC_ID_OFFSET + 1407, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.HAND_OF_DARKNESS.mission_name, "Hand of Darkness: Kill 6 Hybrid", SC2HOTS_LOC_ID_OFFSET + 1408, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.HAND_OF_DARKNESS.mission_name, "Hand of Darkness: Kill 7 Hybrid", SC2HOTS_LOC_ID_OFFSET + 1409, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_basic_anti_air(state)),
        LocationData(SC2Mission.PHANTOMS_OF_THE_VOID.mission_name, "Phantoms of the Void: Victory", SC2HOTS_LOC_ID_OFFSET + 1500, LocationType.VICTORY,
                     lambda state: logic.zerg_competent_comp(state) and
                                   (logic.zerg_competent_anti_air(state) or adv_tactics)),
        LocationData(SC2Mission.PHANTOMS_OF_THE_VOID.mission_name, "Phantoms of the Void: Northwest Crystal", SC2HOTS_LOC_ID_OFFSET + 1501, LocationType.VANILLA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   (logic.zerg_competent_anti_air(state) or adv_tactics)),
        LocationData(SC2Mission.PHANTOMS_OF_THE_VOID.mission_name, "Phantoms of the Void: Northeast Crystal", SC2HOTS_LOC_ID_OFFSET + 1502, LocationType.VANILLA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   (logic.zerg_competent_anti_air(state) or adv_tactics)),
        LocationData(SC2Mission.PHANTOMS_OF_THE_VOID.mission_name, "Phantoms of the Void: South Crystal", SC2HOTS_LOC_ID_OFFSET + 1503, LocationType.VANILLA),
        LocationData(SC2Mission.PHANTOMS_OF_THE_VOID.mission_name, "Phantoms of the Void: Base Established", SC2HOTS_LOC_ID_OFFSET + 1504, LocationType.EXTRA),
        LocationData(SC2Mission.PHANTOMS_OF_THE_VOID.mission_name, "Phantoms of the Void: Close Temple", SC2HOTS_LOC_ID_OFFSET + 1505, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   (logic.zerg_competent_anti_air(state) or adv_tactics)),
        LocationData(SC2Mission.PHANTOMS_OF_THE_VOID.mission_name, "Phantoms of the Void: Mid Temple", SC2HOTS_LOC_ID_OFFSET + 1506, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   (logic.zerg_competent_anti_air(state) or adv_tactics)),
        LocationData(SC2Mission.PHANTOMS_OF_THE_VOID.mission_name, "Phantoms of the Void: Southeast Temple", SC2HOTS_LOC_ID_OFFSET + 1507, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   (logic.zerg_competent_anti_air(state) or adv_tactics)),
        LocationData(SC2Mission.PHANTOMS_OF_THE_VOID.mission_name, "Phantoms of the Void: Northeast Temple", SC2HOTS_LOC_ID_OFFSET + 1508, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   (logic.zerg_competent_anti_air(state) or adv_tactics)),
        LocationData(SC2Mission.PHANTOMS_OF_THE_VOID.mission_name, "Phantoms of the Void: Northwest Temple", SC2HOTS_LOC_ID_OFFSET + 1509, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   (logic.zerg_competent_anti_air(state) or adv_tactics)),
        LocationData(SC2Mission.WITH_FRIENDS_LIKE_THESE.mission_name, "With Friends Like These: Victory", SC2HOTS_LOC_ID_OFFSET + 1600, LocationType.VICTORY),
        LocationData(SC2Mission.WITH_FRIENDS_LIKE_THESE.mission_name, "With Friends Like These: Pirate Capital Ship", SC2HOTS_LOC_ID_OFFSET + 1601, LocationType.VANILLA),
        LocationData(SC2Mission.WITH_FRIENDS_LIKE_THESE.mission_name, "With Friends Like These: First Mineral Patch", SC2HOTS_LOC_ID_OFFSET + 1602, LocationType.VANILLA),
        LocationData(SC2Mission.WITH_FRIENDS_LIKE_THESE.mission_name, "With Friends Like These: Second Mineral Patch", SC2HOTS_LOC_ID_OFFSET + 1603, LocationType.VANILLA),
        LocationData(SC2Mission.WITH_FRIENDS_LIKE_THESE.mission_name, "With Friends Like These: Third Mineral Patch", SC2HOTS_LOC_ID_OFFSET + 1604, LocationType.VANILLA),
        LocationData(SC2Mission.CONVICTION.mission_name, "Conviction: Victory", SC2HOTS_LOC_ID_OFFSET + 1700, LocationType.VICTORY,
                     lambda state: logic.two_kerrigan_actives(state) and
                                   (logic.basic_kerrigan(state) or logic.story_tech_granted) or kerriganless),
        LocationData(SC2Mission.CONVICTION.mission_name, "Conviction: First Secret Documents", SC2HOTS_LOC_ID_OFFSET + 1701, LocationType.VANILLA,
                     lambda state: logic.two_kerrigan_actives(state) or kerriganless),
        LocationData(SC2Mission.CONVICTION.mission_name, "Conviction: Second Secret Documents", SC2HOTS_LOC_ID_OFFSET + 1702, LocationType.VANILLA,
                     lambda state: logic.two_kerrigan_actives(state) and
                                   (logic.basic_kerrigan(state) or logic.story_tech_granted) or kerriganless),
        LocationData(SC2Mission.CONVICTION.mission_name, "Conviction: Power Coupling", SC2HOTS_LOC_ID_OFFSET + 1703, LocationType.EXTRA,
                     lambda state: logic.two_kerrigan_actives(state) or kerriganless),
        LocationData(SC2Mission.CONVICTION.mission_name, "Conviction: Door Blasted", SC2HOTS_LOC_ID_OFFSET + 1704, LocationType.EXTRA,
                     lambda state: logic.two_kerrigan_actives(state) or kerriganless),
        LocationData(SC2Mission.PLANETFALL.mission_name, "Planetfall: Victory", SC2HOTS_LOC_ID_OFFSET + 1800, LocationType.VICTORY,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.PLANETFALL.mission_name, "Planetfall: East Gate", SC2HOTS_LOC_ID_OFFSET + 1801, LocationType.VANILLA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.PLANETFALL.mission_name, "Planetfall: Northwest Gate", SC2HOTS_LOC_ID_OFFSET + 1802, LocationType.VANILLA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.PLANETFALL.mission_name, "Planetfall: North Gate", SC2HOTS_LOC_ID_OFFSET + 1803, LocationType.VANILLA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.PLANETFALL.mission_name, "Planetfall: 1 Bile Launcher Deployed", SC2HOTS_LOC_ID_OFFSET + 1804, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.PLANETFALL.mission_name, "Planetfall: 2 Bile Launchers Deployed", SC2HOTS_LOC_ID_OFFSET + 1805, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.PLANETFALL.mission_name, "Planetfall: 3 Bile Launchers Deployed", SC2HOTS_LOC_ID_OFFSET + 1806, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.PLANETFALL.mission_name, "Planetfall: 4 Bile Launchers Deployed", SC2HOTS_LOC_ID_OFFSET + 1807, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.PLANETFALL.mission_name, "Planetfall: 5 Bile Launchers Deployed", SC2HOTS_LOC_ID_OFFSET + 1808, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.PLANETFALL.mission_name, "Planetfall: Sons of Korhal", SC2HOTS_LOC_ID_OFFSET + 1809, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.PLANETFALL.mission_name, "Planetfall: Night Wolves", SC2HOTS_LOC_ID_OFFSET + 1810, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.PLANETFALL.mission_name, "Planetfall: West Expansion", SC2HOTS_LOC_ID_OFFSET + 1811, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.PLANETFALL.mission_name, "Planetfall: Mid Expansion", SC2HOTS_LOC_ID_OFFSET + 1812, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.DEATH_FROM_ABOVE.mission_name, "Death From Above: Victory", SC2HOTS_LOC_ID_OFFSET + 1900, LocationType.VICTORY,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.DEATH_FROM_ABOVE.mission_name, "Death From Above: First Power Link", SC2HOTS_LOC_ID_OFFSET + 1901, LocationType.VANILLA),
        LocationData(SC2Mission.DEATH_FROM_ABOVE.mission_name, "Death From Above: Second Power Link", SC2HOTS_LOC_ID_OFFSET + 1902, LocationType.VANILLA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.DEATH_FROM_ABOVE.mission_name, "Death From Above: Third Power Link", SC2HOTS_LOC_ID_OFFSET + 1903, LocationType.VANILLA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.DEATH_FROM_ABOVE.mission_name, "Death From Above: Expansion Command Center", SC2HOTS_LOC_ID_OFFSET + 1904, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.DEATH_FROM_ABOVE.mission_name, "Death From Above: Main Path Command Center", SC2HOTS_LOC_ID_OFFSET + 1905, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_comp(state) and
                                   logic.zerg_competent_anti_air(state)),
        LocationData(SC2Mission.THE_RECKONING.mission_name, "The Reckoning: Victory", SC2HOTS_LOC_ID_OFFSET + 2000, LocationType.VICTORY,
                     lambda state: logic.the_reckoning_requirement(state)),
        LocationData(SC2Mission.THE_RECKONING.mission_name, "The Reckoning: South Lane", SC2HOTS_LOC_ID_OFFSET + 2001, LocationType.VANILLA,
                     lambda state: logic.the_reckoning_requirement(state)),
        LocationData(SC2Mission.THE_RECKONING.mission_name, "The Reckoning: North Lane", SC2HOTS_LOC_ID_OFFSET + 2002, LocationType.VANILLA,
                     lambda state: logic.the_reckoning_requirement(state)),
        LocationData(SC2Mission.THE_RECKONING.mission_name, "The Reckoning: East Lane", SC2HOTS_LOC_ID_OFFSET + 2003, LocationType.VANILLA,
                     lambda state: logic.the_reckoning_requirement(state)),
        LocationData(SC2Mission.THE_RECKONING.mission_name, "The Reckoning: Odin", SC2HOTS_LOC_ID_OFFSET + 2004, LocationType.EXTRA,
                     lambda state: logic.the_reckoning_requirement(state)),

        # LotV Prologue
        LocationData(SC2Mission.DARK_WHISPERS.mission_name, "Dark Whispers: Victory", SC2LOTV_LOC_ID_OFFSET + 100, LocationType.VICTORY,
                     lambda state: logic.protoss_common_unit(state) \
                                   and logic.protoss_basic_anti_air(state)),
        LocationData(SC2Mission.DARK_WHISPERS.mission_name, "Dark Whispers: First Prisoner Group", SC2LOTV_LOC_ID_OFFSET + 101, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state) \
                                   and logic.protoss_basic_anti_air(state)),
        LocationData(SC2Mission.DARK_WHISPERS.mission_name, "Dark Whispers: Second Prisoner Group", SC2LOTV_LOC_ID_OFFSET + 102, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state) \
                                   and logic.protoss_basic_anti_air(state)),
        LocationData(SC2Mission.DARK_WHISPERS.mission_name, "Dark Whispers: First Pylon", SC2LOTV_LOC_ID_OFFSET + 103, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state) \
                                   and logic.protoss_basic_anti_air(state)),
        LocationData(SC2Mission.DARK_WHISPERS.mission_name, "Dark Whispers: Second Pylon", SC2LOTV_LOC_ID_OFFSET + 104, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state) \
                                   and logic.protoss_basic_anti_air(state)),
        LocationData(SC2Mission.GHOSTS_IN_THE_FOG.mission_name, "Ghosts in the Fog: Victory", SC2LOTV_LOC_ID_OFFSET + 200, LocationType.VICTORY,
                     lambda state: logic.protoss_common_unit(state) \
                                   and logic.protoss_anti_armor_anti_air(state)),
        LocationData(SC2Mission.GHOSTS_IN_THE_FOG.mission_name, "Ghosts in the Fog: South Rock Formation", SC2LOTV_LOC_ID_OFFSET + 201, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state) \
                                   and logic.protoss_anti_armor_anti_air(state)),
        LocationData(SC2Mission.GHOSTS_IN_THE_FOG.mission_name, "Ghosts in the Fog: West Rock Formation", SC2LOTV_LOC_ID_OFFSET + 202, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state) \
                                   and logic.protoss_anti_armor_anti_air(state)),
        LocationData(SC2Mission.GHOSTS_IN_THE_FOG.mission_name, "Ghosts in the Fog: East Rock Formation", SC2LOTV_LOC_ID_OFFSET + 203, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state) \
                                   and logic.protoss_anti_armor_anti_air(state) \
                                   and logic.protoss_can_attack_behind_chasm(state)),
        LocationData(SC2Mission.EVIL_AWOKEN.mission_name, "Evil Awoken: Victory", SC2LOTV_LOC_ID_OFFSET + 300, LocationType.VICTORY),
        LocationData(SC2Mission.EVIL_AWOKEN.mission_name, "Evil Awoken: Temple Investigated", SC2LOTV_LOC_ID_OFFSET + 301, LocationType.EXTRA),
        LocationData(SC2Mission.EVIL_AWOKEN.mission_name, "Evil Awoken: Void Catalyst", SC2LOTV_LOC_ID_OFFSET + 302, LocationType.EXTRA),
        LocationData(SC2Mission.EVIL_AWOKEN.mission_name, "Evil Awoken: First Particle Cannon", SC2LOTV_LOC_ID_OFFSET + 303, LocationType.VANILLA),
        LocationData(SC2Mission.EVIL_AWOKEN.mission_name, "Evil Awoken: Second Particle Cannon", SC2LOTV_LOC_ID_OFFSET + 304, LocationType.VANILLA),
        LocationData(SC2Mission.EVIL_AWOKEN.mission_name, "Evil Awoken: Third Particle Cannon", SC2LOTV_LOC_ID_OFFSET + 305, LocationType.VANILLA),


        # LotV
        LocationData(SC2Mission.FOR_AIUR.mission_name, "For Aiur!: Victory", SC2LOTV_LOC_ID_OFFSET + 400, LocationType.VICTORY),
        LocationData(SC2Mission.FOR_AIUR.mission_name, "For Aiur!: Southwest Hive", SC2LOTV_LOC_ID_OFFSET + 401, LocationType.VANILLA),
        LocationData(SC2Mission.FOR_AIUR.mission_name, "For Aiur!: Northwest Hive", SC2LOTV_LOC_ID_OFFSET + 402, LocationType.VANILLA),
        LocationData(SC2Mission.FOR_AIUR.mission_name, "For Aiur!: Northeast Hive", SC2LOTV_LOC_ID_OFFSET + 403, LocationType.VANILLA),
        LocationData(SC2Mission.FOR_AIUR.mission_name, "For Aiur!: East Hive", SC2LOTV_LOC_ID_OFFSET + 404, LocationType.VANILLA),
        LocationData(SC2Mission.FOR_AIUR.mission_name, "For Aiur!: West Conduit", SC2LOTV_LOC_ID_OFFSET + 405, LocationType.EXTRA),
        LocationData(SC2Mission.FOR_AIUR.mission_name, "For Aiur!: Middle Conduit", SC2LOTV_LOC_ID_OFFSET + 406, LocationType.EXTRA),
        LocationData(SC2Mission.FOR_AIUR.mission_name, "For Aiur!: Northeast Conduit", SC2LOTV_LOC_ID_OFFSET + 407, LocationType.EXTRA),
        LocationData(SC2Mission.THE_GROWING_SHADOW.mission_name, "The Growing Shadow: Victory", SC2LOTV_LOC_ID_OFFSET + 500, LocationType.VICTORY,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_basic_anti_air(state)),
        LocationData(SC2Mission.THE_GROWING_SHADOW.mission_name, "The Growing Shadow: Close Pylon", SC2LOTV_LOC_ID_OFFSET + 501, LocationType.VANILLA),
        LocationData(SC2Mission.THE_GROWING_SHADOW.mission_name, "The Growing Shadow: East Pylon", SC2LOTV_LOC_ID_OFFSET + 502, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_basic_anti_air(state)),
        LocationData(SC2Mission.THE_GROWING_SHADOW.mission_name, "The Growing Shadow: West Pylon", SC2LOTV_LOC_ID_OFFSET + 503, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_basic_anti_air(state)),
        LocationData(SC2Mission.THE_GROWING_SHADOW.mission_name, "The Growing Shadow: Nexus", SC2LOTV_LOC_ID_OFFSET + 504, LocationType.EXTRA),
        LocationData(SC2Mission.THE_GROWING_SHADOW.mission_name, "The Growing Shadow: Templar Base", SC2LOTV_LOC_ID_OFFSET + 505, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_basic_anti_air(state)),
        LocationData(SC2Mission.THE_SPEAR_OF_ADUN.mission_name, "The Spear of Adun: Victory", SC2LOTV_LOC_ID_OFFSET + 600, LocationType.VICTORY,
                     lambda state: logic.protoss_common_unit(state)
                                    and logic.protoss_anti_light_anti_air(state)),
        LocationData(SC2Mission.THE_SPEAR_OF_ADUN.mission_name, "The Spear of Adun: Close Warp Gate", SC2LOTV_LOC_ID_OFFSET + 601, LocationType.VANILLA),
        LocationData(SC2Mission.THE_SPEAR_OF_ADUN.mission_name, "The Spear of Adun: West Warp Gate", SC2LOTV_LOC_ID_OFFSET + 602, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_light_anti_air(state)),
        LocationData(SC2Mission.THE_SPEAR_OF_ADUN.mission_name, "The Spear of Adun: North Warp Gate", SC2LOTV_LOC_ID_OFFSET + 603, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_light_anti_air(state)),
        LocationData(SC2Mission.THE_SPEAR_OF_ADUN.mission_name, "The Spear of Adun: North Power Cell", SC2LOTV_LOC_ID_OFFSET + 604, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_light_anti_air(state)),
        LocationData(SC2Mission.THE_SPEAR_OF_ADUN.mission_name, "The Spear of Adun: East Power Cell", SC2LOTV_LOC_ID_OFFSET + 605, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_light_anti_air(state)),
        LocationData(SC2Mission.THE_SPEAR_OF_ADUN.mission_name, "The Spear of Adun: South Power Cell", SC2LOTV_LOC_ID_OFFSET + 606, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_light_anti_air(state)),
        LocationData(SC2Mission.THE_SPEAR_OF_ADUN.mission_name, "The Spear of Adun: Southeast Power Cell", SC2LOTV_LOC_ID_OFFSET + 607, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_light_anti_air(state)),
        LocationData(SC2Mission.SKY_SHIELD.mission_name, "Sky Shield: Victory", SC2LOTV_LOC_ID_OFFSET + 700, LocationType.VICTORY,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_basic_anti_air(state)),
        LocationData(SC2Mission.SKY_SHIELD.mission_name, "Sky Shield: Mid EMP Scrambler", SC2LOTV_LOC_ID_OFFSET + 701, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_basic_anti_air(state)),
        LocationData(SC2Mission.SKY_SHIELD.mission_name, "Sky Shield: Southeast EMP Scrambler", SC2LOTV_LOC_ID_OFFSET + 702, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_basic_anti_air(state)),
        LocationData(SC2Mission.SKY_SHIELD.mission_name, "Sky Shield: North EMP Scrambler", SC2LOTV_LOC_ID_OFFSET + 703, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_basic_anti_air(state)),
        LocationData(SC2Mission.SKY_SHIELD.mission_name, "Sky Shield: Mid Stabilizer", SC2LOTV_LOC_ID_OFFSET + 704, LocationType.EXTRA),
        LocationData(SC2Mission.SKY_SHIELD.mission_name, "Sky Shield: Southwest Stabilizer", SC2LOTV_LOC_ID_OFFSET + 705, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_basic_anti_air(state)),
        LocationData(SC2Mission.SKY_SHIELD.mission_name, "Sky Shield: Northwest Stabilizer", SC2LOTV_LOC_ID_OFFSET + 706, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_basic_anti_air(state)),
        LocationData(SC2Mission.SKY_SHIELD.mission_name, "Sky Shield: Northeast Stabilizer", SC2LOTV_LOC_ID_OFFSET + 707, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_basic_anti_air(state)),
        LocationData(SC2Mission.SKY_SHIELD.mission_name, "Sky Shield: Southeast Stabilizer", SC2LOTV_LOC_ID_OFFSET + 708, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_basic_anti_air(state)),
        LocationData(SC2Mission.SKY_SHIELD.mission_name, "Sky Shield: West Raynor Base", SC2LOTV_LOC_ID_OFFSET + 709, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_basic_anti_air(state)),
        LocationData(SC2Mission.SKY_SHIELD.mission_name, "Sky Shield: East Raynor Base", SC2LOTV_LOC_ID_OFFSET + 710, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_basic_anti_air(state)),
        LocationData(SC2Mission.BROTHERS_IN_ARMS.mission_name, "Brothers in Arms: Victory", SC2LOTV_LOC_ID_OFFSET + 800, LocationType.VICTORY,
                     lambda state: logic.brothers_in_arms_requirement(state)),
        LocationData(SC2Mission.BROTHERS_IN_ARMS.mission_name, "Brothers in Arms: Mid Science Facility", SC2LOTV_LOC_ID_OFFSET + 801, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state) or logic.take_over_ai_allies),
        LocationData(SC2Mission.BROTHERS_IN_ARMS.mission_name, "Brothers in Arms: North Science Facility", SC2LOTV_LOC_ID_OFFSET + 802, LocationType.VANILLA,
                     lambda state: logic.brothers_in_arms_requirement(state)
                                   or logic.take_over_ai_allies
                                   and logic.advanced_tactics
                                   and (
                                           logic.terran_common_unit(state)
                                           or logic.protoss_common_unit(state)
                                   )
                     ),
        LocationData(SC2Mission.BROTHERS_IN_ARMS.mission_name, "Brothers in Arms: South Science Facility", SC2LOTV_LOC_ID_OFFSET + 803, LocationType.VANILLA,
                     lambda state: logic.brothers_in_arms_requirement(state)),
        LocationData(SC2Mission.AMON_S_REACH.mission_name, "Amon's Reach: Victory", SC2LOTV_LOC_ID_OFFSET + 900, LocationType.VICTORY,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_light_anti_air(state)),
        LocationData(SC2Mission.AMON_S_REACH.mission_name, "Amon's Reach: Close Solarite Reserve", SC2LOTV_LOC_ID_OFFSET + 901, LocationType.VANILLA),
        LocationData(SC2Mission.AMON_S_REACH.mission_name, "Amon's Reach: North Solarite Reserve", SC2LOTV_LOC_ID_OFFSET + 902, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_light_anti_air(state)),
        LocationData(SC2Mission.AMON_S_REACH.mission_name, "Amon's Reach: East Solarite Reserve", SC2LOTV_LOC_ID_OFFSET + 903, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_light_anti_air(state)),
        LocationData(SC2Mission.AMON_S_REACH.mission_name, "Amon's Reach: West Launch Bay", SC2LOTV_LOC_ID_OFFSET + 904, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_light_anti_air(state)),
        LocationData(SC2Mission.AMON_S_REACH.mission_name, "Amon's Reach: South Launch Bay", SC2LOTV_LOC_ID_OFFSET + 905, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_light_anti_air(state)),
        LocationData(SC2Mission.AMON_S_REACH.mission_name, "Amon's Reach: Northwest Launch Bay", SC2LOTV_LOC_ID_OFFSET + 906, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_light_anti_air(state)),
        LocationData(SC2Mission.AMON_S_REACH.mission_name, "Amon's Reach: East Launch Bay", SC2LOTV_LOC_ID_OFFSET + 907, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_light_anti_air(state)),
        LocationData(SC2Mission.LAST_STAND.mission_name, "Last Stand: Victory", SC2LOTV_LOC_ID_OFFSET + 1000, LocationType.VICTORY,
                     lambda state: logic.last_stand_requirement(state)),
        LocationData(SC2Mission.LAST_STAND.mission_name, "Last Stand: West Zenith Stone", SC2LOTV_LOC_ID_OFFSET + 1001, LocationType.VANILLA,
                     lambda state: logic.last_stand_requirement(state)),
        LocationData(SC2Mission.LAST_STAND.mission_name, "Last Stand: North Zenith Stone", SC2LOTV_LOC_ID_OFFSET + 1002, LocationType.VANILLA,
                     lambda state: logic.last_stand_requirement(state)),
        LocationData(SC2Mission.LAST_STAND.mission_name, "Last Stand: East Zenith Stone", SC2LOTV_LOC_ID_OFFSET + 1003, LocationType.VANILLA,
                     lambda state: logic.last_stand_requirement(state)),
        LocationData(SC2Mission.LAST_STAND.mission_name, "Last Stand: 1 Billion Zerg", SC2LOTV_LOC_ID_OFFSET + 1004, LocationType.EXTRA,
                     lambda state: logic.last_stand_requirement(state)),
        LocationData(SC2Mission.LAST_STAND.mission_name, "Last Stand: 1.5 Billion Zerg", SC2LOTV_LOC_ID_OFFSET + 1005, LocationType.VANILLA,
                     lambda state: logic.last_stand_requirement(state) and (
                         state.has_all({item_names.KHAYDARIN_MONOLITH, item_names.PHOTON_CANNON, item_names.SHIELD_BATTERY}, player)
                         or state.has_any({item_names.SOA_SOLAR_LANCE, item_names.SOA_DEPLOY_FENIX}, player)
                     )),
        LocationData(SC2Mission.FORBIDDEN_WEAPON.mission_name, "Forbidden Weapon: Victory", SC2LOTV_LOC_ID_OFFSET + 1100, LocationType.VICTORY,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_armor_anti_air(state)),
        LocationData(SC2Mission.FORBIDDEN_WEAPON.mission_name, "Forbidden Weapon: South Solarite", SC2LOTV_LOC_ID_OFFSET + 1101, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_armor_anti_air(state)),
        LocationData(SC2Mission.FORBIDDEN_WEAPON.mission_name, "Forbidden Weapon: North Solarite", SC2LOTV_LOC_ID_OFFSET + 1102, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_armor_anti_air(state)),
        LocationData(SC2Mission.FORBIDDEN_WEAPON.mission_name, "Forbidden Weapon: Northwest Solarite", SC2LOTV_LOC_ID_OFFSET + 1103, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_armor_anti_air(state)),
        LocationData(SC2Mission.TEMPLE_OF_UNIFICATION.mission_name, "Temple of Unification: Victory", SC2LOTV_LOC_ID_OFFSET + 1200, LocationType.VICTORY,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_armor_anti_air(state)),
        LocationData(SC2Mission.TEMPLE_OF_UNIFICATION.mission_name, "Temple of Unification: Mid Celestial Lock", SC2LOTV_LOC_ID_OFFSET + 1201, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_armor_anti_air(state)),
        LocationData(SC2Mission.TEMPLE_OF_UNIFICATION.mission_name, "Temple of Unification: West Celestial Lock", SC2LOTV_LOC_ID_OFFSET + 1202, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_armor_anti_air(state)),
        LocationData(SC2Mission.TEMPLE_OF_UNIFICATION.mission_name, "Temple of Unification: South Celestial Lock", SC2LOTV_LOC_ID_OFFSET + 1203, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_armor_anti_air(state)),
        LocationData(SC2Mission.TEMPLE_OF_UNIFICATION.mission_name, "Temple of Unification: East Celestial Lock", SC2LOTV_LOC_ID_OFFSET + 1204, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_armor_anti_air(state)),
        LocationData(SC2Mission.TEMPLE_OF_UNIFICATION.mission_name, "Temple of Unification: North Celestial Lock", SC2LOTV_LOC_ID_OFFSET + 1205, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_armor_anti_air(state)),
        LocationData(SC2Mission.TEMPLE_OF_UNIFICATION.mission_name, "Temple of Unification: Titanic Warp Prism", SC2LOTV_LOC_ID_OFFSET + 1206, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state)
                                   and logic.protoss_anti_armor_anti_air(state)),
        LocationData(SC2Mission.THE_INFINITE_CYCLE.mission_name, "The Infinite Cycle: Victory", SC2LOTV_LOC_ID_OFFSET + 1300, LocationType.VICTORY,
                     lambda state: logic.the_infinite_cycle_requirement(state)),
        LocationData(SC2Mission.THE_INFINITE_CYCLE.mission_name, "The Infinite Cycle: First Hall of Revelation", SC2LOTV_LOC_ID_OFFSET + 1301, LocationType.EXTRA,
                     lambda state: logic.the_infinite_cycle_requirement(state)),
        LocationData(SC2Mission.THE_INFINITE_CYCLE.mission_name, "The Infinite Cycle: Second Hall of Revelation", SC2LOTV_LOC_ID_OFFSET + 1302, LocationType.EXTRA,
                     lambda state: logic.the_infinite_cycle_requirement(state)),
        LocationData(SC2Mission.THE_INFINITE_CYCLE.mission_name, "The Infinite Cycle: First Xel'Naga Device", SC2LOTV_LOC_ID_OFFSET + 1303, LocationType.VANILLA,
                     lambda state: logic.the_infinite_cycle_requirement(state)),
        LocationData(SC2Mission.THE_INFINITE_CYCLE.mission_name, "The Infinite Cycle: Second Xel'Naga Device", SC2LOTV_LOC_ID_OFFSET + 1304, LocationType.VANILLA,
                     lambda state: logic.the_infinite_cycle_requirement(state)),
        LocationData(SC2Mission.THE_INFINITE_CYCLE.mission_name, "The Infinite Cycle: Third Xel'Naga Device", SC2LOTV_LOC_ID_OFFSET + 1305, LocationType.VANILLA,
                     lambda state: logic.the_infinite_cycle_requirement(state)),
        LocationData(SC2Mission.HARBINGER_OF_OBLIVION.mission_name, "Harbinger of Oblivion: Victory", SC2LOTV_LOC_ID_OFFSET + 1400, LocationType.VICTORY,
                     lambda state: logic.harbinger_of_oblivion_requirement(state)),
        LocationData(SC2Mission.HARBINGER_OF_OBLIVION.mission_name, "Harbinger of Oblivion: Artanis", SC2LOTV_LOC_ID_OFFSET + 1401, LocationType.EXTRA),
        LocationData(SC2Mission.HARBINGER_OF_OBLIVION.mission_name, "Harbinger of Oblivion: Northwest Void Crystal", SC2LOTV_LOC_ID_OFFSET + 1402, LocationType.EXTRA,
                     lambda state: logic.harbinger_of_oblivion_requirement(state)),
        LocationData(SC2Mission.HARBINGER_OF_OBLIVION.mission_name, "Harbinger of Oblivion: Northeast Void Crystal", SC2LOTV_LOC_ID_OFFSET + 1403, LocationType.EXTRA,
                     lambda state: logic.harbinger_of_oblivion_requirement(state)),
        LocationData(SC2Mission.HARBINGER_OF_OBLIVION.mission_name, "Harbinger of Oblivion: Southwest Void Crystal", SC2LOTV_LOC_ID_OFFSET + 1404, LocationType.EXTRA,
                     lambda state: logic.harbinger_of_oblivion_requirement(state)),
        LocationData(SC2Mission.HARBINGER_OF_OBLIVION.mission_name, "Harbinger of Oblivion: Southeast Void Crystal", SC2LOTV_LOC_ID_OFFSET + 1405, LocationType.EXTRA,
                     lambda state: logic.harbinger_of_oblivion_requirement(state)),
        LocationData(SC2Mission.HARBINGER_OF_OBLIVION.mission_name, "Harbinger of Oblivion: South Xel'Naga Vessel", SC2LOTV_LOC_ID_OFFSET + 1406, LocationType.VANILLA),
        LocationData(SC2Mission.HARBINGER_OF_OBLIVION.mission_name, "Harbinger of Oblivion: Mid Xel'Naga Vessel", SC2LOTV_LOC_ID_OFFSET + 1407, LocationType.VANILLA,
                     lambda state: logic.harbinger_of_oblivion_requirement(state)),
        LocationData(SC2Mission.HARBINGER_OF_OBLIVION.mission_name, "Harbinger of Oblivion: North Xel'Naga Vessel", SC2LOTV_LOC_ID_OFFSET + 1408, LocationType.VANILLA,
                     lambda state: logic.harbinger_of_oblivion_requirement(state)),
        LocationData(SC2Mission.UNSEALING_THE_PAST.mission_name, "Unsealing the Past: Victory", SC2LOTV_LOC_ID_OFFSET + 1500, LocationType.VICTORY,
                     lambda state: logic.protoss_basic_splash(state)
                                   and logic.protoss_anti_light_anti_air(state)),
        LocationData(SC2Mission.UNSEALING_THE_PAST.mission_name, "Unsealing the Past: Zerg Cleared", SC2LOTV_LOC_ID_OFFSET + 1501, LocationType.EXTRA),
        LocationData(SC2Mission.UNSEALING_THE_PAST.mission_name, "Unsealing the Past: First Stasis Lock", SC2LOTV_LOC_ID_OFFSET + 1502, LocationType.EXTRA,
                     lambda state: logic.advanced_tactics \
                                   or logic.protoss_basic_splash(state)
                                   and logic.protoss_anti_light_anti_air(state)),
        LocationData(SC2Mission.UNSEALING_THE_PAST.mission_name, "Unsealing the Past: Second Stasis Lock", SC2LOTV_LOC_ID_OFFSET + 1503, LocationType.EXTRA,
                     lambda state: logic.protoss_basic_splash(state)
                                   and logic.protoss_anti_light_anti_air(state)),
        LocationData(SC2Mission.UNSEALING_THE_PAST.mission_name, "Unsealing the Past: Third Stasis Lock", SC2LOTV_LOC_ID_OFFSET + 1504, LocationType.EXTRA,
                     lambda state: logic.protoss_basic_splash(state)
                                   and logic.protoss_anti_light_anti_air(state)),
        LocationData(SC2Mission.UNSEALING_THE_PAST.mission_name, "Unsealing the Past: Fourth Stasis Lock", SC2LOTV_LOC_ID_OFFSET + 1505, LocationType.EXTRA,
                     lambda state: logic.protoss_basic_splash(state)
                                   and logic.protoss_anti_light_anti_air(state)),
        LocationData(SC2Mission.UNSEALING_THE_PAST.mission_name, "Unsealing the Past: South Power Core", SC2LOTV_LOC_ID_OFFSET + 1506, LocationType.VANILLA,
                     lambda state: logic.protoss_basic_splash(state)
                                   and logic.protoss_anti_light_anti_air(state)),
        LocationData(SC2Mission.UNSEALING_THE_PAST.mission_name, "Unsealing the Past: East Power Core", SC2LOTV_LOC_ID_OFFSET + 1507, LocationType.VANILLA,
                     lambda state: logic.protoss_basic_splash(state)
                                   and logic.protoss_anti_light_anti_air(state)),
        LocationData(SC2Mission.PURIFICATION.mission_name, "Purification: Victory", SC2LOTV_LOC_ID_OFFSET + 1600, LocationType.VICTORY,
                     lambda state: logic.protoss_competent_comp(state)),
        LocationData(SC2Mission.PURIFICATION.mission_name, "Purification: North Sector: West Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1601, LocationType.VANILLA,
                     lambda state: logic.protoss_competent_comp(state)),
        LocationData(SC2Mission.PURIFICATION.mission_name, "Purification: North Sector: Northeast Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1602, LocationType.EXTRA,
                     lambda state: logic.protoss_competent_comp(state)),
        LocationData(SC2Mission.PURIFICATION.mission_name, "Purification: North Sector: Southeast Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1603, LocationType.EXTRA,
                     lambda state: logic.protoss_competent_comp(state)),
        LocationData(SC2Mission.PURIFICATION.mission_name, "Purification: South Sector: West Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1604, LocationType.VANILLA,
                     lambda state: logic.protoss_competent_comp(state)),
        LocationData(SC2Mission.PURIFICATION.mission_name, "Purification: South Sector: North Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1605, LocationType.EXTRA,
                     lambda state: logic.protoss_competent_comp(state)),
        LocationData(SC2Mission.PURIFICATION.mission_name, "Purification: South Sector: East Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1606, LocationType.EXTRA,
                     lambda state: logic.protoss_competent_comp(state)),
        LocationData(SC2Mission.PURIFICATION.mission_name, "Purification: West Sector: West Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1607, LocationType.VANILLA,
                     lambda state: logic.protoss_competent_comp(state)),
        LocationData(SC2Mission.PURIFICATION.mission_name, "Purification: West Sector: Mid Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1608, LocationType.EXTRA,
                     lambda state: logic.protoss_competent_comp(state)),
        LocationData(SC2Mission.PURIFICATION.mission_name, "Purification: West Sector: East Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1609, LocationType.EXTRA,
                     lambda state: logic.protoss_competent_comp(state)),
        LocationData(SC2Mission.PURIFICATION.mission_name, "Purification: East Sector: North Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1610, LocationType.VANILLA,
                     lambda state: logic.protoss_competent_comp(state)),
        LocationData(SC2Mission.PURIFICATION.mission_name, "Purification: East Sector: West Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1611, LocationType.EXTRA,
                     lambda state: logic.protoss_competent_comp(state)),
        LocationData(SC2Mission.PURIFICATION.mission_name, "Purification: East Sector: South Null Circuit", SC2LOTV_LOC_ID_OFFSET + 1612, LocationType.EXTRA,
                     lambda state: logic.protoss_competent_comp(state)),
        LocationData(SC2Mission.PURIFICATION.mission_name, "Purification: Purifier Warden", SC2LOTV_LOC_ID_OFFSET + 1613, LocationType.VANILLA,
                     lambda state: logic.protoss_competent_comp(state)),
        LocationData(SC2Mission.STEPS_OF_THE_RITE.mission_name, "Steps of the Rite: Victory", SC2LOTV_LOC_ID_OFFSET + 1700, LocationType.VICTORY,
                     lambda state: logic.steps_of_the_rite_requirement(state)),
        LocationData(SC2Mission.STEPS_OF_THE_RITE.mission_name, "Steps of the Rite: First Terrazine Fog", SC2LOTV_LOC_ID_OFFSET + 1701, LocationType.EXTRA,
                     lambda state: logic.steps_of_the_rite_requirement(state)),
        LocationData(SC2Mission.STEPS_OF_THE_RITE.mission_name, "Steps of the Rite: Southwest Guardian", SC2LOTV_LOC_ID_OFFSET + 1702, LocationType.EXTRA,
                     lambda state: logic.steps_of_the_rite_requirement(state)),
        LocationData(SC2Mission.STEPS_OF_THE_RITE.mission_name, "Steps of the Rite: West Guardian", SC2LOTV_LOC_ID_OFFSET + 1703, LocationType.EXTRA,
                     lambda state: logic.steps_of_the_rite_requirement(state)),
        LocationData(SC2Mission.STEPS_OF_THE_RITE.mission_name, "Steps of the Rite: Northwest Guardian", SC2LOTV_LOC_ID_OFFSET + 1704, LocationType.EXTRA,
                     lambda state: logic.steps_of_the_rite_requirement(state)),
        LocationData(SC2Mission.STEPS_OF_THE_RITE.mission_name, "Steps of the Rite: Northeast Guardian", SC2LOTV_LOC_ID_OFFSET + 1705, LocationType.EXTRA,
                     lambda state: logic.steps_of_the_rite_requirement(state)),
        LocationData(SC2Mission.STEPS_OF_THE_RITE.mission_name, "Steps of the Rite: North Mothership", SC2LOTV_LOC_ID_OFFSET + 1706, LocationType.VANILLA,
                     lambda state: logic.steps_of_the_rite_requirement(state)),
        LocationData(SC2Mission.STEPS_OF_THE_RITE.mission_name, "Steps of the Rite: South Mothership", SC2LOTV_LOC_ID_OFFSET + 1707, LocationType.VANILLA,
                     lambda state: logic.steps_of_the_rite_requirement(state)),
        LocationData(SC2Mission.RAK_SHIR.mission_name, "Rak'Shir: Victory", SC2LOTV_LOC_ID_OFFSET + 1800, LocationType.VICTORY,
                     lambda state: logic.protoss_competent_comp(state)),
        LocationData(SC2Mission.RAK_SHIR.mission_name, "Rak'Shir: North Slayn Elemental", SC2LOTV_LOC_ID_OFFSET + 1801, LocationType.VANILLA,
                     lambda state: logic.protoss_competent_comp(state)),
        LocationData(SC2Mission.RAK_SHIR.mission_name, "Rak'Shir: Southwest Slayn Elemental", SC2LOTV_LOC_ID_OFFSET + 1802, LocationType.VANILLA,
                     lambda state: logic.protoss_competent_comp(state)),
        LocationData(SC2Mission.RAK_SHIR.mission_name, "Rak'Shir: East Slayn Elemental", SC2LOTV_LOC_ID_OFFSET + 1803, LocationType.VANILLA,
                     lambda state: logic.protoss_competent_comp(state)),
        LocationData(SC2Mission.TEMPLAR_S_CHARGE.mission_name, "Templar's Charge: Victory", SC2LOTV_LOC_ID_OFFSET + 1900, LocationType.VICTORY,
                     lambda state: logic.templars_charge_requirement(state)),
        LocationData(SC2Mission.TEMPLAR_S_CHARGE.mission_name, "Templar's Charge: Northwest Power Core", SC2LOTV_LOC_ID_OFFSET + 1901, LocationType.EXTRA,
                     lambda state: logic.templars_charge_requirement(state)),
        LocationData(SC2Mission.TEMPLAR_S_CHARGE.mission_name, "Templar's Charge: Northeast Power Core", SC2LOTV_LOC_ID_OFFSET + 1902, LocationType.EXTRA,
                     lambda state: logic.templars_charge_requirement(state)),
        LocationData(SC2Mission.TEMPLAR_S_CHARGE.mission_name, "Templar's Charge: Southeast Power Core", SC2LOTV_LOC_ID_OFFSET + 1903, LocationType.EXTRA,
                     lambda state: logic.templars_charge_requirement(state)),
        LocationData(SC2Mission.TEMPLAR_S_CHARGE.mission_name, "Templar's Charge: West Hybrid Stasis Chamber", SC2LOTV_LOC_ID_OFFSET + 1904, LocationType.VANILLA,
                     lambda state: logic.templars_charge_requirement(state)),
        LocationData(SC2Mission.TEMPLAR_S_CHARGE.mission_name, "Templar's Charge: Southeast Hybrid Stasis Chamber", SC2LOTV_LOC_ID_OFFSET + 1905, LocationType.VANILLA,
                     lambda state: logic.protoss_fleet(state)),
        LocationData(SC2Mission.TEMPLAR_S_RETURN.mission_name, "Templar's Return: Victory", SC2LOTV_LOC_ID_OFFSET + 2000, LocationType.VICTORY,
                     lambda state: logic.templars_return_requirement(state)),
        LocationData(SC2Mission.TEMPLAR_S_RETURN.mission_name, "Templar's Return: Citadel: First Gate", SC2LOTV_LOC_ID_OFFSET + 2001, LocationType.EXTRA),
        LocationData(SC2Mission.TEMPLAR_S_RETURN.mission_name, "Templar's Return: Citadel: Second Gate", SC2LOTV_LOC_ID_OFFSET + 2002, LocationType.EXTRA),
        LocationData(SC2Mission.TEMPLAR_S_RETURN.mission_name, "Templar's Return: Citadel: Power Structure", SC2LOTV_LOC_ID_OFFSET + 2003, LocationType.VANILLA),
        LocationData(SC2Mission.TEMPLAR_S_RETURN.mission_name, "Templar's Return: Temple Grounds: Gather Army", SC2LOTV_LOC_ID_OFFSET + 2004, LocationType.VANILLA,
                     lambda state: logic.templars_return_requirement(state)),
        LocationData(SC2Mission.TEMPLAR_S_RETURN.mission_name, "Templar's Return: Temple Grounds: Power Structure", SC2LOTV_LOC_ID_OFFSET + 2005, LocationType.VANILLA,
                     lambda state: logic.templars_return_requirement(state)),
        LocationData(SC2Mission.TEMPLAR_S_RETURN.mission_name, "Templar's Return: Caverns: Purifier", SC2LOTV_LOC_ID_OFFSET + 2006, LocationType.EXTRA,
                     lambda state: logic.templars_return_requirement(state)),
        LocationData(SC2Mission.TEMPLAR_S_RETURN.mission_name, "Templar's Return: Caverns: Dark Templar", SC2LOTV_LOC_ID_OFFSET + 2007, LocationType.EXTRA,
                     lambda state: logic.templars_return_requirement(state)),
        LocationData(SC2Mission.THE_HOST.mission_name, "The Host: Victory", SC2LOTV_LOC_ID_OFFSET + 2100, LocationType.VICTORY,
                     lambda state: logic.the_host_requirement(state)),
        LocationData(SC2Mission.THE_HOST.mission_name, "The Host: Southeast Void Shard", SC2LOTV_LOC_ID_OFFSET + 2101, LocationType.VICTORY,
                     lambda state: logic.the_host_requirement(state)),
        LocationData(SC2Mission.THE_HOST.mission_name, "The Host: South Void Shard", SC2LOTV_LOC_ID_OFFSET + 2102, LocationType.EXTRA,
                     lambda state: logic.the_host_requirement(state)),
        LocationData(SC2Mission.THE_HOST.mission_name, "The Host: Southwest Void Shard", SC2LOTV_LOC_ID_OFFSET + 2103, LocationType.EXTRA,
                     lambda state: logic.the_host_requirement(state)),
        LocationData(SC2Mission.THE_HOST.mission_name, "The Host: North Void Shard", SC2LOTV_LOC_ID_OFFSET + 2104, LocationType.EXTRA,
                     lambda state: logic.the_host_requirement(state)),
        LocationData(SC2Mission.THE_HOST.mission_name, "The Host: Northwest Void Shard", SC2LOTV_LOC_ID_OFFSET + 2105, LocationType.EXTRA,
                     lambda state: logic.the_host_requirement(state)),
        LocationData(SC2Mission.THE_HOST.mission_name, "The Host: Nerazim Warp in Zone", SC2LOTV_LOC_ID_OFFSET + 2106, LocationType.VANILLA,
                     lambda state: logic.the_host_requirement(state)),
        LocationData(SC2Mission.THE_HOST.mission_name, "The Host: Tal'darim Warp in Zone", SC2LOTV_LOC_ID_OFFSET + 2107, LocationType.VANILLA,
                     lambda state: logic.the_host_requirement(state)),
        LocationData(SC2Mission.THE_HOST.mission_name, "The Host: Purifier Warp in Zone", SC2LOTV_LOC_ID_OFFSET + 2108, LocationType.VANILLA,
                     lambda state: logic.the_host_requirement(state)),
        LocationData(SC2Mission.SALVATION.mission_name, "Salvation: Victory", SC2LOTV_LOC_ID_OFFSET + 2200, LocationType.VICTORY,
                     lambda state: logic.salvation_requirement(state)),
        LocationData(SC2Mission.SALVATION.mission_name, "Salvation: Fabrication Matrix", SC2LOTV_LOC_ID_OFFSET + 2201, LocationType.EXTRA,
                     lambda state: logic.salvation_requirement(state)),
        LocationData(SC2Mission.SALVATION.mission_name, "Salvation: Assault Cluster", SC2LOTV_LOC_ID_OFFSET + 2202, LocationType.EXTRA,
                     lambda state: logic.salvation_requirement(state)),
        LocationData(SC2Mission.SALVATION.mission_name, "Salvation: Hull Breach", SC2LOTV_LOC_ID_OFFSET + 2203, LocationType.EXTRA,
                     lambda state: logic.salvation_requirement(state)),
        LocationData(SC2Mission.SALVATION.mission_name, "Salvation: Core Critical", SC2LOTV_LOC_ID_OFFSET + 2204, LocationType.EXTRA,
                     lambda state: logic.salvation_requirement(state)),

        # Epilogue
        LocationData(SC2Mission.INTO_THE_VOID.mission_name, "Into the Void: Victory", SC2LOTV_LOC_ID_OFFSET + 2300, LocationType.VICTORY,
                     lambda state: logic.into_the_void_requirement(state)),
        LocationData(SC2Mission.INTO_THE_VOID.mission_name, "Into the Void: Corruption Source", SC2LOTV_LOC_ID_OFFSET + 2301, LocationType.EXTRA),
        LocationData(SC2Mission.INTO_THE_VOID.mission_name, "Into the Void: Southwest Forward Position", SC2LOTV_LOC_ID_OFFSET + 2302, LocationType.VANILLA,
                     lambda state: logic.into_the_void_requirement(state)),
        LocationData(SC2Mission.INTO_THE_VOID.mission_name, "Into the Void: Northwest Forward Position", SC2LOTV_LOC_ID_OFFSET + 2303, LocationType.VANILLA,
                     lambda state: logic.into_the_void_requirement(state)),
        LocationData(SC2Mission.INTO_THE_VOID.mission_name, "Into the Void: Southeast Forward Position", SC2LOTV_LOC_ID_OFFSET + 2304, LocationType.VANILLA,
                     lambda state: logic.into_the_void_requirement(state)),
        LocationData(SC2Mission.INTO_THE_VOID.mission_name, "Into the Void: Northeast Forward Position", SC2LOTV_LOC_ID_OFFSET + 2305, LocationType.VANILLA),
        LocationData(SC2Mission.THE_ESSENCE_OF_ETERNITY.mission_name, "The Essence of Eternity: Victory", SC2LOTV_LOC_ID_OFFSET + 2400, LocationType.VICTORY,
                     lambda state: logic.essence_of_eternity_requirement(state)),
        LocationData(SC2Mission.THE_ESSENCE_OF_ETERNITY.mission_name, "The Essence of Eternity: Void Trashers", SC2LOTV_LOC_ID_OFFSET + 2401, LocationType.EXTRA),
        LocationData(SC2Mission.AMON_S_FALL.mission_name, "Amon's Fall: Victory", SC2LOTV_LOC_ID_OFFSET + 2500, LocationType.VICTORY,
                     lambda state: logic.amons_fall_requirement(state)),

        # Nova Covert Ops
        LocationData(SC2Mission.THE_ESCAPE.mission_name, "The Escape: Victory", SC2NCO_LOC_ID_OFFSET + 100, LocationType.VICTORY,
                     lambda state: logic.the_escape_requirement(state)),
        LocationData(SC2Mission.THE_ESCAPE.mission_name, "The Escape: Rifle", SC2NCO_LOC_ID_OFFSET + 101, LocationType.VANILLA,
                     lambda state: logic.the_escape_first_stage_requirement(state)),
        LocationData(SC2Mission.THE_ESCAPE.mission_name, "The Escape: Grenades", SC2NCO_LOC_ID_OFFSET + 102, LocationType.VANILLA,
                     lambda state: logic.the_escape_first_stage_requirement(state)),
        LocationData(SC2Mission.THE_ESCAPE.mission_name, "The Escape: Agent Delta", SC2NCO_LOC_ID_OFFSET + 103, LocationType.VANILLA,
                     lambda state: logic.the_escape_requirement(state)),
        LocationData(SC2Mission.THE_ESCAPE.mission_name, "The Escape: Agent Pierce", SC2NCO_LOC_ID_OFFSET + 104, LocationType.VANILLA,
                     lambda state: logic.the_escape_requirement(state)),
        LocationData(SC2Mission.THE_ESCAPE.mission_name, "The Escape: Agent Stone", SC2NCO_LOC_ID_OFFSET + 105, LocationType.VANILLA,
                     lambda state: logic.the_escape_requirement(state)),
        LocationData(SC2Mission.SUDDEN_STRIKE.mission_name, "Sudden Strike: Victory", SC2NCO_LOC_ID_OFFSET + 200, LocationType.VICTORY,
                     lambda state: logic.sudden_strike_can_reach_objectives(state)),
        LocationData(SC2Mission.SUDDEN_STRIKE.mission_name, "Sudden Strike: Research Center", SC2NCO_LOC_ID_OFFSET + 201, LocationType.VANILLA,
                     lambda state: logic.sudden_strike_can_reach_objectives(state)),
        LocationData(SC2Mission.SUDDEN_STRIKE.mission_name, "Sudden Strike: Weaponry Labs", SC2NCO_LOC_ID_OFFSET + 202, LocationType.VANILLA,
                     lambda state: logic.sudden_strike_requirement(state)),
        LocationData(SC2Mission.SUDDEN_STRIKE.mission_name, "Sudden Strike: Brutalisk", SC2NCO_LOC_ID_OFFSET + 203, LocationType.EXTRA,
                     lambda state: logic.sudden_strike_requirement(state)),
        LocationData(SC2Mission.ENEMY_INTELLIGENCE.mission_name, "Enemy Intelligence: Victory", SC2NCO_LOC_ID_OFFSET + 300, LocationType.VICTORY,
                     lambda state: logic.enemy_intelligence_third_stage_requirement(state)),
        LocationData(SC2Mission.ENEMY_INTELLIGENCE.mission_name, "Enemy Intelligence: West Garrison", SC2NCO_LOC_ID_OFFSET + 301, LocationType.EXTRA,
                     lambda state: logic.enemy_intelligence_first_stage_requirement(state)),
        LocationData(SC2Mission.ENEMY_INTELLIGENCE.mission_name, "Enemy Intelligence: Close Garrison", SC2NCO_LOC_ID_OFFSET + 302, LocationType.EXTRA,
                     lambda state: logic.enemy_intelligence_first_stage_requirement(state)),
        LocationData(SC2Mission.ENEMY_INTELLIGENCE.mission_name, "Enemy Intelligence: Northeast Garrison", SC2NCO_LOC_ID_OFFSET + 303, LocationType.EXTRA,
                     lambda state: logic.enemy_intelligence_first_stage_requirement(state)),
        LocationData(SC2Mission.ENEMY_INTELLIGENCE.mission_name, "Enemy Intelligence: Southeast Garrison", SC2NCO_LOC_ID_OFFSET + 304, LocationType.EXTRA,
                     lambda state: logic.enemy_intelligence_first_stage_requirement(state)
                                   and logic.enemy_intelligence_cliff_garrison(state)),
        LocationData(SC2Mission.ENEMY_INTELLIGENCE.mission_name, "Enemy Intelligence: South Garrison", SC2NCO_LOC_ID_OFFSET + 305, LocationType.EXTRA,
                     lambda state: logic.enemy_intelligence_first_stage_requirement(state)),
        LocationData(SC2Mission.ENEMY_INTELLIGENCE.mission_name, "Enemy Intelligence: All Garrisons", SC2NCO_LOC_ID_OFFSET + 306, LocationType.VANILLA,
                     lambda state: logic.enemy_intelligence_first_stage_requirement(state)
                                   and logic.enemy_intelligence_cliff_garrison(state)),
        LocationData(SC2Mission.ENEMY_INTELLIGENCE.mission_name, "Enemy Intelligence: Forces Rescued", SC2NCO_LOC_ID_OFFSET + 307, LocationType.VANILLA,
                     lambda state: logic.enemy_intelligence_first_stage_requirement(state)),
        LocationData(SC2Mission.ENEMY_INTELLIGENCE.mission_name, "Enemy Intelligence: Communications Hub", SC2NCO_LOC_ID_OFFSET + 308, LocationType.VANILLA,
                     lambda state: logic.enemy_intelligence_second_stage_requirement(state)),
        LocationData(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "Trouble In Paradise: Victory", SC2NCO_LOC_ID_OFFSET + 400, LocationType.VICTORY,
                     lambda state: logic.trouble_in_paradise_requirement(state)),
        LocationData(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "Trouble In Paradise: North Base: West Hatchery", SC2NCO_LOC_ID_OFFSET + 401, LocationType.VANILLA,
                     lambda state: logic.trouble_in_paradise_requirement(state)),
        LocationData(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "Trouble In Paradise: North Base: North Hatchery", SC2NCO_LOC_ID_OFFSET + 402, LocationType.VANILLA,
                     lambda state: logic.trouble_in_paradise_requirement(state)),
        LocationData(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "Trouble In Paradise: North Base: East Hatchery", SC2NCO_LOC_ID_OFFSET + 403, LocationType.VANILLA),
        LocationData(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "Trouble In Paradise: South Base: Northwest Hatchery", SC2NCO_LOC_ID_OFFSET + 404, LocationType.VANILLA,
                     lambda state: logic.trouble_in_paradise_requirement(state)),
        LocationData(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "Trouble In Paradise: South Base: Southwest Hatchery", SC2NCO_LOC_ID_OFFSET + 405, LocationType.VANILLA,
                     lambda state: logic.trouble_in_paradise_requirement(state)),
        LocationData(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "Trouble In Paradise: South Base: East Hatchery", SC2NCO_LOC_ID_OFFSET + 406, LocationType.VANILLA),
        LocationData(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "Trouble In Paradise: North Shield Projector", SC2NCO_LOC_ID_OFFSET + 407, LocationType.EXTRA,
                     lambda state: logic.trouble_in_paradise_requirement(state)),
        LocationData(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "Trouble In Paradise: East Shield Projector", SC2NCO_LOC_ID_OFFSET + 408, LocationType.EXTRA,
                     lambda state: logic.trouble_in_paradise_requirement(state)),
        LocationData(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "Trouble In Paradise: South Shield Projector", SC2NCO_LOC_ID_OFFSET + 409, LocationType.EXTRA,
                     lambda state: logic.trouble_in_paradise_requirement(state)),
        LocationData(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "Trouble In Paradise: West Shield Projector", SC2NCO_LOC_ID_OFFSET + 410, LocationType.EXTRA,
                     lambda state: logic.trouble_in_paradise_requirement(state)),
        LocationData(SC2Mission.TROUBLE_IN_PARADISE.mission_name, "Trouble In Paradise: Fleet Beacon", SC2NCO_LOC_ID_OFFSET + 411, LocationType.VANILLA,
                     lambda state: logic.trouble_in_paradise_requirement(state)),
        LocationData(SC2Mission.NIGHT_TERRORS.mission_name, "Night Terrors: Victory", SC2NCO_LOC_ID_OFFSET + 500, LocationType.VICTORY,
                     lambda state: logic.night_terrors_requirement(state)),
        LocationData(SC2Mission.NIGHT_TERRORS.mission_name, "Night Terrors: 1 Terrazine Node Collected", SC2NCO_LOC_ID_OFFSET + 501, LocationType.EXTRA,
                     lambda state: logic.night_terrors_requirement(state)),
        LocationData(SC2Mission.NIGHT_TERRORS.mission_name, "Night Terrors: 2 Terrazine Nodes Collected", SC2NCO_LOC_ID_OFFSET + 502, LocationType.EXTRA,
                     lambda state: logic.night_terrors_requirement(state)),
        LocationData(SC2Mission.NIGHT_TERRORS.mission_name, "Night Terrors: 3 Terrazine Nodes Collected", SC2NCO_LOC_ID_OFFSET + 503, LocationType.EXTRA,
                     lambda state: logic.night_terrors_requirement(state)),
        LocationData(SC2Mission.NIGHT_TERRORS.mission_name, "Night Terrors: 4 Terrazine Nodes Collected", SC2NCO_LOC_ID_OFFSET + 504, LocationType.EXTRA,
                     lambda state: logic.night_terrors_requirement(state)),
        LocationData(SC2Mission.NIGHT_TERRORS.mission_name, "Night Terrors: 5 Terrazine Nodes Collected", SC2NCO_LOC_ID_OFFSET + 505, LocationType.EXTRA,
                     lambda state: logic.night_terrors_requirement(state)),
        LocationData(SC2Mission.NIGHT_TERRORS.mission_name, "Night Terrors: HERC Outpost", SC2NCO_LOC_ID_OFFSET + 506, LocationType.VANILLA,
                     lambda state: logic.night_terrors_requirement(state)),
        LocationData(SC2Mission.NIGHT_TERRORS.mission_name, "Night Terrors: Umojan Mine", SC2NCO_LOC_ID_OFFSET + 507, LocationType.EXTRA,
                     lambda state: logic.night_terrors_requirement(state)),
        LocationData(SC2Mission.NIGHT_TERRORS.mission_name, "Night Terrors: Blightbringer", SC2NCO_LOC_ID_OFFSET + 508, LocationType.VANILLA,
                     lambda state: logic.night_terrors_requirement(state)
                                   and logic.nova_ranged_weapon(state)
                                   and state.has_any(
                         {item_names.NOVA_HELLFIRE_SHOTGUN, item_names.NOVA_PULSE_GRENADES, item_names.NOVA_STIM_INFUSION,
                          item_names.NOVA_HOLO_DECOY}, player)),
        LocationData(SC2Mission.NIGHT_TERRORS.mission_name, "Night Terrors: Science Facility", SC2NCO_LOC_ID_OFFSET + 509, LocationType.EXTRA,
                     lambda state: logic.night_terrors_requirement(state)),
        LocationData(SC2Mission.NIGHT_TERRORS.mission_name, "Night Terrors: Eradicators", SC2NCO_LOC_ID_OFFSET + 510, LocationType.VANILLA,
                     lambda state: logic.night_terrors_requirement(state)
                                   and logic.nova_any_weapon(state)),
        LocationData(SC2Mission.FLASHPOINT.mission_name, "Flashpoint: Victory", SC2NCO_LOC_ID_OFFSET + 600, LocationType.VICTORY,
                     lambda state: logic.flashpoint_far_requirement(state)),
        LocationData(SC2Mission.FLASHPOINT.mission_name, "Flashpoint: Close North Evidence Coordinates", SC2NCO_LOC_ID_OFFSET + 601, LocationType.EXTRA,
                     lambda state: state.has_any(
                         {item_names.LIBERATOR_RAID_ARTILLERY, item_names.RAVEN_HUNTER_SEEKER_WEAPON}, player)
                                   or logic.terran_common_unit(state)),
        LocationData(SC2Mission.FLASHPOINT.mission_name, "Flashpoint: Close East Evidence Coordinates", SC2NCO_LOC_ID_OFFSET + 602, LocationType.EXTRA,
                     lambda state: state.has_any(
                         {item_names.LIBERATOR_RAID_ARTILLERY, item_names.RAVEN_HUNTER_SEEKER_WEAPON}, player)
                                   or logic.terran_common_unit(state)),
        LocationData(SC2Mission.FLASHPOINT.mission_name, "Flashpoint: Far North Evidence Coordinates", SC2NCO_LOC_ID_OFFSET + 603, LocationType.EXTRA,
                     lambda state: logic.flashpoint_far_requirement(state)),
        LocationData(SC2Mission.FLASHPOINT.mission_name, "Flashpoint: Far East Evidence Coordinates", SC2NCO_LOC_ID_OFFSET + 604, LocationType.EXTRA,
                     lambda state: logic.flashpoint_far_requirement(state)),
        LocationData(SC2Mission.FLASHPOINT.mission_name, "Flashpoint: Experimental Weapon", SC2NCO_LOC_ID_OFFSET + 605, LocationType.VANILLA,
                     lambda state: logic.flashpoint_far_requirement(state)),
        LocationData(SC2Mission.FLASHPOINT.mission_name, "Flashpoint: Northwest Subway Entrance", SC2NCO_LOC_ID_OFFSET + 606, LocationType.VANILLA,
                     lambda state: state.has_any(
                         {item_names.LIBERATOR_RAID_ARTILLERY, item_names.RAVEN_HUNTER_SEEKER_WEAPON}, player)
                                   and logic.terran_common_unit(state)
                                   or logic.flashpoint_far_requirement(state)),
        LocationData(SC2Mission.FLASHPOINT.mission_name, "Flashpoint: Southeast Subway Entrance", SC2NCO_LOC_ID_OFFSET + 607, LocationType.VANILLA,
                     lambda state: state.has_any(
                         {item_names.LIBERATOR_RAID_ARTILLERY, item_names.RAVEN_HUNTER_SEEKER_WEAPON}, player)
                                   and logic.terran_common_unit(state)
                                   or logic.flashpoint_far_requirement(state)),
        LocationData(SC2Mission.FLASHPOINT.mission_name, "Flashpoint: Northeast Subway Entrance", SC2NCO_LOC_ID_OFFSET + 608, LocationType.VANILLA,
                     lambda state: logic.flashpoint_far_requirement(state)),
        LocationData(SC2Mission.FLASHPOINT.mission_name, "Flashpoint: Expansion Hatchery", SC2NCO_LOC_ID_OFFSET + 609, LocationType.EXTRA,
                     lambda state: state.has(item_names.LIBERATOR_RAID_ARTILLERY, player) and logic.terran_common_unit(state)
                                   or logic.flashpoint_far_requirement(state)),
        LocationData(SC2Mission.FLASHPOINT.mission_name, "Flashpoint: Baneling Spawns", SC2NCO_LOC_ID_OFFSET + 610, LocationType.EXTRA,
                     lambda state: logic.flashpoint_far_requirement(state)),
        LocationData(SC2Mission.FLASHPOINT.mission_name, "Flashpoint: Mutalisk Spawns", SC2NCO_LOC_ID_OFFSET + 611, LocationType.EXTRA,
                     lambda state: logic.flashpoint_far_requirement(state)),
        LocationData(SC2Mission.FLASHPOINT.mission_name, "Flashpoint: Nydus Worm Spawns", SC2NCO_LOC_ID_OFFSET + 612, LocationType.EXTRA,
                     lambda state: logic.flashpoint_far_requirement(state)),
        LocationData(SC2Mission.FLASHPOINT.mission_name, "Flashpoint: Lurker Spawns", SC2NCO_LOC_ID_OFFSET + 613, LocationType.EXTRA,
                     lambda state: logic.flashpoint_far_requirement(state)),
        LocationData(SC2Mission.FLASHPOINT.mission_name, "Flashpoint: Brood Lord Spawns", SC2NCO_LOC_ID_OFFSET + 614, LocationType.EXTRA,
                     lambda state: logic.flashpoint_far_requirement(state)),
        LocationData(SC2Mission.FLASHPOINT.mission_name, "Flashpoint: Ultralisk Spawns", SC2NCO_LOC_ID_OFFSET + 615, LocationType.EXTRA,
                     lambda state: logic.flashpoint_far_requirement(state)),
        LocationData(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "In the Enemy's Shadow: Victory", SC2NCO_LOC_ID_OFFSET + 700, LocationType.VICTORY,
                     lambda state: logic.enemy_shadow_victory(state)),
        LocationData(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "In the Enemy's Shadow: Sewers: Domination Visor", SC2NCO_LOC_ID_OFFSET + 701, LocationType.VANILLA,
                     lambda state: logic.enemy_shadow_domination(state)),
        LocationData(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "In the Enemy's Shadow: Sewers: Resupply Crate", SC2NCO_LOC_ID_OFFSET + 702, LocationType.EXTRA,
                     lambda state: logic.enemy_shadow_first_stage(state)),
        LocationData(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "In the Enemy's Shadow: Sewers: Facility Access", SC2NCO_LOC_ID_OFFSET + 703, LocationType.VANILLA,
                     lambda state: logic.enemy_shadow_first_stage(state)),
        LocationData(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "In the Enemy's Shadow: Facility: Northwest Door Lock", SC2NCO_LOC_ID_OFFSET + 704, LocationType.VANILLA,
                     lambda state: logic.enemy_shadow_door_controls(state)),
        LocationData(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "In the Enemy's Shadow: Facility: Southeast Door Lock", SC2NCO_LOC_ID_OFFSET + 705, LocationType.VANILLA,
                     lambda state: logic.enemy_shadow_door_controls(state)),
        LocationData(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "In the Enemy's Shadow: Facility: Blazefire Gunblade", SC2NCO_LOC_ID_OFFSET + 706, LocationType.VANILLA,
                     lambda state: logic.enemy_shadow_second_stage(state)
                                   and (logic.story_tech_granted
                                        or state.has(item_names.NOVA_BLINK, player)
                                        or (adv_tactics and state.has_all({item_names.NOVA_DOMINATION, item_names.NOVA_HOLO_DECOY, item_names.NOVA_JUMP_SUIT_MODULE}, player))
                                        )
                     ),
        LocationData(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "In the Enemy's Shadow: Facility: Blink Suit", SC2NCO_LOC_ID_OFFSET + 707, LocationType.VANILLA,
                     lambda state: logic.enemy_shadow_second_stage(state)),
        LocationData(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "In the Enemy's Shadow: Facility: Advanced Weaponry", SC2NCO_LOC_ID_OFFSET + 708, LocationType.VANILLA,
                     lambda state: logic.enemy_shadow_second_stage(state)),
        LocationData(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "In the Enemy's Shadow: Facility: Entrance Resupply Crate", SC2NCO_LOC_ID_OFFSET + 709, LocationType.EXTRA,
                     lambda state: logic.enemy_shadow_first_stage(state)),
        LocationData(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "In the Enemy's Shadow: Facility: West Resupply Crate", SC2NCO_LOC_ID_OFFSET + 710, LocationType.EXTRA,
                     lambda state: logic.enemy_shadow_second_stage(state)),
        LocationData(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "In the Enemy's Shadow: Facility: North Resupply Crate", SC2NCO_LOC_ID_OFFSET + 711, LocationType.EXTRA,
                     lambda state: logic.enemy_shadow_second_stage(state)),
        LocationData(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "In the Enemy's Shadow: Facility: East Resupply Crate", SC2NCO_LOC_ID_OFFSET + 712, LocationType.EXTRA,
                     lambda state: logic.enemy_shadow_second_stage(state)),
        LocationData(SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, "In the Enemy's Shadow: Facility: South Resupply Crate", SC2NCO_LOC_ID_OFFSET + 713, LocationType.EXTRA,
                     lambda state: logic.enemy_shadow_second_stage(state)),
        LocationData(SC2Mission.DARK_SKIES.mission_name, "Dark Skies: Victory", SC2NCO_LOC_ID_OFFSET + 800, LocationType.VICTORY,
                     lambda state: logic.dark_skies_requirement(state)),
        LocationData(SC2Mission.DARK_SKIES.mission_name, "Dark Skies: First Squadron of Dominion Fleet", SC2NCO_LOC_ID_OFFSET + 801, LocationType.EXTRA,
                     lambda state: logic.dark_skies_requirement(state)),
        LocationData(SC2Mission.DARK_SKIES.mission_name, "Dark Skies: Remainder of Dominion Fleet", SC2NCO_LOC_ID_OFFSET + 802, LocationType.EXTRA,
                     lambda state: logic.dark_skies_requirement(state)),
        LocationData(SC2Mission.DARK_SKIES.mission_name, "Dark Skies: Ji'nara", SC2NCO_LOC_ID_OFFSET + 803, LocationType.EXTRA,
                     lambda state: logic.dark_skies_requirement(state)),
        LocationData(SC2Mission.DARK_SKIES.mission_name, "Dark Skies: Science Facility", SC2NCO_LOC_ID_OFFSET + 804, LocationType.VANILLA,
                     lambda state: logic.dark_skies_requirement(state)),
        LocationData(SC2Mission.END_GAME.mission_name, "End Game: Victory", SC2NCO_LOC_ID_OFFSET + 900, LocationType.VICTORY,
                     lambda state: logic.end_game_requirement(state) and logic.nova_any_weapon(state)),
        LocationData(SC2Mission.END_GAME.mission_name, "End Game: Xanthos", SC2NCO_LOC_ID_OFFSET + 901, LocationType.VANILLA,
                     lambda state: logic.end_game_requirement(state)),

        # Mission Variants
        # 10X/20X - Liberation Day
        LocationData(SC2Mission.THE_OUTLAWS_Z.mission_name, "The Outlaws (Zerg): Victory", SC2_RACESWAP_LOC_ID_OFFSET + 300, LocationType.VICTORY,
                     lambda state: logic.zerg_common_unit(state)),
        LocationData(SC2Mission.THE_OUTLAWS_Z.mission_name, "The Outlaws (Zerg): Rebel Base", SC2_RACESWAP_LOC_ID_OFFSET + 301, LocationType.VANILLA,
                     lambda state: logic.zerg_common_unit(state)),
        LocationData(SC2Mission.THE_OUTLAWS_Z.mission_name, "The Outlaws (Zerg): North Resource Pickups", SC2_RACESWAP_LOC_ID_OFFSET + 302, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state)),
        LocationData(SC2Mission.THE_OUTLAWS_Z.mission_name, "The Outlaws (Zerg): Bunker", SC2_RACESWAP_LOC_ID_OFFSET + 303, LocationType.VANILLA,
                     lambda state: logic.zerg_common_unit(state)),
        LocationData(SC2Mission.THE_OUTLAWS_Z.mission_name, "The Outlaws (Zerg): Close Resource Pickups", SC2_RACESWAP_LOC_ID_OFFSET + 304, LocationType.EXTRA),
        LocationData(SC2Mission.THE_OUTLAWS_P.mission_name, "The Outlaws (Protoss): Victory", SC2_RACESWAP_LOC_ID_OFFSET + 400, LocationType.VICTORY,
                     lambda state: logic.protoss_common_unit(state)),
        LocationData(SC2Mission.THE_OUTLAWS_P.mission_name, "The Outlaws (Protoss): Rebel Base", SC2_RACESWAP_LOC_ID_OFFSET + 401, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state)),
        LocationData(SC2Mission.THE_OUTLAWS_P.mission_name, "The Outlaws (Protoss): North Resource Pickups", SC2_RACESWAP_LOC_ID_OFFSET + 402, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)),
        LocationData(SC2Mission.THE_OUTLAWS_P.mission_name, "The Outlaws (Protoss): Bunker", SC2_RACESWAP_LOC_ID_OFFSET + 403, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state)),
        LocationData(SC2Mission.THE_OUTLAWS_P.mission_name, "The Outlaws (Protoss): Close Resource Pickups", SC2_RACESWAP_LOC_ID_OFFSET + 404, LocationType.EXTRA),
        LocationData(SC2Mission.ZERO_HOUR_Z.mission_name, "Zero Hour (Zerg): Victory", SC2_RACESWAP_LOC_ID_OFFSET + 500, LocationType.VICTORY,
                     lambda state: logic.zerg_competent_defense(state) and 
                                   logic.zerg_basic_kerriganless_anti_air(state)),
        LocationData(SC2Mission.ZERO_HOUR_Z.mission_name, "Zero Hour (Zerg): First Group Rescued", SC2_RACESWAP_LOC_ID_OFFSET + 501, LocationType.VANILLA),
        LocationData(SC2Mission.ZERO_HOUR_Z.mission_name, "Zero Hour (Zerg): Second Group Rescued", SC2_RACESWAP_LOC_ID_OFFSET + 502, LocationType.VANILLA,
                     lambda state: logic.zerg_common_unit(state)),
        LocationData(SC2Mission.ZERO_HOUR_Z.mission_name, "Zero Hour (Zerg): Third Group Rescued", SC2_RACESWAP_LOC_ID_OFFSET + 503, LocationType.VANILLA,
                     lambda state: logic.zerg_competent_defense(state)),
        LocationData(SC2Mission.ZERO_HOUR_Z.mission_name, "Zero Hour (Zerg): First Hatchery", SC2_RACESWAP_LOC_ID_OFFSET + 504, LocationType.CHALLENGE,
                     lambda state: logic.zerg_competent_comp(state)),
        LocationData(SC2Mission.ZERO_HOUR_Z.mission_name, "Zero Hour (Zerg): Second Hatchery", SC2_RACESWAP_LOC_ID_OFFSET + 505, LocationType.CHALLENGE,
                     lambda state: logic.zerg_competent_comp(state)),
        LocationData(SC2Mission.ZERO_HOUR_Z.mission_name, "Zero Hour (Zerg): Third Hatchery", SC2_RACESWAP_LOC_ID_OFFSET + 506, LocationType.CHALLENGE,
                     lambda state: logic.zerg_competent_comp(state)),
        LocationData(SC2Mission.ZERO_HOUR_Z.mission_name, "Zero Hour (Zerg): Fourth Hatchery", SC2_RACESWAP_LOC_ID_OFFSET + 507, LocationType.CHALLENGE,
                     lambda state: logic.zerg_competent_comp(state)),
        LocationData(SC2Mission.ZERO_HOUR_Z.mission_name, "Zero Hour (Zerg): Ride's on its Way", SC2_RACESWAP_LOC_ID_OFFSET + 508, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state)),
        LocationData(SC2Mission.ZERO_HOUR_Z.mission_name, "Zero Hour (Zerg): Hold Just a Little Longer", SC2_RACESWAP_LOC_ID_OFFSET + 509,
                     LocationType.EXTRA,
                     lambda state: logic.zerg_competent_defense(state)),
        LocationData(SC2Mission.ZERO_HOUR_Z.mission_name, "Zero Hour (Zerg): Cavalry's on the Way", SC2_RACESWAP_LOC_ID_OFFSET + 510, LocationType.EXTRA,
                     lambda state: logic.zerg_competent_defense(state)),
        LocationData(SC2Mission.ZERO_HOUR_P.mission_name, "Zero Hour (Protoss): Victory", SC2_RACESWAP_LOC_ID_OFFSET + 600, LocationType.VICTORY,
                     lambda state: logic.protoss_common_unit(state) and
                                   (adv_tactics or logic.protoss_basic_anti_air(state))),
        LocationData(SC2Mission.ZERO_HOUR_P.mission_name, "Zero Hour (Protoss): First Group Rescued", SC2_RACESWAP_LOC_ID_OFFSET + 601, LocationType.VANILLA),
        LocationData(SC2Mission.ZERO_HOUR_P.mission_name, "Zero Hour (Protoss): Second Group Rescued", SC2_RACESWAP_LOC_ID_OFFSET + 602, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state)),
        LocationData(SC2Mission.ZERO_HOUR_P.mission_name, "Zero Hour (Protoss): Third Group Rescued", SC2_RACESWAP_LOC_ID_OFFSET + 603, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state)),
        LocationData(SC2Mission.ZERO_HOUR_P.mission_name, "Zero Hour (Protoss): First Hatchery", SC2_RACESWAP_LOC_ID_OFFSET + 604, LocationType.CHALLENGE,
                     lambda state: logic.protoss_competent_comp(state)),
        LocationData(SC2Mission.ZERO_HOUR_P.mission_name, "Zero Hour (Protoss): Second Hatchery", SC2_RACESWAP_LOC_ID_OFFSET + 605, LocationType.CHALLENGE,
                     lambda state: logic.protoss_competent_comp(state)),
        LocationData(SC2Mission.ZERO_HOUR_P.mission_name, "Zero Hour (Protoss): Third Hatchery", SC2_RACESWAP_LOC_ID_OFFSET + 606, LocationType.CHALLENGE,
                     lambda state: logic.protoss_competent_comp(state)),
        LocationData(SC2Mission.ZERO_HOUR_P.mission_name, "Zero Hour (Protoss): Fourth Hatchery", SC2_RACESWAP_LOC_ID_OFFSET + 607, LocationType.CHALLENGE,
                     lambda state: logic.protoss_competent_comp(state)),
        LocationData(SC2Mission.ZERO_HOUR_P.mission_name, "Zero Hour (Protoss): Ride's on its Way", SC2_RACESWAP_LOC_ID_OFFSET + 608, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)),
        LocationData(SC2Mission.ZERO_HOUR_P.mission_name, "Zero Hour (Protoss): Hold Just a Little Longer", SC2_RACESWAP_LOC_ID_OFFSET + 609,
                     LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)),
        LocationData(SC2Mission.ZERO_HOUR_P.mission_name, "Zero Hour (Protoss): Cavalry's on the Way", SC2_RACESWAP_LOC_ID_OFFSET + 610, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state)),
        # 70X/80X - Evacuation
        # 90X/100X - Outbreak
        # 110X/120X - Safe Haven
        # 130X/140X - Haven's Fall
        LocationData(SC2Mission.SMASH_AND_GRAB_Z.mission_name, "Smash and Grab (Zerg): Victory", SC2_RACESWAP_LOC_ID_OFFSET + 1500, LocationType.VICTORY,
                     lambda state: logic.zerg_common_unit(state) and
                                   (adv_tactics and logic.zerg_basic_anti_air(state)
                                    or logic.zerg_competent_anti_air(state))),
        LocationData(SC2Mission.SMASH_AND_GRAB_Z.mission_name, "Smash and Grab (Zerg): First Relic", SC2_RACESWAP_LOC_ID_OFFSET + 1501, LocationType.VANILLA),
        LocationData(SC2Mission.SMASH_AND_GRAB_Z.mission_name, "Smash and Grab (Zerg): Second Relic", SC2_RACESWAP_LOC_ID_OFFSET + 1502, LocationType.VANILLA),
        LocationData(SC2Mission.SMASH_AND_GRAB_Z.mission_name, "Smash and Grab (Zerg): Third Relic", SC2_RACESWAP_LOC_ID_OFFSET + 1503, LocationType.VANILLA,
                     lambda state: logic.zerg_common_unit(state) and
                                   (adv_tactics and logic.zerg_basic_kerriganless_anti_air(state)
                                    or logic.zerg_competent_anti_air(state))),
        LocationData(SC2Mission.SMASH_AND_GRAB_Z.mission_name, "Smash and Grab (Zerg): Fourth Relic", SC2_RACESWAP_LOC_ID_OFFSET + 1504, LocationType.VANILLA,
                     lambda state: logic.zerg_common_unit(state) and
                                   (adv_tactics and logic.zerg_basic_kerriganless_anti_air(state)
                                    or logic.zerg_competent_anti_air(state))),
        LocationData(SC2Mission.SMASH_AND_GRAB_Z.mission_name, "Smash and Grab (Zerg): First Forcefield Area Busted", SC2_RACESWAP_LOC_ID_OFFSET + 1505, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state) and
                                   (adv_tactics and logic.zerg_basic_kerriganless_anti_air(state)
                                    or logic.zerg_competent_anti_air(state))),
        LocationData(SC2Mission.SMASH_AND_GRAB_Z.mission_name, "Smash and Grab (Zerg): Second Forcefield Area Busted", SC2_RACESWAP_LOC_ID_OFFSET + 1506, LocationType.EXTRA,
                     lambda state: logic.zerg_common_unit(state) and
                                   (adv_tactics and logic.zerg_basic_kerriganless_anti_air(state)
                                    or logic.zerg_competent_anti_air(state))),
        LocationData(SC2Mission.SMASH_AND_GRAB_P.mission_name, "Smash and Grab (Protoss): Victory", SC2_RACESWAP_LOC_ID_OFFSET + 1600, LocationType.VICTORY,
                     lambda state: logic.protoss_common_unit(state) and
                                   (adv_tactics and logic.protoss_basic_anti_air(state)
                                    or logic.protoss_competent_anti_air(state))),
        LocationData(SC2Mission.SMASH_AND_GRAB_P.mission_name, "Smash and Grab (Protoss): First Relic", SC2_RACESWAP_LOC_ID_OFFSET + 1601, LocationType.VANILLA),
        LocationData(SC2Mission.SMASH_AND_GRAB_P.mission_name, "Smash and Grab (Protoss): Second Relic", SC2_RACESWAP_LOC_ID_OFFSET + 1602, LocationType.VANILLA),
        LocationData(SC2Mission.SMASH_AND_GRAB_P.mission_name, "Smash and Grab (Protoss): Third Relic", SC2_RACESWAP_LOC_ID_OFFSET + 1603, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state) and
                                   (adv_tactics and logic.protoss_basic_anti_air(state)
                                    or logic.protoss_competent_anti_air(state))),
        LocationData(SC2Mission.SMASH_AND_GRAB_P.mission_name, "Smash and Grab (Protoss): Fourth Relic", SC2_RACESWAP_LOC_ID_OFFSET + 1604, LocationType.VANILLA,
                     lambda state: logic.protoss_common_unit(state) and
                                   (adv_tactics and logic.protoss_basic_anti_air(state)
                                    or logic.protoss_competent_anti_air(state))),
        LocationData(SC2Mission.SMASH_AND_GRAB_P.mission_name, "Smash and Grab (Protoss): First Forcefield Area Busted", SC2_RACESWAP_LOC_ID_OFFSET + 1605, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state) and
                                   (adv_tactics and logic.protoss_basic_anti_air(state)
                                    or logic.protoss_competent_anti_air(state))),
        LocationData(SC2Mission.SMASH_AND_GRAB_P.mission_name, "Smash and Grab (Protoss): Second Forcefield Area Busted", SC2_RACESWAP_LOC_ID_OFFSET + 1606, LocationType.EXTRA,
                     lambda state: logic.protoss_common_unit(state) and
                                   (adv_tactics and logic.protoss_basic_anti_air(state)
                                    or logic.protoss_competent_anti_air(state))),
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