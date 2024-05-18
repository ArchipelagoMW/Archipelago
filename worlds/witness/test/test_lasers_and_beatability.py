from worlds.witness.rules import _has_lasers
from worlds.witness.test import WitnessTestBase


class TestDisableNonRandomizedLasers(WitnessTestBase):
    options = {
        "disable_non_randomized_puzzles": True,
        "shuffle_doors": "panels",
        "early_symbol_item": False,
    }

    def test_can_reach_lasers_through_alternate_activation_triggers(self):
        self.assertFalse(_has_lasers(1, self.world, False)(self.multiworld.state))

        self.collect_by_name("Triangles")

        # Alternate activation triggers yield Bunker Laser (Mountainside Discard) and Monastery Laser (Desert Discard)
        self.assertTrue(_has_lasers(2, self.world, False)(self.multiworld.state))
