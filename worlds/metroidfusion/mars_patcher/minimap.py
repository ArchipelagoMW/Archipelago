from __future__ import annotations

import json
import os
import pkgutil
from typing import TYPE_CHECKING

from .compress import comp_lz77, decomp_lz77
from .constants.game_data import minimap_ptrs

if TYPE_CHECKING:
    from types import TracebackType

    from .common_types import MinimapId
    from .rom import Rom

MINIMAP_DIM = 32


class Minimap:
    """Class for reading/writing minimap data and setting tiles."""

    def __init__(self, rom: Rom, id: MinimapId):
        self.rom = rom
        self.pointer = minimap_ptrs(rom) + (id * 4)
        addr = rom.read_ptr(self.pointer)
        self.tile_data, self.comp_len = decomp_lz77(rom.data, addr)

    def __enter__(self) -> Minimap:
        # We don't need to do anything
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.write()

    def get_tile_value(self, x: int, y: int) -> tuple[int, int, bool, bool]:
        idx = (y * MINIMAP_DIM + x) * 2
        if idx >= len(self.tile_data):
            raise IndexError(f"Tile coordinate ({x}, {y}) is not within minimap")
        value = self.tile_data[idx] | self.tile_data[idx + 1] << 8
        tile = value & (0x3FF)
        palette = value >> 12
        h_flip = value & 0x400 != 0
        v_flip = value & 0x800 != 0
        return tile, palette, h_flip, v_flip

    def set_tile_value(
        self, x: int, y: int, tile: int, palette: int, h_flip: bool = False, v_flip: bool = False
    ) -> None:
        idx = (y * MINIMAP_DIM + x) * 2
        if idx >= len(self.tile_data):
            raise IndexError(f"Tile coordinate ({x}, {y}) is not within minimap")
        value = tile | (palette << 12)
        if h_flip:
            value |= 0x400
        if v_flip:
            value |= 0x800
        self.tile_data[idx] = value & 0xFF
        self.tile_data[idx + 1] = value >> 8

    def write(self) -> None:
        comp_data = comp_lz77(self.tile_data)
        comp_len = len(comp_data)
        if comp_len > self.comp_len:
            # Repoint data
            addr = self.rom.reserve_free_space(comp_len)
            self.rom.write_ptr(self.pointer, addr)
        else:
            addr = self.rom.read_ptr(self.pointer)
        self.rom.write_bytes(addr, comp_data)
        self.comp_len = comp_len


def apply_minimap_edits(rom: Rom, edit_dict: dict) -> None:
    # Go through every minimap
    for map_id, changes in edit_dict.items():
        with Minimap(rom, int(map_id)) as minimap:
            for change in changes:
                minimap.set_tile_value(
                    change["X"],
                    change["Y"],
                    change["Tile"],
                    change["Palette"],
                    change.get("HFlip", False),
                    change.get("VFlip", False),
                )


def apply_base_minimap_edits(rom: Rom) -> None:
    path = os.path.join("data", "base_minimap_edits.json")
    data = json.loads(pkgutil.get_data(__name__, path).decode())

    # Go through every minimap
    for map in data:
        with Minimap(rom, int(map["MAP_ID"])) as minimap:
            for change in map["CHANGES"]:
                minimap.set_tile_value(
                    change["X"],
                    change["Y"],
                    change["Tile"],
                    change["Palette"],
                    change.get("HFlip", False),
                    change.get("VFlip", False),
                )
