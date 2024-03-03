from enum import IntEnum
from typing import List, Tuple, Optional, Callable, NamedTuple
from BaseClasses import MultiWorld
from .Options import get_option_value

from BaseClasses import Location

SC2WOL_LOC_ID_OFFSET = 1000


class SC2WoLLocation(Location):
    game: str = "Starcraft2WoL"


class LocationType(IntEnum):
    VICTORY = 0 # Winning a mission
    MISSION_PROGRESS = 1 # All tasks done for progressing the mission normally towards victory. All cleaning of expansion bases falls here
    BONUS = 2 # Bonus objective, getting a campaign or mission bonus in vanilla (credits, research, bonus units or resources)
    CHALLENGE = 3 # Challenging objectives, often harder than just completing a mission
    OPTIONAL_BOSS = 4 # Any boss that's not required to win the mission. All Brutalisks, Loki, etc.

class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]
    type: LocationType
    rule: Callable = lambda state: True


def get_locations(multiworld: Optional[MultiWorld], player: Optional[int]) -> Tuple[LocationData, ...]:
    # Note: rules which are ended with or True are rules identified as needed later when restricted units is an option
    logic_level = get_option_value(multiworld, player, 'required_tactics')
    location_table: List[LocationData] = [
        LocationData("Liberation Day", "Liberation Day: Victory", SC2WOL_LOC_ID_OFFSET + 100, LocationType.VICTORY),
        LocationData("Liberation Day", "Liberation Day: First Statue", SC2WOL_LOC_ID_OFFSET + 101, LocationType.BONUS),
        LocationData("Liberation Day", "Liberation Day: Second Statue", SC2WOL_LOC_ID_OFFSET + 102, LocationType.BONUS),
        LocationData("Liberation Day", "Liberation Day: Third Statue", SC2WOL_LOC_ID_OFFSET + 103, LocationType.BONUS),
        LocationData("Liberation Day", "Liberation Day: Fourth Statue", SC2WOL_LOC_ID_OFFSET + 104, LocationType.BONUS),
        LocationData("Liberation Day", "Liberation Day: Fifth Statue", SC2WOL_LOC_ID_OFFSET + 105, LocationType.BONUS),
        LocationData("Liberation Day", "Liberation Day: Sixth Statue", SC2WOL_LOC_ID_OFFSET + 106, LocationType.BONUS),
        LocationData("Liberation Day", "Liberation Day: Special Delivery", SC2WOL_LOC_ID_OFFSET + 107, LocationType.MISSION_PROGRESS),
        LocationData("The Outlaws", "The Outlaws: Victory", SC2WOL_LOC_ID_OFFSET + 200, LocationType.VICTORY,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player)),
        LocationData("The Outlaws", "The Outlaws: Rebel Base", SC2WOL_LOC_ID_OFFSET + 201, LocationType.BONUS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player)),
        LocationData("The Outlaws", "The Outlaws: North Resource Pickups", SC2WOL_LOC_ID_OFFSET + 202, LocationType.BONUS),
        LocationData("The Outlaws", "The Outlaws: Bunker", SC2WOL_LOC_ID_OFFSET + 203, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player)),
        LocationData("Zero Hour", "Zero Hour: Victory", SC2WOL_LOC_ID_OFFSET + 300, LocationType.VICTORY,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, True) >= 2 and
                                   (logic_level > 0 or state._sc2wol_has_anti_air(multiworld, player))),
        LocationData("Zero Hour", "Zero Hour: First Group Rescued", SC2WOL_LOC_ID_OFFSET + 301, LocationType.BONUS),
        LocationData("Zero Hour", "Zero Hour: Second Group Rescued", SC2WOL_LOC_ID_OFFSET + 302, LocationType.BONUS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player)),
        LocationData("Zero Hour", "Zero Hour: Third Group Rescued", SC2WOL_LOC_ID_OFFSET + 303, LocationType.BONUS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, True) >= 2),
        LocationData("Zero Hour", "Zero Hour: First Hatchery", SC2WOL_LOC_ID_OFFSET + 304, LocationType.CHALLENGE,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Zero Hour", "Zero Hour: Second Hatchery", SC2WOL_LOC_ID_OFFSET + 305, LocationType.CHALLENGE,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Zero Hour", "Zero Hour: Third Hatchery", SC2WOL_LOC_ID_OFFSET + 306, LocationType.CHALLENGE,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Zero Hour", "Zero Hour: Fourth Hatchery", SC2WOL_LOC_ID_OFFSET + 307, LocationType.CHALLENGE,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Evacuation", "Evacuation: Victory", SC2WOL_LOC_ID_OFFSET + 400, LocationType.VICTORY,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   (logic_level > 0 and state._sc2wol_has_anti_air(multiworld, player)
                                    or state._sc2wol_has_competent_anti_air(multiworld, player))),
        LocationData("Evacuation", "Evacuation: North Chrysalis", SC2WOL_LOC_ID_OFFSET + 401, LocationType.BONUS),
        LocationData("Evacuation", "Evacuation: West Chrysalis", SC2WOL_LOC_ID_OFFSET + 402, LocationType.BONUS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player)),
        LocationData("Evacuation", "Evacuation: East Chrysalis", SC2WOL_LOC_ID_OFFSET + 403, LocationType.BONUS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player)),
        LocationData("Evacuation", "Evacuation: Reach Hanson", SC2WOL_LOC_ID_OFFSET + 404, LocationType.MISSION_PROGRESS),
        LocationData("Evacuation", "Evacuation: Secret Resource Stash", SC2WOL_LOC_ID_OFFSET + 405, LocationType.BONUS),
        LocationData("Evacuation", "Evacuation: Flawless", SC2WOL_LOC_ID_OFFSET + 406, LocationType.CHALLENGE,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, True, False) >= 2 and
                                   (logic_level > 0 and state._sc2wol_has_anti_air(multiworld, player)
                                    or state._sc2wol_has_competent_anti_air(multiworld, player))),
        LocationData("Outbreak", "Outbreak: Victory", SC2WOL_LOC_ID_OFFSET + 500, LocationType.VICTORY,
                     lambda state: state._sc2wol_defense_rating(multiworld, player, True, False) >= 4 and
                                   (state._sc2wol_has_common_unit(multiworld, player) or state.has("Reaper", player))),
        LocationData("Outbreak", "Outbreak: Left Infestor", SC2WOL_LOC_ID_OFFSET + 501, LocationType.BONUS,
                     lambda state: state._sc2wol_defense_rating(multiworld, player, True, False) >= 2 and
                                   (state._sc2wol_has_common_unit(multiworld, player) or state.has("Reaper", player))),
        LocationData("Outbreak", "Outbreak: Right Infestor", SC2WOL_LOC_ID_OFFSET + 502, LocationType.BONUS,
                     lambda state: state._sc2wol_defense_rating(multiworld, player, True, False) >= 2 and
                                   (state._sc2wol_has_common_unit(multiworld, player) or state.has("Reaper", player))),
        LocationData("Outbreak", "Outbreak: North Infested Command Center", SC2WOL_LOC_ID_OFFSET + 503, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_defense_rating(multiworld, player, True, False) >= 2 and
                                   (state._sc2wol_has_common_unit(multiworld, player) or state.has("Reaper", player))),
        LocationData("Outbreak", "Outbreak: South Infested Command Center", SC2WOL_LOC_ID_OFFSET + 504, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_defense_rating(multiworld, player, True, False) >= 2 and
                                   (state._sc2wol_has_common_unit(multiworld, player) or state.has("Reaper", player))),
        LocationData("Outbreak", "Outbreak: Northwest Bar", SC2WOL_LOC_ID_OFFSET + 505, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_defense_rating(multiworld, player, True, False) >= 2 and
                                   (state._sc2wol_has_common_unit(multiworld, player) or state.has("Reaper", player))),
        LocationData("Outbreak", "Outbreak: North Bar", SC2WOL_LOC_ID_OFFSET + 506, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_defense_rating(multiworld, player, True, False) >= 2 and
                                   (state._sc2wol_has_common_unit(multiworld, player) or state.has("Reaper", player))),
        LocationData("Outbreak", "Outbreak: South Bar", SC2WOL_LOC_ID_OFFSET + 507, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_defense_rating(multiworld, player, True, False) >= 2 and
                                   (state._sc2wol_has_common_unit(multiworld, player) or state.has("Reaper", player))),
        LocationData("Safe Haven", "Safe Haven: Victory", SC2WOL_LOC_ID_OFFSET + 600, LocationType.VICTORY,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_has_competent_anti_air(multiworld, player)),
        LocationData("Safe Haven", "Safe Haven: North Nexus", SC2WOL_LOC_ID_OFFSET + 601, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_has_competent_anti_air(multiworld, player)),
        LocationData("Safe Haven", "Safe Haven: East Nexus", SC2WOL_LOC_ID_OFFSET + 602, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_has_competent_anti_air(multiworld, player)),
        LocationData("Safe Haven", "Safe Haven: South Nexus", SC2WOL_LOC_ID_OFFSET + 603, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_has_competent_anti_air(multiworld, player)),
        LocationData("Safe Haven", "Safe Haven: First Terror Fleet", SC2WOL_LOC_ID_OFFSET + 604, LocationType.BONUS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_has_competent_anti_air(multiworld, player)),
        LocationData("Safe Haven", "Safe Haven: Second Terror Fleet", SC2WOL_LOC_ID_OFFSET + 605, LocationType.BONUS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_has_competent_anti_air(multiworld, player)),
        LocationData("Safe Haven", "Safe Haven: Third Terror Fleet", SC2WOL_LOC_ID_OFFSET + 606, LocationType.BONUS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_has_competent_anti_air(multiworld, player)),
        LocationData("Haven's Fall", "Haven's Fall: Victory", SC2WOL_LOC_ID_OFFSET + 700, LocationType.VICTORY,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_has_competent_anti_air(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, True) >= 3),
        LocationData("Haven's Fall", "Haven's Fall: North Hive", SC2WOL_LOC_ID_OFFSET + 701, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_has_competent_anti_air(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, True) >= 3),
        LocationData("Haven's Fall", "Haven's Fall: East Hive", SC2WOL_LOC_ID_OFFSET + 702, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_has_competent_anti_air(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, True) >= 3),
        LocationData("Haven's Fall", "Haven's Fall: South Hive", SC2WOL_LOC_ID_OFFSET + 703, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_has_competent_anti_air(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, True) >= 3),
        LocationData("Haven's Fall", "Haven's Fall: Northeast Colony Base", SC2WOL_LOC_ID_OFFSET + 704, LocationType.CHALLENGE,
                     lambda state: state._sc2wol_can_respond_to_colony_infestations),
        LocationData("Haven's Fall", "Haven's Fall: East Colony Base", SC2WOL_LOC_ID_OFFSET + 705, LocationType.CHALLENGE,
                     lambda state: state._sc2wol_can_respond_to_colony_infestations),
        LocationData("Haven's Fall", "Haven's Fall: Middle Colony Base", SC2WOL_LOC_ID_OFFSET + 706, LocationType.CHALLENGE,
                     lambda state: state._sc2wol_can_respond_to_colony_infestations),
        LocationData("Haven's Fall", "Haven's Fall: Southeast Colony Base", SC2WOL_LOC_ID_OFFSET + 707, LocationType.CHALLENGE,
                     lambda state: state._sc2wol_can_respond_to_colony_infestations),
        LocationData("Haven's Fall", "Haven's Fall: Southwest Colony Base", SC2WOL_LOC_ID_OFFSET + 708, LocationType.CHALLENGE,
                     lambda state: state._sc2wol_can_respond_to_colony_infestations),
        LocationData("Smash and Grab", "Smash and Grab: Victory", SC2WOL_LOC_ID_OFFSET + 800, LocationType.VICTORY,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   (logic_level > 0 and state._sc2wol_has_anti_air(multiworld, player)
                                    or state._sc2wol_has_competent_anti_air(multiworld, player))),
        LocationData("Smash and Grab", "Smash and Grab: First Relic", SC2WOL_LOC_ID_OFFSET + 801, LocationType.BONUS),
        LocationData("Smash and Grab", "Smash and Grab: Second Relic", SC2WOL_LOC_ID_OFFSET + 802, LocationType.BONUS),
        LocationData("Smash and Grab", "Smash and Grab: Third Relic", SC2WOL_LOC_ID_OFFSET + 803, LocationType.BONUS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   (logic_level > 0 and state._sc2wol_has_anti_air(multiworld, player)
                                    or state._sc2wol_has_competent_anti_air(multiworld, player))),
        LocationData("Smash and Grab", "Smash and Grab: Fourth Relic", SC2WOL_LOC_ID_OFFSET + 804, LocationType.BONUS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   (logic_level > 0 and state._sc2wol_has_anti_air(multiworld, player)
                                    or state._sc2wol_has_competent_anti_air(multiworld, player))),
        LocationData("Smash and Grab", "Smash and Grab: First Forcefield Area Busted", SC2WOL_LOC_ID_OFFSET + 805, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   (logic_level > 0 and state._sc2wol_has_anti_air(multiworld, player)
                                    or state._sc2wol_has_competent_anti_air(multiworld, player))),
        LocationData("Smash and Grab", "Smash and Grab: Second Forcefield Area Busted", SC2WOL_LOC_ID_OFFSET + 806, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   (logic_level > 0 and state._sc2wol_has_anti_air(multiworld, player)
                                    or state._sc2wol_has_competent_anti_air(multiworld, player))),
        LocationData("The Dig", "The Dig: Victory", SC2WOL_LOC_ID_OFFSET + 900, LocationType.VICTORY,
                     lambda state: state._sc2wol_has_anti_air(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, False) >= 7),
        LocationData("The Dig", "The Dig: Left Relic", SC2WOL_LOC_ID_OFFSET + 901, LocationType.BONUS,
                     lambda state: state._sc2wol_defense_rating(multiworld, player, False) >= 5),
        LocationData("The Dig", "The Dig: Right Ground Relic", SC2WOL_LOC_ID_OFFSET + 902, LocationType.BONUS,
                     lambda state: state._sc2wol_defense_rating(multiworld, player, False) >= 5),
        LocationData("The Dig", "The Dig: Right Cliff Relic", SC2WOL_LOC_ID_OFFSET + 903, LocationType.BONUS,
                     lambda state: state._sc2wol_defense_rating(multiworld, player, False) >= 5),
        LocationData("The Dig", "The Dig: Moebius Base", SC2WOL_LOC_ID_OFFSET + 904, LocationType.MISSION_PROGRESS),
        LocationData("The Moebius Factor", "The Moebius Factor: Victory", SC2WOL_LOC_ID_OFFSET + 1000, LocationType.VICTORY,
                     lambda state: state._sc2wol_has_anti_air(multiworld, player) and
                                   (state._sc2wol_has_air(multiworld, player)
                                    or state.has_any({'Medivac', 'Hercules'}, player)
                                    and state._sc2wol_has_common_unit(multiworld, player))),
        LocationData("The Moebius Factor", "The Moebius Factor: 1st Data Core", SC2WOL_LOC_ID_OFFSET + 1001, LocationType.MISSION_PROGRESS),
        LocationData("The Moebius Factor", "The Moebius Factor: 2nd Data Core", SC2WOL_LOC_ID_OFFSET + 1002, LocationType.MISSION_PROGRESS,
                     lambda state: (state._sc2wol_has_air(multiworld, player)
                                    or state.has_any({'Medivac', 'Hercules'}, player)
                                    and state._sc2wol_has_common_unit(multiworld, player))),
        LocationData("The Moebius Factor", "The Moebius Factor: South Rescue", SC2WOL_LOC_ID_OFFSET + 1003, LocationType.BONUS,
                     lambda state: state._sc2wol_able_to_rescue(multiworld, player)),
        LocationData("The Moebius Factor", "The Moebius Factor: Wall Rescue", SC2WOL_LOC_ID_OFFSET + 1004, LocationType.BONUS,
                     lambda state: state._sc2wol_able_to_rescue(multiworld, player)),
        LocationData("The Moebius Factor", "The Moebius Factor: Mid Rescue", SC2WOL_LOC_ID_OFFSET + 1005, LocationType.BONUS,
                     lambda state: state._sc2wol_able_to_rescue(multiworld, player)),
        LocationData("The Moebius Factor", "The Moebius Factor: Nydus Roof Rescue", SC2WOL_LOC_ID_OFFSET + 1006, LocationType.BONUS,
                     lambda state: state._sc2wol_able_to_rescue(multiworld, player)),
        LocationData("The Moebius Factor", "The Moebius Factor: Alive Inside Rescue", SC2WOL_LOC_ID_OFFSET + 1007, LocationType.BONUS,
                     lambda state: state._sc2wol_able_to_rescue(multiworld, player)),
        LocationData("The Moebius Factor", "The Moebius Factor: Brutalisk", SC2WOL_LOC_ID_OFFSET + 1008, LocationType.OPTIONAL_BOSS,
                     lambda state: state._sc2wol_has_anti_air(multiworld, player) and
                                   (state._sc2wol_has_air(multiworld, player)
                                    or state.has_any({'Medivac', 'Hercules'}, player)
                                    and state._sc2wol_has_common_unit(multiworld, player))),
        LocationData("The Moebius Factor", "The Moebius Factor: 3rd Data Core", SC2WOL_LOC_ID_OFFSET + 1009, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_anti_air(multiworld, player) and
                                   (state._sc2wol_has_air(multiworld, player)
                                    or state.has_any({'Medivac', 'Hercules'}, player)
                                    and state._sc2wol_has_common_unit(multiworld, player))),
        LocationData("Supernova", "Supernova: Victory", SC2WOL_LOC_ID_OFFSET + 1100, LocationType.VICTORY,
                     lambda state: state._sc2wol_beats_protoss_deathball(multiworld, player)),
        LocationData("Supernova", "Supernova: West Relic", SC2WOL_LOC_ID_OFFSET + 1101, LocationType.BONUS),
        LocationData("Supernova", "Supernova: North Relic", SC2WOL_LOC_ID_OFFSET + 1102, LocationType.BONUS),
        LocationData("Supernova", "Supernova: South Relic", SC2WOL_LOC_ID_OFFSET + 1103, LocationType.BONUS,
                     lambda state: state._sc2wol_beats_protoss_deathball(multiworld, player)),
        LocationData("Supernova", "Supernova: East Relic", SC2WOL_LOC_ID_OFFSET + 1104, LocationType.BONUS,
                     lambda state: state._sc2wol_beats_protoss_deathball(multiworld, player)),
        LocationData("Supernova", "Supernova: Landing Zone Cleared", SC2WOL_LOC_ID_OFFSET + 1105, LocationType.MISSION_PROGRESS),
        LocationData("Supernova", "Supernova: Middle Base", SC2WOL_LOC_ID_OFFSET + 1106, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_beats_protoss_deathball(multiworld, player)),
        LocationData("Supernova", "Supernova: Southeast Base", SC2WOL_LOC_ID_OFFSET + 1107, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_beats_protoss_deathball(multiworld, player)),
        LocationData("Maw of the Void", "Maw of the Void: Victory", SC2WOL_LOC_ID_OFFSET + 1200, LocationType.VICTORY,
                     lambda state: state._sc2wol_survives_rip_field(multiworld, player)),
        LocationData("Maw of the Void", "Maw of the Void: Landing Zone Cleared", SC2WOL_LOC_ID_OFFSET + 1201, LocationType.MISSION_PROGRESS),
        LocationData("Maw of the Void", "Maw of the Void: Expansion Prisoners", SC2WOL_LOC_ID_OFFSET + 1202, LocationType.BONUS,
                     lambda state: logic_level > 0 or state._sc2wol_survives_rip_field(multiworld, player)),
        LocationData("Maw of the Void", "Maw of the Void: South Close Prisoners", SC2WOL_LOC_ID_OFFSET + 1203, LocationType.BONUS,
                     lambda state: logic_level > 0 or state._sc2wol_survives_rip_field(multiworld, player)),
        LocationData("Maw of the Void", "Maw of the Void: South Far Prisoners", SC2WOL_LOC_ID_OFFSET + 1204, LocationType.BONUS,
                     lambda state: state._sc2wol_survives_rip_field(multiworld, player)),
        LocationData("Maw of the Void", "Maw of the Void: North Prisoners", SC2WOL_LOC_ID_OFFSET + 1205, LocationType.BONUS,
                     lambda state: state._sc2wol_survives_rip_field(multiworld, player)),
        LocationData("Maw of the Void", "Maw of the Void: Mothership", SC2WOL_LOC_ID_OFFSET + 1206, LocationType.OPTIONAL_BOSS,
                     lambda state: state._sc2wol_survives_rip_field(multiworld, player)),
        LocationData("Maw of the Void", "Maw of the Void: Expansion Rip Field Generator", SC2WOL_LOC_ID_OFFSET + 1207, LocationType.MISSION_PROGRESS,
                     lambda state: logic_level > 0 or state._sc2wol_survives_rip_field(multiworld, player)),
        LocationData("Maw of the Void", "Maw of the Void: Middle Rip Field Generator", SC2WOL_LOC_ID_OFFSET + 1208, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_survives_rip_field(multiworld, player)),
        LocationData("Maw of the Void", "Maw of the Void: Southeast Rip Field Generator", SC2WOL_LOC_ID_OFFSET + 1209, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_survives_rip_field(multiworld, player)),
        LocationData("Maw of the Void", "Maw of the Void: Stargate Rip Field Generator", SC2WOL_LOC_ID_OFFSET + 1210, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_survives_rip_field(multiworld, player)),
        LocationData("Maw of the Void", "Maw of the Void: Northwest Rip Field Generator", SC2WOL_LOC_ID_OFFSET + 1211, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_survives_rip_field(multiworld, player)),
        LocationData("Maw of the Void", "Maw of the Void: West Rip Field Generator", SC2WOL_LOC_ID_OFFSET + 1212, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_survives_rip_field(multiworld, player)),
        LocationData("Maw of the Void", "Maw of the Void: Southwest Rip Field Generator", SC2WOL_LOC_ID_OFFSET + 1213, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_survives_rip_field(multiworld, player)),
        LocationData("Devil's Playground", "Devil's Playground: Victory", SC2WOL_LOC_ID_OFFSET + 1300, LocationType.VICTORY,
                     lambda state: logic_level > 0 or
                                   state._sc2wol_has_anti_air(multiworld, player) and (
                                           state._sc2wol_has_common_unit(multiworld, player) or state.has("Reaper", player))),
        LocationData("Devil's Playground", "Devil's Playground: Tosh's Miners", SC2WOL_LOC_ID_OFFSET + 1301, LocationType.BONUS),
        LocationData("Devil's Playground", "Devil's Playground: Brutalisk", SC2WOL_LOC_ID_OFFSET + 1302, LocationType.OPTIONAL_BOSS,
                     lambda state: logic_level > 0 or state._sc2wol_has_common_unit(multiworld, player) or state.has("Reaper", player)),
        LocationData("Devil's Playground", "Devil's Playground: North Reapers", SC2WOL_LOC_ID_OFFSET + 1303, LocationType.BONUS),
        LocationData("Devil's Playground", "Devil's Playground: Middle Reapers", SC2WOL_LOC_ID_OFFSET + 1304, LocationType.BONUS,
                     lambda state: logic_level > 0 or state._sc2wol_has_common_unit(multiworld, player) or state.has("Reaper", player)),
        LocationData("Devil's Playground", "Devil's Playground: Southwest Reapers", SC2WOL_LOC_ID_OFFSET + 1305, LocationType.BONUS,
                     lambda state: logic_level > 0 or state._sc2wol_has_common_unit(multiworld, player) or state.has("Reaper", player)),
        LocationData("Devil's Playground", "Devil's Playground: Southeast Reapers", SC2WOL_LOC_ID_OFFSET + 1306, LocationType.BONUS,
                     lambda state: logic_level > 0 or
                                   state._sc2wol_has_anti_air(multiworld, player) and (
                                           state._sc2wol_has_common_unit(multiworld, player) or state.has("Reaper", player))),
        LocationData("Devil's Playground", "Devil's Playground: East Reapers", SC2WOL_LOC_ID_OFFSET + 1307, LocationType.BONUS,
                     lambda state: state._sc2wol_has_anti_air(multiworld, player) and
                                    (logic_level > 0 or
                                           state._sc2wol_has_common_unit(multiworld, player) or state.has("Reaper", player))),
        LocationData("Welcome to the Jungle", "Welcome to the Jungle: Victory", SC2WOL_LOC_ID_OFFSET + 1400, LocationType.VICTORY,
                     lambda state: state._sc2wol_welcome_to_the_jungle_requirement(multiworld, player)),
        LocationData("Welcome to the Jungle", "Welcome to the Jungle: Close Relic", SC2WOL_LOC_ID_OFFSET + 1401, LocationType.BONUS),
        LocationData("Welcome to the Jungle", "Welcome to the Jungle: West Relic", SC2WOL_LOC_ID_OFFSET + 1402, LocationType.BONUS,
                     lambda state: state._sc2wol_welcome_to_the_jungle_requirement(multiworld, player)),
        LocationData("Welcome to the Jungle", "Welcome to the Jungle: North-East Relic", SC2WOL_LOC_ID_OFFSET + 1403, LocationType.BONUS,
                     lambda state: state._sc2wol_welcome_to_the_jungle_requirement(multiworld, player)),
        LocationData("Welcome to the Jungle", "Welcome to the Jungle: Middle Base", SC2WOL_LOC_ID_OFFSET + 1404, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_welcome_to_the_jungle_requirement(multiworld, player)),
        LocationData("Welcome to the Jungle", "Welcome to the Jungle: Main Base", SC2WOL_LOC_ID_OFFSET + 1405, LocationType.CHALLENGE,
                     lambda state: state._sc2wol_welcome_to_the_jungle_requirement(multiworld, player)
                                    and state._sc2wol_beats_protoss_deathball(multiworld, player)),
        LocationData("Welcome to the Jungle", "Welcome to the Jungle: No Terrazine Nodes Sealed", SC2WOL_LOC_ID_OFFSET + 1406, LocationType.CHALLENGE,
                     lambda state: state._sc2wol_welcome_to_the_jungle_requirement(multiworld, player)
                                    and state._sc2wol_has_competent_ground_to_air(multiworld, player)
                                   and state._sc2wol_beats_protoss_deathball(multiworld, player)),
        LocationData("Welcome to the Jungle", "Welcome to the Jungle: Up to 1 Terrazine Node Sealed", SC2WOL_LOC_ID_OFFSET + 1407, LocationType.CHALLENGE,
                     lambda state: state._sc2wol_welcome_to_the_jungle_requirement(multiworld, player)
                                   and state._sc2wol_has_competent_ground_to_air(multiworld, player)
                                   and state._sc2wol_beats_protoss_deathball(multiworld, player)),
        LocationData("Welcome to the Jungle", "Welcome to the Jungle: Up to 2 Terrazine Nodes Sealed", SC2WOL_LOC_ID_OFFSET + 1408, LocationType.CHALLENGE,
                     lambda state: state._sc2wol_welcome_to_the_jungle_requirement(multiworld, player)
                                   and state._sc2wol_beats_protoss_deathball(multiworld, player)),
        LocationData("Welcome to the Jungle", "Welcome to the Jungle: Up to 3 Terrazine Nodes Sealed", SC2WOL_LOC_ID_OFFSET + 1409, LocationType.CHALLENGE,
                     lambda state: state._sc2wol_welcome_to_the_jungle_requirement(multiworld, player)
                                   and state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Welcome to the Jungle", "Welcome to the Jungle: Up to 4 Terrazine Nodes Sealed", SC2WOL_LOC_ID_OFFSET + 1410, LocationType.CHALLENGE,
                     lambda state: state._sc2wol_welcome_to_the_jungle_requirement(multiworld, player)),
        LocationData("Welcome to the Jungle", "Welcome to the Jungle: Up to 5 Terrazine Nodes Sealed", SC2WOL_LOC_ID_OFFSET + 1411, LocationType.CHALLENGE,
                     lambda state: state._sc2wol_welcome_to_the_jungle_requirement(multiworld, player)),
        LocationData("Breakout", "Breakout: Victory", SC2WOL_LOC_ID_OFFSET + 1500, LocationType.VICTORY),
        LocationData("Breakout", "Breakout: Diamondback Prison", SC2WOL_LOC_ID_OFFSET + 1501, LocationType.BONUS),
        LocationData("Breakout", "Breakout: Siege Tank Prison", SC2WOL_LOC_ID_OFFSET + 1502, LocationType.BONUS),
        LocationData("Breakout", "Breakout: First Checkpoint", SC2WOL_LOC_ID_OFFSET + 1503, LocationType.MISSION_PROGRESS),
        LocationData("Breakout", "Breakout: Second Checkpoint", SC2WOL_LOC_ID_OFFSET + 1504, LocationType.MISSION_PROGRESS),
        LocationData("Ghost of a Chance", "Ghost of a Chance: Victory", SC2WOL_LOC_ID_OFFSET + 1600, LocationType.VICTORY),
        LocationData("Ghost of a Chance", "Ghost of a Chance: Terrazine Tank", SC2WOL_LOC_ID_OFFSET + 1601, LocationType.MISSION_PROGRESS),
        LocationData("Ghost of a Chance", "Ghost of a Chance: Jorium Stockpile", SC2WOL_LOC_ID_OFFSET + 1602, LocationType.MISSION_PROGRESS),
        LocationData("Ghost of a Chance", "Ghost of a Chance: First Island Spectres", SC2WOL_LOC_ID_OFFSET + 1603, LocationType.BONUS),
        LocationData("Ghost of a Chance", "Ghost of a Chance: Second Island Spectres", SC2WOL_LOC_ID_OFFSET + 1604, LocationType.BONUS),
        LocationData("Ghost of a Chance", "Ghost of a Chance: Third Island Spectres", SC2WOL_LOC_ID_OFFSET + 1605, LocationType.BONUS),
        LocationData("The Great Train Robbery", "The Great Train Robbery: Victory", SC2WOL_LOC_ID_OFFSET + 1700, LocationType.VICTORY,
                     lambda state: state._sc2wol_has_train_killers(multiworld, player) and
                                   state._sc2wol_has_anti_air(multiworld, player)),
        LocationData("The Great Train Robbery", "The Great Train Robbery: North Defiler", SC2WOL_LOC_ID_OFFSET + 1701, LocationType.BONUS),
        LocationData("The Great Train Robbery", "The Great Train Robbery: Mid Defiler", SC2WOL_LOC_ID_OFFSET + 1702, LocationType.BONUS),
        LocationData("The Great Train Robbery", "The Great Train Robbery: South Defiler", SC2WOL_LOC_ID_OFFSET + 1703, LocationType.BONUS),
        LocationData("The Great Train Robbery", "The Great Train Robbery: Close Diamondback", SC2WOL_LOC_ID_OFFSET + 1704, LocationType.BONUS),
        LocationData("The Great Train Robbery", "The Great Train Robbery: Northwest Diamondback", SC2WOL_LOC_ID_OFFSET + 1705, LocationType.BONUS),
        LocationData("The Great Train Robbery", "The Great Train Robbery: North Diamondback", SC2WOL_LOC_ID_OFFSET + 1706, LocationType.BONUS),
        LocationData("The Great Train Robbery", "The Great Train Robbery: Northeast Diamondback", SC2WOL_LOC_ID_OFFSET + 1707, LocationType.BONUS),
        LocationData("The Great Train Robbery", "The Great Train Robbery: Southwest Diamondback", SC2WOL_LOC_ID_OFFSET + 1708, LocationType.BONUS),
        LocationData("The Great Train Robbery", "The Great Train Robbery: Southeast Diamondback", SC2WOL_LOC_ID_OFFSET + 1709, LocationType.BONUS),
        LocationData("The Great Train Robbery", "The Great Train Robbery: Kill Team", SC2WOL_LOC_ID_OFFSET + 1710, LocationType.CHALLENGE,
                     lambda state: (logic_level > 0 or state._sc2wol_has_common_unit(multiworld, player)) and
                                   state._sc2wol_has_train_killers(multiworld, player) and
                                   state._sc2wol_has_anti_air(multiworld, player)),
        LocationData("Cutthroat", "Cutthroat: Victory", SC2WOL_LOC_ID_OFFSET + 1800, LocationType.VICTORY,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   (logic_level > 0 or state._sc2wol_has_anti_air)),
        LocationData("Cutthroat", "Cutthroat: Mira Han", SC2WOL_LOC_ID_OFFSET + 1801, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player)),
        LocationData("Cutthroat", "Cutthroat: North Relic", SC2WOL_LOC_ID_OFFSET + 1802, LocationType.BONUS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player)),
        LocationData("Cutthroat", "Cutthroat: Mid Relic", SC2WOL_LOC_ID_OFFSET + 1803, LocationType.BONUS),
        LocationData("Cutthroat", "Cutthroat: Southwest Relic", SC2WOL_LOC_ID_OFFSET + 1804, LocationType.BONUS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player)),
        LocationData("Cutthroat", "Cutthroat: North Command Center", SC2WOL_LOC_ID_OFFSET + 1805, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player)),
        LocationData("Cutthroat", "Cutthroat: South Command Center", SC2WOL_LOC_ID_OFFSET + 1806, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player)),
        LocationData("Cutthroat", "Cutthroat: West Command Center", SC2WOL_LOC_ID_OFFSET + 1807, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player)),
        LocationData("Engine of Destruction", "Engine of Destruction: Victory", SC2WOL_LOC_ID_OFFSET + 1900, LocationType.VICTORY,
                     lambda state: state._sc2wol_has_competent_anti_air(multiworld, player) and
                                   state._sc2wol_has_common_unit(multiworld, player) or state.has('Wraith', player)),
        LocationData("Engine of Destruction", "Engine of Destruction: Odin", SC2WOL_LOC_ID_OFFSET + 1901, LocationType.MISSION_PROGRESS),
        LocationData("Engine of Destruction", "Engine of Destruction: Loki", SC2WOL_LOC_ID_OFFSET + 1902, LocationType.OPTIONAL_BOSS,
                     lambda state: state._sc2wol_has_competent_anti_air(multiworld, player) and
                                   state._sc2wol_has_common_unit(multiworld, player) or state.has('Wraith', player)),
        LocationData("Engine of Destruction", "Engine of Destruction: Lab Devourer", SC2WOL_LOC_ID_OFFSET + 1903, LocationType.BONUS),
        LocationData("Engine of Destruction", "Engine of Destruction: North Devourer", SC2WOL_LOC_ID_OFFSET + 1904, LocationType.BONUS,
                     lambda state: state._sc2wol_has_competent_anti_air(multiworld, player) and
                                   state._sc2wol_has_common_unit(multiworld, player) or state.has('Wraith', player)),
        LocationData("Engine of Destruction", "Engine of Destruction: Southeast Devourer", SC2WOL_LOC_ID_OFFSET + 1905, LocationType.BONUS,
                     lambda state: state._sc2wol_has_competent_anti_air(multiworld, player) and
                                   state._sc2wol_has_common_unit(multiworld, player) or state.has('Wraith', player)),
        LocationData("Engine of Destruction", "Engine of Destruction: West Base", SC2WOL_LOC_ID_OFFSET + 1906, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_competent_anti_air(multiworld, player) and
                                   state._sc2wol_has_common_unit(multiworld, player) or state.has('Wraith', player)),
        LocationData("Engine of Destruction", "Engine of Destruction: Northwest Base", SC2WOL_LOC_ID_OFFSET + 1907, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_competent_anti_air(multiworld, player) and
                                   state._sc2wol_has_common_unit(multiworld, player) or state.has('Wraith', player)),
        LocationData("Engine of Destruction", "Engine of Destruction: Northeast Base", SC2WOL_LOC_ID_OFFSET + 1908, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_competent_anti_air(multiworld, player) and
                                   state._sc2wol_has_common_unit(multiworld, player) or state.has('Wraith', player)),
        LocationData("Engine of Destruction", "Engine of Destruction: Southeast Base", SC2WOL_LOC_ID_OFFSET + 1909, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_competent_anti_air(multiworld, player) and
                                   state._sc2wol_has_common_unit(multiworld, player) or state.has('Wraith', player)),
        LocationData("Media Blitz", "Media Blitz: Victory", SC2WOL_LOC_ID_OFFSET + 2000, LocationType.VICTORY,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Media Blitz", "Media Blitz: Tower 1", SC2WOL_LOC_ID_OFFSET + 2001, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Media Blitz", "Media Blitz: Tower 2", SC2WOL_LOC_ID_OFFSET + 2002, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Media Blitz", "Media Blitz: Tower 3", SC2WOL_LOC_ID_OFFSET + 2003, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Media Blitz", "Media Blitz: Science Facility", SC2WOL_LOC_ID_OFFSET + 2004, LocationType.BONUS),
        LocationData("Media Blitz", "Media Blitz: All Barracks", SC2WOL_LOC_ID_OFFSET + 2005, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Media Blitz", "Media Blitz: All Factories", SC2WOL_LOC_ID_OFFSET + 2006, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Media Blitz", "Media Blitz: All Starports", SC2WOL_LOC_ID_OFFSET + 2007, LocationType.MISSION_PROGRESS,
                     lambda state: logic_level > 0 or state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Media Blitz", "Media Blitz: Odin Not Trashed", SC2WOL_LOC_ID_OFFSET + 2008, LocationType.CHALLENGE,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Piercing the Shroud", "Piercing the Shroud: Victory", SC2WOL_LOC_ID_OFFSET + 2100, LocationType.VICTORY,
                     lambda state: state._sc2wol_has_mm_upgrade(multiworld, player)),
        LocationData("Piercing the Shroud", "Piercing the Shroud: Holding Cell Relic", SC2WOL_LOC_ID_OFFSET + 2101, LocationType.BONUS),
        LocationData("Piercing the Shroud", "Piercing the Shroud: Brutalisk Relic", SC2WOL_LOC_ID_OFFSET + 2102, LocationType.BONUS,
                     lambda state: state._sc2wol_has_mm_upgrade(multiworld, player)),
        LocationData("Piercing the Shroud", "Piercing the Shroud: First Escape Relic", SC2WOL_LOC_ID_OFFSET + 2103,LocationType.BONUS,
                     lambda state: state._sc2wol_has_mm_upgrade(multiworld, player)),
        LocationData("Piercing the Shroud", "Piercing the Shroud: Second Escape Relic", SC2WOL_LOC_ID_OFFSET + 2104, LocationType.BONUS,
                     lambda state: state._sc2wol_has_mm_upgrade(multiworld, player)),
        LocationData("Piercing the Shroud", "Piercing the Shroud: Brutalisk", SC2WOL_LOC_ID_OFFSET + 2105, LocationType.OPTIONAL_BOSS,
                     lambda state: state._sc2wol_has_mm_upgrade(multiworld, player)),
        LocationData("Piercing the Shroud", "Piercing the Shroud: Fusion Reactor", SC2WOL_LOC_ID_OFFSET + 2106, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_mm_upgrade(multiworld, player)),
        LocationData("Whispers of Doom", "Whispers of Doom: Victory", SC2WOL_LOC_ID_OFFSET + 2200, LocationType.VICTORY),
        LocationData("Whispers of Doom", "Whispers of Doom: First Hatchery", SC2WOL_LOC_ID_OFFSET + 2201, LocationType.BONUS),
        LocationData("Whispers of Doom", "Whispers of Doom: Second Hatchery", SC2WOL_LOC_ID_OFFSET + 2202, LocationType.BONUS),
        LocationData("Whispers of Doom", "Whispers of Doom: Third Hatchery", SC2WOL_LOC_ID_OFFSET + 2203, LocationType.BONUS),
        LocationData("Whispers of Doom", "Whispers of Doom: First Prophecy Fragment", SC2WOL_LOC_ID_OFFSET + 2204, LocationType.MISSION_PROGRESS),
        LocationData("Whispers of Doom", "Whispers of Doom: Second Prophecy Fragment", SC2WOL_LOC_ID_OFFSET + 2205, LocationType.MISSION_PROGRESS),
        LocationData("Whispers of Doom", "Whispers of Doom: Third Prophecy Fragment", SC2WOL_LOC_ID_OFFSET + 2206, LocationType.MISSION_PROGRESS),
        LocationData("A Sinister Turn", "A Sinister Turn: Victory", SC2WOL_LOC_ID_OFFSET + 2300, LocationType.VICTORY,
                     lambda state: state._sc2wol_has_protoss_medium_units(multiworld, player)),
        LocationData("A Sinister Turn", "A Sinister Turn: Robotics Facility", SC2WOL_LOC_ID_OFFSET + 2301, LocationType.BONUS,
                     lambda state: logic_level > 0 or state._sc2wol_has_protoss_common_units(multiworld, player)),
        LocationData("A Sinister Turn", "A Sinister Turn: Dark Shrine", SC2WOL_LOC_ID_OFFSET + 2302, LocationType.BONUS,
                     lambda state: logic_level > 0 or state._sc2wol_has_protoss_common_units(multiworld, player)),
        LocationData("A Sinister Turn", "A Sinister Turn: Templar Archives", SC2WOL_LOC_ID_OFFSET + 2303, LocationType.BONUS,
                     lambda state: state._sc2wol_has_protoss_medium_units(multiworld, player)),
        LocationData("A Sinister Turn", "A Sinister Turn: Northeast Base", SC2WOL_LOC_ID_OFFSET + 2304, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_protoss_medium_units(multiworld, player)),
        LocationData("A Sinister Turn", "A Sinister Turn: Southwest Base", SC2WOL_LOC_ID_OFFSET + 2305, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_protoss_medium_units(multiworld, player)),
        LocationData("A Sinister Turn", "A Sinister Turn: Maar", SC2WOL_LOC_ID_OFFSET + 2306, LocationType.MISSION_PROGRESS,
                     lambda state: logic_level > 0 or state._sc2wol_has_protoss_medium_units(multiworld, player)),
        LocationData("A Sinister Turn", "A Sinister Turn: Northwest Preserver", SC2WOL_LOC_ID_OFFSET + 2307, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_protoss_medium_units(multiworld, player)),
        LocationData("A Sinister Turn", "A Sinister Turn: Southwest Preserver", SC2WOL_LOC_ID_OFFSET + 2308, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_protoss_medium_units(multiworld, player)),
        LocationData("A Sinister Turn", "A Sinister Turn: East Preserver", SC2WOL_LOC_ID_OFFSET + 2309, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_protoss_medium_units(multiworld, player)),
        LocationData("Echoes of the Future", "Echoes of the Future: Victory", SC2WOL_LOC_ID_OFFSET + 2400, LocationType.VICTORY,
                     lambda state: logic_level > 0 or state._sc2wol_has_protoss_medium_units(multiworld, player)),
        LocationData("Echoes of the Future", "Echoes of the Future: Close Obelisk", SC2WOL_LOC_ID_OFFSET + 2401, LocationType.BONUS),
        LocationData("Echoes of the Future", "Echoes of the Future: West Obelisk", SC2WOL_LOC_ID_OFFSET + 2402, LocationType.BONUS,
                     lambda state: logic_level > 0 or state._sc2wol_has_protoss_common_units(multiworld, player)),
        LocationData("Echoes of the Future", "Echoes of the Future: Base", SC2WOL_LOC_ID_OFFSET + 2403, LocationType.MISSION_PROGRESS),
        LocationData("Echoes of the Future", "Echoes of the Future: Southwest Tendril", SC2WOL_LOC_ID_OFFSET + 2404, LocationType.MISSION_PROGRESS),
        LocationData("Echoes of the Future", "Echoes of the Future: Southeast Tendril", SC2WOL_LOC_ID_OFFSET + 2405, LocationType.MISSION_PROGRESS,
                     lambda state: logic_level > 0 or state._sc2wol_has_protoss_common_units(multiworld, player)),
        LocationData("Echoes of the Future", "Echoes of the Future: Northeast Tendril", SC2WOL_LOC_ID_OFFSET + 2406, LocationType.MISSION_PROGRESS,
                     lambda state: logic_level > 0 or state._sc2wol_has_protoss_common_units(multiworld, player)),
        LocationData("Echoes of the Future", "Echoes of the Future: Northwest Tendril", SC2WOL_LOC_ID_OFFSET + 2407, LocationType.MISSION_PROGRESS,
                     lambda state: logic_level > 0 or state._sc2wol_has_protoss_common_units(multiworld, player)),
        LocationData("In Utter Darkness", "In Utter Darkness: Defeat", SC2WOL_LOC_ID_OFFSET + 2500, LocationType.VICTORY),
        LocationData("In Utter Darkness", "In Utter Darkness: Protoss Archive", SC2WOL_LOC_ID_OFFSET + 2501, LocationType.BONUS,
                     lambda state: state._sc2wol_has_protoss_medium_units(multiworld, player)),
        LocationData("In Utter Darkness", "In Utter Darkness: Kills", SC2WOL_LOC_ID_OFFSET + 2502, LocationType.CHALLENGE,
                     lambda state: state._sc2wol_has_protoss_common_units(multiworld, player)),
        LocationData("In Utter Darkness", "In Utter Darkness: Urun", SC2WOL_LOC_ID_OFFSET + 2503, LocationType.MISSION_PROGRESS),
        LocationData("In Utter Darkness", "In Utter Darkness: Mohandar", SC2WOL_LOC_ID_OFFSET + 2504, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_protoss_common_units(multiworld, player)),
        LocationData("In Utter Darkness", "In Utter Darkness: Selendis", SC2WOL_LOC_ID_OFFSET + 2505, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_protoss_common_units(multiworld, player)),
        LocationData("In Utter Darkness", "In Utter Darkness: Artanis", SC2WOL_LOC_ID_OFFSET + 2506, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_protoss_common_units(multiworld, player)),
        LocationData("Gates of Hell", "Gates of Hell: Victory", SC2WOL_LOC_ID_OFFSET + 2600, LocationType.VICTORY,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, True) > 6),
        LocationData("Gates of Hell", "Gates of Hell: Large Army", SC2WOL_LOC_ID_OFFSET + 2601, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, True) > 6),
        LocationData("Gates of Hell", "Gates of Hell: 2 Drop Pods", SC2WOL_LOC_ID_OFFSET + 2602, LocationType.BONUS,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, True) > 6),
        LocationData("Gates of Hell", "Gates of Hell: 4 Drop Pods", SC2WOL_LOC_ID_OFFSET + 2603, LocationType.BONUS,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, True) > 6),
        LocationData("Gates of Hell", "Gates of Hell: 6 Drop Pods", SC2WOL_LOC_ID_OFFSET + 2604, LocationType.BONUS,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, True) > 6),
        LocationData("Gates of Hell", "Gates of Hell: 8 Drop Pods", SC2WOL_LOC_ID_OFFSET + 2605, LocationType.BONUS,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, True) > 6),
        LocationData("Belly of the Beast", "Belly of the Beast: Victory", SC2WOL_LOC_ID_OFFSET + 2700, LocationType.VICTORY),
        LocationData("Belly of the Beast", "Belly of the Beast: First Charge", SC2WOL_LOC_ID_OFFSET + 2701, LocationType.MISSION_PROGRESS),
        LocationData("Belly of the Beast", "Belly of the Beast: Second Charge", SC2WOL_LOC_ID_OFFSET + 2702, LocationType.MISSION_PROGRESS),
        LocationData("Belly of the Beast", "Belly of the Beast: Third Charge", SC2WOL_LOC_ID_OFFSET + 2703, LocationType.MISSION_PROGRESS),
        LocationData("Belly of the Beast", "Belly of the Beast: First Group Rescued", SC2WOL_LOC_ID_OFFSET + 2704, LocationType.BONUS),
        LocationData("Belly of the Beast", "Belly of the Beast: Second Group Rescued", SC2WOL_LOC_ID_OFFSET + 2705, LocationType.BONUS),
        LocationData("Belly of the Beast", "Belly of the Beast: Third Group Rescued", SC2WOL_LOC_ID_OFFSET + 2706, LocationType.BONUS),
        LocationData("Shatter the Sky", "Shatter the Sky: Victory", SC2WOL_LOC_ID_OFFSET + 2800, LocationType.VICTORY,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Shatter the Sky", "Shatter the Sky: Close Coolant Tower", SC2WOL_LOC_ID_OFFSET + 2801, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Shatter the Sky", "Shatter the Sky: Northwest Coolant Tower", SC2WOL_LOC_ID_OFFSET + 2802, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Shatter the Sky", "Shatter the Sky: Southeast Coolant Tower", SC2WOL_LOC_ID_OFFSET + 2803, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Shatter the Sky", "Shatter the Sky: Southwest Coolant Tower", SC2WOL_LOC_ID_OFFSET + 2804, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Shatter the Sky", "Shatter the Sky: Leviathan", SC2WOL_LOC_ID_OFFSET + 2805, LocationType.OPTIONAL_BOSS,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Shatter the Sky", "Shatter the Sky: East Hatchery", SC2WOL_LOC_ID_OFFSET + 2806, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Shatter the Sky", "Shatter the Sky: North Hatchery", SC2WOL_LOC_ID_OFFSET + 2807, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Shatter the Sky", "Shatter the Sky: Mid Hatchery", SC2WOL_LOC_ID_OFFSET + 2808, LocationType.MISSION_PROGRESS,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("All-In", "All-In: Victory", None, LocationType.VICTORY,
                     lambda state: state._sc2wol_final_mission_requirements(multiworld, player))
    ]

    beat_events = []

    for i, location_data in enumerate(location_table):
        # Removing all item-based logic on No Logic
        if logic_level == 2:
            location_data = location_data._replace(rule=Location.access_rule)
            location_table[i] = location_data
        # Generating Beat event locations
        if location_data.name.endswith((": Victory", ": Defeat")):
            beat_events.append(
                location_data._replace(name="Beat " + location_data.name.rsplit(": ", 1)[0], code=None)
            )
    return tuple(location_table + beat_events)
