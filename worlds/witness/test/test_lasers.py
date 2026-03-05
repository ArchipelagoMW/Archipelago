from ..test.bases import WitnessTestBase


class TestSymbolsRequiredToWinElevatorNormal(WitnessTestBase):
    options = {
        "shuffle_lasers": True,
        "puzzle_randomization": "sigma_normal",
        "mountain_lasers": 1,
        "victory_condition": "elevator",
        "early_symbol_item": False,
    }

    def test_symbols_to_win(self) -> None:
        """
        In symbol shuffle, the only way to reach the Elevator is through Mountain Entry by descending the Mountain.
        This requires a very specific set of symbol items per puzzle randomization mode.
        In this case, we check Sigma Normal Puzzles.
        """

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

    def test_symbols_to_win(self) -> None:
        """
        In symbol shuffle, the only way to reach the Elevator is through Mountain Entry by descending the Mountain.
        This requires a very specific set of symbol items per puzzle randomization mode.
        In this case, we check Sigma Expert Puzzles.
        """

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

    def test_symbols_to_win(self) -> None:
        """
        In symbol shuffle, the only way to reach the Elevator is through Mountain Entry by descending the Mountain.
        This requires a very specific set of symbol items per puzzle randomization mode.
        In this case, we check Vanilla Puzzles.
        """

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


class TestSymbolsRequiredToWinElevatorVariety(WitnessTestBase):
    options = {
        "shuffle_lasers": True,
        "mountain_lasers": 1,
        "victory_condition": "elevator",
        "early_symbol_item": False,
        "puzzle_randomization": "umbra_variety",
    }

    def test_symbols_to_win(self) -> None:
        """
        In symbol shuffle, the only way to reach the Elevator is through Mountain Entry by descending the Mountain.
        This requires a very specific set of symbol items per puzzle randomization mode.
        In this case, we check Variety Puzzles.
        """

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
            "Triangles": 1,
            "Arrows": 1,
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

    def test_panels_to_win(self) -> None:
        """
        In door panel shuffle , the only way to reach the Elevator is through Mountain Entry by descending the Mountain.
        This requires some control panels for each of the Mountain Floors.
        """

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

    def test_doors_to_elevator_paths(self) -> None:
        """
        In remote door shuffle, there are three ways to win.

        - Through the normal route (Mountain Entry -> Descend through Mountain -> Reach Bottom Floor)
        - Through the Caves using the Caves Shortcuts (Caves -> Reach Bottom Floor)
        - Through the Caves via Challenge (Tunnels -> Challenge -> Caves -> Reach Bottom Floor)
        """

        with self.subTest("Test Elevator victory in shuffle_doors through Mountain Entry."):
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

        with self.subTest("Test Elevator victory in shuffle_doors through Caves Shortcuts."):
            exact_requirement = {
                "Monastery Laser": 1,  # Elevator Panel itself has a laser lock
                "Caves Mountain Shortcut (Door)": 1,
                "Caves Entry (Door)": 1,
                "Mountain Bottom Floor Rock (Door)": 1,
                "Mountain Bottom Floor Pillars Room Entry (Door)": 1,
            }

            self.assert_can_beat_with_minimally(exact_requirement)

        with self.subTest("Test Elevator victory in shuffle_doors through Tunnels->Challenge->Caves."):
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
