from ..test import WitnessMultiworldTestBase, WitnessTestBase


class TestElevatorsComeToYou(WitnessTestBase):
    options = {
        "elevators_come_to_you": True,
        "shuffle_doors": "mixed",
        "shuffle_symbols": False,
    }

    def test_bunker_laser(self) -> None:
        self.collect_by_name("Bunker Drop-Down Door Controls (Panel)")

        self.assertFalse(self.multiworld.state.can_reach("Bunker Laser Panel", "Location", self.player))

        self.collect_by_name("Bunker Elevator Control (Panel)")

        self.assertTrue(self.multiworld.state.can_reach("Bunker Laser Panel", "Location", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Bunker UV Room 2", "Location", self.player))

        self.collect_by_name("Bunker Elevator Room Entry (Door)")

        self.assertTrue(self.multiworld.state.can_reach("Bunker UV Room 2", "Location", self.player))


class TestElevatorsComeToYouBleed(WitnessMultiworldTestBase):
    options_per_world = [
        {
            "elevators_come_to_you": False,
        },
        {
            "elevators_come_to_you": True,
        },
        {
            "elevators_come_to_you": False,
        },
    ]

    common_options = {
        "shuffle_symbols": False,
        "shuffle_doors": "panels",
    }

    def test_correct_access_per_player(self) -> None:
        self.assertFalse(self.multiworld.state.can_reach("Bunker Laser Panel", "Location", 1))
        self.assertFalse(self.multiworld.state.can_reach("Bunker Laser Panel", "Location", 2))
        self.assertFalse(self.multiworld.state.can_reach("Bunker Laser Panel", "Location", 3))

        self.collect_by_name(["Bunker Elevator Control (Panel)"], 1)
        self.collect_by_name(["Bunker Elevator Control (Panel)"], 2)
        self.collect_by_name(["Bunker Elevator Control (Panel)"], 3)

        self.assertFalse(self.multiworld.state.can_reach("Bunker Laser Panel", "Location", 1))
        self.assertTrue(self.multiworld.state.can_reach("Bunker Laser Panel", "Location", 2))
        self.assertFalse(self.multiworld.state.can_reach("Bunker Laser Panel", "Location", 3))
