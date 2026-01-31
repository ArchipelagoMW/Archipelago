from enum import Flag, auto
from BaseClasses import Location
from .ItemNames import *

portal_2_base_id = 98275000
offset_index = 0

class LocationType(Flag):
    MAP_COMPLETION = auto()
    CUTSCENE_COMPLETION = auto()
    STORY_ACHIEVEMENT = auto()
    ITEM = auto()
    ACHIEVEMENT = auto()
    WHEATLY_MONITOR = auto()
    OTHER = auto()

class Portal2LocationData:
    def __init__(self, map_name: str = None, location_type: LocationType = None, required_items: list[str] = []):
        self.map_name = map_name
        self.location_type = location_type

        self.required_items = required_items

        global portal_2_base_id, offset_index
        self.id = portal_2_base_id + offset_index
        offset_index += 1

class Portal2Location(Location):
    game: str = "Portal 2"

map_complete_table: dict[str, Portal2LocationData] = {
    # Chapter 1
    "Chapter 1: Container Ride Completion": Portal2LocationData("sp_a1_intro1", LocationType.MAP_COMPLETION, [weighted_cube, floor_button]),
    "Chapter 1: Portal Carousel Completion": Portal2LocationData("sp_a1_intro2", LocationType.MAP_COMPLETION, [button, weighted_cube, floor_button]),
    "Chapter 1: Portal Gun Completion": Portal2LocationData("sp_a1_intro3", LocationType.MAP_COMPLETION),
    "Chapter 1: Smooth Jazz Completion": Portal2LocationData("sp_a1_intro4", LocationType.MAP_COMPLETION, [weighted_cube, floor_button]),
    "Chapter 1: Cube Momentum Completion": Portal2LocationData("sp_a1_intro5", LocationType.MAP_COMPLETION, [button, weighted_cube, floor_button]),
    "Chapter 1: Future Starter Completion": Portal2LocationData("sp_a1_intro6", LocationType.MAP_COMPLETION, [weighted_cube, floor_button]),
    "Chapter 1: Secret Panel Completion": Portal2LocationData("sp_a1_intro7", LocationType.MAP_COMPLETION),
    "Chapter 1: Wake Up Completion": Portal2LocationData("sp_a1_wakeup", LocationType.MAP_COMPLETION),
    "Chapter 1: Incinerator Completion": Portal2LocationData("sp_a2_intro", LocationType.MAP_COMPLETION, [portal_gun_2]),
    # Chapter 2
    "Chapter 2: Laser Intro Completion": Portal2LocationData("sp_a2_laser_intro", LocationType.MAP_COMPLETION, [portal_gun_2, laser, laser_catcher]),
    "Chapter 2: Laser Stairs Completion": Portal2LocationData("sp_a2_laser_stairs", LocationType.MAP_COMPLETION, [portal_gun_2, reflection_cube, floor_button, laser, laser_catcher]),
    "Chapter 2: Dual Lasers Completion": Portal2LocationData("sp_a2_dual_lasers", LocationType.MAP_COMPLETION, [portal_gun_2, reflection_cube, laser, laser_catcher]),
    "Chapter 2: Laser Over Goo Completion": Portal2LocationData("sp_a2_laser_over_goo", LocationType.MAP_COMPLETION, [button, floor_button, weighted_cube,  portal_gun_2, laser, laser_catcher]),
    "Chapter 2: Catapult Intro Completion": Portal2LocationData("sp_a2_catapult_intro", LocationType.MAP_COMPLETION, [faith_plate, button, weighted_cube, floor_button]),
    "Chapter 2: Trust Fling Completion": Portal2LocationData("sp_a2_trust_fling", LocationType.MAP_COMPLETION, [portal_gun_2, faith_plate, button, weighted_cube, floor_button]),
    "Chapter 2: Pit Flings Completion": Portal2LocationData("sp_a2_pit_flings", LocationType.MAP_COMPLETION, [portal_gun_2, weighted_cube, laser, laser_catcher, floor_button]),
    "Chapter 2: Fizzler Intro Completion": Portal2LocationData("sp_a2_fizzler_intro", LocationType.MAP_COMPLETION, [portal_gun_2, laser, reflection_cube, laser_catcher, button]),
    # Chapter 3
    "Chapter 3: Ceiling Catapult Completion": Portal2LocationData("sp_a2_sphere_peek", LocationType.MAP_COMPLETION, [portal_gun_2, faith_plate, button, reflection_cube, laser, laser_catcher]),
    "Chapter 3: Ricochet Completion": Portal2LocationData("sp_a2_ricochet", LocationType.MAP_COMPLETION, [portal_gun_2, faith_plate, weighted_cube, laser, laser_catcher, reflection_cube, floor_button, button]),
    "Chapter 3: Bridge Intro Completion": Portal2LocationData("sp_a2_bridge_intro", LocationType.MAP_COMPLETION, [portal_gun_2, bridge, floor_button, button, weighted_cube]),
    "Chapter 3: Bridge the Gap Completion": Portal2LocationData("sp_a2_bridge_the_gap", LocationType.MAP_COMPLETION, [portal_gun_2, bridge, floor_button, button, weighted_cube]),
    "Chapter 3: Turret Intro Completion": Portal2LocationData("sp_a2_turret_intro", LocationType.MAP_COMPLETION, [portal_gun_2, weighted_cube, floor_button, turrets]),
    "Chapter 3: Laser Relays Completion": Portal2LocationData("sp_a2_laser_relays", LocationType.MAP_COMPLETION, [portal_gun_2, laser, reflection_cube, laser_relays]),
    "Chapter 3: Turret Blocker Completion": Portal2LocationData("sp_a2_turret_blocker", LocationType.MAP_COMPLETION, [portal_gun_2, bridge, faith_plate, floor_button, weighted_cube]),
    "Chapter 3: Laser Vs. Turret Completion": Portal2LocationData("sp_a2_laser_vs_turret", LocationType.MAP_COMPLETION, [portal_gun_2, laser, laser_catcher, weighted_cube, reflection_cube, floor_button]),
    "Chapter 3: Pull The Rug Completion": Portal2LocationData("sp_a2_pull_the_rug", LocationType.MAP_COMPLETION, [portal_gun_2, bridge, weighted_cube, floor_button, laser, laser_catcher]),
    # Chapter 4
    "Chapter 4: Column Blocker Completion": Portal2LocationData("sp_a2_column_blocker", LocationType.MAP_COMPLETION, [portal_gun_2, bridge, laser, laser_catcher, laser_relays, button, reflection_cube, faith_plate]),
    "Chapter 4: Laser Chaining Completion": Portal2LocationData("sp_a2_laser_chaining", LocationType.MAP_COMPLETION, [portal_gun_2, laser, laser_catcher, laser_relays, reflection_cube, faith_plate]),
    "Chapter 4: Triple Laser Completion": Portal2LocationData("sp_a2_triple_laser", LocationType.MAP_COMPLETION, [portal_gun_2, laser, laser_catcher, reflection_cube]),
    "Chapter 4: Jailbreak Completion": Portal2LocationData("sp_a2_bts1", LocationType.MAP_COMPLETION, [portal_gun_2, bridge, button, weighted_cube]),
    "Chapter 4: Escape Completion": Portal2LocationData("sp_a2_bts2", LocationType.MAP_COMPLETION, [portal_gun_2, turrets]),
    # Chapter 5
    "Chapter 5: Turret Factory Completion": Portal2LocationData("sp_a2_bts3", LocationType.MAP_COMPLETION, [portal_gun_2]),
    "Chapter 5: Turret Sabotage Completion": Portal2LocationData("sp_a2_bts4", LocationType.MAP_COMPLETION, [portal_gun_2, turrets]),
    "Chapter 5: Neurotoxin Sabotage Completion": Portal2LocationData("sp_a2_bts5", LocationType.MAP_COMPLETION, [portal_gun_2, laser]),
    "Chapter 5: Core Completion": Portal2LocationData("sp_a2_core", LocationType.MAP_COMPLETION, [portal_gun_2, button]),
    # Chapter 6
    "Chapter 6: Underground Completion": Portal2LocationData("sp_a3_01", LocationType.MAP_COMPLETION, [portal_gun_2]),
    "Chapter 6: Cave Johnson Completion": Portal2LocationData("sp_a3_03", LocationType.MAP_COMPLETION, [portal_gun_2]),
    "Chapter 6: Repulsion Intro Completion": Portal2LocationData("sp_a3_jump_intro", LocationType.MAP_COMPLETION, [portal_gun_2, paint, old_button, old_floor_button, antique_cube]),
    "Chapter 6: Bomb Flings Completion": Portal2LocationData("sp_a3_bomb_flings", LocationType.MAP_COMPLETION, [portal_gun_2, old_button, paint]),
    "Chapter 6: Crazy Box Completion": Portal2LocationData("sp_a3_crazy_box", LocationType.MAP_COMPLETION, [portal_gun_2, old_button, paint, antique_cube, old_floor_button]),
    "Chapter 6: PotatOS Completion": Portal2LocationData("sp_a3_transition01", LocationType.MAP_COMPLETION, [portal_gun_2, potatos]),
    # Chapter 7
    "Chapter 7: Propulsion Intro Completion": Portal2LocationData("sp_a3_speed_ramp", LocationType.MAP_COMPLETION, [portal_gun_2, paint, antique_cube, old_floor_button, old_button]),
    "Chapter 7: Propulsion Flings Completion": Portal2LocationData("sp_a3_speed_flings", LocationType.MAP_COMPLETION, [portal_gun_2, paint, antique_cube, old_floor_button]),
    "Chapter 7: Conversion Intro Completion": Portal2LocationData("sp_a3_portal_intro", LocationType.MAP_COMPLETION, [portal_gun_2, paint]),
    "Chapter 7: Three Gels Completion": Portal2LocationData("sp_a3_end", LocationType.MAP_COMPLETION, [portal_gun_2, paint]),
    # Chapter 8
    "Chapter 8: Test Completion": Portal2LocationData("sp_a4_intro", LocationType.MAP_COMPLETION, [portal_gun_2, frankenturret, floor_button, button]),
    "Chapter 8: Funnel Intro Completion": Portal2LocationData("sp_a4_tb_intro", LocationType.MAP_COMPLETION, [portal_gun_2, funnel, frankenturret, floor_button]),
    "Chapter 8: Ceiling Button Completion": Portal2LocationData("sp_a4_tb_trust_drop", LocationType.MAP_COMPLETION, [portal_gun_2, funnel, frankenturret, floor_button, button]),
    "Chapter 8: Wall Button Completion": Portal2LocationData("sp_a4_tb_wall_button", LocationType.MAP_COMPLETION, [portal_gun_2, funnel, frankenturret, floor_button, button, faith_plate]),
    "Chapter 8: Polarity Completion": Portal2LocationData("sp_a4_tb_polarity", LocationType.MAP_COMPLETION, [portal_gun_2, funnel, frankenturret, floor_button]),
    "Chapter 8: Funnel Catch Completion": Portal2LocationData("sp_a4_tb_catch", LocationType.MAP_COMPLETION, [portal_gun_2, funnel, frankenturret, floor_button, button, faith_plate]),
    "Chapter 8: Stop The Box Completion": Portal2LocationData("sp_a4_stop_the_box", LocationType.MAP_COMPLETION, [portal_gun_2, frankenturret, floor_button, button, faith_plate, bridge]),
    "Chapter 8: Laser Catapult Completion": Portal2LocationData("sp_a4_laser_catapult", LocationType.MAP_COMPLETION, [portal_gun_2, frankenturret, floor_button, faith_plate, reflection_cube, laser, laser_catcher, funnel]),
    "Chapter 8: Laser Platform Completion": Portal2LocationData("sp_a4_laser_platform", LocationType.MAP_COMPLETION, [portal_gun_2, button, reflection_cube, laser, laser_catcher, funnel]),
    "Chapter 8: Propulsion Catch Completion": Portal2LocationData("sp_a4_speed_tb_catch", LocationType.MAP_COMPLETION, [portal_gun_2, floor_button, funnel, button, frankenturret, paint]),
    "Chapter 8: Repulsion Polarity Completion": Portal2LocationData("sp_a4_jump_polarity", LocationType.MAP_COMPLETION, [portal_gun_2, paint, funnel, floor_button, button]),
    # Chapter 9
    "Chapter 9: Finale 1 Completion": Portal2LocationData("sp_a4_finale1", LocationType.MAP_COMPLETION, [portal_gun_2, faith_plate, funnel, paint]),
    "Chapter 9: Finale 2 Completion": Portal2LocationData("sp_a4_finale2", LocationType.MAP_COMPLETION, [portal_gun_2, funnel, paint, floor_button, turrets]),
    "Chapter 9: Finale 3 Completion": Portal2LocationData("sp_a4_finale3", LocationType.MAP_COMPLETION, [portal_gun_2, paint, funnel]),
    "Chapter 9: Finale 4 Completion": Portal2LocationData("sp_a4_finale4", LocationType.MAP_COMPLETION, [portal_gun_2, potatos, paint, adventure_core, space_core, fact_core]),
}

