from enum import Flag, auto
from  typing import NamedTuple, Optional
from BaseClasses import Location

class LocationType(Flag):
    MAP_COMPLETION = auto()
    CUTSCENE_COMPLETION = auto()
    STORY_ACHIEVEMENT = auto()
    ITEM = auto()
    ACHIEVEMENT = auto()
    WHEATLY_MONITOR = auto()

class Portal2LocationData(NamedTuple):
    map_name: Optional[str]
    location_type: LocationType
    id_offset: int

class Portal2Location(Location):
    game: str = "Portal 2"

map_complete_table: dict[str, Portal2LocationData] = {
    # Chapter 1
    "Chapter 1: Container Ride Completion": Portal2LocationData("sp_a1_intro1", LocationType.MAP_COMPLETION, 0),
    "Chapter 1: Portal Carousel Completion": Portal2LocationData("sp_a1_intro2", LocationType.MAP_COMPLETION, 1),
    "Chapter 1: Portal Gun Completion": Portal2LocationData("sp_a1_intro3", LocationType.MAP_COMPLETION, 2),
    "Chapter 1: Smooth Jazz Completion": Portal2LocationData("sp_a1_intro4", LocationType.MAP_COMPLETION, 3),
    "Chapter 1: Cube Momentum Completion": Portal2LocationData("sp_a1_intro5", LocationType.MAP_COMPLETION, 4),
    "Chapter 1: Future Starter Completion": Portal2LocationData("sp_a1_intro6", LocationType.MAP_COMPLETION, 5),
    "Chapter 1: Secret Panel Completion": Portal2LocationData("sp_a1_intro7", LocationType.MAP_COMPLETION, 6),
    "Chapter 1: Wake Up Completion": Portal2LocationData("sp_a1_wakeup", LocationType.MAP_COMPLETION, 7),
    # Chapter 2
    "Chapter 2: Incinerator Completion": Portal2LocationData("sp_a2_intro", LocationType.MAP_COMPLETION, 8),
    "Chapter 2: Laser Intro Completion": Portal2LocationData("sp_a2_laser_intro", LocationType.MAP_COMPLETION, 9),
    "Chapter 2: Laser Stairs Completion": Portal2LocationData("sp_a2_laser_stairs", LocationType.MAP_COMPLETION, 10),
    "Chapter 2: Dual Lasers Completion": Portal2LocationData("sp_a2_dual_lasers", LocationType.MAP_COMPLETION, 11),
    "Chapter 2: Laser Over Goo Completion": Portal2LocationData("sp_a2_laser_over_goo", LocationType.MAP_COMPLETION, 12),
    "Chapter 2: Catapult Intro Completion": Portal2LocationData("sp_a2_catapult_intro", LocationType.MAP_COMPLETION, 13),
    "Chapter 2: Trust Fling Completion": Portal2LocationData("sp_a2_trust_fling", LocationType.MAP_COMPLETION, 14),
    "Chapter 2: Pit Flings Completion": Portal2LocationData("sp_a2_pit_flings", LocationType.MAP_COMPLETION, 15),
    "Chapter 2: Fizzler Intro Completion": Portal2LocationData("sp_a2_fizzler_intro", LocationType.MAP_COMPLETION, 16),
    # Chapter 3
    "Chapter 3: Ceiling Catapult Completion": Portal2LocationData("sp_a2_sphere_peek", LocationType.MAP_COMPLETION, 17),
    "Chapter 3: Ricochet Completion": Portal2LocationData("sp_a2_ricochet", LocationType.MAP_COMPLETION, 17),
    "Chapter 3: Bridge Intro Completion": Portal2LocationData("sp_a2_bridge_intro", LocationType.MAP_COMPLETION, 18),
    "Chapter 3: Bridge the Gap Completion": Portal2LocationData("sp_a2_bridge_the_gap", LocationType.MAP_COMPLETION, 19),
    "Chapter 3: Turret Intro Completion": Portal2LocationData("sp_a2_turret_intro", LocationType.MAP_COMPLETION, 20),
    "Chapter 3: Laser Relays Completion": Portal2LocationData("sp_a2_laser_relays", LocationType.MAP_COMPLETION, 21),
    "Chapter 3: Turret Blocker Completion": Portal2LocationData("sp_a2_turret_blocker", LocationType.MAP_COMPLETION, 22),
    "Chapter 3: Laser Vs. Turret Completion": Portal2LocationData("sp_a2_laser_vs_turret", LocationType.MAP_COMPLETION, 23),
    "Chapter 3: Pull The Rug Completion": Portal2LocationData("sp_a2_pull_the_rug", LocationType.MAP_COMPLETION, 24),
    # Chapter 4
    "Chapter 4: Column Blocker Completion": Portal2LocationData("sp_a2_column_blocker", LocationType.MAP_COMPLETION, 25),
    "Chapter 4: Laser Chaining Completion": Portal2LocationData("sp_a2_laser_chaining", LocationType.MAP_COMPLETION, 26),
    "Chapter 4: Triple Laser Completion": Portal2LocationData("sp_a2_triple_laser", LocationType.MAP_COMPLETION, 27),
    "Chapter 4: Jailbreak Completion": Portal2LocationData("sp_a2_bts1", LocationType.MAP_COMPLETION, 28),
    "Chapter 4: Escape Completion": Portal2LocationData("sp_a2_bts2", LocationType.MAP_COMPLETION, 29),
    # Chapter 5
    "Chapter 5: Turret Factory Completion": Portal2LocationData("sp_a2_bts3", LocationType.MAP_COMPLETION, 30),
    "Chapter 5: Turret Sabotage Completion": Portal2LocationData("sp_a2_bts4", LocationType.MAP_COMPLETION, 31),
    "Chapter 5: Neurotoxin Sabotage Completion": Portal2LocationData("sp_a2_bts5", LocationType.MAP_COMPLETION, 32),
    "Chapter 5: Core Completion": Portal2LocationData("sp_a2_core", LocationType.MAP_COMPLETION, 33),
    # Chapter 6
    "Chapter 6: Underground Completion": Portal2LocationData("sp_a3_01", LocationType.MAP_COMPLETION, 34),
    "Chapter 6: Cave Johnson Completion": Portal2LocationData("sp_a3_03", LocationType.MAP_COMPLETION, 35),
    "Chapter 6: Repulsion Intro Completion": Portal2LocationData("sp_a3_jump_intro", LocationType.MAP_COMPLETION, 36),
    "Chapter 6: Bomb Flings Completion": Portal2LocationData("sp_a3_bomb_flings", LocationType.MAP_COMPLETION, 37),
    "Chapter 6: Crazy Box Completion": Portal2LocationData("sp_a3_crazy_box", LocationType.MAP_COMPLETION, 38),
    "Chapter 6: PotatOS Completion": Portal2LocationData("sp_a3_transition01", LocationType.MAP_COMPLETION, 39),
    # Chapter 7
    "Chapter 7: Propulsion Intro Completion": Portal2LocationData("sp_a3_speed_ramp", LocationType.MAP_COMPLETION, 40),
    "Chapter 7: Propulsion Flings Completion": Portal2LocationData("sp_a3_speed_flings", LocationType.MAP_COMPLETION, 41),
    "Chapter 7: Conversion Intro Completion": Portal2LocationData("sp_a3_portal_intro", LocationType.MAP_COMPLETION, 42),
    "Chapter 7: Three Gels Completion": Portal2LocationData("sp_a3_end", LocationType.MAP_COMPLETION, 43),
    # Chapter 8
    "Chapter 8: Test Completion": Portal2LocationData("sp_a4_intro", LocationType.MAP_COMPLETION, 44),
    "Chapter 8: Funnel Intro Completion": Portal2LocationData("sp_a4_tb_intro", LocationType.MAP_COMPLETION, 45),
    "Chapter 8: Ceiling Button Completion": Portal2LocationData("sp_a4_tb_trust_drop", LocationType.MAP_COMPLETION, 46),
    "Chapter 8: Wall Button Completion": Portal2LocationData("sp_a4_tb_wall_button", LocationType.MAP_COMPLETION, 47),
    "Chapter 8: Polarity Completion": Portal2LocationData("sp_a4_tb_polarity", LocationType.MAP_COMPLETION, 48),
    "Chapter 8: Funnel Catch Completion": Portal2LocationData("sp_a4_tb_catch", LocationType.MAP_COMPLETION, 49),
    "Chapter 8: Stop The Box Completion": Portal2LocationData("sp_a4_stop_the_box", LocationType.MAP_COMPLETION, 50),
    "Chapter 8: Laser Catapult Completion": Portal2LocationData("sp_a4_laser_catapult", LocationType.MAP_COMPLETION, 51),
    "Chapter 8: Laser Platform Completion": Portal2LocationData("sp_a4_laser_platform", LocationType.MAP_COMPLETION, 52),
    "Chapter 8: Propulsion Catch Completion": Portal2LocationData("sp_a4_speed_catch", LocationType.MAP_COMPLETION, 53),
    "Chapter 8: Repulsion Polarity Completion": Portal2LocationData("sp_a4_jump_polarity", LocationType.MAP_COMPLETION, 54),
    # Chapter 9
    "Chapter 9: Finale 1 Completion": Portal2LocationData("sp_a4_finale1", LocationType.MAP_COMPLETION, 55),
    "Chapter 9: Finale 2 Completion": Portal2LocationData("sp_a4_finale2", LocationType.MAP_COMPLETION, 56),
    "Chapter 9: Finale 3 Completion": Portal2LocationData("sp_a4_finale3", LocationType.MAP_COMPLETION, 57),
    "Chapter 9: Finale 4 Completion": Portal2LocationData("sp_a4_finale4", LocationType.MAP_COMPLETION, 58),
}

