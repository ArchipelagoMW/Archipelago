from ..rules import _has_lasers
from ..test import WitnessTestBase


class TestDisableNonRandomized(WitnessTestBase):
    options = {
        "disable_non_randomized_puzzles": True,
        "shuffle_doors": "panels",
        "early_symbol_item": False,
    }

    def test_unrandomized_locations_do_not_exist(self):
        self.assert_location_does_not_exist("Orchard Apple Tree 5")

    def test_can_reach_lasers_through_alternate_activation_triggers(self):
        """
        Test that specific Discarded Panels give extra lasers.
        """
        self.assertFalse(_has_lasers(1, self.world, False)(self.multiworld.state))

        self.collect_by_name("Triangles")

        # Alternate activation triggers yield Bunker Laser (Mountainside Discard) and Monastery Laser (Desert Discard)
        self.assertTrue(_has_lasers(2, self.world, False)(self.multiworld.state))
        self.assertFalse(_has_lasers(3, self.world, False)(self.multiworld.state))

    def test_town_tower_fourth_door_depends_on_event(self):
        """
        Test that entities with alternate activation triggers depend on their specific event items.
        Specifically, assert that Town Tower Fourth Door requires the Town Tower 4th Door Opens event item.
        """
        self.assert_dependency_on_event_item(
            self.world.get_entrance("Town Tower After Third Door to Town Tower Top"),
            "Town Tower 4th Door Opens",
        )
