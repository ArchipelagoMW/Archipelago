import unittest
from worlds.luigismansion.lm.Wallet.Wallet import Wallet, _RANK_REQ_AMTS
from worlds.luigismansion.lm.Wallet.Currency import *

class _MockCurrency(Currency):
    """
    Testable Currency object, mocking functionality which normally relies upon external dependencies.
    """
    def __init__(self, name: str, mem_loc: str,  calc_value: int, current_amount: int):
        super().__init__(name, mem_loc, calc_value)

        self.current_amount = current_amount
    
    def get(self):
        return self.current_amount

class TEST_DATA:
    def get_test_currencies() -> dict[int, _MockCurrency]:
        return {
            CURRENCY_INDEX.COIN:         _MockCurrency(CURRENCY_NAME.COINS,        0x01, 5000,     0),
            CURRENCY_INDEX.BILLS:        _MockCurrency(CURRENCY_NAME.BILLS,        0x02, 20000,    0),
            CURRENCY_INDEX.GOLD_BARS:    _MockCurrency(CURRENCY_NAME.GOLD_BARS,    0x03, 100000,   0),
            CURRENCY_INDEX.SAPPHIRE:     _MockCurrency(CURRENCY_NAME.SAPPHIRE,     0x04, 500000,   0),
            CURRENCY_INDEX.EMERALD:      _MockCurrency(CURRENCY_NAME.EMERALD,      0x05, 800000,   0),
            CURRENCY_INDEX.RUBY:         _MockCurrency(CURRENCY_NAME.RUBY,         0x06, 1000000,  0),
            CURRENCY_INDEX.DIAMOND:      _MockCurrency(CURRENCY_NAME.DIAMOND,      0x07, 2000000,  0),
            CURRENCY_INDEX.GOLD_DIAMOND: _MockCurrency(CURRENCY_NAME.GOLD_DIAMOND, 0x08, 20000000, 0),
            CURRENCY_INDEX.SMALL_PEARL:  _MockCurrency(CURRENCY_NAME.SMALL_PEARL,  0x09, 50000,    0),
            CURRENCY_INDEX.MEDIUM_PEARL: _MockCurrency(CURRENCY_NAME.MEDIUM_PEARL, 0x10, 100000,   0),
            CURRENCY_INDEX.LARGE_PEARL:  _MockCurrency(CURRENCY_NAME.LARGE_PEARL,  0x11, 1000000,  0),
        }

