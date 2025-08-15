from ..game.Currency import Currency, CURRENCIES, CURRENCY_NAME

# Rank Requirements for each rank. H, G, F, E, D, C, B, A
_RANK_REQ_AMTS = [0, 5000000, 20000000, 40000000, 50000000, 60000000, 70000000, 100000000]

class Wallet:
    """
    Manages Luigi's currencies including adding/removing currencies during a run.
    It also manages the randomizer check 'rank_requirement'.
    """

    def __init__(self, currencies: dict[str, Currency] = CURRENCIES):
        self._currencies = { k:v for k, v in sorted(currencies.items(), key=lambda item: item[1].calc_value, reverse=True) }
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

    def get_calculated_amount_worth(self, amount: int) -> int:
        """
        Determines the rank requirement value of a given 'amount' based upon the lowest currency worth.

        :param amount: The amount to be calculated.
        """
        sorted_currencies = dict(sorted(self._currencies.items(), key=lambda item: item[1].calc_value))
        first_key = next(iter(sorted_currencies))
        return int(self._currencies[first_key].calc_value * amount)

    def get_currencies(self, has_amount: bool = False, ascending: bool = False) -> dict[str, Currency]:
        """
        Gets all currency types in the wallet.

        :param has_amount: If True only gets currency types which has at least one amount of the given type,
            otherwise all currencies are returned.
        :param ascending: If True the order of the dict will sort from lowest calc_value,
            otherwise the dict will be sorted from highest calc_value.
        """
        currencies: dict[str, Currency]
        if has_amount:
            currencies = { k:v for k, v in self._currencies.items() if v.get() > 0 }
        else:
            currencies = self._currencies

        if ascending:
            return dict(sorted(currencies.items(), key=lambda item: item[1]))
        return currencies

    def try_convert_currency(self, name: str) -> bool:
        """
        Attempts to convert the provided currency name to currencies of lower value.
        Returns True if the currency was converted, otherwise retuens false.

        :param name: Name of the currency to be converted.
        :rtype bool:
        """
        if name ==  CURRENCY_NAME.COINS:
            return False

        currency = self._currencies[name]
        if currency.get() < 1:
            return False

        currency_amount = currency.calc_value
        for current_name, currency_type in self._currencies.items():
            if name == current_name:
                continue
            if currency_type.calc_value >= currency_amount:
                continue

            add_amount, remainder = divmod(currency_amount, currency_type.calc_value)
            self.add_to_wallet({ current_name: add_amount})
            currency_amount = remainder

            if remainder == 0:
                break

        self.remove_from_wallet({ name: 1})
        return True
