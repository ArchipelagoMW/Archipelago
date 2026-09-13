import asyncio
import grpc
import os
import sys

from ... import core as polyemu

# grpc generated code doesn't do relative imports
existing_path = sys.path
absolute_path = os.path.abspath(os.path.dirname(__file__))
if absolute_path not in existing_path:
    sys.path.append(absolute_path)

from . import sni_pb2_grpc as sni_grpc
from . import sni_pb2 as sni


__all__ = [
    "SNIAdapter",
]

DOMAIN_ID_TO_FXPACK_BASE = {
    polyemu.PLATFORMS.SNES.ROM: 0x0000000,
    polyemu.PLATFORMS.SNES.SRAM: 0x0E00000,
    polyemu.PLATFORMS.SNES.WRAM: 0xF500000,
    polyemu.PLATFORMS.SNES.VRAM: 0xF700000,
    polyemu.PLATFORMS.SNES.APU: 0xF800000,
    polyemu.PLATFORMS.SNES.CGRAM: 0xF900000,
    polyemu.PLATFORMS.SNES.OAM: 0xF900200,
    polyemu.PLATFORMS.SNES.MISC: 0xF900420,
}


class SNIAdapter(polyemu.Adapter):
    name = "SNI Adapter"

    _channel: grpc.aio.Channel | None
    _devices_stub: sni_grpc.DevicesStub | None
    _memory_stub: sni_grpc.DeviceMemoryStub | None
    _info_stub: sni_grpc.DeviceInfoStub | None
    _device_ids: dict[bytes, str]
    _device_supported_operations: dict[bytes, list[polyemu.RequestType]]
    _lock: asyncio.Lock

    def __init__(self):
        super().__init__()
        self._channel = None
        self._devices_stub = None
        self._memory_stub = None
        self._info_stub = None
        self._device_ids = {}
        self._device_supported_operations = {}
        self._lock = asyncio.Lock()

    def is_connected(self):
        return self._channel is not None

    async def connect(self):
        # TODO: Handle timeouts/errors here instead of waiting forever
        self._channel = grpc.aio.insecure_channel("localhost:8191")
        await self._channel.channel_ready()
        self._devices_stub = sni_grpc.DevicesStub(self._channel)
        self._memory_stub = sni_grpc.DeviceMemoryStub(self._channel)
        self._info_stub = sni_grpc.DeviceInfoStub(self._channel)
        return True

    async def disconnect(self):
        if self._channel is not None:
            try:
                await self._channel.close()
            except Exception as exc:
                raise exc
            finally:
                self._channel = None

    async def send_message(self, message) -> bytes:
        chain = polyemu.RequestChain.from_bytes(message)

        if any(isinstance(request, polyemu.ReadRequest) for request in chain.requests):
            if any(isinstance(request, polyemu.WriteRequest) for request in chain.requests):
                return polyemu.ResponseChain(polyemu.ResponseChainHeader(), [polyemu.ErrorResponse(
                    polyemu.ErrorType.DEVICE_ERROR,
                    b"SNI cannot process a request chain that includes both reads and writes"
                )])

        responses: dict[int, polyemu.Response] = {}
        if chain.header.device_id == polyemu.DEFAULT_DEVICE_ID:
            # Handle requests to this adapter
            for i, request in enumerate(chain.requests):
                match request:
                    case polyemu.NoOpRequest():
                        responses[i] = polyemu.NoOpResponse()
                    case polyemu.SupportedOperationsRequest():
                        responses[i] = polyemu.SupportedOperationsResponse([
                            polyemu.RequestType.NO_OP,
                            polyemu.RequestType.SUPPORTED_OPERATIONS,
                            polyemu.RequestType.LIST_DEVICES,
                            polyemu.RequestType.PLATFORM,
                        ])
                    case polyemu.ListDevicesRequest():
                        await self._get_devices()
                        responses[i] = polyemu.ListDevicesResponse(list(self._device_ids.keys()))
                    case polyemu.PlatformRequest():
                        responses[i] = polyemu.PlatformResponse(polyemu.PLATFORMS.SNES._ID)
                    case _:
                        responses[i] = polyemu.ErrorResponse(polyemu.ErrorType.UNSUPPORTED_OPERATION, bytes([request.type]))
                        break
        else:
            # Handle requests to SNI
            if chain.header.device_id not in self._device_ids:
                return polyemu.ResponseChain(
                    polyemu.ResponseChainHeader(),
                    [polyemu.ErrorResponse(polyemu.ErrorType.NO_SUCH_DEVICE, chain.header.device_id)]
                )

            # Could check ROM hash here, but not implemented for some SNI devices
            # self._info_stub.FetchFields(sni.FieldsRequest(
            #     uri=device_uri,
            #     fields=[sni.Field.RomHashValue]
            # ))

            device_uri = self._device_ids[chain.header.device_id]
            reads: dict[int, polyemu.ReadRequest] = {}
            writes: dict[int, polyemu.WriteRequest] = {}
            for i, request in enumerate(chain.requests):
                match request:
                    case polyemu.NoOpRequest():
                        responses[i] = polyemu.NoOpResponse()
                    case polyemu.SupportedOperationsRequest():
                        responses[i] = polyemu.SupportedOperationsResponse(self._device_supported_operations[chain.header.device_id])
                    case polyemu.PlatformRequest():
                        responses[i] = polyemu.PlatformResponse(polyemu.PLATFORMS.SNES._ID)
                    case polyemu.ReadRequest():
                        reads[i] = request
                    case polyemu.WriteRequest():
                        writes[i] = request
                    case _:
                        responses[i] = polyemu.ErrorResponse(polyemu.ErrorType.UNSUPPORTED_OPERATION, bytes([request.type]))
                        break

            assert not (bool(reads) and bool(writes))

            read_responses = await self._send_reads(device_uri, reads)
            write_responses = await self._send_writes(device_uri, writes)

            for i, response in read_responses.items():
                responses[i] = response
            for i, response in write_responses.items():
                responses[i] = response

        ordered_responses = sorted(responses.items())
        assert all(i == response_tuple[0] for i, response_tuple in zip(range(len(responses)), ordered_responses))

        return polyemu.ResponseChain(
            polyemu.ResponseChainHeader(),
            [response for _, response in ordered_responses]
        ).to_bytes()

    async def _get_devices(self):
        try:
            sni_response: sni.DevicesResponse = await self._devices_stub.ListDevices(sni.DevicesRequest())
        except grpc.aio.AioRpcError as exc:
            await self.disconnect()
            raise polyemu.ConnectionLostError from exc

        # Captures the port of the device as the device id
        self._device_ids = {device.uri.encode("utf-8")[-8:]: device.uri for device in sni_response.devices}
        inverted_device_ids = {v: k for k, v in self._device_ids.items()}

        CAPABILITY_EQUIVALENTS = [
            (sni.DeviceCapability.ReadMemory, polyemu.RequestType.READ),
            (sni.DeviceCapability.WriteMemory, polyemu.RequestType.WRITE),
        ]

        self._device_supported_operations = {}
        for device in sni_response.devices:
            operations = {
                polyemu.RequestType.NO_OP,
                polyemu.RequestType.SUPPORTED_OPERATIONS,
            }

            capabilities = set(device.capabilities)
            for capability, request_type in CAPABILITY_EQUIVALENTS:
                if capability in capabilities:
                    operations.add(request_type)

            self._device_supported_operations[inverted_device_ids[device.uri]] = operations

    async def _send_reads(self, device_uri: str, requests: dict[int, polyemu.ReadRequest]) -> dict[int, polyemu.ReadResponse]:
        if not requests:
            return {}

        requests_by_index = sorted(requests.items())
        indices: tuple[int, ...] = list(zip(*requests_by_index))[0]

        try:
            sni_response: sni.MultiReadMemoryResponse = await self._memory_stub.MultiRead(sni.MultiReadMemoryRequest(
                uri=device_uri,
                requests=[sni.ReadMemoryRequest(
                    requestAddress=DOMAIN_ID_TO_FXPACK_BASE[request.domain_id] + request.address,
                    requestAddressSpace=sni.AddressSpace.FxPakPro,
                    requestMemoryMapping=sni.MemoryMapping.Unknown,  # This seems to make BizHawk log a lot; maybe an SNI bug?
                    size=request.size,
                ) for _, request in requests_by_index]
            ))
        except grpc.aio.AioRpcError as exc:
            raise polyemu.ConnectionLostError() from exc

        return {i: polyemu.ReadResponse(response.data) for i, response in zip(indices, sni_response.responses)}

    async def _send_writes(self, device_uri: str, requests: dict[int, polyemu.WriteRequest]) -> dict[int, polyemu.WriteResponse]:
        if not requests:
            return {}

        requests_by_index = sorted(requests.items())
        indices: tuple[int, ...] = list(zip(*requests_by_index))[0]

        try:
            sni_response: sni.MultiWriteMemoryResponse = await self._memory_stub.MultiWrite(sni.MultiWriteMemoryRequest(
                uri=device_uri,
                requests=[sni.WriteMemoryRequest(
                    requestAddress=DOMAIN_ID_TO_FXPACK_BASE[request.domain_id] + request.address,
                    requestAddressSpace=sni.AddressSpace.FxPakPro,
                    requestMemoryMapping=sni.MemoryMapping.Unknown,  # This seems to make BizHawk log a lot; maybe an SNI bug?
                    data=request.data,
                ) for _, request in requests_by_index]
            ))
        except grpc.aio.AioRpcError as exc:
            raise polyemu.ConnectionLostError() from exc

        return {i: polyemu.WriteResponse() for i, _ in zip(indices, sni_response.responses)}