class TestWalletWorth(unittest.TestCase):
    def test_get_wallet_worth_single_coin(self):
        """Verifies that get_wallet_worth retrurn the correct amount."""
        test_currencies: dict[int, _MockCurrency] = TEST_DATA.get_test_currencies()
        test_currencies[CURRENCY_INDEX.COIN].current_amount = 1
        expected_worth = test_currencies[CURRENCY_INDEX.COIN].calculate_worth()

        wallet = Wallet(test_currencies)
        total_worth = wallet.get_wallet_worth()

        self.assertEqual(total_worth, expected_worth)
    
    def test_get_wallet_worth_single_each(self):
        """Verifies that get_wallet_worth retrurn the correct amount."""
        test_currencies: dict[int, _MockCurrency] = TEST_DATA.get_test_currencies()

        expected_worth = 0
        for test_currency in test_currencies.values():
            test_currency.current_amount = 1
            expected_worth += test_currency.calculate_worth()

        wallet = Wallet(test_currencies)
        total_worth = wallet.get_wallet_worth()

        self.assertEqual(total_worth, expected_worth)

    def test_get_wallet_worth_multiple_currencies(self):
        test_currencies: dict[int, _MockCurrency] = TEST_DATA.get_test_currencies()
        test_currencies[CURRENCY_INDEX.COIN].current_amount = 10
        test_currencies[CURRENCY_INDEX.BILLS].current_amount = 1
        test_currencies[CURRENCY_INDEX.GOLD_BARS].current_amount = 1
        test_currencies[CURRENCY_INDEX.SAPPHIRE].current_amount = 1
        test_currencies[CURRENCY_INDEX.EMERALD].current_amount = 1
        test_currencies[CURRENCY_INDEX.RUBY].current_amount = 1
        test_currencies[CURRENCY_INDEX.DIAMOND].current_amount = 5
        test_currencies[CURRENCY_INDEX.GOLD_DIAMOND].current_amount = 1
        test_currencies[CURRENCY_INDEX.SMALL_PEARL].current_amount = 1
        test_currencies[CURRENCY_INDEX.MEDIUM_PEARL].current_amount = 1
        test_currencies[CURRENCY_INDEX.LARGE_PEARL].current_amount = 3

        expected_worth = 0
        for currency in test_currencies.values():
            expected_worth += currency.calculate_worth()

        wallet = Wallet(test_currencies)
        total_worth = wallet.get_wallet_worth()

        self.assertEqual(total_worth, expected_worth)
    
    def test_check_rank_requirement_no_rank(self):
        """Verifies that an empty wallet will be valid when there's no rank_requirement"""
        test_currencies = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        wallet.rank_requirement = 0
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertTrue(actual_result)
    
    def test_check_rank_requirement_first_rank_meets(self):
        """Verifies that luigi's wallet contains at least: 5,000,000 -> returns True"""
        test_currencies: list[_MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_INDEX.BILLS].current_amount = 250

        wallet.rank_requirement = 1
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertTrue(actual_result)
    
    def test_check_rank_requirement_first_rank_does_not_meet(self):
        """Verifies that luigi's wallet contains less than: 5,000,000 -> returns False"""
        test_currencies: list[_MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_INDEX.BILLS].current_amount = 249

        wallet.rank_requirement = 1
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertFalse(actual_result)
    
    def test_check_rank_requirement_second_rank_meets(self):
        """Verifies that luigi's wallet contains at least 20,000,000 -> returns True"""
        test_currencies: list[_MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_INDEX.GOLD_DIAMOND].current_amount = 1

        wallet.rank_requirement = 2
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertTrue(actual_result)
    
    def test_check_rank_requirement_second_rank_does_not_meet(self):
        """Verifies that luigi's wallet contains less than 20,000,000 -> returns False"""
        test_currencies: list[_MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_INDEX.GOLD_DIAMOND].current_amount = 0

        wallet.rank_requirement = 2
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertFalse(actual_result)
    
    def test_check_rank_requirement_third_rank_meets(self):
        """Verifies that luigi's wallet contains at least 40,000,000 -> returns True"""
        test_currencies: list[_MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_INDEX.GOLD_DIAMOND].current_amount = 2

        wallet.rank_requirement = 3
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertTrue(actual_result)

    def test_check_rank_requirement_third_rank_does_not_meet(self):
        """Verifies that luigi's wallet contains less than 40,000,000 -> returns False"""
        test_currencies: list[_MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_INDEX.GOLD_DIAMOND].current_amount = 1

        wallet.rank_requirement = 3
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertFalse(actual_result)
    
    def test_check_rank_requirement_fourth_rank_meets(self):
        """Verifies that luigi's wallet contains at least 50,000,000 -> returns True"""
        test_currencies: list[_MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_INDEX.GOLD_DIAMOND].current_amount = 3

        wallet.rank_requirement = 4
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertTrue(actual_result)

    def test_check_rank_requirement_fourth_rank_does_not_meet(self):
        """Verifies that luigi's wallet contains less than 50,000,000 -> returns False"""
        test_currencies: list[_MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_INDEX.GOLD_DIAMOND].current_amount = 1

        wallet.rank_requirement = 4
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertFalse(actual_result)
    
    def test_check_rank_requirement_fifth_rank_meets(self):
        """Verifies that luigi's wallet contains at least 60,000,000 -> returns True"""
        test_currencies: list[_MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_INDEX.GOLD_DIAMOND].current_amount = 3

        wallet.rank_requirement = 5
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertTrue(actual_result)
    
    def test_check_rank_requirement_fifth_rank_does_not_meet(self):
        """Verifies that luigi's wallet contains less than 60,000,000 -> returns False"""
        test_currencies: list[_MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_INDEX.GOLD_DIAMOND].current_amount = 2

        wallet.rank_requirement = 5
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertFalse(actual_result)
    
    def test_check_rank_requirement_sixth_rank_meets(self):
        """Verifies that luigi's wallet contains at least 70,000,000 -> returns True"""
        test_currencies: list[_MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_INDEX.GOLD_DIAMOND].current_amount = 4

        wallet.rank_requirement = 6
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertTrue(actual_result)

    def test_check_rank_requirement_sixth_rank_does_not_meet(self):
        """Verifies that luigi's wallet contains less than 70,000,000 -> returns False"""
        test_currencies: list[_MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_INDEX.GOLD_DIAMOND].current_amount = 3

        wallet.rank_requirement = 6
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertFalse(actual_result)
    
    def test_check_rank_requirement_seventh_rank_meets(self):
        """Verifies that luigi's wallet contains at least 100,000,000 -> returns True"""
        test_currencies: list[_MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_INDEX.GOLD_DIAMOND].current_amount = 5

        wallet.rank_requirement = 7
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertTrue(actual_result)
    
    def test_check_rank_requirement_seventh_rank_does_not_meet(self):
        """Verifies that luigi's wallet contains less than 100,000,000 -> returns False"""
        test_currencies: list[_MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_INDEX.GOLD_DIAMOND].current_amount = 4

        wallet.rank_requirement = 7
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertFalse(actual_result)                

class TestWallet(unittest.TestCase):
    def test_get_rank_requirement(self):
        for iterator in range(0, len(_RANK_REQ_AMTS)):
            with self.subTest(label=f"test_rank_requirement_{iterator}"):
                wallet = Wallet()
                wallet.rank_requirement = iterator

                amount = wallet.get_rank_requirement()
                self.assertEqual(amount, _RANK_REQ_AMTS[iterator])

