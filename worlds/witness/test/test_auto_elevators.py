from ..test import WitnessMultiworldTestBase


class TestElevatorsComeToYouBleed(WitnessMultiworldTestBase):
    options_per_world = [
        {
            "elevators_come_to_you": {},
        },
        {
            "elevators_come_to_you": {"Quarry Elevator", "Swamp Long Bridge", "Bunker Elevator"},
        },
        {
            "elevators_come_to_you": {}
        },
    ]

    common_options = {
        "shuffle_symbols": False,
        "shuffle_doors": "panels",
        "shuffle_boat": True,
        "shuffle_EPs": "individual",
        "obelisk_keys": False,
    }

    def test_correct_access_per_player(self) -> None:
        """
        Test that in a multiworld with players that alternate the elevators_come_to_you option,
        the actual behavior alternates as well and doesn't bleed over from slot to slot.
        (This is essentially a "does connection info bleed over" test).
        """

        combinations = [
            ("Quarry Elevator Control (Panel)", "Quarry Boathouse Intro Left"),
            ("Swamp Long Bridge (Panel)", "Swamp Long Bridge Side EP"),
            ("Bunker Elevator Control (Panel)", "Bunker Laser Panel"),
        ]

        for item, location in combinations:
            with self.subTest(f"Test that {item} only locks {location} for player 2"):
                self.assertFalse(self.multiworld.state.can_reach_location(location, 1))
                self.assertFalse(self.multiworld.state.can_reach_location(location, 2))
                self.assertFalse(self.multiworld.state.can_reach_location(location, 3))

                self.collect_by_name(item, 1)
                self.collect_by_name(item, 2)
                self.collect_by_name(item, 3)

                self.assertFalse(self.multiworld.state.can_reach_location(location, 1))
                self.assertTrue(self.multiworld.state.can_reach_location(location, 2))
                self.assertFalse(self.multiworld.state.can_reach_location(location, 3))
