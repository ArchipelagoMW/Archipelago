import unittest

from ..game.Currency import Currency
from unittest.mock import patch

_TEST_CURRENCY_NAME = "TEST_NAME"

class TestCurrency(unittest.TestCase):
    @patch('dolphin_memory_engine.read_word')
    @patch('dolphin_memory_engine.follow_pointers')
    def test_get_currency(self, mock_dme_follow_pointers, mock_dme_read_word):
        """Verifies that when curreny.get is invoked we call into dme.read_word to get that currency's amount"""
        expected_value: int = 100
        mock_dme_read_word.return_value = expected_value

        test_currency = Currency(_TEST_CURRENCY_NAME, 0x01, 1000)
        actual_currency: int = test_currency.get()

        self.assertEqual(mock_dme_follow_pointers.call_count, 1)
        self.assertEqual(mock_dme_read_word.call_count, 1)
        self.assertEqual(actual_currency, expected_value)

    @patch('dolphin_memory_engine.write_word')
    @patch('dolphin_memory_engine.read_word')
    @patch('dolphin_memory_engine.follow_pointers')
    def test_remove_currency_valid(self, mock_dme_follow_pointers, mock_dme_read_word, mock_dme_write_word):
        """Verifies that when currency.remove is invoked we call into dme.write_word to modify that currency's amount"""
        mock_dme_read_word.return_value = 5000

        test_currency = Currency(_TEST_CURRENCY_NAME, 0x01, 1000)
        result = test_currency.remove(1250)

        self.assertEqual(mock_dme_follow_pointers.call_count, 2)
        self.assertEqual(mock_dme_write_word.call_count, 1)
        self.assertEqual(mock_dme_read_word.call_count, 1)
        self.assertTrue(result)

    @patch('dolphin_memory_engine.write_word')
    @patch('dolphin_memory_engine.read_word')
    @patch('dolphin_memory_engine.follow_pointers')
    def test_remove_currency_not_enough(self, mock_dme_follow_pointers, mock_dme_read_word, mock_dme_write_word):
        """Verifies that when more currency is attempted to be removed than exists, we return False"""
        mock_dme_read_word.return_value = 1000

        test_currency = Currency(_TEST_CURRENCY_NAME, 0x01, 1000)
        result = test_currency.remove(1250)

        self.assertEqual(mock_dme_follow_pointers.call_count, 1)
        self.assertEqual(mock_dme_read_word.call_count, 1)
        self.assertEqual(mock_dme_write_word.call_count, 0)
        self.assertFalse(result)
