from ..game.Currency import Currency, CURRENCIES, CURRENCY_NAME

# Rank Requirements for each rank. H, G, F, E, D, C, B, A
_RANK_REQ_AMTS = [0, 5000000, 20000000, 40000000, 50000000, 60000000, 70000000, 100000000]

class Wallet:
    """
    Manages Luigi's currencies including adding/removing currencies during a run.
    It also manages the randomizer check 'rank_requirement'.
    """

    def __init__(self, currencies: dict[str, Currency] = CURRENCIES):
        self._currencies = currencies
        self.rank_requirement = 0

    def get_wallet_worth(self) -> int:
        """
        Determines Luigi's wallet's total worth for 'rank_requirement'.

        :return: The combined worth of each currency.
        :rtype: int
        """
        total_worth = 0
        for currency in self._currencies.values():
            total_worth += currency.calculate_worth()
        return total_worth

    def add_to_wallet(self, currencies: dict[str, int]):
        """
        Adds currencies to Luigi's wallet.
        
        :param currencies: Collection of key value pairs, where the key is the name of the currency
        and the value is the amount to be added.
        """
        for key, value in currencies.items():
            self._currencies[key].add(value)

    def check_rank_requirement(self) -> bool:
        """
        Determines if Luigi's wallet's worth meets or exceeds the rank requirement.

        :return: Returns True when the wallets value is >= the requirement, otherwise returns False.
        :rtype: bool
        """
        return self.get_wallet_worth() >= self.get_rank_requirement()

    def get_rank_requirement(self) -> int:
        """
        Gets the randomizer's Rank Requirement based upon 'rank_requirement' rating (H-A).
        """
        return _RANK_REQ_AMTS[self.rank_requirement]

    def remove_from_wallet(self, currencies: dict[str, int]):
        """
        Removes currencies from Luigi's wallet.

        :param currencies: Collection of key value pairs, where the key is the name of the currency
        and the value is the amount to be removed.
        """
        for key, value in currencies.items():
            self._currencies[key].remove(value)

    def get_currency_amount(self, currency_name: str) -> int:
        """
        Gets the amount of the request currency currently in Luigi's wallet.

        :param currency_name: The friendly name of the requested currency.
        seealso: Currency.CURRENCY_NAME.<NAME>
        """
        return self._currencies[currency_name].get()

    def add_amount_to_wallet(self, amount: int):
        """
        Adds currency to the wallet based upon a calculated amount.

        :param amount: The uncalculated amount to be added to the wallet.
        """
        calculated_amount = self.get_calculated_amount_worth(amount)
        currencies_to_add = _create_currencies_to_update_from_int(calculated_amount, self._currencies)
        self.add_to_wallet(currencies_to_add)

    def remove_amount_from_wallet(self, amount: int):
        """
        Removes currency from the wallet based upon a calculated amount.

        :param amount: The uncalculated amount to be removed from the wallet.
        """
        calculated_amount = self.get_calculated_amount_worth(amount)
        if self.get_wallet_worth() < calculated_amount:
            raise ArithmeticError("Not enough money in wallet to be sent to EnergyLink.")

        currencies_to_remove = _create_currencies_to_update_from_int(calculated_amount, { k:v for k, v in self._currencies.items() if v.get() > 0 } )
        if len(currencies_to_remove) == 0:
            raise ArithmeticError("Not enough money in wallet to be sent to EnergyLink.")

        self.remove_from_wallet(currencies_to_remove)

    def get_calculated_amount_worth(self, amount: int) -> int:
        """
        Determines the rank requirement value of a given 'amount' based upon the lowest currency worth.

        :param amount: The amount to be calculated.
        """
        sorted_currencies = dict(sorted(self._currencies.items(), key=lambda item: item[1].calc_value))
        first_key = next(iter(sorted_currencies))
        return int(self._currencies[first_key].calc_value * amount)

    def get_currencies(self) -> dict[str, Currency]:
        return self._currencies

def _create_currencies_to_update_from_int(amount: int, currencies: dict[str, Currency]) -> dict[str, int]:
    new_amount = amount
    currencies_to_add: dict[str, int] = {}

    sorted_currencies = dict(sorted(currencies.items(), key=lambda item: item[1].calc_value, reverse=True))
    for currency_name, currency_value in sorted_currencies.items():
        if new_amount == 0:
            break

        currency_to_add, remainder = divmod(new_amount, currency_value.calc_value)
        new_amount = remainder

        if currency_to_add > 0:
            currencies_to_add.update({ currency_name: int(currency_to_add) })

    return currencies_to_add
