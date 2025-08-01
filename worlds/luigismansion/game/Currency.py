import dolphin_memory_engine as dme

# This address will start the point to Luigi's inventory to get his wallet to calculate rank.
_WALLET_START_ADDR = 0x803D8B7C

class CURRENCY_NAME:
    COINS = "coin"
    BILLS = "bill"
    GOLD_BARS = "gold"
    SAPPHIRE = "sapphire"
    EMERALD = "emerald"
    RUBY = "ruby"
    DIAMOND = "diamond"
    GOLD_DIAMOND = "rdiamond"
    SMALL_PEARL = "spearl"
    MEDIUM_PEARL = "mpearl"
    LARGE_PEARL = "lpearl"

class Currency:
    """Memory representation of type and worth of currency Luigi can obtain."""
    def __init__(self, name: str, mem_loc: str,  calc_value: int):
        """
        Default ctor for a currency type.

        :param name: Friendly name of the given currency.
        :param mem_loc: Memory location of a given wallet type.
        :param calc_value: Value of the wallet type when checking randomizer 'rank_requirement'.
        """
        self.name = name
        self.mem_loc = mem_loc
        self.calc_value = calc_value
    
    def __str__(self):
        return self.name

    def add(self, amount: int):
        """
        Adds an amount of currency based upon the currency_type.

        :param currency_type: The memory location for the currency type to be added.
        :param amount: The amount of currency to be added based upon the currency_type.
        """
        current_currency = self.get()
        dme.write_word(dme.follow_pointers(_WALLET_START_ADDR, [self.mem_loc]), (current_currency + amount))

    def get(self) -> int:
        """
        Gets the current currency value based upon the currency_type.

        :param currency_type: The memory location for the currency type to be retreived.
        :return: Returns the current amount of the given currency in Luigi's wallet.
        :rtype: int
        """
        return dme.read_word(dme.follow_pointers(_WALLET_START_ADDR, [self.mem_loc]))
    
    def remove(self, amount: int) -> bool:
        """
        Removes an amount of currency based upon the currency_type.

        :param currency_type: The memory location for the currency type to be removed.
        :param amount: The amount of currency to be added based upon the currency_type.
        :return: If the amount was removed from the wallet True is returned, otherwise False.
        :rtype: bool
        """
        current_currency = self.get()

        if amount <= current_currency:
            dme.write_word(dme.follow_pointers(_WALLET_START_ADDR, [self.mem_loc]), (current_currency - amount))
            return True
        return False

    def calculate_worth(self) -> int:
        """
        Gets the value of the currency type when calculating 'rank_requirement'.

        :return: Returns the worth of the given currency in Luigi's wallet.
        :rtype: int
        """
        return self.get() * self.calc_value

CURRENCIES: dict[str, Currency] = {
    CURRENCY_NAME.COINS: Currency(CURRENCY_NAME.COINS, 0x324, 5000),
    CURRENCY_NAME.BILLS: Currency(CURRENCY_NAME.BILLS, 0x328, 20000),
    CURRENCY_NAME.GOLD_BARS: Currency(CURRENCY_NAME.GOLD_BARS, 0x32C, 100000),
    CURRENCY_NAME.SAPPHIRE: Currency(CURRENCY_NAME.SAPPHIRE, 0x330, 500000),
    CURRENCY_NAME.EMERALD: Currency(CURRENCY_NAME.EMERALD, 0x334, 800000),
    CURRENCY_NAME.RUBY: Currency(CURRENCY_NAME.RUBY, 0x338, 1000000),
    CURRENCY_NAME.DIAMOND: Currency(CURRENCY_NAME.DIAMOND, 0x33C, 2000000),
    CURRENCY_NAME.GOLD_DIAMOND: Currency(CURRENCY_NAME.GOLD_DIAMOND, 0x344, 20000000),
    CURRENCY_NAME.SMALL_PEARL: Currency(CURRENCY_NAME.SMALL_PEARL, 0x348, 50000),
    CURRENCY_NAME.MEDIUM_PEARL: Currency(CURRENCY_NAME.MEDIUM_PEARL, 0x34C, 100000),
    CURRENCY_NAME.LARGE_PEARL: Currency(CURRENCY_NAME.LARGE_PEARL, 0x350, 1000000),
}