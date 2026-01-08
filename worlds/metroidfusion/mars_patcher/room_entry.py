from __future__ import annotations

from typing import TYPE_CHECKING

from .compress import comp_rle, decomp_rle
from .constants.game_data import area_room_entry_ptrs

if TYPE_CHECKING:
    from types import TracebackType

    from .rom import Rom


class RoomEntry:
    def __init__(self, rom: Rom, area: int, room: int):
        self.rom = rom
        self.addr = rom.read_ptr(area_room_entry_ptrs(rom) + area * 4) + room * 0x3C

    def bg1_ptr(self) -> int:
        return self.addr + 0xC

    def bg2_ptr(self) -> int:
        return self.addr + 0x10

    def clip_ptr(self) -> int:
        return self.addr + 0x14

    def tileset(self) -> int:
        return self.rom.read_8(self.addr)

    def bg1_addr(self) -> int:
        return self.rom.read_ptr(self.bg1_ptr())

    def bg2_addr(self) -> int:
        return self.rom.read_ptr(self.bg2_ptr())

    def clip_addr(self) -> int:
        return self.rom.read_ptr(self.clip_ptr())

    def default_sprite_layout_addr(self) -> int:
        return self.rom.read_ptr(self.addr + 0x20)

    def default_spriteset(self) -> int:
        return self.rom.read_8(self.addr + 0x24)

    def load_bg1(self) -> BlockLayer:
        return BlockLayer(self.rom, self.bg1_ptr())

    def load_bg2(self) -> BlockLayer:
        return BlockLayer(self.rom, self.bg2_ptr())

    def load_clip(self) -> BlockLayer:
        return BlockLayer(self.rom, self.clip_ptr())

    @property
    def map_x(self) -> int:
        return self.rom.read_8(self.addr + 0x35)

    @property
    def map_y(self) -> int:
        return self.rom.read_8(self.addr + 0x36)


class BlockLayer:
    def __enter__(self) -> BlockLayer:
        # We don't need to do anything
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.write()

    def __init__(self, rom: Rom, ptr: int):
        addr = rom.read_ptr(ptr)
        self.rom = rom
        self.pointer = ptr
        self.width = rom.read_8(addr)
        self.height = rom.read_8(addr + 1)
        self.block_data, self.comp_len = decomp_rle(rom.data, addr + 2)

    def get_block_value(self, x: int, y: int) -> int:
        idx = (y * self.width + x) * 2
        if idx >= len(self.block_data):
            raise IndexError(
                f"Block coordinate ({x}, {y}) is out of bounds!"
                f"Room size: ({self.width}, {self.height})"
            )
        return self.block_data[idx] | self.block_data[idx + 1] << 8

    def set_block_value(self, x: int, y: int, value: int) -> None:
        idx = (y * self.width + x) * 2
        if idx >= len(self.block_data):
            raise IndexError(
                f"Block coordinate ({x}, {y}) is out of bounds!"
                f"Room size: ({self.width}, {self.height})"
            )
        self.block_data[idx] = value & 0xFF
        self.block_data[idx + 1] = value >> 8

    def write(self) -> None:
        comp_data = comp_rle(self.block_data)
        comp_len = len(comp_data)
        if comp_len > self.comp_len:
            # Repoint data
            addr = self.rom.reserve_free_space(comp_len + 2)
            self.rom.write_ptr(self.pointer, addr)
        else:
            addr = self.rom.read_ptr(self.pointer)
        self.rom.write_8(addr, self.width)
        self.rom.write_8(addr + 1, self.height)
        self.rom.write_bytes(addr + 2, comp_data)
        self.comp_len = comp_len