# Optional Checks

cutscene_completion_table: dict[str, Portal2LocationData] = {
    "Chapter 5: Tube Ride Completion": Portal2LocationData("sp_a2_bts6", LocationType.CUTSCENE_COMPLETION),
    "Chapter 6: Long Fall Completion": Portal2LocationData("sp_a3_00", LocationType.CUTSCENE_COMPLETION),
}


# Not implemented
story_achievements_table: dict[str, Portal2LocationData] = {
    "Achievement: Wake Up Call": Portal2LocationData("sp_a1_intro1", LocationType.STORY_ACHIEVEMENT),
    "Achievement: You Monster": Portal2LocationData("sp_a1_wakeup", LocationType.STORY_ACHIEVEMENT),
    "Achievement: Undiscouraged": Portal2LocationData("sp_a2_laser_intro", LocationType.STORY_ACHIEVEMENT),
    "Achievement: Bridge Over Troubling Water": Portal2LocationData("sp_a2_bridge_intro", LocationType.STORY_ACHIEVEMENT),
    "Achievement: SaBOTour": Portal2LocationData("sp_a2_bts1", LocationType.STORY_ACHIEVEMENT),
    "Achievement: Vertically Unchallenged": Portal2LocationData("sp_a3_jump_intro", LocationType.STORY_ACHIEVEMENT),
    "Achievement: Stranger Than Friction": Portal2LocationData("sp_a3_speed_ramp", LocationType.STORY_ACHIEVEMENT),
    "Achievement: White Out": Portal2LocationData("sp_a3_portal_intro", LocationType.STORY_ACHIEVEMENT),
    "Achievement: Dual Pit Experiment": Portal2LocationData("sp_a4_intro", LocationType.STORY_ACHIEVEMENT),
    "Achievement: Tunnel of Funnel": Portal2LocationData("sp_a4_speed_catch", LocationType.STORY_ACHIEVEMENT),
    "Achievement: The Part Where He Kills You": Portal2LocationData("sp_a4_finale1", LocationType.STORY_ACHIEVEMENT),
    "Achievement: Lunacy": Portal2LocationData("sp_a4_finale4", LocationType.STORY_ACHIEVEMENT),
    "Achievement: Drop Box": Portal2LocationData(None, LocationType.STORY_ACHIEVEMENT),
}

