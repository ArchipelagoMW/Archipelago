from ..test import WitnessMultiworldTestBase, WitnessTestBase


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


class TestForbiddenDoors(WitnessMultiworldTestBase):
    options_per_world = [
        {
            "early_caves": "off",
        },
        {
            "early_caves": "add_to_pool",
        },
    ]

    common_options = {
        "shuffle_doors": "panels",
        "shuffle_postgame": True,
    }

    def test_forbidden_doors(self) -> None:
        self.assertTrue(
            self.get_items_by_name("Caves Mountain Shortcut (Panel)", 1),
            "Caves Mountain Shortcut (Panel) should exist in panels shuffle, but it didn't."
        )
        self.assertFalse(
            self.get_items_by_name("Caves Mountain Shortcut (Panel)", 2),
            "Caves Mountain Shortcut (Panel) should be removed when Early Caves is enabled, but it still exists."
        )
