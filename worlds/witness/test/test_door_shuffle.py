from typing import cast

from .. import WitnessWorld
from ..test.bases import WitnessMultiworldTestBase, WitnessTestBase


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
        {
            "early_caves": "add_to_pool",
            "door_groupings": "regional",
        },
    ]

    common_options = {
        "shuffle_doors": "panels",
        "shuffle_postgame": True,
    }

    def test_forbidden_doors(self) -> None:
        with self.subTest("Test that Caves Mountain Shortcut (Panel) exists if Early Caves is off"):
            self.assertTrue(
                self.get_items_by_name("Caves Mountain Shortcut (Panel)", 1),
                "Caves Mountain Shortcut (Panel) should exist in panels shuffle, but it didn't."
            )

        with self.subTest("Test that Caves Mountain Shortcut (Panel) doesn't exist if Early Caves is start_to_pool"):
            self.assertFalse(
                self.get_items_by_name("Caves Mountain Shortcut (Panel)", 2),
                "Caves Mountain Shortcut (Panel) should be removed when Early Caves is enabled, but it still exists."
            )

        with self.subTest("Test that slot data is set up correctly for a panels seed with Early Caves"):
            slot_data = cast(WitnessWorld, self.multiworld.worlds[3])._get_slot_data()

            self.assertIn(
                WitnessWorld.item_name_to_id["Caves Panels"],
                slot_data["door_items_in_the_pool"],
                'Caves Panels should still exist in slot_data under "door_items_in_the_pool".'
            )

            self.assertIn(
                0x021D7,
                slot_data["item_id_to_door_hexes"][WitnessWorld.item_name_to_id["Caves Panels"]],
                "Caves Panels should still contain Caves Mountain Shortcut Panel as a door they unlock.",
            )

            self.assertIn(
                0x021D7,
                slot_data["doors_that_shouldnt_be_locked"],
                "Caves Mountain Shortcut Panel should be marked as \"shouldn't be locked\".",
            )
