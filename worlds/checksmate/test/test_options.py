import unittest

from ..options import CMOptions, MaxBoardSize, MinBoardSize
from ..presets import checksmate_option_presets


class TestMinBoardSize(unittest.TestCase):
    def test_supports_only_selectable_start_sizes(self):
        expected = {
            -1: "6x8",
            0: "8x8",
            1: "10x8",
        }

        self.assertEqual(expected, MinBoardSize.name_lookup)
        for value, name in expected.items():
            with self.subTest(value=value, name=name):
                self.assertEqual(value, MinBoardSize.from_any(value).value)
                self.assertEqual(value, MinBoardSize.from_any(name).value)


class TestMaxBoardSize(unittest.TestCase):
    def test_supports_only_selectable_terminal_sizes(self):
        expected = {
            -1: "6x8",
            0: "8x8",
            1: "10x8",
            2: "10x10",
            3: "12x10",
        }

        self.assertIsNot(MinBoardSize, MaxBoardSize)
        self.assertEqual(expected, MaxBoardSize.name_lookup)
        for value, name in expected.items():
            with self.subTest(value=value, name=name):
                self.assertEqual(value, MaxBoardSize.from_any(value).value)
                self.assertEqual(value, MaxBoardSize.from_any(name).value)


class TestChecksmateOptions(unittest.TestCase):
    def test_exposes_board_size_bounds_instead_of_goal(self):
        self.assertNotIn("goal", CMOptions.type_hints)
        self.assertIs(MinBoardSize, CMOptions.type_hints["min_board_size"])
        self.assertIs(MaxBoardSize, CMOptions.type_hints["max_board_size"])
        self.assertEqual(0, MinBoardSize.default)
        self.assertEqual(3, MaxBoardSize.default)
        self.assertEqual("Minimum Board Size", MinBoardSize.display_name)
        self.assertEqual("Maximum Board Size", MaxBoardSize.display_name)

    def test_presets_use_valid_ordered_board_bounds(self):
        for name, preset in checksmate_option_presets.items():
            with self.subTest(name=name):
                start = MinBoardSize.from_any(
                    preset.get("min_board_size", MinBoardSize.default)
                )
                end = MaxBoardSize.from_any(
                    preset.get("max_board_size", MaxBoardSize.default)
                )
                self.assertLessEqual(start.value, end.value)
