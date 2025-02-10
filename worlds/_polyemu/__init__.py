import abc
import asyncio
import sys
from typing import Sequence

from .broker import CLIENT_PORT
from .enums import BROKER_DEVICE_ID, PolyEmuResponseType
from .errors import AutoPolyEmuErrorRegister, PolyEmuError, NotConnectedError, ConnectionLostError
from .requests import PolyEmuRequest, NoOpRequest, ReadRequest, WriteRequest, GuardRequest, PlatformRequest, ListDevicesRequest, MemorySizeRequest, LockRequest, UnlockRequest, DisplayMessageRequest, SupportedOperationsRequest
from .responses import AutoPolyEmuResponseRegister, PolyEmuResponse, ReadResponse, WriteResponse, GuardResponse, PlatformResponse, ListDevicesResponse, MemorySizeResponse, LockResponse, UnlockResponse, DisplayMessageResponse, SupportedOperationsResponse, ErrorResponse


class PolyEmuConnector(abc.ABC):
    @abc.abstractmethod
    def is_connected(self) -> bool:
        ...

    @abc.abstractmethod
    async def connect(self) -> bool:
        ...

    @abc.abstractmethod
    async def disconnect(self) -> None:
        ...

    @abc.abstractmethod
    async def send_message(self, message: bytes) -> bytes:
        ...


class PolyEmuBrokerConnector(PolyEmuConnector):
    _streams: tuple[asyncio.StreamReader, asyncio.StreamWriter] | None
    _lock: asyncio.Lock

    def __init__(self):
        super().__init__()
        self._streams = None
        self._lock = asyncio.Lock()

    def is_connected(self):
        return self._streams is not None

    async def connect(self):
        try:
            self._streams = await asyncio.open_connection("127.0.0.1", CLIENT_PORT)
            return True
        except (TimeoutError, ConnectionRefusedError):
            self._streams = None
            return False

    async def disconnect(self):
        if self._streams is not None:
            self._streams[1].close()

            try:
                await self._streams[1].wait_closed()
            except:
                pass
            finally:
                self._streams = None

    async def send_message(self, message) -> bytes:
        message = len(message).to_bytes(2, "big") + message

        async with self._lock:
            if self._streams is None:
                raise NotConnectedError()

            try:
                reader, writer = self._streams
                writer.write(message)
                await asyncio.wait_for(writer.drain(), timeout=5)

                response_size = await asyncio.wait_for(reader.read(2), timeout=5)
                if response_size == b"":
                    await self.disconnect()
                    raise ConnectionLostError("Connection closed")

                data = await asyncio.wait_for(reader.read(int.from_bytes(response_size, "big")), timeout=5)
                if data == b"":
                    await self.disconnect()
                    raise ConnectionLostError("Connection closed")

                return data
            except asyncio.TimeoutError as exc:
                await self.disconnect()
                raise ConnectionLostError("Connection timed out") from exc
            except ConnectionResetError as exc:
                await self.disconnect()
                raise ConnectionLostError("Connection reset") from exc


class PolyEmuContext:
    connector: PolyEmuConnector
    selected_device_id: bytes

    def __init__(self, connector_type: type[PolyEmuConnector]):
        self.connector = connector_type()
        self.selected_device_id = BROKER_DEVICE_ID


async def send_requests(ctx: PolyEmuContext, request_list: list[PolyEmuRequest]) -> list[PolyEmuResponse]:
    message = bytes()
    for request in request_list:
        message += request.to_bytes()
    message = ctx.selected_device_id + message

    received = await ctx.connector.send_message(message)
    responses = AutoPolyEmuResponseRegister.convert_response_chain(received)

    errors: list[PolyEmuError] = []

    for response in responses:
        if response.type == PolyEmuResponseType.ERROR:
            assert isinstance(response, ErrorResponse)
            errors.append(AutoPolyEmuErrorRegister.get_error_type(response.error_code).from_response(response))

    if errors:
        if len(errors) == 1 or sys.version_info < (3, 11, 0):
            raise errors[0]
        else:
            raise ExceptionGroup("Emulator returned errors", errors)  # noqa

    return responses


async def ping(ctx: PolyEmuContext) -> None:
    await send_requests(ctx, [NoOpRequest()])


async def list_devices(ctx: PolyEmuContext) -> list[bytes]:
    res: ListDevicesResponse = (await send_requests(ctx, [ListDevicesRequest()]))[0]
    return res.devices


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
