from typing import List, Tuple, Optional, Callable, NamedTuple
from BaseClasses import MultiWorld
from .Options import get_option_value

from BaseClasses import Location

SC2WOL_LOC_ID_OFFSET = 1000


class SC2WoLLocation(Location):
    game: str = "Starcraft2WoL"


class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]
    rule: Callable = lambda state: True


def get_locations(multiworld: Optional[MultiWorld], player: Optional[int]) -> Tuple[LocationData, ...]:
    # Note: rules which are ended with or True are rules identified as needed later when restricted units is an option
    logic_level = get_option_value(multiworld, player, 'required_tactics')
    location_table: List[LocationData] = [
        LocationData("Liberation Day", "Liberation Day: Victory", SC2WOL_LOC_ID_OFFSET + 100),
        LocationData("Liberation Day", "Liberation Day: First Statue", SC2WOL_LOC_ID_OFFSET + 101),
        LocationData("Liberation Day", "Liberation Day: Second Statue", SC2WOL_LOC_ID_OFFSET + 102),
        LocationData("Liberation Day", "Liberation Day: Third Statue", SC2WOL_LOC_ID_OFFSET + 103),
        LocationData("Liberation Day", "Liberation Day: Fourth Statue", SC2WOL_LOC_ID_OFFSET + 104),
        LocationData("Liberation Day", "Liberation Day: Fifth Statue", SC2WOL_LOC_ID_OFFSET + 105),
        LocationData("Liberation Day", "Liberation Day: Sixth Statue", SC2WOL_LOC_ID_OFFSET + 106),
        LocationData("The Outlaws", "The Outlaws: Victory", SC2WOL_LOC_ID_OFFSET + 200,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player)),
        LocationData("The Outlaws", "The Outlaws: Rebel Base", SC2WOL_LOC_ID_OFFSET + 201,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player)),
        LocationData("Zero Hour", "Zero Hour: Victory", SC2WOL_LOC_ID_OFFSET + 300,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, True) >= 2 and
                                   (logic_level > 0 or state._sc2wol_has_anti_air(multiworld, player))),
        LocationData("Zero Hour", "Zero Hour: First Group Rescued", SC2WOL_LOC_ID_OFFSET + 301),
        LocationData("Zero Hour", "Zero Hour: Second Group Rescued", SC2WOL_LOC_ID_OFFSET + 302,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player)),
        LocationData("Zero Hour", "Zero Hour: Third Group Rescued", SC2WOL_LOC_ID_OFFSET + 303,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, True) >= 2),
        LocationData("Evacuation", "Evacuation: Victory", SC2WOL_LOC_ID_OFFSET + 400,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   (logic_level > 0 and state._sc2wol_has_anti_air(multiworld, player)
                                    or state._sc2wol_has_competent_anti_air(multiworld, player))),
        LocationData("Evacuation", "Evacuation: First Chysalis", SC2WOL_LOC_ID_OFFSET + 401),
        LocationData("Evacuation", "Evacuation: Second Chysalis", SC2WOL_LOC_ID_OFFSET + 402,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player)),
        LocationData("Evacuation", "Evacuation: Third Chysalis", SC2WOL_LOC_ID_OFFSET + 403,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player)),
        LocationData("Outbreak", "Outbreak: Victory", SC2WOL_LOC_ID_OFFSET + 500,
                     lambda state: state._sc2wol_defense_rating(multiworld, player, True, False) >= 4 and
                                   (state._sc2wol_has_common_unit(multiworld, player) or state.has("Reaper", player))),
        LocationData("Outbreak", "Outbreak: Left Infestor", SC2WOL_LOC_ID_OFFSET + 501,
                     lambda state: state._sc2wol_defense_rating(multiworld, player, True, False) >= 2 and
                                   (state._sc2wol_has_common_unit(multiworld, player) or state.has("Reaper", player))),
        LocationData("Outbreak", "Outbreak: Right Infestor", SC2WOL_LOC_ID_OFFSET + 502,
                     lambda state: state._sc2wol_defense_rating(multiworld, player, True, False) >= 2 and
                                   (state._sc2wol_has_common_unit(multiworld, player) or state.has("Reaper", player))),
        LocationData("Safe Haven", "Safe Haven: Victory", SC2WOL_LOC_ID_OFFSET + 600,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_has_competent_anti_air(multiworld, player)),
        LocationData("Safe Haven", "Safe Haven: North Nexus", SC2WOL_LOC_ID_OFFSET + 601,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_has_competent_anti_air(multiworld, player)),
        LocationData("Safe Haven", "Safe Haven: East Nexus", SC2WOL_LOC_ID_OFFSET + 602,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_has_competent_anti_air(multiworld, player)),
        LocationData("Safe Haven", "Safe Haven: South Nexus", SC2WOL_LOC_ID_OFFSET + 603,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_has_competent_anti_air(multiworld, player)),
        LocationData("Haven's Fall", "Haven's Fall: Victory", SC2WOL_LOC_ID_OFFSET + 700,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_has_competent_anti_air(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, True) >= 3),
        LocationData("Haven's Fall", "Haven's Fall: North Hive", SC2WOL_LOC_ID_OFFSET + 701,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_has_competent_anti_air(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, True) >= 3),
        LocationData("Haven's Fall", "Haven's Fall: East Hive", SC2WOL_LOC_ID_OFFSET + 702,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_has_competent_anti_air(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, True) >= 3),
        LocationData("Haven's Fall", "Haven's Fall: South Hive", SC2WOL_LOC_ID_OFFSET + 703,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_has_competent_anti_air(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, True) >= 3),
        LocationData("Smash and Grab", "Smash and Grab: Victory", SC2WOL_LOC_ID_OFFSET + 800,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   (logic_level > 0 and state._sc2wol_has_anti_air(multiworld, player)
                                    or state._sc2wol_has_competent_anti_air(multiworld, player))),
        LocationData("Smash and Grab", "Smash and Grab: First Relic", SC2WOL_LOC_ID_OFFSET + 801),
        LocationData("Smash and Grab", "Smash and Grab: Second Relic", SC2WOL_LOC_ID_OFFSET + 802),
        LocationData("Smash and Grab", "Smash and Grab: Third Relic", SC2WOL_LOC_ID_OFFSET + 803,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   (logic_level > 0 and state._sc2wol_has_anti_air(multiworld, player)
                                    or state._sc2wol_has_competent_anti_air(multiworld, player))),
        LocationData("Smash and Grab", "Smash and Grab: Fourth Relic", SC2WOL_LOC_ID_OFFSET + 804,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   (logic_level > 0 and state._sc2wol_has_anti_air(multiworld, player)
                                    or state._sc2wol_has_competent_anti_air(multiworld, player))),
        LocationData("The Dig", "The Dig: Victory", SC2WOL_LOC_ID_OFFSET + 900,
                     lambda state: state._sc2wol_has_anti_air(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, False) >= 7),
        LocationData("The Dig", "The Dig: Left Relic", SC2WOL_LOC_ID_OFFSET + 901,
                     lambda state: state._sc2wol_defense_rating(multiworld, player, False) >= 5),
        LocationData("The Dig", "The Dig: Right Ground Relic", SC2WOL_LOC_ID_OFFSET + 902,
                     lambda state: state._sc2wol_defense_rating(multiworld, player, False) >= 5),
        LocationData("The Dig", "The Dig: Right Cliff Relic", SC2WOL_LOC_ID_OFFSET + 903,
                     lambda state: state._sc2wol_defense_rating(multiworld, player, False) >= 5),
        LocationData("The Moebius Factor", "The Moebius Factor: Victory", SC2WOL_LOC_ID_OFFSET + 1000,
                     lambda state: state._sc2wol_has_anti_air(multiworld, player) and
                                   (state._sc2wol_has_air(multiworld, player)
                                    or state.has_any({'Medivac', 'Hercules'}, player)
                                    and state._sc2wol_has_common_unit(multiworld, player))),
        LocationData("The Moebius Factor", "The Moebius Factor: South Rescue", SC2WOL_LOC_ID_OFFSET + 1003,
                     lambda state: state._sc2wol_able_to_rescue(multiworld, player)),
        LocationData("The Moebius Factor", "The Moebius Factor: Wall Rescue", SC2WOL_LOC_ID_OFFSET + 1004,
                     lambda state: state._sc2wol_able_to_rescue(multiworld, player)),
        LocationData("The Moebius Factor", "The Moebius Factor: Mid Rescue", SC2WOL_LOC_ID_OFFSET + 1005,
                     lambda state: state._sc2wol_able_to_rescue(multiworld, player)),
        LocationData("The Moebius Factor", "The Moebius Factor: Nydus Roof Rescue", SC2WOL_LOC_ID_OFFSET + 1006,
                     lambda state: state._sc2wol_able_to_rescue(multiworld, player)),
        LocationData("The Moebius Factor", "The Moebius Factor: Alive Inside Rescue", SC2WOL_LOC_ID_OFFSET + 1007,
                     lambda state: state._sc2wol_able_to_rescue(multiworld, player)),
        LocationData("The Moebius Factor", "The Moebius Factor: Brutalisk", SC2WOL_LOC_ID_OFFSET + 1008,
                     lambda state: state._sc2wol_has_anti_air(multiworld, player) and
                                   (state._sc2wol_has_air(multiworld, player)
                                    or state.has_any({'Medivac', 'Hercules'}, player)
                                    and state._sc2wol_has_common_unit(multiworld, player))),
        LocationData("Supernova", "Supernova: Victory", SC2WOL_LOC_ID_OFFSET + 1100,
                     lambda state: state._sc2wol_beats_protoss_deathball(multiworld, player)),
        LocationData("Supernova", "Supernova: West Relic", SC2WOL_LOC_ID_OFFSET + 1101),
        LocationData("Supernova", "Supernova: North Relic", SC2WOL_LOC_ID_OFFSET + 1102),
        LocationData("Supernova", "Supernova: South Relic", SC2WOL_LOC_ID_OFFSET + 1103,
                     lambda state: state._sc2wol_beats_protoss_deathball(multiworld, player)),
        LocationData("Supernova", "Supernova: East Relic", SC2WOL_LOC_ID_OFFSET + 1104,
                     lambda state: state._sc2wol_beats_protoss_deathball(multiworld, player)),
        LocationData("Maw of the Void", "Maw of the Void: Victory", SC2WOL_LOC_ID_OFFSET + 1200,
                     lambda state: state._sc2wol_survives_rip_field(multiworld, player)),
        LocationData("Maw of the Void", "Maw of the Void: Landing Zone Cleared", SC2WOL_LOC_ID_OFFSET + 1201),
        LocationData("Maw of the Void", "Maw of the Void: Expansion Prisoners", SC2WOL_LOC_ID_OFFSET + 1202,
                     lambda state: logic_level > 0 or state._sc2wol_survives_rip_field(multiworld, player)),
        LocationData("Maw of the Void", "Maw of the Void: South Close Prisoners", SC2WOL_LOC_ID_OFFSET + 1203,
                     lambda state: logic_level > 0 or state._sc2wol_survives_rip_field(multiworld, player)),
        LocationData("Maw of the Void", "Maw of the Void: South Far Prisoners", SC2WOL_LOC_ID_OFFSET + 1204,
                     lambda state: state._sc2wol_survives_rip_field(multiworld, player)),
        LocationData("Maw of the Void", "Maw of the Void: North Prisoners", SC2WOL_LOC_ID_OFFSET + 1205,
                     lambda state: state._sc2wol_survives_rip_field(multiworld, player)),
        LocationData("Devil's Playground", "Devil's Playground: Victory", SC2WOL_LOC_ID_OFFSET + 1300,
                     lambda state: logic_level > 0 or
                                   state._sc2wol_has_anti_air(multiworld, player) and (
                                           state._sc2wol_has_common_unit(multiworld, player) or state.has("Reaper", player))),
        LocationData("Devil's Playground", "Devil's Playground: Tosh's Miners", SC2WOL_LOC_ID_OFFSET + 1301),
        LocationData("Devil's Playground", "Devil's Playground: Brutalisk", SC2WOL_LOC_ID_OFFSET + 1302,
                     lambda state: logic_level > 0 or state._sc2wol_has_common_unit(multiworld, player) or state.has("Reaper", player)),
        LocationData("Welcome to the Jungle", "Welcome to the Jungle: Victory", SC2WOL_LOC_ID_OFFSET + 1400,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_has_competent_anti_air(multiworld, player)),
        LocationData("Welcome to the Jungle", "Welcome to the Jungle: Close Relic", SC2WOL_LOC_ID_OFFSET + 1401),
        LocationData("Welcome to the Jungle", "Welcome to the Jungle: West Relic", SC2WOL_LOC_ID_OFFSET + 1402,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_has_competent_anti_air(multiworld, player)),
        LocationData("Welcome to the Jungle", "Welcome to the Jungle: North-East Relic", SC2WOL_LOC_ID_OFFSET + 1403,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   state._sc2wol_has_competent_anti_air(multiworld, player)),
        LocationData("Breakout", "Breakout: Victory", SC2WOL_LOC_ID_OFFSET + 1500),
        LocationData("Breakout", "Breakout: Diamondback Prison", SC2WOL_LOC_ID_OFFSET + 1501),
        LocationData("Breakout", "Breakout: Siegetank Prison", SC2WOL_LOC_ID_OFFSET + 1502),
        LocationData("Ghost of a Chance", "Ghost of a Chance: Victory", SC2WOL_LOC_ID_OFFSET + 1600),
        LocationData("Ghost of a Chance", "Ghost of a Chance: Terrazine Tank", SC2WOL_LOC_ID_OFFSET + 1601),
        LocationData("Ghost of a Chance", "Ghost of a Chance: Jorium Stockpile", SC2WOL_LOC_ID_OFFSET + 1602),
        LocationData("Ghost of a Chance", "Ghost of a Chance: First Island Spectres", SC2WOL_LOC_ID_OFFSET + 1603),
        LocationData("Ghost of a Chance", "Ghost of a Chance: Second Island Spectres", SC2WOL_LOC_ID_OFFSET + 1604),
        LocationData("Ghost of a Chance", "Ghost of a Chance: Third Island Spectres", SC2WOL_LOC_ID_OFFSET + 1605),
        LocationData("The Great Train Robbery", "The Great Train Robbery: Victory", SC2WOL_LOC_ID_OFFSET + 1700,
                     lambda state: state._sc2wol_has_train_killers(multiworld, player) and
                                   state._sc2wol_has_anti_air(multiworld, player)),
        LocationData("The Great Train Robbery", "The Great Train Robbery: North Defiler", SC2WOL_LOC_ID_OFFSET + 1701),
        LocationData("The Great Train Robbery", "The Great Train Robbery: Mid Defiler", SC2WOL_LOC_ID_OFFSET + 1702),
        LocationData("The Great Train Robbery", "The Great Train Robbery: South Defiler", SC2WOL_LOC_ID_OFFSET + 1703),
        LocationData("Cutthroat", "Cutthroat: Victory", SC2WOL_LOC_ID_OFFSET + 1800,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player) and
                                   (logic_level > 0 or state._sc2wol_has_anti_air)),
        LocationData("Cutthroat", "Cutthroat: Mira Han", SC2WOL_LOC_ID_OFFSET + 1801,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player)),
        LocationData("Cutthroat", "Cutthroat: North Relic", SC2WOL_LOC_ID_OFFSET + 1802,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player)),
        LocationData("Cutthroat", "Cutthroat: Mid Relic", SC2WOL_LOC_ID_OFFSET + 1803),
        LocationData("Cutthroat", "Cutthroat: Southwest Relic", SC2WOL_LOC_ID_OFFSET + 1804,
                     lambda state: state._sc2wol_has_common_unit(multiworld, player)),
        LocationData("Engine of Destruction", "Engine of Destruction: Victory", SC2WOL_LOC_ID_OFFSET + 1900,
                     lambda state: state._sc2wol_has_competent_anti_air(multiworld, player) and
                                   state._sc2wol_has_common_unit(multiworld, player) or state.has('Wraith', player)),
        LocationData("Engine of Destruction", "Engine of Destruction: Odin", SC2WOL_LOC_ID_OFFSET + 1901),
        LocationData("Engine of Destruction", "Engine of Destruction: Loki", SC2WOL_LOC_ID_OFFSET + 1902,
                     lambda state: state._sc2wol_has_competent_anti_air(multiworld, player) and
                                   state._sc2wol_has_common_unit(multiworld, player) or state.has('Wraith', player)),
        LocationData("Engine of Destruction", "Engine of Destruction: Lab Devourer", SC2WOL_LOC_ID_OFFSET + 1903),
        LocationData("Engine of Destruction", "Engine of Destruction: North Devourer", SC2WOL_LOC_ID_OFFSET + 1904,
                     lambda state: state._sc2wol_has_competent_anti_air(multiworld, player) and
                                   state._sc2wol_has_common_unit(multiworld, player) or state.has('Wraith', player)),
        LocationData("Engine of Destruction", "Engine of Destruction: Southeast Devourer", SC2WOL_LOC_ID_OFFSET + 1905,
                     lambda state: state._sc2wol_has_competent_anti_air(multiworld, player) and
                                   state._sc2wol_has_common_unit(multiworld, player) or state.has('Wraith', player)),
        LocationData("Media Blitz", "Media Blitz: Victory", SC2WOL_LOC_ID_OFFSET + 2000,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Media Blitz", "Media Blitz: Tower 1", SC2WOL_LOC_ID_OFFSET + 2001,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Media Blitz", "Media Blitz: Tower 2", SC2WOL_LOC_ID_OFFSET + 2002,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Media Blitz", "Media Blitz: Tower 3", SC2WOL_LOC_ID_OFFSET + 2003,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Media Blitz", "Media Blitz: Science Facility", SC2WOL_LOC_ID_OFFSET + 2004),
        LocationData("Piercing the Shroud", "Piercing the Shroud: Victory", SC2WOL_LOC_ID_OFFSET + 2100,
                     lambda state: state._sc2wol_has_mm_upgrade(multiworld, player)),
        LocationData("Piercing the Shroud", "Piercing the Shroud: Holding Cell Relic", SC2WOL_LOC_ID_OFFSET + 2101),
        LocationData("Piercing the Shroud", "Piercing the Shroud: Brutalisk Relic", SC2WOL_LOC_ID_OFFSET + 2102,
                     lambda state: state._sc2wol_has_mm_upgrade(multiworld, player)),
        LocationData("Piercing the Shroud", "Piercing the Shroud: First Escape Relic", SC2WOL_LOC_ID_OFFSET + 2103,
                     lambda state: state._sc2wol_has_mm_upgrade(multiworld, player)),
        LocationData("Piercing the Shroud", "Piercing the Shroud: Second Escape Relic", SC2WOL_LOC_ID_OFFSET + 2104,
                     lambda state: state._sc2wol_has_mm_upgrade(multiworld, player)),
        LocationData("Piercing the Shroud", "Piercing the Shroud: Brutalisk", SC2WOL_LOC_ID_OFFSET + 2105,
                     lambda state: state._sc2wol_has_mm_upgrade(multiworld, player)),
        LocationData("Whispers of Doom", "Whispers of Doom: Victory", SC2WOL_LOC_ID_OFFSET + 2200),
        LocationData("Whispers of Doom", "Whispers of Doom: First Hatchery", SC2WOL_LOC_ID_OFFSET + 2201),
        LocationData("Whispers of Doom", "Whispers of Doom: Second Hatchery", SC2WOL_LOC_ID_OFFSET + 2202),
        LocationData("Whispers of Doom", "Whispers of Doom: Third Hatchery", SC2WOL_LOC_ID_OFFSET + 2203),
        LocationData("A Sinister Turn", "A Sinister Turn: Victory", SC2WOL_LOC_ID_OFFSET + 2300,
                     lambda state: state._sc2wol_has_protoss_medium_units(multiworld, player)),
        LocationData("A Sinister Turn", "A Sinister Turn: Robotics Facility", SC2WOL_LOC_ID_OFFSET + 2301,
                     lambda state: logic_level > 0 or state._sc2wol_has_protoss_common_units(multiworld, player)),
        LocationData("A Sinister Turn", "A Sinister Turn: Dark Shrine", SC2WOL_LOC_ID_OFFSET + 2302,
                     lambda state: logic_level > 0 or state._sc2wol_has_protoss_common_units(multiworld, player)),
        LocationData("A Sinister Turn", "A Sinister Turn: Templar Archives", SC2WOL_LOC_ID_OFFSET + 2303,
                     lambda state: state._sc2wol_has_protoss_common_units(multiworld, player)),
        LocationData("Echoes of the Future", "Echoes of the Future: Victory", SC2WOL_LOC_ID_OFFSET + 2400,
                     lambda state: logic_level > 0 or state._sc2wol_has_protoss_medium_units(multiworld, player)),
        LocationData("Echoes of the Future", "Echoes of the Future: Close Obelisk", SC2WOL_LOC_ID_OFFSET + 2401),
        LocationData("Echoes of the Future", "Echoes of the Future: West Obelisk", SC2WOL_LOC_ID_OFFSET + 2402,
                     lambda state: logic_level > 0 or state._sc2wol_has_protoss_common_units(multiworld, player)),
        LocationData("In Utter Darkness", "In Utter Darkness: Defeat", SC2WOL_LOC_ID_OFFSET + 2500),
        LocationData("In Utter Darkness", "In Utter Darkness: Protoss Archive", SC2WOL_LOC_ID_OFFSET + 2501,
                     lambda state: state._sc2wol_has_protoss_medium_units(multiworld, player)),
        LocationData("In Utter Darkness", "In Utter Darkness: Kills", SC2WOL_LOC_ID_OFFSET + 2502,
                     lambda state: state._sc2wol_has_protoss_common_units(multiworld, player)),
        LocationData("Gates of Hell", "Gates of Hell: Victory", SC2WOL_LOC_ID_OFFSET + 2600,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, True) > 6),
        LocationData("Gates of Hell", "Gates of Hell: Large Army", SC2WOL_LOC_ID_OFFSET + 2601,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player) and
                                   state._sc2wol_defense_rating(multiworld, player, True) > 6),
        LocationData("Belly of the Beast", "Belly of the Beast: Victory", SC2WOL_LOC_ID_OFFSET + 2700),
        LocationData("Belly of the Beast", "Belly of the Beast: First Charge", SC2WOL_LOC_ID_OFFSET + 2701),
        LocationData("Belly of the Beast", "Belly of the Beast: Second Charge", SC2WOL_LOC_ID_OFFSET + 2702),
        LocationData("Belly of the Beast", "Belly of the Beast: Third Charge", SC2WOL_LOC_ID_OFFSET + 2703),
        LocationData("Shatter the Sky", "Shatter the Sky: Victory", SC2WOL_LOC_ID_OFFSET + 2800,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Shatter the Sky", "Shatter the Sky: Close Coolant Tower", SC2WOL_LOC_ID_OFFSET + 2801,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Shatter the Sky", "Shatter the Sky: Northwest Coolant Tower", SC2WOL_LOC_ID_OFFSET + 2802,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Shatter the Sky", "Shatter the Sky: Southeast Coolant Tower", SC2WOL_LOC_ID_OFFSET + 2803,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Shatter the Sky", "Shatter the Sky: Southwest Coolant Tower", SC2WOL_LOC_ID_OFFSET + 2804,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("Shatter the Sky", "Shatter the Sky: Leviathan", SC2WOL_LOC_ID_OFFSET + 2805,
                     lambda state: state._sc2wol_has_competent_comp(multiworld, player)),
        LocationData("All-In", "All-In: Victory", None,
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
