from dataclasses import dataclass
from typing import Literal
from collections.abc import Callable

ByteOrder = Literal["big", "little"]


class BitmaskAction(int):
    UNSET_UNCHECKED = 0
    SET_UNCHECKED = 1
    UNSET_CHECKED = 2


class TypeSize(int):
    WORD = 4
    HALF_WORD = 2
    BYTE = 1


def is_address(address: int) -> bool:
    return address & 0x80000000 != 0 and address & 0x7F000000 == 0


def read_int(
    data: bytearray, start: int, size: int, byteorder: Literal["little", "big"] = "little", signed: bool = False
) -> int:
    try:
        return int.from_bytes(data[start : start + size], byteorder=byteorder, signed=signed)
    except Exception:
        return 0x00


def write_int(
    data: bytearray,
    start: int,
    size: int,
    value: int,
    byteorder: Literal["little", "big"] = "little",
    signed: bool = False,
) -> bytearray:
    value = min(value, (1 << (8 * size)) - 1)

    data[start : start + size] = value.to_bytes(size, byteorder=byteorder, signed=signed)
    return data


@dataclass
class Trigger:
    address: int
    is_triggered: Callable[[int], bool]


@dataclass
class Bitmask:
    """Maps a specific bit in RAM"""

    address: int
    mask: int = 0x00

    def __init__(
        self,
        address: int,
        mask: int | None = None,
    ):
        position = None
        assert mask is not None or position is not None

        self.address = address

        if mask is not None:
            self.mask = mask

    def __hash__(self) -> int:
        return hash((self.address, self.mask))


def reverse(hex: str) -> str:
    """Reverse HEX string"""
    return "".join([hex[i : i + 2] for i in range(0, len(hex), 2)][::-1])
