import unittest
from ..client.Wallet import Wallet, _RANK_REQ_AMTS
from ..game.Currency import *

class _MockCurrency(Currency):
    """
    Testable Currency object, mocking functionality which normally relies upon external dependencies.
    """
    def __init__(self, name: str, mem_loc: str,  calc_value: int, current_amount: int):
        super().__init__(name, mem_loc, calc_value)

        self.current_amount = current_amount

    def get(self):
        return self.current_amount

    def remove(self, amount: int):
        self.current_amount -= amount

    def add(self, amount: int):
        self.current_amount += amount

class TEST_DATA:
    @staticmethod
    def get_test_currencies(coins = 0, bills = 0, gold_bars = 0, sapphire = 0, emerald = 0, ruby = 0, diamond = 0, gold_diamond = 0, small_pearl = 0, medium_pearl = 0, large_pearl = 0) -> dict[str, _MockCurrency]:
        return {
            CURRENCY_NAME.COINS:        _MockCurrency(CURRENCY_NAME.COINS,        0x01, 5000,     coins),
            CURRENCY_NAME.BILLS:        _MockCurrency(CURRENCY_NAME.BILLS,        0x02, 20000,    bills),
            CURRENCY_NAME.GOLD_BARS:    _MockCurrency(CURRENCY_NAME.GOLD_BARS,    0x03, 100000,   gold_bars),
            CURRENCY_NAME.SAPPHIRE:     _MockCurrency(CURRENCY_NAME.SAPPHIRE,     0x04, 500000,   sapphire),
            CURRENCY_NAME.EMERALD:      _MockCurrency(CURRENCY_NAME.EMERALD,      0x05, 800000,   emerald),
            CURRENCY_NAME.RUBY:         _MockCurrency(CURRENCY_NAME.RUBY,         0x06, 1000000,  ruby),
            CURRENCY_NAME.DIAMOND:      _MockCurrency(CURRENCY_NAME.DIAMOND,      0x07, 2000000,  diamond),
            CURRENCY_NAME.GOLD_DIAMOND: _MockCurrency(CURRENCY_NAME.GOLD_DIAMOND, 0x08, 20000000, gold_diamond),
            CURRENCY_NAME.SMALL_PEARL:  _MockCurrency(CURRENCY_NAME.SMALL_PEARL,  0x09, 50000,    small_pearl),
            CURRENCY_NAME.MEDIUM_PEARL: _MockCurrency(CURRENCY_NAME.MEDIUM_PEARL, 0x10, 100000,   medium_pearl),
            CURRENCY_NAME.LARGE_PEARL:  _MockCurrency(CURRENCY_NAME.LARGE_PEARL,  0x11, 1000000,  large_pearl),
        }