# Not implementd
achievements_table: dict[str, Portal2LocationData] = {}

wheatley_monitor_table: dict[str, Portal2LocationData] = {
    "Wheatley Monitor 1": Portal2LocationData("sp_a4_tb_intro", LocationType.WHEATLY_MONITOR, [portal_gun_2, funnel, frankenturret]),
    "Wheatley Monitor 2": Portal2LocationData("sp_a4_tb_trust_drop", LocationType.WHEATLY_MONITOR, [portal_gun_2, button, funnel, frankenturret]),
    "Wheatley Monitor 3": Portal2LocationData("sp_a4_tb_wall_button", LocationType.WHEATLY_MONITOR, [portal_gun_2]),
    "Wheatley Monitor 4": Portal2LocationData("sp_a4_tb_polarity", LocationType.WHEATLY_MONITOR, [turrets]),
    "Wheatley Monitor 5": Portal2LocationData("sp_a4_tb_catch", LocationType.WHEATLY_MONITOR, [portal_gun_2, frankenturret, funnel, faith_plate, button]), #monitor1
    "Wheatley Monitor 6": Portal2LocationData("sp_a4_tb_catch", LocationType.WHEATLY_MONITOR, [portal_gun_2, frankenturret, funnel, faith_plate, button]), #monitor2
    "Wheatley Monitor 7": Portal2LocationData("sp_a4_stop_the_box", LocationType.WHEATLY_MONITOR, [faith_plate]),
    "Wheatley Monitor 8": Portal2LocationData("sp_a4_laser_catapult", LocationType.WHEATLY_MONITOR, [portal_gun_2, frankenturret, faith_plate, funnel, reflection_cube, laser, laser_catcher]),
    "Wheatley Monitor 9": Portal2LocationData("sp_a4_laser_platform", LocationType.WHEATLY_MONITOR, [portal_gun_2, laser, laser_catcher, reflection_cube, button]),
    "Wheatley Monitor 10": Portal2LocationData("sp_a4_speed_tb_catch", LocationType.WHEATLY_MONITOR, [portal_gun_2]),
    "Wheatley Monitor 11": Portal2LocationData("sp_a4_jump_polarity", LocationType.WHEATLY_MONITOR, [portal_gun_2, paint, funnel, turrets, floor_button, button]),
    "Wheatley Monitor 12": Portal2LocationData("sp_a4_finale3", LocationType.WHEATLY_MONITOR, [portal_gun_2, paint]),
}

