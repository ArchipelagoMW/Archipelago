"""
A module for interacting with BizHawk through `connector_bizhawk_generic.lua`.

Any mention of `domain` in this module refers to the names BizHawk gives to memory domains in its own lua api. They are
naively passed to BizHawk without validation or modification.
"""
from __future__ import annotations

import abc
import asyncio
import enum
import struct
import sys
from typing import Any, ClassVar, Self, Sequence, Type  # Self py 3.11+

from .broker import CLIENT_PORT
from .enums import PLATFORMS, PlatformEnum, OperationEnum


class ConnectionStatus(enum.IntEnum):
    NOT_CONNECTED = 1
    TENTATIVE = 2
    CONNECTED = 3


class Request(abc.ABC):
    type: OperationEnum

    @abc.abstractmethod
    def _get_body(self) -> bytes:
        ...

    def to_bytes(self) -> bytes:
        return struct.pack(">B", self.type) + self._get_body()


class NoOpRequest(Request):
    type = OperationEnum.NO_OP

    def _get_body(self):
        return b""


class ReadRequest(Request):
    type = OperationEnum.READ

    domain_id: int
    address: int
    size: int

    def __init__(self, domain_id: int, address: int, size: int):
        super().__init__()
        self.domain_id = domain_id
        self.address = address
        self.size = size

    def _get_body(self):
        return struct.pack(">B", self.domain_id) + \
            struct.pack(">Q", self.address) + \
            struct.pack(">H", self.size)


class WriteRequest(Request):
    type = OperationEnum.WRITE

    domain_id: int
    address: int
    data: bytes

    def __init__(self, domain_id: int, address: int, data: Sequence[int]):
        super().__init__()
        self.domain_id = domain_id
        self.address = address
        self.data = bytes(data)

    def _get_body(self):
        return struct.pack(">B", self.domain_id) + \
            struct.pack(">Q", self.address) + \
            struct.pack(">H", len(self.data)) + \
            self.data


class GuardRequest(Request):
    type = OperationEnum.GUARD

    domain_id: int
    address: int
    expected_data: bytes

    def __init__(self, domain_id: int, address: int, expected_data: Sequence[int]):
        super().__init__()
        self.domain_id = domain_id
        self.address = address
        self.expected_data = bytes(expected_data)

    def _get_body(self):
        return struct.pack(">B", self.domain_id) + \
            struct.pack(">Q", self.address) + \
            struct.pack(">H", len(self.expected_data)) + \
            self.expected_data


class PlatformRequest(Request):
    type = OperationEnum.PLATFORM

    def _get_body(self):
        return b""


class AutoResponseRegister(abc.ABCMeta):
    response_types: ClassVar[dict[int, Response]] = {}

    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> AutoResponseRegister:
        new_class = super().__new__(cls, name, bases, namespace)

        # Register response type
        if "type" in namespace:
            AutoResponseRegister.response_types[namespace["type"]] = new_class

        return new_class

    @staticmethod
    def get_response_type(code: int) -> Type[Response]:
        try:
            return AutoResponseRegister.response_types[code]
        except KeyError:
            raise KeyError(f"Response code [{hex(code)}] does not have a corresponding response type")

    @staticmethod
    def convert_message_chain(msg: bytes) -> list[Response]:
        responses: list[Response] = []
        while len(msg) > 0:
            response, msg = AutoResponseRegister.get_response_type(msg[0]).consume_from_message(msg)
            responses.append(response)
        return responses


class Response(abc.ABC, metaclass=AutoResponseRegister):
    type: ClassVar[int]

    @staticmethod
    @abc.abstractmethod
    def consume_from_message(msg: bytes) -> tuple[Self, bytes]:
        ...


class PingResponse(Response):
    type = 0x80

    @staticmethod
    def consume_from_message(msg) -> tuple[PingResponse, bytes]:
        assert msg[0] == PingResponse.type
        return (PingResponse(), msg[1:])


class ReadResponse(Response):
    type = 0x81

    data: bytes

    def __init__(self, data: bytes):
        self.data = data

    @staticmethod
    def consume_from_message(msg) -> tuple[ReadResponse, bytes]:
        assert msg[0] == ReadResponse.type

        data_size = int.from_bytes(msg[1:3], "big")
        return (ReadResponse(msg[3:data_size + 3]), msg[data_size + 3:])


