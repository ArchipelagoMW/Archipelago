from ..test import WitnessTestBase


class TestIndividualEPs(WitnessTestBase):
    options = {
        "shuffle_EPs": "individual",
        "EP_difficulty": "normal",
        "obelisk_keys": True,
        "disable_non_randomized_puzzles": True,
        "shuffle_postgame": False,
        "victory_condition": "mountain_box_short",
        "early_caves": "off",
    }

    def test_correct_eps_exist_and_are_locked(self) -> None:
        """
        Test that EP locations exist in shuffle_EPs, but only the ones that actually should (based on options)
        """

        # Test Tutorial First Hallways EP as a proxy for "EPs exist at all"
        # Don't wrap in a subtest - If this fails, there is no point.
        self.assert_location_exists("Tutorial First Hallway EP")

        with self.subTest("Test that disable_non_randomized disables Monastery Garden Left EP"):
            self.assert_location_does_not_exist("Monastery Garden Left EP")

        with self.subTest("Test that shuffle_postgame being off disables postgame EPs."):
            self.assert_location_does_not_exist("Caves Skylight EP")

        with self.subTest("Test that ep_difficulty being set to normal excludes tedious EPs."):
            self.assert_location_does_not_exist("Shipwreck Couch EP")

        with self.subTest("Test that EPs are being locked by Obelisk Keys."):
            self.assertAccessDependency(["Desert Sand Snake EP"], [["Desert Obelisk Key"]], True)


class TestObeliskSides(WitnessTestBase):
    options = {
        "shuffle_EPs": "obelisk_sides",
        "EP_difficulty": "eclipse",
        "shuffle_vault_boxes": True,
        "shuffle_postgame": True,
    }

    def test_eclipse_required_for_town_side_6(self) -> None:
        """
        Test that Obelisk Sides require the appropriate event items from the individual EPs.
        Specifically, assert that Town Obelisk Side 6 needs Theater Eclipse EP.
        This doubles as a test for Theater Eclipse EP existing with the right options.
        """

        self.assert_dependency_on_event_item(
            self.world.get_location("Town Obelisk Side 6"), "Town Obelisk Side 6 - Theater Eclipse EP"
        )
