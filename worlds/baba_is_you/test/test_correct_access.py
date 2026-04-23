from .bases import BabaIsYouTestBase

from ..levels import LEVEL_DATA

from BaseClasses import CollectionState

class TestCorrectAccess(BabaIsYouTestBase):
    options = {
        "goal": 0,
        "level_shuffle": 0,
        "open_map": False,
        "start_with_default_words": True,
        "world_keys": False,
        "logic_difficulty": 0,
        #"accessibility": "minimal",
    }

    run_default_tests = False

    # Make sure accessible levels are being calculated correctly
    def test_accessible_regions(self) -> None:
        with self.subTest("Test accessible regions"):
            state = CollectionState(self.multiworld)
            locations = self.multiworld.get_reachable_locations(state, self.player)
            self.assertEqual(len(locations), 12, locations[8])
            state.add_item("And", self.player)
            state.add_item("Sink", self.player)
            state.update_reachable_regions(self.player)
            locations = self.multiworld.get_reachable_locations(state, self.player)
            self.assertEqual(len(locations), 14)