class WriteResponse(Response):
    type = 0x82

    @staticmethod
    def consume_from_message(msg) -> tuple[WriteResponse, bytes]:
        assert msg[0] == WriteResponse.type
        return (WriteResponse(), msg[1:])


class GuardResponse(Response):
    type = 0x83

    validated: bool

    def __init__(self, validated: bool):
        self.validated = validated

    @staticmethod
    def consume_from_message(msg) -> tuple[GuardResponse, bytes]:
        assert msg[0] == GuardResponse.type
        return (GuardResponse(msg[1] != 0), msg[2:])


class PlatformResponse(Response):
    type = 0x86

    platform_id: PlatformEnum

    def __init__(self, platform_id: int):
        self.platform_id = PLATFORMS.get_by_id(platform_id)

    @staticmethod
    def consume_from_message(msg) -> tuple[PlatformResponse, bytes]:
        assert msg[0] == PlatformResponse.type
        return (PlatformResponse(msg[1]), msg[2:])


class ErrorResponse(Response):
    type = 0xFF

    error_code: int
    error_context: bytes

    def __init__(self, code: int, context: bytes):
        self.error_code = code
        self.error_context = context

    @staticmethod
    def consume_from_message(msg) -> tuple[ErrorResponse, bytes]:
        assert msg[0] == ErrorResponse.type

        context_size = int.from_bytes(msg[2:4], "big")
        return (ErrorResponse(msg[1], msg[4:context_size + 4]), msg[context_size + 4:])


class NotConnectedError(Exception):
    """Raised when something tries to make a request to the connector script before a connection has been established"""
    pass


class RequestFailedError(Exception):
    """Raised when the connector script did not respond to a request"""
    pass


class ConnectorError(Exception):
    """Raised when the connector script encounters an error while processing a request"""
    pass


class SyncError(Exception):
    """Raised when the connector script responded with a mismatched response type"""
    pass


class PolyEmuContext:
    streams: tuple[asyncio.StreamReader, asyncio.StreamWriter] | None
    connection_status: ConnectionStatus
    selected_device_id: int | None
    _lock: asyncio.Lock

    def __init__(self) -> None:
        self.streams = None
        self.connection_status = ConnectionStatus.NOT_CONNECTED
        self.selected_device_id = 12
        self._lock = asyncio.Lock()

    def _disconnect(self):
        if self.streams is not None:
            self.streams[1].close()
            self.streams = None
        self.connection_status = ConnectionStatus.NOT_CONNECTED

    async def _send_message(self, message: bytes):
        # Attach header
        message = bytearray([self.selected_device_id]) + message

        # Prepend message size
        message = len(message).to_bytes(2, "big") + message

        async with self._lock:
            if self.streams is None:
                raise NotConnectedError("You tried to send a request before a connection to the emulator was made")

            try:
                reader, writer = self.streams
                writer.write(message)
                await asyncio.wait_for(writer.drain(), timeout=5)

                response_size = await asyncio.wait_for(reader.read(2), timeout=5)
                if response_size == b"":
                    self._disconnect()
                    raise RequestFailedError("Connection closed")

                data = await asyncio.wait_for(reader.read(int.from_bytes(response_size, "big")), timeout=5)
                if data == b"":
                    self._disconnect()
                    raise RequestFailedError("Connection closed")

                if self.connection_status == ConnectionStatus.TENTATIVE:
                    self.connection_status = ConnectionStatus.CONNECTED

                return data
            except asyncio.TimeoutError as exc:
                self._disconnect()
                raise RequestFailedError("Connection timed out") from exc
            except ConnectionResetError as exc:
                self._disconnect()
                raise RequestFailedError("Connection reset") from exc


async def connect(ctx: PolyEmuContext) -> bool:
    """Attempts to establish a connection with a connector script. Returns True if successful."""
    try:
        ctx.streams = await asyncio.open_connection("127.0.0.1", CLIENT_PORT)
        ctx.connection_status = ConnectionStatus.TENTATIVE
        return True
    except (TimeoutError, ConnectionRefusedError):
        ctx.streams = None
        ctx.connection_status = ConnectionStatus.NOT_CONNECTED
        return False


