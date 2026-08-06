"""Pickupsanity location data: every freestanding consumable pickup in the game.

Extracted STATICALLY from the disc (2026-08-05) and fully proven - no live
harvesting involved. The derivation chain, all in the static EXE or raw in
ROCK_X5.BIN:

  * overlay loader table  0x8006FD50  u8[stage*2 + area] -> ROCK chunk
  * placement list table  0x80072EAC  u32[stage*8 + area*4] -> list RAM addr
  * every stage module streams to RAM base 0x800EE970, so
        disc_offset = chunk_base + (list_ram - 0x800EE970)
  * list = 8-byte records {flags, minor, id, sub, s16 x, s16 y}, terminator
    sub == 0x0F; minor 0x2F = item; sub & 0x0F = spawn gate, and the spawner
    REJECTS gate >= 3 outright (0x8002AFC0) - gated records never exist.
  * item id -> kind proven from the ctor (0x8005367C): 0x20 small life,
    0x21 large life, 0x22 full life, 0x23/24/25 small/large/full weapon,
    0x26 1-UP.

Validated against the live placement harvest (identical on every stage it
covered), a live-dump anchor for Dark Dizzy area 1 (chunk3) and one for the
X-vs-Zero duel (chunk28). Full account: docs/mmx5-ghidra-findings.md 9.13,
row-level data in docs/mmx5-placements.csv.

LOCATION IDENTITY. Consumable ids are TYPE ids and collide (three Izzy Glow
capsules are all id 0x24), so records are identified by their placement-record
ADDRESS: the spawner stores a pointer to the spawning record into the item
object at +0x10 (sw $s2, 0x10($s1) @ 0x8002B2B8), the pickupsanity stub
copies it into the mailbox record, and the client resolves it through
RECORD_TO_LOCATION below. List bases are static EXE data, so the addresses
are stable for every player on every disc.

INTRO IS DELIBERATELY EXCLUDED. The intro stage cannot be re-entered after
completion, so its single pickup would be a permanently missable location -
the exact class of bug (unreachable check holding progression) this world has
already been bitten by. 32 locations, not 33.
"""
from . import names

# Endgame stage display names (stage ids 0x0C / 0x10 / 0x11). The eight
# Maverick stages use names.STAGES via STAGE_PREFIX below.
SIGMA_STAGE = "Sigma"
ZERO_SPACE_1 = "Zero Space 1"
ZERO_SPACE_2 = "Zero Space 2"

# Spawn-engine stage id (0x800D1C0C) -> location-name prefix. Matches the
# client's STAGE_ID_TO_NAME for the Mavericks; endgame ids from the stage-id
# table in mmx5-ram-notes.md (NOT contiguous: Sigma is BELOW Zero Space).
STAGE_PREFIX = {
    1: names.GRIZZLY, 2: names.NECROBAT, 3: names.WHALE, 4: names.DINOREX,
    5: names.KRAKEN, 6: names.FIREFLY, 7: names.ROSERED, 8: names.PEGASUS,
    0x0C: SIGMA_STAGE, 0x10: ZERO_SPACE_1, 0x11: ZERO_SPACE_2,
}
ENDGAME_STAGE_IDS = frozenset({0x0C, 0x10, 0x11})

# (stage id, area) -> placement list RAM address (primary table 0x80072EAC,
# static EXE data - identical at runtime on every disc, vanilla or patched).
# Only lists that hold pickupsanity locations are needed here.
LIST_BASE = {
    (1, 0): 0x800FBD3C,     # Grizzly Slash
    (2, 0): 0x800F37E0,     # Dark Dizzy
    (2, 1): 0x800F8B4C,
    (3, 0): 0x80100BB0,     # Duff McWhalen
    (4, 0): 0x800F4558,     # Mattrex
    (6, 1): 0x800F9E48,     # Izzy Glow (area 1; area 0 has no consumables)
    (7, 0): 0x800FA618,     # Axle the Red
    (8, 0): 0x800F8C64,     # The Skiver
    (0x0C, 0): 0x80074140,  # Sigma (EXE-resident list)
    (0x10, 0): 0x800F892C,  # Zero Space 1
    (0x11, 0): 0x800FC1E4,  # Zero Space 2
}

# Item id (record id byte) -> human name, proven from the ctor mapping.
PICKUP_TYPE = {
    0x20: "Small Life Energy",
    0x21: "Large Life Energy",
    0x22: "Full Life Energy",
    0x23: "Small Weapon Energy",
    0x24: "Large Weapon Energy",
    0x25: "Full Weapon Energy",
    0x26: "1-UP",
}

