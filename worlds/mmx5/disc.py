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
# Pickup check-record stub (patch spec item 2, proto v3): one shared stub in
# EXE free space serves every randomized pickup kind - the dispatcher enters
# handlers via `lw a0,table[kind]; jr a0` with s1 = the item object, so the
# stub reads kind (s1+0x82) and id (s1+2) itself. It appends
# {stage 0x800D1C41, kind, id, seq} to the mailbox ring (16 slots at
# 0x801FA020, monotonic count u32 at 0x801FA080, seq bit7 = record valid) and
# exits through the consume-only tail j 0x800543C8 (li v0,3 = item consumed,
# no vanilla effect - the client owns all grants; the item respawns until the
# server confirms the check, which the client then acks by zeroing seq).
PICKUP_STUB_ADDR = 0x800776A0          # free-space run A (zero in file, canaried)
PICKUP_STUB = bytes.fromhex(
    "1f80083c"  # lui   t0, 0x801F
    "00a00835"  # ori   t0, t0, 0xA000     ; t0 = mailbox 0x801FA000
    "8000098d"  # lw    t1, 0x80(t0)       ; t1 = monotonic pickup count
    "0f002a31"  # andi  t2, t1, 0xF        ; ring slot index
    "80500a00"  # sll   t2, t2, 2
    "21500a01"  # addu  t2, t0, t2
    "0d800b3c"  # lui   t3, 0x800D
    "0c1c6c91"  # lbu   t4, 0x1C0C(t3)     ; stage id (spawn engine's input;
                #   0x1C41 disproven live - read 0xE4 mid-stage)
    "20004ca1"  # sb    t4, 0x20(t2)       ; slot+0: stage
    "82006c92"  # lbu   t4, 0x82(s1)       ; item kind
    "21004ca1"  # sb    t4, 0x21(t2)       ; slot+1: kind
    "02006c92"  # lbu   t4, 0x02(s1)       ; item id
    "22004ca1"  # sb    t4, 0x22(t2)       ; slot+2: id
    "7f002c31"  # andi  t4, t1, 0x7F
    "80008c35"  # ori   t4, t4, 0x80       ; seq = (count & 0x7F) | 0x80
    "23004ca1"  # sb    t4, 0x23(t2)       ; slot+3: seq
    "01002925"  # addiu t1, t1, 1
    "f2500108"  # j     0x800543C8         ; consume item, no vanilla effect
    "800009ad"  # sw    t1, 0x80(t0)       ; (delay slot) commit count
)
RANDOMIZED_KINDS = (0x0, 0x1, 0x9, 0xA, 0xB)  # heart, EX, sub/W/EX-tank

BASE_EDITS: List[Tuple[int, bytes, str]] = [
    (0x8003C324, b"\x4D", "SLUS exe"),
    (0x8003D660, b"\x4D", "SLUS exe"),
    (0x8003D814, b"\x4D", "SLUS exe"),
    (PICKUP_STUB_ADDR, PICKUP_STUB, "SLUS exe"),
] + [
    # Jump-table redirects for the randomized kinds. Base-patch for now;
    # becomes per-seed edits once options can keep kinds vanilla.
    (0x80011068 + kind * 4, PICKUP_STUB_ADDR.to_bytes(4, "little"), "SLUS exe")
    for kind in RANDOMIZED_KINDS
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
