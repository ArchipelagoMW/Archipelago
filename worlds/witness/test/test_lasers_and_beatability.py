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


class TestSymbolsRequiredToWinNormal(WitnessTestBase):
    options = {
        "puzzle_randomization": "sigma_normal",
        "mountain_lasers": 1,
        "victory_condition": "elevator",
        "early_symbol_item": False,
    }

    def test_symbols_to_win(self):
        exact_requirement = {
            "Progressive Dots": 2,
            "Progressive Stars": 2,
            "Progressive Symmetry": 2,
            "Black/White Squares": 1,
            "Colored Squares": 1,
            "Shapers": 1,
            "Rotated Shapers": 1,
            "Eraser": 1,
        }

        self.assert_can_beat_with_minimally(exact_requirement)


class TestSymbolsRequiredToWinExpert(WitnessTestBase):
    options = {
        "mountain_lasers": 1,
        "victory_condition": "elevator",
        "early_symbol_item": False,
        "puzzle_randomization": "sigma_expert",
    }

    def test_symbols_to_win(self):
        exact_requirement = {
            "Progressive Dots": 2,
            "Progressive Stars": 2,
            "Progressive Symmetry": 2,
            "Black/White Squares": 1,
            "Colored Squares": 1,
            "Shapers": 1,
            "Rotated Shapers": 1,
            "Negative Shapers": 1,
            "Eraser": 1,
            "Triangles": 1,
        }

        self.assert_can_beat_with_minimally(exact_requirement)


class TestSymbolsRequiredToWinVanilla(WitnessTestBase):
    options = {
        "mountain_lasers": 1,
        "victory_condition": "elevator",
        "early_symbol_item": False,
        "puzzle_randomization": "none",
    }

    def test_symbols_to_win(self):
        exact_requirement = {
            "Progressive Dots": 2,
            "Progressive Stars": 2,
            "Progressive Symmetry": 1,
            "Black/White Squares": 1,
            "Colored Squares": 1,
            "Shapers": 1,
            "Rotated Shapers": 1,
            "Eraser": 1,
        }

        self.assert_can_beat_with_minimally(exact_requirement)