# Optional Checks

cutscene_completion_table: dict[str, Portal2LocationData] = {
    "Chapter 5: Tube Ride Completion": Portal2LocationData("sp_a2_bts6", LocationType.CUTSCENE_COMPLETION, 59),
    "Chapter 6: Unknown Completion": Portal2LocationData("sp_a3_00", LocationType.CUTSCENE_COMPLETION, 60),
}

story_achievements_table: dict[str, Portal2LocationData] = {
    "Achievement: Wake Up Call": Portal2LocationData("sp_a1_intro1", LocationType.STORY_ACHIEVEMENT, 61),
    "Achievement: You Monster": Portal2LocationData("sp_a1_wakeup", LocationType.STORY_ACHIEVEMENT, 62),
    "Achievement: Undiscouraged": Portal2LocationData("sp_a2_laser_intro", LocationType.STORY_ACHIEVEMENT, 63),
    "Achievement: Bridge Over Troubling Water": Portal2LocationData("sp_a2_bridge_intro", LocationType.STORY_ACHIEVEMENT, 64),
    "Achievement: SaBOTour": Portal2LocationData("sp_a2_bts1", LocationType.STORY_ACHIEVEMENT, 65),
    "Achievement: Vertically Unchallenged": Portal2LocationData("sp_a3_jump_intro", LocationType.STORY_ACHIEVEMENT, 66),
    "Achievement: Stranger Than Friction": Portal2LocationData("sp_a3_speed_ramp", LocationType.STORY_ACHIEVEMENT, 67),
    "Achievement: White Out": Portal2LocationData("sp_a3_portal_intro", LocationType.STORY_ACHIEVEMENT, 68),
    "Achievement: Dual Pit Experiment": Portal2LocationData("sp_a4_intro", LocationType.STORY_ACHIEVEMENT, 69),
    "Achievement: Tunnel of Funnel": Portal2LocationData("sp_a4_speed_catch", LocationType.STORY_ACHIEVEMENT, 70),
    "Achievement: The Part Where He Kills You": Portal2LocationData("sp_a4_finale1", LocationType.STORY_ACHIEVEMENT, 71),
    "Achievement: Lunacy": Portal2LocationData("sp_a4_finale4", LocationType.STORY_ACHIEVEMENT, 72),
    "Achievement: Drop Box": Portal2LocationData(None, LocationType.STORY_ACHIEVEMENT, 73),
}

