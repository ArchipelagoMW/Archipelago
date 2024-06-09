from ..rules import _has_lasers
from ..test import WitnessTestBase


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
        self.assertFalse(_has_lasers(3, self.world, False)(self.multiworld.state))


class TestSymbolsRequiredToWinElevatorNormal(WitnessTestBase):
    options = {
        "shuffle_lasers": True,
        "puzzle_randomization": "sigma_normal",
        "mountain_lasers": 1,
        "victory_condition": "elevator",
        "early_symbol_item": False,
    }

    def test_symbols_to_win(self):
        exact_requirement = {
            "Monastery Laser": 1,
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


class TestSymbolsRequiredToWinElevatorExpert(WitnessTestBase):
    options = {
        "shuffle_lasers": True,
        "mountain_lasers": 1,
        "victory_condition": "elevator",
        "early_symbol_item": False,
        "puzzle_randomization": "sigma_expert",
    }

    def test_symbols_to_win(self):
        exact_requirement = {
            "Monastery Laser": 1,
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


class TestSymbolsRequiredToWinElevatorVanilla(WitnessTestBase):
    options = {
        "shuffle_lasers": True,
        "mountain_lasers": 1,
        "victory_condition": "elevator",
        "early_symbol_item": False,
        "puzzle_randomization": "none",
    }

    def test_symbols_to_win(self):
        exact_requirement = {
            "Monastery Laser": 1,
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


class TestPanelsRequiredToWinElevator(WitnessTestBase):
    options = {
        "shuffle_lasers": True,
        "mountain_lasers": 1,
        "victory_condition": "elevator",
        "early_symbol_item": False,
        "shuffle_symbols": False,
        "shuffle_doors": "panels",
        "door_groupings": "off",
    }

    def test_panels_to_win(self):
        exact_requirement = {
            "Desert Laser": 1,
            "Town Desert Laser Redirect Control (Panel)": 1,
            "Mountain Floor 1 Light Bridge (Panel)": 1,
            "Mountain Floor 2 Light Bridge Near (Panel)": 1,
            "Mountain Floor 2 Light Bridge Far (Panel)": 1,
            "Mountain Floor 2 Elevator Control (Panel)": 1,
        }

        self.assert_can_beat_with_minimally(exact_requirement)


class TestDoorsRequiredToWinElevator(WitnessTestBase):
    options = {
        "shuffle_lasers": True,
        "mountain_lasers": 1,
        "victory_condition": "elevator",
        "early_symbol_item": False,
        "shuffle_symbols": False,
        "shuffle_doors": "doors",
        "door_groupings": "off",
    }

    def test_win_from_upper_mountain(self):
        exact_requirement = {
            "Monastery Laser": 1,
            "Mountain Floor 1 Exit (Door)": 1,
            "Mountain Floor 2 Staircase Near (Door)": 1,
            "Mountain Floor 2 Staircase Far (Door)": 1,
            "Mountain Floor 2 Exit (Door)": 1,
            "Mountain Bottom Floor Giant Puzzle Exit (Door)": 1,
            "Mountain Bottom Floor Pillars Room Entry (Door)": 1,
        }

        self.assert_can_beat_with_minimally(exact_requirement)

    def test_win_through_caves(self):
        exact_requirement = {
            "Monastery Laser": 1,  # Elevator Panel itself has a laser lock
            "Caves Mountain Shortcut (Door)": 1,
            "Caves Entry (Door)": 1,
            "Mountain Bottom Floor Rock (Door)": 1,
            "Mountain Bottom Floor Pillars Room Entry (Door)": 1,
        }

        self.assert_can_beat_with_minimally(exact_requirement)

    def test_win_through_tunnels_caves(self):
        exact_requirement = {
            "Monastery Laser": 1,  # Elevator Panel itself has a laser lock
            "Windmill Entry (Door)": 1,
            "Tunnels Theater Shortcut (Door)": 1,
            "Tunnels Entry (Door)": 1,
            "Challenge Entry (Door)": 1,
            "Caves Pillar Door": 1,
            "Caves Entry (Door)": 1,
            "Mountain Bottom Floor Rock (Door)": 1,
            "Mountain Bottom Floor Pillars Room Entry (Door)": 1,
        }

        self.assert_can_beat_with_minimally(exact_requirement)
