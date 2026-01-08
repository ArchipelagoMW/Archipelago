import random
from unittest import TestCase

from ..pokemon import get_random_colors, convert_color


class ColorTests(TestCase):
    def test_get_random_colors(self):
        r = random.Random(1)

        colors = get_random_colors(r)
        self.assertEqual(colors, [136, 64, 231, 115, 30, 55, 230, 7])

        colors = get_random_colors(r)
        self.assertEqual(colors, [120, 3, 60, 58, 134, 6, 33, 0])

    def test_convert_color(self):
        result = convert_color(200, 100, 0)
        self.assertEqual(result, b"\xff\x03")

        result = convert_color(200, 100, 100)
        self.assertEqual(result, b"\xff\x7f")

        result = convert_color(10, 15, 20)
        self.assertEqual(result, b"\xeaQ")

        result = convert_color(0, 0, 0)
        self.assertEqual(result, b"\x00\x00")

        result = convert_color(-100, -1, -1)
        self.assertEqual(result, b"\x00\x00")