wheatly_monitor_table: dict[str, Portal2LocationData] = {
    "Wheatley Monitor 1": Portal2LocationData("", LocationType.WHEATLY_MONITOR, 74),
    "Wheatley Monitor 2": Portal2LocationData("", LocationType.WHEATLY_MONITOR, 75),
    "Wheatley Monitor 3": Portal2LocationData("", LocationType.WHEATLY_MONITOR, 76),
    "Wheatley Monitor 4": Portal2LocationData("", LocationType.WHEATLY_MONITOR, 77),
    "Wheatley Monitor 5": Portal2LocationData("", LocationType.WHEATLY_MONITOR, 78),
    "Wheatley Monitor 6": Portal2LocationData("", LocationType.WHEATLY_MONITOR, 79),
    "Wheatley Monitor 7": Portal2LocationData("", LocationType.WHEATLY_MONITOR, 80),
    "Wheatley Monitor 8": Portal2LocationData("", LocationType.WHEATLY_MONITOR, 81),
    "Wheatley Monitor 9": Portal2LocationData("", LocationType.WHEATLY_MONITOR, 82),
    "Wheatley Monitor 10": Portal2LocationData("", LocationType.WHEATLY_MONITOR, 83),
    "Wheatley Monitor 11": Portal2LocationData("", LocationType.WHEATLY_MONITOR, 84),
    "Wheatley Monitor 12": Portal2LocationData("", LocationType.WHEATLY_MONITOR, 85),
}

item_location_table: dict[str, Portal2LocationData] = {}

achievements_table: dict[str, Portal2LocationData] = {}

all_locations_table: dict[str, Portal2LocationData] = map_complete_table
all_locations_table.update(cutscene_completion_table)

location_names_to_map_codes: dict[str, str] = {name: value.map_name for
                                               name, value in all_locations_table.items()}
map_codes_to_location_names: dict[str, str] = {value: key for key, value in location_names_to_map_codes.items()}

all_locations_table.update(story_achievements_table)
all_locations_table.update(wheatly_monitor_table)
all_locations_table.update(item_location_table)
all_locations_table.update(achievements_table)

