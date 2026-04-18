from ..rules import _has_lasers
from ..test.bases import WitnessTestBase


class TestDisableNonRandomized(WitnessTestBase):
    run_default_tests = False

    options = {
        "disable_non_randomized_puzzles": True,
        "shuffle_doors": "panels",
        "early_symbol_item": False,
    }

    def test_locations_got_disabled_and_alternate_activation_triggers_work(self) -> None:
        """
        Test the different behaviors of the disable_non_randomized mode:

        1. Unrandomized locations like Orchard Apple Tree 5 are disabled.
        2. Certain doors or lasers that would usually be activated by unrandomized panels depend on event items instead.
        3. These alternate activations are tied to solving Discarded Panels.
        """

        with self.subTest("Test that unrandomized locations are disabled."):
            self.assert_location_does_not_exist("Orchard Apple Tree 5")

        with self.subTest("Test that alternate activation trigger events exist."):
            self.assert_dependency_on_event_item(
                self.world.get_entrance("Town Tower After Third Door to Town Tower Top"),
                "Town Tower 4th Door Opens",
            )

        with self.subTest("Test that alternate activation triggers award lasers."):
            self.assertFalse(_has_lasers(1, self.world, False)(self.multiworld.state))

            self.collect_by_name("Triangles")

            # Alternate triggers yield Bunker Laser (Mountainside Discard) and Monastery Laser (Desert Discard)
            self.assertTrue(_has_lasers(2, self.world, False)(self.multiworld.state))
            self.assertFalse(_has_lasers(3, self.world, False)(self.multiworld.state))
