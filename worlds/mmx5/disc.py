"""Disc model for the Mega Man X5 AP patch (NTSC-U SLUS-01334, Mode2 Form1).

Self-contained: PS1-RAM-address -> raw .bin offset mapping, Mode2 Form1
EDC/ECC regeneration, and the AP basepatch edit list. Everything the patch
does to the image funnels through apply_basepatch() so that parity
regeneration ALWAYS runs last over every touched sector - BizHawk's disc
layer error-corrects un-reparitied edits back to vanilla (workspace
Reference/mmx5-overlay-findings.md §9.0 documents the live failure).

Research provenance for every address lives in the project workspace
(mmx5-overlay-findings.md, mmx5-ram-notes.md); this module only carries
what the shipping patch needs.
"""
from typing import Dict, Iterable, List, Tuple

SECTOR_RAW = 2352
USER_OFF = 24          # Mode2 Form1: 12 sync + 4 header + 8 subheader
USER_LEN = 2048

# (name, ram_start, ram_end_exclusive, first .bin sector, offset of ram_start
# in that sector's user data). SLUS text/data begins at sector 23433 (23432 is
# the 2048-byte PS-EXE header); the results-screen overlay module streams from
# sector 24073 to its EXE-descriptor dest 0x800EE970.
REGIONS: List[Tuple[str, int, int, int, int]] = [
    ("SLUS exe", 0x80010000, 0x80092000, 23433, 0),
    ("results overlay", 0x800EE970, 0x800F9000, 24073, 0),
]


def addr_to_disc(addr: int, region_name: str) -> int:
    """PS1 RAM address -> raw .bin byte offset (single byte; callers iterate)."""
    for name, lo, hi, sec0, off0 in REGIONS:
        if name == region_name and lo <= addr < hi:
            delta = addr - lo + off0
            sec = sec0 + delta // USER_LEN
            return sec * SECTOR_RAW + USER_OFF + delta % USER_LEN
    raise ValueError(f"no region {region_name!r} maps RAM 0x{addr:08X}")


# ---- AP basepatch edit list -------------------------------------------------
# NOTE: do NOT suppress the results-overlay weapon commit (0x800EECCC): story
# chapters advance on popcount(0x800D1C4C) - killing the commit softlocks the
# endgame. 0x1C4C stays the game-written kill record; randomization decouples
# the CAPABILITY readers instead.
#
# Weapon capability decoupling: the three stage-load repopulation sites read
# save weapons 0x1C4C into the live player struct. Changing each lbu's offset
# byte 0x4C -> 0x4D derives capability from 0x800D1C4D (unused save byte,
# memory-card-persisted) = the AP-owned weapons byte the client writes.
BASE_EDITS: List[Tuple[int, bytes, str]] = [
    (0x8003C324, b"\x4D", "SLUS exe"),
    (0x8003D660, b"\x4D", "SLUS exe"),
    (0x8003D814, b"\x4D", "SLUS exe"),
]


# ---- Mode2 Form1 EDC/ECC (Corlett ecm-style tables) --------------------------
_ecc_f = [0] * 256
_ecc_b = [0] * 256
_edc = [0] * 256
for _i in range(256):
    _j = ((_i << 1) ^ (0x11D if (_i & 0x80) else 0)) & 0xFF
    _ecc_f[_i] = _j
    _ecc_b[_i ^ _j] = _i
    _e = _i
    for _ in range(8):
        _e = (_e >> 1) ^ (0xD8018001 if (_e & 1) else 0)
    _edc[_i] = _e


def _edc_compute(data: bytes) -> int:
    edc = 0
    for b in data:
        edc = (edc >> 8) ^ _edc[(edc ^ b) & 0xFF]
    return edc


def _ecc_block(sec: bytearray, major_count: int, minor_count: int,
               major_mult: int, minor_inc: int, dest: int) -> None:
    size = major_count * minor_count
    for major in range(major_count):
        index = (major >> 1) * major_mult + (major & 1)
        ecc_a = 0
        ecc_b = 0
        for _ in range(minor_count):
            temp = 0 if index < 4 else sec[0xC + index]  # header zeroed (Mode 2)
            index += minor_inc
            if index >= size:
                index -= size
            ecc_a ^= temp
            ecc_b ^= temp
            ecc_a = _ecc_f[ecc_a]
        ecc_a = _ecc_b[_ecc_f[ecc_a] ^ ecc_b]
        sec[dest + major] = ecc_a
        sec[dest + major + major_count] = ecc_a ^ ecc_b


def regenerate_sector(image: bytearray, sector: int) -> None:
    base = sector * SECTOR_RAW
    sec = bytearray(image[base:base + SECTOR_RAW])
    if sec[15] != 2 or (sec[18] & 0x20):
        raise ValueError(f"sector {sector} is not Mode2 Form1")
    edc = _edc_compute(bytes(sec[0x10:0x818]))
    sec[0x818:0x81C] = edc.to_bytes(4, "little")
    _ecc_block(sec, 86, 24, 2, 86, 0x81C)    # P parity
    _ecc_block(sec, 52, 43, 86, 88, 0x8C8)   # Q parity
    image[base:base + SECTOR_RAW] = sec


def apply_basepatch(rom: bytes, extra_edits: Iterable[Tuple[int, bytes, str]] = ()) -> bytes:
    """Apply BASE_EDITS (+ per-seed extras), then regenerate EDC/ECC for every
    touched sector. The single funnel for all image modification."""
    image = bytearray(rom)
    touched: Dict[int, None] = {}
    for addr, payload, region in list(BASE_EDITS) + list(extra_edits):
        for i, b in enumerate(payload):
            off = addr_to_disc(addr + i, region)
            image[off] = b
            touched[off // SECTOR_RAW] = None
    for sector in sorted(touched):
        regenerate_sector(image, sector)
    return bytes(image)
