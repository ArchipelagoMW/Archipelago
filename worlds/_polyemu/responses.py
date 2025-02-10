from __future__ import annotations

import abc
from typing import Any, ClassVar, Self, Sequence  # Self py 3.11+

from .enums import PLATFORMS, PlatformEnum, PolyEmuResponseType
from .errors import MalformedResponseError


RESPONSE_HEADER_SIZE = 1


class ResponseBuffer:
    _buffer: bytes
    _cursor: int

    def __init__(self, data: bytes):
        self._buffer = data
        self._cursor = 0

    def reached_end(self):
        return self._cursor >= len(self._buffer)

    def consume_bytes(self, size: int) -> bytes:
        ret = self._buffer[self._cursor:self._cursor + size]
        self._cursor = self._cursor + size
        return ret

    def consume_int(self, size: int) -> int:
        ret = int.from_bytes(self._buffer[self._cursor:self._cursor + size], "big")
        self._cursor = self._cursor + size
        return ret

    def __str__(self):
        byte_strs = [hex(d) for d in self._buffer]
        byte_strs = [b[b.find("x") + 1:].rjust(2, "0") for b in byte_strs]
        byte_strs = [f"[{b}]" if i == self._cursor else b for i, b in enumerate(byte_strs)]
        return " ".join(byte_strs)


class AutoPolyEmuResponseRegister(abc.ABCMeta):
    response_types: ClassVar[dict[int, PolyEmuResponse]] = {}

    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> AutoPolyEmuResponseRegister:
        new_class = super().__new__(cls, name, bases, namespace)

        # Register response type
        if "type" in namespace:
            AutoPolyEmuResponseRegister.response_types[namespace["type"]] = new_class

        return new_class

    @staticmethod
    def get_response_class(code: int) -> type[PolyEmuResponse]:
        try:
            return AutoPolyEmuResponseRegister.response_types[code]
        except KeyError:
            raise KeyError(f"Response code [{hex(code)}] does not have a corresponding response type")

    @staticmethod
    def convert_response_chain(msg: bytes) -> list[PolyEmuResponse]:
        buffer = ResponseBuffer(msg)
        responses: list[PolyEmuResponse] = []
        while not buffer.reached_end():
            try:
                response_header = buffer.consume_bytes(RESPONSE_HEADER_SIZE)
                response_class = AutoPolyEmuResponseRegister.get_response_class(response_header[0])
                assert response_header[0] == response_class.type
                response = response_class.consume_response_body(response_header, buffer)
                responses.append(response)
            except KeyError as exc:
                raise MalformedResponseError(f"Could not read response: {buffer}") from exc
        return responses


class PolyEmuResponse(abc.ABC, metaclass=AutoPolyEmuResponseRegister):
    type: ClassVar[int]

    @classmethod
    def consume_response_body(cls, header: bytes, buffer: ResponseBuffer) -> Self:
        return cls()


class NoOpResponse(PolyEmuResponse):
    type = PolyEmuResponseType.NO_OP


class SupportedOperationsResponse(PolyEmuResponse):
    type = PolyEmuResponseType.PLATFORM

    supported_operations: list[int]

    def __init__(self, supported_operations: Sequence[int]):
        self.supported_operations = list(supported_operations)

    @classmethod
    def consume_response_body(cls, header, buffer):
        return cls(buffer.consume_bytes(buffer.consume_int(1)))


class PlatformResponse(PolyEmuResponse):
    type = PolyEmuResponseType.PLATFORM

    platform_id: PlatformEnum

    def __init__(self, platform_id: int):
        self.platform_id = PLATFORMS.get_by_id(platform_id)

    @classmethod
    def consume_response_body(cls, header, buffer):
        return cls(buffer.consume_int(1))


class ListDevicesResponse(PolyEmuResponse):
    type = PolyEmuResponseType.LIST_DEVICES

    devices: list[bytes]

    def __init__(self, devices: list[bytes]):
        self.devices = devices[:]

    @classmethod
    def consume_response_body(cls, header, buffer):
        num_devices = buffer.consume_int(1)
        devices = [buffer.consume_bytes(8) for _ in range(num_devices)]
        return cls(devices)


class MemorySizeResponse(PolyEmuResponse):
    type = PolyEmuResponseType.MEMORY_SIZE

    memory_sizes: dict[int, int]

    def __init__(self, memory_sizes: dict[int, int]):
        self.memory_sizes = memory_sizes

    @classmethod
    def consume_response_body(cls, header, buffer):
        num_entries = buffer.consume_int(1)
        sizes = {}
        for _ in range(num_entries):
            sizes[buffer.consume_int(1)] = buffer.consume_int(8)
        return cls(sizes)


class ReadResponse(PolyEmuResponse):
    type = PolyEmuResponseType.READ

    data: bytes

    def __init__(self, data: bytes):
        self.data = data

    @classmethod
    def consume_response_body(cls, header, buffer):
        return cls(buffer.consume_bytes(buffer.consume_int(2)))


class WriteResponse(PolyEmuResponse):
    type = PolyEmuResponseType.WRITE


class GuardResponse(PolyEmuResponse):
    type = PolyEmuResponseType.GUARD

    validated: bool

    def __init__(self, validated: bool):
        self.validated = validated

    @classmethod
    def consume_response_body(cls, header, buffer):
        return cls(buffer.consume_int(1) != 0)


class LockResponse(PolyEmuResponse):
    type = PolyEmuResponseType.LOCK


class UnlockResponse(PolyEmuResponse):
    type = PolyEmuResponseType.UNLOCK


class DisplayMessageResponse(PolyEmuResponse):
    type = PolyEmuResponseType.DISPLAY_MESSAGE


class ErrorResponse(PolyEmuResponse):
    type = PolyEmuResponseType.ERROR

    error_code: int
    error_context: bytes

    def __init__(self, code: int, context: bytes):
        self.error_code = code
        self.error_context = context

    @classmethod
    def consume_response_body(cls, header, buffer):
        return cls(buffer.consume_int(1), buffer.consume_bytes(buffer.consume_int(2)))
