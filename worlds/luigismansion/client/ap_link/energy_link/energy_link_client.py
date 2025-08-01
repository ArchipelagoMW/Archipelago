""" Module providing LMClient with EnergyLink integration operations. """

from CommonClient import CommonContext
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

    _current_currency_amount: dict[str, int] = {}

    def __init__(self, ctx: CommonContext, wallet: Wallet):
        self._ctx = ctx
        self._energy_link = EnergyLink(ctx)
        self._wallet = wallet

    async def get_currency_updates(self) -> int:
        amount_to_be_sent_to_energy_link = 0
        for currency_name, currency in self._wallet.get_currencies().items():
            temp_amount = 0
            if currency_name in self._current_currency_amount:
                temp_amount = self._current_currency_amount[currency_name]
            current_amount = currency.get()

            self._current_currency_amount.update({ currency_name: current_amount })
            if temp_amount == 0:
                continue

            current_diff = _calc_currency_difference(temp_amount, current_amount, percentage=1) * currency.calc_value

            if current_diff > 0:
                amount_to_be_sent_to_energy_link += current_diff
                self._wallet.remove_from_wallet({ currency_name:amount_to_be_sent_to_energy_link })

        return int(amount_to_be_sent_to_energy_link / self._wallet.get_calculated_amount_worth(1))

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
        self._wallet.add_amount_to_wallet(request.received_amount)

        request.status = RequestStatus.COMPLETED
        return True

def _calc_currency_difference(previous_amount: int, amount: int, percentage: float = 0.25) -> int:
    temp_amount = amount - previous_amount
    return int(temp_amount * percentage)