wheatley_maps_to_monitor_names: dict[str, list[str]] = {}
for key, value in wheatley_monitor_table.items():
    map_name = value.map_name
    if map_name not in wheatley_maps_to_monitor_names:
        wheatley_maps_to_monitor_names[map_name] = [key]
    else:
        wheatley_maps_to_monitor_names[map_name].append(key)

item_location_table: dict[str, Portal2LocationData] = {
    portal_gun_1: Portal2LocationData("sp_a1_intro3", LocationType.ITEM),
    portal_gun_2: Portal2LocationData("sp_a2_intro", LocationType.ITEM),
    potatos: Portal2LocationData("sp_a3_transition01", LocationType.ITEM, [portal_gun_2]),
}

item_maps_to_item_location : dict[str, str] = {value.map_name:key for key, value in item_location_table.items()}

ratman_den_locations_table: dict[str, Portal2LocationData] = {
    "Ratman Den 1": Portal2LocationData("sp_a1_intro4", LocationType.OTHER, [weighted_cube, floor_button]),
    "Ratman Den 2": Portal2LocationData("sp_a2_dual_lasers", LocationType.OTHER),
    "Ratman Den 3": Portal2LocationData("sp_a2_trust_fling", LocationType.OTHER, [portal_gun_2, faith_plate]),
    "Ratman Den 4": Portal2LocationData("sp_a2_bridge_intro", LocationType.OTHER),
    "Ratman Den 5": Portal2LocationData("sp_a2_bridge_the_gap", LocationType.OTHER, [portal_gun_2]),
    "Ratman Den 6": Portal2LocationData("sp_a2_laser_vs_turret", LocationType.OTHER, [portal_gun_2, laser, floor_button, reflection_cube]),
    "Ratman Den 7": Portal2LocationData("sp_a2_pull_the_rug", LocationType.OTHER, [portal_gun_2, bridge])
}

ratman_map_to_ratman_den: dict[str, str] = {value.map_name: key for key, value in ratman_den_locations_table.items()}

all_locations_table: dict[str, Portal2LocationData] = map_complete_table.copy()
all_locations_table.update(cutscene_completion_table)

location_names_to_map_codes: dict[str, str] = {name: value.map_name for
                                               name, value in all_locations_table.items()}
map_codes_to_location_names: dict[str, str] = {value: key for key, value in location_names_to_map_codes.items()}

# all_locations_table.update(story_achievements_table)
all_locations_table.update(wheatley_monitor_table)
all_locations_table.update(item_location_table)
all_locations_table.update(ratman_den_locations_table)
# all_locations_table.update(achievements_table)

