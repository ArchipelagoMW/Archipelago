""" Module providing LMClient with EnergyLink integration operations. """

import asyncio
from CommonClient import CommonContext, logger
from ...Wallet import Wallet
from .energy_link import EnergyLink, RequestStatus

class _ResponseArgs:
    ORIGINAL_VALUE = "original_value"
    VALUE = "value"
    TAG = "tag"
    KEY = "key"

class EnergyLinkClient:
    """
    Service which allows clients interact with energy link responses.
    """
    _energy_link: EnergyLink
    _ctx: CommonContext
    _wallet: Wallet

    _current_currency_amount: dict[str, int]

    def __init__(self, ctx: CommonContext, wallet: Wallet):
        self._ctx = ctx
        self._energy_link = EnergyLink(ctx)
        self._wallet = wallet
        self._current_currency_amount = {}

    async def send_energy_to_pool(self, delay_in_seconds: int = 5, wait_timer_in_seconds: int = 5):
        """
        Sends energy to pool on a timer when possible.

        :param delay_in_seconds: The amount loops to cache energy before sending it to the server to be stored as energy.
        :param wait_timer_in_seconds: The duration between energy caching in seconds.
        """
        amount_to_send = 0
        while delay_in_seconds >= 5:
            delay_in_seconds -= 1
            amount_to_send += self._get_currency_updates()
            await asyncio.sleep(wait_timer_in_seconds)

        if amount_to_send > 0:
            logger.info("Sending %s energy to pool.", amount_to_send)
            await self._energy_link.send_energy_async(amount_to_send)

    def _get_currency_updates(self, percentage: float = 0.25) -> int:
        """
        Pulls an amount of currency from the wallet to be stored in the team's EnergyLink pool.
        The amount pulled is based upon the difference of currencies multiplied by a percentage to be stored.

        :param percentage: The percent of currency to be send to the EnergyLink pool.
        """
        if len(self._current_currency_amount) == 0:
            for currency_name, currency in self._wallet.get_currencies().items():
                self._current_currency_amount.update({ currency_name: currency.calculate_worth() })
            return 0

        amount_to_be_sent_to_energy_link = 0
        for currency_name, currency in self._wallet.get_currencies().items():
            twmp_worth = 0
            if currency_name in self._current_currency_amount:
                twmp_worth = self._current_currency_amount[currency_name]
            current_amount = currency.calculate_worth()

            self._current_currency_amount.update({ currency_name: current_amount })
            current_diff = _calc_currency_difference(twmp_worth, current_amount, percentage)

            if current_diff > 0:
                amount_to_be_sent_to_energy_link += current_diff

        calculated_amount = int(amount_to_be_sent_to_energy_link / self._wallet.get_calculated_amount_worth(1))
        raise Exception("wallet.remove_amount_from_wallet function has been removed and this function should not be run.")
        try:
            self._wallet.remove_amount_from_wallet(calculated_amount)
        except ArithmeticError:
            calculated_amount = 0

        return calculated_amount

    def try_update_energy_request(self, args: dict[str, str]) -> bool:
        """
        Checks args for a matching EnergyLink key and a 'tag' attribute in the given. 
        If there's a match we iterate through the EnergyLink requests looking for a matching tag.
        If a matching tag is found we update the request object with the actual amount received from the server and setting the status to COMPLETED.

        :param args: Dict of parameters used to determine if a EnergyLink request was fufilled.
        """
        if args[_ResponseArgs.KEY] is not self._energy_link.get_ap_key() and _ResponseArgs.TAG not in args:
            return False

        request = self._energy_link.energy_requests.pop(args[_ResponseArgs.TAG], None)
        if request is None:
            return False

        if request.status != RequestStatus.REQUESTED:
            return False

        request.received_amount = args[_ResponseArgs.ORIGINAL_VALUE] - args[_ResponseArgs.VALUE]
        _get_currencies_to_be_added(self._wallet, request.received_amount)

        request.status = RequestStatus.COMPLETED
        return True

def _calc_currency_difference(previous_amount: int, amount: int, percentage: float = 0.25) -> int:
    temp_amount = amount - previous_amount
    return int(temp_amount * percentage)

def _get_currencies_to_be_added(wallet: Wallet, amount_to_add: int):
    currencies_to_add = _add_currencies(wallet, amount_to_add)
    wallet.add_to_wallet(currencies_to_add)

def _add_currencies(wallet: Wallet, amount_to_receive: int) -> dict[str, int]:
    new_amount = amount_to_receive
    currencies_to_add: dict[str, int] = {}

    for currency_name, currency_type in wallet.get_currencies().items():
        # If we added the entire amount we want to stop trying to add new currencies.
        if new_amount == 0:
            break

        currency_to_add, remainder = divmod(new_amount, currency_type.calc_value)
        new_amount = remainder

        # If we don't have any amount of a given currency to add we want to skip updating.
        if currency_to_add <= 0:
            continue

        currencies_to_add.update({ currency_name: int(currency_to_add) })

    return currencies_to_add
