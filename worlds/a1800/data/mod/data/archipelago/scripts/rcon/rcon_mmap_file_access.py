from mmap import mmap
from typing import Optional

from .util import to_int8, to_int32, from_int

# Layout
# buffer server WRITE
#   1 int8 - READ
#   1 int8 - WRITE
#   64 * REQUEST_SIZE - 64 requests
# buffer client WRITE
#   1 int8 - READ
#   1 int8 - WRITE
#   64 * REQUEST_SIZE - 64 requests

PACKET_SIZE = 4096
REQUEST_SIZE = PACKET_SIZE + 4
_BUFFER_CAPACITY = 64
_BUFFER_SIZE = _BUFFER_CAPACITY * REQUEST_SIZE + 4
FILE_SIZE = 2 * _BUFFER_SIZE

_BUFFER_READ_IDX_SIZE = 1
_BUFFER_WRITE_IDX_SIZE = 1

_BUFFER_SERVER = 0
_BUFFER_CLIENT = _BUFFER_SERVER + _BUFFER_SIZE

_BUFFER_READ_IDX = 0
_BUFFER_WRITE_IDX = _BUFFER_READ_IDX + _BUFFER_READ_IDX_SIZE
_BUFFER_REQUESTS = _BUFFER_WRITE_IDX + _BUFFER_WRITE_IDX_SIZE


class _MMapAccess:
    def __init__(self, mmap_obj: mmap, size: Optional[int] = None, offset: int = 0) -> None:
        self._mmap_obj = mmap_obj
        self._SIZE = size if size else self._mmap_obj.size()
        self._OFFSET = offset

    def get(self, idx: int, size: int) -> bytes:
        return self._mmap_obj[self._OFFSET + idx:self._OFFSET + idx + size]

    def set(self, idx: int, size: int, value: bytes) -> None:
        self._mmap_obj[self._OFFSET + idx:self._OFFSET + idx + min(size, len(value))] = value

    def get_bool(self, idx: int, size: int) -> bool:
        return bool(self.get(idx, size))

    def set_bool(self, idx: int, size: int, value: bool) -> None:
        self.set(idx, size, bytes(value))

    def get_int(self, idx: int, size: int) -> int:
        return from_int(self.get(idx, size))

    def set_int8(self, idx: int, size: int, value: int) -> None:
        return self.set(idx, size, to_int8(value))

    def set_int32(self, idx: int, size: int, value: int) -> None:
        return self.set(idx, size, to_int32(value))

    def get_str(self, idx: int, size: int) -> str:
        return self.get(idx, size).decode()

    def set_str(self, idx: int, size: int, value: str) -> None:
        self.set(idx, size, value.encode("ascii"))

    def flush(self) -> None:
        self._mmap_obj.flush()

    def clear(self) -> None:
        self._mmap_obj[self._OFFSET:self._OFFSET + self._SIZE] = bytes(self._SIZE)
        self.flush()

    def close(self) -> None:
        self._mmap_obj.close()

    @property
    def closed(self) -> bool:
        return self._mmap_obj.closed


class _BufferAccess(_MMapAccess):
    def __init__(self, mmap_obj: mmap, offset: int = 0) -> None:
        super().__init__(mmap_obj, _BUFFER_SIZE, offset)

    @property
    def read_idx(self) -> int:
        return self.get_int(_BUFFER_READ_IDX, _BUFFER_READ_IDX_SIZE)

    @read_idx.setter
    def read_idx(self, value: int) -> None:
        self.set_int8(_BUFFER_READ_IDX, _BUFFER_READ_IDX_SIZE, value)

    @property
    def write_idx(self) -> int:
        return self.get_int(_BUFFER_WRITE_IDX, _BUFFER_WRITE_IDX_SIZE)

    @write_idx.setter
    def write_idx(self, value: int) -> None:
        self.set_int8(_BUFFER_WRITE_IDX, _BUFFER_WRITE_IDX_SIZE, value)

    def get_request(self, idx: int) -> bytes:
        assert idx >= 0, "Index cannot be negative"
        assert idx < _BUFFER_CAPACITY, "Index must be smaller than capacity {}".format(_BUFFER_CAPACITY)
        return self.get(_BUFFER_REQUESTS + idx * REQUEST_SIZE, REQUEST_SIZE)

    def write_request(self, idx: int, request: bytes) -> None:
        assert idx >= 0, "Index cannot be negative"
        assert idx < _BUFFER_CAPACITY, "Index must be smaller than capacity {}".format(_BUFFER_CAPACITY)
        self.set(_BUFFER_REQUESTS + idx * REQUEST_SIZE, REQUEST_SIZE, request)


class _RequestRingBuffer:
    def __init__(self, mmap_obj: mmap, offset: int = 0) -> None:
        self._memory = _BufferAccess(mmap_obj, offset)

    def put_request(self, request: bytes) -> bool:
        assert len(request) <= REQUEST_SIZE, "Request size cannot be larger than {}".format(REQUEST_SIZE)

        if ((self._memory.write_idx + 1) % _BUFFER_CAPACITY) == self._memory.read_idx:
            return False

        self._memory.write_request(self._memory.write_idx, request)

        self._memory.write_idx = (self._memory.write_idx + 1) % _BUFFER_CAPACITY

        self._memory.flush()

        return True

    def get_request(self) -> Optional[bytes]:
        if self._memory.read_idx == self._memory.write_idx:
            return None

        request = self._memory.get_request(self._memory.read_idx)

        self._memory.read_idx = (self._memory.read_idx + 1) % _BUFFER_CAPACITY

        self._memory.flush()

        return request

    def has_request(self) -> bool:
        return self._memory.read_idx != self._memory.write_idx


class RCONMMapFileAccess(_MMapAccess):
    def __init__(self, mmap_obj: mmap) -> None:
        super().__init__(mmap_obj)
        self.ring_buffer_server = _RequestRingBuffer(mmap_obj, _BUFFER_SERVER)
        self.ring_buffer_client = _RequestRingBuffer(mmap_obj, _BUFFER_CLIENT)
