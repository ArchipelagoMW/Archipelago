"""Disc model for the Mega Man X5 AP patch (NTSC-U SLUS-01334, Mode2 Form1).

Self-contained: PS1-RAM-address -> raw .bin offset mapping, Mode2 Form1
EDC/ECC regeneration, and the AP basepatch edit list. Everything the patch
does to the image funnels through apply_basepatch() so that parity
regeneration ALWAYS runs last over every touched sector - BizHawk's disc
layer error-corrects un-reparitied edits back to vanilla
(mmx5-overlay-findings.md §9.0 documents the live failure).

Research provenance for every address lives in the project's research notes
(mmx5-overlay-findings.md, mmx5-ram-notes.md - found in worlds/mmx5/docs/ on
the author's fork: github.com/Shinnuu/Archipelago, branch mmx5-apworld); this
module only carries what the shipping patch needs.
"""
from collections.abc import Iterable

SECTOR_RAW = 2352
USER_OFF = 24          # Mode2 Form1: 12 sync + 4 header + 8 subheader
USER_LEN = 2048

# (name, ram_start, ram_end_exclusive, first .bin sector, offset of ram_start
# in that sector's user data). SLUS text/data begins at sector 23433 (23432 is
# the 2048-byte PS-EXE header); the results-screen overlay module streams from
# sector 24073 to its EXE-descriptor dest 0x800EE970.
REGIONS: list[tuple[str, int, int, int, int]] = [
    ("SLUS exe", 0x80010000, 0x80092000, 23433, 0),
    ("results overlay", 0x800EE970, 0x800F9000, 24073, 0),
    # Launch cutscene module: resolution fn's only on-disc copy; mapping
    # disc-scan verified (RAM 0x800FA000 = sector 24319 user offset 0).
    ("launch overlay", 0x800FA000, 0x800FB000, 24319, 0),
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
# v7: R3000 LOAD-DELAY-SLOT SAFE. A loaded value is not available to the
# very next instruction on the PS1 CPU; the v3..v6 stubs did lbu/sb pairs
# back-to-back and recorded every field one store late (live-diagnosed via
# the s1 capture). Loads now interleave through t4/t5/t6 with their first
# uses at least one instruction away - same layout the game's own compiled
# code achieves with explicit NOPs (see the dispatcher's lbu; nop; sltiu).
PICKUP_STUB = bytes.fromhex(
    "1f80083c"  # lui   t0, 0x801F
    "00a00835"  # ori   t0, t0, 0xA000     ; t0 = mailbox 0x801FA000
    "8000098d"  # lw    t1, 0x80(t0)       ; t1 = monotonic pickup count
    "0d800b3c"  # lui   t3, 0x800D         ; (fills t1's load delay slot)
    "0f002a31"  # andi  t2, t1, 0xF        ; ring slot index
    "80500a00"  # sll   t2, t2, 2
    "21500a01"  # addu  t2, t0, t2         ; t2 = mailbox + slot*4
    "0c1c6c91"  # lbu   t4, 0x1C0C(t3)     ; stage id (spawn engine's input)
    "82002d92"  # lbu   t5, 0x82(s1)       ; item kind (fills t4's delay)
    "02002e92"  # lbu   t6, 0x02(s1)       ; item id   (fills t5's delay)
    "20004ca1"  # sb    t4, 0x20(t2)       ; slot+0: stage
    "21004da1"  # sb    t5, 0x21(t2)       ; slot+1: kind
    "22004ea1"  # sb    t6, 0x22(t2)       ; slot+2: id
    "7f002c31"  # andi  t4, t1, 0x7F
    "80008c35"  # ori   t4, t4, 0x80       ; seq = (count & 0x7F) | 0x80
    "23004ca1"  # sb    t4, 0x23(t2)       ; slot+3: seq
    # Since disc rev 11: the debug s1-capture (`sw s1,0xA0(t2)`) that sat
    # here is STRIPPED. (Current disc revision is 12 - the tank fix.)
    # It mirrored the item object pointer into 0x801FA0A0+slot*4 solely so the
    # research Lua could dump object headers; nothing in the client read it,
    # and the capsule stub never wrote it - which is why capsule records
    # logged "captured s1 = 00000000". Stub is now 19 words / 76 bytes and its
    # tail sits at +0x48 instead of +0x4C.
    "01002925"  # addiu t1, t1, 1
    "f2500108"  # j     0x800543C8         ; consume item, no vanilla effect
    "800009ad"  # sw    t1, 0x80(t0)       ; (delay slot) commit count
)
RANDOMIZED_KINDS = (0x0, 0x1, 0x9, 0xA, 0xB)  # heart, EX, sub/W/EX-tank

# Armor-capsule check-record stub (patch spec item 6, proto v9). The capsule
# grant fn (static EXE, s1 = capsule object, id at s1+2) splits at 0x80055D60:
# id 8 (Zero-space Ultimate/Black-Zero capsule, not a location) keeps its
# vanilla path; ids 0-7 reach the parts RMW `lbu/or/sb 0xA1(a1)` at
# 0x80055DB8-DC8 and rejoin at 0x80055DCC (state advance + epilogue, all
# t-regs dead). The hook replaces the RMW head with `j stub; nop`; the stub
# appends {stage, kind 0x20 (synthetic - real dispatcher kinds stop well
# below), id, seq} to the same mailbox ring and rejoins - grant suppressed,
# capsule dialog untouched. Suppressed capsules re-record on revisit; the
# client de-dupes and maps stage -> capsule location.
CAPSULE_STUB_ADDR = 0x80077700         # free-space run A, after the pickup stub
CAPSULE_STUB = bytes.fromhex(
    "1f80083c"  # lui   t0, 0x801F
    "00a00835"  # ori   t0, t0, 0xA000     ; t0 = mailbox 0x801FA000
    "8000098d"  # lw    t1, 0x80(t0)       ; t1 = monotonic pickup count
    "0d800b3c"  # lui   t3, 0x800D         ; (fills t1's load delay slot)
    "0f002a31"  # andi  t2, t1, 0xF        ; ring slot index
    "80500a00"  # sll   t2, t2, 2
    "21500a01"  # addu  t2, t0, t2         ; t2 = mailbox + slot*4
    "0c1c6c91"  # lbu   t4, 0x1C0C(t3)     ; stage id (spawn engine's input)
    "02002e92"  # lbu   t6, 0x02(s1)       ; capsule id (fills t4's delay)
    "20000d24"  # addiu t5, zero, 0x20     ; kind 0x20 (ALU, fills t6's delay)
    "20004ca1"  # sb    t4, 0x20(t2)       ; slot+0: stage
    "21004da1"  # sb    t5, 0x21(t2)       ; slot+1: kind
    "22004ea1"  # sb    t6, 0x22(t2)       ; slot+2: id
    "7f002c31"  # andi  t4, t1, 0x7F
    "80008c35"  # ori   t4, t4, 0x80       ; seq = (count & 0x7F) | 0x80
    "23004ca1"  # sb    t4, 0x23(t2)       ; slot+3: seq
    "01002925"  # addiu t1, t1, 1
    "73570108"  # j     0x80055DCC         ; rejoin: state advance + return
    "800009ad"  # sw    t1, 0x80(t0)       ; (delay slot) commit count
)

BASE_EDITS: list[tuple[int, bytes, str]] = [
    (0x8003C324, b"\x4D", "SLUS exe"),
    (0x8003D660, b"\x4D", "SLUS exe"),
    (0x8003D814, b"\x4D", "SLUS exe"),
    (PICKUP_STUB_ADDR, PICKUP_STUB, "SLUS exe"),
] + [
    # Jump-table redirects for the randomized kinds. Base-patch for now;
    # becomes per-seed edits once options can keep kinds vanilla.
    (0x80011068 + kind * 4, PICKUP_STUB_ADDR.to_bytes(4, "little"), "SLUS exe")
    for kind in RANDOMIZED_KINDS
] + [
    # Armor-capsule hook (spec item 6): stub, grant-RMW-head redirect, and
    # the spawn-gate retarget (id!=8 branch at 0x80055018 jumps past the
    # despawn ladder to its JOIN 0x80055130, where a3=0 from the prologue
    # takes the spawn branch) so an AP-GRANTED armor part can never despawn
    # an unchecked capsule (missable-check hazard). NOT 0x80055148 directly
    # (the v10 fix for the v9 area-entry freeze): the join beq's delay slot
    # `addiu a0,zero,0x86` feeds the spawn path's jal at 0x8005518C -
    # skipping it passes the capsule object pointer as a0 and the game
    # hangs when the capsule spawns.
    (CAPSULE_STUB_ADDR, CAPSULE_STUB, "SLUS exe"),
    (0x80055DB8, bytes.fromhex("c0dd010800000000"), "SLUS exe"),  # j stub; nop
    (0x80055018, bytes.fromhex("4500c214"), "SLUS exe"),          # bne -> join
] + [
    # Tank already-owned despawn (disasm + live capture 2026-08-03). The item
    # init 0x800535C8 tests "do I already own this?" per kind and, when the
    # answer is yes, writes 3 to obj+0x04 which destroys the object one frame
    # after construction. The AP client grants tanks by setting exactly those
    # ownership bits (that is what shows a tank in the pause menu), so a tank
    # arriving from the multiworld DELETED the pickup that is its own check -
    # permanently, and those locations can hold progression.
    # Measured in Grizzly Slash, one pass: consumable object lived 251
    # frames, an un-owned Heart Tank 47, the OWNED Sub-Tank exactly 2.
    # Zeroing the three per-kind masks defeats the test for tanks only;
    # hearts (kind 0), EX items (kind 1) and consumables are untouched, and
    # hearts never needed it because the client grants those via max HP.
    # The client reads TANK_FIX_PROBE_ADDR to tell a fixed disc from an old
    # one and only applies its own workaround when this patch is absent.
    (0x80053804, (0x24020000).to_bytes(4, "little"), "SLUS exe"),  # sub-tanks
    (0x80053838, (0x30420000).to_bytes(4, "little"), "SLUS exe"),  # W-Tank
    (0x80053848, (0x30420000).to_bytes(4, "little"), "SLUS exe"),  # EX-Tank
] + [
    # Launch determinism (research overlay-findings 11): the resolution
    # roll `andi v1,v0,0xF` -> `li v1,0`; success <=> score > 0, and the
    # client owns the score bytes (pinned each cycle from AP part items).
    # Never ship this word without the client's score pinning.
    (0x800FA0D4, (0x24030000).to_bytes(4, "little"), "launch overlay"),
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


def apply_basepatch(rom: bytes, extra_edits: Iterable[tuple[int, bytes, str]] = ()) -> bytes:
    """Apply BASE_EDITS (+ per-seed extras), then regenerate EDC/ECC for every
    touched sector. The single funnel for all image modification."""
    image = bytearray(rom)
    touched: dict[int, None] = {}
    for addr, payload, region in list(BASE_EDITS) + list(extra_edits):
        for i, b in enumerate(payload):
            off = addr_to_disc(addr + i, region)
            image[off] = b
            touched[off // SECTOR_RAW] = None
    for sector in sorted(touched):
        regenerate_sector(image, sector)
    return bytes(image)
