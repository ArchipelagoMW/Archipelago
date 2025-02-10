import abc
import struct
from typing import ClassVar, Sequence

from .enums import PolyEmuRequestType


class PolyEmuRequest(abc.ABC):
    type: ClassVar[PolyEmuRequestType]

    def _get_body(self) -> bytes:
        return b""

    def to_bytes(self) -> bytes:
        return struct.pack(">B", self.type) + self._get_body()


class NoOpRequest(PolyEmuRequest):
    type = PolyEmuRequestType.NO_OP


class SupportedOperationsRequest(PolyEmuRequest):
    type = PolyEmuRequestType.SUPPORTED_OPERATIONS


class PlatformRequest(PolyEmuRequest):
    type = PolyEmuRequestType.PLATFORM


class ListDevicesRequest(PolyEmuRequest):
    type = PolyEmuRequestType.LIST_DEVICES


class MemorySizeRequest(PolyEmuRequest):
    type = PolyEmuRequestType.MEMORY_SIZE


class ReadRequest(PolyEmuRequest):
    type = PolyEmuRequestType.READ

    domain_id: int
    address: int
    size: int

    def __init__(self, domain_id: int, address: int, size: int):
        super().__init__()
        self.domain_id = domain_id
        self.address = address
        self.size = size

    def _get_body(self):
        return struct.pack(">BQH", self.domain_id, self.address, self.size)


class WriteRequest(PolyEmuRequest):
    type = PolyEmuRequestType.WRITE

    domain_id: int
    address: int
    data: bytes

    def __init__(self, domain_id: int, address: int, data: Sequence[int]):
        super().__init__()
        self.domain_id = domain_id
        self.address = address
        self.data = bytes(data)

    def _get_body(self):
        return struct.pack(">BQH", self.domain_id, self.address, len(self.data)) + self.data


class GuardRequest(PolyEmuRequest):
    type = PolyEmuRequestType.GUARD

    domain_id: int
    address: int
    expected_data: bytes

    def __init__(self, domain_id: int, address: int, expected_data: Sequence[int]):
        super().__init__()
        self.domain_id = domain_id
        self.address = address
        self.expected_data = bytes(expected_data)

    def _get_body(self):
        return struct.pack(">BQH", self.domain_id, self.address, len(self.expected_data)) + self.expected_data


class LockRequest(PolyEmuRequest):
    type = PolyEmuRequestType.LOCK


class UnlockRequest(PolyEmuRequest):
    type = PolyEmuRequestType.UNLOCK


class DisplayMessageRequest(PolyEmuRequest):
    type = PolyEmuRequestType.DISPLAY_MESSAGE

    message: str

    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def _get_body(self):
        return len(self.message).to_bytes(2, "big") + self.message.encode("utf-8")