def disconnect(ctx: PolyEmuContext) -> None:
    """Closes the connection to the connector script."""
    ctx._disconnect()


async def get_script_version(ctx: PolyEmuContext) -> int:
    return 1


async def send_requests(ctx: PolyEmuContext, request_list: list[Request]) -> list[Response]:
    """Sends a list of requests to the Emulator and returns their responses.

    It's likely you want to use the wrapper functions instead of this."""
    message = bytes()
    for request in request_list:
        message += request.to_bytes()

    responses = AutoResponseRegister.convert_message_chain(await ctx._send_message(message))

    errors: list[Exception] = []

    for response in responses:
        if response.type == 0xFF:
            errors.append(RequestFailedError(response.error_context))
            # if response.error_code == 0x01:
            #     errors.append(NotConnectedError(response.error_context))
            # else:
            #     errors.append(ConnectorError(response.error_context))

    if errors:
        if sys.version_info >= (3, 11, 0):
            raise ExceptionGroup("Connector script returned errors", errors)  # noqa
        else:
            raise errors[0]

    return responses


async def ping(ctx: PolyEmuContext) -> None:
    """Sends a PING request and receives a PONG response."""
    await send_requests(ctx, [NoOpRequest()])


# async def get_game_id(ctx: PolyEmuContext) -> bytes:
#     """Gets the hash value of the currently loaded ROM"""
#     res = await send_requests(ctx, [b"\x00"])

#     # if res["type"] != "HASH_RESPONSE":
#     #     raise SyncError(f"Expected response of type HASH_RESPONSE but got {res['type']}")

#     return res["value"]


# async def get_memory_size(ctx: BizHawkContext, domain: str) -> int:
#     """Gets the size in bytes of the specified memory domain"""
#     res = (await send_requests(ctx, [{"type": "MEMORY_SIZE", "domain": domain}]))[0]

#     if res["type"] != "MEMORY_SIZE_RESPONSE":
#         raise SyncError(f"Expected response of type MEMORY_SIZE_RESPONSE but got {res['type']}")

#     return res["value"]


async def get_platform(ctx: PolyEmuContext) -> str:
    """Gets the platform for the currently loaded ROM"""
    res: PlatformResponse = (await send_requests(ctx, [PlatformRequest()]))[0]
    return res.platform_id


# async def get_cores(ctx: BizHawkContext) -> dict[str, str]:
#     """Gets the preferred cores for systems with multiple cores. Only systems with multiple available cores have
#     entries."""
#     res = (await send_requests(ctx, [{"type": "PREFERRED_CORES"}]))[0]

#     if res["type"] != "PREFERRED_CORES_RESPONSE":
#         raise SyncError(f"Expected response of type PREFERRED_CORES_RESPONSE but got {res['type']}")

#     return res["value"]


# async def lock(ctx: BizHawkContext) -> None:
#     """Locks BizHawk in anticipation of receiving more requests this frame.

#     Consider using guarded reads and writes instead of locks if possible.

#     While locked, emulation will halt and the connector will block on incoming requests until an `UNLOCK` request is
#     sent. Remember to unlock when you're done, or the emulator will appear to freeze.

#     Sending multiple lock commands is the same as sending one."""
#     res = (await send_requests(ctx, [{"type": "LOCK"}]))[0]

#     if res["type"] != "LOCKED":
#         raise SyncError(f"Expected response of type LOCKED but got {res['type']}")


# async def unlock(ctx: BizHawkContext) -> None:
#     """Unlocks BizHawk to allow it to resume emulation. See `lock` for more info.

#     Sending multiple unlock commands is the same as sending one."""
#     res = (await send_requests(ctx, [{"type": "UNLOCK"}]))[0]

#     if res["type"] != "UNLOCKED":
#         raise SyncError(f"Expected response of type UNLOCKED but got {res['type']}")


# async def display_message(ctx: BizHawkContext, message: str) -> None:
#     """Displays the provided message in BizHawk's message queue."""
#     res = (await send_requests(ctx, [{"type": "DISPLAY_MESSAGE", "message": message}]))[0]

