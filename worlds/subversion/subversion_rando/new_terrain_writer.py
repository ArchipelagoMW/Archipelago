from bisect import insort_right
from typing import Union

from .romWriter import RomWriter, RomWriterType
from .terrain_patch import Patch, Space


class TerrainWriter:
    empty_space: int
    rom_writer: RomWriter
    emptied: list[Space]

    def __init__(self, rom_writer: RomWriter) -> None:
        self.empty_space = 0x2f51c4
        self.rom_writer = rom_writer
        self.emptied = []

    def add_space(self, freed_space: Space) -> None:
        """ let the `TerrainWriter` use this space to put new level data in the rom """
        insort_right(self.emptied, freed_space)

    def _take_space(self, data: Union[bytes, bytearray]) -> int:
        size_needed = len(data)
        i = 0
        while i < len(self.emptied):
            entry = self.emptied[i]
            if size_needed < entry.size:
                self.emptied.pop(i)
                # print(f"using freed rom space {entry}")
                return entry.location
            i += 1

        # verify the space is empty
        if self.rom_writer.romWriterType == RomWriterType.file:
            for i in range(len(data)):
                assert self.rom_writer.rom_data[self.empty_space + i] == 0xff
        tr = self.empty_space
        self.empty_space += len(data) + 1
        return tr

    def write(self, patch: Patch) -> None:
        if patch.freed_space:
            self.add_space(patch.freed_space)
        destination = self._take_space(patch.data)

        self.rom_writer.writeBytes(destination, patch.data)
        p_level_data = RomWriter.index_to_snes_addr(destination).to_bytes(3, "little")
        # print(f"{p_level_data=}")
        for pointer in patch.pointers:
            self.rom_writer.writeBytes(pointer, p_level_data)