# The 32 locations: (stage id, area, record index, item id, location name).
# ORDER IS THE ID LAYOUT (BASE_ID + 200 + position) - append only, never
# reorder. Names number duplicates of the same type within a stage in record
# order.
PICKUPS: list[tuple[int, int, int, int, str]] = [
    (1, 0, 60, 0x21, f"{names.GRIZZLY} - Large Life Energy"),
    (2, 0, 173, 0x21, f"{names.NECROBAT} - Large Life Energy"),
    (2, 1, 12, 0x24, f"{names.NECROBAT} - Large Weapon Energy"),
    (3, 0, 21, 0x21, f"{names.WHALE} - Large Life Energy"),
    (3, 0, 22, 0x20, f"{names.WHALE} - Small Life Energy 1"),
    (3, 0, 23, 0x20, f"{names.WHALE} - Small Life Energy 2"),
    (3, 0, 24, 0x20, f"{names.WHALE} - Small Life Energy 3"),
    (4, 0, 38, 0x21, f"{names.DINOREX} - Large Life Energy"),
    (4, 0, 39, 0x24, f"{names.DINOREX} - Large Weapon Energy"),
    (4, 0, 40, 0x26, f"{names.DINOREX} - 1-UP"),
    (6, 1, 58, 0x24, f"{names.FIREFLY} - Large Weapon Energy 1"),
    (6, 1, 59, 0x24, f"{names.FIREFLY} - Large Weapon Energy 2"),
    (6, 1, 60, 0x21, f"{names.FIREFLY} - Large Life Energy"),
    (6, 1, 61, 0x24, f"{names.FIREFLY} - Large Weapon Energy 3"),
    (7, 0, 109, 0x21, f"{names.ROSERED} - Large Life Energy 1"),
    (7, 0, 110, 0x21, f"{names.ROSERED} - Large Life Energy 2"),
    (8, 0, 86, 0x21, f"{names.PEGASUS} - Large Life Energy"),
    (0x0C, 0, 36, 0x26, f"{SIGMA_STAGE} - 1-UP"),
    (0x0C, 0, 37, 0x21, f"{SIGMA_STAGE} - Large Life Energy 1"),
    (0x0C, 0, 38, 0x21, f"{SIGMA_STAGE} - Large Life Energy 2"),
    (0x0C, 0, 39, 0x21, f"{SIGMA_STAGE} - Large Life Energy 3"),
    (0x0C, 0, 40, 0x22, f"{SIGMA_STAGE} - Full Life Energy 1"),
    (0x0C, 0, 41, 0x22, f"{SIGMA_STAGE} - Full Life Energy 2"),
    (0x0C, 0, 42, 0x25, f"{SIGMA_STAGE} - Full Weapon Energy"),
    (0x0C, 0, 43, 0x22, f"{SIGMA_STAGE} - Full Life Energy 3"),
    (0x10, 0, 69, 0x26, f"{ZERO_SPACE_1} - 1-UP 1"),
    (0x10, 0, 70, 0x26, f"{ZERO_SPACE_1} - 1-UP 2"),
    (0x10, 0, 71, 0x24, f"{ZERO_SPACE_1} - Large Weapon Energy 1"),
    (0x10, 0, 72, 0x24, f"{ZERO_SPACE_1} - Large Weapon Energy 2"),
    (0x11, 0, 78, 0x21, f"{ZERO_SPACE_2} - Large Life Energy"),
    (0x11, 0, 79, 0x22, f"{ZERO_SPACE_2} - Full Life Energy"),
    (0x11, 0, 80, 0x26, f"{ZERO_SPACE_2} - 1-UP"),
]


def record_addr(stage: int, area: int, index: int) -> int:
    """Absolute RAM address of a placement record (the obj+0x10 pointer)."""
    return LIST_BASE[(stage, area)] + index * 8


# What the client resolves a mailbox record pointer against. Unique by
# construction: list bases are distinct addresses and indices are per-list.
RECORD_TO_LOCATION: dict[int, str] = {
    record_addr(stage, area, idx): name
    for stage, area, idx, _iid, name in PICKUPS
}

# For sanity-checking a mailbox record's stage byte against its pointer.
LOCATION_STAGE_ID: dict[str, int] = {
    name: stage for stage, _area, _idx, _iid, name in PICKUPS
}

assert len(RECORD_TO_LOCATION) == len(PICKUPS), "record addresses must be unique"
