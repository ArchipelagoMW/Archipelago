import json
from typing import Optional, Callable, Any, TypeVar
import pkgutil

T = TypeVar("T")


def fetch_json(
    path: str, object_hook: Optional[Callable[[dict[str, Any]], T]] = None
) -> Any:
    data = pkgutil.get_data(__name__, path)
    if data is None:
        raise FileNotFoundError
    return json.loads(data.decode("utf-8"), object_hook=object_hook)


def write_bytes_le(data: bytearray, addr: int, val: int, size: int):
    for offset in range(size):
        data[addr + offset] = val & 0xFF
        val >>= 8


def write_short_le(data: bytearray, addr: int, val: int):
    write_bytes_le(data, addr, val, 2)


def write_word_le(data: bytearray, addr: int, val: int):
    write_bytes_le(data, addr, val, 4)


def read_bytes_le(data: bytearray, offs: int, size: int) -> int:
    result = 0
    for i in range(size):
        result += data[offs + i] << 8*i
    return result


def read_short_le(data: bytearray, offs: int) -> int:
    return read_bytes_le(data, offs, 2)


def read_word_le(data: bytearray, offs: int) -> int:
    return read_bytes_le(data, offs, 4)
