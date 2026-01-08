from __future__ import annotations

import dataclasses
import struct
from pathlib import Path
from typing import BinaryIO, Iterable, Tuple, Union

from ppc_asm import assembler

__all__ = [
    "Section",
    "DolHeader",
    "Symbol",
    "DolEditor",
    "DolFile"
]

_NUM_TEXT_SECTIONS = 7
_NUM_DATA_SECTIONS = 11
_NUM_SECTIONS = _NUM_TEXT_SECTIONS + _NUM_DATA_SECTIONS


@dataclasses.dataclass(frozen=True)
class Section:
    offset: int
    base_address: int
    size: int


@dataclasses.dataclass(frozen=True)
class DolHeader:
    sections: tuple[Section, ...]
    bss_address: int
    bss_size: int
    entry_point: int

    @classmethod
    def from_bytes(cls, data: bytes) -> DolHeader:
        struct_format = f">{_NUM_SECTIONS}L"
        offset_for_section = struct.unpack_from(struct_format, data, 0)
        base_address_for_section = struct.unpack_from(struct_format, data, 0x48)
        size_for_section = struct.unpack_from(struct_format, data, 0x90)

        bss_address, bss_size, entry_point = struct.unpack_from(">LLL", data, 0xD8)
        sections = tuple(Section(offset_for_section[i], base_address_for_section[i], size_for_section[i])
                         for i in range(_NUM_SECTIONS))

        return cls(sections, bss_address, bss_size, entry_point)

    def as_bytes(self) -> bytes:
        args = []
        args.extend(section.offset for section in self.sections)
        args.extend(section.base_address for section in self.sections)
        args.extend(section.size for section in self.sections)
        args.extend([self.bss_address, self.bss_size, self.entry_point])

        return struct.pack(f">{_NUM_SECTIONS}L{_NUM_SECTIONS}L{_NUM_SECTIONS}LLLL", *args) + (b"\x00" * 0x1C)

    def section_for_address(self, address: int) -> Section | None:
        for section in self.sections:
            relative_to_base = address - section.base_address
            if 0 <= relative_to_base < section.size:
                return section

    def offset_for_address(self, address: int) -> int | None:
        section = self.section_for_address(address)
        if section is not None:
            return section.offset + (address - section.base_address)
        return None


Symbol = Union[int, str, Tuple[str, int]]


class DolEditor:
    header: DolHeader
    symbols: dict[str, int]

    def __init__(self, header: DolHeader):
        self.header = header
        self.symbols = {}

    def resolve_symbol(self, address_or_symbol: Symbol) -> int:
        if isinstance(address_or_symbol, tuple):
            symbol, offset = address_or_symbol
            return self.symbols[symbol] + offset
        elif isinstance(address_or_symbol, str):
            return self.symbols[address_or_symbol]
        else:
            return address_or_symbol

    def offset_for_address(self, address: int) -> int:
        offset = self.header.offset_for_address(address)
        if offset is None:
            raise ValueError(f"Address 0x{address:x} could not be resolved for dol")
        return offset

    def _seek_and_read(self, seek: int, size: int):
        raise NotImplementedError()

    def _seek_and_write(self, seek: int, data: bytes):
        raise NotImplementedError()

    def read(self, address: int, size: int) -> bytes:
        offset = self.offset_for_address(address)
        return self._seek_and_read(offset, size)

    def write(self, address_or_symbol: Symbol, code_points: Iterable[int]):
        offset = self.offset_for_address(self.resolve_symbol(address_or_symbol))
        self._seek_and_write(offset, bytes(code_points))

    def write_instructions(self, address_or_symbol: Symbol,
                           instructions: list[assembler.BaseInstruction]):
        address = self.resolve_symbol(address_or_symbol)
        self.write(address, assembler.assemble_instructions(address, instructions, symbols=self.symbols))


class DolFile(DolEditor):
    symbols: dict[str, int]
    dol_file: BinaryIO | None = None
    editable: bool = False

    def __init__(self, dol_path: Path):
        with dol_path.open("rb") as f:
            header_bytes = f.read(0x100)

        self.dol_path = dol_path
        super().__init__(DolHeader.from_bytes(header_bytes))

    def set_editable(self, editable: bool):
        self.editable = editable

    def __enter__(self):
        if self.editable:
            f = self.dol_path.open("r+b")
        else:
            f = self.dol_path.open("rb")
        self.dol_file = f.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dol_file.__exit__(exc_type, exc_type, exc_tb)
        self.dol_file = None

    def _seek_and_read(self, seek: int, size: int):
        self.dol_file.seek(seek)
        return self.dol_file.read(size)

    def _seek_and_write(self, seek: int, data: bytes):
        self.dol_file.seek(seek)
        self.dol_file.write(data)
