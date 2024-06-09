from ..test import WitnessTestBase


class TestIndividualDoors(WitnessTestBase):
    options = {
        "shuffle_doors": "doors",
        "door_groupings": "off",
    }

    def test_swamp_laser_shortcut(self):
        self.assertTrue(self.get_items_by_name("Swamp Laser Shortcut (Door)"))

        self.assertAccessDependency(
            ["Swamp Laser Panel"],
            [
                ["Swamp Laser Shortcut (Door)"],
                ["Swamp Entry (Door)"],
                ["Boat"],
            ],
            only_check_listed=True,
        )
