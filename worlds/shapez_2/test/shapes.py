from unittest import TestCase
from .._testing import test


class TestShapeGeneration(TestCase):

    def test_tetragonal_4_layers(self):
        test(False, 4, False, 1000, True)

    def test_tetragonal_2_layers(self):
        test(False, 2, False, 1000, True)

    def test_tetragonal_10_layers(self):
        test(False, 10, False, 1000, True)

    def test_hexagonal_4_layers(self):
        test(False, 4, True, 1000, True)

    def test_hexagonal_2_layers(self):
        test(False, 2, True, 1000, True)

    def test_hexagonal_10_layers(self):
        test(False, 10, True, 1000, True)
