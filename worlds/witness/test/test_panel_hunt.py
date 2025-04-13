from BaseClasses import CollectionState

from worlds.witness.test import WitnessMultiworldTestBase, WitnessTestBase


class TestMaxPanelHuntMinChecks(WitnessTestBase):
    options = {
        "victory_condition": "panel_hunt",
        "panel_hunt_total": 100,
        "panel_hunt_required_percentage": 100,
        "panel_hunt_postgame": "disable_anything_locked_by_lasers",
        "disable_non_randomized_puzzles": True,
        "shuffle_discarded_panels": False,
        "shuffle_vault_boxes": False,
    }

    def test_correct_panels_were_picked(self) -> None:
        with self.subTest("Check that 100 Hunt Panels were actually picked."):
            self.assertEqual(len(self.multiworld.find_item_locations("+1 Panel Hunt", self.player)), 100)

        with self.subTest("Check that 100 Hunt Panels are enough"):
            state_100 = CollectionState(self.multiworld)
            panel_hunt_item = self.get_item_by_name("+1 Panel Hunt")

            for _ in range(100):
                state_100.collect(panel_hunt_item, True)
            state_100.sweep_for_advancements([self.world.get_location("Tutorial Gate Open Solved")])

            self.assertTrue(self.multiworld.completion_condition[self.player](state_100))

        with self.subTest("Check that 99 Hunt Panels are not enough"):
            state_99 = CollectionState(self.multiworld)
            panel_hunt_item = self.get_item_by_name("+1 Panel Hunt")

            for _ in range(99):
                state_99.collect(panel_hunt_item, True)
            state_99.sweep_for_advancements([self.world.get_location("Tutorial Gate Open Solved")])

            self.assertFalse(self.multiworld.completion_condition[self.player](state_99))


class TestPanelHuntPostgame(WitnessMultiworldTestBase):
    options_per_world = [
        {
            "panel_hunt_postgame": "everything_is_eligible"
        },
        {
            "panel_hunt_postgame": "disable_mountain_lasers_locations"
        },
        {
            "panel_hunt_postgame": "disable_challenge_lasers_locations"
        },
        {
            "panel_hunt_postgame": "disable_anything_locked_by_lasers"
        },
    ]

    common_options = {
        "victory_condition": "panel_hunt",
        "panel_hunt_total": 40,

        # Make sure we can check for Short vs Long Lasers locations by making Mountain Bottom Floor Discard accessible.
        "shuffle_doors": "doors",
        "shuffle_discarded_panels": True,
    }

    def test_panel_hunt_postgame(self) -> None:
        for player_minus_one, options in enumerate(self.options_per_world):
            player = player_minus_one + 1
            postgame_option = options["panel_hunt_postgame"]
            with self.subTest(f'Test that "{postgame_option}" results in 40 Hunt Panels.'):
                self.assertEqual(len(self.multiworld.find_item_locations("+1 Panel Hunt", player)), 40)

        # Test that the box gets extra checks from panel_hunt_postgame

        with self.subTest('Test that "everything_is_eligible" has no Mountaintop Box Hunt Panels.'):
            self.assert_location_does_not_exist("Mountaintop Box Short (Panel Hunt)", 1, strict_check=False)
            self.assert_location_does_not_exist("Mountaintop Box Long (Panel Hunt)", 1, strict_check=False)

        with self.subTest('Test that "disable_mountain_lasers_locations" has a Hunt Panel for Short, but not Long.'):
            self.assert_location_exists("Mountaintop Box Short (Panel Hunt)", 2, strict_check=False)
            self.assert_location_does_not_exist("Mountaintop Box Long (Panel Hunt)", 2, strict_check=False)

        with self.subTest('Test that "disable_challenge_lasers_locations" has a Hunt Panel for Long, but not Short.'):
            self.assert_location_does_not_exist("Mountaintop Box Short (Panel Hunt)", 3, strict_check=False)
            self.assert_location_exists("Mountaintop Box Long (Panel Hunt)", 3, strict_check=False)

        with self.subTest('Test that "disable_anything_locked_by_lasers" has both Mountaintop Box Hunt Panels.'):
            self.assert_location_exists("Mountaintop Box Short (Panel Hunt)", 4, strict_check=False)
            self.assert_location_exists("Mountaintop Box Long (Panel Hunt)", 4, strict_check=False)

        # Check panel_hunt_postgame locations get disabled

        with self.subTest('Test that "everything_is_eligible" does not disable any locked-by-lasers panels.'):
            self.assert_location_exists("Mountain Floor 1 Right Row 5", 1)
            self.assert_location_exists("Mountain Bottom Floor Discard", 1)

        with self.subTest('Test that "disable_mountain_lasers_locations" disables only Shortbox-Locked panels.'):
            self.assert_location_does_not_exist("Mountain Floor 1 Right Row 5", 2)
            self.assert_location_exists("Mountain Bottom Floor Discard", 2)

        with self.subTest('Test that "disable_challenge_lasers_locations" disables only Longbox-Locked panels.'):
            self.assert_location_exists("Mountain Floor 1 Right Row 5", 3)
            self.assert_location_does_not_exist("Mountain Bottom Floor Discard", 3)

        with self.subTest('Test that "everything_is_eligible" disables only Shortbox-Locked panels.'):
            self.assert_location_does_not_exist("Mountain Floor 1 Right Row 5", 4)
            self.assert_location_does_not_exist("Mountain Bottom Floor Discard", 4)
