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

    def test_eps_exist(self) -> None:
        """
        Test that EP locations exist in shuffle_EPs by checking for the existence of Tutorial First Hallway EP
        """
        self.assert_location_exists("Tutorial First Hallway EP")

    def test_disable_non_randomized_eps(self) -> None:
        """
        Test that disable_non_randomized also disables EPs that are unreachable as a consequence of disabled puzzles.
        One example is Monastery Garden Left EP, which would be unreachable due to Monastery Puzzles being disabled.
        """
        self.assert_location_does_not_exist("Monastery Garden Left EP")

    def test_postgame_eps(self) -> None:
        """
        Test that shuffle_postgame correctly excludes postgame EPs.
        Specifically, we check for Caves Skylight EP, which is in the Caves, which is a postgame location.
        """
        self.assert_location_does_not_exist("Caves Skylight EP")

    def test_ep_difficulty(self) -> None:
        """
        Test that ep_difficulty correctly excludes the EPs it's supposed to.
        Shipwreck Couch EP always exists on tedious, but not on normal, so we test that it doesn't exist.
        """
        self.assert_location_does_not_exist("Shipwreck Couch EP")

    def test_obelisk_keys_work(self) -> None:
        """
        Test that EPs depend on their Obelisk's key by asserting that Desert Sand Snake EP needs the Desert Obelisk Key.
        """

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
