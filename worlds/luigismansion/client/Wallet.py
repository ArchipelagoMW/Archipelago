from ..game.Currency import Currency, CURRENCIES

# Rank Requirements for each rank. H, G, F, E, D, C, B, A
_RANK_REQ_AMTS = [0, 5000000, 20000000, 40000000, 50000000, 60000000, 70000000, 100000000]

class Wallet:
    """Manages Luigi's currencies including adding/removing currencies during a run. It also manages the randomizer check 'rank_requirement'."""

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
        
        :param currencies: Collection of key value pairs, where the key is the name of the currency and the value is the amount to be added.
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
        return _RANK_REQ_AMTS[self.rank_requirement]
