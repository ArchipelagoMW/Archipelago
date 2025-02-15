import asyncio
import grpc
import os
import sys

from ...core import PLATFORMS, Connector, RequestChain, NoOpRequest, ListDevicesRequest, PlatformRequest, ReadRequest, ResponseChain, ResponseChainHeader, NoOpResponse, ListDevicesResponse, PlatformResponse, ReadResponse

# grpc generated code doesn't do relative imports
existing_path = sys.path
absolute_path = os.path.abspath(os.path.dirname(__file__))
if absolute_path not in existing_path:
    sys.path.append(absolute_path)

from .sni_pb2_grpc import DevicesStub, DeviceMemoryStub
from .sni_pb2 import DevicesRequest, DevicesResponse, MemoryMapping, SingleReadMemoryRequest, ReadMemoryRequest, AddressSpace, SingleReadMemoryResponse


__all__ = (
    "SNIConnector",
)

DOMAIN_ID_TO_FXPACK_BASE = {
    PLATFORMS.SNES.ROM: 0x00_0000,
    PLATFORMS.SNES.SRAM: 0x0E_0000,
}


class SNIConnector(Connector):
    _channel: grpc.Channel | None
    _devices_stub: DevicesStub | None
    _memory_stub: DeviceMemoryStub | None
    _device_ids: dict[bytes, str]
    _lock: asyncio.Lock

    def __init__(self):
        super().__init__()
        self._channel = None
        self._devices_stub = None
        self._memory_stub = None
        self._device_ids = {}
        self._lock = asyncio.Lock()

    def is_connected(self):
        return self._channel is not None

    async def connect(self):
        try:
            self._channel = grpc.insecure_channel("localhost:8191")
            self._devices_stub = DevicesStub(self._channel)
            self._memory_stub = DeviceMemoryStub(self._channel)
            return True
        except (TimeoutError, ConnectionRefusedError):
            self._streams = None
            return False

    async def disconnect(self):
        if self._channel is not None:
            try:
                self._channel.close()
            except Exception as exc:
                raise exc
            finally:
                self._channel = None

    async def send_message(self, message) -> bytes:
        # TODO: Print warning or something if request chain cannot be executed in a single request to SNI
        chain = RequestChain.from_bytes(message)

        responses = []
        for request in chain.requests:
            match request:
                case NoOpRequest():
                    responses.append(NoOpResponse())
                case ListDevicesRequest():
                    sni_response: DevicesResponse = self._devices_stub.ListDevices(DevicesRequest())
                    self._device_ids = {device.uri.encode("utf-8")[-8:]: device.uri for device in sni_response.devices}
                    responses.append(ListDevicesResponse(list(self._device_ids.keys())))
                case PlatformRequest():
                    responses.append(PlatformResponse(PLATFORMS.SNES._ID))
                case ReadRequest(domain_id=domain_id, address=address, size=size):
                    # TODO: Collect and batch reads
                    sni_response: SingleReadMemoryResponse = self._memory_stub.SingleRead(
                        SingleReadMemoryRequest(uri=self._device_ids[chain.header.device_id], request=ReadMemoryRequest(
                            requestAddress=DOMAIN_ID_TO_FXPACK_BASE[domain_id] + address,
                            requestAddressSpace=AddressSpace.FxPakPro,
                            requestMemoryMapping=MemoryMapping.Unknown,
                            size=size
                        ))
                    )
                    responses.append(ReadResponse(sni_response.response.data))

        return ResponseChain(ResponseChainHeader(), responses).to_bytes()
