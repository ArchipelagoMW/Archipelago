import asyncio
import enum
import sys
from typing import Sequence

from .broker import CLIENT_PORT
from .enums import RequestType
from .requests import Request, NoOpRequest, ReadRequest, WriteRequest, GuardRequest, PlatformRequest, GameIdRequest, MemorySizeRequest, LockRequest, UnlockRequest, DisplayMessageRequest, SupportedOperationsRequest
from .responses import AutoResponseRegister, Response, ReadResponse, WriteResponse, GuardResponse, PlatformResponse, GameIdResponse, MemorySizeResponse, LockResponse, UnlockResponse, DisplayMessageResponse, SupportedOperationsResponse


class ConnectionStatus(enum.IntEnum):
    NOT_CONNECTED = 1
    TENTATIVE = 2
    CONNECTED = 3


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
        message = bytes([self.selected_device_id]) + message

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
    try:
        ctx.streams = await asyncio.open_connection("127.0.0.1", CLIENT_PORT)
        ctx.connection_status = ConnectionStatus.TENTATIVE
        return True
    except (TimeoutError, ConnectionRefusedError):
        ctx.streams = None
        ctx.connection_status = ConnectionStatus.NOT_CONNECTED
        return False


def disconnect(ctx: PolyEmuContext) -> None:
    ctx._disconnect()


async def get_script_version(ctx: PolyEmuContext) -> int:
    return 1


async def send_requests(ctx: PolyEmuContext, request_list: list[Request]) -> list[Response]:
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
    await send_requests(ctx, [NoOpRequest()])


async def get_game_id(ctx: PolyEmuContext) -> bytes:
    res: GameIdResponse = (await send_requests(ctx, [GameIdRequest()]))[0]
    return res.game_id


async def get_memory_size(ctx: PolyEmuContext) -> dict[int, int]:
    res: MemorySizeResponse = (await send_requests(ctx, [MemorySizeRequest()]))[0]
    return res.memory_sizes


async def get_platform(ctx: PolyEmuContext) -> str:
    res: PlatformResponse = (await send_requests(ctx, [PlatformRequest()]))[0]
    return res.platform_id


async def get_supported_operations(ctx: PolyEmuContext) -> list[int]:
    res: SupportedOperationsResponse = (await send_requests(ctx, [SupportedOperationsRequest()]))[0]
    return res.supported_operations[:]


async def guarded_read(ctx: PolyEmuContext, read_list: Sequence[tuple[int, int, int]],
                       guard_list: Sequence[tuple[int, Sequence[int], int]]) -> list[bytes] | None:
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
    return await guarded_read(ctx, read_list, [])


async def guarded_write(ctx: PolyEmuContext, write_list: Sequence[tuple[int, Sequence[int], int]],
                        guard_list: Sequence[tuple[int, Sequence[int], int]]) -> bool:
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
    await guarded_write(ctx, write_list, [])


async def lock(ctx: PolyEmuContext) -> None:
    res: LockResponse = (await send_requests(ctx, [LockRequest()]))[0]


async def unlock(ctx: PolyEmuContext) -> None:
    res: UnlockResponse = (await send_requests(ctx, [UnlockRequest()]))[0]


async def display_message(ctx: PolyEmuContext, message: str) -> None:
    res: DisplayMessageResponse = (await send_requests(ctx, [DisplayMessageRequest(message)]))[0]
