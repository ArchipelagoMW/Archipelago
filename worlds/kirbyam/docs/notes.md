\# Kirby \& The Amazing Mirror (GBA) — Archipelago Setup (Work-in-Progress)



This integration is currently implemented as a \*\*BizHawk client + ROM patch memory contract\*\*.



\- The \*\*Python world\*\* is stable for seed generation.

\- The \*\*ROM patch\*\* is responsible for implementing the RAM protocol described below.

\- No seed-specific ROM patching is required yet; all randomization is mediated via RAM.



This document describes the \*\*minimum contract required for a playable game\*\*.



---



\## BizHawk requirements



\- BizHawk 2.x

\- `connector\_bizhawk\_generic.lua` (standard Archipelago BizHawk connector)



All memory access uses the \*\*System Bus\*\* domain.



---



\## Memory contract (EWRAM, System Bus)



All Archipelago-related RAM is located in \*\*EWRAM starting at `0x0202C000`\*\*.



Addresses are defined in: `worlds/kirbyam/data/addresses.json`



The ROM patch must treat this region as \*\*reserved and owned by Archipelago\*\*.



\### AP EWRAM layout



Base address: \*\*`0x0202C000`\*\*



| Address | Size | Name | Description |

|------|------|------|-------------|

| `0x0202C000` | u32 | `shard\_bitfield` | Location check bitfield |

| `0x0202C004` | u32 | `incoming\_item\_flag` | Incoming item mailbox flag |

| `0x0202C008` | u32 | `incoming\_item\_id` | Incoming AP item id |

| `0x0202C00C` | u32 | `incoming\_item\_player` | Sender slot id |



All values are \*\*little-endian 32-bit integers\*\*.



---



\## Location checks



\### `shard\_bitfield` (u32)



\- Each bit represents whether a location has been checked.

\- Bits are \*\*monotonic\*\* (once set, never cleared).



Current proof-of-concept mapping:



\- bit 0 → `SHARD\_1` location checked

\- bit 1 → `SHARD\_2` location checked

\- …

\- bit 7 → `SHARD\_8` location checked



\*\*Client behavior:\*\*

\- Polls `shard\_bitfield` each tick.

\- When a new bit transitions from `0 → 1`, sends a `LocationChecks` message to the server.



\*\*ROM behavior:\*\*

\- When the player completes a shard location, set the corresponding bit.

\- Bits should only ever be set, never cleared.



---



\## Incoming item mailbox



This is a \*\*single-slot mailbox\*\* used to deliver AP items from the client to the ROM.



\### Fields



\- `incoming\_item\_flag` (u32)

&nbsp; - `0` = mailbox empty (client may write)

&nbsp; - `1` = mailbox full (ROM must consume)

\- `incoming\_item\_id` (u32)

&nbsp; - AP item id (world-defined; opaque to the ROM except for effect mapping)

\- `incoming\_item\_player` (u32)

&nbsp; - Slot id of the sending player (informational; optional to use)



\### Client behavior



\- Maintains a local queue of newly received AP items.

\- When `incoming\_item\_flag == 0`:

&nbsp; 1. Writes `incoming\_item\_id`

&nbsp; 2. Writes `incoming\_item\_player`

&nbsp; 3. Sets `incoming\_item\_flag = 1`

\- Does not overwrite the mailbox while the flag is `1`.



\### ROM behavior (implemented in the base patch)



\- Poll `incoming\_item\_flag` periodically (e.g., once per frame).

\- When `incoming\_item\_flag == 1`:

&nbsp; 1. Read `incoming\_item\_id` (and optionally `incoming\_item\_player`)

&nbsp; 2. Grant the item’s in-game effect

&nbsp; 3. Clear `incoming\_item\_flag` back to `0`



For initial playability, item effects may be implemented in a minimal or placeholder manner (e.g., shard items directly advancing shard progress).



---



\## Notes



\- This RAM contract is intentionally minimal and designed for early playability.

\- Future revisions may replace the single-slot mailbox with a ring buffer or add save persistence.

\- All addresses may be relocated if conflicts with game memory are discovered, but must remain consistent between ROM patch and client.



