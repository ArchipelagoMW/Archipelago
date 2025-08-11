""" Module which performs NetworkProtocol operations for the EnergyLink integration. """

from CommonClient import CommonContext
from ..network_engine import ArchipelagoRequest, RequestStatus, ArchipelagoNetworkEngine, SetNetworkRequest, GetNetworkRequest

class EnergyLinkConstants:
    """
    Constants for internal and public facing energy link names.
    """
    FRIENDLY_NAME = "EnergyLink"
    INTERNAL_NAME = "energy_link"

class EnergyRequest(ArchipelagoRequest):
    """
    Object representation of an energy link request.
    """
    request_amount: int
    received_amount: int

    def __init__(self, amount: int):
        self.request_amount = amount
        self.received_amount: int = 0
        super().__init__()

class EnergyLink:
    """
    EnergyLink service for interactions between Luigi's Mansion and Archipelago.

    Requests/Sends 'energy' to the team's energy pool to be used as needed.
    """
    _ctx: CommonContext

    energy_requests: dict[str, EnergyRequest] = {}
    network_engine: ArchipelagoNetworkEngine

    def __init__(self, ctx: CommonContext):
        self.network_engine = ArchipelagoNetworkEngine(ctx)
        self._ctx = ctx

    async def request_energy_async(self, amount: int) -> EnergyRequest:
        """
        Requests energy for use from the Archipelago server.

        :param amount: The amount of energy to be added to Luigi's wallet. 
        The actual amount may vary due to the async nature of the call.
        """
        current_ctx = self._ctx
        if not _validate_energy_request(current_ctx.tags, amount):
            raise AttributeError("Could not validate arguments for given request.")

        request = EnergyRequest(amount)
        await self.network_engine.send_set_request_async(
            SetNetworkRequest(
                tag= f"{request.uuid}",
                key= self.get_ap_key(),
                want_reply= True,
                default= 0,
                operations= [
                    { "operation": "add", "value": (request.request_amount * -1) },
                    { "operation": "max", "value": 0 },
                ]
            )
        )

        request.status = RequestStatus.REQUESTED
        self.energy_requests.update({ request.uuid: request })
        return request

    async def send_energy_async(self, amount: int) -> EnergyRequest:
        """
        Sends energy to Archipelago server for other slots to consume.

        :param amount: The amount of energy to be removed from Luigi's wallet.
        """

        current_ctx = self._ctx
        if not _validate_energy_request(current_ctx.tags, amount):
            raise AttributeError("Could not validate arguments for given request.")

        request = EnergyRequest(amount)
        network_request = SetNetworkRequest(
            tag= request.uuid,
            key= self.get_ap_key(),
            default= 0,
            want_reply=False,
            operations= [
                { "operation": "add", "value": amount },
            ]
        )

        await self.network_engine.send_set_request_async(network_request)

        request.status = RequestStatus.REQUESTED
        self.energy_requests.update({ request.uuid: request })
        return request

    async def get_energy_async(self):
        """
        Gets the available amount of energy from the team's pool.
        """
        network_request = GetNetworkRequest(
            tag="",
            keys= [ self.get_ap_key(), ]
        )

        await self.network_engine.send_get_request_async(network_request)

    def get_ap_key(self) -> str:
        """
        Gets the energy link team identifier.
        """
        return f"{EnergyLinkConstants.FRIENDLY_NAME}{self._ctx.team}"

def _validate_energy_request(tags: set, amount: int) -> bool:
    """
    Determines if the request is valid before sending it to Archipelago.

    :param self: The client context making the request to the server.
    :param amount: The amount to be verified before sending the request.
    """
    try:
        amount_as_int = int(amount)
    except ValueError:
        return False
    if amount_as_int <= 0:
        return False
    if not EnergyLinkConstants.FRIENDLY_NAME in tags:
        return False
    return True
