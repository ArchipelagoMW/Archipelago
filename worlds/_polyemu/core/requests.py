from __future__ import annotations

import abc
from enum import IntEnum
import struct
from typing import Any, ClassVar, Self, Sequence

from .errors import MalformedRequestError
from .utils import Buffer


__all__ = [
    "RequestType", "RequestChainHeader", "RequestChain",
    "AutoRequestRegister", "Request", "NoOpRequest",
    "SupportedOperationsRequest", "PlatformRequest", "ListDevicesRequest",
    "MemorySizeRequest", "ReadRequest", "WriteRequest", "GuardRequest",
    "LockRequest", "UnlockRequest", "DisplayMessageRequest",
]


class RequestType(IntEnum):
    NO_OP = 0x00
    SUPPORTED_OPERATIONS = 0x01
    PLATFORM = 0x02
    MEMORY_SIZE = 0x03
    LIST_DEVICES = 0x04
    READ = 0x10
    WRITE = 0x11
    GUARD = 0x12
    LOCK = 0x20
    UNLOCK = 0x21
    DISPLAY_MESSAGE = 0x22


class RequestChainHeader:
    device_id: bytes

    def __init__(self, device_id: bytes):
        self.device_id = device_id

    @classmethod
    def consume_from_buffer(cls, buffer: Buffer) -> Self:
        return cls(buffer.consume_bytes(8))

    def to_bytes(self) -> bytes:
        return self.device_id


class RequestChain:
    header: RequestChainHeader
    requests: list[Request]

    def __init__(self, header: RequestChainHeader, requests: list[Request]):
        self.header = header
        self.requests = requests
    
    def to_bytes(self) -> bytes:
        data = self.header.to_bytes()
        for request in self.requests:
            data += request.to_bytes()
        return data

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        buffer = Buffer(data)
        header = RequestChainHeader.consume_from_buffer(buffer)
        requests: list[Request] = []

        while not buffer.reached_end():
            try:
                request_type = buffer.consume_int(1)
                request_class = AutoRequestRegister.get_request_class(request_type)
                assert request_type == request_class.type
                requests.append(request_class.consume_from_buffer(buffer))
            except KeyError as exc:
                raise MalformedRequestError(f"Could not read request: {buffer}") from exc
        return cls(header, requests)


class AutoRequestRegister(abc.ABCMeta):
    request_types: ClassVar[dict[int, Request]] = {}

    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> AutoRequestRegister:
        new_class = super().__new__(cls, name, bases, namespace)

        # Register request type
        if "type" in namespace:
            AutoRequestRegister.request_types[namespace["type"]] = new_class

        return new_class

    @staticmethod
    def get_request_class(code: int) -> type[Request]:
        try:
            return AutoRequestRegister.request_types[code]
        except KeyError:
            raise KeyError(f"Request code [{hex(code)}] does not have a corresponding request type")


class Request(abc.ABC, metaclass=AutoRequestRegister):
    type: ClassVar[RequestType]

    @staticmethod
    def get_header(buffer: Buffer) -> bytes:
        return buffer.consume_bytes(1)

    @classmethod
    def consume_from_buffer(cls, buffer: Buffer) -> Self:
        return cls()

    def _get_body(self) -> bytes:
        return b""

    def to_bytes(self) -> bytes:
        return struct.pack(">B", self.type) + self._get_body()


class NoOpRequest(Request):
    type = RequestType.NO_OP


class SupportedOperationsRequest(Request):
    type = RequestType.SUPPORTED_OPERATIONS


class PlatformRequest(Request):
    type = RequestType.PLATFORM


class ListDevicesRequest(Request):
    type = RequestType.LIST_DEVICES


class MemorySizeRequest(Request):
    type = RequestType.MEMORY_SIZE


class ReadRequest(Request):
    type = RequestType.READ

    domain_id: int
    address: int
    size: int

    def __init__(self, domain_id: int, address: int, size: int):
        super().__init__()
        self.domain_id = domain_id
        self.address = address
        self.size = size

    @classmethod
    def consume_from_buffer(cls, buffer):
        return cls(buffer.consume_int(1), buffer.consume_int(8), buffer.consume_int(2))

    def _get_body(self):
        return struct.pack(">BQH", self.domain_id, self.address, self.size)


class WriteRequest(Request):
    type = RequestType.WRITE

    domain_id: int
    address: int
    data: bytes

    def __init__(self, domain_id: int, address: int, data: Sequence[int]):
        super().__init__()
        self.domain_id = domain_id
        self.address = address
        self.data = bytes(data)

    @classmethod
    def consume_from_buffer(cls, buffer):
        return cls(buffer.consume_int(1), buffer.consume_int(8), buffer.consume_bytes(buffer.consume_int(2)))

    def _get_body(self):
        return struct.pack(">BQH", self.domain_id, self.address, len(self.data)) + self.data


class GuardRequest(Request):
    type = RequestType.GUARD

    domain_id: int
    address: int
    expected_data: bytes

    def __init__(self, domain_id: int, address: int, expected_data: Sequence[int]):
        super().__init__()
        self.domain_id = domain_id
        self.address = address
        self.expected_data = bytes(expected_data)

    @classmethod
    def consume_from_buffer(cls, buffer):
        return cls(buffer.consume_int(1), buffer.consume_int(8), buffer.consume_bytes(buffer.consume_int(2)))

    def _get_body(self):
        return struct.pack(">BQH", self.domain_id, self.address, len(self.expected_data)) + self.expected_data


class LockRequest(Request):
    type = RequestType.LOCK


class UnlockRequest(Request):
    type = RequestType.UNLOCK


class DisplayMessageRequest(Request):
    type = RequestType.DISPLAY_MESSAGE

    message: str

    def __init__(self, message: str):
        super().__init__()
        self.message = message

    @classmethod
    def consume_from_buffer(cls, buffer):
        return cls(buffer.consume_bytes(buffer.consume_int(2)).decode("utf-8"))

    def _get_body(self):
        return len(self.message).to_bytes(2, "big") + self.message.encode("utf-8")
