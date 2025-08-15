import unittest
from ..client.Wallet import Wallet
from ..game.Currency import *
from ..client.ap_link.energy_link.energy_link_client import EnergyLinkClient
from CommonClient import CommonContext

class _MockCommonContext(CommonContext):
    def __init__(self):
        pass

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

#TODO: These tests are commented out until we determine how to manage energy link without commands.
class TestEnergyLinkClient(unittest.TestCase):
    # def test_get_currency_updates(self):
    #     """Verifies that the currency amount being pulled for energy link is accurate."""
    #     test_currencies = TEST_DATA.get_test_currencies()
    #     wallet = Wallet(test_currencies)
    #     common_context = _MockCommonContext()

    #     energy_link = EnergyLinkClient(common_context, wallet)

    #     # initial run to set values.
    #     amount_to_be_sent_to_energy_link = energy_link._get_currency_updates()
    #     self.assertEqual(amount_to_be_sent_to_energy_link, 0)

    #     test_currencies[CURRENCY_NAME.BILLS].current_amount = 20
    #     amount_to_be_sent_to_energy_link = energy_link._get_currency_updates()

    #     # Send 20 energy, and reduce the amount of Bills by 5
    #     self.assertEqual(amount_to_be_sent_to_energy_link, 20)
    #     self.assertEqual(test_currencies[CURRENCY_NAME.BILLS].current_amount, 15)

    # def test_get_currency_updates_negative_currency(self):
    #     """Verifies that the currency amount being pulled for energy link is accurate."""
    #     test_currencies = TEST_DATA.get_test_currencies()
    #     wallet = Wallet(test_currencies)
    #     common_context = _MockCommonContext()

    #     energy_link = EnergyLinkClient(common_context, wallet)
    #     amount_to_be_sent_to_energy_link = energy_link._get_currency_updates()
    #     self.assertEqual(amount_to_be_sent_to_energy_link, 0)

    #     test_currencies[CURRENCY_NAME.BILLS].current_amount = 20
    #     amount_to_be_sent_to_energy_link = energy_link._get_currency_updates()

    #     self.assertEqual(amount_to_be_sent_to_energy_link, 20)
    #     self.assertEqual(test_currencies[CURRENCY_NAME.BILLS].current_amount, 15)

    #     test_currencies[CURRENCY_NAME.BILLS].current_amount -= 5
    #     amount_to_be_sent_to_energy_link = energy_link._get_currency_updates()

    #     self.assertEqual(amount_to_be_sent_to_energy_link, 0)
    #     self.assertEqual(test_currencies[CURRENCY_NAME.BILLS].current_amount, 10)

    # def test_get_currency_updates_not_enough_calculated(self):
    #     """Verifies that if the amount of currency being added is less than a point of energy, no errors are thrown."""
    #     test_currencies = TEST_DATA.get_test_currencies()
    #     wallet = Wallet(test_currencies)
    #     common_context = _MockCommonContext()

    #     energy_link = EnergyLinkClient(common_context, wallet)

    #     test_currencies[CURRENCY_NAME.COINS].current_amount = 2
    #     amount_to_be_sent_to_energy_link = energy_link._get_currency_updates()

    #     self.assertEqual(amount_to_be_sent_to_energy_link, 0)
    #     self.assertEqual(test_currencies[CURRENCY_NAME.COINS].current_amount, 2)

    #     test_currencies[CURRENCY_NAME.COINS].current_amount += 3
    #     amount_to_be_sent_to_energy_link = energy_link._get_currency_updates()

    #     self.assertEqual(amount_to_be_sent_to_energy_link, 0)
    #     self.assertEqual(test_currencies[CURRENCY_NAME.COINS].current_amount, 5)

    # def test_get_currency_updates_valuable_single_item(self):
    #     """Verifies that a single valuable item will not try to send energy."""
    #     test_currencies = TEST_DATA.get_test_currencies()
    #     wallet = Wallet(test_currencies)
    #     common_context = _MockCommonContext()

    #     energy_link = EnergyLinkClient(common_context, wallet)
    #     test_currencies[CURRENCY_NAME.GOLD_DIAMOND].current_amount = 1
    #     amount_to_be_sent_to_energy_link = energy_link._get_currency_updates()

    #     self.assertEqual(amount_to_be_sent_to_energy_link, 0)
    #     self.assertEqual(test_currencies[CURRENCY_NAME.GOLD_DIAMOND].current_amount, 1)

    #     test_currencies[CURRENCY_NAME.GOLD_DIAMOND].current_amount += 1
    #     amount_to_be_sent_to_energy_link = energy_link._get_currency_updates()

    #     self.assertEqual(amount_to_be_sent_to_energy_link, 0)
    #     self.assertEqual(test_currencies[CURRENCY_NAME.GOLD_DIAMOND].current_amount, 2)
