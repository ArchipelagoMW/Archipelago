from ..test import WitnessTestBase


class TestIndividualDoors(WitnessTestBase):
    options = {
        "shuffle_doors": "doors",
        "door_groupings": "off",
    }

    def test_swamp_laser_shortcut(self) -> None:
        """
        Test that Door Shuffle grants early access to Swamp Laser from the back shortcut.
        """

        self.assertTrue(self.get_items_by_name("Swamp Laser Shortcut (Door)"))

        self.assertAccessDependency(
            ["Swamp Laser Panel"],
            [
                ["Swamp Laser Shortcut (Door)"],
                ["Swamp Red Underwater Exit (Door)"],
            ],
            only_check_listed=True,
        )
