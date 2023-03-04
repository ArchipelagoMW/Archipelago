import unittest

from BaseClasses import CollectionState
from worlds.AutoWorld import AutoWorldRegister

from . import setup_solo_multiworld


class TestBase(unittest.TestCase):
    gen_steps = ["generate_early", "create_regions", "create_items", "set_rules", "generate_basic", "pre_fill"]

    default_settings_unreachable_regions = {
        "A Link to the Past": {
            "Chris Houlihan Room",  # glitch room by definition
            "Desert Northern Cliffs",  # on top of mountain, only reachable via OWG
            "Dark Death Mountain Bunny Descent Area"  # OWG Mountain descent
        },
        "Ocarina of Time": {
            "Prelude of Light Warp",  # Prelude is not progression by default
            "Serenade of Water Warp",  # Serenade is not progression by default
            "Lost Woods Mushroom Timeout",  # trade quest starts after this item
            "ZD Eyeball Frog Timeout",  # trade quest starts after this item
            "ZR Top of Waterfall",  # dummy region used for entrance shuffle
        },
        # The following SM regions are only used when the corresponding StartLocation option is selected (so not with default settings).
        # Also, those dont have any entrances as they serve as starting Region (that's why they have to be excluded for testAllStateCanReachEverything).
        "Super Metroid": {
            "Ceres",
            "Gauntlet Top",
            "Mama Turtle"
        }
    }

    def testAllStateCanReachEverything(self):
        for game_name, world_type in AutoWorldRegister.world_types.items():
            # Final Fantasy logic is controlled by finalfantasyrandomizer.com
            if game_name not in {"Ori and the Blind Forest"}:  # TODO: fix Ori Logic
                unreachable_regions = self.default_settings_unreachable_regions.get(game_name, set())
                with self.subTest("Game", game=game_name):
                    world = setup_solo_multiworld(world_type)
                    excluded = world.exclude_locations[1].value
                    state = world.get_all_state(False)
                    for location in world.get_locations():
                        if location.name not in excluded:
                            with self.subTest("Location should be reached", location=location):
                                self.assertTrue(location.can_reach(state), f"{location.name} unreachable")

                    for region in world.get_regions():
                        if region.name not in unreachable_regions:
                            with self.subTest("Region should be reached", region=region):
                                self.assertTrue(region.can_reach(state))

                    with self.subTest("Completion Condition"):
                        self.assertTrue(world.can_beat_game(state))

    def testEmptyStateCanReachSomething(self):
        for game_name, world_type in AutoWorldRegister.world_types.items():
            # Final Fantasy logic is controlled by finalfantasyrandomizer.com
            if game_name not in {"Archipelago", "Sudoku"}:
                with self.subTest("Game", game=game_name):
                    world = setup_solo_multiworld(world_type)
                    state = CollectionState(world)
                    locations = set()
                    for location in world.get_locations():
                        if location.can_reach(state):
                            locations.add(location)
                    self.assertGreater(len(locations), 0,
                                       msg="Need to be able to reach at least one location to get started.")
