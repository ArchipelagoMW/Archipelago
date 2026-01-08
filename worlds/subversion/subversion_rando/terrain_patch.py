from dataclasses import dataclass
from typing import NamedTuple, Optional, Union


class Space(NamedTuple):
    size: int
    location: int


@dataclass
class Patch:
    data: Union[bytes, bytearray]
    pointers: list[int]
    freed_space: Optional[Space] = None