class TestWalletWorth(unittest.TestCase):
    def test_get_wallet_worth_single_coin(self):
        """Verifies that get_wallet_worth retrurn the correct amount."""
        test_currencies: dict[str, _MockCurrency] = TEST_DATA.get_test_currencies()
        test_currencies[CURRENCY_NAME.COINS].current_amount = 1
        expected_worth = test_currencies[CURRENCY_NAME.COINS].calculate_worth()

        wallet = Wallet(test_currencies)
        total_worth = wallet.get_wallet_worth()

        self.assertEqual(total_worth, expected_worth)

    def test_get_wallet_worth_single_each(self):
        """Verifies that get_wallet_worth retrurn the correct amount."""
        test_currencies: dict[str, _MockCurrency] = TEST_DATA.get_test_currencies()

        expected_worth = 0
        for test_currency in test_currencies.values():
            test_currency.current_amount = 1
            expected_worth += test_currency.calculate_worth()

        wallet = Wallet(test_currencies)
        total_worth = wallet.get_wallet_worth()

        self.assertEqual(total_worth, expected_worth)

    def test_get_wallet_worth_multiple_currencies(self):
        test_currencies: dict[str, _MockCurrency] = TEST_DATA.get_test_currencies()
        test_currencies[CURRENCY_NAME.COINS].current_amount = 10
        test_currencies[CURRENCY_NAME.BILLS].current_amount = 1
        test_currencies[CURRENCY_NAME.GOLD_BARS].current_amount = 1
        test_currencies[CURRENCY_NAME.SAPPHIRE].current_amount = 1
        test_currencies[CURRENCY_NAME.EMERALD].current_amount = 1
        test_currencies[CURRENCY_NAME.RUBY].current_amount = 1
        test_currencies[CURRENCY_NAME.DIAMOND].current_amount = 5
        test_currencies[CURRENCY_NAME.GOLD_DIAMOND].current_amount = 1
        test_currencies[CURRENCY_NAME.SMALL_PEARL].current_amount = 1
        test_currencies[CURRENCY_NAME.MEDIUM_PEARL].current_amount = 1
        test_currencies[CURRENCY_NAME.LARGE_PEARL].current_amount = 3

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
        test_currencies: dict[str, _MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_NAME.BILLS].current_amount = 250

        wallet.rank_requirement = 1
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertTrue(actual_result)

    def test_check_rank_requirement_first_rank_does_not_meet(self):
        """Verifies that luigi's wallet contains less than: 5,000,000 -> returns False"""
        test_currencies: dict[str, _MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_NAME.BILLS].current_amount = 249

        wallet.rank_requirement = 1
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertFalse(actual_result)

    def test_check_rank_requirement_second_rank_meets(self):
        """Verifies that luigi's wallet contains at least 20,000,000 -> returns True"""
        test_currencies: dict[str, _MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_NAME.GOLD_DIAMOND].current_amount = 1

        wallet.rank_requirement = 2
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertTrue(actual_result)

    def test_check_rank_requirement_second_rank_does_not_meet(self):
        """Verifies that luigi's wallet contains less than 20,000,000 -> returns False"""
        test_currencies: dict[str, _MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_NAME.GOLD_DIAMOND].current_amount = 0

        wallet.rank_requirement = 2
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertFalse(actual_result)

    def test_check_rank_requirement_third_rank_meets(self):
        """Verifies that luigi's wallet contains at least 40,000,000 -> returns True"""
        test_currencies: dict[str, _MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_NAME.GOLD_DIAMOND].current_amount = 2

        wallet.rank_requirement = 3
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertTrue(actual_result)

    def test_check_rank_requirement_third_rank_does_not_meet(self):
        """Verifies that luigi's wallet contains less than 40,000,000 -> returns False"""
        test_currencies: dict[str, _MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_NAME.GOLD_DIAMOND].current_amount = 1

        wallet.rank_requirement = 3
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertFalse(actual_result)

    def test_check_rank_requirement_fourth_rank_meets(self):
        """Verifies that luigi's wallet contains at least 50,000,000 -> returns True"""
        test_currencies: dict[str, _MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_NAME.GOLD_DIAMOND].current_amount = 3

        wallet.rank_requirement = 4
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertTrue(actual_result)

    def test_check_rank_requirement_fourth_rank_does_not_meet(self):
        """Verifies that luigi's wallet contains less than 50,000,000 -> returns False"""
        test_currencies: dict[str, _MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_NAME.GOLD_DIAMOND].current_amount = 1

        wallet.rank_requirement = 4
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertFalse(actual_result)

    def test_check_rank_requirement_fifth_rank_meets(self):
        """Verifies that luigi's wallet contains at least 60,000,000 -> returns True"""
        test_currencies: dict[str, _MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_NAME.GOLD_DIAMOND].current_amount = 3

        wallet.rank_requirement = 5
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertTrue(actual_result)

    def test_check_rank_requirement_fifth_rank_does_not_meet(self):
        """Verifies that luigi's wallet contains less than 60,000,000 -> returns False"""
        test_currencies: dict[str, _MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_NAME.GOLD_DIAMOND].current_amount = 2

        wallet.rank_requirement = 5
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertFalse(actual_result)

    def test_check_rank_requirement_sixth_rank_meets(self):
        """Verifies that luigi's wallet contains at least 70,000,000 -> returns True"""
        test_currencies: dict[str, _MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_NAME.GOLD_DIAMOND].current_amount = 4

        wallet.rank_requirement = 6
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertTrue(actual_result)

    def test_check_rank_requirement_sixth_rank_does_not_meet(self):
        """Verifies that luigi's wallet contains less than 70,000,000 -> returns False"""
        test_currencies: dict[str, _MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_NAME.GOLD_DIAMOND].current_amount = 3

        wallet.rank_requirement = 6
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertFalse(actual_result)

    def test_check_rank_requirement_seventh_rank_meets(self):
        """Verifies that luigi's wallet contains at least 100,000,000 -> returns True"""
        test_currencies: dict[str, _MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_NAME.GOLD_DIAMOND].current_amount = 5

        wallet.rank_requirement = 7
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertTrue(actual_result)

    def test_check_rank_requirement_seventh_rank_does_not_meet(self):
        """Verifies that luigi's wallet contains less than 100,000,000 -> returns False"""
        test_currencies: dict[str, _MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        test_currencies[CURRENCY_NAME.GOLD_DIAMOND].current_amount = 4

        wallet.rank_requirement = 7
        wallet.check_rank_requirement()

        actual_result = wallet.check_rank_requirement()
        self.assertFalse(actual_result)

    def test_add_currencies(self):
        """Verifies that multiple currency types can be added to luigi's wallet."""
        test_currencies: dict[str, _MockCurrency] = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        wallet.add_to_wallet({
            CURRENCY_NAME.COINS: 10,
            CURRENCY_NAME.BILLS: 15,
        })

        self.assertEqual(test_currencies[CURRENCY_NAME.COINS].get(), 10)
        self.assertEqual(test_currencies[CURRENCY_NAME.BILLS].get(), 15)

    def test_get_calculated_amount_worth(self):
        """Verifies that the lowest worth item is pulled when calculating worth."""
        test_currencies = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        actual_worth = wallet.get_calculated_amount_worth(1)
        self.assertEqual(test_currencies[CURRENCY_NAME.COINS].calc_value, actual_worth)

    def test_get_calculated_amount_worth_amount_matches(self):
        """Verifies that the the lowest worth amount is multipled by the amount being calculated."""
        test_currencies = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        amount = 50
        test_currencies[CURRENCY_NAME.COINS].calc_value = 50

        actual_worth = wallet.get_calculated_amount_worth(amount)
        self.assertEqual(actual_worth, 2500)

    def test_get_calculated_amount_worth_returns_int(self):
        """Verifies that the the lowest worth amount is multipled by the amount being calculated."""
        test_currencies = TEST_DATA.get_test_currencies()
        wallet = Wallet(test_currencies)

        amount = 50
        test_currencies[CURRENCY_NAME.COINS].calc_value = 50.0

        actual_worth = wallet.get_calculated_amount_worth(amount)
        self.assertEqual(actual_worth, 2500)
        self.assertIsInstance(actual_worth, int)

class TestWallet(unittest.TestCase):
    def test_get_rank_requirement(self):
        for iterator in range(0, len(_RANK_REQ_AMTS)):
            with self.subTest(label=f"test_rank_requirement_{iterator}"):
                wallet = Wallet()
                wallet.rank_requirement = iterator

                amount = wallet.get_rank_requirement()
                self.assertEqual(amount, _RANK_REQ_AMTS[iterator])
