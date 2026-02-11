from BaseClasses import LocationProgressType
from test.bases import *



# class TestGenerationEx(WorldTestBase):
#     game = "The Legend of Zelda - Phantom Hourglass"
#     options = {
#         "keysanity": "in_own_dungeon",
#         "phantom_combat_difficulty": "require_traps",
#         "logic": "hard",
#         "accessibility": "items",
#         "randomize_frogs": "start_with",
#         "dungeons_required": 0,
#         "goal": "metal_hunt",
#         "ghost_ship_in_dungeon_pool": "rescue_tetra",
#         "totok_in_dungeon_pool": False,
#         "randomize_harrow": "no_harrow",
#         "exclude_non_required_dungeons": True,
#         "randomize_masked_beedle": False,
#         "randomize minigames": "no_minigames",
#         "randomize_salvage": "no_salvage",
#         "additional_metal_names": "additional_rare_metal",
#         "zauz_required_metals": 16,
#         "metal_hunt_required": 30,
#         "metal_hunt_total": 30,
#         "ph_time_logic": "easy",
#         "ph_starting_time": 0,
#         "ph_time_increment": 6,
#         "randomize_beedle_membership": "no_beedle_points",
#         "shuffle_dungeon_entrances": True,
#         "shuffle_island_entrances": True,
#
#
#                }

options_metal_bug = {
        "goal_requirements": "defeat_bosses",
        "bellum_access": "spawn_bellumbeck",
        "dungeons_required": 7,
        "require_specific_bosses": False,
        "exclude_non_required_dungeons": False,
        "ghost_ship_in_dungeon_pool": False,
        "totok_in_dungeon_pool": False,

    "keysanity": "in_own_dungeon",
    "randomize_pedestal_items": "vanilla_abstract",
    "randomize_boss_keys": "in_own_dungeon",
    "boss_key_behaviour": "vanilla",
    "pedestal_item_options": "open_per_dungeon",

    "shuffle_dungeon_entrances": "shuffle",
    "shuffle_ports": "simple_mixed_pool",
    "shuffle_caves": "shuffle",
    "shuffle_houses": "shuffle_on_own_island",
    "shuffle_overworld_transitions": "simple_mixed_pool",
    "shuffle_bosses": "no_shuffle",

    "map_warp_options": "ports_open",
    "fog_settings": "no_fog",
    "skip_ocean_fights": True,
    "zauz_required_metals": 1,
    "dungeon_shortcuts": True,

    "randomize_minigames": "no_minigames",
    "randomize_frogs": "vanilla",
    "randomize_fishing": "no_fish",
    "randomize_salvage": "randomize_with_hints",
    "randomize_harrow": "randomize_without_hints",
    "randomize_digs": False,
    "randomize_triforce_crest": True,

    "logic": "hard",
    "phantom_combat_difficulty": "require_stun",
    "boat_requires_sea_chart": False,

    "metal_hunt_required": 20,
    "metal_hunt_total": 27,

    "spirit_gem_packs": 18,
    "additional_spirit_gems": 3,
    "ph_time_logic": "ph_only_b4",
    "ph_required": True,
    "ph_starting_time": 60,
    "ph_heart_time": 45,
    "ph_time_increment": 10,

    "ut_blocked_entrances_behaviour": "mark_on_check",
    "ut_smart_keys": False,
    "ut_events": "no_events",
    "additional_metal_names": "custom",

        }

options_decoupled_bosses= {
    "accessibility": "none",
    #"dungeons_required": 8,
    "shuffle_bosses": "shuffle",
    #"decouple_entrances": "couple_all",
    "entrance_directionality": "disregard_all"
}

options_full_er = {
        "keysanity": "anywhere",
        "phantom_combat_difficulty": "require_traps",
        "logic": "normal",
        "accessibility": "items",
        "randomize_frogs": "randomize",
        "dungeons_required": 3,
        "require_specific_bosses": False,
        "goal": "defeat_bosses",
        "ghost_ship_in_dungeon_pool": "rescue_tetra",
        "totok_in_dungeon_pool": False,
        "randomize_harrow": "no_harrow",
        "exclude_non_required_dungeons": False,
        "randomize_masked_beedle": False,
        "randomize minigames": "randomize_with_hints",
        "randomize_salvage": "randomize_with_hints",
        "additional_metal_names": "additional_rare_metal",
        "zauz_required_metals": 10,
        "metal_hunt_required": 20,
        "metal_hunt_total": 25,
        "ph_time_logic": "beginner",
        "ph_starting_time": 120,
        "ph_time_increment": 60,
        "randomize_beedle_membership": "no_beedle_points",
        # Entrance types
        "shuffle_dungeon_entrances": "shuffle",
        "shuffle_ports": "simple_mixed_pool",
        "shuffle_caves": "no_shuffle",
        "shuffle_houses": "no_shuffle",
        # "shuffle_overworld_transitions": "shuffle_on_own_island",
        "shuffle_bosses": "simple_mixed_pool",
        # entrance options
        "entrance_directionality": "preserve_all",
        "shuffle_between_islands": "shuffle_anywhere",
        "decouple_entrances": 0,

        "ut_smart_keys": True,
               }

options_excluded_crystals = {"dungeons_required": 8,
               "totok_in_dungeon_pool": False,
               "ghost_ship_in_dungeon_pool": False,
               "randomize_pedestal_items": "anywhere",
               "pedestal_item_options": "unique_pedestals",
               "shuffle_bosses": "no_shuffle",
               "randomize_boss_keys": "in_own_dungeon",
               # "shuffle_houses": "shuffle",
               "entrance_directionality": "disregard_all",
               }

class TestPHGeneration(WorldTestBase):
    game = "The Legend of Zelda - Phantom Hourglass"
    options = options_excluded_crystals