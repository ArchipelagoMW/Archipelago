""" Module providing type representation of the Archipelago NetworkProtocol """

import uuid
import abc

from typing import NamedTuple, Optional, Any
from enum import Enum
from CommonClient import CommonContext

class RequestStatus(Enum):
    """ Archipelago client -> server request statuses. """
    UNKNOWN = 0
    """ Used during initialization. """
    REQUESTED = 1
    """ Indicates that a request was made to Archipelago. """
    RECEIVED = 2
    """ Indicates that a response from the initial response was received and ready for processing. """
    COMPLETED = 3
    """ Indicates that the request was processed to completion. """

class ArchipelagoRequest:
    """ Base level request object for clients to interact with the Archipelago DataStorage. """
    uuid: str
    status: RequestStatus

    def __init__(self):
        self.uuid = str(uuid.uuid4())
        self.status = RequestStatus.UNKNOWN

    def __eq__(self, other):
        if isinstance(other, ArchipelagoRequest):
            return self.uuid == other.uuid
        return False

class NetworkRequest(NamedTuple):
    """
    Object representation of Archipelago's NetworkProtocol Client--> Server DataStorage operations.

    more information can be found at: 
        https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/network%20protocol.md#client---server
    """
    command: str
    tag: str

    @abc.abstractmethod
    def create_request(self) -> dict[str, Any]:
        """ Creates a dict[str, Any] of the object to be used in 'CommonContext.send_msgs()'. """
        return

class SetNetworkRequest(NetworkRequest):
    """ Object representation of the 'Set'command in Archipelago's NetworkProtocol. """
    operations: dict[str, Any]
    key: str
    default: Optional[Any]
    want_reply: bool

    def __new__(cls, tag, key, want_reply, default, operations):
        instance = super().__new__(cls, "Set", tag)
        instance.operations = operations
        instance.key = key
        instance.default = default
        instance.want_reply = want_reply

        return instance

    def create_request(self) -> dict[str, Any]:
        request = {
            "cmd": self.command,
            "tag": self.tag,
            "key": self.key,
            "operations": self.operations,
        }

        if self.want_reply is not None:
            request.update({ "want_reply": self.want_reply })

        if self.default is not None:
            request.update({ "default": self.default })

        return request

class GetNetworkRequest(NetworkRequest):
    """ Object representation of the 'Get'command in Archipelago's NetworkProtocol. """
    keys: list[str]

    def __new__(cls, tag, keys):
        instance = super().__new__(cls, "Get", tag)
        instance.keys = keys
        return instance

    def create_request(self) -> dict[str, Any]:
        request = {
            "cmd": self.command,
            "tag": self.tag,
            "keys": self.keys,
        }

        return request

class ArchipelagoNetworkEngine:
    """
    Archipelago's Client to Server NetworkProtocol which utilizes
    typing instead of manual request construction.
    """
    _ctx: CommonContext

    def __init__(self, ctx: CommonContext):
        self._ctx = ctx

    async def send_set_request_async(self, network_request: SetNetworkRequest):
        """ Sends a 'Set' command to the Archipelago server. """
        return await self._send_network_request_async(network_request)

    async def send_get_request_async(self, network_request: GetNetworkRequest):
        """ Sends a 'Get' command to the Archipelago server. """
        return await self._send_network_request_async(network_request)

    async def _send_network_request_async(self, request: NetworkRequest):
        await self._ctx.send_msgs([ request.create_request() ])
