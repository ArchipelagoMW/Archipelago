from typing import cast

from BaseClasses import LocationProgressType

from .. import WitnessWorld
from ..test.bases import WitnessMultiworldTestBase


class TestEasterEggShuffle(WitnessMultiworldTestBase):
    options_per_world = [
        {
            "easter_egg_hunt": "off",
        },
        {
            "easter_egg_hunt": "easy",
        },
        {
            "easter_egg_hunt": "normal",
        },
        {
            "easter_egg_hunt": "hard",
        },
        {
            "easter_egg_hunt": "very_hard",
        },
        {
            "easter_egg_hunt": "extreme",
        },
    ]

    def test_easter_egg_hunt(self) -> None:
        with self.subTest("Test that player without Easter Egg Hunt has no easter egg related locations"):
            egg_locations = {location for location in self.multiworld.get_locations(1) if "Egg" in location.name}
            self.assertFalse(egg_locations)

        for player, eggs_per_check, logical_eggs_per_check in zip([2, 3, 4, 5, 6], [3, 3, 4, 4, 4], [8, 6, 6, 5, 4]):
            world = cast(WitnessWorld, self.multiworld.worlds[player])
            option_name = world.options.easter_egg_hunt

            with self.subTest(f"Test that {option_name} Egg Hunt player starts with 0 eggs"):
                self.assertEqual(self.multiworld.state.count("Egg", player), 0)

            with self.subTest(f"Test that the correct Egg Collection locations exist for {option_name} player"):
                first_egg_location = f"{eggs_per_check} Easter Eggs Collected"
                one_less_location = f"{eggs_per_check - 1} Easter Eggs Collected"
                one_more_location = f"{eggs_per_check + 1} Easter Eggs Collected"
                self.assert_location_exists(first_egg_location, player)
                self.assert_location_does_not_exist(one_less_location, player, strict_check=False)
                self.assert_location_does_not_exist(one_more_location, player, strict_check=False)

            one_too_few = logical_eggs_per_check - 1
            with self.subTest(f'Test that "+{one_too_few} Easter Eggs" item adds 4 easter eggs'):
                item = world.create_item(f"+{one_too_few} Easter Eggs")
                self.multiworld.state.collect(item, prevent_sweep=True)
                self.assertEqual(self.multiworld.state.count("Egg", player), one_too_few)

            with self.subTest(
                f"Test that {one_too_few} Easter Eggs are not enough for {option_name} player's first location"
            ):
                self.assertFalse(self.multiworld.state.can_reach_location(first_egg_location, player))

            with self.subTest(
                f"Test that {logical_eggs_per_check} Easter Eggs are enough for {option_name} player's first location"
            ):
                item = world.create_item("+1 Easter Egg")
                self.multiworld.state.collect(item, prevent_sweep=True)
                self.assertTrue(self.multiworld.state.can_reach_location(first_egg_location, player))


class TestEggRestrictions(WitnessMultiworldTestBase):
    options_per_world = [
        {
            "shuffle_postgame": False,
        },
        {
            "shuffle_postgame": True,
        },
        {
            "shuffle_postgame": True,
            "exclude_locations": frozenset({"Bunker Easter Egg 3"}),
        }
    ]

    common_options = {
        "victory_condition": "mountain_box_short",
        "shuffle_doors": "off",
        "easter_egg_hunt": "very_hard",
        "shuffle_vault_boxes": True,
    }

    def test_egg_restrictions(self) -> None:
        with self.subTest("Test that locations beyond 108 Easter Eggs don't exist for a seed without Mountain"):
            self.assert_location_exists("108 Easter Eggs Collected", 1)
            self.assert_location_does_not_exist("112 Easter Eggs Collected", 1)

        with self.subTest(
            "Test that locations beyond 86 Easter Eggs, which would logically require more than 108 Eggs, are excluded"
        ):
            egg_84_location = self.multiworld.get_location("84 Easter Eggs Collected", 1)
            egg_88_location = self.multiworld.get_location("88 Easter Eggs Collected", 1)

            self.assertNotEqual(egg_84_location.progress_type, LocationProgressType.EXCLUDED)
            self.assertEqual(egg_88_location.progress_type, LocationProgressType.EXCLUDED)

        with self.subTest("Test that in a seed with the whole game included, the 120 egg location exists"):
            self.assert_location_exists("120 Easter Eggs Collected", 2)

        with self.subTest(
            "Test that locations beyond 96 Easter Eggs, which would logically require more than 120 Eggs, are excluded"
        ):
            egg_96_location = self.multiworld.get_location("96 Easter Eggs Collected", 2)
            egg_100_location = self.multiworld.get_location("100 Easter Eggs Collected", 2)

            self.assertNotEqual(egg_96_location.progress_type, LocationProgressType.EXCLUDED)
            self.assertEqual(egg_100_location.progress_type, LocationProgressType.EXCLUDED)

        with self.subTest("Test that you can exclude and egg to disable it"):
            self.assert_location_exists("116 Easter Eggs Collected", 3)
            self.assert_location_does_not_exist("120 Easter Eggs Collected", 3)


class TestBunkerElevatorEgg(WitnessMultiworldTestBase):
    options_per_world = [
        {
            "elevators_come_to_you": frozenset()
        },
        {
            "elevators_come_to_you": frozenset({"Bunker Elevator"})
        },
    ]

    common_options = {
        "easter_egg_hunt": "normal",
        "shuffle_doors": "panels",
        "shuffle_symbols": False,
    }

    def test_bunker_elevator_egg(self) -> None:
        items_to_reach_bunker_elevator = [
            "Bunker Entry (Panel)",
            "Bunker Tinted Glass Door (Panel)",
            "Bunker Drop-Down Door Controls (Panel)"
        ]

        with self.subTest("Test that normally, the egg behind the elevator needs Elevator Control"):
            self.assertFalse(self.multiworld.state.can_reach_location("Bunker Under Elevator Easter Egg", 1))
            self.collect_by_name(items_to_reach_bunker_elevator, 1)
            self.assertFalse(self.multiworld.state.can_reach_location("Bunker Under Elevator Easter Egg", 1))
            self.collect_by_name(["Bunker Elevator Control (Panel)"], 1)
            self.assertTrue(self.multiworld.state.can_reach_location("Bunker Under Elevator Easter Egg", 1))

        with self.subTest("Test that with auto-elevators, the egg behind the elevator doesn't need Elevator Control"):
            self.assertFalse(self.multiworld.state.can_reach_location("Bunker Under Elevator Easter Egg", 2))
            self.collect_by_name(items_to_reach_bunker_elevator, 2)
            self.assertTrue(self.multiworld.state.can_reach_location("Bunker Under Elevator Easter Egg", 2))
