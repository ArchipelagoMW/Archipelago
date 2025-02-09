import abc
import struct
from typing import ClassVar, Sequence

from .enums import RequestType


class Request(abc.ABC):
    type: ClassVar[RequestType]

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


class GameIdRequest(Request):
    type = RequestType.GAME_ID


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

    def _get_body(self):
        return len(self.message).to_bytes(2, "big") + self.message.encode("utf-8")
