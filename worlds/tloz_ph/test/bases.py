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

class DefaultSettings(WorldTestBase):
    game = "The Legend of Zelda - Phantom Hourglass"
    options = {
        "logic": "normal",
        "keysanity": "in_own_dungeon",
        "randomize_pedestal_items": "in_own_dungeon",
        "pedestal_item_options": "unique_pedestals",
        "time_logic": "no_logic",
        # "add_items_to_pool": {"Grappling Hook": 1, "Boomerang": 1, "Shovel": 1, "Hammer": 1},
        # "remove_items_from_pool": {"Red Rupee (20)": 5},
        # "plando_transitions": [{"entrance": "Mercay SW Oshus' House", "exit": "Apricot's Exit"},
        #                        ]
    }

# class TestGeneration(WorldTestBase):
#     game = "The Legend of Zelda - Phantom Hourglass"
#     options = {
#         "keysanity": "anywhere",
#         "phantom_combat_difficulty": "require_traps",
#         "logic": "normal",
#         "accessibility": "items",
#         "randomize_frogs": "randomize",
#         "dungeons_required": 3,
#         "require_specific_bosses": False,
#         "goal": "defeat_bosses",
#         "ghost_ship_in_dungeon_pool": "rescue_tetra",
#         "totok_in_dungeon_pool": False,
#         "randomize_harrow": "no_harrow",
#         "exclude_non_required_dungeons": False,
#         "randomize_masked_beedle": False,
#         "randomize minigames": "randomize_with_hints",
#         "randomize_salvage": "randomize_with_hints",
#         "additional_metal_names": "additional_rare_metal",
#         "zauz_required_metals": 10,
#         "metal_hunt_required": 20,
#         "metal_hunt_total": 25,
#         "ph_time_logic": "beginner",
#         "ph_starting_time": 120,
#         "ph_time_increment": 60,
#         "randomize_beedle_membership": "no_beedle_points",
#         # Entrance types
#         "shuffle_dungeon_entrances": "simple_mixed_pool",
#         "shuffle_ports": "shuffle",
#         "shuffle_caves": "shuffle",
#         "shuffle_houses": "shuffle",
#         "shuffle_overworld_transitions": "shuffle",
#         "shuffle_bosses": "simple_mixed_pool",
#         # entrance options
#         "entrance_directionality": "preserve_all",
#         "shuffle_between_islands": "shuffle_anywhere",
#         "decouple_entrances": "couple_all",
#                }