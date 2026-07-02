from __future__ import annotations

from ...interface_orchestrator.memory.base import MemoryInterface
from ...interface import Pine


class PineInterface(MemoryInterface):
    """
    This is a wrapper for Pine interface.
    The plan is to implement a PSP interface here matching MemoryInterface, then swap
    out the interface per game, as there is very little logic difference in these
    games' memory.
    """

    def __init__(self, pine: Pine) -> None:
        self._pine = pine

    def read(self, address: int, size: int) -> bytes:
        return self._pine.read_bytes(address, size)

    def write(self, address: int, data: bytes) -> None:
        self._pine.write_bytes(address, data)

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass
