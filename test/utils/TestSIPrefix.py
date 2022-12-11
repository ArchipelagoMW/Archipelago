# Tests for SI prefix in Utils.py

import unittest
from decimal import Decimal
from Utils import format_SI_prefix


class TestGenerateMain(unittest.TestCase):
    """This tests SI prefix formatting in Utils.py"""
    def assertEqual(self, first, second, msg=None):
        # we strip spaces everywhere because that is an undefined implementation detail
        super().assertEqual(first.replace(" ", ""), second.replace(" ", ""), msg)

    def test_rounding(self):
        # we don't care if float(999.995) would fail due to error in precision
        self.assertEqual(format_SI_prefix(999.999), "1.00k")
        self.assertEqual(format_SI_prefix(1000.001), "1.00k")
        self.assertEqual(format_SI_prefix(Decimal("999.995")), "1.00k")
        self.assertEqual(format_SI_prefix(Decimal("1000.004")), "1.00k")

    def test_letters(self):
        self.assertEqual(format_SI_prefix(0e0), "0.00")
        self.assertEqual(format_SI_prefix(1e3), "1.00k")
        self.assertEqual(format_SI_prefix(2e6), "2.00M")
        self.assertEqual(format_SI_prefix(3e9), "3.00G")
        self.assertEqual(format_SI_prefix(4e12), "4.00T")
        self.assertEqual(format_SI_prefix(5e15), "5.00P")
        self.assertEqual(format_SI_prefix(6e18), "6.00E")
        self.assertEqual(format_SI_prefix(7e21), "7.00Z")
        self.assertEqual(format_SI_prefix(8e24), "8.00Y")

    def test_multiple_letters(self):
        self.assertEqual(format_SI_prefix(9e27), "9.00kY")

    def test_custom_power(self):
        self.assertEqual(format_SI_prefix(1023.99, 1024), "1023.99")
        self.assertEqual(format_SI_prefix(1034.24, 1024), "1.01k")

    def test_custom_labels(self):
        labels = ("E", "da", "h", "k")
        self.assertEqual(format_SI_prefix(1, 10, labels), "1.00E")
        self.assertEqual(format_SI_prefix(10, 10, labels), "1.00da")
        self.assertEqual(format_SI_prefix(100, 10, labels), "1.00h")
        self.assertEqual(format_SI_prefix(1000, 10, labels), "1.00k")
