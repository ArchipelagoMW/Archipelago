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

    def __init__(self, ctx: CommonContext, wallet: Wallet):
        self._ctx = ctx
        self._energy_link = EnergyLink(ctx)
        self._wallet = wallet

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
