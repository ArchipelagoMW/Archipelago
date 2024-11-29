from ..test import WitnessMultiworldTestBase, WitnessTestBase


class TestElevatorsComeToYou(WitnessTestBase):
    options = {
        "elevators_come_to_you": True,
        "shuffle_doors": "mixed",
        "shuffle_symbols": False,
    }

    def test_bunker_laser(self) -> None:
        """
        In elevators_come_to_you, Bunker can be entered from the back.
        This means that you can access the laser with just Bunker Elevator Control (Panel).
        It also means that you can, for example, access UV Room with the Control and the Elevator Room Entry Door.
        """

        self.assertFalse(self.multiworld.state.can_reach("Bunker Laser Panel", "Location", self.player))

        self.collect_by_name("Bunker Elevator Control (Panel)")

        self.assertTrue(self.multiworld.state.can_reach("Bunker Laser Panel", "Location", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Bunker UV Room 2", "Location", self.player))

        self.collect_by_name("Bunker Elevator Room Entry (Door)")
        self.collect_by_name("Bunker Drop-Down Door Controls (Panel)")

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
        """
        Test that in a multiworld with players that alternate the elevators_come_to_you option,
        the actual behavior alternates as well and doesn't bleed over from slot to slot.
        (This is essentially a "does connection info bleed over" test).
        """

        self.assertFalse(self.multiworld.state.can_reach("Bunker Laser Panel", "Location", 1))
        self.assertFalse(self.multiworld.state.can_reach("Bunker Laser Panel", "Location", 2))
        self.assertFalse(self.multiworld.state.can_reach("Bunker Laser Panel", "Location", 3))

        self.collect_by_name(["Bunker Elevator Control (Panel)"], 1)
        self.collect_by_name(["Bunker Elevator Control (Panel)"], 2)
        self.collect_by_name(["Bunker Elevator Control (Panel)"], 3)

        self.assertFalse(self.multiworld.state.can_reach("Bunker Laser Panel", "Location", 1))
        self.assertTrue(self.multiworld.state.can_reach("Bunker Laser Panel", "Location", 2))
        self.assertFalse(self.multiworld.state.can_reach("Bunker Laser Panel", "Location", 3))
