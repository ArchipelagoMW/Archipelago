from typing import cast

from BaseClasses import LocationProgressType

from .. import WitnessWorld
from ..test import WitnessMultiworldTestBase


class TestEasterEggShuffle(WitnessMultiworldTestBase):
    options_per_world = [
        {
            "easter_egg_hunt": "off"
        },
        {
            "easter_egg_hunt": "easy"
        },
        {
            "easter_egg_hunt": "normal"
        },
        {
            "easter_egg_hunt": "hard"
        },
        {
            "easter_egg_hunt": "very_hard"
        },
    ]

    def test_easter_egg_hunt(self) -> None:
        with self.subTest("Test that player without Easter Egg Hunt has no easter egg related locations"):
            egg_locations = {location for location in self.multiworld.get_locations(1) if "Egg" in location.name}
            self.assertFalse(egg_locations)

        for player, required_eggs_per_check in zip([2, 3, 4, 5], [2, 3, 4, 5]):
            world = cast(WitnessWorld, self.multiworld.worlds[player])
            option_name = world.options.easter_egg_hunt

            with self.subTest(f"Test that {option_name} Egg Hunt player starts with 0 eggs"):
                self.assertEqual(self.multiworld.state.count("Egg", player), 0)

            with self.subTest(f"Test that the correct Egg Collection locations exist for {option_name} player"):
                first_egg_location = f"{required_eggs_per_check} Easter Eggs Collected"
                one_less_location = f"{required_eggs_per_check - 1} Easter Eggs Collected"
                one_more_location = f"{required_eggs_per_check + 1} Easter Eggs Collected"
                self.assert_location_exists(first_egg_location, player)
                self.assert_location_does_not_exist(one_less_location, player, strict_check=False)
                self.assert_location_does_not_exist(one_more_location, player, strict_check=False)

            with self.subTest('Test that "+4 Easter Eggs" item adds 4 easter eggs'):
                item = world.create_item("+4 Easter Eggs")
                self.multiworld.state.collect(item, prevent_sweep=True)
                self.assertEqual(self.multiworld.state.count("Egg", player), 4)

            with self.subTest(f"Test that 4 Easter Eggs are not enough for {option_name} player's first location"):
                self.assertFalse(self.multiworld.state.can_reach_location(first_egg_location, player))

            with self.subTest(f"Test that 5 Easter Eggs are enough for {option_name} player's first location"):
                item = world.create_item("+1 Easter Egg")
                self.multiworld.state.collect(item, prevent_sweep=True)
                self.assertTrue(self.multiworld.state.can_reach_location(first_egg_location, player))


class TestEggRestrictions(WitnessMultiworldTestBase):
    options_per_world = [{
        "shuffle_postgame": False
    },
    {
        "shuffle_postgame": True
    }]

    common_options = {
        "victory_condition": "mountain_box_short",
        "shuffle_doors": "off",
        "easter_egg_hunt": "hard",
        "shuffle_vault_boxes": True
    }

    def test_egg_restrictions(self) -> None:
        with self.subTest("Test that locations beyond 91 Easter Eggs don't exist for a seed without Mountain"):
            self.assert_location_exists("88 Easter Eggs Collected", 1)
            self.assert_location_does_not_exist("92 Easter Eggs Collected", 1)

        with self.subTest(
            "Test that locations beyond 72 Easter Eggs, which would logically require more than 91 Eggs, are excluded"
        ):
            egg_68_location = self.multiworld.get_location("72 Easter Eggs Collected", 1)
            egg_72_location = self.multiworld.get_location("76 Easter Eggs Collected", 1)

            self.assertNotEqual(egg_68_location.progress_type, LocationProgressType.EXCLUDED)
            self.assertEqual(egg_72_location.progress_type, LocationProgressType.EXCLUDED)

        with self.subTest("Test that in a seed with the whole game included, the 100 egg location exists"):
            self.assert_location_exists("100 Easter Eggs Collected", 2)

        with self.subTest(
            "Test that locations beyond 80 Easter Eggs, which would logically require more than 100 Eggs, are excluded"
        ):
            egg_80_location = self.multiworld.get_location("80 Easter Eggs Collected", 2)
            egg_84_location = self.multiworld.get_location("84 Easter Eggs Collected", 2)

            self.assertNotEqual(egg_80_location.progress_type, LocationProgressType.EXCLUDED)
            self.assertEqual(egg_84_location.progress_type, LocationProgressType.EXCLUDED)
