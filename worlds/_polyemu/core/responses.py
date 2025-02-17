from __future__ import annotations

import abc
from enum import IntEnum
import struct
from typing import Any, ClassVar, Self, Sequence  # Self py 3.11+

from .errors import MalformedResponseError
from .utils import Buffer


__all__ = [
    "ResponseType", "ResponseChainHeader", "ResponseChain",
    "AutoResponseRegister", "Response", "NoOpResponse",
    "SupportedOperationsResponse", "PlatformResponse", "ListDevicesResponse",
    "MemorySizeResponse", "ReadResponse", "WriteResponse", "GuardResponse",
    "LockResponse", "UnlockResponse", "DisplayMessageResponse", "ErrorResponse",
]


class ResponseType(IntEnum):
    NO_OP = 0x80
    SUPPORTED_OPERATIONS = 0x81
    PLATFORM = 0x82
    MEMORY_SIZE = 0x83
    LIST_DEVICES = 0x84
    READ = 0x90
    WRITE = 0x91
    GUARD = 0x92
    LOCK = 0xA0
    UNLOCK = 0xA1
    DISPLAY_MESSAGE = 0xA2
    ERROR = 0xFF


# This class mostly exists to parallel requests, but also sets up for the
# possibility of adding data to a response header.
class ResponseChainHeader:
    @classmethod
    def consume_from_buffer(cls, buffer: Buffer) -> Self:
        return cls()

    def to_bytes(self) -> bytes:
        return b""


class ResponseChain:
    header: ResponseChainHeader
    responses: list[Response]

    def __init__(self, header: ResponseChainHeader, responses: list[Response]):
        self.header = header
        self.responses = responses
    
    def to_bytes(self) -> bytes:
        data = self.header.to_bytes()
        for response in self.responses:
            data += response.to_bytes()
        return data

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        buffer = Buffer(data)
        header = ResponseChainHeader.consume_from_buffer(buffer)
        responses: list[Response] = []

        while not buffer.reached_end():
            try:
                response_type = buffer.consume_int(1)
                response_class = AutoResponseRegister.get_response_class(response_type)
                assert response_type == response_class.type
                responses.append(response_class.consume_from_buffer(buffer))
            except KeyError as exc:
                raise MalformedResponseError(f"Could not read response: {buffer}") from exc
        return cls(header, responses)


class AutoResponseRegister(abc.ABCMeta):
    response_types: ClassVar[dict[int, Response]] = {}

    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> AutoResponseRegister:
        new_class = super().__new__(cls, name, bases, namespace)

        # Register response type
        if "type" in namespace:
            AutoResponseRegister.response_types[namespace["type"]] = new_class

        return new_class

    @staticmethod
    def get_response_class(code: int) -> type[Response]:
        try:
            return AutoResponseRegister.response_types[code]
        except KeyError:
            raise KeyError(f"Response code [{hex(code)}] does not have a corresponding response type")


class Response(abc.ABC, metaclass=AutoResponseRegister):
    type: ClassVar[ResponseType]

    @classmethod
    def consume_from_buffer(cls, buffer: Buffer) -> Self:
        return cls()

    def _get_body(self) -> bytes:
        return b""

    def to_bytes(self) -> bytes:
        return struct.pack(">B", self.type) + self._get_body()


class NoOpResponse(Response):
    type = ResponseType.NO_OP


class SupportedOperationsResponse(Response):
    type = ResponseType.SUPPORTED_OPERATIONS

    supported_operations: list[int]

    def __init__(self, supported_operations: Sequence[int]):
        self.supported_operations = list(supported_operations)

    @classmethod
    def consume_from_buffer(cls, buffer):
        return cls(buffer.consume_bytes(buffer.consume_int(1)))

    def _get_body(self):
        return struct.pack(">B", len(self.supported_operations)) + bytes(self.supported_operations)


class PlatformResponse(Response):
    type = ResponseType.PLATFORM

    platform_id: int

    def __init__(self, platform_id: int):
        self.platform_id = platform_id

    @classmethod
    def consume_from_buffer(cls, buffer):
        return cls(buffer.consume_int(1))

    def _get_body(self):
        return struct.pack(">B", self.platform_id)


class MemorySizeResponse(Response):
    type = ResponseType.MEMORY_SIZE

    memory_sizes: dict[int, int]

    def __init__(self, memory_sizes: dict[int, int]):
        self.memory_sizes = memory_sizes

    @classmethod
    def consume_from_buffer(cls, buffer):
        num_entries = buffer.consume_int(1)
        sizes = {}
        for _ in range(num_entries):
            sizes[buffer.consume_int(1)] = buffer.consume_int(8)
        return cls(sizes)

    def _get_body(self):
        body = struct.pack(">B", len(self.memory_sizes))
        for domain_id, size in self.memory_sizes.items():
            body += struct.pack(">BQ", domain_id, size)
        return body


class ListDevicesResponse(Response):
    type = ResponseType.LIST_DEVICES

    devices: list[bytes]

    def __init__(self, devices: list[bytes]):
        self.devices = devices[:]

    @classmethod
    def consume_from_buffer(cls, buffer):
        num_devices = buffer.consume_int(1)
        devices = [buffer.consume_bytes(8) for _ in range(num_devices)]
        return cls(devices)

    def _get_body(self):
        body = struct.pack(">B", len(self.devices))
        for device_id in self.devices:
            body += device_id
        return body


class ReadResponse(Response):
    type = ResponseType.READ

    data: bytes

    def __init__(self, data: bytes):
        self.data = data

    @classmethod
    def consume_from_buffer(cls, buffer):
        return cls(buffer.consume_bytes(buffer.consume_int(2)))

    def _get_body(self):
        return struct.pack(">H", len(self.data)) + self.data


class WriteResponse(Response):
    type = ResponseType.WRITE


class GuardResponse(Response):
    type = ResponseType.GUARD

    validated: bool

    def __init__(self, validated: bool):
        self.validated = validated

    @classmethod
    def consume_from_buffer(cls, buffer):
        return cls(buffer.consume_int(1) != 0)

    def _get_body(self):
        return struct.pack(">B", int(self.validated))


class LockResponse(Response):
    type = ResponseType.LOCK


class UnlockResponse(Response):
    type = ResponseType.UNLOCK


class DisplayMessageResponse(Response):
    type = ResponseType.DISPLAY_MESSAGE


class ErrorResponse(Response):
    type = ResponseType.ERROR

    error_code: int
    error_context: bytes

    def __init__(self, code: int, context: bytes = b""):
        self.error_code = code
        self.error_context = context

    @classmethod
    def consume_from_buffer(cls, buffer):
        return cls(buffer.consume_int(1), buffer.consume_bytes(buffer.consume_int(2)))

    def _get_body(self):
        return struct.pack(">BH", self.error_code, len(self.error_context)) + self.error_context