#     if res["type"] != "DISPLAY_MESSAGE_RESPONSE":
#         raise SyncError(f"Expected response of type DISPLAY_MESSAGE_RESPONSE but got {res['type']}")


# async def set_message_interval(ctx: BizHawkContext, value: float) -> None:
#     """Sets the minimum amount of time in seconds to wait between queued messages. The default value of 0 will allow one
#     new message to display per frame."""
#     res = (await send_requests(ctx, [{"type": "SET_MESSAGE_INTERVAL", "value": value}]))[0]

#     if res["type"] != "SET_MESSAGE_INTERVAL_RESPONSE":
#         raise SyncError(f"Expected response of type SET_MESSAGE_INTERVAL_RESPONSE but got {res['type']}")


async def guarded_read(ctx: PolyEmuContext, read_list: Sequence[tuple[int, int, int]],
                       guard_list: Sequence[tuple[int, Sequence[int], int]]) -> list[bytes] | None:
    """Reads an array of bytes at 1 or more addresses if and only if every byte in guard_list matches its expected
    value.

    Items in read_list should be organized (address, size, domain) where
    - `address` is the address of the first byte of data
    - `size` is the number of bytes to read
    - `domain` is the name of the region of memory the address corresponds to

    Items in `guard_list` should be organized `(address, expected_data, domain)` where
    - `address` is the address of the first byte of data
    - `expected_data` is the bytes that the data starting at this address is expected to match
    - `domain` is the name of the region of memory the address corresponds to

    Returns None if any item in guard_list failed to validate. Otherwise returns a list of bytes in the order they
    were requested."""
    guards = [GuardRequest(domain, address, expected_data) for address, expected_data, domain in guard_list]
    reads = [ReadRequest(domain, address, size) for address, size, domain in read_list]

    responses = await send_requests(ctx, guards + reads)
    guard_responses: list[GuardResponse] = responses[:len(guards)]
    read_responses: list[ReadResponse | GuardResponse] = responses[len(guards):]

    for res in guard_responses:
        if not res.validated:
            return None

    return [res.data for res in read_responses]


async def read(ctx: PolyEmuContext, read_list: Sequence[tuple[int, int, str]]) -> list[bytes]:
    """Reads data at 1 or more addresses.

    Items in `read_list` should be organized `(address, size, domain)` where
    - `address` is the address of the first byte of data
    - `size` is the number of bytes to read
    - `domain` is the name of the region of memory the address corresponds to

    Returns a list of bytes in the order they were requested."""
    return await guarded_read(ctx, read_list, [])


async def guarded_write(ctx: PolyEmuContext, write_list: Sequence[tuple[int, Sequence[int], int]],
                        guard_list: Sequence[tuple[int, Sequence[int], int]]) -> bool:
    """Writes data to 1 or more addresses if and only if every byte in guard_list matches its expected value.

    Items in `write_list` should be organized `(address, value, domain)` where
    - `address` is the address of the first byte of data
    - `value` is a list of bytes to write, in order, starting at `address`
    - `domain` is the name of the region of memory the address corresponds to

    Items in `guard_list` should be organized `(address, expected_data, domain)` where
    - `address` is the address of the first byte of data
    - `expected_data` is the bytes that the data starting at this address is expected to match
    - `domain` is the name of the region of memory the address corresponds to

    Returns False if any item in guard_list failed to validate. Otherwise returns True."""
    guards = [GuardRequest(domain, address, expected_data) for address, expected_data, domain in guard_list]
    writes = [WriteRequest(domain, address, data) for address, data, domain in write_list]

    responses = await send_requests(ctx, guards + writes)
    guard_responses: list[GuardResponse] = responses[:len(guards)]
    write_responses: list[WriteResponse | GuardResponse] = responses[len(guards):]

    for res in guard_responses:
        if not res.validated:
            return False

    return True


async def write(ctx: PolyEmuContext, write_list: Sequence[tuple[int, Sequence[int], int]]) -> None:
    """Writes data to 1 or more addresses.

    Items in write_list should be organized `(address, value, domain)` where
    - `address` is the address of the first byte of data
    - `value` is a list of bytes to write, in order, starting at `address`
    - `domain` is the name of the region of memory the address corresponds to"""
    await guarded_write(ctx, write_list, [])
