"""Rescueable Reploid dataset — the 14 real Reploids, from the disc.

Extraction (2026-08-08 live session + disc census): Reploid objects are
placement records with `minor 0x04`. Of the 33 such records on the disc, the
REAL rescueable Reploids are exactly the `id 0x00, gate 4` ones — proven by
four live rescues across two stages (Izzy records 20/21/22, Skiver 37), each
overlapping its record within ~25px, plus a negative control (an `id 0x11`
record 95px from a real rescue with no NPC present) and a prediction the
data made against the player's own memory (Izzy's third Reploid at x=3432,
which nobody knew was there until the record said so). The remaining 19
records (`id 0x10/0x11` or gates 0-2) never manifest.

NOTE the gate rule is INVERTED relative to pickups: for pickup-class records
gate>=3 means "never spawns"; for Reploids gate 4 marks the real ones. Do
not unify the two rules.

Squid Adler's six are the only ones shipped without an on-screen sighting
(same record shape, contiguous like the others, wiki-corroborated) — a
deliberate accepted risk (Ivor, 2026-08-08): if one turns out conditional we
fix it in a release rather than withholding the stage.

Duff McWhalen's U-555 also releases Reploids, but those are spawned
dynamically by the mid-boss object - no placement records, so no stable
identity, so no locations.

Order is (stage id order, record order) and fixes location ids - append
only, never reorder. Coordinates are the record's spawn point; the client
matches the player's position against them at rescue time.
"""
from . import names

# (stage name, record index in the stage's area-0 list, x, y, location name)
REPLOIDS: list[tuple[str, int, int, int, str]] = [
    (names.KRAKEN, 60, 7728, 432,  f"{names.KRAKEN} - Reploid 1"),
    (names.KRAKEN, 61, 6448, 528,  f"{names.KRAKEN} - Reploid 2"),
    (names.KRAKEN, 62, 6992, 1008, f"{names.KRAKEN} - Reploid 3"),
    (names.KRAKEN, 63, 6768, 1120, f"{names.KRAKEN} - Reploid 4"),
    (names.KRAKEN, 64, 6976, 1216, f"{names.KRAKEN} - Reploid 5"),
    (names.KRAKEN, 65, 7632, 1280, f"{names.KRAKEN} - Reploid 6"),
    (names.FIREFLY, 20, 384,  651, f"{names.FIREFLY} - Reploid 1"),
    (names.FIREFLY, 21, 1776, 248, f"{names.FIREFLY} - Reploid 2"),
    (names.FIREFLY, 22, 3432, 283, f"{names.FIREFLY} - Reploid 3"),
    (names.PEGASUS, 37, 896,  1616, f"{names.PEGASUS} - Reploid 1"),
    (names.PEGASUS, 38, 984,  1616, f"{names.PEGASUS} - Reploid 2"),
    (names.PEGASUS, 39, 3760, 1136, f"{names.PEGASUS} - Reploid 3"),
    (names.PEGASUS, 40, 3888, 1136, f"{names.PEGASUS} - Reploid 4"),
    (names.PEGASUS, 41, 3888, 656,  f"{names.PEGASUS} - Reploid 5"),
]

REPLOID_STAGES = {names.KRAKEN, names.FIREFLY, names.PEGASUS}
