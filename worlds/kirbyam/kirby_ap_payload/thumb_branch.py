"""Shared Thumb branch encoding helpers used by patching and diagnostics."""

from __future__ import annotations


def thumb_bl_bytes(src_rom_addr: int, dst_rom_addr: int) -> bytes:
    """Encode a Thumb-1 BL instruction that branches from src_rom_addr to dst_rom_addr."""
    if src_rom_addr % 2 != 0 or dst_rom_addr % 2 != 0:
        raise SystemExit(
            f"Error: cannot encode Thumb BL from {src_rom_addr:#010x} to {dst_rom_addr:#010x}: "
            "address is not halfword aligned."
        )

    diff = dst_rom_addr - (src_rom_addr + 4)
    if diff % 2 != 0:
        raise SystemExit(
            f"Error: cannot encode Thumb BL from {src_rom_addr:#010x} to {dst_rom_addr:#010x}: "
            "target is not halfword aligned."
        )

    imm = diff >> 1
    if not (-(1 << 21) <= imm < (1 << 21)):
        raise SystemExit(
            f"Error: cannot encode Thumb BL from {src_rom_addr:#010x} to {dst_rom_addr:#010x}: "
            "branch out of range."
        )

    imm &= (1 << 22) - 1
    hi = 0xF000 | ((imm >> 11) & 0x7FF)
    lo = 0xF800 | (imm & 0x7FF)
    return hi.to_bytes(2, "little") + lo.to_bytes(2, "little")


def is_thumb_bl_instruction(opcode: bytes) -> bool:
    """Return True when opcode encodes a 32-bit Thumb BL instruction."""
    if len(opcode) != 4:
        return False
    hi = int.from_bytes(opcode[0:2], "little")
    lo = int.from_bytes(opcode[2:4], "little")
    return (hi & 0xF800) == 0xF000 and (lo & 0xF800) == 0xF800